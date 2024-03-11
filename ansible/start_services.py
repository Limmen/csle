import paramiko
import time
import sys

if __name__ == '__main__':
    ip = sys.argv[1]
    user = sys.argv[2]
    conda_env = sys.argv[3]
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip, port=22, username=user)
    stdin, stdout, stderr = ssh_client.exec_command(f"bash -ic 'nohup ~/csle/ansible/start.sh {conda_env} &'", get_pty=True)
    time.sleep(120)
