import os
import glob
from gym_pycr_ctf.agents.config.agent_config import AgentConfig
from gym_pycr_ctf.dao.experiment.client_config import ClientConfig
from gym_pycr_ctf.dao.agent.agent_type import AgentType
from gym_pycr_ctf.util.experiments_util import util
from gym_pycr_ctf.util.experiments_util import plotting_util
from gym_pycr_ctf.dao.network.cluster_config import ClusterConfig
from gym_pycr_ctf.dao.experiment.runner_mode import RunnerMode
from gym_pycr_ctf.envs.config.generator.env_config_generator import EnvConfigGenerator
from gym_pycr_ctf.dao.network.env_config import EnvConfig

def default_config() -> ClientConfig:
    """
    :return: Default configuration for the experiment
    """
    max_num_nodes = 10
    agent_config = AgentConfig(gamma=0.99, alpha=0.00005, epsilon=1, render=False, eval_sleep=0.0,
                                                min_epsilon=0.01, eval_episodes=1, train_log_frequency=1,
                                                epsilon_decay=0.9999, video=False, eval_log_frequency=1,
                                                video_fps=5, video_dir=util.default_output_dir() + "/results/videos",
                                                num_iterations=5000,
                                                eval_render=False, gifs=True,
                                                gif_dir=util.default_output_dir() + "/results/gifs",
                                                eval_frequency=100, video_frequency=10,
                                                save_dir=util.default_output_dir() + "/results/data",
                                                checkpoint_freq=500,
                                                input_dim=(max_num_nodes-1) * 12,
                                                output_dim = 9 + (3*(max_num_nodes-1)),
                                                pi_hidden_dim=64, pi_hidden_layers=1,
                                                vf_hidden_dim=64, vf_hidden_layers=1,
                                                shared_hidden_layers=2, shared_hidden_dim=64,
                                                batch_size=2000,
                                                gpu=False, tensorboard=True,
                                                tensorboard_dir=util.default_output_dir() + "/results/tensorboard",
                                                optimizer="Adam", lr_exp_decay=False, lr_decay_rate=0.999,
                                                state_length=1, gpu_id=0, sde_sample_freq=4, use_sde=False,
                                                lr_progress_decay=False, lr_progress_power_decay=4, ent_coef=0.0005,
                                                vf_coef=0.5, features_dim=512, gae_lambda=0.95, max_gradient_norm=0.5,
                                                eps_clip=0.2, optimization_iterations=10,
                                                render_steps=100, illegal_action_logit=-100,
                                                filter_illegal_actions=True, train_progress_deterministic_eval=True,
                                                n_deterministic_eval_iter=1, eval_deterministic=False,
                                                num_nodes=max_num_nodes, domain_randomization = True,
                                                dr_max_num_nodes=max_num_nodes,
                                                dr_min_num_nodes=4, dr_min_num_users=1,
                                                dr_max_num_users=5, dr_min_num_flags=1, dr_max_num_flags=3,
                                                dr_use_base=True, log_regret=True, running_avg=50
                                                )
    eval_env_name = "pycr-ctf-multisim-v1"
    eval_n_envs = 1
    env_name="pycr-ctf-multisim-v1"
    client_config = ClientConfig(env_name=env_name, agent_config=agent_config,
                                 agent_type=AgentType.PPO_BASELINE.value,
                                 output_dir=util.default_output_dir(),
                                 title="PPO-Baseline multisim v1",
                                 run_many=True, random_seeds=[0, 999],
                                 random_seed=399, mode=RunnerMode.TRAIN_ATTACKER.value,
                                 dummy_vec_env=False, sub_proc_env=True, n_envs=1,
                                 randomized_env=False, multi_env=False,
                                 eval_env=True,
                                 eval_env_name=eval_env_name,
                                 eval_multi_env=False,
                                 eval_env_num_nodes=max_num_nodes, eval_n_envs = eval_n_envs,
                                 eval_dummy_vec_env=False, eval_sub_proc_env=True,
                                 train_multi_sim=True,  eval_multi_sim=True, num_sims = 10, num_sims_eval=2
                                 )
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
    experiment_title = "PPO multisim v1 cluster"
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
