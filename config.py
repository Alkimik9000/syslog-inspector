import json
import os

# Load sensitive credentials from secrets.json for secure SSH access
with open(os.path.join(os.path.dirname(__file__), "secrets.json")) as f:
    secrets = json.load(f)

PEM_FILE_PATH: str = secrets["PEM_FILE_PATH"]
HOST: str = secrets["HOST"]
USERNAME: str = secrets["USERNAME"]

LOCAL_CSV_FILE: str = "results.csv"
REMOTE_PYTHON_SCRIPT: str = "syslog_inspect.py"