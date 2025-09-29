"""
Database initialization utilities.
"""
import os
import shutil
import time
from ..database.manager import db_manager

class DatabaseInitializer:
    """Handles database initialization and maintenance."""
    
    @staticmethod
    def initialize_database():
        """Initialize the database with required tables."""
        create_tables_script = """
        CREATE TABLE IF NOT EXISTS subscribed_subreddits (
            id TEXT PRIMARY KEY,
            subreddit_title TEXT
        );
        
        CREATE TABLE IF NOT EXISTS subscribed_submissions (
            id TEXT PRIMARY KEY,
            subreddit_title TEXT,
            submission_title TEXT,
            date_created INTEGER DEFAULT (strftime('%s', 'now'))
        );
        
        CREATE TABLE IF NOT EXISTS submission_records (
            time INTEGER NOT NULL,
            id TEXT NOT NULL,
            score INTEGER NOT NULL,
            upvotes INTEGER NOT NULL,
            downvotes INTEGER NOT NULL,
            PRIMARY KEY (time, id)
        );
        """
        
        try:
            db_manager.execute_script(create_tables_script)
            print("Database initialized successfully")
        except Exception as e:
            print(f"Error initializing database: {str(e)}")
            raise
    
    @staticmethod
    def wipe_subscribed_submissions():
        """Clear all subscribed submissions."""
        try:
            db_manager.execute_query("DROP TABLE IF EXISTS subscribed_submissions", fetch_all=False)
            print("Subscribed submissions table cleared")
        except Exception as e:
            print(f"Error clearing submissions: {str(e)}")
    
    @staticmethod
    def wipe_submission_records():
        """Clear all submission records."""
        try:
            db_manager.execute_query("DROP TABLE IF EXISTS submission_records", fetch_all=False)
            print("Submission records table cleared")
        except Exception as e:
            print(f"Error clearing records: {str(e)}")
    
    @staticmethod
    def cache_database_state(cache_path: str = None):
        """Backup the current cache file."""
        if not cache_path:
            cache_path = "subreddits_cache.json"
        
        if os.path.exists(cache_path):
            backup_path = f"db/subreddits_cache_{int(time.time())}.json"
            os.makedirs("db", exist_ok=True)
            shutil.move(cache_path, backup_path)
            print(f"Cache backed up to {backup_path}")
        else:
            print("No cache file found to backup")
