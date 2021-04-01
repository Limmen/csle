import os
import glob
from gym_pycr_ctf.agents.config.agent_config import AgentConfig
from gym_pycr_ctf.dao.experiment.client_config import ClientConfig
from gym_pycr_ctf.dao.agent.agent_type import AgentType
from gym_pycr_ctf.util.experiments_util import util
from gym_pycr_ctf.util.experiments_util import plotting_util
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.dao.experiment.runner_mode import RunnerMode
from gym_pycr_ctf.envs_model.config.generator.env_config_generator import EnvConfigGenerator


def default_config() -> ClientConfig:
    """
    :return: Default configuration for the experiment
    """
    # containers_configs = EnvConfigGenerator.get_all_envs_containers_config(
    #     "/home/kim/pycr/emulation-envs/minigames/network_intrusion/ctf/001/random_many/")
    # flags_configs = EnvConfigGenerator.get_all_envs_flags_config(
    #     "/home/kim/pycr/emulation-envs/minigames/network_intrusion/ctf/001/random_many/")
    # eval_env_containers_configs = EnvConfigGenerator.get_all_envs_containers_config(
    #     "/home/kim/pycr/emulation-envs/minigames/network_intrusion/ctf/001/random_many_2")
    # eval_env_flags_configs = EnvConfigGenerator.get_all_envs_flags_config(
    #     "/home/kim/pycr/emulation-envs/minigames/network_intrusion/ctf/001/random_many_2")
    containers_configs = EnvConfigGenerator.get_all_envs_containers_config(
        "/home/kim/pycr/emulation-envs/minigames/network_intrusion/ctf/001/random_many/")
    flags_configs = EnvConfigGenerator.get_all_envs_flags_config(
        "/home/kim/pycr/emulation-envs/minigames/network_intrusion/ctf/001/random_many/")
    eval_env_containers_configs = EnvConfigGenerator.get_all_envs_containers_config(
        "/home/kim/pycr/emulation-envs/minigames/network_intrusion/ctf/001/random_many_2/")
    eval_env_flags_configs = EnvConfigGenerator.get_all_envs_flags_config(
        "/home/kim/pycr/emulation-envs/minigames/network_intrusion/ctf/001/random_many_2/")

    max_num_nodes_train = max(list(map(lambda x: len(x.containers), containers_configs)))
    max_num_nodes_eval = max(list(map(lambda x: len(x.containers), eval_env_containers_configs)))
    max_num_nodes = max(max_num_nodes_train, max_num_nodes_eval)
    num_nodes = max_num_nodes-1
    n_envs = 1
    agent_config = AgentConfig(gamma=0.99, alpha=0.00005, epsilon=1, render=False, eval_sleep=0.0,
                               min_epsilon=0.01, eval_episodes=1, train_log_frequency=1,
                               epsilon_decay=0.9999, video=False, eval_log_frequency=1,
                               video_fps=5, video_dir=util.default_output_dir() + "/results/videos",
                               num_iterations=400,
                               eval_render=False, gifs=True,
                               gif_dir=util.default_output_dir() + "/results/gifs",
                               eval_frequency=100, video_frequency=10,
                               save_dir=util.default_output_dir() + "/results/data",
                               checkpoint_freq=50,
                               input_dim=num_nodes * 12,
                               # input_dim=7,
                               # input_dim=11 * 8,
                               # output_dim=9,
                               output_dim=9 + (3 * num_nodes),
                               pi_hidden_dim=64, pi_hidden_layers=1,
                               vf_hidden_dim=64, vf_hidden_layers=1,
                               shared_hidden_layers=2, shared_hidden_dim=64,
                               # batch_size=util.round_batch_size(int(2000/n_envs)),
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
                               n_deterministic_eval_iter=0, eval_deterministic=False,
                               num_nodes=max_num_nodes, domain_randomization=False,
                               n_quick_eval_iter=50, dr_max_num_nodes=max_num_nodes,
                               dr_min_num_nodes=4, dr_min_num_users=1,
                               dr_max_num_users=5, dr_min_num_flags=1, dr_max_num_flags=3,
                               dr_use_base=True, log_regret=True, running_avg=50
                               )
    # eval_env_name = "pycr-ctf-random-emulation-v1"
    # eval_env_containers_config = util.read_containers_config(
    #     "/home/kim/storage/workspace/pycr/emulation-envs/minigames/network_intrusion/ctf/001/level_1/containers.json")
    # eval_env_flags_config = util.read_flags_config("/home/kim/storage/workspace/pycr/emulation-envs/minigames/network_intrusion/ctf/001/level_1/flags.json")
    eval_env_name = "pycr-ctf-random-many-emulation-v1"
    eval_n_envs = 1

    env_name = "pycr-ctf-random-many-emulation-v1"
    #env_name = "pycr-ctf-random-many-emulation-costs-v1"
    emulation_configs = [
        EmulationConfig(agent_ip=containers_configs[i].agent_ip, agent_username="agent", agent_pw="agent",
                        server_connection=False, port_forward_next_port=4001 + i*150,
                        warmup=True, warmup_iterations=500)
        for i in range(len(containers_configs))
    ]
    # emulation_configs = [
    #     emulationConfig(agent_ip=containers_configs[i].agent_ip, agent_username="agent", agent_pw="agent",
    #                   server_connection=True, server_private_key_file="/home/kim/.ssh/id_rsa",
    #                   server_username="kim", server_ip="172.31.212.92",
    #                   port_forward_next_port=2001 + i * 150,
    #                   warmup=True, warmup_iterations=500)
    #     for i in range(len(containers_configs))
    # ]

    # eval_emulation_config = emulationConfig(agent_ip="172.18.1.191", agent_username="agent", agent_pw="agent",
    #                                     server_connection=False)
    eval_env_emulation_configs = [
        EmulationConfig(agent_ip=eval_env_containers_configs[i].agent_ip, agent_username="agent", agent_pw="agent",
                        server_connection=False, port_forward_next_port=6001 + i * 150,
                        warmup=True, warmup_iterations=500)
        for i in range(len(eval_env_containers_configs))
    ]

    # eval_env_emulation_configs = [
    #     emulationConfig(agent_ip=eval_env_containers_configs[i].agent_ip, agent_username="agent", agent_pw="agent",
    #                   server_connection=True, server_private_key_file="/home/kim/.ssh/id_rsa",
    #                   server_username="kim", server_ip="172.31.212.92",
    #                   port_forward_next_port=8001 + i * 150,
    #                   warmup=True, warmup_iterations=500)
    #     for i in range(len(eval_env_containers_configs))
    # ]

    # emulation_config = emulationConfig(server_ip="172.31.212.92", agent_ip="172.18.2.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim", warmup=True, warmup_iterations=500,
    #                                port_forward_next_port=4000)
    # emulation_config = emulationConfig(server_ip="172.31.212.91", agent_ip="172.18.2.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")
    # emulation_config = emulationConfig(server_ip="172.31.212.91", agent_ip="172.18.2.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
    #                                server_username="kim")
    client_config = ClientConfig(env_name=env_name, agent_config=agent_config,
                                 agent_type=AgentType.PPO_BASELINE.value,
                                 output_dir=util.default_output_dir(),
                                 title="PPO-Baseline random many v1",
                                 run_many=True, random_seeds=[0, 999, 299],
                                 random_seed=399, emulation_configs=emulation_configs, mode=RunnerMode.TRAIN_ATTACKER.value,
                                 containers_configs=containers_configs, flags_configs=flags_configs,
                                 dummy_vec_env=False, sub_proc_env=True, n_envs=n_envs,
                                 randomized_env=False, multi_env=True,
                                 eval_env=True,
                                 eval_env_name=eval_env_name, eval_env_emulation_configs=eval_env_emulation_configs,
                                 eval_env_containers_configs=eval_env_containers_configs,
                                 eval_env_flags_configs=eval_env_flags_configs, eval_multi_env=True,
                                 eval_env_num_nodes=max_num_nodes, eval_n_envs = eval_n_envs,
                                 eval_dummy_vec_env=False, eval_sub_proc_env=True
                                 # eval_env_flags_config = eval_env_flags_config,
                                 # eval_env_containers_config = eval_env_containers_config,
                                 # eval_env_num_nodes=num_nodes, eval_randomized_env=True
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
    experiment_title = "PPO random many v1 emulation"
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
