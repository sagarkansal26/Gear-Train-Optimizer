from src.calculations import calc_gear_ratio, rpm_to_omega, calc_driver_torque, calc_driven_side, calc_pitch_diameter
from src.candidates import generate_candidates, filter_by_ratio, calculate_row_metrics
from src.optimiser import filter_safe_candidates, select_best_candidate
import pandas as pd
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