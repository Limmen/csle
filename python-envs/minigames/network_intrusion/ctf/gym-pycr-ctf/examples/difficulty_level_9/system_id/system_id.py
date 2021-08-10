from gym_pycr_ctf.envs.derived_envs.level1.simulation.pycr_ctf_level1_sim_env import PyCRCTFLevel1Sim1Env
from gym_pycr_ctf.envs.derived_envs.level1.emulation.pycr_ctf_level1_emulation_env import PyCRCTFLevel1Emulation1Env
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.envs_model.logic.exploration.random_exploration_policy import RandomExplorationPolicy
from gym_pycr_ctf.envs_model.logic.exploration.custom_exploration_policy import CustomExplorationPolicy
from gym_pycr_ctf.agents.policy_gradient.ppo_baseline.impl.ppo.ppo import PPO
import gym


def initialize_models(self) -> None:
    """
    Initialize models

    :return: None
    """
    # Initialize models
    model = PPO.load(env=self.env, load_path=self.agent_config.load_path, device=self.device,
                          agent_config=self.agent_config)
    return model

def system_id():
    # emulation_config = EmulationConfig(server_ip="172.31.212.91", agent_ip="172.18.4.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
    #                                server_username="kim")
    # emulation_config = EmulationConfig(server_ip="172.31.212.91", agent_ip="172.18.4.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")
    emulation_config = EmulationConfig(agent_ip="172.18.9.191", agent_username="agent", agent_pw="agent",
                                     server_connection=False, port_forward_next_port=9600)
    # emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip="172.18.9.191",
    #                                         agent_username="agent", agent_pw="agent", server_connection=True,
    #                                         server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                         server_username="kim", port_forward_next_port=3000)
    emulation_config.skip_exploration = False
    model_path_dir = "/home/kim/pycr/python-envs/minigames/network_intrusion/ctf/" \
                     "gym-pycr-ctf/examples/difficulty_level_9/system_id"
    # model_path_dir = "/home/kim/pycr/python-envs/minigames/network_intrusion/ctf/" \
    #                  "gym-pycr-ctf/examples/difficulty_level_9/hello_world/"
    emulation_config.save_dynamics_model_dir = model_path_dir

    # Create Env
    env = gym.make("pycr-ctf-level-9-generated-sim-v5", env_config=None, emulation_config=emulation_config)

    # Configure Env for System ID
    env.env_config.attacker_use_nmap_cache = False
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
    env.env_config.defender_sleep_before_state_update = 10
    env.env_config.attacker_continue_action_sleep = 0.001

    # Novice Attacker
    # env.env_config.attacker_exploration_policy = CustomExplorationPolicy(
    #     num_actions=env.env_config.attacker_action_conf.num_actions,
    #
    #     # Continue, TCP/UDP Scan, SSH Brute (0), Telnet Brute (1), FTP Brute (4), Login, Install Tools, Backdoor, Continue,
    #     # TCP/UDP Scan, Shellshock (CVE-2014-6271) (24) with backdoor, Login, Install Tools,
    #     # Continue, SSH brute (25), Login,
    #     # CVE-2010-0426 (25), Continue, TCP/UDP Scan
    #     strategy=[372, 99, 33, 1, 70, 104, 106, 107, 99, 165, 104, 106, 58, 104, 331, 99]
    # )

    # Experienced Attacker
    env.env_config.attacker_exploration_policy = CustomExplorationPolicy(
        num_actions=env.env_config.attacker_action_conf.num_actions,

        # Continue, Ping Scan, SambaCry Exploit(1), Login, Install tools, Backdoor, Ping Scan
        # Shellshock (CVE-2014-6271) (24) with backdoor, login, SSH brute (25), Login, CVE-2010-0426 (25),
        # Ping scan, SQL injection (26), Login, Install tools,
        # Ping scan, CVE-2015-1427 (26), Login, Install Tools,
        strategy=[372, 100, 109, 33, 104, 106, 107, 100, 165, 104, 58, 104, 331, 106, 100, 200, 104,106,100,
                  266, 104, 106]
    )


    #, 100, 113, 104
    # Ping scan, SambaCry (5), Login

    #
    # env.env_config.randomize_starting_state_policy = CustomExplorationPolicy(
    #     num_actions=env.env_config.attacker_action_conf.num_actions,
    #     strategy=[100, 33, 104, 105, 106, 1, 104, 105, 106, 70, 104, 105, 107, 100, 165, 104, 105, 106, 200, 104, 105,
    #               106, 58, 104,
    #               105, 331, 105, 100, 266, 104, 105, 106, 100, 113, 104, 105])
    #
    # # Expert Attacker
    # env.env_config.randomize_starting_state_policy = CustomExplorationPolicy(
    #     num_actions=env.env_config.attacker_action_conf.num_actions,
    #     strategy=[100, 33, 104, 105, 106, 1, 104, 105, 106, 70, 104, 105, 107, 100, 165, 104, 105, 106, 200, 104, 105,
    #               106, 58, 104,
    #               105, 331, 105, 100, 266, 104, 105, 106, 100, 113, 104, 105])

    env.env_config.attacker_max_exploration_steps = len(env.env_config.attacker_exploration_policy.strategy)

    # System ID
    env.system_identification()


if __name__ == '__main__':
    system_id()