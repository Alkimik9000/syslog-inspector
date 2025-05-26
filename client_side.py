from SshToServer import SshToServer
from config import REMOTE_PYTHON_SCRIPT, LOCAL_JSON_FOLDER, LOCAL_CSV_FILE, REMOTE_JSON_FOLDER
import pandas as pd
import json
import os

print("starting script")

def append_to_csv(file_path, row_data):
    df_new = pd.DataFrame([row_data])
    if os.path.isfile(file_path):
        df_existing = pd.read_csv(file_path)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new
    df_combined.to_csv(file_path, index=False)

print("about to connect to server")
my_ssh = SshToServer()
print("connveted to server with ssh")

output = my_ssh.runShellCommand("python3 " + REMOTE_PYTHON_SCRIPT)
print("Sent command to server")
print("Remote output:", output)  # Debug

remote_filename = output.strip()
print("remote_filename:", remote_filename)  # Debug

os.makedirs(LOCAL_JSON_FOLDER, exist_ok=True)

local_filename = os.path.join(LOCAL_JSON_FOLDER, os.path.basename(remote_filename))

my_ssh = SshToServer()
sftp = my_ssh.getSftpConnection()  # This will now work
sftp.get(REMOTE_JSON_FOLDER + remote_filename, LOCAL_JSON_FOLDER + remote_filename)
sftp.close()  # Close the SFTP connection when done
my_ssh.close()  # Close the SSH connection

with open(local_filename, 'r') as f:
    data = json.load(f)
append_to_csv(LOCAL_CSV_FILE, data)