import json
import os
# from dotenv import load_dotenv
from supabase import create_client, Client

# load_dotenv()

supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY"),
)

current_directory = os.path.dirname(__file__)
data_directory = os.path.join(current_directory, '..' ,'data')
file_path_band6 = os.path.join(data_directory, 'band6Marks.json')

with open(file_path_band6, "r") as f:
    band6_marks = json.load(f)

rows = []
for school, subjects in band6_marks.items():
    for subject, years in subjects.items():
        for year, band6_count in years.items():
            rows.append(
                {
                    "school": school,
                    "subject": subject,
                    "subject": subject,
                    "year": int(year),
                    "num_band6": band6_count
                }
            )

for i in range(0, len(rows), 100):
    supabase.table("Band 6 Data").insert(rows[i:i+100]).execute()