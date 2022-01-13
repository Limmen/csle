from typing import List
import pandas as pd
import numpy as np
import glob
from csle_common.util.experiments_util import util
from csle_common.dao.container_config.containers_config import ContainersConfig
from csle_common.envs_model.config.generator.env_config_generator import EnvConfigGenerator
from gym_csle_ctf.util.plots import plotting_util_mult_envs

def parse_data(base_path: str, suffix: str,
               train_containers_configs: List[ContainersConfig], eval_containers_configs: List[ContainersConfig],
               ips = None, eval_ips = None, multi_env: bool = False, mult_env_dr : bool = False):
    print(glob.glob(base_path + "0/*_train.csv"))
    if multi_env:
        ppo_v1_df_0 = pd.read_csv(glob.glob(base_path + "0/*_train.csv")[0])
        ppo_v1_df_7615 = pd.read_csv(glob.glob(base_path + "7615/*_train.csv")[0])
        ppo_dfs_v1 = [ppo_v1_df_0, ppo_v1_df_7615]
    elif mult_env_dr:
        ppo_v1_df_0 = pd.read_csv(glob.glob(base_path + "0/*_train.csv")[0])
        ppo_v1_df_9170 = pd.read_csv(glob.glob(base_path + "9170/*_train.csv")[0])
        ppo_v1_df_81810 = pd.read_csv(glob.glob(base_path + "81810/*_train.csv")[0])
        #ppo_dfs_v1 = [ppo_v1_df_0, ppo_v1_df_9170, ppo_v1_df_81810]
        ppo_dfs_v1 = [ppo_v1_df_9170, ppo_v1_df_81810]
        #ppo_dfs_v1 = [ppo_v1_df_9170, ppo_v1_df_81810]
        #ppo_dfs_v1 = [ppo_v1_df_9170]
        # ppo_dfs_v1 = [ppo_v1_df_81810]
        # ppo_dfs_v1 = [ppo_v1_df_0]
    else:
        ppo_v1_df_0 = pd.read_csv(glob.glob(base_path + "0/*_train.csv")[0])
        ppo_v1_df_71820 = pd.read_csv(glob.glob(base_path + "71820/*_train.csv")[0])
        ppo_v1_df_91444 = pd.read_csv(glob.glob(base_path + "91444/*_train.csv")[0])
        ppo_dfs_v1 = [ppo_v1_df_0, ppo_v1_df_71820, ppo_v1_df_91444]
    max_len = min(list(map(lambda x: len(x), ppo_dfs_v1)))

    running_avg = 10

    # Train avg
    avg_train_rewards_data_v1 = list(
        map(lambda df: util.running_average_list(df["attacker_avg_episode_rewards"].values[0:max_len], running_avg), ppo_dfs_v1))
    avg_train_rewards_means_v1 = np.mean(tuple(avg_train_rewards_data_v1), axis=0)
    avg_train_rewards_stds_v1 = np.std(tuple(avg_train_rewards_data_v1), axis=0, ddof=1)

    avg_train_steps_data_v1 = list(
        map(lambda df: util.running_average_list(df["avg_episode_steps"].values[0:max_len], running_avg), ppo_dfs_v1))
    avg_train_steps_means_v1 = np.mean(tuple(avg_train_steps_data_v1), axis=0)
    avg_train_steps_stds_v1 = np.std(tuple(avg_train_steps_data_v1), axis=0, ddof=1)

    avg_train_regret_data_v1 = list(
        map(lambda df: util.running_average_list(df["attacker_avg_regret"].values[0:max_len], running_avg), ppo_dfs_v1))
    avg_train_regret_means_v1 = np.mean(tuple(avg_train_regret_data_v1), axis=0)
    avg_train_regret_stds_v1 = np.std(tuple(avg_train_regret_data_v1), axis=0, ddof=1)

    avg_train_opt_frac_data_v1 = list(
        map(lambda df: util.running_average_list(df["attacker_avg_opt_frac"].values[0:max_len], running_avg), ppo_dfs_v1))
    avg_train_opt_frac_data_v1 = list(map(lambda x: np.minimum(np.array([1] * len(x)), x), avg_train_opt_frac_data_v1))
    avg_train_opt_frac_means_v1 = np.mean(tuple(avg_train_opt_frac_data_v1), axis=0)
    avg_train_opt_frac_stds_v1 = np.std(tuple(avg_train_opt_frac_data_v1), axis=0, ddof=1)

    avg_train_caught_frac_data_v1 = list(
        map(lambda df: util.running_average_list(df["caught_frac"].values[0:max_len], running_avg), ppo_dfs_v1))
    avg_train_caught_frac_means_v1 = np.mean(tuple(avg_train_caught_frac_data_v1), axis=0)
    avg_train_caught_frac_stds_v1 = np.std(tuple(avg_train_caught_frac_data_v1), axis=0, ddof=1)

    avg_train_early_stopping_frac_data_v1 = list(
        map(lambda df: util.running_average_list(df["early_stopping_frac"].values[0:max_len], running_avg), ppo_dfs_v1))
    avg_train_early_stopping_means_v1 = np.mean(tuple(avg_train_early_stopping_frac_data_v1), axis=0)
    avg_train_early_stopping_stds_v1 = np.std(tuple(avg_train_early_stopping_frac_data_v1), axis=0, ddof=1)

    avg_train_intrusion_frac_data_v1 = list(
        map(lambda df: util.running_average_list(df["intrusion_frac"].values[0:max_len], running_avg), ppo_dfs_v1))
    avg_train_intrusion_means_v1 = np.mean(tuple(avg_train_intrusion_frac_data_v1), axis=0)
    avg_train_intrusion_stds_v1 = np.std(tuple(avg_train_intrusion_frac_data_v1), axis=0, ddof=1)

    avg_train_attacker_action_costs_data_v1 = list(
        map(lambda df: util.running_average_list(df["attacker_action_costs"].values[0:max_len], running_avg), ppo_dfs_v1))
    avg_train_attacker_action_costs_means_v1 = np.mean(tuple(avg_train_attacker_action_costs_data_v1), axis=0)
    avg_train_attacker_action_costs_stds_v1 = np.std(tuple(avg_train_attacker_action_costs_data_v1), axis=0, ddof=1)

    avg_train_attacker_action_alerts_data_v1 = list(
        map(lambda df: util.running_average_list(df["attacker_action_alerts"].values[0:max_len], running_avg),
            ppo_dfs_v1))
    avg_train_attacker_action_alerts_means_v1 = np.mean(tuple(avg_train_attacker_action_alerts_data_v1), axis=0)
    avg_train_attacker_action_alerts_stds_v1 = np.std(tuple(avg_train_attacker_action_alerts_data_v1), axis=0,
                                                      ddof=1)

    avg_train_flags_data_v1 = list(
        map(lambda df: util.running_average_list(df["avg_episode_flags_percentage"].values[0:max_len], running_avg), ppo_dfs_v1))
    avg_train_flags_means_v1 = np.mean(tuple(avg_train_flags_data_v1), axis=0)
    avg_train_flags_stds_v1 = np.std(tuple(avg_train_flags_data_v1), axis=0, ddof=1)

    # Eval avg
    avg_eval_rewards_data_v1 = list(
        map(lambda df: util.running_average_list(df["attacker_eval_avg_episode_rewards"].values[0:max_len], running_avg), ppo_dfs_v1))
    avg_eval_rewards_means_v1 = np.mean(tuple(avg_eval_rewards_data_v1), axis=0)
    avg_eval_rewards_stds_v1 = np.std(tuple(avg_eval_rewards_data_v1), axis=0, ddof=1)

    avg_eval_steps_data_v1 = list(
        map(lambda df: util.running_average_list(df["eval_avg_episode_steps"].values[0:max_len], running_avg), ppo_dfs_v1))
    avg_eval_steps_means_v1 = np.mean(tuple(avg_eval_steps_data_v1), axis=0)
    avg_eval_steps_stds_v1 = np.std(tuple(avg_eval_steps_data_v1), axis=0, ddof=1)

    avg_eval_regret_data_v1 = list(
        map(lambda df: util.running_average_list(df["attacker_eval_avg_regret"].values[0:max_len], running_avg), ppo_dfs_v1))
    avg_eval_regret_means_v1 = np.mean(tuple(avg_eval_regret_data_v1), axis=0)
    avg_eval_regret_stds_v1 = np.std(tuple(avg_eval_regret_data_v1), axis=0, ddof=1)

    avg_eval_opt_frac_data_v1 = list(
        map(lambda df: util.running_average_list(df["attacker_eval_avg_opt_frac"].values[0:max_len], running_avg), ppo_dfs_v1))
    avg_eval_opt_frac_data_v1 = list(map(lambda x: np.minimum(np.array([1] * len(x)), x), avg_eval_opt_frac_data_v1))
    avg_eval_opt_frac_means_v1 = np.mean(tuple(avg_eval_opt_frac_data_v1), axis=0)
    avg_eval_opt_frac_stds_v1 = np.std(tuple(avg_eval_opt_frac_data_v1), axis=0, ddof=1)

    avg_eval_caught_frac_data_v1 = list(
        map(lambda df: util.running_average_list(df["eval_caught_frac"].values[0:max_len], running_avg), ppo_dfs_v1))
    avg_eval_caught_frac_means_v1 = np.mean(tuple(avg_eval_caught_frac_data_v1), axis=0)
    avg_eval_caught_frac_stds_v1 = np.std(tuple(avg_eval_caught_frac_data_v1), axis=0, ddof=1)

    avg_eval_early_stopping_frac_data_v1 = list(
        map(lambda df: util.running_average_list(df["eval_early_stopping_frac"].values[0:max_len], running_avg), ppo_dfs_v1))
    avg_eval_early_stopping_means_v1 = np.mean(tuple(avg_eval_early_stopping_frac_data_v1), axis=0)
    avg_eval_early_stopping_stds_v1 = np.std(tuple(avg_eval_early_stopping_frac_data_v1), axis=0, ddof=1)

    avg_eval_intrusion_frac_data_v1 = list(
        map(lambda df: util.running_average_list(df["eval_intrusion_frac"].values[0:max_len], running_avg), ppo_dfs_v1))
    avg_eval_intrusion_means_v1 = np.mean(tuple(avg_eval_intrusion_frac_data_v1), axis=0)
    avg_eval_intrusion_stds_v1 = np.std(tuple(avg_eval_intrusion_frac_data_v1), axis=0, ddof=1)


    avg_eval_attacker_action_alerts_data_v1 = list(
        map(lambda df: util.running_average_list(df["eval_attacker_action_alerts"].values[0:max_len], running_avg),
            ppo_dfs_v1))
    avg_eval_attacker_action_alerts_means_v1 = np.mean(tuple(avg_eval_attacker_action_alerts_data_v1), axis=0)
    avg_eval_attacker_action_alerts_stds_v1 = np.std(tuple(avg_eval_attacker_action_alerts_data_v1), axis=0,
                                                      ddof=1)

    avg_eval_attacker_action_costs_data_v1 = list(
        map(lambda df: util.running_average_list(df["eval_attacker_action_costs"].values[0:max_len], running_avg),
            ppo_dfs_v1))
    avg_eval_attacker_action_costs_means_v1 = np.mean(tuple(avg_eval_attacker_action_costs_data_v1), axis=0)
    avg_eval_attacker_action_costs_stds_v1 = np.std(tuple(avg_eval_attacker_action_costs_data_v1), axis=0, ddof=1)

    avg_eval_flags_data_v1 = list(
        map(lambda df: util.running_average_list(df["eval_avg_episode_flags_percentage"].values[0:max_len], running_avg), ppo_dfs_v1))
    avg_eval_flags_means_v1 = np.mean(tuple(avg_eval_flags_data_v1), axis=0)
    avg_eval_flags_stds_v1 = np.std(tuple(avg_eval_flags_data_v1), axis=0, ddof=1)

    # Eval 2 avg
    avg_eval_2_rewards_data_v1 = list(
        map(lambda df: util.running_average_list(df["attacker_eval_2_avg_episode_rewards"].values[0:max_len], running_avg) + 10,
            ppo_dfs_v1))
    avg_eval_2_rewards_means_v1 = np.mean(tuple(avg_eval_2_rewards_data_v1), axis=0)
    avg_eval_2_rewards_stds_v1 = np.std(tuple(avg_eval_2_rewards_data_v1), axis=0, ddof=1)

    avg_eval_2_steps_data_v1 = list(
        map(lambda df: util.running_average_list(df["eval_2_avg_episode_steps"].values[0:max_len], running_avg), ppo_dfs_v1))
    avg_eval_2_steps_means_v1 = np.mean(tuple(avg_eval_2_steps_data_v1), axis=0)
    avg_eval_2_steps_stds_v1 = np.std(tuple(avg_eval_2_steps_data_v1), axis=0, ddof=1)

    avg_eval_2_regret_data_v1 = list(
        map(lambda df: util.running_average_list(df["attacker_eval_2_avg_regret"].values[0:max_len], running_avg), ppo_dfs_v1))
    avg_eval_2_regret_means_v1 = np.mean(tuple(avg_eval_2_regret_data_v1), axis=0)
    avg_eval_2_regret_stds_v1 = np.std(tuple(avg_eval_2_regret_data_v1), axis=0, ddof=1)

    avg_eval_2_opt_frac_data_v1 = list(
        map(lambda df: util.running_average_list(df["attacker_eval_2_avg_opt_frac"].values[0:max_len], running_avg), ppo_dfs_v1))
    avg_eval_2_opt_frac_data_v1 = list(map(lambda x: np.minimum(np.array([1] * len(x)), x), avg_eval_2_opt_frac_data_v1))
    avg_eval_2_opt_frac_means_v1 = np.mean(tuple(avg_eval_2_opt_frac_data_v1), axis=0)
    avg_eval_2_opt_frac_stds_v1 = np.std(tuple(avg_eval_2_opt_frac_data_v1), axis=0, ddof=1)

    avg_eval_2_caught_frac_data_v1 = list(
        map(lambda df: util.running_average_list(df["eval_2_caught_frac"].values[0:max_len], running_avg), ppo_dfs_v1))
    avg_eval_2_caught_frac_means_v1 = np.mean(tuple(avg_eval_2_caught_frac_data_v1), axis=0)
    avg_eval_2_caught_frac_stds_v1 = np.std(tuple(avg_eval_2_caught_frac_data_v1), axis=0, ddof=1)

    avg_eval_2_early_stopping_frac_data_v1 = list(
        map(lambda df: util.running_average_list(df["eval_2_early_stopping_frac"].values[0:max_len], running_avg), ppo_dfs_v1))
    avg_eval_2_early_stopping_means_v1 = np.mean(tuple(avg_eval_2_early_stopping_frac_data_v1), axis=0)
    avg_eval_2_early_stopping_stds_v1 = np.std(tuple(avg_eval_2_early_stopping_frac_data_v1), axis=0, ddof=1)

    avg_eval_2_intrusion_frac_data_v1 = list(
        map(lambda df: util.running_average_list(df["eval_2_intrusion_frac"].values[0:max_len], running_avg), ppo_dfs_v1))
    avg_eval_2_intrusion_means_v1 = np.mean(tuple(avg_eval_2_intrusion_frac_data_v1), axis=0)
    avg_eval_2_intrusion_stds_v1 = np.std(tuple(avg_eval_2_intrusion_frac_data_v1), axis=0, ddof=1)

    avg_eval_2_attacker_action_alerts_data_v1 = list(
        map(lambda df: util.running_average_list(df["eval_2_attacker_action_alerts"].values[0:max_len], running_avg),
            ppo_dfs_v1))
    avg_eval_2_attacker_action_alerts_means_v1 = np.mean(tuple(avg_eval_2_attacker_action_alerts_data_v1), axis=0)
    avg_eval_2_attacker_action_alerts_stds_v1 = np.std(tuple(avg_eval_2_attacker_action_alerts_data_v1), axis=0,
                                                      ddof=1)

    avg_eval_2_attacker_action_costs_data_v1 = list(
        map(lambda df: util.running_average_list(df["eval_2_attacker_action_costs"].values[0:max_len], running_avg),
            ppo_dfs_v1))
    avg_eval_2_attacker_action_costs_means_v1 = np.mean(tuple(avg_eval_2_attacker_action_costs_data_v1), axis=0)
    avg_eval_2_attacker_action_costs_stds_v1 = np.std(tuple(avg_eval_2_attacker_action_costs_data_v1), axis=0, ddof=1)

    avg_eval_2_flags_data_v1 = list(
        map(lambda df: util.running_average_list(df["eval_2_avg_episode_flags_percentage"].values[0:max_len], running_avg), ppo_dfs_v1))
    avg_eval_2_flags_means_v1 = np.mean(tuple(avg_eval_2_flags_data_v1), axis=0)
    avg_eval_2_flags_stds_v1 = np.std(tuple(avg_eval_2_flags_data_v1), axis=0, ddof=1)


    # Env-Specific Metrics

    train_containers_rewards_data_v1 = {}
    train_containers_rewards_means_v1 = {}
    train_containers_rewards_stds_v1 = {}
    train_containers_flags_data_v1 = {}
    train_containers_flags_means_v1 = {}
    train_containers_flags_stds_v1 = {}
    train_containers_steps_data_v1 = {}
    train_containers_steps_means_v1 = {}
    train_containers_steps_stds_v1 = {}
    train_containers_regret_data_v1 = {}
    train_containers_regret_means_v1 = {}
    train_containers_regret_stds_v1 = {}
    train_containers_opt_frac_data_v1 = {}
    train_containers_opt_frac_means_v1 = {}
    train_containers_opt_frac_stds_v1 = {}

    if ips is None or len(ips) == 0:
        ips = list(map(lambda x: x.agent_ip, train_containers_configs))
    if not multi_env:
        ips = []
    for agent_ip in ips:
        rewards_label = agent_ip + "_attacker_avg_episode_rewards"
        flags_label = agent_ip + "_avg_episode_flags"
        steps_label = agent_ip + "_avg_episode_steps"
        regret_label = agent_ip + "_attacker_avg_episode_regrets"
        opt_frac_label = agent_ip + "_attacker_avg_episode_opt_fracs"

        print("ip:{}".format(agent_ip))

        env_train_rewards_data_v1 = list(map(lambda df: df[rewards_label].values[0:max_len], ppo_dfs_v1))
        env_train_rewards_means_v1 = np.mean(tuple(env_train_rewards_data_v1), axis=0)
        env_train_rewards_stds_v1 = np.std(tuple(env_train_rewards_data_v1), axis=0, ddof=1)

        env_train_flags_data_v1 = list(map(lambda df: df[flags_label].values[0:max_len], ppo_dfs_v1))
        env_train_flags_means_v1 = np.mean(tuple(env_train_flags_data_v1), axis=0)
        env_train_flags_stds_v1 = np.std(tuple(env_train_flags_data_v1), axis=0, ddof=1)

        env_train_steps_data_v1 = list(map(lambda df: df[steps_label].values[0:max_len], ppo_dfs_v1))
        env_train_steps_means_v1 = np.mean(tuple(env_train_steps_data_v1), axis=0)
        env_train_steps_stds_v1 = np.std(tuple(env_train_steps_data_v1), axis=0, ddof=1)

        env_train_regret_data_v1 = list(map(lambda df: df[regret_label].values[0:max_len], ppo_dfs_v1))
        env_train_regret_means_v1 = np.mean(tuple(env_train_regret_data_v1), axis=0)
        env_train_regret_stds_v1 = np.std(tuple(env_train_regret_data_v1), axis=0, ddof=1)

        env_train_opt_frac_data_v1 = list(map(lambda df: df[opt_frac_label].values[0:max_len], ppo_dfs_v1))
        env_train_opt_frac_data_v1 = list(
            map(lambda x: np.minimum(np.array([1] * len(x)), x), env_train_opt_frac_data_v1))
        env_train_opt_frac_means_v1 = np.mean(tuple(env_train_opt_frac_data_v1), axis=0)
        env_train_opt_frac_stds_v1 = np.std(tuple(env_train_opt_frac_data_v1), axis=0, ddof=1)

        train_containers_rewards_data_v1[agent_ip] = env_train_rewards_data_v1
        train_containers_rewards_means_v1[agent_ip] = env_train_rewards_means_v1
        train_containers_rewards_stds_v1[agent_ip] = env_train_rewards_stds_v1

        train_containers_flags_data_v1[agent_ip] = env_train_flags_data_v1
        train_containers_flags_means_v1[agent_ip] = env_train_flags_means_v1
        train_containers_flags_stds_v1[agent_ip] = env_train_flags_stds_v1

        train_containers_steps_data_v1[agent_ip] = env_train_steps_data_v1
        train_containers_steps_means_v1[agent_ip] = env_train_steps_means_v1
        train_containers_steps_stds_v1[agent_ip] = env_train_steps_stds_v1

        train_containers_regret_data_v1[agent_ip] = env_train_regret_data_v1
        train_containers_regret_means_v1[agent_ip] = env_train_regret_means_v1
        train_containers_regret_stds_v1[agent_ip] = env_train_regret_stds_v1

        train_containers_opt_frac_data_v1[agent_ip] = env_train_opt_frac_data_v1
        train_containers_opt_frac_means_v1[agent_ip] = env_train_opt_frac_means_v1
        train_containers_opt_frac_stds_v1[agent_ip] = env_train_opt_frac_stds_v1

    eval_2_containers_rewards_data_v1 = {}
    eval_2_containers_rewards_means_v1 = {}
    eval_2_containers_rewards_stds_v1 = {}
    eval_2_containers_flags_data_v1 = {}
    eval_2_containers_flags_means_v1 = {}
    eval_2_containers_flags_stds_v1 = {}
    eval_2_containers_steps_data_v1 = {}
    eval_2_containers_steps_means_v1 = {}
    eval_2_containers_steps_stds_v1 = {}
    eval_2_containers_regret_data_v1 = {}
    eval_2_containers_regret_means_v1 = {}
    eval_2_containers_regret_stds_v1 = {}
    eval_2_containers_opt_frac_data_v1 = {}
    eval_2_containers_opt_frac_means_v1 = {}
    eval_2_containers_opt_frac_stds_v1 = {}

    if eval_ips is None or len(eval_ips) == 0:
        eval_ips = list(map(lambda x: x.agent_ip, eval_containers_configs))
    if not multi_env:
        eval_ips = []
    for agent_ip in eval_ips:
        rewards_label = agent_ip + "_attacker_eval_2_avg_episode_rewards"
        flags_label = agent_ip + "_eval_2_avg_episode_flags"
        steps_label = agent_ip + "_eval_2_avg_episode_steps"
        regrets_label = agent_ip + "_attacker_eval_2_avg_episode_regrets"
        opt_frac_label = agent_ip + "_attacker_eval_2_avg_episode_opt_fracs"

        env_eval_2_rewards_data_v1 = list(map(lambda df: df[rewards_label].values[0:max_len], ppo_dfs_v1))
        env_eval_2_rewards_means_v1 = np.mean(tuple(env_eval_2_rewards_data_v1), axis=0)
        env_eval_2_rewards_stds_v1 = np.std(tuple(env_eval_2_rewards_data_v1), axis=0, ddof=1)

        env_eval_2_flags_data_v1 = list(map(lambda df: df[flags_label].values[0:max_len], ppo_dfs_v1))
        env_eval_2_flags_means_v1 = np.mean(tuple(env_eval_2_flags_data_v1), axis=0)
        env_eval_2_flags_stds_v1 = np.std(tuple(env_eval_2_flags_data_v1), axis=0, ddof=1)

        env_eval_2_steps_data_v1 = list(map(lambda df: df[steps_label].values[0:max_len], ppo_dfs_v1))
        env_eval_2_steps_means_v1 = np.mean(tuple(env_eval_2_steps_data_v1), axis=0)
        env_eval_2_steps_stds_v1 = np.std(tuple(env_eval_2_steps_data_v1), axis=0, ddof=1)

        env_eval_2_regret_data_v1 = list(map(lambda df: df[regrets_label].values[0:max_len], ppo_dfs_v1))
        env_eval_2_regret_means_v1 = np.mean(tuple(env_eval_2_regret_data_v1), axis=0)
        env_eval_2_regret_stds_v1 = np.std(tuple(env_eval_2_regret_data_v1), axis=0, ddof=1)

        env_eval_2_opt_frac_data_v1 = list(map(lambda df: df[opt_frac_label].values[0:max_len], ppo_dfs_v1))
        env_eval_2_opt_frac_data_v1 = list(
            map(lambda x: np.minimum(np.array([1] * len(x)), x), env_eval_2_opt_frac_data_v1))
        env_eval_2_opt_frac_means_v1 = np.mean(tuple(env_eval_2_opt_frac_data_v1), axis=0)
        env_eval_2_opt_frac_stds_v1 = np.std(tuple(env_eval_2_opt_frac_data_v1), axis=0, ddof=1)

        eval_2_containers_rewards_data_v1[agent_ip] = env_eval_2_rewards_data_v1
        eval_2_containers_rewards_means_v1[agent_ip] = env_eval_2_rewards_means_v1
        eval_2_containers_rewards_stds_v1[agent_ip] = env_eval_2_rewards_stds_v1

        eval_2_containers_flags_data_v1[agent_ip] = env_eval_2_flags_data_v1
        eval_2_containers_flags_means_v1[agent_ip] = env_eval_2_flags_means_v1
        eval_2_containers_flags_stds_v1[agent_ip] = env_eval_2_flags_stds_v1

        eval_2_containers_steps_data_v1[agent_ip] = env_eval_2_steps_data_v1
        eval_2_containers_steps_means_v1[agent_ip] = env_eval_2_steps_means_v1
        eval_2_containers_steps_stds_v1[agent_ip] = env_eval_2_steps_stds_v1

        eval_2_containers_regret_data_v1[agent_ip] = env_eval_2_regret_data_v1
        eval_2_containers_regret_means_v1[agent_ip] = env_eval_2_regret_means_v1
        eval_2_containers_regret_stds_v1[agent_ip] = env_eval_2_regret_stds_v1

        eval_2_containers_opt_frac_data_v1[agent_ip] = env_eval_2_opt_frac_data_v1
        eval_2_containers_opt_frac_means_v1[agent_ip] = env_eval_2_opt_frac_means_v1
        eval_2_containers_opt_frac_stds_v1[agent_ip] = env_eval_2_opt_frac_stds_v1

    eval_containers_rewards_data_v1 = {}
    eval_containers_rewards_means_v1 = {}
    eval_containers_rewards_stds_v1 = {}
    eval_containers_flags_data_v1 = {}
    eval_containers_flags_means_v1 = {}
    eval_containers_flags_stds_v1 = {}
    eval_containers_steps_data_v1 = {}
    eval_containers_steps_means_v1 = {}
    eval_containers_steps_stds_v1 = {}
    eval_containers_regret_data_v1 = {}
    eval_containers_regret_means_v1 = {}
    eval_containers_regret_stds_v1 = {}
    eval_containers_opt_frac_data_v1 = {}
    eval_containers_opt_frac_means_v1 = {}
    eval_containers_opt_frac_stds_v1 = {}

    #if eval_ips is None or len(eval_ips) == 0:
    train_ips = list(map(lambda x: x.agent_ip, containers_configs))
    if not multi_env:
        train_ips = []
    for agent_ip in train_ips:
        rewards_label = agent_ip + "_attacker_eval_avg_episode_rewards"
        flags_label = agent_ip + "_eval_avg_episode_flags"
        steps_label = agent_ip + "_eval_avg_episode_steps"
        regrets_label = agent_ip + "_attacker_eval_avg_episode_regrets"
        #opt_frac_label = agent_ip + "_attacker_eval_avg_episode_opt_fracs"

        env_eval_rewards_data_v1 = list(map(lambda df: df[rewards_label].values[0:max_len], ppo_dfs_v1))
        env_eval_rewards_means_v1 = np.mean(tuple(env_eval_rewards_data_v1), axis=0)
        env_eval_rewards_stds_v1 = np.std(tuple(env_eval_rewards_data_v1), axis=0, ddof=1)

        env_eval_flags_data_v1 = list(map(lambda df: df[flags_label].values[0:max_len], ppo_dfs_v1))
        env_eval_flags_means_v1 = np.mean(tuple(env_eval_flags_data_v1), axis=0)
        env_eval_flags_stds_v1 = np.std(tuple(env_eval_flags_data_v1), axis=0, ddof=1)

        env_eval_steps_data_v1 = list(map(lambda df: df[steps_label].values[0:max_len], ppo_dfs_v1))
        env_eval_steps_means_v1 = np.mean(tuple(env_eval_steps_data_v1), axis=0)
        env_eval_steps_stds_v1 = np.std(tuple(env_eval_steps_data_v1), axis=0, ddof=1)

        env_eval_regret_data_v1 = list(map(lambda df: df[regrets_label].values[0:max_len], ppo_dfs_v1))
        env_eval_regret_means_v1 = np.mean(tuple(env_eval_regret_data_v1), axis=0)
        env_eval_regret_stds_v1 = np.std(tuple(env_eval_regret_data_v1), axis=0, ddof=1)

        # env_eval_opt_frac_data_v1 = list(map(lambda df: df[opt_frac_label].values, ppo_dfs_v1))
        # env_eval_opt_frac_data_v1 = list(
        #     map(lambda x: np.minimum(np.array([1] * len(x)), x), env_eval_opt_frac_data_v1))
        # env_eval_opt_frac_means_v1 = np.mean(tuple(env_eval_opt_frac_data_v1), axis=0)
        # env_eval_opt_frac_stds_v1 = np.std(tuple(env_eval_opt_frac_data_v1), axis=0, ddof=1)

        eval_containers_rewards_data_v1[agent_ip] = env_eval_rewards_data_v1
        eval_containers_rewards_means_v1[agent_ip] = env_eval_rewards_means_v1
        eval_containers_rewards_stds_v1[agent_ip] = env_eval_rewards_stds_v1

        eval_containers_flags_data_v1[agent_ip] = env_eval_flags_data_v1
        eval_containers_flags_means_v1[agent_ip] = env_eval_flags_means_v1
        eval_containers_flags_stds_v1[agent_ip] = env_eval_flags_stds_v1

        eval_containers_steps_data_v1[agent_ip] = env_eval_steps_data_v1
        eval_containers_steps_means_v1[agent_ip] = env_eval_steps_means_v1
        eval_containers_steps_stds_v1[agent_ip] = env_eval_steps_stds_v1

        eval_containers_regret_data_v1[agent_ip] = env_eval_regret_data_v1
        eval_containers_regret_means_v1[agent_ip] = env_eval_regret_means_v1
        eval_containers_regret_stds_v1[agent_ip] = env_eval_regret_stds_v1

        # eval_containers_opt_frac_data_v1[agent_ip] = env_eval_opt_frac_data_v1
        # eval_containers_opt_frac_means_v1[agent_ip] = env_eval_opt_frac_means_v1
        # eval_containers_opt_frac_stds_v1[agent_ip] = env_eval_opt_frac_stds_v1


    return avg_train_rewards_data_v1, avg_train_rewards_means_v1, avg_train_rewards_stds_v1, avg_train_steps_data_v1, \
           avg_train_steps_means_v1, avg_train_steps_stds_v1, avg_train_regret_data_v1, avg_train_regret_means_v1, \
           avg_train_regret_stds_v1, avg_train_opt_frac_data_v1, avg_train_opt_frac_means_v1, \
           avg_train_opt_frac_stds_v1, avg_train_caught_frac_data_v1, avg_train_caught_frac_means_v1, \
           avg_train_caught_frac_stds_v1, avg_train_early_stopping_frac_data_v1, avg_train_early_stopping_means_v1, \
           avg_train_early_stopping_stds_v1, avg_train_intrusion_frac_data_v1, avg_train_intrusion_means_v1, \
           avg_train_intrusion_stds_v1, avg_eval_rewards_data_v1, avg_eval_rewards_means_v1, avg_eval_rewards_stds_v1, \
           avg_eval_steps_data_v1, avg_eval_steps_means_v1, avg_eval_steps_stds_v1, avg_eval_regret_data_v1, \
           avg_eval_regret_means_v1, avg_eval_regret_stds_v1, avg_eval_opt_frac_data_v1, avg_eval_opt_frac_means_v1, \
           avg_eval_opt_frac_stds_v1, avg_eval_caught_frac_data_v1, avg_eval_caught_frac_means_v1, \
           avg_eval_caught_frac_stds_v1, avg_eval_early_stopping_frac_data_v1, avg_eval_early_stopping_means_v1, \
           avg_eval_early_stopping_stds_v1,  avg_eval_intrusion_frac_data_v1, avg_eval_intrusion_means_v1, \
           avg_eval_intrusion_stds_v1, \
           avg_eval_2_rewards_data_v1, avg_eval_2_rewards_means_v1, avg_eval_2_rewards_stds_v1, \
           avg_eval_2_steps_data_v1, avg_eval_2_steps_means_v1, avg_eval_2_steps_stds_v1, \
           avg_eval_2_caught_frac_data_v1, avg_eval_2_caught_frac_means_v1, \
           avg_eval_2_caught_frac_stds_v1, avg_eval_2_early_stopping_frac_data_v1, avg_eval_2_early_stopping_means_v1, \
           avg_eval_2_early_stopping_stds_v1,  avg_eval_2_intrusion_frac_data_v1, avg_eval_2_intrusion_means_v1, \
           avg_eval_2_intrusion_stds_v1,\
           avg_eval_2_regret_data_v1, avg_eval_2_regret_means_v1, \
           avg_eval_2_regret_stds_v1, avg_eval_2_opt_frac_data_v1, avg_eval_2_opt_frac_means_v1, \
           avg_eval_2_opt_frac_stds_v1, \
           avg_train_attacker_action_alerts_data_v1, avg_train_attacker_action_alerts_means_v1, \
           avg_train_attacker_action_alerts_stds_v1, \
           avg_eval_attacker_action_alerts_data_v1, avg_eval_attacker_action_alerts_means_v1, \
           avg_eval_attacker_action_alerts_stds_v1, avg_eval_2_attacker_action_alerts_data_v1, \
           avg_eval_2_attacker_action_alerts_means_v1, avg_eval_2_attacker_action_alerts_stds_v1, \
           avg_train_attacker_action_costs_data_v1, avg_train_attacker_action_costs_means_v1, \
           avg_train_attacker_action_costs_stds_v1, \
           avg_eval_attacker_action_costs_data_v1, avg_eval_attacker_action_costs_means_v1, \
           avg_eval_attacker_action_costs_stds_v1, avg_eval_2_attacker_action_costs_data_v1, \
           avg_eval_2_attacker_action_costs_means_v1, avg_eval_2_attacker_action_costs_stds_v1, \
           avg_train_flags_data_v1, avg_train_flags_means_v1, avg_train_flags_stds_v1, \
           avg_eval_flags_data_v1, avg_eval_flags_means_v1, avg_eval_flags_stds_v1, \
           avg_eval_2_flags_data_v1, avg_eval_2_flags_means_v1, avg_eval_2_flags_stds_v1, \
           train_containers_rewards_data_v1, train_containers_rewards_means_v1, train_containers_rewards_stds_v1, \
           train_containers_flags_data_v1, train_containers_flags_means_v1, train_containers_flags_stds_v1, train_containers_steps_data_v1, \
           train_containers_steps_means_v1, train_containers_steps_stds_v1, train_containers_regret_data_v1, train_containers_regret_means_v1, \
           train_containers_regret_stds_v1, train_containers_opt_frac_data_v1, train_containers_opt_frac_means_v1, train_containers_opt_frac_stds_v1, \
           eval_2_containers_rewards_data_v1, eval_2_containers_rewards_means_v1, eval_2_containers_rewards_stds_v1, \
           eval_2_containers_flags_data_v1, eval_2_containers_flags_means_v1, eval_2_containers_flags_stds_v1, eval_2_containers_steps_data_v1, \
           eval_2_containers_steps_means_v1, eval_2_containers_steps_stds_v1, eval_2_containers_regret_data_v1, eval_2_containers_regret_means_v1, \
           eval_2_containers_regret_stds_v1, eval_2_containers_opt_frac_data_v1, eval_2_containers_opt_frac_means_v1, eval_2_containers_opt_frac_stds_v1, \
           eval_containers_rewards_data_v1, eval_containers_rewards_means_v1, eval_containers_rewards_stds_v1, \
           eval_containers_flags_data_v1, eval_containers_flags_means_v1, eval_containers_flags_stds_v1, eval_containers_steps_data_v1, \
           eval_containers_steps_means_v1, eval_containers_steps_stds_v1, eval_containers_regret_data_v1, eval_containers_regret_means_v1, \
           eval_containers_regret_stds_v1

def plot_train(avg_train_rewards_data_v1_20, avg_train_rewards_means_v1_20, avg_train_rewards_stds_v1_20, avg_train_steps_data_v1_20,
    avg_train_steps_means_v1_20, avg_train_steps_stds_v1_20, avg_train_regret_data_v1_20, avg_train_regret_means_v1_20,
    avg_train_regret_stds_v1_20, avg_train_opt_frac_data_v1_20, avg_train_opt_frac_means_v1_20,
    avg_train_opt_frac_stds_v1_20, avg_train_caught_frac_data_v1_20, avg_train_caught_frac_means_v1_20,
    avg_train_caught_frac_stds_v1_20, avg_train_early_stopping_frac_data_v1_20, avg_train_early_stopping_means_v1_20,
    avg_train_early_stopping_stds_v1_20, avg_train_intrusion_frac_data_v1_20, avg_train_intrusion_means_v1_20,
    avg_train_intrusion_stds_v1_20, avg_eval_rewards_data_v1_20, avg_eval_rewards_means_v1_20, avg_eval_rewards_stds_v1_20,
    avg_eval_steps_data_v1_20, avg_eval_steps_means_v1_20, avg_eval_steps_stds_v1_20, avg_eval_regret_data_v1_20,
    avg_eval_regret_means_v1_20, avg_eval_regret_stds_v1_20, avg_eval_opt_frac_data_v1_20, avg_eval_opt_frac_means_v1_20,
    avg_eval_opt_frac_stds_v1_20, avg_eval_caught_frac_data_v1_20, avg_eval_caught_frac_means_v1_20,
    avg_eval_caught_frac_stds_v1_20, avg_eval_early_stopping_frac_data_v1_20, avg_eval_early_stopping_means_v1_20,
    avg_eval_early_stopping_stds_v1_20, avg_eval_intrusion_frac_data_v1_20, avg_eval_intrusion_means_v1_20,
    avg_eval_intrusion_stds_v1_20, avg_eval_2_rewards_data_v1_20, avg_eval_2_rewards_means_v1_20, avg_eval_2_rewards_stds_v1_20,
    avg_eval_2_steps_data_v1_20, avg_eval_2_steps_means_v1_20, avg_eval_2_steps_stds_v1_20,
    avg_eval_2_caught_frac_data_v1_20, avg_eval_2_caught_frac_means_v1_20,
    avg_eval_2_caught_frac_stds_v1_20, avg_eval_2_early_stopping_frac_data_v1_20, avg_eval_2_early_stopping_means_v1_20,
    avg_eval_2_early_stopping_stds_v1_20,  avg_eval_2_intrusion_frac_data_v1_20, avg_eval_2_intrusion_means_v1_20,
    avg_eval_2_intrusion_stds_v1_20, avg_eval_2_regret_data_v1_20, avg_eval_2_regret_means_v1_20,  avg_eval_2_regret_stds_v1_20,
    avg_eval_2_opt_frac_data_v1_20, avg_eval_2_opt_frac_means_v1_20, avg_eval_2_opt_frac_stds_v1_20,
    avg_train_attacker_action_alerts_data_v1_20, avg_train_attacker_action_alerts_means_v1_20,
    avg_train_attacker_action_alerts_stds_v1_20, avg_eval_attacker_action_alerts_data_v1_20,
    avg_eval_attacker_action_alerts_means_v1_20,
    avg_eval_attacker_action_alerts_stds_v1_20, avg_eval_2_attacker_action_alerts_data_v1_20,
    avg_eval_2_attacker_action_alerts_means_v1_20, avg_eval_2_attacker_action_alerts_stds_v1_20,
    avg_train_attacker_action_costs_data_v1_20, avg_train_attacker_action_costs_means_v1_20,
    avg_train_attacker_action_costs_stds_v1_20,
    avg_eval_attacker_action_costs_data_v1_20, avg_eval_attacker_action_costs_means_v1_20,
    avg_eval_attacker_action_costs_stds_v1_20, avg_eval_2_attacker_action_costs_data_v1_20,
    avg_eval_2_attacker_action_costs_means_v1_20, avg_eval_2_attacker_action_costs_stds_v1_20,
    avg_train_flags_data_v1_20, avg_train_flags_means_v1_20, avg_train_flags_stds_v1_20,
    avg_eval_flags_data_v1_20, avg_eval_flags_means_v1_20, avg_eval_flags_stds_v1_20,
    avg_eval_2_flags_data_v1_20, avg_eval_2_flags_means_v1_20, avg_eval_2_flags_stds_v1_20,
    train_containers_rewards_data_v1_20, train_containers_rewards_means_v1_20, train_containers_rewards_stds_v1_20,
    train_containers_flags_data_v1_20, train_containers_flags_means_v1_20, train_containers_flags_stds_v1_20, train_containers_steps_data_v1_20,
    train_containers_steps_means_v1_20, train_containers_steps_stds_v1_20, train_containers_regret_data_v1_20, train_containers_regret_means_v1_20,
    train_containers_regret_stds_v1_20, train_containers_opt_frac_data_v1_20, train_containers_opt_frac_means_v1_20, train_containers_opt_frac_stds_v1_20,
    eval_2_containers_rewards_data_v1_20, eval_2_containers_rewards_means_v1_20, eval_2_containers_rewards_stds_v1_20,
    eval_2_containers_flags_data_v1_20, eval_2_containers_flags_means_v1_20, eval_2_containers_flags_stds_v1_20, eval_2_containers_steps_data_v1_20,
    eval_2_containers_steps_means_v1_20, eval_2_containers_steps_stds_v1_20, eval_2_containers_regret_data_v1_20, eval_2_containers_regret_means_v1_20,
    eval_2_containers_regret_stds_v1_20, eval_2_containers_opt_frac_data_v1_20, eval_2_containers_opt_frac_means_v1_20, eval_2_containers_opt_frac_stds_v1_20,
    eval_containers_rewards_data_v1_20, eval_containers_rewards_means_v1_20, eval_containers_rewards_stds_v1_20,
    eval_containers_flags_data_v1_20, eval_containers_flags_means_v1_20, eval_containers_flags_stds_v1_20, eval_containers_steps_data_v1_20,
    eval_containers_steps_means_v1_20, eval_containers_steps_stds_v1_20, eval_containers_regret_data_v1_20, eval_containers_regret_means_v1_20,
    eval_containers_regret_stds_v1_20,
    avg_train_rewards_data_v1_1, avg_train_rewards_means_v1_1, avg_train_rewards_stds_v1_1, avg_train_steps_data_v1_1,
    avg_train_steps_means_v1_1, avg_train_steps_stds_v1_1, avg_train_regret_data_v1_1, avg_train_regret_means_v1_1,
    avg_train_regret_stds_v1_1, avg_train_opt_frac_data_v1_1, avg_train_opt_frac_means_v1_1,
    avg_train_opt_frac_stds_v1_1, avg_train_caught_frac_data_v1_1, avg_train_caught_frac_means_v1_1,
    avg_train_caught_frac_stds_v1_1, avg_train_early_stopping_frac_data_v1_1, avg_train_early_stopping_means_v1_1,
    avg_train_early_stopping_stds_v1_1, avg_train_intrusion_frac_data_v1_1, avg_train_intrusion_means_v1_1,
    avg_train_intrusion_stds_v1_1, avg_eval_rewards_data_v1_1, avg_eval_rewards_means_v1_1, avg_eval_rewards_stds_v1_1,
    avg_eval_steps_data_v1_1, avg_eval_steps_means_v1_1, avg_eval_steps_stds_v1_1, avg_eval_regret_data_v1_1,
    avg_eval_regret_means_v1_1, avg_eval_regret_stds_v1_1, avg_eval_opt_frac_data_v1_1, avg_eval_opt_frac_means_v1_1,
    avg_eval_opt_frac_stds_v1_1, avg_eval_caught_frac_data_v1_1, avg_eval_caught_frac_means_v1_1,
    avg_eval_caught_frac_stds_v1_1, avg_eval_early_stopping_frac_data_v1_1, avg_eval_early_stopping_means_v1_1,
    avg_eval_early_stopping_stds_v1_1, avg_eval_intrusion_frac_data_v1_1, avg_eval_intrusion_means_v1_1,
    avg_eval_intrusion_stds_v1_1, avg_eval_2_rewards_data_v1_1, avg_eval_2_rewards_means_v1_1, avg_eval_2_rewards_stds_v1_1,
    avg_eval_2_steps_data_v1_1, avg_eval_2_steps_means_v1_1, avg_eval_2_steps_stds_v1_1,
    avg_eval_2_caught_frac_data_v1_1, avg_eval_2_caught_frac_means_v1_1,
    avg_eval_2_caught_frac_stds_v1_1, avg_eval_2_early_stopping_frac_data_v1_1, avg_eval_2_early_stopping_means_v1_1,
    avg_eval_2_early_stopping_stds_v1_1,  avg_eval_2_intrusion_frac_data_v1_1, avg_eval_2_intrusion_means_v1_1,
    avg_eval_2_intrusion_stds_v1_1, avg_eval_2_regret_data_v1_1, avg_eval_2_regret_means_v1_1,  avg_eval_2_regret_stds_v1_1,
    avg_eval_2_opt_frac_data_v1_1, avg_eval_2_opt_frac_means_v1_1, avg_eval_2_opt_frac_stds_v1_1,
    avg_train_attacker_action_alerts_data_v1_1, avg_train_attacker_action_alerts_means_v1_1,
    avg_train_attacker_action_alerts_stds_v1_1, avg_eval_attacker_action_alerts_data_v1_1,
    avg_eval_attacker_action_alerts_means_v1_1,
    avg_eval_attacker_action_alerts_stds_v1_1, avg_eval_2_attacker_action_alerts_data_v1_1,
    avg_eval_2_attacker_action_alerts_means_v1_1, avg_eval_2_attacker_action_alerts_stds_v1_1,
    avg_train_attacker_action_costs_data_v1_1, avg_train_attacker_action_costs_means_v1_1,
    avg_train_attacker_action_costs_stds_v1_1,
    avg_eval_attacker_action_costs_data_v1_1, avg_eval_attacker_action_costs_means_v1_1,
    avg_eval_attacker_action_costs_stds_v1_1, avg_eval_2_attacker_action_costs_data_v1_1,
    avg_eval_2_attacker_action_costs_means_v1_1, avg_eval_2_attacker_action_costs_stds_v1_1,
    avg_train_flags_data_v1_1, avg_train_flags_means_v1_1, avg_train_flags_stds_v1_1,
    avg_eval_flags_data_v1_1, avg_eval_flags_means_v1_1, avg_eval_flags_stds_v1_1,
    avg_eval_2_flags_data_v1_1, avg_eval_2_flags_means_v1_1, avg_eval_2_flags_stds_v1_1,
    train_containers_rewards_data_v1_1, train_containers_rewards_means_v1_1, train_containers_rewards_stds_v1_1,
    train_containers_flags_data_v1_1, train_containers_flags_means_v1_1, train_containers_flags_stds_v1_1, train_containers_steps_data_v1_1,
    train_containers_steps_means_v1_1, train_containers_steps_stds_v1_1, train_containers_regret_data_v1_1, train_containers_regret_means_v1_1,
    train_containers_regret_stds_v1_1, train_containers_opt_frac_data_v1_1, train_containers_opt_frac_means_v1_1, train_containers_opt_frac_stds_v1_1,
    eval_2_containers_rewards_data_v1_1, eval_2_containers_rewards_means_v1_1, eval_2_containers_rewards_stds_v1_1,
    eval_2_containers_flags_data_v1_1, eval_2_containers_flags_means_v1_1, eval_2_containers_flags_stds_v1_1, eval_2_containers_steps_data_v1_1,
    eval_2_containers_steps_means_v1_1, eval_2_containers_steps_stds_v1_1, eval_2_containers_regret_data_v1_1, eval_2_containers_regret_means_v1_1,
    eval_2_containers_regret_stds_v1_1, eval_2_containers_opt_frac_data_v1_1, eval_2_containers_opt_frac_means_v1_1, eval_2_containers_opt_frac_stds_v1_1,
    eval_containers_rewards_data_v1_1, eval_containers_rewards_means_v1_1, eval_containers_rewards_stds_v1_1,
    eval_containers_flags_data_v1_1, eval_containers_flags_means_v1_1, eval_containers_flags_stds_v1_1, eval_containers_steps_data_v1_1,
    eval_containers_steps_means_v1_1, eval_containers_steps_stds_v1_1, eval_containers_regret_data_v1_1, eval_containers_regret_means_v1_1,
    eval_containers_regret_stds_v1_1,
    avg_train_rewards_data_v1_20_dr, avg_train_rewards_means_v1_20_dr, avg_train_rewards_stds_v1_20_dr, avg_train_steps_data_v1_20_dr,
    avg_train_steps_means_v1_20_dr, avg_train_steps_stds_v1_20_dr, avg_train_regret_data_v1_20_dr, avg_train_regret_means_v1_20_dr,
    avg_train_regret_stds_v1_20_dr, avg_train_opt_frac_data_v1_20_dr, avg_train_opt_frac_means_v1_20_dr,
    avg_train_opt_frac_stds_v1_20_dr, avg_train_caught_frac_data_v1_20_dr, avg_train_caught_frac_means_v1_20_dr,
    avg_train_caught_frac_stds_v1_20_dr, avg_train_early_stopping_frac_data_v1_20_dr, avg_train_early_stopping_means_v1_20_dr,
    avg_train_early_stopping_stds_v1_20_dr, avg_train_intrusion_frac_data_v1_20_dr, avg_train_intrusion_means_v1_20_dr,
    avg_train_intrusion_stds_v1_20_dr, avg_eval_rewards_data_v1_20_dr, avg_eval_rewards_means_v1_20_dr, avg_eval_rewards_stds_v1_20_dr,
    avg_eval_steps_data_v1_20_dr, avg_eval_steps_means_v1_20_dr, avg_eval_steps_stds_v1_20_dr, avg_eval_regret_data_v1_20_dr,
    avg_eval_regret_means_v1_20_dr, avg_eval_regret_stds_v1_20_dr, avg_eval_opt_frac_data_v1_20_dr, avg_eval_opt_frac_means_v1_20_dr,
    avg_eval_opt_frac_stds_v1_20_dr, avg_eval_caught_frac_data_v1_20_dr, avg_eval_caught_frac_means_v1_20_dr,
    avg_eval_caught_frac_stds_v1_20_dr, avg_eval_early_stopping_frac_data_v1_20_dr, avg_eval_early_stopping_means_v1_20_dr,
    avg_eval_early_stopping_stds_v1_20_dr, avg_eval_intrusion_frac_data_v1_20_dr, avg_eval_intrusion_means_v1_20_dr,
    avg_eval_intrusion_stds_v1_20_dr, avg_eval_2_rewards_data_v1_20_dr, avg_eval_2_rewards_means_v1_20_dr, avg_eval_2_rewards_stds_v1_20_dr,
    avg_eval_2_steps_data_v1_20_dr, avg_eval_2_steps_means_v1_20_dr, avg_eval_2_steps_stds_v1_20_dr,
    avg_eval_2_caught_frac_data_v1_20_dr, avg_eval_2_caught_frac_means_v1_20_dr,
    avg_eval_2_caught_frac_stds_v1_20_dr, avg_eval_2_early_stopping_frac_data_v1_20_dr, avg_eval_2_early_stopping_means_v1_20_dr,
    avg_eval_2_early_stopping_stds_v1_20_dr,  avg_eval_2_intrusion_frac_data_v1_20_dr, avg_eval_2_intrusion_means_v1_20_dr,
    avg_eval_2_intrusion_stds_v1_20_dr, avg_eval_2_regret_data_v1_20_dr, avg_eval_2_regret_means_v1_20_dr,  avg_eval_2_regret_stds_v1_20_dr,
    avg_eval_2_opt_frac_data_v1_20_dr, avg_eval_2_opt_frac_means_v1_20_dr, avg_eval_2_opt_frac_stds_v1_20_dr,
    avg_train_attacker_action_alerts_data_v1_20_dr, avg_train_attacker_action_alerts_means_v1_20_dr,
    avg_train_attacker_action_alerts_stds_v1_20_dr, avg_eval_attacker_action_alerts_data_v1_20_dr,
    avg_eval_attacker_action_alerts_means_v1_20_dr,
    avg_eval_attacker_action_alerts_stds_v1_20_dr, avg_eval_2_attacker_action_alerts_data_v1_20_dr,
    avg_eval_2_attacker_action_alerts_means_v1_20_dr, avg_eval_2_attacker_action_alerts_stds_v1_20_dr,
    avg_train_attacker_action_costs_data_v1_20_dr, avg_train_attacker_action_costs_means_v1_20_dr,
    avg_train_attacker_action_costs_stds_v1_20_dr,
    avg_eval_attacker_action_costs_data_v1_20_dr, avg_eval_attacker_action_costs_means_v1_20_dr,
    avg_eval_attacker_action_costs_stds_v1_20_dr, avg_eval_2_attacker_action_costs_data_v1_20_dr,
    avg_eval_2_attacker_action_costs_means_v1_20_dr, avg_eval_2_attacker_action_costs_stds_v1_20_dr,
    avg_train_flags_data_v1_20_dr, avg_train_flags_means_v1_20_dr, avg_train_flags_stds_v1_20_dr,
    avg_eval_flags_data_v1_20_dr, avg_eval_flags_means_v1_20_dr, avg_eval_flags_stds_v1_20_dr,
    avg_eval_2_flags_data_v1_20_dr, avg_eval_2_flags_means_v1_20_dr, avg_eval_2_flags_stds_v1_20_dr,
    train_containers_rewards_data_v1_20_dr, train_containers_rewards_means_v1_20_dr, train_containers_rewards_stds_v1_20_dr,
    train_containers_flags_data_v1_20_dr, train_containers_flags_means_v1_20_dr, train_containers_flags_stds_v1_20_dr, train_containers_steps_data_v1_20_dr,
    train_containers_steps_means_v1_20_dr, train_containers_steps_stds_v1_20_dr, train_containers_regret_data_v1_20_dr, train_containers_regret_means_v1_20_dr,
    train_containers_regret_stds_v1_20_dr, train_containers_opt_frac_data_v1_20_dr, train_containers_opt_frac_means_v1_20_dr, train_containers_opt_frac_stds_v1_20_dr,
    eval_2_containers_rewards_data_v1_20_dr, eval_2_containers_rewards_means_v1_20_dr, eval_2_containers_rewards_stds_v1_20_dr,
    eval_2_containers_flags_data_v1_20_dr, eval_2_containers_flags_means_v1_20_dr, eval_2_containers_flags_stds_v1_20_dr, eval_2_containers_steps_data_v1_20_dr,
    eval_2_containers_steps_means_v1_20_dr, eval_2_containers_steps_stds_v1_20_dr, eval_2_containers_regret_data_v1_20_dr, eval_2_containers_regret_means_v1_20_dr,
    eval_2_containers_regret_stds_v1_20_dr, eval_2_containers_opt_frac_data_v1_20_dr, eval_2_containers_opt_frac_means_v1_20_dr, eval_2_containers_opt_frac_stds_v1_20_dr,
    eval_containers_rewards_data_v1_20_dr, eval_containers_rewards_means_v1_20_dr, eval_containers_rewards_stds_v1_20_dr,
    eval_containers_flags_data_v1_20_dr, eval_containers_flags_means_v1_20_dr, eval_containers_flags_stds_v1_20_dr, eval_containers_steps_data_v1_20_dr,
    eval_containers_steps_means_v1_20_dr, eval_containers_steps_stds_v1_20_dr, eval_containers_regret_data_v1_20_dr, eval_containers_regret_means_v1_20_dr,
    eval_containers_regret_stds_v1_20_dr
               ):

    print("plot")
    suffix = "gensim"
    ylim_rew = (10, 100)
    max_iter = 550

    plotting_util_mult_envs.plot_rew_det_fl_al_many(
        avg_eval_rewards_data_v1_20[0:max_iter], avg_eval_rewards_means_v1_20[0:max_iter],
        avg_eval_rewards_stds_v1_20[0:max_iter],
        avg_eval_2_rewards_data_v1_20[0:max_iter], avg_eval_2_rewards_means_v1_20[0:max_iter],
        avg_eval_2_rewards_stds_v1_20[0:max_iter],
        avg_train_rewards_data_v1_20[0:max_iter], avg_train_rewards_means_v1_20[0:max_iter],
        avg_train_rewards_stds_v1_20[0:max_iter],
        avg_eval_caught_frac_data_v1_20[0:max_iter], avg_eval_caught_frac_means_v1_20[0:max_iter],
        avg_eval_caught_frac_stds_v1_20[0:max_iter],
        avg_eval_intrusion_frac_data_v1_20[0:max_iter], avg_eval_intrusion_means_v1_20[0:max_iter],
        avg_eval_intrusion_stds_v1_20[0:max_iter],
        avg_eval_2_caught_frac_data_v1_20[0:max_iter], avg_eval_2_caught_frac_means_v1_20[0:max_iter],
        avg_eval_2_caught_frac_stds_v1_20[0:max_iter],
        avg_eval_2_intrusion_frac_data_v1_20[0:max_iter], avg_eval_2_intrusion_means_v1_20[0:max_iter],
        avg_eval_2_intrusion_stds_v1_20[0:max_iter],
        avg_train_caught_frac_data_v1_20[0:max_iter], avg_train_caught_frac_means_v1_20[0:max_iter],
        avg_train_caught_frac_stds_v1_20[0:max_iter],
        avg_train_intrusion_frac_data_v1_20[0:max_iter], avg_train_intrusion_means_v1_20[0:max_iter],
        avg_train_intrusion_stds_v1_20[0:max_iter],
        avg_eval_flags_data_v1_20[0:max_iter], avg_eval_flags_means_v1_20[0:max_iter],
        avg_eval_flags_stds_v1_20[0:max_iter],
        avg_eval_2_flags_data_v1_20[0:max_iter], avg_eval_2_flags_means_v1_20[0:max_iter],
        avg_eval_2_flags_stds_v1_20[0:max_iter],
        avg_train_flags_data_v1_20[0:max_iter], avg_train_flags_means_v1_20[0:max_iter],
        avg_train_flags_stds_v1_20[0:max_iter],
        avg_eval_attacker_action_costs_data_v1_20[0:max_iter], avg_eval_attacker_action_costs_means_v1_20[0:max_iter],
        avg_eval_attacker_action_costs_stds_v1_20[0:max_iter],
        avg_eval_2_attacker_action_costs_data_v1_20[0:max_iter],
        avg_eval_2_attacker_action_costs_means_v1_20[0:max_iter],
        avg_eval_2_attacker_action_costs_stds_v1_20[0:max_iter],
        avg_train_attacker_action_costs_data_v1_20[0:max_iter],
        avg_train_attacker_action_costs_means_v1_20[0:max_iter],
        avg_train_attacker_action_costs_stds_v1_20[0:max_iter],
        avg_eval_attacker_action_alerts_data_v1_20[0:max_iter], avg_eval_attacker_action_alerts_means_v1_20[0:max_iter],
        avg_eval_attacker_action_alerts_stds_v1_20[0:max_iter],
        avg_eval_2_attacker_action_alerts_data_v1_20[0:max_iter],
        avg_eval_2_attacker_action_alerts_means_v1_20[0:max_iter],
        avg_eval_2_attacker_action_alerts_stds_v1_20[0:max_iter],
        avg_train_attacker_action_alerts_data_v1_20[0:max_iter],
        avg_train_attacker_action_alerts_means_v1_20[0:max_iter],
        avg_train_attacker_action_alerts_stds_v1_20[0:max_iter],
        avg_eval_steps_data_v1_20[0:max_iter], avg_eval_steps_means_v1_20[0:max_iter],
        avg_eval_steps_stds_v1_20[0:max_iter],
        avg_eval_2_steps_data_v1_20[0:max_iter], avg_eval_2_steps_means_v1_20[0:max_iter],
        avg_eval_2_steps_stds_v1_20[0:max_iter],
        avg_train_steps_data_v1_20[0:max_iter], avg_train_steps_means_v1_20[0:max_iter],
        avg_train_steps_stds_v1_20[0:max_iter],
        avg_eval_rewards_data_v1_1[0:max_iter], avg_eval_rewards_means_v1_1[0:max_iter],
        avg_eval_rewards_stds_v1_1[0:max_iter],
        avg_eval_2_rewards_data_v1_1[0:max_iter], avg_eval_2_rewards_means_v1_1[0:max_iter],
        avg_eval_2_rewards_stds_v1_1[0:max_iter],
        avg_train_rewards_data_v1_1[0:max_iter], avg_train_rewards_means_v1_1[0:max_iter],
        avg_train_rewards_stds_v1_1[0:max_iter],
        avg_eval_caught_frac_data_v1_1[0:max_iter], avg_eval_caught_frac_means_v1_1[0:max_iter],
        avg_eval_caught_frac_stds_v1_1[0:max_iter],
        avg_eval_intrusion_frac_data_v1_1[0:max_iter], avg_eval_intrusion_means_v1_1[0:max_iter],
        avg_eval_intrusion_stds_v1_1[0:max_iter],
        avg_eval_2_caught_frac_data_v1_1[0:max_iter], avg_eval_2_caught_frac_means_v1_1[0:max_iter],
        avg_eval_2_caught_frac_stds_v1_1[0:max_iter],
        avg_eval_2_intrusion_frac_data_v1_1[0:max_iter], avg_eval_2_intrusion_means_v1_1[0:max_iter],
        avg_eval_2_intrusion_stds_v1_1[0:max_iter],
        avg_train_caught_frac_data_v1_1[0:max_iter], avg_train_caught_frac_means_v1_1[0:max_iter],
        avg_train_caught_frac_stds_v1_1[0:max_iter],
        avg_train_intrusion_frac_data_v1_1[0:max_iter], avg_train_intrusion_means_v1_1[0:max_iter],
        avg_train_intrusion_stds_v1_1[0:max_iter],
        avg_eval_flags_data_v1_1[0:max_iter], avg_eval_flags_means_v1_1[0:max_iter],
        avg_eval_flags_stds_v1_1[0:max_iter],
        avg_eval_2_flags_data_v1_1[0:max_iter], avg_eval_2_flags_means_v1_1[0:max_iter],
        avg_eval_2_flags_stds_v1_1[0:max_iter],
        avg_train_flags_data_v1_1[0:max_iter], avg_train_flags_means_v1_1[0:max_iter],
        avg_train_flags_stds_v1_1[0:max_iter],
        avg_eval_attacker_action_costs_data_v1_1[0:max_iter], avg_eval_attacker_action_costs_means_v1_1[0:max_iter],
        avg_eval_attacker_action_costs_stds_v1_1[0:max_iter],
        avg_eval_2_attacker_action_costs_data_v1_1[0:max_iter],
        avg_eval_2_attacker_action_costs_means_v1_1[0:max_iter],
        avg_eval_2_attacker_action_costs_stds_v1_1[0:max_iter],
        avg_train_attacker_action_costs_data_v1_1[0:max_iter],
        avg_train_attacker_action_costs_means_v1_1[0:max_iter],
        avg_train_attacker_action_costs_stds_v1_1[0:max_iter],
        avg_eval_attacker_action_alerts_data_v1_1[0:max_iter], avg_eval_attacker_action_alerts_means_v1_1[0:max_iter],
        avg_eval_attacker_action_alerts_stds_v1_1[0:max_iter],
        avg_eval_2_attacker_action_alerts_data_v1_1[0:max_iter],
        avg_eval_2_attacker_action_alerts_means_v1_1[0:max_iter],
        avg_eval_2_attacker_action_alerts_stds_v1_1[0:max_iter],
        avg_train_attacker_action_alerts_data_v1_1[0:max_iter],
        avg_train_attacker_action_alerts_means_v1_1[0:max_iter],
        avg_train_attacker_action_alerts_stds_v1_1[0:max_iter],
        avg_eval_steps_data_v1_1[0:max_iter], avg_eval_steps_means_v1_1[0:max_iter],
        avg_eval_steps_stds_v1_1[0:max_iter],
        avg_eval_2_steps_data_v1_1[0:max_iter], avg_eval_2_steps_means_v1_1[0:max_iter],
        avg_eval_2_steps_stds_v1_1[0:max_iter],
        avg_train_steps_data_v1_1[0:max_iter], avg_train_steps_means_v1_1[0:max_iter],
        avg_train_steps_stds_v1_1[0:max_iter],
        avg_eval_rewards_data_v1_20_dr[0:max_iter], avg_eval_rewards_means_v1_20_dr[0:max_iter],
        avg_eval_rewards_stds_v1_20_dr[0:max_iter],
        avg_eval_2_rewards_data_v1_20_dr[0:max_iter], avg_eval_2_rewards_means_v1_20_dr[0:max_iter],
        avg_eval_2_rewards_stds_v1_20_dr[0:max_iter],
        avg_train_rewards_data_v1_20_dr[0:max_iter], avg_train_rewards_means_v1_20_dr[0:max_iter],
        avg_train_rewards_stds_v1_20_dr[0:max_iter],
        avg_eval_caught_frac_data_v1_20_dr[0:max_iter], avg_eval_caught_frac_means_v1_20_dr[0:max_iter],
        avg_eval_caught_frac_stds_v1_20_dr[0:max_iter],
        avg_eval_intrusion_frac_data_v1_20_dr[0:max_iter], avg_eval_intrusion_means_v1_20_dr[0:max_iter],
        avg_eval_intrusion_stds_v1_20_dr[0:max_iter],
        avg_eval_2_caught_frac_data_v1_20_dr[0:max_iter], avg_eval_2_caught_frac_means_v1_20_dr[0:max_iter],
        avg_eval_2_caught_frac_stds_v1_20_dr[0:max_iter],
        avg_eval_2_intrusion_frac_data_v1_20_dr[0:max_iter], avg_eval_2_intrusion_means_v1_20_dr[0:max_iter],
        avg_eval_2_intrusion_stds_v1_20_dr[0:max_iter],
        avg_train_caught_frac_data_v1_20_dr[0:max_iter], avg_train_caught_frac_means_v1_20_dr[0:max_iter],
        avg_train_caught_frac_stds_v1_20_dr[0:max_iter],
        avg_train_intrusion_frac_data_v1_20_dr[0:max_iter], avg_train_intrusion_means_v1_20_dr[0:max_iter],
        avg_train_intrusion_stds_v1_20_dr[0:max_iter],
        avg_eval_flags_data_v1_20_dr[0:max_iter], avg_eval_flags_means_v1_20_dr[0:max_iter],
        avg_eval_flags_stds_v1_20_dr[0:max_iter],
        avg_eval_2_flags_data_v1_20_dr[0:max_iter], avg_eval_2_flags_means_v1_20_dr[0:max_iter],
        avg_eval_2_flags_stds_v1_20_dr[0:max_iter],
        avg_train_flags_data_v1_20_dr[0:max_iter], avg_train_flags_means_v1_20_dr[0:max_iter],
        avg_train_flags_stds_v1_20_dr[0:max_iter],
        avg_eval_attacker_action_costs_data_v1_20_dr[0:max_iter], avg_eval_attacker_action_costs_means_v1_20_dr[0:max_iter],
        avg_eval_attacker_action_costs_stds_v1_20_dr[0:max_iter],
        avg_eval_2_attacker_action_costs_data_v1_20_dr[0:max_iter],
        avg_eval_2_attacker_action_costs_means_v1_20_dr[0:max_iter],
        avg_eval_2_attacker_action_costs_stds_v1_20_dr[0:max_iter],
        avg_train_attacker_action_costs_data_v1_20_dr[0:max_iter],
        avg_train_attacker_action_costs_means_v1_20_dr[0:max_iter],
        avg_train_attacker_action_costs_stds_v1_20_dr[0:max_iter],
        avg_eval_attacker_action_alerts_data_v1_20_dr[0:max_iter], avg_eval_attacker_action_alerts_means_v1_20_dr[0:max_iter],
        avg_eval_attacker_action_alerts_stds_v1_20_dr[0:max_iter],
        avg_eval_2_attacker_action_alerts_data_v1_20_dr[0:max_iter],
        avg_eval_2_attacker_action_alerts_means_v1_20_dr[0:max_iter],
        avg_eval_2_attacker_action_alerts_stds_v1_20_dr[0:max_iter],
        avg_train_attacker_action_alerts_data_v1_20_dr[0:max_iter],
        avg_train_attacker_action_alerts_means_v1_20_dr[0:max_iter],
        avg_train_attacker_action_alerts_stds_v1_20_dr[0:max_iter],
        avg_eval_steps_data_v1_20_dr[0:max_iter], avg_eval_steps_means_v1_20_dr[0:max_iter],
        avg_eval_steps_stds_v1_20_dr[0:max_iter],
        avg_eval_2_steps_data_v1_20_dr[0:max_iter], avg_eval_2_steps_means_v1_20_dr[0:max_iter],
        avg_eval_2_steps_stds_v1_20_dr[0:max_iter],
        avg_train_steps_data_v1_20_dr[0:max_iter], avg_train_steps_means_v1_20_dr[0:max_iter],
        avg_train_steps_stds_v1_20_dr[0:max_iter],
        fontsize=6.5, figsize=(7.5, 4.25), title_fontsize=8, lw=0.75, wspace=0.20, hspace=0.09, top=0.0,
        bottom=0.152, labelsize=5.25, markevery=5, optimal_reward=150, sample_step=10,
        eval_only=False, plot_opt=False, iterations_per_step=10, optimal_int=1.0,
        optimal_flag=1.0, file_name="mult_env_rew_det_fl_al_le", markersize=2.25
    )

    # plotting_util_attacker.plot_flags_int_r_steps_costs_alerts(
    #     avg_eval_rewards_data_v1_20[0:max_iter], avg_eval_rewards_means_v1_20[0:max_iter],
    #     avg_eval_rewards_stds_v1_20[0:max_iter],
    #     avg_eval_2_rewards_data_v1_20[0:max_iter], avg_eval_2_rewards_means_v1_20[0:max_iter],
    #     avg_eval_2_rewards_stds_v1_20[0:max_iter],
    #     avg_eval_caught_frac_data_v1_20[0:max_iter], avg_eval_caught_frac_means_v1_20[0:max_iter],
    #     avg_eval_caught_frac_stds_v1_20[0:max_iter],
    #     avg_eval_intrusion_frac_data_v1_20[0:max_iter], avg_eval_intrusion_means_v1_20[0:max_iter],
    #     avg_eval_intrusion_stds_v1_20[0:max_iter],
    #     avg_eval_2_caught_frac_data_v1_20[0:max_iter], avg_eval_2_caught_frac_means_v1_20[0:max_iter],
    #     avg_eval_2_caught_frac_stds_v1_20[0:max_iter],
    #     avg_eval_2_intrusion_frac_data_v1_20[0:max_iter], avg_eval_2_intrusion_means_v1_20[0:max_iter],
    #     avg_eval_2_intrusion_stds_v1_20[0:max_iter],
    #     avg_eval_flags_data_v1_20[0:max_iter], avg_eval_flags_means_v1_20[0:max_iter],
    #     avg_eval_flags_stds_v1_20[0:max_iter],
    #     avg_eval_2_flags_data_v1_20[0:max_iter], avg_eval_2_flags_means_v1_20[0:max_iter],
    #     avg_eval_2_flags_stds_v1_20[0:max_iter],
    #     avg_eval_attacker_action_costs_data_v1_20[0:max_iter], avg_eval_attacker_action_costs_means_v1_20[0:max_iter],
    #     avg_eval_attacker_action_costs_stds_v1_20[0:max_iter],
    #     avg_eval_2_attacker_action_costs_data_v1_20[0:max_iter], avg_eval_2_attacker_action_costs_means_v1_20[0:max_iter],
    #     avg_eval_2_attacker_action_costs_stds_v1_20[0:max_iter],
    #     avg_eval_attacker_action_alerts_data_v1_20[0:max_iter], avg_eval_attacker_action_alerts_means_v1_20[0:max_iter],
    #     avg_eval_attacker_action_alerts_stds_v1_20[0:max_iter],
    #     avg_eval_2_attacker_action_alerts_data_v1_20[0:max_iter], avg_eval_2_attacker_action_alerts_means_v1_20[0:max_iter],
    #     avg_eval_2_attacker_action_alerts_stds_v1_20[0:max_iter],
    #     avg_eval_steps_data_v1_20[0:max_iter], avg_eval_steps_means_v1_20[0:max_iter],
    #     avg_eval_steps_stds_v1_20[0:max_iter],
    #     avg_eval_2_steps_data_v1_20[0:max_iter], avg_eval_2_steps_means_v1_20[0:max_iter],
    #     avg_eval_2_steps_stds_v1_20[0:max_iter],
    #     fontsize= 6.5, figsize= (7.5, 2.75), title_fontsize=8, lw=0.75, wspace=0.12, hspace=0.4, top=0.0,
    #     bottom=0.152, labelsize=6, markevery=5, optimal_reward = 150, sample_step =10,
    #     eval_only=False, plot_opt = False, iterations_per_step= 10, optimal_int = 1.0,
    #     optimal_flag = 1.0, file_name = "flags_int_steps_r_costs_alerts_attacker", markersize=2.25
    # )

    # plotting_util_mult_envs.plot_mega_2(
    #     avg_train_rewards_data_v1_20, avg_train_rewards_means_v1_20, avg_train_rewards_stds_v1_20,
    #     avg_eval_rewards_data_v1_20, avg_eval_rewards_means_v1_20, avg_eval_rewards_stds_v1_20,
    #     train_containers_rewards_data_v1_20, train_containers_rewards_means_v1_20,
    #     train_containers_rewards_stds_v1_20, eval_containers_rewards_data_v1_20,
    #     eval_containers_rewards_means_v1_20, eval_containers_rewards_stds_v1_20,
    #
    #     avg_train_regret_data_v1_20, avg_train_regret_means_v1_20, avg_train_regret_stds_v1_20,
    #     avg_eval_regret_data_v1_20, avg_eval_regret_means_v1_20, avg_eval_regret_stds_v1_20,
    #     train_containers_regret_data_v1_20, train_containers_regret_means_v1_20,
    #     train_containers_regret_stds_v1_20, eval_containers_regret_data_v1_20,
    #     eval_containers_regret_means_v1_20, eval_containers_regret_stds_v1_20,
    #
    #     avg_train_steps_data_v1_20, avg_train_steps_means_v1_20, avg_train_steps_stds_v1_20,
    #     avg_eval_steps_data_v1_20, avg_eval_steps_means_v1_20, avg_eval_steps_stds_v1_20,
    #     train_containers_steps_data_v1_20, train_containers_steps_means_v1_20,
    #     train_containers_steps_stds_v1_20, eval_containers_steps_data_v1_20,
    #     eval_containers_steps_means_v1_20, eval_containers_steps_stds_v1_20,
    #
    #     avg_eval_rewards_data_v1_20, avg_eval_rewards_means_v1_20, avg_eval_rewards_stds_v1_20,
    #     avg_eval_rewards_data_v1_20, avg_eval_rewards_means_v1_20, avg_eval_rewards_stds_v1_20,
    #     eval_containers_rewards_data_v1_20, eval_containers_rewards_means_v1_20,
    #     eval_containers_rewards_stds_v1_20, eval_containers_rewards_data_v1_20,
    #     eval_containers_rewards_means_v1_20, eval_containers_rewards_stds_v1_20,
    #
    #     avg_eval_regret_data_v1_20, avg_eval_regret_means_v1_20, avg_eval_regret_stds_v1_20,
    #     avg_eval_regret_data_v1_20, avg_eval_regret_means_v1_20, avg_eval_regret_stds_v1_20,
    #     eval_containers_regret_data_v1_20, eval_containers_regret_means_v1_20,
    #     eval_containers_regret_stds_v1_20, eval_containers_regret_data_v1_20,
    #     eval_containers_regret_means_v1_20, eval_containers_regret_stds_v1_20,
    #
    #     avg_eval_steps_data_v1_20, avg_eval_steps_means_v1_20, avg_eval_steps_stds_v1_20,
    #     avg_eval_steps_data_v1_20, avg_eval_steps_means_v1_20, avg_eval_steps_stds_v1_20,
    #     eval_containers_steps_data_v1_20, eval_containers_steps_means_v1_20,
    #     eval_containers_steps_stds_v1_20, eval_containers_steps_data_v1_20,
    #     eval_containers_steps_means_v1_20, eval_containers_steps_stds_v1_20,
    #
    #
    #     avg_eval_2_rewards_data_v1_20, avg_eval_2_rewards_means_v1_20,
    #     avg_eval_2_rewards_stds_v1_20,
    #     avg_eval_rewards_data_v1_20, avg_eval_rewards_means_v1_20,
    #     avg_eval_rewards_stds_v1_20,
    #     eval_2_containers_rewards_data_v1_20, eval_2_containers_rewards_means_v1_20,
    #     eval_2_containers_rewards_stds_v1_20, eval_containers_rewards_data_v1_20,
    #     eval_containers_rewards_means_v1_20, eval_containers_rewards_stds_v1_20,
    #
    #     avg_eval_2_regret_data_v1_20, avg_eval_2_regret_means_v1_20, avg_eval_2_regret_stds_v1_20,
    #     avg_eval_regret_data_v1_20, avg_eval_regret_means_v1_20, avg_eval_regret_stds_v1_20,
    #     eval_2_containers_regret_data_v1_20, eval_2_containers_regret_means_v1_20,
    #     eval_2_containers_regret_stds_v1_20, eval_containers_regret_data_v1_20,
    #     eval_containers_regret_means_v1_20, eval_containers_regret_stds_v1_20,
    #
    #     avg_eval_2_steps_data_v1_20, avg_eval_2_steps_means_v1_20, avg_eval_2_steps_stds_v1_20,
    #     avg_eval_steps_data_v1_20, avg_eval_steps_means_v1_20, avg_eval_steps_stds_v1_20,
    #     eval_2_containers_steps_data_v1_20, eval_2_containers_steps_means_v1_20,
    #     eval_2_containers_steps_stds_v1_20, eval_containers_steps_data_v1_20,
    #     eval_containers_steps_means_v1_20, eval_containers_steps_stds_v1_20,
    #
    #     ylim_rew=(10, 100), file_name="mega_2_test", markevery=100000, optimal_steps = 10, optimal_reward = 1,
    #     sample_step = 1,
    #     plot_opt=True, ylim_reg=(-2.5,36.5), ylim_step=(1, 20), linewidth=0.7)

    # plotting_util_attacker.plot_rewards_attacker(
    #     avg_eval_rewards_data_v1_20[0:max_iter], avg_eval_rewards_means_v1_20[0:max_iter],
    #     avg_eval_rewards_stds_v1_20[0:max_iter],
    #     avg_eval_2_rewards_data_v1_20[0:max_iter], avg_eval_2_rewards_means_v1_20[0:max_iter],
    #     avg_eval_2_rewards_stds_v1_20[0:max_iter],
    #     ylim_rew=ylim_rew,
    #     file_name="./rewards_attacker_train_" + suffix,
    #     markevery=3, optimal_reward=150, sample_step=5, plot_opt=True, iterations_per_step=10
    # )
    #
    # ylim_rew = (0.0, 1.1)
    #
    # plotting_util_attacker.plot_caught_stopped_intruded(
    #     avg_eval_caught_frac_data_v1_20[0:max_iter], avg_eval_caught_frac_means_v1_20[0:max_iter],
    #     avg_eval_caught_frac_stds_v1_20[0:max_iter],
    #     avg_eval_early_stopping_frac_data_v1_20[0:max_iter], avg_eval_early_stopping_means_v1_20[0:max_iter],
    #     avg_eval_early_stopping_stds_v1_20[0:max_iter],
    #     avg_eval_intrusion_frac_data_v1_20[0:max_iter], avg_eval_intrusion_means_v1_20[0:max_iter],
    #     avg_eval_intrusion_stds_v1_20[0:max_iter],
    #     avg_eval_2_caught_frac_data_v1_20[0:max_iter], avg_eval_2_caught_frac_means_v1_20[0:max_iter],
    #     avg_eval_2_caught_frac_stds_v1_20[0:max_iter],
    #     avg_eval_2_early_stopping_frac_data_v1_20[0:max_iter], avg_eval_2_early_stopping_means_v1_20[0:max_iter],
    #     avg_eval_2_early_stopping_stds_v1_20[0:max_iter],
    #     avg_eval_2_intrusion_frac_data_v1_20[0:max_iter], avg_eval_2_intrusion_means_v1_20[0:max_iter],
    #     avg_eval_2_intrusion_stds_v1_20[0:max_iter],
    #     ylim_rew=ylim_rew,
    #     file_name="./attacker_caught_stopped_intruded_" + suffix,
    #     markevery=3, optimal_reward=1, sample_step=5, plot_opt=True, iterations_per_step=10
    # )
    #
    # ylim_rew = (400, 8000)
    #
    # plotting_util_attacker.plot_costs_attacker(
    #     avg_eval_attacker_action_costs_data_v1_20[0:max_iter], avg_eval_attacker_action_costs_means_v1_20[0:max_iter],
    #     avg_eval_attacker_action_costs_stds_v1_20[0:max_iter],
    #     avg_eval_2_attacker_action_costs_data_v1_20[0:max_iter], avg_eval_2_attacker_action_costs_means_v1_20[0:max_iter],
    #     avg_eval_2_attacker_action_costs_stds_v1_20[0:max_iter],
    #     ylim_rew=ylim_rew,
    #     file_name="./attacker_action_costs_attacker_train_" + suffix,
    #     markevery=3, optimal_reward=450, sample_step=5, plot_opt=False, iterations_per_step=10
    # )
    #
    # ylim_rew = (0, 2000)
    #
    # plotting_util_attacker.plot_alerts_attacker(
    #     avg_eval_attacker_action_alerts_data_v1_20[0:max_iter], avg_eval_attacker_action_alerts_means_v1_20[0:max_iter],
    #     avg_eval_attacker_action_alerts_stds_v1_20[0:max_iter],
    #     avg_eval_2_attacker_action_alerts_data_v1_20[0:max_iter], avg_eval_2_attacker_action_alerts_means_v1_20[0:max_iter],
    #     avg_eval_2_attacker_action_alerts_stds_v1_20[0:max_iter],
    #     ylim_rew=ylim_rew,
    #     file_name="./attacker_action_alerts_attacker_train_" + suffix,
    #     markevery=3, optimal_reward=450, sample_step=5, plot_opt=False, iterations_per_step=10
    # )
    #
    # ylim_rew = (0, 1.1)
    #
    # plotting_util_attacker.plot_flags_attacker(
    #     avg_eval_flags_data_v1_20[0:max_iter], avg_eval_flags_means_v1_20[0:max_iter],
    #     avg_eval_flags_stds_v1_20[0:max_iter],
    #     avg_eval_2_flags_data_v1_20[0:max_iter], avg_eval_2_flags_means_v1_20[0:max_iter],
    #     avg_eval_2_flags_stds_v1_20[0:max_iter],
    #     ylim_rew=ylim_rew,
    #     file_name="./flags_attacker_train_" + suffix,
    #     markevery=3, optimal_reward=1, sample_step=5, plot_opt=True, iterations_per_step=10
    # )
    #
    # ylim_rew = (0, 110)
    #
    # plotting_util_attacker.plot_steps_attacker(
    #     avg_eval_steps_data_v1_20[0:max_iter], avg_eval_steps_means_v1_20[0:max_iter],
    #     avg_eval_steps_stds_v1_20[0:max_iter],
    #     avg_eval_2_steps_data_v1_20[0:max_iter], avg_eval_2_steps_means_v1_20[0:max_iter],
    #     avg_eval_2_steps_stds_v1_20[0:max_iter],
    #     ylim_rew=ylim_rew,
    #     file_name="./steps_attacker_train_" + suffix,
    #     markevery=3, optimal_reward=450, sample_step=5, plot_opt=False, iterations_per_step=10
    # )


if __name__ == '__main__':
    # containers_configs = EnvConfigGenerator.get_all_envs_containers_config(
    #     "/Users/kimham/workspace/csle/emulation-system/minigames/network_intrusion/ctf/001/random_many_train/")
    # flags_configs = EnvConfigGenerator.get_all_envs_flags_config(
    #     "/Users/kimham/workspace/csle/emulation-system/minigames/network_intrusion/ctf/001/random_many_train/")
    # eval_env_containers_configs = EnvConfigGenerator.get_all_envs_containers_config(
    #     "/Users/kimham/workspace/csle/emulation-system/minigames/network_intrusion/ctf/001/random_many_eval/")
    # eval_env_flags_configs = EnvConfigGenerator.get_all_envs_flags_config(
    #     "/Users/kimham/workspace/csle/emulation-system/minigames/network_intrusion/ctf/001/random_many_eval/")
    containers_configs = EnvConfigGenerator.get_all_envs_containers_config(
        "/home/kim/storage/workspace/csle/emulation-system/minigames/network_intrusion/ctf/001/random_many_train/")
    flags_configs = EnvConfigGenerator.get_all_envs_flags_config(
        "/home/kim/storage/workspace/csle/emulation-system/minigames/network_intrusion/ctf/001/random_many_train/")
    eval_env_containers_configs = EnvConfigGenerator.get_all_envs_containers_config(
        "/home/kim/storage/workspace/csle/emulation-system/minigames/network_intrusion/ctf/001/random_many_eval/")
    eval_env_flags_configs = EnvConfigGenerator.get_all_envs_flags_config(
        "/home/kim/storage/workspace/csle/emulation-system/minigames/network_intrusion/ctf/001/random_many_eval/")

    base_path = "/home/kim/storage/workspace/csle/simulation-system/minigames/network_intrusion/ctf/gym-csle-ctf/examples/random_many/plot2/20_results/data/"
    avg_train_rewards_data_v1_20, avg_train_rewards_means_v1_20, avg_train_rewards_stds_v1_20, avg_train_steps_data_v1_20, \
    avg_train_steps_means_v1_20, avg_train_steps_stds_v1_20, avg_train_regret_data_v1_20, avg_train_regret_means_v1_20, \
    avg_train_regret_stds_v1_20, avg_train_opt_frac_data_v1_20, avg_train_opt_frac_means_v1_20, \
    avg_train_opt_frac_stds_v1_20, avg_train_caught_frac_data_v1_20, avg_train_caught_frac_means_v1_20, \
    avg_train_caught_frac_stds_v1_20, avg_train_early_stopping_frac_data_v1_20, avg_train_early_stopping_means_v1_20, \
    avg_train_early_stopping_stds_v1_20, avg_train_intrusion_frac_data_v1_20, avg_train_intrusion_means_v1_20, \
    avg_train_intrusion_stds_v1_20, avg_eval_rewards_data_v1_20, avg_eval_rewards_means_v1_20, avg_eval_rewards_stds_v1_20, \
    avg_eval_steps_data_v1_20, avg_eval_steps_means_v1_20, avg_eval_steps_stds_v1_20, avg_eval_regret_data_v1_20, \
    avg_eval_regret_means_v1_20, avg_eval_regret_stds_v1_20, avg_eval_opt_frac_data_v1_20, avg_eval_opt_frac_means_v1_20, \
    avg_eval_opt_frac_stds_v1_20, avg_eval_caught_frac_data_v1_20, avg_eval_caught_frac_means_v1_20, \
    avg_eval_caught_frac_stds_v1_20, avg_eval_early_stopping_frac_data_v1_20, avg_eval_early_stopping_means_v1_20, \
    avg_eval_early_stopping_stds_v1_20, avg_eval_intrusion_frac_data_v1_20, avg_eval_intrusion_means_v1_20, \
    avg_eval_intrusion_stds_v1_20, avg_eval_2_rewards_data_v1_20, avg_eval_2_rewards_means_v1_20, avg_eval_2_rewards_stds_v1_20,\
    avg_eval_2_steps_data_v1_20, avg_eval_2_steps_means_v1_20, avg_eval_2_steps_stds_v1_20, \
    avg_eval_2_caught_frac_data_v1_20, avg_eval_2_caught_frac_means_v1_20,\
    avg_eval_2_caught_frac_stds_v1_20, avg_eval_2_early_stopping_frac_data_v1_20, avg_eval_2_early_stopping_means_v1_20, \
    avg_eval_2_early_stopping_stds_v1_20,  avg_eval_2_intrusion_frac_data_v1_20, avg_eval_2_intrusion_means_v1_20, \
    avg_eval_2_intrusion_stds_v1_20, avg_eval_2_regret_data_v1_20, \
    avg_eval_2_regret_means_v1_20, avg_eval_2_regret_stds_v1_20, avg_eval_2_opt_frac_data_v1_20, \
    avg_eval_2_opt_frac_means_v1_20, avg_eval_2_opt_frac_stds_v1_20, avg_train_attacker_action_alerts_data_v1_20, \
    avg_train_attacker_action_alerts_means_v1_20, \
    avg_train_attacker_action_alerts_stds_v1_20, avg_eval_attacker_action_alerts_data_v1_20, \
    avg_eval_attacker_action_alerts_means_v1_20, \
    avg_eval_attacker_action_alerts_stds_v1_20, avg_eval_2_attacker_action_alerts_data_v1_20, \
    avg_eval_2_attacker_action_alerts_means_v1_20, avg_eval_2_attacker_action_alerts_stds_v1_20, \
    avg_train_attacker_action_costs_data_v1_20, avg_train_attacker_action_costs_means_v1_20, \
    avg_train_attacker_action_costs_stds_v1_20, \
    avg_eval_attacker_action_costs_data_v1_20, avg_eval_attacker_action_costs_means_v1_20, \
    avg_eval_attacker_action_costs_stds_v1_20, avg_eval_2_attacker_action_costs_data_v1_20, \
    avg_eval_2_attacker_action_costs_means_v1_20, avg_eval_2_attacker_action_costs_stds_v1_20, \
    avg_train_flags_data_v1_20, avg_train_flags_means_v1_20, avg_train_flags_stds_v1_20, \
    avg_eval_flags_data_v1_20, avg_eval_flags_means_v1_20, avg_eval_flags_stds_v1_20, \
    avg_eval_2_flags_data_v1_20, avg_eval_2_flags_means_v1_20, avg_eval_2_flags_stds_v1_20, \
    train_containers_rewards_data_v1_20, train_containers_rewards_means_v1_20, train_containers_rewards_stds_v1_20, \
    train_containers_flags_data_v1_20, train_containers_flags_means_v1_20, train_containers_flags_stds_v1_20, train_containers_steps_data_v1_20, \
    train_containers_steps_means_v1_20, train_containers_steps_stds_v1_20, train_containers_regret_data_v1_20, train_containers_regret_means_v1_20, \
    train_containers_regret_stds_v1_20, train_containers_opt_frac_data_v1_20, train_containers_opt_frac_means_v1_20, train_containers_opt_frac_stds_v1_20, \
    eval_2_containers_rewards_data_v1_20, eval_2_containers_rewards_means_v1_20, eval_2_containers_rewards_stds_v1_20, \
    eval_2_containers_flags_data_v1_20, eval_2_containers_flags_means_v1_20, eval_2_containers_flags_stds_v1_20, eval_2_containers_steps_data_v1_20, \
    eval_2_containers_steps_means_v1_20, eval_2_containers_steps_stds_v1_20, eval_2_containers_regret_data_v1_20, eval_2_containers_regret_means_v1_20, \
    eval_2_containers_regret_stds_v1_20, eval_2_containers_opt_frac_data_v1_20, eval_2_containers_opt_frac_means_v1_20, eval_2_containers_opt_frac_stds_v1_20, \
    eval_containers_rewards_data_v1_20, eval_containers_rewards_means_v1_20, eval_containers_rewards_stds_v1_20, \
    eval_containers_flags_data_v1_20, eval_containers_flags_means_v1_20, eval_containers_flags_stds_v1_20, eval_containers_steps_data_v1_20, \
    eval_containers_steps_means_v1_20, eval_containers_steps_stds_v1_20, eval_containers_regret_data_v1_20, eval_containers_regret_means_v1_20, \
    eval_containers_regret_stds_v1_20 = \
        parse_data(base_path=base_path, suffix="gensim", train_containers_configs=containers_configs,
                     eval_containers_configs=eval_env_containers_configs, multi_env=True)

    base_path = "/home/kim/storage/workspace/csle/simulation-system/minigames/network_intrusion/ctf/gym-csle-ctf/examples/random_many/plot2/1_results/data/"
    avg_train_rewards_data_v1_1, avg_train_rewards_means_v1_1, avg_train_rewards_stds_v1_1, avg_train_steps_data_v1_1, \
    avg_train_steps_means_v1_1, avg_train_steps_stds_v1_1, avg_train_regret_data_v1_1, avg_train_regret_means_v1_1, \
    avg_train_regret_stds_v1_1, avg_train_opt_frac_data_v1_1, avg_train_opt_frac_means_v1_1, \
    avg_train_opt_frac_stds_v1_1, avg_train_caught_frac_data_v1_1, avg_train_caught_frac_means_v1_1, \
    avg_train_caught_frac_stds_v1_1, avg_train_early_stopping_frac_data_v1_1, avg_train_early_stopping_means_v1_1, \
    avg_train_early_stopping_stds_v1_1, avg_train_intrusion_frac_data_v1_1, avg_train_intrusion_means_v1_1, \
    avg_train_intrusion_stds_v1_1, avg_eval_rewards_data_v1_1, avg_eval_rewards_means_v1_1, avg_eval_rewards_stds_v1_1, \
    avg_eval_steps_data_v1_1, avg_eval_steps_means_v1_1, avg_eval_steps_stds_v1_1, avg_eval_regret_data_v1_1, \
    avg_eval_regret_means_v1_1, avg_eval_regret_stds_v1_1, avg_eval_opt_frac_data_v1_1, avg_eval_opt_frac_means_v1_1, \
    avg_eval_opt_frac_stds_v1_1, avg_eval_caught_frac_data_v1_1, avg_eval_caught_frac_means_v1_1, \
    avg_eval_caught_frac_stds_v1_1, avg_eval_early_stopping_frac_data_v1_1, avg_eval_early_stopping_means_v1_1, \
    avg_eval_early_stopping_stds_v1_1, avg_eval_intrusion_frac_data_v1_1, avg_eval_intrusion_means_v1_1, \
    avg_eval_intrusion_stds_v1_1, avg_eval_2_rewards_data_v1_1, avg_eval_2_rewards_means_v1_1, avg_eval_2_rewards_stds_v1_1, \
    avg_eval_2_steps_data_v1_1, avg_eval_2_steps_means_v1_1, avg_eval_2_steps_stds_v1_1, \
    avg_eval_2_caught_frac_data_v1_1, avg_eval_2_caught_frac_means_v1_1, \
    avg_eval_2_caught_frac_stds_v1_1, avg_eval_2_early_stopping_frac_data_v1_1, avg_eval_2_early_stopping_means_v1_1, \
    avg_eval_2_early_stopping_stds_v1_1, avg_eval_2_intrusion_frac_data_v1_1, avg_eval_2_intrusion_means_v1_1, \
    avg_eval_2_intrusion_stds_v1_1, avg_eval_2_regret_data_v1_1, \
    avg_eval_2_regret_means_v1_1, avg_eval_2_regret_stds_v1_1, avg_eval_2_opt_frac_data_v1_1, \
    avg_eval_2_opt_frac_means_v1_1, avg_eval_2_opt_frac_stds_v1_1, avg_train_attacker_action_alerts_data_v1_1, \
    avg_train_attacker_action_alerts_means_v1_1, \
    avg_train_attacker_action_alerts_stds_v1_1, avg_eval_attacker_action_alerts_data_v1_1, \
    avg_eval_attacker_action_alerts_means_v1_1, \
    avg_eval_attacker_action_alerts_stds_v1_1, avg_eval_2_attacker_action_alerts_data_v1_1, \
    avg_eval_2_attacker_action_alerts_means_v1_1, avg_eval_2_attacker_action_alerts_stds_v1_1, \
    avg_train_attacker_action_costs_data_v1_1, avg_train_attacker_action_costs_means_v1_1, \
    avg_train_attacker_action_costs_stds_v1_1, \
    avg_eval_attacker_action_costs_data_v1_1, avg_eval_attacker_action_costs_means_v1_1, \
    avg_eval_attacker_action_costs_stds_v1_1, avg_eval_2_attacker_action_costs_data_v1_1, \
    avg_eval_2_attacker_action_costs_means_v1_1, avg_eval_2_attacker_action_costs_stds_v1_1, \
    avg_train_flags_data_v1_1, avg_train_flags_means_v1_1, avg_train_flags_stds_v1_1, \
    avg_eval_flags_data_v1_1, avg_eval_flags_means_v1_1, avg_eval_flags_stds_v1_1, \
    avg_eval_2_flags_data_v1_1, avg_eval_2_flags_means_v1_1, avg_eval_2_flags_stds_v1_1, \
    train_containers_rewards_data_v1_1, train_containers_rewards_means_v1_1, train_containers_rewards_stds_v1_1, \
    train_containers_flags_data_v1_1, train_containers_flags_means_v1_1, train_containers_flags_stds_v1_1, train_containers_steps_data_v1_1, \
    train_containers_steps_means_v1_1, train_containers_steps_stds_v1_1, train_containers_regret_data_v1_1, train_containers_regret_means_v1_1, \
    train_containers_regret_stds_v1_1, train_containers_opt_frac_data_v1_1, train_containers_opt_frac_means_v1_1, train_containers_opt_frac_stds_v1_1, \
    eval_2_containers_rewards_data_v1_1, eval_2_containers_rewards_means_v1_1, eval_2_containers_rewards_stds_v1_1, \
    eval_2_containers_flags_data_v1_1, eval_2_containers_flags_means_v1_1, eval_2_containers_flags_stds_v1_1, eval_2_containers_steps_data_v1_1, \
    eval_2_containers_steps_means_v1_1, eval_2_containers_steps_stds_v1_1, eval_2_containers_regret_data_v1_1, eval_2_containers_regret_means_v1_1, \
    eval_2_containers_regret_stds_v1_1, eval_2_containers_opt_frac_data_v1_1, eval_2_containers_opt_frac_means_v1_1, eval_2_containers_opt_frac_stds_v1_1, \
    eval_containers_rewards_data_v1_1, eval_containers_rewards_means_v1_1, eval_containers_rewards_stds_v1_1, \
    eval_containers_flags_data_v1_1, eval_containers_flags_means_v1_1, eval_containers_flags_stds_v1_1, eval_containers_steps_data_v1_1, \
    eval_containers_steps_means_v1_1, eval_containers_steps_stds_v1_1, eval_containers_regret_data_v1_1, eval_containers_regret_means_v1_1, \
    eval_containers_regret_stds_v1_1 = \
        parse_data(base_path=base_path, suffix="gensim", train_containers_configs=containers_configs,
                   eval_containers_configs=eval_env_containers_configs, multi_env=False)

    base_path = "/home/kim/storage/workspace/csle/simulation-system/minigames/network_intrusion/ctf/gym-csle-ctf/examples/random_many/plot2/20_dr_results/data/"
    avg_train_rewards_data_v1_20_dr, avg_train_rewards_means_v1_20_dr, avg_train_rewards_stds_v1_20_dr, avg_train_steps_data_v1_20_dr, \
    avg_train_steps_means_v1_20_dr, avg_train_steps_stds_v1_20_dr, avg_train_regret_data_v1_20_dr, avg_train_regret_means_v1_20_dr, \
    avg_train_regret_stds_v1_20_dr, avg_train_opt_frac_data_v1_20_dr, avg_train_opt_frac_means_v1_20_dr, \
    avg_train_opt_frac_stds_v1_20_dr, avg_train_caught_frac_data_v1_20_dr, avg_train_caught_frac_means_v1_20_dr, \
    avg_train_caught_frac_stds_v1_20_dr, avg_train_early_stopping_frac_data_v1_20_dr, avg_train_early_stopping_means_v1_20_dr, \
    avg_train_early_stopping_stds_v1_20_dr, avg_train_intrusion_frac_data_v1_20_dr, avg_train_intrusion_means_v1_20_dr, \
    avg_train_intrusion_stds_v1_20_dr, avg_eval_rewards_data_v1_20_dr, avg_eval_rewards_means_v1_20_dr, avg_eval_rewards_stds_v1_20_dr, \
    avg_eval_steps_data_v1_20_dr, avg_eval_steps_means_v1_20_dr, avg_eval_steps_stds_v1_20_dr, avg_eval_regret_data_v1_20_dr, \
    avg_eval_regret_means_v1_20_dr, avg_eval_regret_stds_v1_20_dr, avg_eval_opt_frac_data_v1_20_dr, avg_eval_opt_frac_means_v1_20_dr, \
    avg_eval_opt_frac_stds_v1_20_dr, avg_eval_caught_frac_data_v1_20_dr, avg_eval_caught_frac_means_v1_20_dr, \
    avg_eval_caught_frac_stds_v1_20_dr, avg_eval_early_stopping_frac_data_v1_20_dr, avg_eval_early_stopping_means_v1_20_dr, \
    avg_eval_early_stopping_stds_v1_20_dr, avg_eval_intrusion_frac_data_v1_20_dr, avg_eval_intrusion_means_v1_20_dr, \
    avg_eval_intrusion_stds_v1_20_dr, avg_eval_2_rewards_data_v1_20_dr, avg_eval_2_rewards_means_v1_20_dr, avg_eval_2_rewards_stds_v1_20_dr, \
    avg_eval_2_steps_data_v1_20_dr, avg_eval_2_steps_means_v1_20_dr, avg_eval_2_steps_stds_v1_20_dr, \
    avg_eval_2_caught_frac_data_v1_20_dr, avg_eval_2_caught_frac_means_v1_20_dr, \
    avg_eval_2_caught_frac_stds_v1_20_dr, avg_eval_2_early_stopping_frac_data_v1_20_dr, avg_eval_2_early_stopping_means_v1_20_dr, \
    avg_eval_2_early_stopping_stds_v1_20_dr, avg_eval_2_intrusion_frac_data_v1_20_dr, avg_eval_2_intrusion_means_v1_20_dr, \
    avg_eval_2_intrusion_stds_v1_20_dr, avg_eval_2_regret_data_v1_20_dr, \
    avg_eval_2_regret_means_v1_20_dr, avg_eval_2_regret_stds_v1_20_dr, avg_eval_2_opt_frac_data_v1_20_dr, \
    avg_eval_2_opt_frac_means_v1_20_dr, avg_eval_2_opt_frac_stds_v1_20_dr, avg_train_attacker_action_alerts_data_v1_20_dr, \
    avg_train_attacker_action_alerts_means_v1_20_dr, \
    avg_train_attacker_action_alerts_stds_v1_20_dr, avg_eval_attacker_action_alerts_data_v1_20_dr, \
    avg_eval_attacker_action_alerts_means_v1_20_dr, \
    avg_eval_attacker_action_alerts_stds_v1_20_dr, avg_eval_2_attacker_action_alerts_data_v1_20_dr, \
    avg_eval_2_attacker_action_alerts_means_v1_20_dr, avg_eval_2_attacker_action_alerts_stds_v1_20_dr, \
    avg_train_attacker_action_costs_data_v1_20_dr, avg_train_attacker_action_costs_means_v1_20_dr, \
    avg_train_attacker_action_costs_stds_v1_20_dr, \
    avg_eval_attacker_action_costs_data_v1_20_dr, avg_eval_attacker_action_costs_means_v1_20_dr, \
    avg_eval_attacker_action_costs_stds_v1_20_dr, avg_eval_2_attacker_action_costs_data_v1_20_dr, \
    avg_eval_2_attacker_action_costs_means_v1_20_dr, avg_eval_2_attacker_action_costs_stds_v1_20_dr, \
    avg_train_flags_data_v1_20_dr, avg_train_flags_means_v1_20_dr, avg_train_flags_stds_v1_20_dr, \
    avg_eval_flags_data_v1_20_dr, avg_eval_flags_means_v1_20_dr, avg_eval_flags_stds_v1_20_dr, \
    avg_eval_2_flags_data_v1_20_dr, avg_eval_2_flags_means_v1_20_dr, avg_eval_2_flags_stds_v1_20_dr, \
    train_containers_rewards_data_v1_20_dr, train_containers_rewards_means_v1_20_dr, train_containers_rewards_stds_v1_20_dr, \
    train_containers_flags_data_v1_20_dr, train_containers_flags_means_v1_20_dr, train_containers_flags_stds_v1_20_dr, train_containers_steps_data_v1_20_dr, \
    train_containers_steps_means_v1_20_dr, train_containers_steps_stds_v1_20_dr, train_containers_regret_data_v1_20_dr, train_containers_regret_means_v1_20_dr, \
    train_containers_regret_stds_v1_20_dr, train_containers_opt_frac_data_v1_20_dr, train_containers_opt_frac_means_v1_20_dr, train_containers_opt_frac_stds_v1_20_dr, \
    eval_2_containers_rewards_data_v1_20_dr, eval_2_containers_rewards_means_v1_20_dr, eval_2_containers_rewards_stds_v1_20_dr, \
    eval_2_containers_flags_data_v1_20_dr, eval_2_containers_flags_means_v1_20_dr, eval_2_containers_flags_stds_v1_20_dr, eval_2_containers_steps_data_v1_20_dr, \
    eval_2_containers_steps_means_v1_20_dr, eval_2_containers_steps_stds_v1_20_dr, eval_2_containers_regret_data_v1_20_dr, eval_2_containers_regret_means_v1_20_dr, \
    eval_2_containers_regret_stds_v1_20_dr, eval_2_containers_opt_frac_data_v1_20_dr, eval_2_containers_opt_frac_means_v1_20_dr, eval_2_containers_opt_frac_stds_v1_20_dr, \
    eval_containers_rewards_data_v1_20_dr, eval_containers_rewards_means_v1_20_dr, eval_containers_rewards_stds_v1_20_dr, \
    eval_containers_flags_data_v1_20_dr, eval_containers_flags_means_v1_20_dr, eval_containers_flags_stds_v1_20_dr, eval_containers_steps_data_v1_20_dr, \
    eval_containers_steps_means_v1_20_dr, eval_containers_steps_stds_v1_20_dr, eval_containers_regret_data_v1_20_dr, eval_containers_regret_means_v1_20_dr, \
    eval_containers_regret_stds_v1_20_dr = \
        parse_data(base_path=base_path, suffix="gensim", train_containers_configs=containers_configs,
                   eval_containers_configs=eval_env_containers_configs, multi_env=False, mult_env_dr=True)

    plot_train(avg_train_rewards_data_v1_20, avg_train_rewards_means_v1_20, avg_train_rewards_stds_v1_20, avg_train_steps_data_v1_20,
    avg_train_steps_means_v1_20, avg_train_steps_stds_v1_20, avg_train_regret_data_v1_20, avg_train_regret_means_v1_20,
    avg_train_regret_stds_v1_20, avg_train_opt_frac_data_v1_20, avg_train_opt_frac_means_v1_20,
    avg_train_opt_frac_stds_v1_20, avg_train_caught_frac_data_v1_20, avg_train_caught_frac_means_v1_20,
    avg_train_caught_frac_stds_v1_20, avg_train_early_stopping_frac_data_v1_20, avg_train_early_stopping_means_v1_20,
    avg_train_early_stopping_stds_v1_20, avg_train_intrusion_frac_data_v1_20, avg_train_intrusion_means_v1_20,
    avg_train_intrusion_stds_v1_20, avg_eval_rewards_data_v1_20, avg_eval_rewards_means_v1_20, avg_eval_rewards_stds_v1_20,
    avg_eval_steps_data_v1_20, avg_eval_steps_means_v1_20, avg_eval_steps_stds_v1_20, avg_eval_regret_data_v1_20,
    avg_eval_regret_means_v1_20, avg_eval_regret_stds_v1_20, avg_eval_opt_frac_data_v1_20, avg_eval_opt_frac_means_v1_20,
    avg_eval_opt_frac_stds_v1_20, avg_eval_caught_frac_data_v1_20, avg_eval_caught_frac_means_v1_20,
    avg_eval_caught_frac_stds_v1_20, avg_eval_early_stopping_frac_data_v1_20, avg_eval_early_stopping_means_v1_20,
    avg_eval_early_stopping_stds_v1_20, avg_eval_intrusion_frac_data_v1_20, avg_eval_intrusion_means_v1_20,
    avg_eval_intrusion_stds_v1_20, avg_eval_2_rewards_data_v1_20, avg_eval_2_rewards_means_v1_20, avg_eval_2_rewards_stds_v1_20,
    avg_eval_2_steps_data_v1_20, avg_eval_2_steps_means_v1_20, avg_eval_2_steps_stds_v1_20,
    avg_eval_2_caught_frac_data_v1_20, avg_eval_2_caught_frac_means_v1_20,
    avg_eval_2_caught_frac_stds_v1_20, avg_eval_2_early_stopping_frac_data_v1_20, avg_eval_2_early_stopping_means_v1_20,
    avg_eval_2_early_stopping_stds_v1_20,  avg_eval_2_intrusion_frac_data_v1_20, avg_eval_2_intrusion_means_v1_20,
    avg_eval_2_intrusion_stds_v1_20, avg_eval_2_regret_data_v1_20, avg_eval_2_regret_means_v1_20, avg_eval_2_regret_stds_v1_20,
    avg_eval_2_opt_frac_data_v1_20, avg_eval_2_opt_frac_means_v1_20, avg_eval_2_opt_frac_stds_v1_20,
    avg_train_attacker_action_alerts_data_v1_20, avg_train_attacker_action_alerts_means_v1_20,
    avg_train_attacker_action_alerts_stds_v1_20, avg_eval_attacker_action_alerts_data_v1_20,
    avg_eval_attacker_action_alerts_means_v1_20,
    avg_eval_attacker_action_alerts_stds_v1_20, avg_eval_2_attacker_action_alerts_data_v1_20,
    avg_eval_2_attacker_action_alerts_means_v1_20, avg_eval_2_attacker_action_alerts_stds_v1_20,
    avg_train_attacker_action_costs_data_v1_20, avg_train_attacker_action_costs_means_v1_20,
    avg_train_attacker_action_costs_stds_v1_20,
    avg_eval_attacker_action_costs_data_v1_20, avg_eval_attacker_action_costs_means_v1_20,
    avg_eval_attacker_action_costs_stds_v1_20, avg_eval_2_attacker_action_costs_data_v1_20,
    avg_eval_2_attacker_action_costs_means_v1_20, avg_eval_2_attacker_action_costs_stds_v1_20,
    avg_train_flags_data_v1_20, avg_train_flags_means_v1_20, avg_train_flags_stds_v1_20,
    avg_eval_flags_data_v1_20, avg_eval_flags_means_v1_20, avg_eval_flags_stds_v1_20,
    avg_eval_2_flags_data_v1_20, avg_eval_2_flags_means_v1_20, avg_eval_2_flags_stds_v1_20,
   train_containers_rewards_data_v1_20, train_containers_rewards_means_v1_20, train_containers_rewards_stds_v1_20,
   train_containers_flags_data_v1_20, train_containers_flags_means_v1_20, train_containers_flags_stds_v1_20,
   train_containers_steps_data_v1_20,
   train_containers_steps_means_v1_20, train_containers_steps_stds_v1_20, train_containers_regret_data_v1_20,
   train_containers_regret_means_v1_20,
   train_containers_regret_stds_v1_20, train_containers_opt_frac_data_v1_20, train_containers_opt_frac_means_v1_20,
   train_containers_opt_frac_stds_v1_20,
   eval_2_containers_rewards_data_v1_20, eval_2_containers_rewards_means_v1_20, eval_2_containers_rewards_stds_v1_20,
   eval_2_containers_flags_data_v1_20, eval_2_containers_flags_means_v1_20, eval_2_containers_flags_stds_v1_20,
   eval_2_containers_steps_data_v1_20,
   eval_2_containers_steps_means_v1_20, eval_2_containers_steps_stds_v1_20, eval_2_containers_regret_data_v1_20,
   eval_2_containers_regret_means_v1_20,
   eval_2_containers_regret_stds_v1_20, eval_2_containers_opt_frac_data_v1_20,
   eval_2_containers_opt_frac_means_v1_20, eval_2_containers_opt_frac_stds_v1_20,
   eval_containers_rewards_data_v1_20, eval_containers_rewards_means_v1_20, eval_containers_rewards_stds_v1_20,
   eval_containers_flags_data_v1_20, eval_containers_flags_means_v1_20, eval_containers_flags_stds_v1_20,
   eval_containers_steps_data_v1_20,
   eval_containers_steps_means_v1_20, eval_containers_steps_stds_v1_20, eval_containers_regret_data_v1_20,
   eval_containers_regret_means_v1_20, eval_containers_regret_stds_v1_20,
    avg_train_rewards_data_v1_1, avg_train_rewards_means_v1_1, avg_train_rewards_stds_v1_1, avg_train_steps_data_v1_1,
    avg_train_steps_means_v1_1, avg_train_steps_stds_v1_1, avg_train_regret_data_v1_1, avg_train_regret_means_v1_1,
    avg_train_regret_stds_v1_1, avg_train_opt_frac_data_v1_1, avg_train_opt_frac_means_v1_1,
    avg_train_opt_frac_stds_v1_1, avg_train_caught_frac_data_v1_1, avg_train_caught_frac_means_v1_1,
    avg_train_caught_frac_stds_v1_1, avg_train_early_stopping_frac_data_v1_1, avg_train_early_stopping_means_v1_1,
    avg_train_early_stopping_stds_v1_1, avg_train_intrusion_frac_data_v1_1, avg_train_intrusion_means_v1_1,
    avg_train_intrusion_stds_v1_1, avg_eval_rewards_data_v1_1, avg_eval_rewards_means_v1_1, avg_eval_rewards_stds_v1_1,
    avg_eval_steps_data_v1_1, avg_eval_steps_means_v1_1, avg_eval_steps_stds_v1_1, avg_eval_regret_data_v1_1,
    avg_eval_regret_means_v1_1, avg_eval_regret_stds_v1_1, avg_eval_opt_frac_data_v1_1, avg_eval_opt_frac_means_v1_1,
    avg_eval_opt_frac_stds_v1_1, avg_eval_caught_frac_data_v1_1, avg_eval_caught_frac_means_v1_1,
    avg_eval_caught_frac_stds_v1_1, avg_eval_early_stopping_frac_data_v1_1, avg_eval_early_stopping_means_v1_1,
    avg_eval_early_stopping_stds_v1_1, avg_eval_intrusion_frac_data_v1_1, avg_eval_intrusion_means_v1_1,
    avg_eval_intrusion_stds_v1_1, avg_eval_2_rewards_data_v1_1, avg_eval_2_rewards_means_v1_1, avg_eval_2_rewards_stds_v1_1,
    avg_eval_2_steps_data_v1_1, avg_eval_2_steps_means_v1_1, avg_eval_2_steps_stds_v1_1,
    avg_eval_2_caught_frac_data_v1_1, avg_eval_2_caught_frac_means_v1_1,
    avg_eval_2_caught_frac_stds_v1_1, avg_eval_2_early_stopping_frac_data_v1_1, avg_eval_2_early_stopping_means_v1_1,
    avg_eval_2_early_stopping_stds_v1_1, avg_eval_2_intrusion_frac_data_v1_1, avg_eval_2_intrusion_means_v1_1,
    avg_eval_2_intrusion_stds_v1_1, avg_eval_2_regret_data_v1_1, avg_eval_2_regret_means_v1_1, avg_eval_2_regret_stds_v1_1,
    avg_eval_2_opt_frac_data_v1_1, avg_eval_2_opt_frac_means_v1_1, avg_eval_2_opt_frac_stds_v1_1,
    avg_train_attacker_action_alerts_data_v1_1, avg_train_attacker_action_alerts_means_v1_1,
    avg_train_attacker_action_alerts_stds_v1_1, avg_eval_attacker_action_alerts_data_v1_1,
    avg_eval_attacker_action_alerts_means_v1_1,
    avg_eval_attacker_action_alerts_stds_v1_1, avg_eval_2_attacker_action_alerts_data_v1_1,
    avg_eval_2_attacker_action_alerts_means_v1_1, avg_eval_2_attacker_action_alerts_stds_v1_1,
    avg_train_attacker_action_costs_data_v1_1, avg_train_attacker_action_costs_means_v1_1,
    avg_train_attacker_action_costs_stds_v1_1,
    avg_eval_attacker_action_costs_data_v1_1, avg_eval_attacker_action_costs_means_v1_1,
    avg_eval_attacker_action_costs_stds_v1_1, avg_eval_2_attacker_action_costs_data_v1_1,
    avg_eval_2_attacker_action_costs_means_v1_1, avg_eval_2_attacker_action_costs_stds_v1_1,
    avg_train_flags_data_v1_1, avg_train_flags_means_v1_1, avg_train_flags_stds_v1_1,
    avg_eval_flags_data_v1_1, avg_eval_flags_means_v1_1, avg_eval_flags_stds_v1_1,
    avg_eval_2_flags_data_v1_1, avg_eval_2_flags_means_v1_1, avg_eval_2_flags_stds_v1_1,
    train_containers_rewards_data_v1_1, train_containers_rewards_means_v1_1, train_containers_rewards_stds_v1_1,
    train_containers_flags_data_v1_1, train_containers_flags_means_v1_1, train_containers_flags_stds_v1_1,
    train_containers_steps_data_v1_1,
    train_containers_steps_means_v1_1, train_containers_steps_stds_v1_1, train_containers_regret_data_v1_1,
    train_containers_regret_means_v1_1,
    train_containers_regret_stds_v1_1, train_containers_opt_frac_data_v1_1, train_containers_opt_frac_means_v1_1,
    train_containers_opt_frac_stds_v1_1,
    eval_2_containers_rewards_data_v1_1, eval_2_containers_rewards_means_v1_1, eval_2_containers_rewards_stds_v1_1,
    eval_2_containers_flags_data_v1_1, eval_2_containers_flags_means_v1_1, eval_2_containers_flags_stds_v1_1,
    eval_2_containers_steps_data_v1_1,
    eval_2_containers_steps_means_v1_1, eval_2_containers_steps_stds_v1_1, eval_2_containers_regret_data_v1_1,
    eval_2_containers_regret_means_v1_1,
    eval_2_containers_regret_stds_v1_1, eval_2_containers_opt_frac_data_v1_1,
    eval_2_containers_opt_frac_means_v1_1, eval_2_containers_opt_frac_stds_v1_1,
    eval_containers_rewards_data_v1_1, eval_containers_rewards_means_v1_1, eval_containers_rewards_stds_v1_1,
    eval_containers_flags_data_v1_1, eval_containers_flags_means_v1_1, eval_containers_flags_stds_v1_1,
    eval_containers_steps_data_v1_1,
    eval_containers_steps_means_v1_1, eval_containers_steps_stds_v1_1, eval_containers_regret_data_v1_1,
    eval_containers_regret_means_v1_1, eval_containers_regret_stds_v1_1,
    avg_train_rewards_data_v1_20_dr, avg_train_rewards_means_v1_20_dr, avg_train_rewards_stds_v1_20_dr, avg_train_steps_data_v1_20_dr,
    avg_train_steps_means_v1_20_dr, avg_train_steps_stds_v1_20_dr, avg_train_regret_data_v1_20_dr, avg_train_regret_means_v1_20_dr,
    avg_train_regret_stds_v1_20_dr, avg_train_opt_frac_data_v1_20_dr, avg_train_opt_frac_means_v1_20_dr,
    avg_train_opt_frac_stds_v1_20_dr, avg_train_caught_frac_data_v1_20_dr, avg_train_caught_frac_means_v1_20_dr,
    avg_train_caught_frac_stds_v1_20_dr, avg_train_early_stopping_frac_data_v1_20_dr, avg_train_early_stopping_means_v1_20_dr,
    avg_train_early_stopping_stds_v1_20_dr, avg_train_intrusion_frac_data_v1_20_dr, avg_train_intrusion_means_v1_20_dr,
    avg_train_intrusion_stds_v1_20_dr, avg_eval_rewards_data_v1_20_dr, avg_eval_rewards_means_v1_20_dr, avg_eval_rewards_stds_v1_20_dr,
    avg_eval_steps_data_v1_20_dr, avg_eval_steps_means_v1_20_dr, avg_eval_steps_stds_v1_20_dr, avg_eval_regret_data_v1_20_dr,
    avg_eval_regret_means_v1_20_dr, avg_eval_regret_stds_v1_20_dr, avg_eval_opt_frac_data_v1_20_dr, avg_eval_opt_frac_means_v1_20_dr,
    avg_eval_opt_frac_stds_v1_20_dr, avg_eval_caught_frac_data_v1_20_dr, avg_eval_caught_frac_means_v1_20_dr,
    avg_eval_caught_frac_stds_v1_20_dr, avg_eval_early_stopping_frac_data_v1_20_dr, avg_eval_early_stopping_means_v1_20_dr,
    avg_eval_early_stopping_stds_v1_20_dr, avg_eval_intrusion_frac_data_v1_20_dr, avg_eval_intrusion_means_v1_20_dr,
    avg_eval_intrusion_stds_v1_20_dr, avg_eval_2_rewards_data_v1_20_dr, avg_eval_2_rewards_means_v1_20_dr, avg_eval_2_rewards_stds_v1_20_dr,
    avg_eval_2_steps_data_v1_20_dr, avg_eval_2_steps_means_v1_20_dr, avg_eval_2_steps_stds_v1_20_dr,
    avg_eval_2_caught_frac_data_v1_20_dr, avg_eval_2_caught_frac_means_v1_20_dr,
    avg_eval_2_caught_frac_stds_v1_20_dr, avg_eval_2_early_stopping_frac_data_v1_20_dr, avg_eval_2_early_stopping_means_v1_20_dr,
    avg_eval_2_early_stopping_stds_v1_20_dr, avg_eval_2_intrusion_frac_data_v1_20_dr, avg_eval_2_intrusion_means_v1_20_dr,
    avg_eval_2_intrusion_stds_v1_20_dr, avg_eval_2_regret_data_v1_20_dr, avg_eval_2_regret_means_v1_20_dr, avg_eval_2_regret_stds_v1_20_dr,
    avg_eval_2_opt_frac_data_v1_20_dr, avg_eval_2_opt_frac_means_v1_20_dr, avg_eval_2_opt_frac_stds_v1_20_dr,
    avg_train_attacker_action_alerts_data_v1_20_dr, avg_train_attacker_action_alerts_means_v1_20_dr,
    avg_train_attacker_action_alerts_stds_v1_20_dr, avg_eval_attacker_action_alerts_data_v1_20_dr,
    avg_eval_attacker_action_alerts_means_v1_20_dr,
    avg_eval_attacker_action_alerts_stds_v1_20_dr, avg_eval_2_attacker_action_alerts_data_v1_20_dr,
    avg_eval_2_attacker_action_alerts_means_v1_20_dr, avg_eval_2_attacker_action_alerts_stds_v1_20_dr,
    avg_train_attacker_action_costs_data_v1_20_dr, avg_train_attacker_action_costs_means_v1_20_dr,
    avg_train_attacker_action_costs_stds_v1_20_dr,
    avg_eval_attacker_action_costs_data_v1_20_dr, avg_eval_attacker_action_costs_means_v1_20_dr,
    avg_eval_attacker_action_costs_stds_v1_20_dr, avg_eval_2_attacker_action_costs_data_v1_20_dr,
    avg_eval_2_attacker_action_costs_means_v1_20_dr, avg_eval_2_attacker_action_costs_stds_v1_20_dr,
    avg_train_flags_data_v1_20_dr, avg_train_flags_means_v1_20_dr, avg_train_flags_stds_v1_20_dr,
    avg_eval_flags_data_v1_20_dr, avg_eval_flags_means_v1_20_dr, avg_eval_flags_stds_v1_20_dr,
    avg_eval_2_flags_data_v1_20_dr, avg_eval_2_flags_means_v1_20_dr, avg_eval_2_flags_stds_v1_20_dr,
    train_containers_rewards_data_v1_20_dr, train_containers_rewards_means_v1_20_dr, train_containers_rewards_stds_v1_20_dr,
    train_containers_flags_data_v1_20_dr, train_containers_flags_means_v1_20_dr, train_containers_flags_stds_v1_20_dr,
    train_containers_steps_data_v1_20_dr,
    train_containers_steps_means_v1_20_dr, train_containers_steps_stds_v1_20_dr, train_containers_regret_data_v1_20_dr,
    train_containers_regret_means_v1_20_dr,
    train_containers_regret_stds_v1_20_dr, train_containers_opt_frac_data_v1_20_dr, train_containers_opt_frac_means_v1_20_dr,
    train_containers_opt_frac_stds_v1_20_dr,
    eval_2_containers_rewards_data_v1_20_dr, eval_2_containers_rewards_means_v1_20_dr, eval_2_containers_rewards_stds_v1_20_dr,
    eval_2_containers_flags_data_v1_20_dr, eval_2_containers_flags_means_v1_20_dr, eval_2_containers_flags_stds_v1_20_dr,
    eval_2_containers_steps_data_v1_20_dr,
    eval_2_containers_steps_means_v1_20_dr, eval_2_containers_steps_stds_v1_20_dr, eval_2_containers_regret_data_v1_20_dr,
    eval_2_containers_regret_means_v1_20_dr,
    eval_2_containers_regret_stds_v1_20_dr, eval_2_containers_opt_frac_data_v1_20_dr,
    eval_2_containers_opt_frac_means_v1_20_dr, eval_2_containers_opt_frac_stds_v1_20_dr,
    eval_containers_rewards_data_v1_20_dr, eval_containers_rewards_means_v1_20_dr, eval_containers_rewards_stds_v1_20_dr,
    eval_containers_flags_data_v1_20_dr, eval_containers_flags_means_v1_20_dr, eval_containers_flags_stds_v1_20_dr,
    eval_containers_steps_data_v1_20_dr,
    eval_containers_steps_means_v1_20_dr, eval_containers_steps_stds_v1_20_dr, eval_containers_regret_data_v1_20_dr,
    eval_containers_regret_means_v1_20_dr, eval_containers_regret_stds_v1_20_dr)


