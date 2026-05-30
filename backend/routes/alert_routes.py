"""
backend/routes/alert_routes.py
==============================
Blueprint serving real-time dynamic cybersecurity alerts for the SOC Command Center feed.
"""

from flask import Blueprint, jsonify, request, session, current_app
from services.dashboard_service import get_cached_data, ensure_session_data
from analysis.alert_engine import generate_dashboard_alerts
from utils.logger import logger

alert_bp = Blueprint("alert", __name__)

@alert_bp.route("/api/alerts")
def api_alerts():
    """
    Ingests Year, City, and Crime Type query parameters, filters active database context,
    and returns a structured rule-based alerts list.
    """
    data_dir = current_app.config["DATA_DIR"]
    if not ensure_session_data(data_dir):
        return jsonify({"error": "No database context loaded"}), 400
        
    cache = get_cached_data(session["dataset_path"])
    df = cache["df"]
    
    # Ingest dynamic dashboard queries
    year = request.args.get("year", "All")
    city = request.args.get("city", "All")
    crime_type = request.args.get("crime_type", "All")
    
    # Apply filters dynamically
    filtered_df = df
    if year != "All":
        try:
            filtered_df = filtered_df[filtered_df["Year"] == int(year)]
        except ValueError:
            pass
            
    if city != "All":
        filtered_df = filtered_df[filtered_df["City"].str.lower() == city.lower()]
        
    if crime_type != "All":
        filtered_df = filtered_df[filtered_df["Crime Description"].str.lower() == crime_type.lower()]
        
    alerts = generate_dashboard_alerts(filtered_df)
    return jsonify({"alerts": alerts})
