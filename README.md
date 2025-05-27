# EC2 Syslog Inspector

This project connects from your local machine (Mac) to an EC2 Ubuntu server, runs a Python script remotely that inspects the server’s syslog, counts:
- number of INFO
- number of WARN
- number of ERROR  
and saves the result in a JSON file on the server.

The local script then pulls that JSON file back and updates (or creates) a local CSV (`results.csv`) to track these logs over time.

**IMPORTANT:**  
-There’s a `secrets.json` file in the repo (dummy version).  
You **must fill it** with your real values:

-The files 'syslog_inspect.py', 'config.py' & 'sercrets.json' must all reside on the home directory of the server's home directory. 

