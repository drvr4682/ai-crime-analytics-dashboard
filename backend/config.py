import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "crime-analysis-secret-2024")
    UPLOAD_DIR = os.path.join(os.path.dirname(BASE_DIR), "uploads")
    GRAPHS_DIR = os.path.join(BASE_DIR, "static", "graphs")
    DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")
    ALLOWED_EXTENSIONS = {"csv"}
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
