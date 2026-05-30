"""
backend/routes/filter_routes.py
==============================
Blueprint coordinating interactive telemetry filtering and natural-language AI insights compilation.
"""

from flask import Blueprint, jsonify, request, session, current_app
from services.dashboard_service import get_cached_data, ensure_session_data
from services.filter_service import filter_dataset
from analysis.insights_engine import generate_dashboard_insights
from utils.logger import logger

filter_bp = Blueprint("filter", __name__)

@filter_bp.route("/filter-data")
def filter_data():
    """
    Ingests dropdown filter parameters, executes Pandas queries,
    and returns complete dynamic visual datasets for Chart.js.
    """
    data_dir = current_app.config["DATA_DIR"]
    if not ensure_session_data(data_dir):
        return jsonify({"error": "No database context loaded"}), 400
        
    cache = get_cached_data(session["dataset_path"])
    df = cache["df"]
    
    year = request.args.get("year", "All")
    city = request.args.get("city", "All")
    crime_type = request.args.get("crime_type", "All")
    
    payload = filter_dataset(df, year, city, crime_type)
    return jsonify(payload)


@filter_bp.route("/api/insights")
def api_insights():
    """
    Ingests filter constraints, evaluates dataset subsets,
    and returns 5 synthesized natural-language intelligence observations.
    """
    data_dir = current_app.config["DATA_DIR"]
    if not ensure_session_data(data_dir):
        return jsonify({"error": "No database context loaded"}), 400
        
    cache = get_cached_data(session["dataset_path"])
    df = cache["df"]
    
    year = request.args.get("year", "All")
    city = request.args.get("city", "All")
    crime_type = request.args.get("crime_type", "All")
    
    # Run filters reactively
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
        
    insights = generate_dashboard_insights(filtered_df)
    return jsonify({"insights": insights})
