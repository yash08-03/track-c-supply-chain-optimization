import pandas as pd
from pulp import *
from pulp import COIN_CMD

print("Loading files...")

# ---------------------------
# Load Forecast Output
# ---------------------------

df = pd.read_csv(
    "results/forecasts/xgb_predictions.csv"
)

# ---------------------------
# Latest Forecast Month
# ---------------------------

df["Month"] = pd.to_datetime(df["Month"])

latest_month = df["Month"].max()

df = df[
    df["Month"] == latest_month
].copy()

# ---------------------------
# Rename Columns
# ---------------------------

rename_map = {
    "Unit_Price_x": "Unit_Price",
    "Unit_Cost_x": "Unit_Cost",
    "Supplier_Risk_x": "Supplier_Risk",
    "ABC_Class_x": "ABC_Class",
    "Warehouse_Capacity_x": "Warehouse_Capacity",
    "Transport_Cost_Index_x": "Transport_Cost_Index"
}

df = df.rename(columns=rename_map)

# ---------------------------
# Validation
# ---------------------------

required_cols = [
    "SKU_ID",
    "Branch_ID",
    "Prediction",
    "Unit_Price",
    "Unit_Cost",
    "Supplier_Risk",
    "ABC_Class",
    "Warehouse_Capacity",
    "Transport_Cost_Index"
]

missing = [
    c for c in required_cols
    if c not in df.columns
]

if len(missing) > 0:
    raise ValueError(
        f"Missing columns: {missing}"
    )

print("Validation passed")

# ---------------------------
# Business Parameters
# ---------------------------

SERVICE_LEVELS = {
    "A": 0.98,
    "B": 0.95,
    "C": 0.90
}

df["Margin"] = (
    df["Unit_Price"]
    -
    df["Unit_Cost"]
)

df["Available_Inventory"] = (
    df["Prediction"] * 1.10
)

df["Stockout_Penalty"] = (
    df["Margin"] * 0.25
)

df["Risk_Penalty"] = (
    df["Supplier_Risk"] * 10
)

df["Transport_Penalty"] = (
    df["Transport_Cost_Index"] * 2
)

# ---------------------------
# Optimization Model
# ---------------------------

model = LpProblem(
    "Inventory_Optimization",
    LpMaximize
)

# ---------------------------
# Decision Variables
# ---------------------------

allocation = {}

for idx in df.index:

    allocation[idx] = LpVariable(
        f"alloc_{idx}",
        lowBound=0
    )

# ---------------------------
# Objective Function
# ---------------------------

model += lpSum(

    allocation[idx]

    *

    (

        df.loc[idx, "Margin"]

        -

        df.loc[idx, "Transport_Penalty"]

        -

        df.loc[idx, "Risk_Penalty"]

    )

    for idx in df.index

)

# ---------------------------
# Inventory Constraints
# ---------------------------

for sku_id in df["SKU_ID"].unique():

    rows = df[
        df["SKU_ID"] == sku_id
    ]

    inventory_limit = rows[
        "Available_Inventory"
    ].sum()

    model += (

        lpSum(
            allocation[idx]
            for idx in rows.index
        )

        <= inventory_limit

    )

# ---------------------------
# Warehouse Constraints
# ---------------------------

for branch_id in df["Branch_ID"].unique():

    rows = df[
        df["Branch_ID"] == branch_id
    ]

    capacity = rows[
        "Warehouse_Capacity"
    ].iloc[0]

    model += (

        lpSum(
            allocation[idx]
            for idx in rows.index
        )

        <= capacity

    )
# ---------------------------
# Service Level Constraints
# ---------------------------

for idx in df.index:

    abc_val = df.loc[idx, "ABC_Class"]

    if abc_val == 0:
        service_level = 0.98
    elif abc_val == 1:
        service_level = 0.95
    else:
        service_level = 0.90

    model += (
        allocation[idx]
        >= service_level * df.loc[idx, "Prediction"]
    )
# ---------------------------
# Demand Constraints
# ---------------------------

for idx in df.index:

    model += (

        allocation[idx]

        <=

        df.loc[idx, "Prediction"]

    )

print("Rows:", len(df))
print("SKUs:", df["SKU_ID"].nunique())
print("Branches:", df["Branch_ID"].nunique())

# ---------------------------
# Solve
# ---------------------------

print("Solving model...")

import shutil

cbc_path = shutil.which("cbc")

print("CBC Path:", cbc_path)

solver = COIN_CMD(
    path=cbc_path,
    msg=True
)

model.solve(solver)

print(
    "Status:",
    LpStatus[model.status]
)

# ---------------------------
# Save Results
# ---------------------------

df["Optimized_Allocation"] = [
    allocation[idx].varValue
    if allocation[idx].varValue is not None
    else 0
    for idx in df.index
]

df.to_csv(
    "results/optimized_allocation.csv",
    index=False
)

# ---------------------------
# Metrics
# ---------------------------

profit = (

    df["Optimized_Allocation"]

    *

    (

        df["Margin"]

        -

        df["Transport_Penalty"]

        -

        df["Risk_Penalty"]

    )

).sum()

metrics = pd.DataFrame({

    "Metric": [
        "Objective_Value",
        "Solver_Status",
        "Rows_Optimized"
    ],

    "Value": [
        round(profit, 2),
        LpStatus[model.status],
        len(df)
    ]

})

metrics.to_csv(
    "results/optimization_metrics.csv",
    index=False
)

print(
    f"Profit: {profit:,.2f}"
)

print(
    "Optimization complete."
)