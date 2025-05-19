import json
import os

def load_subjects():
    current_directory = os.path.dirname(__file__)
    data_directory = os.path.join(current_directory, '..' ,'data')
    file_path_band6 = os.path.join(data_directory, 'band6Marks.json')
    with open(file_path_band6, 'r', encoding='utf-8') as f:
        band6_data = json.load(f)
    return band6_data

band6_data = load_subjects()

