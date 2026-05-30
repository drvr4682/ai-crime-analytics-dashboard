"""
backend/analysis/anomaly_analysis.py
====================================
Analyzes and aggregates Isolation Forest anomaly results.
Generates structured security intelligence warnings based on outlier density and severe incidents.
"""

from utils.logger import logger

def get_anomaly_summary(iso_package: dict) -> dict:
    """
    Summarizes Isolation Forest anomalies, providing percentages, threat alerts,
    and a tactical threat classification level (System Secure / Elevated Risk / Critical Threat).
    """
    if not iso_package or "error" in iso_package or "metrics" not in iso_package:
        logger.warning("Empty or invalid Isolation Forest package provided to anomaly analyzer.")
        return {
            "anomaly_count": 0,
            "anomaly_percent": 0.0,
            "threat_classification": "UNKNOWN",
            "tactical_alert_summary": "Anomaly detection engine offline."
        }
        
    metrics = iso_package["metrics"]
    count = metrics.get("anomaly_count", 0)
    percent = metrics.get("anomaly_percent", 0.0)
    
    # Assess threat classification
    if percent > 3.0:
        threat_class = "CRITICAL DEVIATION THREAT"
        tactical_summary = f"CRITICAL ANOMALY PROFILE: Suddden behavioral surges isolated across {count} incident clusters. Immediate patrol reinforcement recommended."
    elif percent > 1.0:
        threat_class = "ELEVATED CONFLICT WARNING"
        tactical_summary = f"ELEVATED INCIDENT SPIKES: Outlier patterns detected at {percent:.2f}% rate ({count} cases). Threat escalation index moderate."
    else:
        threat_class = "STABILIZED SECTOR PROFILE"
        tactical_summary = "STABILIZED PATTERNS: System reports baseline incident anomalies. Outlier contamination index nominal."
        
    return {
        "anomaly_count": count,
        "anomaly_percent": percent,
        "threat_classification": threat_class,
        "tactical_alert_summary": tactical_summary
    }
