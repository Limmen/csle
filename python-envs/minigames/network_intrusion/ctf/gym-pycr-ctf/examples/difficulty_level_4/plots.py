from typing import List
import pandas as pd
import numpy as np
import torch
import glob
from gym_pycr_ctf.util.experiments_util import plotting_util
from gym_pycr_ctf.dao.container_config.containers_config import ContainersConfig
from gym_pycr_ctf.envs_model.config.generator.env_config_generator import EnvConfigGenerator
from gym_pycr_ctf.agents.policy_gradient.ppo_baseline.impl.ppo.ppo import PPO
from gym_pycr_ctf.util.experiments_util import util

def parse_data(base_path: str, suffix: str, ips = None, eval_ips = None):
    print(glob.glob(base_path + "0/*_train.csv"))
    ppo_v1_df_0 = pd.read_csv(glob.glob(base_path + "0/*_train.csv")[0])
    ppo_v1_df_999 = pd.read_csv(glob.glob(base_path + "999/*_train.csv")[0])
    ppo_dfs_v1 = [ppo_v1_df_0, ppo_v1_df_999]

    print(ppo_v1_df_0["defender_avg_episode_rewards"].values)
    print(ppo_v1_df_999["defender_avg_episode_rewards"].values)


    running_avg = 10

    # Train avg
    avg_train_rewards_data_v1 = list(
        map(lambda df: util.running_average_list(df["defender_avg_episode_rewards"].values, running_avg), ppo_dfs_v1))
    avg_train_rewards_means_v1 = np.mean(tuple(avg_train_rewards_data_v1), axis=0)
    avg_train_rewards_stds_v1 = np.std(tuple(avg_train_rewards_data_v1), axis=0, ddof=1)

    avg_train_steps_data_v1 = list(
        map(lambda df: util.running_average_list(df["avg_episode_steps"].values, running_avg), ppo_dfs_v1))
    avg_train_steps_means_v1 = np.mean(tuple(avg_train_steps_data_v1), axis=0)
    avg_train_steps_stds_v1 = np.std(tuple(avg_train_steps_data_v1), axis=0, ddof=1)

    avg_train_regret_data_v1 = list(
        map(lambda df: util.running_average_list(df["defender_avg_regret"].values, running_avg), ppo_dfs_v1))
    avg_train_regret_means_v1 = np.mean(tuple(avg_train_regret_data_v1), axis=0)
    avg_train_regret_stds_v1 = np.std(tuple(avg_train_regret_data_v1), axis=0, ddof=1)

    avg_train_opt_frac_data_v1 = list(
        map(lambda df: util.running_average_list(df["defender_avg_opt_frac"].values, running_avg), ppo_dfs_v1))
    avg_train_opt_frac_data_v1 = list(map(lambda x: np.minimum(np.array([1] * len(x)), x), avg_train_opt_frac_data_v1))
    avg_train_opt_frac_means_v1 = np.mean(tuple(avg_train_opt_frac_data_v1), axis=0)
    avg_train_opt_frac_stds_v1 = np.std(tuple(avg_train_opt_frac_data_v1), axis=0, ddof=1)

    avg_train_caught_frac_data_v1 = list(
        map(lambda df: util.running_average_list(df["caught_frac"].values, running_avg), ppo_dfs_v1))
    avg_train_caught_frac_means_v1 = np.mean(tuple(avg_train_caught_frac_data_v1), axis=0)
    avg_train_caught_frac_stds_v1 = np.std(tuple(avg_train_caught_frac_data_v1), axis=0, ddof=1)

    avg_train_early_stopping_frac_data_v1 = list(
        map(lambda df: util.running_average_list(df["early_stopping_frac"].values, running_avg), ppo_dfs_v1))
    avg_train_early_stopping_means_v1 = np.mean(tuple(avg_train_early_stopping_frac_data_v1), axis=0)
    avg_train_early_stopping_stds_v1 = np.std(tuple(avg_train_early_stopping_frac_data_v1), axis=0, ddof=1)

    avg_train_intrusion_frac_data_v1 = list(
        map(lambda df: util.running_average_list(df["intrusion_frac"].values, running_avg), ppo_dfs_v1))
    avg_train_intrusion_means_v1 = np.mean(tuple(avg_train_intrusion_frac_data_v1), axis=0)
    avg_train_intrusion_stds_v1 = np.std(tuple(avg_train_intrusion_frac_data_v1), axis=0, ddof=1)

    # Eval avg
    avg_eval_rewards_data_v1 = list(
        map(lambda df: util.running_average_list(df["defender_eval_avg_episode_rewards"].values, running_avg), ppo_dfs_v1))
    avg_eval_rewards_means_v1 = np.mean(tuple(avg_eval_rewards_data_v1), axis=0)
    avg_eval_rewards_stds_v1 = np.std(tuple(avg_eval_rewards_data_v1), axis=0, ddof=1)

    avg_eval_steps_data_v1 = list(
        map(lambda df: util.running_average_list(df["eval_avg_episode_steps"].values, running_avg), ppo_dfs_v1))
    avg_eval_steps_means_v1 = np.mean(tuple(avg_eval_steps_data_v1), axis=0)
    avg_eval_steps_stds_v1 = np.std(tuple(avg_eval_steps_data_v1), axis=0, ddof=1)

    avg_eval_regret_data_v1 = list(
        map(lambda df: util.running_average_list(df["defender_eval_avg_regret"].values, running_avg), ppo_dfs_v1))
    avg_eval_regret_means_v1 = np.mean(tuple(avg_eval_regret_data_v1), axis=0)
    avg_eval_regret_stds_v1 = np.std(tuple(avg_eval_regret_data_v1), axis=0, ddof=1)

    avg_eval_opt_frac_data_v1 = list(
        map(lambda df: util.running_average_list(df["defender_eval_avg_opt_frac"].values, running_avg), ppo_dfs_v1))
    avg_eval_opt_frac_data_v1 = list(map(lambda x: np.minimum(np.array([1] * len(x)), x), avg_eval_opt_frac_data_v1))
    avg_eval_opt_frac_means_v1 = np.mean(tuple(avg_eval_opt_frac_data_v1), axis=0)
    avg_eval_opt_frac_stds_v1 = np.std(tuple(avg_eval_opt_frac_data_v1), axis=0, ddof=1)

    avg_eval_caught_frac_data_v1 = list(
        map(lambda df: util.running_average_list(df["eval_caught_frac"].values, running_avg), ppo_dfs_v1))
    avg_eval_caught_frac_means_v1 = np.mean(tuple(avg_eval_caught_frac_data_v1), axis=0)
    avg_eval_caught_frac_stds_v1 = np.std(tuple(avg_eval_caught_frac_data_v1), axis=0, ddof=1)

    avg_eval_early_stopping_frac_data_v1 = list(
        map(lambda df: util.running_average_list(df["eval_early_stopping_frac"].values, running_avg), ppo_dfs_v1))
    avg_eval_early_stopping_means_v1 = np.mean(tuple(avg_eval_early_stopping_frac_data_v1), axis=0)
    avg_eval_early_stopping_stds_v1 = np.std(tuple(avg_eval_early_stopping_frac_data_v1), axis=0, ddof=1)

    avg_eval_intrusion_frac_data_v1 = list(
        map(lambda df: util.running_average_list(df["eval_intrusion_frac"].values, running_avg), ppo_dfs_v1))
    avg_eval_intrusion_means_v1 = np.mean(tuple(avg_eval_intrusion_frac_data_v1), axis=0)
    avg_eval_intrusion_stds_v1 = np.std(tuple(avg_eval_intrusion_frac_data_v1), axis=0, ddof=1)

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
           avg_eval_intrusion_stds_v1

def plot_train(avg_train_rewards_data_v1, avg_train_rewards_means_v1, avg_train_rewards_stds_v1, avg_train_steps_data_v1,
    avg_train_steps_means_v1, avg_train_steps_stds_v1, avg_train_regret_data_v1, avg_train_regret_means_v1,
    avg_train_regret_stds_v1, avg_train_opt_frac_data_v1, avg_train_opt_frac_means_v1,
    avg_train_opt_frac_stds_v1, avg_train_caught_frac_data_v1, avg_train_caught_frac_means_v1,
    avg_train_caught_frac_stds_v1, avg_train_early_stopping_frac_data_v1, avg_train_early_stopping_means_v1,
    avg_train_early_stopping_stds_v1, avg_train_intrusion_frac_data_v1, avg_train_intrusion_means_v1,
    avg_train_intrusion_stds_v1, avg_eval_rewards_data_v1, avg_eval_rewards_means_v1, avg_eval_rewards_stds_v1,
    avg_eval_steps_data_v1, avg_eval_steps_means_v1, avg_eval_steps_stds_v1, avg_eval_regret_data_v1,
    avg_eval_regret_means_v1, avg_eval_regret_stds_v1, avg_eval_opt_frac_data_v1, avg_eval_opt_frac_means_v1,
    avg_eval_opt_frac_stds_v1, avg_eval_caught_frac_data_v1, avg_eval_caught_frac_means_v1,
    avg_eval_caught_frac_stds_v1, avg_eval_early_stopping_frac_data_v1, avg_eval_early_stopping_means_v1,
    avg_eval_early_stopping_stds_v1, avg_eval_intrusion_frac_data_v1, avg_eval_intrusion_means_v1,
    avg_eval_intrusion_stds_v1):
    print("plot")
    suffix = "gensim"
    ylim_rew = (-5, 15)
    print(avg_train_rewards_stds_v1)
    plotting_util.plot_rewards_defender(
        avg_train_rewards_data_v1, avg_train_rewards_means_v1, avg_train_rewards_stds_v1,
        ylim_rew=ylim_rew,
        file_name="./rewards_defender_train_" + suffix,
        markevery=3, optimal_reward=16, sample_step = 5
    )

if __name__ == '__main__':
    base_path = "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_4/training/v5/generated_simulation/defender/results_backup/data/"
    avg_train_rewards_data_v1, avg_train_rewards_means_v1, avg_train_rewards_stds_v1, avg_train_steps_data_v1, \
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
    avg_eval_early_stopping_stds_v1, avg_eval_intrusion_frac_data_v1, avg_eval_intrusion_means_v1, \
    avg_eval_intrusion_stds_v1 = parse_data(base_path=base_path, suffix="gensim")

    plot_train(avg_train_rewards_data_v1, avg_train_rewards_means_v1, avg_train_rewards_stds_v1, avg_train_steps_data_v1,
    avg_train_steps_means_v1, avg_train_steps_stds_v1, avg_train_regret_data_v1, avg_train_regret_means_v1,
    avg_train_regret_stds_v1, avg_train_opt_frac_data_v1, avg_train_opt_frac_means_v1,
    avg_train_opt_frac_stds_v1, avg_train_caught_frac_data_v1, avg_train_caught_frac_means_v1,
    avg_train_caught_frac_stds_v1, avg_train_early_stopping_frac_data_v1, avg_train_early_stopping_means_v1,
    avg_train_early_stopping_stds_v1, avg_train_intrusion_frac_data_v1, avg_train_intrusion_means_v1,
    avg_train_intrusion_stds_v1, avg_eval_rewards_data_v1, avg_eval_rewards_means_v1, avg_eval_rewards_stds_v1,
    avg_eval_steps_data_v1, avg_eval_steps_means_v1, avg_eval_steps_stds_v1, avg_eval_regret_data_v1,
    avg_eval_regret_means_v1, avg_eval_regret_stds_v1, avg_eval_opt_frac_data_v1, avg_eval_opt_frac_means_v1,
    avg_eval_opt_frac_stds_v1, avg_eval_caught_frac_data_v1, avg_eval_caught_frac_means_v1,
    avg_eval_caught_frac_stds_v1, avg_eval_early_stopping_frac_data_v1, avg_eval_early_stopping_means_v1,
    avg_eval_early_stopping_stds_v1, avg_eval_intrusion_frac_data_v1, avg_eval_intrusion_means_v1,
    avg_eval_intrusion_stds_v1)

