"""
utils.py

Common utility functions used across the project.
"""

from pathlib import Path
import pandas as pd
import logging


# ==========================================================
# Logging
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# ==========================================================
# Save DataFrame
# ==========================================================

def save_dataframe(df: pd.DataFrame, output_path: Path) -> None:
    """
    Save a dataframe to CSV.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path, index=False)

    logger.info(f"Saved: {output_path}")


# ==========================================================
# Dataset Summary
# ==========================================================

def dataset_summary(df: pd.DataFrame) -> None:
    """
    Print dataset summary.
    """

    print("=" * 60)
    print("DATASET SUMMARY")
    print("=" * 60)

    print(f"Rows      : {df.shape[0]}")
    print(f"Columns   : {df.shape[1]}")
    print(f"Duplicates: {df.duplicated().sum()}")

    print("\nMissing Values")

    print(df.isnull().sum())


# ==========================================================
# Memory Usage
# ==========================================================

def memory_usage(df: pd.DataFrame) -> None:

    memory = df.memory_usage(deep=True).sum() / 1024**2

    print(f"Memory Usage : {memory:.2f} MB")


# ==========================================================
# Currency Formatting
# ==========================================================

def format_currency(value: float) -> str:

    return f"${value:,.2f}"


# ==========================================================
# Percentage Formatting
# ==========================================================

def format_percentage(value: float) -> str:

    return f"{value:.2f}%"


# ==========================================================
# Validation
# ==========================================================

def validate_dataframe(df: pd.DataFrame) -> bool:
    """
    Basic dataframe validation.
    """

    if df.empty:
        raise ValueError("DataFrame is empty.")

    logger.info("DataFrame validation passed.")

    return True