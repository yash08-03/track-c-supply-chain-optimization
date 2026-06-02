import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# ==========================================
# 1. Data Loading & Merging
# ==========================================

monthly = pd.read_csv("data/monthly_demand.csv")
sku = pd.read_csv("data/sku_master.csv")
branch = pd.read_csv("data/branch_master.csv")

# Merge dataframes and sort chronologically per group
df = monthly.merge(sku, on="SKU_ID").merge(branch, on="Branch_ID")
df["Month"] = pd.to_datetime(df["Month"])
df = df.sort_values(["SKU_ID", "Branch_ID", "Month"]).reset_index(drop=True)


# ==========================================
# 2. Feature Engineering
# ==========================================

# Date-based features
df["month_num"] = df["Month"].dt.month
df["quarter"] = df["Month"].dt.quarter
df["year"] = df["Month"].dt.year

# Grouping object for sequential features
grouped_demand = df.groupby(["SKU_ID", "Branch_ID"])["Demand"]

# Lag features
for lag in [1, 2, 3, 6, 12]:
    df[f"lag_{lag}"] = grouped_demand.shift(lag)

# Rolling window features (shifted to prevent data leakage)
for w in [3, 6]:
    # Shift first to avoid looking ahead, then group and calculate rolling metrics
    shifted_group = df.groupby(["SKU_ID", "Branch_ID"])["Demand"].shift(1)
    rolling_obj = shifted_group.groupby(df["SKU_ID"] + "_" + df["Branch_ID"]).rolling(w)
    
    df[f"rolling_mean_{w}"] = rolling_obj.mean().reset_index(level=0, drop=True)
    df[f"rolling_std_{w}"] = rolling_obj.std().reset_index(level=0, drop=True)

# Ratios and rates
df["inventory_ratio"] = df["Inventory"] / (df["Demand"] + 1)
df["demand_growth_rate"] = grouped_demand.pct_change()

# Categorical Encoding
le = LabelEncoder()
categorical_cols = ["Category", "ABC_Class", "Supplier_ID", "Region"]
for col in categorical_cols:
    df[col] = le.fit_transform(df[col].astype(str))


# ==========================================
# 3. Data Cleaning & Safety Checks
# ==========================================

# Drop rows with initial NaN values resulting from lags/rolling windows
df = df.dropna()

# Handle residual mathematical anomalies (e.g., from pct_change or division)
df = df.replace([np.inf, -np.inf], np.nan)
df = df.fillna(0)

# Safety check for remaining infinite values
numeric_df = df.select_dtypes(include=[np.number])
remaining_infs = np.isinf(numeric_df).sum().sum()
print(f"Remaining INF values: {remaining_infs}")


# ==========================================
# 4. Export
# ==========================================

df.to_csv("results/feature_engineered_data.csv", index=False)