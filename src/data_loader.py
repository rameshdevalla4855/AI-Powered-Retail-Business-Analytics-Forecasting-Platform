"""
data_loader.py

Centralized data loading module.

All notebooks, scripts and dashboard pages should use this module
instead of calling pd.read_csv() directly.
"""

from pathlib import Path
import pandas as pd

from src.config import (
    RAW_DATA_DIR,
    CLEANED_DATA_DIR,
    PROCESSED_DATA_DIR,
    FINAL_DATASET,
)


# ==========================================================
# Generic Loader
# ==========================================================

def load_csv(file_path: Path, **kwargs) -> pd.DataFrame:
    """
    Load any CSV file safely.

    Parameters
    ----------
    file_path : Path
        CSV file path.

    kwargs :
        Additional arguments for pandas.read_csv()

    Returns
    -------
    pd.DataFrame
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"\nCSV File Not Found:\n{file_path}"
        )

    return pd.read_csv(file_path, **kwargs)


# ==========================================================
# RAW DATA LOADERS
# ==========================================================

def load_customers():
    return load_csv(RAW_DATA_DIR / "olist_customers_dataset.csv")


def load_orders():
    return load_csv(
        RAW_DATA_DIR / "olist_orders_dataset.csv",
        parse_dates=[
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ],
    )


def load_products():
    return load_csv(RAW_DATA_DIR / "olist_products_dataset.csv")


def load_order_items():
    return load_csv(RAW_DATA_DIR / "olist_order_items_dataset.csv")


def load_payments():
    return load_csv(RAW_DATA_DIR / "olist_order_payments_dataset.csv")


def load_reviews():
    return load_csv(RAW_DATA_DIR / "olist_order_reviews_dataset.csv")


def load_sellers():
    return load_csv(RAW_DATA_DIR / "olist_sellers_dataset.csv")


def load_geolocation():
    return load_csv(RAW_DATA_DIR / "olist_geolocation_dataset.csv")


def load_translation():
    return load_csv(
        RAW_DATA_DIR / "product_category_name_translation.csv"
    )


# ==========================================================
# CLEANED DATA LOADERS
# ==========================================================

def load_clean_customers():
    return load_csv(CLEANED_DATA_DIR / "customers_clean.csv")


def load_clean_orders():
    return load_csv(CLEANED_DATA_DIR / "orders_clean.csv")


def load_clean_products():
    return load_csv(CLEANED_DATA_DIR / "products_clean.csv")


# ==========================================================
# PROCESSED DATA
# ==========================================================

def load_processed_dataset():
    """
    Loads the final processed dataset used by
    analytics, forecasting and dashboard.
    """

    return load_csv(
        FINAL_DATASET,
        parse_dates=[
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ],
    )


# ==========================================================
# Dataset Information
# ==========================================================

def dataset_info(df: pd.DataFrame):
    """
    Print basic dataset information.
    """

    print("=" * 60)
    print("Dataset Information")
    print("=" * 60)

    print(f"Rows    : {df.shape[0]}")
    print(f"Columns : {df.shape[1]}")

    print("\nMissing Values\n")
    print(df.isnull().sum())

    print("\nDuplicate Rows")
    print(df.duplicated().sum())