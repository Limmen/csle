from csle_common.dao.network.emulation_config import EmulationConfig
from gym_csle_ctf.agents.manual.manual_attacker_agent import ManualAttackerAgent
import gym

def manual_control():
    # emulation_config = emulationConfig(server_ip="172.31.212.92", agent_ip="172.18.8.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/csle_id_rsa",
    #                                server_username="kim")
    emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip="172.18.8.191",
                                     agent_username="agent", agent_pw="agent", server_connection=True,
                                     server_private_key_file="/home/kim/.ssh/id_rsa",
                                     server_username="kim")
    # emulation_config = emulationConfig(agent_ip="172.18.8.191", agent_username="agent", agent_pw="agent",
    #                                port_forward_next_port=4600,
    #                                server_connection=True, warmup=False, warmup_iterations=500,
    #                                server_private_key_file="/Users/kimham/.ssh/csle_id_rsa",
    #                                server_username="kim", server_ip="172.31.212.92"
    #                                )
    # emulation_config = emulationConfig(agent_ip="172.18.8.191", agent_username="agent", agent_pw="agent",
    #                                server_connection=False, port_forward_next_port=9600)
    env = gym.make("csle-ctf-level-8-emulation-v1", env_config=None, emulation_config=emulation_config)
    ManualAttackerAgent(env=env, env_config=env.env_config, render=False)


if __name__ == '__main__':
    manual_control()

# Test case: 75,25,80,81,82,83,75,34,80,81,82,83,75,94,80,81,82,75,120,80,81,82,75,146,80,81,82,75,172,80,81,82,75,198,80,81,82,75,224,80,81,82,75,41,80,81,250,82,75,42,80,81,276,82,75,43,80,81,1,80,81,82,88,80,81,82,115,80,81,82,142,80,81,82,166,80,81,82,206,80,81,82,229,80,81,82,44,80,81,253,81,82,28,80,81,262,82,81,71,80,81,75,34,80,81