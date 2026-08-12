import pandas as pd

def generate_candidates(target_ratio, standard_modules, teeth_range):
    """
    Calculating Candidates

    Args:
    target_ratio(float): Desired gear ratio the candidates should approximate
    standard_modules: list of standard modules
    teeth_range: range of teeth

    Returns:
    df (DataFrame): Table of candidate gear designs with columns
        module, teeth_driver, teeth_driven, actual_ratio.
    """
    candidates = []   # empty list to collect rows

    for module in standard_modules:
        for teeth_driver in teeth_range:
            teeth_driven = round(teeth_driver * target_ratio)
            actual_ratio = teeth_driven / teeth_driver

            candidates.append({
                "module": module,
                "teeth_driver": teeth_driver,
                "teeth_driven": teeth_driven,
                "actual_ratio": actual_ratio
            })

    df = pd.DataFrame(candidates)
    return df

result_df = generate_candidates(2.7, [1, 2, 3], [15, 20, 25])
print(result_df)