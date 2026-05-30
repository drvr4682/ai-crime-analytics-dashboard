"""
backend/services/filter_service.py
==================================
Business service coordinating spatial, temporal, and offense query filtering.
Aggregates and formats timeline metrics, predictions, and hotspots for dynamic AJAX updates.
"""

import pandas as pd
from services.analytics_service import (
    get_summary, get_trends_data, get_types_data, get_weapons_data, 
    get_heatmap_data, get_correlation_data, get_cities_data
)
from services.ml_service import predict_future_crimes
from utils.logger import logger

def filter_dataset(df: pd.DataFrame, year: str = "All", city: str = "All", crime_type: str = "All") -> dict:
    """
    Applies Year, City, and Crime Type query constraints to the DataFrame.
    Returns aggregated JSON summaries and dynamic Chart.js datasets.
    """
    logger.info(f"Filtering dataset: Year={year}, City={city}, Type={crime_type}")
    
    filtered_df = df
    
    # 1. Apply Year constraint
    if year != "All":
        try:
            filtered_df = filtered_df[filtered_df["Year"] == int(year)]
        except ValueError:
            logger.warning(f"Could not convert year parameter to integer: {year}")
            
    # 2. Apply City constraint
    if city != "All":
        filtered_df = filtered_df[filtered_df["City"].str.lower() == city.lower()]
        
    # 3. Apply Crime Type constraint
    if crime_type != "All":
        filtered_df = filtered_df[filtered_df["Crime Description"].str.lower() == crime_type.lower()]
        
    logger.debug(f"Filtered DataFrame size: {len(filtered_df)}")
    
    # Handle empty filtered state
    if len(filtered_df) == 0:
        logger.info("Filter parameters yielded an empty active record set.")
        return {
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
        }
        
    # 4. Generate Aggregates
    summary = get_summary(filtered_df)
    ml_result = predict_future_crimes(filtered_df)
    
    preds = ml_result.get("predictions", {}) if "error" not in ml_result else {}
    pred_labels = sorted([int(yr) for yr in preds.keys()])
    
    # Secure numeric conversion and lookup mapping
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
    
    return {
        "summary": summary,
        "crime_trends": get_trends_data(filtered_df),
        "crime_types": get_types_data(filtered_df),
        "weapons": get_weapons_data(filtered_df),
        "heatmap": get_heatmap_data(filtered_df),
        "predictions": predictions_data,
        "correlation": get_correlation_data(filtered_df),
        "top_cities": get_cities_data(filtered_df)
    }
