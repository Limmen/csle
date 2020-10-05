from gym_pycr_pwcrack.envs.pycr_pwcrack_env import PyCRPwCrackSimpleSim1Env, PyCRPwCrackSimpleCluster1Env
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
import gym
import time
import numpy as np
import paramiko
import re
from xml.etree.ElementTree import XML, fromstring
import xml.etree.ElementTree as ET
from gym_pycr_pwcrack.dao.action_results.nmap_port_status import NmapPortStatus
from gym_pycr_pwcrack.dao.action_results.nmap_port import NmapPort

def test_env(env_name : str, num_steps : int):
    # cluster_config = ClusterConfig(server_ip="172.31.212.91", agent_ip="172.18.1.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
    #                                server_username="kim")
    # cluster_config = ClusterConfig(server_ip="172.31.212.91", agent_ip="172.18.1.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")
    cluster_config = ClusterConfig(agent_ip="172.18.1.191", agent_username="agent", agent_pw="agent",
                                   server_connection=False)
    env = gym.make(env_name, env_config=None, cluster_config=cluster_config)
    env.env_config.max_episode_length = 1000000000
    env.reset()

    num_actions = env.env_config.action_conf.num_actions
    actions = np.array(list(range(num_actions)))
    print("num actions:{}".format(num_actions))
    # actions = np.array([0,1,2,3,4,5,6, 7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,
    #                     34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,
    #                     63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,
    #                     92,93,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,
    #                     116,117,118,119,120,121,122,123,124,125,126,127,134,135,136,137,138,139, 140, 141, 142, 143, 144])
    #actions = np.array([127])
    #actions = np.array([119,120,121,122,123,124,125])
    for i in range(num_steps):
        legal_actions = list(filter(lambda x: env.is_action_legal(x, env.env_config, env.env_state), actions))
        action = np.random.choice(legal_actions)
        obs, reward, done, info = env.step(action)
        env.render()
        if done:
            env.reset()
        time.sleep(0.001)
        #time.sleep(0.5)
    env.reset()
    env.close()

def test_ssh2():
    key = paramiko.RSAKey.from_private_key_file("/Users/kimham/.ssh/pycr_id_rsa")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('172.31.212.91', username='kim', pkey=key)
    print("connected")
    stdin, stdout, stderr = client.exec_command('ll')
    for line in stdout:
        print(line.strip('\n'))
    server_transport = client.get_transport()

    dest_addr = ('172.18.1.191', 22)  # edited#
    local_addr = ('172.31.212.91', 22)  # edited#
    relay_channel = server_transport.open_channel("direct-tcpip", dest_addr, local_addr)
    print("channel created")

    agent_conn = paramiko.SSHClient()
    agent_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    agent_conn.connect('172.18.1.191', username='agent', password='agent', sock=relay_channel)
    print("agent connected")

    # stdin, stdout, stderr = agent_conn.exec_command("ls -al /")
    # for line in stdout:
    #     print(line.strip('\n'))
    #
    # stdin, stdout, stderr = agent_conn.exec_command("sudo nmap -sS --min-rate 100000 --max-retries 1 -T5 -oX 0.xml 172.18.1.10")
    # for line in stdout:
    #     print(line.strip('\n'))

    sftp_client = agent_conn.open_sftp()
    remote_file = sftp_client.open('/home/agent/19.xml')
    try:
        xml_data = ET.parse(remote_file)
        root = xml_data.getroot()
        print("root:{}".format(root))
        # for line in remote_file:
        #     print(line)
    finally:
        remote_file.close()


def test_ssh():
    key = paramiko.RSAKey.from_private_key_file("/Users/kimham/.ssh/pycr_id_rsa")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('172.31.212.91', username='kim', pkey=key)
    print("connected")
    stdin, stdout, stderr = client.exec_command('ll')
    for line in stdout:
        print(line.strip('\n'))
    server_transport = client.get_transport()

    dest_addr = ('172.18.1.191', 22)  # edited#
    local_addr = ('172.31.212.91', 22)  # edited#
    relay_channel = server_transport.open_channel("direct-tcpip", dest_addr, local_addr)
    print("channel created")

    agent_conn = paramiko.SSHClient()
    agent_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    agent_conn.connect('172.18.1.191', username='agent', password='agent', sock=relay_channel)
    print("agent connected")

    agent_channel = agent_conn.invoke_shell()

    # clear output
    time.sleep(0.2)
    if agent_channel.recv_ready():
        output = agent_channel.recv(5000)

    agent_channel.send('ls -al /\n')
    time.sleep(0.2)
    if agent_channel.recv_ready():
        output = agent_channel.recv(5000)

    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    output_str = output.decode("utf-8")
    output_str = ansi_escape.sub("", output_str)
    lines = output_str.split('\r\n')
    print(lines)

    agent_channel.send("su root\n")
    time.sleep(0.2)
    agent_channel.send("root\n")
    time.sleep(0.2)
    if agent_channel.recv_ready():
        output = agent_channel.recv(5000)
        print(output)

    agent_channel.send("whoami\n")
    time.sleep(0.2)
    if agent_channel.recv_ready():
        output = agent_channel.recv(5000)
        print(output)

    # agent_channel.send("nmap -sS --min-rate 100000 --max-retries 1 -T5 -oX 0.xml 172.18.1.10\n")
    # time.sleep(0.2)
    # if agent_channel.recv_ready():
    #     output = agent_channel.recv(5000)
    #     print(output)
    #     output_str = output.decode("utf-8")
    #     output_str = ansi_escape.sub("", output_str)
    #     lines = output_str.split('\r\n')
    #     print(lines)

    agent_channel.send("ls -1 /home/agent/\n")
    time.sleep(0.2)
    if agent_channel.recv_ready():
        output = agent_channel.recv(5000)
        #print(output)
    output_str = output.decode("utf-8")
    output_str = ansi_escape.sub("", output_str)
    lines = output_str.split('\r\n')
    lines = lines[1:-1] # remove command ([0]) and prompt ([-1])
    agent_channel.send("cat /home/agent/0.xml\n")
    time.sleep(0.3)
    if agent_channel.recv_ready():
        output = agent_channel.recv(1000000)
    output_str = output.decode("utf-8")
    output_str = ansi_escape.sub("", output_str)
    lines = output_str.split('\r\n')
    lines = lines[1:-1]  # remove command ([0]) and prompt ([-1])
    xml_str = "\n".join(lines)
    myxml = fromstring(xml_str)

    #root = myxml.getroot()
    #nmap_scan_result = NmapScanResult()
    #nmap_host_result = NmapHostResult()
    for child in myxml:
        print(child)
        tag = child.tag
        attributes = child.items()
        children = list(child.iter())
        if tag == "host":
            status = NmapPortStatus.DOWN
            hostnames = []
            ports = []
            for c_1 in children:
                if c_1.tag == "status":
                    for attr, val in c_1.items():
                        if attr == "state":
                            if val == "up":
                                status = NmapPortStatus.UP
                elif c_1.tag == "address":
                    addr = None
                    ip = True
                    mac = False
                    for attr, val in c_1.items():
                        if attr == "addr":
                            addr = val
                            if attr == "addrtype":
                                if "ip" in val:
                                    ip = True
                                    mac = False
                                elif "mac" in val:
                                    ip = False
                                    mac = True
                    if ip:
                        ip_addr = addr
                    if mac:
                        mac_addr = addr
                elif c_1.tag == "hostnames":
                    for c_2 in list(c_1.iter())[1:]:
                        if c_2.tag == "hostname":
                            hostnames.append(c_2.attrib["name"])
                elif c_1.tag == "ports":
                    for c_2 in list(c_1.iter())[1:]:
                        if c_2.tag == "port":
                            port_status = NmapPortStatus.DOWN
                            print(c_2.items())
                            protocol = c_2.attrib["protocol"]
                            port_id = c_2.attrib["portid"]
                            service_name = None
                            for c_3 in list(c_2.iter()):
                                print(list(c_2.iter()))
                                if c_3.tag == "state":
                                    if c_3.attrib["state"] == "open":
                                        port_status = NmapPortStatus.UP
                                if c_3.tag == "service":
                                    service_name = c_3.attrib["name"]
                            port = NmapPort(port_id=port_id, protocol=protocol, status=port_status, service_name=service_name)
                            ports.append(port)
                t_1 = c_1.tag
                print(t_1)


def test_all():
    #test_env("pycr-pwcrack-simple-sim-v1", num_steps=1000000000)
    #test_ssh()
    test_env("pycr-pwcrack-simple-cluster-v1", num_steps=1000000000)
    #test_ssh2()

if __name__ == '__main__':
    test_all()