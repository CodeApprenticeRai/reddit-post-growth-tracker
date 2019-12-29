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
record_submission_statistics_sql_string = "INSERT INTO submission_records VALUES (?, ?, ?, ?, ?) "


'''
*Get all subscribed_subreddits from the database
::For each sub_reddit in this collection:
*Get all the new submissions to this sub_reddit and add them to the database of
subscribed submissions
'''
def register_new_submissions():
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
def record_submission_statistics():
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


if __name__ == "__main__":
    counter=1

    while True:
        print("-"*10 + "Loop {}".format(counter) + "-"*10)
        execution_time = time.time()
        register_new_submissions()
        execution_time = time.time() - execution_time

        print("register_new_submissions compeleted: {} s".format(execution_time))

        execution_time = time.time()
        record_submission_statistics()
        execution_time = time.time() - execution_time

        print("record_submission_statistics completed: {} s".format(execution_time))

        counter+=1
        time.sleep(30)
