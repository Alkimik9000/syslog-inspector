import paramiko
import time


class SshToServer:
    def __init__(self, pem_file_path, host, username):
        self.pem_file_path = pem_file_path
        self.host = host
        self.username = username
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

    def close(self):
        self.shell.close()
        self.sshClient.close()
