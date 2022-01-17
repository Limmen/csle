from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.logic.exploration.custom_exploration_policy import CustomExplorationPolicy
from gym_csle_ctf.envs.csle_ctf_env import CSLECTFEnv # register envs
import gym


def system_id():
    emulation_config = EmulationConfig(agent_ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}1.191", agent_username="agent", agent_pw="agent",
                                     server_connection=False, port_forward_next_port=9600)
    # emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}1.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim", port_forward_next_port=9600)
    emulation_config.skip_exploration = False
    model_path_dir = "/simulation-system/use_cases/intrusion_prevention/" \
                     "minigames/ctf/gym-csle-ctf/examples/difficulty_level_1/system_id"
    emulation_config.save_dynamics_model_dir = model_path_dir

    # Create Env
    env = gym.make("csle-ctf-level-1-generated-sim-v1", env_config=None, emulation_config=emulation_config)

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

    # Expert Attacker
    env.env_config.attacker_exploration_policy = CustomExplorationPolicy(
        num_actions=env.env_config.attacker_action_conf.num_actions,

        # Ping scan, SSH brute force on .2, login, find flag, Telnet brute force on .3, Login, find flag,
        # FTP brute force on .79, Login, find flag
        strategy=[16, 5, 20, 21, 1, 20, 21, 14, 20, 21]
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