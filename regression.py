import matplotlib.pyplot as plt
import numpy as np
import json
import os


def main():
    current_directory = os.path.dirname(__file__)
    data_directory = os.path.join(current_directory, 'data')
    file_path = os.path.join(data_directory, 'raw_marks.json')

    with open(file_path, 'r') as file:
        subjects = json.load(file).items()

    for subject in subjects:
        polynomial = polynomials(subject[1])
        subject[1]["polynomial"] = polynomial

    subjectName = input("What subject are your curious about?\n")
    subjectInQuestion = findSubject(subjectName, subjects)
    predict_marks(subjectInQuestion)


def findSubject(name, subjects):
    for subject in subjects:
        if name == subject[0]:
            return subject

    return None

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

def calculate_bic(y, y_pred, p):
    n = len(y)
    residual_sum_of_squares = np.sum((y - y_pred) ** 2)
    return n * np.log(residual_sum_of_squares / n) + p * np.log(n)

def is_monotonically_increasing(polynomial, x_values):
    derivative = np.polyder(polynomial)
    derivative_values = derivative(x_values)
    return np.all(derivative_values >= 0)

def predict_marks(subject):
    raw_mark = get_valid_raw_mark()

    if raw_mark is None:
        return

    predicted_mark = subject[1]["polynomial"](raw_mark)
    band = determine_band(predicted_mark)

    print(f"Your predicted HSC Mark for {subject[0]} is {round(predicted_mark, 2)}, which is a {band}")
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

def plot_subject(subject):
    x_values = np.linspace(min(subject[1]["raw_marks"]), max(subject[1]["raw_marks"]), 100)
    y_values = subject[1]["polynomial"](x_values)
    plt.plot(x_values, y_values, label="Regression Line")
    plt.plot(subject[1]["raw_marks"], subject[1]["aligned_marks"], "o", label="Data points")
    plt.title(f"Raw Marks vs Aligned Marks for {subject[0]}")
    plt.xlabel("Raw Marks")
    plt.ylabel("Aligned Marks")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()