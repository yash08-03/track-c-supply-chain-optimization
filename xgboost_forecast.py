import pandas as pd
import numpy as np

from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder

# -----------------------
# Load Data
# -----------------------

df = pd.read_csv("results/feature_engineered_data.csv")

df = df.replace([np.inf, -np.inf], np.nan)
df = df.fillna(0)

branch_encoder = LabelEncoder()

df["Branch_ID_ENC"] = branch_encoder.fit_transform(
    df["Branch_ID"]
)
# -----------------------
# Time Split
# -----------------------

df["Month"] = pd.to_datetime(df["Month"])

train = df[df["Month"] < "2025-07-01"]
test = df[df["Month"] >= "2025-07-01"]

# -----------------------
# Features
# -----------------------

exclude_cols = [
    "Demand",
    "Month",
    "Branch_ID"
    ]

features = [c for c in df.columns if c not in exclude_cols]

X_train = train[features]
y_train = train["Demand"]

X_test = test[features]
y_test = test["Demand"]

# -----------------------
# Model
# -----------------------

model = XGBRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=8,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="reg:squarederror",
    random_state=42
)

model.fit(X_train, y_train)

preds = model.predict(X_test)

# -----------------------
# Metrics
# -----------------------

rmse = np.sqrt(mean_squared_error(y_test, preds))

mae = mean_absolute_error(y_test, preds)

mape = np.mean(
    np.abs((y_test - preds) / (y_test + 1))
) * 100

print(f"RMSE: {rmse:.2f}")
print(f"MAE : {mae:.2f}")
print(f"MAPE: {mape:.2f}")

# -----------------------
# Save Predictions
# -----------------------

output = test.copy()

output["Prediction"] = preds

output.to_csv(
    "results/forecasts/xgb_predictions.csv",
    index=False
)

metrics = pd.DataFrame({
    "Model": ["XGBoost"],
    "RMSE": [rmse],
    "MAE": [mae],
    "MAPE": [mape]
})

metrics.to_csv(
    "results/metrics/xgb_metrics.csv",
    index=False
)

model.save_model(
    "results/xgb_model.json"
)

print("XGBoost completed.")