import requests
import string
import json
import os

headers = { "Content-Type": "application/json" }

def url_by_year(year):

    if year == 2021:
        return "https://www.nsw.gov.au/api/v1/elasticsearch/prod_nesa_2021_hsc_distinguished_achievers_0/_search"
    return f"https://www.nsw.gov.au/api/v1/elasticsearch/prod_nesa_{year}_hsc_distinguished_achievers/_search"

def fetch_students_by_letter(letter, year):
    payload = {
        "from": 0,
        "size": 10000,
        "query": {
            "bool": {
                "must": [],
                "should": { "match_all": {} },
                "filter": {
                    "prefix": {
                        "last_name.keyword": {
                            "value": letter,
                            "case_insensitive": True
                        }
                    }
                }
            }
        },
        "sort": [
            {
                "_script": {
                    "type": "string",
                    "script": {
                        "lang": "painless",
                        "source": "/<[^\>]*>/.matcher(doc['last_name.keyword'].value).replaceAll('').toLowerCase()"
                    },
                    "order": "asc"
                }
            }
        ]
    }

    response = requests.post(url_by_year(year), headers=headers, json=payload)
    if response.ok:
        return response.json().get("hits", {}).get("hits", [])
    else:
        print(f"Failed to fetch for {letter}: {response.status_code}")
        print(f"Response: {response.text}")
        return []

band6Count = {}

for letter in string.ascii_uppercase:
    print(f"Fetching students with last names starting with '{letter}'")

    for year in range(2020, 2025):
        students = fetch_students_by_letter(letter, year)

        for entry in students:
            src = entry["_source"]
            school = src.get("main_school_name")
            subject = src.get("top_band_courses")

            if not (school and subject):
                continue

            subject = subject.strip()
            if year == 2023 or year == 2024:
                subject = subject[8:]
            else:
                subject = subject[6:]

            if school not in band6Count:
                band6Count[school] = {}

            if subject not in band6Count[school]:
                band6Count[school][subject] = {}

            if year not in band6Count[school][subject]:
                band6Count[school][subject] = {
                    y : 0 for y in range(2024, 2019, -1)
                }
            else:
                band6Count[school][subject][year] += 1

current_directory = os.path.dirname(__file__)
data_directory = os.path.join(current_directory, 'data')
file_path = os.path.join(data_directory, 'band6Marks.json')

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(band6Count, f, indent=2, ensure_ascii=False)

print("Done")
