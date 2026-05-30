"""
backend/services/chart_service.py
=================================
Prepares and formats structured JSON payloads for frontend Chart.js components.
Ensures unified type conversions and structures for multi-model forecasts.
"""

from utils.logger import logger

def format_predictions_payload(ml_package: dict) -> dict:
    """
    Formats Scikit-Learn linear regression timeline projections into Chart.js friendly labels and arrays.
    """
    if not ml_package or "error" in ml_package:
        logger.warning("Empty or errored ML package passed to chart formatter.")
        return {
            "historical_labels": [],
            "historical_values": [],
            "predicted_labels": [],
            "predicted_values": [],
            "r2_score": 0
        }
        
    preds = ml_package.get("predictions", {})
    pred_labels = sorted([int(yr) for yr in preds.keys()])
    
    pred_values = []
    for yr in pred_labels:
        if yr in preds:
            pred_values.append(preds[yr])
        elif str(yr) in preds:
            pred_values.append(preds[str(yr)])
        else:
            pred_values.append(0)
            
    return {
        "historical_labels": ml_package.get("historical_years", []),
        "historical_values": ml_package.get("historical_counts", []),
        "predicted_labels": pred_labels,
        "predicted_values": pred_values,
        "r2_score": ml_package.get("r2_score", 0)
    }
