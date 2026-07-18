"""
preprocessing.py

Reusable preprocessing functions for the
AI Powered Retail Business Analytics Platform.
"""

import pandas as pd
import numpy as np

from src.utils import logger


# ==========================================================
# Missing Values
# ==========================================================

def fill_missing_categorical(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill missing categorical values.
    """

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns

    for column in categorical_columns:

        if df[column].isnull().sum() > 0:

            df[column] = df[column].fillna("Unknown")

    logger.info("Filled missing categorical values.")

    return df


# ==========================================================
# Numeric Missing Values
# ==========================================================

def fill_missing_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill missing numeric values using median.
    """

    numeric_columns = df.select_dtypes(
        include=[np.number]
    ).columns

    for column in numeric_columns:

        if df[column].isnull().sum() > 0:

            median = df[column].median()

            df[column] = df[column].fillna(median)

    logger.info("Filled missing numeric values.")

    return df


# ==========================================================
# Date Columns
# ==========================================================

def convert_date_columns(
    df: pd.DataFrame,
    columns: list
) -> pd.DataFrame:

    for column in columns:

        if column in df.columns:

            df[column] = pd.to_datetime(
                df[column],
                errors="coerce"
            )

    logger.info("Date conversion completed.")

    return df


# ==========================================================
# Duplicate Removal
# ==========================================================

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:

    before = len(df)

    df = df.drop_duplicates()

    after = len(df)

    logger.info(
        f"Removed {before-after} duplicate rows."
    )

    return df


# ==========================================================
# Negative Values
# ==========================================================

def remove_negative_values(
    df: pd.DataFrame,
    columns: list
) -> pd.DataFrame:

    for column in columns:

        if column in df.columns:

            df = df[df[column] >= 0]

    logger.info("Removed negative values.")

    return df


# ==========================================================
# Outlier Capping (IQR)
# ==========================================================

def cap_outliers(
    df: pd.DataFrame,
    columns: list
) -> pd.DataFrame:

    for column in columns:

        if column not in df.columns:
            continue

        q1 = df[column].quantile(0.25)

        q3 = df[column].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr

        upper = q3 + 1.5 * iqr

        df[column] = df[column].clip(
            lower=lower,
            upper=upper
        )

    logger.info("Outliers capped.")

    return df


# ==========================================================
# Full Pipeline
# ==========================================================

def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:

    df = fill_missing_categorical(df)

    df = fill_missing_numeric(df)

    df = remove_duplicates(df)

    return df