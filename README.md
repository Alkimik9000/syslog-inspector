# EC2 Syslog Inspector

This project connects from your local machine (Mac) to an EC2 Ubuntu server, runs a Python script remotely that inspects the server's syslog, counts:

- Number of INFO
- Number of WARN
- Number of ERROR

and prints the result as a JSON object.

The local script captures this JSON output over SSH and appends it directly to a local CSV file (`results.csv`) to track these logs over time.

## Setup Instructions

### On the server:
- Place `syslog_inspect.py` in the home directory (e.g., `/home/ubuntu/`)

### On the local machine:
- Make sure the following files are in your project directory:
  - `client_side.py`
  - `ssh_to_server.py`
  - `config.py`
  - `secrets.json`

- Fill `secrets.json` with your real values:
  - `PEM_FILE_PATH`
  - `HOST`
  - `USERNAME`

> **IMPORTANT**: There’s a `secrets.json` file in the repo (dummy version). You must fill it with your real values.
