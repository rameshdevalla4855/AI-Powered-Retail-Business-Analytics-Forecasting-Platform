"""
segmentation.py

Customer Segmentation Module
AI Powered Retail Business Analytics Platform
"""

import joblib
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from src.config import MODEL_DIR
from src.utils import logger


# ==========================================================
# Features used for clustering
# ==========================================================

SEGMENT_COLUMNS = [
    "payment_value",
    "delivery_days",
    "review_score"
]


# ==========================================================
# Prepare Customer Data
# ==========================================================

def prepare_customer_data(df: pd.DataFrame):

    customer_df = (
        df.groupby("customer_id")
        .agg(
            TotalSpent=("payment_value", "sum"),
            AvgDelivery=("delivery_days", "mean"),
            AvgReview=("review_score", "mean"),
        )
        .reset_index()
    )

    return customer_df


# ==========================================================
# Scale Features
# ==========================================================

def scale_features(customer_df: pd.DataFrame):

    features = customer_df[
        ["TotalSpent", "AvgDelivery", "AvgReview"]
    ]

    scaler = StandardScaler()

    scaled = scaler.fit_transform(features)

    logger.info("Customer features scaled.")

    return scaler, scaled


# ==========================================================
# Train KMeans
# ==========================================================

def train_segmentation(df: pd.DataFrame):

    customer_df = prepare_customer_data(df)

    scaler, scaled = scale_features(customer_df)

    model = KMeans(
        n_clusters=4,
        random_state=42,
        n_init=10
    )

    customer_df["Cluster"] = model.fit_predict(scaled)

    logger.info("Customer segmentation completed.")

    return customer_df, model, scaler


# ==========================================================
# Cluster Summary
# ==========================================================

def cluster_summary(customer_df: pd.DataFrame):

    summary = (
        customer_df
        .groupby("Cluster")
        .agg(
            Customers=("customer_id", "count"),
            AvgSpent=("TotalSpent", "mean"),
            AvgDelivery=("AvgDelivery", "mean"),
            AvgReview=("AvgReview", "mean")
        )
        .reset_index()
    )

    return summary


# ==========================================================
# Predict New Customer
# ==========================================================

def predict_customer_segment(
    model,
    scaler,
    total_spent,
    delivery_days,
    review_score
):

    sample = pd.DataFrame({

        "TotalSpent": [total_spent],
        "AvgDelivery": [delivery_days],
        "AvgReview": [review_score]

    })

    scaled = scaler.transform(sample)

    return int(model.predict(scaled)[0])


# ==========================================================
# Save Models
# ==========================================================

def save_segmentation_model(model, scaler):

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    joblib.dump(
        model,
        MODEL_DIR / "customer_segmentation.pkl"
    )

    joblib.dump(
        scaler,
        MODEL_DIR / "customer_scaler.pkl"
    )

    logger.info("Segmentation models saved.")


# ==========================================================
# Load Models
# ==========================================================

def load_segmentation_model():

    model = joblib.load(
        MODEL_DIR / "customer_segmentation.pkl"
    )

    scaler = joblib.load(
        MODEL_DIR / "customer_scaler.pkl"
    )

    return model, scaler