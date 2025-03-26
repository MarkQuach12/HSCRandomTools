from bs4 import BeautifulSoup
import requests
import numpy as np
import json
import os

class Subject:
    def __init__(self, name='', link='', raw_marks=None, aligned_marks=None, polynomial=None):
        self.name = name
        self.link = link
        self.years = {}

    def add_year_data(self, year, raw_mark, aligned_mark):
        if year not in self.years:
            self.years[year] = {"raw_marks": [], "aligned_marks": []}

        self.years[year]["raw_marks"].append(raw_mark)
        self.years[year]["aligned_marks"].append(aligned_mark)

    def __repr__(self):
        return f"Subject(name={self.name}, link={self.link})"

def fetch_subject_links():
    department_list = ['english', 'mathematics', 'science', 'technologies', 'hsie', 'creative-arts', 'pdhpe']
    index_page = requests.get("https://rawmarks.info/")
    soup = BeautifulSoup(index_page.text, "html.parser")
    subjects = []

    for link in soup.find_all("a"):
        address = link.get("href")
        if any(subject in address for subject in department_list) and address.count('/') > 4:
            subjects.append(Subject(link=address))
    return subjects

def get_information(subject):
    page_to_scrape = requests.get(subject.link).text
    soup = BeautifulSoup(page_to_scrape, "html.parser")
    subject.name = soup.find('h1').text
    print(subject.name)

    years = [int(year.text) for year in soup.find_all("td", class_="column-1")]
    raw_marks = [float(mark.text) for mark in soup.find_all("td", class_="column-2")]
    aligned_marks = [float(mark.text) for mark in soup.find_all("td", class_="column-3")]

    for information in zip(years, raw_marks, aligned_marks):
        if information[0] >= 2019:
            subject.add_year_data(information[0], information[1], information[2])


def dictionaryConversion(subjects):
    return {
        subject.name: {
            year: {
                "raw_marks": data["raw_marks"],
                "aligned_marks": data["aligned_marks"]
            }
            for year, data in subject.years.items()
        }
        for subject in subjects
    }


def main():
    subjects_list = fetch_subject_links()
    for subject in subjects_list:
        get_information(subject)
    subjects_list = dictionaryConversion(subjects_list)

    current_directory = os.path.dirname(__file__)
    data_directory = os.path.join(current_directory, 'data')
    file_path = os.path.join(data_directory, 'raw_marks.json')

    with open(file_path, 'w') as _f:
        json.dump(subjects_list, _f, indent=4)

if __name__ == "__main__":
    main()