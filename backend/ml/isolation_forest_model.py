"""
isolation_forest_model.py
=========================
Identifies highly anomalous crime incidents using Scikit-Learn IsolationForest.
Generates structured severity-based alerts with customized explanations.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from ml.preprocessing import clean_and_prepare_features, encode_categorical

def run_isolation_forest_anomalies(df: pd.DataFrame) -> dict:
    """
    Trains an Isolation Forest on incident telemetry, isolates the top 2% of outliers,
    and returns anomaly metrics alongside structured intelligence alert cards.
    """
    required_cols = ["City", "Weapon Used", "Crime Domain", "Victim Age", "Police Deployed"]
    cols_to_use = [col for col in required_cols if col in df.columns]
    
    if len(cols_to_use) < 2:
        return {"error": "Insufficient dataset features to execute anomaly clustering."}
        
    df_clean = clean_and_prepare_features(df)
    
    # ── Categorical encoding ────────────────────────────────────────────────────
    cat_cols = [col for col in ["City", "Weapon Used", "Crime Domain"] if col in df_clean.columns]
    df_encoded, mappings = encode_categorical(df_clean, cat_cols)
    
    # ── Feature Selection ───────────────────────────────────────────────────────
    feature_cols = []
    for col in ["City", "Weapon Used", "Crime Domain"]:
        if col in df_clean.columns:
            feature_cols.append(col + "_Encoded")
    for col in ["Victim Age", "Police Deployed"]:
        if col in df_clean.columns:
            feature_cols.append(col)
            
    X = df_encoded[feature_cols].values
    if X.shape[0] < 5:
        return {
            "anomaly_count": 0,
            "anomaly_percent": 0.0,
            "alerts": [],
            "metrics": {"anomaly_count": 0, "anomaly_percent": 0.0}
        }
        
    # ── Fit Isolation Forest ────────────────────────────────────────────────────
    # Target contamination at 2% outlier rate
    iso = IsolationForest(contamination=0.02, random_state=42)
    labels = iso.fit_predict(X)          # Inliers = 1, Outliers = -1
    scores = iso.decision_function(X)    # Lower means more anomalous
    
    df_clean["is_anomaly"] = labels
    df_clean["anomaly_score"] = scores
    
    anomalous_records = df_clean[df_clean["is_anomaly"] == -1].copy()
    
    anomaly_count = len(anomalous_records)
    anomaly_percent = (anomaly_count / len(df_clean)) * 100
    
    # ── Isolate Top 8 Most Severe Outliers ──────────────────────────────────────
    most_severe = anomalous_records.sort_values(by="anomaly_score").head(8)
    
    alerts = []
    for idx, row in most_severe.iterrows():
        city = row.get("City", "Unknown")
        crime_desc = row.get("Crime Description", "Unknown Offense").upper()
        weapon = row.get("Weapon Used", "Unknown")
        police = int(row.get("Police Deployed", 0))
        age = int(row.get("Victim Age", 0))
        
        # ── Synthesize Dynamic Threat Descriptions ──────────────────────────────
        if police > 30 and age < 15:
            msg = f"TACTICAL ESCALATION: High police deployment ({police} personnel) involving child victim (Age {age}) in {city}."
            severity = "Critical"
            badge_class = "badge-danger"
        elif weapon != "Unknown" and weapon != "None" and police <= 2:
            msg = f"SECURITY BREACH: Armed infraction ({weapon}) reported with critical lack of police presence ({police} deployed) in {city}."
            severity = "High"
            badge_class = "badge-warning"
        elif age > 80:
            msg = f"VULNERABLE DEMOGRAPHIC: Unusual target profile ({crime_desc}) isolated targeting senior citizen (Age {age}) in {city}."
            severity = "Medium"
            badge_class = "badge-info"
        else:
            msg = f"OUTLIER ANOMALY: Incident behavior profile ({crime_desc}) flagged using {weapon} in {city}."
            severity = "High"
            badge_class = "badge-warning"
            
        alerts.append({
            "id": int(idx),
            "city": city,
            "crime_type": row.get("Crime Description", "Unknown"),
            "weapon": weapon,
            "message": msg,
            "severity": severity,
            "badge_class": badge_class,
            "score": round(float(row["anomaly_score"]), 4)
        })
        
    return {
        "anomaly_count": anomaly_count,
        "anomaly_percent": round(anomaly_percent, 2),
        "alerts": alerts,
        "metrics": {
            "anomaly_count": anomaly_count,
            "anomaly_percent": round(anomaly_percent, 2)
        }
    }
