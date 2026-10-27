
import pandas as pd
import matplotlib.pyplot as plt
import joblib

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

ROOT = Path(__file__).resolve().parent.parent
df = pd.read_csv(ROOT / "data" / "ev_synthetic_dataset.csv")

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

# Must match the split used during training
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

models = {
    "Linear Regression": joblib.load(
        ROOT / "models" / "linear_regression.joblib"
    ),
    "Random Forest": joblib.load(
        ROOT / "models" / "random_forest.joblib"
    ),
}

plt.figure(figsize=(8, 6))

for name, model in models.items():
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5
    r2 = r2_score(y_test, predictions)

    print(f"\n{name}")
    print(f"MAE: {mae:.2f} km")
    print(f"RMSE: {rmse:.2f} km")
    print(f"R2: {r2:.4f}")

    plt.scatter(
        y_test, predictions,
        alpha=0.45, s=18, label=name
    )

lower = min(y_test.min(), 0)
upper = max(y_test.max(), 0)

plt.plot([lower, upper], [lower, upper], linestyle="--",
         label="Ideal prediction")

plt.xlabel("Actual synthetic range (km)")
plt.ylabel("Predicted range (km)")
plt.title("Actual vs Predicted EV Range")
plt.legend()
plt.tight_layout()

output = ROOT / "data" / "actual_vs_predicted.png"
plt.savefig(output, dpi=150)
print(f"\nGraph saved to: {output}")

plt.show()
