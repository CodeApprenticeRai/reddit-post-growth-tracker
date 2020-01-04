import json
import praw
import sqlite3
import sys
import time

db_connection = sqlite3.connect("./db/data.db")


reddit_client = None

with open('config.json') as config:
    config = json.load(config)
    reddit_client = praw.Reddit(
        client_id=config["client_id"],
        client_secret=config["client_secret"],
        user_agent=config["user_agent"]
    )

get_subscribed_subreddits_sql_string = "SELECT subreddit_title FROM subscribed_subreddits"
subscribe_to_new_submissions_sql_string = "INSERT or IGNORE INTO subscribed_submissions VALUES (?, ?, ?)"

get_subscribed_submissions_sql_string = "SELECT id from subscribed_submissions"
record_submission_statistics_sql_string = "INSERT or IGNORE INTO submission_records VALUES (?, ?, ?, ?, ?) "


'''
*Get all subscribed_subreddits from the database
::For each sub_reddit in this collection:
*Get all the new submissions to this sub_reddit and add them to the database of
subscribed submissions
'''
def register_new_submissions(db_connection):
    cursor = db_connection.cursor()
    cursor.execute( get_subscribed_subreddits_sql_string )
    subreddit_rows = cursor.fetchall()

    for subreddit_row in subreddit_rows:
        # get subreddit instance
        subreddit = reddit_client.subreddit(subreddit_row[0])


        rows_to_insert = []

        for submission in subreddit.new():
            row = ( submission.id, subreddit.display_name, submission.title )
            rows_to_insert.append( row )

        # push posts to subscribed_posts table ( ignoring any unique constraint errors and perhaps in the future avoiding trying to update existing posts anyway )
        cursor.executemany( subscribe_to_new_submissions_sql_string, rows_to_insert )
        db_connection.commit()
    return None


'''
*for every submission subscribed to, get the ( time, submission_id, score, upvote_ratio )
and store it in submission_records table
'''
def record_submission_statistics(db_connection):
    cursor = db_connection.cursor()
    cursor.execute( get_subscribed_submissions_sql_string )
    subreddit_rows = cursor.fetchall()

    rows_to_insert = []
    for subreddit_row in subreddit_rows:
        submission = reddit_client.submission(id=subreddit_row[0])

        current_time = int( time.time() / 60 ) * 60 # rounded back to the nearest minute
        row = ( current_time, submission.id, submission.score, submission.ups, submission.downs )

        rows_to_insert.append( row )


    cursor.executemany( record_submission_statistics_sql_string, rows_to_insert )
    db_connection.commit()
    return None


'''
    Helpers for get_subreddit_submission_time_series()
'''
# Helper 1
def get_subscribed_subreddits(db_connection):
    cursor = db_connection.cursor()
    get_subscribed_subreddits_sql_string = "SELECT subreddit_title FROM subscribed_subreddits"
    cursor.execute( get_subscribed_subreddits_sql_string )
    subreddits = [ row[0] for row in cursor.fetchall() ]
    return subreddits

# Helper 2
def get_subscribed_subreddit_submissions( db_connection, subreddit_name ):
    get_subscribed_submissions_sql_string = "SELECT id,submission_title from subscribed_submissions where subreddit_title=?"
    cursor = db_connection.cursor()
    cursor.execute( get_subscribed_submissions_sql_string, [subreddit_name] )
    return cursor.fetchall()

# Helper 3
def get_subscribed_subreddit_submission_ids( db_connection, subreddit_name ):
    get_subscribed_submissions_id_sql_string = "SELECT id from subscribed_submissions where subreddit_title=?"
    cursor = db_connection.cursor()
    cursor.execute( get_subscribed_submissions_id_sql_string, [subreddit_name] )
    submission_ids  = [ row[0] for row in  cursor.fetchall() ]
    return submission_ids

# Helper 4
def get_submission_recorded_statistics( db_connection, submission_id ):
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
def get_subreddit_submission_time_series(db_connection, number_of_submissions=-1): # bad function name
    # for each subreddit in the database ( get subreddits from database )
    subscribed_subreddits = { subreddit_name : {} for subreddit_name in  get_subscribed_subreddits(db_connection) }

    # for each submission under subreddit ( get submission under subreddit )
    for subreddit_name in subscribed_subreddits:
        submissions = get_subscribed_subreddit_submissions( db_connection, subreddit_name )

        number_of_submissions = len(submissions) if (number_of_submissions == -1) else number_of_submissions

        subscribed_subreddits[ subreddit_name ]["submissions"] = { submission[0] : { "title": submission[1] }  for submission in submissions[: number_of_submissions] }

        for submission_id in subscribed_subreddits[ subreddit_name ]["submissions"]:
            submission_time_series = get_submission_recorded_statistics( db_connection, submission_id )
            formatted_jsonified_time_series = [
                {
                    "time": row[0],
                    "id": row[1],
                    "score": row[2],
                    "upvotes": row[3],
                    "downvotes": row[4]
                } for row in submission_time_series
            ]
            subscribed_subreddits[ subreddit_name ]["submissions"][ submission_id ][ "data" ] = formatted_jsonified_time_series

    return subscribed_subreddits


if __name__ == "__main__":
    counter=1

    while True:
        loop_execution_time = 0
        print("-"*10 + "Loop {}".format(counter) + "-"*10)
        execution_time = time.time()
        register_new_submissions(db_connection)
        execution_time = time.time() - execution_time
        loop_execution_time += execution_time

        print("register_new_submissions compeleted: {} s".format(execution_time))

        execution_time = time.time()
        record_submission_statistics(db_connection)
        execution_time = time.time() - execution_time
        loop_execution_time += execution_time

        print("record_submission_statistics completed: {} s".format(execution_time))

        time.sleep( max(0, 60 - loop_execution_time) )
        counter+=1
