from csle_common.dao.network.emulation_config import EmulationConfig
from gym_csle_ctf.agents.manual.manual_attacker_agent import ManualAttackerAgent
import gym


def manual_control():
    # emulation_config = emulationConfig(server_ip="172.31.212.91", agent_ip="172.18.7.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/csle_id_rsa",
    #                                server_username="kim")
    # emulation_config = emulationConfig(server_ip="172.31.212.91", agent_ip="172.18.7.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")
    # emulation_config = emulationConfig(agent_ip="172.18.7.191", agent_username="agent", agent_pw="agent",
    #                                port_forward_next_port=4600,
    #                                server_connection=True, warmup=False, warmup_iterations=500,
    #                                server_private_key_file="/Users/kimham/.ssh/csle_id_rsa",
    #                                server_username="kim", server_ip="172.31.212.92"
    #                                )
    emulation_config = EmulationConfig(agent_ip="172.18.7.191", agent_username="agent", agent_pw="agent",
                                     server_connection=False, port_forward_next_port=9600)

    env = gym.make("csle-ctf-level-7-emulation-v1", env_config=None, emulation_config=emulation_config)

    ManualAttackerAgent(env=env, env_config=env.env_config, render=True)




if __name__ == '__main__':
    manual_control()

# Test case: 39, 13, 1, 37, 44, 45, 50, 44, 45, 65, 44, 45, 80, 44, 45, 92, 44, 45, 110, 44, 45, 121, 44, 45, 22, 44, 133, 45, 16, 44, 140, 45