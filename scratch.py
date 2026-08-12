from src.calculations import calc_bending_stress,get_allowable_stress,calc_safety_factor,calc_radial_force, get_lewis_form_factor,calc_tangential_force
from src.candidates import generate_candidates,filter_by_ratio
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

torque_driver = 31.85
pressure_angle = 20
material_name = "Steel (Low Carbon)"

def calculate_row_metrics(row, torque_driver, pressure_angle, material_name):
    """
    Calculate tangential force, radial force, bending stress, and safety
    factor for one candidate gear design.

    Args:
    row (Series): One row of the candidates DataFrame (must contain
        pitch_diameter_driver, teeth_driver, module columns).
    torque_driver (float): Torque on the driver gear, in N.m.
    pressure_angle (float): Pressure angle of the gear teeth, in degrees.
    material_name (str): Material name, must match an entry in
        data/materials.csv.

    Returns:
    Series: tangential_force, radial_force, bending_stress, safety_factor
        for this candidate.
    """

    tangential_force = calc_tangential_force(torque_driver, row["pitch_diameter_driver"])
    radial_force = calc_radial_force(tangential_force, pressure_angle)
    y_factor = get_lewis_form_factor(row["teeth_driver"])
    face_width = 10 * row["module"]
    bending_stress = calc_bending_stress(tangential_force, row["module"], face_width, y_factor)
    allowable_stress = get_allowable_stress(material_name)
    safety_factor = calc_safety_factor(allowable_stress, bending_stress)

    return pd.Series({
        "tangential_force": tangential_force,
        "radial_force": radial_force,
        "bending_stress": bending_stress,
        "safety_factor": safety_factor
    })
result = generate_candidates(2.7, [1,2,3], [15,20,25])


filtered_result = filter_by_ratio(result,2.7,0.01)


new_columns = filtered_result.apply(calculate_row_metrics, axis=1)
filtered_result = pd.concat([filtered_result, new_columns], axis=1)
print(filtered_result)
