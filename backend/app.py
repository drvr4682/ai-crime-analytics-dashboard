"""
app.py
======
Flask application entry point.
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
    if "summary" not in session:
        filepath = os.path.join(DATA_DIR, "crime_dataset_india.csv")
        if os.path.exists(filepath):
            try:
                df = load_and_clean(filepath)
                session["summary"]   = get_summary(df)
                session["ml"]        = predict_future_crimes(df, GRAPHS_DIR)
                session["row_count"] = len(df)
                session["trends_data"] = get_trends_data(df)
                session["types_data"] = get_types_data(df)
                session["weapons_data"] = get_weapons_data(df)
                session["heatmap_data"] = get_heatmap_data(df)
                session["correlation_data"] = get_correlation_data(df)
                session["cities_data"] = get_cities_data(df)
                return True
            except Exception:
                return False
        return False
    return True


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
        df = load_and_clean(filepath)
    except Exception as e:
        return jsonify({"error": f"Failed to read CSV: {e}"}), 400

    summary   = get_summary(df)
    ml_result = predict_future_crimes(df, GRAPHS_DIR)

    session["summary"]   = summary
    session["ml"]        = ml_result
    session["row_count"] = len(df)
    session["trends_data"] = get_trends_data(df)
    session["types_data"] = get_types_data(df)
    session["weapons_data"] = get_weapons_data(df)
    session["heatmap_data"] = get_heatmap_data(df)
    session["correlation_data"] = get_correlation_data(df)
    session["cities_data"] = get_cities_data(df)

    return redirect(url_for("dashboard"))


# ── Route: Dashboard ──────────────────────────────────────────────────────────
@app.route("/dashboard")
def dashboard():
    """
    Renders the dashboard page with all processed data.
    """
    if not ensure_session_data():
        return redirect(url_for("index"))

    return render_template(
        "index.html",
        summary   = session["summary"],
        ml        = session["ml"],
        row_count = session.get("row_count", 0),
        show_dashboard = True,
    )


# ── REST APIs: JSON Telemetry Feeds ──────────────────────────────────────────

@app.route("/api/dashboard-summary")
def api_summary():
    if not ensure_session_data():
        return jsonify({"error": "No database context loaded"}), 400
    return jsonify(session.get("summary", {}))


@app.route("/api/crime-trends")
def api_trends():
    if not ensure_session_data():
        return jsonify({"error": "No database context loaded"}), 400
    return jsonify(session.get("trends_data", {}))


@app.route("/api/crime-types")
def api_types():
    if not ensure_session_data():
        return jsonify({"error": "No database context loaded"}), 400
    return jsonify(session.get("types_data", {}))


@app.route("/api/weapons")
def api_weapons():
    if not ensure_session_data():
        return jsonify({"error": "No database context loaded"}), 400
    return jsonify(session.get("weapons_data", {}))


@app.route("/api/top-cities")
def api_top_cities():
    if not ensure_session_data():
        return jsonify({"error": "No database context loaded"}), 400
    return jsonify(session.get("cities_data", {}))


@app.route("/api/heatmap")
def api_heatmap():
    if not ensure_session_data():
        return jsonify({"error": "No database context loaded"}), 400
    return jsonify(session.get("heatmap_data", {}))


@app.route("/api/predictions")
def api_predictions():
    if not ensure_session_data():
        return jsonify({"error": "No database context loaded"}), 400
    
    ml = session.get("ml", {})
    if "error" in ml:
        return jsonify(ml), 400
        
    preds = ml.get("predictions", {})
    pred_labels = sorted([int(yr) for yr in preds.keys()])
    pred_values = [preds[yr] for yr in pred_labels]
    
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
    return jsonify(session.get("correlation_data", {}))


# ── Route: Download Report ────────────────────────────────────────────────────
@app.route("/download")
def download():
    """Generates a plain-text summary report and sends it as a download."""
    if "summary" not in session:
        return redirect(url_for("index"))

    s  = session["summary"]
    ml = session.get("ml", {})
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