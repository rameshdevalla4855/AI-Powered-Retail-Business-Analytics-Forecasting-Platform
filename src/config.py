"""
config.py

Central configuration file for the AI-Powered Retail Business Analytics Platform.

Author : Ramesh Devalla
Project: AI-Powered Retail Business Analytics & Forecasting Platform
"""

from pathlib import Path


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent


# ============================================================
# DATA DIRECTORIES
# ============================================================

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

CLEANED_DATA_DIR = DATA_DIR / "cleaned"

PROCESSED_DATA_DIR = DATA_DIR / "processed"


# ============================================================
# REPORT DIRECTORIES
# ============================================================

REPORTS_DIR = PROJECT_ROOT / "reports"

EDA_REPORT_DIR = REPORTS_DIR / "eda"

ANALYTICS_REPORT_DIR = REPORTS_DIR / "analytics"

FORECAST_REPORT_DIR = REPORTS_DIR / "forecasting"

RECOMMENDATION_REPORT_DIR = REPORTS_DIR / "recommendation"


# ============================================================
# DASHBOARD
# ============================================================

DASHBOARD_DATA_DIR = PROJECT_ROOT / "dashboard_data"

DASHBOARD_DIR = PROJECT_ROOT / "dashboard"


# ============================================================
# MODEL DIRECTORY
# ============================================================

MODEL_DIR = PROJECT_ROOT / "models"


# ============================================================
# SCREENSHOTS
# ============================================================

SCREENSHOT_DIR = PROJECT_ROOT / "screenshots"


# ============================================================
# MAIN DATASET
# ============================================================

FINAL_DATASET = (
    PROCESSED_DATA_DIR /
    "final_feature_dataset.csv"
)


# ============================================================
# CREATE REQUIRED DIRECTORIES
# ============================================================

DIRECTORIES = [

    CLEANED_DATA_DIR,

    PROCESSED_DATA_DIR,

    EDA_REPORT_DIR,

    ANALYTICS_REPORT_DIR,

    FORECAST_REPORT_DIR,

    RECOMMENDATION_REPORT_DIR,

    DASHBOARD_DATA_DIR,

    DASHBOARD_DIR,

    MODEL_DIR,

    SCREENSHOT_DIR

]


for directory in DIRECTORIES:
    directory.mkdir(
        parents=True,
        exist_ok=True
    )


# ============================================================
# RANDOM STATE
# ============================================================

RANDOM_STATE = 42


# ============================================================
# TEST SIZE
# ============================================================

TEST_SIZE = 0.20


# ============================================================
# DISPLAY OPTIONS
# ============================================================

PANDAS_MAX_COLUMNS = 100

PANDAS_MAX_ROWS = 100


# ============================================================
# PROJECT INFORMATION
# ============================================================

PROJECT_NAME = (
    "AI Powered Retail Business Analytics Platform"
)

PROJECT_VERSION = "1.0.0"