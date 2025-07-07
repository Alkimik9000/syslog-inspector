import json
import subprocess
from typing import Dict, Any

SEV_WORDS = {"warn": "warn_count",
             "warning": "warn_count",
             "error": "error_count",
             "info": "info_count"}

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

            # precise: "program[pid]: … - SEVERITY - …"
            if "]: " in line_lower and " - " in line_lower:
                parts = line_lower.split(" - ")
                if len(parts) >= 2:
                    sev_token = parts[1].strip()
                    key = SEV_WORDS.get(sev_token)
                    if key:
                        data[key] += 1
                continue

            # fallback: quick substring scan (no f-string)
            for word, key in SEV_WORDS.items():
                pattern = " " + word + " "
                if pattern in line_lower:
                    data[key] += 1
                    break

    return data

if __name__ == "__main__":
    print(json.dumps(getSyslogSummary())) 