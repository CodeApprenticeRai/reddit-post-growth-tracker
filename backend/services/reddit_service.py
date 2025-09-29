"""
Reddit API service for interacting with Reddit's API.
"""
import praw
import time
from typing import List, Dict, Any, Optional
from ..config.settings import Config

class RedditService:
    """Service for interacting with Reddit API."""
    
    def __init__(self):
        self._client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the Reddit client."""
        try:
            config_data = Config.load_reddit_config()
            self._client = praw.Reddit(
                client_id=config_data["client_id"],
                client_secret=config_data["client_secret"],
                user_agent=config_data["user_agent"]
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Reddit client: {str(e)}")
    
    def get_subreddit(self, subreddit_name: str) -> Optional[praw.models.Subreddit]:
        """Get a subreddit instance."""
        try:
            return self._client.subreddit(subreddit_name)
        except Exception:
            return None
    
    def validate_subreddit(self, subreddit_name: str) -> bool:
        """Validate if a subreddit exists and is accessible."""
        try:
            subreddit = self.get_subreddit(subreddit_name)
            if subreddit:
                # Try to access a property to verify it's valid
                _ = subreddit.id
                return True
        except Exception:
            pass
        return False
    
    def get_subreddit_id(self, subreddit_name: str) -> Optional[str]:
        """Get the ID of a subreddit."""
        try:
            subreddit = self.get_subreddit(subreddit_name)
            return subreddit.id if subreddit else None
        except Exception:
            return None
    
    def get_new_submissions(self, subreddit_name: str, limit: int = 25) -> List[Dict[str, Any]]:
        """Get new submissions from a subreddit."""
        try:
            subreddit = self.get_subreddit(subreddit_name)
            if not subreddit:
                return []
            
            submissions = []
            for submission in subreddit.new(limit=limit):
                submissions.append({
                    'id': submission.id,
                    'title': submission.title,
                    'subreddit': subreddit_name
                })
            
            return submissions
        except Exception as e:
            print(f"Error fetching submissions for {subreddit_name}: {str(e)}")
            return []
    
    def get_submission_stats(self, submission_id: str) -> Optional[Dict[str, Any]]:
        """Get current statistics for a submission."""
        try:
            submission = self._client.submission(id=submission_id)
            return {
                'id': submission.id,
                'score': submission.score,
                'upvotes': submission.ups,
                'downvotes': submission.downs,
                'timestamp': int(time.time() / 60) * 60  # Rounded to nearest minute
            }
        except Exception as e:
            print(f"Error fetching stats for submission {submission_id}: {str(e)}")
            return None
    
    def get_multiple_submission_stats(self, submission_ids: List[str]) -> List[Dict[str, Any]]:
        """Get statistics for multiple submissions efficiently."""
        stats = []
        for submission_id in submission_ids:
            stat = self.get_submission_stats(submission_id)
            if stat:
                stats.append(stat)
        return stats
