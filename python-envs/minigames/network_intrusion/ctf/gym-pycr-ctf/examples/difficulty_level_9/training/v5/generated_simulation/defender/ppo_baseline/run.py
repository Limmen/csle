import glob
import os

from gym_pycr_ctf.util.plots import plotting_util_defender
from gym_pycr_ctf.agents.config.agent_config import AgentConfig
from gym_pycr_ctf.dao.agent.agent_type import AgentType
from gym_pycr_ctf.dao.agent.train_mode import TrainMode
from gym_pycr_ctf.dao.experiment.client_config import ClientConfig
from gym_pycr_ctf.dao.experiment.runner_mode import RunnerMode
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.util.experiments_util import util


def default_config() -> ClientConfig:
    """
    :return: Default configuration for the experiment
    """
    agent_config = AgentConfig(gamma=1, alpha=0.00001, epsilon=1, render=False, eval_sleep=0.0,
                               min_epsilon=0.01, eval_episodes=0, train_log_frequency=1,
                               epsilon_decay=0.9999, video=False, eval_log_frequency=1,
                               video_fps=5, video_dir=util.default_output_dir() + "/results/videos",
                               num_iterations=200,
                               eval_render=False, gifs=False,
                               gif_dir=util.default_output_dir() + "/results/gifs",
                               eval_frequency=500000, video_frequency=10,
                               save_dir=util.default_output_dir() + "/results/data",
                               checkpoint_freq=50, input_dim=(9),
                               output_dim=2,
                               pi_hidden_dim=32, pi_hidden_layers=1,
                               vf_hidden_dim=32, vf_hidden_layers=1,
                               shared_hidden_layers=2, shared_hidden_dim=128,
                               batch_size=8000,
                               gpu=False, tensorboard=True,
                               tensorboard_dir=util.default_output_dir() + "/results/tensorboard",
                               optimizer="Adam", lr_exp_decay=False, lr_decay_rate=0.999,
                               state_length=1, gpu_id=0, sde_sample_freq=4, use_sde=False,
                               lr_progress_decay=False, lr_progress_power_decay=4, ent_coef=0.0005,
                               vf_coef=0.5, features_dim=512, gae_lambda=0.95, max_gradient_norm=0.5,
                               eps_clip=0.2, optimization_iterations=10,
                               render_steps=100, illegal_action_logit=-1000,
                               filter_illegal_actions=True, train_progress_deterministic_eval=True,
                               n_deterministic_eval_iter=1, attacker_opponent_baseline_type = 8,
                               running_avg=50, n_quick_eval_iter=100,
                               log_regret=True, snort_baseline_simulate=True, quick_eval_freq=1,
                               eval_deterministic = False, static_eval_defender=True
                               )
    env_name = "pycr-ctf-level-9-generated-sim-v5"
    #eval_env_name = "pycr-ctf-level-9-generated-sim-v5"
    eval_env_name = "pycr-ctf-level-9-emulation-v5"

    # env_name = "pycr-ctf-level-4-generated-sim-costs-v1"
    # eval_env_name = "pycr-ctf-level-4-emulation-costs-v1"

    # eval_emulation_config = EmulationConfig(server_ip="172.31.212.91", agent_ip="172.18.4.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
    #                                server_username="kim")
    #     EmulationConfig(agent_ip=eval_env_containers_configs[i].agent_ip, agent_username="agent", agent_pw="agent",
    #                   server_connection=True, server_private_key_file="/home/kim/.ssh/id_rsa",
    #                   server_username="kim", server_ip="172.31.212.92",
    #                   port_forward_next_port=8001 + i * 150,
    #                   warmup=True, warmup_iterations=500)

    # emulation_config = EmulationConfig(agent_ip="172.18.9.191", agent_username="agent", agent_pw="agent",
    #                                         server_connection=False, port_forward_next_port=4000)
    emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip="172.18.9.191",
                                            agent_username="agent", agent_pw="agent", server_connection=True,
                                            server_private_key_file="/home/kim/.ssh/id_rsa",
                                            server_username="kim", port_forward_next_port=4000)
    # eval_emulation_config = EmulationConfig(agent_ip="172.18.9.191", agent_username="agent", agent_pw="agent",
    #                                       server_connection=False, port_forward_next_port=5000)
    eval_emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip="172.18.9.191",
                                   agent_username="agent", agent_pw="agent", server_connection=True,
                                   server_private_key_file="/home/kim/.ssh/id_rsa",
                                   server_username="kim", port_forward_next_port=5000)

    eval_emulation_config.save_dynamics_model_dir = "/home/kim/storage/workspace/pycr/python-envs/minigames/" \
                                                    "network_intrusion/ctf/gym-pycr-ctf/" \
                                                    "examples/difficulty_level_9/hello_world/"
    # eval_emulation_config.save_dynamics_model_dir = "/Users/kimham/workspace/pycr/python-envs/minigames/" \
    #                                                 "network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_4/" \
    #                                                 "hello_world/defender_dynamics_model.json"

    # eval_emulation_config.save_dynamics_model_dir = "/home/kim/pycr/python-envs/minigames/network_intrusion/ctf/" \
    #                                                 "gym-pycr-ctf/examples/difficulty_level_9/hello_world"

    eval_emulation_config.skip_exploration = True
    emulation_config.skip_exploration = True
    emulation_config.save_dynamics_model_dir = eval_emulation_config.save_dynamics_model_dir
    client_config = ClientConfig(env_name=env_name, defender_agent_config=agent_config,
                                 agent_type=AgentType.PPO_BASELINE.value,
                                 output_dir=util.default_output_dir(),
                                 title="PPO-Baseline level 9 v5",
                                 run_many=True, random_seeds=[0, 999],
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