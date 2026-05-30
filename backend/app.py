"""
backend/app.py
==============
Flask Application Bootstrap Entry Point.
Performs config registration, directory validation, modular Blueprint mapping,
and thread-safe in-memory cache pre-warming on startup.
"""

import os
import sys

# Make sure backend subdirectories are importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from utils.config import DevelopmentConfig
from utils.logger import logger
from services.dashboard_service import get_cached_data

# ── 1. Flask App Initialization ──────────────────────────────────────────────
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Ensure essential local directories exist
os.makedirs(app.config["UPLOAD_DIR"], exist_ok=True)
os.makedirs(app.config["GRAPHS_DIR"], exist_ok=True)
os.makedirs(app.config["DATA_DIR"], exist_ok=True)
os.makedirs(app.config["REPORTS_DIR"], exist_ok=True)

# ── 2. Blueprints & Routes Registrations ─────────────────────────────────────
# Deferred imports to avoid circular reference hazards
from routes.dashboard_routes import dashboard_bp
from routes.api_routes import api_bp
from routes.ml_routes import ml_bp
from routes.alert_routes import alert_bp
from routes.filter_routes import filter_bp

app.register_blueprint(dashboard_bp)
app.register_blueprint(api_bp)
app.register_blueprint(ml_bp)
app.register_blueprint(alert_bp)
app.register_blueprint(filter_bp)

logger.info("Modular MVC Blueprint routing registration completed successfully.")

# ── 3. Startup Cache & Scikit-Learn Model Pre-Warming ────────────────────────
default_csv = os.path.join(app.config["DATA_DIR"], "crime_dataset_india.csv")
if os.path.exists(default_csv):
    try:
        logger.info("Pre-warming in-memory cache and training Scikit-Learn models...")
        get_cached_data(default_csv)
        logger.info("Pre-warming cache pre-training cycles finished successfully.")
    except Exception as e:
        logger.error(f"Failed to pre-warm startup cache: {e}", exc_info=True)
else:
    logger.warning(f"Baseline dataset missing. Pre-warming skipped: {default_csv}")

logger.info("CrimeScope Intel System bootstrapped and ready.")