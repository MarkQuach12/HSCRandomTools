import json
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY"),
)

current_directory = os.path.dirname(__file__)
data_directory = os.path.join(current_directory, '..' ,'data')
file_path_rawMarks = os.path.join(data_directory, 'raw_marks.json')

with open(file_path_rawMarks, "r") as f:
    raw_marks = json.load(f)

rows = []

for subject, years in raw_marks.items():
    for year, marks in years.items():
        for raw, aligned in zip(marks["raw_marks"], marks["aligned_marks"]):
            rows.append(
                {
                    "subject": subject,
                    "year": year,
                    "raw_mark": raw,
                    "aligned_mark": aligned,
                }
            )

for i in range(0, len(rows), 100):
    supabase.table("Raw Mark Polynomials").insert(rows[i:i+100]).execute()