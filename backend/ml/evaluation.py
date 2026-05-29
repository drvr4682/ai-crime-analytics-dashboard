"""
evaluation.py
=============
Provides central metric calculation functions for:
- Regression (MAE, RMSE, R2 Score)
- Classification (Accuracy, Precision, Recall, F1 Score)
- Clustering (Silhouette Score)
"""

import numpy as np
from sklearn.metrics import (mean_squared_error, mean_absolute_error, r2_score,
                             accuracy_score, precision_recall_fscore_support,
                             silhouette_score)

def evaluate_regression(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    """
    Computes regression evaluation indexes: MAE, RMSE, and R² Score.
    """
    if len(y_true) == 0:
        return {"mae": 0.0, "rmse": 0.0, "r2_score": 0.0}
        
    mae = float(mean_absolute_error(y_true, y_pred))
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    
    # R2 can be negative if model performs extremely poorly, handle safely
    try:
        r2 = float(r2_score(y_true, y_pred))
    except Exception:
        r2 = 0.0
        
    return {
        "mae": round(mae, 2),
        "rmse": round(rmse, 2),
        "r2_score": round(max(r2, 0.0), 4)
    }


def evaluate_classification(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    """
    Computes multi-class classification metrics: Accuracy, Precision, Recall, F1 Score.
    """
    if len(y_true) == 0:
        return {"accuracy": 0.0, "precision": 0.0, "recall": 0.0, "f1_score": 0.0}
        
    accuracy = float(accuracy_score(y_true, y_pred))
    
    # Use macro averaging to capture performance across multi-class scenarios evenly
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average="macro", zero_division=0
    )
    
    return {
        "accuracy": round(accuracy * 100, 2),
        "precision": round(float(precision) * 100, 2),
        "recall": round(float(recall) * 100, 2),
        "f1_score": round(float(f1) * 100, 2)
    }


def evaluate_clustering(X: np.ndarray, labels: np.ndarray) -> dict:
    """
    Computes KMeans cluster cohesion score using the Silhouette Score metric.
    Samples coordinates for performance optimization when scaling.
    """
    unique_clusters = np.unique(labels)
    if len(unique_clusters) < 2 or X.shape[0] < 3:
        return {"silhouette_score": 0.0}
        
    try:
        # Scale protection: sample up to 1000 items to keep API response times sub-10ms
        if X.shape[0] > 1000:
            np.random.seed(42)
            sample_idx = np.random.choice(X.shape[0], size=1000, replace=False)
            score = float(silhouette_score(X[sample_idx], labels[sample_idx]))
        else:
            score = float(silhouette_score(X, labels))
    except Exception:
        score = 0.0
        
    return {
        "silhouette_score": round(score, 4)
    }
