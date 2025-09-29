"""
API routes for analytics and data retrieval.
"""
from flask import Blueprint, request, jsonify
from ..services import AnalyticsService, SubmissionService

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')
analytics_service = AnalyticsService()
submission_service = SubmissionService()

@analytics_bp.route('/submissions/<int:number_of_submissions>', methods=['GET'])
def get_subreddit_submission_time_series(number_of_submissions):
    """Get time series data for subreddit submissions."""
    try:
        data = analytics_service.get_subreddit_submission_time_series(number_of_submissions)
        return jsonify(data), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to get submission data: {str(e)}"
        }), 500

@analytics_bp.route('/submissions', methods=['GET'])
def get_all_subreddit_submission_time_series():
    """Get time series data for all subreddit submissions."""
    try:
        data = analytics_service.get_subreddit_submission_time_series()
        return jsonify(data), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to get submission data: {str(e)}"
        }), 500

@analytics_bp.route('/update-submissions', methods=['POST'])
def update_submissions():
    """Register new submissions and update statistics."""
    try:
        # Register new submissions
        new_submissions_result = submission_service.register_new_submissions()
        
        # Record statistics
        stats_result = submission_service.record_submission_statistics()
        
        return jsonify({
            "success": True,
            "new_submissions": new_submissions_result,
            "statistics_update": stats_result
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to update submissions: {str(e)}"
        }), 500
