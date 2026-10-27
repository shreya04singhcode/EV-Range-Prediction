
import numpy as np
import pandas as pd
from pathlib import Path

# Reproducible synthetic dataset
rng = np.random.default_rng(42)
n = 1500

# Generate illustrative EV operating conditions
capacity = rng.uniform(30, 80, n)          # kWh
soc = rng.uniform(10, 100, n)             # %
voltage = rng.uniform(300, 400, n)        # V
current = rng.uniform(10, 80, n)          # A
speed = rng.uniform(20, 100, n)           # km/h
temperature = rng.uniform(-5, 45, n)      # deg C
efficiency = rng.uniform(85, 95, n)       # %

# Simplified illustrative temperature factors
capacity_factor = np.select(
    [
        temperature < 0,
        temperature < 10,
        temperature <= 35,
        temperature <= 45,
    ],
    [0.75, 0.88, 1.00, 0.95],
    default=0.85,
)

consumption_factor = np.select(
    [
        temperature < 0,
        temperature < 10,
        temperature <= 35,
        temperature <= 45,
    ],
    [1.25, 1.12, 1.00, 1.08],
    default=1.20,
)

# Electrical calculations
power_kw = voltage * current / 1000

# Simplified physics-based range target
stored_energy = capacity * soc / 100
adjusted_energy = stored_energy * capacity_factor
usable_energy = adjusted_energy * efficiency / 100

consumption_wh_per_km = (power_kw / speed) * 1000
adjusted_consumption = (
    consumption_wh_per_km * consumption_factor
)

# Small illustrative measurement noise
noise = rng.normal(0, 0.02, n)

range_km = (
    usable_energy / (adjusted_consumption / 1000)
) * (1 + noise)

# Assemble dataset
df = pd.DataFrame({
    "battery_capacity_kwh": capacity,
    "soc_percent": soc,
    "voltage_v": voltage,
    "current_a": current,
    "speed_kmh": speed,
    "temperature_c": temperature,
    "efficiency_percent": efficiency,
    "power_kw": power_kw,
    "energy_consumption_wh_per_km": adjusted_consumption,
    "remaining_range_km": range_km,
})

# Save CSV in the project's data folder
project_root = Path(__file__).resolve().parent.parent
output_file = project_root / "data" / "ev_synthetic_dataset.csv"
output_file.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(output_file, index=False)

print("Synthetic dataset created successfully!")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"Saved to: {output_file}")
print("\nFirst five records:")
print(df.head().round(2).to_string(index=False))
print("\nDataset summary:")
print(df[["soc_percent", "temperature_c",
          "remaining_range_km"]].describe().round(2))
