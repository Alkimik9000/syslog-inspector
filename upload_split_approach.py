#!/usr/bin/env python3
"""
Script to upload the split approach version to the server
"""
from ssh_to_server import SshToServer

def uploadSplitApproach():
    print("=== UPLOADING SPLIT APPROACH TO SERVER ===")
    print("Connecting to remote server...")
    
    try:
        my_ssh = SshToServer()
        print("Connected to remote server")
        
        # Upload the split approach version
        print("\n1. Uploading split approach syslog_inspect.py...")
        
        # Read local file
        with open("syslog_inspect.py", "r") as f:
            content = f.read()
        
        # Create upload command
        upload_cmd = "cat > syslog_inspect.py << 'EOF'\n" + content + "\nEOF"
        my_ssh.execCommand(upload_cmd)
        print("✅ Split approach syslog_inspect.py uploaded")
        
        # Verify upload
        print("\n2. Verifying upload...")
        verify_output = my_ssh.execCommand("ls -la syslog_inspect.py")
        print("File info: " + verify_output.strip())
        
        # Test the split approach
        print("\n3. Testing split approach...")
        test_output = my_ssh.execCommand("python3 syslog_inspect.py")
        print("=== SPLIT APPROACH TEST OUTPUT ===")
        print(test_output)
        
        my_ssh.close()
        print("\nSSH connection closed")
        
    except Exception as e:
        print("Error during upload: " + str(e))
        return False
    
    return True

if __name__ == "__main__":
    success = uploadSplitApproach()
    if success:
        print("\n=== UPLOAD COMPLETED SUCCESSFULLY ===")
    else:
        print("\n=== UPLOAD FAILED ===") 