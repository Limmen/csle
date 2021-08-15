import pandas as pd
import numpy as np
import glob
import math
from gym_pycr_ctf.dao.defender_dynamics.defender_dynamics_model import DefenderDynamicsModel
from gym_pycr_ctf.util.plots import plotting_util_defender
from gym_pycr_ctf.util.experiments_util import util

def parse_data(novice_attacker_base_path: str, suffix: str, ips = None, eval_ips = None):
    ppo_novice_attacker_0 = pd.read_csv(glob.glob(novice_attacker_base_path + "0/*_train.csv")[0])
    ppo_novice_attacker_999 = pd.read_csv(glob.glob(novice_attacker_base_path + "999/*_train.csv")[0])

    ppo_dfs_novice_attacker = [ppo_novice_attacker_0, ppo_novice_attacker_999]
    ppo_dfs_experienced_attacker = [ppo_novice_attacker_0, ppo_novice_attacker_999]

    max_len = min(list(map(lambda x: len(x), ppo_dfs_novice_attacker)))

    running_avg = 1

    # Train Avg Novice
    avg_train_rewards_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["defender_avg_episode_rewards"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    avg_train_rewards_means_novice_attacker = np.mean(tuple(avg_train_rewards_data_novice_attacker), axis=0)
    avg_train_rewards_stds_novice_attacker = np.std(tuple(avg_train_rewards_data_novice_attacker), axis=0, ddof=1)

    avg_train_steps_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["avg_episode_steps"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    avg_train_steps_means_novice_attacker = np.mean(tuple(avg_train_steps_data_novice_attacker), axis=0)
    avg_train_steps_stds_novice_attacker = np.std(tuple(avg_train_steps_data_novice_attacker), axis=0, ddof=1)

    avg_train_caught_frac_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["caught_frac"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    avg_train_caught_frac_means_novice_attacker = np.mean(tuple(avg_train_caught_frac_data_novice_attacker), axis=0)
    avg_train_caught_frac_stds_novice_attacker = np.std(tuple(avg_train_caught_frac_data_novice_attacker), axis=0, ddof=1)

    avg_train_early_stopping_frac_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["early_stopping_frac"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    avg_train_early_stopping_means_novice_attacker = np.mean(tuple(avg_train_early_stopping_frac_data_novice_attacker), axis=0)
    avg_train_early_stopping_stds_novice_attacker = np.std(tuple(avg_train_early_stopping_frac_data_novice_attacker), axis=0, ddof=1)

    avg_train_intrusion_frac_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["intrusion_frac"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    avg_train_intrusion_means_novice_attacker = np.mean(tuple(avg_train_intrusion_frac_data_novice_attacker), axis=0)
    avg_train_intrusion_stds_novice_attacker = np.std(tuple(avg_train_intrusion_frac_data_novice_attacker), axis=0, ddof=1)

    # optimal_rewards_novice_attacker_data = list(
    #     map(lambda df: util.running_average_list(df["optimal_rewards"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    # optimal_rewards_novice_attacker_means = np.mean(tuple(optimal_rewards_novice_attacker_data), axis=0)
    # optimal_rewards_novice_attacker_stds = np.std(tuple(optimal_rewards_novice_attacker_data), axis=0, ddof=1)

    # optimal_steps_novice_attacker_data = list(
    #     map(lambda df: util.running_average_list(df["optimal_steps"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    # optimal_steps_novice_attacker_means = np.mean(tuple(optimal_steps_novice_attacker_data), axis=0)
    # optimal_steps_novice_attacker_stds = np.std(tuple(optimal_steps_novice_attacker_data), axis=0, ddof=1)

    avg_train_i_steps_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["intrusion_steps"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    avg_train_i_steps_means_novice_attacker = np.mean(tuple(avg_train_i_steps_data_novice_attacker), axis=0)
    avg_train_i_steps_stds_novice_attacker = np.std(tuple(avg_train_i_steps_data_novice_attacker), axis=0, ddof=1)

    train_snort_severe_baseline_rewards_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["snort_severe_baseline_rewards"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    train_snort_severe_baseline_rewards_means_novice_attacker = np.mean(tuple(train_snort_severe_baseline_rewards_data_novice_attacker), axis=0)
    train_snort_severe_baseline_rewards_stds_novice_attacker = np.std(tuple(train_snort_severe_baseline_rewards_data_novice_attacker), axis=0, ddof=1)

    train_step_baseline_rewards_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["step_baseline_rewards"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    train_step_baseline_rewards_means_novice_attacker = np.mean(
        tuple(train_step_baseline_rewards_data_novice_attacker), axis=0)
    train_step_baseline_rewards_stds_novice_attacker = np.std(
        tuple(train_step_baseline_rewards_data_novice_attacker), axis=0, ddof=1)

    # Eval Avg Novice Attacker

    avg_eval_rewards_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["defender_eval_avg_episode_rewards"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_rewards_means_novice_attacker = np.mean(tuple(avg_eval_rewards_data_novice_attacker), axis=0)
    avg_eval_rewards_stds_novice_attacker = np.std(tuple(avg_eval_rewards_data_novice_attacker), axis=0, ddof=1)

    avg_eval_steps_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_avg_episode_steps"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_steps_means_novice_attacker = np.mean(tuple(avg_eval_steps_data_novice_attacker), axis=0)
    avg_eval_steps_stds_novice_attacker = np.std(tuple(avg_eval_steps_data_novice_attacker), axis=0, ddof=1)

    avg_eval_caught_frac_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_caught_frac"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_caught_frac_means_novice_attacker = np.mean(tuple(avg_eval_caught_frac_data_novice_attacker), axis=0)
    avg_eval_caught_frac_stds_novice_attacker = np.std(tuple(avg_eval_caught_frac_data_novice_attacker), axis=0,
                                                        ddof=1)

    avg_eval_early_stopping_frac_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_early_stopping_frac"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_early_stopping_means_novice_attacker = np.mean(tuple(avg_eval_early_stopping_frac_data_novice_attacker),
                                                             axis=0)
    avg_eval_early_stopping_stds_novice_attacker = np.std(tuple(avg_eval_early_stopping_frac_data_novice_attacker),
                                                           axis=0, ddof=1)

    avg_eval_intrusion_frac_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_intrusion_frac"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_intrusion_means_novice_attacker = np.mean(tuple(avg_eval_intrusion_frac_data_novice_attacker), axis=0)
    avg_eval_intrusion_stds_novice_attacker = np.std(tuple(avg_eval_intrusion_frac_data_novice_attacker), axis=0,
                                                      ddof=1)

    # optimal_rewards_novice_attacker_data = list(
    #     map(lambda df: util.running_average_list(df["optimal_rewards"].values[0:max_len], running_avg),
    #         ppo_dfs_novice_attacker))
    # optimal_rewards_novice_attacker_means = np.mean(tuple(optimal_rewards_novice_attacker_data), axis=0)
    # optimal_rewards_novice_attacker_stds = np.std(tuple(optimal_rewards_novice_attacker_data), axis=0, ddof=1)

    # optimal_steps_novice_attacker_data = list(
    #     map(lambda df: util.running_average_list(df["optimal_steps"].values[0:max_len], running_avg),
    #         ppo_dfs_novice_attacker))
    # optimal_steps_novice_attacker_means = np.mean(tuple(optimal_steps_novice_attacker_data), axis=0)
    # optimal_steps_novice_attacker_stds = np.std(tuple(optimal_steps_novice_attacker_data), axis=0, ddof=1)

    avg_eval_i_steps_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_intrusion_steps"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_i_steps_means_novice_attacker = np.mean(tuple(avg_eval_i_steps_data_novice_attacker), axis=0)
    avg_eval_i_steps_stds_novice_attacker = np.std(tuple(avg_train_i_steps_data_novice_attacker), axis=0, ddof=1)

    eval_snort_severe_baseline_rewards_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_snort_severe_baseline_rewards"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    eval_snort_severe_baseline_rewards_means_novice_attacker = np.mean(
        tuple(eval_snort_severe_baseline_rewards_data_novice_attacker), axis=0)
    eval_snort_severe_baseline_rewards_stds_novice_attacker = np.std(
        tuple(eval_snort_severe_baseline_rewards_data_novice_attacker), axis=0, ddof=1)

    eval_step_baseline_rewards_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_step_baseline_rewards"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    eval_step_baseline_rewards_means_novice_attacker = np.mean(
        tuple(eval_step_baseline_rewards_data_novice_attacker), axis=0)
    eval_step_baseline_rewards_stds_novice_attacker = np.std(
        tuple(eval_step_baseline_rewards_data_novice_attacker), axis=0, ddof=1)


    # Eval 2 Avg Novice Attacker

    avg_eval_2_rewards_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["defender_eval_2_avg_episode_rewards"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_2_rewards_means_novice_attacker = np.mean(tuple(avg_eval_2_rewards_data_novice_attacker), axis=0)
    avg_eval_2_rewards_stds_novice_attacker = np.std(tuple(avg_eval_2_rewards_data_novice_attacker), axis=0, ddof=1)

    avg_eval_2_steps_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_2_avg_episode_steps"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_2_steps_means_novice_attacker = np.mean(tuple(avg_eval_2_steps_data_novice_attacker), axis=0)
    avg_eval_2_steps_stds_novice_attacker = np.std(tuple(avg_eval_2_steps_data_novice_attacker), axis=0, ddof=1)

    avg_eval_2_caught_frac_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_2_caught_frac"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_2_caught_frac_means_novice_attacker = np.mean(tuple(avg_eval_2_caught_frac_data_novice_attacker), axis=0)
    avg_eval_2_caught_frac_stds_novice_attacker = np.std(tuple(avg_eval_2_caught_frac_data_novice_attacker), axis=0,
                                                        ddof=1)

    avg_eval_2_early_stopping_frac_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_2_early_stopping_frac"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_2_early_stopping_means_novice_attacker = np.mean(tuple(avg_eval_2_early_stopping_frac_data_novice_attacker),
                                                             axis=0)
    avg_eval_2_early_stopping_stds_novice_attacker = np.std(tuple(avg_eval_2_early_stopping_frac_data_novice_attacker),
                                                           axis=0, ddof=1)

    avg_eval_2_intrusion_frac_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_2_intrusion_frac"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_2_intrusion_means_novice_attacker = np.mean(tuple(avg_eval_2_intrusion_frac_data_novice_attacker), axis=0)
    avg_eval_2_intrusion_stds_novice_attacker = np.std(tuple(avg_eval_2_intrusion_frac_data_novice_attacker), axis=0,
                                                      ddof=1)

    # optimal_rewards_novice_attacker_data = list(
    #     map(lambda df: util.running_average_list(df["optimal_rewards"].values[0:max_len], running_avg),
    #         ppo_dfs_novice_attacker))
    # optimal_rewards_novice_attacker_means = np.mean(tuple(optimal_rewards_novice_attacker_data), axis=0)
    # optimal_rewards_novice_attacker_stds = np.std(tuple(optimal_rewards_novice_attacker_data), axis=0, ddof=1)

    # optimal_steps_novice_attacker_data = list(
    #     map(lambda df: util.running_average_list(df["optimal_steps"].values[0:max_len], running_avg),
    #         ppo_dfs_novice_attacker))
    # optimal_steps_novice_attacker_means = np.mean(tuple(optimal_steps_novice_attacker_data), axis=0)
    # optimal_steps_novice_attacker_stds = np.std(tuple(optimal_steps_novice_attacker_data), axis=0, ddof=1)

    avg_eval_2_i_steps_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_2_intrusion_steps"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_2_i_steps_means_novice_attacker = np.mean(tuple(avg_eval_2_i_steps_data_novice_attacker), axis=0)
    avg_eval_2_i_steps_stds_novice_attacker = np.std(tuple(avg_eval_2_i_steps_data_novice_attacker), axis=0, ddof=1)

    eval_2_snort_severe_baseline_rewards_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_2_snort_severe_baseline_rewards"].values[0:max_len],
                                                 running_avg),
            ppo_dfs_novice_attacker))
    eval_2_snort_severe_baseline_rewards_means_novice_attacker = np.mean(
        tuple(eval_2_snort_severe_baseline_rewards_data_novice_attacker), axis=0)
    eval_2_snort_severe_baseline_rewards_stds_novice_attacker = np.std(
        tuple(eval_2_snort_severe_baseline_rewards_data_novice_attacker), axis=0, ddof=1)

    eval_2_step_baseline_rewards_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_2_step_baseline_rewards"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    eval_2_step_baseline_rewards_means_novice_attacker = np.mean(
        tuple(eval_2_step_baseline_rewards_data_novice_attacker), axis=0)
    eval_2_step_baseline_rewards_stds_novice_attacker = np.std(
        tuple(eval_2_step_baseline_rewards_data_novice_attacker), axis=0, ddof=1)


    return avg_train_rewards_data_novice_attacker, avg_train_rewards_means_novice_attacker, \
           avg_train_rewards_stds_novice_attacker, \
           avg_train_steps_data_novice_attacker, avg_train_steps_means_novice_attacker, \
           avg_train_steps_stds_novice_attacker, \
           avg_train_caught_frac_data_novice_attacker, avg_train_caught_frac_means_novice_attacker, \
           avg_train_caught_frac_stds_novice_attacker, \
           avg_train_early_stopping_frac_data_novice_attacker, avg_train_early_stopping_means_novice_attacker, \
           avg_train_early_stopping_stds_novice_attacker, avg_train_intrusion_frac_data_novice_attacker, \
           avg_train_intrusion_means_novice_attacker, \
           avg_train_intrusion_stds_novice_attacker, \
           avg_train_i_steps_data_novice_attacker, avg_train_i_steps_means_novice_attacker, \
           avg_train_i_steps_stds_novice_attacker, \
           train_snort_severe_baseline_rewards_data_novice_attacker, train_snort_severe_baseline_rewards_means_novice_attacker, \
           train_snort_severe_baseline_rewards_stds_novice_attacker, train_step_baseline_rewards_data_novice_attacker, \
           train_step_baseline_rewards_means_novice_attacker, train_step_baseline_rewards_stds_novice_attacker, \
           avg_eval_rewards_data_novice_attacker, avg_eval_rewards_means_novice_attacker, \
           avg_eval_rewards_stds_novice_attacker, \
           avg_eval_steps_data_novice_attacker, avg_eval_steps_means_novice_attacker, \
           avg_eval_steps_stds_novice_attacker, \
           avg_eval_caught_frac_data_novice_attacker, avg_eval_caught_frac_means_novice_attacker, \
           avg_eval_caught_frac_stds_novice_attacker, \
           avg_eval_early_stopping_frac_data_novice_attacker, avg_eval_early_stopping_means_novice_attacker, \
           avg_eval_early_stopping_stds_novice_attacker, avg_eval_intrusion_frac_data_novice_attacker, \
           avg_eval_intrusion_means_novice_attacker, \
           avg_eval_intrusion_stds_novice_attacker, \
           avg_eval_i_steps_data_novice_attacker, avg_eval_i_steps_means_novice_attacker, \
           avg_eval_i_steps_stds_novice_attacker, eval_snort_severe_baseline_rewards_data_novice_attacker, \
           eval_snort_severe_baseline_rewards_means_novice_attacker, \
           eval_snort_severe_baseline_rewards_stds_novice_attacker, \
           eval_step_baseline_rewards_data_novice_attacker, eval_step_baseline_rewards_means_novice_attacker, \
           eval_step_baseline_rewards_stds_novice_attacker, \
           avg_eval_2_rewards_data_novice_attacker, avg_eval_2_rewards_means_novice_attacker, \
           avg_eval_2_rewards_stds_novice_attacker, \
           avg_eval_2_steps_data_novice_attacker, avg_eval_2_steps_means_novice_attacker, \
           avg_eval_2_steps_stds_novice_attacker, \
           avg_eval_2_caught_frac_data_novice_attacker, avg_eval_2_caught_frac_means_novice_attacker, \
           avg_eval_2_caught_frac_stds_novice_attacker, \
           avg_eval_2_early_stopping_frac_data_novice_attacker, avg_eval_2_early_stopping_means_novice_attacker, \
           avg_eval_2_early_stopping_stds_novice_attacker, avg_eval_2_intrusion_frac_data_novice_attacker, \
           avg_eval_2_intrusion_means_novice_attacker, \
           avg_eval_2_intrusion_stds_novice_attacker, \
           avg_eval_2_i_steps_data_novice_attacker, avg_eval_2_i_steps_means_novice_attacker, \
           avg_eval_2_i_steps_stds_novice_attacker, eval_2_snort_severe_baseline_rewards_data_novice_attacker, \
           eval_2_snort_severe_baseline_rewards_means_novice_attacker, \
           eval_2_snort_severe_baseline_rewards_stds_novice_attacker, \
           eval_2_step_baseline_rewards_data_novice_attacker, \
           eval_2_step_baseline_rewards_means_novice_attacker, eval_2_step_baseline_rewards_stds_novice_attacker


def plot_train(
        avg_train_rewards_data_novice_attacker, avg_train_rewards_means_novice_attacker,
        avg_train_rewards_stds_novice_attacker,
        avg_train_steps_data_novice_attacker, avg_train_steps_means_novice_attacker,
        avg_train_steps_stds_novice_attacker,
        avg_train_caught_frac_data_novice_attacker, avg_train_caught_frac_means_novice_attacker,
        avg_train_caught_frac_stds_novice_attacker,
        avg_train_early_stopping_frac_data_novice_attacker, avg_train_early_stopping_means_novice_attacker,
        avg_train_early_stopping_stds_novice_attacker, avg_train_intrusion_frac_data_novice_attacker,
        avg_train_intrusion_means_novice_attacker,
        avg_train_intrusion_stds_novice_attacker,
        avg_train_i_steps_data_novice_attacker, avg_train_i_steps_means_novice_attacker,
        avg_train_i_steps_stds_novice_attacker,
        train_snort_severe_baseline_rewards_data_novice_attacker,
        train_snort_severe_baseline_rewards_means_novice_attacker,
        train_snort_severe_baseline_rewards_stds_novice_attacker, train_step_baseline_rewards_data_novice_attacker,
        train_step_baseline_rewards_means_novice_attacker, train_step_baseline_rewards_stds_novice_attacker,
        avg_eval_rewards_data_novice_attacker, avg_eval_rewards_means_novice_attacker,
        avg_eval_rewards_stds_novice_attacker,
        avg_eval_steps_data_novice_attacker, avg_eval_steps_means_novice_attacker,
        avg_eval_steps_stds_novice_attacker,
        avg_eval_caught_frac_data_novice_attacker, avg_eval_caught_frac_means_novice_attacker,
        avg_eval_caught_frac_stds_novice_attacker,
        avg_eval_early_stopping_frac_data_novice_attacker, avg_eval_early_stopping_means_novice_attacker,
        avg_eval_early_stopping_stds_novice_attacker, avg_eval_intrusion_frac_data_novice_attacker,
        avg_eval_intrusion_means_novice_attacker,
        avg_eval_intrusion_stds_novice_attacker,
        avg_eval_i_steps_data_novice_attacker, avg_eval_i_steps_means_novice_attacker,
        avg_eval_i_steps_stds_novice_attacker, eval_snort_severe_baseline_rewards_data_novice_attacker,
        eval_snort_severe_baseline_rewards_means_novice_attacker,
        eval_snort_severe_baseline_rewards_stds_novice_attacker,
        eval_step_baseline_rewards_data_novice_attacker, eval_step_baseline_rewards_means_novice_attacker,
        eval_step_baseline_rewards_stds_novice_attacker,
        avg_eval_2_rewards_data_novice_attacker, avg_eval_2_rewards_means_novice_attacker,
        avg_eval_2_rewards_stds_novice_attacker,
        avg_eval_2_steps_data_novice_attacker, avg_eval_2_steps_means_novice_attacker,
        avg_eval_2_steps_stds_novice_attacker,
        avg_eval_2_caught_frac_data_novice_attacker, avg_eval_2_caught_frac_means_novice_attacker,
        avg_eval_2_caught_frac_stds_novice_attacker,
        avg_eval_2_early_stopping_frac_data_novice_attacker, avg_eval_2_early_stopping_means_novice_attacker,
        avg_eval_2_early_stopping_stds_novice_attacker, avg_eval_2_intrusion_frac_data_novice_attacker,
        avg_eval_2_intrusion_means_novice_attacker,
        avg_eval_2_intrusion_stds_novice_attacker,
        avg_eval_2_i_steps_data_novice_attacker, avg_eval_2_i_steps_means_novice_attacker,
        avg_eval_2_i_steps_stds_novice_attacker, eval_2_snort_severe_baseline_rewards_data_novice_attacker,
        eval_2_snort_severe_baseline_rewards_means_novice_attacker,
        eval_2_snort_severe_baseline_rewards_stds_novice_attacker,
        eval_2_step_baseline_rewards_data_novice_attacker,
        eval_2_step_baseline_rewards_means_novice_attacker, eval_2_step_baseline_rewards_stds_novice_attacker
               ):
    print("plot")

    suffix = "gensim"
    ylim_rew = (-300, 170)
    max_iter = 400
    #avg_train_rewards_data_v3[0:max_iter]
    plotting_util_defender.plot_defender_simulation_emulation_tnsm_21(
        avg_rewards_data_simulation= avg_train_rewards_data_novice_attacker,
        avg_rewards_means_simulation= avg_train_rewards_means_novice_attacker,
        avg_rewards_stds_simulation= avg_train_rewards_stds_novice_attacker,
        avg_steps_data_simulation= avg_train_steps_data_novice_attacker,
        avg_tsteps_means_simulation=avg_train_steps_means_novice_attacker,
        avg_steps_stds_simulation= avg_train_steps_stds_novice_attacker,
        avg_caught_frac_data_simulation= avg_train_caught_frac_data_novice_attacker,
        avg_caught_frac_means_simulation= avg_train_caught_frac_means_novice_attacker,
        avg_caught_frac_stds_simulation= avg_train_caught_frac_stds_novice_attacker,
        avg_early_stopping_frac_data_simulation= avg_train_early_stopping_frac_data_novice_attacker,
        avg_early_stopping_means_simulation= avg_train_early_stopping_means_novice_attacker,
        avg_early_stopping_stds_simulation= avg_train_early_stopping_stds_novice_attacker,
        avg_intrusion_frac_data_simulation= avg_train_intrusion_frac_data_novice_attacker,
        avg_intrusion_means_simulation= avg_train_intrusion_means_novice_attacker,
        avg_intrusion_stds_simulation= avg_train_intrusion_stds_novice_attacker,
        avg_i_steps_data_simulation= avg_train_i_steps_data_novice_attacker,
        avg_i_steps_means_simulation= avg_train_i_steps_means_novice_attacker,
        avg_i_steps_stds_simulation= avg_train_i_steps_stds_novice_attacker,
        optimal_rewards_data_simulation = avg_train_rewards_data_novice_attacker,
        optimal_rewards_means_simulation=avg_train_rewards_means_novice_attacker,
        optimal_rewards_stds_simulation = avg_train_rewards_stds_novice_attacker,
        optimal_steps_data_simulation = avg_train_steps_data_novice_attacker,
        optimal_steps_means_simulation = avg_train_steps_means_novice_attacker,
        optimal_steps_stds_simulation = avg_train_steps_stds_novice_attacker,
        avg_rewards_data_emulation=avg_eval_2_rewards_data_novice_attacker,
        avg_rewards_means_emulation=avg_eval_2_rewards_means_novice_attacker,
        avg_rewards_stds_emulation=avg_eval_2_rewards_stds_novice_attacker,
        avg_steps_data_emulation=avg_eval_2_steps_data_novice_attacker,
        avg_steps_means_emulation=avg_eval_2_steps_means_novice_attacker,
        avg_steps_stds_emulation=avg_eval_2_steps_stds_novice_attacker,
        avg_caught_frac_data_emulation=avg_eval_2_caught_frac_data_novice_attacker,
        avg_caught_frac_means_emulation=avg_eval_2_caught_frac_means_novice_attacker,
        avg_caught_frac_stds_emulation=avg_eval_2_caught_frac_stds_novice_attacker,
        avg_early_stopping_frac_data_emulation=avg_eval_2_early_stopping_frac_data_novice_attacker,
        avg_early_stopping_means_emulation=avg_eval_2_early_stopping_means_novice_attacker,
        avg_early_stopping_stds_emulation=avg_eval_2_early_stopping_stds_novice_attacker,
        avg_intrusion_frac_data_emulation=avg_eval_2_intrusion_frac_data_novice_attacker,
        avg_intrusion_means_emulation=avg_eval_2_intrusion_means_novice_attacker,
        avg_intrusion_stds_emulation=avg_eval_2_intrusion_stds_novice_attacker,
        avg_i_steps_data_emulation=avg_eval_2_i_steps_data_novice_attacker,
        avg_i_steps_means_emulation=avg_eval_2_i_steps_means_novice_attacker,
        avg_i_steps_stds_emulation=avg_eval_2_i_steps_stds_novice_attacker,
        optimal_rewards_data_emulation=avg_eval_2_rewards_data_novice_attacker,
        optimal_rewards_means_emulation=avg_eval_2_rewards_means_novice_attacker,
        optimal_rewards_stds_emulation=avg_eval_2_rewards_stds_novice_attacker,
        optimal_steps_data_emulation=avg_eval_2_steps_data_novice_attacker,
        optimal_steps_means_emulation=avg_eval_2_steps_means_novice_attacker,
        optimal_steps_stds_emulation=avg_eval_2_steps_stds_novice_attacker,

        steps_baseline_rewards_data = eval_2_step_baseline_rewards_data_novice_attacker,
        steps_baseline_rewards_means=eval_2_step_baseline_rewards_means_novice_attacker,
        steps_baseline_rewards_stds = eval_2_step_baseline_rewards_stds_novice_attacker,
        steps_baseline_steps_data=avg_eval_2_steps_data_novice_attacker,
        steps_baseline_steps_means=avg_eval_2_steps_means_novice_attacker,
        steps_baseline_steps_stds=avg_eval_2_steps_stds_novice_attacker,
        steps_baseline_early_stopping_data = avg_eval_2_early_stopping_frac_data_novice_attacker,
        steps_baseline_early_stopping_means=avg_eval_2_early_stopping_means_novice_attacker,
        steps_baseline_early_stopping_stds=avg_eval_2_early_stopping_stds_novice_attacker,
        steps_baseline_caught_data = avg_eval_2_caught_frac_data_novice_attacker,
        steps_baseline_caught_means=avg_eval_2_caught_frac_means_novice_attacker,
        steps_baseline_caught_stds = avg_eval_2_caught_frac_stds_novice_attacker,
        steps_baseline_i_steps_data = avg_eval_2_i_steps_data_novice_attacker,
        steps_baseline_i_steps_means = avg_eval_2_i_steps_means_novice_attacker,
        steps_baseline_i_steps_stds = avg_eval_2_i_steps_stds_novice_attacker,

        snort_severe_baseline_rewards_data=eval_2_snort_severe_baseline_rewards_data_novice_attacker,
        snort_severe_baseline_rewards_means=eval_2_snort_severe_baseline_rewards_means_novice_attacker,
        snort_severe_baseline_rewards_stds=eval_2_snort_severe_baseline_rewards_stds_novice_attacker,
        snort_severe_baseline_steps_data=avg_eval_2_steps_data_novice_attacker,
        snort_severe_baseline_steps_means=avg_eval_2_steps_means_novice_attacker,
        snort_severe_baseline_steps_stds=avg_eval_2_steps_stds_novice_attacker,
        snort_severe_baseline_early_stopping_data=avg_eval_2_early_stopping_frac_data_novice_attacker,
        snort_severe_baseline_early_stopping_means=avg_eval_2_early_stopping_means_novice_attacker,
        snort_severe_baseline_early_stopping_stds=avg_eval_2_early_stopping_stds_novice_attacker,
        snort_severe_baseline_caught_data=avg_eval_2_caught_frac_data_novice_attacker,
        snort_severe_baseline_caught_means=avg_eval_2_caught_frac_means_novice_attacker,
        snort_severe_baseline_caught_stds=avg_eval_2_caught_frac_stds_novice_attacker,
        snort_severe_baseline_i_steps_data=avg_eval_2_i_steps_data_novice_attacker,
        snort_severe_baseline_i_steps_means=avg_eval_2_i_steps_means_novice_attacker,
        snort_severe_baseline_i_steps_stds=avg_eval_2_i_steps_stds_novice_attacker,

        fontsize= 6.5, figsize= (7.5, 1.5), title_fontsize=8, lw=0.75, wspace=0.17, hspace=0.4, top=0.0,
        bottom=0.28, labelsize=6, markevery=25, optimal_reward = 100, sample_step = 2,
        eval_only=False, plot_opt = False, iterations_per_step= 10, optimal_int = 1.0,
        optimal_flag = 1.0, file_name = "defender_simulation_emulation_novice_attacker_tnsm_21", markersize=2.25
    )


if __name__ == '__main__':
    base_path_1 = "/home/kim/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_9/training/v5/generated_simulation/defender/results_backup3/data/"
    avg_train_rewards_data_novice_attacker, avg_train_rewards_means_novice_attacker, \
    avg_train_rewards_stds_novice_attacker, \
    avg_train_steps_data_novice_attacker, avg_train_steps_means_novice_attacker, \
    avg_train_steps_stds_novice_attacker, \
    avg_train_caught_frac_data_novice_attacker, avg_train_caught_frac_means_novice_attacker, \
    avg_train_caught_frac_stds_novice_attacker, \
    avg_train_early_stopping_frac_data_novice_attacker, avg_train_early_stopping_means_novice_attacker, \
    avg_train_early_stopping_stds_novice_attacker, avg_train_intrusion_frac_data_novice_attacker, \
    avg_train_intrusion_means_novice_attacker, \
    avg_train_intrusion_stds_novice_attacker, \
    avg_train_i_steps_data_novice_attacker, avg_train_i_steps_means_novice_attacker, \
    avg_train_i_steps_stds_novice_attacker, \
    train_snort_severe_baseline_rewards_data_novice_attacker, train_snort_severe_baseline_rewards_means_novice_attacker, \
    train_snort_severe_baseline_rewards_stds_novice_attacker, train_step_baseline_rewards_data_novice_attacker, \
    train_step_baseline_rewards_means_novice_attacker, train_step_baseline_rewards_stds_novice_attacker, \
    avg_eval_rewards_data_novice_attacker, avg_eval_rewards_means_novice_attacker, \
    avg_eval_rewards_stds_novice_attacker, \
    avg_eval_steps_data_novice_attacker, avg_eval_steps_means_novice_attacker, \
    avg_eval_steps_stds_novice_attacker, \
    avg_eval_caught_frac_data_novice_attacker, avg_eval_caught_frac_means_novice_attacker, \
    avg_eval_caught_frac_stds_novice_attacker, \
    avg_eval_early_stopping_frac_data_novice_attacker, avg_eval_early_stopping_means_novice_attacker, \
    avg_eval_early_stopping_stds_novice_attacker, avg_eval_intrusion_frac_data_novice_attacker, \
    avg_eval_intrusion_means_novice_attacker, \
    avg_eval_intrusion_stds_novice_attacker, \
    avg_eval_i_steps_data_novice_attacker, avg_eval_i_steps_means_novice_attacker, \
    avg_eval_i_steps_stds_novice_attacker, eval_snort_severe_baseline_rewards_data_novice_attacker, \
    eval_snort_severe_baseline_rewards_means_novice_attacker, \
    eval_snort_severe_baseline_rewards_stds_novice_attacker, \
    eval_step_baseline_rewards_data_novice_attacker, eval_step_baseline_rewards_means_novice_attacker, \
    eval_step_baseline_rewards_stds_novice_attacker, \
    avg_eval_2_rewards_data_novice_attacker, avg_eval_2_rewards_means_novice_attacker, \
    avg_eval_2_rewards_stds_novice_attacker, \
    avg_eval_2_steps_data_novice_attacker, avg_eval_2_steps_means_novice_attacker, \
    avg_eval_2_steps_stds_novice_attacker, \
    avg_eval_2_caught_frac_data_novice_attacker, avg_eval_2_caught_frac_means_novice_attacker, \
    avg_eval_2_caught_frac_stds_novice_attacker, \
    avg_eval_2_early_stopping_frac_data_novice_attacker, avg_eval_2_early_stopping_means_novice_attacker, \
    avg_eval_2_early_stopping_stds_novice_attacker, avg_eval_2_intrusion_frac_data_novice_attacker, \
    avg_eval_2_intrusion_means_novice_attacker, \
    avg_eval_2_intrusion_stds_novice_attacker, \
    avg_eval_2_i_steps_data_novice_attacker, avg_eval_2_i_steps_means_novice_attacker, \
    avg_eval_2_i_steps_stds_novice_attacker, eval_2_snort_severe_baseline_rewards_data_novice_attacker, \
    eval_2_snort_severe_baseline_rewards_means_novice_attacker, \
    eval_2_snort_severe_baseline_rewards_stds_novice_attacker, \
    eval_2_step_baseline_rewards_data_novice_attacker, \
    eval_2_step_baseline_rewards_means_novice_attacker, eval_2_step_baseline_rewards_stds_novice_attacker\
        = parse_data(novice_attacker_base_path=base_path_1, suffix="gensim")

    plot_train(
        avg_train_rewards_data_novice_attacker, avg_train_rewards_means_novice_attacker,
        avg_train_rewards_stds_novice_attacker,
        avg_train_steps_data_novice_attacker, avg_train_steps_means_novice_attacker,
        avg_train_steps_stds_novice_attacker,
        avg_train_caught_frac_data_novice_attacker, avg_train_caught_frac_means_novice_attacker,
        avg_train_caught_frac_stds_novice_attacker,
        avg_train_early_stopping_frac_data_novice_attacker, avg_train_early_stopping_means_novice_attacker,
        avg_train_early_stopping_stds_novice_attacker, avg_train_intrusion_frac_data_novice_attacker,
        avg_train_intrusion_means_novice_attacker,
        avg_train_intrusion_stds_novice_attacker,
        avg_train_i_steps_data_novice_attacker, avg_train_i_steps_means_novice_attacker,
        avg_train_i_steps_stds_novice_attacker,
        train_snort_severe_baseline_rewards_data_novice_attacker,
        train_snort_severe_baseline_rewards_means_novice_attacker,
        train_snort_severe_baseline_rewards_stds_novice_attacker, train_step_baseline_rewards_data_novice_attacker,
        train_step_baseline_rewards_means_novice_attacker, train_step_baseline_rewards_stds_novice_attacker,
        avg_eval_rewards_data_novice_attacker, avg_eval_rewards_means_novice_attacker,
        avg_eval_rewards_stds_novice_attacker,
        avg_eval_steps_data_novice_attacker, avg_eval_steps_means_novice_attacker,
        avg_eval_steps_stds_novice_attacker,
        avg_eval_caught_frac_data_novice_attacker, avg_eval_caught_frac_means_novice_attacker,
        avg_eval_caught_frac_stds_novice_attacker,
        avg_eval_early_stopping_frac_data_novice_attacker, avg_eval_early_stopping_means_novice_attacker,
        avg_eval_early_stopping_stds_novice_attacker, avg_eval_intrusion_frac_data_novice_attacker,
        avg_eval_intrusion_means_novice_attacker,
        avg_eval_intrusion_stds_novice_attacker,
        avg_eval_i_steps_data_novice_attacker, avg_eval_i_steps_means_novice_attacker,
        avg_eval_i_steps_stds_novice_attacker, eval_snort_severe_baseline_rewards_data_novice_attacker,
        eval_snort_severe_baseline_rewards_means_novice_attacker,
        eval_snort_severe_baseline_rewards_stds_novice_attacker,
        eval_step_baseline_rewards_data_novice_attacker, eval_step_baseline_rewards_means_novice_attacker,
        eval_step_baseline_rewards_stds_novice_attacker,
        avg_eval_2_rewards_data_novice_attacker, avg_eval_2_rewards_means_novice_attacker,
        avg_eval_2_rewards_stds_novice_attacker,
        avg_eval_2_steps_data_novice_attacker, avg_eval_2_steps_means_novice_attacker,
        avg_eval_2_steps_stds_novice_attacker,
        avg_eval_2_caught_frac_data_novice_attacker, avg_eval_2_caught_frac_means_novice_attacker,
        avg_eval_2_caught_frac_stds_novice_attacker,
        avg_eval_2_early_stopping_frac_data_novice_attacker, avg_eval_2_early_stopping_means_novice_attacker,
        avg_eval_2_early_stopping_stds_novice_attacker, avg_eval_2_intrusion_frac_data_novice_attacker,
        avg_eval_2_intrusion_means_novice_attacker,
        avg_eval_2_intrusion_stds_novice_attacker,
        avg_eval_2_i_steps_data_novice_attacker, avg_eval_2_i_steps_means_novice_attacker,
        avg_eval_2_i_steps_stds_novice_attacker, eval_2_snort_severe_baseline_rewards_data_novice_attacker,
        eval_2_snort_severe_baseline_rewards_means_novice_attacker,
        eval_2_snort_severe_baseline_rewards_stds_novice_attacker,
        eval_2_step_baseline_rewards_data_novice_attacker,
        eval_2_step_baseline_rewards_means_novice_attacker, eval_2_step_baseline_rewards_stds_novice_attacker
    )
