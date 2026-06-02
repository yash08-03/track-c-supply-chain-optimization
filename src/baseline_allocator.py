import pandas as pd
import numpy as np

print("Loading data...")

# -------------------------
# Load Forecast Results
# -------------------------

forecast_df = pd.read_csv(
    "results/forecasts/xgb_predictions.csv"
)

# -------------------------
# Use latest forecast month
# -------------------------

forecast_df["Month"] = pd.to_datetime(
    forecast_df["Month"]
)

latest_month = forecast_df["Month"].max()

forecast_df = forecast_df[
    forecast_df["Month"] == latest_month
]

print(f"Forecast Month: {latest_month}")

# -------------------------
# Branch Demand Share
# -------------------------

total_demand = forecast_df.groupby(
    "SKU_ID"
)["Prediction"].transform("sum")

forecast_df["Demand_Share"] = (
    forecast_df["Prediction"] /
    total_demand
)

# -------------------------
# Inventory Assumption
# -------------------------

forecast_df["Available_Inventory"] = (
    forecast_df["Prediction"] * 1.10
)

# -------------------------
# Baseline Allocation
# -------------------------

forecast_df["Baseline_Allocation"] = (
    forecast_df["Demand_Share"] *
    forecast_df["Available_Inventory"]
)

# -------------------------
# Save Output
# -------------------------

output_cols = [
    "SKU_ID",
    "Branch_ID",
    "Prediction",
    "Demand_Share",
    "Available_Inventory",
    "Baseline_Allocation"
]

forecast_df[
    output_cols
].to_csv(
    "results/baseline_allocation.csv",
    index=False
)

print(
    "Saved results/baseline_allocation.csv"
)

print(
    forecast_df[
        output_cols
    ].head()
)
