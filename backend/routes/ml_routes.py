"""
backend/routes/ml_routes.py
==========================
Blueprint serving REST API endpoints for multi-model Scikit-Learn predictions and classification.
"""

from flask import Blueprint, jsonify, request, session, current_app
from services.dashboard_service import get_cached_data, ensure_session_data
from services.ml_service import predict_crime_class
from utils.logger import logger

ml_bp = Blueprint("ml_api", __name__)

@ml_bp.route("/api/ml/predictions")
def api_ml_predictions():
    data_dir = current_app.config["DATA_DIR"]
    if not ensure_session_data(data_dir):
        return jsonify({"error": "No database context loaded"}), 400
    cache = get_cached_data(session["dataset_path"])
    lr = cache["lr_package"]
    if "error" in lr:
        return jsonify(lr), 400
    return jsonify(lr)


@ml_bp.route("/api/ml/accuracy")
def api_ml_accuracy():
    """
    Returns accuracy scores for all active machine learning models (R2, F1, Silhouette, Contamination Rate).
    """
    data_dir = current_app.config["DATA_DIR"]
    if not ensure_session_data(data_dir):
        return jsonify({"error": "No database context loaded"}), 400
    cache = get_cached_data(session["dataset_path"])
    
    lr = cache["lr_package"]
    rf = cache["rf_package"]
    km = cache["km_package"]
    iso = cache["iso_package"]
    
    return jsonify({
        "regression": lr.get("metrics", {}) if "error" not in lr else {},
        "classification": rf.get("metrics", {}) if "error" not in rf else {},
        "clustering": km.get("metrics", {}) if "error" not in km else {},
        "anomalies": iso.get("metrics", {}) if "error" not in iso else {}
    })


@ml_bp.route("/api/ml/hotspots")
def api_ml_hotspots():
    data_dir = current_app.config["DATA_DIR"]
    if not ensure_session_data(data_dir):
        return jsonify({"error": "No database context loaded"}), 400
    cache = get_cached_data(session["dataset_path"])
    km = cache["km_package"]
    if "error" in km:
        return jsonify(km), 400
    return jsonify(km)


@ml_bp.route("/api/ml/anomalies")
def api_ml_anomalies():
    data_dir = current_app.config["DATA_DIR"]
    if not ensure_session_data(data_dir):
        return jsonify({"error": "No database context loaded"}), 400
    cache = get_cached_data(session["dataset_path"])
    iso = cache["iso_package"]
    if "error" in iso:
        return jsonify(iso), 400
    return jsonify(iso)


@ml_bp.route("/api/ml/predict-category", methods=["GET", "POST"])
def api_ml_predict_category():
    """
    Predicts the target likely crime category based on user query parameters or JSON body inputs.
    """
    data_dir = current_app.config["DATA_DIR"]
    if not ensure_session_data(data_dir):
        return jsonify({"error": "No database context loaded"}), 400
        
    cache = get_cached_data(session["dataset_path"])
    rf = cache["rf_package"]
    if "error" in rf:
        return jsonify(rf), 400
        
    # Extract query params or JSON body safely
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        city = data.get("city")
        month = data.get("month")
        victim_age = data.get("victim_age")
        victim_gender = data.get("victim_gender")
        weapon_used = data.get("weapon_used")
    else:
        city = request.args.get("city")
        month = request.args.get("month")
        victim_age = request.args.get("victim_age")
        victim_gender = request.args.get("victim_gender")
        weapon_used = request.args.get("weapon_used")
        
    if not city or not month or not victim_age or not victim_gender or not weapon_used:
        logger.warning("Predictor infraction: Missing variables for dynamic classification.")
        return jsonify({"error": "Missing parameters for dynamic inference."}), 400
        
    try:
        res = predict_crime_class(
            rf,
            city=city,
            month=int(month),
            victim_age=int(victim_age),
            victim_gender=victim_gender,
            weapon_used=weapon_used
        )
        return jsonify(res)
    except Exception as e:
        logger.error(f"Random Forest classification inference failed: {e}", exc_info=True)
        return jsonify({"error": f"AI Inference execution failed: {e}"}), 400
