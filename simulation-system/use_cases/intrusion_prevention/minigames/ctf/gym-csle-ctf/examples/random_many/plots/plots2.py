import pandas as pd
import numpy as np
import glob
from gym_csle_ctf.util.plots import plotting_util_attacker
from csle_common.util.experiments_util import util

def parse_data(base_path: str, suffix: str, ips = None, eval_ips = None):
    ppo_v1_df_0 = pd.read_csv(glob.glob(base_path + "0/*_train.csv")[0])
    #ppo_dfs_v1 = [ppo_v1_df_888, ppo_v1_df_210, ppo_v1_df_111, ppo_v1_df_235, ppo_v1_df_52112]
    ppo_dfs_v1 = [ppo_v1_df_0]
    # ppo_dfs_v1 = [ppo_v1_df_888, ppo_v1_df_210, ppo_v1_df_91, ppo_v1_df_110, ppo_v1_df_21, ppo_v1_df_111, ppo_v1_df_235,
    #               ppo_v1_df_52112]
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
        map(lambda df: util.running_average_list(df["attacker_eval_2_avg_episode_rewards"].values[0:max_len], running_avg),
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
           avg_eval_2_flags_data_v1, avg_eval_2_flags_means_v1, avg_eval_2_flags_stds_v1

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
    avg_eval_intrusion_stds_v1, avg_eval_2_rewards_data_v1, avg_eval_2_rewards_means_v1, avg_eval_2_rewards_stds_v1,
    avg_eval_2_steps_data_v1, avg_eval_2_steps_means_v1, avg_eval_2_steps_stds_v1,
    avg_eval_2_caught_frac_data_v1, avg_eval_2_caught_frac_means_v1,
    avg_eval_2_caught_frac_stds_v1, avg_eval_2_early_stopping_frac_data_v1, avg_eval_2_early_stopping_means_v1,
    avg_eval_2_early_stopping_stds_v1,  avg_eval_2_intrusion_frac_data_v1, avg_eval_2_intrusion_means_v1,
    avg_eval_2_intrusion_stds_v1, avg_eval_2_regret_data_v1, avg_eval_2_regret_means_v1,  avg_eval_2_regret_stds_v1,
    avg_eval_2_opt_frac_data_v1, avg_eval_2_opt_frac_means_v1, avg_eval_2_opt_frac_stds_v1,
    avg_train_attacker_action_alerts_data_v1, avg_train_attacker_action_alerts_means_v1,
    avg_train_attacker_action_alerts_stds_v1, avg_eval_attacker_action_alerts_data_v1,
    avg_eval_attacker_action_alerts_means_v1,
    avg_eval_attacker_action_alerts_stds_v1, avg_eval_2_attacker_action_alerts_data_v1,
    avg_eval_2_attacker_action_alerts_means_v1, avg_eval_2_attacker_action_alerts_stds_v1,
    avg_train_attacker_action_costs_data_v1, avg_train_attacker_action_costs_means_v1,
    avg_train_attacker_action_costs_stds_v1,
    avg_eval_attacker_action_costs_data_v1, avg_eval_attacker_action_costs_means_v1,
    avg_eval_attacker_action_costs_stds_v1, avg_eval_2_attacker_action_costs_data_v1,
    avg_eval_2_attacker_action_costs_means_v1, avg_eval_2_attacker_action_costs_stds_v1,
    avg_train_flags_data_v1, avg_train_flags_means_v1, avg_train_flags_stds_v1,
    avg_eval_flags_data_v1, avg_eval_flags_means_v1, avg_eval_flags_stds_v1,
    avg_eval_2_flags_data_v1, avg_eval_2_flags_means_v1, avg_eval_2_flags_stds_v1
               ):

    print("plot")
    suffix = "gensim"
    ylim_rew = (-300, 170)
    max_iter = 270

    plotting_util_attacker.plot_flags_int_r_steps_costs_alerts(
        avg_eval_rewards_data_v1[0:max_iter], avg_eval_rewards_means_v1[0:max_iter],
        avg_eval_rewards_stds_v1[0:max_iter],
        avg_eval_2_rewards_data_v1[0:max_iter], avg_eval_2_rewards_means_v1[0:max_iter],
        avg_eval_2_rewards_stds_v1[0:max_iter],
        avg_eval_caught_frac_data_v1[0:max_iter], avg_eval_caught_frac_means_v1[0:max_iter],
        avg_eval_caught_frac_stds_v1[0:max_iter],
        avg_eval_intrusion_frac_data_v1[0:max_iter], avg_eval_intrusion_means_v1[0:max_iter],
        avg_eval_intrusion_stds_v1[0:max_iter],
        avg_eval_2_caught_frac_data_v1[0:max_iter], avg_eval_2_caught_frac_means_v1[0:max_iter],
        avg_eval_2_caught_frac_stds_v1[0:max_iter],
        avg_eval_2_intrusion_frac_data_v1[0:max_iter], avg_eval_2_intrusion_means_v1[0:max_iter],
        avg_eval_2_intrusion_stds_v1[0:max_iter],
        avg_eval_flags_data_v1[0:max_iter], avg_eval_flags_means_v1[0:max_iter],
        avg_eval_flags_stds_v1[0:max_iter],
        avg_eval_2_flags_data_v1[0:max_iter], avg_eval_2_flags_means_v1[0:max_iter],
        avg_eval_2_flags_stds_v1[0:max_iter],
        avg_eval_attacker_action_costs_data_v1[0:max_iter], avg_eval_attacker_action_costs_means_v1[0:max_iter],
        avg_eval_attacker_action_costs_stds_v1[0:max_iter],
        avg_eval_2_attacker_action_costs_data_v1[0:max_iter], avg_eval_2_attacker_action_costs_means_v1[0:max_iter],
        avg_eval_2_attacker_action_costs_stds_v1[0:max_iter],
        avg_eval_attacker_action_alerts_data_v1[0:max_iter], avg_eval_attacker_action_alerts_means_v1[0:max_iter],
        avg_eval_attacker_action_alerts_stds_v1[0:max_iter],
        avg_eval_2_attacker_action_alerts_data_v1[0:max_iter], avg_eval_2_attacker_action_alerts_means_v1[0:max_iter],
        avg_eval_2_attacker_action_alerts_stds_v1[0:max_iter],
        avg_eval_steps_data_v1[0:max_iter], avg_eval_steps_means_v1[0:max_iter],
        avg_eval_steps_stds_v1[0:max_iter],
        avg_eval_2_steps_data_v1[0:max_iter], avg_eval_2_steps_means_v1[0:max_iter],
        avg_eval_2_steps_stds_v1[0:max_iter],
        fontsize= 6.5, figsize= (7.5, 2.75), title_fontsize=8, lw=0.75, wspace=0.12, hspace=0.4, top=0.0,
        bottom=0.152, labelsize=6, markevery=10, optimal_reward = 150, sample_step = 2,
        eval_only=False, plot_opt = False, iterations_per_step= 10, optimal_int = 1.0,
        optimal_flag = 1.0, file_name = "flags_int_steps_r_costs_alerts_attacker", markersize=2.25
    )

    # plotting_util_attacker.plot_rewards_attacker(
    #     avg_eval_rewards_data_v1[0:max_iter], avg_eval_rewards_means_v1[0:max_iter],
    #     avg_eval_rewards_stds_v1[0:max_iter],
    #     avg_eval_2_rewards_data_v1[0:max_iter], avg_eval_2_rewards_means_v1[0:max_iter],
    #     avg_eval_2_rewards_stds_v1[0:max_iter],
    #     ylim_rew=ylim_rew,
    #     file_name="./rewards_attacker_train_" + suffix,
    #     markevery=3, optimal_reward=150, sample_step=5, plot_opt=True, iterations_per_step=10
    # )
    #
    # ylim_rew = (0.0, 1.1)
    #
    # plotting_util_attacker.plot_caught_stopped_intruded(
    #     avg_eval_caught_frac_data_v1[0:max_iter], avg_eval_caught_frac_means_v1[0:max_iter],
    #     avg_eval_caught_frac_stds_v1[0:max_iter],
    #     avg_eval_early_stopping_frac_data_v1[0:max_iter], avg_eval_early_stopping_means_v1[0:max_iter],
    #     avg_eval_early_stopping_stds_v1[0:max_iter],
    #     avg_eval_intrusion_frac_data_v1[0:max_iter], avg_eval_intrusion_means_v1[0:max_iter],
    #     avg_eval_intrusion_stds_v1[0:max_iter],
    #     avg_eval_2_caught_frac_data_v1[0:max_iter], avg_eval_2_caught_frac_means_v1[0:max_iter],
    #     avg_eval_2_caught_frac_stds_v1[0:max_iter],
    #     avg_eval_2_early_stopping_frac_data_v1[0:max_iter], avg_eval_2_early_stopping_means_v1[0:max_iter],
    #     avg_eval_2_early_stopping_stds_v1[0:max_iter],
    #     avg_eval_2_intrusion_frac_data_v1[0:max_iter], avg_eval_2_intrusion_means_v1[0:max_iter],
    #     avg_eval_2_intrusion_stds_v1[0:max_iter],
    #     ylim_rew=ylim_rew,
    #     file_name="./attacker_caught_stopped_intruded_" + suffix,
    #     markevery=3, optimal_reward=1, sample_step=5, plot_opt=True, iterations_per_step=10
    # )
    #
    # ylim_rew = (400, 8000)
    #
    # plotting_util_attacker.plot_costs_attacker(
    #     avg_eval_attacker_action_costs_data_v1[0:max_iter], avg_eval_attacker_action_costs_means_v1[0:max_iter],
    #     avg_eval_attacker_action_costs_stds_v1[0:max_iter],
    #     avg_eval_2_attacker_action_costs_data_v1[0:max_iter], avg_eval_2_attacker_action_costs_means_v1[0:max_iter],
    #     avg_eval_2_attacker_action_costs_stds_v1[0:max_iter],
    #     ylim_rew=ylim_rew,
    #     file_name="./attacker_action_costs_attacker_train_" + suffix,
    #     markevery=3, optimal_reward=450, sample_step=5, plot_opt=False, iterations_per_step=10
    # )
    #
    # ylim_rew = (0, 2000)
    #
    # plotting_util_attacker.plot_alerts_attacker(
    #     avg_eval_attacker_action_alerts_data_v1[0:max_iter], avg_eval_attacker_action_alerts_means_v1[0:max_iter],
    #     avg_eval_attacker_action_alerts_stds_v1[0:max_iter],
    #     avg_eval_2_attacker_action_alerts_data_v1[0:max_iter], avg_eval_2_attacker_action_alerts_means_v1[0:max_iter],
    #     avg_eval_2_attacker_action_alerts_stds_v1[0:max_iter],
    #     ylim_rew=ylim_rew,
    #     file_name="./attacker_action_alerts_attacker_train_" + suffix,
    #     markevery=3, optimal_reward=450, sample_step=5, plot_opt=False, iterations_per_step=10
    # )
    #
    # ylim_rew = (0, 1.1)
    #
    # plotting_util_attacker.plot_flags_attacker(
    #     avg_eval_flags_data_v1[0:max_iter], avg_eval_flags_means_v1[0:max_iter],
    #     avg_eval_flags_stds_v1[0:max_iter],
    #     avg_eval_2_flags_data_v1[0:max_iter], avg_eval_2_flags_means_v1[0:max_iter],
    #     avg_eval_2_flags_stds_v1[0:max_iter],
    #     ylim_rew=ylim_rew,
    #     file_name="./flags_attacker_train_" + suffix,
    #     markevery=3, optimal_reward=1, sample_step=5, plot_opt=True, iterations_per_step=10
    # )
    #
    # ylim_rew = (0, 110)
    #
    # plotting_util_attacker.plot_steps_attacker(
    #     avg_eval_steps_data_v1[0:max_iter], avg_eval_steps_means_v1[0:max_iter],
    #     avg_eval_steps_stds_v1[0:max_iter],
    #     avg_eval_2_steps_data_v1[0:max_iter], avg_eval_2_steps_means_v1[0:max_iter],
    #     avg_eval_2_steps_stds_v1[0:max_iter],
    #     ylim_rew=ylim_rew,
    #     file_name="./steps_attacker_train_" + suffix,
    #     markevery=3, optimal_reward=450, sample_step=5, plot_opt=False, iterations_per_step=10
    # )


if __name__ == '__main__':
    base_path = "/Users/kimham/workspace/csle/simulation-system/minigames/network_intrusion/ctf/gym-csle-ctf/examples/random_many/results_backup3/data/"
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
    avg_eval_intrusion_stds_v1, avg_eval_2_rewards_data_v1, avg_eval_2_rewards_means_v1, avg_eval_2_rewards_stds_v1,\
    avg_eval_2_steps_data_v1, avg_eval_2_steps_means_v1, avg_eval_2_steps_stds_v1, \
    avg_eval_2_caught_frac_data_v1, avg_eval_2_caught_frac_means_v1,\
    avg_eval_2_caught_frac_stds_v1, avg_eval_2_early_stopping_frac_data_v1, avg_eval_2_early_stopping_means_v1, \
    avg_eval_2_early_stopping_stds_v1,  avg_eval_2_intrusion_frac_data_v1, avg_eval_2_intrusion_means_v1, \
    avg_eval_2_intrusion_stds_v1, avg_eval_2_regret_data_v1, \
    avg_eval_2_regret_means_v1, avg_eval_2_regret_stds_v1, avg_eval_2_opt_frac_data_v1, \
    avg_eval_2_opt_frac_means_v1, avg_eval_2_opt_frac_stds_v1, avg_train_attacker_action_alerts_data_v1, \
    avg_train_attacker_action_alerts_means_v1, \
    avg_train_attacker_action_alerts_stds_v1, avg_eval_attacker_action_alerts_data_v1, \
    avg_eval_attacker_action_alerts_means_v1, \
    avg_eval_attacker_action_alerts_stds_v1, avg_eval_2_attacker_action_alerts_data_v1, \
    avg_eval_2_attacker_action_alerts_means_v1, avg_eval_2_attacker_action_alerts_stds_v1, \
    avg_train_attacker_action_costs_data_v1, avg_train_attacker_action_costs_means_v1, \
    avg_train_attacker_action_costs_stds_v1, \
    avg_eval_attacker_action_costs_data_v1, avg_eval_attacker_action_costs_means_v1, \
    avg_eval_attacker_action_costs_stds_v1, avg_eval_2_attacker_action_costs_data_v1, \
    avg_eval_2_attacker_action_costs_means_v1, avg_eval_2_attacker_action_costs_stds_v1, \
    avg_train_flags_data_v1, avg_train_flags_means_v1, avg_train_flags_stds_v1, \
    avg_eval_flags_data_v1, avg_eval_flags_means_v1, avg_eval_flags_stds_v1, \
    avg_eval_2_flags_data_v1, avg_eval_2_flags_means_v1, avg_eval_2_flags_stds_v1 \
        = parse_data(base_path=base_path, suffix="gensim")

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
    avg_eval_intrusion_stds_v1, avg_eval_2_rewards_data_v1, avg_eval_2_rewards_means_v1, avg_eval_2_rewards_stds_v1,
    avg_eval_2_steps_data_v1, avg_eval_2_steps_means_v1, avg_eval_2_steps_stds_v1,
    avg_eval_2_caught_frac_data_v1, avg_eval_2_caught_frac_means_v1,
    avg_eval_2_caught_frac_stds_v1, avg_eval_2_early_stopping_frac_data_v1, avg_eval_2_early_stopping_means_v1,
    avg_eval_2_early_stopping_stds_v1,  avg_eval_2_intrusion_frac_data_v1, avg_eval_2_intrusion_means_v1,
    avg_eval_2_intrusion_stds_v1, avg_eval_2_regret_data_v1, avg_eval_2_regret_means_v1, avg_eval_2_regret_stds_v1,
    avg_eval_2_opt_frac_data_v1, avg_eval_2_opt_frac_means_v1, avg_eval_2_opt_frac_stds_v1,
    avg_train_attacker_action_alerts_data_v1, avg_train_attacker_action_alerts_means_v1,
    avg_train_attacker_action_alerts_stds_v1, avg_eval_attacker_action_alerts_data_v1,
    avg_eval_attacker_action_alerts_means_v1,
    avg_eval_attacker_action_alerts_stds_v1, avg_eval_2_attacker_action_alerts_data_v1,
    avg_eval_2_attacker_action_alerts_means_v1, avg_eval_2_attacker_action_alerts_stds_v1,
    avg_train_attacker_action_costs_data_v1, avg_train_attacker_action_costs_means_v1,
    avg_train_attacker_action_costs_stds_v1,
    avg_eval_attacker_action_costs_data_v1, avg_eval_attacker_action_costs_means_v1,
    avg_eval_attacker_action_costs_stds_v1, avg_eval_2_attacker_action_costs_data_v1,
    avg_eval_2_attacker_action_costs_means_v1, avg_eval_2_attacker_action_costs_stds_v1,
    avg_train_flags_data_v1, avg_train_flags_means_v1, avg_train_flags_stds_v1,
    avg_eval_flags_data_v1, avg_eval_flags_means_v1, avg_eval_flags_stds_v1,
    avg_eval_2_flags_data_v1, avg_eval_2_flags_means_v1, avg_eval_2_flags_stds_v1)

