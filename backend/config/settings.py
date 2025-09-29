"""
Configuration management for the Reddit Post Growth Tracker application.
"""
import os
import json
from pathlib import Path

class Config:
    """Base configuration class."""
    
    # Database settings
    DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "db", "data.db")
    
    # Reddit API settings
    REDDIT_CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config.json")
    
    # Cache settings
    CACHE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "subreddits_cache.json")
    
    # Application settings
    DEBUG = False
    CORS_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    @classmethod
    def load_reddit_config(cls):
        """Load Reddit API configuration from config.json."""
        try:
            with open(cls.REDDIT_CONFIG_PATH, 'r') as config_file:
                return json.load(config_file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Reddit configuration file not found at {cls.REDDIT_CONFIG_PATH}")
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
