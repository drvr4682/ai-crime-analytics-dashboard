"""
preprocessing.py
================
Central data preprocessing pipeline for the CrimeScope ML suite.
Provides clean feature imputation and deterministic categorical encoding.
"""

import pandas as pd
import numpy as np

def clean_and_prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensures essential numeric fields are imputed, formatted, and parsed safely.
    Handles 'Victim Age' and 'Police Deployed' with safe median fallbacks.
    """
    df_clean = df.copy()
    
    # ── Impute Victim Age ──────────────────────────────────────────────────────
    if "Victim Age" in df_clean.columns:
        df_clean["Victim Age"] = pd.to_numeric(df_clean["Victim Age"], errors="coerce")
        median_age = df_clean["Victim Age"].median()
        # Fallback to default if median is NaN (empty column)
        if pd.isna(median_age):
            median_age = 35.0
        df_clean["Victim Age"] = df_clean["Victim Age"].fillna(median_age).astype(int)
    else:
        df_clean["Victim Age"] = 35
        
    # ── Impute Police Deployed ─────────────────────────────────────────────────
    if "Police Deployed" in df_clean.columns:
        df_clean["Police Deployed"] = pd.to_numeric(df_clean["Police Deployed"], errors="coerce")
        median_police = df_clean["Police Deployed"].median()
        if pd.isna(median_police):
            median_police = 10.0
        df_clean["Police Deployed"] = df_clean["Police Deployed"].fillna(median_police).astype(int)
    else:
        df_clean["Police Deployed"] = 10
        
    # ── Verify Date intervals ──────────────────────────────────────────────────
    if "Month" not in df_clean.columns:
        df_clean["Month"] = 1
        
    if "Year" not in df_clean.columns:
        df_clean["Year"] = 2020
        
    return df_clean


def encode_categorical(df: pd.DataFrame, columns: list) -> tuple:
    """
    Applies a deterministic label encoding mapping to categorical columns.
    Ensures compatibility with Scikit-Learn models without pickling overhead.
    
    Returns:
        df_encoded: DataFrame with new columns formatted as '{column}_Encoded'
        mappings: dict containing {'forward': {label: code}, 'reverse': {code: label}, 'classes': list}
    """
    df_encoded = df.copy()
    mappings = {}
    
    for col in columns:
        if col in df_encoded.columns:
            # Sort unique values to maintain clean encoding indices
            unique_vals = sorted([str(x).title() for x in df_encoded[col].dropna().unique().tolist()])
            
            # Ensure "Unknown" is mapped or added to support fallback predictions
            if "Unknown" not in unique_vals:
                unique_vals.append("Unknown")
                
            forward_map = {val: idx for idx, val in enumerate(unique_vals)}
            reverse_map = {idx: val for idx, val in enumerate(unique_vals)}
            
            mappings[col] = {
                "forward": forward_map,
                "reverse": reverse_map,
                "classes": unique_vals
            }
            
            # Form Title Case values for safe matching
            temp_col = df_encoded[col].astype(str).str.title()
            df_encoded[col + "_Encoded"] = temp_col.map(forward_map).fillna(forward_map["Unknown"]).astype(int)
            
    return df_encoded, mappings
