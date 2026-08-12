lewis_form_factors = {
    12: 0.245, 14: 0.261, 17: 0.277, 20: 0.290, 24: 0.302,
    30: 0.314, 40: 0.336, 60: 0.355, 75: 0.371, 100: 0.400,
    150: 0.446, 300: 0.506
}

closest_teeth = min(lewis_form_factors.keys(), key=lambda t: abs(t - 23))
y_factor = lewis_form_factors[closest_teeth]
print(f"closest_teeth={closest_teeth}, y_factor={y_factor}")