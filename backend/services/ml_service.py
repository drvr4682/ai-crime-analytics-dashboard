"""
backend/services/ml_service.py
==============================
Business service layer coordinating Scikit-Learn model invocations and evaluations.
Combines legacy regression projections with modern multi-model analytics pipelines.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from ml.linear_regression_model import train_linear_regression
from ml.random_forest_model import train_random_forest, predict_crime_category
from ml.kmeans_model import run_kmeans_hotspots
from ml.isolation_forest_model import run_isolation_forest_anomalies
from utils.logger import logger

def train_all_models(df: pd.DataFrame) -> dict:
    """
    Trains all four core machine learning models in parallel on ingestion/load.
    Returns standard result packages for cache synchronization.
    """
    logger.info("Initializing multi-model AI suite training cycles.")
    
    lr_res = train_linear_regression(df)
    rf_res = train_random_forest(df)
    km_res = run_kmeans_hotspots(df)
    iso_res = run_isolation_forest_anomalies(df)
    
    logger.info("AI models pre-warmed and cached successfully.")
    
    return {
        "lr_package": lr_res,
        "rf_package": rf_res,
        "km_package": km_res,
        "iso_package": iso_res
    }


def predict_future_crimes(df: pd.DataFrame, forecast_years: int = 5) -> dict:
    """
    Identical backward-compatible implementation of linear regression projections.
    Fits LinearRegression on yearly crime aggregates and returns future projections.
    """
    if "Year" not in df.columns:
        return {"error": "No Year column found in dataset."}
        
    yearly = df[df["Year"] > 0].groupby("Year").size().reset_index(name="count")
    if len(yearly) < 2:
        return {"error": "Not enough yearly data to train a model."}
        
    X = yearly["Year"].values.reshape(-1, 1)
    y = yearly["count"].values
    
    model = LinearRegression()
    model.fit(X, y)
    r2 = float(model.score(X, y))
    
    last_year = int(yearly["Year"].max())
    future_years = np.arange(last_year + 1, last_year + forecast_years + 1).reshape(-1, 1)
    future_counts = model.predict(future_years).astype(int)
    future_counts = np.clip(future_counts, 0, None)
    
    predictions = {int(y_val): int(c_val) for y_val, c_val in zip(future_years.flatten(), future_counts)}
    
    return {
        "predictions": predictions,
        "r2_score": round(r2, 4),
        "historical_years": [int(yr) for yr in yearly["Year"].values],
        "historical_counts": [int(cnt) for cnt in y]
    }


def predict_crime_class(rf_package: dict, city: str, month: int, victim_age: int, victim_gender: str, weapon_used: str) -> dict:
    """
    Wrapper for Random Forest crime classification.
    """
    return predict_crime_category(
        rf_package,
        city=city,
        month=month,
        victim_age=victim_age,
        victim_gender=victim_gender,
        weapon_used=weapon_used
    )
