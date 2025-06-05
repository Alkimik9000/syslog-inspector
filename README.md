EC2 Syslog Inspector

This project connects from your local machine (Mac) to an EC2 Ubuntu server, runs a Python script remotely that inspects the server’s syslog, counts:

number of INFO
number of WARN
number of ERROR and prints the result as a JSON object.

The local script captures this JSON output over SSH and appends it directly to a local CSV (results.csv) to track these logs over time.

Setup Instructions:

On the server:

Place syslog_inspect.py in the home directory (e.g., /home/ubuntu/).

On the local machine:

Ensure client_side.py, ssh_to_server.py, config.py, and secrets.json are in the project directory.

Fill secrets.json with your real values for PEM_FILE_PATH, HOST, and USERNAME.

IMPORTANT:

There’s a secrets.json file in the repo (dummy version). You must fill it with your real values.