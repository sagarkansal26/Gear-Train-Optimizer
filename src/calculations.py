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



