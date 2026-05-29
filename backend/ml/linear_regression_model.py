"""
linear_regression_model.py
==========================
Uses Linear Regression to forecast future crime count trends.
Includes train/test splits for calculating MAE, RMSE, and R² scores.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from ml.evaluation import evaluate_regression

def train_linear_regression(df: pd.DataFrame, forecast_years: int = 5) -> dict:
    """
    Groups crime occurrences per year, splits data for train/test evaluation,
    and returns a future forecast dict alongside evaluation metrics.
    """
    if "Year" not in df.columns:
        return {"error": "Missing 'Year' column in dataset features."}
        
    yearly = df[df["Year"] > 0].groupby("Year").size().reset_index(name="count")
    if len(yearly) < 2:
        return {"error": "Insufficient yearly entries to train forecasting regression."}
        
    X = yearly["Year"].values.reshape(-1, 1)
    y = yearly["count"].values
    
    # ── Train/Test Split for Evaluation ────────────────────────────────────────
    # Standard time-series split: train on early years, test on the final year.
    # Safe fallback if yearly coordinates are tiny.
    if len(yearly) >= 3:
        X_train, X_test = X[:-1], X[-1:]
        y_train, y_test = y[:-1], y[-1:]
        
        eval_model = LinearRegression()
        eval_model.fit(X_train, y_train)
        y_pred = eval_model.predict(X_test)
        metrics = evaluate_regression(y_test, y_pred)
    else:
        # Fallback to evaluating fit on training set
        eval_model = LinearRegression()
        eval_model.fit(X, y)
        y_pred = eval_model.predict(X)
        metrics = evaluate_regression(y, y_pred)
        
    # ── Fit Full Model ──────────────────────────────────────────────────────────
    model = LinearRegression()
    model.fit(X, y)
    
    # Calculate R2 on full training data to reflect trend alignment
    full_r2 = float(model.score(X, y))
    metrics["r2_score"] = round(max(full_r2, 0.0), 4)
    
    # ── Future Forecasting ──────────────────────────────────────────────────────
    last_year = int(X.max())
    future_years = np.arange(last_year + 1, last_year + forecast_years + 1).reshape(-1, 1)
    future_counts = model.predict(future_years).astype(int)
    # Clip negative values
    future_counts = np.clip(future_counts, 0, None)
    
    predictions = {int(yr): int(cnt) for yr, cnt in zip(future_years.flatten(), future_counts)}
    
    return {
        "predictions": predictions,
        "metrics": metrics,
        "historical_years": [int(x) for x in yearly["Year"].values],
        "historical_counts": [int(x) for x in y]
    }
