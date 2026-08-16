import streamlit as st
import pandas as pd
from src.calculations import calc_gear_ratio, rpm_to_omega, calc_driver_torque, calc_driven_side, calc_pitch_diameter
from src.candidates import generate_candidates, filter_by_ratio, calculate_row_metrics
from src.optimiser import filter_safe_candidates, select_best_candidate

#Stage 1#
st.title("Gear Train Design & Optimization Tool")

materials_df = pd.read_csv("data/materials.csv")

with st.expander("View material reference data"):
    st.dataframe(materials_df)

#Stage 2#
st.subheader("Design Requirements")

power = st.number_input("Power (Watts)", value=5000)
rpm = st.number_input("RPM", value=1500)
target_ratio = st.number_input("Target Gear Ratio", value=2.7)
material_name = st.selectbox("Material", options=materials_df["material"].tolist())
min_safety_factor = st.number_input("Minimum Safety Factor", value=1.5, help="Real designs typically target 1.5–3+ for meaningful margin.")

with st.expander("Advanced options"):
    pressure_angle = st.number_input("Pressure Angle (degrees)", value=20)
    standard_modules = st.multiselect("Standard Modules", options=[1, 1.5, 2, 2.5, 3, 4, 5], default=[1, 2, 3])
    teeth_range = st.slider("Teeth Range", min_value=12, max_value=100, value=(15, 25))
    tolerance = st.number_input("Ratio Tolerance", value=0.01)

#Stage 3#
if st.button("Calculate Best Design"):

    # 1. Convert teeth_range slider tuple into a full list
    teeth_min, teeth_max = teeth_range
    teeth_range_list = list(range(teeth_min, teeth_max + 1))

    # 2. Single-candidate style chain — get omega/torque for the driver
    omega_driver = rpm_to_omega(rpm)
    torque_driver = calc_driver_torque(power, omega_driver)

    # 3. Generate + filter candidates using widget inputs
    candidates = generate_candidates(target_ratio, standard_modules, teeth_range_list)
    filtered = filter_by_ratio(candidates, target_ratio, tolerance)

    # 4. Compute metrics for every filtered candidate (same .apply + pd.concat pattern you already have)
    new_columns = filtered.apply(
        calculate_row_metrics,
        axis=1,
        args=(torque_driver, pressure_angle, material_name)
    )
    filtered = pd.concat([filtered, new_columns], axis=1)

    # 5. Filter to safe candidates, then pick the best one
    safe_candidates = filter_safe_candidates(filtered, min_safety_factor)
    best_candidate = select_best_candidate(safe_candidates)

    # 6. Display the result
    if best_candidate is None:
        st.warning(
            f"No safe candidates found with a minimum safety factor of {min_safety_factor}. Try lowering it, or widen your teeth range / module options in Advanced options.")
    else:
        st.subheader("Best Candidate Design")
        st.write(best_candidate)

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

teeth_driver = 20
teeth_driven = 60
module = 2

gear_ratio = calc_gear_ratio(teeth_driver, teeth_driven)
print("Gear Ratio: ", gear_ratio)

omega_driver =rpm_to_omega(1500)
print("omega_driver: ", omega_driver)

torque_driver = calc_driver_torque(5000,omega_driver)
print("torque_driver: ", torque_driver)

driven_side = calc_driven_side (gear_ratio, omega_driver, torque_driver)
print("driven_side: ", driven_side)

pitch_diameter_driver = calc_pitch_diameter(module, teeth_driver)
print("pitch_diameter of driver: ", pitch_diameter_driver)

pitch_diameter_driven = calc_pitch_diameter(module, teeth_driven)
print("pitch_diameter of driven: ", pitch_diameter_driven)

centre_dist = (pitch_diameter_driver + pitch_diameter_driven) / 2
print("centre_dist of driver: ", centre_dist)

result = generate_candidates(2.7, [1,2,3], [15,20,25])
print(result)

filtered_result = filter_by_ratio(result,2.7,0.01)
print(filtered_result)

pressure_angle = 20
material_name = "Steel (Low Carbon)"

new_columns = filtered_result.apply(
    calculate_row_metrics,
    axis=1,
    args=(torque_driver, pressure_angle, material_name)
)

filtered_result = pd.concat([filtered_result, new_columns], axis=1)
print(filtered_result)

filtered_safe_candidates = filter_safe_candidates(filtered_result, 1.5)
print(filtered_safe_candidates)

best_candidate = select_best_candidate(filtered_safe_candidates)
print(best_candidate)