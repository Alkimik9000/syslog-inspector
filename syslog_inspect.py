import json
import subprocess

data = {
    "server_timestamp": subprocess.check_output(["date", "+%s"]).decode().strip(),    
    "info_count": 0,
    "warn_count": 0,
    "error_count": 0
}

with open("/var/log/syslog", "r") as file:
    line = file.readline()
    while line:
        line_lower = line.lower()
        if "info" in line_lower:
            data["info_count"] += 1
        if "warn" in line_lower:
            data["warn_count"] += 1
        if "error" in line_lower:
            data["error_count"] += 1
        line = file.readline()

print(json.dumps(data))