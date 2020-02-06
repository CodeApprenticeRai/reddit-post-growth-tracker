import sys, sqlite3, shutil, time

def initialize_database():
    db_connection = sqlite3.connect("./db/data.db")

    create_subscribed_subreddts_table_sql_string = "CREATE TABLE IF NOT EXISTS subscribed_subreddits ( id TEXT PRIMARY KEY, subreddit_title TEXT )";
    create_subscribed_submissions_table_sql_string = "CREATE TABLE IF NOT EXISTS subscribed_submissions ( id TEXT PRIMARY KEY, subreddit_title TEXT, submission_title TEXT )";
    create_submission_records_table_sql_string = "CREATE TABLE IF NOT EXISTS submission_records ( time INTEGER NOT NULL, id TEXT NOT NULL, score INTEGER NOT NULL, upvotes INTEGER NOT NULL, downvotes INTEGER NOT NULL, PRIMARY KEY (time, id) )";

    cursor = db_connection.cursor()
    cursor.execute( create_subscribed_subreddts_table_sql_string )
    cursor.execute( create_subscribed_submissions_table_sql_string )
    cursor.execute( create_submission_records_table_sql_string )

    db_connection.commit()
    db_connection.close()
    return None

def wipe_subscribed_submissions():
    try:
        db_connection = sqlite3.connect("./db/data.db")

        drop_subscribed_submissions_table_sql_string = "DROP TABLE subscribed_submissions"

        cursor = db_connection.cursor()
        cursor.execute( drop_subscribed_submissions_table_sql_string )
        db_connection.commit()
        db_connection.close()
    except:
        pass
    return None

def wipe_submission_records():
    try:
        db_connection = sqlite3.connect("./db/data.db")

        drop_submission_records_table_sql_string = "DROP TABLE submission_records"
        cursor = db_connection.cursor()
        cursor.execute( drop_submission_records_table_sql_string )
        db_connection.commit()
        db_connection.close()
    except:
        pass
    return None

def cache_database_state():
    shutil.move(
        "./subreddits_cache.json",
        "./db/subreddits_cache_{}.json".format( int(time.time()) )
    )

    return None

if __name__ == "__main__":
    if (len(sys.argv) > 1 ):
        cache_database_state()
        wipe_subscribed_submissions()
        wipe_submission_records()

    initialize_database()
