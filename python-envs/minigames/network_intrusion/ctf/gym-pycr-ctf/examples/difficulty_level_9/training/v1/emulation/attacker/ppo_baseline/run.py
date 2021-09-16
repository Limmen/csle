import os
import glob
from pycr_common.agents.config.agent_config import AgentConfig
from pycr_common.dao.experiment.client_config import ClientConfig
from pycr_common.dao.agent.agent_type import AgentType
from pycr_common.util.experiments_util import util
from gym_pycr_ctf.util.plots import plotting_util_basic
from pycr_common.dao.network.emulation_config import EmulationConfig
from pycr_common.dao.experiment.runner_mode import RunnerMode
from pycr_common.dao.agent.train_mode import TrainMode

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
                               checkpoint_freq=50, input_dim=(20)*33,
                               output_dim=372,
                               pi_hidden_dim=64, pi_hidden_layers=2,
                               vf_hidden_dim=64, vf_hidden_layers=2,
                               shared_hidden_layers=2, shared_hidden_dim=64,
                               batch_size=2000,
                               gpu=False, tensorboard=True,
                               tensorboard_dir=util.default_output_dir() + "/results/tensorboard",
                               optimizer="Adam", lr_exp_decay=False, lr_decay_rate=0.999,
                               state_length=1, gpu_id=0, sde_sample_freq=4, use_sde=False,
                               lr_progress_decay=False, lr_progress_power_decay=4, ent_coef=0.0005,
                               vf_coef=0.5, features_dim=512, gae_lambda=0.95, max_gradient_norm=0.5,
                               eps_clip=0.2, optimization_iterations=10,
                               render_steps=100, illegal_action_logit=-1000,
                               filter_illegal_actions=True, train_progress_deterministic_eval=True,
                               n_deterministic_eval_iter=1, attacker_opponent_baseline_type=8,
                               running_avg=50, n_quick_eval_iter=10,
                               log_regret=True, snort_baseline_simulate=False, quick_eval_freq=1,
                               eval_deterministic=False
                               )
    env_name = "pycr-ctf-level-9-generated-sim-v1"
    eval_env_name = "pycr-ctf-level-9-generated-sim-v1"

    emulation_config = EmulationConfig(agent_ip="172.18.9.191", agent_username="agent", agent_pw="agent",
                                       server_connection=False, port_forward_next_port=4000)
    # emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip="172.18.4.191",
    #                                         agent_username="agent", agent_pw="agent", server_connection=True,
    #                                         server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                         server_username="kim", port_forward_next_port=4000)
    eval_emulation_config = EmulationConfig(agent_ip="172.18.9.191", agent_username="agent", agent_pw="agent",
                                            server_connection=False, port_forward_next_port=5000)
    # eval_emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip="172.18.4.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim", port_forward_next_port=5000)

    # eval_emulation_config.save_dynamics_model_dir = "/home/kim/storage/workspace/pycr/python-envs/minigames/" \
    #                                                 "network_intrusion/ctf/gym-pycr-ctf/" \
    #                                                 "examples/difficulty_level_4/hello_world/"
    # eval_emulation_config.save_dynamics_model_dir = "/Users/kimham/workspace/pycr/python-envs/minigames/" \
    #                                                 "network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_4/" \
    #                                                 "hello_world/defender_dynamics_model.json"
    eval_emulation_config.save_dynamics_model_dir = "/home/kim/pycr/python-envs/minigames/network_intrusion/ctf/" \
                                                    "gym-pycr-ctf/examples/difficulty_level_9/hello_world/"

    eval_emulation_config.skip_exploration = True
    emulation_config.skip_exploration = True
    emulation_config.save_dynamics_model_dir = eval_emulation_config.save_dynamics_model_dir

    client_config = ClientConfig(env_name=env_name, attacker_agent_config=agent_config,
                                 agent_type=AgentType.PPO_BASELINE.value,
                                 output_dir=util.default_output_dir(),
                                 title="PPO level_9 v1 emulation",
                                 run_many=True, random_seeds=[0, 999, 299],
                                 random_seed=299, emulation_config=emulation_config,
                                 mode=RunnerMode.TRAIN_ATTACKER.value, train_mode=TrainMode.TRAIN_ATTACKER
                                 )
    #random_seeds = [0, 999, 299, 399, 499],
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
    experiment_title = "PPO level_9 v1 emulation"
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
            plotting_util_basic.plot_csv_files([args.csvfile],
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

            plotting_util_basic.plot_two_csv_files(total_files, config.output_dir + "/")

        elif config.run_many:
            csv_files = []
            for seed in config.random_seeds:
                p = glob.glob(config.output_dir + "/results/data/" + str(seed) + "/*_train.csv")[0]
                csv_files.append(p)
            plotting_util_basic.plot_csv_files(csv_files, config.output_dir + "/results/plots/")
        else:
            p = glob.glob(config.output_dir + "/results/data/" + str(config.random_seed) + "/*_train.csv")[0]
            plotting_util_basic.plot_csv_files([p], config.output_dir + "/results/plots/" + str(config.random_seed) + "/")

    # Run experiment
    else:
        if not config.run_many:
            train_csv_path, eval_csv_path = util.run_experiment(config, config.random_seed)
            if train_csv_path is not None and not train_csv_path == "":
                plotting_util_basic.plot_csv_files([train_csv_path], config.output_dir + "/results/plots/")
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

            plotting_util_basic.plot_csv_files(train_csv_paths, config.output_dir + "/results/plots/")
