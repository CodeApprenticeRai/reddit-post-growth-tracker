from flask import Flask, g, request, jsonify
from flask_cors import CORS
import sqlite3
import json
import praw
import time
import os
import controls

app = Flask(__name__)
CORS(app)


DATABASE_PATH = "./db/data.db"
reddit_client = None
SUBREDDITS_CACHE = None

with open('config.json') as config:
    config = json.load(config)
    reddit_client = praw.Reddit(
        client_id=config["client_id"],
        client_secret=config["client_secret"],
        user_agent=config["user_agent"]
    )


if os.path.exists('subreddits_cache.json'):
    with open('subreddits_cache.json') as subreddits_cache:
        SUBREDDITS_CACHE = json.load(subreddits_cache)

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
    returns:

    a dict of subreddits_names
        each subreddit has a dict of submissions
        each submission has a time_series of it's recorded historical values
'''
# @app.route('/subreddits', methods=["GET"])
# def get_subreddit_submission_time_series_request_handler(): # bad function name
#     if os.path.exists('subreddits_cache.json'):
#         with open('subreddits_cache.json') as subreddits_cache:
#             SUBREDDITS_CACHE = json.load(subreddits_cache)
#             subscribed_subreddits = SUBREDDITS_CACHE
#     else:
#         # for each subreddit in the database ( get subreddits from database )
#         subscribed_subreddits = controls.get_subreddit_submission_time_series()
#
#         SUBREDDITS_CACHE = subcribed_subreddits
#
#         with open('subreddits_cache.json', 'w') as subreddits_cache:
#             json.dump(SUBREDDITS_CACHE, subreddits_cache)
#
#     return jsonify(subscribed_subreddits)

@app.route('/developmental/get_subreddit_submissions/<int:number_of_submissions>', methods=["GET"])
def get_subreddit_submission_time_series_request_handler_test(number_of_submissions): # bad function name
    subscribed_subreddits = controls.get_subreddit_submission_time_series( get_db(), number_of_submissions )

    return jsonify(subscribed_subreddits)
