"""
backend/services/dashboard_service.py
=====================================
Orchestrates in-memory data caching and session parameter auto-hydration.
Centralizes the global _DATA_CACHE singleton to enable instant, sub-millisecond dynamic responses.
"""

import os
from flask import session
from utils.logger import logger
from utils.data_loader import load_and_clean
from services.analytics_service import (
    get_summary, get_trends_data, get_types_data, get_weapons_data, 
    get_heatmap_data, get_correlation_data, get_cities_data
)
from services.ml_service import train_all_models

# ── In-Memory Singleton Data Cache ──────────────────────────────────────────
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
    "lr_package": None,
    "rf_package": None,
    "km_package": None,
    "iso_package": None
}

def get_cached_data(filepath: str) -> dict:
    """
    Looks up or hydrates the central data cache. On a cache miss, trains Scikit-Learn
    models and aggregates raw timeline/frequency matrices in-memory.
    """
    global _DATA_CACHE
    
    if _DATA_CACHE["filepath"] == filepath and _DATA_CACHE["df"] is not None:
        logger.debug(f"Cache HIT for telemetry path: {filepath}")
        return _DATA_CACHE
        
    logger.info(f"Cache MISS for telemetry path. Building indexes: {filepath}")
    df = load_and_clean(filepath)
    
    # Pre-train all Scikit-Learn pipelines
    ml_packages = train_all_models(df)
    lr_res = ml_packages["lr_package"]
    
    # Assemble cache object
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
        "rf_package": ml_packages["rf_package"],
        "km_package": ml_packages["km_package"],
        "iso_package": ml_packages["iso_package"]
    }
    
    return _DATA_CACHE


def ensure_session_data(data_dir: str) -> bool:
    """
    Ensures that session parameters have a loaded dataset.
    Auto-hydrates baseline Indian dataset CSV if not present.
    """
    if "dataset_path" not in session:
        filepath = os.path.join(data_dir, "crime_dataset_india.csv")
        if os.path.exists(filepath):
            session["dataset_path"] = filepath
            logger.info("Session context initialized with baseline dataset.")
            try:
                get_cached_data(filepath)
                return True
            except Exception as e:
                logger.error(f"Failed to pre-cache default session context: {e}")
                return False
        logger.warning(f"No baseline dataset found at: {filepath}")
        return False
    else:
        try:
            get_cached_data(session["dataset_path"])
            return True
        except Exception as e:
            logger.error(f"Failed to read dataset session cache context: {e}")
            return False
