"""
generate_dashboard_data.py

Generates lightweight CSV files required for the Streamlit dashboard.
"""

from pathlib import Path
import pandas as pd
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_ROOT / "data" / "processed" / "final_feature_dataset.csv"

OUTPUT_PATH = PROJECT_ROOT / "dashboard_data"

OUTPUT_PATH.mkdir(parents=True, exist_ok=True)


# ==========================================
# LOAD DATA
# ==========================================

print("=" * 60)
print("Loading Processed Dataset...")
print("=" * 60)

df = pd.read_csv(
    DATA_PATH,
    parse_dates=[
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]
)

print(f"Dataset Shape : {df.shape}")


print("\nChecking Dataset Quality...\n")

print("Duplicate Rows :", df.duplicated().sum())

print("Remaining Missing Values")

print(
    df.isnull()
      .sum()
      .sort_values(ascending=False)
      .head(20)
)



df = df.drop_duplicates()


print("\nGenerating KPI Summary...")

kpi = pd.DataFrame({

    "Metric": [

        "Total Revenue",

        "Total Orders",

        "Total Customers",

        "Total Sellers",

        "Average Order Value"

    ],

    "Value": [

        round(df["total_order_value"].sum(),2),

        df["order_id"].nunique(),

        df["customer_id"].nunique(),

        df["seller_id"].nunique(),

        round(df["total_order_value"].mean(),2)

    ]

})

kpi.to_csv(

    OUTPUT_PATH / "kpi_summary.csv",

    index=False

)

print("KPI Summary Saved")



print("Generating Monthly Sales...")

monthly_sales = (

    df

    .groupby(

        df["order_purchase_timestamp"]

        .dt.to_period("M")

    )["total_order_value"]

    .sum()

    .reset_index()

)

monthly_sales.columns = [

    "Month",

    "Revenue"

]

monthly_sales["Month"] = monthly_sales["Month"].astype(str)

monthly_sales.to_csv(

    OUTPUT_PATH / "monthly_sales.csv",

    index=False

)

print("Monthly Sales Saved")




print("Generating Category Sales...")

category_sales = (

    df

    .groupby("product_category_name_english")

    ["total_order_value"]

    .sum()

    .sort_values(ascending=False)

    .reset_index()

)

category_sales.to_csv(

    OUTPUT_PATH / "category_sales.csv",

    index=False

)

print("Category Sales Saved")





print("Generating State Sales...")

state_sales = (

    df

    .groupby("customer_state")

    ["total_order_value"]

    .sum()

    .sort_values(ascending=False)

    .reset_index()

)

state_sales.to_csv(

    OUTPUT_PATH / "state_sales.csv",

    index=False

)

print("State Sales Saved")


print("Generating Payment Summary...")

payment_summary = (

    df

    .groupby("payment_type")

    .agg(

        Revenue=("payment_value","sum"),

        Orders=("order_id","count")

    )

    .reset_index()

)

payment_summary.to_csv(

    OUTPUT_PATH / "payment_summary.csv",

    index=False

)



print("Generating Top Products...")

top_products = (

    df

    .groupby([

        "product_id",

        "product_category_name_english"

    ])

    .agg(

        Revenue=("total_order_value","sum"),

        Orders=("order_id","count")

    )

    .sort_values(

        "Revenue",

        ascending=False

    )

    .head(50)

    .reset_index()

)

top_products.to_csv(

    OUTPUT_PATH / "top_products.csv",

    index=False

)



if "customer_segment" in df.columns:

    customer_segments = (

        df[

            [

                "customer_id",

                "customer_segment"

            ]

        ]

        .drop_duplicates()

    )

    customer_segments.to_csv(

        OUTPUT_PATH / "customer_segments.csv",

        index=False

    )



print("\n" + "=" * 60)
print("Dashboard Data Generated Successfully")
print("=" * 60)

print(f"Files saved to:\n{OUTPUT_PATH}")


