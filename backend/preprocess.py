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

    open_cases = total - closed
    closure_rate = f"{(closed / total * 100):.1f}%" if total > 0 else "0%"

    return {
        "total_cases": total,
        "closed_cases": closed,
        "open_cases": open_cases,
        "top_city": top_city,
        "top_weapon": top_weapon,
        "closure_rate": closure_rate,
    }