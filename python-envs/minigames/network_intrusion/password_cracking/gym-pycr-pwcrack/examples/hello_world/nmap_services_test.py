import paramiko
from xml.etree.ElementTree import XML, fromstring
import xml.etree.ElementTree as ET
import time
import pickle

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

def cves():
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
    remote_file = sftp_client.open('/allitems.csv', "rb")
    list2 = []
    try:
        print("reading file")
        start = time.time()
        for line in remote_file:
            list2.append(line.decode("ISO-8859-1").split(",")[0])
        end = time.time()
        print(end - start)
        # for line in remote_file:
        #     print(line)
    finally:
        remote_file.close()
    print("read {} CVEs in {}s, example:{}".format(len(list2), end-start, list2[10]))
    with open('/Users/kimham/Downloads/cves.txt', 'w') as f:
        for item in list2:
            f.write("%s\n" % item)
    print("written to file")
    print("reading file")
    list3 = []
    with open('/Users/kimham/Downloads/cves.txt', 'r') as f:
        start = time.time()
        for line in f:
            list3.append(line)
        end = time.time()
        print("read {} CVEs in {}s, example:{}".format(len(list3), end - start, list3[10]))
    with open('/Users/kimham/Downloads/cves.pickle', 'wb') as f:
        pickle.dump(list3, f)

    print("start reading")
    start = time.time()
    with open('/Users/kimham/Downloads/cves.pickle', 'rb') as f:
        list4 = pickle.load(f)
        end = time.time()
        print("read {} CVEs in {}s, example:{}".format(len(list4), end - start, list4[10]))
    # with open("mylist.csv") as f:
    #     for row in f:
    #         list2.append(row.split()[0])

    # remote_file = sftp_client.open('/allitems-cvrf.xml')
    # try:
    #     print("Parsing CVEs")
    #     xml_data = ET.parse(remote_file)
    #     print("Parsing Done")
    #     root = xml_data.getroot()
    #     print("root:{}".format(root))
    #     # for line in remote_file:
    #     #     print(line)
    # finally:
    #     remote_file.close()


if __name__ == '__main__':
    #nmap_services()
    cves()