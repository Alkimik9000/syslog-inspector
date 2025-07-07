#!/usr/bin/env python3
"""
Test to see if word boundaries matter in our real syslog data
"""
from ssh_to_server import SshToServer

def testWordBoundaries():
    print("=== TESTING WORD BOUNDARIES IN REAL SYSLOG ===")
    print("Connecting to remote server...")
    
    try:
        my_ssh = SshToServer()
        print("Connected to remote server")
        
        # Search for potential false positives
        print("\n1. Checking for 'error' without word boundaries...")
        error_check = my_ssh.execCommand("grep -i 'error' /var/log/syslog | head -5")
        print("Sample 'error' matches:")
        print(error_check)
        
        print("\n2. Checking for potential false positives like 'error_logs', 'errors', etc...")
        false_pos_check = my_ssh.execCommand("grep -iE '(error[a-z_]|[a-z_]error)' /var/log/syslog | head -3")
        print("Potential false positives:")
        print(false_pos_check)
        
        print("\n3. Checking for 'info' patterns...")
        info_check = my_ssh.execCommand("grep -i 'info' /var/log/syslog | head -3")
        print("Sample 'info' matches:")
        print(info_check)
        
        print("\n4. Checking for 'warn' patterns...")
        warn_check = my_ssh.execCommand("grep -i 'warn' /var/log/syslog | head -3")
        print("Sample 'warn' matches:")
        print(warn_check)
        
        my_ssh.close()
        print("\nSSH connection closed")
        
    except Exception as e:
        print("Error during test: " + str(e))
        return False
    
    return True

if __name__ == "__main__":
    success = testWordBoundaries()
    if success:
        print("\n=== WORD BOUNDARY TEST COMPLETED ===")
    else:
        print("\n=== TEST FAILED ===") 