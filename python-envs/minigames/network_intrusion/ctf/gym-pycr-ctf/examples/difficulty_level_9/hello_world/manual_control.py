from gym_pycr_ctf.envs.derived_envs.level1.simulation.pycr_ctf_level1_sim_env import PyCRCTFLevel1Sim1Env
from gym_pycr_ctf.envs.derived_envs.level1.emulation.pycr_ctf_level1_emulation_env import PyCRCTFLevel1Emulation1Env
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.agents.manual.manual_attacker_agent import ManualAttackerAgent
import gym

def manual_control():
    # emulation_config = emulationConfig(server_ip="172.31.212.92", agent_ip="172.18.9.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
    #                                server_username="kim")
    # emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip="172.18.9.191",
    #                                  agent_username="agent", agent_pw="agent", server_connection=True,
    #                                  server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                  server_username="kim", port_forward_next_port=8120)
    # emulation_config = EmulationConfig(agent_ip="172.18.9.192", agent_username="agent", agent_pw="agent",
    #                                port_forward_next_port=4600,
    #                                server_connection=True, warmup=False, warmup_iterations=500,
    #                                server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
    #                                server_username="kim", server_ip="172.31.212.92"
    #                                )
    # emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip="172.18.9.191",
    #                                  agent_username="agent", agent_pw="agent", server_connection=True,
    #                                  server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                  server_username="kim", port_forward_next_port=3600)
    emulation_config = EmulationConfig(agent_ip="172.18.9.191", agent_username="agent", agent_pw="agent",
                                   server_connection=False, port_forward_next_port=3600)

    # emulation_config.save_dynamics_model_dir = "/home/kim/pycr/python-envs/minigames/network_intrusion/ctf/" \
    #                                            "gym-pycr-ctf/examples/difficulty_level_9/hello_world/"
    emulation_config.save_dynamics_model_dir = "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion" \
                                                    "/ctf/gym-pycr-ctf/examples/difficulty_level_9/hello_world/"
    emulation_config.skip_exploration = True
    #env = gym.make("pycr-ctf-level-9-emulation-v5", env_config=None, emulation_config=emulation_config)
    #env = gym.make("pycr-ctf-level-9-generated-sim-v5", env_config=None, emulation_config=emulation_config)
    env = gym.make("pycr-ctf-level-9-generated-sim-v5", env_config=None, emulation_config=emulation_config)
    env.env_config.randomize_attacker_starting_state = False
    ManualAttackerAgent(env=env, env_config=env.env_config, render=False)


if __name__ == '__main__':
    manual_control()

# Test case: 99,33,1,70,104,105,106,107,99,165,200,58,104,105,106,331,99,266,104,105,106,99,113,104,105
# Test case: 100,33,1,70,104,105,106,107,100,165,200,58,104,105,106,331,100,266,104,105,106,100,113,104,105

# Test case: 100,33,104,105,106,1,104,105,106,70,104,105,107,100,165,104,105,106,200,104,105,106,58,104,105,331,105,100,266,104,105,106,100,113,104,105
# Test case: 100, 33, 104, 105, 106, 1, 104, 105, 106, 70, 104, 105, 107, 100, 165, 104, 105, 106, 200, 104, 105, 106, 58, 104, 105, 331, 105, 100, 266, 104, 105, 106, 100, 113, 104, 105

# Test case: 372, 100, 372, 33, 372, 104, 372, 105, 372, 106, 372, 1, 372, 104, 372, 372, 372, 105, 372, 106, 372, 70, 372, 104, 105, 107, 372, 100, 372, 165, 372, 104, 372, 105, 372, 106, 372, 200, 372, 372, 104, 372, 105, 372, 106, 372, 372, 58, 372, 104, 372, 105, 372, 331, 372, 105, 100, 266, 372, 104, 105, 106, 100, 372, 113, 104, 372, 105

#372, 99, 372, 33, 372, 104, 372, 105, 372, 106, 372, 1, 372, 104, 372, 372, 372, 105, 372, 106, 372, 70, 372, 104, 105, 107, 372, 99, 372, 165, 372, 104, 372, 105, 372, 106, 372, 200, 372, 372, 104, 372, 105, 372, 106, 372, 372, 58, 372, 104, 372, 105, 372, 331, 372, 105, 99, 266, 372, 104, 105, 106, 99, 372, 113, 104, 372, 105

#99,33,104,105,106,1,104,105,106,70,104,105,107,99,165,104,105,106,200,104,105,106,58,104,105,331,105,99,266,104,105,106,99,113,104,105