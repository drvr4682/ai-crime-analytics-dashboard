"""
backend/routes/api_routes.py
============================
Blueprint serving JSON endpoints for Chart.js dashboard visualization telemetry.
"""

from flask import Blueprint, jsonify, session, current_app, request, Response
import io
import datetime
import re
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


@api_bp.route("/api/export/excel")
def export_excel():
    """
    Validates filter constraints, filters the active Pandas DataFrame in-memory,
    and streams a UTF-8 BOM CSV compatible with Microsoft Excel.
    """
    logger.info("Excel export endpoint invoked.")
    data_dir = current_app.config["DATA_DIR"]
    if not ensure_session_data(data_dir):
        logger.error("Excel export failed: No dataset loaded in active session.")
        return jsonify({"error": "No dataset loaded. Ingest a dataset first."}), 400
        
    cache = get_cached_data(session["dataset_path"])
    df = cache["df"]
    
    # 1. Ingest request parameters
    year = request.args.get("year", "All").strip()
    city = request.args.get("city", "All").strip()
    crime_type = request.args.get("crime_type", "All").strip()
    
    # 2. Extract allowed values from DataFrame for strict validation
    allowed_years = sorted([int(x) for x in df["Year"].dropna().unique() if x > 0])
    allowed_cities = sorted([str(x).lower() for x in df["City"].dropna().unique()])
    allowed_crime_types = sorted([str(x).lower() for x in df["Crime Description"].dropna().unique()])
    
    # 3. Perform input validation
    if year != "All":
        try:
            year_val = int(year)
            if year_val not in allowed_years:
                logger.warning(f"Excel export blocked: Invalid year input ({year})")
                return jsonify({"error": f"Invalid year filter constraint: {year}"}), 400
        except ValueError:
            logger.warning(f"Excel export blocked: Malformed year input ({year})")
            return jsonify({"error": f"Malformed year filter constraint: {year}"}), 400
            
    if city != "All" and city.lower() not in allowed_cities:
        logger.warning(f"Excel export blocked: Invalid city input ({city})")
        return jsonify({"error": f"Invalid city filter constraint: {city}"}), 400
        
    if crime_type != "All" and crime_type.lower() not in allowed_crime_types:
        logger.warning(f"Excel export blocked: Invalid crime type input ({crime_type})")
        return jsonify({"error": f"Invalid crime type filter constraint: {crime_type}"}), 400
        
    # 4. Perform dynamic in-memory filtering
    filtered_df = df.copy()
    if year != "All":
        filtered_df = filtered_df[filtered_df["Year"] == int(year)]
    if city != "All":
        filtered_df = filtered_df[filtered_df["City"].str.lower() == city.lower()]
    if crime_type != "All":
        filtered_df = filtered_df[filtered_df["Crime Description"].str.lower() == crime_type.lower()]
        
    # 5. Generate secure CSV with UTF-8 BOM integration for Excel
    output = io.StringIO()
    output.write(u'\ufeff')  # Prepend BOM (essential for Microsoft Excel Unicode mapping)
    filtered_df.to_csv(output, index=False)
    csv_data = output.getvalue()
    
    # 6. Generate dynamic sanitized filename
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    sanitized_city = re.sub(r'[^a-zA-Z0-9]', '', city) if city != "All" else "AllCities"
    sanitized_year = str(year)
    sanitized_crime = re.sub(r'[^a-zA-Z0-9]', '', crime_type)[:20] if crime_type != "All" else "AllOffenses"
    
    filename = f"crime_report_{sanitized_year}_{sanitized_city}_{sanitized_crime}_{timestamp}.csv"
    
    logger.info(f"Successfully compiled filtered spreadsheet dataset. Rows: {len(filtered_df)}. Filename: {filename}")
    
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename={filename}"}
    )

