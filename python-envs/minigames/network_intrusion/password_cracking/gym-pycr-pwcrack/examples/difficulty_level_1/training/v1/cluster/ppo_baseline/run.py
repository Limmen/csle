import os
import glob
from gym_pycr_pwcrack.agents.config.agent_config import AgentConfig
from gym_pycr_pwcrack.dao.experiment.client_config import ClientConfig
from gym_pycr_pwcrack.dao.agent.agent_type import AgentType
from gym_pycr_pwcrack.util.experiments_util import util
from gym_pycr_pwcrack.util.experiments_util import plotting_util
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
from gym_pycr_pwcrack.dao.experiment.runner_mode import RunnerMode

def default_config() -> ClientConfig:
    """
    :return: Default configuration for the experiment
    """
    agent_config = AgentConfig(gamma=0.99, alpha=0.0005, epsilon=1, render=False, eval_sleep=0.0,
                                                min_epsilon=0.01, eval_episodes=10, train_log_frequency=1,
                                                epsilon_decay=0.9999, video=False, eval_log_frequency=1,
                                                video_fps=5, video_dir=util.default_output_dir() + "/results/videos",
                                                num_iterations=300,
                                                eval_render=False, gifs=True,
                                                gif_dir=util.default_output_dir() + "/results/gifs",
                                                eval_frequency=100, video_frequency=10,
                                                save_dir=util.default_output_dir() + "/results/data",
                                                checkpoint_freq=100, input_dim=6 * 30,
                                                output_dim=133,
                                                pi_hidden_dim=128, pi_hidden_layers=1,
                                                vf_hidden_dim=128, vf_hidden_layers=1,
                                                shared_hidden_layers=1, shared_hidden_dim=128,
                                                batch_size=2000,
                                                gpu=False, tensorboard=True,
                                                tensorboard_dir=util.default_output_dir() + "/results/tensorboard",
                                                optimizer="Adam", lr_exp_decay=False, lr_decay_rate=0.999,
                                                state_length=1, gpu_id=0, sde_sample_freq=4, use_sde=False,
                                                lr_progress_decay=False, lr_progress_power_decay=4, ent_coef=0.001,
                                                vf_coef=0.5, features_dim=512, gae_lambda=0.95, max_gradient_norm=0.5,
                                                eps_clip=0.2, optimization_iterations=10,
                                                render_steps=20, illegal_action_logit=-100
                                                )
    env_name = "pycr-pwcrack-simple-cluster-v1"
    cluster_config = ClusterConfig(agent_ip="172.18.1.191", agent_username="agent", agent_pw="agent",
                                   server_connection=False)
    # cluster_config = ClusterConfig(server_ip="172.31.212.91", agent_ip="172.18.1.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")
    client_config = ClientConfig(env_name=env_name, agent_config=agent_config,
                                 agent_type=AgentType.PPO_BASELINE.value,
                                 output_dir=util.default_output_dir(),
                                 title="PPO-Baseline v1",
                                 run_many=True, random_seeds=[0, 999, 299, 399, 499],
                                 random_seed=399, cluster_config=cluster_config, mode=RunnerMode.TRAIN_ATTACKER.value)
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
    experiment_title = "PPO simple v1 cluster"
    if args.configpath is not None and not args.noconfig:
        if not os.path.exists(args.configpath):
            write_default_config()
        config = util.read_config(args.configpath)
    else:
        config = default_config()

    # args.plotonly = True
    # args.resultdirs = "results,results2"
    # Plot
    if args.plotonly:
        if args.csvfile is not None:
            plotting_util.plot_csv_files([args.csvfile],
                                        config.output_dir + "/results/plots/" + str(config.random_seed) + "/")
        elif args.resultdirs is not None:
            rds = args.resultdirs.split(",")
            total_files = []
            for rd in rds:
                if config.run_many:
                    csv_files = []
                    for seed in config.random_seeds:
                        p = glob.glob(config.output_dir + "/" + rd + "/data/" + str(seed) + "/*_train.csv")[0]
                        csv_files.append(p)
                    total_files.append(csv_files)
                    #plotting_util.plot_csv_files(csv_files, config.output_dir + "/" + rd + "/plots/")
                else:
                    p = glob.glob(config.output_dir + "/" + rd + "/data/" + str(config.random_seed) + "/*_train.csv")[0]
                    total_files.append([p])
                    # plotting_util.plot_csv_files([p], config.output_dir + "/" + rd + "/plots/"
                    #                              + str(config.random_seed) + "/")

            plotting_util.plot_two_csv_files(total_files, config.output_dir + "/")

        elif config.run_many:
            csv_files = []
            for seed in config.random_seeds:
                p = glob.glob(config.output_dir + "/results/data/" + str(seed) + "/*_train.csv")[0]
                csv_files.append(p)
            plotting_util.plot_csv_files(csv_files, config.output_dir + "/results/plots/")
        else:
            p = glob.glob(config.output_dir + "/results/data/" + str(config.random_seed) + "/*_train.csv")[0]
            plotting_util.plot_csv_files([p], config.output_dir + "/results/plots/" + str(config.random_seed) + "/")

    # Run experiment
    else:
        if not config.run_many:
            train_csv_path, eval_csv_path = util.run_experiment(config, config.random_seed)
            if train_csv_path is not None and not train_csv_path == "":
                plotting_util.plot_csv_files([train_csv_path], config.output_dir + "/results/plots/")
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

            plotting_util.plot_csv_files(train_csv_paths, config.output_dir + "/results/plots/")
