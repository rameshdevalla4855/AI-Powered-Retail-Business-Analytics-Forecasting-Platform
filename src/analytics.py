"""
analytics.py

Business Analytics Module
AI Powered Retail Business Analytics Platform
"""

import pandas as pd

from src.utils import logger


# ==========================================================
# KPI Dashboard
# ==========================================================

def get_kpis(df: pd.DataFrame) -> dict:
    """
    Calculate overall business KPIs.
    """

    kpis = {
        "Total Orders": df["order_id"].nunique(),
        "Total Customers": df["customer_id"].nunique(),
        "Total Products": df["product_id"].nunique(),
        "Total Sellers": df["seller_id"].nunique(),
        "Total Revenue": round(df["payment_value"].sum(), 2),
        "Average Order Value": round(df["payment_value"].mean(), 2),
        "Average Review Score": round(df["review_score"].mean(), 2),
    }

    logger.info("KPIs calculated.")

    return kpis


# ==========================================================
# Monthly Sales
# ==========================================================

def monthly_sales(df: pd.DataFrame):

    sales = (
        df.groupby("purchase_month")["payment_value"]
        .sum()
        .reset_index()
        .sort_values("purchase_month")
    )

    return sales


# ==========================================================
# Monthly Orders
# ==========================================================

def monthly_orders(df: pd.DataFrame):

    orders = (
        df.groupby("purchase_month")["order_id"]
        .nunique()
        .reset_index(name="orders")
    )

    return orders


# ==========================================================
# Revenue by Category
# ==========================================================

def revenue_by_category(df: pd.DataFrame):

    category = (
        df.groupby(
            "product_category_name_english"
        )["payment_value"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    return category


# ==========================================================
# Top Products
# ==========================================================

def top_products(df: pd.DataFrame, top_n=10):

    products = (
        df.groupby("product_id")["payment_value"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    return products


# ==========================================================
# Top Sellers
# ==========================================================

def top_sellers(df: pd.DataFrame, top_n=10):

    sellers = (
        df.groupby("seller_id")["payment_value"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    return sellers


# ==========================================================
# Customer State Analysis
# ==========================================================

def customer_state_sales(df: pd.DataFrame):

    state = (
        df.groupby("customer_state")["payment_value"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    return state


# ==========================================================
# Payment Analysis
# ==========================================================

def payment_analysis(df: pd.DataFrame):

    payment = (
        df.groupby("payment_type")
        .agg(
            Orders=("order_id", "nunique"),
            Revenue=("payment_value", "sum"),
        )
        .reset_index()
    )

    return payment


# ==========================================================
# Review Score Analysis
# ==========================================================

def review_analysis(df: pd.DataFrame):

    review = (
        df.groupby("review_score")
        .size()
        .reset_index(name="count")
    )

    return review


# ==========================================================
# Delivery Performance
# ==========================================================

def delivery_performance(df: pd.DataFrame):

    performance = {
        "Average Delivery Days":
            round(df["delivery_days"].mean(), 2),

        "Average Delay":
            round(df["delivery_delay_days"].mean(), 2),

        "Maximum Delay":
            round(df["delivery_delay_days"].max(), 2),
    }

    return performance


# ==========================================================
# Seller Performance
# ==========================================================

def seller_performance(df: pd.DataFrame):

    seller = (
        df.groupby("seller_id")
        .agg(
            Orders=("order_id", "nunique"),
            Revenue=("payment_value", "sum"),
            AvgReview=("review_score", "mean")
        )
        .reset_index()
    )

    return seller


# ==========================================================
# Category Performance
# ==========================================================

def category_performance(df: pd.DataFrame):

    category = (
        df.groupby(
            "product_category_name_english"
        )
        .agg(
            Orders=("order_id", "nunique"),
            Revenue=("payment_value", "sum"),
            AvgReview=("review_score", "mean")
        )
        .reset_index()
        .sort_values("Revenue", ascending=False)
    )

    return category