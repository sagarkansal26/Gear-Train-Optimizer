from src.calculations import calc_gear_ratio, rpm_to_omega, calc_driver_torque, calc_driven_side
gear_ratio = calc_gear_ratio(20,60)
print("Gear Ratio: ", gear_ratio)

omega_driver =rpm_to_omega(1500)
print("omega_driver: ", omega_driver)

torque_driver = calc_driver_torque(5000,omega_driver)
print("torque_driver: ", torque_driver)

driven_side = calc_driven_side (gear_ratio, omega_driver, torque_driver)
print("driven_side: ", driven_side)
