from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import numpy as np

class subjects:
    def __init__(self, name, include2019, link, rawMarks, alignedMarks, polynomial):
        self.name = name
        self.include2019 = include2019
        self.link = link
        self.rawMarks = rawMarks
        self.alignedMarks = alignedMarks
        self.polynomial = polynomial

    def __repr__ (self):
        return f"Subject(name={self.name}, link={self.link})"

subjectsList = []

departmentList = ['english', 'mathematics' ,'science', 'technologies', 'hsie', 'creative-arts', 'pdhpe']

indexPage = requests.get("https://rawmarks.info/")
soup = BeautifulSoup(indexPage.text, "html.parser")
for link in soup.findAll("a"):
    address = link.get("href")

    isSubject = False

    for subject in departmentList:
        if subject in address and address.count('/') > 4:
            subjectsList.append(subjects('', False, address, [], [], ''))
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

def gettingInformation(subject):
    # Scrapping
    page_to_scrape = requests.get(subject.link).text
    soup = BeautifulSoup(page_to_scrape, "html.parser")
    name = soup.find('h1').text
    print(name)
    years = soup.findAll("td", attrs = {"class": "column-1"})
    rawMarks = soup.findAll("td", attrs = {"class": "column-2"})
    alignedMarks = soup.findAll("td", attrs = {"class": "column-3"})

    yearBoundary = 0

    rawMarksArray = []
    alignedMarksArray = []

    if subject.include2019:
        yearBoundary = 2019
    else:
        yearBoundary = 2020

    for year, rawMark, alignedMark in zip(years, rawMarks, alignedMarks):
        if int(year.text) >= yearBoundary:
            # print(year.text + " - " + rawMark.text + " - " + alignedMark.text)
            rawMarksArray.append(float(rawMark.text))
            alignedMarksArray.append(float(alignedMark.text))

    subject.name = name
    subject.rawMarks = rawMarksArray
    subject.alignedMarks = alignedMarksArray

    minBic = float('inf')
    bestPolynomial = None
    bestDegree = 0

    if len(rawMarksArray) < 10:
        return

    # Building Regression with Bayesian Information Criterion
    for degree in range(1, 6):
        if len(rawMarksArray) >= degree + 1:
            coefficients = np.polyfit(rawMarksArray, alignedMarksArray, degree)
            polynomial = np.poly1d(coefficients)

            if not is_monotonically_increasing(polynomial, rawMarksArray):
                print(f"Degree {degree} polynomial for {subject.name} is not monotonically increasing.")
                continue

            y_pred = polynomial(rawMarksArray)

            bic = calculate_bic(np.array(alignedMarksArray), y_pred, degree + 1)

            if bic < minBic:
                minBic = bic
                bestPolynomial = polynomial
                bestDegree = degree

    subject.polynomial = bestPolynomial
    print(f"Selected polynomial degree {bestDegree} for {subject.name} with BIC: {minBic}")


for subject in subjectsList:
    gettingInformation(subject)

def cleanUp():
    for subject in subjectsList[:]:
        if len(subject.rawMarks) < 10:
            subjectsList.remove(subject)

cleanUp()

def findSubject(subjectName):
    for subject in subjectsList:
        if subject.name == subjectName:
            return subject

def predictMarks(subjectName):
        subject = findSubject(subjectName)
        print("Enter Predicted Raw Marks")
        x = input()

        if 0 < float(x) and float(x) > 100:
            print("Pick a real mark lol")
            return

        newResult = subject.polynomial(float(x))

        band = ""

        if newResult >= 90:
            band = "Band 6"
        elif newResult >= 80:
            band = "Band 5"
        elif newResult >= 70:
            band = "Band 4"
        elif newResult >= 60:
            band = "Band 3"
        elif newResult >= 50:
            band = "Band 2"
        else:
            band = "Band 1"

        print("Your predicted HSC Mark for " + subjectName + " is " + str(round(newResult, 2)) + " which is a " + band)
        getPlot(subject)

def getPlot(subject):
    x_values = np.linspace(min(subject.rawMarks), max(subject.rawMarks), 100)
    y_values = subject.polynomial(x_values)
    plt.plot(x_values, y_values, label="Regression Line")
    plt.plot(subject.rawMarks, subject.alignedMarks, "o", label="Data points")
    plt.title("Raw Marks vs Aligned Marks for " + subject.name)
    plt.xlabel("Raw Marks")
    plt.ylabel("Aligned Marks")
    plt.show()

def shallowPrint():
    print("----------UPDATED LIST OF ITEMS----------")
    for subject in subjectsList:
        getPlot(subject)

shallowPrint()