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

# print(subjectsList)
# for subject in subjectsList:
#     page_to_scrape = requests.get("https://rawmarks.info/mathematics/" + subject.name + "/")

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

    # Building Regression
    if len(rawMarksArray) >= 10:
        coefficients = np.polyfit(rawMarksArray, alignedMarksArray, 3)
        polynomial = np.poly1d(coefficients)
        subject.polynomial = polynomial
    subject.name = name
    subject.rawMarks = rawMarksArray
    subject.alignedMarks = alignedMarksArray

    # print(len(subject.polynomial))

for subject in subjectsList:
    gettingInformation(subject)

def cleanUp():
    for subject in subjectsList[:]:
        if len(subject.rawMarks) < 10:
            subjectsList.remove(subject)

cleanUp()

def shallowPrint():
    for subject in subjectsList[:]:
        print(subject.name)

shallowPrint()

# print(subjectsList)

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