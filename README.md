# EC2 Syslog Inspector

This project connects from your local machine (Mac) to an EC2 Ubuntu server, runs a Python script remotely that inspects the server's syslog, counts:

- Number of INFO
- Number of WARN
- Number of ERROR

## How the Script Works

The script uses a two-step approach to catch different types of log entries:

### First step : Precise branch

Fires only on lines that contain both "]: " and " - ".

Splits once at " - " → grabs the token right after the first dash (info, warn, error).

Uses severity_map to pick the right counter and bumps it.

continue prevents double-counting—once a line matches here, we skip the generic scan.

### Second step: Fallback branch

Runs for every other line.

Loops through the known severity words; if the word appears with spaces around it, we count it and break.

Together, this combo nails structured Python logs and plain system logs in one pass.

### The Word Map
At the top of the script, there's a simple dictionary that says "if you find this word, add to this counter":
```python
severity_map = {
    "warn": "warn_count",
    "error": "error_count", 
    "info": "info_count",
}
```

This makes it easy to add new severity levels later if needed.

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

## Setting Up and Running the Project

### 1. Create a Virtual Environment
If you do not have a virtual environment, create one using:

    python3 -m venv venv

Activate the virtual environment:

    source venv/bin/activate

### 2. Install Dependencies

A `requirements.txt` file is provided and maintained by the developer.
To ensure the project runs properly, install all dependencies with:

    pip install -r requirements.txt

### 3. Run the Program
To run the main client script:

    python client_side.py
