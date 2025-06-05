import json
import os

import pandas as pd

from config import REMOTE_PYTHON_SCRIPT, LOCAL_CSV_FILE
from ssh_to_server import SshToServer


def appendToCsv(file_path, row_data):
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

output = my_ssh.execCommand("python3 " + REMOTE_PYTHON_SCRIPT)

try:
    data = json.loads(output)
except json.JSONDecodeError as e:
    print("Failed to decode JSON from remote script:", e)
    my_ssh.close()
    raise

print("Appending remote syslog summary to " + LOCAL_CSV_FILE)
appendToCsv(LOCAL_CSV_FILE, data)

my_ssh.close()
print("Process completed")
