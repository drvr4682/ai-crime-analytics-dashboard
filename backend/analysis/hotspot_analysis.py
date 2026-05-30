"""
backend/analysis/hotspot_analysis.py
====================================
Analyzes and aggregates KMeans city-clustering risk tiers.
Translates statistical cluster labels into descriptive threat level metrics for the Command Center.
"""

from utils.logger import logger

def get_hotspot_summary_insights(km_package: dict) -> dict:
    """
    Summarizes the risk tiers from KMeans hotspot clustering.
    Provides counts, identifies high-risk urban epicenters, and yields tactical observations.
    """
    if not km_package or "error" in km_package or "hotspots" not in km_package:
        logger.warning("Empty or invalid KMeans package provided to hotspot analyzer.")
        return {
            "high_risk_count": 0,
            "medium_risk_count": 0,
            "low_risk_count": 0,
            "tactical_alert_text": "System cluster telemetry currently unavailable."
        }
        
    hotspots = km_package["hotspots"]
    
    high_cities = [hs["city"] for hs in hotspots if hs["risk_level"] == "High Risk"]
    medium_cities = [hs["city"] for hs in hotspots if hs["risk_level"] == "Medium Risk"]
    low_cities = [hs["city"] for hs in hotspots if hs["risk_level"] == "Low Risk"]
    
    # Compile a tactical warning based on the high risk centers
    if len(high_cities) > 0:
        cities_str = ", ".join(high_cities[:3])
        if len(high_cities) > 3:
            cities_str += f" (+{len(high_cities) - 3} others)"
        tactical_alert_text = f"CRITICAL INCIDENT THREAT: {len(high_cities)} major urban epicenter(s) labeled High Risk, led by: {cities_str}. Immediate deployment recommended."
    else:
        tactical_alert_text = "SECURE SECTOR ENVELOPE: All active urban sectors are currently clustered within stable risk envelopes."
        
    return {
        "high_risk_count": len(high_cities),
        "medium_risk_count": len(medium_cities),
        "low_risk_count": len(low_cities),
        "tactical_alert_text": tactical_alert_text,
        "high_risk_cities": high_cities,
        "medium_risk_cities": medium_cities,
        "low_risk_cities": low_cities
    }
