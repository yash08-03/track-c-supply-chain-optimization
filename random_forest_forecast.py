import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder

# -----------------------
# Load Data
# -----------------------

df = pd.read_csv("results/feature_engineered_data.csv")
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

rf = RandomForestRegressor(
    n_estimators=300,
    max_depth=12,
    random_state=42,
    n_jobs=-1
)

rf.fit(X_train, y_train)

preds = rf.predict(X_test)

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
    "results/forecasts/rf_predictions.csv",
    index=False
)

metrics = pd.DataFrame({
    "Model": ["RandomForest"],
    "RMSE": [rmse],
    "MAE": [mae],
    "MAPE": [mape]
})

metrics.to_csv(
    "results/metrics/rf_metrics.csv",
    index=False
)

print("Random Forest completed.")