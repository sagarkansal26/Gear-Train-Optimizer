import pytest
from pygments.styles import material

from src.calculations import calc_gear_ratio, rpm_to_omega, calc_driven_side, calc_driver_torque, calc_pitch_diameter, calc_tangential_force, calc_radial_force,calc_bending_stress,calc_safety_factor, get_lewis_form_factor, get_allowable_stress

def test_calc_gear_ratio():
    result = calc_gear_ratio(teeth_driver=20, teeth_driven=60)
    assert result == 3

def test_rpm_to_omega():
    result = rpm_to_omega(1500)
    assert result == pytest.approx(157, rel=1e-3)

def test_calc_driven_side():
    omega_driven, torque_driven = calc_driven_side(
        gear_ratio=3.0,
        omega_driver=157.0,
        torque_driver=31.85
    )
    assert omega_driven == pytest.approx(52.33, rel=1e-3)
    assert torque_driven == pytest.approx(95.54, rel=1e-3)

def test_calc_driver_torque():
    result = calc_driver_torque(power = 5000, omega_driver = 157)
    assert result == pytest.approx(31.85, rel=1e-3)

def test_calc_pitch_diameter():
    result = calc_pitch_diameter(module=2, teeth=20)
    assert result == 40   # pitch_diameter_driver from PROCESS.md

def test_calc_tangential_force():
    result = calc_tangential_force(torque=31.85, pitch_diameter_mm=40)
    assert result == pytest.approx(1592.5, rel=1e-3)   # tangential_force

def test_calc_radial_force():
    result = calc_radial_force(tangential_force=1592.5, pressure_angle_degree=20)
    assert result == pytest.approx(579.62, rel=1e-3)   # radial_force

def test_get_lewis_form_factor():
    result = get_lewis_form_factor(teeth=20)
    assert result == 0.29   # Y_factor, exact table match

def test_calc_bending_stress():
    result = calc_bending_stress(tangential_force=1592.5, module=2, face_width=20, y_factor=0.29)
    assert result == pytest.approx(137.28, rel=1e-3)   # bending_stress

def test_get_allowable_stress():
    result = get_allowable_stress("Steel (Low Carbon)")
    assert result == 138  # allowable_stress

def test_calc_safety_factor():
    result = calc_safety_factor(allowable_stress=138, bending_stress=137.28)
    assert result == pytest.approx(1.005, rel=1e-3)   # safety_factor

def test_get_allowable_stress_invalid_materials():
    with pytest.raises(ValueError, match = "Unknown material"):
        get_allowable_stress("Titanium")





