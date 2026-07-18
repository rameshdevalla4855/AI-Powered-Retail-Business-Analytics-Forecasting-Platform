"""
forecasting.py

Sales Forecasting Module
AI Powered Retail Business Analytics Platform
"""

from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

from src.config import MODEL_DIR
from src.utils import logger


# ==========================================================
# Feature Selection
# ==========================================================

FEATURE_COLUMNS = [
    "price",
    "freight_value",
    "review_score",
    "delivery_days",
    "delivery_delay_days"
]

TARGET_COLUMN = "payment_value"


# ==========================================================
# Prepare Dataset
# ==========================================================

def prepare_training_data(df: pd.DataFrame):

    required = FEATURE_COLUMNS + [TARGET_COLUMN]

    data = df[required].copy()

    data = data.dropna()

    X = data[FEATURE_COLUMNS]

    y = data[TARGET_COLUMN]

    return train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42
    )


# ==========================================================
# Train Linear Regression
# ==========================================================

def train_linear_regression(df: pd.DataFrame):

    X_train, X_test, y_train, y_test = prepare_training_data(df)

    model = LinearRegression()

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    metrics = {
        "MAE": mean_absolute_error(y_test, predictions),
        "RMSE": mean_squared_error(
            y_test,
            predictions,
            squared=False
        ),
        "R2": r2_score(
            y_test,
            predictions
        )
    }

    logger.info("Linear Regression trained.")

    return model, metrics


# ==========================================================
# Train Random Forest
# ==========================================================

def train_random_forest(df: pd.DataFrame):

    X_train, X_test, y_train, y_test = prepare_training_data(df)

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    metrics = {
        "MAE": mean_absolute_error(y_test, predictions),
        "RMSE": mean_squared_error(
            y_test,
            predictions,
            squared=False
        ),
        "R2": r2_score(
            y_test,
            predictions
        )
    }

    logger.info("Random Forest trained.")

    return model, metrics


# ==========================================================
# Compare Models
# ==========================================================

def compare_models(df: pd.DataFrame):

    linear_model, linear_metrics = train_linear_regression(df)

    rf_model, rf_metrics = train_random_forest(df)

    results = pd.DataFrame({

        "Model": [
            "Linear Regression",
            "Random Forest"
        ],

        "MAE": [
            linear_metrics["MAE"],
            rf_metrics["MAE"]
        ],

        "RMSE": [
            linear_metrics["RMSE"],
            rf_metrics["RMSE"]
        ],

        "R2": [
            linear_metrics["R2"],
            rf_metrics["R2"]
        ]

    })

    return results, linear_model, rf_model


# ==========================================================
# Save Model
# ==========================================================

def save_model(model, filename: str):

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    path = MODEL_DIR / filename

    joblib.dump(
        model,
        path
    )

    logger.info(f"Model saved -> {path}")


# ==========================================================
# Load Model
# ==========================================================

def load_model(filename: str):

    path = MODEL_DIR / filename

    return joblib.load(path)


# ==========================================================
# Prediction
# ==========================================================

def predict_sales(model, input_df: pd.DataFrame):

    return model.predict(input_df[FEATURE_COLUMNS])