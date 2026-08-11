def calc_pitch_diametre (module, teeth) :
    """
    Calculate the pitch diameter of the teeth

    Args:
    module (int): Module of the Gear
    teeth (int): Teeth of the gear

    Returns:
    pitch_diameter (float): Pitch diameter of the teeth
    """
    pit_diameter = module * teeth
    return pit_diameter

pitch_diameter_driver = calc_pitch_diametre(2,20)
print("pitch_diameter of driver: ", pitch_diameter_driver)

pitch_diameter_driven = calc_pitch_diametre(2,60)
print("pitch_diametre of driven: ", pitch_diameter_driven)

centre_dist = (pitch_diameter_driver + pitch_diameter_driven) / 2
print("centre_dist of driver: ", centre_dist)