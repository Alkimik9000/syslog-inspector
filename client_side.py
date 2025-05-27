from SshToServer import SshToServer
from config import REMOTE_PYTHON_SCRIPT, LOCAL_JSON_FOLDER, LOCAL_CSV_FILE, REMOTE_JSON_FOLDER, USERNAME, HOST, PEM_FILE_PATH
import pandas as pd
import subprocess
import json
import os
import time

def append_to_csv(file_path, row_data):
    df_new = pd.DataFrame([row_data])
    if os.path.isfile(file_path):
        df_existing = pd.read_csv(file_path)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new
    df_combined.to_csv(file_path, index=False)

print("About to attempt to connect to remote server using SSH")
my_ssh = SshToServer()
print("Connections to Remote Server Succeeded")

# Create json file remotely and Extract the remote filename and path
output = my_ssh.execCommand("python3 " + REMOTE_PYTHON_SCRIPT)
lines = [line.strip() for line in output.split('\n') if line.strip()]
remote_filename = lines[-1]

os.makedirs(LOCAL_JSON_FOLDER, exist_ok=True)

local_filename = os.path.abspath(os.path.join(LOCAL_JSON_FOLDER, os.path.basename(remote_filename)))

print("Waiting for file to be written on server")
time.sleep(3)

print("Fetching file using scp")
remote_path = USERNAME + "@" + HOST + ":" + remote_filename
scp_command = ["scp", "-i", PEM_FILE_PATH, remote_path, local_filename]

try:
    subprocess.run(scp_command, check=True)
except subprocess.CalledProcessError as e:
    print("scp failed:", e)
    raise

print("Extracting data from JSON and writing it to results.csv databae")
with open(local_filename, 'r') as f:
    data = json.load(f)
append_to_csv(LOCAL_CSV_FILE, data)

my_ssh.close()
print("Processing complete")
