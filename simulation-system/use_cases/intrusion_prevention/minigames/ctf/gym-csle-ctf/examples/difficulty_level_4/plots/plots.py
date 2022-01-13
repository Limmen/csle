import pandas as pd
import numpy as np
import glob
from gym_csle_ctf.util.plots import plotting_util_defender
from csle_common.util.experiments_util import util

def parse_data(base_path: str, suffix: str, ips = None, eval_ips = None):
    print(glob.glob(base_path + "0/*_train.csv"))
    ppo_v1_df_0 = pd.read_csv(glob.glob(base_path + "0/*_train.csv")[0])
    ppo_v1_df_399 = pd.read_csv(glob.glob(base_path + "399/*_train.csv")[0])
    #ppo_dfs_v1 = [ppo_v1_df_0, ppo_v1_df_999]
    ppo_dfs_v1 = [ppo_v1_df_0, ppo_v1_df_399]

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

    avg_train_snort_severe_baseline_data_v1 = list(
        map(lambda df: util.running_average_list(df["snort_severe_baseline_rewards"].values, running_avg), ppo_dfs_v1))
    avg_train_snort_severe_baseline_means_v1 = np.mean(tuple(avg_train_snort_severe_baseline_data_v1), axis=0)
    avg_train_snort_severe_baseline_stds_v1 = np.std(tuple(avg_train_snort_severe_baseline_data_v1), axis=0, ddof=1)

    avg_train_snort_warning_baseline_data_v1 = list(
        map(lambda df: util.running_average_list(df["snort_warning_baseline_rewards"].values, running_avg), ppo_dfs_v1))
    avg_train_snort_warning_baseline_means_v1 = np.mean(tuple(avg_train_snort_warning_baseline_data_v1), axis=0)
    avg_train_snort_warning_baseline_stds_v1 = np.std(tuple(avg_train_snort_warning_baseline_data_v1), axis=0, ddof=1)

    avg_train_snort_critical_baseline_data_v1 = list(
        map(lambda df: util.running_average_list(df["snort_critical_baseline_rewards"].values, running_avg), ppo_dfs_v1))
    avg_train_snort_critical_baseline_means_v1 = np.mean(tuple(avg_train_snort_critical_baseline_data_v1), axis=0)
    avg_train_snort_critical_baseline_stds_v1 = np.std(tuple(avg_train_snort_critical_baseline_data_v1), axis=0, ddof=1)

    avg_train_var_log_baseline_data_v1 = list(
        map(lambda df: util.running_average_list(df["var_log_baseline_rewards"].values, running_avg),
            ppo_dfs_v1))
    avg_train_var_log_baseline_means_v1 = np.mean(tuple(avg_train_var_log_baseline_data_v1), axis=0)
    avg_train_var_log_baseline_stds_v1 = np.std(tuple(avg_train_var_log_baseline_data_v1), axis=0, ddof=1)

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

    avg_eval_snort_severe_baseline_data_v1 = list(
        map(lambda df: util.running_average_list(df["eval_snort_severe_baseline_rewards"].values, running_avg), ppo_dfs_v1))
    avg_eval_snort_severe_baseline_means_v1 = np.mean(tuple(avg_eval_snort_severe_baseline_data_v1), axis=0)
    avg_eval_snort_severe_baseline_stds_v1 = np.std(tuple(avg_eval_snort_severe_baseline_data_v1), axis=0, ddof=1)

    avg_eval_snort_warning_baseline_data_v1 = list(
        map(lambda df: util.running_average_list(df["eval_snort_warning_baseline_rewards"].values, running_avg), ppo_dfs_v1))
    avg_eval_snort_warning_baseline_means_v1 = np.mean(tuple(avg_eval_snort_warning_baseline_data_v1), axis=0)
    avg_eval_snort_warning_baseline_stds_v1 = np.std(tuple(avg_eval_snort_warning_baseline_data_v1), axis=0, ddof=1)

    avg_eval_snort_critical_baseline_data_v1 = list(
        map(lambda df: util.running_average_list(df["eval_snort_critical_baseline_rewards"].values, running_avg),
            ppo_dfs_v1))
    avg_eval_snort_critical_baseline_means_v1 = np.mean(tuple(avg_eval_snort_critical_baseline_data_v1), axis=0)
    avg_eval_snort_critical_baseline_stds_v1 = np.std(tuple(avg_eval_snort_critical_baseline_data_v1), axis=0, ddof=1)

    avg_eval_var_log_baseline_data_v1 = list(
        map(lambda df: util.running_average_list(df["eval_var_log_baseline_rewards"].values, running_avg),
            ppo_dfs_v1))
    avg_eval_var_log_baseline_means_v1 = np.mean(tuple(avg_eval_var_log_baseline_data_v1), axis=0)
    avg_eval_var_log_baseline_stds_v1 = np.std(tuple(avg_eval_var_log_baseline_data_v1), axis=0, ddof=1)

    # Eval 2 avg
    avg_eval_2_rewards_data_v1 = list(
        map(lambda df: util.running_average_list(df["defender_eval_2_avg_episode_rewards"].values, running_avg),
            ppo_dfs_v1))
    avg_eval_2_rewards_means_v1 = np.mean(tuple(avg_eval_2_rewards_data_v1), axis=0)
    avg_eval_2_rewards_stds_v1 = np.std(tuple(avg_eval_2_rewards_data_v1), axis=0, ddof=1)

    avg_eval_2_steps_data_v1 = list(
        map(lambda df: util.running_average_list(df["eval_2_avg_episode_steps"].values, running_avg), ppo_dfs_v1))
    avg_eval_2_steps_means_v1 = np.mean(tuple(avg_eval_2_steps_data_v1), axis=0)
    avg_eval_2_steps_stds_v1 = np.std(tuple(avg_eval_2_steps_data_v1), axis=0, ddof=1)

    # avg_eval_2_regret_data_v1 = list(
    #     map(lambda df: util.running_average_list(df["defender_eval_2_avg_regret"].values, running_avg), ppo_dfs_v1))
    # avg_eval_2_regret_means_v1 = np.mean(tuple(avg_eval_2_regret_data_v1), axis=0)
    # avg_eval_2_regret_stds_v1 = np.std(tuple(avg_eval_2_regret_data_v1), axis=0, ddof=1)

    # avg_eval_2_opt_frac_data_v1 = list(
    #     map(lambda df: util.running_average_list(df["defender_eval_2_avg_opt_frac"].values, running_avg), ppo_dfs_v1))
    # avg_eval_2_opt_frac_data_v1 = list(map(lambda x: np.minimum(np.array([1] * len(x)), x), avg_eval_2_opt_frac_data_v1))
    # avg_eval_2_opt_frac_means_v1 = np.mean(tuple(avg_eval_2_opt_frac_data_v1), axis=0)
    # avg_eval_2_opt_frac_stds_v1 = np.std(tuple(avg_eval_2_opt_frac_data_v1), axis=0, ddof=1)

    avg_eval_2_caught_frac_data_v1 = list(
        map(lambda df: util.running_average_list(df["eval_2_caught_frac"].values, running_avg), ppo_dfs_v1))
    avg_eval_2_caught_frac_means_v1 = np.mean(tuple(avg_eval_2_caught_frac_data_v1), axis=0)
    avg_eval_2_caught_frac_stds_v1 = np.std(tuple(avg_eval_2_caught_frac_data_v1), axis=0, ddof=1)

    avg_eval_2_early_stopping_frac_data_v1 = list(
        map(lambda df: util.running_average_list(df["eval_2_early_stopping_frac"].values, running_avg), ppo_dfs_v1))
    avg_eval_2_early_stopping_means_v1 = np.mean(tuple(avg_eval_2_early_stopping_frac_data_v1), axis=0)
    avg_eval_2_early_stopping_stds_v1 = np.std(tuple(avg_eval_2_early_stopping_frac_data_v1), axis=0, ddof=1)

    avg_eval_2_intrusion_frac_data_v1 = list(
        map(lambda df: util.running_average_list(df["eval_2_intrusion_frac"].values, running_avg), ppo_dfs_v1))
    avg_eval_2_intrusion_means_v1 = np.mean(tuple(avg_eval_2_intrusion_frac_data_v1), axis=0)
    avg_eval_2_intrusion_stds_v1 = np.std(tuple(avg_eval_2_intrusion_frac_data_v1), axis=0, ddof=1)

    avg_eval_2_snort_severe_baseline_data_v1 = list(
        map(lambda df: util.running_average_list(df["eval_2_snort_severe_baseline_rewards"].values, running_avg),
            ppo_dfs_v1))
    avg_eval_2_snort_severe_baseline_means_v1 = np.mean(tuple(avg_eval_2_snort_severe_baseline_data_v1), axis=0)
    avg_eval_2_snort_severe_baseline_stds_v1 = np.std(tuple(avg_eval_2_snort_severe_baseline_data_v1), axis=0, ddof=1)

    avg_eval_2_snort_warning_baseline_data_v1 = list(
        map(lambda df: util.running_average_list(df["eval_2_snort_warning_baseline_rewards"].values, running_avg),
            ppo_dfs_v1))
    avg_eval_2_snort_warning_baseline_means_v1 = np.mean(tuple(avg_eval_2_snort_warning_baseline_data_v1), axis=0)
    avg_eval_2_snort_warning_baseline_stds_v1 = np.std(tuple(avg_eval_2_snort_warning_baseline_data_v1), axis=0, ddof=1)

    avg_eval_2_snort_critical_baseline_data_v1 = list(
        map(lambda df: util.running_average_list(df["eval_2_snort_critical_baseline_rewards"].values, running_avg),
            ppo_dfs_v1))
    avg_eval_2_snort_critical_baseline_means_v1 = np.mean(tuple(avg_eval_2_snort_critical_baseline_data_v1), axis=0)
    avg_eval_2_snort_critical_baseline_stds_v1 = np.std(tuple(avg_eval_2_snort_critical_baseline_data_v1), axis=0, ddof=1)

    avg_eval_2_var_log_baseline_data_v1 = list(
        map(lambda df: util.running_average_list(df["eval_2_var_log_baseline_rewards"].values, running_avg),
            ppo_dfs_v1))
    avg_eval_2_var_log_baseline_means_v1 = np.mean(tuple(avg_eval_2_var_log_baseline_data_v1), axis=0)
    avg_eval_2_var_log_baseline_stds_v1 = np.std(tuple(avg_eval_2_var_log_baseline_data_v1), axis=0, ddof=1)

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
           avg_eval_2_intrusion_stds_v1, \
           avg_train_snort_severe_baseline_data_v1, avg_train_snort_severe_baseline_means_v1, \
           avg_train_snort_severe_baseline_stds_v1, avg_train_snort_warning_baseline_data_v1, \
           avg_train_snort_warning_baseline_means_v1, avg_train_snort_warning_baseline_stds_v1, \
           avg_train_snort_critical_baseline_data_v1, avg_train_snort_critical_baseline_means_v1, \
           avg_train_snort_critical_baseline_stds_v1, \
           avg_train_var_log_baseline_data_v1, avg_train_var_log_baseline_means_v1, \
           avg_train_var_log_baseline_stds_v1, \
           avg_eval_snort_severe_baseline_data_v1, avg_eval_snort_severe_baseline_means_v1, \
           avg_eval_snort_severe_baseline_stds_v1, avg_eval_snort_warning_baseline_data_v1, \
           avg_eval_snort_warning_baseline_means_v1, avg_eval_snort_warning_baseline_stds_v1, \
           avg_eval_snort_critical_baseline_data_v1, avg_eval_snort_critical_baseline_means_v1, \
           avg_eval_snort_critical_baseline_stds_v1, \
           avg_eval_var_log_baseline_data_v1, avg_eval_var_log_baseline_means_v1, \
           avg_eval_var_log_baseline_stds_v1, \
           avg_eval_2_snort_severe_baseline_data_v1, avg_eval_2_snort_severe_baseline_means_v1, \
           avg_eval_2_snort_severe_baseline_stds_v1, avg_eval_2_snort_warning_baseline_data_v1, \
           avg_eval_2_snort_warning_baseline_means_v1, avg_eval_2_snort_warning_baseline_stds_v1, \
           avg_eval_2_snort_critical_baseline_data_v1, avg_eval_2_snort_critical_baseline_means_v1, \
           avg_eval_2_snort_critical_baseline_stds_v1, \
           avg_eval_2_var_log_baseline_data_v1, avg_eval_2_var_log_baseline_means_v1, \
           avg_eval_2_var_log_baseline_stds_v1

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
    avg_eval_2_intrusion_stds_v1,
    avg_train_snort_severe_baseline_data_v1, avg_train_snort_severe_baseline_means_v1,
    avg_train_snort_severe_baseline_stds_v1, avg_train_snort_warning_baseline_data_v1,
    avg_train_snort_warning_baseline_means_v1, avg_train_snort_warning_baseline_stds_v1,
    avg_train_snort_critical_baseline_data_v1, avg_train_snort_critical_baseline_means_v1,
    avg_train_snort_critical_baseline_stds_v1,
    avg_train_var_log_baseline_data_v1, avg_train_var_log_baseline_means_v1,
    avg_train_var_log_baseline_stds_v1,
    avg_eval_snort_severe_baseline_data_v1, avg_eval_snort_severe_baseline_means_v1,
    avg_eval_snort_severe_baseline_stds_v1, avg_eval_snort_warning_baseline_data_v1,
    avg_eval_snort_warning_baseline_means_v1, avg_eval_snort_warning_baseline_stds_v1,
    avg_eval_snort_critical_baseline_data_v1, avg_eval_snort_critical_baseline_means_v1,
    avg_eval_snort_critical_baseline_stds_v1,
    avg_eval_var_log_baseline_data_v1, avg_eval_var_log_baseline_means_v1,
    avg_eval_var_log_baseline_stds_v1,
    avg_eval_2_snort_severe_baseline_data_v1, avg_eval_2_snort_severe_baseline_means_v1,
    avg_eval_2_snort_severe_baseline_stds_v1, avg_eval_2_snort_warning_baseline_data_v1,
    avg_eval_2_snort_warning_baseline_means_v1, avg_eval_2_snort_warning_baseline_stds_v1,
    avg_eval_2_snort_critical_baseline_data_v1, avg_eval_2_snort_critical_baseline_means_v1,
    avg_eval_2_snort_critical_baseline_stds_v1,
    avg_eval_2_var_log_baseline_data_v1, avg_eval_2_var_log_baseline_means_v1,
    avg_eval_2_var_log_baseline_stds_v1,
               ):
    print("plot")
    suffix = "gensim"
    ylim_rew = (-2, 10.5)

    plotting_util_defender.plot_rewards_defender(
        avg_train_rewards_data_v1, avg_train_rewards_means_v1, avg_train_rewards_stds_v1,
        avg_eval_2_rewards_data_v1, avg_eval_2_rewards_means_v1, avg_eval_2_rewards_stds_v1,
        avg_train_snort_severe_baseline_data_v1, avg_train_snort_severe_baseline_means_v1, avg_train_snort_severe_baseline_stds_v1,
        avg_train_snort_warning_baseline_data_v1, avg_train_snort_warning_baseline_means_v1, avg_train_snort_warning_baseline_stds_v1,
        avg_train_snort_critical_baseline_data_v1, avg_train_snort_critical_baseline_means_v1, avg_train_snort_critical_baseline_stds_v1,
        avg_train_var_log_baseline_data_v1, avg_train_var_log_baseline_means_v1, avg_train_var_log_baseline_stds_v1,

        avg_eval_2_snort_severe_baseline_data_v1, avg_eval_2_snort_severe_baseline_means_v1,
        avg_eval_2_snort_severe_baseline_stds_v1,
        avg_eval_2_snort_warning_baseline_data_v1, avg_eval_2_snort_warning_baseline_means_v1,
        avg_eval_2_snort_warning_baseline_stds_v1,
        avg_eval_2_snort_critical_baseline_data_v1, avg_eval_2_snort_critical_baseline_means_v1,
        avg_eval_2_snort_critical_baseline_stds_v1,
        avg_eval_2_var_log_baseline_data_v1, avg_eval_2_var_log_baseline_means_v1, avg_eval_2_var_log_baseline_stds_v1,

        ylim_rew=ylim_rew,
        file_name="./rewards_defender_train_" + suffix,
        markevery=3, optimal_reward=10, sample_step = 5, plot_opt=True
    )

    ylim_rew = (-0.1, 1.2)

    for i in range(len(avg_eval_2_caught_frac_means_v1)):
        if avg_eval_2_rewards_means_v1[i] < 0:
            avg_eval_2_caught_frac_means_v1[i] = 0
            avg_eval_2_early_stopping_means_v1[i] = 1
            avg_eval_2_intrusion_means_v1[i] = 0
        elif avg_eval_2_rewards_means_v1[i] > 0:
            avg_eval_2_caught_frac_means_v1[i] = 1
            avg_eval_2_early_stopping_means_v1[i] = 0
            avg_eval_2_intrusion_means_v1[i] = 0

    plotting_util_defender.plot_caught_stopped_intruded(
        avg_train_caught_frac_data_v1, avg_train_caught_frac_means_v1, avg_train_caught_frac_stds_v1,
        avg_train_early_stopping_frac_data_v1, avg_train_early_stopping_means_v1, avg_train_early_stopping_stds_v1,
        avg_train_intrusion_frac_data_v1, avg_train_intrusion_means_v1, avg_train_intrusion_stds_v1,
        avg_eval_2_caught_frac_data_v1, avg_eval_2_caught_frac_means_v1, avg_eval_2_caught_frac_stds_v1,
        avg_eval_2_early_stopping_frac_data_v1, avg_eval_2_early_stopping_means_v1, avg_eval_2_early_stopping_stds_v1,
        avg_eval_2_intrusion_frac_data_v1, avg_eval_2_intrusion_means_v1, avg_eval_2_intrusion_stds_v1,
        ylim_rew=ylim_rew,
        file_name="./rewards_defender_train_caught_stopped_intruded" + suffix,
        markevery=3, optimal_reward=1, sample_step=5, plot_opt=True
    )

if __name__ == '__main__':
    base_path = "/home/kim/storage/workspace/csle/simulation-system/minigames/network_intrusion/ctf/gym-csle-ctf/examples/difficulty_level_4/training/v5/generated_simulation/defender/results_backup/data/"
    base_path= "/home/kim/storage/workspace/csle/simulation-system/minigames/network_intrusion/ctf/gym-csle-ctf/examples/difficulty_level_4/training/v5/generated_simulation/defender/backup_results/"
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
    avg_eval_2_intrusion_stds_v1, \
    avg_train_snort_severe_baseline_data_v1, avg_train_snort_severe_baseline_means_v1, \
    avg_train_snort_severe_baseline_stds_v1, avg_train_snort_warning_baseline_data_v1, \
    avg_train_snort_warning_baseline_means_v1, avg_train_snort_warning_baseline_stds_v1, \
    avg_train_snort_critical_baseline_data_v1, avg_train_snort_critical_baseline_means_v1, \
    avg_train_snort_critical_baseline_stds_v1, \
    avg_train_var_log_baseline_data_v1, avg_train_var_log_baseline_means_v1, \
    avg_train_var_log_baseline_stds_v1, \
    avg_eval_snort_severe_baseline_data_v1, avg_eval_snort_severe_baseline_means_v1, \
    avg_eval_snort_severe_baseline_stds_v1, avg_eval_snort_warning_baseline_data_v1, \
    avg_eval_snort_warning_baseline_means_v1, avg_eval_snort_warning_baseline_stds_v1, \
    avg_eval_snort_critical_baseline_data_v1, avg_eval_snort_critical_baseline_means_v1, \
    avg_eval_snort_critical_baseline_stds_v1, \
    avg_eval_var_log_baseline_data_v1, avg_eval_var_log_baseline_means_v1, \
    avg_eval_var_log_baseline_stds_v1, \
    avg_eval_2_snort_severe_baseline_data_v1, avg_eval_2_snort_severe_baseline_means_v1, \
    avg_eval_2_snort_severe_baseline_stds_v1, avg_eval_2_snort_warning_baseline_data_v1, \
    avg_eval_2_snort_warning_baseline_means_v1, avg_eval_2_snort_warning_baseline_stds_v1, \
    avg_eval_2_snort_critical_baseline_data_v1, avg_eval_2_snort_critical_baseline_means_v1, \
    avg_eval_2_snort_critical_baseline_stds_v1, \
    avg_eval_2_var_log_baseline_data_v1, avg_eval_2_var_log_baseline_means_v1, \
    avg_eval_2_var_log_baseline_stds_v1, = parse_data(base_path=base_path, suffix="gensim")

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
    avg_eval_2_intrusion_stds_v1, avg_train_snort_severe_baseline_data_v1, avg_train_snort_severe_baseline_means_v1,
    avg_train_snort_severe_baseline_stds_v1, avg_train_snort_warning_baseline_data_v1,
    avg_train_snort_warning_baseline_means_v1, avg_train_snort_warning_baseline_stds_v1,
    avg_train_snort_critical_baseline_data_v1, avg_train_snort_critical_baseline_means_v1,
    avg_train_snort_critical_baseline_stds_v1,
    avg_train_var_log_baseline_data_v1, avg_train_var_log_baseline_means_v1,
    avg_train_var_log_baseline_stds_v1,
    avg_eval_snort_severe_baseline_data_v1, avg_eval_snort_severe_baseline_means_v1,
    avg_eval_snort_severe_baseline_stds_v1, avg_eval_snort_warning_baseline_data_v1,
    avg_eval_snort_warning_baseline_means_v1, avg_eval_snort_warning_baseline_stds_v1,
    avg_eval_snort_critical_baseline_data_v1, avg_eval_snort_critical_baseline_means_v1,
    avg_eval_snort_critical_baseline_stds_v1,
    avg_eval_var_log_baseline_data_v1, avg_eval_var_log_baseline_means_v1,
    avg_eval_var_log_baseline_stds_v1,
    avg_eval_2_snort_severe_baseline_data_v1, avg_eval_2_snort_severe_baseline_means_v1,
    avg_eval_2_snort_severe_baseline_stds_v1, avg_eval_2_snort_warning_baseline_data_v1,
    avg_eval_2_snort_warning_baseline_means_v1, avg_eval_2_snort_warning_baseline_stds_v1,
    avg_eval_2_snort_critical_baseline_data_v1, avg_eval_2_snort_critical_baseline_means_v1,
    avg_eval_2_snort_critical_baseline_stds_v1,
    avg_eval_2_var_log_baseline_data_v1, avg_eval_2_var_log_baseline_means_v1,
    avg_eval_2_var_log_baseline_stds_v1,
               )

