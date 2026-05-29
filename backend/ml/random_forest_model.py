"""
random_forest_model.py
======================
Trains a RandomForestClassifier to predict likely crime categories.
Includes custom categorical encoding mapping and interactive inference handlers.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from ml.preprocessing import clean_and_prepare_features, encode_categorical
from ml.evaluation import evaluate_classification

def train_random_forest(df: pd.DataFrame) -> dict:
    """
    Cleans dataset, encodes categorical properties, splits into train/test (80/20),
    and trains a highly optimized RandomForestClassifier to predict 'Crime Description'.
    """
    required_cols = ["City", "Month", "Victim Age", "Victim Gender", "Weapon Used", "Crime Description"]
    cols_to_use = [col for col in required_cols if col in df.columns]
    
    if len(cols_to_use) < 2 or "Crime Description" not in cols_to_use:
        return {"error": "Missing essential columns for Random Forest classification."}
        
    df_clean = clean_and_prepare_features(df)
    
    # ── Categorical encoding ────────────────────────────────────────────────────
    cat_cols = [col for col in ["City", "Victim Gender", "Weapon Used", "Crime Description"] if col in df_clean.columns]
    df_encoded, mappings = encode_categorical(df_clean, cat_cols)
    
    # ── Assemble Features X & Target y ──────────────────────────────────────────
    feature_cols = []
    for col in ["City", "Victim Gender", "Weapon Used"]:
        if col in df_clean.columns:
            feature_cols.append(col + "_Encoded")
    for col in ["Month", "Victim Age"]:
        if col in df_clean.columns:
            feature_cols.append(col)
            
    if not feature_cols:
        return {"error": "No features isolated for classification training."}
        
    X = df_encoded[feature_cols].values
    y = df_encoded["Crime Description_Encoded"].values
    
    unique_classes = np.unique(y)
    if len(unique_classes) < 2:
        return {"error": "Insufficient unique crime categories to train classifier."}
        
    # ── Train/Test Split ────────────────────────────────────────────────────────
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # ── Train Model ─────────────────────────────────────────────────────────────
    # Keep estimators and depth optimized to ensure ultra-fast startup training
    clf = RandomForestClassifier(n_estimators=30, max_depth=8, random_state=42, n_jobs=-1)
    clf.fit(X_train, y_train)
    
    # ── Evaluate ────────────────────────────────────────────────────────────────
    y_pred = clf.predict(X_test)
    metrics = evaluate_classification(y_test, y_pred)
    
    return {
        "model": clf,
        "features": feature_cols,
        "mappings": mappings,
        "metrics": metrics
    }


def predict_crime_category(model_package: dict, city: str, month: int,
                           victim_age: int, victim_gender: str, weapon_used: str) -> dict:
    """
    Evaluates dynamic input coordinates and returns predicted crime category + confidence score.
    """
    if "error" in model_package:
        return model_package
        
    clf = model_package["model"]
    feature_cols = model_package["features"]
    mappings = model_package["mappings"]
    
    city_map = mappings.get("City", {}).get("forward", {})
    gender_map = mappings.get("Victim Gender", {}).get("forward", {})
    weapon_map = mappings.get("Weapon Used", {}).get("forward", {})
    crime_rev_map = mappings.get("Crime Description", {}).get("reverse", {})
    
    def safe_encode(val, mapping):
        val_title = str(val).strip().title()
        return mapping.get(val_title, mapping.get("Unknown", 0))
        
    # Build input features in matching column order
    features_input = []
    for col in feature_cols:
        if col == "City_Encoded":
            features_input.append(safe_encode(city, city_map))
        elif col == "Victim Gender_Encoded":
            features_input.append(safe_encode(victim_gender, gender_map))
        elif col == "Weapon Used_Encoded":
            features_input.append(safe_encode(weapon_used, weapon_map))
        elif col == "Month":
            features_input.append(int(month))
        elif col == "Victim Age":
            features_input.append(int(victim_age))
            
    features_input = np.array(features_input).reshape(1, -1)
    
    # Run prediction & probability extraction
    pred_class_encoded = clf.predict(features_input)[0]
    pred_probs = clf.predict_proba(features_input)[0]
    
    confidence = float(np.max(pred_probs))
    pred_crime = crime_rev_map.get(pred_class_encoded, "Unknown")
    
    return {
        "predicted_crime_type": pred_crime,
        "confidence": round(confidence * 100, 2)
    }
