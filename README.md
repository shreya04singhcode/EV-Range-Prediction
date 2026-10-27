# Electric Vehicle Range Prediction using Machine Learning with Battery Electrical Modeling

## Project Overview
This project estimates the remaining driving range of an electric vehicle (EV) using machine learning and a simplified battery electrical model.

## Objectives
- Estimate remaining EV range using battery and driving parameters.
- Compare Linear Regression and Random Forest models.
- Calculate electrical power using battery voltage and current.
- Demonstrate predictions through an interactive Streamlit application.

## Input Parameters
- Battery capacity (kWh)
- State of Charge (SOC, %)
- Battery voltage (V)
- Battery current (A)
- Vehicle speed (km/h)
- Temperature (°C)
- Efficiency (%)

## Technologies Used
- Python
- Streamlit
- NumPy and Pandas
- Matplotlib
- Scikit-learn
- Joblib

## Project Structure
- pp.py — interactive application
- data/ — datasets and model evaluation results
- models/v2/ — trained V2 machine learning models
- src/battery_model.py — simplified battery electrical model
- src/generate_dataset_v2.py — synthetic dataset generation
- src/train_model_v2.py — model training
- src/evaluate_model.py — model evaluation
- equirements.txt — Python dependencies

## Model Evaluation
Evaluation on the synthetic test dataset:

| Model | MAE (km) | RMSE (km) |
|---|---:|---:|
| Linear Regression | 55.12 | 81.16 |
| Random Forest | 26.62 | 41.64 |

Random Forest performed better on this synthetic test dataset.

## How to Run
1. Install Python.
2. Open a terminal in the project directory.
3. Install dependencies:
   python -m pip install -r requirements.txt
4. Launch the application:
   python -m streamlit run app.py
5. Open the local URL displayed in the terminal.

## Limitations
The dataset is synthetic, not collected from actual EV road tests. The battery model uses simplified assumptions, including illustrative temperature adjustment factors. Results are educational estimates and are not validated for real-world driving or safety-critical use.

## Future Scope
- Validate using measured EV driving and battery data.
- Improve energy-consumption modelling.
- Test the model across different vehicle types and environmental conditions.
- Compare additional machine learning algorithms.
