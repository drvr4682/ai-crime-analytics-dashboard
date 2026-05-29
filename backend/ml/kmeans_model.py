"""
kmeans_model.py
===============
Clusters cities based on incident density, average police deployment,
and case resolution rate using Scikit-Learn KMeans.
Groups urban centers into: 'High Risk', 'Medium Risk', 'Low Risk'.
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from ml.evaluation import evaluate_clustering

def run_kmeans_hotspots(df: pd.DataFrame) -> dict:
    """
    Aggregates incident dataset by City, runs scaling + KMeans (3 clusters),
    computes cluster Silhouette metric, and labels hotspot danger tiers.
    """
    if "City" not in df.columns:
        return {"error": "Missing 'City' column in dataset features."}
        
    # ── 1. Aggregate City Telemetry ─────────────────────────────────────────────
    # Compute: Crime Count, Avg Police Deployed, and Resolution Rate
    city_stats = df.groupby("City").agg(
        crime_count=("City", "size"),
        avg_police=("Police Deployed", "mean") if "Police Deployed" in df.columns else ("City", lambda x: 10.0)
    ).reset_index()
    
    if "Case Closed" in df.columns:
        closure_stats = df.groupby("City")["Case Closed"].apply(
            lambda x: (x.str.lower() == "yes").sum() / len(x) if len(x) > 0 else 0.0
        ).reset_index(name="closure_rate")
        city_stats = city_stats.merge(closure_stats, on="City")
    else:
        city_stats["closure_rate"] = 0.5
        
    # Handle safe fallback if dataset contains very few cities (< 3)
    if len(city_stats) < 3:
        hotspots = []
        for _, row in city_stats.iterrows():
            is_high = row["crime_count"] > 1000
            hotspots.append({
                "city": row["City"],
                "crime_count": int(row["crime_count"]),
                "avg_police": round(float(row["avg_police"]), 1),
                "closure_rate": f"{row['closure_rate'] * 100:.1f}%",
                "risk_level": "High Risk" if is_high else "Low Risk",
                "risk_class": "risk-high" if is_high else "risk-low"
            })
        return {
            "hotspots": hotspots,
            "metrics": {"silhouette_score": 0.0}
        }
        
    # ── 2. Standardize Features & Cluster ───────────────────────────────────────
    features = ["crime_count", "avg_police", "closure_rate"]
    X = city_stats[features].values
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)
    
    # Compute Silhouette Coeff
    metrics = evaluate_clustering(X_scaled, labels)
    
    city_stats["cluster"] = labels
    
    # ── 3. Map Danger Tiers Deterministically ──────────────────────────────────
    # Sort cluster IDs by average crime count so lowest is Low Risk, highest is High Risk
    cluster_means = city_stats.groupby("cluster")["crime_count"].mean().sort_values()
    
    cluster_mapping = {
        cluster_means.index[0]: ("Low Risk", "risk-low"),
        cluster_means.index[1]: ("Medium Risk", "risk-medium"),
        cluster_means.index[2]: ("High Risk", "risk-high")
    }
    
    hotspots = []
    for _, row in city_stats.iterrows():
        risk_level, risk_class = cluster_mapping[row["cluster"]]
        hotspots.append({
            "city": row["City"],
            "crime_count": int(row["crime_count"]),
            "avg_police": round(float(row["avg_police"]), 1),
            "closure_rate": f"{row['closure_rate'] * 100:.1f}%",
            "risk_level": risk_level,
            "risk_class": risk_class
        })
        
    return {
        "hotspots": hotspots,
        "metrics": metrics
    }
