"""
backend/utils/config.py
=======================
Centralized configuration management for the Flask application.
Resolves dynamic absolute paths for uploaded files, data folders, and graph static artifacts.
"""

import os

# BASE_DIR represents the 'backend' folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "crime-analysis-secret-2024")
    
    # Siblings of 'backend' directory
    UPLOAD_DIR = os.path.join(os.path.dirname(BASE_DIR), "uploads")
    DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")
    REPORTS_DIR = os.path.join(os.path.dirname(BASE_DIR), "reports")
    
    # Under 'backend/static' directory
    GRAPHS_DIR = os.path.join(BASE_DIR, "static", "graphs")
    
    ALLOWED_EXTENSIONS = {"csv"}
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """Development environment overrides."""
    DEBUG = True

class ProductionConfig(Config):
    """Production environment overrides."""
    DEBUG = False

class TestingConfig(Config):
    """Testing environment overrides."""
    TESTING = True
    DEBUG = True
