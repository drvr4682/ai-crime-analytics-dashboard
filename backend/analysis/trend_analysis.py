"""
trend_analysis.py
=================
Computes trend metrics, month-over-month growth, and YoY category growth changes.
"""

import pandas as pd
import numpy as np

def get_monthly_growth_rate(df: pd.DataFrame) -> float:
    """
    Calculates the average month-over-month (MoM) crime count percentage growth.
    """
    if "Month" not in df.columns or len(df) == 0:
        return 0.0
        
    monthly_counts = df.groupby("Month").size().sort_index()
    if len(monthly_counts) < 2:
        return 0.0
        
    pct_changes = monthly_counts.pct_change().dropna()
    return float(pct_changes.mean() * 100)


def detect_peak_months(df: pd.DataFrame) -> list:
    """
    Identifies the months with the highest crime counts, returning standardized month abbreviations.
    """
    if "Month" not in df.columns or len(df) == 0:
        return []
        
    monthly_counts = df.groupby("Month").size()
    if len(monthly_counts) == 0:
        return []
        
    months_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    # Isolate top 2 peak months
    top_months = monthly_counts.nlargest(2).index.tolist()
    return [months_names[m - 1] for m in top_months if 1 <= m <= 12]


def find_fastest_growing_category(df: pd.DataFrame) -> dict:
    """
    Analyzes YoY crime count changes per category and isolates the category
    with the highest positive percentage growth rate between the last two active years.
    """
    if "Year" not in df.columns or "Crime Description" not in df.columns or len(df) == 0:
        return {"category": "N/A", "growth": 0.0}
        
    active_years = sorted([int(y) for y in df["Year"].dropna().unique() if y > 0])
    if len(active_years) < 2:
        # Fallback if we only have one year: just return the highest count category
        top_cat = df["Crime Description"].value_counts().head(1)
        if len(top_cat) > 0:
            return {"category": str(top_cat.index[0]), "growth": 0.0, "is_fallback": True}
        return {"category": "N/A", "growth": 0.0}
        
    year_prev, year_curr = active_years[-2], active_years[-1]
    
    # Counts per category for both years
    counts_prev = df[df["Year"] == year_prev]["Crime Description"].value_counts()
    counts_curr = df[df["Year"] == year_curr]["Crime Description"].value_counts()
    
    growth_rates = {}
    for cat in counts_curr.index:
        prev_val = counts_prev.get(cat, 0)
        curr_val = counts_curr[cat]
        
        # Calculate percent growth safely (ignore categories with very small baselines to avoid massive anomalies)
        if prev_val > 5:
            growth = ((curr_val - prev_val) / prev_val) * 100
            growth_rates[cat] = growth
            
    if not growth_rates:
        # Fallback if no category meets baseline count
        top_cat = df["Crime Description"].value_counts().head(1)
        if len(top_cat) > 0:
            return {"category": str(top_cat.index[0]), "growth": 0.0, "is_fallback": True}
        return {"category": "N/A", "growth": 0.0}
        
    fastest_cat = max(growth_rates, key=growth_rates.get)
    return {
        "category": str(fastest_cat),
        "growth": round(float(growth_rates[fastest_cat]), 1),
        "is_fallback": False
    }
