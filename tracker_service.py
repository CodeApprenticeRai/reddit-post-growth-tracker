#!/usr/bin/env python3
"""
Background service for Reddit Post Growth Tracker.
This script runs continuously to update submission data.
"""
import sys
import os
import time
import signal

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.services import SubmissionService

class RedditTrackerService:
    """Background service for tracking Reddit post growth."""
    
    def __init__(self):
        self.submission_service = SubmissionService()
        self.running = True
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print(f"\nReceived signal {signum}. Shutting down gracefully...")
        self.running = False
    
    def run_loop(self):
        """Main service loop."""
        counter = 1
        
        print("Reddit Post Growth Tracker Service started")
        print("Press Ctrl+C to stop")
        
        while self.running:
            loop_start_time = time.time()
            
            print(f"{'='*20} Loop {counter} {'='*20}")
            
            try:
                # Register new submissions
                print("Registering new submissions...")
                start_time = time.time()
                new_submissions_result = self.submission_service.register_new_submissions()
                execution_time = time.time() - start_time
                
                print(f"New submissions processed: {new_submissions_result['new_submissions']}")
                print(f"Subreddits processed: {new_submissions_result['processed_subreddits']}")
                if new_submissions_result['errors']:
                    print(f"Errors: {new_submissions_result['errors']}")
                print(f"Registration completed in: {execution_time:.2f}s")
                
                # Record statistics
                print("Recording submission statistics...")
                start_time = time.time()
                stats_result = self.submission_service.record_submission_statistics()
                execution_time = time.time() - start_time
                
                print(f"Records created: {stats_result['new_records']}")
                print(f"Submissions processed: {stats_result['processed_submissions']}")
                if stats_result['errors']:
                    print(f"Errors: {stats_result['errors']}")
                print(f"Statistics recording completed in: {execution_time:.2f}s")
                
            except Exception as e:
                print(f"Error in main loop: {str(e)}")
            
            loop_execution_time = time.time() - loop_start_time
            
            # Sleep for the remaining time to maintain 60-second intervals
            sleep_time = max(0, 60 - loop_execution_time)
            print(f"Loop {counter} completed in {loop_execution_time:.2f}s. Sleeping for {sleep_time:.2f}s")
            
            if self.running and sleep_time > 0:
                time.sleep(sleep_time)
            
            counter += 1
        
        print("Service stopped")

def main():
    """Main function."""
    service = RedditTrackerService()
    service.run_loop()

if __name__ == "__main__":
    main()
