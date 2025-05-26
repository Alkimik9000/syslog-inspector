from SshToServer import SshToServer
import subprocess
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

my_ssh = SshToServer("/Users/markofir/Downloads/key-pair.pem", "51.20.1.114", "ubuntu")
output = my_ssh.runShellCommand("python3 inspect_syslog_server_side.py")


lines = output.strip().split('\n')
remote_filename = lines[-2].strip()

os.makedirs(local_json_folder, exist_ok=True)



