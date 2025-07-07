#!/usr/bin/env python3
"""
Script to compare the split approach with the original approach
"""
from ssh_to_server import SshToServer

def compareApproaches():
    print("=== COMPARING SYSLOG APPROACHES ===")
    print("Connecting to remote server...")
    
    try:
        my_ssh = SshToServer()
        print("Connected to remote server")
        
        # Test the split approach
        print("\n1. Testing SPLIT APPROACH...")
        split_output = my_ssh.execCommand("python3 syslog_inspect.py")
        print("=== SPLIT APPROACH OUTPUT ===")
        print(split_output)
        
        # Get some sample lines to analyze
        print("\n2. Getting sample syslog lines for analysis...")
        sample_output = my_ssh.execCommand("tail -n 10 /var/log/syslog")
        print("=== SAMPLE SYSLOG LINES ===")
        print(sample_output)
        
        # Test manual parsing of a few lines
        print("\n3. Manual parsing test...")
        lines = sample_output.strip().split('\n')
        for i, line in enumerate(lines[-3:], 1):  # Test last 3 lines
            print("Line " + str(i) + ": " + line)
            
            # Test split approach manually
            line_lower = line.lower()
            if ":" in line_lower:
                msg_after_colon = line_lower.split(":", 1)[1].lstrip()
                if msg_after_colon.strip():
                    sev_token = msg_after_colon.split(None, 1)[0]
                    print("  Split approach - First token after colon: '" + sev_token + "'")
                    
                    if sev_token in ("warn", "warning", "error", "info"):
                        print("  ✅ Would be counted as: " + sev_token)
                    else:
                        print("  ❌ Would NOT be counted (not a severity token)")
                else:
                    print("  ❌ No content after colon")
            else:
                print("  ❌ No colon found")
            
            # Test original approach for comparison
            if "." in line_lower and ":" in line_lower:
                if " warn " in line_lower:
                    print("  Original approach: ✅ Would count as WARN")
                elif " error " in line_lower:
                    print("  Original approach: ✅ Would count as ERROR")
                elif " info " in line_lower:
                    print("  Original approach: ✅ Would count as INFO")
                else:
                    print("  Original approach: ❌ Would NOT count")
            else:
                print("  Original approach: ❌ No timestamp pattern")
            
            print()
        
        my_ssh.close()
        print("SSH connection closed")
        
    except Exception as e:
        print("Error during comparison: " + str(e))
        return False
    
    return True

if __name__ == "__main__":
    success = compareApproaches()
    if success:
        print("\n=== COMPARISON COMPLETED ===")
    else:
        print("\n=== COMPARISON FAILED ===") 