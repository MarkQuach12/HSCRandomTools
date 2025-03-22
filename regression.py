import matplotlib.pyplot as plt
import numpy as np
import json
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

current_directory = os.path.dirname(__file__)
data_directory = os.path.join(current_directory, 'data')
file_path = os.path.join(data_directory, 'raw_marks.json')

with open(file_path, 'r') as file:
    subjects = json.load(file)

def is_monotonically_increasing(polynomial, x_values):
    derivative = np.polyder(polynomial)
    derivative_values = derivative(x_values)
    return np.all(derivative_values >= 0)

def calculate_bic(y, y_pred, p):
    n = len(y)
    residual_sum_of_squares = np.sum((y - y_pred) ** 2)
    return n * np.log(residual_sum_of_squares / n) + p * np.log(n)

def polynomials(subject):
    min_bic = float('inf')
    best_polynomial = None

    for degree in range(1, 6):
        if len(subject['raw_marks']) >= degree + 1:
            coefficients = np.polyfit(subject['raw_marks'], subject["aligned_marks"], degree)
            polynomial = np.poly1d(coefficients)

            if not is_monotonically_increasing(polynomial, subject['raw_marks']):
                continue

            y_pred = polynomial(subject['raw_marks'])
            bic = calculate_bic(np.array(subject["aligned_marks"]), y_pred, degree + 1)

            if bic < min_bic:
                min_bic = bic
                best_polynomial = polynomial

    return best_polynomial

for subject_name, years_data in subjects.items():
    for year, marks in years_data.items():
        if len(marks["raw_marks"]) >= 5:
            polynomial = polynomials(marks)
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

@app.route('/predict', methods=['GET'])
def predict():
    subject_name = request.args.get('subject')
    raw_mark = request.args.get('raw_mark', type=float)

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
    app.run(debug=True)