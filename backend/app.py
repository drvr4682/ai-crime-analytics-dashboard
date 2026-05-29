"""
app.py
======
Flask application entry point (Upgraded for Phase 4: Multi-Model ML Suite).
Routes:
  GET  /              → upload page (index.html)
  POST /upload        → process uploaded CSV, return dashboard JSON
  GET  /dashboard     → render dashboard with results
  GET  /download      → download analysis report as text

Run:
  python backend/app.py
"""

import os
import json
import sys

# ── Make sure sibling modules (preprocess, analysis, model) are importable ────
sys.path.insert(0, os.path.dirname(__file__))

from flask import (Flask, render_template, request,
                   redirect, url_for, jsonify, send_file, session)
from werkzeug.utils import secure_filename

from preprocess import (load_and_clean, get_summary, get_trends_data, 
                        get_types_data, get_weapons_data, get_heatmap_data, 
                        get_correlation_data, get_cities_data)
from model      import predict_future_crimes
from config     import DevelopmentConfig

# ── Upgraded modular ML components ─────────────────────────────────────────────
from ml.linear_regression_model import train_linear_regression
from ml.random_forest_model     import train_random_forest, predict_crime_category
from ml.kmeans_model            import run_kmeans_hotspots
from ml.isolation_forest_model  import run_isolation_forest_anomalies

# ── Flask init ─────────────────────────────────────────────────────────────────
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# ── Paths ──────────────────────────────────────────────────────────────────────
UPLOAD_DIR  = app.config["UPLOAD_DIR"]
GRAPHS_DIR  = app.config["GRAPHS_DIR"]
DATA_DIR    = app.config["DATA_DIR"]
ALLOWED     = app.config["ALLOWED_EXTENSIONS"]

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(GRAPHS_DIR, exist_ok=True)


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED


# ── In-Memory Singleton Data Cache ──────────────────────────────────────────────
_DATA_CACHE = {
    "filepath": None,
    "df": None,
    "summary": None,
    "ml": None,
    "trends_data": None,
    "types_data": None,
    "weapons_data": None,
    "heatmap_data": None,
    "correlation_data": None,
    "cities_data": None,
    # Phase 4 components
    "lr_package": None,
    "rf_package": None,
    "km_package": None,
    "iso_package": None
}

def get_cached_data(filepath):
    global _DATA_CACHE
    if _DATA_CACHE["filepath"] == filepath and _DATA_CACHE["df"] is not None:
        return _DATA_CACHE
    
    df = load_and_clean(filepath)
    
    # ── Train all Scikit-Learn models on startup / ingestion ───────────────────
    lr_res = train_linear_regression(df)
    rf_res = train_random_forest(df)
    km_res = run_kmeans_hotspots(df)
    iso_res = run_isolation_forest_anomalies(df)
    
    _DATA_CACHE = {
        "filepath": filepath,
        "df": df,
        "summary": get_summary(df),
        
        # Backward compatibility alias for legacy API predictions
        "ml": {
            "predictions": lr_res.get("predictions", {}) if "error" not in lr_res else {},
            "r2_score": lr_res.get("metrics", {}).get("r2_score", 0.0) if "error" not in lr_res else 0.0,
            "historical_years": lr_res.get("historical_years", []),
            "historical_counts": lr_res.get("historical_counts", [])
        },
        
        "trends_data": get_trends_data(df),
        "types_data": get_types_data(df),
        "weapons_data": get_weapons_data(df),
        "heatmap_data": get_heatmap_data(df),
        "correlation_data": get_correlation_data(df),
        "cities_data": get_cities_data(df),
        
        # Upgraded ML Packages
        "lr_package": lr_res,
        "rf_package": rf_res,
        "km_package": km_res,
        "iso_package": iso_res
    }
    return _DATA_CACHE


# ── Route: Home ───────────────────────────────────────────────────────────────
@app.route("/")
def index():
    """
    Renders the main HTML page (index.html).
    render_template looks inside the templates/ folder automatically.
    """
    return render_template("index.html")


# ── Helper: Hydrate Data ──────────────────────────────────────────────────────
def ensure_session_data() -> bool:
    """Auto-hydrates session parameters from built-in CSV if not already present."""
    if "dataset_path" not in session:
        filepath = os.path.join(DATA_DIR, "crime_dataset_india.csv")
        if os.path.exists(filepath):
            session["dataset_path"] = filepath
            try:
                get_cached_data(filepath)
                return True
            except Exception:
                return False
        return False
    else:
        try:
            get_cached_data(session["dataset_path"])
            return True
        except Exception:
            return False


# ── Route: Upload & Analyse ───────────────────────────────────────────────────
@app.route("/upload", methods=["POST"])
def upload():
    """
    Handles CSV upload (or uses the built-in dataset if no file is uploaded).
    """
    filepath = None

    if "file" in request.files and request.files["file"].filename != "":
        f = request.files["file"]
        if not allowed_file(f.filename):
            return jsonify({"error": "Only CSV files are allowed."}), 400
        filename = secure_filename(f.filename)
        filepath = os.path.join(UPLOAD_DIR, filename)
        f.save(filepath)
    else:
        filepath = os.path.join(DATA_DIR, "crime_dataset_india.csv")
        if not os.path.exists(filepath):
            return jsonify({"error": "No dataset found. Please upload a CSV file."}), 400

    try:
        get_cached_data(filepath)
        session["dataset_path"] = filepath
    except Exception as e:
        return jsonify({"error": f"Failed to read CSV: {e}"}), 400

    return redirect(url_for("dashboard"))


# ── Route: Dashboard ──────────────────────────────────────────────────────────
@app.route("/dashboard")
def dashboard():
    """
    Renders the dashboard page with all processed data.
    """
    if not ensure_session_data():
        return redirect(url_for("index"))

    cache = get_cached_data(session["dataset_path"])
    return render_template(
        "index.html",
        summary   = cache["summary"],
        ml        = cache["ml"],
        row_count = len(cache["df"]),
        show_dashboard = True,
    )


# ── REST APIs: JSON Telemetry Feeds ──────────────────────────────────────────

@app.route("/api/dashboard-summary")
def api_summary():
    if not ensure_session_data():
        return jsonify({"error": "No database context loaded"}), 400
    cache = get_cached_data(session["dataset_path"])
    return jsonify(cache["summary"])


@app.route("/api/crime-trends")
def api_trends():
    if not ensure_session_data():
        return jsonify({"error": "No database context loaded"}), 400
    cache = get_cached_data(session["dataset_path"])
    return jsonify(cache["trends_data"])


@app.route("/api/crime-types")
def api_types():
    if not ensure_session_data():
        return jsonify({"error": "No database context loaded"}), 400
    cache = get_cached_data(session["dataset_path"])
    return jsonify(cache["types_data"])


@app.route("/api/weapons")
def api_weapons():
    if not ensure_session_data():
        return jsonify({"error": "No database context loaded"}), 400
    cache = get_cached_data(session["dataset_path"])
    return jsonify(cache["weapons_data"])


@app.route("/api/top-cities")
def api_top_cities():
    if not ensure_session_data():
        return jsonify({"error": "No database context loaded"}), 400
    cache = get_cached_data(session["dataset_path"])
    return jsonify(cache["cities_data"])


@app.route("/api/heatmap")
def api_heatmap():
    if not ensure_session_data():
        return jsonify({"error": "No database context loaded"}), 400
    cache = get_cached_data(session["dataset_path"])
    return jsonify(cache["heatmap_data"])


@app.route("/api/predictions")
def api_predictions():
    if not ensure_session_data():
        return jsonify({"error": "No database context loaded"}), 400
    
    cache = get_cached_data(session["dataset_path"])
    ml = cache["ml"]
    if "error" in ml:
        return jsonify(ml), 400
        
    preds = ml.get("predictions", {})
    pred_labels = sorted([int(yr) for yr in preds.keys()])
    
    # Secure numeric conversion and string/int key lookup matching
    pred_values = []
    for yr in pred_labels:
        if yr in preds:
            pred_values.append(preds[yr])
        elif str(yr) in preds:
            pred_values.append(preds[str(yr)])
        else:
            pred_values.append(0)
    
    return jsonify({
        "historical_labels": ml.get("historical_years", []),
        "historical_values": ml.get("historical_counts", []),
        "predicted_labels": pred_labels,
        "predicted_values": pred_values,
        "r2_score": ml.get("r2_score", 0)
    })


@app.route("/api/correlation")
def api_correlation():
    if not ensure_session_data():
        return jsonify({"error": "No database context loaded"}), 400
    cache = get_cached_data(session["dataset_path"])
    return jsonify(cache["correlation_data"])


@app.route("/api/filter-options")
def api_filter_options():
    if not ensure_session_data():
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


@app.route("/filter-data")
def filter_data():
    if not ensure_session_data():
        return jsonify({"error": "No database context loaded"}), 400
    
    cache = get_cached_data(session["dataset_path"])
    df = cache["df"]

    # Ingest query constraints
    year = request.args.get("year", "All")
    city = request.args.get("city", "All")
    crime_type = request.args.get("crime_type", "All")

    # Run query constraints in Pandas
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

    # If results are empty, return safe mock parameters
    if len(filtered_df) == 0:
        return jsonify({
            "summary": {
                "total_cases": 0,
                "closed_cases": 0,
                "open_cases": 0,
                "top_city": "N/A",
                "top_weapon": "N/A",
                "top_crime": "N/A",
                "closure_rate": "0.0%"
            },
            "crime_trends": {"months": [], "counts": []},
            "crime_types": {"crime_types": [], "counts": []},
            "weapons": {"weapons": [], "counts": []},
            "heatmap": {"cities": [], "months": [], "matrix": []},
            "predictions": {
                "historical_labels": [],
                "historical_values": [],
                "predicted_labels": [],
                "predicted_values": [],
                "r2_score": 0
            },
            "correlation": {"data": []},
            "top_cities": {"cities": [], "counts": []}
        })

    # Calculations
    summary = get_summary(filtered_df)
    ml_result = predict_future_crimes(filtered_df, GRAPHS_DIR)

    preds = ml_result.get("predictions", {}) if "error" not in ml_result else {}
    pred_labels = sorted([int(yr) for yr in preds.keys()])
    
    # Secure numeric conversion and string/int key lookup matching
    pred_values = []
    for yr in pred_labels:
        if yr in preds:
            pred_values.append(preds[yr])
        elif str(yr) in preds:
            pred_values.append(preds[str(yr)])
        else:
            pred_values.append(0)
    
    predictions_data = {
        "historical_labels": ml_result.get("historical_years", []),
        "historical_values": ml_result.get("historical_counts", []),
        "predicted_labels": pred_labels,
        "predicted_values": pred_values,
        "r2_score": ml_result.get("r2_score", 0)
    }

    return jsonify({
        "summary": summary,
        "crime_trends": get_trends_data(filtered_df),
        "crime_types": get_types_data(filtered_df),
        "weapons": get_weapons_data(filtered_df),
        "heatmap": get_heatmap_data(filtered_df),
        "predictions": predictions_data,
        "correlation": get_correlation_data(filtered_df),
        "top_cities": get_cities_data(filtered_df)
    })


# ── Upgraded REST APIs: Phase 4 Model Intelligence ───────────────────────────

@app.route("/api/ml/predictions")
def api_ml_predictions():
    if not ensure_session_data():
        return jsonify({"error": "No database context loaded"}), 400
    cache = get_cached_data(session["dataset_path"])
    lr = cache["lr_package"]
    if "error" in lr:
        return jsonify(lr), 400
    return jsonify(lr)


@app.route("/api/ml/accuracy")
def api_ml_accuracy():
    if not ensure_session_data():
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


@app.route("/api/ml/hotspots")
def api_ml_hotspots():
    if not ensure_session_data():
        return jsonify({"error": "No database context loaded"}), 400
    cache = get_cached_data(session["dataset_path"])
    km = cache["km_package"]
    if "error" in km:
        return jsonify(km), 400
    return jsonify(km)


@app.route("/api/ml/anomalies")
def api_ml_anomalies():
    if not ensure_session_data():
        return jsonify({"error": "No database context loaded"}), 400
    cache = get_cached_data(session["dataset_path"])
    iso = cache["iso_package"]
    if "error" in iso:
        return jsonify(iso), 400
    return jsonify(iso)


@app.route("/api/ml/predict-category", methods=["GET", "POST"])
def api_ml_predict_category():
    if not ensure_session_data():
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
        return jsonify({"error": "Missing parameters for dynamic inference."}), 400
        
    try:
        res = predict_crime_category(
            rf,
            city=city,
            month=int(month),
            victim_age=int(victim_age),
            victim_gender=victim_gender,
            weapon_used=weapon_used
        )
        return jsonify(res)
    except Exception as e:
        return jsonify({"error": f"AI Inference execution failed: {e}"}), 400


# ── Route: Download Report ────────────────────────────────────────────────────
@app.route("/download")
def download():
    """Generates a plain-text summary report and sends it as a download."""
    if not ensure_session_data():
        return redirect(url_for("index"))

    cache = get_cached_data(session["dataset_path"])
    s  = cache["summary"]
    ml = cache["ml"]
    preds = ml.get("predictions", {})
    pred_lines = "\n".join(f"  {yr}: {cnt} cases" for yr, cnt in preds.items())

    report = f"""
CRIME DATA ANALYSIS REPORT
===========================
Generated by AI-Powered Crime Data Analysis System

DATASET SUMMARY
---------------
Total Cases     : {s['total_cases']:,}
Closed Cases    : {s['closed_cases']:,}
Open Cases      : {s['open_cases']:,}
Closure Rate    : {s['closure_rate']}
Top Crime City  : {s['top_city']}
Most Used Weapon: {s['top_weapon']}

ML PREDICTION (Linear Regression)
-----------------------------------
Model R² Score  : {ml.get('r2_score', 'N/A')}
Forecasted Crime Counts:
{pred_lines}

CHARTS GENERATED
----------------
1. Bar Chart   – Top 10 Cities by Crime Count
2. Pie Chart   – Crime Domain Distribution
3. Heatmap     – Monthly Crime Frequency by City
4. Line Chart  – Crime Trend Over the Years
5. Scatter Plot– Victim Age vs Police Deployed
6. Prediction  – Future Crime Trend (ML)

===========================
End of Report
""".strip()

    report_path = os.path.join(GRAPHS_DIR, "crime_report.txt")
    with open(report_path, "w", encoding="utf-8") as fh:
        fh.write(report)

    return send_file(report_path, as_attachment=True,
                     download_name="crime_analysis_report.txt")


# ── Entry point ───────────────────────────────────────────────────────────────
# The app is now run via run.py at the backend root folder.