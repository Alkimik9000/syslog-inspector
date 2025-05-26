from SshToServer import SshToServer
from config import REMOTE_PYTHON_SCRIPT, LOCAL_JSON_FOLDER, LOCAL_CSV_FILE
import pandas as pd
import json
import os

def append_to_csv(file_path, row_data):
    df_new = pd.DataFrame([row_data])
    if os.path.isfile(file_path):
        df_existing = pd.read_csv(file_path)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new
    df_combined.to_csv(file_path, index=False)

my_ssh = SshToServer()

output = my_ssh.runShellCommand("python3 " + REMOTE_PYTHON_SCRIPT)

lines = output.strip().split('\n')
lines = [line.strip() for line in output.split('\n') if line.strip()]
remote_filename = lines[-1] 

os.makedirs(LOCAL_JSON_FOLDER, exist_ok=True)

local_filename = os.path.join(LOCAL_JSON_FOLDER, os.path.basename(remote_filename))

sftp = my_ssh.sshClient.open_sftp()
sftp.get(remote_filename, local_filename)
sftp.close()

with open(local_filename, 'r') as f:
    data = json.load(f)
append_to_csv(LOCAL_CSV_FILE, data)