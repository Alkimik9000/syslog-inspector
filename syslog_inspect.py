import json
import subprocess
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
            line_lower = line.lower()
            
            if "." in line_lower and ":" in line_lower:
                if " warn " in line_lower:
                    data["warn_count"] += 1
                elif " error " in line_lower:
                    data["error_count"] += 1
                elif " info " in line_lower:
                    data["info_count"] += 1

    return data

if __name__ == "__main__":
    print(json.dumps(getSyslogSummary())) 