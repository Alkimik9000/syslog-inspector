import json
import subprocess
import re 

data = {
    "server_timestamp": subprocess.check_output(["date", "+%s"]).decode().strip(),    
    "info_count": 0,
    "warn_count": 0,
    "error_count": 0
}

with open("/var/log/syslog", "r") as file:
    line = file.readline()
    while line:
        lower_cased_line = line.lower()
        if re.search(r'\binfo\b', lower_cased_line):
            data["info_count"] += 1
        if re.search(r'\bwarn\b|\bwarning\b', lower_cased_line):  # Matches "warn" or "warning"
            data["warn_count"] += 1
        if re.search(r'\berror\b', lower_cased_line):
            data["error_count"] += 1
        line = file.readline()

print(json.dumps(data))