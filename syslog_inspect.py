import json
import os
import subprocess

from config import REMOTE_JSON_FOLDER

def runLocalCommand(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print("Command failed: " + command + " (exit code " + str(e.returncode) + ")")

server_timestamp = os.popen("date +%s").read().strip()
if not server_timestamp:
    print("Failed to capture timestamp")
    exit(1)

print(server_timestamp)

info_count = runLocalCommand("less /var/log/syslog | grep -i  'info' | wc -l")
warn_count = runLocalCommand("less /var/log/syslog | grep -i  'warn' | wc -l")
error_count = runLocalCommand("less /var/log/syslog | grep -i  'error' | wc -l")

data = {
    "server_timestamp": server_timestamp,
    "info_count": info_count,
    "warn_count": warn_count,
    "error_count": error_count
}

# Collect system log metrics for analysis

os.makedirs(REMOTE_JSON_FOLDER, exist_ok=True)
json_filename = os.path.join(REMOTE_JSON_FOLDER, "results-" + str(server_timestamp) + ".json")

with open(json_filename, "w") as json_file:
    json.dump(data, json_file, indent=4)

try:
    with open(json_filename, "w") as json_file:
        json.dump(data, json_file, indent=4)
    print("Generated JSON file: " + json_filename) 
except Exception as e:
    print("Failed to write JSON file: " + str(e))
    raise
