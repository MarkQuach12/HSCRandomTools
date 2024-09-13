from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import numpy as np

class Subject:
    def __init__(self, name, include_2019, link, raw_marks, aligned_marks, polynomial):
        self.name = name
        self.include_2019 = include_2019
        self.link = link
        self.raw_marks = raw_marks
        self.aligned_marks = aligned_marks
        self.polynomial = polynomial

    def __repr__ (self):
        return f"Subject(name={self.name}, link={self.link})"

subjects_list = []

department_list = ['english', 'mathematics', 'science', 'technologies', 'hsie', 'creative-arts', 'pdhpe']

index_page = requests.get("https://rawmarks.info/")
soup = BeautifulSoup(index_page.text, "html.parser")
for link in soup.findAll("a"):
    address = link.get("href")

    for subject in department_list:
        if subject in address and address.count('/') > 4:
            subjects_list.append(Subject('', False, address, [], [], ''))
            break
    continue

def calculate_bic(y, y_pred, p):
    """
    Calculate BIC using the residual sum of squares method.
    """
    n = len(y)
    residual_sum_of_squares = np.sum((y - y_pred) ** 2)
    bic_score = n * np.log(residual_sum_of_squares / n) + p * np.log(n)
    return bic_score

def is_monotonically_increasing(polynomial, x_values):
    derivative = np.polyder(polynomial)
    derivative_values = derivative(x_values)

    return np.all(derivative_values >= 0)

def get_information(subject):
    # Scraping
    page_to_scrape = requests.get(subject.link).text
    soup = BeautifulSoup(page_to_scrape, "html.parser")
    name = soup.find('h1').text
    print(name)
    years = soup.findAll("td", attrs={"class": "column-1"})
    raw_marks = soup.findAll("td", attrs={"class": "column-2"})
    aligned_marks = soup.findAll("td", attrs={"class": "column-3"})

    year_boundary = 0

    raw_marks_array = []
    aligned_marks_array = []

    if subject.include_2019:
        year_boundary = 2019
    else:
        year_boundary = 2020

    for year, raw_mark, aligned_mark in zip(years, raw_marks, aligned_marks):
        if int(year.text) >= year_boundary:
            raw_marks_array.append(float(raw_mark.text))
            aligned_marks_array.append(float(aligned_mark.text))

    subject.name = name
    subject.raw_marks = raw_marks_array
    subject.aligned_marks = aligned_marks_array

    min_bic = float('inf')
    best_polynomial = None
    best_degree = 0

    if len(raw_marks_array) < 10:
        return

    # Building Regression with Bayesian Information Criterion
    for degree in range(1, 6):
        if len(raw_marks_array) >= degree + 1:
            coefficients = np.polyfit(raw_marks_array, aligned_marks_array, degree)
            polynomial = np.poly1d(coefficients)

            if not is_monotonically_increasing(polynomial, raw_marks_array):
                print(f"Degree {degree} polynomial for {subject.name} is not monotonically increasing.")
                continue

            y_pred = polynomial(raw_marks_array)

            bic = calculate_bic(np.array(aligned_marks_array), y_pred, degree + 1)

            if bic < min_bic:
                min_bic = bic
                best_polynomial = polynomial
                best_degree = degree

    subject.polynomial = best_polynomial
    print(f"Selected polynomial degree {best_degree} for {subject.name} with BIC: {min_bic}")

for subject in subjects_list:
    get_information(subject)

def clean_up():
    for subject in subjects_list[:]:
        if len(subject.raw_marks) < 10:
            subjects_list.remove(subject)

clean_up()

def find_subject(subject_name):
    for subject in subjects_list:
        if subject.name == subject_name:
            return subject

def predict_marks(subject_name):
    subject = find_subject(subject_name)
    print("Enter Predicted Raw Marks")
    x = input()

    if 0 < float(x) and float(x) > 100:
        print("Pick a real mark lol")
        return

    new_result = subject.polynomial(float(x))

    band = ""

    if new_result >= 90:
        band = "Band 6"
    elif new_result >= 80:
        band = "Band 5"
    elif new_result >= 70:
        band = "Band 4"
    elif new_result >= 60:
        band = "Band 3"
    elif new_result >= 50:
        band = "Band 2"
    else:
        band = "Band 1"

    print(f"Your predicted HSC Mark for {subject_name} is {str(round(new_result, 2))}, which is a {band}")
    get_plot(subject)

def get_plot(subject):
    x_values = np.linspace(min(subject.raw_marks), max(subject.raw_marks), 100)
    y_values = subject.polynomial(x_values)
    plt.plot(x_values, y_values, label="Regression Line")
    plt.plot(subject.raw_marks, subject.aligned_marks, "o", label="Data points")
    plt.title(f"Raw Marks vs Aligned Marks for {subject.name}")
    plt.xlabel("Raw Marks")
    plt.ylabel("Aligned Marks")
    plt.show()

def shallow_print():
    print("----------UPDATED LIST OF ITEMS----------")
    for subject in subjects_list:
        get_plot(subject)

shallow_print()
