"""
train_models.py

Train every ML model used in the project.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.append(str(PROJECT_ROOT))




from src.data_loader import load_processed_dataset

from src.forecasting import (
    compare_models,
    save_model
)

from src.segmentation import (
    train_segmentation,
    save_segmentation_model
)

from src.recommendation import (
    train_recommendation,
    save_recommendation_model
)


def main():

    print("=" * 60)
    print("Loading Dataset")
    print("=" * 60)

    df = load_processed_dataset()

    print(df.shape)

    print("\nTraining Forecasting Model...")

    results, linear_model, rf_model = compare_models(df)

    print(results)

    save_model(
        linear_model,
        "linear_regression.pkl"
    )

    save_model(
        rf_model,
        "random_forest.pkl"
    )

    print("\nTraining Customer Segmentation...")

    customer_df, segment_model, scaler = train_segmentation(df)

    save_segmentation_model(
        segment_model,
        scaler
    )

    print("\nTraining Recommendation System...")

    products, vectorizer, similarity = train_recommendation(df)

    save_recommendation_model(
        products,
        vectorizer,
        similarity
    )

    print("\n" + "=" * 60)
    print("ALL MODELS TRAINED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()