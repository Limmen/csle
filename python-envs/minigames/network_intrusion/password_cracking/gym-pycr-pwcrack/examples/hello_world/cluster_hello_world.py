from gym_pycr_pwcrack.envs.pycr_pwcrack_env import PyCRPwCrackSimpleSim1Env
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
import gym
import time
import numpy as np
import paramiko

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
    #actions = np.array([70, 127, 132])
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
    agent_channel = server_transport.open_channel("direct-tcpip", dest_addr, local_addr)
    print("channel created")

    agent_conn = paramiko.SSHClient()
    agent_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    agent_conn.connect('172.18.1.191', username='agent', password='agent', sock=agent_channel)
    print("agent connected")

    stdin, stdout, stderr = agent_conn.exec_command('ls /')
    for line in stdout:
        print(line.strip('\n'))

def test_all():
    test_env("pycr-pwcrack-simple-sim-v1", num_steps=1000000000)

if __name__ == '__main__':
    test_all()