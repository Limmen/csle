import paramiko

def nmap_services():
    key = paramiko.RSAKey.from_private_key_file("/Users/kimham/.ssh/pycr_id_rsa")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('172.31.212.91', username='kim', pkey=key)
    print("connected")

    server_transport = client.get_transport()
    dest_addr = ('172.18.1.191', 22)  # edited#
    local_addr = ('172.31.212.91', 22)  # edited#
    relay_channel = server_transport.open_channel("direct-tcpip", dest_addr, local_addr)
    print("channel created")

    agent_conn = paramiko.SSHClient()
    agent_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    agent_conn.connect('172.18.1.191', username='agent', password='agent', sock=relay_channel)
    print("agent connected")

    sftp_client = agent_conn.open_sftp()
    remote_file = sftp_client.open('/nmap-services')
    try:
        for line in remote_file:
            if not line.startswith("#"):
                service = line.split(" ", 1)[0]
                service = service.split("\t", 1)[0]
                print(service)
        # for line in remote_file:
        #     print(line)
    finally:
        remote_file.close()


if __name__ == '__main__':
    nmap_services()