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

    # ── Plot ──────────────────────────────────────────────────────────────────
    all_years_x = np.arange(yearly["Year"].min(), last_year + forecast_years + 1).reshape(-1, 1)
    trend_y = model.predict(all_years_x)

    fig, ax = plt.subplots(figsize=(11, 5))
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(CARD_BG)

    # Historical bars
    ax.bar(yearly["Year"], y, color=ACCENT, alpha=0.55,
           label="Historical", width=0.6, edgecolor="none")

    # Trend line (full range)
    ax.plot(all_years_x, trend_y, color=ACCENT2, linewidth=2,
            linestyle="--", label="Linear Trend")

    # Predicted points
    ax.scatter(future_years, future_counts, color=ACCENT2,
               s=80, zorder=5, label="Forecast")
    for fy, fc in zip(future_years.flatten(), future_counts):
        ax.annotate(str(fc), (fy, fc), textcoords="offset points",
                    xytext=(0, 8), color=TEXT, fontsize=8, ha="center")

    ax.set_title("Crime Trend Prediction (Linear Regression)",
                 fontsize=14, fontweight="bold", color=ACCENT, pad=14)
    ax.set_xlabel("Year", fontsize=10, color=TEXT)
    ax.set_ylabel("Predicted Crime Count", fontsize=10, color=TEXT)
    ax.tick_params(colors=TEXT, labelsize=9)
    ax.legend(fontsize=9, facecolor=CARD_BG, labelcolor=TEXT,
              framealpha=0.9, edgecolor=GRID)
    ax.grid(axis="y", color=GRID, linestyle="--", linewidth=0.6, alpha=0.7)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID)

    os.makedirs(graphs_dir, exist_ok=True)
    graph_path = os.path.join(graphs_dir, "prediction.png")
    fig.savefig(graph_path, bbox_inches="tight", dpi=130, facecolor=DARK_BG)
    plt.close(fig)

    return {
        "predictions": predictions,
        "r2_score": round(r2, 4),
        "graph": "prediction.png",
    }