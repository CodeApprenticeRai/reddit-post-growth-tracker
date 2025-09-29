"""
Business logic services for the Reddit Post Growth Tracker application.
"""
import time
from typing import List, Dict, Any, Optional
from ..models import Subreddit, Submission, SubmissionRecord
from .reddit_service import RedditService

class SubredditService:
    """Service for managing subreddit subscriptions."""
    
    def __init__(self):
        self.reddit_service = RedditService()
    
    def subscribe_to_subreddit(self, subreddit_name: str) -> Dict[str, Any]:
        """Subscribe to a subreddit for tracking."""
        response = {"success": False, "message": ""}
        
        # Validate subreddit exists
        if not self.reddit_service.validate_subreddit(subreddit_name):
            response["message"] = "invalid_subreddit_name"
            return response
        
        # Get subreddit ID
        subreddit_id = self.reddit_service.get_subreddit_id(subreddit_name)
        if not subreddit_id:
            response["message"] = "failed_to_get_subreddit_id"
            return response
        
        # Check if already subscribed
        existing = Subreddit.get_by_title(subreddit_name)
        if existing:
            response["message"] = "already_subscribed"
            return response
        
        try:
            # Create subscription
            Subreddit.create(subreddit_id, subreddit_name)
            response["success"] = True
            response["message"] = "successfully_subscribed"
        except Exception as e:
            response["message"] = f"database_error: {str(e)}"
        
        return response
    
    def get_subscribed_subreddits(self) -> List[Dict[str, str]]:
        """Get all subscribed subreddits."""
        subreddits = Subreddit.get_all()
        return [subreddit.to_dict() for subreddit in subreddits]

class SubmissionService:
    """Service for managing submission tracking."""
    
    def __init__(self):
        self.reddit_service = RedditService()
    
    def register_new_submissions(self) -> Dict[str, Any]:
        """Register new submissions from all subscribed subreddits."""
        result = {"processed_subreddits": 0, "new_submissions": 0, "errors": []}
        
        try:
            subreddits = Subreddit.get_all()
            
            for subreddit in subreddits:
                try:
                    # Get new submissions from Reddit
                    submissions = self.reddit_service.get_new_submissions(subreddit.title)
                    
                    # Register new submissions
                    for submission_data in submissions:
                        try:
                            Submission.create(
                                submission_data['id'],
                                submission_data['subreddit'],
                                submission_data['title']
                            )
                            result["new_submissions"] += 1
                        except Exception as e:
                            result["errors"].append(f"Failed to register submission {submission_data['id']}: {str(e)}")
                    
                    result["processed_subreddits"] += 1
                    
                except Exception as e:
                    result["errors"].append(f"Failed to process subreddit {subreddit.title}: {str(e)}")
            
        except Exception as e:
            result["errors"].append(f"Failed to get subscribed subreddits: {str(e)}")
        
        return result
    
    def record_submission_statistics(self) -> Dict[str, Any]:
        """Record current statistics for all tracked submissions."""
        result = {"processed_submissions": 0, "new_records": 0, "errors": []}
        
        try:
            submission_ids = Submission.get_all_ids()
            
            # Get statistics for all submissions
            stats_list = self.reddit_service.get_multiple_submission_stats(submission_ids)
            
            # Prepare records for batch insertion
            records = []
            for stats in stats_list:
                records.append((
                    stats['timestamp'],
                    stats['id'],
                    stats['score'],
                    stats['upvotes'],
                    stats['downvotes']
                ))
            
            if records:
                SubmissionRecord.create_many(records)
                result["new_records"] = len(records)
            
            result["processed_submissions"] = len(submission_ids)
            
        except Exception as e:
            result["errors"].append(f"Failed to record statistics: {str(e)}")
        
        return result

class AnalyticsService:
    """Service for generating analytics and reports."""
    
    def get_subreddit_submission_time_series(self, number_of_submissions: int = -1) -> Dict[str, Any]:
        """Get time series data for all subreddits and their submissions."""
        result = {}
        
        try:
            subreddits = Subreddit.get_all()
            
            for subreddit in subreddits:
                # Get submissions for this subreddit
                submissions = Submission.get_by_subreddit(subreddit.title, number_of_submissions)
                
                subreddit_data = {"submissions": {}}
                
                for submission in submissions:
                    # Get time series data for this submission
                    records = SubmissionRecord.get_by_submission_id(submission.id)
                    
                    submission_data = {
                        "title": submission.title,
                        "data": [record.to_dict() for record in records]
                    }
                    
                    subreddit_data["submissions"][submission.id] = submission_data
                
                result[subreddit.title] = subreddit_data
            
        except Exception as e:
            print(f"Error generating time series data: {str(e)}")
            result = {}
        
        return result
