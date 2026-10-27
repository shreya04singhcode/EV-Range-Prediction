
# EV Range Prediction Project
# Phase 1: Basic Battery Electrical Model

def calculate_remaining_range(
    battery_capacity_kwh,
    soc_percent,
    consumption_wh_per_km,
    efficiency_percent
):
    """Estimate EV range using battery energy and consumption."""

    if battery_capacity_kwh <= 0:
        raise ValueError("Battery capacity must be positive.")

    if not 0 <= soc_percent <= 100:
        raise ValueError("SOC must be between 0 and 100.")

    if consumption_wh_per_km <= 0:
        raise ValueError("Energy consumption must be positive.")

    if not 0 < efficiency_percent <= 100:
        raise ValueError("Efficiency must be greater than 0 and at most 100.")

    # Available energy stored in the battery
    available_energy_kwh = battery_capacity_kwh * soc_percent / 100

    # Account for drivetrain efficiency
    usable_energy_kwh = available_energy_kwh * efficiency_percent / 100

    # Convert energy consumption from Wh/km to kWh/km
    consumption_kwh_per_km = consumption_wh_per_km / 1000

    # Calculate estimated remaining range
    remaining_range_km = usable_energy_kwh / consumption_kwh_per_km

    return available_energy_kwh, remaining_range_km


if __name__ == "__main__":
    # Example EV parameters (illustrative values)
    battery_capacity = 40       # kWh
    state_of_charge = 75        # %
    energy_consumption = 150    # Wh/km
    drivetrain_efficiency = 90  # %

    energy, range_km = calculate_remaining_range(
        battery_capacity,
        state_of_charge,
        energy_consumption,
        drivetrain_efficiency
    )

    print("===== EV BATTERY RANGE ESTIMATOR =====")
    print(f"Battery capacity: {battery_capacity} kWh")
    print(f"Battery SOC: {state_of_charge}%")
    print(f"Available battery energy: {energy:.2f} kWh")
    print(f"Energy consumption: {energy_consumption} Wh/km")
    print(f"Drivetrain efficiency: {drivetrain_efficiency}%")
    print(f"Estimated remaining range: {range_km:.2f} km")




# EV Range Prediction Project
# Phase 2: Battery Electrical Modeling
# Educational simulation - illustrative assumptions

def get_temperature_factors(temperature_c):
    """
    Simplified temperature correction factors.
    These are illustrative, NOT calibrated battery data.
    Returns: capacity factor, consumption factor.
    """

    if temperature_c < 0:
        return 0.75, 1.25
    elif temperature_c < 10:
        return 0.88, 1.12
    elif temperature_c <= 35:
        return 1.00, 1.00
    elif temperature_c <= 45:
        return 0.95, 1.08
    else:
        return 0.85, 1.20


def model_ev_battery(
    battery_capacity_kwh,
    soc_percent,
    voltage_v,
    current_a,
    speed_kmh,
    temperature_c,
    drivetrain_efficiency_percent
):
    """Calculate electrical quantities and estimate remaining range."""

    # Validate inputs
    if battery_capacity_kwh <= 0:
        raise ValueError("Battery capacity must be positive.")

    if not 0 <= soc_percent <= 100:
        raise ValueError("SOC must be between 0 and 100.")

    if voltage_v <= 0 or current_a < 0:
        raise ValueError("Voltage must be positive and current non-negative.")

    if speed_kmh <= 0:
        raise ValueError("Speed must be positive for this range estimate.")

    if not 0 < drivetrain_efficiency_percent <= 100:
        raise ValueError("Efficiency must be greater than 0 and at most 100.")

    # 1. Electrical power: P = V x I
    battery_power_kw = voltage_v * current_a / 1000

    # 2. Battery energy available from current SOC
    stored_energy_kwh = battery_capacity_kwh * soc_percent / 100

    # 3. Simplified temperature corrections
    capacity_factor, consumption_factor = (
        get_temperature_factors(temperature_c)
    )

    temperature_adjusted_energy_kwh = (
        stored_energy_kwh * capacity_factor
    )

    # 4. Estimate energy consumption from power and speed.
    # Assumes the measured power represents a steady driving load.
    consumption_wh_per_km = (
        battery_power_kw / speed_kmh
    ) * 1000

    # Account for temperature-related consumption changes
    adjusted_consumption_wh_per_km = (
        consumption_wh_per_km * consumption_factor
    )

    # 5. Account for drivetrain efficiency
    usable_energy_kwh = (
        temperature_adjusted_energy_kwh
        * drivetrain_efficiency_percent / 100
    )

    # 6. Remaining range estimate
    adjusted_consumption_kwh_per_km = (
        adjusted_consumption_wh_per_km / 1000
    )

    remaining_range_km = (
        usable_energy_kwh / adjusted_consumption_kwh_per_km
    )

    return {
        "battery_power_kw": battery_power_kw,
        "stored_energy_kwh": stored_energy_kwh,
        "temperature_adjusted_energy_kwh":
            temperature_adjusted_energy_kwh,
        "consumption_wh_per_km": consumption_wh_per_km,
        "adjusted_consumption_wh_per_km":
            adjusted_consumption_wh_per_km,
        "usable_energy_kwh": usable_energy_kwh,
        "remaining_range_km": remaining_range_km,
        "capacity_temperature_factor": capacity_factor,
        "consumption_temperature_factor": consumption_factor,
    }


if __name__ == "__main__":
    # Example inputs for an illustrative EV
    results = model_ev_battery(
        battery_capacity_kwh=40,
        soc_percent=75,
        voltage_v=350,
        current_a=40,
        speed_kmh=50,
        temperature_c=5,
        drivetrain_efficiency_percent=90,
    )

    print("\n===== EV BATTERY ELECTRICAL MODEL =====")
    print(f"Battery voltage: {350} V")
    print(f"Battery current: {40} A")
    print(f"Battery power: {results['battery_power_kw']:.2f} kW")
    print(f"Battery SOC: {75}%")
    print(f"Stored energy: {results['stored_energy_kwh']:.2f} kWh")
    print(
        "Temperature-adjusted energy: "
        f"{results['temperature_adjusted_energy_kwh']:.2f} kWh"
    )
    print(f"Driving speed: {50} km/h")
    print(f"Battery temperature: {5} deg C")
    print(
        "Estimated energy consumption: "
        f"{results['adjusted_consumption_wh_per_km']:.2f} Wh/km"
    )
    print(f"Usable energy after efficiency: "
          f"{results['usable_energy_kwh']:.2f} kWh")
    print(
        "Estimated remaining range: "
        f"{results['remaining_range_km']:.2f} km"
    )
