from src.calculations import calc_pitch_diameter
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

