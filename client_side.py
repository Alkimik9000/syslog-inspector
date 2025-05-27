from SshToServer import SshToServer
from config import REMOTE_PYTHON_SCRIPT, LOCAL_JSON_FOLDER, LOCAL_CSV_FILE, REMOTE_JSON_FOLDER, USERNAME, HOST, PEM_FILE_PATH
import pandas as pd
import subprocess
import json
import os
import time

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

# Extract the remote filename
output = my_ssh.execCommand("python3 " + REMOTE_PYTHON_SCRIPT)
print("Sent command to server")
print("Raw output from server:", repr(str(output)))  # Debug: See the exact output

lines = [line.strip() for line in output.split('\n') if line.strip()]
print("Processed lines:", lines)  # Debug: See the list of lines

# Check if there’s at least one line
if not lines:
    print("Error: No output from remote command.")
    print("Raw output:", repr(output))
    raise ValueError("Could not find remote filename in output")

# Use the last line as the remote filename
remote_filename = lines[-1]
print("remote_filename: " + remote_filename)  # Debug

# Optional: Validate the file path format
if not remote_filename.startswith('/home/ubuntu/json_results/results-'):
    print("Error: Invalid file path format.")
    print("Extracted path:", remote_filename)
    raise ValueError("Invalid remote filename format")

os.makedirs(LOCAL_JSON_FOLDER, exist_ok=True)

local_filename = os.path.abspath(os.path.join(LOCAL_JSON_FOLDER, os.path.basename(remote_filename)))

print("Local filename is: " + local_filename )
print(remote_filename)

# Wait briefly to ensure file is written
print("Waiting for file to be written on server")
time.sleep(5)


# Pull the file using scp
print("Fetching file using scp")
scp_command = [
    "scp",
    "-i", PEM_FILE_PATH,
    f"{USERNAME}@{HOST}:{remote_filename}",
    local_filename
]

try:
    result = subprocess.run(scp_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print("scp output:", result.stdout)
except subprocess.CalledProcessError as e:
    print(f"scp error:{e.stderr}")
    raise

# # Pull the file via SFTP
# print("Fetching file via SFTP")
# sftp = my_ssh.getSftpConnection()
# try:
#     sftp.get(remote_filename, local_filename)
# except Exception as e:
#     print(f"SFTP error: {e}")
#     raise
# finally:
#     sftp.close()


# Process the local file
print("Extracting data from JSON")
with open(local_filename, 'r') as f:
    data = json.load(f)
append_to_csv(LOCAL_CSV_FILE, data)

# sftp = my_ssh.getSftpConnection()  # This will now work
# sftp.get(remote_filename, local_filename)
# sftp.close()  # Close the SFTP connection when done
# my_ssh.close()  # Close the SSH connection


# Close SSH connection
my_ssh.close()
print("Processing complete")
