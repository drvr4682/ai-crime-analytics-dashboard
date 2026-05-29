"""
preprocess.py
=============
Handles all data cleaning and preparation steps.
Every function is explained in detail below.
"""

import pandas as pd
import numpy as np


def load_and_clean(filepath: str) -> pd.DataFrame:
    """
    Reads a CSV file and returns a clean DataFrame.

    Steps performed:
      1. Read CSV with UTF-8-sig encoding (handles BOM character in Windows CSVs)
      2. Strip leading/trailing spaces from column names
      3. Drop fully duplicate rows
      4. Fill or drop missing values sensibly
      5. Parse date columns → extract Year and Month
      6. Normalise text columns to Title Case

    Parameters
    ----------
    filepath : str
        Absolute or relative path to the CSV file.

    Returns
    -------
    pd.DataFrame
        A clean, analysis-ready DataFrame.
    """

    # ── 1. Read CSV ────────────────────────────────────────────────────────────
    # encoding='utf-8-sig' silently removes the BOM (﻿) that Windows adds to CSVs.
    df = pd.read_csv(filepath, encoding="utf-8-sig")

    # ── 2. Clean column names ──────────────────────────────────────────────────
    # Removes accidental spaces: "  City " → "City"
    df.columns = df.columns.str.strip()

    # ── 3. Drop full duplicates ────────────────────────────────────────────────
    df.drop_duplicates(inplace=True)

    # ── 4. Handle missing values ───────────────────────────────────────────────
    # For text/categorical columns → fill with "Unknown"
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].fillna("Unknown").str.strip()

    # For numeric columns → fill with the column median
    for col in df.select_dtypes(include=[np.number]).columns:
        df[col] = df[col].fillna(df[col].median())

    # ── 5. Parse dates → Year / Month ─────────────────────────────────────────
    # We try to convert the first column that looks like a date.
    date_candidates = [c for c in df.columns if "date" in c.lower()]
    for dc in date_candidates:
        try:
            df[dc] = pd.to_datetime(df[dc], dayfirst=True, errors="coerce")
        except Exception:
            pass

    # Extract Year and Month from "Date of Occurrence" if it exists
    occ_col = next((c for c in df.columns if "occurrence" in c.lower()), None)
    if occ_col and pd.api.types.is_datetime64_any_dtype(df[occ_col]):
        df["Year"] = df[occ_col].dt.year.fillna(0).astype(int)
        df["Month"] = df[occ_col].dt.month.fillna(0).astype(int)
    else:
        # Fallback: try any datetime column
        dt_cols = df.select_dtypes(include="datetime64").columns
        if len(dt_cols) > 0:
            df["Year"] = df[dt_cols[0]].dt.year.fillna(0).astype(int)
            df["Month"] = df[dt_cols[0]].dt.month.fillna(0).astype(int)

    # ── 6. Normalise key text columns ─────────────────────────────────────────
    for col in ["City", "Crime Description", "Weapon Used", "Crime Domain"]:
        if col in df.columns:
            df[col] = df[col].str.title()

    return df


def get_summary(df: pd.DataFrame) -> dict:
    """
    Returns a dictionary of high-level KPIs shown on the dashboard cards.

    Keys returned
    -------------
    total_cases    : int   – total number of rows
    closed_cases   : int   – rows where Case Closed == 'Yes'
    top_city       : str   – city with the most crimes
    top_weapon     : str   – most frequently used weapon
    open_cases     : int   – rows where Case Closed == 'No'
    closure_rate   : str   – percentage of cases closed
    """

    total = len(df)

    closed = 0
    if "Case Closed" in df.columns:
        closed = int((df["Case Closed"].str.lower() == "yes").sum())

    top_city = "N/A"
    if "City" in df.columns:
        top_city = df["City"].value_counts().idxmax()

    top_weapon = "N/A"
    if "Weapon Used" in df.columns:
        top_weapon = df["Weapon Used"].value_counts().idxmax()

    top_crime = "N/A"
    if "Crime Description" in df.columns:
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


def get_trends_data(df) -> dict:
    """Groups counts by Month (1-12) to return annual monthly trends."""
    if "Month" not in df.columns:
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


def get_types_data(df) -> dict:
    """Classifies Crime Description counts into target categories and Others."""
    col = next((c for c in df.columns if any(k in c.lower() for k in ["domain", "type", "description"])), None)
    if col is None:
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


def get_weapons_data(df) -> dict:
    """Returns top 8 weapons used in crimes and their counts."""
    col = "Weapon Used"
    if col not in df.columns:
        return {"weapons": [], "counts": []}
    
    counts = df[col].value_counts().head(8)
    return {
        "weapons": [str(x) for x in counts.index],
        "counts": [int(x) for x in counts.values]
    }


def get_heatmap_data(df) -> dict:
    """Returns an 8-city by 12-month matrix representing monthly frequency counts."""
    city_col = next((c for c in df.columns if "city" in c.lower()), None)
    if city_col is None or "Month" not in df.columns:
        return {"cities": [], "months": [], "matrix": []}
    
    top_cities = df[city_col].value_counts().head(8).index.tolist()
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


def get_correlation_data(df) -> dict:
    """Pulls 1,000 random samples of Victim Age vs Police Deployed grouped by Crime Domain."""
    age_col = next((c for c in df.columns if "age" in c.lower()), None)
    police_col = next((c for c in df.columns if "police" in c.lower()), None)
    domain_col = next((c for c in df.columns if "domain" in c.lower()), None)
    
    if age_col is None or police_col is None:
        return {"data": []}
    
    sample = df[[age_col, police_col] + ([domain_col] if domain_col else [])].dropna()
    sample = sample.sample(min(1000, len(sample)), random_state=42)
    
    points = []
    for _, r in sample.iterrows():
        points.append({
            "x": int(r[age_col]),
            "y": int(r[police_col]),
            "group": str(r[domain_col]) if domain_col else "General"
        })
        
    return {"data": points}


def get_cities_data(df) -> dict:
    """Returns top 10 cities by crime count for bar chart representation."""
    col = next((c for c in df.columns if "city" in c.lower()), None)
    if col is None:
        return {"cities": [], "counts": []}
    
    counts = df[col].value_counts().head(10)
    return {
        "cities": [str(x) for x in counts.index],
        "counts": [int(x) for x in counts.values]
    }