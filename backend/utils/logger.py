"""
backend/utils/logger.py
=======================
Standardized, thread-safe application logging system.
Logs events, database ingestion warnings, API traffic, and Scikit-Learn training states.
"""

import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name="CrimeScope"):
    """
    Sets up and returns a logger instance with console and file handlers.
    """
    logger = logging.getLogger(name)
    
    # Avoid duplicating handlers if already configured
    if logger.handlers:
        return logger
        
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Console Handler (INFO level)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    # File Handler (DEBUG level)
    # Resolve log path relative to 'backend' parent directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    reports_dir = os.path.join(os.path.dirname(base_dir), "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    log_file = os.path.join(reports_dir, "app_execution.log")
    fh = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    
    return logger

# Global default logger instance
logger = setup_logger()
