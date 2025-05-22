import numpy as np
from supabase_client.client import supabase
from collections import defaultdict

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

def load_subjects(subject):
    response = supabase.table("Raw Mark Polynomials").select("*").eq("subject", subject).execute()
    rows = response.data

    subject_polynomial = {}

    for row in rows:
        subject_name = row['subject']
        year = row['year']
        raw_mark = row['raw_mark']
        aligned_mark = row['aligned_mark']

        if subject_name not in subject_polynomial:
            subject_polynomial[subject_name] = {}
        if year not in subject_polynomial[subject_name]:
            subject_polynomial[subject_name][year] = {
                "raw_marks": [],
                "aligned_marks": [],
                "polynomial": None
            }

        subject_polynomial[subject_name][year]["raw_marks"].append(raw_mark)
        subject_polynomial[subject_name][year]["aligned_marks"].append(aligned_mark)

    for subject_name, years_data in subject_polynomial.items():
        for year, marks in years_data.items():
            if len(marks["raw_marks"]) >= 5:
                polynomial = constrained_polynomials(marks)
                marks["polynomial"] = polynomial
    return subject_polynomial