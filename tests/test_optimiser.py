from src.optimiser import filter_safe_candidates, select_best_candidate
import pytest
import pandas as pd

df = pd.DataFrame([
    {"module": 1, "safety_factor": 0.5},
    {"module": 2, "safety_factor": 1.2},
    {"module": 3, "safety_factor": 2.8},
])

def test_filter_safe_candidates():
    result = filter_safe_candidates(df, min_safety_factor=1.5)
    assert len(result) == 1
    assert (result["safety_factor"] >= 1.5).all()

def test_select_best_candidate():
    result = select_best_candidate(df)
    assert result["safety_factor"] == pytest.approx(2.8, rel=1e-3)
    assert result["module"] == 3