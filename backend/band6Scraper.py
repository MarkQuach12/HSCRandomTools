import requests
import string
import json
import os

url = "https://www.nsw.gov.au/api/v1/elasticsearch/prod_nesa_2024_hsc_distinguished_achievers/_search"
headers = { "Content-Type": "application/json" }

def fetch_students_by_letter(letter):
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

    response = requests.post(url, headers=headers, json=payload)
    if response.ok:
        return response.json().get("hits", {}).get("hits", [])
    else:
        print(f"Failed to fetch for {letter}: {response.status_code}")
        return []

band6Count = {}

for letter in string.ascii_uppercase:
    print(f"Fetching students with last names starting with '{letter}'")
    students = fetch_students_by_letter(letter)

    for entry in students:
        src = entry["_source"]
        school = src.get("main_school_name")
        subject = src.get("top_band_courses")

        if not (school and subject):
            continue

        subject = subject.strip()
        subject = subject[8:]

        if school not in band6Count:
            band6Count[school] = {}

        if subject not in band6Count[school]:
            band6Count[school][subject] = 1
        else:
            band6Count[school][subject] += 1

current_directory = os.path.dirname(__file__)
data_directory = os.path.join(current_directory, 'data')
file_path = os.path.join(data_directory, 'band6Marks.json')

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(band6Count, f, indent=2, ensure_ascii=False)

print("Done")
