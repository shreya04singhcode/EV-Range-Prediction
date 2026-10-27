
# EV Range Prediction - V2 Model Training
# Synthetic data experiment

import pandas as pd
import joblib

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "ev_synthetic_dataset_v2.csv"
MODEL_DIR = ROOT / "models" / "v2"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_FILE)

features = [
    "battery_capacity_kwh",
    "soc_percent",
    "voltage_v",
    "current_a",
    "speed_kmh",
    "temperature_c",
    "efficiency_percent",
]

X = df[features]
y = df["remaining_range_km"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

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

for name, model in models.items():
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5
    r2 = r2_score(y_test, predictions)

    results.append({
        "Model": name,
        "MAE_km": mae,
        "RMSE_km": rmse,
        "R2": r2,
    })

    filename = name.lower().replace(" ", "_") + ".joblib"
    joblib.dump(model, MODEL_DIR / filename)

    print(f"\n{name}")
    print(f"MAE: {mae:.2f} km")
    print(f"RMSE: {rmse:.2f} km")
    print(f"R2: {r2:.4f}")

comparison = pd.DataFrame(results)
comparison.to_csv(
    ROOT / "data" / "model_comparison_v2.csv",
    index=False
)

print("\n===== V2 MODEL COMPARISON =====")
print(comparison.to_string(index=False))
print("\nModels saved in:", MODEL_DIR)
print("Comparison saved in data/model_comparison_v2.csv")
print("\nReminder: Evaluation uses synthetic data only.")

