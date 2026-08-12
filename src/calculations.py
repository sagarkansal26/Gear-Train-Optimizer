import math as math
import pandas as pd

#Function 1#
def calc_gear_ratio (teeth_driver, teeth_driven) :
    """
    Calculate the gear ratio of a gear pair

    Args:
    teeth_driver (int): number of teeth on the driver gear
    teeth_driven (int): number of teeth on the driven gear

    Returns:
    float: gear ratio (teeth_driven / teeth_driver)
    """
    gear_ratio = teeth_driven / teeth_driver
    return gear_ratio

#Function 2#
def rpm_to_omega (rpm) :
    """
    Convert RPM to omega

    Args:
    rpm (int): RPM at which the gear is moving

    Returns:
    float: omega (angular velocity) in radian per second
    """
    omega = 2 * 3.14 * rpm / 60
    return omega

#Function 3#
def calc_driver_torque (power, omega_driver) :
    """
    Calculate the torque of driver gear

    Args:
    power (int): Power transmitted by the driver gear in Watts
    omega_driver (float): Angular Velocity of driver gear in rad per sec

    Returns:
    float: torque on the driver gear in N.m
    """
    torque = power / omega_driver
    return torque

#Function 4#
def calc_driven_side (gear_ratio, omega_driver, torque_driver) :
    """
    Calculate the driven side of gear

    Args:
    gear_ratio (float): gear ratio (N_driven / N_driver)
    omega_driver (float): Angular Velocity of driver gear in rad per sec
    torque_driver (float): torque on the driver gear in N.m

    Returns:
    tuple: (omega_driven, torque_driven)
        omega_driven (float): Angular velocity of the driven gear, in radians per second.
        torque_driven (float): Torque on the driven gear, in Newton-meters (N·m).
    """
    omega_driven = omega_driver / gear_ratio
    torque_driven = torque_driver * gear_ratio
    return omega_driven, torque_driven

#Function 5#
def calc_pitch_diameter (module, teeth) :
    """
    Calculate the pitch diameter of the teeth

    Args:
    module (int): Module of the Gear
    teeth (int): Teeth of the gear

    Returns:
    pitch_diameter (float): Pitch diameter of the teeth
    """
    pitch_diameter = module * teeth
    return pitch_diameter

#Function 6#
def calc_tangential_force (torque, pitch_diameter_mm) :
    """
    Calculate the tangential force of the gear

    Args:
    torque (float): Torque on the driver gear in N.m
    pitch_diameter_mm (float): Pitch diameter of the teeth in mm

    Returns:
    float: tangential force of the gear
    """
    pitch_diameter_m = pitch_diameter_mm / 1000
    tangential_force = 2 * torque / pitch_diameter_m
    return tangential_force

#Function 7#
def calc_radial_force(tangential_force, pressure_angle_degree) :
    """
    Calculate the radial force of the gear
    
    Args:
    tangential_force (float): tangential force of the gear
    pressure_angle_degree (float): Pressure angle of the gear in degrees

    Returns:
    float: radial force of the gear
    """
    pressure_angle_radian = math.radians(pressure_angle_degree)
    radial_force = tangential_force * math.tan(pressure_angle_radian)
    return radial_force

#Function 8#
def get_lewis_form_factor(teeth):
    lewis_form_factors = {
        12: 0.245, 14: 0.261, 17: 0.277, 20: 0.290, 24: 0.302,
        30: 0.314, 40: 0.336, 60: 0.355, 75: 0.371, 100: 0.400,
        150: 0.446, 300: 0.506
    }

    """
    Calculate the lewis form factor

    Args:
    teeth (int): Teeth of the gear

    Returns:
    float: lewis form factor
    """
    closest_teeth = min(lewis_form_factors.keys(), key=lambda t: abs(t - teeth))
    y_factor = lewis_form_factors[closest_teeth]
    return y_factor

#Function 9#
def calc_bending_stress (tangential_force, module, face_width, y_factor):
    """
    Calculate the bending stress of the gear

    Args:
    tangential_force (float): tangential force of the gear
    module (float): Module of the Gear
    face_width (float): Face width of the gear
    y_factor (float): lewis form factor

    Returns:
    float: bending stress of the gear in N/mm ^ 2
    """
    bending_stress = tangential_force / (module * face_width * y_factor)
    return bending_stress

#Function 10#
def get_allowable_stress(material_name):
    """
    Look up the allowable bending stress for a given material.

    Simplified reference values for the Lewis bending stress equation,
    from common introductory machine design references. Not a substitute
    for a full material datasheet — validate against a proper materials
    engineering source before real design use.

    Args:
        material_name (str): Name of the material, must match an entry
            in data/materials.csv exactly.

    Returns:
        float: Allowable bending stress in N/mm^2 (MPa).
    """
    materials_df = pd.read_csv("data/materials.csv")
    row = materials_df[materials_df["material"] == material_name]
    allowable_stress = row["allowable_bending_stress_mpa"].values[0]
    return allowable_stress

#Function 11#
def calc_safety_factor (allowable_stress, bending_stress):
    """
    Calculate the safety factor

    Args:
    allowable_stress (float): allowable bending stress in N/mm ^ 2
    bending_stress (float): bending stress in N/mm ^ 2

    Returns:
    float: safety factor
    """
    safety_factor = allowable_stress / bending_stress
    return safety_factor