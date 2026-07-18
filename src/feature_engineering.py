"""
feature_engineering.py

Feature engineering functions for the
AI Powered Retail Business Analytics Platform.
"""

import numpy as np
import pandas as pd

from src.utils import logger


# ==========================================================
# Purchase Date Features
# ==========================================================

def add_purchase_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create features from order_purchase_timestamp.
    """

    if "order_purchase_timestamp" not in df.columns:
        return df

    df["purchase_year"] = df["order_purchase_timestamp"].dt.year

    df["purchase_month"] = df["order_purchase_timestamp"].dt.month

    df["purchase_day"] = df["order_purchase_timestamp"].dt.day

    df["purchase_weekday"] = (
        df["order_purchase_timestamp"]
        .dt.day_name()
    )

    df["purchase_hour"] = (
        df["order_purchase_timestamp"]
        .dt.hour
    )

    logger.info("Purchase date features created.")

    return df


# ==========================================================
# Delivery Features
# ==========================================================

def add_delivery_features(df: pd.DataFrame) -> pd.DataFrame:

    if (
        "order_delivered_customer_date" not in df.columns
        or
        "order_purchase_timestamp" not in df.columns
    ):
        return df

    df["delivery_days"] = (
        df["order_delivered_customer_date"]
        -
        df["order_purchase_timestamp"]
    ).dt.days

    df["delivery_days"] = (
        df["delivery_days"]
        .clip(lower=0)
    )

    logger.info("Delivery features created.")

    return df


# ==========================================================
# Delivery Delay
# ==========================================================

def add_delay_features(df: pd.DataFrame) -> pd.DataFrame:

    required = [
        "order_estimated_delivery_date",
        "order_delivered_customer_date"
    ]

    if not all(col in df.columns for col in required):
        return df

    df["delivery_delay_days"] = (
        df["order_delivered_customer_date"]
        -
        df["order_estimated_delivery_date"]
    ).dt.days

    df["delivery_delay_days"] = (
        df["delivery_delay_days"]
        .fillna(0)
    )

    logger.info("Delay features created.")

    return df


# ==========================================================
# Product Volume
# ==========================================================

def add_product_volume(df: pd.DataFrame) -> pd.DataFrame:

    cols = [
        "product_length_cm",
        "product_height_cm",
        "product_width_cm"
    ]

    if not all(col in df.columns for col in cols):
        return df

    df["product_volume_cm3"] = (
        df["product_length_cm"]
        *
        df["product_height_cm"]
        *
        df["product_width_cm"]
    )

    logger.info("Product volume created.")

    return df


# ==========================================================
# Weight Category
# ==========================================================

def add_weight_category(df: pd.DataFrame) -> pd.DataFrame:

    if "product_weight_g" not in df.columns:
        return df

    bins = [
        0,
        500,
        1000,
        5000,
        np.inf
    ]

    labels = [
        "Light",
        "Medium",
        "Heavy",
        "Very Heavy"
    ]

    df["weight_category"] = pd.cut(
        df["product_weight_g"],
        bins=bins,
        labels=labels
    )

    logger.info("Weight category created.")

    return df


# ==========================================================
# Price Category
# ==========================================================

def add_price_category(df: pd.DataFrame) -> pd.DataFrame:

    if "price" not in df.columns:
        return df

    q1 = df["price"].quantile(.25)

    q2 = df["price"].quantile(.50)

    q3 = df["price"].quantile(.75)

    df["price_category"] = pd.cut(

        df["price"],

        bins=[
            0,
            q1,
            q2,
            q3,
            np.inf
        ],

        labels=[
            "Budget",
            "Standard",
            "Premium",
            "Luxury"
        ]
    )

    logger.info("Price category created.")

    return df


# ==========================================================
# Freight Percentage
# ==========================================================

def add_freight_percentage(df: pd.DataFrame) -> pd.DataFrame:

    cols = [
        "price",
        "freight_value"
    ]

    if not all(col in df.columns for col in cols):
        return df

    df["freight_percentage"] = (
        df["freight_value"]
        /
        df["price"]
    ) * 100

    df["freight_percentage"] = (
        df["freight_percentage"]
        .replace(np.inf, 0)
        .fillna(0)
    )

    logger.info("Freight percentage created.")

    return df


# ==========================================================
# Description Quality
# ==========================================================

def add_description_quality(df: pd.DataFrame) -> pd.DataFrame:

    if "product_description_lenght" not in df.columns:
        return df

    median = df[
        "product_description_lenght"
    ].median()

    df["description_quality"] = np.where(

        df["product_description_lenght"] >= median,

        "Good",

        "Poor"

    )

    logger.info("Description quality created.")

    return df


# ==========================================================
# Full Feature Pipeline
# ==========================================================

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:

    df = add_purchase_features(df)

    df = add_delivery_features(df)

    df = add_delay_features(df)

    df = add_product_volume(df)

    df = add_weight_category(df)

    df = add_price_category(df)

    df = add_freight_percentage(df)

    df = add_description_quality(df)

    logger.info("Feature engineering completed.")

    return df