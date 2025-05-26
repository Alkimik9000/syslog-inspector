import paramiko
import time
from config import PEM_FILE_PATH, HOST, USERNAME

class SshToServer:
    def __init__(self):
        self.pem_file_path = PEM_FILE_PATH
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
        time.sleep(1)  # wait for command to execute
        output = ""
        while self.shell.recv_ready():
            output += self.shell.recv(4096).decode()
        return output
    
    def getSftpConnection(self):
        """Return an SFTP client connection using the existing SSH client."""
        return self.sshClient.open_sftp()

    def close(self):
        self.shell.close()
        self.sshClient.close()
