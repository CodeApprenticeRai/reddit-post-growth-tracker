"""
API routes for subreddit management.
"""
from flask import Blueprint, request, jsonify
from ..services import SubredditService

subreddit_bp = Blueprint('subreddit', __name__, url_prefix='/api/subreddits')
subreddit_service = SubredditService()

@subreddit_bp.route('/subscribe', methods=['POST'])
def subscribe_to_subreddit():
    """Subscribe to a subreddit for tracking."""
    try:
        request_body = request.json
        
        if not request_body or 'subreddit_name' not in request_body:
            return jsonify({
                "success": False,
                "message": "subreddit_name must be specified"
            }), 400
        
        subreddit_name = request_body["subreddit_name"]
        result = subreddit_service.subscribe_to_subreddit(subreddit_name)
        
        status_code = 200 if result["success"] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Internal server error: {str(e)}"
        }), 500

@subreddit_bp.route('/', methods=['GET'])
def get_subscribed_subreddits():
    """Get all subscribed subreddits."""
    try:
        subreddits = subreddit_service.get_subscribed_subreddits()
        return jsonify({
            "success": True,
            "subreddits": subreddits
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Failed to get subreddits: {str(e)}"
        }), 500
