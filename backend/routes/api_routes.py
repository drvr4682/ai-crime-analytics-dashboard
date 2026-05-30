"""
backend/routes/api_routes.py
============================
Blueprint serving JSON endpoints for Chart.js dashboard visualization telemetry.
"""

from flask import Blueprint, jsonify, session, current_app
from services.dashboard_service import get_cached_data, ensure_session_data
from services.chart_service import format_predictions_payload
from utils.logger import logger

api_bp = Blueprint("api", __name__)

@api_bp.route("/api/dashboard-summary")
def api_summary():
    data_dir = current_app.config["DATA_DIR"]
    if not ensure_session_data(data_dir):
        return jsonify({"error": "No database context loaded"}), 400
    cache = get_cached_data(session["dataset_path"])
    return jsonify(cache["summary"])


@api_bp.route("/api/crime-trends")
def api_trends():
    data_dir = current_app.config["DATA_DIR"]
    if not ensure_session_data(data_dir):
        return jsonify({"error": "No database context loaded"}), 400
    cache = get_cached_data(session["dataset_path"])
    return jsonify(cache["trends_data"])


@api_bp.route("/api/crime-types")
def api_types():
    data_dir = current_app.config["DATA_DIR"]
    if not ensure_session_data(data_dir):
        return jsonify({"error": "No database context loaded"}), 400
    cache = get_cached_data(session["dataset_path"])
    return jsonify(cache["types_data"])


@api_bp.route("/api/weapons")
def api_weapons():
    data_dir = current_app.config["DATA_DIR"]
    if not ensure_session_data(data_dir):
        return jsonify({"error": "No database context loaded"}), 400
    cache = get_cached_data(session["dataset_path"])
    return jsonify(cache["weapons_data"])


@api_bp.route("/api/top-cities")
def api_top_cities():
    data_dir = current_app.config["DATA_DIR"]
    if not ensure_session_data(data_dir):
        return jsonify({"error": "No database context loaded"}), 400
    cache = get_cached_data(session["dataset_path"])
    return jsonify(cache["cities_data"])


@api_bp.route("/api/heatmap")
def api_heatmap():
    data_dir = current_app.config["DATA_DIR"]
    if not ensure_session_data(data_dir):
        return jsonify({"error": "No database context loaded"}), 400
    cache = get_cached_data(session["dataset_path"])
    return jsonify(cache["heatmap_data"])


@api_bp.route("/api/predictions")
def api_predictions():
    """
    Returns time-series forecasted values formatted cleanly for client-side Chart.js.
    """
    data_dir = current_app.config["DATA_DIR"]
    if not ensure_session_data(data_dir):
        return jsonify({"error": "No database context loaded"}), 400
        
    cache = get_cached_data(session["dataset_path"])
    ml_package = cache["lr_package"]
    
    formatted = format_predictions_payload(ml_package)
    return jsonify(formatted)


@api_bp.route("/api/correlation")
def api_correlation():
    data_dir = current_app.config["DATA_DIR"]
    if not ensure_session_data(data_dir):
        return jsonify({"error": "No database context loaded"}), 400
    cache = get_cached_data(session["dataset_path"])
    return jsonify(cache["correlation_data"])


@api_bp.route("/api/filter-options")
def api_filter_options():
    """
    Extracts dynamic unique options for Year, City, Crime Type, and Weapon Used.
    """
    data_dir = current_app.config["DATA_DIR"]
    if not ensure_session_data(data_dir):
        return jsonify({"error": "No database context loaded"}), 400
        
    cache = get_cached_data(session["dataset_path"])
    df = cache["df"]
    
    years = sorted([int(x) for x in df["Year"].dropna().unique() if x > 0])
    cities = sorted([str(x) for x in df["City"].dropna().unique()])
    crime_types = sorted([str(x) for x in df["Crime Description"].dropna().unique()])
    weapons = sorted([str(x) for x in df["Weapon Used"].dropna().unique()])
    
    return jsonify({
        "years": years,
        "cities": cities,
        "crime_types": crime_types,
        "weapons": weapons
    })
