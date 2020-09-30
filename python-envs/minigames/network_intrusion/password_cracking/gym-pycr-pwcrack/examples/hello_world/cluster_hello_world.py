from gym_pycr_pwcrack.envs.pycr_pwcrack_env import PyCRPwCrackSimpleSim1Env, PyCRPwCrackSimpleCluster1Env
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
import gym
import time
import numpy as np
import paramiko
import re
from xml.etree.ElementTree import XML, fromstring
from gym_pycr_pwcrack.dao.action_results.nmap_scan_result import NmapScanResult
from gym_pycr_pwcrack.dao.action_results.nmap_host import NmapHostResult
from gym_pycr_pwcrack.dao.action_results.nmap_host_status import NmapHostStatus
from gym_pycr_pwcrack.dao.action_results.nmap_port_status import NmapPortStatus
from gym_pycr_pwcrack.dao.action_results.nmap_port import NmapPort

def test_env(env_name : str, num_steps : int):
    cluster_config = ClusterConfig(server_ip="172.31.212.91", agent_ip="172.18.1.191",
                                   agent_username="agent", agent_pw="agent", server_connection=True,
                                   server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
                                   server_username="kim")
    env = gym.make(env_name, env_config=None, cluster_config=cluster_config)
    env.reset()

    num_actions = env.env_config.action_conf.num_actions
    actions = np.array(list(range(num_actions)))
    print("num actions:{}".format(num_actions))
    actions = np.array([0,1,2,3,4,5,6])
    for i in range(num_steps):
        action = np.random.choice(actions)
        obs, reward, done, info = env.step(action)
        env.render()
        if done:
            env.reset()
        time.sleep(0.001)
    env.reset()
    env.close()

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
                            port = NmapPort(port_id=port_id, protocol=protocol, status=status, service_name=service_name)
                            ports.append(port)
                # nmap_host_result = NmapHostResult(status=status, ip_addr=ip_addr, mac_addr=mac_addr,
                #                                   hostnames=hostnames, ports=ports)
                t_1 = c_1.tag
                print(t_1)

                #nmap_host_result = NmapHostResult()
        #print(child.tag)
        #print(child.text)
        #print(child.tail)
        #print(child.items())
        #print(child.getchildren())


def test_all():
    #test_env("pycr-pwcrack-simple-sim-v1", num_steps=1000000000)
    #test_ssh()
    test_env("pycr-pwcrack-simple-cluster-v1", num_steps=1000000000)

if __name__ == '__main__':
    test_all()