import json
import os

import pandas as pd

from config import REMOTE_PYTHON_SCRIPT, LOCAL_CSV_FILE
from ssh_to_server import SshToServer


def appendToCsv(file_path: str, row_data: dict) -> None:
    """
    Appends a row of data to a CSV file. If the file does not exist, it creates a new one.
    Args:
        file_path (str): Path to the CSV file.
        row_data (dict): Data to append as a new row.
    """
    df_new: pd.DataFrame = pd.DataFrame([row_data])
    if os.path.isfile(file_path):
        # Read existing data if file exists
        df_existing: pd.DataFrame = pd.read_csv(file_path)
        # Concatenate the new row with existing data
        df_combined: pd.DataFrame = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        # If file does not exist, use only the new row
        df_combined = df_new
    # Write the combined data back to the CSV file
    df_combined.to_csv(file_path, index=False)

# Start SSH connection to remote server
print("Connecting to remote server...")
my_ssh: SshToServer = SshToServer()
print("Connected to remote server")

# Build the command to run the remote Python script
command: str = "python3 " + REMOTE_PYTHON_SCRIPT
print("Running remote command: " + command)
output: str = my_ssh.execCommand(command)

print("Raw output: " + output)

try:
    # Parse the output from the remote script as JSON
    data: dict = json.loads(output)
except json.JSONDecodeError as e:
    # Handle JSON parsing errors
    print("Failed to decode JSON: " + str(e))
    my_ssh.close()
    raise

# Append the parsed data to the local CSV file
print("Appending remote syslog summary to " + LOCAL_CSV_FILE)
appendToCsv(LOCAL_CSV_FILE, data)
print("Data appended")

# Close the SSH connection
my_ssh.close()
print("SSH connection closed")
print("Process completed")