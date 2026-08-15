#Func 1#
def filter_safe_candidates(df, min_safety_factor):
    """
    Filter candidates to only those meeting a minimum safety factor.

    Args:
        df (DataFrame): Table of candidates, must contain a safety_factor column.
        min_safety_factor (float): Minimum acceptable safety factor.

    Returns:
        df (DataFrame): Filtered table of candidates that are "safe".
    """
    mask = df["safety_factor"] >= min_safety_factor
    safe_df = df[mask]

    if safe_df.empty:
        print(f"No candidates met the minimum safety factor of {min_safety_factor}.")

    return safe_df

#Func 2#
def select_best_candidate(df):
    """
    Select the single best candidate from a table of safe candidates.

    Args:
        df (DataFrame): Table of candidates, must contain a safety_factor column.
                         Expected to already be filtered to only safe candidates.

    Returns:
        Series: The row with the highest safety_factor.
    """
    if df.empty:
        print("No candidates available to select from.")
        return None

    best_row = df.loc[df["safety_factor"].idxmax()]
    return best_row