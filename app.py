from src.calculations import calc_gear_ratio, rpm_to_omega, calc_driver_torque, calc_driven_side, calc_pitch_diameter

gear_ratio = calc_gear_ratio(20,60)
print("Gear Ratio: ", gear_ratio)

omega_driver =rpm_to_omega(1500)
print("omega_driver: ", omega_driver)

torque_driver = calc_driver_torque(5000,omega_driver)
print("torque_driver: ", torque_driver)

driven_side = calc_driven_side (gear_ratio, omega_driver, torque_driver)
print("driven_side: ", driven_side)

pitch_diameter_driver = calc_pitch_diameter(2,20)
print("pitch_diameter of driver: ", pitch_diameter_driver)

pitch_diameter_driven = calc_pitch_diameter(2,60)
print("pitch_diameter of driven: ", pitch_diameter_driven)

centre_dist = (pitch_diameter_driver + pitch_diameter_driven) / 2
print("centre_dist of driver: ", centre_dist)