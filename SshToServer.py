import paramiko
from config import PEM_FILE_PATH, HOST, USERNAME

class SshToServer:
    def __init__(self):
        self.pem_file_path: str = PEM_FILE_PATH
        self.host = HOST
        self.username = USERNAME
        self.sshClient = paramiko.SSHClient()
        self.connect()

    def connect(self):
        self.sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        private_key = paramiko.RSAKey.from_private_key_file(self.pem_file_path)
        self.sshClient.connect(hostname=self.host, username=self.username, pkey=private_key)

    def execCommand(self, command):
        _, stdout, stderr = self.sshClient.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        if error:
            print("Error from server:", error)
        return output

    def close(self):
        self.sshClient.close()