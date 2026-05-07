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

from preprocess import load_and_clean, get_summary
from analysis   import generate_all
from model      import predict_future_crimes

# ── Flask init ─────────────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = "crime-analysis-secret-2024"   # needed for session storage

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR  = os.path.join(BASE_DIR, "uploads")
GRAPHS_DIR  = os.path.join(os.path.dirname(__file__), "static", "graphs")
DATA_DIR    = os.path.join(BASE_DIR, "data")

ALLOWED = {"csv"}

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


# ── Route: Upload & Analyse ───────────────────────────────────────────────────
@app.route("/upload", methods=["POST"])
def upload():
    """
    Handles CSV upload (or uses the built-in dataset if no file is uploaded).
    Steps:
      1. Save uploaded file to uploads/
      2. Clean it with preprocess.py
      3. Generate graphs with analysis.py
      4. Run ML prediction with model.py
      5. Store summary in session → redirect to /dashboard
    """
    filepath = None

    # Check if user uploaded a file
    if "file" in request.files and request.files["file"].filename != "":
        f = request.files["file"]
        if not allowed_file(f.filename):
            return jsonify({"error": "Only CSV files are allowed."}), 400
        filename = secure_filename(f.filename)
        filepath = os.path.join(UPLOAD_DIR, filename)
        f.save(filepath)
    else:
        # Fall back to the built-in sample dataset
        filepath = os.path.join(DATA_DIR, "crime_dataset_india.csv")
        if not os.path.exists(filepath):
            return jsonify({"error": "No dataset found. Please upload a CSV file."}), 400

    # ── Process ───────────────────────────────────────────────────────────────
    try:
        df = load_and_clean(filepath)
    except Exception as e:
        return jsonify({"error": f"Failed to read CSV: {e}"}), 400

    summary   = get_summary(df)
    graphs    = generate_all(df, GRAPHS_DIR)
    ml_result = predict_future_crimes(df, GRAPHS_DIR)

    # Store everything in session so /dashboard can read it
    session["summary"]   = summary
    session["graphs"]    = {k: v for k, v in graphs.items() if v}
    session["ml"]        = ml_result
    session["row_count"] = len(df)

    return redirect(url_for("dashboard"))


# ── Route: Dashboard ──────────────────────────────────────────────────────────
@app.route("/dashboard")
def dashboard():
    """
    Renders the dashboard page with all processed data.
    If the session is empty (user navigated directly), use the built-in dataset.
    """
    if "summary" not in session:
        # Auto-process the built-in dataset
        filepath = os.path.join(DATA_DIR, "crime_dataset_india.csv")
        if os.path.exists(filepath):
            df        = load_and_clean(filepath)
            session["summary"]   = get_summary(df)
            session["graphs"]    = {k: v for k, v in generate_all(df, GRAPHS_DIR).items() if v}
            session["ml"]        = predict_future_crimes(df, GRAPHS_DIR)
            session["row_count"] = len(df)
        else:
            return redirect(url_for("index"))

    return render_template(
        "index.html",
        summary   = session["summary"],
        graphs    = session["graphs"],
        ml        = session["ml"],
        row_count = session.get("row_count", 0),
        show_dashboard = True,
    )


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
if __name__ == "__main__":
    print("\n" + "="*55)
    print("  AI-Powered Crime Data Analysis System")
    print("  http://127.0.0.1:5000")
    print("="*55 + "\n")
    app.run(debug=True, port=5000)