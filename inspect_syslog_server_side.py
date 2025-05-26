import subprocess
import json
import os

def run_local_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()

    except subprocess.CalledProcessError as e:
        print("Command '" + command + "' returned non-zero exit status " + str(e.returncode))
        print("Error output: " + e.stderr)

server_timestamp = run_local_command("date +%s")
info_count = run_local_command("less /var/log/syslog | grep -i  'info' | wc -l")
warn_count = run_local_command("less /var/log/syslog | grep -i  'warn' | wc -l")
error_count = run_local_command("less /var/log/syslog | grep -i  'error' | wc -l")



data = {
    "server_timestamp": server_timestamp,
    "info_count": info_count,
    "warn_count": warn_count,
    "error_count": error_count
}

output_folder = "json_results"
os.makedirs(output_folder, exist_ok=True)

json_filename = output_folder + "/results-" + server_timestamp + ".json"


with open(json_filename, "w") as json_file:
    json.dump(data, json_file, indent=4)

print(json_filename)
