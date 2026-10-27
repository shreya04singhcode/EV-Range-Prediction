import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
from src.battery_model import model_ev_battery

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "models" / "v2" / "random_forest.joblib"

st.set_page_config(
    page_title="EV Range Predictor",
    page_icon="🔋",
    layout="centered",
)

st.title("🔋 EV Range Predictor")
st.caption(
    "Electric Vehicle Range Prediction using Machine Learning "
    "with Battery Electrical Modeling"
)

st.info(
    "Educational prototype: the ML model uses synthetic data. "
    "Neither range estimate is validated for real-world EV driving."
)

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

try:
    model = load_model()
except Exception as error:
    st.error(f"Could not load the trained model: {error}")
    st.stop()

st.subheader("Enter battery and driving parameters")

with st.form("prediction_form"):
    col1, col2 = st.columns(2)

    with col1:
        capacity = st.number_input(
            "Battery capacity (kWh)", 30.0, 80.0, 50.0, 1.0
        )
        soc = st.number_input(
            "Battery SOC (%)", 10.0, 100.0, 75.0, 1.0
        )
        voltage = st.number_input(
            "Battery voltage (V)", 300.0, 400.0, 350.0, 5.0
        )
        current = st.number_input(
            "Battery current (A)", 10.0, 60.0, 30.0, 1.0
        )

    with col2:
        speed = st.number_input(
            "Driving speed (km/h)", 30.0, 100.0, 50.0, 5.0
        )
        temperature = st.number_input(
            "Battery temperature (°C)", 0.0, 40.0, 25.0, 1.0
        )
        efficiency = st.number_input(
            "Drivetrain efficiency (%)", 85.0, 95.0, 90.0, 1.0
        )

    submitted = st.form_submit_button(
        "🚗 Predict Remaining Range",
        use_container_width=True,
    )

if submitted:
    input_data = pd.DataFrame([{
        "battery_capacity_kwh": capacity,
        "soc_percent": soc,
        "voltage_v": voltage,
        "current_a": current,
        "speed_kmh": speed,
        "temperature_c": temperature,
        "efficiency_percent": efficiency,
    }])

    try:
        predicted_range = float(model.predict(input_data)[0])

        battery_result = model_ev_battery(
            battery_capacity_kwh=capacity,
            soc_percent=soc,
            voltage_v=voltage,
            current_a=current,
            speed_kmh=speed,
            temperature_c=temperature,
            drivetrain_efficiency_percent=efficiency,
        )

        st.divider()
        st.subheader("Prediction Results")

        a, b = st.columns(2)
        if predicted_range > 0:
            a.metric("ML estimated range", f"{predicted_range:.1f} km")
        else:
            a.metric("ML estimated range", "Invalid result")

        physics_range = float(battery_result["remaining_range_km"])
        if physics_range > 0:
            b.metric("Electrical-model range", f"{physics_range:.1f} km")
        else:
            b.metric("Electrical-model range", "Invalid result")

        st.caption(
            "These are educational estimates, not real-world range guarantees."
        )

        c, d = st.columns(2)
        c.metric("Battery electrical power", f"{voltage * current / 1000:.2f} kW")
        d.metric("Battery charge", f"{soc:.0f}%")

        with st.expander("Electrical-model details"):
            st.write(
                f"Stored battery energy: "
                f"{battery_result['stored_energy_kwh']:.2f} kWh"
            )
            st.write(
                f"Usable battery energy: "
                f"{battery_result['usable_energy_kwh']:.2f} kWh"
            )
            st.write(
                f"Estimated energy consumption: "
                f"{battery_result['adjusted_consumption_wh_per_km']:.2f} Wh/km"
            )

        st.write("Input summary")
        st.dataframe(input_data, use_container_width=True, hide_index=True)

    except Exception as error:
        st.error(f"Prediction failed: {error}")
        st.caption(
            "Please share the full error message before changing other files."
        )

st.divider()
st.caption(
    "Project: EV Range Prediction using Machine Learning "
    "with Battery Electrical Modeling"
)

