import os
from csle_common.agents.config.agent_config import AgentConfig
from csle_common.dao.agent.agent_type import AgentType
from csle_common.dao.agent.train_mode import TrainMode
from csle_common.dao.experiment.client_config import ClientConfig
from csle_common.dao.experiment.runner_mode import RunnerMode
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.util.experiments_util import util


def default_config() -> ClientConfig:
    """
    :return: Default configuration for the experiment
    """
    agent_config = AgentConfig(gamma=1, alpha=0.00005, epsilon=1, render=False, eval_sleep=0.0,
                               min_epsilon=0.01, eval_episodes=0, train_log_frequency=1,
                               epsilon_decay=0.9999, video=False, eval_log_frequency=1,
                               video_fps=5, video_dir=util.default_output_dir() + "/results/videos",
                               num_iterations=400,
                               eval_render=False, gifs=False,
                               gif_dir=util.default_output_dir() + "/results/gifs",
                               eval_frequency=500000, video_frequency=10,
                               save_dir=util.default_output_dir() + "/results/data",
                               checkpoint_freq=100, input_dim=(5),
                               output_dim=2,
                               pi_hidden_dim=128, pi_hidden_layers=2,
                               vf_hidden_dim=128, vf_hidden_layers=2,
                               shared_hidden_layers=2, shared_hidden_dim=128,
                               batch_size=12000,
                               gpu=False, tensorboard=True,
                               tensorboard_dir=util.default_output_dir() + "/results/tensorboard",
                               optimizer="Adam", lr_exp_decay=False, lr_decay_rate=0.999,
                               state_length=1, gpu_id=0, sde_sample_freq=4, use_sde=False,
                               lr_progress_decay=False, lr_progress_power_decay=4, ent_coef=0.0005,
                               vf_coef=0.5, features_dim=512, gae_lambda=0.95, max_gradient_norm=0.5,
                               eps_clip=0.2, optimization_iterations=10,
                               render_steps=100, illegal_action_logit=-1000,
                               filter_illegal_actions=True, train_progress_deterministic_eval=True,
                               n_deterministic_eval_iter=100, attacker_opponent_baseline_type = 8,
                               running_avg=50, n_quick_eval_iter=100,
                               log_regret=True, snort_baseline_simulate=True, quick_eval_freq=1,
                               eval_deterministic = False, static_eval_defender=True)

    env_name = "csle-ctf-level-9-generated-sim-v6"
    #eval_env_name = "csle-ctf-level-9-generated-sim-v5"
    eval_env_name = "csle-ctf-level-9-generated-sim-v6"

    emulation_config = EmulationConfig(agent_ip="172.18.9.191", agent_username="agent", agent_pw="agent",
                                             server_connection=False, port_forward_next_port=4000)
    # emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip="172.18.9.191",
    #                                        agent_username="agent", agent_pw="agent", server_connection=True,
    #                                        server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                        server_username="kim", port_forward_next_port=4000)
    # emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip="172.18.9.191",
    #                                    agent_username="agent", agent_pw="agent", server_connection=True,
    #                                    server_private_key_file="/Users/kimham/.ssh/csle_id_rsa",
    #                                    server_username="kim", port_forward_next_port=4000)
    eval_emulation_config = EmulationConfig(agent_ip="172.18.9.191", agent_username="agent", agent_pw="agent",
                                           server_connection=False, port_forward_next_port=5000)
    # eval_emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip="172.18.9.191",
    #                               agent_username="agent", agent_pw="agent", server_connection=True,
    #                               server_private_key_file="/Users/kimham/.ssh/csle_id_rsa",
    #                               server_username="kim", port_forward_next_port=5000)
    # eval_emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip="172.18.9.191",
    #                                         agent_username="agent", agent_pw="agent", server_connection=True,
    #                                         server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                         server_username="kim", port_forward_next_port=5000)

    # Novice attacker
    emulation_config.static_attacker_strategy = [99, 33, 1, 70, 104, 106, 107, 99, 165, 104, 106, 58, 104, 331, 99]
    emulation_config.static_attacker_stops_prevented = 2

    # # Experienced Attacker
    # emulation_config.static_attacker_strategy = \
    #     [100, 109, 33, 104, 106, 107, 100, 165, 104, 58, 104, 331, 106, 100, 200, 104,106,100, 266, 104, 106]
    # emulation_config.static_attacker_stops_prevented = 0
    #
    # # Expert attacker
    # emulation_config.static_attacker_strategy = [100, 109, 104, 106, 100, 199, 104, 106,100, 265,
    #                                              104, 106, 100, 113, 104]
    # emulation_config.static_attacker_stops_prevented = 0

    # eval_emulation_config.save_dynamics_model_dir = "/home/kim/workspace/csle/simulation-system/minigames/" \
    #                                                "network_intrusion/ctf/gym-csle-ctf/" \
    #                                               "examples/difficulty_level_9/hello_world/"

    # eval_emulation_config.save_dynamics_model_dir = "/Users/kimham/workspace/csle/simulation-system/minigames/" \
    #                                                 "network_intrusion/ctf/gym-csle-ctf/" \
    #                                                 "examples/difficulty_level_9/hello_world/"

    eval_emulation_config.save_dynamics_model_dir = "/home/kim/csle/simulation-system/use_cases/intrusion_prevention/minigames/ctf/" \
                                                     "gym-csle-ctf/examples/difficulty_level_9/hello_world/"

    eval_emulation_config.skip_exploration = True
    eval_emulation_config.skip_exploration = True
    eval_emulation_config.domain_randomization = False
    eval_emulation_config.emulate_detection = False
    eval_emulation_config.explore_defense_states = False
    eval_emulation_config.use_attacker_action_stats_to_update_defender_state = False

    emulation_config.skip_exploration = True
    emulation_config.domain_randomization = False
    emulation_config.emulate_detection = False
    emulation_config.explore_defense_states = False
    emulation_config.use_attacker_action_stats_to_update_defender_state = False
    emulation_config.save_dynamics_model_dir = eval_emulation_config.save_dynamics_model_dir
    client_config = ClientConfig(env_name=env_name, defender_agent_config=agent_config,
                                 agent_type=AgentType.PPO_BASELINE.value,
                                 output_dir=util.default_output_dir(),
                                 title="PPO-Baseline level 9 v6",
                                 run_many=True, random_seeds=[0, 399, 999],
                                 random_seed=399, mode=RunnerMode.TRAIN_DEFENDER.value,
                                 eval_env=True, eval_env_name=eval_env_name,
                                 eval_emulation_config=eval_emulation_config,
                                 emulation_config=emulation_config,
                                 train_mode =TrainMode.TRAIN_DEFENDER.value)
    return client_config


def write_default_config(path:str = None) -> None:
    """
    Writes the default configuration to a json file

    :param path: the path to write the configuration to
    :return: None
    """
    if path is None:
        path = util.default_config_path()
    config = default_config()
    util.write_config_file(config, path)


# Program entrypoint
if __name__ == '__main__':

    # Setup
    args = util.parse_args(util.default_config_path())
    experiment_title = "PPO level_9 v5 generated simulation"
    if args.configpath is not None and not args.noconfig:
        if not os.path.exists(args.configpath):
            write_default_config()
        config = util.read_config(args.configpath)
    else:
        config = default_config()

    # Run experiment
    if not config.run_many:
        train_csv_path, eval_csv_path = util.run_experiment(config, config.random_seed)
    else:
        train_csv_paths = []
        eval_csv_paths = []
        for seed in config.random_seeds:
            if args.configpath is not None and not args.noconfig:
                if not os.path.exists(args.configpath):
                    write_default_config()
                config = util.read_config(args.configpath)
            else:
                config = default_config()
            train_csv_path, eval_csv_path = util.run_experiment(config, seed)
            train_csv_paths.append(train_csv_path)
            eval_csv_paths.append(eval_csv_path)
