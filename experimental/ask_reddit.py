'''
AskReddit is a high volume subreddit.
A batch of many new questions are posted,
all day, everyday.
There a good bit of variation between posts too.

Reddit doesn't let you visualize the growth of
these posts, and so it'd be cool to see the different
classes of posts based on how they grow.

Spec:
* Register every new submission as soon as it is posted ( check every 30 seconds, or if possible be notified )
* Every 30s for every registered submission record it's stats at the current time
* allow for posts to be queried based on this info:
    * show a graph of all posts

That's it. Just being able to see the growth curves of new posts.
Being able to see what's on people's minds.
'''

import sqlite3
import json
import praw
import time
import os
import threading


# non-blocking function scheduler
# credit: https://stackoverflow.com/a/48709380/6318046
class setInterval:
    def __init__(self, action, interval) :
        self.interval = interval
        self.action = action
        self.stop_event = threading.Event()
        thread= threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self):
        nextTime = time.time() + self.interval
        while not self.stop_event.wait(nextTime-time.time()) :
            nextTime+=self.interval
            self.action()

    def cancel(self) :
        self.stop_event.set()

class App:
    def __init__(self):
        self.DATABASE_PATH = "./data.db"
        self.reddit_client = self.get_reddit_client()
        self.db_connection = self.get_db_connection()
        setInterval( self.register_new_submissions, 30)
        setInterval( self.record_submissions_statistics, 60)
        return None

    '''
    Load reddit praw client
    '''
    def get_reddit_client(self):
        try:
            with open('../config.json') as config:
                config = json.load(config)
                reddit_client = praw.Reddit(
                    client_id=config["client_id"],
                    client_secret=config["client_secret"],
                    user_agent=config["user_agent"]
                )
                return reddit_client
        except:
            raise FileNotFoundError("Couldn't find config file necessary to load PRAW configuration.")


    '''
    Create tables: (submissions, submisison_records) if not
    exists, returns db_connection

    submissions: for recording which posts we are growth-monitoring,
    submisison_records: for recording submission stats at a given time
    '''
    def get_db_connection(self):
        db_connection = sqlite3.connect("./data.db")

        create_subscribed_submissions_table_sql_string = "CREATE TABLE IF NOT EXISTS submissions ( id TEXT PRIMARY KEY, submission_title TEXT, created_utc INTEGER NOT NULL );"
        create_submission_records_table_sql_string = "CREATE TABLE IF NOT EXISTS submission_records ( time INTEGER NOT NULL, submission_id TEXT NOT NULL, upvotes INTEGER NOT NULL, downvotes INTEGER NOT NULL, num_comments INTEGER NOT NULL, PRIMARY KEY (time, submission_id) );"

        cursor = db_connection.cursor()
        cursor.execute( create_subscribed_submissions_table_sql_string )
        cursor.execute( create_submission_records_table_sql_string )

        db_connection.commit()
        return db_connection


    '''
    * Register every new submission as soon as it is posted
    '''
    def register_new_submissions(self):
        register_new_submission_sql_string = "INSERT or IGNORE INTO submissions VALUES (?, ?, ?)"
        new_rows_to_insert = []
        subreddit = self.reddit_client.subreddit('AskReddit')
        for submission in subreddit.new():
            new_submission = ( submission.id, submission.title, submission.created_utc )
            new_rows_to_insert.append( new_submission )

        cursor = self.db_connection.cursor()
        cursor.executemany( register_new_submission_sql_string, new_rows_to_insert )
        self.db_connection.commit()
        return None

    '''
    * For every registered submission: record current (upvotes, downvotes, num_comments)
    '''
    def record_submissions_statistics(self):
        self.zero_time = time.time()
        registered_submissions = self.get_registered_submissions()

        submission_records_to_insert = []

        # !! costly for loop,
        # and get's more costly as the number of registered
        # submissions increase.
        for submission_record in registered_submissions:
            print( time.time() - self.zero_time )
            submission = self.reddit_client.submission(id=submission_record[0])
            current_time = int(time.time())
            submission_downvotes = int((submission.score/ submission.upvote_ratio) - submission.score) # :(
            submission_stat_record = (current_time, submission.id, submission.score, submission_downvotes, submission.num_comments )
            submission_records_to_insert.append(submission_stat_record)

        print( time.time() - self.zero_time )
        register_new_submission_sql_string = "INSERT or IGNORE INTO submission_records VALUES (?, ?, ?, ?, ?)"
        cursor = self.db_connection.cursor()
        cursor.executemany( register_new_submission_sql_string, submission_records_to_insert )
        self.db_connection.commit()
        print( time.time() - self.zero_time )
        return None

    def get_registered_submissions(self):
        cursor = self.db_connection.cursor()
        cursor.execute( 'SELECT id from submissions' )
        submission_rows = cursor.fetchall()
        return submission_rows

    # Close db connection on destruction ( does not cause issues if absence )
    def __del__(self):
        self.db_connection.close()
        return None


if __name__ == "__main__":
    app = App()
