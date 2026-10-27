
# EV Range Prediction - Improved Synthetic Dataset V2
# Educational simulation, not real EV data

import numpy as np
import pandas as pd
from pathlib import Path

rng = np.random.default_rng(2026)
n = 2000

# Define illustrative, bounded operating conditions
capacity = rng.uniform(30, 80, n)        # kWh
soc = rng.uniform(10, 100, n)            # %
voltage = rng.uniform(300, 400, n)       # V
current = rng.uniform(10, 60, n)         # A
speed = rng.uniform(30, 100, n)          # km/h
temperature = rng.uniform(0, 40, n)      # deg C
efficiency = rng.uniform(85, 95, n)      # %

# Simplified temperature correction assumptions
capacity_factor = np.select(
    [temperature < 10, temperature <= 35],
    [0.90, 1.00],
    default=0.95,
)

consumption_factor = np.select(
    [temperature < 10, temperature <= 35],
    [1.10, 1.00],
    default=1.05,
)

# Electrical power
power_kw = voltage * current / 1000

# Battery energy at current SOC
stored_energy_kwh = capacity * soc / 100

# Simplified energy available after temperature and efficiency
usable_energy_kwh = (
    stored_energy_kwh
    * capacity_factor
    * efficiency / 100
)

# Estimate consumption from power and speed
base_consumption_wh_per_km = power_kw / speed * 1000
consumption_wh_per_km = (
    base_consumption_wh_per_km * consumption_factor
)

# Physics-based illustrative target, with small measurement noise
range_km = (
    usable_energy_kwh / (consumption_wh_per_km / 1000)
)

noise = rng.normal(1.0, 0.015, n)
range_km = range_km * noise

df = pd.DataFrame({
    "battery_capacity_kwh": capacity,
    "soc_percent": soc,
    "voltage_v": voltage,
    "current_a": current,
    "speed_kmh": speed,
    "temperature_c": temperature,
    "efficiency_percent": efficiency,
    "power_kw": power_kw,
    "energy_consumption_wh_per_km": consumption_wh_per_km,
    "remaining_range_km": range_km,
})

# Save as a separate version
root = Path(__file__).resolve().parent.parent
output = root / "data" / "ev_synthetic_dataset_v2.csv"
df.to_csv(output, index=False)

print("===== SYNTHETIC DATASET V2 =====")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"Saved to: {output}")
print("\nRange summary (km):")
print(df["remaining_range_km"].describe().round(2))
print("\nConsumption summary (Wh/km):")
print(df["energy_consumption_wh_per_km"].describe().round(2))
print("\nAll values finite:", np.isfinite(df.select_dtypes("number")).all().all())
