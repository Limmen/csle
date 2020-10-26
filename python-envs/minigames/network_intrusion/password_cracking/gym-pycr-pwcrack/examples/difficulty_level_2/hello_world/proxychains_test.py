from gym_pycr_pwcrack.envs.pycr_pwcrack_env import PyCRPwCrackSimpleSim1Env, PyCRPwCrackSimpleCluster1Env
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
import gym
import time
import numpy as np

def proxychains(env_name):
    cluster_config = ClusterConfig(agent_ip="172.18.2.191", agent_username="agent", agent_pw="agent",
                                   server_connection=False)
    env = gym.make(env_name, env_config=None, cluster_config=cluster_config)
    env.env_config.max_episode_length = 1000000000
    env.reset()
    agent_conn = env.env_config.cluster_config.agent_conn

    transport_conn = agent_conn.get_transport()
    session = transport_conn.open_session()
    start = time.time()
    session.exec_command("ls")
    outdata, errdata = b'', b''
    # Wait for completion
    while True:
        # Reading from output streams
        while session.recv_ready():
            outdata += session.recv(1000)
        while session.recv_stderr_ready():
            errdata += session.recv_stderr(1000)

        # Check for completion
        if session.exit_status_ready():
            break
    end = time.time()
    total_time = end - start
    print("outdata:{}".format(outdata))




if __name__ == '__main__':
    proxychains("pycr-pwcrack-medium-cluster-base-v1")