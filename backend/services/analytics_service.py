"""
backend/services/analytics_service.py
=====================================
Business service layer for compiling dashboard analytics, KPIs, and visual data models.
Relocates all profiling metrics calculations cleanly from preprocess.py.
"""

import pandas as pd
import numpy as np
from utils.logger import logger

def get_summary(df: pd.DataFrame) -> dict:
    """
    Returns high-level KPIs shown on the dashboard cards.
    """
    logger.debug("Calculating dashboard KPI card aggregates.")
    total = len(df)
    
    closed = 0
    if "Case Closed" in df.columns:
        closed = int((df["Case Closed"].str.lower() == "yes").sum())
        
    top_city = "N/A"
    if "City" in df.columns and len(df) > 0:
        top_city = df["City"].value_counts().idxmax()
        
    top_weapon = "N/A"
    if "Weapon Used" in df.columns and len(df) > 0:
        top_weapon = df["Weapon Used"].value_counts().idxmax()
        
    top_crime = "N/A"
    if "Crime Description" in df.columns and len(df) > 0:
        top_crime = df["Crime Description"].value_counts().idxmax()
        
    open_cases = total - closed
    closure_rate = f"{(closed / total * 100):.1f}%" if total > 0 else "0%"
    
    return {
        "total_cases": total,
        "closed_cases": closed,
        "open_cases": open_cases,
        "top_city": top_city,
        "top_weapon": top_weapon,
        "top_crime": top_crime,
        "closure_rate": closure_rate,
    }


def get_trends_data(df: pd.DataFrame) -> dict:
    """Groups counts by Month (1-12) to return annual monthly trends."""
    if "Month" not in df.columns or len(df) == 0:
        return {"months": [], "counts": []}
        
    monthly = df[df["Month"] > 0].groupby("Month").size()
    months_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    counts = []
    labels = []
    for m_num in range(1, 13):
        labels.append(months_names[m_num - 1])
        counts.append(int(monthly.get(m_num, 0)))
        
    return {
        "months": labels,
        "counts": counts
    }


def get_types_data(df: pd.DataFrame) -> dict:
    """Classifies Crime Description counts into target categories and Others."""
    col = next((c for c in df.columns if any(k in c.lower() for k in ["domain", "type", "description"])), None)
    if col is None or len(df) == 0:
        return {"crime_types": [], "counts": []}
        
    counts = df[col].value_counts()
    target_categories = ["Theft", "Assault", "Robbery", "Fraud", "Kidnapping"]
    data_map = {cat: 0 for cat in target_categories}
    others_count = 0
    
    for crime, count in counts.items():
        matched = False
        for target in target_categories:
            if target.lower() in str(crime).lower():
                data_map[target] += int(count)
                matched = True
                break
        if not matched:
            others_count += int(count)
            
    crime_types = target_categories + ["Others"]
    counts_list = [data_map[cat] for cat in target_categories] + [others_count]
    
    return {
        "crime_types": crime_types,
        "counts": counts_list
    }


def get_weapons_data(df: pd.DataFrame) -> dict:
    """Returns top 8 weapons used in crimes and their counts."""
    col = "Weapon Used"
    if col not in df.columns or len(df) == 0:
        return {"weapons": [], "counts": []}
        
    counts = df[col].value_counts().head(8)
    return {
        "weapons": [str(x) for x in counts.index],
        "counts": [int(x) for x in counts.values]
    }


def get_heatmap_data(df: pd.DataFrame) -> dict:
    """Returns an 8-city by 12-month matrix representing monthly frequency counts."""
    city_col = next((c for c in df.columns if "city" in c.lower()), None)
    if city_col is None or "Month" not in df.columns or len(df) == 0:
        return {"cities": [], "months": [], "matrix": []}
        
    top_cities = df[city_col].value_counts().head(8).index.tolist()
    if not top_cities:
        return {"cities": [], "months": [], "matrix": []}
        
    sub = df[df[city_col].isin(top_cities)]
    pivot = sub.groupby(["Month", city_col]).size().unstack(fill_value=0)
    
    months_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    matrix = []
    
    for m_num in range(1, 13):
        row = []
        for city in top_cities:
            count = int(pivot.loc[m_num, city]) if m_num in pivot.index and city in pivot.columns else 0
            row.append(count)
        matrix.append(row)
        
    return {
        "cities": top_cities,
        "months": months_names,
        "matrix": matrix
    }


def get_correlation_data(df: pd.DataFrame) -> dict:
    """Pulls 1,000 random samples of Victim Age vs Police Deployed grouped by Crime Domain."""
    age_col = next((c for c in df.columns if "age" in c.lower()), None)
    police_col = next((c for c in df.columns if "police" in c.lower()), None)
    domain_col = next((c for c in df.columns if "domain" in c.lower()), None)
    
    if age_col is None or police_col is None or len(df) == 0:
        return {"data": []}
        
    cols = [age_col, police_col]
    if domain_col and domain_col in df.columns:
        cols.append(domain_col)
        
    sample = df[cols].dropna()
    if len(sample) == 0:
        return {"data": []}
        
    sample = sample.sample(min(1000, len(sample)), random_state=42)
    
    points = []
    for _, r in sample.iterrows():
        points.append({
            "x": int(r[age_col]),
            "y": int(r[police_col]),
            "group": str(r[domain_col]) if domain_col and domain_col in r else "General"
        })
        
    return {"data": points}


def get_cities_data(df: pd.DataFrame) -> dict:
    """Returns top 10 cities by crime count for bar chart representation."""
    col = next((c for c in df.columns if "city" in c.lower()), None)
    if col is None or len(df) == 0:
        return {"cities": [], "counts": []}
        
    counts = df[col].value_counts().head(10)
    return {
        "cities": [str(x) for x in counts.index],
        "counts": [int(x) for x in counts.values]
    }
