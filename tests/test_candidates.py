import pandas as pd
import pytest
from src.candidates import generate_candidates, filter_by_ratio, calculate_row_metrics

def test_generate_candidates():
    result = generate_candidates(target_ratio=2.7, standard_modules=[1,2,3], teeth_range=[15,20,25])
    assert len(result) == 9
    assert list(result.columns) == ["module", "teeth_driver", "teeth_driven", "actual_ratio", "pitch_diameter_driver",
                                    "pitch_diameter_driven", "center_distance"]

def test_filter_by_ratio():
    candidates = generate_candidates(target_ratio=2.7, standard_modules=[1,2,3], teeth_range=[15,20,25])
    result = filter_by_ratio(candidates, target_ratio=2.7, tolerance=0.01)
    assert len(result) == 3
    assert (result["actual_ratio"] >= 2.7 - 0.01).all()
    assert (result["actual_ratio"] <= 2.7 + 0.01).all()

row = pd.Series({
    "pitch_diameter_driver": 40,
    "teeth_driver": 20,
    "module": 2
})

def test_calculate_row_metrics():
    result = calculate_row_metrics(row, torque_driver=31.85, pressure_angle=20, material_name="Steel (Low Carbon)")
    assert (result["tangential_force"]) == pytest.approx(1592.5, rel=1e-3)
    assert (result["radial_force"]) == pytest.approx (579.62, rel=1e-3)
    assert (result["bending_stress"]) == pytest.approx (137.28, rel=1e-3)
    assert (result["safety_factor"]) == pytest.approx (1.005, rel=1e-3)


