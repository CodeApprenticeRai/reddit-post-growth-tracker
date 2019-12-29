from flask import Flask, g, request, jsonify
import sqlite3
import json
import praw
import time

app = Flask(__name__)


DATABASE_PATH = "./db/data.db"
reddit_client = None

with open('config.json') as config:
    config = json.load(config)
    reddit_client = praw.Reddit(
        client_id=config["client_id"],
        client_secret=config["client_secret"],
        user_agent=config["user_agent"]
    )

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_PATH)
    return db

# def query_db(query, args=(), one=False):
#     cursor = get_db().execute(query, args)
#     results = cur.fetchall()
#     cursor.close()
#     return results


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/subscribe', methods=['POST'])
# post (id, name) to subcribed_subreddits table
def subscribe_to_subreddit():
    if request.method == 'POST':
        request_body = request.json

        response = {
        "success": False,
        "message" :""
        }

        if ( 'subreddit_name' in request_body ):
            subreddit_name = request_body["subreddit_name"]

            subreddit = reddit_client.subreddit(subreddit_name)
            subreddit_id = None

            try:
                subreddit_id = subreddit.id
            except:
                response["message"] = "invalid_subreddit_name"
                return jsonify(response)

            # !! DB interaction can be modularized
            db_connection = get_db()
            cursor = db_connection.cursor()

            try:
                insert_into_subscribed_subreddts_table_sql_string = "INSERT INTO subscribed_subreddits VALUES ( ?, ? )"
                cursor.execute(insert_into_subscribed_subreddts_table_sql_string, [subreddit_id, subreddit_name] )
                db_connection.commit()

            except sqlite3.Error as error:
                response["message"] = "database insert error. May already be subscribed to this subreddit."
                return jsonify(response)

            response["success"] = True

        else:
            response["message"] = "subreddit_name must be specified"

        return jsonify(response)


'''
    Helpers for get_subreddit_submission_time_series()
'''
# Helper 1
def get_subscribed_subreddits():
    db_connection = get_db()
    cursor = db_connection.cursor()
    get_subscribed_subreddits_sql_string = "SELECT subreddit_title FROM subscribed_subreddits"
    cursor.execute( get_subscribed_subreddits_sql_string )
    subreddits = [ row[0] for row in cursor.fetchall() ]
    return subreddits

# Helper 2
def get_subscribed_subreddit_submissions( subreddit_name ):
    db_connection = get_db()
    get_subscribed_submissions_sql_string = "SELECT id,submission_title from subscribed_submissions where subreddit_title=?"
    cursor = db_connection.cursor()
    cursor.execute( get_subscribed_submissions_sql_string, [subreddit_name] )
    return cursor.fetchall()

# Helper 3
def get_subscribed_subreddit_submission_ids( subreddit_name ):
    db_connection = get_db()
    get_subscribed_submissions_id_sql_string = "SELECT id from subscribed_submissions where subreddit_title=?"
    cursor = db_connection.cursor()
    cursor.execute( get_subscribed_submissions_id_sql_string, [subreddit_name] )
    submission_ids  = [ row[0] for row in  cursor.fetchall() ]
    return submission_ids

# Helper 4
def get_submission_recorded_statistics( submission_id ):
    db_connection = get_db()
    get_submission_recorded_statistics_sql_string = "select * from submission_records where id=? ORDER BY time DESC;"
    cursor = db_connection.cursor()
    cursor.execute( get_submission_recorded_statistics_sql_string, [submission_id] )
    return cursor.fetchall()


'''
    returns:

    a dict of subreddits_names
        each subreddit has a dict of submissions
        each submission has a time_series of it's recorded historical values
'''
@app.route('/subreddits', methods=["GET"])
def get_subreddit_submission_time_series(): # bad function name
    # for each subreddit in the database ( get subreddits from database )
    print("Recieved GET request for /subreddits")
    execution_time = time.time()
    subscribed_subreddits = { subreddit_name : {} for subreddit_name in  get_subscribed_subreddits() }

    # for each submission under subreddit ( get submission under subreddit )
    for subreddit_name in subscribed_subreddits:

        submissions = get_subscribed_subreddit_submissions( subreddit_name )
        subscribed_subreddits[ subreddit_name ]["submissions"] = { submission[0] : { "title": submission[1] }  for submission in submissions }

        for submission_id in subscribed_subreddits[ subreddit_name ]["submissions"]:
            subscribed_subreddits[ subreddit_name ]["submissions"][ submission_id ][ "data" ] = get_submission_recorded_statistics( submission_id )

    execution_time = time.time() - execution_time
    print("GET /subreddits fulfilled: {} s".format( execution_time ))
    return jsonify(subscribed_subreddits)
