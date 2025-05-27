import paramiko
import time
from config import PEM_FILE_PATH, HOST, USERNAME

class SshToServer:
    def __init__(self):
        self.pem_file_path: str = PEM_FILE_PATH
        self.host = HOST
        self.username = USERNAME
        self.sshClient = paramiko.SSHClient()
        self.connect()
        self.shell = self.sshClient.invoke_shell()

    def connect(self):
        self.sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        private_key = paramiko.RSAKey.from_private_key_file(self.pem_file_path)
        self.sshClient.connect(hostname=self.host, username=self.username, pkey=private_key)

    def runShellCommand(self, command):
        self.shell.send(command + '\n')
        time.sleep(3)  # Initial wait for command to start
        output = ""
        timeout = 10  # Max seconds to wait
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.shell.recv_ready():
                output += self.shell.recv(4096).decode()
            time.sleep(0.1)  # Small delay to avoid busy waiting
        return output
        
    def getSftpConnection(self):
        return self.sshClient.open_sftp()

    def close(self):
        self.shell.close()
        self.sshClient.close()
    
    def execCommand(self, command):
        stdin, stdout, stderr = self.sshClient.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        if error:
            print("Error from server:", error)
        return output
