#!/usr/bin/env python3
"""
Database initialization script for Reddit Post Growth Tracker.
"""
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.utils.database_init import DatabaseInitializer

def main():
    """Main initialization function."""
    if len(sys.argv) > 1 and sys.argv[1] == '--reset':
        print("Resetting database...")
        DatabaseInitializer.cache_database_state()
        DatabaseInitializer.wipe_subscribed_subreddits()
        DatabaseInitializer.wipe_subscribed_submissions()
        DatabaseInitializer.wipe_submission_records()
    
    print("Initializing database...")
    DatabaseInitializer.initialize_database()
    print("Database initialization complete!")

if __name__ == '__main__':
    main()
