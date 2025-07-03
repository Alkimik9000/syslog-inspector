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
