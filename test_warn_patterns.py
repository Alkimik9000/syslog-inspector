#!/usr/bin/env python3
"""
Test to see if we need to catch both 'warn' and 'warning' in our real syslog
"""
from ssh_to_server import SshToServer

def testWarnPatterns():
    print("=== TESTING WARN vs WARNING PATTERNS ===")
    print("Connecting to remote server...")
    
    try:
        my_ssh = SshToServer()
        print("Connected to remote server")
        
        # Count exact matches for 'warn' (not 'warning')
        print("\n1. Counting ' warn ' (not warning)...")
        warn_count = my_ssh.execCommand("grep -i ' warn ' /var/log/syslog | grep -v -i 'warning' | wc -l")
        print("Lines with ' warn ' (not warning): " + warn_count.strip())
        
        # Show samples of ' warn '
        print("\n2. Sample ' warn ' entries:")
        warn_samples = my_ssh.execCommand("grep -i ' warn ' /var/log/syslog | grep -v -i 'warning' | head -3")
        print(warn_samples)
        
        # Count exact matches for 'warning'
        print("\n3. Counting ' warning ' patterns...")
        warning_count = my_ssh.execCommand("grep -i ' warning ' /var/log/syslog | wc -l")
        print("Lines with ' warning ': " + warning_count.strip())
        
        # Show samples of ' warning '
        print("\n4. Sample ' warning ' entries:")
        warning_samples = my_ssh.execCommand("grep -i ' warning ' /var/log/syslog | head -3")
        print(warning_samples if warning_samples else "No ' warning ' entries found")
        
        # Check for - WARN - vs - WARNING - in structured logs
        print("\n5. Checking structured log patterns...")
        dash_warn = my_ssh.execCommand("grep -i ' - warn - ' /var/log/syslog | head -2")
        print("Lines with ' - warn - ':")
        print(dash_warn if dash_warn else "No ' - warn - ' entries found")
        
        dash_warning = my_ssh.execCommand("grep -i ' - warning - ' /var/log/syslog | head -2")
        print("\nLines with ' - warning - ':")
        print(dash_warning if dash_warning else "No ' - warning - ' entries found")
        
        my_ssh.close()
        print("\nSSH connection closed")
        
    except Exception as e:
        print("Error during test: " + str(e))
        return False
    
    return True

if __name__ == "__main__":
    success = testWarnPatterns()
    if success:
        print("\n=== WARN PATTERN TEST COMPLETED ===")
    else:
        print("\n=== TEST FAILED ===") 