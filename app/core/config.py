import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build the path to the JSON file
json_path = os.path.join(BASE_DIR, 'testdata.json')

SHEET_KEY = "1fkllLw5dIi9frCz0FV19PJinZd9-Yc3wG51FEyYkS_Q"
CREDENTIALS_PATH = json_path
ROWS_PER_SHEET = 800
