import matplotlib.pyplot as plt
import numpy as np
import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

current_directory = os.path.dirname(__file__)
data_directory = os.path.join(current_directory, 'data')
file_path = os.path.join(data_directory, 'raw_marks.json')

with open(file_path, 'r') as file:
    subjects = json.load(file)


def is_monotonically_increasing(func, x_min=0, x_max=100, step=0.1, tolerance=1e-6):
    x_vals = np.arange(x_min, x_max + step, step)
    y_vals = func(x_vals)
    diffs = np.diff(y_vals)
    return np.all(diffs >= -tolerance)


def calculate_bic(y, y_pred, p):
    n = len(y)
    residual_sum_of_squares = np.sum((y - y_pred) ** 2)
    return n * np.log(residual_sum_of_squares / n) + p * np.log(n)

import numpy as np

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

for subject_name, years_data in subjects.items():
    for year, marks in years_data.items():
        if len(marks["raw_marks"]) >= 5:
            polynomial = constrained_polynomials(marks)
            marks["polynomial"] = polynomial

def main():
    subjectName = input("What subject are your curious about?\n")
    subjectInQuestion = subjects.get(subjectName)
    predict_marks(subjectInQuestion)


def predict_marks(subject):
    raw_mark = get_valid_raw_mark()

    if raw_mark is None:
        return

    print(f"\nPredicted Marks for {subject[0]}:")

    for year, marks in subject[1].items():
        if "polynomial" in marks and marks["polynomial"] is not None:
            predicted_mark = marks["polynomial"](raw_mark)
            band = determine_band(predicted_mark)

            print(f"Year {year}: Predicted Aligned Mark = {round(predicted_mark, 2)}, {band}")


    # predicted_mark = subject[1]["polynomial"](raw_mark)
    # band = determine_band(predicted_mark)

    # print(f"Your predicted HSC Mark for {subject[0]} is {round(predicted_mark, 2)}, which is a {band}")
    # plot_subject(subject)

def get_valid_raw_mark():
    try:
        raw_mark = float(input("Enter Predicted Raw Marks: "))
        if not (0 < raw_mark <= 100):
            print("Pick a real mark lol")
            return None
        return raw_mark
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None

def determine_band(mark):
    if mark >= 90:
        return "Band 6"
    elif mark >= 80:
        return "Band 5"
    elif mark >= 70:
        return "Band 4"
    elif mark >= 60:
        return "Band 3"
    elif mark >= 50:
        return "Band 2"
    else:
        return "Band 1"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    subject_name = data.get('subject')
    raw_mark = data.get('rawMark')

    if not subject_name or raw_mark is None:
        return jsonify({'error': 'Missing subject name or raw mark'}), 400

    subject = subjects.get(subject_name)

    print(subject)
    if not subject:
        return jsonify({'error': 'Subject not found'}), 404

    predictions = []

    for years, marks in subject.items():
        if "polynomial" in marks and marks["polynomial"] is not None:
            predicted_mark = marks["polynomial"](raw_mark)
            predictions.append({'year': years, 'predicted_mark': round(predicted_mark, 2)})

    return jsonify({'predictions': predictions})

file_path_band6 = os.path.join(data_directory, 'band6Marks.json')
with open(file_path_band6, 'r', encoding='utf-8') as f:
    band6_data = json.load(f)

@app.route('/band6', methods=['POST'])
def get_band6():
    data = request.get_json()
    school_name = data.get('school')

    if not school_name:
        return jsonify({'error': 'Missing school name'}), 400

    school_data = band6_data.get(school_name)

    if not school_data:
        return jsonify({'error': 'School not found'}), 404

    return jsonify({'school_data': school_data})

# def plot_subject(subject):
#     x_values = np.linspace(min(subject[1]["raw_marks"]), max(subject[1]["raw_marks"]), 100)
#     y_values = subject[1]["polynomial"](x_values)
#     plt.plot(x_values, y_values, label="Regression Line")
#     plt.plot(subject[1]["raw_marks"], subject[1]["aligned_marks"], "o", label="Data points")
#     plt.title(f"Raw Marks vs Aligned Marks for {subject[0]}")
#     plt.xlabel("Raw Marks")
#     plt.ylabel("Aligned Marks")
#     plt.legend()
#     plt.show()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)