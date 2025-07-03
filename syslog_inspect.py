import json
import subprocess
import re
from typing import Dict, Any

def getSyslogSummary() -> Dict[str, Any]:
    data: Dict[str, Any] = {
        "server_timestamp": subprocess.check_output(["date", "+%s"]).decode().strip(),
        "info_count": 0,
        "warn_count": 0,
        "error_count": 0
    }

    with open("/var/log/syslog", "r") as file:
        for line in file:
            line_lower: str = line.lower()
            severity_match = re.search(r":\s*([a-z]+)", line_lower)
            if severity_match:
                severity: str = severity_match.group(1)
                if severity == "info":
                    data["info_count"] += 1
                elif severity.startswith("warn"):
                    data["warn_count"] += 1
                elif severity == "error":
                    data["error_count"] += 1

    return data

if __name__ == "__main__":
    print(json.dumps(getSyslogSummary()))