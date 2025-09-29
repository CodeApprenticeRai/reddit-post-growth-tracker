"""
Database models for the Reddit Post Growth Tracker application.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from ..database.manager import db_manager

class Subreddit:
    """Model for subscribed subreddits."""
    
    def __init__(self, subreddit_id: str, title: str):
        self.id = subreddit_id
        self.title = title
    
    @classmethod
    def create(cls, subreddit_id: str, title: str) -> 'Subreddit':
        """Create a new subreddit subscription."""
        query = "INSERT INTO subscribed_subreddits VALUES (?, ?)"
        db_manager.execute_query(query, (subreddit_id, title), fetch_all=False)
        return cls(subreddit_id, title)
    
    @classmethod
    def get_all(cls) -> List['Subreddit']:
        """Get all subscribed subreddits."""
        query = "SELECT id, subreddit_title FROM subscribed_subreddits"
        results = db_manager.execute_query(query)
        return [cls(row['id'], row['subreddit_title']) for row in results]
    
    @classmethod
    def get_by_title(cls, title: str) -> Optional['Subreddit']:
        """Get a subreddit by its title."""
        query = "SELECT id, subreddit_title FROM subscribed_subreddits WHERE subreddit_title = ?"
        result = db_manager.execute_query(query, (title,), fetch_one=True)
        return cls(result['id'], result['subreddit_title']) if result else None
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary."""
        return {'id': self.id, 'title': self.title}

class Submission:
    """Model for subscribed submissions."""
    
    def __init__(self, submission_id: str, subreddit_title: str, title: str, date_created: Optional[datetime] = None):
        self.id = submission_id
        self.subreddit_title = subreddit_title
        self.title = title
        self.date_created = date_created or datetime.now()
    
    @classmethod
    def create(cls, submission_id: str, subreddit_title: str, title: str) -> 'Submission':
        """Create a new submission subscription."""
        query = "INSERT OR IGNORE INTO subscribed_submissions VALUES (?, ?, ?, ?)"
        db_manager.execute_query(query, (submission_id, subreddit_title, title, cls._datetime_to_timestamp(datetime.now())), fetch_all=False)
        return cls(submission_id, subreddit_title, title)
    
    @classmethod
    def get_by_subreddit(cls, subreddit_title: str, limit: int = -1) -> List['Submission']:
        """Get submissions for a specific subreddit."""
        query = "SELECT id, subreddit_title, submission_title, date_created FROM subscribed_submissions WHERE subreddit_title = ?"
        if limit > 0:
            query += f" LIMIT {limit}"
        
        results = db_manager.execute_query(query, (subreddit_title,))
        return [cls(row['id'], row['subreddit_title'], row['submission_title'], 
                   cls._timestamp_to_datetime(row['date_created'])) for row in results]
    
    @classmethod
    def get_all_ids(cls) -> List[str]:
        """Get all submission IDs."""
        query = "SELECT id FROM subscribed_submissions"
        results = db_manager.execute_query(query)
        return [row['id'] for row in results]
    
    @staticmethod
    def _datetime_to_timestamp(dt: datetime) -> int:
        """Convert datetime to timestamp."""
        return int(dt.timestamp())
    
    @staticmethod
    def _timestamp_to_datetime(timestamp: int) -> datetime:
        """Convert timestamp to datetime."""
        return datetime.fromtimestamp(timestamp)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'subreddit_title': self.subreddit_title,
            'title': self.title,
            'date_created': self.date_created.isoformat()
        }

class SubmissionRecord:
    """Model for submission statistics records."""
    
    def __init__(self, timestamp: int, submission_id: str, score: int, upvotes: int, downvotes: int):
        self.timestamp = timestamp
        self.submission_id = submission_id
        self.score = score
        self.upvotes = upvotes
        self.downvotes = downvotes
    
    @classmethod
    def create(cls, timestamp: int, submission_id: str, score: int, upvotes: int, downvotes: int) -> 'SubmissionRecord':
        """Create a new submission record."""
        query = "INSERT OR IGNORE INTO submission_records VALUES (?, ?, ?, ?, ?)"
        db_manager.execute_query(query, (timestamp, submission_id, score, upvotes, downvotes), fetch_all=False)
        return cls(timestamp, submission_id, score, upvotes, downvotes)
    
    @classmethod
    def get_by_submission_id(cls, submission_id: str) -> List['SubmissionRecord']:
        """Get all records for a specific submission."""
        query = "SELECT * FROM submission_records WHERE id = ? ORDER BY time DESC"
        results = db_manager.execute_query(query, (submission_id,))
        return [cls(row['time'], row['id'], row['score'], row['upvotes'], row['downvotes']) for row in results]
    
    @classmethod
    def create_many(cls, records: List[tuple]) -> None:
        """Create multiple records efficiently."""
        query = "INSERT OR IGNORE INTO submission_records VALUES (?, ?, ?, ?, ?)"
        db_manager.execute_many(query, records)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'time': self.timestamp,
            'id': self.submission_id,
            'score': self.score,
            'upvotes': self.upvotes,
            'downvotes': self.downvotes
        }
