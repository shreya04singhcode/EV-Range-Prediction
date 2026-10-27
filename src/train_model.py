
# EV Range Prediction Project
# Phase 3: Train and Compare ML Models

import pandas as pd
import joblib

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Project paths
ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "ev_synthetic_dataset.csv"
MODEL_DIR = ROOT / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# 1. Load dataset
df = pd.read_csv(DATA_FILE)

# 2. Select inputs available to the prediction model
features = [
    "battery_capacity_kwh",
    "soc_percent",
    "voltage_v",
    "current_a",
    "speed_kmh",
    "temperature_c",
    "efficiency_percent",
]

target = "remaining_range_km"

X = df[features]
y = df[target]

# 3. Split data BEFORE training
# Keep a separate test set for evaluation.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

# 4. Define models
models = {
    "Linear Regression": make_pipeline(
        StandardScaler(),
        LinearRegression()
    ),
    "Random Forest": RandomForestRegressor(
        n_estimators=200,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    ),
}

results = []

# 5. Train and evaluate each model
for name, model in models.items():
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5
    r2 = r2_score(y_test, predictions)

    results.append({
        "Model": name,
        "MAE (km)": mae,
        "RMSE (km)": rmse,
        "R2": r2,
    })

    # Save trained model
    filename = name.lower().replace(" ", "_") + ".joblib"
    joblib.dump(model, MODEL_DIR / filename)

    print(f"\n{name}")
    print(f"MAE:  {mae:.2f} km")
    print(f"RMSE: {rmse:.2f} km")
    print(f"R2:   {r2:.4f}")

# 6. Display comparison
comparison = pd.DataFrame(results).sort_values("MAE (km)")
print("\n===== MODEL COMPARISON =====")
print(comparison.to_string(index=False))

comparison.to_csv(
    ROOT / "data" / "model_comparison.csv", index=False
)

print("\nTraining complete!")
print("Saved models in:", MODEL_DIR)
print("Saved comparison in:", ROOT / "data" / "model_comparison.csv")
print("\nNote: Results are from synthetic data, not real EV validation.")
