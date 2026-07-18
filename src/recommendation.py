"""
recommendation.py

Content-Based Product Recommendation System
AI Powered Retail Business Analytics Platform
"""

import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.config import MODEL_DIR
from src.utils import logger


# ==========================================================
# Prepare Product Dataset
# ==========================================================

def prepare_products(df: pd.DataFrame):

    products = (
        df[
            [
                "product_id",
                "product_category_name_english",
                "product_description_lenght",
                "product_name_lenght"
            ]
        ]
        .drop_duplicates("product_id")
        .copy()
    )

    products.fillna("Unknown", inplace=True)

    products["text"] = (
        products["product_category_name_english"].astype(str)
        + " "
        + products["product_description_lenght"].astype(str)
        + " "
        + products["product_name_lenght"].astype(str)
    )

    logger.info("Product dataset prepared.")

    return products


# ==========================================================
# Train Recommendation Model
# ==========================================================

def train_recommendation(df):

    products = prepare_products(df)

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(
        products["text"]
    )

    similarity_matrix = cosine_similarity(
        tfidf_matrix
    )

    logger.info("Recommendation model trained.")

    return products, vectorizer, similarity_matrix


# ==========================================================
# Recommend Similar Products
# ==========================================================

def recommend_products(
    product_id,
    products,
    similarity_matrix,
    top_n=5
):

    if product_id not in products["product_id"].values:
        return pd.DataFrame()

    idx = products.index[
        products["product_id"] == product_id
    ][0]

    scores = list(
        enumerate(similarity_matrix[idx])
    )

    scores = sorted(
        scores,
        key=lambda x: x[1],
        reverse=True
    )

    scores = scores[1:top_n+1]

    indices = [i[0] for i in scores]

    return products.iloc[indices][
        [
            "product_id",
            "product_category_name_english"
        ]
    ]


# ==========================================================
# Save Recommendation Model
# ==========================================================

def save_recommendation_model(
    products,
    vectorizer,
    similarity_matrix
):

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    joblib.dump(
        products,
        MODEL_DIR / "products.pkl"
    )

    joblib.dump(
        vectorizer,
        MODEL_DIR / "tfidf_vectorizer.pkl"
    )

    joblib.dump(
        similarity_matrix,
        MODEL_DIR / "similarity_matrix.pkl"
    )

    logger.info("Recommendation model saved.")


# ==========================================================
# Load Recommendation Model
# ==========================================================

def load_recommendation_model():

    products = joblib.load(
        MODEL_DIR / "products.pkl"
    )

    vectorizer = joblib.load(
        MODEL_DIR / "tfidf_vectorizer.pkl"
    )

    similarity_matrix = joblib.load(
        MODEL_DIR / "similarity_matrix.pkl"
    )

    return (
        products,
        vectorizer,
        similarity_matrix
    )