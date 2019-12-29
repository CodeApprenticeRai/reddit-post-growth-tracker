import sqlite3

db_connection = sqlite3.connect("./db/data.db")

create_subscribed_subreddts_table_sql_string = "CREATE TABLE IF NOT EXISTS subscribed_subreddits ( id TEXT PRIMARY KEY, subreddit_title TEXT )";
create_subscribed_submissionss_table_sql_string = "CREATE TABLE IF NOT EXISTS subscribed_submissions ( id TEXT PRIMARY KEY, subreddit_title TEXT, submission_title TEXT )";
create_submission_records_table_sql_string = "CREATE TABLE IF NOT EXISTS submission_records ( time INTEGER NOT NULL, id TEXT NOT NULL, score INTEGER NOT NULL, upvotes INTEGER NOT NULL, downvotes INTEGER NOT NULL, PRIMARY KEY (time, id) )";

cursor = db_connection.cursor()
cursor.execute( create_subscribed_subreddts_table_sql_string )
cursor.execute( create_subscribed_submissionss_table_sql_string )
cursor.execute( create_submission_records_table_sql_string )

db_connection.commit()
db_connection.close()
