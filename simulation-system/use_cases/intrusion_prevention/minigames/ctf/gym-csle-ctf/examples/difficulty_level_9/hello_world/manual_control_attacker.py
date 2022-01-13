from csle_common.dao.network.emulation_config import EmulationConfig
from gym_csle_ctf.agents.manual.manual_attacker_agent import ManualAttackerAgent
import gym


def manual_control():
    # emulation_config = emulationConfig(server_ip="172.31.212.92", agent_ip="172.18.9.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/csle_id_rsa",
    #                                server_username="kim")
    # emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip="172.18.9.191",
    #                                  agent_username="agent", agent_pw="agent", server_connection=True,
    #                                  server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                  server_username="kim", port_forward_next_port=8120)
    # emulation_config = EmulationConfig(agent_ip="172.18.9.192", agent_username="agent", agent_pw="agent",
    #                                port_forward_next_port=4600,
    #                                server_connection=True, warmup=False, warmup_iterations=500,
    #                                server_private_key_file="/Users/kimham/.ssh/csle_id_rsa",
    #                                server_username="kim", server_ip="172.31.212.92"
    #                                )
    # emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip="172.18.9.191",
    #                                  agent_username="agent", agent_pw="agent", server_connection=True,
    #                                  server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                  server_username="kim", port_forward_next_port=3600)
    emulation_config = EmulationConfig(agent_ip="172.18.9.191", agent_username="agent", agent_pw="agent",
                                   server_connection=False, port_forward_next_port=3600)

    # emulation_config.save_dynamics_model_dir = "/home/kim/csle/simulation-system/use_cases/intrusion_prevention/minigames/ctf/" \
    #                                            "gym-csle-ctf/examples/difficulty_level_9/hello_world/"
    # emulation_config.save_dynamics_model_dir = "/home/kim/storage/workspace/csle/simulation-system/minigames/network_intrusion" \
    #                                                 "/ctf/gym-csle-ctf/examples/difficulty_level_9/hello_world/"

    emulation_config.save_dynamics_model_dir = "/simulation-system/use_cases/intrusion_prevention/minigames/" \
                                               "ctf/gym-csle-ctf/examples/difficulty_level_9/hello_world/"
    emulation_config.skip_exploration = True
    #env = gym.make("csle-ctf-level-9-emulation-v5", env_config=None, emulation_config=emulation_config)
    #env = gym.make("csle-ctf-level-9-generated-sim-v5", env_config=None, emulation_config=emulation_config)
    env = gym.make("csle-ctf-level-9-generated-sim-v6", env_config=None, emulation_config=emulation_config)
    #env = gym.make("csle-ctf-level-9-emulation-v6", env_config=None, emulation_config=emulation_config)

    env.env_config.attacker_use_nmap_cache = False
    env.env_config.attacker_nmap_scan_cache = False
    env.env_config.attacker_use_nikto_cache = False
    env.env_config.attacker_use_file_system_cache = False
    env.env_config.attacker_use_user_command_cache = False
    env.env_config.randomize_attacker_starting_state = False
    env.env_config.attacker_max_exploration_steps = 5000
    env.env_config.attacker_max_exploration_trajectories = 1000
    env.env_config.domain_randomization = False
    env.env_config.emulate_detection = False
    env.env_config.explore_defense_states = True
    env.env_config.use_attacker_action_stats_to_update_defender_state = False
    env.env_config.defender_sleep_before_state_update = 15
    env.env_config.randomize_attacker_starting_state = False

    ManualAttackerAgent(env=env, env_config=env.env_config, render=False)


if __name__ == '__main__':
    manual_control()

# Novice: 99, 33, 1, 70, 104, 106, 107, 99, 165, 104, 106, 58, 104, 331, 99
# Experienced: 100, 109, 33, 104, 106, 107, 100, 165, 104, 58, 104, 331, 106, 100, 200, 104, 106, 100,266, 104, 106
# Expert: 100, 109, 104, 106, 100, 199, 104, 106,100, 265, 104, 106, 100, 113, 104

# Test case: 99,33,1,70,104,105,106,107,99,165,200,58,104,105,106,331,99,266,104,105,106,99,113,104,105
# Test case: 100,33,1,70,104,105,106,107,100,165,200,58,104,105,106,331,100,266,104,105,106,100,113,104,105

# Test case: 100,33,104,105,106,1,104,105,106,70,104,105,107,100,165,104,105,106,200,104,105,106,58,104,105,331,105,100,266,104,105,106,100,113,104,105
# Test case: 100, 33, 104, 105, 106, 1, 104, 105, 106, 70, 104, 105, 107, 100, 165, 104, 105, 106, 200, 104, 105, 106, 58, 104, 105, 331, 105, 100, 266, 104, 105, 106, 100, 113, 104, 105

# Test case: 372, 100, 372, 33, 372, 104, 372, 105, 372, 106, 372, 1, 372, 104, 372, 372, 372, 105, 372, 106, 372, 70, 372, 104, 105, 107, 372, 100, 372, 165, 372, 104, 372, 105, 372, 106, 372, 200, 372, 372, 104, 372, 105, 372, 106, 372, 372, 58, 372, 104, 372, 105, 372, 331, 372, 105, 100, 266, 372, 104, 105, 106, 100, 372, 113, 104, 372, 105

#372, 99, 372, 33, 372, 104, 372, 105, 372, 106, 372, 1, 372, 104, 372, 372, 372, 105, 372, 106, 372, 70, 372, 104, 105, 107, 372, 99, 372, 165, 372, 104, 372, 105, 372, 106, 372, 200, 372, 372, 104, 372, 105, 372, 106, 372, 372, 58, 372, 104, 372, 105, 372, 331, 372, 105, 99, 266, 372, 104, 105, 106, 99, 372, 113, 104, 372, 105

#99,33,104,105,106,1,104,105,106,70,104,105,107,99,165,104,105,106,200,104,105,106,58,104,105,331,105,99,266,104,105,106,99,113,104,105