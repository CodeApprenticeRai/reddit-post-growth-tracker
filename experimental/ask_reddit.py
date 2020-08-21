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

import sys, sqlite3, shutil, time


'''
Create tables: (submissions, submisison_records).

submissions: for recording which posts we are growth-monitoring,
submisison_records: for recording submission stats at a given time
'''
def initialize_database():
    db_connection = sqlite3.connect("./data.db")

    create_subscribed_submissions_table_sql_string = "CREATE TABLE IF NOT EXISTS submissions ( id TEXT PRIMARY KEY, submission_title TEXT, created_utc INTEGER NOT NULL,  )";
    create_submission_records_table_sql_string = "CREATE TABLE IF NOT EXISTS submission_records ( time INTEGER NOT NULL, submission_id TEXT NOT NULL, upvotes INTEGER NOT NULL, downvotes INTEGER NOT NULL, num_comments INTEGER NOT NULL, PRIMARY KEY (time, id) )";

    cursor = db_connection.cursor()
    cursor.execute( create_subscribed_submissions_table_sql_string )
    cursor.execute( create_submission_records_table_sql_string )

    db_connection.commit()
    db_connection.close()
    return None


'''
* Register every new submission as soon as it is posted
'''
