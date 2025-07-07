import json
import subprocess
from typing import Dict, Any

severity_map: Dict[str, str] = {
    "warn": "warn_count",
    "warning": "warn_count",
    "error": "error_count",
    "info": "info_count",
}

def getSyslogSummary() -> Dict[str, Any]:
    data: Dict[str, Any] = {
        "server_timestamp": subprocess.check_output(["date", "+%s"]).decode().strip(),
        "info_count": 0,
        "warn_count": 0,
        "error_count": 0
    }

    with open("/var/log/syslog", "r", errors="replace") as file:
        for line in file:
            line_lower = line.lower()

            if "]: " in line_lower and " - " in line_lower:
                sev_token = line_lower.split(" - ", 2)[1].strip()
                counter_key = severity_map.get(sev_token)
                if counter_key:
                    data[counter_key] += 1
                continue

            for sev_word, counter_key in severity_map.items():
                if (" " + sev_word + " ") in line_lower:
                    data[counter_key] += 1
                    break

    return data

if __name__ == "__main__":
    print(json.dumps(getSyslogSummary())) 