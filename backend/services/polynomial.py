import numpy as np
import json
import os

def is_monotonically_increasing(func, x_min=0, x_max=100, step=0.1, tolerance=1e-6):
    x_vals = np.arange(x_min, x_max + step, step)
    y_vals = func(x_vals)
    diffs = np.diff(y_vals)
    return np.all(diffs >= -tolerance)

def calculate_bic(y, y_pred, p):
    n = len(y)
    residual_sum_of_squares = np.sum((y - y_pred) ** 2)
    return n * np.log(residual_sum_of_squares / n) + p * np.log(n)

def constrained_polynomials(subject, max_degree=5):
    min_bic = float('inf')
    best_poly = None

    x = np.array(subject['raw_marks'])
    y = np.array(subject['aligned_marks'])

    for degree in range(1, max_degree + 1):
        if len(x) >= degree + 1:
            coeffs = np.polyfit(x, y, degree)
            poly = np.poly1d(coeffs)

            # Scale the whole polynomial so that f(100) = 100
            scale = 100 / poly(100)
            scaled_poly = np.poly1d(poly.coefficients * scale)

            if not is_monotonically_increasing(scaled_poly):
                continue

            y_pred = scaled_poly(x)
            bic = calculate_bic(y, y_pred, degree + 1)

            if bic < min_bic:
                min_bic = bic
                best_poly = scaled_poly

    return best_poly

def load_subjects():
    current_directory = os.path.dirname(__file__)
    data_directory = os.path.join(current_directory, '..' ,'data')
    file_path = os.path.join(data_directory, 'raw_marks.json')

    with open(file_path, 'r') as file:
        subjects_polynomial = json.load(file)

    for subject_name, years_data in subjects_polynomial.items():
        for year, marks in years_data.items():
            if len(marks["raw_marks"]) >= 5:
                polynomial = constrained_polynomials(marks)
                marks["polynomial"] = polynomial
    return subjects_polynomial

subjects_polynomial = load_subjects()