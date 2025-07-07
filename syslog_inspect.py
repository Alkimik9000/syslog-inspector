import json
import subprocess
from typing import Dict, Any
import sys

def getSyslogSummary() -> Dict[str, Any]:
    data: Dict[str, Any] = {
        "server_timestamp": subprocess.check_output(["date", "+%s"]).decode().strip(),
        "info_count": 0,
        "warn_count": 0,
        "error_count": 0
    }

    # Debug: Check if syslog file exists and is readable
    try:
        with open("/var/log/syslog", "r") as file:
            line_count = 0
            for line in file:
                line_count += 1
                line_lower = line.lower()
                
                # Improved split approach: Use the colon that follows the closing bracket ]:
                if "]: " in line_lower:
                    msg_after_colon = line_lower.split("]:", 1)[1].lstrip()
                else:
                    continue  # can't locate header delimiter, skip

                if msg_after_colon:
                    # Look for pattern "- SEVERITY -" in the message
                    if " - " in msg_after_colon:
                        parts = msg_after_colon.split(" - ")
                        if len(parts) >= 2:
                            # The severity should be the second part (between first and second -)
                            sev_token = parts[1].strip()
                            if sev_token in ("warn", "warning"):
                                data["warn_count"] += 1
                            elif sev_token == "error":
                                data["error_count"] += 1
                            elif sev_token == "info":
                                data["info_count"] += 1
            
            # Debug output to stderr
            print("DEBUG: Processed " + str(line_count) + " lines from syslog", file=sys.stderr)
            print("DEBUG: Found " + str(data['info_count']) + " info, " + str(data['warn_count']) + " warn, " + str(data['error_count']) + " error", file=sys.stderr)
            
    except Exception as e:
        print("DEBUG: Error reading syslog: " + str(e), file=sys.stderr)

    return data

if __name__ == "__main__":
    print(json.dumps(getSyslogSummary())) 