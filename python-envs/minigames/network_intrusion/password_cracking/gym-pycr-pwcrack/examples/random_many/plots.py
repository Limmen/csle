from typing import List
import pandas as pd
import numpy as np
import torch
import glob
from gym_pycr_pwcrack.util.experiments_util import plotting_util
from gym_pycr_pwcrack.dao.container_config.containers_config import ContainersConfig
from gym_pycr_pwcrack.envs.config.generator.env_config_generator import EnvConfigGenerator
from gym_pycr_pwcrack.agents.policy_gradient.ppo_baseline.impl.ppo.ppo import PPO
from gym_pycr_pwcrack.agents.config.agent_config import AgentConfig
from gym_pycr_pwcrack.util.experiments_util import util

def plot_cluster_train(train_containers_configs: List[ContainersConfig], eval_containers_configs: List[ContainersConfig],
                       base_path: str, suffix: str, ips = None, eval_ips = None):
    print(glob.glob(base_path + "0/*_train.csv"))
    ppo_v1_df_0 = pd.read_csv(glob.glob(base_path + "0/*_train.csv")[0])
    # ppo_v1_df_399 = pd.read_csv(glob.glob(base_path + "399/*_train.csv")[0])
    ppo_v1_df_999 = pd.read_csv(glob.glob(base_path + "999/*_train.csv")[0])
    #ppo_dfs_v1 = [ppo_v1_df_0, ppo_v1_df_399, ppo_v1_df_999]
    ppo_dfs_v1=[ppo_v1_df_0, ppo_v1_df_999]
    running_avg = 10

    # Train avg
    avg_train_rewards_data_v1 = list(map(lambda df: util.running_average_list(df["avg_episode_rewards"].values, running_avg), ppo_dfs_v1))
    avg_train_rewards_means_v1 = np.mean(tuple(avg_train_rewards_data_v1), axis=0)
    avg_train_rewards_stds_v1 = np.std(tuple(avg_train_rewards_data_v1), axis=0, ddof=1)

    avg_train_flags_data_v1 = list(map(lambda df: util.running_average_list(df["avg_episode_flags_percentage"].values, running_avg), ppo_dfs_v1))
    avg_train_flags_means_v1 = np.mean(tuple(avg_train_flags_data_v1), axis=0)
    avg_train_flags_stds_v1 = np.std(tuple(avg_train_flags_data_v1), axis=0, ddof=1)

    avg_train_steps_data_v1 = list(map(lambda df: util.running_average_list(df["avg_episode_steps"].values, running_avg), ppo_dfs_v1))
    avg_train_steps_means_v1 = np.mean(tuple(avg_train_steps_data_v1), axis=0)
    avg_train_steps_stds_v1 = np.std(tuple(avg_train_steps_data_v1), axis=0, ddof=1)

    avg_train_regret_data_v1 = list(map(lambda df: util.running_average_list(df["avg_regret"].values, running_avg), ppo_dfs_v1))
    avg_train_regret_means_v1 = np.mean(tuple(avg_train_regret_data_v1), axis=0)
    avg_train_regret_stds_v1 = np.std(tuple(avg_train_regret_data_v1), axis=0, ddof=1)

    avg_train_opt_frac_data_v1 = list(map(lambda df: util.running_average_list(df["avg_opt_frac"].values, running_avg), ppo_dfs_v1))
    avg_train_opt_frac_data_v1 = list(map(lambda x: np.minimum(np.array([1]* len(x)), x), avg_train_opt_frac_data_v1))
    avg_train_opt_frac_means_v1 = np.mean(tuple(avg_train_opt_frac_data_v1), axis=0)
    avg_train_opt_frac_stds_v1 = np.std(tuple(avg_train_opt_frac_data_v1), axis=0, ddof=1)

    # Eval avg
    avg_eval_rewards_data_v1 = list(map(lambda df: util.running_average_list(df["eval_2_avg_episode_rewards"].values, running_avg), ppo_dfs_v1))
    avg_eval_rewards_means_v1 = np.mean(tuple(avg_eval_rewards_data_v1), axis=0)
    avg_eval_rewards_stds_v1 = np.std(tuple(avg_eval_rewards_data_v1), axis=0, ddof=1)

    avg_eval_flags_data_v1 = list(map(lambda df: util.running_average_list(df["eval_2_avg_episode_flags_percentage"].values, running_avg), ppo_dfs_v1))
    avg_eval_flags_means_v1 = np.mean(tuple(avg_eval_flags_data_v1), axis=0)
    avg_eval_flags_stds_v1 = np.std(tuple(avg_eval_flags_data_v1), axis=0, ddof=1)

    avg_eval_steps_data_v1 = list(map(lambda df: util.running_average_list(df["eval_2_avg_episode_steps"].values, running_avg), ppo_dfs_v1))
    avg_eval_steps_means_v1 = np.mean(tuple(avg_eval_steps_data_v1), axis=0)
    avg_eval_steps_stds_v1 = np.std(tuple(avg_eval_steps_data_v1), axis=0, ddof=1)

    avg_eval_regret_data_v1 = list(map(lambda df: util.running_average_list(df["eval_2_avg_regret"].values, running_avg), ppo_dfs_v1))
    avg_eval_regret_means_v1 = np.mean(tuple(avg_eval_regret_data_v1), axis=0)
    avg_eval_regret_stds_v1 = np.std(tuple(avg_eval_regret_data_v1), axis=0, ddof=1)

    avg_eval_opt_frac_data_v1 = list(map(lambda df: util.running_average_list(df["eval_2_avg_opt_frac"].values, running_avg), ppo_dfs_v1))
    avg_eval_opt_frac_data_v1 = list(map(lambda x: np.minimum(np.array([1]* len(x)), x), avg_eval_opt_frac_data_v1))
    avg_eval_opt_frac_means_v1 = np.mean(tuple(avg_eval_opt_frac_data_v1), axis=0)
    avg_eval_opt_frac_stds_v1 = np.std(tuple(avg_eval_opt_frac_data_v1), axis=0, ddof=1)

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
    for agent_ip in ips:
        rewards_label = agent_ip + "_avg_episode_rewards"
        flags_label = agent_ip + "_avg_episode_flags_percentage"
        steps_label = agent_ip + "_avg_episode_steps"
        regret_label = agent_ip + "_avg_episode_regrets"
        opt_frac_label = agent_ip + "_avg_episode_opt_fracs"

        env_train_rewards_data_v1 = list(map(lambda df: df[rewards_label].values, ppo_dfs_v1))
        env_train_rewards_means_v1 = np.mean(tuple(env_train_rewards_data_v1), axis=0)
        env_train_rewards_stds_v1 = np.std(tuple(env_train_rewards_data_v1), axis=0, ddof=1)

        env_train_flags_data_v1 = list(map(lambda df: df[flags_label].values, ppo_dfs_v1))
        env_train_flags_means_v1 = np.mean(tuple(env_train_flags_data_v1), axis=0)
        env_train_flags_stds_v1 = np.std(tuple(env_train_flags_data_v1), axis=0, ddof=1)

        env_train_steps_data_v1 = list(map(lambda df: df[steps_label].values, ppo_dfs_v1))
        env_train_steps_means_v1 = np.mean(tuple(env_train_steps_data_v1), axis=0)
        env_train_steps_stds_v1 = np.std(tuple(env_train_steps_data_v1), axis=0, ddof=1)

        env_train_regret_data_v1 = list(map(lambda df: df[regret_label].values, ppo_dfs_v1))
        env_train_regret_means_v1 = np.mean(tuple(env_train_regret_data_v1), axis=0)
        env_train_regret_stds_v1 = np.std(tuple(env_train_regret_data_v1), axis=0, ddof=1)

        env_train_opt_frac_data_v1 = list(map(lambda df: df[opt_frac_label].values, ppo_dfs_v1))
        env_train_opt_frac_data_v1 = list(map(lambda x: np.minimum(np.array([1]* len(x)), x), env_train_opt_frac_data_v1))
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

    if eval_ips is None or len(eval_ips) == 0:
        eval_ips = list(map(lambda x: x.agent_ip, eval_containers_configs))
    for agent_ip in eval_ips:
        rewards_label = agent_ip + "_eval_2_avg_episode_rewards"
        flags_label = agent_ip + "_eval_2_avg_episode_flags_percentage"
        steps_label = agent_ip + "_eval_2_avg_episode_steps"
        regrets_label = agent_ip + "_eval_2_avg_episode_regrets"
        opt_frac_label = agent_ip + "_eval_2_avg_episode_opt_fracs"

        env_eval_rewards_data_v1 = list(map(lambda df: df[rewards_label].values, ppo_dfs_v1))
        env_eval_rewards_means_v1 = np.mean(tuple(env_eval_rewards_data_v1), axis=0)
        env_eval_rewards_stds_v1 = np.std(tuple(env_eval_rewards_data_v1), axis=0, ddof=1)

        env_eval_flags_data_v1 = list(map(lambda df: df[flags_label].values, ppo_dfs_v1))
        env_eval_flags_means_v1 = np.mean(tuple(env_eval_flags_data_v1), axis=0)
        env_eval_flags_stds_v1 = np.std(tuple(env_eval_flags_data_v1), axis=0, ddof=1)

        env_eval_steps_data_v1 = list(map(lambda df: df[steps_label].values, ppo_dfs_v1))
        env_eval_steps_means_v1 = np.mean(tuple(env_eval_steps_data_v1), axis=0)
        env_eval_steps_stds_v1 = np.std(tuple(env_eval_steps_data_v1), axis=0, ddof=1)

        env_eval_regret_data_v1 = list(map(lambda df: df[regrets_label].values, ppo_dfs_v1))
        env_eval_regret_means_v1 = np.mean(tuple(env_eval_regret_data_v1), axis=0)
        env_eval_regret_stds_v1 = np.std(tuple(env_eval_regret_data_v1), axis=0, ddof=1)

        env_eval_opt_frac_data_v1 = list(map(lambda df: df[opt_frac_label].values, ppo_dfs_v1))
        env_eval_opt_frac_data_v1 = list(map(lambda x: np.minimum(np.array([1]* len(x)), x), env_eval_opt_frac_data_v1))
        env_eval_opt_frac_means_v1 = np.mean(tuple(env_eval_opt_frac_data_v1), axis=0)
        env_eval_opt_frac_stds_v1 = np.std(tuple(env_eval_opt_frac_data_v1), axis=0, ddof=1)

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

        eval_containers_opt_frac_data_v1[agent_ip] = env_eval_opt_frac_data_v1
        eval_containers_opt_frac_means_v1[agent_ip] = env_eval_opt_frac_means_v1
        eval_containers_opt_frac_stds_v1[agent_ip] = env_eval_opt_frac_stds_v1


    # ylim_rew = (min([min(rewards_means_v1 - rewards_stds_v1)]),
    #             max([max(rewards_means_v1 + rewards_stds_v1)]))
    # ylim_step = (min([min(steps_means_v1 - steps_stds_v1)]),
    #              max([max(steps_means_v1 + steps_stds_v1)]))
    ylim_rew = (-15, 20)

    # plotting_util.plot_rewards_train_cluster(train_avg_rewards_data_1=avg_train_rewards_data_v1,
    #                                          train_avg_rewards_means_1=avg_train_rewards_means_v1,
    #                                          train_avg_rewards_stds_1=avg_train_rewards_stds_v1,
    #                                          eval_avg_rewards_data_1=avg_eval_rewards_data_v1,
    #                                          eval_avg_rewards_means_1=avg_eval_rewards_means_v1,
    #                                          eval_avg_rewards_stds_1=avg_eval_rewards_stds_v1,
    #                                          train_envs_specific_rewards_data=train_containers_rewards_data_v1,
    #                                          train_envs_specific_rewards_means=train_containers_rewards_means_v1,
    #                                          train_envs_specific_rewards_stds=train_containers_rewards_stds_v1,
    #                                          eval_envs_specific_rewards_data=eval_containers_rewards_data_v1,
    #                                          eval_envs_specific_rewards_means=eval_containers_rewards_means_v1,
    #                                          eval_envs_specific_rewards_stds=eval_containers_rewards_stds_v1,
    #                                          ylim_rew=ylim_rew,
    #                                          file_name="./rewards_cluster_train_mult_env_" + suffix,
    #                                          markevery=3, optimal_steps=5, optimal_reward=16,  sample_step = 10
    #                                          )
    #
    # ylim_rew = (-15, 20)
    #
    # plotting_util.plot_rewards_train_cluster_two_colors(train_avg_rewards_data_1=avg_train_rewards_data_v1,
    #                                          train_avg_rewards_means_1=avg_train_rewards_means_v1,
    #                                          train_avg_rewards_stds_1=avg_train_rewards_stds_v1,
    #                                          eval_avg_rewards_data_1=avg_eval_rewards_data_v1,
    #                                          eval_avg_rewards_means_1=avg_eval_rewards_means_v1,
    #                                          eval_avg_rewards_stds_1=avg_eval_rewards_stds_v1,
    #                                          train_envs_specific_rewards_data=train_containers_rewards_data_v1,
    #                                          train_envs_specific_rewards_means=train_containers_rewards_means_v1,
    #                                          train_envs_specific_rewards_stds=train_containers_rewards_stds_v1,
    #                                          eval_envs_specific_rewards_data=eval_containers_rewards_data_v1,
    #                                          eval_envs_specific_rewards_means=eval_containers_rewards_means_v1,
    #                                          eval_envs_specific_rewards_stds=eval_containers_rewards_stds_v1,
    #                                          ylim_rew=ylim_rew,
    #                                          file_name="./rewards_cluster_train_mult_env_2_colors_" + suffix,
    #                                          markevery=3, optimal_steps=5, optimal_reward=16, sample_step = 10
    #                                          )
    #
    # ylim_rew = (-15, 20)
    #
    # plotting_util.plot_rewards_train_cluster_avg_only(train_avg_rewards_data_1=avg_train_rewards_data_v1,
    #                                                     train_avg_rewards_means_1=avg_train_rewards_means_v1,
    #                                                     train_avg_rewards_stds_1=avg_train_rewards_stds_v1,
    #                                                     eval_avg_rewards_data_1=avg_eval_rewards_data_v1,
    #                                                     eval_avg_rewards_means_1=avg_eval_rewards_means_v1,
    #                                                     eval_avg_rewards_stds_1=avg_eval_rewards_stds_v1,
    #                                                     train_envs_specific_rewards_data=train_containers_rewards_data_v1,
    #                                                     train_envs_specific_rewards_means=train_containers_rewards_means_v1,
    #                                                     train_envs_specific_rewards_stds=train_containers_rewards_stds_v1,
    #                                                     eval_envs_specific_rewards_data=eval_containers_rewards_data_v1,
    #                                                     eval_envs_specific_rewards_means=eval_containers_rewards_means_v1,
    #                                                     eval_envs_specific_rewards_stds=eval_containers_rewards_stds_v1,
    #                                                     ylim_rew=ylim_rew,
    #                                                     file_name="./rewards_cluster_train_mult_env_avg_" + suffix,
    #                                                     markevery=3, optimal_steps=5, optimal_reward=16, sample_step = 10
    #                                                     )
    #
    # ylim_rew = (-0.5, 20)
    # plotting_util.plot_regret_train_cluster(train_avg_regret_data_1=avg_train_regret_data_v1,
    #                                          train_avg_regret_means_1=avg_train_regret_means_v1,
    #                                          train_avg_regret_stds_1=avg_train_regret_stds_v1,
    #                                          eval_avg_regret_data_1=avg_eval_regret_data_v1,
    #                                          eval_avg_regret_means_1=avg_eval_regret_means_v1,
    #                                          eval_avg_regret_stds_1=avg_eval_regret_stds_v1,
    #                                          train_envs_specific_regret_data=train_containers_regret_data_v1,
    #                                          train_envs_specific_regret_means=train_containers_regret_means_v1,
    #                                          train_envs_specific_regret_stds=train_containers_regret_stds_v1,
    #                                          eval_envs_specific_regret_data=eval_containers_regret_data_v1,
    #                                          eval_envs_specific_regret_means=eval_containers_regret_means_v1,
    #                                          eval_envs_specific_regret_stds=eval_containers_regret_stds_v1,
    #                                          ylim_rew=ylim_rew,
    #                                          file_name="./regret_cluster_train_mult_env_" + suffix,
    #                                          markevery=3, optimal_steps=5, optimal_regret=0, sample_step=10
    #                                          )
    #
    # plotting_util.plot_regret_train_cluster_two_colors(train_avg_regret_data_1=avg_train_regret_data_v1,
    #                                          train_avg_regret_means_1=avg_train_regret_means_v1,
    #                                          train_avg_regret_stds_1=avg_train_regret_stds_v1,
    #                                          eval_avg_regret_data_1=avg_eval_regret_data_v1,
    #                                          eval_avg_regret_means_1=avg_eval_regret_means_v1,
    #                                          eval_avg_regret_stds_1=avg_eval_regret_stds_v1,
    #                                          train_envs_specific_regret_data=train_containers_regret_data_v1,
    #                                          train_envs_specific_regret_means=train_containers_regret_means_v1,
    #                                          train_envs_specific_regret_stds=train_containers_regret_stds_v1,
    #                                          eval_envs_specific_regret_data=eval_containers_regret_data_v1,
    #                                          eval_envs_specific_regret_means=eval_containers_regret_means_v1,
    #                                          eval_envs_specific_regret_stds=eval_containers_regret_stds_v1,
    #                                          ylim_rew=ylim_rew,
    #                                          file_name="./regret_cluster_train_mult_env_2_colors_" + suffix,
    #                                          markevery=3, optimal_steps=5, optimal_regret=0, sample_step = 10
    #                                          )
    #
    # plotting_util.plot_regret_train_cluster_avg_only(train_avg_regret_data_1=avg_train_regret_data_v1,
    #                                                    train_avg_regret_means_1=avg_train_regret_means_v1,
    #                                                    train_avg_regret_stds_1=avg_train_regret_stds_v1,
    #                                                    eval_avg_regret_data_1=avg_eval_regret_data_v1,
    #                                                    eval_avg_regret_means_1=avg_eval_regret_means_v1,
    #                                                    eval_avg_regret_stds_1=avg_eval_regret_stds_v1,
    #                                                    train_envs_specific_regret_data=train_containers_regret_data_v1,
    #                                                    train_envs_specific_regret_means=train_containers_regret_means_v1,
    #                                                    train_envs_specific_regret_stds=train_containers_regret_stds_v1,
    #                                                    eval_envs_specific_regret_data=eval_containers_regret_data_v1,
    #                                                    eval_envs_specific_regret_means=eval_containers_regret_means_v1,
    #                                                    eval_envs_specific_regret_stds=eval_containers_regret_stds_v1,
    #                                                    ylim_rew=ylim_rew,
    #                                                    file_name="./regret_cluster_train_mult_env_avg_" + suffix,
    #                                                    markevery=3, optimal_steps=5, optimal_regret=0, sample_step=10
    #                                                    )
    # ylim_rew = (-1.5, 1.5)
    # plotting_util.plot_rewards_train_cluster(train_avg_rewards_data_1=avg_train_opt_frac_data_v1,
    #                                          train_avg_rewards_means_1=avg_train_opt_frac_means_v1,
    #                                          train_avg_rewards_stds_1=avg_train_opt_frac_stds_v1,
    #                                          eval_avg_rewards_data_1=avg_eval_opt_frac_data_v1,
    #                                          eval_avg_rewards_means_1=avg_eval_opt_frac_means_v1,
    #                                          eval_avg_rewards_stds_1=avg_eval_opt_frac_stds_v1,
    #                                          train_envs_specific_rewards_data=train_containers_opt_frac_data_v1,
    #                                          train_envs_specific_rewards_means=train_containers_opt_frac_means_v1,
    #                                          train_envs_specific_rewards_stds=train_containers_opt_frac_stds_v1,
    #                                          eval_envs_specific_rewards_data=eval_containers_opt_frac_data_v1,
    #                                          eval_envs_specific_rewards_means=eval_containers_opt_frac_means_v1,
    #                                          eval_envs_specific_rewards_stds=eval_containers_opt_frac_stds_v1,
    #                                          ylim_rew=ylim_rew,
    #                                          file_name="./opt_frac_cluster_train_mult_env_" + suffix,
    #                                          markevery=3, optimal_steps=5, optimal_reward=1,  sample_step = 10,
    #                                          plot_opt=True
    #                                          )
    #
    # plotting_util.plot_rewards_train_cluster_two_colors(train_avg_rewards_data_1=avg_train_opt_frac_data_v1,
    #                                          train_avg_rewards_means_1=avg_train_opt_frac_means_v1,
    #                                          train_avg_rewards_stds_1=avg_train_opt_frac_stds_v1,
    #                                          eval_avg_rewards_data_1=avg_eval_opt_frac_data_v1,
    #                                          eval_avg_rewards_means_1=avg_eval_opt_frac_means_v1,
    #                                          eval_avg_rewards_stds_1=avg_eval_opt_frac_stds_v1,
    #                                          train_envs_specific_rewards_data=train_containers_opt_frac_data_v1,
    #                                          train_envs_specific_rewards_means=train_containers_opt_frac_means_v1,
    #                                          train_envs_specific_rewards_stds=train_containers_opt_frac_stds_v1,
    #                                          eval_envs_specific_rewards_data=eval_containers_opt_frac_data_v1,
    #                                          eval_envs_specific_rewards_means=eval_containers_opt_frac_means_v1,
    #                                          eval_envs_specific_rewards_stds=eval_containers_opt_frac_stds_v1,
    #                                          ylim_rew=ylim_rew,
    #                                          file_name="./opt_frac_cluster_train_mult_env_2_colors_" + suffix,
    #                                          markevery=3, optimal_steps=5, optimal_reward=1, sample_step = 10,
    #                                          plot_opt=True
    #                                          )
    #
    # plotting_util.plot_rewards_train_cluster_avg_only(train_avg_rewards_data_1=avg_train_opt_frac_data_v1,
    #                                                     train_avg_rewards_means_1=avg_train_opt_frac_means_v1,
    #                                                     train_avg_rewards_stds_1=avg_train_opt_frac_stds_v1,
    #                                                     eval_avg_rewards_data_1=avg_eval_opt_frac_data_v1,
    #                                                     eval_avg_rewards_means_1=avg_eval_opt_frac_means_v1,
    #                                                     eval_avg_rewards_stds_1=avg_eval_opt_frac_stds_v1,
    #                                                     train_envs_specific_rewards_data=train_containers_opt_frac_data_v1,
    #                                                     train_envs_specific_rewards_means=train_containers_opt_frac_means_v1,
    #                                                     train_envs_specific_rewards_stds=train_containers_opt_frac_stds_v1,
    #                                                     eval_envs_specific_rewards_data=eval_containers_opt_frac_data_v1,
    #                                                     eval_envs_specific_rewards_means=eval_containers_opt_frac_means_v1,
    #                                                     eval_envs_specific_rewards_stds=eval_containers_opt_frac_stds_v1,
    #                                                     ylim_rew=ylim_rew,
    #                                                     file_name="./opt_frac_cluster_train_mult_env_avg_" + suffix,
    #                                                     markevery=3, optimal_steps=5, optimal_reward=1, sample_step = 10,
    #                                                     plot_opt=True
    #                                                     )
    #
    # # Steps
    #
    # ylim_rew = (1, 15)
    # plotting_util.plot_steps_train_cluster(train_avg_steps_data_1=avg_train_steps_data_v1,
    #                                          train_avg_steps_means_1=avg_train_steps_means_v1,
    #                                          train_avg_steps_stds_1=avg_train_steps_stds_v1,
    #                                          eval_avg_steps_data_1=avg_eval_steps_data_v1,
    #                                          eval_avg_steps_means_1=avg_eval_steps_means_v1,
    #                                          eval_avg_steps_stds_1=avg_eval_steps_stds_v1,
    #                                          train_envs_specific_steps_data=train_containers_steps_data_v1,
    #                                          train_envs_specific_steps_means=train_containers_steps_means_v1,
    #                                          train_envs_specific_steps_stds=train_containers_steps_stds_v1,
    #                                          eval_envs_specific_steps_data=eval_containers_steps_data_v1,
    #                                          eval_envs_specific_steps_means=eval_containers_steps_means_v1,
    #                                          eval_envs_specific_steps_stds=eval_containers_steps_stds_v1,
    #                                          ylim_rew=ylim_rew,
    #                                          file_name="./steps_cluster_train_mult_env_" + suffix,
    #                                          markevery=3, optimal_steps=5, sample_step=10
    #                                          )
    #
    # plotting_util.plot_steps_train_cluster_two_colors(train_avg_steps_data_1=avg_train_steps_data_v1,
    #                                                     train_avg_steps_means_1=avg_train_steps_means_v1,
    #                                                     train_avg_steps_stds_1=avg_train_steps_stds_v1,
    #                                                     eval_avg_steps_data_1=avg_eval_steps_data_v1,
    #                                                     eval_avg_steps_means_1=avg_eval_steps_means_v1,
    #                                                     eval_avg_steps_stds_1=avg_eval_steps_stds_v1,
    #                                                     train_envs_specific_steps_data=train_containers_steps_data_v1,
    #                                                     train_envs_specific_steps_means=train_containers_steps_means_v1,
    #                                                     train_envs_specific_steps_stds=train_containers_steps_stds_v1,
    #                                                     eval_envs_specific_steps_data=eval_containers_steps_data_v1,
    #                                                     eval_envs_specific_steps_means=eval_containers_steps_means_v1,
    #                                                     eval_envs_specific_steps_stds=eval_containers_steps_stds_v1,
    #                                                     ylim_rew=ylim_rew,
    #                                                     file_name="./steps_cluster_train_mult_env_2_colors_" + suffix,
    #                                                     markevery=3, optimal_steps=5, sample_step=10
    #                                                     )
    #
    # plotting_util.plot_steps_train_cluster_avg_only(train_avg_steps_data_1=avg_train_steps_data_v1,
    #                                                   train_avg_steps_means_1=avg_train_steps_means_v1,
    #                                                   train_avg_steps_stds_1=avg_train_steps_stds_v1,
    #                                                   eval_avg_steps_data_1=avg_eval_steps_data_v1,
    #                                                   eval_avg_steps_means_1=avg_eval_steps_means_v1,
    #                                                   eval_avg_steps_stds_1=avg_eval_steps_stds_v1,
    #                                                   train_envs_specific_steps_data=train_containers_steps_data_v1,
    #                                                   train_envs_specific_steps_means=train_containers_steps_means_v1,
    #                                                   train_envs_specific_steps_stds=train_containers_steps_stds_v1,
    #                                                   eval_envs_specific_steps_data=eval_containers_steps_data_v1,
    #                                                   eval_envs_specific_steps_means=eval_containers_steps_means_v1,
    #                                                   eval_envs_specific_steps_stds=eval_containers_steps_stds_v1,
    #                                                   ylim_rew=ylim_rew,
    #                                                   file_name="./steps_cluster_train_mult_env_avg_" + suffix,
    #                                                   markevery=3, optimal_steps=5, sample_step=10
    #                                                   )


    # ylim_rew = (min([min(avg_train_rewards_means_v1 - avg_train_rewards_stds_v1)]),
    #             max([max(avg_train_rewards_means_v1 + avg_train_rewards_stds_v1)]))
    # ylim_step = (min([min(avg_train_steps_means_v1 - avg_train_steps_stds_v1)]),
    #              max([max(avg_train_steps_means_v1 + avg_train_steps_stds_v1)]))

    # ylim_rew = (min([min(rewards_means_v1 - rewards_stds_v1)]),
    #             max([max(rewards_means_v1 + rewards_stds_v1)]))
    # ylim_step = (min([min(steps_means_v1 - steps_stds_v1)]),
    #              max([max(steps_means_v1 + steps_stds_v1)]))

    #ylim_rew = (-100, max([max(avg_train_rewards_means_v1 + avg_train_rewards_stds_v1)]))

    return avg_train_steps_data_v1, avg_train_steps_means_v1, avg_train_steps_stds_v1, avg_eval_steps_data_v1, \
           avg_eval_steps_means_v1, avg_eval_steps_stds_v1, \
           avg_train_rewards_data_v1, avg_train_rewards_means_v1, avg_train_rewards_stds_v1, avg_eval_rewards_data_v1, \
           avg_eval_rewards_means_v1, avg_eval_rewards_stds_v1, \
           avg_train_regret_data_v1, avg_train_regret_means_v1, avg_train_regret_stds_v1, avg_eval_regret_data_v1, \
           avg_eval_regret_means_v1, avg_eval_regret_stds_v1, \
           avg_train_opt_frac_data_v1, avg_train_opt_frac_means_v1, avg_train_opt_frac_stds_v1, avg_eval_opt_frac_data_v1, \
           avg_eval_opt_frac_means_v1, avg_eval_opt_frac_stds_v1, \
           train_containers_rewards_data_v1, train_containers_rewards_means_v1, train_containers_rewards_stds_v1, \
           train_containers_flags_data_v1, train_containers_flags_means_v1, train_containers_flags_stds_v1, train_containers_steps_data_v1, \
           train_containers_steps_means_v1, train_containers_steps_stds_v1, train_containers_regret_data_v1, train_containers_regret_means_v1, \
           train_containers_regret_stds_v1, train_containers_opt_frac_data_v1, train_containers_opt_frac_means_v1, train_containers_opt_frac_stds_v1, \
           eval_containers_rewards_data_v1, eval_containers_rewards_means_v1, eval_containers_rewards_stds_v1, \
           eval_containers_flags_data_v1, eval_containers_flags_means_v1, eval_containers_flags_stds_v1, eval_containers_steps_data_v1, \
           eval_containers_steps_means_v1, eval_containers_steps_stds_v1, eval_containers_regret_data_v1, eval_containers_regret_means_v1, \
           eval_containers_regret_stds_v1, eval_containers_opt_frac_data_v1, eval_containers_opt_frac_means_v1, eval_containers_opt_frac_stds_v1


def plot_value_function(model_path: str, env, device):
    model = PPO.load(env=env, load_path=model_path, device=device, agent_config=None)
    print("model loaded!")
    obs = np.zeros((model.agent_config.input_dim,))
    obs = np.array([obs])
    obs_tensor = torch.as_tensor(obs).to(device)
    actions, values, log_prob = model.policy.forward(obs=obs_tensor, deterministic=True, mask_actions = False)
    print(actions)
    print(values)
    print(log_prob)

def plot_avg_comparison(avg_train_steps_data_v1_gensim, avg_train_steps_means_v1_gensim, avg_train_steps_stds_v1_gensim, avg_eval_steps_data_v1_gensim,
    avg_eval_steps_means_v1_gensim, avg_eval_steps_stds_v1_gensim,
    avg_train_rewards_data_v1_gensim, avg_train_rewards_means_v1_gensim, avg_train_rewards_stds_v1_gensim, avg_eval_rewards_data_v1_gensim,
    avg_eval_rewards_means_v1_gensim, avg_eval_rewards_stds_v1_gensim,
    avg_train_regret_data_v1_gensim, avg_train_regret_means_v1_gensim, avg_train_regret_stds_v1_gensim, avg_eval_regret_data_v1_gensim,
    avg_eval_regret_means_v1_gensim, avg_eval_regret_stds_v1_gensim,
    avg_train_opt_frac_data_v1_gensim, avg_train_opt_frac_means_v1_gensim, avg_train_opt_frac_stds_v1_gensim, avg_eval_opt_frac_data_v1_gensim,
    avg_eval_opt_frac_means_v1_gensim, avg_eval_opt_frac_stds_v1_gensim,
    avg_train_steps_data_v1_cluster_20,
    avg_train_steps_means_v1_cluster_20, avg_train_steps_stds_v1_cluster_20, avg_eval_steps_data_v1_cluster_20,
    avg_eval_steps_means_v1_cluster_20, avg_eval_steps_stds_v1_cluster_20,
    avg_train_rewards_data_v1_cluster_20, avg_train_rewards_means_v1_cluster_20,
    avg_train_rewards_stds_v1_cluster_20, avg_eval_rewards_data_v1_cluster_20,
    avg_eval_rewards_means_v1_cluster_20, avg_eval_rewards_stds_v1_cluster_20,
    avg_train_regret_data_v1_cluster_20, avg_train_regret_means_v1_cluster_20,
    avg_train_regret_stds_v1_cluster_20, avg_eval_regret_data_v1_cluster_20,
    avg_eval_regret_means_v1_cluster_20, avg_eval_regret_stds_v1_cluster_20,
    avg_train_opt_frac_data_v1_cluster_20, avg_train_opt_frac_means_v1_cluster_20,
    avg_train_opt_frac_stds_v1_cluster_20, avg_eval_opt_frac_data_v1_cluster_20,
    avg_eval_opt_frac_means_v1_cluster_20, avg_eval_opt_frac_stds_v1_cluster_20,
    avg_train_steps_data_v1_cluster_1,
    avg_train_steps_means_v1_cluster_1, avg_train_steps_stds_v1_cluster_1, avg_eval_steps_data_v1_cluster_1,
    avg_eval_steps_means_v1_cluster_1, avg_eval_steps_stds_v1_cluster_1,
    avg_train_rewards_data_v1_cluster_1, avg_train_rewards_means_v1_cluster_1,
    avg_train_rewards_stds_v1_cluster_1, avg_eval_rewards_data_v1_cluster_1,
    avg_eval_rewards_means_v1_cluster_1, avg_eval_rewards_stds_v1_cluster_1,
    avg_train_regret_data_v1_cluster_1, avg_train_regret_means_v1_cluster_1,
    avg_train_regret_stds_v1_cluster_1, avg_eval_regret_data_v1_cluster_1,
    avg_eval_regret_means_v1_cluster_1, avg_eval_regret_stds_v1_cluster_1,
    avg_train_opt_frac_data_v1_cluster_1, avg_train_opt_frac_means_v1_cluster_1,
    avg_train_opt_frac_stds_v1_cluster_1, avg_eval_opt_frac_data_v1_cluster_1,
    avg_eval_opt_frac_means_v1_cluster_1, avg_eval_opt_frac_stds_v1_cluster_1
                        ):
    # ylim_rew = (1, 15)
    # plotting_util.plot_steps_train_cluster_avg_comparison(
    #     train_avg_steps_data_1_gensim=avg_train_steps_data_v1_gensim, train_avg_steps_means_1_gensim=avg_train_steps_means_v1_gensim,
    #     train_avg_steps_stds_1_gensim=avg_train_steps_stds_v1_gensim, eval_avg_steps_data_1_gensim=avg_eval_steps_data_v1_gensim,
    #     eval_avg_steps_means_1_gensim=avg_eval_steps_means_v1_gensim, eval_avg_steps_stds_1_gensim=avg_eval_steps_stds_v1_gensim,
    #     train_avg_steps_data_1_cluster_20=avg_train_steps_data_v1_cluster_20, train_avg_steps_means_1_cluster_20=avg_train_steps_means_v1_cluster_20,
    #     train_avg_steps_stds_1_cluster_20=avg_train_steps_stds_v1_cluster_20,
    #     eval_avg_steps_data_1_cluster_20=avg_eval_steps_data_v1_cluster_20, eval_avg_steps_means_1_cluster_20=avg_eval_steps_means_v1_cluster_20,
    #     eval_avg_steps_stds_1_cluster_20=avg_eval_steps_stds_v1_cluster_20,
    #     train_avg_steps_data_1_cluster_1=avg_train_steps_data_v1_cluster_1, train_avg_steps_means_1_cluster_1=avg_train_steps_means_v1_cluster_1,
    #     train_avg_steps_stds_1_cluster_1=avg_train_steps_stds_v1_cluster_1, eval_avg_steps_data_1_cluster_1=avg_eval_steps_data_v1_cluster_1,
    #     eval_avg_steps_means_1_cluster_1=avg_eval_steps_means_v1_cluster_1,
    #     eval_avg_steps_stds_1_cluster_1=avg_eval_steps_stds_v1_cluster_1,
    #     ylim_rew=ylim_rew, file_name="avg_steps_comparison", markevery=3, optimal_steps=5, sample_step=10
    # )
    #
    # plotting_util.plot_steps_train_cluster_avg_comparison_eval_only(
    #     eval_avg_steps_data_1_gensim=avg_eval_steps_data_v1_gensim,
    #     eval_avg_steps_means_1_gensim=avg_eval_steps_means_v1_gensim,
    #     eval_avg_steps_stds_1_gensim=avg_eval_steps_stds_v1_gensim,
    #     eval_avg_steps_data_1_cluster_20=avg_eval_steps_data_v1_cluster_20,
    #     eval_avg_steps_means_1_cluster_20=avg_eval_steps_means_v1_cluster_20,
    #     eval_avg_steps_stds_1_cluster_20=avg_eval_steps_stds_v1_cluster_20,
    #     eval_avg_steps_data_1_cluster_1=avg_eval_steps_data_v1_cluster_1,
    #     eval_avg_steps_means_1_cluster_1=avg_eval_steps_means_v1_cluster_1,
    #     eval_avg_steps_stds_1_cluster_1=avg_eval_steps_stds_v1_cluster_1,
    #     ylim_rew=ylim_rew, file_name="avg_steps_comparison_eval_only", markevery=3, optimal_steps=5, sample_step=10
    # )

    ylim_rew = (-13, 11)

    # plotting_util.plot_rewards_train_cluster_avg_comparison(
    #     train_avg_rewards_data_1_gensim=avg_train_rewards_data_v1_gensim,
    #     train_avg_rewards_means_1_gensim=avg_train_rewards_means_v1_gensim,
    #     train_avg_rewards_stds_1_gensim=avg_train_rewards_stds_v1_gensim,
    #     eval_avg_rewards_data_1_gensim=avg_eval_rewards_data_v1_gensim,
    #     eval_avg_rewards_means_1_gensim=avg_eval_rewards_means_v1_gensim,
    #     eval_avg_rewards_stds_1_gensim=avg_eval_rewards_stds_v1_gensim,
    #     train_avg_rewards_data_1_cluster_20=avg_train_rewards_data_v1_cluster_20,
    #     train_avg_rewards_means_1_cluster_20=avg_train_rewards_means_v1_cluster_20,
    #     train_avg_rewards_stds_1_cluster_20=avg_train_rewards_stds_v1_cluster_20,
    #     eval_avg_rewards_data_1_cluster_20=avg_eval_rewards_data_v1_cluster_20,
    #     eval_avg_rewards_means_1_cluster_20=avg_eval_rewards_means_v1_cluster_20,
    #     eval_avg_rewards_stds_1_cluster_20=avg_eval_rewards_stds_v1_cluster_20,
    #     train_avg_rewards_data_1_cluster_1=avg_train_rewards_data_v1_cluster_1,
    #     train_avg_rewards_means_1_cluster_1=avg_train_rewards_means_v1_cluster_1,
    #     train_avg_rewards_stds_1_cluster_1=avg_train_rewards_stds_v1_cluster_1,
    #     eval_avg_rewards_data_1_cluster_1=avg_eval_rewards_data_v1_cluster_1,
    #     eval_avg_rewards_means_1_cluster_1=avg_eval_rewards_means_v1_cluster_1,
    #     eval_avg_rewards_stds_1_cluster_1=avg_eval_rewards_stds_v1_cluster_1,
    #     ylim_rew=ylim_rew, file_name="avg_rewards_comparison", markevery=3, sample_step=10,
    #     plot_opt=False
    # )
    #
    # plotting_util.plot_rewards_train_cluster_avg_comparison_eval_only(
    #     eval_avg_rewards_data_1_gensim=avg_eval_rewards_data_v1_gensim,
    #     eval_avg_rewards_means_1_gensim=avg_eval_rewards_means_v1_gensim,
    #     eval_avg_rewards_stds_1_gensim=avg_eval_rewards_stds_v1_gensim,
    #     eval_avg_rewards_data_1_cluster_20=avg_eval_rewards_data_v1_cluster_20,
    #     eval_avg_rewards_means_1_cluster_20=avg_eval_rewards_means_v1_cluster_20,
    #     eval_avg_rewards_stds_1_cluster_20=avg_eval_rewards_stds_v1_cluster_20,
    #     eval_avg_rewards_data_1_cluster_1=avg_eval_rewards_data_v1_cluster_1,
    #     eval_avg_rewards_means_1_cluster_1=avg_eval_rewards_means_v1_cluster_1,
    #     eval_avg_rewards_stds_1_cluster_1=avg_eval_rewards_stds_v1_cluster_1,
    #     ylim_rew=ylim_rew, file_name="avg_rewards_comparison_eval_only", markevery=3, sample_step=10,
    #     plot_opt=False
    # )

    # ylim_rew = (-1, 1.1)
    #
    # plotting_util.plot_rewards_train_cluster_avg_comparison(
    #     train_avg_rewards_data_1_gensim=avg_train_opt_frac_data_v1_gensim,
    #     train_avg_rewards_means_1_gensim=avg_train_opt_frac_means_v1_gensim,
    #     train_avg_rewards_stds_1_gensim=avg_train_opt_frac_stds_v1_gensim,
    #     eval_avg_rewards_data_1_gensim=avg_eval_opt_frac_data_v1_gensim,
    #     eval_avg_rewards_means_1_gensim=avg_eval_opt_frac_means_v1_gensim,
    #     eval_avg_rewards_stds_1_gensim=avg_eval_opt_frac_stds_v1_gensim,
    #     train_avg_rewards_data_1_cluster_20=avg_train_opt_frac_data_v1_cluster_20,
    #     train_avg_rewards_means_1_cluster_20=avg_train_opt_frac_means_v1_cluster_20,
    #     train_avg_rewards_stds_1_cluster_20=avg_train_opt_frac_stds_v1_cluster_20,
    #     eval_avg_rewards_data_1_cluster_20=avg_eval_opt_frac_data_v1_cluster_20,
    #     eval_avg_rewards_means_1_cluster_20=avg_eval_opt_frac_means_v1_cluster_20,
    #     eval_avg_rewards_stds_1_cluster_20=avg_eval_opt_frac_stds_v1_cluster_20,
    #     train_avg_rewards_data_1_cluster_1=avg_train_opt_frac_data_v1_cluster_1,
    #     train_avg_rewards_means_1_cluster_1=avg_train_opt_frac_means_v1_cluster_1,
    #     train_avg_rewards_stds_1_cluster_1=avg_train_opt_frac_stds_v1_cluster_1,
    #     eval_avg_rewards_data_1_cluster_1=avg_eval_opt_frac_data_v1_cluster_1,
    #     eval_avg_rewards_means_1_cluster_1=avg_eval_opt_frac_means_v1_cluster_1,
    #     eval_avg_rewards_stds_1_cluster_1=avg_eval_opt_frac_stds_v1_cluster_1,
    #     ylim_rew=ylim_rew, file_name="avg_opt_frac_comparison", markevery=3, optimal_reward=1, sample_step=10,
    #     plot_opt=True
    # )
    #
    # plotting_util.plot_rewards_train_cluster_avg_comparison_eval_only(
    #     eval_avg_rewards_data_1_gensim=avg_eval_opt_frac_data_v1_gensim,
    #     eval_avg_rewards_means_1_gensim=avg_eval_opt_frac_means_v1_gensim,
    #     eval_avg_rewards_stds_1_gensim=avg_eval_opt_frac_stds_v1_gensim,
    #     eval_avg_rewards_data_1_cluster_20=avg_eval_opt_frac_data_v1_cluster_20,
    #     eval_avg_rewards_means_1_cluster_20=avg_eval_opt_frac_means_v1_cluster_20,
    #     eval_avg_rewards_stds_1_cluster_20=avg_eval_opt_frac_stds_v1_cluster_20,
    #     eval_avg_rewards_data_1_cluster_1=avg_eval_opt_frac_data_v1_cluster_1,
    #     eval_avg_rewards_means_1_cluster_1=avg_eval_opt_frac_means_v1_cluster_1,
    #     eval_avg_rewards_stds_1_cluster_1=avg_eval_opt_frac_stds_v1_cluster_1,
    #     ylim_rew=ylim_rew, file_name="avg_opt_frac_comparison_eval_only", markevery=3, optimal_reward=1, sample_step=10,
    #     plot_opt=True
    # )

    ylim_rew = (-0.5, 20)
    plotting_util.plot_regret_train_cluster_avg_comparison(
        train_avg_regret_data_1_gensim=avg_train_regret_data_v1_gensim,
        train_avg_regret_means_1_gensim=avg_train_regret_means_v1_gensim,
        train_avg_regret_stds_1_gensim=avg_train_regret_stds_v1_gensim,
        eval_avg_regret_data_1_gensim=avg_eval_regret_data_v1_gensim,
        eval_avg_regret_means_1_gensim=avg_eval_regret_means_v1_gensim,
        eval_avg_regret_stds_1_gensim=avg_eval_regret_stds_v1_gensim,
        train_avg_regret_data_1_cluster_20=avg_train_regret_data_v1_cluster_20,
        train_avg_regret_means_1_cluster_20=avg_train_regret_means_v1_cluster_20,
        train_avg_regret_stds_1_cluster_20=avg_train_regret_stds_v1_cluster_20,
        eval_avg_regret_data_1_cluster_20=avg_eval_regret_data_v1_cluster_20,
        eval_avg_regret_means_1_cluster_20=avg_eval_regret_means_v1_cluster_20,
        eval_avg_regret_stds_1_cluster_20=avg_eval_regret_stds_v1_cluster_20,
        train_avg_regret_data_1_cluster_1=avg_train_regret_data_v1_cluster_1,
        train_avg_regret_means_1_cluster_1=avg_train_regret_means_v1_cluster_1,
        train_avg_regret_stds_1_cluster_1=avg_train_regret_stds_v1_cluster_1,
        eval_avg_regret_data_1_cluster_1=avg_eval_regret_data_v1_cluster_1,
        eval_avg_regret_means_1_cluster_1=avg_eval_regret_means_v1_cluster_1,
        eval_avg_regret_stds_1_cluster_1=avg_eval_regret_stds_v1_cluster_1,
        ylim_rew=ylim_rew, file_name="avg_regret_comparison", markevery=3, optimal_regret=0, sample_step=10,
        plot_opt=True
    )

    plotting_util.plot_regret_train_cluster_avg_comparison_eval_only(
        eval_avg_regret_data_1_gensim=avg_eval_regret_data_v1_gensim,
        eval_avg_regret_means_1_gensim=avg_eval_regret_means_v1_gensim,
        eval_avg_regret_stds_1_gensim=avg_eval_regret_stds_v1_gensim,
        eval_avg_regret_data_1_cluster_20=avg_eval_regret_data_v1_cluster_20,
        eval_avg_regret_means_1_cluster_20=avg_eval_regret_means_v1_cluster_20,
        eval_avg_regret_stds_1_cluster_20=avg_eval_regret_stds_v1_cluster_20,
        eval_avg_regret_data_1_cluster_1=avg_eval_regret_data_v1_cluster_1,
        eval_avg_regret_means_1_cluster_1=avg_eval_regret_means_v1_cluster_1,
        eval_avg_regret_stds_1_cluster_1=avg_eval_regret_stds_v1_cluster_1,
        ylim_rew=ylim_rew, file_name="avg_regret_comparison_eval_only", markevery=3, optimal_regret=0, sample_step=10,
        plot_opt=True
    )


if __name__ == '__main__':
    # containers_configs = EnvConfigGenerator.get_all_envs_containers_config(
    #     "/home/kim/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/random_many/")
    # flags_configs = EnvConfigGenerator.get_all_envs_flags_config(
    #     "/home/kim/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/random_many/")
    # eval_env_containers_configs = EnvConfigGenerator.get_all_envs_containers_config(
    #     "/home/kim/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/random_many_2/")
    # eval_env_flags_configs = EnvConfigGenerator.get_all_envs_flags_config(
    #     "/home/kim/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/random_many_2/")
    containers_configs = EnvConfigGenerator.get_all_envs_containers_config(
        "/Users/kimham/workspace/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/random_many/")
    flags_configs = EnvConfigGenerator.get_all_envs_flags_config(
        "/Users/kimham/workspace/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/random_many/")
    eval_env_containers_configs = EnvConfigGenerator.get_all_envs_containers_config(
        "/Users/kimham/workspace/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/random_many_2/")
    eval_env_flags_configs = EnvConfigGenerator.get_all_envs_flags_config(
        "/Users/kimham/workspace/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/random_many_2/")
    # base_path = "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/password_cracking/gym-pycr-pwcrack/examples/random_many/training/v1/cluster/ppo_baseline/results/data/"
    # base_path = "/home/kim/pycr/python-envs/minigames/network_intrusion/password_cracking/gym-pycr-pwcrack/examples/random_many/training/v1/generated_simulation/ppo_baseline/results_backup/data/"

    base_path = "/Users/kimham/workspace/pycr/python-envs/minigames/network_intrusion/password_cracking/gym-pycr-pwcrack/examples/random_many/training/v1/generated_simulation/ppo_baseline/results/data/"
    avg_train_steps_data_v1_gensim, avg_train_steps_means_v1_gensim, avg_train_steps_stds_v1_gensim, avg_eval_steps_data_v1_gensim, \
    avg_eval_steps_means_v1_gensim, avg_eval_steps_stds_v1_gensim, \
    avg_train_rewards_data_v1_gensim, avg_train_rewards_means_v1_gensim, avg_train_rewards_stds_v1_gensim, avg_eval_rewards_data_v1_gensim, \
    avg_eval_rewards_means_v1_gensim, avg_eval_rewards_stds_v1_gensim, \
    avg_train_regret_data_v1_gensim, avg_train_regret_means_v1_gensim, avg_train_regret_stds_v1_gensim, avg_eval_regret_data_v1_gensim, \
    avg_eval_regret_means_v1_gensim, avg_eval_regret_stds_v1_gensim, \
    avg_train_opt_frac_data_v1_gensim, avg_train_opt_frac_means_v1_gensim, avg_train_opt_frac_stds_v1_gensim, avg_eval_opt_frac_data_v1_gensim, \
    avg_eval_opt_frac_means_v1_gensim, avg_eval_opt_frac_stds_v1_gensim, \
    train_containers_rewards_data_v1_gensim, train_containers_rewards_means_v1_gensim, train_containers_rewards_stds_v1_gensim, \
    train_containers_flags_data_v1_gensim, train_containers_flags_means_v1_gensim, train_containers_flags_stds_v1_gensim, train_containers_steps_data_v1_gensim, \
    train_containers_steps_means_v1_gensim, train_containers_steps_stds_v1_gensim, train_containers_regret_data_v1_gensim, train_containers_regret_means_v1_gensim, \
    train_containers_regret_stds_v1_gensim, train_containers_opt_frac_data_v1_gensim, train_containers_opt_frac_means_v1_gensim, train_containers_opt_frac_stds_v1_gensim, \
    eval_containers_rewards_data_v1_gensim, eval_containers_rewards_means_v1_gensim, eval_containers_rewards_stds_v1_gensim, \
    eval_containers_flags_data_v1_gensim, eval_containers_flags_means_v1_gensim, eval_containers_flags_stds_v1_gensim, eval_containers_steps_data_v1_gensim, \
    eval_containers_steps_means_v1_gensim, eval_containers_steps_stds_v1_gensim, eval_containers_regret_data_v1_gensim, eval_containers_regret_means_v1_gensim, \
    eval_containers_regret_stds_v1_gensim, eval_containers_opt_frac_data_v1_gensim, eval_containers_opt_frac_means_v1_gensim, eval_containers_opt_frac_stds_v1_gensim, \
        = plot_cluster_train(train_containers_configs=containers_configs, eval_containers_configs=eval_env_containers_configs, base_path=base_path, suffix="gensim")

    base_path = "/Users/kimham/workspace/pycr/python-envs/minigames/network_intrusion/password_cracking/gym-pycr-pwcrack/examples/random_many/training/v1/cluster/ppo_baseline/results/data/"
    avg_train_steps_data_v1_cluster_20, avg_train_steps_means_v1_cluster_20, avg_train_steps_stds_v1_cluster_20, avg_eval_steps_data_v1_cluster_20, \
    avg_eval_steps_means_v1_cluster_20, avg_eval_steps_stds_v1_cluster_20, \
    avg_train_rewards_data_v1_cluster_20, avg_train_rewards_means_v1_cluster_20, avg_train_rewards_stds_v1_cluster_20, avg_eval_rewards_data_v1_cluster_20, \
    avg_eval_rewards_means_v1_cluster_20, avg_eval_rewards_stds_v1_cluster_20, \
    avg_train_regret_data_v1_cluster_20, avg_train_regret_means_v1_cluster_20, avg_train_regret_stds_v1_cluster_20, avg_eval_regret_data_v1_cluster_20, \
    avg_eval_regret_means_v1_cluster_20, avg_eval_regret_stds_v1_cluster_20, \
    avg_train_opt_frac_data_v1_cluster_20, avg_train_opt_frac_means_v1_cluster_20, avg_train_opt_frac_stds_v1_cluster_20, avg_eval_opt_frac_data_v1_cluster_20, \
    avg_eval_opt_frac_means_v1_cluster_20, avg_eval_opt_frac_stds_v1_cluster_20, \
    train_containers_rewards_data_v1_cluster_20, train_containers_rewards_means_v1_cluster_20, train_containers_rewards_stds_v1_cluster_20, \
    train_containers_flags_data_v1_cluster_20, train_containers_flags_means_v1_cluster_20, train_containers_flags_stds_v1_cluster_20, train_containers_steps_data_v1_cluster_20, \
    train_containers_steps_means_v1_cluster_20, train_containers_steps_stds_v1_cluster_20, train_containers_regret_data_v1_cluster_20, train_containers_regret_means_v1_cluster_20, \
    train_containers_regret_stds_v1_cluster_20, train_containers_opt_frac_data_v1_cluster_20, train_containers_opt_frac_means_v1_cluster_20, train_containers_opt_frac_stds_v1_cluster_20, \
    eval_containers_rewards_data_v1_cluster_20, eval_containers_rewards_means_v1_cluster_20, eval_containers_rewards_stds_v1_cluster_20, \
    eval_containers_flags_data_v1_cluster_20, eval_containers_flags_means_v1_cluster_20, eval_containers_flags_stds_v1_cluster_20, eval_containers_steps_data_v1_cluster_20, \
    eval_containers_steps_means_v1_cluster_20, eval_containers_steps_stds_v1_cluster_20, eval_containers_regret_data_v1_cluster_20, eval_containers_regret_means_v1_cluster_20, \
    eval_containers_regret_stds_v1_cluster_20, eval_containers_opt_frac_data_v1_cluster_20, eval_containers_opt_frac_means_v1_cluster_20, eval_containers_opt_frac_stds_v1_cluster_20 \
        = \
        plot_cluster_train(train_containers_configs=containers_configs, eval_containers_configs=eval_env_containers_configs,
                       base_path=base_path, suffix="cluster_20")

    base_path = "/Users/kimham/workspace/pycr/python-envs/minigames/network_intrusion/password_cracking/gym-pycr-pwcrack/examples/random_many/training/v1/cluster_1/ppo_baseline/results/data/"
    ips = ["172.18.28.151", "172.18.33.23"]
    avg_train_steps_data_v1_cluster_1, avg_train_steps_means_v1_cluster_1, avg_train_steps_stds_v1_cluster_1, avg_eval_steps_data_v1_cluster_1, \
    avg_eval_steps_means_v1_cluster_1, avg_eval_steps_stds_v1_cluster_1, \
    avg_train_rewards_data_v1_cluster_1, avg_train_rewards_means_v1_cluster_1, avg_train_rewards_stds_v1_cluster_1, avg_eval_rewards_data_v1_cluster_1, \
    avg_eval_rewards_means_v1_cluster_1, avg_eval_rewards_stds_v1_cluster_1, \
    avg_train_regret_data_v1_cluster_1, avg_train_regret_means_v1_cluster_1, avg_train_regret_stds_v1_cluster_1, avg_eval_regret_data_v1_cluster_1, \
    avg_eval_regret_means_v1_cluster_1, avg_eval_regret_stds_v1_cluster_1, \
    avg_train_opt_frac_data_v1_cluster_1, avg_train_opt_frac_means_v1_cluster_1, avg_train_opt_frac_stds_v1_cluster_1, avg_eval_opt_frac_data_v1_cluster_1, \
    avg_eval_opt_frac_means_v1_cluster_1, avg_eval_opt_frac_stds_v1_cluster_1, \
    train_containers_rewards_data_v1_cluster_1, train_containers_rewards_means_v1_cluster_1, train_containers_rewards_stds_v1_cluster_1, \
    train_containers_flags_data_v1_cluster_1, train_containers_flags_means_v1_cluster_1, train_containers_flags_stds_v1_cluster_1, train_containers_steps_data_v1_cluster_1, \
    train_containers_steps_means_v1_cluster_1, train_containers_steps_stds_v1_cluster_1, train_containers_regret_data_v1_cluster_1, train_containers_regret_means_v1_cluster_1, \
    train_containers_regret_stds_v1_cluster_1, train_containers_opt_frac_data_v1_cluster_1, train_containers_opt_frac_means_v1_cluster_1, train_containers_opt_frac_stds_v1_cluster_1, \
    eval_containers_rewards_data_v1_cluster_1, eval_containers_rewards_means_v1_cluster_1, eval_containers_rewards_stds_v1_cluster_1, \
    eval_containers_flags_data_v1_cluster_1, eval_containers_flags_means_v1_cluster_1, eval_containers_flags_stds_v1_cluster_1, eval_containers_steps_data_v1_cluster_1, \
    eval_containers_steps_means_v1_cluster_1, eval_containers_steps_stds_v1_cluster_1, eval_containers_regret_data_v1_cluster_1, eval_containers_regret_means_v1_cluster_1, \
    eval_containers_regret_stds_v1_cluster_1, eval_containers_opt_frac_data_v1_cluster_1, eval_containers_opt_frac_means_v1_cluster_1, eval_containers_opt_frac_stds_v1_cluster_1 \
        = \
        plot_cluster_train(train_containers_configs=containers_configs, eval_containers_configs=eval_env_containers_configs,
                       base_path=base_path, suffix="cluster_1", ips=ips, eval_ips=None)

    # plot_avg_comparison(
    #     avg_train_steps_data_v1_gensim, avg_train_steps_means_v1_gensim, avg_train_steps_stds_v1_gensim,
    #     avg_eval_steps_data_v1_gensim,
    #     avg_eval_steps_means_v1_gensim, avg_eval_steps_stds_v1_gensim,
    #     avg_train_rewards_data_v1_gensim, avg_train_rewards_means_v1_gensim, avg_train_rewards_stds_v1_gensim,
    #     avg_eval_rewards_data_v1_gensim,
    #     avg_eval_rewards_means_v1_gensim, avg_eval_rewards_stds_v1_gensim,
    #     avg_train_regret_data_v1_gensim, avg_train_regret_means_v1_gensim, avg_train_regret_stds_v1_gensim,
    #     avg_eval_regret_data_v1_gensim,
    #     avg_eval_regret_means_v1_gensim, avg_eval_regret_stds_v1_gensim,
    #     avg_train_opt_frac_data_v1_gensim, avg_train_opt_frac_means_v1_gensim, avg_train_opt_frac_stds_v1_gensim,
    #     avg_eval_opt_frac_data_v1_gensim,
    #     avg_eval_opt_frac_means_v1_gensim, avg_eval_opt_frac_stds_v1_gensim,
    #     avg_train_steps_data_v1_cluster_20, avg_train_steps_means_v1_cluster_20, avg_train_steps_stds_v1_cluster_20,
    #     avg_eval_steps_data_v1_cluster_20,
    #     avg_eval_steps_means_v1_cluster_20, avg_eval_steps_stds_v1_cluster_20,
    #     avg_train_rewards_data_v1_cluster_20, avg_train_rewards_means_v1_cluster_20,
    #     avg_train_rewards_stds_v1_cluster_20, avg_eval_rewards_data_v1_cluster_20,
    #     avg_eval_rewards_means_v1_cluster_20, avg_eval_rewards_stds_v1_cluster_20,
    #     avg_train_regret_data_v1_cluster_20, avg_train_regret_means_v1_cluster_20, avg_train_regret_stds_v1_cluster_20,
    #     avg_eval_regret_data_v1_cluster_20,
    #     avg_eval_regret_means_v1_cluster_20, avg_eval_regret_stds_v1_cluster_20,
    #     avg_train_opt_frac_data_v1_cluster_20, avg_train_opt_frac_means_v1_cluster_20,
    #     avg_train_opt_frac_stds_v1_cluster_20, avg_eval_opt_frac_data_v1_cluster_20,
    #     avg_eval_opt_frac_means_v1_cluster_20, avg_eval_opt_frac_stds_v1_cluster_20,
    #     avg_train_steps_data_v1_cluster_1, avg_train_steps_means_v1_cluster_1, avg_train_steps_stds_v1_cluster_1,
    #     avg_eval_steps_data_v1_cluster_1,
    #     avg_eval_steps_means_v1_cluster_1, avg_eval_steps_stds_v1_cluster_1,
    #     avg_train_rewards_data_v1_cluster_1, avg_train_rewards_means_v1_cluster_1, avg_train_rewards_stds_v1_cluster_1,
    #     avg_eval_rewards_data_v1_cluster_1,
    #     avg_eval_rewards_means_v1_cluster_1, avg_eval_rewards_stds_v1_cluster_1,
    #     avg_train_regret_data_v1_cluster_1, avg_train_regret_means_v1_cluster_1, avg_train_regret_stds_v1_cluster_1,
    #     avg_eval_regret_data_v1_cluster_1,
    #     avg_eval_regret_means_v1_cluster_1, avg_eval_regret_stds_v1_cluster_1,
    #     avg_train_opt_frac_data_v1_cluster_1, avg_train_opt_frac_means_v1_cluster_1,
    #     avg_train_opt_frac_stds_v1_cluster_1, avg_eval_opt_frac_data_v1_cluster_1,
    #     avg_eval_opt_frac_means_v1_cluster_1, avg_eval_opt_frac_stds_v1_cluster_1
    # )

    plotting_util.plot_mega(
        avg_train_opt_frac_data_v1_gensim, avg_train_opt_frac_means_v1_gensim, avg_train_opt_frac_stds_v1_gensim,
        avg_eval_opt_frac_data_v1_gensim, avg_eval_opt_frac_means_v1_gensim, avg_eval_opt_frac_stds_v1_gensim,
        train_containers_opt_frac_data_v1_gensim, train_containers_opt_frac_means_v1_gensim,
        train_containers_opt_frac_stds_v1_gensim, eval_containers_opt_frac_data_v1_gensim,
        eval_containers_opt_frac_means_v1_gensim, eval_containers_opt_frac_stds_v1_gensim,

        avg_train_regret_data_v1_gensim, avg_train_regret_means_v1_gensim, avg_train_regret_stds_v1_gensim,
        avg_eval_regret_data_v1_gensim, avg_eval_regret_means_v1_gensim, avg_eval_regret_stds_v1_gensim,
        train_containers_regret_data_v1_gensim, train_containers_regret_means_v1_gensim,
        train_containers_regret_stds_v1_gensim, eval_containers_regret_data_v1_gensim,
        eval_containers_regret_means_v1_gensim, eval_containers_regret_stds_v1_gensim,

        avg_train_steps_data_v1_gensim, avg_train_steps_means_v1_gensim, avg_train_steps_stds_v1_gensim,
        avg_eval_steps_data_v1_gensim, avg_eval_steps_means_v1_gensim, avg_eval_steps_stds_v1_gensim,
        train_containers_steps_data_v1_gensim, train_containers_steps_means_v1_gensim,
        train_containers_steps_stds_v1_gensim, eval_containers_steps_data_v1_gensim,
        eval_containers_steps_means_v1_gensim, eval_containers_steps_stds_v1_gensim,

        avg_train_opt_frac_data_v1_cluster_20, avg_train_opt_frac_means_v1_cluster_20, avg_train_opt_frac_stds_v1_cluster_20,
        avg_eval_opt_frac_data_v1_cluster_20, avg_eval_opt_frac_means_v1_cluster_20, avg_eval_opt_frac_stds_v1_cluster_20,
        train_containers_opt_frac_data_v1_cluster_20, train_containers_opt_frac_means_v1_cluster_20,
        train_containers_opt_frac_stds_v1_cluster_20, eval_containers_opt_frac_data_v1_cluster_20,
        eval_containers_opt_frac_means_v1_cluster_20, eval_containers_opt_frac_stds_v1_cluster_20,

        avg_train_regret_data_v1_cluster_20, avg_train_regret_means_v1_cluster_20, avg_train_regret_stds_v1_cluster_20,
        avg_eval_regret_data_v1_cluster_20, avg_eval_regret_means_v1_cluster_20, avg_eval_regret_stds_v1_cluster_20,
        train_containers_regret_data_v1_cluster_20, train_containers_regret_means_v1_cluster_20,
        train_containers_regret_stds_v1_cluster_20, eval_containers_regret_data_v1_cluster_20,
        eval_containers_regret_means_v1_cluster_20, eval_containers_regret_stds_v1_cluster_20,

        avg_train_steps_data_v1_cluster_20, avg_train_steps_means_v1_cluster_20, avg_train_steps_stds_v1_cluster_20,
        avg_eval_steps_data_v1_cluster_20, avg_eval_steps_means_v1_cluster_20, avg_eval_steps_stds_v1_cluster_20,
        train_containers_steps_data_v1_cluster_20, train_containers_steps_means_v1_cluster_20,
        train_containers_steps_stds_v1_cluster_20, eval_containers_steps_data_v1_cluster_20,
        eval_containers_steps_means_v1_cluster_20, eval_containers_steps_stds_v1_cluster_20,


        avg_train_opt_frac_data_v1_cluster_1, avg_train_opt_frac_means_v1_cluster_1,
        avg_train_opt_frac_stds_v1_cluster_1,
        avg_eval_opt_frac_data_v1_cluster_1, avg_eval_opt_frac_means_v1_cluster_1,
        avg_eval_opt_frac_stds_v1_cluster_1,
        train_containers_opt_frac_data_v1_cluster_1, train_containers_opt_frac_means_v1_cluster_1,
        train_containers_opt_frac_stds_v1_cluster_1, eval_containers_opt_frac_data_v1_cluster_1,
        eval_containers_opt_frac_means_v1_cluster_1, eval_containers_opt_frac_stds_v1_cluster_1,

        avg_train_regret_data_v1_cluster_1, avg_train_regret_means_v1_cluster_1, avg_train_regret_stds_v1_cluster_1,
        avg_eval_regret_data_v1_cluster_1, avg_eval_regret_means_v1_cluster_1, avg_eval_regret_stds_v1_cluster_1,
        train_containers_regret_data_v1_cluster_1, train_containers_regret_means_v1_cluster_1,
        train_containers_regret_stds_v1_cluster_1, eval_containers_regret_data_v1_cluster_1,
        eval_containers_regret_means_v1_cluster_1, eval_containers_regret_stds_v1_cluster_1,

        avg_train_steps_data_v1_cluster_1, avg_train_steps_means_v1_cluster_1, avg_train_steps_stds_v1_cluster_1,
        avg_eval_steps_data_v1_cluster_1, avg_eval_steps_means_v1_cluster_1, avg_eval_steps_stds_v1_cluster_1,
        train_containers_steps_data_v1_cluster_1, train_containers_steps_means_v1_cluster_1,
        train_containers_steps_stds_v1_cluster_1, eval_containers_steps_data_v1_cluster_1,
        eval_containers_steps_means_v1_cluster_1, eval_containers_steps_stds_v1_cluster_1,

        ylim_rew=(-0.5,1.25), file_name="mega_20_dr_20_1", markevery=100000, optimal_steps = 10, optimal_reward = 1, sample_step = 10,
        plot_opt=True, ylim_reg=(-2.5,36.5), ylim_step=(1, 20), linewidth=0.7)

    # plotting_util.plot_all_train_cluster_avg_comparison_eval_only(
    #         eval_avg_rewards_data_1_gensim=avg_eval_opt_frac_data_v1_gensim,
    #         eval_avg_rewards_means_1_gensim=avg_eval_opt_frac_means_v1_gensim,
    #         eval_avg_rewards_stds_1_gensim=avg_eval_opt_frac_stds_v1_gensim,
    #         eval_avg_rewards_data_1_cluster_20=avg_eval_opt_frac_data_v1_cluster_20,
    #         eval_avg_rewards_means_1_cluster_20=avg_eval_opt_frac_means_v1_cluster_20,
    #         eval_avg_rewards_stds_1_cluster_20=avg_eval_opt_frac_stds_v1_cluster_20,
    #         eval_avg_rewards_data_1_cluster_1=avg_eval_opt_frac_data_v1_cluster_1,
    #         eval_avg_rewards_means_1_cluster_1=avg_eval_opt_frac_means_v1_cluster_1,
    #         eval_avg_rewards_stds_1_cluster_1=avg_eval_opt_frac_stds_v1_cluster_1,
    #         eval_avg_regret_data_1_gensim=avg_eval_regret_data_v1_gensim,
    #         eval_avg_regret_means_1_gensim=avg_eval_regret_means_v1_gensim,
    #         eval_avg_regret_stds_1_gensim=avg_eval_regret_stds_v1_gensim,
    #         eval_avg_regret_data_1_cluster_20=avg_eval_regret_data_v1_cluster_20,
    #         eval_avg_regret_means_1_cluster_20=avg_eval_regret_means_v1_cluster_20,
    #         eval_avg_regret_stds_1_cluster_20=avg_eval_regret_stds_v1_cluster_20,
    #         eval_avg_regret_data_1_cluster_1=avg_eval_regret_data_v1_cluster_1,
    #         eval_avg_regret_means_1_cluster_1=avg_eval_regret_means_v1_cluster_1,
    #         eval_avg_regret_stds_1_cluster_1=avg_eval_regret_stds_v1_cluster_1,
    #         eval_avg_steps_data_1_gensim=avg_eval_steps_data_v1_gensim,
    #         eval_avg_steps_means_1_gensim=avg_eval_steps_means_v1_gensim,
    #         eval_avg_steps_stds_1_gensim=avg_eval_steps_stds_v1_gensim,
    #         eval_avg_steps_data_1_cluster_20=avg_eval_steps_data_v1_cluster_20,
    #         eval_avg_steps_means_1_cluster_20=avg_eval_steps_means_v1_cluster_20,
    #         eval_avg_steps_stds_1_cluster_20=avg_eval_steps_stds_v1_cluster_20,
    #         eval_avg_steps_data_1_cluster_1=avg_eval_steps_data_v1_cluster_1,
    #         eval_avg_steps_means_1_cluster_1=avg_eval_steps_means_v1_cluster_1,
    #         eval_avg_steps_stds_1_cluster_1=avg_eval_steps_stds_v1_cluster_1,
    #     ylim_rew=(-0.5, 1.1), file_name="avg_all_comparison_eval_only", markevery=3, sample_step=10,
    #     plot_opt=True, optimal_reward = 1, optimal_regret=0, ylim_reg=(-0.5,20), ylim_step=(1, 15)
    # )

    # plotting_util.plot_all_train_cluster_avg_comparison(
    #     eval_avg_rewards_data_1_gensim=avg_eval_opt_frac_data_v1_gensim,
    #     eval_avg_rewards_means_1_gensim=avg_eval_opt_frac_means_v1_gensim,
    #     eval_avg_rewards_stds_1_gensim=avg_eval_opt_frac_stds_v1_gensim,
    #     eval_avg_rewards_data_1_cluster_20=avg_eval_opt_frac_data_v1_cluster_20,
    #     eval_avg_rewards_means_1_cluster_20=avg_eval_opt_frac_means_v1_cluster_20,
    #     eval_avg_rewards_stds_1_cluster_20=avg_eval_opt_frac_stds_v1_cluster_20,
    #     eval_avg_rewards_data_1_cluster_1=avg_eval_opt_frac_data_v1_cluster_1,
    #     eval_avg_rewards_means_1_cluster_1=avg_eval_opt_frac_means_v1_cluster_1,
    #     eval_avg_rewards_stds_1_cluster_1=avg_eval_opt_frac_stds_v1_cluster_1,
    #     eval_avg_regret_data_1_gensim=avg_eval_regret_data_v1_gensim,
    #     eval_avg_regret_means_1_gensim=avg_eval_regret_means_v1_gensim,
    #     eval_avg_regret_stds_1_gensim=avg_eval_regret_stds_v1_gensim,
    #     eval_avg_regret_data_1_cluster_20=avg_eval_regret_data_v1_cluster_20,
    #     eval_avg_regret_means_1_cluster_20=avg_eval_regret_means_v1_cluster_20,
    #     eval_avg_regret_stds_1_cluster_20=avg_eval_regret_stds_v1_cluster_20,
    #     eval_avg_regret_data_1_cluster_1=avg_eval_regret_data_v1_cluster_1,
    #     eval_avg_regret_means_1_cluster_1=avg_eval_regret_means_v1_cluster_1,
    #     eval_avg_regret_stds_1_cluster_1=avg_eval_regret_stds_v1_cluster_1,
    #     eval_avg_steps_data_1_gensim=avg_eval_steps_data_v1_gensim,
    #     eval_avg_steps_means_1_gensim=avg_eval_steps_means_v1_gensim,
    #     eval_avg_steps_stds_1_gensim=avg_eval_steps_stds_v1_gensim,
    #     eval_avg_steps_data_1_cluster_20=avg_eval_steps_data_v1_cluster_20,
    #     eval_avg_steps_means_1_cluster_20=avg_eval_steps_means_v1_cluster_20,
    #     eval_avg_steps_stds_1_cluster_20=avg_eval_steps_stds_v1_cluster_20,
    #     eval_avg_steps_data_1_cluster_1=avg_eval_steps_data_v1_cluster_1,
    #     eval_avg_steps_means_1_cluster_1=avg_eval_steps_means_v1_cluster_1,
    #     eval_avg_steps_stds_1_cluster_1=avg_eval_steps_stds_v1_cluster_1,
    #
    #     train_avg_rewards_data_1_gensim=avg_train_opt_frac_data_v1_gensim,
    #     train_avg_rewards_means_1_gensim=avg_train_opt_frac_means_v1_gensim,
    #     train_avg_rewards_stds_1_gensim=avg_train_opt_frac_stds_v1_gensim,
    #     train_avg_rewards_data_1_cluster_20=avg_train_opt_frac_data_v1_cluster_20,
    #     train_avg_rewards_means_1_cluster_20=avg_train_opt_frac_means_v1_cluster_20,
    #     train_avg_rewards_stds_1_cluster_20=avg_train_opt_frac_stds_v1_cluster_20,
    #     train_avg_rewards_data_1_cluster_1=avg_train_opt_frac_data_v1_cluster_1,
    #     train_avg_rewards_means_1_cluster_1=avg_train_opt_frac_means_v1_cluster_1,
    #     train_avg_rewards_stds_1_cluster_1=avg_train_opt_frac_stds_v1_cluster_1,
    #     train_avg_regret_data_1_gensim=avg_train_regret_data_v1_gensim,
    #     train_avg_regret_means_1_gensim=avg_train_regret_means_v1_gensim,
    #     train_avg_regret_stds_1_gensim=avg_train_regret_stds_v1_gensim,
    #     train_avg_regret_data_1_cluster_20=avg_train_regret_data_v1_cluster_20,
    #     train_avg_regret_means_1_cluster_20=avg_train_regret_means_v1_cluster_20,
    #     train_avg_regret_stds_1_cluster_20=avg_train_regret_stds_v1_cluster_20,
    #     train_avg_regret_data_1_cluster_1=avg_train_regret_data_v1_cluster_1,
    #     train_avg_regret_means_1_cluster_1=avg_train_regret_means_v1_cluster_1,
    #     train_avg_regret_stds_1_cluster_1=avg_train_regret_stds_v1_cluster_1,
    #     train_avg_steps_data_1_gensim=avg_train_steps_data_v1_gensim,
    #     train_avg_steps_means_1_gensim=avg_train_steps_means_v1_gensim,
    #     train_avg_steps_stds_1_gensim=avg_train_steps_stds_v1_gensim,
    #     train_avg_steps_data_1_cluster_20=avg_train_steps_data_v1_cluster_20,
    #     train_avg_steps_means_1_cluster_20=avg_train_steps_means_v1_cluster_20,
    #     train_avg_steps_stds_1_cluster_20=avg_train_steps_stds_v1_cluster_20,
    #     train_avg_steps_data_1_cluster_1=avg_train_steps_data_v1_cluster_1,
    #     train_avg_steps_means_1_cluster_1=avg_train_steps_means_v1_cluster_1,
    #     train_avg_steps_stds_1_cluster_1=avg_train_steps_stds_v1_cluster_1,
    #
    #     ylim_rew=(-0.5, 1.1), file_name="avg_all_comparison", markevery=3, sample_step=10,
    #     plot_opt=True, optimal_reward=1, optimal_regret=0, ylim_reg=(-0.5, 20), ylim_step=(1, 15)
    # )


    #base_path = "/home/kim/pycr/python-envs/minigames/network_intrusion/password_cracking/gym-pycr-pwcrack/examples/random_many/training/v1/cluster/ppo_baseline/results/data/"
    # base_path = "/home/kim/pycr/python-envs/minigames/network_intrusion/password_cracking/gym-pycr-pwcrack/examples/random/training/v1/cluster/ppo_baseline/results/data/"
    # model_path = base_path + "0/1608569758.6168735_policy_network.zip"
    # max_num_nodes_train = max(list(map(lambda x: len(x.containers), containers_configs)))
    # max_num_nodes_eval = max(list(map(lambda x: len(x.containers), eval_env_containers_configs)))
    # max_num_nodes = max(max_num_nodes_train, max_num_nodes_eval)
    # num_nodes = max_num_nodes - 1
    # n_envs = 1
    # print(model_path)
    # plot_value_function(model_path=model_path, device="cpu", env=None)

