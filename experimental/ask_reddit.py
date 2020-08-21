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
        self.interval = interval
        def __init__(self, interval, action) :
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

        create_subscribed_submissions_table_sql_string = "CREATE TABLE IF NOT EXISTS submissions ( id TEXT PRIMARY KEY, submission_title TEXT, created_utc INTEGER NOT NULL,  )";
        create_submission_records_table_sql_string = "CREATE TABLE IF NOT EXISTS submission_records ( time INTEGER NOT NULL, submission_id TEXT NOT NULL, upvotes INTEGER NOT NULL, downvotes INTEGER NOT NULL, num_comments INTEGER NOT NULL, PRIMARY KEY (time, id) )";

        cursor = db_connection.cursor()
        cursor.execute( create_subscribed_submissions_table_sql_string )
        cursor.execute( create_submission_records_table_sql_string )

        db_connection.commit()
        return db_connection


    '''
    * Register every new submission as soon as it is posted

    Spec-Thoughts:
    '''
    def register_new_submissions(self):
        raise NotImplementedError

    # Close db connection on destruction ( does not cause issues if absence )
    def __del__(self):
        self.db_connection.close()
        return None
