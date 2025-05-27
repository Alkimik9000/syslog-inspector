
import subprocess
import json
import os
import time

import pandas as pd

from config import REMOTE_PYTHON_SCRIPT, LOCAL_JSON_FOLDER, LOCAL_CSV_FILE, USERNAME, HOST, PEM_FILE_PATH
from ssh_to_server import SshToServer


def appendToCSV(file_path, row_data):
    df_new = pd.DataFrame([row_data])
    if os.path.isfile(file_path):
        df_existing = pd.read_csv(file_path)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new
    df_combined.to_csv(file_path, index=False)

print("Connecting to remote server...")
my_ssh = SshToServer()
print("Connected to remote server")

# Run remote script to generate JSON file for log analysis
output = my_ssh.execCommand("python3 " + REMOTE_PYTHON_SCRIPT)
lines = [line.strip() for line in output.split('\n') if line.strip()]
remote_filename = lines[-1]

print("Waiting for file creation on server...")
time.sleep(3)

print("Copying file from server: " + remote_filename)
local_filename = os.path.abspath(os.path.join(LOCAL_JSON_FOLDER, os.path.basename(remote_filename)))
remote_path = USERNAME + "@" + HOST + ":" + remote_filename
scp_command = ["scp", "-i", PEM_FILE_PATH, remote_path, local_filename]

try:
    subprocess.run(scp_command, check=True)
except subprocess.CalledProcessError as e:
    print("scp failed:", e)
    raise

print("Processing " + os.path.basename(local_filename) + " and appending to " + LOCAL_CSV_FILE)
os.makedirs(LOCAL_JSON_FOLDER, exist_ok=True)
with open(local_filename, 'r') as f:
    data = json.load(f)
appendToCSV(LOCAL_CSV_FILE, data)

my_ssh.close()
print("Process completed")