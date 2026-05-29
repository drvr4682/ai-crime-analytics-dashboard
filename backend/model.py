"""
model.py
========
Uses Linear Regression (Scikit-learn) to predict future crime counts
based on historical yearly data, then saves a prediction chart.
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

DARK_BG = "#0d1117"
CARD_BG = "#161b22"
ACCENT  = "#00d4aa"
ACCENT2 = "#ff6b6b"
TEXT    = "#e6edf3"
GRID    = "#21262d"


def predict_future_crimes(df, graphs_dir: str, forecast_years: int = 5) -> dict:
    """
    Trains a Linear Regression model on yearly crime counts and predicts
    the next `forecast_years` years.

    How it works
    ------------
    1. Count crimes per year  →  X = [year], y = [count]
    2. Fit LinearRegression(X, y)  →  learns a straight-line trend
    3. Predict for (last_year + 1) … (last_year + forecast_years)
    4. Plot historical data + predicted line + forecast points
    5. Return model score (R²) and the predictions dict

    Parameters
    ----------
    df            : cleaned DataFrame from preprocess.py
    graphs_dir    : folder to save the chart PNG
    forecast_years: how many years ahead to predict (default 5)

    Returns
    -------
    dict with keys:
        predictions  : {year: predicted_count}
        r2_score     : float (model accuracy 0–1)
        graph        : PNG filename
    """

    if "Year" not in df.columns:
        return {"error": "No Year column found in dataset."}

    # ── Prepare training data ──────────────────────────────────────────────────
    yearly = df[df["Year"] > 0].groupby("Year").size().reset_index(name="count")
    if len(yearly) < 2:
        return {"error": "Not enough yearly data to train a model."}

    X = yearly["Year"].values.reshape(-1, 1)   # shape (n, 1) – required by sklearn
    y = yearly["count"].values

    # ── Train model ───────────────────────────────────────────────────────────
    model = LinearRegression()
    model.fit(X, y)
    r2 = float(model.score(X, y))

    # ── Predict future years ──────────────────────────────────────────────────
    last_year = int(yearly["Year"].max())
    future_years = np.arange(last_year + 1, last_year + forecast_years + 1).reshape(-1, 1)
    future_counts = model.predict(future_years).astype(int)
    future_counts = np.clip(future_counts, 0, None)   # no negative crimes

    predictions = {int(y): int(c) for y, c in zip(future_years.flatten(), future_counts)}

    # ── Return raw data arrays instead of generating PNG charts ───────────────
    return {
        "predictions": predictions,
        "r2_score": round(r2, 4),
        "historical_years": [int(yr) for yr in yearly["Year"].values],
        "historical_counts": [int(cnt) for cnt in y]
    }