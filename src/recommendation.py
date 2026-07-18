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
    """Return safe recommendations without assuming a strict matrix-to-DataFrame index match."""
    normalized_products = products.reset_index(drop=True).copy()
    normalized_products["product_id"] = normalized_products["product_id"].astype(str)
    product_key = str(product_id)

    if product_key not in normalized_products["product_id"].values:
        return pd.DataFrame()

    matched = normalized_products[normalized_products["product_id"] == product_key]
    if matched.empty:
        return pd.DataFrame()

    if not isinstance(similarity_matrix, pd.DataFrame):
        matrix_size = len(similarity_matrix)
    else:
        matrix_size = similarity_matrix.shape[0]

    row_index = int(matched.index[0])
    if row_index < 0 or row_index >= matrix_size:
        return pd.DataFrame()

    try:
        row_scores = similarity_matrix[row_index]
    except Exception:
        return pd.DataFrame()

    if hasattr(row_scores, "tolist"):
        row_scores = row_scores.tolist()

    scored = list(enumerate(row_scores))
    scored = sorted(scored, key=lambda item: item[1], reverse=True)
    scored = scored[1:top_n + 1]

    valid_indices = [int(item[0]) for item in scored if 0 <= int(item[0]) < len(normalized_products)]
    if not valid_indices:
        return pd.DataFrame()

    return normalized_products.iloc[valid_indices][["product_id", "product_category_name_english"]]


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