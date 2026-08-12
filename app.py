from src.calculations import calc_gear_ratio, rpm_to_omega, calc_driver_torque, calc_driven_side, calc_pitch_diameter, calc_tangential_force, calc_radial_force, get_lewis_form_factor, calc_bending_stress, get_allowable_stress, calc_safety_factor
from src.candidates import generate_candidates
from src.candidates import filter_by_ratio
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

tangential_force = calc_tangential_force(31.85,40)
print("tangential_force: ", tangential_force)

radial_force = calc_radial_force(tangential_force,20)
print("radial_force: ", radial_force)

Y_factor = get_lewis_form_factor(teeth_driver)
print("Y_factor: ", Y_factor)

bending_stress = calc_bending_stress(tangential_force, module, 10*module, Y_factor)
print("bending_stress: ", bending_stress)

allowable_stress = get_allowable_stress("Steel (Low Carbon)")
print("allowable_stress: ", allowable_stress)

safety_factor = calc_safety_factor(allowable_stress, bending_stress)
print("safety_factor: ", safety_factor)


