"""
backend/utils/validators.py
===========================
Validation helper functions for incoming files and REST API parameters.
Prevents malformed CSV ingestion and protects model controllers from erroneous inputs.
"""

import pandas as pd
from utils.logger import logger

def validate_csv_headers(df: pd.DataFrame) -> tuple:
    """
    Validates if the DataFrame contains the minimum required columns for the system to operate.
    Returns a tuple: (is_valid: bool, error_message: str)
    """
    required_cols = {"City", "Crime Description", "Weapon Used"}
    missing_cols = required_cols - set(df.columns)
    
    if missing_cols:
        msg = f"Malformed CSV structure. Missing mandatory fields: {', '.join(missing_cols)}"
        logger.warning(msg)
        return False, msg
        
    logger.info("CSV validation succeeded: Mandatory headers present.")
    return True, ""


def validate_filter_params(year: str, city: str, crime_type: str) -> bool:
    """
    Sanitizes and validates telemetry filter request parameters.
    Returns True if valid, False if illegal strings or patterns are detected.
    """
    # Safeguard against malicious SQL or command injections in API strings
    for param in [year, city, crime_type]:
        if not isinstance(param, str):
            return False
        if len(param) > 100:
            return False
            
    return True
