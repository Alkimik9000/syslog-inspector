import json

with open("secrets.json") as f: 
    secrets = json.load(f)

PEM_FILE_PATH = secrets["PEM_FILE_PATH"]
HOST = secrets["HOST"]
USERNAME = secrets["USERNAME"]

LOCAL_JSON_FOLDER = "json_results"
LOCAL_CSV_FILE = "results.csv"

REMOTE_JSON_FOLDER = "/home/ubuntu/json_results" 
REMOTE_PYTHON_SCRIPT = "syslog_inspect.py"