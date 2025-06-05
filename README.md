# EC2 Syslog Inspector

This project connects from your local machine (Mac) to an EC2 Ubuntu server, runs a Python script remotely that inspects the server’s syslog, counts:
- number of INFO
- number of WARN
- number of ERROR
and prints the result as a JSON object.

The local script captures this JSON output over SSH and appends it directly to a local CSV (`results.csv`) to track these logs over time.

**IMPORTANT:**
- There’s a `secrets.json` file in the repo (dummy version).
  You **must fill it** with your real values:

- The files `syslog_inspect.py`, `config.py` and `secrets.json` must all reside in the server's home directory.