"""
Configuration management for the Reddit Post Growth Tracker application.
"""
import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class."""
    
    # Database settings
    DATABASE_PATH = os.getenv('DATABASE_PATH', os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "db", "data.db"))
    
    # Reddit API settings
    REDDIT_CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config.json")
    
    # Cache settings
    CACHE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "subreddits_cache.json")
    
    # Application settings
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', "http://localhost:3000,http://127.0.0.1:3000").split(',')
    
    # Reddit API credentials from environment variables
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
    REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
    REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'RedditPostGrowthTracker/1.0')
    
    @classmethod
    def load_reddit_config(cls):
        """Load Reddit API configuration from config.json or environment variables."""
        # Try environment variables first
        if cls.REDDIT_CLIENT_ID and cls.REDDIT_CLIENT_SECRET:
            return {
                "client_id": cls.REDDIT_CLIENT_ID,
                "client_secret": cls.REDDIT_CLIENT_SECRET,
                "user_agent": cls.REDDIT_USER_AGENT
            }
        
        # Fall back to config.json file
        try:
            with open(cls.REDDIT_CONFIG_PATH, 'r') as config_file:
                return json.load(config_file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Reddit configuration not found. Please set environment variables or create {cls.REDDIT_CONFIG_PATH}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in configuration file {cls.REDDIT_CONFIG_PATH}")

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
