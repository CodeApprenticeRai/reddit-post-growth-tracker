import datetime
import sqlite3
import json
import sys
import time
import praw
import asyncio

class RPGT:
    def __init__(self, use_command_line=False):
        self.use_command_line = use_command_line
        self.DATABASE_PATH = "./data.db"
        self.SQL = {
            "create_subreddts_table_sql_string" : "CREATE TABLE IF NOT EXISTS subreddits_subscribed_to ( id TEXT PRIMARY KEY, subreddit_display_name TEXT NOT NULL )",
            "create_submissions_subscribed_to_table_sql_string" : "CREATE TABLE IF NOT EXISTS submissions_subscribed_to ( id TEXT PRIMARY KEY, subreddit_display_name TEXT NOT NULL, submission_title TEXT NOT NULL )",
            "create_submission_records_table_sql_string" : "CREATE TABLE IF NOT EXISTS submission_records ( time INTEGER NOT NULL, id TEXT NOT NULL, score INTEGER NOT NULL, PRIMARY KEY (time, id) )"
        }
        self.db_connection = self.initialize_database()
        self.reddit_client = self.get_reddit_client()
        
        # set of subreddit titles
        self.subreddits_cache = set([ subreddit_display_name for subreddit_id, subreddit_display_name in  self.get_subreddits_subscribed_to()]) 
        # set of submission ids
        self.submissions_cache = set([ submission_id for submission_id, subreddit_display_name, submission_title in self.get_submissions_subscribed_to() ]) 
        # dict of submission ids to list of submission records
        self.submission_records_cache = { submission_id : self.get_submission_records_by_submission_id(submission_id) for submission_id in self.submissions_cache } 

        self.command_line_actions = {
            4 : ("get submissions subscribed to by subreddit display name", self.cl_get_submissions_subscribed_to_by_subreddit_display_name),
            3 : ("clean and initialize db", self.reinitialize_database),
            2 : ("add new subreddit from input", self.add_new_subreddit_from_input),
            1 : ("get subreddits subscribed to", self.get_subreddits_subscribed_to),
            0 : ("exit", self.exit)
        }

        # self.actions = {
        #     "subscribe_to_subreddit" : self.subscribe_to_subreddit,
        #     "remove_subreddit" : self.remove_subreddit,
        #     "get_subreddits_subscribed_to" : self.get_subreddits_subscribed_to,
        #     "subscribe_to_submission" : self.subscribe_to_submission,
        #     "get_submissions_subscribed_to_by_subreddit_id" : self.get_submissions_subscribed_to_by_subreddit_id,
        #     "insert_submission_record" : self.insert_submission_record,
        #     "get_submission_records_by_submission_id" : self.get_submission_records_by_submission_id,
        #     "exit" : self.exit
        # }

        self._exit = False


    def initialize_database(self):
        self.db_connection = sqlite3.connect(self.DATABASE_PATH, check_same_thread=False )

        cursor = self.db_connection.cursor()
        cursor.execute( self.SQL["create_subreddts_table_sql_string"] )
        cursor.execute( self.SQL["create_submissions_subscribed_to_table_sql_string"] )
        cursor.execute( self.SQL["create_submission_records_table_sql_string"] )
        self.db_connection.commit()

        return self.db_connection

    def wipe_database(self):
        cursor = self.db_connection.cursor()
        cursor.execute("DROP TABLE submissions_subscribed_to")
        cursor.execute("DROP TABLE subreddits_subscribed_to")
        cursor.execute("DROP TABLE submission_records")
        self.db_connection.commit()
        return None

    def reinitialize_database(self):
        self.wipe_database()
        self.initialize_database()
        return None

    def get_reddit_client(self):
        with open('config.json') as config:
            config = json.load(config)
            self.reddit_client = praw.Reddit(
                client_id=config["client_id"],
                client_secret=config["client_secret"],
                user_agent=config["user_agent"]
            )
        return self.reddit_client


    '''
    A set of subreddits is maintained in the database.
    This set of subreddits are the subreddits that submissions
    will be subscribed to from. 
    '''
    def subscribe_to_subreddit(self, subreddit_id, subreddit_display_name):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO subreddits_subscribed_to VALUES (?, ?)", (subreddit_id, subreddit_display_name))
        self.db_connection.commit()
        return None
    

    def remove_subreddit_by_id(self, subreddit_id):
        cursor = self.db_connection.cursor()
        cursor.execute("DELETE FROM subreddits_subscribed_to WHERE id = ?", (subreddit_id,))
        self.db_connection.commit()
        return None


    def get_subreddits_subscribed_to(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM subreddits_subscribed_to")
        return cursor.fetchall()

    '''
    Submissions that are subscribed to have their state recorded
    at a regular inverval (default 1 minute).  
    '''
    def subscribe_to_submission(self, submission_id, subreddit_display_name, submission_title):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO submissions_subscribed_to VALUES (?, ?, ?)", (submission_id, subreddit_display_name, submission_title))
        self.db_connection.commit()
        return None


    def subscribe_to_submissions(self, submissions):
        cursor = self.db_connection.cursor()
        cursor.executemany("INSERT INTO submissions_subscribed_to VALUES (?, ?, ?)", submissions)
        self.db_connection.commit()
        return None

    '''
    For a given subreddit, gete all submissions
    that have previously been subscribed to.
    '''
    def get_submissions_subscribed_to(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM submissions_subscribed_to")
        return cursor.fetchall()


    def get_submissions_subscribed_to_by_subreddit_id(self, subreddit_id):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM submissions_subscribed_to WHERE subreddit_id = ?", (subreddit_id,))
        return cursor.fetchall()

    def cl_get_submissions_subscribed_to_by_subreddit_display_name(self):
        subreddit_display_name = input("Enter subreddit display name: ")
        return self.get_submissions_subscribed_to_by_subreddit_display_name(subreddit_display_name)

    def get_submissions_subscribed_to_by_subreddit_display_name(self, subreddit_display_name):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM submissions_subscribed_to WHERE subreddit_display_name = ?", (subreddit_display_name,))
        return cursor.fetchall()

    def insert_submission_record(self, time, submission_id, score):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO submission_records VALUES (?, ?, ?)", (time, submission_id, score))
        self.db_connection.commit()
        return None

    def insert_submission_records(self, records):
        cursor = self.db_connection.cursor()
        cursor.executemany("INSERT INTO submission_records VALUES (?, ?, ?)", records)
        self.db_connection.commit()
        return None

    def get_submission_records_by_submission_id(self, submission_id):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM submission_records WHERE id = ?", (submission_id,))
        return cursor.fetchall()
    
    def exit(self):
        self._exit = True
        return None

    def update_submissions_subscribed_to(self):
        # async process 1: check for new submissions and add
        #   each new submission to the table submissions_subscribed_to 
        self.subreddits_cache = set([ subreddit_display_name for subreddit_id, subreddit_display_name in  self.get_subreddits_subscribed_to()])

        submissions_to_be_added = []
        print("Updating submissions subscribed to...")
        for subreddit_display_name in self.subreddits_cache:
            subreddit_object = self.reddit_client.subreddit(display_name=subreddit_display_name)
            for submission in subreddit_object.new(limit=50):
                if submission.id not in self.submissions_cache:
                    submissions_to_be_added.append((submission.id, subreddit_display_name, submission.title))
                    self.submissions_cache.add(submission.id)
        
        # print("Submissions to be added: {}".format(submissions_to_be_added)) 
        
        self.subscribe_to_submissions(submissions_to_be_added)
        return None


    def update_submission_records(self):
        # async process 2: record the state of each submission subscribed to
        self.submissions_cache = set([ submission_id for submission_id, subreddit_display_name, submission_title in self.get_submissions_subscribed_to() ])
        
        submission_records_to_be_added = []
        print("Updating submission records...")
        print("Length of submissions_cache: {}".format(len(self.submissions_cache)))

        update_start_time = time.time()
        for submission_id in self.submissions_cache:
            submission_object = self.reddit_client.submission(id=submission_id)
            new_submission_record = (int(time.time()), submission_id, submission_object.score)
            submission_records_to_be_added.append(new_submission_record)
        update_time_taken = time.time() - update_start_time
        print("Update time taken: {}".format(update_time_taken))
        # print("submission records to be added: {}".format(submission_records_to_be_added))
        self.insert_submission_records(submission_records_to_be_added)
        print("Length of submission_records_to_be_added: {}".format(len(submission_records_to_be_added)))
        return None

    def add_new_subreddit_from_input(self):
        subreddit_display_name = input("Enter subreddit display name: ")
        subreddit = self.reddit_client.subreddit(display_name=subreddit_display_name)
        self.subscribe_to_subreddit(subreddit.id, subreddit.display_name)
        return None

    def main_menu(self):
        print("Menu")
        for action_number in self.command_line_actions:
            print("{}: {}".format(action_number, self.command_line_actions[action_number][0]))
        
        user_choice = input("Please select a number from the above menu: ")
        try:
            result = self.command_line_actions[int(user_choice)][1]()
            if (result != None):
                for row in result:
                    print(row)
        except KeyError:
            print("Invalid choice")
        return None
    

    def main(self):
        if self.use_command_line:
            self.main_menu()
            # print("got here")
            # coroutine_start_time = time.time()
            # asyncio.gather(self.update_submissions_subscribed_to(), self.update_submission_records())
            # sleep_time = 60 - (time.time() - coroutine_start_time)
            # await asyncio.sleep(sleep_time)
        if not self._exit:
            self.update_submissions_subscribed_to()
            self.update_submission_records()

        return None


    def run(self):
        self.initialize_database()
        while (not self._exit):    
            start_time = time.time()
            self.main()
            sleep_time = max(0, 60 - (time.time() - start_time))
            time.sleep(sleep_time)
        return None    
            
if __name__ == "__main__":
    use_command_line = False
    if ( (len(sys.argv) > 1) and (sys.argv[1] == "--use-command-line") ):
        use_command_line = True

    rpgt = RPGT(use_command_line=use_command_line)
    rpgt.run()
    