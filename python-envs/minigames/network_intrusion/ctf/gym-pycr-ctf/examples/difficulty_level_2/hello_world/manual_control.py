from pycr_common.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.agents.manual.manual_attacker_agent import ManualAttackerAgent
import gym

def manual_control():
    # emulation_config = emulationConfig(server_ip="172.31.212.91", agent_ip="172.18.1.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
    #                                server_username="kim")
    # emulation_config = emulationConfig(server_ip="172.31.212.91", agent_ip="172.18.1.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")
    emulation_config = EmulationConfig(agent_ip="172.18.2.191", agent_username="agent", agent_pw="agent",
                                     server_connection=False, port_forward_next_port=8200)
    # emulation_config = emulationConfig(server_ip="172.31.212.92", agent_ip="172.18.2.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")

    #env = gym.make("pycr-ctf-level-2-emulation-base-v1", env_config=None, emulation_config=emulation_config)
    #env = gym.make("pycr-ctf-level-2-emulation-v1", env_config=None, emulation_config=emulation_config)
    env = gym.make("pycr-ctf-level-2-emulation-v1", env_config=None, emulation_config=emulation_config)
    #env = gym.make("pycr-ctf-level-2-sim-v1", env_config=None, emulation_config=emulation_config)

    #env = gym.make("pycr-ctf-level-2-sim-base-v1", env_config=None)
    ManualAttackerAgent(env=env, env_config=env.env_config)




if __name__ == '__main__':
    manual_control()