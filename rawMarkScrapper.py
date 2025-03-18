from bs4 import BeautifulSoup
import requests
import numpy as np
import json
import os

class Subject:
    def __init__(self, name='', link='', raw_marks=None, aligned_marks=None, polynomial=None):
        self.name = name
        self.link = link
        self.raw_marks = raw_marks if raw_marks is not None else []
        self.aligned_marks = aligned_marks if aligned_marks is not None else []

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

    subject.raw_marks = [raw for year, raw in zip(years, raw_marks) if year >= 2020]
    subject.aligned_marks = [aligned for year, aligned in zip(years, aligned_marks) if year >= 2020]

    if len(subject.raw_marks) < 10:
        return

def clean_up(subjects):
    return [subject for subject in subjects if len(subject.raw_marks) >= 10]

def dictionaryConversion(subjects, default_value=None):
    return {subject.name:
            {"raw_marks": subject.raw_marks,
             "aligned_marks": subject.aligned_marks} for subject in subjects}

def main():
    subjects_list = fetch_subject_links()
    for subject in subjects_list:
        get_information(subject)
    subjects_list = clean_up(subjects_list)
    subjects_list = dictionaryConversion(subjects_list)

    current_directory = os.path.dirname(__file__)
    data_directory = os.path.join(current_directory, 'data')
    file_path = os.path.join(data_directory, 'raw_marks.json')

    with open(file_path, 'w') as _f:
        json.dump(subjects_list, _f, indent=4)

if __name__ == "__main__":
    main()