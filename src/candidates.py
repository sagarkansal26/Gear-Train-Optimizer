from src.calculations import calc_pitch_diameter,calc_tangential_force,calc_radial_force,calc_safety_factor, get_allowable_stress,calc_bending_stress, get_lewis_form_factor
import pandas as pd

def generate_candidates(target_ratio, standard_modules, teeth_range):
    """
    Calculating Candidates

    Args:
    target_ratio(float): Desired gear ratio the candidates should approximate
    standard_modules: list of standard modules
    teeth_range: range of teeth
    pitch_diameter_driver: pitch diameter driver
    pitch_diameter_driven: pitch diameter driven
    center_distance: distance between teeth_driven and teeth_driver

    Returns:
    df (DataFrame): Table of candidate gear designs with columns
        module, teeth_driver, teeth_driven, actual_ratio, pitch_diameter_driver, pitch_diameter_driven, center_distance
    """
    candidates = []   # empty list to collect rows

    for module in standard_modules:
        for teeth_driver in teeth_range:
            teeth_driven = round(teeth_driver * target_ratio)
            pitch_diameter_driver = calc_pitch_diameter(module, teeth_driver)
            pitch_diameter_driven = calc_pitch_diameter(module, teeth_driven)
            center_distance = (pitch_diameter_driver + pitch_diameter_driven) / 2
            actual_ratio = teeth_driven / teeth_driver

            candidates.append({
                "module": module,
                "teeth_driver": teeth_driver,
                "teeth_driven": teeth_driven,
                "actual_ratio": actual_ratio,
                "pitch_diameter_driver": pitch_diameter_driver,
                "pitch_diameter_driven": pitch_diameter_driven,
                "center_distance": center_distance
            })

    df = pd.DataFrame(candidates)
    return df

def filter_by_ratio (df, target_ratio, tolerance):
    """
   Filter Candidate gear design to only those within a tolerance of the target ratio
    
    Args:
    df (DataFrame): Table of candidate gear designs with columns
    target_ratio(float): Desired gear ratio the candidates should approximate
    tolerance: tolerance
    
    Returns:
    df (DataFrame): Table of candidate gear designs with columns
    """
    mask = (df["actual_ratio"] >= target_ratio - tolerance) & (df["actual_ratio"] <= target_ratio + tolerance)
    filtered_df = df[mask]
    return filtered_df

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