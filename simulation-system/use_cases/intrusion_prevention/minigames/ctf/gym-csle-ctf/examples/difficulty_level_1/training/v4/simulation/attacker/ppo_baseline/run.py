import os
from csle_common.agents.config.agent_config import AgentConfig
from csle_common.dao.experiment.client_config import ClientConfig
from csle_common.dao.agent.agent_type import AgentType
from csle_common.util.experiments_util import util
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.dao.experiment.runner_mode import RunnerMode


def default_config() -> ClientConfig:
    """
    :return: Default configuration for the experiment
    """
    agent_config = AgentConfig(gamma=0.0, alpha=0.0001, epsilon=1, render=False, eval_sleep=0.0,
                               min_epsilon=0.01, eval_episodes=0, train_log_frequency=1,
                               epsilon_decay=0.9999, video=False, eval_log_frequency=1,
                               video_fps=5, video_dir=util.default_output_dir() + "/results/videos",
                               num_iterations=4000,
                               eval_render=True, gifs=True,
                               gif_dir=util.default_output_dir() + "/results/gifs",
                               eval_frequency=25, video_frequency=10,
                               save_dir=util.default_output_dir() + "/results/data",
                               checkpoint_freq=150, input_dim=5 * 8,
                               output_dim=151,
                               pi_hidden_dim=128, pi_hidden_layers=1,
                               vf_hidden_dim=128, vf_hidden_layers=1,
                               shared_hidden_layers=2, shared_hidden_dim=128,
                               batch_size=500,
                               gpu=False, tensorboard=True,
                               tensorboard_dir=util.default_output_dir() + "/results/tensorboard",
                               optimizer="Adam", lr_exp_decay=False, lr_decay_rate=0.999,
                               state_length=1, gpu_id=0, sde_sample_freq=4, use_sde=False,
                               lr_progress_decay=False, lr_progress_power_decay=4, ent_coef=0.001,
                               vf_coef=0.5, features_dim=512, gae_lambda=0.95, max_gradient_norm=0.5,
                               eps_clip=0.2, optimization_iterations=10,
                               render_steps=100, illegal_action_logit=-100,
                               filter_illegal_actions=True, train_progress_deterministic_eval=True,
                               n_deterministic_eval_iter=10)

    # env_name = "csle-ctf-level-1-sim-v4"
    # eval_env_name = "csle-ctf-level-1-emulation-v4"
    env_name = "csle-ctf-level-1-sim-costs-v4"
    eval_env_name = "csle-ctf-level-1-emulation-costs-v4"
    # eval_emulation_config = emulationConfig(server_ip="172.31.212.91", agent_ip="172.18.1.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/csle_id_rsa",
    #                                server_username="kim")
    eval_emulation_config = EmulationConfig(agent_ip="172.18.1.191", agent_username="agent", agent_pw="agent",
                                          server_connection=False)
    client_config = ClientConfig(env_name=env_name, agent_config=agent_config,
                                 agent_type=AgentType.PPO_BASELINE.value,
                                 output_dir=util.default_output_dir(),
                                 title="PPO-Baseline v4",
                                 run_many=True, random_seeds=[0, 999, 299, 399, 499],
                                 random_seed=399, mode=RunnerMode.TRAIN_ATTACKER.value,
                                 eval_env=True, eval_env_name=eval_env_name,
                                 eval_emulation_config=eval_emulation_config)

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

    args = util.parse_args(util.default_config_path())
    experiment_title = "PPO level_1 v4 simulation"
    if args.configpath is not None and not args.noconfig:
        if not os.path.exists(args.configpath):
            write_default_config()
        config = util.read_config(args.configpath)
    else:
        config = default_config()
    if not config.run_many:
        util.run_experiment(config, config.random_seed)
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
