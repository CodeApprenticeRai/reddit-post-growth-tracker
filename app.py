"""
Main Flask application for the Reddit Post Growth Tracker.
"""
from flask import Flask
from flask_cors import CORS
import os
import sys

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.config.settings import config
from backend.routes.subreddit_routes import subreddit_bp
from backend.routes.analytics_routes import analytics_bp
from backend.utils.database_init import DatabaseInitializer

def create_app(config_name='default'):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Enable CORS
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Initialize database
    DatabaseInitializer.initialize_database()
    
    # Register blueprints
    app.register_blueprint(subreddit_bp)
    app.register_blueprint(analytics_bp)
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Reddit Post Growth Tracker API is running'}
    
    return app

if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True, host='0.0.0.0', port=5001)
