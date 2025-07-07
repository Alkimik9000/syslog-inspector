# EC2 Syslog Inspector

This project connects from your local machine (Mac) to an EC2 Ubuntu server, runs a Python script remotely that inspects the server's syslog, counts:

- Number of INFO
- Number of WARN
- Number of ERROR

## How the Script Works

The script uses a smart two-step approach to catch different types of log entries:

### Step 1: Precise Matching
First, it looks for logs that follow a specific format with dashes, like:
```
2025-07-07 14:22:23,534 - INFO - Starting process...
2025-07-07 14:22:24,123 - ERROR - Connection failed
```

When it finds this pattern (`]: ... - SEVERITY - ...`), it knows exactly where the severity word is - right between the dashes. This is super accurate for Python logging entries.

### Step 2: General Search
If a line doesn't have that dash pattern, the script does a simple word search. It looks for severity words with spaces around them (like ` warn ` or ` error `). This catches other types of logs like:
```
2025-07-03 13:58:43.1204 WARN EC2RoleProvider Failed to connect
```

### Why Two Steps?
We need both because logs come in different formats:
- Python apps use the dash format: `- INFO -`
- System services just put the word directly: `WARN`

By checking both ways, we catch everything without counting the same line twice (that's why we use `continue` after the first match).

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
