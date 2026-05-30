"""
backend/utils/data_loader.py
============================
Responsible for raw dataset loading and structural cleaning.
Handles Windows BOM characters, duplicate records, datetime parsing, and categorical normalizations.
"""

import pandas as pd
import numpy as np
from utils.logger import logger

def load_and_clean(filepath: str) -> pd.DataFrame:
    """
    Reads a CSV file, cleans headers and missing values, parses dates,
    and returns a clean, structured Pandas DataFrame.
    """
    logger.info(f"Initiating raw dataset ingestion: {filepath}")
    
    try:
        # ── 1. Read CSV with BOM-stripping encoding ──────────────────────────
        df = pd.read_csv(filepath, encoding="utf-8-sig")
        logger.debug(f"CSV read complete. Shape: {df.shape}")
        
        # ── 2. Clean column names ────────────────────────────────────────────
        df.columns = df.columns.str.strip()
        
        # ── 3. Drop full duplicates ──────────────────────────────────────────
        df.drop_duplicates(inplace=True)
        
        # ── 4. Impute missing values ─────────────────────────────────────────
        # For object types -> fill with "Unknown"
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].fillna("Unknown").str.strip()
            
        # For numeric types -> fill with median
        for col in df.select_dtypes(include=[np.number]).columns:
            df[col] = df[col].fillna(df[col].median())
            
        # ── 5. Parse dates and extract temporal features (Year / Month) ──────
        date_candidates = [c for c in df.columns if "date" in c.lower()]
        for dc in date_candidates:
            try:
                df[dc] = pd.to_datetime(df[dc], dayfirst=True, errors="coerce")
            except Exception as ex:
                logger.warning(f"Datetime conversion failed on column {dc}: {ex}")
                
        occ_col = next((c for c in df.columns if "occurrence" in c.lower()), None)
        if occ_col and pd.api.types.is_datetime64_any_dtype(df[occ_col]):
            df["Year"] = df[occ_col].dt.year.fillna(0).astype(int)
            df["Month"] = df[occ_col].dt.month.fillna(0).astype(int)
        else:
            dt_cols = df.select_dtypes(include="datetime64").columns
            if len(dt_cols) > 0:
                df["Year"] = df[dt_cols[0]].dt.year.fillna(0).astype(int)
                df["Month"] = df[dt_cols[0]].dt.month.fillna(0).astype(int)
                
        # ── 6. Normalize text columns ────────────────────────────────────────
        for col in ["City", "Crime Description", "Weapon Used", "Crime Domain"]:
            if col in df.columns:
                df[col] = df[col].str.title()
                
        logger.info(f"Dataset cleaning completed successfully. Cleaned records: {len(df)}")
        return df
        
    except Exception as e:
        logger.error(f"Failed to ingest dataset {filepath}: {e}", exc_info=True)
        raise e
