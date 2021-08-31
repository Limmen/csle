import pandas as pd
import numpy as np
import glob
import math
from gym_pycr_ctf.dao.defender_dynamics.defender_dynamics_model import DefenderDynamicsModel
from gym_pycr_ctf.util.plots import plotting_util_defender
from gym_pycr_ctf.util.experiments_util import util

def parse_data(novice_attacker_base_path: str, suffix: str, ips = None, eval_ips = None):
    ppo_novice_attacker_0 = pd.read_csv(glob.glob(novice_attacker_base_path + "0/*_train.csv")[0])
    # ppo_novice_attacker_999 = pd.read_csv(glob.glob(novice_attacker_base_path + "999/*_train.csv")[0])
    # ppo_novice_attacker_399 = pd.read_csv(glob.glob(novice_attacker_base_path + "399/*_train.csv")[0])

    # ppo_dfs_novice_attacker = [ppo_novice_attacker_0, ppo_novice_attacker_999, ppo_novice_attacker_399]
    ppo_dfs_novice_attacker = [ppo_novice_attacker_0]

    max_len = min(list(map(lambda x: len(x), ppo_dfs_novice_attacker)))

    running_avg = 1
    confidence=0.95
    num_seeds = len(ppo_dfs_novice_attacker)
    print("running avg:{}".format(running_avg))

    # Train Avg Novice
    avg_train_rewards_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["defender_avg_episode_rewards"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    max_len = len(avg_train_rewards_data_novice_attacker[0])

    avg_train_rewards_data_novice_attacker = np.array(avg_train_rewards_data_novice_attacker).reshape(max_len, num_seeds)
    avg_train_rewards_stds_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], avg_train_rewards_data_novice_attacker)))
    avg_train_rewards_means_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], avg_train_rewards_data_novice_attacker)))
    # avg_train_rewards_means_novice_attacker = np.mean(tuple(avg_train_rewards_data_novice_attacker), axis=0)
    # avg_train_rewards_stds_novice_attacker = np.std(tuple(avg_train_rewards_data_novice_attacker), axis=0, ddof=1)

    avg_train_steps_data_novice_attacker = list(map(lambda df: util.running_average_list(df["avg_episode_steps"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    avg_train_steps_data_novice_attacker = np.array(avg_train_steps_data_novice_attacker).reshape(max_len, num_seeds)
    avg_train_steps_stds_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], avg_train_steps_data_novice_attacker)))
    avg_train_steps_means_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], avg_train_steps_data_novice_attacker)))
    # avg_train_steps_means_novice_attacker = np.mean(tuple(avg_train_steps_data_novice_attacker), axis=0)
    # avg_train_steps_stds_novice_attacker = np.std(tuple(avg_train_steps_data_novice_attacker), axis=0, ddof=1)

    avg_train_caught_frac_data_novice_attacker = list(map(lambda df: util.running_average_list(df["caught_frac"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    avg_train_caught_frac_data_novice_attacker = np.array(avg_train_caught_frac_data_novice_attacker).reshape(max_len, num_seeds)
    avg_train_caught_frac_stds_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], avg_train_caught_frac_data_novice_attacker)))
    avg_train_caught_frac_means_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], avg_train_caught_frac_data_novice_attacker)))
    # avg_train_caught_frac_means_novice_attacker = np.mean(tuple(avg_train_caught_frac_data_novice_attacker), axis=0)
    # avg_train_caught_frac_stds_novice_attacker = np.std(tuple(avg_train_caught_frac_data_novice_attacker), axis=0, ddof=1)

    avg_train_early_stopping_data_novice_attacker = list(map(lambda df: util.running_average_list(df["early_stopping_frac"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    avg_train_early_stopping_data_novice_attacker = np.array(avg_train_early_stopping_data_novice_attacker).reshape(max_len, num_seeds)
    avg_train_early_stopping_stds_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], avg_train_early_stopping_data_novice_attacker)))
    avg_train_early_stopping_means_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], avg_train_early_stopping_data_novice_attacker)))
    # avg_train_early_stopping_means_novice_attacker = np.mean(tuple(avg_train_early_stopping_data_novice_attacker), axis=0)
    # avg_train_early_stopping_stds_novice_attacker = np.std(tuple(avg_train_early_stopping_data_novice_attacker), axis=0, ddof=1)

    avg_train_intrusion_frac_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["intrusion_frac"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    avg_train_intrusion_frac_data_novice_attacker = np.array(avg_train_intrusion_frac_data_novice_attacker).reshape(max_len, num_seeds)
    avg_train_intrusion_frac_stds_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], avg_train_intrusion_frac_data_novice_attacker)))
    avg_train_intrusion_frac_means_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], avg_train_intrusion_frac_data_novice_attacker)))
    # avg_train_intrusion_frac_means_novice_attacker = np.mean(tuple(avg_train_intrusion_frac_data_novice_attacker), axis=0)
    # avg_train_intrusion_frac_stds_novice_attacker = np.std(tuple(avg_train_intrusion_frac_data_novice_attacker), axis=0, ddof=1)

    avg_train_optimal_defender_rewards_novice_attacker_data = list(map(lambda df: util.running_average_list(df["avg_optimal_defender_reward"].values[0:max_len], running_avg),ppo_dfs_novice_attacker))
    avg_train_optimal_defender_rewards_data_novice_attacker = np.array(avg_train_optimal_defender_rewards_novice_attacker_data).reshape(max_len, num_seeds)
    avg_train_optimal_defender_rewards_novice_attacker_stds = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], avg_train_optimal_defender_rewards_data_novice_attacker)))
    avg_train_optimal_defender_rewards_novice_attacker_means = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], avg_train_optimal_defender_rewards_data_novice_attacker)))
    # avg_train_optimal_defender_rewards_novice_attacker_means = np.mean(tuple(avg_train_optimal_defender_rewards_novice_attacker_data), axis=0)
    # avg_train_optimal_defender_rewards_novice_attacker_stds = np.std(tuple(avg_train_optimal_defender_rewards_novice_attacker_data), axis=0, ddof=1)

    avg_train_i_steps_data_novice_attacker = list(map(lambda df: util.running_average_list(df["intrusion_steps"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    avg_train_i_steps_data_novice_attacker = np.array(avg_train_i_steps_data_novice_attacker).reshape(max_len, num_seeds)
    avg_train_i_steps_stds_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], avg_train_i_steps_data_novice_attacker)))
    avg_train_i_steps_means_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], avg_train_i_steps_data_novice_attacker)))
    # avg_train_i_steps_means_novice_attacker = np.mean(tuple(avg_train_i_steps_data_novice_attacker), axis=0)
    # avg_train_i_steps_stds_novice_attacker = np.std(tuple(avg_train_i_steps_data_novice_attacker), axis=0, ddof=1)

    avg_train_uncaught_intrusion_steps_data_novice_attacker = list(map(lambda df: util.running_average_list(df["avg_uncaught_intrusion_steps"].values[0:max_len], running_avg),ppo_dfs_novice_attacker))
    # avg_train_uncaught_intrusion_steps_means_novice_attacker = np.mean(tuple(avg_train_uncaught_intrusion_steps_data_novice_attacker), axis=0)
    # avg_train_uncaught_intrusion_steps_stds_novice_attacker = np.std(tuple(avg_train_uncaught_intrusion_steps_data_novice_attacker), axis=0, ddof=1)
    avg_train_uncaught_intrusion_steps_data_novice_attacker = np.array(avg_train_uncaught_intrusion_steps_data_novice_attacker).reshape(max_len, num_seeds)
    avg_train_uncaught_intrusion_steps_stds_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], avg_train_uncaught_intrusion_steps_data_novice_attacker)))
    avg_train_uncaught_intrusion_steps_means_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], avg_train_uncaught_intrusion_steps_data_novice_attacker)))

    train_snort_severe_baseline_rewards_data_novice_attacker = list(map(lambda df: util.running_average_list(df["snort_severe_baseline_rewards"].values[0:max_len], running_avg),ppo_dfs_novice_attacker))
    avg_train_snort_severe_baseline_rewards_data_novice_attacker = np.array(train_snort_severe_baseline_rewards_data_novice_attacker).reshape(max_len, num_seeds)
    train_snort_severe_baseline_rewards_stds_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], avg_train_snort_severe_baseline_rewards_data_novice_attacker)))
    train_snort_severe_baseline_rewards_means_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], avg_train_snort_severe_baseline_rewards_data_novice_attacker)))
    # train_snort_severe_baseline_rewards_means_novice_attacker = np.mean(tuple(train_snort_severe_baseline_rewards_data_novice_attacker), axis=0)
    # train_snort_severe_baseline_rewards_stds_novice_attacker = np.std(tuple(train_snort_severe_baseline_rewards_data_novice_attacker), axis=0, ddof=1)

    train_step_baseline_rewards_data_novice_attacker = list(map(lambda df: util.running_average_list(df["step_baseline_rewards"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    avg_train_step_baseline_rewards_data_novice_attacker = np.array(train_step_baseline_rewards_data_novice_attacker).reshape(max_len, num_seeds)
    train_step_baseline_rewards_stds_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], avg_train_step_baseline_rewards_data_novice_attacker)))
    train_step_baseline_rewards_means_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], avg_train_step_baseline_rewards_data_novice_attacker)))
    # train_step_baseline_rewards_means_novice_attacker = np.mean(tuple(train_step_baseline_rewards_data_novice_attacker), axis=0)
    # train_step_baseline_rewards_stds_novice_attacker = np.std(tuple(train_step_baseline_rewards_data_novice_attacker), axis=0, ddof=1)

    train_snort_severe_baseline_steps_data_novice_attacker = list(map(lambda df: util.running_average_list(df["snort_severe_baseline_steps"].values[0:max_len], running_avg),ppo_dfs_novice_attacker))
    avg_train_snort_severe_baseline_steps_data_novice_attacker = np.array(train_snort_severe_baseline_steps_data_novice_attacker).reshape(max_len, num_seeds)
    train_snort_severe_baseline_steps_stds_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], avg_train_snort_severe_baseline_steps_data_novice_attacker)))
    train_snort_severe_baseline_steps_means_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], avg_train_snort_severe_baseline_steps_data_novice_attacker)))
    # train_snort_severe_baseline_steps_means_novice_attacker = np.mean(tuple(train_snort_severe_baseline_steps_data_novice_attacker), axis=0)
    # train_snort_severe_baseline_steps_stds_novice_attacker = np.std(tuple(train_snort_severe_baseline_steps_data_novice_attacker), axis=0, ddof=1)

    train_step_baseline_steps_data_novice_attacker = list(map(lambda df: util.running_average_list(df["step_baseline_steps"].values[0:max_len], running_avg),ppo_dfs_novice_attacker))
    avg_train_step_baseline_steps_data_novice_attacker = np.array(train_step_baseline_steps_data_novice_attacker).reshape(max_len, num_seeds)
    train_step_baseline_steps_stds_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], avg_train_step_baseline_steps_data_novice_attacker)))
    train_step_baseline_steps_means_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], avg_train_step_baseline_steps_data_novice_attacker)))
    # train_step_baseline_steps_means_novice_attacker = np.mean(tuple(train_step_baseline_steps_data_novice_attacker), axis=0)
    # train_step_baseline_steps_stds_novice_attacker = np.std(tuple(train_step_baseline_steps_data_novice_attacker), axis=0, ddof=1)

    train_snort_severe_baseline_early_stopping_data_novice_attacker = list(map(lambda df: util.running_average_list(df["snort_severe_baseline_early_stopping"].values[0:max_len], running_avg),ppo_dfs_novice_attacker))
    avg_train_snort_severe_baseline_early_stopping_data_novice_attacker = np.array(train_snort_severe_baseline_early_stopping_data_novice_attacker).reshape(max_len, num_seeds)
    train_snort_severe_baseline_early_stopping_stds_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], avg_train_snort_severe_baseline_early_stopping_data_novice_attacker)))
    train_snort_severe_baseline_early_stopping_means_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], avg_train_snort_severe_baseline_early_stopping_data_novice_attacker)))
    # train_snort_severe_baseline_early_stopping_means_novice_attacker = np.mean(tuple(train_snort_severe_baseline_early_stopping_data_novice_attacker), axis=0)
    # train_snort_severe_baseline_early_stopping_stds_novice_attacker = np.std(tuple(train_snort_severe_baseline_early_stopping_data_novice_attacker), axis=0, ddof=1)

    train_step_baseline_early_stopping_data_novice_attacker = list(map(lambda df: util.running_average_list(df["step_baseline_early_stopping"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    avg_train_step_baseline_early_stopping_data_novice_attacker = np.array(train_step_baseline_early_stopping_data_novice_attacker).reshape(max_len, num_seeds)
    train_step_baseline_early_stopping_stds_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], avg_train_step_baseline_early_stopping_data_novice_attacker)))
    train_step_baseline_early_stopping_means_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], avg_train_step_baseline_early_stopping_data_novice_attacker)))
    # train_step_baseline_early_stopping_means_novice_attacker = np.mean(tuple(train_step_baseline_early_stopping_data_novice_attacker), axis=0)
    # train_step_baseline_early_stopping_stds_novice_attacker = np.std(tuple(train_step_baseline_early_stopping_data_novice_attacker), axis=0, ddof=1)

    train_snort_severe_baseline_caught_attacker_data_novice_attacker = list(map(lambda df: util.running_average_list(df["snort_severe_baseline_caught_attacker"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    avg_train_snort_severe_baseline_caught_attacker_data_novice_attacker = np.array(train_snort_severe_baseline_caught_attacker_data_novice_attacker).reshape(max_len, num_seeds)
    train_snort_severe_baseline_caught_attacker_stds_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], avg_train_snort_severe_baseline_caught_attacker_data_novice_attacker)))
    train_snort_severe_baseline_caught_attacker_means_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], avg_train_snort_severe_baseline_caught_attacker_data_novice_attacker)))
    # train_snort_severe_baseline_caught_attacker_means_novice_attacker = np.mean(tuple(train_snort_severe_baseline_caught_attacker_data_novice_attacker), axis=0)
    # train_snort_severe_baseline_caught_attacker_stds_novice_attacker = np.std(tuple(train_snort_severe_baseline_caught_attacker_data_novice_attacker), axis=0, ddof=1)

    train_step_baseline_caught_attacker_data_novice_attacker = list(map(lambda df: util.running_average_list(df["step_baseline_caught_attacker"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    avg_train_step_baseline_caught_attacker_data_novice_attacker = np.array(train_step_baseline_caught_attacker_data_novice_attacker).reshape(max_len, num_seeds)
    train_step_baseline_caught_attacker_stds_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], avg_train_step_baseline_caught_attacker_data_novice_attacker)))
    train_step_baseline_caught_attacker_means_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], avg_train_step_baseline_caught_attacker_data_novice_attacker)))
    # train_step_baseline_caught_attacker_means_novice_attacker = np.mean(tuple(train_step_baseline_caught_attacker_data_novice_attacker), axis=0)
    # train_step_baseline_caught_attacker_stds_novice_attacker = np.std(tuple(train_step_baseline_caught_attacker_data_novice_attacker), axis=0, ddof=1)

    train_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker = list(map(lambda df: util.running_average_list(df["snort_severe_baseline_uncaught_intrusion_steps"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    avg_train_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker = np.array(train_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker).reshape(max_len, num_seeds)
    train_snort_severe_baseline_uncaught_intrusion_steps_stds_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], avg_train_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker)))
    train_snort_severe_baseline_uncaught_intrusion_steps_means_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], avg_train_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker)))
    # train_snort_severe_baseline_uncaught_intrusion_steps_means_novice_attacker = np.mean(tuple(train_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker), axis=0)
    # train_snort_severe_baseline_uncaught_intrusion_steps_stds_novice_attacker = np.std(tuple(train_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker), axis=0, ddof=1)

    train_step_baseline_uncaught_intrusion_steps_data_novice_attacker = list(map(lambda df: util.running_average_list(df["step_baseline_uncaught_intrusion_steps"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    avg_train_step_baseline_uncaught_intrusion_steps_data_novice_attacker = np.array(train_step_baseline_uncaught_intrusion_steps_data_novice_attacker).reshape(max_len, num_seeds)
    train_step_baseline_uncaught_intrusion_steps_stds_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], avg_train_step_baseline_uncaught_intrusion_steps_data_novice_attacker)))
    train_step_baseline_uncaught_intrusion_steps_means_novice_attacker = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], avg_train_step_baseline_uncaught_intrusion_steps_data_novice_attacker)))
    # train_step_baseline_uncaught_intrusion_steps_means_novice_attacker = np.mean(tuple(train_step_baseline_uncaught_intrusion_steps_data_novice_attacker), axis=0)
    # train_step_baseline_uncaught_intrusion_steps_stds_novice_attacker = np.std(tuple(train_step_baseline_uncaught_intrusion_steps_data_novice_attacker), axis=0, ddof=1)

    train_defender_first_stop_step_novice_attacker_data = list(map(lambda df: util.running_average_list(df["avg_defender_first_stop_step"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    train_defender_first_stop_step_novice_attacker_data = np.array(train_defender_first_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    train_defender_first_stop_step_novice_attacker_stds = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],train_defender_first_stop_step_novice_attacker_data)))
    train_defender_first_stop_step_novice_attacker_means = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],train_defender_first_stop_step_novice_attacker_data)))
    # train_defender_first_stop_step_novice_attacker_means = np.mean(tuple(train_defender_first_stop_step_novice_attacker_data), axis=0)
    # train_defender_first_stop_step_novice_attacker_stds = np.std(tuple(train_defender_first_stop_step_novice_attacker_data), axis=0, ddof=1)

    train_defender_second_stop_step_novice_attacker_data = list(map(lambda df: util.running_average_list(df["avg_defender_second_stop_step"].values[0:max_len], running_avg),ppo_dfs_novice_attacker))
    train_defender_second_stop_step_novice_attacker_data = np.array(train_defender_second_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    train_defender_second_stop_step_novice_attacker_stds = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],train_defender_second_stop_step_novice_attacker_data)))
    train_defender_second_stop_step_novice_attacker_means = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],train_defender_second_stop_step_novice_attacker_data)))
    # train_defender_second_stop_step_novice_attacker_means = np.mean(tuple(train_defender_second_stop_step_novice_attacker_data), axis=0)
    # train_defender_second_stop_step_novice_attacker_stds = np.std(tuple(train_defender_second_stop_step_novice_attacker_data), axis=0, ddof=1)

    train_defender_third_stop_step_novice_attacker_data = list(map(lambda df: util.running_average_list(df["avg_defender_third_stop_step"].values[0:max_len], running_avg),ppo_dfs_novice_attacker))
    train_defender_third_stop_step_novice_attacker_data = np.array(train_defender_third_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    train_defender_third_stop_step_novice_attacker_stds = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], train_defender_third_stop_step_novice_attacker_data)))
    train_defender_third_stop_step_novice_attacker_means = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], train_defender_third_stop_step_novice_attacker_data)))
    # train_defender_third_stop_step_novice_attacker_means = np.mean(tuple(train_defender_third_stop_step_novice_attacker_data), axis=0)
    # train_defender_third_stop_step_novice_attacker_stds = np.std(tuple(train_defender_third_stop_step_novice_attacker_data), axis=0, ddof=1)

    train_defender_fourth_stop_step_novice_attacker_data = list(map(lambda df: util.running_average_list(df["avg_defender_fourth_stop_step"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    train_defender_fourth_stop_step_novice_attacker_data = np.array(train_defender_fourth_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    train_defender_fourth_stop_step_novice_attacker_stds = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], train_defender_fourth_stop_step_novice_attacker_data)))
    train_defender_fourth_stop_step_novice_attacker_means = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], train_defender_fourth_stop_step_novice_attacker_data)))
    # train_defender_fourth_stop_step_novice_attacker_means = np.mean(tuple(train_defender_fourth_stop_step_novice_attacker_data), axis=0)
    # train_defender_fourth_stop_step_novice_attacker_stds = np.std(tuple(train_defender_fourth_stop_step_novice_attacker_data), axis=0, ddof=1)

    train_defender_stops_remaining_novice_attacker_data = list(map(lambda df: util.running_average_list(df["avg_defender_stops_remaining"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    train_defender_stops_remaining_novice_attacker_data = np.array(train_defender_stops_remaining_novice_attacker_data).reshape(max_len, num_seeds)
    train_defender_stops_remaining_novice_attacker_stds = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], train_defender_stops_remaining_novice_attacker_data)))
    train_defender_stops_remaining_novice_attacker_means = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], train_defender_stops_remaining_novice_attacker_data)))
    # train_defender_stops_remaining_novice_attacker_means = np.mean(tuple(train_defender_stops_remaining_novice_attacker_data), axis=0)
    # train_defender_stops_remaining_novice_attacker_stds = np.std(tuple(train_defender_stops_remaining_novice_attacker_data), axis=0, ddof=1)

    train_optimal_first_stop_step_novice_attacker_data = list(map(lambda df: util.running_average_list(df["avg_optimal_first_stop_step"].values[0:max_len], running_avg),ppo_dfs_novice_attacker))
    train_optimal_first_stop_step_novice_attacker_data = np.array(train_optimal_first_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    train_optimal_first_stop_step_novice_attacker_stds = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], train_optimal_first_stop_step_novice_attacker_data)))
    train_optimal_first_stop_step_novice_attacker_means = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], train_optimal_first_stop_step_novice_attacker_data)))
    # train_optimal_first_stop_step_novice_attacker_means = np.mean(tuple(train_optimal_first_stop_step_novice_attacker_data), axis=0)
    # train_optimal_first_stop_step_novice_attacker_stds = np.std(tuple(train_optimal_first_stop_step_novice_attacker_data), axis=0, ddof=1)

    train_optimal_second_stop_step_novice_attacker_data = list(map(lambda df: util.running_average_list(df["avg_optimal_second_stop_step"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    train_optimal_second_stop_step_novice_attacker_data = np.array(train_optimal_second_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    train_optimal_second_stop_step_novice_attacker_stds = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], train_optimal_second_stop_step_novice_attacker_data)))
    train_optimal_second_stop_step_novice_attacker_means = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], train_optimal_second_stop_step_novice_attacker_data)))
    # train_optimal_second_stop_step_novice_attacker_means = np.mean(tuple(train_optimal_second_stop_step_novice_attacker_data), axis=0)
    # train_optimal_second_stop_step_novice_attacker_stds = np.std(tuple(train_optimal_second_stop_step_novice_attacker_data), axis=0, ddof=1)

    train_optimal_third_stop_step_novice_attacker_data = list(map(lambda df: util.running_average_list(df["avg_optimal_third_stop_step"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    train_optimal_third_stop_step_novice_attacker_data = np.array(train_optimal_third_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    train_optimal_third_stop_step_novice_attacker_stds = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], train_optimal_third_stop_step_novice_attacker_data)))
    train_optimal_third_stop_step_novice_attacker_means = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], train_optimal_third_stop_step_novice_attacker_data)))
    # train_optimal_third_stop_step_novice_attacker_means = np.mean(tuple(train_optimal_third_stop_step_novice_attacker_data), axis=0)
    # train_optimal_third_stop_step_novice_attacker_stds = np.std(tuple(train_optimal_third_stop_step_novice_attacker_data), axis=0, ddof=1)

    train_optimal_fourth_stop_step_novice_attacker_data = list(map(lambda df: util.running_average_list(df["avg_optimal_fourth_stop_step"].values[0:max_len], running_avg),ppo_dfs_novice_attacker))
    train_optimal_fourth_stop_step_novice_attacker_data = np.array(train_optimal_fourth_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    train_optimal_fourth_stop_step_novice_attacker_stds = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], train_optimal_fourth_stop_step_novice_attacker_data)))
    train_optimal_fourth_stop_step_novice_attacker_means = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], train_optimal_fourth_stop_step_novice_attacker_data)))
    # train_optimal_fourth_stop_step_novice_attacker_means = np.mean(tuple(train_optimal_fourth_stop_step_novice_attacker_data), axis=0)
    # train_optimal_fourth_stop_step_novice_attacker_stds = np.std(tuple(train_optimal_fourth_stop_step_novice_attacker_data), axis=0, ddof=1)

    train_optimal_stops_remaining_novice_attacker_data = list(map(lambda df: util.running_average_list(df["avg_optimal_stops_remaining"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    train_optimal_stops_remaining_novice_attacker_data = np.array(train_optimal_stops_remaining_novice_attacker_data).reshape(max_len, num_seeds)
    train_optimal_stops_remaining_novice_attacker_stds = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], train_optimal_stops_remaining_novice_attacker_data)))
    train_optimal_stops_remaining_novice_attacker_means = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], train_optimal_stops_remaining_novice_attacker_data)))
    # train_optimal_stops_remaining_novice_attacker_means = np.mean(tuple(train_optimal_stops_remaining_novice_attacker_data), axis=0)
    # train_optimal_stops_remaining_novice_attacker_stds = np.std(tuple(train_optimal_stops_remaining_novice_attacker_data), axis=0, ddof=1)

    train_snort_severe_baseline_first_stop_step_novice_attacker_data = list(map(lambda df: util.running_average_list(df["avg_snort_severe_baseline_first_stop_step"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    train_snort_severe_baseline_first_stop_step_novice_attacker_data = np.array(train_snort_severe_baseline_first_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    train_snort_severe_baseline_first_stop_step_novice_attacker_stds = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], train_snort_severe_baseline_first_stop_step_novice_attacker_data)))
    train_snort_severe_baseline_first_stop_step_novice_attacker_means = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], train_snort_severe_baseline_first_stop_step_novice_attacker_data)))
    # train_snort_severe_baseline_first_stop_step_novice_attacker_means = np.mean(tuple(train_snort_severe_baseline_first_stop_step_novice_attacker_data), axis=0)
    # train_snort_severe_baseline_first_stop_step_novice_attacker_stds = np.std(tuple(train_snort_severe_baseline_first_stop_step_novice_attacker_data), axis=0, ddof=1)

    train_snort_severe_baseline_second_stop_step_novice_attacker_data = list(map(lambda df: util.running_average_list(df["avg_snort_severe_baseline_second_stop_step"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    train_snort_severe_baseline_second_stop_step_novice_attacker_data = np.array(train_snort_severe_baseline_second_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    train_snort_severe_baseline_second_stop_step_novice_attacker_stds = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], train_snort_severe_baseline_second_stop_step_novice_attacker_data)))
    train_snort_severe_baseline_second_stop_step_novice_attacker_means = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], train_snort_severe_baseline_second_stop_step_novice_attacker_data)))
    # train_snort_severe_baseline_second_stop_step_novice_attacker_means = np.mean(tuple(train_snort_severe_baseline_second_stop_step_novice_attacker_data), axis=0)
    # train_snort_severe_baseline_second_stop_step_novice_attacker_stds = np.std(tuple(train_snort_severe_baseline_second_stop_step_novice_attacker_data), axis=0, ddof=1)

    train_snort_severe_baseline_third_stop_step_novice_attacker_data = list(map(lambda df: util.running_average_list(df["avg_snort_severe_baseline_third_stop_step"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    train_snort_severe_baseline_third_stop_step_novice_attacker_data = np.array(train_snort_severe_baseline_third_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    train_snort_severe_baseline_third_stop_step_novice_attacker_stds = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],train_snort_severe_baseline_third_stop_step_novice_attacker_data)))
    train_snort_severe_baseline_third_stop_step_novice_attacker_means = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], train_snort_severe_baseline_third_stop_step_novice_attacker_data)))
    # train_snort_severe_baseline_third_stop_step_novice_attacker_means = np.mean(tuple(train_snort_severe_baseline_third_stop_step_novice_attacker_data), axis=0)
    # train_snort_severe_baseline_third_stop_step_novice_attacker_stds = np.std(tuple(train_snort_severe_baseline_third_stop_step_novice_attacker_data), axis=0, ddof=1)

    train_snort_severe_baseline_fourth_stop_step_novice_attacker_data = list(map(lambda df: util.running_average_list(df["avg_snort_severe_baseline_fourth_stop_step"].values[0:max_len], running_avg),ppo_dfs_novice_attacker))
    train_snort_severe_baseline_fourth_stop_step_novice_attacker_data = np.array(train_snort_severe_baseline_fourth_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    train_snort_severe_baseline_fourth_stop_step_novice_attacker_stds = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],train_snort_severe_baseline_fourth_stop_step_novice_attacker_data)))
    train_snort_severe_baseline_fourth_stop_step_novice_attacker_means = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], train_snort_severe_baseline_fourth_stop_step_novice_attacker_data)))
    # train_snort_severe_baseline_fourth_stop_step_novice_attacker_means = np.mean(tuple(train_snort_severe_baseline_fourth_stop_step_novice_attacker_data), axis=0)
    # train_snort_severe_baseline_fourth_stop_step_novice_attacker_stds = np.std(tuple(train_snort_severe_baseline_fourth_stop_step_novice_attacker_data), axis=0, ddof=1)

    train_snort_severe_baseline_stops_remaining_novice_attacker_data = list(map(lambda df: util.running_average_list(df["avg_snort_severe_baseline_stops_remaining"].values[0:max_len], running_avg),ppo_dfs_novice_attacker))
    train_snort_severe_baseline_stops_remaining_novice_attacker_data = np.array(train_snort_severe_baseline_stops_remaining_novice_attacker_data).reshape(max_len, num_seeds)
    train_snort_severe_baseline_stops_remaining_novice_attacker_stds = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], train_snort_severe_baseline_stops_remaining_novice_attacker_data)))
    train_snort_severe_baseline_stops_remaining_novice_attacker_means = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], train_snort_severe_baseline_stops_remaining_novice_attacker_data)))
    # train_snort_severe_baseline_stops_remaining_novice_attacker_means = np.mean(tuple(train_snort_severe_baseline_stops_remaining_novice_attacker_data), axis=0)
    # train_snort_severe_baseline_stops_remaining_novice_attacker_stds = np.std(tuple(train_snort_severe_baseline_stops_remaining_novice_attacker_data), axis=0, ddof=1)

    train_step_baseline_first_stop_step_novice_attacker_data = list(map(lambda df: util.running_average_list(df["avg_step_baseline_first_stop_step"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    train_step_baseline_first_stop_step_novice_attacker_data = np.array(train_step_baseline_first_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    train_step_baseline_first_stop_step_novice_attacker_stds = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], train_step_baseline_first_stop_step_novice_attacker_data)))
    train_step_baseline_first_stop_step_novice_attacker_means = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], train_step_baseline_first_stop_step_novice_attacker_data)))
    # train_step_baseline_first_stop_step_novice_attacker_means = np.mean(tuple(train_step_baseline_first_stop_step_novice_attacker_data), axis=0)
    # train_step_baseline_first_stop_step_novice_attacker_stds = np.std(tuple(train_step_baseline_first_stop_step_novice_attacker_data), axis=0, ddof=1)

    train_step_baseline_second_stop_step_novice_attacker_data = list(map(lambda df: util.running_average_list(df["avg_step_baseline_second_stop_step"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    train_step_baseline_second_stop_step_novice_attacker_data = np.array(train_step_baseline_second_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    train_step_baseline_second_stop_step_novice_attacker_stds = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], train_step_baseline_second_stop_step_novice_attacker_data)))
    train_step_baseline_second_stop_step_novice_attacker_means = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], train_step_baseline_second_stop_step_novice_attacker_data)))
    # train_step_baseline_second_stop_step_novice_attacker_means = np.mean(tuple(train_step_baseline_second_stop_step_novice_attacker_data), axis=0)
    # train_step_baseline_second_stop_step_novice_attacker_stds = np.std(tuple(train_step_baseline_second_stop_step_novice_attacker_data), axis=0, ddof=1)

    train_step_baseline_third_stop_step_novice_attacker_data = list(map(lambda df: util.running_average_list(df["avg_step_baseline_third_stop_step"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    train_step_baseline_third_stop_step_novice_attacker_data = np.array(train_step_baseline_third_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    train_step_baseline_third_stop_step_novice_attacker_stds = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], train_step_baseline_third_stop_step_novice_attacker_data)))
    train_step_baseline_third_stop_step_novice_attacker_means = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], train_step_baseline_third_stop_step_novice_attacker_data)))
    # train_step_baseline_third_stop_step_novice_attacker_means = np.mean(tuple(train_step_baseline_third_stop_step_novice_attacker_data), axis=0)
    # train_step_baseline_third_stop_step_novice_attacker_stds = np.std(tuple(train_step_baseline_third_stop_step_novice_attacker_data), axis=0, ddof=1)

    train_step_baseline_fourth_stop_step_novice_attacker_data = list(map(lambda df: util.running_average_list(df["avg_step_baseline_fourth_stop_step"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    train_step_baseline_fourth_stop_step_novice_attacker_data = np.array(train_step_baseline_fourth_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    train_step_baseline_fourth_stop_step_novice_attacker_stds = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], train_step_baseline_fourth_stop_step_novice_attacker_data)))
    train_step_baseline_fourth_stop_step_novice_attacker_means = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], train_step_baseline_fourth_stop_step_novice_attacker_data)))
    # train_step_baseline_fourth_stop_step_novice_attacker_means = np.mean(tuple(train_step_baseline_fourth_stop_step_novice_attacker_data), axis=0)
    # train_step_baseline_fourth_stop_step_novice_attacker_stds = np.std(tuple(train_step_baseline_fourth_stop_step_novice_attacker_data), axis=0, ddof=1)

    train_step_baseline_stops_remaining_novice_attacker_data = list(map(lambda df: util.running_average_list(df["avg_step_baseline_stops_remaining"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    train_step_baseline_stops_remaining_novice_attacker_data = np.array(train_step_baseline_stops_remaining_novice_attacker_data).reshape(max_len, num_seeds)
    train_step_baseline_stops_remaining_novice_attacker_stds = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1], train_step_baseline_stops_remaining_novice_attacker_data)))
    train_step_baseline_stops_remaining_novice_attacker_means = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],train_step_baseline_stops_remaining_novice_attacker_data)))
    # train_step_baseline_stops_remaining_novice_attacker_means = np.mean(tuple(train_step_baseline_stops_remaining_novice_attacker_data), axis=0)
    # train_step_baseline_stops_remaining_novice_attacker_stds = np.std(tuple(train_step_baseline_stops_remaining_novice_attacker_data), axis=0, ddof=1)

    train_optimal_episode_steps_novice_attacker_data = list(map(lambda df: util.running_average_list(df["avg_optimal_episode_steps"].values[0:max_len], running_avg), ppo_dfs_novice_attacker))
    train_optimal_episode_steps_novice_attacker_data = np.array(train_optimal_episode_steps_novice_attacker_data).reshape(max_len, num_seeds)
    train_optimal_episode_steps_novice_attacker_stds = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],train_optimal_episode_steps_novice_attacker_data)))
    train_optimal_episode_steps_novice_attacker_means = np.array(list(map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0], train_optimal_episode_steps_novice_attacker_data)))
    # train_optimal_episode_steps_novice_attacker_means = np.mean(tuple(train_optimal_episode_steps_novice_attacker_data), axis=0)
    # train_optimal_episode_steps_novice_attacker_stds = np.std(tuple(train_optimal_episode_steps_novice_attacker_data), axis=0, ddof=1)

    # Eval Avg Novice Attacker

    avg_eval_rewards_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["defender_eval_avg_episode_rewards"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))

    avg_eval_rewards_data_novice_attacker = np.array(avg_eval_rewards_data_novice_attacker).reshape(max_len,
                                                                                                      num_seeds)
    avg_eval_rewards_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_rewards_data_novice_attacker)))
    avg_eval_rewards_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_rewards_data_novice_attacker)))
    # avg_eval_rewards_means_novice_attacker = np.mean(tuple(avg_eval_rewards_data_novice_attacker), axis=0)
    # avg_eval_rewards_stds_novice_attacker = np.std(tuple(avg_eval_rewards_data_novice_attacker), axis=0, ddof=1)

    avg_eval_steps_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_avg_episode_steps"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_steps_data_novice_attacker = np.array(avg_eval_steps_data_novice_attacker).reshape(max_len, num_seeds)
    avg_eval_steps_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_steps_data_novice_attacker)))
    avg_eval_steps_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_steps_data_novice_attacker)))
    # avg_eval_steps_means_novice_attacker = np.mean(tuple(avg_eval_steps_data_novice_attacker), axis=0)
    # avg_eval_steps_stds_novice_attacker = np.std(tuple(avg_eval_steps_data_novice_attacker), axis=0, ddof=1)

    avg_eval_caught_frac_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_caught_frac"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_caught_frac_data_novice_attacker = np.array(avg_eval_caught_frac_data_novice_attacker).reshape(max_len,
                                                                                                              num_seeds)
    avg_eval_caught_frac_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_caught_frac_data_novice_attacker)))
    avg_eval_caught_frac_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_caught_frac_data_novice_attacker)))
    # avg_eval_caught_frac_means_novice_attacker = np.mean(tuple(avg_eval_caught_frac_data_novice_attacker), axis=0)
    # avg_eval_caught_frac_stds_novice_attacker = np.std(tuple(avg_eval_caught_frac_data_novice_attacker), axis=0, ddof=1)

    avg_eval_early_stopping_frac_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_early_stopping_frac"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_early_stopping_data_novice_attacker = np.array(avg_eval_early_stopping_frac_data_novice_attacker).reshape(
        max_len, num_seeds)
    avg_eval_early_stopping_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_early_stopping_data_novice_attacker)))
    avg_eval_early_stopping_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_early_stopping_data_novice_attacker)))
    # avg_eval_early_stopping_means_novice_attacker = np.mean(tuple(avg_eval_early_stopping_data_novice_attacker), axis=0)
    # avg_eval_early_stopping_stds_novice_attacker = np.std(tuple(avg_eval_early_stopping_data_novice_attacker), axis=0, ddof=1)

    avg_eval_intrusion_frac_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_intrusion_frac"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_intrusion_frac_data_novice_attacker = np.array(avg_eval_intrusion_frac_data_novice_attacker).reshape(
        max_len, num_seeds)
    avg_eval_intrusion_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_intrusion_frac_data_novice_attacker)))
    avg_eval_intrusion_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_intrusion_frac_data_novice_attacker)))
    # avg_eval_intrusion_frac_means_novice_attacker = np.mean(tuple(avg_eval_intrusion_frac_data_novice_attacker), axis=0)
    # avg_eval_intrusion_frac_stds_novice_attacker = np.std(tuple(avg_eval_intrusion_frac_data_novice_attacker), axis=0, ddof=1)

    avg_eval_optimal_defender_rewards_novice_attacker_data = list(
        map(lambda df: util.running_average_list(df["eval_avg_optimal_defender_reward"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_optimal_defender_rewards_data_novice_attacker = np.array(
        avg_eval_optimal_defender_rewards_novice_attacker_data).reshape(max_len, num_seeds)
    avg_eval_optimal_defender_rewards_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_optimal_defender_rewards_data_novice_attacker)))
    avg_eval_optimal_defender_rewards_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_optimal_defender_rewards_data_novice_attacker)))
    # avg_eval_optimal_defender_rewards_novice_attacker_means = np.mean(tuple(avg_eval_optimal_defender_rewards_novice_attacker_data), axis=0)
    # avg_eval_optimal_defender_rewards_novice_attacker_stds = np.std(tuple(avg_eval_optimal_defender_rewards_novice_attacker_data), axis=0, ddof=1)

    avg_eval_i_steps_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_intrusion_steps"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_i_steps_data_novice_attacker = np.array(avg_eval_i_steps_data_novice_attacker).reshape(max_len,
                                                                                                      num_seeds)
    avg_eval_i_steps_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_i_steps_data_novice_attacker)))
    avg_eval_i_steps_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_i_steps_data_novice_attacker)))
    # avg_eval_i_steps_means_novice_attacker = np.mean(tuple(avg_eval_i_steps_data_novice_attacker), axis=0)
    # avg_eval_i_steps_stds_novice_attacker = np.std(tuple(avg_eval_i_steps_data_novice_attacker), axis=0, ddof=1)

    avg_eval_uncaught_intrusion_steps_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_avg_uncaught_intrusion_steps"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    # avg_eval_uncaught_intrusion_steps_means_novice_attacker = np.mean(tuple(avg_eval_uncaught_intrusion_steps_data_novice_attacker), axis=0)
    # avg_eval_uncaught_intrusion_steps_stds_novice_attacker = np.std(tuple(avg_eval_uncaught_intrusion_steps_data_novice_attacker), axis=0, ddof=1)
    avg_eval_uncaught_intrusion_steps_data_novice_attacker = np.array(
        avg_eval_uncaught_intrusion_steps_data_novice_attacker).reshape(max_len, num_seeds)
    avg_eval_uncaught_intrusion_steps_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_uncaught_intrusion_steps_data_novice_attacker)))
    avg_eval_uncaught_intrusion_steps_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_uncaught_intrusion_steps_data_novice_attacker)))

    eval_snort_severe_baseline_rewards_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_snort_severe_baseline_rewards"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_snort_severe_baseline_rewards_data_novice_attacker = np.array(
        eval_snort_severe_baseline_rewards_data_novice_attacker).reshape(max_len, num_seeds)
    eval_snort_severe_baseline_rewards_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_snort_severe_baseline_rewards_data_novice_attacker)))
    eval_snort_severe_baseline_rewards_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_snort_severe_baseline_rewards_data_novice_attacker)))
    # eval_snort_severe_baseline_rewards_means_novice_attacker = np.mean(tuple(eval_snort_severe_baseline_rewards_data_novice_attacker), axis=0)
    # eval_snort_severe_baseline_rewards_stds_novice_attacker = np.std(tuple(eval_snort_severe_baseline_rewards_data_novice_attacker), axis=0, ddof=1)

    eval_step_baseline_rewards_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_step_baseline_rewards"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_step_baseline_rewards_data_novice_attacker = np.array(
        eval_step_baseline_rewards_data_novice_attacker).reshape(max_len, num_seeds)
    eval_step_baseline_rewards_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_step_baseline_rewards_data_novice_attacker)))
    eval_step_baseline_rewards_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_step_baseline_rewards_data_novice_attacker)))
    # eval_step_baseline_rewards_means_novice_attacker = np.mean(tuple(eval_step_baseline_rewards_data_novice_attacker), axis=0)
    # eval_step_baseline_rewards_stds_novice_attacker = np.std(tuple(eval_step_baseline_rewards_data_novice_attacker), axis=0, ddof=1)

    eval_snort_severe_baseline_steps_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_snort_severe_baseline_steps"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_snort_severe_baseline_steps_data_novice_attacker = np.array(
        eval_snort_severe_baseline_steps_data_novice_attacker).reshape(max_len, num_seeds)
    eval_snort_severe_baseline_steps_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_snort_severe_baseline_steps_data_novice_attacker)))
    eval_snort_severe_baseline_steps_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_snort_severe_baseline_steps_data_novice_attacker)))
    # eval_snort_severe_baseline_steps_means_novice_attacker = np.mean(tuple(eval_snort_severe_baseline_steps_data_novice_attacker), axis=0)
    # eval_snort_severe_baseline_steps_stds_novice_attacker = np.std(tuple(eval_snort_severe_baseline_steps_data_novice_attacker), axis=0, ddof=1)

    eval_step_baseline_steps_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_step_baseline_steps"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_step_baseline_steps_data_novice_attacker = np.array(
        eval_step_baseline_steps_data_novice_attacker).reshape(max_len, num_seeds)
    eval_step_baseline_steps_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_step_baseline_steps_data_novice_attacker)))
    eval_step_baseline_steps_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_step_baseline_steps_data_novice_attacker)))
    # eval_step_baseline_steps_means_novice_attacker = np.mean(tuple(eval_step_baseline_steps_data_novice_attacker), axis=0)
    # eval_step_baseline_steps_stds_novice_attacker = np.std(tuple(eval_step_baseline_steps_data_novice_attacker), axis=0, ddof=1)

    eval_snort_severe_baseline_early_stopping_data_novice_attacker = list(map(
        lambda df: util.running_average_list(df["eval_snort_severe_baseline_early_stopping"].values[0:max_len], running_avg),
        ppo_dfs_novice_attacker))
    avg_eval_snort_severe_baseline_early_stopping_data_novice_attacker = np.array(
        eval_snort_severe_baseline_early_stopping_data_novice_attacker).reshape(max_len, num_seeds)
    eval_snort_severe_baseline_early_stopping_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_snort_severe_baseline_early_stopping_data_novice_attacker)))
    eval_snort_severe_baseline_early_stopping_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_snort_severe_baseline_early_stopping_data_novice_attacker)))
    # eval_snort_severe_baseline_early_stopping_means_novice_attacker = np.mean(tuple(eval_snort_severe_baseline_early_stopping_data_novice_attacker), axis=0)
    # eval_snort_severe_baseline_early_stopping_stds_novice_attacker = np.std(tuple(eval_snort_severe_baseline_early_stopping_data_novice_attacker), axis=0, ddof=1)

    eval_step_baseline_early_stopping_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_step_baseline_early_stopping"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_step_baseline_early_stopping_data_novice_attacker = np.array(
        eval_step_baseline_early_stopping_data_novice_attacker).reshape(max_len, num_seeds)
    eval_step_baseline_early_stopping_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_step_baseline_early_stopping_data_novice_attacker)))
    eval_step_baseline_early_stopping_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_step_baseline_early_stopping_data_novice_attacker)))
    # eval_step_baseline_early_stopping_means_novice_attacker = np.mean(tuple(eval_step_baseline_early_stopping_data_novice_attacker), axis=0)
    # eval_step_baseline_early_stopping_stds_novice_attacker = np.std(tuple(eval_step_baseline_early_stopping_data_novice_attacker), axis=0, ddof=1)

    eval_snort_severe_baseline_caught_attacker_data_novice_attacker = list(map(
        lambda df: util.running_average_list(df["eval_snort_severe_baseline_caught_attacker"].values[0:max_len],
                                             running_avg), ppo_dfs_novice_attacker))
    avg_eval_snort_severe_baseline_caught_attacker_data_novice_attacker = np.array(
        eval_snort_severe_baseline_caught_attacker_data_novice_attacker).reshape(max_len, num_seeds)
    eval_snort_severe_baseline_caught_attacker_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_snort_severe_baseline_caught_attacker_data_novice_attacker)))
    eval_snort_severe_baseline_caught_attacker_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_snort_severe_baseline_caught_attacker_data_novice_attacker)))
    # eval_snort_severe_baseline_caught_attacker_means_novice_attacker = np.mean(tuple(eval_snort_severe_baseline_caught_attacker_data_novice_attacker), axis=0)
    # eval_snort_severe_baseline_caught_attacker_stds_novice_attacker = np.std(tuple(eval_snort_severe_baseline_caught_attacker_data_novice_attacker), axis=0, ddof=1)

    eval_step_baseline_caught_attacker_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_step_baseline_caught_attacker"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_step_baseline_caught_attacker_data_novice_attacker = np.array(
        eval_step_baseline_caught_attacker_data_novice_attacker).reshape(max_len, num_seeds)
    eval_step_baseline_caught_attacker_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_step_baseline_caught_attacker_data_novice_attacker)))
    eval_step_baseline_caught_attacker_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_step_baseline_caught_attacker_data_novice_attacker)))
    # eval_step_baseline_caught_attacker_means_novice_attacker = np.mean(tuple(eval_step_baseline_caught_attacker_data_novice_attacker), axis=0)
    # eval_step_baseline_caught_attacker_stds_novice_attacker = np.std(tuple(eval_step_baseline_caught_attacker_data_novice_attacker), axis=0, ddof=1)

    eval_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker = list(map(
        lambda df: util.running_average_list(df["eval_snort_severe_baseline_uncaught_intrusion_steps"].values[0:max_len],
                                             running_avg), ppo_dfs_novice_attacker))
    avg_eval_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker = np.array(
        eval_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker).reshape(max_len, num_seeds)
    eval_snort_severe_baseline_uncaught_intrusion_steps_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker)))
    eval_snort_severe_baseline_uncaught_intrusion_steps_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker)))
    # eval_snort_severe_baseline_uncaught_intrusion_steps_means_novice_attacker = np.mean(tuple(eval_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker), axis=0)
    # eval_snort_severe_baseline_uncaught_intrusion_steps_stds_novice_attacker = np.std(tuple(eval_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker), axis=0, ddof=1)

    eval_step_baseline_uncaught_intrusion_steps_data_novice_attacker = list(map(
        lambda df: util.running_average_list(df["eval_step_baseline_uncaught_intrusion_steps"].values[0:max_len],
                                             running_avg), ppo_dfs_novice_attacker))
    avg_eval_step_baseline_uncaught_intrusion_steps_data_novice_attacker = np.array(
        eval_step_baseline_uncaught_intrusion_steps_data_novice_attacker).reshape(max_len, num_seeds)
    eval_step_baseline_uncaught_intrusion_steps_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_step_baseline_uncaught_intrusion_steps_data_novice_attacker)))
    eval_step_baseline_uncaught_intrusion_steps_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_step_baseline_uncaught_intrusion_steps_data_novice_attacker)))
    # eval_step_baseline_uncaught_intrusion_steps_means_novice_attacker = np.mean(tuple(eval_step_baseline_uncaught_intrusion_steps_data_novice_attacker), axis=0)
    # eval_step_baseline_uncaught_intrusion_steps_stds_novice_attacker = np.std(tuple(eval_step_baseline_uncaught_intrusion_steps_data_novice_attacker), axis=0, ddof=1)

    eval_defender_first_stop_step_novice_attacker_data = list(
        map(lambda df: util.running_average_list(df["eval_avg_defender_first_stop_step"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    eval_defender_first_stop_step_novice_attacker_data = np.array(
        eval_defender_first_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    eval_defender_first_stop_step_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_defender_first_stop_step_novice_attacker_data)))
    eval_defender_first_stop_step_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_defender_first_stop_step_novice_attacker_data)))
    # eval_defender_first_stop_step_novice_attacker_means = np.mean(tuple(eval_defender_first_stop_step_novice_attacker_data), axis=0)
    # eval_defender_first_stop_step_novice_attacker_stds = np.std(tuple(eval_defender_first_stop_step_novice_attacker_data), axis=0, ddof=1)

    eval_defender_second_stop_step_novice_attacker_data = list(
        map(lambda df: util.running_average_list(df["eval_avg_defender_second_stop_step"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    eval_defender_second_stop_step_novice_attacker_data = np.array(
        eval_defender_second_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    eval_defender_second_stop_step_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_defender_second_stop_step_novice_attacker_data)))
    eval_defender_second_stop_step_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_defender_second_stop_step_novice_attacker_data)))
    # eval_defender_second_stop_step_novice_attacker_means = np.mean(tuple(eval_defender_second_stop_step_novice_attacker_data), axis=0)
    # eval_defender_second_stop_step_novice_attacker_stds = np.std(tuple(eval_defender_second_stop_step_novice_attacker_data), axis=0, ddof=1)

    eval_defender_third_stop_step_novice_attacker_data = list(
        map(lambda df: util.running_average_list(df["eval_avg_defender_third_stop_step"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    eval_defender_third_stop_step_novice_attacker_data = np.array(
        eval_defender_third_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    eval_defender_third_stop_step_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_defender_third_stop_step_novice_attacker_data)))
    eval_defender_third_stop_step_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_defender_third_stop_step_novice_attacker_data)))
    # eval_defender_third_stop_step_novice_attacker_means = np.mean(tuple(eval_defender_third_stop_step_novice_attacker_data), axis=0)
    # eval_defender_third_stop_step_novice_attacker_stds = np.std(tuple(eval_defender_third_stop_step_novice_attacker_data), axis=0, ddof=1)

    eval_defender_fourth_stop_step_novice_attacker_data = list(
        map(lambda df: util.running_average_list(df["eval_avg_defender_fourth_stop_step"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    eval_defender_fourth_stop_step_novice_attacker_data = np.array(
        eval_defender_fourth_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    eval_defender_fourth_stop_step_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_defender_fourth_stop_step_novice_attacker_data)))
    eval_defender_fourth_stop_step_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_defender_fourth_stop_step_novice_attacker_data)))
    # eval_defender_fourth_stop_step_novice_attacker_means = np.mean(tuple(eval_defender_fourth_stop_step_novice_attacker_data), axis=0)
    # eval_defender_fourth_stop_step_novice_attacker_stds = np.std(tuple(eval_defender_fourth_stop_step_novice_attacker_data), axis=0, ddof=1)

    eval_defender_stops_remaining_novice_attacker_data = list(
        map(lambda df: util.running_average_list(df["eval_avg_defender_stops_remaining"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    eval_defender_stops_remaining_novice_attacker_data = np.array(
        eval_defender_stops_remaining_novice_attacker_data).reshape(max_len, num_seeds)
    eval_defender_stops_remaining_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_defender_stops_remaining_novice_attacker_data)))
    eval_defender_stops_remaining_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_defender_stops_remaining_novice_attacker_data)))
    # eval_defender_stops_remaining_novice_attacker_means = np.mean(tuple(eval_defender_stops_remaining_novice_attacker_data), axis=0)
    # eval_defender_stops_remaining_novice_attacker_stds = np.std(tuple(eval_defender_stops_remaining_novice_attacker_data), axis=0, ddof=1)

    eval_optimal_first_stop_step_novice_attacker_data = list(
        map(lambda df: util.running_average_list(df["eval_avg_optimal_first_stop_step"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    eval_optimal_first_stop_step_novice_attacker_data = np.array(
        eval_optimal_first_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    eval_optimal_first_stop_step_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_optimal_first_stop_step_novice_attacker_data)))
    eval_optimal_first_stop_step_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_optimal_first_stop_step_novice_attacker_data)))
    # eval_optimal_first_stop_step_novice_attacker_means = np.mean(tuple(eval_optimal_first_stop_step_novice_attacker_data), axis=0)
    # eval_optimal_first_stop_step_novice_attacker_stds = np.std(tuple(eval_optimal_first_stop_step_novice_attacker_data), axis=0, ddof=1)

    eval_optimal_second_stop_step_novice_attacker_data = list(
        map(lambda df: util.running_average_list(df["eval_avg_optimal_second_stop_step"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    eval_optimal_second_stop_step_novice_attacker_data = np.array(
        eval_optimal_second_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    eval_optimal_second_stop_step_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_optimal_second_stop_step_novice_attacker_data)))
    eval_optimal_second_stop_step_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_optimal_second_stop_step_novice_attacker_data)))
    # eval_optimal_second_stop_step_novice_attacker_means = np.mean(tuple(eval_optimal_second_stop_step_novice_attacker_data), axis=0)
    # eval_optimal_second_stop_step_novice_attacker_stds = np.std(tuple(eval_optimal_second_stop_step_novice_attacker_data), axis=0, ddof=1)

    eval_optimal_third_stop_step_novice_attacker_data = list(
        map(lambda df: util.running_average_list(df["eval_avg_optimal_third_stop_step"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    eval_optimal_third_stop_step_novice_attacker_data = np.array(
        eval_optimal_third_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    eval_optimal_third_stop_step_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_optimal_third_stop_step_novice_attacker_data)))
    eval_optimal_third_stop_step_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_optimal_third_stop_step_novice_attacker_data)))
    # eval_optimal_third_stop_step_novice_attacker_means = np.mean(tuple(eval_optimal_third_stop_step_novice_attacker_data), axis=0)
    # eval_optimal_third_stop_step_novice_attacker_stds = np.std(tuple(eval_optimal_third_stop_step_novice_attacker_data), axis=0, ddof=1)

    eval_optimal_fourth_stop_step_novice_attacker_data = list(
        map(lambda df: util.running_average_list(df["eval_avg_optimal_fourth_stop_step"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    eval_optimal_fourth_stop_step_novice_attacker_data = np.array(
        eval_optimal_fourth_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    eval_optimal_fourth_stop_step_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_optimal_fourth_stop_step_novice_attacker_data)))
    eval_optimal_fourth_stop_step_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_optimal_fourth_stop_step_novice_attacker_data)))
    # eval_optimal_fourth_stop_step_novice_attacker_means = np.mean(tuple(eval_optimal_fourth_stop_step_novice_attacker_data), axis=0)
    # eval_optimal_fourth_stop_step_novice_attacker_stds = np.std(tuple(eval_optimal_fourth_stop_step_novice_attacker_data), axis=0, ddof=1)

    eval_optimal_stops_remaining_novice_attacker_data = list(
        map(lambda df: util.running_average_list(df["eval_avg_optimal_stops_remaining"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    eval_optimal_stops_remaining_novice_attacker_data = np.array(
        eval_optimal_stops_remaining_novice_attacker_data).reshape(max_len, num_seeds)
    eval_optimal_stops_remaining_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_optimal_stops_remaining_novice_attacker_data)))
    eval_optimal_stops_remaining_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_optimal_stops_remaining_novice_attacker_data)))
    # eval_optimal_stops_remaining_novice_attacker_means = np.mean(tuple(eval_optimal_stops_remaining_novice_attacker_data), axis=0)
    # eval_optimal_stops_remaining_novice_attacker_stds = np.std(tuple(eval_optimal_stops_remaining_novice_attacker_data), axis=0, ddof=1)

    eval_snort_severe_baseline_first_stop_step_novice_attacker_data = list(map(
        lambda df: util.running_average_list(df["eval_avg_snort_severe_baseline_first_stop_step"].values[0:max_len],
                                             running_avg), ppo_dfs_novice_attacker))
    eval_snort_severe_baseline_first_stop_step_novice_attacker_data = np.array(
        eval_snort_severe_baseline_first_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    eval_snort_severe_baseline_first_stop_step_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_snort_severe_baseline_first_stop_step_novice_attacker_data)))
    eval_snort_severe_baseline_first_stop_step_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_snort_severe_baseline_first_stop_step_novice_attacker_data)))
    # eval_snort_severe_baseline_first_stop_step_novice_attacker_means = np.mean(tuple(eval_snort_severe_baseline_first_stop_step_novice_attacker_data), axis=0)
    # eval_snort_severe_baseline_first_stop_step_novice_attacker_stds = np.std(tuple(eval_snort_severe_baseline_first_stop_step_novice_attacker_data), axis=0, ddof=1)

    eval_snort_severe_baseline_second_stop_step_novice_attacker_data = list(map(
        lambda df: util.running_average_list(df["eval_avg_snort_severe_baseline_second_stop_step"].values[0:max_len],
                                             running_avg), ppo_dfs_novice_attacker))
    eval_snort_severe_baseline_second_stop_step_novice_attacker_data = np.array(
        eval_snort_severe_baseline_second_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    eval_snort_severe_baseline_second_stop_step_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_snort_severe_baseline_second_stop_step_novice_attacker_data)))
    eval_snort_severe_baseline_second_stop_step_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_snort_severe_baseline_second_stop_step_novice_attacker_data)))
    # eval_snort_severe_baseline_second_stop_step_novice_attacker_means = np.mean(tuple(eval_snort_severe_baseline_second_stop_step_novice_attacker_data), axis=0)
    # eval_snort_severe_baseline_second_stop_step_novice_attacker_stds = np.std(tuple(eval_snort_severe_baseline_second_stop_step_novice_attacker_data), axis=0, ddof=1)

    eval_snort_severe_baseline_third_stop_step_novice_attacker_data = list(map(
        lambda df: util.running_average_list(df["eval_avg_snort_severe_baseline_third_stop_step"].values[0:max_len],
                                             running_avg), ppo_dfs_novice_attacker))
    eval_snort_severe_baseline_third_stop_step_novice_attacker_data = np.array(
        eval_snort_severe_baseline_third_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    eval_snort_severe_baseline_third_stop_step_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_snort_severe_baseline_third_stop_step_novice_attacker_data)))
    eval_snort_severe_baseline_third_stop_step_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_snort_severe_baseline_third_stop_step_novice_attacker_data)))
    # eval_snort_severe_baseline_third_stop_step_novice_attacker_means = np.mean(tuple(eval_snort_severe_baseline_third_stop_step_novice_attacker_data), axis=0)
    # eval_snort_severe_baseline_third_stop_step_novice_attacker_stds = np.std(tuple(eval_snort_severe_baseline_third_stop_step_novice_attacker_data), axis=0, ddof=1)

    eval_snort_severe_baseline_fourth_stop_step_novice_attacker_data = list(map(
        lambda df: util.running_average_list(df["eval_avg_snort_severe_baseline_fourth_stop_step"].values[0:max_len],
                                             running_avg), ppo_dfs_novice_attacker))
    eval_snort_severe_baseline_fourth_stop_step_novice_attacker_data = np.array(
        eval_snort_severe_baseline_fourth_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    eval_snort_severe_baseline_fourth_stop_step_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_snort_severe_baseline_fourth_stop_step_novice_attacker_data)))
    eval_snort_severe_baseline_fourth_stop_step_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_snort_severe_baseline_fourth_stop_step_novice_attacker_data)))
    # eval_snort_severe_baseline_fourth_stop_step_novice_attacker_means = np.mean(tuple(eval_snort_severe_baseline_fourth_stop_step_novice_attacker_data), axis=0)
    # eval_snort_severe_baseline_fourth_stop_step_novice_attacker_stds = np.std(tuple(eval_snort_severe_baseline_fourth_stop_step_novice_attacker_data), axis=0, ddof=1)

    eval_snort_severe_baseline_stops_remaining_novice_attacker_data = list(map(
        lambda df: util.running_average_list(df["eval_avg_snort_severe_baseline_stops_remaining"].values[0:max_len],
                                             running_avg), ppo_dfs_novice_attacker))
    eval_snort_severe_baseline_stops_remaining_novice_attacker_data = np.array(
        eval_snort_severe_baseline_stops_remaining_novice_attacker_data).reshape(max_len, num_seeds)
    eval_snort_severe_baseline_stops_remaining_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_snort_severe_baseline_stops_remaining_novice_attacker_data)))
    eval_snort_severe_baseline_stops_remaining_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_snort_severe_baseline_stops_remaining_novice_attacker_data)))
    # eval_snort_severe_baseline_stops_remaining_novice_attacker_means = np.mean(tuple(eval_snort_severe_baseline_stops_remaining_novice_attacker_data), axis=0)
    # eval_snort_severe_baseline_stops_remaining_novice_attacker_stds = np.std(tuple(eval_snort_severe_baseline_stops_remaining_novice_attacker_data), axis=0, ddof=1)

    eval_step_baseline_first_stop_step_novice_attacker_data = list(map(
        lambda df: util.running_average_list(df["eval_avg_step_baseline_first_stop_step"].values[0:max_len], running_avg),
        ppo_dfs_novice_attacker))
    eval_step_baseline_first_stop_step_novice_attacker_data = np.array(
        eval_step_baseline_first_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    eval_step_baseline_first_stop_step_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_step_baseline_first_stop_step_novice_attacker_data)))
    eval_step_baseline_first_stop_step_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_step_baseline_first_stop_step_novice_attacker_data)))
    # eval_step_baseline_first_stop_step_novice_attacker_means = np.mean(tuple(eval_step_baseline_first_stop_step_novice_attacker_data), axis=0)
    # eval_step_baseline_first_stop_step_novice_attacker_stds = np.std(tuple(eval_step_baseline_first_stop_step_novice_attacker_data), axis=0, ddof=1)

    eval_step_baseline_second_stop_step_novice_attacker_data = list(map(
        lambda df: util.running_average_list(df["eval_avg_step_baseline_second_stop_step"].values[0:max_len], running_avg),
        ppo_dfs_novice_attacker))
    eval_step_baseline_second_stop_step_novice_attacker_data = np.array(
        eval_step_baseline_second_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    eval_step_baseline_second_stop_step_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_step_baseline_second_stop_step_novice_attacker_data)))
    eval_step_baseline_second_stop_step_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_step_baseline_second_stop_step_novice_attacker_data)))
    # eval_step_baseline_second_stop_step_novice_attacker_means = np.mean(tuple(eval_step_baseline_second_stop_step_novice_attacker_data), axis=0)
    # eval_step_baseline_second_stop_step_novice_attacker_stds = np.std(tuple(eval_step_baseline_second_stop_step_novice_attacker_data), axis=0, ddof=1)

    eval_step_baseline_third_stop_step_novice_attacker_data = list(map(
        lambda df: util.running_average_list(df["eval_avg_step_baseline_third_stop_step"].values[0:max_len], running_avg),
        ppo_dfs_novice_attacker))
    eval_step_baseline_third_stop_step_novice_attacker_data = np.array(
        eval_step_baseline_third_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    eval_step_baseline_third_stop_step_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_step_baseline_third_stop_step_novice_attacker_data)))
    eval_step_baseline_third_stop_step_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_step_baseline_third_stop_step_novice_attacker_data)))
    # eval_step_baseline_third_stop_step_novice_attacker_means = np.mean(tuple(eval_step_baseline_third_stop_step_novice_attacker_data), axis=0)
    # eval_step_baseline_third_stop_step_novice_attacker_stds = np.std(tuple(eval_step_baseline_third_stop_step_novice_attacker_data), axis=0, ddof=1)

    eval_step_baseline_fourth_stop_step_novice_attacker_data = list(map(
        lambda df: util.running_average_list(df["eval_avg_step_baseline_fourth_stop_step"].values[0:max_len], running_avg),
        ppo_dfs_novice_attacker))
    eval_step_baseline_fourth_stop_step_novice_attacker_data = np.array(
        eval_step_baseline_fourth_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    eval_step_baseline_fourth_stop_step_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_step_baseline_fourth_stop_step_novice_attacker_data)))
    eval_step_baseline_fourth_stop_step_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_step_baseline_fourth_stop_step_novice_attacker_data)))
    # eval_step_baseline_fourth_stop_step_novice_attacker_means = np.mean(tuple(eval_step_baseline_fourth_stop_step_novice_attacker_data), axis=0)
    # eval_step_baseline_fourth_stop_step_novice_attacker_stds = np.std(tuple(eval_step_baseline_fourth_stop_step_novice_attacker_data), axis=0, ddof=1)

    eval_step_baseline_stops_remaining_novice_attacker_data = list(map(
        lambda df: util.running_average_list(df["eval_avg_step_baseline_stops_remaining"].values[0:max_len], running_avg),
        ppo_dfs_novice_attacker))
    eval_step_baseline_stops_remaining_novice_attacker_data = np.array(
        eval_step_baseline_stops_remaining_novice_attacker_data).reshape(max_len, num_seeds)
    eval_step_baseline_stops_remaining_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_step_baseline_stops_remaining_novice_attacker_data)))
    eval_step_baseline_stops_remaining_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_step_baseline_stops_remaining_novice_attacker_data)))
    # eval_step_baseline_stops_remaining_novice_attacker_means = np.mean(tuple(eval_step_baseline_stops_remaining_novice_attacker_data), axis=0)
    # eval_step_baseline_stops_remaining_novice_attacker_stds = np.std(tuple(eval_step_baseline_stops_remaining_novice_attacker_data), axis=0, ddof=1)

    eval_optimal_episode_steps_novice_attacker_data = list(
        map(lambda df: util.running_average_list(df["eval_avg_optimal_episode_steps"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    eval_optimal_episode_steps_novice_attacker_data = np.array(
        eval_optimal_episode_steps_novice_attacker_data).reshape(max_len, num_seeds)
    eval_optimal_episode_steps_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_optimal_episode_steps_novice_attacker_data)))
    eval_optimal_episode_steps_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_optimal_episode_steps_novice_attacker_data)))
    # eval_optimal_episode_steps_novice_attacker_means = np.mean(tuple(eval_optimal_episode_steps_novice_attacker_data), axis=0)
    # eval_optimal_episode_steps_novice_attacker_stds = np.std(tuple(eval_optimal_episode_steps_novice_attacker_data), axis=0, ddof=1)


    # Eval 2 Avg Novice Attacker

    avg_eval_2_rewards_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["defender_eval_2_avg_episode_rewards"].values[0:max_len],
                                                 running_avg),
            ppo_dfs_novice_attacker))

    avg_eval_2_rewards_data_novice_attacker = np.array(avg_eval_2_rewards_data_novice_attacker).reshape(max_len,
                                                                                                    num_seeds)
    avg_eval_2_rewards_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_2_rewards_data_novice_attacker)))
    avg_eval_2_rewards_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_2_rewards_data_novice_attacker)))
    # avg_eval_2_rewards_means_novice_attacker = np.mean(tuple(avg_eval_2_rewards_data_novice_attacker), axis=0)
    # avg_eval_2_rewards_stds_novice_attacker = np.std(tuple(avg_eval_2_rewards_data_novice_attacker), axis=0, ddof=1)

    avg_eval_2_steps_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_2_avg_episode_steps"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_2_steps_data_novice_attacker = np.array(avg_eval_2_steps_data_novice_attacker).reshape(max_len, num_seeds)
    avg_eval_2_steps_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_2_steps_data_novice_attacker)))
    avg_eval_2_steps_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_2_steps_data_novice_attacker)))
    # avg_eval_2_steps_means_novice_attacker = np.mean(tuple(avg_eval_2_steps_data_novice_attacker), axis=0)
    # avg_eval_2_steps_stds_novice_attacker = np.std(tuple(avg_eval_2_steps_data_novice_attacker), axis=0, ddof=1)

    avg_eval_2_caught_frac_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_2_caught_frac"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_2_caught_frac_data_novice_attacker = np.array(avg_eval_2_caught_frac_data_novice_attacker).reshape(max_len,
                                                                                                            num_seeds)
    avg_eval_2_caught_frac_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_2_caught_frac_data_novice_attacker)))
    avg_eval_2_caught_frac_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_2_caught_frac_data_novice_attacker)))
    # avg_eval_2_caught_frac_means_novice_attacker = np.mean(tuple(avg_eval_2_caught_frac_data_novice_attacker), axis=0)
    # avg_eval_2_caught_frac_stds_novice_attacker = np.std(tuple(avg_eval_2_caught_frac_data_novice_attacker), axis=0, ddof=1)

    avg_eval_2_early_stopping_frac_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_2_early_stopping_frac"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_2_early_stopping_data_novice_attacker = np.array(avg_eval_2_early_stopping_frac_data_novice_attacker).reshape(
        max_len, num_seeds)
    avg_eval_2_early_stopping_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_2_early_stopping_data_novice_attacker)))
    avg_eval_2_early_stopping_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_2_early_stopping_data_novice_attacker)))
    # avg_eval_2_early_stopping_means_novice_attacker = np.mean(tuple(avg_eval_2_early_stopping_data_novice_attacker), axis=0)
    # avg_eval_2_early_stopping_stds_novice_attacker = np.std(tuple(avg_eval_2_early_stopping_data_novice_attacker), axis=0, ddof=1)

    avg_eval_2_intrusion_frac_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_2_intrusion_frac"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_2_intrusion_frac_data_novice_attacker = np.array(avg_eval_2_intrusion_frac_data_novice_attacker).reshape(
        max_len, num_seeds)
    avg_eval_2_intrusion_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_2_intrusion_frac_data_novice_attacker)))
    avg_eval_2_intrusion_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_2_intrusion_frac_data_novice_attacker)))
    # avg_eval_2_intrusion_frac_means_novice_attacker = np.mean(tuple(avg_eval_2_intrusion_frac_data_novice_attacker), axis=0)
    # avg_eval_2_intrusion_frac_stds_novice_attacker = np.std(tuple(avg_eval_2_intrusion_frac_data_novice_attacker), axis=0, ddof=1)

    avg_eval_2_optimal_defender_rewards_novice_attacker_data = list(
        map(lambda df: util.running_average_list(df["eval_2_avg_optimal_defender_reward"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_2_optimal_defender_rewards_data_novice_attacker = np.array(
        avg_eval_2_optimal_defender_rewards_novice_attacker_data).reshape(max_len, num_seeds)
    avg_eval_2_optimal_defender_rewards_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_2_optimal_defender_rewards_data_novice_attacker)))
    avg_eval_2_optimal_defender_rewards_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_2_optimal_defender_rewards_data_novice_attacker)))
    # avg_eval_2_optimal_defender_rewards_novice_attacker_means = np.mean(tuple(avg_eval_2_optimal_defender_rewards_novice_attacker_data), axis=0)
    # avg_eval_2_optimal_defender_rewards_novice_attacker_stds = np.std(tuple(avg_eval_2_optimal_defender_rewards_novice_attacker_data), axis=0, ddof=1)

    avg_eval_2_i_steps_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_2_intrusion_steps"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_2_i_steps_data_novice_attacker = np.array(avg_eval_2_i_steps_data_novice_attacker).reshape(max_len,
                                                                                                    num_seeds)
    avg_eval_2_i_steps_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_2_i_steps_data_novice_attacker)))
    avg_eval_2_i_steps_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_2_i_steps_data_novice_attacker)))
    # avg_eval_2_i_steps_means_novice_attacker = np.mean(tuple(avg_eval_2_i_steps_data_novice_attacker), axis=0)
    # avg_eval_2_i_steps_stds_novice_attacker = np.std(tuple(avg_eval_2_i_steps_data_novice_attacker), axis=0, ddof=1)

    avg_eval_2_uncaught_intrusion_steps_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_2_avg_uncaught_intrusion_steps"].values[0:max_len],
                                                 running_avg),
            ppo_dfs_novice_attacker))
    # avg_eval_2_uncaught_intrusion_steps_means_novice_attacker = np.mean(tuple(avg_eval_2_uncaught_intrusion_steps_data_novice_attacker), axis=0)
    # avg_eval_2_uncaught_intrusion_steps_stds_novice_attacker = np.std(tuple(avg_eval_2_uncaught_intrusion_steps_data_novice_attacker), axis=0, ddof=1)
    avg_eval_2_uncaught_intrusion_steps_data_novice_attacker = np.array(
        avg_eval_2_uncaught_intrusion_steps_data_novice_attacker).reshape(max_len, num_seeds)
    avg_eval_2_uncaught_intrusion_steps_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_2_uncaught_intrusion_steps_data_novice_attacker)))
    avg_eval_2_uncaught_intrusion_steps_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_2_uncaught_intrusion_steps_data_novice_attacker)))

    eval_2_snort_severe_baseline_rewards_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_2_snort_severe_baseline_rewards"].values[0:max_len],
                                                 running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_2_snort_severe_baseline_rewards_data_novice_attacker = np.array(
        eval_2_snort_severe_baseline_rewards_data_novice_attacker).reshape(max_len, num_seeds)
    eval_2_snort_severe_baseline_rewards_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_2_snort_severe_baseline_rewards_data_novice_attacker)))
    eval_2_snort_severe_baseline_rewards_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_2_snort_severe_baseline_rewards_data_novice_attacker)))
    # eval_2_snort_severe_baseline_rewards_means_novice_attacker = np.mean(tuple(eval_2_snort_severe_baseline_rewards_data_novice_attacker), axis=0)
    # eval_2_snort_severe_baseline_rewards_stds_novice_attacker = np.std(tuple(eval_2_snort_severe_baseline_rewards_data_novice_attacker), axis=0, ddof=1)

    eval_2_step_baseline_rewards_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_2_step_baseline_rewards"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_2_step_baseline_rewards_data_novice_attacker = np.array(
        eval_2_step_baseline_rewards_data_novice_attacker).reshape(max_len, num_seeds)
    eval_2_step_baseline_rewards_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_2_step_baseline_rewards_data_novice_attacker)))
    eval_2_step_baseline_rewards_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_2_step_baseline_rewards_data_novice_attacker)))
    # eval_2_step_baseline_rewards_means_novice_attacker = np.mean(tuple(eval_2_step_baseline_rewards_data_novice_attacker), axis=0)
    # eval_2_step_baseline_rewards_stds_novice_attacker = np.std(tuple(eval_2_step_baseline_rewards_data_novice_attacker), axis=0, ddof=1)

    eval_2_snort_severe_baseline_steps_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_2_snort_severe_baseline_steps"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_2_snort_severe_baseline_steps_data_novice_attacker = np.array(
        eval_2_snort_severe_baseline_steps_data_novice_attacker).reshape(max_len, num_seeds)
    eval_2_snort_severe_baseline_steps_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_2_snort_severe_baseline_steps_data_novice_attacker)))
    eval_2_snort_severe_baseline_steps_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_2_snort_severe_baseline_steps_data_novice_attacker)))
    # eval_2_snort_severe_baseline_steps_means_novice_attacker = np.mean(tuple(eval_2_snort_severe_baseline_steps_data_novice_attacker), axis=0)
    # eval_2_snort_severe_baseline_steps_stds_novice_attacker = np.std(tuple(eval_2_snort_severe_baseline_steps_data_novice_attacker), axis=0, ddof=1)

    eval_2_step_baseline_steps_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_2_step_baseline_steps"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_2_step_baseline_steps_data_novice_attacker = np.array(
        eval_2_step_baseline_steps_data_novice_attacker).reshape(max_len, num_seeds)
    eval_2_step_baseline_steps_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_2_step_baseline_steps_data_novice_attacker)))
    eval_2_step_baseline_steps_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_2_step_baseline_steps_data_novice_attacker)))
    # eval_2_step_baseline_steps_means_novice_attacker = np.mean(tuple(eval_2_step_baseline_steps_data_novice_attacker), axis=0)
    # eval_2_step_baseline_steps_stds_novice_attacker = np.std(tuple(eval_2_step_baseline_steps_data_novice_attacker), axis=0, ddof=1)

    eval_2_snort_severe_baseline_early_stopping_data_novice_attacker = list(map(
        lambda df: util.running_average_list(df["eval_2_snort_severe_baseline_early_stopping"].values[0:max_len],
                                             running_avg),
        ppo_dfs_novice_attacker))
    avg_eval_2_snort_severe_baseline_early_stopping_data_novice_attacker = np.array(
        eval_2_snort_severe_baseline_early_stopping_data_novice_attacker).reshape(max_len, num_seeds)
    eval_2_snort_severe_baseline_early_stopping_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_2_snort_severe_baseline_early_stopping_data_novice_attacker)))
    eval_2_snort_severe_baseline_early_stopping_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_2_snort_severe_baseline_early_stopping_data_novice_attacker)))
    # eval_2_snort_severe_baseline_early_stopping_means_novice_attacker = np.mean(tuple(eval_2_snort_severe_baseline_early_stopping_data_novice_attacker), axis=0)
    # eval_2_snort_severe_baseline_early_stopping_stds_novice_attacker = np.std(tuple(eval_2_snort_severe_baseline_early_stopping_data_novice_attacker), axis=0, ddof=1)

    eval_2_step_baseline_early_stopping_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_2_step_baseline_early_stopping"].values[0:max_len],
                                                 running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_2_step_baseline_early_stopping_data_novice_attacker = np.array(
        eval_2_step_baseline_early_stopping_data_novice_attacker).reshape(max_len, num_seeds)
    eval_2_step_baseline_early_stopping_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_2_step_baseline_early_stopping_data_novice_attacker)))
    eval_2_step_baseline_early_stopping_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_2_step_baseline_early_stopping_data_novice_attacker)))
    # eval_2_step_baseline_early_stopping_means_novice_attacker = np.mean(tuple(eval_2_step_baseline_early_stopping_data_novice_attacker), axis=0)
    # eval_2_step_baseline_early_stopping_stds_novice_attacker = np.std(tuple(eval_2_step_baseline_early_stopping_data_novice_attacker), axis=0, ddof=1)

    eval_2_snort_severe_baseline_caught_attacker_data_novice_attacker = list(map(
        lambda df: util.running_average_list(df["eval_2_snort_severe_baseline_caught_attacker"].values[0:max_len],
                                             running_avg), ppo_dfs_novice_attacker))
    avg_eval_2_snort_severe_baseline_caught_attacker_data_novice_attacker = np.array(
        eval_2_snort_severe_baseline_caught_attacker_data_novice_attacker).reshape(max_len, num_seeds)
    eval_2_snort_severe_baseline_caught_attacker_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_2_snort_severe_baseline_caught_attacker_data_novice_attacker)))
    eval_2_snort_severe_baseline_caught_attacker_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_2_snort_severe_baseline_caught_attacker_data_novice_attacker)))
    # eval_2_snort_severe_baseline_caught_attacker_means_novice_attacker = np.mean(tuple(eval_2_snort_severe_baseline_caught_attacker_data_novice_attacker), axis=0)
    # eval_2_snort_severe_baseline_caught_attacker_stds_novice_attacker = np.std(tuple(eval_2_snort_severe_baseline_caught_attacker_data_novice_attacker), axis=0, ddof=1)

    eval_2_step_baseline_caught_attacker_data_novice_attacker = list(
        map(lambda df: util.running_average_list(df["eval_2_step_baseline_caught_attacker"].values[0:max_len],
                                                 running_avg),
            ppo_dfs_novice_attacker))
    avg_eval_2_step_baseline_caught_attacker_data_novice_attacker = np.array(
        eval_2_step_baseline_caught_attacker_data_novice_attacker).reshape(max_len, num_seeds)
    eval_2_step_baseline_caught_attacker_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_2_step_baseline_caught_attacker_data_novice_attacker)))
    eval_2_step_baseline_caught_attacker_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_2_step_baseline_caught_attacker_data_novice_attacker)))
    # eval_2_step_baseline_caught_attacker_means_novice_attacker = np.mean(tuple(eval_2_step_baseline_caught_attacker_data_novice_attacker), axis=0)
    # eval_2_step_baseline_caught_attacker_stds_novice_attacker = np.std(tuple(eval_2_step_baseline_caught_attacker_data_novice_attacker), axis=0, ddof=1)

    eval_2_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker = list(map(
        lambda df: util.running_average_list(
            df["eval_2_snort_severe_baseline_uncaught_intrusion_steps"].values[0:max_len],
            running_avg), ppo_dfs_novice_attacker))
    avg_eval_2_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker = np.array(
        eval_2_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker).reshape(max_len, num_seeds)
    eval_2_snort_severe_baseline_uncaught_intrusion_steps_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_2_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker)))
    eval_2_snort_severe_baseline_uncaught_intrusion_steps_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_2_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker)))
    # eval_2_snort_severe_baseline_uncaught_intrusion_steps_means_novice_attacker = np.mean(tuple(eval_2_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker), axis=0)
    # eval_2_snort_severe_baseline_uncaught_intrusion_steps_stds_novice_attacker = np.std(tuple(eval_2_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker), axis=0, ddof=1)

    eval_2_step_baseline_uncaught_intrusion_steps_data_novice_attacker = list(map(
        lambda df: util.running_average_list(df["eval_2_step_baseline_uncaught_intrusion_steps"].values[0:max_len],
                                             running_avg), ppo_dfs_novice_attacker))
    avg_eval_2_step_baseline_uncaught_intrusion_steps_data_novice_attacker = np.array(
        eval_2_step_baseline_uncaught_intrusion_steps_data_novice_attacker).reshape(max_len, num_seeds)
    eval_2_step_baseline_uncaught_intrusion_steps_stds_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            avg_eval_2_step_baseline_uncaught_intrusion_steps_data_novice_attacker)))
    eval_2_step_baseline_uncaught_intrusion_steps_means_novice_attacker = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            avg_eval_2_step_baseline_uncaught_intrusion_steps_data_novice_attacker)))
    # eval_2_step_baseline_uncaught_intrusion_steps_means_novice_attacker = np.mean(tuple(eval_2_step_baseline_uncaught_intrusion_steps_data_novice_attacker), axis=0)
    # eval_2_step_baseline_uncaught_intrusion_steps_stds_novice_attacker = np.std(tuple(eval_2_step_baseline_uncaught_intrusion_steps_data_novice_attacker), axis=0, ddof=1)

    eval_2_defender_first_stop_step_novice_attacker_data = list(
        map(lambda df: util.running_average_list(df["eval_2_avg_defender_first_stop_step"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    eval_2_defender_first_stop_step_novice_attacker_data = np.array(
        eval_2_defender_first_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    eval_2_defender_first_stop_step_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_2_defender_first_stop_step_novice_attacker_data)))
    eval_2_defender_first_stop_step_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_2_defender_first_stop_step_novice_attacker_data)))
    # eval_2_defender_first_stop_step_novice_attacker_means = np.mean(tuple(eval_2_defender_first_stop_step_novice_attacker_data), axis=0)
    # eval_2_defender_first_stop_step_novice_attacker_stds = np.std(tuple(eval_2_defender_first_stop_step_novice_attacker_data), axis=0, ddof=1)

    eval_2_defender_second_stop_step_novice_attacker_data = list(
        map(lambda df: util.running_average_list(df["eval_2_avg_defender_second_stop_step"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    eval_2_defender_second_stop_step_novice_attacker_data = np.array(
        eval_2_defender_second_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    eval_2_defender_second_stop_step_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_2_defender_second_stop_step_novice_attacker_data)))
    eval_2_defender_second_stop_step_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_2_defender_second_stop_step_novice_attacker_data)))
    # eval_2_defender_second_stop_step_novice_attacker_means = np.mean(tuple(eval_2_defender_second_stop_step_novice_attacker_data), axis=0)
    # eval_2_defender_second_stop_step_novice_attacker_stds = np.std(tuple(eval_2_defender_second_stop_step_novice_attacker_data), axis=0, ddof=1)

    eval_2_defender_third_stop_step_novice_attacker_data = list(
        map(lambda df: util.running_average_list(df["eval_2_avg_defender_third_stop_step"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    eval_2_defender_third_stop_step_novice_attacker_data = np.array(
        eval_2_defender_third_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    eval_2_defender_third_stop_step_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_2_defender_third_stop_step_novice_attacker_data)))
    eval_2_defender_third_stop_step_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_2_defender_third_stop_step_novice_attacker_data)))
    # eval_2_defender_third_stop_step_novice_attacker_means = np.mean(tuple(eval_2_defender_third_stop_step_novice_attacker_data), axis=0)
    # eval_2_defender_third_stop_step_novice_attacker_stds = np.std(tuple(eval_2_defender_third_stop_step_novice_attacker_data), axis=0, ddof=1)

    eval_2_defender_fourth_stop_step_novice_attacker_data = list(
        map(lambda df: util.running_average_list(df["eval_2_avg_defender_fourth_stop_step"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    eval_2_defender_fourth_stop_step_novice_attacker_data = np.array(
        eval_2_defender_fourth_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    eval_2_defender_fourth_stop_step_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_2_defender_fourth_stop_step_novice_attacker_data)))
    eval_2_defender_fourth_stop_step_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_2_defender_fourth_stop_step_novice_attacker_data)))
    # eval_2_defender_fourth_stop_step_novice_attacker_means = np.mean(tuple(eval_2_defender_fourth_stop_step_novice_attacker_data), axis=0)
    # eval_2_defender_fourth_stop_step_novice_attacker_stds = np.std(tuple(eval_2_defender_fourth_stop_step_novice_attacker_data), axis=0, ddof=1)

    eval_2_defender_stops_remaining_novice_attacker_data = list(
        map(lambda df: util.running_average_list(df["eval_2_avg_defender_stops_remaining"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    eval_2_defender_stops_remaining_novice_attacker_data = np.array(
        eval_2_defender_stops_remaining_novice_attacker_data).reshape(max_len, num_seeds)
    eval_2_defender_stops_remaining_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_2_defender_stops_remaining_novice_attacker_data)))
    eval_2_defender_stops_remaining_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_2_defender_stops_remaining_novice_attacker_data)))
    # eval_2_defender_stops_remaining_novice_attacker_means = np.mean(tuple(eval_2_defender_stops_remaining_novice_attacker_data), axis=0)
    # eval_2_defender_stops_remaining_novice_attacker_stds = np.std(tuple(eval_2_defender_stops_remaining_novice_attacker_data), axis=0, ddof=1)

    eval_2_optimal_first_stop_step_novice_attacker_data = list(
        map(lambda df: util.running_average_list(df["eval_2_avg_optimal_first_stop_step"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    eval_2_optimal_first_stop_step_novice_attacker_data = np.array(
        eval_2_optimal_first_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    eval_2_optimal_first_stop_step_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_2_optimal_first_stop_step_novice_attacker_data)))
    eval_2_optimal_first_stop_step_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_2_optimal_first_stop_step_novice_attacker_data)))
    # eval_2_optimal_first_stop_step_novice_attacker_means = np.mean(tuple(eval_2_optimal_first_stop_step_novice_attacker_data), axis=0)
    # eval_2_optimal_first_stop_step_novice_attacker_stds = np.std(tuple(eval_2_optimal_first_stop_step_novice_attacker_data), axis=0, ddof=1)

    eval_2_optimal_second_stop_step_novice_attacker_data = list(
        map(lambda df: util.running_average_list(df["eval_2_avg_optimal_second_stop_step"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    eval_2_optimal_second_stop_step_novice_attacker_data = np.array(
        eval_2_optimal_second_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    eval_2_optimal_second_stop_step_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_2_optimal_second_stop_step_novice_attacker_data)))
    eval_2_optimal_second_stop_step_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_2_optimal_second_stop_step_novice_attacker_data)))
    # eval_2_optimal_second_stop_step_novice_attacker_means = np.mean(tuple(eval_2_optimal_second_stop_step_novice_attacker_data), axis=0)
    # eval_2_optimal_second_stop_step_novice_attacker_stds = np.std(tuple(eval_2_optimal_second_stop_step_novice_attacker_data), axis=0, ddof=1)

    eval_2_optimal_third_stop_step_novice_attacker_data = list(
        map(lambda df: util.running_average_list(df["eval_2_avg_optimal_third_stop_step"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    eval_2_optimal_third_stop_step_novice_attacker_data = np.array(
        eval_2_optimal_third_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    eval_2_optimal_third_stop_step_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_2_optimal_third_stop_step_novice_attacker_data)))
    eval_2_optimal_third_stop_step_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_2_optimal_third_stop_step_novice_attacker_data)))
    # eval_2_optimal_third_stop_step_novice_attacker_means = np.mean(tuple(eval_2_optimal_third_stop_step_novice_attacker_data), axis=0)
    # eval_2_optimal_third_stop_step_novice_attacker_stds = np.std(tuple(eval_2_optimal_third_stop_step_novice_attacker_data), axis=0, ddof=1)

    eval_2_optimal_fourth_stop_step_novice_attacker_data = list(
        map(lambda df: util.running_average_list(df["eval_2_avg_optimal_fourth_stop_step"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    eval_2_optimal_fourth_stop_step_novice_attacker_data = np.array(
        eval_2_optimal_fourth_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    eval_2_optimal_fourth_stop_step_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_2_optimal_fourth_stop_step_novice_attacker_data)))
    eval_2_optimal_fourth_stop_step_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_2_optimal_fourth_stop_step_novice_attacker_data)))
    # eval_2_optimal_fourth_stop_step_novice_attacker_means = np.mean(tuple(eval_2_optimal_fourth_stop_step_novice_attacker_data), axis=0)
    # eval_2_optimal_fourth_stop_step_novice_attacker_stds = np.std(tuple(eval_2_optimal_fourth_stop_step_novice_attacker_data), axis=0, ddof=1)

    eval_2_optimal_stops_remaining_novice_attacker_data = list(
        map(lambda df: util.running_average_list(df["eval_2_avg_optimal_stops_remaining"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    eval_2_optimal_stops_remaining_novice_attacker_data = np.array(
        eval_2_optimal_stops_remaining_novice_attacker_data).reshape(max_len, num_seeds)
    eval_2_optimal_stops_remaining_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_2_optimal_stops_remaining_novice_attacker_data)))
    eval_2_optimal_stops_remaining_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_2_optimal_stops_remaining_novice_attacker_data)))
    # eval_2_optimal_stops_remaining_novice_attacker_means = np.mean(tuple(eval_2_optimal_stops_remaining_novice_attacker_data), axis=0)
    # eval_2_optimal_stops_remaining_novice_attacker_stds = np.std(tuple(eval_2_optimal_stops_remaining_novice_attacker_data), axis=0, ddof=1)

    eval_2_snort_severe_baseline_first_stop_step_novice_attacker_data = list(map(
        lambda df: util.running_average_list(df["eval_2_avg_snort_severe_baseline_first_stop_step"].values[0:max_len],
                                             running_avg), ppo_dfs_novice_attacker))
    eval_2_snort_severe_baseline_first_stop_step_novice_attacker_data = np.array(
        eval_2_snort_severe_baseline_first_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    eval_2_snort_severe_baseline_first_stop_step_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_2_snort_severe_baseline_first_stop_step_novice_attacker_data)))
    eval_2_snort_severe_baseline_first_stop_step_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_2_snort_severe_baseline_first_stop_step_novice_attacker_data)))
    # eval_2_snort_severe_baseline_first_stop_step_novice_attacker_means = np.mean(tuple(eval_2_snort_severe_baseline_first_stop_step_novice_attacker_data), axis=0)
    # eval_2_snort_severe_baseline_first_stop_step_novice_attacker_stds = np.std(tuple(eval_2_snort_severe_baseline_first_stop_step_novice_attacker_data), axis=0, ddof=1)

    eval_2_snort_severe_baseline_second_stop_step_novice_attacker_data = list(map(
        lambda df: util.running_average_list(df["eval_2_avg_snort_severe_baseline_second_stop_step"].values[0:max_len],
                                             running_avg), ppo_dfs_novice_attacker))
    eval_2_snort_severe_baseline_second_stop_step_novice_attacker_data = np.array(
        eval_2_snort_severe_baseline_second_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    eval_2_snort_severe_baseline_second_stop_step_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_2_snort_severe_baseline_second_stop_step_novice_attacker_data)))
    eval_2_snort_severe_baseline_second_stop_step_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_2_snort_severe_baseline_second_stop_step_novice_attacker_data)))
    # eval_2_snort_severe_baseline_second_stop_step_novice_attacker_means = np.mean(tuple(eval_2_snort_severe_baseline_second_stop_step_novice_attacker_data), axis=0)
    # eval_2_snort_severe_baseline_second_stop_step_novice_attacker_stds = np.std(tuple(eval_2_snort_severe_baseline_second_stop_step_novice_attacker_data), axis=0, ddof=1)

    eval_2_snort_severe_baseline_third_stop_step_novice_attacker_data = list(map(
        lambda df: util.running_average_list(df["eval_2_avg_snort_severe_baseline_third_stop_step"].values[0:max_len],
                                             running_avg), ppo_dfs_novice_attacker))
    eval_2_snort_severe_baseline_third_stop_step_novice_attacker_data = np.array(
        eval_2_snort_severe_baseline_third_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    eval_2_snort_severe_baseline_third_stop_step_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_2_snort_severe_baseline_third_stop_step_novice_attacker_data)))
    eval_2_snort_severe_baseline_third_stop_step_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_2_snort_severe_baseline_third_stop_step_novice_attacker_data)))
    # eval_2_snort_severe_baseline_third_stop_step_novice_attacker_means = np.mean(tuple(eval_2_snort_severe_baseline_third_stop_step_novice_attacker_data), axis=0)
    # eval_2_snort_severe_baseline_third_stop_step_novice_attacker_stds = np.std(tuple(eval_2_snort_severe_baseline_third_stop_step_novice_attacker_data), axis=0, ddof=1)

    eval_2_snort_severe_baseline_fourth_stop_step_novice_attacker_data = list(map(
        lambda df: util.running_average_list(df["eval_2_avg_snort_severe_baseline_fourth_stop_step"].values[0:max_len],
                                             running_avg), ppo_dfs_novice_attacker))
    eval_2_snort_severe_baseline_fourth_stop_step_novice_attacker_data = np.array(
        eval_2_snort_severe_baseline_fourth_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    eval_2_snort_severe_baseline_fourth_stop_step_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_2_snort_severe_baseline_fourth_stop_step_novice_attacker_data)))
    eval_2_snort_severe_baseline_fourth_stop_step_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_2_snort_severe_baseline_fourth_stop_step_novice_attacker_data)))
    # eval_2_snort_severe_baseline_fourth_stop_step_novice_attacker_means = np.mean(tuple(eval_2_snort_severe_baseline_fourth_stop_step_novice_attacker_data), axis=0)
    # eval_2_snort_severe_baseline_fourth_stop_step_novice_attacker_stds = np.std(tuple(eval_2_snort_severe_baseline_fourth_stop_step_novice_attacker_data), axis=0, ddof=1)

    eval_2_snort_severe_baseline_stops_remaining_novice_attacker_data = list(map(
        lambda df: util.running_average_list(df["eval_2_avg_snort_severe_baseline_stops_remaining"].values[0:max_len],
                                             running_avg), ppo_dfs_novice_attacker))
    eval_2_snort_severe_baseline_stops_remaining_novice_attacker_data = np.array(
        eval_2_snort_severe_baseline_stops_remaining_novice_attacker_data).reshape(max_len, num_seeds)
    eval_2_snort_severe_baseline_stops_remaining_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_2_snort_severe_baseline_stops_remaining_novice_attacker_data)))
    eval_2_snort_severe_baseline_stops_remaining_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_2_snort_severe_baseline_stops_remaining_novice_attacker_data)))
    # eval_2_snort_severe_baseline_stops_remaining_novice_attacker_means = np.mean(tuple(eval_2_snort_severe_baseline_stops_remaining_novice_attacker_data), axis=0)
    # eval_2_snort_severe_baseline_stops_remaining_novice_attacker_stds = np.std(tuple(eval_2_snort_severe_baseline_stops_remaining_novice_attacker_data), axis=0, ddof=1)

    eval_2_step_baseline_first_stop_step_novice_attacker_data = list(map(
        lambda df: util.running_average_list(df["eval_2_avg_step_baseline_first_stop_step"].values[0:max_len], running_avg),
        ppo_dfs_novice_attacker))
    eval_2_step_baseline_first_stop_step_novice_attacker_data = np.array(
        eval_2_step_baseline_first_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    eval_2_step_baseline_first_stop_step_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_2_step_baseline_first_stop_step_novice_attacker_data)))
    eval_2_step_baseline_first_stop_step_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_2_step_baseline_first_stop_step_novice_attacker_data)))
    # eval_2_step_baseline_first_stop_step_novice_attacker_means = np.mean(tuple(eval_2_step_baseline_first_stop_step_novice_attacker_data), axis=0)
    # eval_2_step_baseline_first_stop_step_novice_attacker_stds = np.std(tuple(eval_2_step_baseline_first_stop_step_novice_attacker_data), axis=0, ddof=1)

    eval_2_step_baseline_second_stop_step_novice_attacker_data = list(map(
        lambda df: util.running_average_list(df["eval_2_avg_step_baseline_second_stop_step"].values[0:max_len], running_avg),
        ppo_dfs_novice_attacker))
    eval_2_step_baseline_second_stop_step_novice_attacker_data = np.array(
        eval_2_step_baseline_second_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    eval_2_step_baseline_second_stop_step_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_2_step_baseline_second_stop_step_novice_attacker_data)))
    eval_2_step_baseline_second_stop_step_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_2_step_baseline_second_stop_step_novice_attacker_data)))
    # eval_2_step_baseline_second_stop_step_novice_attacker_means = np.mean(tuple(eval_2_step_baseline_second_stop_step_novice_attacker_data), axis=0)
    # eval_2_step_baseline_second_stop_step_novice_attacker_stds = np.std(tuple(eval_2_step_baseline_second_stop_step_novice_attacker_data), axis=0, ddof=1)

    eval_2_step_baseline_third_stop_step_novice_attacker_data = list(map(
        lambda df: util.running_average_list(df["eval_2_avg_step_baseline_third_stop_step"].values[0:max_len], running_avg),
        ppo_dfs_novice_attacker))
    eval_2_step_baseline_third_stop_step_novice_attacker_data = np.array(
        eval_2_step_baseline_third_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    eval_2_step_baseline_third_stop_step_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_2_step_baseline_third_stop_step_novice_attacker_data)))
    eval_2_step_baseline_third_stop_step_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_2_step_baseline_third_stop_step_novice_attacker_data)))
    # eval_2_step_baseline_third_stop_step_novice_attacker_means = np.mean(tuple(eval_2_step_baseline_third_stop_step_novice_attacker_data), axis=0)
    # eval_2_step_baseline_third_stop_step_novice_attacker_stds = np.std(tuple(eval_2_step_baseline_third_stop_step_novice_attacker_data), axis=0, ddof=1)

    eval_2_step_baseline_fourth_stop_step_novice_attacker_data = list(map(
        lambda df: util.running_average_list(df["eval_2_avg_step_baseline_fourth_stop_step"].values[0:max_len], running_avg),
        ppo_dfs_novice_attacker))
    eval_2_step_baseline_fourth_stop_step_novice_attacker_data = np.array(
        eval_2_step_baseline_fourth_stop_step_novice_attacker_data).reshape(max_len, num_seeds)
    eval_2_step_baseline_fourth_stop_step_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_2_step_baseline_fourth_stop_step_novice_attacker_data)))
    eval_2_step_baseline_fourth_stop_step_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_2_step_baseline_fourth_stop_step_novice_attacker_data)))
    # eval_2_step_baseline_fourth_stop_step_novice_attacker_means = np.mean(tuple(eval_2_step_baseline_fourth_stop_step_novice_attacker_data), axis=0)
    # eval_2_step_baseline_fourth_stop_step_novice_attacker_stds = np.std(tuple(eval_2_step_baseline_fourth_stop_step_novice_attacker_data), axis=0, ddof=1)

    eval_2_step_baseline_stops_remaining_novice_attacker_data = list(map(
        lambda df: util.running_average_list(df["eval_2_avg_step_baseline_stops_remaining"].values[0:max_len], running_avg),
        ppo_dfs_novice_attacker))
    eval_2_step_baseline_stops_remaining_novice_attacker_data = np.array(
        eval_2_step_baseline_stops_remaining_novice_attacker_data).reshape(max_len, num_seeds)
    eval_2_step_baseline_stops_remaining_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_2_step_baseline_stops_remaining_novice_attacker_data)))
    eval_2_step_baseline_stops_remaining_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_2_step_baseline_stops_remaining_novice_attacker_data)))
    # eval_2_step_baseline_stops_remaining_novice_attacker_means = np.mean(tuple(eval_2_step_baseline_stops_remaining_novice_attacker_data), axis=0)
    # eval_2_step_baseline_stops_remaining_novice_attacker_stds = np.std(tuple(eval_2_step_baseline_stops_remaining_novice_attacker_data), axis=0, ddof=1)

    eval_2_optimal_episode_steps_novice_attacker_data = list(
        map(lambda df: util.running_average_list(df["eval_2_avg_optimal_episode_steps"].values[0:max_len], running_avg),
            ppo_dfs_novice_attacker))
    eval_2_optimal_episode_steps_novice_attacker_data = np.array(
        eval_2_optimal_episode_steps_novice_attacker_data).reshape(max_len, num_seeds)
    eval_2_optimal_episode_steps_novice_attacker_stds = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
            eval_2_optimal_episode_steps_novice_attacker_data)))
    eval_2_optimal_episode_steps_novice_attacker_means = np.array(list(
        map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
            eval_2_optimal_episode_steps_novice_attacker_data)))
    # eval_2_optimal_episode_steps_novice_attacker_means = np.mean(tuple(eval_2_optimal_episode_steps_novice_attacker_data), axis=0)
    # eval_2_optimal_episode_steps_novice_attacker_stds = np.std(tuple(eval_2_optimal_episode_steps_novice_attacker_data), axis=0, ddof=1)


    return avg_train_rewards_data_novice_attacker, avg_train_rewards_means_novice_attacker, \
           avg_train_rewards_stds_novice_attacker, \
           avg_train_steps_data_novice_attacker, avg_train_steps_means_novice_attacker, \
           avg_train_steps_stds_novice_attacker, \
           avg_train_caught_frac_data_novice_attacker, avg_train_caught_frac_means_novice_attacker, \
           avg_train_caught_frac_stds_novice_attacker, \
           avg_train_early_stopping_data_novice_attacker, avg_train_early_stopping_means_novice_attacker, \
           avg_train_early_stopping_stds_novice_attacker, avg_train_intrusion_frac_data_novice_attacker, \
           avg_train_intrusion_frac_means_novice_attacker, \
           avg_train_intrusion_frac_stds_novice_attacker, \
           avg_train_i_steps_data_novice_attacker, avg_train_i_steps_means_novice_attacker, \
           avg_train_i_steps_stds_novice_attacker, \
           avg_train_uncaught_intrusion_steps_data_novice_attacker, \
           avg_train_uncaught_intrusion_steps_means_novice_attacker, \
           avg_train_uncaught_intrusion_steps_stds_novice_attacker, \
           avg_train_optimal_defender_rewards_novice_attacker_data, \
           avg_train_optimal_defender_rewards_novice_attacker_means, \
           avg_train_optimal_defender_rewards_novice_attacker_stds, \
           train_snort_severe_baseline_rewards_data_novice_attacker, train_snort_severe_baseline_rewards_means_novice_attacker, \
           train_snort_severe_baseline_rewards_stds_novice_attacker, train_step_baseline_rewards_data_novice_attacker, \
           train_step_baseline_rewards_means_novice_attacker, train_step_baseline_rewards_stds_novice_attacker, \
           train_snort_severe_baseline_steps_data_novice_attacker, \
           train_snort_severe_baseline_steps_means_novice_attacker, \
           train_snort_severe_baseline_steps_stds_novice_attacker, \
           train_step_baseline_steps_data_novice_attacker, train_step_baseline_steps_means_novice_attacker, \
           train_step_baseline_steps_stds_novice_attacker, \
           train_snort_severe_baseline_early_stopping_data_novice_attacker, \
           train_snort_severe_baseline_early_stopping_means_novice_attacker, \
           train_snort_severe_baseline_early_stopping_stds_novice_attacker, \
           train_step_baseline_early_stopping_data_novice_attacker, \
           train_step_baseline_early_stopping_means_novice_attacker, \
           train_step_baseline_early_stopping_stds_novice_attacker, \
           train_snort_severe_baseline_caught_attacker_data_novice_attacker, \
           train_snort_severe_baseline_caught_attacker_means_novice_attacker, \
           train_snort_severe_baseline_caught_attacker_stds_novice_attacker, \
           train_step_baseline_caught_attacker_data_novice_attacker, \
           train_step_baseline_caught_attacker_means_novice_attacker, \
           train_step_baseline_caught_attacker_stds_novice_attacker, \
           train_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker, \
           train_snort_severe_baseline_uncaught_intrusion_steps_means_novice_attacker, \
           train_snort_severe_baseline_uncaught_intrusion_steps_stds_novice_attacker, \
           train_step_baseline_uncaught_intrusion_steps_data_novice_attacker, \
           train_step_baseline_uncaught_intrusion_steps_means_novice_attacker, \
           train_step_baseline_uncaught_intrusion_steps_stds_novice_attacker, \
           train_defender_first_stop_step_novice_attacker_data, \
           train_defender_first_stop_step_novice_attacker_means, train_defender_first_stop_step_novice_attacker_stds, \
           train_defender_second_stop_step_novice_attacker_data, \
           train_defender_second_stop_step_novice_attacker_means, train_defender_second_stop_step_novice_attacker_stds, \
           train_defender_third_stop_step_novice_attacker_data, train_defender_third_stop_step_novice_attacker_means, \
           train_defender_third_stop_step_novice_attacker_stds, train_defender_fourth_stop_step_novice_attacker_data, \
           train_defender_fourth_stop_step_novice_attacker_means, train_defender_fourth_stop_step_novice_attacker_stds, \
           train_defender_stops_remaining_novice_attacker_data, train_defender_stops_remaining_novice_attacker_means, \
           train_defender_stops_remaining_novice_attacker_stds, train_optimal_first_stop_step_novice_attacker_data, \
           train_optimal_first_stop_step_novice_attacker_means, train_optimal_first_stop_step_novice_attacker_stds, \
           train_optimal_second_stop_step_novice_attacker_data, train_optimal_second_stop_step_novice_attacker_means, \
           train_optimal_second_stop_step_novice_attacker_stds, train_optimal_third_stop_step_novice_attacker_data, \
           train_optimal_third_stop_step_novice_attacker_means, train_optimal_third_stop_step_novice_attacker_stds, \
           train_optimal_fourth_stop_step_novice_attacker_data, train_optimal_fourth_stop_step_novice_attacker_means, \
           train_optimal_fourth_stop_step_novice_attacker_stds, train_optimal_stops_remaining_novice_attacker_data, \
           train_optimal_stops_remaining_novice_attacker_means, train_optimal_stops_remaining_novice_attacker_stds, \
           train_snort_severe_baseline_first_stop_step_novice_attacker_data, \
           train_snort_severe_baseline_first_stop_step_novice_attacker_means, \
           train_snort_severe_baseline_first_stop_step_novice_attacker_stds, \
           train_snort_severe_baseline_second_stop_step_novice_attacker_data, \
           train_snort_severe_baseline_second_stop_step_novice_attacker_means, \
           train_snort_severe_baseline_second_stop_step_novice_attacker_stds, \
           train_snort_severe_baseline_third_stop_step_novice_attacker_data, \
           train_snort_severe_baseline_third_stop_step_novice_attacker_means, \
           train_snort_severe_baseline_third_stop_step_novice_attacker_stds, \
           train_snort_severe_baseline_fourth_stop_step_novice_attacker_data, \
           train_snort_severe_baseline_fourth_stop_step_novice_attacker_means, \
           train_snort_severe_baseline_fourth_stop_step_novice_attacker_stds, \
           train_snort_severe_baseline_stops_remaining_novice_attacker_data, \
           train_snort_severe_baseline_stops_remaining_novice_attacker_means, \
           train_snort_severe_baseline_stops_remaining_novice_attacker_stds, \
           train_step_baseline_first_stop_step_novice_attacker_data, \
           train_step_baseline_first_stop_step_novice_attacker_means, \
           train_step_baseline_first_stop_step_novice_attacker_stds, \
           train_step_baseline_second_stop_step_novice_attacker_data, \
           train_step_baseline_second_stop_step_novice_attacker_means, \
           train_step_baseline_second_stop_step_novice_attacker_stds, \
           train_step_baseline_third_stop_step_novice_attacker_data, \
           train_step_baseline_third_stop_step_novice_attacker_means, \
           train_step_baseline_third_stop_step_novice_attacker_stds, \
           train_step_baseline_fourth_stop_step_novice_attacker_data, \
           train_step_baseline_fourth_stop_step_novice_attacker_means, \
           train_step_baseline_fourth_stop_step_novice_attacker_stds, \
           train_step_baseline_stops_remaining_novice_attacker_data, \
           train_step_baseline_stops_remaining_novice_attacker_means, \
           train_step_baseline_stops_remaining_novice_attacker_stds, \
           train_optimal_episode_steps_novice_attacker_data, train_optimal_episode_steps_novice_attacker_means, \
           train_optimal_episode_steps_novice_attacker_stds, \
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
           avg_eval_i_steps_stds_novice_attacker,\
           avg_eval_uncaught_intrusion_steps_data_novice_attacker, \
           avg_eval_uncaught_intrusion_steps_means_novice_attacker, \
           avg_eval_uncaught_intrusion_steps_stds_novice_attacker, \
           avg_eval_optimal_defender_rewards_novice_attacker_data, \
           avg_eval_optimal_defender_rewards_novice_attacker_means, \
           avg_eval_optimal_defender_rewards_novice_attacker_stds, \
           eval_snort_severe_baseline_rewards_data_novice_attacker, \
           eval_snort_severe_baseline_rewards_means_novice_attacker, \
           eval_snort_severe_baseline_rewards_stds_novice_attacker, \
           eval_step_baseline_rewards_data_novice_attacker, eval_step_baseline_rewards_means_novice_attacker, \
           eval_step_baseline_rewards_stds_novice_attacker, \
           eval_snort_severe_baseline_steps_data_novice_attacker, \
           eval_snort_severe_baseline_steps_means_novice_attacker, \
           eval_snort_severe_baseline_steps_stds_novice_attacker, \
           eval_step_baseline_steps_data_novice_attacker, eval_step_baseline_steps_means_novice_attacker, \
           eval_step_baseline_steps_stds_novice_attacker, \
           eval_snort_severe_baseline_early_stopping_data_novice_attacker, \
           eval_snort_severe_baseline_early_stopping_means_novice_attacker, \
           eval_snort_severe_baseline_early_stopping_stds_novice_attacker, \
           eval_step_baseline_early_stopping_data_novice_attacker, \
           eval_step_baseline_early_stopping_means_novice_attacker, \
           eval_step_baseline_early_stopping_stds_novice_attacker, \
           eval_snort_severe_baseline_caught_attacker_data_novice_attacker, \
           eval_snort_severe_baseline_caught_attacker_means_novice_attacker, \
           eval_snort_severe_baseline_caught_attacker_stds_novice_attacker, \
           eval_step_baseline_caught_attacker_data_novice_attacker, \
           eval_step_baseline_caught_attacker_means_novice_attacker, \
           eval_step_baseline_caught_attacker_stds_novice_attacker, \
           eval_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker, \
           eval_snort_severe_baseline_uncaught_intrusion_steps_means_novice_attacker, \
           eval_snort_severe_baseline_uncaught_intrusion_steps_stds_novice_attacker, \
           eval_step_baseline_uncaught_intrusion_steps_data_novice_attacker, \
           eval_step_baseline_uncaught_intrusion_steps_means_novice_attacker, \
           eval_step_baseline_uncaught_intrusion_steps_stds_novice_attacker, \
           eval_defender_first_stop_step_novice_attacker_data, \
           eval_defender_first_stop_step_novice_attacker_means, eval_defender_first_stop_step_novice_attacker_stds, \
           eval_defender_second_stop_step_novice_attacker_data, \
           eval_defender_second_stop_step_novice_attacker_means, eval_defender_second_stop_step_novice_attacker_stds, \
           eval_defender_third_stop_step_novice_attacker_data, eval_defender_third_stop_step_novice_attacker_means, \
           eval_defender_third_stop_step_novice_attacker_stds, eval_defender_fourth_stop_step_novice_attacker_data, \
           eval_defender_fourth_stop_step_novice_attacker_means, eval_defender_fourth_stop_step_novice_attacker_stds, \
           eval_defender_stops_remaining_novice_attacker_data, eval_defender_stops_remaining_novice_attacker_means, \
           eval_defender_stops_remaining_novice_attacker_stds, eval_optimal_first_stop_step_novice_attacker_data, \
           eval_optimal_first_stop_step_novice_attacker_means, eval_optimal_first_stop_step_novice_attacker_stds, \
           eval_optimal_second_stop_step_novice_attacker_data, eval_optimal_second_stop_step_novice_attacker_means, \
           eval_optimal_second_stop_step_novice_attacker_stds, eval_optimal_third_stop_step_novice_attacker_data, \
           eval_optimal_third_stop_step_novice_attacker_means, eval_optimal_third_stop_step_novice_attacker_stds, \
           eval_optimal_fourth_stop_step_novice_attacker_data, eval_optimal_fourth_stop_step_novice_attacker_means, \
           eval_optimal_fourth_stop_step_novice_attacker_stds, eval_optimal_stops_remaining_novice_attacker_data, \
           eval_optimal_stops_remaining_novice_attacker_means, eval_optimal_stops_remaining_novice_attacker_stds, \
           eval_snort_severe_baseline_first_stop_step_novice_attacker_data, \
           eval_snort_severe_baseline_first_stop_step_novice_attacker_means, \
           eval_snort_severe_baseline_first_stop_step_novice_attacker_stds, \
           eval_snort_severe_baseline_second_stop_step_novice_attacker_data, \
           eval_snort_severe_baseline_second_stop_step_novice_attacker_means, \
           eval_snort_severe_baseline_second_stop_step_novice_attacker_stds, \
           eval_snort_severe_baseline_third_stop_step_novice_attacker_data, \
           eval_snort_severe_baseline_third_stop_step_novice_attacker_means, \
           eval_snort_severe_baseline_third_stop_step_novice_attacker_stds, \
           eval_snort_severe_baseline_fourth_stop_step_novice_attacker_data, \
           eval_snort_severe_baseline_fourth_stop_step_novice_attacker_means, \
           eval_snort_severe_baseline_fourth_stop_step_novice_attacker_stds, \
           eval_snort_severe_baseline_stops_remaining_novice_attacker_data, \
           eval_snort_severe_baseline_stops_remaining_novice_attacker_means, \
           eval_snort_severe_baseline_stops_remaining_novice_attacker_stds, \
           eval_step_baseline_first_stop_step_novice_attacker_data, \
           eval_step_baseline_first_stop_step_novice_attacker_means, \
           eval_step_baseline_first_stop_step_novice_attacker_stds, \
           eval_step_baseline_second_stop_step_novice_attacker_data, \
           eval_step_baseline_second_stop_step_novice_attacker_means, \
           eval_step_baseline_second_stop_step_novice_attacker_stds, \
           eval_step_baseline_third_stop_step_novice_attacker_data, \
           eval_step_baseline_third_stop_step_novice_attacker_means, \
           eval_step_baseline_third_stop_step_novice_attacker_stds, \
           eval_step_baseline_fourth_stop_step_novice_attacker_data, \
           eval_step_baseline_fourth_stop_step_novice_attacker_means, \
           eval_step_baseline_fourth_stop_step_novice_attacker_stds, \
           eval_step_baseline_stops_remaining_novice_attacker_data, \
           eval_step_baseline_stops_remaining_novice_attacker_means, \
           eval_step_baseline_stops_remaining_novice_attacker_stds, \
           eval_optimal_episode_steps_novice_attacker_data, eval_optimal_episode_steps_novice_attacker_means, \
           eval_optimal_episode_steps_novice_attacker_stds, \
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
           avg_eval_2_i_steps_stds_novice_attacker,\
           avg_eval_2_uncaught_intrusion_steps_data_novice_attacker, \
           avg_eval_2_uncaught_intrusion_steps_means_novice_attacker, \
           avg_eval_2_uncaught_intrusion_steps_stds_novice_attacker, \
           avg_eval_2_optimal_defender_rewards_novice_attacker_data, \
           avg_eval_2_optimal_defender_rewards_novice_attacker_means, \
           avg_eval_2_optimal_defender_rewards_novice_attacker_stds, \
           eval_2_snort_severe_baseline_rewards_data_novice_attacker, \
           eval_2_snort_severe_baseline_rewards_means_novice_attacker, \
           eval_2_snort_severe_baseline_rewards_stds_novice_attacker, \
           eval_2_step_baseline_rewards_data_novice_attacker, \
           eval_2_step_baseline_rewards_means_novice_attacker, eval_2_step_baseline_rewards_stds_novice_attacker, \
           eval_2_snort_severe_baseline_steps_data_novice_attacker, \
           eval_2_snort_severe_baseline_steps_means_novice_attacker, \
           eval_2_snort_severe_baseline_steps_stds_novice_attacker, \
           eval_2_step_baseline_steps_data_novice_attacker, eval_2_step_baseline_steps_means_novice_attacker, \
           eval_2_step_baseline_steps_stds_novice_attacker, \
           eval_2_snort_severe_baseline_early_stopping_data_novice_attacker, \
           eval_2_snort_severe_baseline_early_stopping_means_novice_attacker, \
           eval_2_snort_severe_baseline_early_stopping_stds_novice_attacker, \
           eval_2_step_baseline_early_stopping_data_novice_attacker, \
           eval_2_step_baseline_early_stopping_means_novice_attacker, \
           eval_2_step_baseline_early_stopping_stds_novice_attacker, \
           eval_2_snort_severe_baseline_caught_attacker_data_novice_attacker, \
           eval_2_snort_severe_baseline_caught_attacker_means_novice_attacker, \
           eval_2_snort_severe_baseline_caught_attacker_stds_novice_attacker, \
           eval_2_step_baseline_caught_attacker_data_novice_attacker, \
           eval_2_step_baseline_caught_attacker_means_novice_attacker, \
           eval_2_step_baseline_caught_attacker_stds_novice_attacker, \
           eval_2_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker, \
           eval_2_snort_severe_baseline_uncaught_intrusion_steps_means_novice_attacker, \
           eval_2_snort_severe_baseline_uncaught_intrusion_steps_stds_novice_attacker, \
           eval_2_step_baseline_uncaught_intrusion_steps_data_novice_attacker, \
           eval_2_step_baseline_uncaught_intrusion_steps_means_novice_attacker, \
           eval_2_step_baseline_uncaught_intrusion_steps_stds_novice_attacker,\
           eval_2_defender_first_stop_step_novice_attacker_data, \
           eval_2_defender_first_stop_step_novice_attacker_means, eval_2_defender_first_stop_step_novice_attacker_stds, \
           eval_2_defender_second_stop_step_novice_attacker_data, \
           eval_2_defender_second_stop_step_novice_attacker_means, eval_2_defender_second_stop_step_novice_attacker_stds, \
           eval_2_defender_third_stop_step_novice_attacker_data, eval_2_defender_third_stop_step_novice_attacker_means, \
           eval_2_defender_third_stop_step_novice_attacker_stds, eval_2_defender_fourth_stop_step_novice_attacker_data, \
           eval_2_defender_fourth_stop_step_novice_attacker_means, eval_2_defender_fourth_stop_step_novice_attacker_stds, \
           eval_2_defender_stops_remaining_novice_attacker_data, eval_2_defender_stops_remaining_novice_attacker_means, \
           eval_2_defender_stops_remaining_novice_attacker_stds, eval_2_optimal_first_stop_step_novice_attacker_data, \
           eval_2_optimal_first_stop_step_novice_attacker_means, eval_2_optimal_first_stop_step_novice_attacker_stds, \
           eval_2_optimal_second_stop_step_novice_attacker_data, eval_2_optimal_second_stop_step_novice_attacker_means, \
           eval_2_optimal_second_stop_step_novice_attacker_stds, eval_2_optimal_third_stop_step_novice_attacker_data, \
           eval_2_optimal_third_stop_step_novice_attacker_means, eval_2_optimal_third_stop_step_novice_attacker_stds, \
           eval_2_optimal_fourth_stop_step_novice_attacker_data, eval_2_optimal_fourth_stop_step_novice_attacker_means, \
           eval_2_optimal_fourth_stop_step_novice_attacker_stds, eval_2_optimal_stops_remaining_novice_attacker_data, \
           eval_2_optimal_stops_remaining_novice_attacker_means, eval_2_optimal_stops_remaining_novice_attacker_stds, \
           eval_2_snort_severe_baseline_first_stop_step_novice_attacker_data, \
           eval_2_snort_severe_baseline_first_stop_step_novice_attacker_means, \
           eval_2_snort_severe_baseline_first_stop_step_novice_attacker_stds, \
           eval_2_snort_severe_baseline_second_stop_step_novice_attacker_data, \
           eval_2_snort_severe_baseline_second_stop_step_novice_attacker_means, \
           eval_2_snort_severe_baseline_second_stop_step_novice_attacker_stds, \
           eval_2_snort_severe_baseline_third_stop_step_novice_attacker_data, \
           eval_2_snort_severe_baseline_third_stop_step_novice_attacker_means, \
           eval_2_snort_severe_baseline_third_stop_step_novice_attacker_stds, \
           eval_2_snort_severe_baseline_fourth_stop_step_novice_attacker_data, \
           eval_2_snort_severe_baseline_fourth_stop_step_novice_attacker_means, \
           eval_2_snort_severe_baseline_fourth_stop_step_novice_attacker_stds, \
           eval_2_snort_severe_baseline_stops_remaining_novice_attacker_data, \
           eval_2_snort_severe_baseline_stops_remaining_novice_attacker_means, \
           eval_2_snort_severe_baseline_stops_remaining_novice_attacker_stds, \
           eval_2_step_baseline_first_stop_step_novice_attacker_data, \
           eval_2_step_baseline_first_stop_step_novice_attacker_means, \
           eval_2_step_baseline_first_stop_step_novice_attacker_stds, \
           eval_2_step_baseline_second_stop_step_novice_attacker_data, \
           eval_2_step_baseline_second_stop_step_novice_attacker_means, \
           eval_2_step_baseline_second_stop_step_novice_attacker_stds, \
           eval_2_step_baseline_third_stop_step_novice_attacker_data, \
           eval_2_step_baseline_third_stop_step_novice_attacker_means, \
           eval_2_step_baseline_third_stop_step_novice_attacker_stds, \
           eval_2_step_baseline_fourth_stop_step_novice_attacker_data, \
           eval_2_step_baseline_fourth_stop_step_novice_attacker_means, \
           eval_2_step_baseline_fourth_stop_step_novice_attacker_stds, \
           eval_2_step_baseline_stops_remaining_novice_attacker_data, \
           eval_2_step_baseline_stops_remaining_novice_attacker_means, \
           eval_2_step_baseline_stops_remaining_novice_attacker_stds, \
           eval_2_optimal_episode_steps_novice_attacker_data, eval_2_optimal_episode_steps_novice_attacker_means, \
           eval_2_optimal_episode_steps_novice_attacker_stds


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
        avg_train_uncaught_intrusion_steps_data_novice_attacker,
        avg_train_uncaught_intrusion_steps_means_novice_attacker,
        avg_train_uncaught_intrusion_steps_stds_novice_attacker,
        avg_train_optimal_defender_rewards_novice_attacker_data,
        avg_train_optimal_defender_rewards_novice_attacker_means,
        avg_train_optimal_defender_rewards_novice_attacker_stds,
        train_snort_severe_baseline_rewards_data_novice_attacker,
        train_snort_severe_baseline_rewards_means_novice_attacker,
        train_snort_severe_baseline_rewards_stds_novice_attacker, train_step_baseline_rewards_data_novice_attacker,
        train_step_baseline_rewards_means_novice_attacker, train_step_baseline_rewards_stds_novice_attacker,
        train_snort_severe_baseline_steps_data_novice_attacker,
        train_snort_severe_baseline_steps_means_novice_attacker,
        train_snort_severe_baseline_steps_stds_novice_attacker,
        train_step_baseline_steps_data_novice_attacker, train_step_baseline_steps_means_novice_attacker,
        train_step_baseline_steps_stds_novice_attacker,
        train_snort_severe_baseline_early_stopping_data_novice_attacker,
        train_snort_severe_baseline_early_stopping_means_novice_attacker,
        train_snort_severe_baseline_early_stopping_stds_novice_attacker,
        train_step_baseline_early_stopping_data_novice_attacker,
        train_step_baseline_early_stopping_means_novice_attacker,
        train_step_baseline_early_stopping_stds_novice_attacker,
        train_snort_severe_baseline_caught_attacker_data_novice_attacker,
        train_snort_severe_baseline_caught_attacker_means_novice_attacker,
        train_snort_severe_baseline_caught_attacker_stds_novice_attacker,
        train_step_baseline_caught_attacker_data_novice_attacker,
        train_step_baseline_caught_attacker_means_novice_attacker,
        train_step_baseline_caught_attacker_stds_novice_attacker,
        train_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker,
        train_snort_severe_baseline_uncaught_intrusion_steps_means_novice_attacker,
        train_snort_severe_baseline_uncaught_intrusion_steps_stds_novice_attacker,
        train_step_baseline_uncaught_intrusion_steps_data_novice_attacker,
        train_step_baseline_uncaught_intrusion_steps_means_novice_attacker,
        train_step_baseline_uncaught_intrusion_steps_stds_novice_attacker,
        train_defender_first_stop_step_novice_attacker_data,
        train_defender_first_stop_step_novice_attacker_means, train_defender_first_stop_step_novice_attacker_stds,
        train_defender_second_stop_step_novice_attacker_data,
        train_defender_second_stop_step_novice_attacker_means, train_defender_second_stop_step_novice_attacker_stds,
        train_defender_third_stop_step_novice_attacker_data, train_defender_third_stop_step_novice_attacker_means,
        train_defender_third_stop_step_novice_attacker_stds, train_defender_fourth_stop_step_novice_attacker_data,
        train_defender_fourth_stop_step_novice_attacker_means, train_defender_fourth_stop_step_novice_attacker_stds,
        train_defender_stops_remaining_novice_attacker_data, train_defender_stops_remaining_novice_attacker_means,
        train_defender_stops_remaining_novice_attacker_stds, train_optimal_first_stop_step_novice_attacker_data,
        train_optimal_first_stop_step_novice_attacker_means, train_optimal_first_stop_step_novice_attacker_stds,
        train_optimal_second_stop_step_novice_attacker_data, train_optimal_second_stop_step_novice_attacker_means,
        train_optimal_second_stop_step_novice_attacker_stds, train_optimal_third_stop_step_novice_attacker_data,
        train_optimal_third_stop_step_novice_attacker_means, train_optimal_third_stop_step_novice_attacker_stds,
        train_optimal_fourth_stop_step_novice_attacker_data, train_optimal_fourth_stop_step_novice_attacker_means,
        train_optimal_fourth_stop_step_novice_attacker_stds, train_optimal_stops_remaining_novice_attacker_data,
        train_optimal_stops_remaining_novice_attacker_means, train_optimal_stops_remaining_novice_attacker_stds,
        train_snort_severe_baseline_first_stop_step_novice_attacker_data,
        train_snort_severe_baseline_first_stop_step_novice_attacker_means,
        train_snort_severe_baseline_first_stop_step_novice_attacker_stds,
        train_snort_severe_baseline_second_stop_step_novice_attacker_data,
        train_snort_severe_baseline_second_stop_step_novice_attacker_means,
        train_snort_severe_baseline_second_stop_step_novice_attacker_stds,
        train_snort_severe_baseline_third_stop_step_novice_attacker_data,
        train_snort_severe_baseline_third_stop_step_novice_attacker_means,
        train_snort_severe_baseline_third_stop_step_novice_attacker_stds,
        train_snort_severe_baseline_fourth_stop_step_novice_attacker_data,
        train_snort_severe_baseline_fourth_stop_step_novice_attacker_means,
        train_snort_severe_baseline_fourth_stop_step_novice_attacker_stds,
        train_snort_severe_baseline_stops_remaining_novice_attacker_data,
        train_snort_severe_baseline_stops_remaining_novice_attacker_means,
        train_snort_severe_baseline_stops_remaining_novice_attacker_stds,
        train_step_baseline_first_stop_step_novice_attacker_data,
        train_step_baseline_first_stop_step_novice_attacker_means,
        train_step_baseline_first_stop_step_novice_attacker_stds,
        train_step_baseline_second_stop_step_novice_attacker_data,
        train_step_baseline_second_stop_step_novice_attacker_means,
        train_step_baseline_second_stop_step_novice_attacker_stds,
        train_step_baseline_third_stop_step_novice_attacker_data,
        train_step_baseline_third_stop_step_novice_attacker_means,
        train_step_baseline_third_stop_step_novice_attacker_stds,
        train_step_baseline_fourth_stop_step_novice_attacker_data,
        train_step_baseline_fourth_stop_step_novice_attacker_means,
        train_step_baseline_fourth_stop_step_novice_attacker_stds,
        train_step_baseline_stops_remaining_novice_attacker_data,
        train_step_baseline_stops_remaining_novice_attacker_means,
        train_step_baseline_stops_remaining_novice_attacker_stds,
        train_optimal_episode_steps_novice_attacker_data, train_optimal_episode_steps_novice_attacker_means,
        train_optimal_episode_steps_novice_attacker_stds,
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
        avg_eval_i_steps_stds_novice_attacker,
        avg_eval_uncaught_intrusion_steps_data_novice_attacker,
        avg_eval_uncaught_intrusion_steps_means_novice_attacker,
        avg_eval_uncaught_intrusion_steps_stds_novice_attacker,
        avg_eval_optimal_defender_rewards_novice_attacker_data,
        avg_eval_optimal_defender_rewards_novice_attacker_means,
        avg_eval_optimal_defender_rewards_novice_attacker_stds,
        eval_snort_severe_baseline_rewards_data_novice_attacker,
        eval_snort_severe_baseline_rewards_means_novice_attacker,
        eval_snort_severe_baseline_rewards_stds_novice_attacker,
        eval_step_baseline_rewards_data_novice_attacker, eval_step_baseline_rewards_means_novice_attacker,
        eval_step_baseline_rewards_stds_novice_attacker,
        eval_snort_severe_baseline_steps_data_novice_attacker,
        eval_snort_severe_baseline_steps_means_novice_attacker,
        eval_snort_severe_baseline_steps_stds_novice_attacker,
        eval_step_baseline_steps_data_novice_attacker, eval_step_baseline_steps_means_novice_attacker,
        eval_step_baseline_steps_stds_novice_attacker,
        eval_snort_severe_baseline_early_stopping_data_novice_attacker,
        eval_snort_severe_baseline_early_stopping_means_novice_attacker,
        eval_snort_severe_baseline_early_stopping_stds_novice_attacker,
        eval_step_baseline_early_stopping_data_novice_attacker,
        eval_step_baseline_early_stopping_means_novice_attacker,
        eval_step_baseline_early_stopping_stds_novice_attacker,
        eval_snort_severe_baseline_caught_attacker_data_novice_attacker,
        eval_snort_severe_baseline_caught_attacker_means_novice_attacker,
        eval_snort_severe_baseline_caught_attacker_stds_novice_attacker,
        eval_step_baseline_caught_attacker_data_novice_attacker,
        eval_step_baseline_caught_attacker_means_novice_attacker,
        eval_step_baseline_caught_attacker_stds_novice_attacker,
        eval_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker,
        eval_snort_severe_baseline_uncaught_intrusion_steps_means_novice_attacker,
        eval_snort_severe_baseline_uncaught_intrusion_steps_stds_novice_attacker,
        eval_step_baseline_uncaught_intrusion_steps_data_novice_attacker,
        eval_step_baseline_uncaught_intrusion_steps_means_novice_attacker,
        eval_step_baseline_uncaught_intrusion_steps_stds_novice_attacker,
        eval_defender_first_stop_step_novice_attacker_data,
        eval_defender_first_stop_step_novice_attacker_means, eval_defender_first_stop_step_novice_attacker_stds,
        eval_defender_second_stop_step_novice_attacker_data,
        eval_defender_second_stop_step_novice_attacker_means, eval_defender_second_stop_step_novice_attacker_stds,
        eval_defender_third_stop_step_novice_attacker_data, eval_defender_third_stop_step_novice_attacker_means,
        eval_defender_third_stop_step_novice_attacker_stds, eval_defender_fourth_stop_step_novice_attacker_data,
        eval_defender_fourth_stop_step_novice_attacker_means, eval_defender_fourth_stop_step_novice_attacker_stds,
        eval_defender_stops_remaining_novice_attacker_data, eval_defender_stops_remaining_novice_attacker_means,
        eval_defender_stops_remaining_novice_attacker_stds, eval_optimal_first_stop_step_novice_attacker_data,
        eval_optimal_first_stop_step_novice_attacker_means, eval_optimal_first_stop_step_novice_attacker_stds,
        eval_optimal_second_stop_step_novice_attacker_data, eval_optimal_second_stop_step_novice_attacker_means,
        eval_optimal_second_stop_step_novice_attacker_stds, eval_optimal_third_stop_step_novice_attacker_data,
        eval_optimal_third_stop_step_novice_attacker_means, eval_optimal_third_stop_step_novice_attacker_stds,
        eval_optimal_fourth_stop_step_novice_attacker_data, eval_optimal_fourth_stop_step_novice_attacker_means,
        eval_optimal_fourth_stop_step_novice_attacker_stds, eval_optimal_stops_remaining_novice_attacker_data,
        eval_optimal_stops_remaining_novice_attacker_means, eval_optimal_stops_remaining_novice_attacker_stds,
        eval_snort_severe_baseline_first_stop_step_novice_attacker_data,
        eval_snort_severe_baseline_first_stop_step_novice_attacker_means,
        eval_snort_severe_baseline_first_stop_step_novice_attacker_stds,
        eval_snort_severe_baseline_second_stop_step_novice_attacker_data,
        eval_snort_severe_baseline_second_stop_step_novice_attacker_means,
        eval_snort_severe_baseline_second_stop_step_novice_attacker_stds,
        eval_snort_severe_baseline_third_stop_step_novice_attacker_data,
        eval_snort_severe_baseline_third_stop_step_novice_attacker_means,
        eval_snort_severe_baseline_third_stop_step_novice_attacker_stds,
        eval_snort_severe_baseline_fourth_stop_step_novice_attacker_data,
        eval_snort_severe_baseline_fourth_stop_step_novice_attacker_means,
        eval_snort_severe_baseline_fourth_stop_step_novice_attacker_stds,
        eval_snort_severe_baseline_stops_remaining_novice_attacker_data,
        eval_snort_severe_baseline_stops_remaining_novice_attacker_means,
        eval_snort_severe_baseline_stops_remaining_novice_attacker_stds,
        eval_step_baseline_first_stop_step_novice_attacker_data,
        eval_step_baseline_first_stop_step_novice_attacker_means,
        eval_step_baseline_first_stop_step_novice_attacker_stds,
        eval_step_baseline_second_stop_step_novice_attacker_data,
        eval_step_baseline_second_stop_step_novice_attacker_means,
        eval_step_baseline_second_stop_step_novice_attacker_stds,
        eval_step_baseline_third_stop_step_novice_attacker_data,
        eval_step_baseline_third_stop_step_novice_attacker_means,
        eval_step_baseline_third_stop_step_novice_attacker_stds,
        eval_step_baseline_fourth_stop_step_novice_attacker_data,
        eval_step_baseline_fourth_stop_step_novice_attacker_means,
        eval_step_baseline_fourth_stop_step_novice_attacker_stds,
        eval_step_baseline_stops_remaining_novice_attacker_data,
        eval_step_baseline_stops_remaining_novice_attacker_means,
        eval_step_baseline_stops_remaining_novice_attacker_stds,
        eval_optimal_episode_steps_novice_attacker_data, eval_optimal_episode_steps_novice_attacker_means,
        eval_optimal_episode_steps_novice_attacker_stds,
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
        avg_eval_2_i_steps_stds_novice_attacker,
        avg_eval_2_uncaught_intrusion_steps_data_novice_attacker,
        avg_eval_2_uncaught_intrusion_steps_means_novice_attacker,
        avg_eval_2_uncaught_intrusion_steps_stds_novice_attacker,
        avg_eval_2_optimal_defender_rewards_novice_attacker_data,
        avg_eval_2_optimal_defender_rewards_novice_attacker_means,
        avg_eval_2_optimal_defender_rewards_novice_attacker_stds,
        eval_2_snort_severe_baseline_rewards_data_novice_attacker,
        eval_2_snort_severe_baseline_rewards_means_novice_attacker,
        eval_2_snort_severe_baseline_rewards_stds_novice_attacker,
        eval_2_step_baseline_rewards_data_novice_attacker,
        eval_2_step_baseline_rewards_means_novice_attacker, eval_2_step_baseline_rewards_stds_novice_attacker,
        eval_2_snort_severe_baseline_steps_data_novice_attacker,
        eval_2_snort_severe_baseline_steps_means_novice_attacker,
        eval_2_snort_severe_baseline_steps_stds_novice_attacker,
        eval_2_step_baseline_steps_data_novice_attacker, eval_2_step_baseline_steps_means_novice_attacker,
        eval_2_step_baseline_steps_stds_novice_attacker,
        eval_2_snort_severe_baseline_early_stopping_data_novice_attacker,
        eval_2_snort_severe_baseline_early_stopping_means_novice_attacker,
        eval_2_snort_severe_baseline_early_stopping_stds_novice_attacker,
        eval_2_step_baseline_early_stopping_data_novice_attacker,
        eval_2_step_baseline_early_stopping_means_novice_attacker,
        eval_2_step_baseline_early_stopping_stds_novice_attacker,
        eval_2_snort_severe_baseline_caught_attacker_data_novice_attacker,
        eval_2_snort_severe_baseline_caught_attacker_means_novice_attacker,
        eval_2_snort_severe_baseline_caught_attacker_stds_novice_attacker,
        eval_2_step_baseline_caught_attacker_data_novice_attacker,
        eval_2_step_baseline_caught_attacker_means_novice_attacker,
        eval_2_step_baseline_caught_attacker_stds_novice_attacker,
        eval_2_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker,
        eval_2_snort_severe_baseline_uncaught_intrusion_steps_means_novice_attacker,
        eval_2_snort_severe_baseline_uncaught_intrusion_steps_stds_novice_attacker,
        eval_2_step_baseline_uncaught_intrusion_steps_data_novice_attacker,
        eval_2_step_baseline_uncaught_intrusion_steps_means_novice_attacker,
        eval_2_step_baseline_uncaught_intrusion_steps_stds_novice_attacker,
        eval_2_defender_first_stop_step_novice_attacker_data,
        eval_2_defender_first_stop_step_novice_attacker_means, eval_2_defender_first_stop_step_novice_attacker_stds,
        eval_2_defender_second_stop_step_novice_attacker_data,
        eval_2_defender_second_stop_step_novice_attacker_means, eval_2_defender_second_stop_step_novice_attacker_stds,
        eval_2_defender_third_stop_step_novice_attacker_data, eval_2_defender_third_stop_step_novice_attacker_means,
        eval_2_defender_third_stop_step_novice_attacker_stds, eval_2_defender_fourth_stop_step_novice_attacker_data,
        eval_2_defender_fourth_stop_step_novice_attacker_means, eval_2_defender_fourth_stop_step_novice_attacker_stds,
        eval_2_defender_stops_remaining_novice_attacker_data, eval_2_defender_stops_remaining_novice_attacker_means,
        eval_2_defender_stops_remaining_novice_attacker_stds, eval_2_optimal_first_stop_step_novice_attacker_data,
        eval_2_optimal_first_stop_step_novice_attacker_means, eval_2_optimal_first_stop_step_novice_attacker_stds,
        eval_2_optimal_second_stop_step_novice_attacker_data, eval_2_optimal_second_stop_step_novice_attacker_means,
        eval_2_optimal_second_stop_step_novice_attacker_stds, eval_2_optimal_third_stop_step_novice_attacker_data,
        eval_2_optimal_third_stop_step_novice_attacker_means, eval_2_optimal_third_stop_step_novice_attacker_stds,
        eval_2_optimal_fourth_stop_step_novice_attacker_data, eval_2_optimal_fourth_stop_step_novice_attacker_means,
        eval_2_optimal_fourth_stop_step_novice_attacker_stds, eval_2_optimal_stops_remaining_novice_attacker_data,
        eval_2_optimal_stops_remaining_novice_attacker_means, eval_2_optimal_stops_remaining_novice_attacker_stds,
        eval_2_snort_severe_baseline_first_stop_step_novice_attacker_data,
        eval_2_snort_severe_baseline_first_stop_step_novice_attacker_means,
        eval_2_snort_severe_baseline_first_stop_step_novice_attacker_stds,
        eval_2_snort_severe_baseline_second_stop_step_novice_attacker_data,
        eval_2_snort_severe_baseline_second_stop_step_novice_attacker_means,
        eval_2_snort_severe_baseline_second_stop_step_novice_attacker_stds,
        eval_2_snort_severe_baseline_third_stop_step_novice_attacker_data,
        eval_2_snort_severe_baseline_third_stop_step_novice_attacker_means,
        eval_2_snort_severe_baseline_third_stop_step_novice_attacker_stds,
        eval_2_snort_severe_baseline_fourth_stop_step_novice_attacker_data,
        eval_2_snort_severe_baseline_fourth_stop_step_novice_attacker_means,
        eval_2_snort_severe_baseline_fourth_stop_step_novice_attacker_stds,
        eval_2_snort_severe_baseline_stops_remaining_novice_attacker_data,
        eval_2_snort_severe_baseline_stops_remaining_novice_attacker_means,
        eval_2_snort_severe_baseline_stops_remaining_novice_attacker_stds,
        eval_2_step_baseline_first_stop_step_novice_attacker_data,
        eval_2_step_baseline_first_stop_step_novice_attacker_means,
        eval_2_step_baseline_first_stop_step_novice_attacker_stds,
        eval_2_step_baseline_second_stop_step_novice_attacker_data,
        eval_2_step_baseline_second_stop_step_novice_attacker_means,
        eval_2_step_baseline_second_stop_step_novice_attacker_stds,
        eval_2_step_baseline_third_stop_step_novice_attacker_data,
        eval_2_step_baseline_third_stop_step_novice_attacker_means,
        eval_2_step_baseline_third_stop_step_novice_attacker_stds,
        eval_2_step_baseline_fourth_stop_step_novice_attacker_data,
        eval_2_step_baseline_fourth_stop_step_novice_attacker_means,
        eval_2_step_baseline_fourth_stop_step_novice_attacker_stds,
        eval_2_step_baseline_stops_remaining_novice_attacker_data,
        eval_2_step_baseline_stops_remaining_novice_attacker_means,
        eval_2_step_baseline_stops_remaining_novice_attacker_stds,
        eval_2_optimal_episode_steps_novice_attacker_data, eval_2_optimal_episode_steps_novice_attacker_means,
        eval_2_optimal_episode_steps_novice_attacker_stds,
        avg_train_rewards_data_experienced_attacker, avg_train_rewards_means_experienced_attacker,
        avg_train_rewards_stds_experienced_attacker,
        avg_train_steps_data_experienced_attacker, avg_train_steps_means_experienced_attacker,
        avg_train_steps_stds_experienced_attacker,
        avg_train_caught_frac_data_experienced_attacker, avg_train_caught_frac_means_experienced_attacker,
        avg_train_caught_frac_stds_experienced_attacker,
        avg_train_early_stopping_frac_data_experienced_attacker, avg_train_early_stopping_means_experienced_attacker,
        avg_train_early_stopping_stds_experienced_attacker, avg_train_intrusion_frac_data_experienced_attacker,
        avg_train_intrusion_means_experienced_attacker,
        avg_train_intrusion_stds_experienced_attacker,
        avg_train_i_steps_data_experienced_attacker, avg_train_i_steps_means_experienced_attacker,
        avg_train_i_steps_stds_experienced_attacker,
        avg_train_uncaught_intrusion_steps_data_experienced_attacker,
        avg_train_uncaught_intrusion_steps_means_experienced_attacker,
        avg_train_uncaught_intrusion_steps_stds_experienced_attacker,
        avg_train_optimal_defender_rewards_experienced_attacker_data,
        avg_train_optimal_defender_rewards_experienced_attacker_means,
        avg_train_optimal_defender_rewards_experienced_attacker_stds,
        train_snort_severe_baseline_rewards_data_experienced_attacker,
        train_snort_severe_baseline_rewards_means_experienced_attacker,
        train_snort_severe_baseline_rewards_stds_experienced_attacker, train_step_baseline_rewards_data_experienced_attacker,
        train_step_baseline_rewards_means_experienced_attacker, train_step_baseline_rewards_stds_experienced_attacker,
        train_snort_severe_baseline_steps_data_experienced_attacker,
        train_snort_severe_baseline_steps_means_experienced_attacker,
        train_snort_severe_baseline_steps_stds_experienced_attacker,
        train_step_baseline_steps_data_experienced_attacker, train_step_baseline_steps_means_experienced_attacker,
        train_step_baseline_steps_stds_experienced_attacker,
        train_snort_severe_baseline_early_stopping_data_experienced_attacker,
        train_snort_severe_baseline_early_stopping_means_experienced_attacker,
        train_snort_severe_baseline_early_stopping_stds_experienced_attacker,
        train_step_baseline_early_stopping_data_experienced_attacker,
        train_step_baseline_early_stopping_means_experienced_attacker,
        train_step_baseline_early_stopping_stds_experienced_attacker,
        train_snort_severe_baseline_caught_attacker_data_experienced_attacker,
        train_snort_severe_baseline_caught_attacker_means_experienced_attacker,
        train_snort_severe_baseline_caught_attacker_stds_experienced_attacker,
        train_step_baseline_caught_attacker_data_experienced_attacker,
        train_step_baseline_caught_attacker_means_experienced_attacker,
        train_step_baseline_caught_attacker_stds_experienced_attacker,
        train_snort_severe_baseline_uncaught_intrusion_steps_data_experienced_attacker,
        train_snort_severe_baseline_uncaught_intrusion_steps_means_experienced_attacker,
        train_snort_severe_baseline_uncaught_intrusion_steps_stds_experienced_attacker,
        train_step_baseline_uncaught_intrusion_steps_data_experienced_attacker,
        train_step_baseline_uncaught_intrusion_steps_means_experienced_attacker,
        train_step_baseline_uncaught_intrusion_steps_stds_experienced_attacker,
        train_defender_first_stop_step_experienced_attacker_data,
        train_defender_first_stop_step_experienced_attacker_means, train_defender_first_stop_step_experienced_attacker_stds,
        train_defender_second_stop_step_experienced_attacker_data,
        train_defender_second_stop_step_experienced_attacker_means, train_defender_second_stop_step_experienced_attacker_stds,
        train_defender_third_stop_step_experienced_attacker_data, train_defender_third_stop_step_experienced_attacker_means,
        train_defender_third_stop_step_experienced_attacker_stds, train_defender_fourth_stop_step_experienced_attacker_data,
        train_defender_fourth_stop_step_experienced_attacker_means, train_defender_fourth_stop_step_experienced_attacker_stds,
        train_defender_stops_remaining_experienced_attacker_data, train_defender_stops_remaining_experienced_attacker_means,
        train_defender_stops_remaining_experienced_attacker_stds, train_optimal_first_stop_step_experienced_attacker_data,
        train_optimal_first_stop_step_experienced_attacker_means, train_optimal_first_stop_step_experienced_attacker_stds,
        train_optimal_second_stop_step_experienced_attacker_data, train_optimal_second_stop_step_experienced_attacker_means,
        train_optimal_second_stop_step_experienced_attacker_stds, train_optimal_third_stop_step_experienced_attacker_data,
        train_optimal_third_stop_step_experienced_attacker_means, train_optimal_third_stop_step_experienced_attacker_stds,
        train_optimal_fourth_stop_step_experienced_attacker_data, train_optimal_fourth_stop_step_experienced_attacker_means,
        train_optimal_fourth_stop_step_experienced_attacker_stds, train_optimal_stops_remaining_experienced_attacker_data,
        train_optimal_stops_remaining_experienced_attacker_means, train_optimal_stops_remaining_experienced_attacker_stds,
        train_snort_severe_baseline_first_stop_step_experienced_attacker_data,
        train_snort_severe_baseline_first_stop_step_experienced_attacker_means,
        train_snort_severe_baseline_first_stop_step_experienced_attacker_stds,
        train_snort_severe_baseline_second_stop_step_experienced_attacker_data,
        train_snort_severe_baseline_second_stop_step_experienced_attacker_means,
        train_snort_severe_baseline_second_stop_step_experienced_attacker_stds,
        train_snort_severe_baseline_third_stop_step_experienced_attacker_data,
        train_snort_severe_baseline_third_stop_step_experienced_attacker_means,
        train_snort_severe_baseline_third_stop_step_experienced_attacker_stds,
        train_snort_severe_baseline_fourth_stop_step_experienced_attacker_data,
        train_snort_severe_baseline_fourth_stop_step_experienced_attacker_means,
        train_snort_severe_baseline_fourth_stop_step_experienced_attacker_stds,
        train_snort_severe_baseline_stops_remaining_experienced_attacker_data,
        train_snort_severe_baseline_stops_remaining_experienced_attacker_means,
        train_snort_severe_baseline_stops_remaining_experienced_attacker_stds,
        train_step_baseline_first_stop_step_experienced_attacker_data,
        train_step_baseline_first_stop_step_experienced_attacker_means,
        train_step_baseline_first_stop_step_experienced_attacker_stds,
        train_step_baseline_second_stop_step_experienced_attacker_data,
        train_step_baseline_second_stop_step_experienced_attacker_means,
        train_step_baseline_second_stop_step_experienced_attacker_stds,
        train_step_baseline_third_stop_step_experienced_attacker_data,
        train_step_baseline_third_stop_step_experienced_attacker_means,
        train_step_baseline_third_stop_step_experienced_attacker_stds,
        train_step_baseline_fourth_stop_step_experienced_attacker_data,
        train_step_baseline_fourth_stop_step_experienced_attacker_means,
        train_step_baseline_fourth_stop_step_experienced_attacker_stds,
        train_step_baseline_stops_remaining_experienced_attacker_data,
        train_step_baseline_stops_remaining_experienced_attacker_means,
        train_step_baseline_stops_remaining_experienced_attacker_stds,
        train_optimal_episode_steps_experienced_attacker_data, train_optimal_episode_steps_experienced_attacker_means,
        train_optimal_episode_steps_experienced_attacker_stds,
        avg_eval_rewards_data_experienced_attacker, avg_eval_rewards_means_experienced_attacker,
        avg_eval_rewards_stds_experienced_attacker,
        avg_eval_steps_data_experienced_attacker, avg_eval_steps_means_experienced_attacker,
        avg_eval_steps_stds_experienced_attacker,
        avg_eval_caught_frac_data_experienced_attacker, avg_eval_caught_frac_means_experienced_attacker,
        avg_eval_caught_frac_stds_experienced_attacker,
        avg_eval_early_stopping_frac_data_experienced_attacker, avg_eval_early_stopping_means_experienced_attacker,
        avg_eval_early_stopping_stds_experienced_attacker, avg_eval_intrusion_frac_data_experienced_attacker,
        avg_eval_intrusion_means_experienced_attacker,
        avg_eval_intrusion_stds_experienced_attacker,
        avg_eval_i_steps_data_experienced_attacker, avg_eval_i_steps_means_experienced_attacker,
        avg_eval_i_steps_stds_experienced_attacker,
        avg_eval_uncaught_intrusion_steps_data_experienced_attacker,
        avg_eval_uncaught_intrusion_steps_means_experienced_attacker,
        avg_eval_uncaught_intrusion_steps_stds_experienced_attacker,
        avg_eval_optimal_defender_rewards_experienced_attacker_data,
        avg_eval_optimal_defender_rewards_experienced_attacker_means,
        avg_eval_optimal_defender_rewards_experienced_attacker_stds,
        eval_snort_severe_baseline_rewards_data_experienced_attacker,
        eval_snort_severe_baseline_rewards_means_experienced_attacker,
        eval_snort_severe_baseline_rewards_stds_experienced_attacker,
        eval_step_baseline_rewards_data_experienced_attacker, eval_step_baseline_rewards_means_experienced_attacker,
        eval_step_baseline_rewards_stds_experienced_attacker,
        eval_snort_severe_baseline_steps_data_experienced_attacker,
        eval_snort_severe_baseline_steps_means_experienced_attacker,
        eval_snort_severe_baseline_steps_stds_experienced_attacker,
        eval_step_baseline_steps_data_experienced_attacker, eval_step_baseline_steps_means_experienced_attacker,
        eval_step_baseline_steps_stds_experienced_attacker,
        eval_snort_severe_baseline_early_stopping_data_experienced_attacker,
        eval_snort_severe_baseline_early_stopping_means_experienced_attacker,
        eval_snort_severe_baseline_early_stopping_stds_experienced_attacker,
        eval_step_baseline_early_stopping_data_experienced_attacker,
        eval_step_baseline_early_stopping_means_experienced_attacker,
        eval_step_baseline_early_stopping_stds_experienced_attacker,
        eval_snort_severe_baseline_caught_attacker_data_experienced_attacker,
        eval_snort_severe_baseline_caught_attacker_means_experienced_attacker,
        eval_snort_severe_baseline_caught_attacker_stds_experienced_attacker,
        eval_step_baseline_caught_attacker_data_experienced_attacker,
        eval_step_baseline_caught_attacker_means_experienced_attacker,
        eval_step_baseline_caught_attacker_stds_experienced_attacker,
        eval_snort_severe_baseline_uncaught_intrusion_steps_data_experienced_attacker,
        eval_snort_severe_baseline_uncaught_intrusion_steps_means_experienced_attacker,
        eval_snort_severe_baseline_uncaught_intrusion_steps_stds_experienced_attacker,
        eval_step_baseline_uncaught_intrusion_steps_data_experienced_attacker,
        eval_step_baseline_uncaught_intrusion_steps_means_experienced_attacker,
        eval_step_baseline_uncaught_intrusion_steps_stds_experienced_attacker,
        eval_defender_first_stop_step_experienced_attacker_data,
        eval_defender_first_stop_step_experienced_attacker_means, eval_defender_first_stop_step_experienced_attacker_stds,
        eval_defender_second_stop_step_experienced_attacker_data,
        eval_defender_second_stop_step_experienced_attacker_means, eval_defender_second_stop_step_experienced_attacker_stds,
        eval_defender_third_stop_step_experienced_attacker_data, eval_defender_third_stop_step_experienced_attacker_means,
        eval_defender_third_stop_step_experienced_attacker_stds, eval_defender_fourth_stop_step_experienced_attacker_data,
        eval_defender_fourth_stop_step_experienced_attacker_means, eval_defender_fourth_stop_step_experienced_attacker_stds,
        eval_defender_stops_remaining_experienced_attacker_data, eval_defender_stops_remaining_experienced_attacker_means,
        eval_defender_stops_remaining_experienced_attacker_stds, eval_optimal_first_stop_step_experienced_attacker_data,
        eval_optimal_first_stop_step_experienced_attacker_means, eval_optimal_first_stop_step_experienced_attacker_stds,
        eval_optimal_second_stop_step_experienced_attacker_data, eval_optimal_second_stop_step_experienced_attacker_means,
        eval_optimal_second_stop_step_experienced_attacker_stds, eval_optimal_third_stop_step_experienced_attacker_data,
        eval_optimal_third_stop_step_experienced_attacker_means, eval_optimal_third_stop_step_experienced_attacker_stds,
        eval_optimal_fourth_stop_step_experienced_attacker_data, eval_optimal_fourth_stop_step_experienced_attacker_means,
        eval_optimal_fourth_stop_step_experienced_attacker_stds, eval_optimal_stops_remaining_experienced_attacker_data,
        eval_optimal_stops_remaining_experienced_attacker_means, eval_optimal_stops_remaining_experienced_attacker_stds,
        eval_snort_severe_baseline_first_stop_step_experienced_attacker_data,
        eval_snort_severe_baseline_first_stop_step_experienced_attacker_means,
        eval_snort_severe_baseline_first_stop_step_experienced_attacker_stds,
        eval_snort_severe_baseline_second_stop_step_experienced_attacker_data,
        eval_snort_severe_baseline_second_stop_step_experienced_attacker_means,
        eval_snort_severe_baseline_second_stop_step_experienced_attacker_stds,
        eval_snort_severe_baseline_third_stop_step_experienced_attacker_data,
        eval_snort_severe_baseline_third_stop_step_experienced_attacker_means,
        eval_snort_severe_baseline_third_stop_step_experienced_attacker_stds,
        eval_snort_severe_baseline_fourth_stop_step_experienced_attacker_data,
        eval_snort_severe_baseline_fourth_stop_step_experienced_attacker_means,
        eval_snort_severe_baseline_fourth_stop_step_experienced_attacker_stds,
        eval_snort_severe_baseline_stops_remaining_experienced_attacker_data,
        eval_snort_severe_baseline_stops_remaining_experienced_attacker_means,
        eval_snort_severe_baseline_stops_remaining_experienced_attacker_stds,
        eval_step_baseline_first_stop_step_experienced_attacker_data,
        eval_step_baseline_first_stop_step_experienced_attacker_means,
        eval_step_baseline_first_stop_step_experienced_attacker_stds,
        eval_step_baseline_second_stop_step_experienced_attacker_data,
        eval_step_baseline_second_stop_step_experienced_attacker_means,
        eval_step_baseline_second_stop_step_experienced_attacker_stds,
        eval_step_baseline_third_stop_step_experienced_attacker_data,
        eval_step_baseline_third_stop_step_experienced_attacker_means,
        eval_step_baseline_third_stop_step_experienced_attacker_stds,
        eval_step_baseline_fourth_stop_step_experienced_attacker_data,
        eval_step_baseline_fourth_stop_step_experienced_attacker_means,
        eval_step_baseline_fourth_stop_step_experienced_attacker_stds,
        eval_step_baseline_stops_remaining_experienced_attacker_data,
        eval_step_baseline_stops_remaining_experienced_attacker_means,
        eval_step_baseline_stops_remaining_experienced_attacker_stds,
        eval_optimal_episode_steps_experienced_attacker_data, eval_optimal_episode_steps_experienced_attacker_means,
        eval_optimal_episode_steps_experienced_attacker_stds,
        avg_eval_2_rewards_data_experienced_attacker, avg_eval_2_rewards_means_experienced_attacker,
        avg_eval_2_rewards_stds_experienced_attacker,
        avg_eval_2_steps_data_experienced_attacker, avg_eval_2_steps_means_experienced_attacker,
        avg_eval_2_steps_stds_experienced_attacker,
        avg_eval_2_caught_frac_data_experienced_attacker, avg_eval_2_caught_frac_means_experienced_attacker,
        avg_eval_2_caught_frac_stds_experienced_attacker,
        avg_eval_2_early_stopping_frac_data_experienced_attacker, avg_eval_2_early_stopping_means_experienced_attacker,
        avg_eval_2_early_stopping_stds_experienced_attacker, avg_eval_2_intrusion_frac_data_experienced_attacker,
        avg_eval_2_intrusion_means_experienced_attacker,
        avg_eval_2_intrusion_stds_experienced_attacker,
        avg_eval_2_i_steps_data_experienced_attacker, avg_eval_2_i_steps_means_experienced_attacker,
        avg_eval_2_i_steps_stds_experienced_attacker,
        avg_eval_2_uncaught_intrusion_steps_data_experienced_attacker,
        avg_eval_2_uncaught_intrusion_steps_means_experienced_attacker,
        avg_eval_2_uncaught_intrusion_steps_stds_experienced_attacker,
        avg_eval_2_optimal_defender_rewards_experienced_attacker_data,
        avg_eval_2_optimal_defender_rewards_experienced_attacker_means,
        avg_eval_2_optimal_defender_rewards_experienced_attacker_stds,
        eval_2_snort_severe_baseline_rewards_data_experienced_attacker,
        eval_2_snort_severe_baseline_rewards_means_experienced_attacker,
        eval_2_snort_severe_baseline_rewards_stds_experienced_attacker,
        eval_2_step_baseline_rewards_data_experienced_attacker,
        eval_2_step_baseline_rewards_means_experienced_attacker, eval_2_step_baseline_rewards_stds_experienced_attacker,
        eval_2_snort_severe_baseline_steps_data_experienced_attacker,
        eval_2_snort_severe_baseline_steps_means_experienced_attacker,
        eval_2_snort_severe_baseline_steps_stds_experienced_attacker,
        eval_2_step_baseline_steps_data_experienced_attacker, eval_2_step_baseline_steps_means_experienced_attacker,
        eval_2_step_baseline_steps_stds_experienced_attacker,
        eval_2_snort_severe_baseline_early_stopping_data_experienced_attacker,
        eval_2_snort_severe_baseline_early_stopping_means_experienced_attacker,
        eval_2_snort_severe_baseline_early_stopping_stds_experienced_attacker,
        eval_2_step_baseline_early_stopping_data_experienced_attacker,
        eval_2_step_baseline_early_stopping_means_experienced_attacker,
        eval_2_step_baseline_early_stopping_stds_experienced_attacker,
        eval_2_snort_severe_baseline_caught_attacker_data_experienced_attacker,
        eval_2_snort_severe_baseline_caught_attacker_means_experienced_attacker,
        eval_2_snort_severe_baseline_caught_attacker_stds_experienced_attacker,
        eval_2_step_baseline_caught_attacker_data_experienced_attacker,
        eval_2_step_baseline_caught_attacker_means_experienced_attacker,
        eval_2_step_baseline_caught_attacker_stds_experienced_attacker,
        eval_2_snort_severe_baseline_uncaught_intrusion_steps_data_experienced_attacker,
        eval_2_snort_severe_baseline_uncaught_intrusion_steps_means_experienced_attacker,
        eval_2_snort_severe_baseline_uncaught_intrusion_steps_stds_experienced_attacker,
        eval_2_step_baseline_uncaught_intrusion_steps_data_experienced_attacker,
        eval_2_step_baseline_uncaught_intrusion_steps_means_experienced_attacker,
        eval_2_step_baseline_uncaught_intrusion_steps_stds_experienced_attacker,
        eval_2_defender_first_stop_step_experienced_attacker_data,
        eval_2_defender_first_stop_step_experienced_attacker_means, eval_2_defender_first_stop_step_experienced_attacker_stds,
        eval_2_defender_second_stop_step_experienced_attacker_data,
        eval_2_defender_second_stop_step_experienced_attacker_means, eval_2_defender_second_stop_step_experienced_attacker_stds,
        eval_2_defender_third_stop_step_experienced_attacker_data, eval_2_defender_third_stop_step_experienced_attacker_means,
        eval_2_defender_third_stop_step_experienced_attacker_stds, eval_2_defender_fourth_stop_step_experienced_attacker_data,
        eval_2_defender_fourth_stop_step_experienced_attacker_means, eval_2_defender_fourth_stop_step_experienced_attacker_stds,
        eval_2_defender_stops_remaining_experienced_attacker_data, eval_2_defender_stops_remaining_experienced_attacker_means,
        eval_2_defender_stops_remaining_experienced_attacker_stds, eval_2_optimal_first_stop_step_experienced_attacker_data,
        eval_2_optimal_first_stop_step_experienced_attacker_means, eval_2_optimal_first_stop_step_experienced_attacker_stds,
        eval_2_optimal_second_stop_step_experienced_attacker_data, eval_2_optimal_second_stop_step_experienced_attacker_means,
        eval_2_optimal_second_stop_step_experienced_attacker_stds, eval_2_optimal_third_stop_step_experienced_attacker_data,
        eval_2_optimal_third_stop_step_experienced_attacker_means, eval_2_optimal_third_stop_step_experienced_attacker_stds,
        eval_2_optimal_fourth_stop_step_experienced_attacker_data, eval_2_optimal_fourth_stop_step_experienced_attacker_means,
        eval_2_optimal_fourth_stop_step_experienced_attacker_stds, eval_2_optimal_stops_remaining_experienced_attacker_data,
        eval_2_optimal_stops_remaining_experienced_attacker_means, eval_2_optimal_stops_remaining_experienced_attacker_stds,
        eval_2_snort_severe_baseline_first_stop_step_experienced_attacker_data,
        eval_2_snort_severe_baseline_first_stop_step_experienced_attacker_means,
        eval_2_snort_severe_baseline_first_stop_step_experienced_attacker_stds,
        eval_2_snort_severe_baseline_second_stop_step_experienced_attacker_data,
        eval_2_snort_severe_baseline_second_stop_step_experienced_attacker_means,
        eval_2_snort_severe_baseline_second_stop_step_experienced_attacker_stds,
        eval_2_snort_severe_baseline_third_stop_step_experienced_attacker_data,
        eval_2_snort_severe_baseline_third_stop_step_experienced_attacker_means,
        eval_2_snort_severe_baseline_third_stop_step_experienced_attacker_stds,
        eval_2_snort_severe_baseline_fourth_stop_step_experienced_attacker_data,
        eval_2_snort_severe_baseline_fourth_stop_step_experienced_attacker_means,
        eval_2_snort_severe_baseline_fourth_stop_step_experienced_attacker_stds,
        eval_2_snort_severe_baseline_stops_remaining_experienced_attacker_data,
        eval_2_snort_severe_baseline_stops_remaining_experienced_attacker_means,
        eval_2_snort_severe_baseline_stops_remaining_experienced_attacker_stds,
        eval_2_step_baseline_first_stop_step_experienced_attacker_data,
        eval_2_step_baseline_first_stop_step_experienced_attacker_means,
        eval_2_step_baseline_first_stop_step_experienced_attacker_stds,
        eval_2_step_baseline_second_stop_step_experienced_attacker_data,
        eval_2_step_baseline_second_stop_step_experienced_attacker_means,
        eval_2_step_baseline_second_stop_step_experienced_attacker_stds,
        eval_2_step_baseline_third_stop_step_experienced_attacker_data,
        eval_2_step_baseline_third_stop_step_experienced_attacker_means,
        eval_2_step_baseline_third_stop_step_experienced_attacker_stds,
        eval_2_step_baseline_fourth_stop_step_experienced_attacker_data,
        eval_2_step_baseline_fourth_stop_step_experienced_attacker_means,
        eval_2_step_baseline_fourth_stop_step_experienced_attacker_stds,
        eval_2_step_baseline_stops_remaining_experienced_attacker_data,
        eval_2_step_baseline_stops_remaining_experienced_attacker_means,
        eval_2_step_baseline_stops_remaining_experienced_attacker_stds,
        eval_2_optimal_episode_steps_experienced_attacker_data, eval_2_optimal_episode_steps_experienced_attacker_means,
        eval_2_optimal_episode_steps_experienced_attacker_stds,
        avg_train_rewards_data_expert_attacker, avg_train_rewards_means_expert_attacker,
        avg_train_rewards_stds_expert_attacker,
        avg_train_steps_data_expert_attacker, avg_train_steps_means_expert_attacker,
        avg_train_steps_stds_expert_attacker,
        avg_train_caught_frac_data_expert_attacker, avg_train_caught_frac_means_expert_attacker,
        avg_train_caught_frac_stds_expert_attacker,
        avg_train_early_stopping_frac_data_expert_attacker, avg_train_early_stopping_means_expert_attacker,
        avg_train_early_stopping_stds_expert_attacker, avg_train_intrusion_frac_data_expert_attacker,
        avg_train_intrusion_means_expert_attacker,
        avg_train_intrusion_stds_expert_attacker,
        avg_train_i_steps_data_expert_attacker, avg_train_i_steps_means_expert_attacker,
        avg_train_i_steps_stds_expert_attacker,
        avg_train_uncaught_intrusion_steps_data_expert_attacker,
        avg_train_uncaught_intrusion_steps_means_expert_attacker,
        avg_train_uncaught_intrusion_steps_stds_expert_attacker,
        avg_train_optimal_defender_rewards_expert_attacker_data,
        avg_train_optimal_defender_rewards_expert_attacker_means,
        avg_train_optimal_defender_rewards_expert_attacker_stds,
        train_snort_severe_baseline_rewards_data_expert_attacker,
        train_snort_severe_baseline_rewards_means_expert_attacker,
        train_snort_severe_baseline_rewards_stds_expert_attacker, train_step_baseline_rewards_data_expert_attacker,
        train_step_baseline_rewards_means_expert_attacker, train_step_baseline_rewards_stds_expert_attacker,
        train_snort_severe_baseline_steps_data_expert_attacker,
        train_snort_severe_baseline_steps_means_expert_attacker,
        train_snort_severe_baseline_steps_stds_expert_attacker,
        train_step_baseline_steps_data_expert_attacker, train_step_baseline_steps_means_expert_attacker,
        train_step_baseline_steps_stds_expert_attacker,
        train_snort_severe_baseline_early_stopping_data_expert_attacker,
        train_snort_severe_baseline_early_stopping_means_expert_attacker,
        train_snort_severe_baseline_early_stopping_stds_expert_attacker,
        train_step_baseline_early_stopping_data_expert_attacker,
        train_step_baseline_early_stopping_means_expert_attacker,
        train_step_baseline_early_stopping_stds_expert_attacker,
        train_snort_severe_baseline_caught_attacker_data_expert_attacker,
        train_snort_severe_baseline_caught_attacker_means_expert_attacker,
        train_snort_severe_baseline_caught_attacker_stds_expert_attacker,
        train_step_baseline_caught_attacker_data_expert_attacker,
        train_step_baseline_caught_attacker_means_expert_attacker,
        train_step_baseline_caught_attacker_stds_expert_attacker,
        train_snort_severe_baseline_uncaught_intrusion_steps_data_expert_attacker,
        train_snort_severe_baseline_uncaught_intrusion_steps_means_expert_attacker,
        train_snort_severe_baseline_uncaught_intrusion_steps_stds_expert_attacker,
        train_step_baseline_uncaught_intrusion_steps_data_expert_attacker,
        train_step_baseline_uncaught_intrusion_steps_means_expert_attacker,
        train_step_baseline_uncaught_intrusion_steps_stds_expert_attacker,
        train_defender_first_stop_step_expert_attacker_data,
        train_defender_first_stop_step_expert_attacker_means, train_defender_first_stop_step_expert_attacker_stds,
        train_defender_second_stop_step_expert_attacker_data,
        train_defender_second_stop_step_expert_attacker_means, train_defender_second_stop_step_expert_attacker_stds,
        train_defender_third_stop_step_expert_attacker_data, train_defender_third_stop_step_expert_attacker_means,
        train_defender_third_stop_step_expert_attacker_stds, train_defender_fourth_stop_step_expert_attacker_data,
        train_defender_fourth_stop_step_expert_attacker_means, train_defender_fourth_stop_step_expert_attacker_stds,
        train_defender_stops_remaining_expert_attacker_data, train_defender_stops_remaining_expert_attacker_means,
        train_defender_stops_remaining_expert_attacker_stds, train_optimal_first_stop_step_expert_attacker_data,
        train_optimal_first_stop_step_expert_attacker_means, train_optimal_first_stop_step_expert_attacker_stds,
        train_optimal_second_stop_step_expert_attacker_data, train_optimal_second_stop_step_expert_attacker_means,
        train_optimal_second_stop_step_expert_attacker_stds, train_optimal_third_stop_step_expert_attacker_data,
        train_optimal_third_stop_step_expert_attacker_means, train_optimal_third_stop_step_expert_attacker_stds,
        train_optimal_fourth_stop_step_expert_attacker_data, train_optimal_fourth_stop_step_expert_attacker_means,
        train_optimal_fourth_stop_step_expert_attacker_stds, train_optimal_stops_remaining_expert_attacker_data,
        train_optimal_stops_remaining_expert_attacker_means, train_optimal_stops_remaining_expert_attacker_stds,
        train_snort_severe_baseline_first_stop_step_expert_attacker_data,
        train_snort_severe_baseline_first_stop_step_expert_attacker_means,
        train_snort_severe_baseline_first_stop_step_expert_attacker_stds,
        train_snort_severe_baseline_second_stop_step_expert_attacker_data,
        train_snort_severe_baseline_second_stop_step_expert_attacker_means,
        train_snort_severe_baseline_second_stop_step_expert_attacker_stds,
        train_snort_severe_baseline_third_stop_step_expert_attacker_data,
        train_snort_severe_baseline_third_stop_step_expert_attacker_means,
        train_snort_severe_baseline_third_stop_step_expert_attacker_stds,
        train_snort_severe_baseline_fourth_stop_step_expert_attacker_data,
        train_snort_severe_baseline_fourth_stop_step_expert_attacker_means,
        train_snort_severe_baseline_fourth_stop_step_expert_attacker_stds,
        train_snort_severe_baseline_stops_remaining_expert_attacker_data,
        train_snort_severe_baseline_stops_remaining_expert_attacker_means,
        train_snort_severe_baseline_stops_remaining_expert_attacker_stds,
        train_step_baseline_first_stop_step_expert_attacker_data,
        train_step_baseline_first_stop_step_expert_attacker_means,
        train_step_baseline_first_stop_step_expert_attacker_stds,
        train_step_baseline_second_stop_step_expert_attacker_data,
        train_step_baseline_second_stop_step_expert_attacker_means,
        train_step_baseline_second_stop_step_expert_attacker_stds,
        train_step_baseline_third_stop_step_expert_attacker_data,
        train_step_baseline_third_stop_step_expert_attacker_means,
        train_step_baseline_third_stop_step_expert_attacker_stds,
        train_step_baseline_fourth_stop_step_expert_attacker_data,
        train_step_baseline_fourth_stop_step_expert_attacker_means,
        train_step_baseline_fourth_stop_step_expert_attacker_stds,
        train_step_baseline_stops_remaining_expert_attacker_data,
        train_step_baseline_stops_remaining_expert_attacker_means,
        train_step_baseline_stops_remaining_expert_attacker_stds,
        train_optimal_episode_steps_expert_attacker_data, train_optimal_episode_steps_expert_attacker_means,
        train_optimal_episode_steps_expert_attacker_stds,
        avg_eval_rewards_data_expert_attacker, avg_eval_rewards_means_expert_attacker,
        avg_eval_rewards_stds_expert_attacker,
        avg_eval_steps_data_expert_attacker, avg_eval_steps_means_expert_attacker,
        avg_eval_steps_stds_expert_attacker,
        avg_eval_caught_frac_data_expert_attacker, avg_eval_caught_frac_means_expert_attacker,
        avg_eval_caught_frac_stds_expert_attacker,
        avg_eval_early_stopping_frac_data_expert_attacker, avg_eval_early_stopping_means_expert_attacker,
        avg_eval_early_stopping_stds_expert_attacker, avg_eval_intrusion_frac_data_expert_attacker,
        avg_eval_intrusion_means_expert_attacker,
        avg_eval_intrusion_stds_expert_attacker,
        avg_eval_i_steps_data_expert_attacker, avg_eval_i_steps_means_expert_attacker,
        avg_eval_i_steps_stds_expert_attacker,
        avg_eval_uncaught_intrusion_steps_data_expert_attacker,
        avg_eval_uncaught_intrusion_steps_means_expert_attacker,
        avg_eval_uncaught_intrusion_steps_stds_expert_attacker,
        avg_eval_optimal_defender_rewards_expert_attacker_data,
        avg_eval_optimal_defender_rewards_expert_attacker_means,
        avg_eval_optimal_defender_rewards_expert_attacker_stds,
        eval_snort_severe_baseline_rewards_data_expert_attacker,
        eval_snort_severe_baseline_rewards_means_expert_attacker,
        eval_snort_severe_baseline_rewards_stds_expert_attacker,
        eval_step_baseline_rewards_data_expert_attacker, eval_step_baseline_rewards_means_expert_attacker,
        eval_step_baseline_rewards_stds_expert_attacker,
        eval_snort_severe_baseline_steps_data_expert_attacker,
        eval_snort_severe_baseline_steps_means_expert_attacker,
        eval_snort_severe_baseline_steps_stds_expert_attacker,
        eval_step_baseline_steps_data_expert_attacker, eval_step_baseline_steps_means_expert_attacker,
        eval_step_baseline_steps_stds_expert_attacker,
        eval_snort_severe_baseline_early_stopping_data_expert_attacker,
        eval_snort_severe_baseline_early_stopping_means_expert_attacker,
        eval_snort_severe_baseline_early_stopping_stds_expert_attacker,
        eval_step_baseline_early_stopping_data_expert_attacker,
        eval_step_baseline_early_stopping_means_expert_attacker,
        eval_step_baseline_early_stopping_stds_expert_attacker,
        eval_snort_severe_baseline_caught_attacker_data_expert_attacker,
        eval_snort_severe_baseline_caught_attacker_means_expert_attacker,
        eval_snort_severe_baseline_caught_attacker_stds_expert_attacker,
        eval_step_baseline_caught_attacker_data_expert_attacker,
        eval_step_baseline_caught_attacker_means_expert_attacker,
        eval_step_baseline_caught_attacker_stds_expert_attacker,
        eval_snort_severe_baseline_uncaught_intrusion_steps_data_expert_attacker,
        eval_snort_severe_baseline_uncaught_intrusion_steps_means_expert_attacker,
        eval_snort_severe_baseline_uncaught_intrusion_steps_stds_expert_attacker,
        eval_step_baseline_uncaught_intrusion_steps_data_expert_attacker,
        eval_step_baseline_uncaught_intrusion_steps_means_expert_attacker,
        eval_step_baseline_uncaught_intrusion_steps_stds_expert_attacker,
        eval_defender_first_stop_step_expert_attacker_data,
        eval_defender_first_stop_step_expert_attacker_means, eval_defender_first_stop_step_expert_attacker_stds,
        eval_defender_second_stop_step_expert_attacker_data,
        eval_defender_second_stop_step_expert_attacker_means, eval_defender_second_stop_step_expert_attacker_stds,
        eval_defender_third_stop_step_expert_attacker_data, eval_defender_third_stop_step_expert_attacker_means,
        eval_defender_third_stop_step_expert_attacker_stds, eval_defender_fourth_stop_step_expert_attacker_data,
        eval_defender_fourth_stop_step_expert_attacker_means, eval_defender_fourth_stop_step_expert_attacker_stds,
        eval_defender_stops_remaining_expert_attacker_data, eval_defender_stops_remaining_expert_attacker_means,
        eval_defender_stops_remaining_expert_attacker_stds, eval_optimal_first_stop_step_expert_attacker_data,
        eval_optimal_first_stop_step_expert_attacker_means, eval_optimal_first_stop_step_expert_attacker_stds,
        eval_optimal_second_stop_step_expert_attacker_data, eval_optimal_second_stop_step_expert_attacker_means,
        eval_optimal_second_stop_step_expert_attacker_stds, eval_optimal_third_stop_step_expert_attacker_data,
        eval_optimal_third_stop_step_expert_attacker_means, eval_optimal_third_stop_step_expert_attacker_stds,
        eval_optimal_fourth_stop_step_expert_attacker_data, eval_optimal_fourth_stop_step_expert_attacker_means,
        eval_optimal_fourth_stop_step_expert_attacker_stds, eval_optimal_stops_remaining_expert_attacker_data,
        eval_optimal_stops_remaining_expert_attacker_means, eval_optimal_stops_remaining_expert_attacker_stds,
        eval_snort_severe_baseline_first_stop_step_expert_attacker_data,
        eval_snort_severe_baseline_first_stop_step_expert_attacker_means,
        eval_snort_severe_baseline_first_stop_step_expert_attacker_stds,
        eval_snort_severe_baseline_second_stop_step_expert_attacker_data,
        eval_snort_severe_baseline_second_stop_step_expert_attacker_means,
        eval_snort_severe_baseline_second_stop_step_expert_attacker_stds,
        eval_snort_severe_baseline_third_stop_step_expert_attacker_data,
        eval_snort_severe_baseline_third_stop_step_expert_attacker_means,
        eval_snort_severe_baseline_third_stop_step_expert_attacker_stds,
        eval_snort_severe_baseline_fourth_stop_step_expert_attacker_data,
        eval_snort_severe_baseline_fourth_stop_step_expert_attacker_means,
        eval_snort_severe_baseline_fourth_stop_step_expert_attacker_stds,
        eval_snort_severe_baseline_stops_remaining_expert_attacker_data,
        eval_snort_severe_baseline_stops_remaining_expert_attacker_means,
        eval_snort_severe_baseline_stops_remaining_expert_attacker_stds,
        eval_step_baseline_first_stop_step_expert_attacker_data,
        eval_step_baseline_first_stop_step_expert_attacker_means,
        eval_step_baseline_first_stop_step_expert_attacker_stds,
        eval_step_baseline_second_stop_step_expert_attacker_data,
        eval_step_baseline_second_stop_step_expert_attacker_means,
        eval_step_baseline_second_stop_step_expert_attacker_stds,
        eval_step_baseline_third_stop_step_expert_attacker_data,
        eval_step_baseline_third_stop_step_expert_attacker_means,
        eval_step_baseline_third_stop_step_expert_attacker_stds,
        eval_step_baseline_fourth_stop_step_expert_attacker_data,
        eval_step_baseline_fourth_stop_step_expert_attacker_means,
        eval_step_baseline_fourth_stop_step_expert_attacker_stds,
        eval_step_baseline_stops_remaining_expert_attacker_data,
        eval_step_baseline_stops_remaining_expert_attacker_means,
        eval_step_baseline_stops_remaining_expert_attacker_stds,
        eval_optimal_episode_steps_expert_attacker_data, eval_optimal_episode_steps_expert_attacker_means,
        eval_optimal_episode_steps_expert_attacker_stds,
        avg_eval_2_rewards_data_expert_attacker, avg_eval_2_rewards_means_expert_attacker,
        avg_eval_2_rewards_stds_expert_attacker,
        avg_eval_2_steps_data_expert_attacker, avg_eval_2_steps_means_expert_attacker,
        avg_eval_2_steps_stds_expert_attacker,
        avg_eval_2_caught_frac_data_expert_attacker, avg_eval_2_caught_frac_means_expert_attacker,
        avg_eval_2_caught_frac_stds_expert_attacker,
        avg_eval_2_early_stopping_frac_data_expert_attacker, avg_eval_2_early_stopping_means_expert_attacker,
        avg_eval_2_early_stopping_stds_expert_attacker, avg_eval_2_intrusion_frac_data_expert_attacker,
        avg_eval_2_intrusion_means_expert_attacker,
        avg_eval_2_intrusion_stds_expert_attacker,
        avg_eval_2_i_steps_data_expert_attacker, avg_eval_2_i_steps_means_expert_attacker,
        avg_eval_2_i_steps_stds_expert_attacker,
        avg_eval_2_uncaught_intrusion_steps_data_expert_attacker,
        avg_eval_2_uncaught_intrusion_steps_means_expert_attacker,
        avg_eval_2_uncaught_intrusion_steps_stds_expert_attacker,
        avg_eval_2_optimal_defender_rewards_expert_attacker_data,
        avg_eval_2_optimal_defender_rewards_expert_attacker_means,
        avg_eval_2_optimal_defender_rewards_expert_attacker_stds,
        eval_2_snort_severe_baseline_rewards_data_expert_attacker,
        eval_2_snort_severe_baseline_rewards_means_expert_attacker,
        eval_2_snort_severe_baseline_rewards_stds_expert_attacker,
        eval_2_step_baseline_rewards_data_expert_attacker,
        eval_2_step_baseline_rewards_means_expert_attacker, eval_2_step_baseline_rewards_stds_expert_attacker,
        eval_2_snort_severe_baseline_steps_data_expert_attacker,
        eval_2_snort_severe_baseline_steps_means_expert_attacker,
        eval_2_snort_severe_baseline_steps_stds_expert_attacker,
        eval_2_step_baseline_steps_data_expert_attacker, eval_2_step_baseline_steps_means_expert_attacker,
        eval_2_step_baseline_steps_stds_expert_attacker,
        eval_2_snort_severe_baseline_early_stopping_data_expert_attacker,
        eval_2_snort_severe_baseline_early_stopping_means_expert_attacker,
        eval_2_snort_severe_baseline_early_stopping_stds_expert_attacker,
        eval_2_step_baseline_early_stopping_data_expert_attacker,
        eval_2_step_baseline_early_stopping_means_expert_attacker,
        eval_2_step_baseline_early_stopping_stds_expert_attacker,
        eval_2_snort_severe_baseline_caught_attacker_data_expert_attacker,
        eval_2_snort_severe_baseline_caught_attacker_means_expert_attacker,
        eval_2_snort_severe_baseline_caught_attacker_stds_expert_attacker,
        eval_2_step_baseline_caught_attacker_data_expert_attacker,
        eval_2_step_baseline_caught_attacker_means_expert_attacker,
        eval_2_step_baseline_caught_attacker_stds_expert_attacker,
        eval_2_snort_severe_baseline_uncaught_intrusion_steps_data_expert_attacker,
        eval_2_snort_severe_baseline_uncaught_intrusion_steps_means_expert_attacker,
        eval_2_snort_severe_baseline_uncaught_intrusion_steps_stds_expert_attacker,
        eval_2_step_baseline_uncaught_intrusion_steps_data_expert_attacker,
        eval_2_step_baseline_uncaught_intrusion_steps_means_expert_attacker,
        eval_2_step_baseline_uncaught_intrusion_steps_stds_expert_attacker,
        eval_2_defender_first_stop_step_expert_attacker_data,
        eval_2_defender_first_stop_step_expert_attacker_means, eval_2_defender_first_stop_step_expert_attacker_stds,
        eval_2_defender_second_stop_step_expert_attacker_data,
        eval_2_defender_second_stop_step_expert_attacker_means, eval_2_defender_second_stop_step_expert_attacker_stds,
        eval_2_defender_third_stop_step_expert_attacker_data, eval_2_defender_third_stop_step_expert_attacker_means,
        eval_2_defender_third_stop_step_expert_attacker_stds, eval_2_defender_fourth_stop_step_expert_attacker_data,
        eval_2_defender_fourth_stop_step_expert_attacker_means, eval_2_defender_fourth_stop_step_expert_attacker_stds,
        eval_2_defender_stops_remaining_expert_attacker_data, eval_2_defender_stops_remaining_expert_attacker_means,
        eval_2_defender_stops_remaining_expert_attacker_stds, eval_2_optimal_first_stop_step_expert_attacker_data,
        eval_2_optimal_first_stop_step_expert_attacker_means, eval_2_optimal_first_stop_step_expert_attacker_stds,
        eval_2_optimal_second_stop_step_expert_attacker_data, eval_2_optimal_second_stop_step_expert_attacker_means,
        eval_2_optimal_second_stop_step_expert_attacker_stds, eval_2_optimal_third_stop_step_expert_attacker_data,
        eval_2_optimal_third_stop_step_expert_attacker_means, eval_2_optimal_third_stop_step_expert_attacker_stds,
        eval_2_optimal_fourth_stop_step_expert_attacker_data, eval_2_optimal_fourth_stop_step_expert_attacker_means,
        eval_2_optimal_fourth_stop_step_expert_attacker_stds, eval_2_optimal_stops_remaining_expert_attacker_data,
        eval_2_optimal_stops_remaining_expert_attacker_means, eval_2_optimal_stops_remaining_expert_attacker_stds,
        eval_2_snort_severe_baseline_first_stop_step_expert_attacker_data,
        eval_2_snort_severe_baseline_first_stop_step_expert_attacker_means,
        eval_2_snort_severe_baseline_first_stop_step_expert_attacker_stds,
        eval_2_snort_severe_baseline_second_stop_step_expert_attacker_data,
        eval_2_snort_severe_baseline_second_stop_step_expert_attacker_means,
        eval_2_snort_severe_baseline_second_stop_step_expert_attacker_stds,
        eval_2_snort_severe_baseline_third_stop_step_expert_attacker_data,
        eval_2_snort_severe_baseline_third_stop_step_expert_attacker_means,
        eval_2_snort_severe_baseline_third_stop_step_expert_attacker_stds,
        eval_2_snort_severe_baseline_fourth_stop_step_expert_attacker_data,
        eval_2_snort_severe_baseline_fourth_stop_step_expert_attacker_means,
        eval_2_snort_severe_baseline_fourth_stop_step_expert_attacker_stds,
        eval_2_snort_severe_baseline_stops_remaining_expert_attacker_data,
        eval_2_snort_severe_baseline_stops_remaining_expert_attacker_means,
        eval_2_snort_severe_baseline_stops_remaining_expert_attacker_stds,
        eval_2_step_baseline_first_stop_step_expert_attacker_data,
        eval_2_step_baseline_first_stop_step_expert_attacker_means,
        eval_2_step_baseline_first_stop_step_expert_attacker_stds,
        eval_2_step_baseline_second_stop_step_expert_attacker_data,
        eval_2_step_baseline_second_stop_step_expert_attacker_means,
        eval_2_step_baseline_second_stop_step_expert_attacker_stds,
        eval_2_step_baseline_third_stop_step_expert_attacker_data,
        eval_2_step_baseline_third_stop_step_expert_attacker_means,
        eval_2_step_baseline_third_stop_step_expert_attacker_stds,
        eval_2_step_baseline_fourth_stop_step_expert_attacker_data,
        eval_2_step_baseline_fourth_stop_step_expert_attacker_means,
        eval_2_step_baseline_fourth_stop_step_expert_attacker_stds,
        eval_2_step_baseline_stops_remaining_expert_attacker_data,
        eval_2_step_baseline_stops_remaining_expert_attacker_means,
        eval_2_step_baseline_stops_remaining_expert_attacker_stds,
        eval_2_optimal_episode_steps_expert_attacker_data, eval_2_optimal_episode_steps_expert_attacker_means,
        eval_2_optimal_episode_steps_expert_attacker_stds):
    print("plot")

    suffix = "gensim"
    ylim_rew = (-300, 170)
    max_iter = 400
    print(train_snort_severe_baseline_rewards_data_novice_attacker[0:max_iter])
    print(train_snort_severe_baseline_rewards_data_experienced_attacker[0:max_iter])
    print(train_snort_severe_baseline_rewards_data_expert_attacker[0:max_iter])


    plotting_util_defender.plot_defender_simulation_emulation_tnsm_21_multiple_attackers_four_stops(
        avg_rewards_data_simulation_novice_attacker=avg_train_rewards_data_novice_attacker[0:max_iter],
        avg_rewards_means_simulation_novice_attacker= avg_train_rewards_means_novice_attacker[0:max_iter],
        avg_rewards_stds_simulation_novice_attacker= avg_train_rewards_stds_novice_attacker[0:max_iter],
        avg_steps_data_simulation_novice_attacker= avg_train_steps_data_novice_attacker[0:max_iter],
        avg_steps_means_simulation_novice_attacker=avg_train_steps_means_novice_attacker[0:max_iter],
        avg_steps_stds_simulation_novice_attacker= avg_train_steps_stds_novice_attacker[0:max_iter],
        avg_caught_frac_data_simulation_novice_attacker= avg_train_caught_frac_data_novice_attacker[0:max_iter],
        avg_caught_frac_means_simulation_novice_attacker= avg_train_caught_frac_means_novice_attacker[0:max_iter],
        avg_caught_frac_stds_simulation_novice_attacker= avg_train_caught_frac_stds_novice_attacker[0:max_iter],
        avg_early_stopping_frac_data_simulation_novice_attacker= avg_train_early_stopping_frac_data_novice_attacker[0:max_iter],
        avg_early_stopping_means_simulation_novice_attacker= avg_train_early_stopping_means_novice_attacker[0:max_iter],
        avg_early_stopping_stds_simulation_novice_attacker= avg_train_early_stopping_stds_novice_attacker[0:max_iter],
        avg_intrusion_frac_data_simulation_novice_attacker= avg_train_intrusion_frac_data_novice_attacker[0:max_iter],
        avg_intrusion_means_simulation_novice_attacker= avg_train_intrusion_means_novice_attacker[0:max_iter],
        avg_intrusion_stds_simulation_novice_attacker= avg_train_intrusion_stds_novice_attacker[0:max_iter],
        avg_i_steps_data_simulation_novice_attacker= avg_train_uncaught_intrusion_steps_data_novice_attacker[0:max_iter],
        avg_i_steps_means_simulation_novice_attacker= avg_train_uncaught_intrusion_steps_means_novice_attacker[0:max_iter],
        avg_i_steps_stds_simulation_novice_attacker= avg_train_uncaught_intrusion_steps_stds_novice_attacker[0:max_iter],
        optimal_rewards_data_simulation_novice_attacker = avg_train_optimal_defender_rewards_novice_attacker_data[0:max_iter],
        optimal_rewards_means_simulation_novice_attacker=avg_train_optimal_defender_rewards_novice_attacker_means[0:max_iter],
        optimal_rewards_stds_simulation_novice_attacker = avg_train_optimal_defender_rewards_novice_attacker_stds[0:max_iter],
        optimal_steps_data_simulation_novice_attacker = train_optimal_episode_steps_novice_attacker_data[0:max_iter],
        optimal_steps_means_simulation_novice_attacker = train_optimal_episode_steps_novice_attacker_means[0:max_iter],
        optimal_steps_stds_simulation_novice_attacker = train_optimal_episode_steps_novice_attacker_stds[0:max_iter],
        avg_rewards_data_emulation_novice_attacker=avg_eval_2_rewards_data_novice_attacker[0:max_iter],
        avg_rewards_means_emulation_novice_attacker=avg_eval_2_rewards_means_novice_attacker[0:max_iter],
        avg_rewards_stds_emulation_novice_attacker=avg_eval_2_rewards_stds_novice_attacker[0:max_iter],
        avg_steps_data_emulation_novice_attacker=avg_eval_2_steps_data_novice_attacker[0:max_iter],
        avg_steps_means_emulation_novice_attacker=avg_eval_2_steps_means_novice_attacker[0:max_iter],
        avg_steps_stds_emulation_novice_attacker=avg_eval_2_steps_stds_novice_attacker[0:max_iter],
        avg_caught_frac_data_emulation_novice_attacker=avg_eval_2_caught_frac_data_novice_attacker[0:max_iter],
        avg_caught_frac_means_emulation_novice_attacker=avg_eval_2_caught_frac_means_novice_attacker[0:max_iter],
        avg_caught_frac_stds_emulation_novice_attacker=avg_eval_2_caught_frac_stds_novice_attacker[0:max_iter],
        avg_early_stopping_frac_data_emulation_novice_attacker=avg_eval_2_early_stopping_frac_data_novice_attacker[0:max_iter],
        avg_early_stopping_means_emulation_novice_attacker=avg_eval_2_early_stopping_means_novice_attacker[0:max_iter],
        avg_early_stopping_stds_emulation_novice_attacker=avg_eval_2_early_stopping_stds_novice_attacker[0:max_iter],
        avg_intrusion_frac_data_emulation_novice_attacker=avg_eval_2_intrusion_frac_data_novice_attacker[0:max_iter],
        avg_intrusion_means_emulation_novice_attacker=avg_eval_2_intrusion_means_novice_attacker[0:max_iter],
        avg_intrusion_stds_emulation_novice_attacker=avg_eval_2_intrusion_stds_novice_attacker[0:max_iter],
        avg_i_steps_data_emulation_novice_attacker=avg_eval_2_uncaught_intrusion_steps_data_novice_attacker[0:max_iter],
        avg_i_steps_means_emulation_novice_attacker=avg_eval_2_uncaught_intrusion_steps_means_novice_attacker[0:max_iter],
        avg_i_steps_stds_emulation_novice_attacker=avg_eval_2_uncaught_intrusion_steps_stds_novice_attacker[0:max_iter],
        optimal_rewards_data_emulation_novice_attacker=avg_eval_2_optimal_defender_rewards_novice_attacker_data[0:max_iter],
        optimal_rewards_means_emulation_novice_attacker=avg_eval_2_optimal_defender_rewards_novice_attacker_means[0:max_iter],
        optimal_rewards_stds_emulation_novice_attacker=avg_eval_2_optimal_defender_rewards_novice_attacker_stds[0:max_iter],
        optimal_steps_data_emulation_novice_attacker=eval_2_optimal_episode_steps_novice_attacker_data[0:max_iter],
        optimal_steps_means_emulation_novice_attacker=eval_2_optimal_episode_steps_novice_attacker_means[0:max_iter],
        optimal_steps_stds_emulation_novice_attacker=eval_2_optimal_episode_steps_novice_attacker_stds[0:max_iter],
        avg_rewards_data_simulation_experienced_attacker=avg_train_rewards_data_experienced_attacker[0:max_iter],
        avg_rewards_means_simulation_experienced_attacker=avg_train_rewards_means_experienced_attacker[0:max_iter],
        avg_rewards_stds_simulation_experienced_attacker=avg_train_rewards_stds_experienced_attacker[0:max_iter],
        avg_steps_data_simulation_experienced_attacker=avg_train_steps_data_experienced_attacker[0:max_iter],
        avg_steps_means_simulation_experienced_attacker=avg_train_steps_means_experienced_attacker[0:max_iter],
        avg_steps_stds_simulation_experienced_attacker=avg_train_steps_stds_experienced_attacker[0:max_iter],
        avg_caught_frac_data_simulation_experienced_attacker=avg_train_caught_frac_data_experienced_attacker[0:max_iter],
        avg_caught_frac_means_simulation_experienced_attacker=avg_train_caught_frac_means_experienced_attacker[0:max_iter],
        avg_caught_frac_stds_simulation_experienced_attacker=avg_train_caught_frac_stds_experienced_attacker[0:max_iter],
        avg_early_stopping_frac_data_simulation_experienced_attacker=avg_train_early_stopping_frac_data_experienced_attacker[0:max_iter],
        avg_early_stopping_means_simulation_experienced_attacker=avg_train_early_stopping_means_experienced_attacker[0:max_iter],
        avg_early_stopping_stds_simulation_experienced_attacker=avg_train_early_stopping_stds_experienced_attacker[0:max_iter],
        avg_intrusion_frac_data_simulation_experienced_attacker=avg_train_intrusion_frac_data_experienced_attacker[0:max_iter],
        avg_intrusion_means_simulation_experienced_attacker=avg_train_intrusion_means_experienced_attacker[0:max_iter],
        avg_intrusion_stds_simulation_experienced_attacker=avg_train_intrusion_stds_experienced_attacker[0:max_iter],
        avg_i_steps_data_simulation_experienced_attacker=avg_train_uncaught_intrusion_steps_data_experienced_attacker[0:max_iter],
        avg_i_steps_means_simulation_experienced_attacker=avg_train_uncaught_intrusion_steps_means_experienced_attacker[0:max_iter],
        avg_i_steps_stds_simulation_experienced_attacker=avg_train_uncaught_intrusion_steps_stds_experienced_attacker[0:max_iter],
        optimal_rewards_data_simulation_experienced_attacker=avg_train_optimal_defender_rewards_experienced_attacker_data[0:max_iter],
        optimal_rewards_means_simulation_experienced_attacker=avg_train_optimal_defender_rewards_experienced_attacker_means[0:max_iter],
        optimal_rewards_stds_simulation_experienced_attacker=avg_train_optimal_defender_rewards_experienced_attacker_stds[0:max_iter],
        optimal_steps_data_simulation_experienced_attacker=train_optimal_episode_steps_experienced_attacker_data[0:max_iter],
        optimal_steps_means_simulation_experienced_attacker=train_optimal_episode_steps_experienced_attacker_means[0:max_iter],
        optimal_steps_stds_simulation_experienced_attacker=train_optimal_episode_steps_experienced_attacker_stds[0:max_iter],
        avg_rewards_data_emulation_experienced_attacker=avg_eval_2_rewards_data_experienced_attacker[0:max_iter],
        avg_rewards_means_emulation_experienced_attacker=avg_eval_2_rewards_means_experienced_attacker[0:max_iter],
        avg_rewards_stds_emulation_experienced_attacker=avg_eval_2_rewards_stds_experienced_attacker[0:max_iter],
        avg_steps_data_emulation_experienced_attacker=avg_eval_2_steps_data_experienced_attacker[0:max_iter],
        avg_steps_means_emulation_experienced_attacker=avg_eval_2_steps_means_experienced_attacker[0:max_iter],
        avg_steps_stds_emulation_experienced_attacker=avg_eval_2_steps_stds_experienced_attacker[0:max_iter],
        avg_caught_frac_data_emulation_experienced_attacker=avg_eval_2_caught_frac_data_experienced_attacker[0:max_iter],
        avg_caught_frac_means_emulation_experienced_attacker=avg_eval_2_caught_frac_means_experienced_attacker[0:max_iter],
        avg_caught_frac_stds_emulation_experienced_attacker=avg_eval_2_caught_frac_stds_experienced_attacker[0:max_iter],
        avg_early_stopping_frac_data_emulation_experienced_attacker=avg_eval_2_early_stopping_frac_data_experienced_attacker[0:max_iter],
        avg_early_stopping_means_emulation_experienced_attacker=avg_eval_2_early_stopping_means_experienced_attacker[0:max_iter],
        avg_early_stopping_stds_emulation_experienced_attacker=avg_eval_2_early_stopping_stds_experienced_attacker[0:max_iter],
        avg_intrusion_frac_data_emulation_experienced_attacker=avg_eval_2_intrusion_frac_data_experienced_attacker[0:max_iter],
        avg_intrusion_means_emulation_experienced_attacker=avg_eval_2_intrusion_means_experienced_attacker[0:max_iter],
        avg_intrusion_stds_emulation_experienced_attacker=avg_eval_2_intrusion_stds_experienced_attacker[0:max_iter],
        avg_i_steps_data_emulation_experienced_attacker=avg_eval_2_uncaught_intrusion_steps_data_experienced_attacker[0:max_iter],
        avg_i_steps_means_emulation_experienced_attacker=avg_eval_2_uncaught_intrusion_steps_means_experienced_attacker[0:max_iter],
        avg_i_steps_stds_emulation_experienced_attacker=avg_eval_2_uncaught_intrusion_steps_stds_experienced_attacker[0:max_iter],
        optimal_rewards_data_emulation_experienced_attacker=avg_eval_2_optimal_defender_rewards_experienced_attacker_data[0:max_iter],
        optimal_rewards_means_emulation_experienced_attacker=avg_eval_2_optimal_defender_rewards_experienced_attacker_means[0:max_iter],
        optimal_rewards_stds_emulation_experienced_attacker=avg_eval_2_optimal_defender_rewards_experienced_attacker_stds[0:max_iter],
        optimal_steps_data_emulation_experienced_attacker=eval_2_optimal_episode_steps_experienced_attacker_data[0:max_iter],
        optimal_steps_means_emulation_experienced_attacker=eval_2_optimal_episode_steps_experienced_attacker_means[0:max_iter],
        optimal_steps_stds_emulation_experienced_attacker=eval_2_optimal_episode_steps_experienced_attacker_stds[0:max_iter],

        avg_rewards_data_simulation_expert_attacker=avg_train_rewards_data_expert_attacker[0:max_iter],
        avg_rewards_means_simulation_expert_attacker=avg_train_rewards_means_expert_attacker[0:max_iter],
        avg_rewards_stds_simulation_expert_attacker=avg_train_rewards_stds_expert_attacker[0:max_iter],
        avg_steps_data_simulation_expert_attacker=avg_train_steps_data_expert_attacker[0:max_iter],
        avg_steps_means_simulation_expert_attacker=avg_train_steps_means_expert_attacker[0:max_iter],
        avg_steps_stds_simulation_expert_attacker=avg_train_steps_stds_expert_attacker[0:max_iter],
        avg_caught_frac_data_simulation_expert_attacker=avg_train_caught_frac_data_expert_attacker[0:max_iter],
        avg_caught_frac_means_simulation_expert_attacker=avg_train_caught_frac_means_expert_attacker[0:max_iter],
        avg_caught_frac_stds_simulation_expert_attacker=avg_train_caught_frac_stds_expert_attacker[0:max_iter],
        avg_early_stopping_frac_data_simulation_expert_attacker=avg_train_early_stopping_frac_data_expert_attacker[0:max_iter],
        avg_early_stopping_means_simulation_expert_attacker=avg_train_early_stopping_means_expert_attacker[0:max_iter],
        avg_early_stopping_stds_simulation_expert_attacker=avg_train_early_stopping_stds_expert_attacker[0:max_iter],
        avg_intrusion_frac_data_simulation_expert_attacker=avg_train_intrusion_frac_data_expert_attacker[0:max_iter],
        avg_intrusion_means_simulation_expert_attacker=avg_train_intrusion_means_expert_attacker[0:max_iter],
        avg_intrusion_stds_simulation_expert_attacker=avg_train_intrusion_stds_expert_attacker[0:max_iter],
        avg_i_steps_data_simulation_expert_attacker=avg_train_uncaught_intrusion_steps_data_expert_attacker[0:max_iter],
        avg_i_steps_means_simulation_expert_attacker=avg_train_uncaught_intrusion_steps_means_expert_attacker[0:max_iter],
        avg_i_steps_stds_simulation_expert_attacker=avg_train_uncaught_intrusion_steps_stds_expert_attacker[0:max_iter],
        optimal_rewards_data_simulation_expert_attacker=avg_train_optimal_defender_rewards_expert_attacker_data[0:max_iter],
        optimal_rewards_means_simulation_expert_attacker=avg_train_optimal_defender_rewards_expert_attacker_means[0:max_iter],
        optimal_rewards_stds_simulation_expert_attacker=avg_train_optimal_defender_rewards_expert_attacker_stds[0:max_iter],
        optimal_steps_data_simulation_expert_attacker=train_optimal_episode_steps_expert_attacker_data[0:max_iter],
        optimal_steps_means_simulation_expert_attacker=train_optimal_episode_steps_expert_attacker_means[0:max_iter],
        optimal_steps_stds_simulation_expert_attacker=train_optimal_episode_steps_expert_attacker_stds[0:max_iter],
        avg_rewards_data_emulation_expert_attacker=avg_eval_2_rewards_data_expert_attacker[0:max_iter],
        avg_rewards_means_emulation_expert_attacker=avg_eval_2_rewards_means_expert_attacker[0:max_iter],
        avg_rewards_stds_emulation_expert_attacker=avg_eval_2_rewards_stds_expert_attacker[0:max_iter],
        avg_steps_data_emulation_expert_attacker=avg_eval_2_steps_data_expert_attacker[0:max_iter],
        avg_steps_means_emulation_expert_attacker=avg_eval_2_steps_means_expert_attacker[0:max_iter],
        avg_steps_stds_emulation_expert_attacker=avg_eval_2_steps_stds_expert_attacker[0:max_iter],
        avg_caught_frac_data_emulation_expert_attacker=avg_eval_2_caught_frac_data_expert_attacker[0:max_iter],
        avg_caught_frac_means_emulation_expert_attacker=avg_eval_2_caught_frac_means_expert_attacker[0:max_iter],
        avg_caught_frac_stds_emulation_expert_attacker=avg_eval_2_caught_frac_stds_expert_attacker[0:max_iter],
        avg_early_stopping_frac_data_emulation_expert_attacker=avg_eval_2_early_stopping_frac_data_expert_attacker[0:max_iter],
        avg_early_stopping_means_emulation_expert_attacker=avg_eval_2_early_stopping_means_expert_attacker[0:max_iter],
        avg_early_stopping_stds_emulation_expert_attacker=avg_eval_2_early_stopping_stds_expert_attacker[0:max_iter],
        avg_intrusion_frac_data_emulation_expert_attacker=avg_eval_2_intrusion_frac_data_expert_attacker[0:max_iter],
        avg_intrusion_means_emulation_expert_attacker=avg_eval_2_intrusion_means_expert_attacker[0:max_iter],
        avg_intrusion_stds_emulation_expert_attacker=avg_eval_2_intrusion_stds_expert_attacker[0:max_iter],
        avg_i_steps_data_emulation_expert_attacker=avg_eval_2_uncaught_intrusion_steps_data_expert_attacker[0:max_iter],
        avg_i_steps_means_emulation_expert_attacker=avg_eval_2_uncaught_intrusion_steps_means_expert_attacker[0:max_iter],
        avg_i_steps_stds_emulation_expert_attacker=avg_eval_2_uncaught_intrusion_steps_stds_expert_attacker[0:max_iter],
        optimal_rewards_data_emulation_expert_attacker=avg_eval_2_optimal_defender_rewards_expert_attacker_data[0:max_iter],
        optimal_rewards_means_emulation_expert_attacker=avg_eval_2_optimal_defender_rewards_expert_attacker_means[0:max_iter],
        optimal_rewards_stds_emulation_expert_attacker=avg_eval_2_optimal_defender_rewards_expert_attacker_stds[0:max_iter],
        optimal_steps_data_emulation_expert_attacker=eval_2_optimal_episode_steps_expert_attacker_data[0:max_iter],
        optimal_steps_means_emulation_expert_attacker=eval_2_optimal_episode_steps_expert_attacker_means[0:max_iter],
        optimal_steps_stds_emulation_expert_attacker=train_optimal_episode_steps_expert_attacker_stds[0:max_iter],

        steps_baseline_rewards_data_novice_attacker=train_step_baseline_rewards_data_novice_attacker[0:max_iter],
        steps_baseline_rewards_means_novice_attacker=train_step_baseline_rewards_means_novice_attacker[0:max_iter],
        steps_baseline_rewards_stds_novice_attacker=train_step_baseline_rewards_stds_novice_attacker[0:max_iter],
        steps_baseline_steps_data_novice_attacker=train_step_baseline_steps_data_novice_attacker[0:max_iter],
        steps_baseline_steps_means_novice_attacker=train_step_baseline_steps_means_novice_attacker[0:max_iter],
        steps_baseline_steps_stds_novice_attacker=train_step_baseline_steps_stds_novice_attacker[0:max_iter],
        steps_baseline_early_stopping_data_novice_attacker=train_step_baseline_early_stopping_data_novice_attacker[0:max_iter],
        steps_baseline_early_stopping_means_novice_attacker=train_step_baseline_early_stopping_means_novice_attacker[0:max_iter],
        steps_baseline_early_stopping_stds_novice_attacker=train_step_baseline_early_stopping_stds_novice_attacker[0:max_iter],
        steps_baseline_caught_data_novice_attacker=train_step_baseline_caught_attacker_data_novice_attacker[0:max_iter],
        steps_baseline_caught_means_novice_attacker=train_step_baseline_caught_attacker_means_novice_attacker[0:max_iter],
        steps_baseline_caught_stds_novice_attacker=train_step_baseline_caught_attacker_stds_novice_attacker[0:max_iter],
        steps_baseline_i_steps_data_novice_attacker=train_step_baseline_uncaught_intrusion_steps_data_novice_attacker[0:max_iter],
        steps_baseline_i_steps_means_novice_attacker=train_step_baseline_uncaught_intrusion_steps_means_novice_attacker[0:max_iter],
        steps_baseline_i_steps_stds_novice_attacker=train_step_baseline_uncaught_intrusion_steps_stds_novice_attacker[0:max_iter],

        snort_severe_baseline_rewards_data_novice_attacker=train_snort_severe_baseline_rewards_data_novice_attacker[0:max_iter],
        snort_severe_baseline_rewards_means_novice_attacker=train_snort_severe_baseline_rewards_means_novice_attacker[0:max_iter],
        snort_severe_baseline_rewards_stds_novice_attacker=train_snort_severe_baseline_rewards_stds_novice_attacker[0:max_iter],
        snort_severe_baseline_steps_data_novice_attacker=train_snort_severe_baseline_steps_data_novice_attacker[0:max_iter],
        snort_severe_baseline_steps_means_novice_attacker=train_snort_severe_baseline_steps_means_novice_attacker[0:max_iter],
        snort_severe_baseline_steps_stds_novice_attacker=train_snort_severe_baseline_steps_stds_novice_attacker[0:max_iter],
        snort_severe_baseline_early_stopping_data_novice_attacker=train_snort_severe_baseline_early_stopping_data_novice_attacker[0:max_iter],
        snort_severe_baseline_early_stopping_means_novice_attacker=train_snort_severe_baseline_early_stopping_means_novice_attacker[0:max_iter],
        snort_severe_baseline_early_stopping_stds_novice_attacker=train_snort_severe_baseline_early_stopping_stds_novice_attacker[0:max_iter],
        snort_severe_baseline_caught_data_novice_attacker=train_snort_severe_baseline_caught_attacker_data_novice_attacker[0:max_iter],
        snort_severe_baseline_caught_means_novice_attacker=train_snort_severe_baseline_caught_attacker_means_novice_attacker[0:max_iter],
        snort_severe_baseline_caught_stds_novice_attacker=train_snort_severe_baseline_caught_attacker_stds_novice_attacker[0:max_iter],
        snort_severe_baseline_i_steps_data_novice_attacker=train_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker[0:max_iter],
        snort_severe_baseline_i_steps_means_novice_attacker=train_snort_severe_baseline_uncaught_intrusion_steps_means_novice_attacker[0:max_iter],
        snort_severe_baseline_i_steps_stds_novice_attacker=train_snort_severe_baseline_uncaught_intrusion_steps_stds_novice_attacker[0:max_iter],

        steps_baseline_rewards_data_experienced_attacker=train_step_baseline_rewards_data_experienced_attacker[0:max_iter],
        steps_baseline_rewards_means_experienced_attacker=train_step_baseline_rewards_means_experienced_attacker[0:max_iter],
        steps_baseline_rewards_stds_experienced_attacker=train_step_baseline_rewards_stds_experienced_attacker[0:max_iter],
        steps_baseline_steps_data_experienced_attacker=train_step_baseline_steps_data_experienced_attacker[0:max_iter],
        steps_baseline_steps_means_experienced_attacker=train_step_baseline_steps_means_experienced_attacker[0:max_iter],
        steps_baseline_steps_stds_experienced_attacker=train_step_baseline_steps_stds_experienced_attacker[0:max_iter],
        steps_baseline_early_stopping_data_experienced_attacker=train_step_baseline_early_stopping_data_experienced_attacker[0:max_iter],
        steps_baseline_early_stopping_means_experienced_attacker=train_step_baseline_early_stopping_means_experienced_attacker[0:max_iter],
        steps_baseline_early_stopping_stds_experienced_attacker=train_step_baseline_early_stopping_stds_experienced_attacker[0:max_iter],
        steps_baseline_caught_data_experienced_attacker=train_step_baseline_caught_attacker_data_experienced_attacker[0:max_iter],
        steps_baseline_caught_means_experienced_attacker=train_step_baseline_caught_attacker_means_experienced_attacker[0:max_iter],
        steps_baseline_caught_stds_experienced_attacker=train_step_baseline_caught_attacker_stds_experienced_attacker[0:max_iter],
        steps_baseline_i_steps_data_experienced_attacker=train_step_baseline_uncaught_intrusion_steps_data_experienced_attacker[0:max_iter],
        steps_baseline_i_steps_means_experienced_attacker=train_step_baseline_uncaught_intrusion_steps_means_experienced_attacker[0:max_iter],
        steps_baseline_i_steps_stds_experienced_attacker=train_step_baseline_uncaught_intrusion_steps_stds_experienced_attacker[0:max_iter],

        snort_severe_baseline_rewards_data_experienced_attacker=train_snort_severe_baseline_rewards_data_experienced_attacker[0:max_iter],
        snort_severe_baseline_rewards_means_experienced_attacker=train_snort_severe_baseline_rewards_means_experienced_attacker[0:max_iter],
        snort_severe_baseline_rewards_stds_experienced_attacker=train_snort_severe_baseline_rewards_stds_experienced_attacker[0:max_iter],
        snort_severe_baseline_steps_data_experienced_attacker=train_snort_severe_baseline_steps_data_experienced_attacker[0:max_iter],
        snort_severe_baseline_steps_means_experienced_attacker=train_snort_severe_baseline_steps_means_experienced_attacker[0:max_iter],
        snort_severe_baseline_steps_stds_experienced_attacker=train_snort_severe_baseline_steps_stds_experienced_attacker[0:max_iter],
        snort_severe_baseline_early_stopping_data_experienced_attacker=train_snort_severe_baseline_early_stopping_data_experienced_attacker[0:max_iter],
        snort_severe_baseline_early_stopping_means_experienced_attacker=train_snort_severe_baseline_early_stopping_means_experienced_attacker[0:max_iter],
        snort_severe_baseline_early_stopping_stds_experienced_attacker=train_snort_severe_baseline_early_stopping_stds_experienced_attacker[0:max_iter],
        snort_severe_baseline_caught_data_experienced_attacker=train_snort_severe_baseline_caught_attacker_data_experienced_attacker[0:max_iter],
        snort_severe_baseline_caught_means_experienced_attacker=train_snort_severe_baseline_caught_attacker_means_experienced_attacker[0:max_iter],
        snort_severe_baseline_caught_stds_experienced_attacker=train_snort_severe_baseline_caught_attacker_stds_experienced_attacker[0:max_iter],
        snort_severe_baseline_i_steps_data_experienced_attacker=train_snort_severe_baseline_uncaught_intrusion_steps_data_experienced_attacker[0:max_iter],
        snort_severe_baseline_i_steps_means_experienced_attacker=train_snort_severe_baseline_uncaught_intrusion_steps_means_experienced_attacker[0:max_iter],
        snort_severe_baseline_i_steps_stds_experienced_attacker=train_snort_severe_baseline_uncaught_intrusion_steps_stds_experienced_attacker[0:max_iter],

        steps_baseline_rewards_data_expert_attacker=train_step_baseline_rewards_data_expert_attacker[0:max_iter],
        steps_baseline_rewards_means_expert_attacker=train_step_baseline_rewards_means_expert_attacker[0:max_iter],
        steps_baseline_rewards_stds_expert_attacker=train_step_baseline_rewards_stds_expert_attacker[0:max_iter],
        steps_baseline_steps_data_expert_attacker=train_step_baseline_steps_data_expert_attacker[0:max_iter],
        steps_baseline_steps_means_expert_attacker=train_step_baseline_steps_means_expert_attacker[0:max_iter],
        steps_baseline_steps_stds_expert_attacker=train_step_baseline_steps_stds_expert_attacker[0:max_iter],
        steps_baseline_early_stopping_data_expert_attacker=train_step_baseline_early_stopping_data_expert_attacker[0:max_iter],
        steps_baseline_early_stopping_means_expert_attacker=train_step_baseline_early_stopping_means_expert_attacker[0:max_iter],
        steps_baseline_early_stopping_stds_expert_attacker=train_step_baseline_early_stopping_stds_expert_attacker[0:max_iter],
        steps_baseline_caught_data_expert_attacker=train_step_baseline_caught_attacker_data_expert_attacker[0:max_iter],
        steps_baseline_caught_means_expert_attacker=train_step_baseline_caught_attacker_means_expert_attacker[0:max_iter],
        steps_baseline_caught_stds_expert_attacker=train_step_baseline_caught_attacker_stds_expert_attacker[0:max_iter],
        steps_baseline_i_steps_data_expert_attacker=train_step_baseline_uncaught_intrusion_steps_data_expert_attacker[0:max_iter],
        steps_baseline_i_steps_means_expert_attacker=train_step_baseline_uncaught_intrusion_steps_means_expert_attacker[0:max_iter],
        steps_baseline_i_steps_stds_expert_attacker=train_step_baseline_uncaught_intrusion_steps_stds_expert_attacker[0:max_iter],

        snort_severe_baseline_rewards_data_expert_attacker=train_snort_severe_baseline_rewards_data_expert_attacker[0:max_iter],
        snort_severe_baseline_rewards_means_expert_attacker=train_snort_severe_baseline_rewards_means_expert_attacker[0:max_iter],
        snort_severe_baseline_rewards_stds_expert_attacker=train_snort_severe_baseline_rewards_stds_expert_attacker[0:max_iter],
        snort_severe_baseline_steps_data_expert_attacker=train_snort_severe_baseline_steps_data_expert_attacker[0:max_iter],
        snort_severe_baseline_steps_means_expert_attacker=train_snort_severe_baseline_steps_means_expert_attacker[0:max_iter],
        snort_severe_baseline_steps_stds_expert_attacker=train_snort_severe_baseline_steps_stds_expert_attacker[0:max_iter],
        snort_severe_baseline_early_stopping_data_expert_attacker=train_snort_severe_baseline_early_stopping_data_expert_attacker[0:max_iter],
        snort_severe_baseline_early_stopping_means_expert_attacker=train_snort_severe_baseline_early_stopping_means_expert_attacker[0:max_iter],
        snort_severe_baseline_early_stopping_stds_expert_attacker=train_snort_severe_baseline_early_stopping_stds_expert_attacker[0:max_iter],
        snort_severe_baseline_caught_data_expert_attacker=train_snort_severe_baseline_caught_attacker_data_expert_attacker[0:max_iter],
        snort_severe_baseline_caught_means_expert_attacker=train_snort_severe_baseline_caught_attacker_means_expert_attacker[0:max_iter],
        snort_severe_baseline_caught_stds_expert_attacker=train_snort_severe_baseline_caught_attacker_stds_expert_attacker[0:max_iter],
        snort_severe_baseline_i_steps_data_expert_attacker=train_snort_severe_baseline_uncaught_intrusion_steps_data_expert_attacker[0:max_iter],
        snort_severe_baseline_i_steps_means_expert_attacker=train_snort_severe_baseline_uncaught_intrusion_steps_means_expert_attacker[0:max_iter],
        snort_severe_baseline_i_steps_stds_expert_attacker=train_snort_severe_baseline_uncaught_intrusion_steps_stds_expert_attacker[0:max_iter],

        fontsize= 6.5, figsize= (7.5, 3.25), title_fontsize=8, lw=0.75, wspace=0.19, hspace=0.08, top=0.0,
        bottom=0.11, labelsize=6, markevery=10, optimal_reward = 100, sample_step = 10,
        eval_only=False, plot_opt = False, iterations_per_step= 12000, optimal_int = 1.0,
        optimal_flag = 1.0, file_name = "defender_simulation_emulation_multiple_attackers_multiple_stop_tnsm_21_four_stops", markersize=2.25
    )

    plotting_util_defender.plot_defender_emulation_with_baselines_tnsm_21_four_stops(
        avg_rewards_data_emulation_novice_attacker=avg_eval_2_rewards_data_novice_attacker[0:max_iter],
        avg_rewards_means_emulation_novice_attacker=avg_eval_2_rewards_means_novice_attacker[0:max_iter],
        avg_rewards_stds_emulation_novice_attacker=avg_eval_2_rewards_stds_novice_attacker[0:max_iter],
        avg_steps_data_emulation_novice_attacker=avg_eval_2_steps_data_novice_attacker[0:max_iter],
        avg_steps_means_emulation_novice_attacker=avg_eval_2_steps_means_novice_attacker[0:max_iter],
        avg_steps_stds_emulation_novice_attacker=avg_eval_2_steps_stds_novice_attacker[0:max_iter],
        avg_caught_frac_data_emulation_novice_attacker=avg_eval_2_caught_frac_data_novice_attacker[0:max_iter],
        avg_caught_frac_means_emulation_novice_attacker=avg_eval_2_caught_frac_means_novice_attacker[0:max_iter],
        avg_caught_frac_stds_emulation_novice_attacker=avg_eval_2_caught_frac_stds_novice_attacker[0:max_iter],
        avg_early_stopping_frac_data_emulation_novice_attacker=avg_eval_2_early_stopping_frac_data_novice_attacker[0:max_iter],
        avg_early_stopping_means_emulation_novice_attacker=avg_eval_2_early_stopping_means_novice_attacker[0:max_iter],
        avg_early_stopping_stds_emulation_novice_attacker=avg_eval_2_early_stopping_stds_novice_attacker[0:max_iter],
        avg_intrusion_frac_data_emulation_novice_attacker=avg_eval_2_intrusion_frac_data_novice_attacker[0:max_iter],
        avg_intrusion_means_emulation_novice_attacker=avg_eval_2_intrusion_means_novice_attacker[0:max_iter],
        avg_intrusion_stds_emulation_novice_attacker=avg_eval_2_intrusion_stds_novice_attacker[0:max_iter],
        avg_i_steps_data_emulation_novice_attacker=avg_eval_2_uncaught_intrusion_steps_data_novice_attacker[0:max_iter],
        avg_i_steps_means_emulation_novice_attacker=avg_eval_2_uncaught_intrusion_steps_means_novice_attacker[0:max_iter],
        avg_i_steps_stds_emulation_novice_attacker=avg_eval_2_uncaught_intrusion_steps_stds_novice_attacker[0:max_iter],

        avg_rewards_data_emulation_experienced_attacker=avg_eval_2_rewards_data_experienced_attacker[0:max_iter],
        avg_rewards_means_emulation_experienced_attacker=avg_eval_2_rewards_means_experienced_attacker[0:max_iter],
        avg_rewards_stds_emulation_experienced_attacker=avg_eval_2_rewards_stds_experienced_attacker[0:max_iter],
        avg_steps_data_emulation_experienced_attacker=avg_eval_2_steps_data_experienced_attacker[0:max_iter],
        avg_steps_means_emulation_experienced_attacker=avg_eval_2_steps_means_experienced_attacker[0:max_iter],
        avg_steps_stds_emulation_experienced_attacker=avg_eval_2_steps_stds_experienced_attacker[0:max_iter],
        avg_caught_frac_data_emulation_experienced_attacker=avg_eval_2_caught_frac_data_experienced_attacker[0:max_iter],
        avg_caught_frac_means_emulation_experienced_attacker=avg_eval_2_caught_frac_means_experienced_attacker[0:max_iter],
        avg_caught_frac_stds_emulation_experienced_attacker=avg_eval_2_caught_frac_stds_experienced_attacker[0:max_iter],
        avg_early_stopping_frac_data_emulation_experienced_attacker=avg_eval_2_early_stopping_frac_data_experienced_attacker[0:max_iter],
        avg_early_stopping_means_emulation_experienced_attacker=avg_eval_2_early_stopping_means_experienced_attacker[0:max_iter],
        avg_early_stopping_stds_emulation_experienced_attacker=avg_eval_2_early_stopping_stds_experienced_attacker[0:max_iter],
        avg_intrusion_frac_data_emulation_experienced_attacker=avg_eval_2_intrusion_frac_data_experienced_attacker[0:max_iter],
        avg_intrusion_means_emulation_experienced_attacker=avg_eval_2_intrusion_means_experienced_attacker[0:max_iter],
        avg_intrusion_stds_emulation_experienced_attacker=avg_eval_2_intrusion_stds_experienced_attacker[0:max_iter],
        avg_i_steps_data_emulation_experienced_attacker=avg_eval_2_uncaught_intrusion_steps_data_experienced_attacker[0:max_iter],
        avg_i_steps_means_emulation_experienced_attacker=avg_eval_2_uncaught_intrusion_steps_means_experienced_attacker[0:max_iter],
        avg_i_steps_stds_emulation_experienced_attacker=avg_eval_2_uncaught_intrusion_steps_stds_experienced_attacker[0:max_iter],

        avg_rewards_data_emulation_expert_attacker=avg_eval_2_rewards_data_expert_attacker[0:max_iter],
        avg_rewards_means_emulation_expert_attacker=avg_eval_2_rewards_means_expert_attacker[0:max_iter],
        avg_rewards_stds_emulation_expert_attacker=avg_eval_2_rewards_stds_expert_attacker[0:max_iter],
        avg_steps_data_emulation_expert_attacker=avg_eval_2_steps_data_expert_attacker[0:max_iter],
        avg_steps_means_emulation_expert_attacker=avg_eval_2_steps_means_expert_attacker[0:max_iter],
        avg_steps_stds_emulation_expert_attacker=avg_eval_2_steps_stds_expert_attacker[0:max_iter],
        avg_caught_frac_data_emulation_expert_attacker=avg_eval_2_caught_frac_data_expert_attacker[0:max_iter],
        avg_caught_frac_means_emulation_expert_attacker=avg_eval_2_caught_frac_means_expert_attacker[0:max_iter],
        avg_caught_frac_stds_emulation_expert_attacker=avg_eval_2_caught_frac_stds_expert_attacker[0:max_iter],
        avg_early_stopping_frac_data_emulation_expert_attacker=avg_eval_2_early_stopping_frac_data_expert_attacker[0:max_iter],
        avg_early_stopping_means_emulation_expert_attacker=avg_eval_2_early_stopping_means_expert_attacker[0:max_iter],
        avg_early_stopping_stds_emulation_expert_attacker=avg_eval_2_early_stopping_stds_expert_attacker[0:max_iter],
        avg_intrusion_frac_data_emulation_expert_attacker=avg_eval_2_intrusion_frac_data_expert_attacker[0:max_iter],
        avg_intrusion_means_emulation_expert_attacker=avg_eval_2_intrusion_means_expert_attacker[0:max_iter],
        avg_intrusion_stds_emulation_expert_attacker=avg_eval_2_intrusion_stds_expert_attacker[0:max_iter],
        avg_i_steps_data_emulation_expert_attacker=avg_eval_2_uncaught_intrusion_steps_data_expert_attacker[0:max_iter],
        avg_i_steps_means_emulation_expert_attacker=avg_eval_2_uncaught_intrusion_steps_means_expert_attacker[0:max_iter],
        avg_i_steps_stds_emulation_expert_attacker=avg_eval_2_uncaught_intrusion_steps_stds_expert_attacker[0:max_iter],

        optimal_rewards_data_emulation=avg_eval_2_optimal_defender_rewards_novice_attacker_data[0:max_iter],
        optimal_rewards_means_emulation=avg_eval_2_optimal_defender_rewards_novice_attacker_means[0:max_iter],
        optimal_rewards_stds_emulation=avg_eval_2_optimal_defender_rewards_novice_attacker_stds[0:max_iter],
        optimal_steps_data_emulation=eval_2_optimal_episode_steps_novice_attacker_data[0:max_iter],
        optimal_steps_means_emulation=eval_2_optimal_episode_steps_novice_attacker_means[0:max_iter],
        optimal_steps_stds_emulation=eval_2_optimal_episode_steps_novice_attacker_stds[0:max_iter],

        steps_baseline_rewards_data=eval_2_step_baseline_rewards_data_novice_attacker[0:max_iter],
        steps_baseline_rewards_means=eval_2_step_baseline_rewards_means_novice_attacker[0:max_iter],
        steps_baseline_rewards_stds=eval_2_step_baseline_rewards_stds_novice_attacker[0:max_iter],
        steps_baseline_steps_data=eval_2_step_baseline_steps_data_novice_attacker[0:max_iter],
        steps_baseline_steps_means=eval_2_step_baseline_steps_means_novice_attacker[0:max_iter],
        steps_baseline_steps_stds=eval_2_step_baseline_steps_stds_novice_attacker[0:max_iter],
        steps_baseline_early_stopping_data=eval_2_step_baseline_early_stopping_data_novice_attacker[0:max_iter],
        steps_baseline_early_stopping_means=eval_2_step_baseline_early_stopping_means_novice_attacker[0:max_iter],
        steps_baseline_early_stopping_stds=eval_2_step_baseline_early_stopping_stds_novice_attacker[0:max_iter],
        steps_baseline_caught_data=eval_2_step_baseline_caught_attacker_data_novice_attacker[0:max_iter],
        steps_baseline_caught_means=eval_2_step_baseline_caught_attacker_means_novice_attacker[0:max_iter],
        steps_baseline_caught_stds=eval_2_step_baseline_caught_attacker_stds_novice_attacker[0:max_iter],
        steps_baseline_i_steps_data=eval_2_step_baseline_uncaught_intrusion_steps_data_novice_attacker[0:max_iter],
        steps_baseline_i_steps_means=eval_2_step_baseline_uncaught_intrusion_steps_means_novice_attacker[0:max_iter],
        steps_baseline_i_steps_stds=eval_2_step_baseline_uncaught_intrusion_steps_stds_novice_attacker[0:max_iter],

        snort_severe_baseline_rewards_data=eval_2_snort_severe_baseline_rewards_data_novice_attacker[0:max_iter],
        snort_severe_baseline_rewards_means=eval_2_snort_severe_baseline_rewards_means_novice_attacker[0:max_iter],
        snort_severe_baseline_rewards_stds=eval_2_snort_severe_baseline_rewards_stds_novice_attacker[0:max_iter],
        snort_severe_baseline_steps_data=eval_2_snort_severe_baseline_steps_data_novice_attacker[0:max_iter],
        snort_severe_baseline_steps_means=eval_2_snort_severe_baseline_steps_means_novice_attacker[0:max_iter],
        snort_severe_baseline_steps_stds=eval_2_snort_severe_baseline_steps_stds_novice_attacker[0:max_iter],
        snort_severe_baseline_early_stopping_data=eval_2_snort_severe_baseline_early_stopping_data_novice_attacker[0:max_iter],
        snort_severe_baseline_early_stopping_means=eval_2_snort_severe_baseline_early_stopping_means_novice_attacker[0:max_iter],
        snort_severe_baseline_early_stopping_stds=eval_2_snort_severe_baseline_early_stopping_stds_novice_attacker[0:max_iter],
        snort_severe_baseline_caught_data=eval_2_snort_severe_baseline_caught_attacker_data_novice_attacker[0:max_iter],
        snort_severe_baseline_caught_means=eval_2_snort_severe_baseline_caught_attacker_means_novice_attacker[0:max_iter],
        snort_severe_baseline_caught_stds=eval_2_snort_severe_baseline_caught_attacker_stds_novice_attacker[0:max_iter],
        snort_severe_baseline_i_steps_data=eval_2_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker[0:max_iter],
        snort_severe_baseline_i_steps_means=eval_2_snort_severe_baseline_uncaught_intrusion_steps_means_novice_attacker[0:max_iter],
        snort_severe_baseline_i_steps_stds=eval_2_snort_severe_baseline_uncaught_intrusion_steps_stds_novice_attacker[0:max_iter],

        fontsize=6.5, figsize=(7.5, 1.5), title_fontsize=8, lw=0.75, wspace=0.17, hspace=0.4, top=0.0,
        bottom=0.28, labelsize=6, markevery=10, optimal_reward=100, sample_step=10,
        eval_only=False, plot_opt=False, iterations_per_step=12000, optimal_int=1.0,
        optimal_flag=1.0, file_name="defender_emulation_multiple_attackers_w_baselines_multiple_stop_tnsm_21_four_stops", markersize=2.25
    )

    plotting_util_defender.plot_defender_simulation_emulation_steps_dist_tnsm_21_multiple_attackers_four_stops(
        avg_first_stop_step_data_simulation_novice_attacker=train_defender_first_stop_step_novice_attacker_data[0:max_iter],
        avg_first_stop_step_means_simulation_novice_attacker=train_defender_first_stop_step_novice_attacker_means[0:max_iter],
        avg_first_stop_step_stds_simulation_novice_attacker=train_defender_first_stop_step_novice_attacker_stds[0:max_iter],
        avg_second_stop_step_data_simulation_novice_attacker=train_defender_second_stop_step_novice_attacker_data[0:max_iter],
        avg_second_stop_step_means_simulation_novice_attacker=train_defender_second_stop_step_novice_attacker_means[0:max_iter],
        avg_second_stop_step_stds_simulation_novice_attacker=train_defender_second_stop_step_novice_attacker_stds[0:max_iter],
        avg_third_stop_step_data_simulation_novice_attacker=train_defender_third_stop_step_novice_attacker_data[0:max_iter],
        avg_third_stop_step_means_simulation_novice_attacker=train_defender_third_stop_step_novice_attacker_means[0:max_iter],
        avg_third_stop_step_stds_simulation_novice_attacker=train_defender_third_stop_step_novice_attacker_stds[0:max_iter],
        avg_fourth_stop_step_data_simulation_novice_attacker=train_defender_fourth_stop_step_novice_attacker_data[0:max_iter],
        avg_fourth_stop_step_means_simulation_novice_attacker=train_defender_fourth_stop_step_novice_attacker_means[0:max_iter],
        avg_fourth_stop_step_stds_simulation_novice_attacker=train_defender_fourth_stop_step_novice_attacker_stds[0:max_iter],
        avg_stops_remaining_data_simulation_novice_attacker=train_defender_stops_remaining_novice_attacker_data[0:max_iter],
        avg_stops_remaining_means_simulation_novice_attacker=train_defender_stops_remaining_novice_attacker_means[0:max_iter],
        avg_stops_remaining_stds_simulation_novice_attacker=train_defender_stops_remaining_novice_attacker_stds[0:max_iter],
        optimal_first_stop_step_data_simulation_novice_attacker=train_optimal_first_stop_step_novice_attacker_data[0:max_iter],
        optimal_first_stop_step_means_simulation_novice_attacker=train_optimal_first_stop_step_novice_attacker_means[0:max_iter],
        optimal_first_stop_step_stds_simulation_novice_attacker=train_optimal_first_stop_step_novice_attacker_stds[0:max_iter],
        optimal_second_stop_step_data_simulation_novice_attacker=train_optimal_second_stop_step_novice_attacker_data[0:max_iter],
        optimal_second_stop_step_means_simulation_novice_attacker=train_optimal_second_stop_step_novice_attacker_means[0:max_iter],
        optimal_second_stop_step_stds_simulation_novice_attacker=train_optimal_second_stop_step_novice_attacker_stds[0:max_iter],
        optimal_third_stop_step_data_simulation_novice_attacker=train_optimal_third_stop_step_novice_attacker_data[0:max_iter],
        optimal_third_stop_step_means_simulation_novice_attacker=train_optimal_third_stop_step_novice_attacker_means[0:max_iter],
        optimal_third_stop_step_stds_simulation_novice_attacker=train_optimal_third_stop_step_novice_attacker_stds[0:max_iter],
        optimal_fourth_stop_step_data_simulation_novice_attacker=train_optimal_fourth_stop_step_novice_attacker_data[0:max_iter],
        optimal_fourth_stop_step_means_simulation_novice_attacker=train_optimal_fourth_stop_step_novice_attacker_means[0:max_iter],
        optimal_fourth_stop_step_stds_simulation_novice_attacker=train_optimal_fourth_stop_step_novice_attacker_stds[0:max_iter],
        optimal_stops_remaining_data_simulation_novice_attacker=train_optimal_stops_remaining_novice_attacker_data[0:max_iter],
        optimal_stops_remaining_means_simulation_novice_attacker=train_optimal_stops_remaining_novice_attacker_means[0:max_iter],
        optimal_stops_remaining_stds_simulation_novice_attacker=train_optimal_stops_remaining_novice_attacker_stds[0:max_iter],
        avg_first_stop_step_data_emulation_novice_attacker=train_defender_first_stop_step_novice_attacker_data[0:max_iter],
        avg_first_stop_step_means_emulation_novice_attacker=train_defender_first_stop_step_novice_attacker_means[0:max_iter],
        avg_first_stop_step_stds_emulation_novice_attacker=train_defender_first_stop_step_novice_attacker_stds[0:max_iter],
        avg_second_stop_step_data_emulation_novice_attacker=eval_2_defender_second_stop_step_novice_attacker_data[0:max_iter],
        avg_second_stop_step_means_emulation_novice_attacker=eval_2_defender_second_stop_step_novice_attacker_means[0:max_iter],
        avg_second_stop_step_stds_emulation_novice_attacker=eval_2_defender_second_stop_step_novice_attacker_stds[0:max_iter],
        avg_third_stop_step_data_emulation_novice_attacker=eval_2_defender_third_stop_step_novice_attacker_data[0:max_iter],
        avg_third_stop_step_means_emulation_novice_attacker=eval_2_defender_third_stop_step_novice_attacker_means[0:max_iter],
        avg_third_stop_step_stds_emulation_novice_attacker=eval_2_defender_third_stop_step_novice_attacker_stds[0:max_iter],
        avg_fourth_stop_step_data_emulation_novice_attacker=eval_2_defender_fourth_stop_step_novice_attacker_data[0:max_iter],
        avg_fourth_stop_step_means_emulation_novice_attacker=eval_2_defender_fourth_stop_step_novice_attacker_means[0:max_iter],
        avg_fourth_stop_step_stds_emulation_novice_attacker=eval_2_defender_fourth_stop_step_novice_attacker_stds[0:max_iter],
        avg_stops_remaining_data_emulation_novice_attacker=eval_2_defender_stops_remaining_novice_attacker_data[0:max_iter],
        avg_stops_remaining_means_emulation_novice_attacker=eval_2_defender_stops_remaining_novice_attacker_means[0:max_iter],
        avg_stops_remaining_stds_emulation_novice_attacker=eval_2_defender_stops_remaining_novice_attacker_stds[0:max_iter],
        optimal_first_stop_step_data_emulation_novice_attacker=eval_2_optimal_first_stop_step_novice_attacker_data[0:max_iter],
        optimal_first_stop_step_means_emulation_novice_attacker=eval_2_optimal_first_stop_step_novice_attacker_means[0:max_iter],
        optimal_first_stop_step_stds_emulation_novice_attacker=eval_2_optimal_first_stop_step_novice_attacker_stds[0:max_iter],
        optimal_second_stop_step_data_emulation_novice_attacker=eval_2_optimal_second_stop_step_novice_attacker_data[0:max_iter],
        optimal_second_stop_step_means_emulation_novice_attacker=eval_2_optimal_second_stop_step_novice_attacker_means[0:max_iter],
        optimal_second_stop_step_stds_emulation_novice_attacker=eval_2_optimal_second_stop_step_novice_attacker_stds[0:max_iter],
        optimal_third_stop_step_data_emulation_novice_attacker=eval_2_optimal_third_stop_step_novice_attacker_data[0:max_iter],
        optimal_third_stop_step_means_emulation_novice_attacker=eval_2_optimal_third_stop_step_novice_attacker_means[0:max_iter],
        optimal_third_stop_step_stds_emulation_novice_attacker=eval_2_optimal_third_stop_step_novice_attacker_stds[0:max_iter],
        optimal_fourth_stop_step_data_emulation_novice_attacker=eval_2_optimal_fourth_stop_step_novice_attacker_data[0:max_iter],
        optimal_fourth_stop_step_means_emulation_novice_attacker=eval_2_optimal_fourth_stop_step_novice_attacker_means[0:max_iter],
        optimal_fourth_stop_step_stds_emulation_novice_attacker=eval_2_optimal_fourth_stop_step_novice_attacker_stds[0:max_iter],
        optimal_stops_remaining_data_emulation_novice_attacker=eval_2_optimal_stops_remaining_novice_attacker_data[0:max_iter],
        optimal_stops_remaining_means_emulation_novice_attacker=eval_2_optimal_stops_remaining_novice_attacker_means[0:max_iter],
        optimal_stops_remaining_stds_emulation_novice_attacker=eval_2_optimal_stops_remaining_novice_attacker_stds[0:max_iter],
        avg_first_stop_step_data_simulation_experienced_attacker=train_defender_first_stop_step_experienced_attacker_data[0:max_iter],
        avg_first_stop_step_means_simulation_experienced_attacker=train_defender_first_stop_step_experienced_attacker_means[0:max_iter],
        avg_first_stop_step_stds_simulation_experienced_attacker=train_defender_first_stop_step_experienced_attacker_stds[0:max_iter],
        avg_second_stop_step_data_simulation_experienced_attacker=train_defender_second_stop_step_experienced_attacker_data[0:max_iter],
        avg_second_stop_step_means_simulation_experienced_attacker=train_defender_second_stop_step_experienced_attacker_means[0:max_iter],
        avg_second_stop_step_stds_simulation_experienced_attacker=train_defender_second_stop_step_experienced_attacker_stds[0:max_iter],
        avg_third_stop_step_data_simulation_experienced_attacker=train_defender_third_stop_step_experienced_attacker_data[0:max_iter],
        avg_third_stop_step_means_simulation_experienced_attacker=train_defender_third_stop_step_experienced_attacker_means[0:max_iter],
        avg_third_stop_step_stds_simulation_experienced_attacker=train_defender_third_stop_step_experienced_attacker_stds[0:max_iter],
        avg_fourth_stop_step_data_simulation_experienced_attacker=train_defender_fourth_stop_step_experienced_attacker_data[0:max_iter],
        avg_fourth_stop_step_means_simulation_experienced_attacker=train_defender_fourth_stop_step_experienced_attacker_means[0:max_iter],
        avg_fourth_stop_step_stds_simulation_experienced_attacker=train_defender_fourth_stop_step_experienced_attacker_stds[0:max_iter],
        avg_stops_remaining_data_simulation_experienced_attacker=train_defender_stops_remaining_experienced_attacker_data[0:max_iter],
        avg_stops_remaining_means_simulation_experienced_attacker=train_defender_stops_remaining_experienced_attacker_means[0:max_iter],
        avg_stops_remaining_stds_simulation_experienced_attacker=train_defender_stops_remaining_experienced_attacker_stds[0:max_iter],
        optimal_first_stop_step_data_simulation_experienced_attacker=train_optimal_first_stop_step_experienced_attacker_data[0:max_iter],
        optimal_first_stop_step_means_simulation_experienced_attacker=train_optimal_first_stop_step_experienced_attacker_means[0:max_iter],
        optimal_first_stop_step_stds_simulation_experienced_attacker=train_optimal_first_stop_step_experienced_attacker_stds[0:max_iter],
        optimal_second_stop_step_data_simulation_experienced_attacker=train_optimal_second_stop_step_experienced_attacker_data[0:max_iter],
        optimal_second_stop_step_means_simulation_experienced_attacker=train_optimal_second_stop_step_experienced_attacker_means[0:max_iter],
        optimal_second_stop_step_stds_simulation_experienced_attacker=train_optimal_second_stop_step_experienced_attacker_stds[0:max_iter],
        optimal_third_stop_step_data_simulation_experienced_attacker=train_optimal_third_stop_step_experienced_attacker_data[0:max_iter],
        optimal_third_stop_step_means_simulation_experienced_attacker=train_optimal_third_stop_step_experienced_attacker_means[0:max_iter],
        optimal_third_stop_step_stds_simulation_experienced_attacker=train_optimal_third_stop_step_experienced_attacker_stds[0:max_iter],
        optimal_fourth_stop_step_data_simulation_experienced_attacker=train_optimal_fourth_stop_step_experienced_attacker_data[0:max_iter],
        optimal_fourth_stop_step_means_simulation_experienced_attacker=train_optimal_fourth_stop_step_experienced_attacker_means[0:max_iter],
        optimal_fourth_stop_step_stds_simulation_experienced_attacker=train_optimal_fourth_stop_step_experienced_attacker_stds[0:max_iter],
        optimal_stops_remaining_data_simulation_experienced_attacker=train_optimal_stops_remaining_experienced_attacker_data[0:max_iter],
        optimal_stops_remaining_means_simulation_experienced_attacker=train_optimal_stops_remaining_experienced_attacker_means[0:max_iter],
        optimal_stops_remaining_stds_simulation_experienced_attacker=train_optimal_stops_remaining_experienced_attacker_stds[0:max_iter],
        avg_first_stop_step_data_emulation_experienced_attacker=eval_2_defender_first_stop_step_experienced_attacker_data[0:max_iter],
        avg_first_stop_step_means_emulation_experienced_attacker=eval_2_defender_first_stop_step_experienced_attacker_means[0:max_iter],
        avg_first_stop_step_stds_emulation_experienced_attacker=eval_2_defender_first_stop_step_experienced_attacker_stds[0:max_iter],
        avg_second_stop_step_data_emulation_experienced_attacker=eval_2_defender_second_stop_step_experienced_attacker_data[0:max_iter],
        avg_second_stop_step_means_emulation_experienced_attacker=eval_2_defender_second_stop_step_experienced_attacker_means[0:max_iter],
        avg_second_stop_step_stds_emulation_experienced_attacker=eval_2_defender_second_stop_step_experienced_attacker_stds[0:max_iter],
        avg_third_stop_step_data_emulation_experienced_attacker=eval_2_defender_third_stop_step_experienced_attacker_data[0:max_iter],
        avg_third_stop_step_means_emulation_experienced_attacker=eval_2_defender_third_stop_step_experienced_attacker_means[0:max_iter],
        avg_third_stop_step_stds_emulation_experienced_attacker=eval_2_defender_third_stop_step_experienced_attacker_stds[0:max_iter],
        avg_fourth_stop_step_data_emulation_experienced_attacker=eval_2_defender_fourth_stop_step_experienced_attacker_data[0:max_iter],
        avg_fourth_stop_step_means_emulation_experienced_attacker=eval_2_defender_fourth_stop_step_experienced_attacker_means[0:max_iter],
        avg_fourth_stop_step_stds_emulation_experienced_attacker=eval_2_defender_fourth_stop_step_experienced_attacker_stds[0:max_iter],
        avg_stops_remaining_data_emulation_experienced_attacker=eval_2_defender_stops_remaining_experienced_attacker_data[0:max_iter],
        avg_stops_remaining_means_emulation_experienced_attacker=eval_2_defender_stops_remaining_experienced_attacker_means[0:max_iter],
        avg_stops_remaining_stds_emulation_experienced_attacker=eval_2_defender_stops_remaining_experienced_attacker_stds[0:max_iter],
        optimal_first_stop_step_data_emulation_experienced_attacker=eval_2_optimal_first_stop_step_experienced_attacker_data[0:max_iter],
        optimal_first_stop_step_means_emulation_experienced_attacker=eval_2_optimal_first_stop_step_experienced_attacker_means[0:max_iter],
        optimal_first_stop_step_stds_emulation_experienced_attacker=eval_2_optimal_first_stop_step_experienced_attacker_stds[0:max_iter],
        optimal_second_stop_step_data_emulation_experienced_attacker=eval_2_optimal_second_stop_step_experienced_attacker_data[0:max_iter],
        optimal_second_stop_step_means_emulation_experienced_attacker=eval_2_optimal_second_stop_step_experienced_attacker_means[0:max_iter],
        optimal_second_stop_step_stds_emulation_experienced_attacker=eval_2_optimal_second_stop_step_experienced_attacker_stds[0:max_iter],
        optimal_third_stop_step_data_emulation_experienced_attacker=eval_2_optimal_third_stop_step_experienced_attacker_data[0:max_iter],
        optimal_third_stop_step_means_emulation_experienced_attacker=eval_2_optimal_third_stop_step_experienced_attacker_means[0:max_iter],
        optimal_third_stop_step_stds_emulation_experienced_attacker=eval_2_optimal_third_stop_step_experienced_attacker_stds[0:max_iter],
        optimal_fourth_stop_step_data_emulation_experienced_attacker=eval_2_optimal_fourth_stop_step_experienced_attacker_data[0:max_iter],
        optimal_fourth_stop_step_means_emulation_experienced_attacker=eval_2_optimal_fourth_stop_step_experienced_attacker_means[0:max_iter],
        optimal_fourth_stop_step_stds_emulation_experienced_attacker=eval_2_optimal_fourth_stop_step_experienced_attacker_stds[0:max_iter],
        optimal_stops_remaining_data_emulation_experienced_attacker=eval_2_optimal_stops_remaining_experienced_attacker_data[0:max_iter],
        optimal_stops_remaining_means_emulation_experienced_attacker=eval_2_optimal_stops_remaining_experienced_attacker_means[0:max_iter],
        optimal_stops_remaining_stds_emulation_experienced_attacker=eval_2_optimal_stops_remaining_experienced_attacker_stds[0:max_iter],
        avg_first_stop_step_data_simulation_expert_attacker=train_defender_first_stop_step_expert_attacker_data[0:max_iter],
        avg_first_stop_step_means_simulation_expert_attacker=train_defender_first_stop_step_expert_attacker_means[0:max_iter],
        avg_first_stop_step_stds_simulation_expert_attacker=train_defender_first_stop_step_expert_attacker_stds[0:max_iter],
        avg_second_stop_step_data_simulation_expert_attacker=train_defender_second_stop_step_expert_attacker_data[0:max_iter],
        avg_second_stop_step_means_simulation_expert_attacker=train_defender_second_stop_step_expert_attacker_means[0:max_iter],
        avg_second_stop_step_stds_simulation_expert_attacker=train_defender_second_stop_step_expert_attacker_stds[0:max_iter],
        avg_third_stop_step_data_simulation_expert_attacker=train_defender_third_stop_step_expert_attacker_data[0:max_iter],
        avg_third_stop_step_means_simulation_expert_attacker=train_defender_third_stop_step_expert_attacker_means[0:max_iter],
        avg_third_stop_step_stds_simulation_expert_attacker=train_defender_third_stop_step_expert_attacker_stds[0:max_iter],
        avg_fourth_stop_step_data_simulation_expert_attacker=train_defender_fourth_stop_step_expert_attacker_data[0:max_iter],
        avg_fourth_stop_step_means_simulation_expert_attacker=train_defender_fourth_stop_step_expert_attacker_means[0:max_iter],
        avg_fourth_stop_step_stds_simulation_expert_attacker=train_defender_fourth_stop_step_expert_attacker_stds[0:max_iter],
        avg_stops_remaining_data_simulation_expert_attacker=train_defender_stops_remaining_expert_attacker_data[0:max_iter],
        avg_stops_remaining_means_simulation_expert_attacker=train_defender_stops_remaining_expert_attacker_means[0:max_iter],
        avg_stops_remaining_stds_simulation_expert_attacker=train_defender_stops_remaining_expert_attacker_stds[0:max_iter],
        optimal_first_stop_step_data_simulation_expert_attacker=train_optimal_first_stop_step_expert_attacker_data[0:max_iter],
        optimal_first_stop_step_means_simulation_expert_attacker=train_optimal_first_stop_step_expert_attacker_means[0:max_iter],
        optimal_first_stop_step_stds_simulation_expert_attacker=train_optimal_first_stop_step_expert_attacker_stds[0:max_iter],
        optimal_second_stop_step_data_simulation_expert_attacker=train_optimal_second_stop_step_expert_attacker_data[0:max_iter],
        optimal_second_stop_step_means_simulation_expert_attacker=train_optimal_second_stop_step_expert_attacker_means[0:max_iter],
        optimal_second_stop_step_stds_simulation_expert_attacker=train_optimal_second_stop_step_expert_attacker_stds[0:max_iter],
        optimal_third_stop_step_data_simulation_expert_attacker=train_optimal_third_stop_step_expert_attacker_data[0:max_iter],
        optimal_third_stop_step_means_simulation_expert_attacker=train_optimal_third_stop_step_expert_attacker_means[0:max_iter],
        optimal_third_stop_step_stds_simulation_expert_attacker=train_optimal_third_stop_step_expert_attacker_stds[0:max_iter],
        optimal_fourth_stop_step_data_simulation_expert_attacker=train_optimal_fourth_stop_step_expert_attacker_data[0:max_iter],
        optimal_fourth_stop_step_means_simulation_expert_attacker=train_optimal_fourth_stop_step_expert_attacker_means[0:max_iter],
        optimal_fourth_stop_step_stds_simulation_expert_attacker=train_optimal_fourth_stop_step_expert_attacker_stds[0:max_iter],
        optimal_stops_remaining_data_simulation_expert_attacker=train_optimal_stops_remaining_expert_attacker_data[0:max_iter],
        optimal_stops_remaining_means_simulation_expert_attacker=train_optimal_stops_remaining_expert_attacker_means[0:max_iter],
        optimal_stops_remaining_stds_simulation_expert_attacker=train_optimal_stops_remaining_expert_attacker_stds[0:max_iter],
        avg_first_stop_step_data_emulation_expert_attacker=eval_2_defender_first_stop_step_expert_attacker_data[0:max_iter],
        avg_first_stop_step_means_emulation_expert_attacker=eval_2_defender_first_stop_step_expert_attacker_means[0:max_iter],
        avg_first_stop_step_stds_emulation_expert_attacker=eval_2_defender_first_stop_step_expert_attacker_stds[0:max_iter],
        avg_second_stop_step_data_emulation_expert_attacker=eval_2_defender_second_stop_step_experienced_attacker_data[0:max_iter],
        avg_second_stop_step_means_emulation_expert_attacker=eval_2_defender_second_stop_step_experienced_attacker_means[0:max_iter],
        avg_second_stop_step_stds_emulation_expert_attacker=eval_2_defender_second_stop_step_experienced_attacker_stds[0:max_iter],
        avg_third_stop_step_data_emulation_expert_attacker=eval_2_defender_third_stop_step_expert_attacker_data[0:max_iter],
        avg_third_stop_step_means_emulation_expert_attacker=eval_2_defender_third_stop_step_expert_attacker_means[0:max_iter],
        avg_third_stop_step_stds_emulation_expert_attacker=eval_2_defender_third_stop_step_expert_attacker_stds[0:max_iter],
        avg_fourth_stop_step_data_emulation_expert_attacker=eval_2_defender_fourth_stop_step_expert_attacker_data[0:max_iter],
        avg_fourth_stop_step_means_emulation_expert_attacker=eval_2_defender_fourth_stop_step_expert_attacker_means[0:max_iter],
        avg_fourth_stop_step_stds_emulation_expert_attacker=eval_2_defender_fourth_stop_step_expert_attacker_stds[0:max_iter],
        avg_stops_remaining_data_emulation_expert_attacker=eval_2_defender_stops_remaining_expert_attacker_data[0:max_iter],
        avg_stops_remaining_means_emulation_expert_attacker=eval_2_defender_stops_remaining_expert_attacker_means[0:max_iter],
        avg_stops_remaining_stds_emulation_expert_attacker=eval_2_defender_stops_remaining_expert_attacker_stds[0:max_iter],
        optimal_first_stop_step_data_emulation_expert_attacker=eval_2_optimal_first_stop_step_expert_attacker_data[0:max_iter],
        optimal_first_stop_step_means_emulation_expert_attacker=eval_2_optimal_first_stop_step_expert_attacker_means[0:max_iter],
        optimal_first_stop_step_stds_emulation_expert_attacker=eval_2_optimal_first_stop_step_expert_attacker_stds[0:max_iter],
        optimal_second_stop_step_data_emulation_expert_attacker=eval_2_optimal_second_stop_step_expert_attacker_data[0:max_iter],
        optimal_second_stop_step_means_emulation_expert_attacker=eval_2_optimal_second_stop_step_expert_attacker_means[0:max_iter],
        optimal_second_stop_step_stds_emulation_expert_attacker=eval_2_optimal_second_stop_step_expert_attacker_stds[0:max_iter],
        optimal_third_stop_step_data_emulation_expert_attacker=eval_2_optimal_third_stop_step_expert_attacker_data[0:max_iter],
        optimal_third_stop_step_means_emulation_expert_attacker=eval_2_optimal_third_stop_step_expert_attacker_means[0:max_iter],
        optimal_third_stop_step_stds_emulation_expert_attacker=eval_2_optimal_third_stop_step_expert_attacker_stds[0:max_iter],
        optimal_fourth_stop_step_data_emulation_expert_attacker=eval_2_optimal_fourth_stop_step_expert_attacker_data[0:max_iter],
        optimal_fourth_stop_step_means_emulation_expert_attacker=eval_2_optimal_fourth_stop_step_expert_attacker_means[0:max_iter],
        optimal_fourth_stop_step_stds_emulation_expert_attacker=eval_2_optimal_fourth_stop_step_expert_attacker_stds[0:max_iter],
        optimal_stops_remaining_data_emulation_expert_attacker=eval_2_optimal_stops_remaining_expert_attacker_data[0:max_iter],
        optimal_stops_remaining_means_emulation_expert_attacker=eval_2_optimal_stops_remaining_expert_attacker_means[0:max_iter],
        optimal_stops_remaining_stds_emulation_expert_attacker=eval_2_optimal_stops_remaining_expert_attacker_stds[0:max_iter],

        fontsize=6.5, figsize=(7.5, 3.25), title_fontsize=8, lw=0.75, wspace=0.19, hspace=0.08, top=0.0,
        bottom=0.11, labelsize=6, markevery=10, optimal_reward=100, sample_step=10,
        eval_only=False, plot_opt=False, iterations_per_step=12000, optimal_int=1.0,
        optimal_flag=1.0, file_name="plot_defender_simulation_emulation_steps_dist_tnsm_21_multiple_attackers_four_stops",
        markersize=2.25
    )


if __name__ == '__main__':
    base_path_1 = "/Users/kimham/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_9/hello_world/results_novice_31_aug/data/"
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
    avg_train_uncaught_intrusion_steps_data_novice_attacker,\
    avg_train_uncaught_intrusion_steps_means_novice_attacker,\
    avg_train_uncaught_intrusion_steps_stds_novice_attacker, \
    avg_train_optimal_defender_rewards_novice_attacker_data,\
    avg_train_optimal_defender_rewards_novice_attacker_means,\
    avg_train_optimal_defender_rewards_novice_attacker_stds,\
    train_snort_severe_baseline_rewards_data_novice_attacker, \
    train_snort_severe_baseline_rewards_means_novice_attacker, \
    train_snort_severe_baseline_rewards_stds_novice_attacker, train_step_baseline_rewards_data_novice_attacker, \
    train_step_baseline_rewards_means_novice_attacker, train_step_baseline_rewards_stds_novice_attacker, \
    train_snort_severe_baseline_steps_data_novice_attacker, \
    train_snort_severe_baseline_steps_means_novice_attacker, \
    train_snort_severe_baseline_steps_stds_novice_attacker, \
    train_step_baseline_steps_data_novice_attacker, train_step_baseline_steps_means_novice_attacker, \
    train_step_baseline_steps_stds_novice_attacker, \
    train_snort_severe_baseline_early_stopping_data_novice_attacker, \
    train_snort_severe_baseline_early_stopping_means_novice_attacker, \
    train_snort_severe_baseline_early_stopping_stds_novice_attacker, \
    train_step_baseline_early_stopping_data_novice_attacker, \
    train_step_baseline_early_stopping_means_novice_attacker, \
    train_step_baseline_early_stopping_stds_novice_attacker, \
    train_snort_severe_baseline_caught_attacker_data_novice_attacker, \
    train_snort_severe_baseline_caught_attacker_means_novice_attacker, \
    train_snort_severe_baseline_caught_attacker_stds_novice_attacker, \
    train_step_baseline_caught_attacker_data_novice_attacker, \
    train_step_baseline_caught_attacker_means_novice_attacker, \
    train_step_baseline_caught_attacker_stds_novice_attacker, \
    train_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker, \
    train_snort_severe_baseline_uncaught_intrusion_steps_means_novice_attacker, \
    train_snort_severe_baseline_uncaught_intrusion_steps_stds_novice_attacker, \
    train_step_baseline_uncaught_intrusion_steps_data_novice_attacker, \
    train_step_baseline_uncaught_intrusion_steps_means_novice_attacker, \
    train_step_baseline_uncaught_intrusion_steps_stds_novice_attacker, \
    train_defender_first_stop_step_novice_attacker_data, \
    train_defender_first_stop_step_novice_attacker_means, train_defender_first_stop_step_novice_attacker_stds, \
    train_defender_second_stop_step_novice_attacker_data, \
    train_defender_second_stop_step_novice_attacker_means, train_defender_second_stop_step_novice_attacker_stds, \
    train_defender_third_stop_step_novice_attacker_data, train_defender_third_stop_step_novice_attacker_means, \
    train_defender_third_stop_step_novice_attacker_stds, train_defender_fourth_stop_step_novice_attacker_data, \
    train_defender_fourth_stop_step_novice_attacker_means, train_defender_fourth_stop_step_novice_attacker_stds, \
    train_defender_stops_remaining_novice_attacker_data, train_defender_stops_remaining_novice_attacker_means, \
    train_defender_stops_remaining_novice_attacker_stds, train_optimal_first_stop_step_novice_attacker_data, \
    train_optimal_first_stop_step_novice_attacker_means, train_optimal_first_stop_step_novice_attacker_stds, \
    train_optimal_second_stop_step_novice_attacker_data, train_optimal_second_stop_step_novice_attacker_means, \
    train_optimal_second_stop_step_novice_attacker_stds, train_optimal_third_stop_step_novice_attacker_data, \
    train_optimal_third_stop_step_novice_attacker_means, train_optimal_third_stop_step_novice_attacker_stds, \
    train_optimal_fourth_stop_step_novice_attacker_data, train_optimal_fourth_stop_step_novice_attacker_means, \
    train_optimal_fourth_stop_step_novice_attacker_stds, train_optimal_stops_remaining_novice_attacker_data, \
    train_optimal_stops_remaining_novice_attacker_means, train_optimal_stops_remaining_novice_attacker_stds, \
    train_snort_severe_baseline_first_stop_step_novice_attacker_data, \
    train_snort_severe_baseline_first_stop_step_novice_attacker_means, \
    train_snort_severe_baseline_first_stop_step_novice_attacker_stds, \
    train_snort_severe_baseline_second_stop_step_novice_attacker_data, \
    train_snort_severe_baseline_second_stop_step_novice_attacker_means, \
    train_snort_severe_baseline_second_stop_step_novice_attacker_stds, \
    train_snort_severe_baseline_third_stop_step_novice_attacker_data, \
    train_snort_severe_baseline_third_stop_step_novice_attacker_means, \
    train_snort_severe_baseline_third_stop_step_novice_attacker_stds, \
    train_snort_severe_baseline_fourth_stop_step_novice_attacker_data, \
    train_snort_severe_baseline_fourth_stop_step_novice_attacker_means, \
    train_snort_severe_baseline_fourth_stop_step_novice_attacker_stds, \
    train_snort_severe_baseline_stops_remaining_novice_attacker_data, \
    train_snort_severe_baseline_stops_remaining_novice_attacker_means, \
    train_snort_severe_baseline_stops_remaining_novice_attacker_stds, \
    train_step_baseline_first_stop_step_novice_attacker_data, \
    train_step_baseline_first_stop_step_novice_attacker_means, \
    train_step_baseline_first_stop_step_novice_attacker_stds, \
    train_step_baseline_second_stop_step_novice_attacker_data, \
    train_step_baseline_second_stop_step_novice_attacker_means, \
    train_step_baseline_second_stop_step_novice_attacker_stds, \
    train_step_baseline_third_stop_step_novice_attacker_data, \
    train_step_baseline_third_stop_step_novice_attacker_means, \
    train_step_baseline_third_stop_step_novice_attacker_stds, \
    train_step_baseline_fourth_stop_step_novice_attacker_data, \
    train_step_baseline_fourth_stop_step_novice_attacker_means, \
    train_step_baseline_fourth_stop_step_novice_attacker_stds, \
    train_step_baseline_stops_remaining_novice_attacker_data, \
    train_step_baseline_stops_remaining_novice_attacker_means, \
    train_step_baseline_stops_remaining_novice_attacker_stds, \
    train_optimal_episode_steps_novice_attacker_data, train_optimal_episode_steps_novice_attacker_means, \
    train_optimal_episode_steps_novice_attacker_stds, \
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
    avg_eval_i_steps_stds_novice_attacker,\
    avg_eval_uncaught_intrusion_steps_data_novice_attacker,\
    avg_eval_uncaught_intrusion_steps_means_novice_attacker,\
    avg_eval_uncaught_intrusion_steps_stds_novice_attacker, \
    avg_eval_optimal_defender_rewards_novice_attacker_data, \
    avg_eval_optimal_defender_rewards_novice_attacker_means, \
    avg_eval_optimal_defender_rewards_novice_attacker_stds, \
    eval_snort_severe_baseline_rewards_data_novice_attacker, \
    eval_snort_severe_baseline_rewards_means_novice_attacker, \
    eval_snort_severe_baseline_rewards_stds_novice_attacker, \
    eval_step_baseline_rewards_data_novice_attacker, eval_step_baseline_rewards_means_novice_attacker, \
    eval_step_baseline_rewards_stds_novice_attacker, \
    eval_snort_severe_baseline_steps_data_novice_attacker, \
    eval_snort_severe_baseline_steps_means_novice_attacker, \
    eval_snort_severe_baseline_steps_stds_novice_attacker, \
    eval_step_baseline_steps_data_novice_attacker, eval_step_baseline_steps_means_novice_attacker, \
    eval_step_baseline_steps_stds_novice_attacker, \
    eval_snort_severe_baseline_early_stopping_data_novice_attacker, \
    eval_snort_severe_baseline_early_stopping_means_novice_attacker, \
    eval_snort_severe_baseline_early_stopping_stds_novice_attacker, \
    eval_step_baseline_early_stopping_data_novice_attacker, \
    eval_step_baseline_early_stopping_means_novice_attacker, \
    eval_step_baseline_early_stopping_stds_novice_attacker, \
    eval_snort_severe_baseline_caught_attacker_data_novice_attacker, \
    eval_snort_severe_baseline_caught_attacker_means_novice_attacker, \
    eval_snort_severe_baseline_caught_attacker_stds_novice_attacker, \
    eval_step_baseline_caught_attacker_data_novice_attacker, \
    eval_step_baseline_caught_attacker_means_novice_attacker, \
    eval_step_baseline_caught_attacker_stds_novice_attacker, \
    eval_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker, \
    eval_snort_severe_baseline_uncaught_intrusion_steps_means_novice_attacker, \
    eval_snort_severe_baseline_uncaught_intrusion_steps_stds_novice_attacker, \
    eval_step_baseline_uncaught_intrusion_steps_data_novice_attacker, \
    eval_step_baseline_uncaught_intrusion_steps_means_novice_attacker, \
    eval_step_baseline_uncaught_intrusion_steps_stds_novice_attacker, \
    eval_defender_first_stop_step_novice_attacker_data, \
    eval_defender_first_stop_step_novice_attacker_means, eval_defender_first_stop_step_novice_attacker_stds, \
    eval_defender_second_stop_step_novice_attacker_data, \
    eval_defender_second_stop_step_novice_attacker_means, eval_defender_second_stop_step_novice_attacker_stds, \
    eval_defender_third_stop_step_novice_attacker_data, eval_defender_third_stop_step_novice_attacker_means, \
    eval_defender_third_stop_step_novice_attacker_stds, eval_defender_fourth_stop_step_novice_attacker_data, \
    eval_defender_fourth_stop_step_novice_attacker_means, eval_defender_fourth_stop_step_novice_attacker_stds, \
    eval_defender_stops_remaining_novice_attacker_data, eval_defender_stops_remaining_novice_attacker_means, \
    eval_defender_stops_remaining_novice_attacker_stds, eval_optimal_first_stop_step_novice_attacker_data, \
    eval_optimal_first_stop_step_novice_attacker_means, eval_optimal_first_stop_step_novice_attacker_stds, \
    eval_optimal_second_stop_step_novice_attacker_data, eval_optimal_second_stop_step_novice_attacker_means, \
    eval_optimal_second_stop_step_novice_attacker_stds, eval_optimal_third_stop_step_novice_attacker_data, \
    eval_optimal_third_stop_step_novice_attacker_means, eval_optimal_third_stop_step_novice_attacker_stds, \
    eval_optimal_fourth_stop_step_novice_attacker_data, eval_optimal_fourth_stop_step_novice_attacker_means, \
    eval_optimal_fourth_stop_step_novice_attacker_stds, eval_optimal_stops_remaining_novice_attacker_data, \
    eval_optimal_stops_remaining_novice_attacker_means, eval_optimal_stops_remaining_novice_attacker_stds, \
    eval_snort_severe_baseline_first_stop_step_novice_attacker_data, \
    eval_snort_severe_baseline_first_stop_step_novice_attacker_means, \
    eval_snort_severe_baseline_first_stop_step_novice_attacker_stds, \
    eval_snort_severe_baseline_second_stop_step_novice_attacker_data, \
    eval_snort_severe_baseline_second_stop_step_novice_attacker_means, \
    eval_snort_severe_baseline_second_stop_step_novice_attacker_stds, \
    eval_snort_severe_baseline_third_stop_step_novice_attacker_data, \
    eval_snort_severe_baseline_third_stop_step_novice_attacker_means, \
    eval_snort_severe_baseline_third_stop_step_novice_attacker_stds, \
    eval_snort_severe_baseline_fourth_stop_step_novice_attacker_data, \
    eval_snort_severe_baseline_fourth_stop_step_novice_attacker_means, \
    eval_snort_severe_baseline_fourth_stop_step_novice_attacker_stds, \
    eval_snort_severe_baseline_stops_remaining_novice_attacker_data, \
    eval_snort_severe_baseline_stops_remaining_novice_attacker_means, \
    eval_snort_severe_baseline_stops_remaining_novice_attacker_stds, \
    eval_step_baseline_first_stop_step_novice_attacker_data, \
    eval_step_baseline_first_stop_step_novice_attacker_means, \
    eval_step_baseline_first_stop_step_novice_attacker_stds, \
    eval_step_baseline_second_stop_step_novice_attacker_data, \
    eval_step_baseline_second_stop_step_novice_attacker_means, \
    eval_step_baseline_second_stop_step_novice_attacker_stds, \
    eval_step_baseline_third_stop_step_novice_attacker_data, \
    eval_step_baseline_third_stop_step_novice_attacker_means, \
    eval_step_baseline_third_stop_step_novice_attacker_stds, \
    eval_step_baseline_fourth_stop_step_novice_attacker_data, \
    eval_step_baseline_fourth_stop_step_novice_attacker_means, \
    eval_step_baseline_fourth_stop_step_novice_attacker_stds, \
    eval_step_baseline_stops_remaining_novice_attacker_data, \
    eval_step_baseline_stops_remaining_novice_attacker_means, \
    eval_step_baseline_stops_remaining_novice_attacker_stds, \
    eval_optimal_episode_steps_novice_attacker_data, eval_optimal_episode_steps_novice_attacker_means, \
    eval_optimal_episode_steps_novice_attacker_stds, \
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
    avg_eval_2_i_steps_stds_novice_attacker,\
    avg_eval_2_uncaught_intrusion_steps_data_novice_attacker,\
    avg_eval_2_uncaught_intrusion_steps_means_novice_attacker,\
    avg_eval_2_uncaught_intrusion_steps_stds_novice_attacker, \
    avg_eval_2_optimal_defender_rewards_novice_attacker_data, \
    avg_eval_2_optimal_defender_rewards_novice_attacker_means, \
    avg_eval_2_optimal_defender_rewards_novice_attacker_stds, \
    eval_2_snort_severe_baseline_rewards_data_novice_attacker, \
    eval_2_snort_severe_baseline_rewards_means_novice_attacker, \
    eval_2_snort_severe_baseline_rewards_stds_novice_attacker, \
    eval_2_step_baseline_rewards_data_novice_attacker, \
    eval_2_step_baseline_rewards_means_novice_attacker, eval_2_step_baseline_rewards_stds_novice_attacker, \
    eval_2_snort_severe_baseline_steps_data_novice_attacker, \
    eval_2_snort_severe_baseline_steps_means_novice_attacker, \
    eval_2_snort_severe_baseline_steps_stds_novice_attacker, \
    eval_2_step_baseline_steps_data_novice_attacker, eval_2_step_baseline_steps_means_novice_attacker, \
    eval_2_step_baseline_steps_stds_novice_attacker, \
    eval_2_snort_severe_baseline_early_stopping_data_novice_attacker, \
    eval_2_snort_severe_baseline_early_stopping_means_novice_attacker, \
    eval_2_snort_severe_baseline_early_stopping_stds_novice_attacker, \
    eval_2_step_baseline_early_stopping_data_novice_attacker, \
    eval_2_step_baseline_early_stopping_means_novice_attacker, \
    eval_2_step_baseline_early_stopping_stds_novice_attacker, \
    eval_2_snort_severe_baseline_caught_attacker_data_novice_attacker, \
    eval_2_snort_severe_baseline_caught_attacker_means_novice_attacker, \
    eval_2_snort_severe_baseline_caught_attacker_stds_novice_attacker, \
    eval_2_step_baseline_caught_attacker_data_novice_attacker, \
    eval_2_step_baseline_caught_attacker_means_novice_attacker, \
    eval_2_step_baseline_caught_attacker_stds_novice_attacker, \
    eval_2_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker, \
    eval_2_snort_severe_baseline_uncaught_intrusion_steps_means_novice_attacker, \
    eval_2_snort_severe_baseline_uncaught_intrusion_steps_stds_novice_attacker, \
    eval_2_step_baseline_uncaught_intrusion_steps_data_novice_attacker, \
    eval_2_step_baseline_uncaught_intrusion_steps_means_novice_attacker, \
    eval_2_step_baseline_uncaught_intrusion_steps_stds_novice_attacker, \
    eval_2_defender_first_stop_step_novice_attacker_data, \
    eval_2_defender_first_stop_step_novice_attacker_means, eval_2_defender_first_stop_step_novice_attacker_stds, \
    eval_2_defender_second_stop_step_novice_attacker_data, \
    eval_2_defender_second_stop_step_novice_attacker_means, eval_2_defender_second_stop_step_novice_attacker_stds, \
    eval_2_defender_third_stop_step_novice_attacker_data, eval_2_defender_third_stop_step_novice_attacker_means, \
    eval_2_defender_third_stop_step_novice_attacker_stds, eval_2_defender_fourth_stop_step_novice_attacker_data, \
    eval_2_defender_fourth_stop_step_novice_attacker_means, eval_2_defender_fourth_stop_step_novice_attacker_stds, \
    eval_2_defender_stops_remaining_novice_attacker_data, eval_2_defender_stops_remaining_novice_attacker_means, \
    eval_2_defender_stops_remaining_novice_attacker_stds, eval_2_optimal_first_stop_step_novice_attacker_data, \
    eval_2_optimal_first_stop_step_novice_attacker_means, eval_2_optimal_first_stop_step_novice_attacker_stds, \
    eval_2_optimal_second_stop_step_novice_attacker_data, eval_2_optimal_second_stop_step_novice_attacker_means, \
    eval_2_optimal_second_stop_step_novice_attacker_stds, eval_2_optimal_third_stop_step_novice_attacker_data, \
    eval_2_optimal_third_stop_step_novice_attacker_means, eval_2_optimal_third_stop_step_novice_attacker_stds, \
    eval_2_optimal_fourth_stop_step_novice_attacker_data, eval_2_optimal_fourth_stop_step_novice_attacker_means, \
    eval_2_optimal_fourth_stop_step_novice_attacker_stds, eval_2_optimal_stops_remaining_novice_attacker_data, \
    eval_2_optimal_stops_remaining_novice_attacker_means, eval_2_optimal_stops_remaining_novice_attacker_stds, \
    eval_2_snort_severe_baseline_first_stop_step_novice_attacker_data, \
    eval_2_snort_severe_baseline_first_stop_step_novice_attacker_means, \
    eval_2_snort_severe_baseline_first_stop_step_novice_attacker_stds, \
    eval_2_snort_severe_baseline_second_stop_step_novice_attacker_data, \
    eval_2_snort_severe_baseline_second_stop_step_novice_attacker_means, \
    eval_2_snort_severe_baseline_second_stop_step_novice_attacker_stds, \
    eval_2_snort_severe_baseline_third_stop_step_novice_attacker_data, \
    eval_2_snort_severe_baseline_third_stop_step_novice_attacker_means, \
    eval_2_snort_severe_baseline_third_stop_step_novice_attacker_stds, \
    eval_2_snort_severe_baseline_fourth_stop_step_novice_attacker_data, \
    eval_2_snort_severe_baseline_fourth_stop_step_novice_attacker_means, \
    eval_2_snort_severe_baseline_fourth_stop_step_novice_attacker_stds, \
    eval_2_snort_severe_baseline_stops_remaining_novice_attacker_data, \
    eval_2_snort_severe_baseline_stops_remaining_novice_attacker_means, \
    eval_2_snort_severe_baseline_stops_remaining_novice_attacker_stds, \
    eval_2_step_baseline_first_stop_step_novice_attacker_data, \
    eval_2_step_baseline_first_stop_step_novice_attacker_means, \
    eval_2_step_baseline_first_stop_step_novice_attacker_stds, \
    eval_2_step_baseline_second_stop_step_novice_attacker_data, \
    eval_2_step_baseline_second_stop_step_novice_attacker_means, \
    eval_2_step_baseline_second_stop_step_novice_attacker_stds, \
    eval_2_step_baseline_third_stop_step_novice_attacker_data, \
    eval_2_step_baseline_third_stop_step_novice_attacker_means, \
    eval_2_step_baseline_third_stop_step_novice_attacker_stds, \
    eval_2_step_baseline_fourth_stop_step_novice_attacker_data, \
    eval_2_step_baseline_fourth_stop_step_novice_attacker_means, \
    eval_2_step_baseline_fourth_stop_step_novice_attacker_stds, \
    eval_2_step_baseline_stops_remaining_novice_attacker_data, \
    eval_2_step_baseline_stops_remaining_novice_attacker_means, \
    eval_2_step_baseline_stops_remaining_novice_attacker_stds, \
    eval_2_optimal_episode_steps_novice_attacker_data, eval_2_optimal_episode_steps_novice_attacker_means, \
    eval_2_optimal_episode_steps_novice_attacker_stds \
        = parse_data(novice_attacker_base_path=base_path_1, suffix="gensim")


    # Experienced

    base_path_1 = "/Users/kimham/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_9/hello_world/results_experienced_31_aug/data/"
    avg_train_rewards_data_experienced_attacker, avg_train_rewards_means_experienced_attacker, \
    avg_train_rewards_stds_experienced_attacker, \
    avg_train_steps_data_experienced_attacker, avg_train_steps_means_experienced_attacker, \
    avg_train_steps_stds_experienced_attacker, \
    avg_train_caught_frac_data_experienced_attacker, avg_train_caught_frac_means_experienced_attacker, \
    avg_train_caught_frac_stds_experienced_attacker, \
    avg_train_early_stopping_frac_data_experienced_attacker, avg_train_early_stopping_means_experienced_attacker, \
    avg_train_early_stopping_stds_experienced_attacker, avg_train_intrusion_frac_data_experienced_attacker, \
    avg_train_intrusion_means_experienced_attacker, \
    avg_train_intrusion_stds_experienced_attacker, \
    avg_train_i_steps_data_experienced_attacker, avg_train_i_steps_means_experienced_attacker, \
    avg_train_i_steps_stds_experienced_attacker, \
    avg_train_uncaught_intrusion_steps_data_experienced_attacker, \
    avg_train_uncaught_intrusion_steps_means_experienced_attacker, \
    avg_train_uncaught_intrusion_steps_stds_experienced_attacker, \
    avg_train_optimal_defender_rewards_experienced_attacker_data, \
    avg_train_optimal_defender_rewards_experienced_attacker_means, \
    avg_train_optimal_defender_rewards_experienced_attacker_stds, \
    train_snort_severe_baseline_rewards_data_experienced_attacker, \
    train_snort_severe_baseline_rewards_means_experienced_attacker, \
    train_snort_severe_baseline_rewards_stds_experienced_attacker, train_step_baseline_rewards_data_experienced_attacker, \
    train_step_baseline_rewards_means_experienced_attacker, train_step_baseline_rewards_stds_experienced_attacker, \
    train_snort_severe_baseline_steps_data_experienced_attacker, \
    train_snort_severe_baseline_steps_means_experienced_attacker, \
    train_snort_severe_baseline_steps_stds_experienced_attacker, \
    train_step_baseline_steps_data_experienced_attacker, train_step_baseline_steps_means_experienced_attacker, \
    train_step_baseline_steps_stds_experienced_attacker, \
    train_snort_severe_baseline_early_stopping_data_experienced_attacker, \
    train_snort_severe_baseline_early_stopping_means_experienced_attacker, \
    train_snort_severe_baseline_early_stopping_stds_experienced_attacker, \
    train_step_baseline_early_stopping_data_experienced_attacker, \
    train_step_baseline_early_stopping_means_experienced_attacker, \
    train_step_baseline_early_stopping_stds_experienced_attacker, \
    train_snort_severe_baseline_caught_attacker_data_experienced_attacker, \
    train_snort_severe_baseline_caught_attacker_means_experienced_attacker, \
    train_snort_severe_baseline_caught_attacker_stds_experienced_attacker, \
    train_step_baseline_caught_attacker_data_experienced_attacker, \
    train_step_baseline_caught_attacker_means_experienced_attacker, \
    train_step_baseline_caught_attacker_stds_experienced_attacker, \
    train_snort_severe_baseline_uncaught_intrusion_steps_data_experienced_attacker, \
    train_snort_severe_baseline_uncaught_intrusion_steps_means_experienced_attacker, \
    train_snort_severe_baseline_uncaught_intrusion_steps_stds_experienced_attacker, \
    train_step_baseline_uncaught_intrusion_steps_data_experienced_attacker, \
    train_step_baseline_uncaught_intrusion_steps_means_experienced_attacker, \
    train_step_baseline_uncaught_intrusion_steps_stds_experienced_attacker, \
    train_defender_first_stop_step_experienced_attacker_data, \
    train_defender_first_stop_step_experienced_attacker_means, train_defender_first_stop_step_experienced_attacker_stds, \
    train_defender_second_stop_step_experienced_attacker_data, \
    train_defender_second_stop_step_experienced_attacker_means, train_defender_second_stop_step_experienced_attacker_stds, \
    train_defender_third_stop_step_experienced_attacker_data, train_defender_third_stop_step_experienced_attacker_means, \
    train_defender_third_stop_step_experienced_attacker_stds, train_defender_fourth_stop_step_experienced_attacker_data, \
    train_defender_fourth_stop_step_experienced_attacker_means, train_defender_fourth_stop_step_experienced_attacker_stds, \
    train_defender_stops_remaining_experienced_attacker_data, train_defender_stops_remaining_experienced_attacker_means, \
    train_defender_stops_remaining_experienced_attacker_stds, train_optimal_first_stop_step_experienced_attacker_data, \
    train_optimal_first_stop_step_experienced_attacker_means, train_optimal_first_stop_step_experienced_attacker_stds, \
    train_optimal_second_stop_step_experienced_attacker_data, train_optimal_second_stop_step_experienced_attacker_means, \
    train_optimal_second_stop_step_experienced_attacker_stds, train_optimal_third_stop_step_experienced_attacker_data, \
    train_optimal_third_stop_step_experienced_attacker_means, train_optimal_third_stop_step_experienced_attacker_stds, \
    train_optimal_fourth_stop_step_experienced_attacker_data, train_optimal_fourth_stop_step_experienced_attacker_means, \
    train_optimal_fourth_stop_step_experienced_attacker_stds, train_optimal_stops_remaining_experienced_attacker_data, \
    train_optimal_stops_remaining_experienced_attacker_means, train_optimal_stops_remaining_experienced_attacker_stds, \
    train_snort_severe_baseline_first_stop_step_experienced_attacker_data, \
    train_snort_severe_baseline_first_stop_step_experienced_attacker_means, \
    train_snort_severe_baseline_first_stop_step_experienced_attacker_stds, \
    train_snort_severe_baseline_second_stop_step_experienced_attacker_data, \
    train_snort_severe_baseline_second_stop_step_experienced_attacker_means, \
    train_snort_severe_baseline_second_stop_step_experienced_attacker_stds, \
    train_snort_severe_baseline_third_stop_step_experienced_attacker_data, \
    train_snort_severe_baseline_third_stop_step_experienced_attacker_means, \
    train_snort_severe_baseline_third_stop_step_experienced_attacker_stds, \
    train_snort_severe_baseline_fourth_stop_step_experienced_attacker_data, \
    train_snort_severe_baseline_fourth_stop_step_experienced_attacker_means, \
    train_snort_severe_baseline_fourth_stop_step_experienced_attacker_stds, \
    train_snort_severe_baseline_stops_remaining_experienced_attacker_data, \
    train_snort_severe_baseline_stops_remaining_experienced_attacker_means, \
    train_snort_severe_baseline_stops_remaining_experienced_attacker_stds, \
    train_step_baseline_first_stop_step_experienced_attacker_data, \
    train_step_baseline_first_stop_step_experienced_attacker_means, \
    train_step_baseline_first_stop_step_experienced_attacker_stds, \
    train_step_baseline_second_stop_step_experienced_attacker_data, \
    train_step_baseline_second_stop_step_experienced_attacker_means, \
    train_step_baseline_second_stop_step_experienced_attacker_stds, \
    train_step_baseline_third_stop_step_experienced_attacker_data, \
    train_step_baseline_third_stop_step_experienced_attacker_means, \
    train_step_baseline_third_stop_step_experienced_attacker_stds, \
    train_step_baseline_fourth_stop_step_experienced_attacker_data, \
    train_step_baseline_fourth_stop_step_experienced_attacker_means, \
    train_step_baseline_fourth_stop_step_experienced_attacker_stds, \
    train_step_baseline_stops_remaining_experienced_attacker_data, \
    train_step_baseline_stops_remaining_experienced_attacker_means, \
    train_step_baseline_stops_remaining_experienced_attacker_stds, \
    train_optimal_episode_steps_experienced_attacker_data, train_optimal_episode_steps_experienced_attacker_means, \
    train_optimal_episode_steps_experienced_attacker_stds, \
    avg_eval_rewards_data_experienced_attacker, avg_eval_rewards_means_experienced_attacker, \
    avg_eval_rewards_stds_experienced_attacker, \
    avg_eval_steps_data_experienced_attacker, avg_eval_steps_means_experienced_attacker, \
    avg_eval_steps_stds_experienced_attacker, \
    avg_eval_caught_frac_data_experienced_attacker, avg_eval_caught_frac_means_experienced_attacker, \
    avg_eval_caught_frac_stds_experienced_attacker, \
    avg_eval_early_stopping_frac_data_experienced_attacker, avg_eval_early_stopping_means_experienced_attacker, \
    avg_eval_early_stopping_stds_experienced_attacker, avg_eval_intrusion_frac_data_experienced_attacker, \
    avg_eval_intrusion_means_experienced_attacker, \
    avg_eval_intrusion_stds_experienced_attacker, \
    avg_eval_i_steps_data_experienced_attacker, avg_eval_i_steps_means_experienced_attacker, \
    avg_eval_i_steps_stds_experienced_attacker, \
    avg_eval_uncaught_intrusion_steps_data_experienced_attacker, \
    avg_eval_uncaught_intrusion_steps_means_experienced_attacker, \
    avg_eval_uncaught_intrusion_steps_stds_experienced_attacker, \
    avg_eval_optimal_defender_rewards_experienced_attacker_data, \
    avg_eval_optimal_defender_rewards_experienced_attacker_means, \
    avg_eval_optimal_defender_rewards_experienced_attacker_stds, \
    eval_snort_severe_baseline_rewards_data_experienced_attacker, \
    eval_snort_severe_baseline_rewards_means_experienced_attacker, \
    eval_snort_severe_baseline_rewards_stds_experienced_attacker, \
    eval_step_baseline_rewards_data_experienced_attacker, eval_step_baseline_rewards_means_experienced_attacker, \
    eval_step_baseline_rewards_stds_experienced_attacker, \
    eval_snort_severe_baseline_steps_data_experienced_attacker, \
    eval_snort_severe_baseline_steps_means_experienced_attacker, \
    eval_snort_severe_baseline_steps_stds_experienced_attacker, \
    eval_step_baseline_steps_data_experienced_attacker, eval_step_baseline_steps_means_experienced_attacker, \
    eval_step_baseline_steps_stds_experienced_attacker, \
    eval_snort_severe_baseline_early_stopping_data_experienced_attacker, \
    eval_snort_severe_baseline_early_stopping_means_experienced_attacker, \
    eval_snort_severe_baseline_early_stopping_stds_experienced_attacker, \
    eval_step_baseline_early_stopping_data_experienced_attacker, \
    eval_step_baseline_early_stopping_means_experienced_attacker, \
    eval_step_baseline_early_stopping_stds_experienced_attacker, \
    eval_snort_severe_baseline_caught_attacker_data_experienced_attacker, \
    eval_snort_severe_baseline_caught_attacker_means_experienced_attacker, \
    eval_snort_severe_baseline_caught_attacker_stds_experienced_attacker, \
    eval_step_baseline_caught_attacker_data_experienced_attacker, \
    eval_step_baseline_caught_attacker_means_experienced_attacker, \
    eval_step_baseline_caught_attacker_stds_experienced_attacker, \
    eval_snort_severe_baseline_uncaught_intrusion_steps_data_experienced_attacker, \
    eval_snort_severe_baseline_uncaught_intrusion_steps_means_experienced_attacker, \
    eval_snort_severe_baseline_uncaught_intrusion_steps_stds_experienced_attacker, \
    eval_step_baseline_uncaught_intrusion_steps_data_experienced_attacker, \
    eval_step_baseline_uncaught_intrusion_steps_means_experienced_attacker, \
    eval_step_baseline_uncaught_intrusion_steps_stds_experienced_attacker, \
    eval_defender_first_stop_step_experienced_attacker_data, \
    eval_defender_first_stop_step_experienced_attacker_means, eval_defender_first_stop_step_experienced_attacker_stds, \
    eval_defender_second_stop_step_experienced_attacker_data, \
    eval_defender_second_stop_step_experienced_attacker_means, eval_defender_second_stop_step_experienced_attacker_stds, \
    eval_defender_third_stop_step_experienced_attacker_data, eval_defender_third_stop_step_experienced_attacker_means, \
    eval_defender_third_stop_step_experienced_attacker_stds, eval_defender_fourth_stop_step_experienced_attacker_data, \
    eval_defender_fourth_stop_step_experienced_attacker_means, eval_defender_fourth_stop_step_experienced_attacker_stds, \
    eval_defender_stops_remaining_experienced_attacker_data, eval_defender_stops_remaining_experienced_attacker_means, \
    eval_defender_stops_remaining_experienced_attacker_stds, eval_optimal_first_stop_step_experienced_attacker_data, \
    eval_optimal_first_stop_step_experienced_attacker_means, eval_optimal_first_stop_step_experienced_attacker_stds, \
    eval_optimal_second_stop_step_experienced_attacker_data, eval_optimal_second_stop_step_experienced_attacker_means, \
    eval_optimal_second_stop_step_experienced_attacker_stds, eval_optimal_third_stop_step_experienced_attacker_data, \
    eval_optimal_third_stop_step_experienced_attacker_means, eval_optimal_third_stop_step_experienced_attacker_stds, \
    eval_optimal_fourth_stop_step_experienced_attacker_data, eval_optimal_fourth_stop_step_experienced_attacker_means, \
    eval_optimal_fourth_stop_step_experienced_attacker_stds, eval_optimal_stops_remaining_experienced_attacker_data, \
    eval_optimal_stops_remaining_experienced_attacker_means, eval_optimal_stops_remaining_experienced_attacker_stds, \
    eval_snort_severe_baseline_first_stop_step_experienced_attacker_data, \
    eval_snort_severe_baseline_first_stop_step_experienced_attacker_means, \
    eval_snort_severe_baseline_first_stop_step_experienced_attacker_stds, \
    eval_snort_severe_baseline_second_stop_step_experienced_attacker_data, \
    eval_snort_severe_baseline_second_stop_step_experienced_attacker_means, \
    eval_snort_severe_baseline_second_stop_step_experienced_attacker_stds, \
    eval_snort_severe_baseline_third_stop_step_experienced_attacker_data, \
    eval_snort_severe_baseline_third_stop_step_experienced_attacker_means, \
    eval_snort_severe_baseline_third_stop_step_experienced_attacker_stds, \
    eval_snort_severe_baseline_fourth_stop_step_experienced_attacker_data, \
    eval_snort_severe_baseline_fourth_stop_step_experienced_attacker_means, \
    eval_snort_severe_baseline_fourth_stop_step_experienced_attacker_stds, \
    eval_snort_severe_baseline_stops_remaining_experienced_attacker_data, \
    eval_snort_severe_baseline_stops_remaining_experienced_attacker_means, \
    eval_snort_severe_baseline_stops_remaining_experienced_attacker_stds, \
    eval_step_baseline_first_stop_step_experienced_attacker_data, \
    eval_step_baseline_first_stop_step_experienced_attacker_means, \
    eval_step_baseline_first_stop_step_experienced_attacker_stds, \
    eval_step_baseline_second_stop_step_experienced_attacker_data, \
    eval_step_baseline_second_stop_step_experienced_attacker_means, \
    eval_step_baseline_second_stop_step_experienced_attacker_stds, \
    eval_step_baseline_third_stop_step_experienced_attacker_data, \
    eval_step_baseline_third_stop_step_experienced_attacker_means, \
    eval_step_baseline_third_stop_step_experienced_attacker_stds, \
    eval_step_baseline_fourth_stop_step_experienced_attacker_data, \
    eval_step_baseline_fourth_stop_step_experienced_attacker_means, \
    eval_step_baseline_fourth_stop_step_experienced_attacker_stds, \
    eval_step_baseline_stops_remaining_experienced_attacker_data, \
    eval_step_baseline_stops_remaining_experienced_attacker_means, \
    eval_step_baseline_stops_remaining_experienced_attacker_stds, \
    eval_optimal_episode_steps_experienced_attacker_data, eval_optimal_episode_steps_experienced_attacker_means, \
    eval_optimal_episode_steps_experienced_attacker_stds, \
    avg_eval_2_rewards_data_experienced_attacker, avg_eval_2_rewards_means_experienced_attacker, \
    avg_eval_2_rewards_stds_experienced_attacker, \
    avg_eval_2_steps_data_experienced_attacker, avg_eval_2_steps_means_experienced_attacker, \
    avg_eval_2_steps_stds_experienced_attacker, \
    avg_eval_2_caught_frac_data_experienced_attacker, avg_eval_2_caught_frac_means_experienced_attacker, \
    avg_eval_2_caught_frac_stds_experienced_attacker, \
    avg_eval_2_early_stopping_frac_data_experienced_attacker, avg_eval_2_early_stopping_means_experienced_attacker, \
    avg_eval_2_early_stopping_stds_experienced_attacker, avg_eval_2_intrusion_frac_data_experienced_attacker, \
    avg_eval_2_intrusion_means_experienced_attacker, \
    avg_eval_2_intrusion_stds_experienced_attacker, \
    avg_eval_2_i_steps_data_experienced_attacker, avg_eval_2_i_steps_means_experienced_attacker, \
    avg_eval_2_i_steps_stds_experienced_attacker, \
    avg_eval_2_uncaught_intrusion_steps_data_experienced_attacker, \
    avg_eval_2_uncaught_intrusion_steps_means_experienced_attacker, \
    avg_eval_2_uncaught_intrusion_steps_stds_experienced_attacker, \
    avg_eval_2_optimal_defender_rewards_experienced_attacker_data, \
    avg_eval_2_optimal_defender_rewards_experienced_attacker_means, \
    avg_eval_2_optimal_defender_rewards_experienced_attacker_stds, \
    eval_2_snort_severe_baseline_rewards_data_experienced_attacker, \
    eval_2_snort_severe_baseline_rewards_means_experienced_attacker, \
    eval_2_snort_severe_baseline_rewards_stds_experienced_attacker, \
    eval_2_step_baseline_rewards_data_experienced_attacker, \
    eval_2_step_baseline_rewards_means_experienced_attacker, eval_2_step_baseline_rewards_stds_experienced_attacker, \
    eval_2_snort_severe_baseline_steps_data_experienced_attacker, \
    eval_2_snort_severe_baseline_steps_means_experienced_attacker, \
    eval_2_snort_severe_baseline_steps_stds_experienced_attacker, \
    eval_2_step_baseline_steps_data_experienced_attacker, eval_2_step_baseline_steps_means_experienced_attacker, \
    eval_2_step_baseline_steps_stds_experienced_attacker, \
    eval_2_snort_severe_baseline_early_stopping_data_experienced_attacker, \
    eval_2_snort_severe_baseline_early_stopping_means_experienced_attacker, \
    eval_2_snort_severe_baseline_early_stopping_stds_experienced_attacker, \
    eval_2_step_baseline_early_stopping_data_experienced_attacker, \
    eval_2_step_baseline_early_stopping_means_experienced_attacker, \
    eval_2_step_baseline_early_stopping_stds_experienced_attacker, \
    eval_2_snort_severe_baseline_caught_attacker_data_experienced_attacker, \
    eval_2_snort_severe_baseline_caught_attacker_means_experienced_attacker, \
    eval_2_snort_severe_baseline_caught_attacker_stds_experienced_attacker, \
    eval_2_step_baseline_caught_attacker_data_experienced_attacker, \
    eval_2_step_baseline_caught_attacker_means_experienced_attacker, \
    eval_2_step_baseline_caught_attacker_stds_experienced_attacker, \
    eval_2_snort_severe_baseline_uncaught_intrusion_steps_data_experienced_attacker, \
    eval_2_snort_severe_baseline_uncaught_intrusion_steps_means_experienced_attacker, \
    eval_2_snort_severe_baseline_uncaught_intrusion_steps_stds_experienced_attacker, \
    eval_2_step_baseline_uncaught_intrusion_steps_data_experienced_attacker, \
    eval_2_step_baseline_uncaught_intrusion_steps_means_experienced_attacker, \
    eval_2_step_baseline_uncaught_intrusion_steps_stds_experienced_attacker, \
    eval_2_defender_first_stop_step_experienced_attacker_data, \
    eval_2_defender_first_stop_step_experienced_attacker_means, eval_2_defender_first_stop_step_experienced_attacker_stds, \
    eval_2_defender_second_stop_step_experienced_attacker_data, \
    eval_2_defender_second_stop_step_experienced_attacker_means, eval_2_defender_second_stop_step_experienced_attacker_stds, \
    eval_2_defender_third_stop_step_experienced_attacker_data, eval_2_defender_third_stop_step_experienced_attacker_means, \
    eval_2_defender_third_stop_step_experienced_attacker_stds, eval_2_defender_fourth_stop_step_experienced_attacker_data, \
    eval_2_defender_fourth_stop_step_experienced_attacker_means, eval_2_defender_fourth_stop_step_experienced_attacker_stds, \
    eval_2_defender_stops_remaining_experienced_attacker_data, eval_2_defender_stops_remaining_experienced_attacker_means, \
    eval_2_defender_stops_remaining_experienced_attacker_stds, eval_2_optimal_first_stop_step_experienced_attacker_data, \
    eval_2_optimal_first_stop_step_experienced_attacker_means, eval_2_optimal_first_stop_step_experienced_attacker_stds, \
    eval_2_optimal_second_stop_step_experienced_attacker_data, eval_2_optimal_second_stop_step_experienced_attacker_means, \
    eval_2_optimal_second_stop_step_experienced_attacker_stds, eval_2_optimal_third_stop_step_experienced_attacker_data, \
    eval_2_optimal_third_stop_step_experienced_attacker_means, eval_2_optimal_third_stop_step_experienced_attacker_stds, \
    eval_2_optimal_fourth_stop_step_experienced_attacker_data, eval_2_optimal_fourth_stop_step_experienced_attacker_means, \
    eval_2_optimal_fourth_stop_step_experienced_attacker_stds, eval_2_optimal_stops_remaining_experienced_attacker_data, \
    eval_2_optimal_stops_remaining_experienced_attacker_means, eval_2_optimal_stops_remaining_experienced_attacker_stds, \
    eval_2_snort_severe_baseline_first_stop_step_experienced_attacker_data, \
    eval_2_snort_severe_baseline_first_stop_step_experienced_attacker_means, \
    eval_2_snort_severe_baseline_first_stop_step_experienced_attacker_stds, \
    eval_2_snort_severe_baseline_second_stop_step_experienced_attacker_data, \
    eval_2_snort_severe_baseline_second_stop_step_experienced_attacker_means, \
    eval_2_snort_severe_baseline_second_stop_step_experienced_attacker_stds, \
    eval_2_snort_severe_baseline_third_stop_step_experienced_attacker_data, \
    eval_2_snort_severe_baseline_third_stop_step_experienced_attacker_means, \
    eval_2_snort_severe_baseline_third_stop_step_experienced_attacker_stds, \
    eval_2_snort_severe_baseline_fourth_stop_step_experienced_attacker_data, \
    eval_2_snort_severe_baseline_fourth_stop_step_experienced_attacker_means, \
    eval_2_snort_severe_baseline_fourth_stop_step_experienced_attacker_stds, \
    eval_2_snort_severe_baseline_stops_remaining_experienced_attacker_data, \
    eval_2_snort_severe_baseline_stops_remaining_experienced_attacker_means, \
    eval_2_snort_severe_baseline_stops_remaining_experienced_attacker_stds, \
    eval_2_step_baseline_first_stop_step_experienced_attacker_data, \
    eval_2_step_baseline_first_stop_step_experienced_attacker_means, \
    eval_2_step_baseline_first_stop_step_experienced_attacker_stds, \
    eval_2_step_baseline_second_stop_step_experienced_attacker_data, \
    eval_2_step_baseline_second_stop_step_experienced_attacker_means, \
    eval_2_step_baseline_second_stop_step_experienced_attacker_stds, \
    eval_2_step_baseline_third_stop_step_experienced_attacker_data, \
    eval_2_step_baseline_third_stop_step_experienced_attacker_means, \
    eval_2_step_baseline_third_stop_step_experienced_attacker_stds, \
    eval_2_step_baseline_fourth_stop_step_experienced_attacker_data, \
    eval_2_step_baseline_fourth_stop_step_experienced_attacker_means, \
    eval_2_step_baseline_fourth_stop_step_experienced_attacker_stds, \
    eval_2_step_baseline_stops_remaining_experienced_attacker_data, \
    eval_2_step_baseline_stops_remaining_experienced_attacker_means, \
    eval_2_step_baseline_stops_remaining_experienced_attacker_stds, \
    eval_2_optimal_episode_steps_experienced_attacker_data, eval_2_optimal_episode_steps_experienced_attacker_means, \
    eval_2_optimal_episode_steps_experienced_attacker_stds \
        = parse_data(novice_attacker_base_path=base_path_1, suffix="gensim")


    # Expert

    base_path_1 = "/Users/kimham/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_9/hello_world/results_expert_31_aug/data/"
    avg_train_rewards_data_expert_attacker, avg_train_rewards_means_expert_attacker, \
    avg_train_rewards_stds_expert_attacker, \
    avg_train_steps_data_expert_attacker, avg_train_steps_means_expert_attacker, \
    avg_train_steps_stds_expert_attacker, \
    avg_train_caught_frac_data_expert_attacker, avg_train_caught_frac_means_expert_attacker, \
    avg_train_caught_frac_stds_expert_attacker, \
    avg_train_early_stopping_frac_data_expert_attacker, avg_train_early_stopping_means_expert_attacker, \
    avg_train_early_stopping_stds_expert_attacker, avg_train_intrusion_frac_data_expert_attacker, \
    avg_train_intrusion_means_expert_attacker, \
    avg_train_intrusion_stds_expert_attacker, \
    avg_train_i_steps_data_expert_attacker, avg_train_i_steps_means_expert_attacker, \
    avg_train_i_steps_stds_expert_attacker, \
    avg_train_uncaught_intrusion_steps_data_expert_attacker, \
    avg_train_uncaught_intrusion_steps_means_expert_attacker, \
    avg_train_uncaught_intrusion_steps_stds_expert_attacker, \
    avg_train_optimal_defender_rewards_expert_attacker_data, \
    avg_train_optimal_defender_rewards_expert_attacker_means, \
    avg_train_optimal_defender_rewards_expert_attacker_stds, \
    train_snort_severe_baseline_rewards_data_expert_attacker, \
    train_snort_severe_baseline_rewards_means_expert_attacker, \
    train_snort_severe_baseline_rewards_stds_expert_attacker, train_step_baseline_rewards_data_expert_attacker, \
    train_step_baseline_rewards_means_expert_attacker, train_step_baseline_rewards_stds_expert_attacker, \
    train_snort_severe_baseline_steps_data_expert_attacker, \
    train_snort_severe_baseline_steps_means_expert_attacker, \
    train_snort_severe_baseline_steps_stds_expert_attacker, \
    train_step_baseline_steps_data_expert_attacker, train_step_baseline_steps_means_expert_attacker, \
    train_step_baseline_steps_stds_expert_attacker, \
    train_snort_severe_baseline_early_stopping_data_expert_attacker, \
    train_snort_severe_baseline_early_stopping_means_expert_attacker, \
    train_snort_severe_baseline_early_stopping_stds_expert_attacker, \
    train_step_baseline_early_stopping_data_expert_attacker, \
    train_step_baseline_early_stopping_means_expert_attacker, \
    train_step_baseline_early_stopping_stds_expert_attacker, \
    train_snort_severe_baseline_caught_attacker_data_expert_attacker, \
    train_snort_severe_baseline_caught_attacker_means_expert_attacker, \
    train_snort_severe_baseline_caught_attacker_stds_expert_attacker, \
    train_step_baseline_caught_attacker_data_expert_attacker, \
    train_step_baseline_caught_attacker_means_expert_attacker, \
    train_step_baseline_caught_attacker_stds_expert_attacker, \
    train_snort_severe_baseline_uncaught_intrusion_steps_data_expert_attacker, \
    train_snort_severe_baseline_uncaught_intrusion_steps_means_expert_attacker, \
    train_snort_severe_baseline_uncaught_intrusion_steps_stds_expert_attacker, \
    train_step_baseline_uncaught_intrusion_steps_data_expert_attacker, \
    train_step_baseline_uncaught_intrusion_steps_means_expert_attacker, \
    train_step_baseline_uncaught_intrusion_steps_stds_expert_attacker, \
    train_defender_first_stop_step_expert_attacker_data, \
    train_defender_first_stop_step_expert_attacker_means, train_defender_first_stop_step_expert_attacker_stds, \
    train_defender_second_stop_step_expert_attacker_data, \
    train_defender_second_stop_step_expert_attacker_means, train_defender_second_stop_step_expert_attacker_stds, \
    train_defender_third_stop_step_expert_attacker_data, train_defender_third_stop_step_expert_attacker_means, \
    train_defender_third_stop_step_expert_attacker_stds, train_defender_fourth_stop_step_expert_attacker_data, \
    train_defender_fourth_stop_step_expert_attacker_means, train_defender_fourth_stop_step_expert_attacker_stds, \
    train_defender_stops_remaining_expert_attacker_data, train_defender_stops_remaining_expert_attacker_means, \
    train_defender_stops_remaining_expert_attacker_stds, train_optimal_first_stop_step_expert_attacker_data, \
    train_optimal_first_stop_step_expert_attacker_means, train_optimal_first_stop_step_expert_attacker_stds, \
    train_optimal_second_stop_step_expert_attacker_data, train_optimal_second_stop_step_expert_attacker_means, \
    train_optimal_second_stop_step_expert_attacker_stds, train_optimal_third_stop_step_expert_attacker_data, \
    train_optimal_third_stop_step_expert_attacker_means, train_optimal_third_stop_step_expert_attacker_stds, \
    train_optimal_fourth_stop_step_expert_attacker_data, train_optimal_fourth_stop_step_expert_attacker_means, \
    train_optimal_fourth_stop_step_expert_attacker_stds, train_optimal_stops_remaining_expert_attacker_data, \
    train_optimal_stops_remaining_expert_attacker_means, train_optimal_stops_remaining_expert_attacker_stds, \
    train_snort_severe_baseline_first_stop_step_expert_attacker_data, \
    train_snort_severe_baseline_first_stop_step_expert_attacker_means, \
    train_snort_severe_baseline_first_stop_step_expert_attacker_stds, \
    train_snort_severe_baseline_second_stop_step_expert_attacker_data, \
    train_snort_severe_baseline_second_stop_step_expert_attacker_means, \
    train_snort_severe_baseline_second_stop_step_expert_attacker_stds, \
    train_snort_severe_baseline_third_stop_step_expert_attacker_data, \
    train_snort_severe_baseline_third_stop_step_expert_attacker_means, \
    train_snort_severe_baseline_third_stop_step_expert_attacker_stds, \
    train_snort_severe_baseline_fourth_stop_step_expert_attacker_data, \
    train_snort_severe_baseline_fourth_stop_step_expert_attacker_means, \
    train_snort_severe_baseline_fourth_stop_step_expert_attacker_stds, \
    train_snort_severe_baseline_stops_remaining_expert_attacker_data, \
    train_snort_severe_baseline_stops_remaining_expert_attacker_means, \
    train_snort_severe_baseline_stops_remaining_expert_attacker_stds, \
    train_step_baseline_first_stop_step_expert_attacker_data, \
    train_step_baseline_first_stop_step_expert_attacker_means, \
    train_step_baseline_first_stop_step_expert_attacker_stds, \
    train_step_baseline_second_stop_step_expert_attacker_data, \
    train_step_baseline_second_stop_step_expert_attacker_means, \
    train_step_baseline_second_stop_step_expert_attacker_stds, \
    train_step_baseline_third_stop_step_expert_attacker_data, \
    train_step_baseline_third_stop_step_expert_attacker_means, \
    train_step_baseline_third_stop_step_expert_attacker_stds, \
    train_step_baseline_fourth_stop_step_expert_attacker_data, \
    train_step_baseline_fourth_stop_step_expert_attacker_means, \
    train_step_baseline_fourth_stop_step_expert_attacker_stds, \
    train_step_baseline_stops_remaining_expert_attacker_data, \
    train_step_baseline_stops_remaining_expert_attacker_means, \
    train_step_baseline_stops_remaining_expert_attacker_stds, \
    train_optimal_episode_steps_expert_attacker_data, train_optimal_episode_steps_expert_attacker_means, \
    train_optimal_episode_steps_expert_attacker_stds, \
    avg_eval_rewards_data_expert_attacker, avg_eval_rewards_means_expert_attacker, \
    avg_eval_rewards_stds_expert_attacker, \
    avg_eval_steps_data_expert_attacker, avg_eval_steps_means_expert_attacker, \
    avg_eval_steps_stds_expert_attacker, \
    avg_eval_caught_frac_data_expert_attacker, avg_eval_caught_frac_means_expert_attacker, \
    avg_eval_caught_frac_stds_expert_attacker, \
    avg_eval_early_stopping_frac_data_expert_attacker, avg_eval_early_stopping_means_expert_attacker, \
    avg_eval_early_stopping_stds_expert_attacker, avg_eval_intrusion_frac_data_expert_attacker, \
    avg_eval_intrusion_means_expert_attacker, \
    avg_eval_intrusion_stds_expert_attacker, \
    avg_eval_i_steps_data_expert_attacker, avg_eval_i_steps_means_expert_attacker, \
    avg_eval_i_steps_stds_expert_attacker, \
    avg_eval_uncaught_intrusion_steps_data_expert_attacker, \
    avg_eval_uncaught_intrusion_steps_means_expert_attacker, \
    avg_eval_uncaught_intrusion_steps_stds_expert_attacker, \
    avg_eval_optimal_defender_rewards_expert_attacker_data, \
    avg_eval_optimal_defender_rewards_expert_attacker_means, \
    avg_eval_optimal_defender_rewards_expert_attacker_stds, \
    eval_snort_severe_baseline_rewards_data_expert_attacker, \
    eval_snort_severe_baseline_rewards_means_expert_attacker, \
    eval_snort_severe_baseline_rewards_stds_expert_attacker, \
    eval_step_baseline_rewards_data_expert_attacker, eval_step_baseline_rewards_means_expert_attacker, \
    eval_step_baseline_rewards_stds_expert_attacker, \
    eval_snort_severe_baseline_steps_data_expert_attacker, \
    eval_snort_severe_baseline_steps_means_expert_attacker, \
    eval_snort_severe_baseline_steps_stds_expert_attacker, \
    eval_step_baseline_steps_data_expert_attacker, eval_step_baseline_steps_means_expert_attacker, \
    eval_step_baseline_steps_stds_expert_attacker, \
    eval_snort_severe_baseline_early_stopping_data_expert_attacker, \
    eval_snort_severe_baseline_early_stopping_means_expert_attacker, \
    eval_snort_severe_baseline_early_stopping_stds_expert_attacker, \
    eval_step_baseline_early_stopping_data_expert_attacker, \
    eval_step_baseline_early_stopping_means_expert_attacker, \
    eval_step_baseline_early_stopping_stds_expert_attacker, \
    eval_snort_severe_baseline_caught_attacker_data_expert_attacker, \
    eval_snort_severe_baseline_caught_attacker_means_expert_attacker, \
    eval_snort_severe_baseline_caught_attacker_stds_expert_attacker, \
    eval_step_baseline_caught_attacker_data_expert_attacker, \
    eval_step_baseline_caught_attacker_means_expert_attacker, \
    eval_step_baseline_caught_attacker_stds_expert_attacker, \
    eval_snort_severe_baseline_uncaught_intrusion_steps_data_expert_attacker, \
    eval_snort_severe_baseline_uncaught_intrusion_steps_means_expert_attacker, \
    eval_snort_severe_baseline_uncaught_intrusion_steps_stds_expert_attacker, \
    eval_step_baseline_uncaught_intrusion_steps_data_expert_attacker, \
    eval_step_baseline_uncaught_intrusion_steps_means_expert_attacker, \
    eval_step_baseline_uncaught_intrusion_steps_stds_expert_attacker, \
    eval_defender_first_stop_step_expert_attacker_data, \
    eval_defender_first_stop_step_expert_attacker_means, eval_defender_first_stop_step_expert_attacker_stds, \
    eval_defender_second_stop_step_expert_attacker_data, \
    eval_defender_second_stop_step_expert_attacker_means, eval_defender_second_stop_step_expert_attacker_stds, \
    eval_defender_third_stop_step_expert_attacker_data, eval_defender_third_stop_step_expert_attacker_means, \
    eval_defender_third_stop_step_expert_attacker_stds, eval_defender_fourth_stop_step_expert_attacker_data, \
    eval_defender_fourth_stop_step_expert_attacker_means, eval_defender_fourth_stop_step_expert_attacker_stds, \
    eval_defender_stops_remaining_expert_attacker_data, eval_defender_stops_remaining_expert_attacker_means, \
    eval_defender_stops_remaining_expert_attacker_stds, eval_optimal_first_stop_step_expert_attacker_data, \
    eval_optimal_first_stop_step_expert_attacker_means, eval_optimal_first_stop_step_expert_attacker_stds, \
    eval_optimal_second_stop_step_expert_attacker_data, eval_optimal_second_stop_step_expert_attacker_means, \
    eval_optimal_second_stop_step_expert_attacker_stds, eval_optimal_third_stop_step_expert_attacker_data, \
    eval_optimal_third_stop_step_expert_attacker_means, eval_optimal_third_stop_step_expert_attacker_stds, \
    eval_optimal_fourth_stop_step_expert_attacker_data, eval_optimal_fourth_stop_step_expert_attacker_means, \
    eval_optimal_fourth_stop_step_expert_attacker_stds, eval_optimal_stops_remaining_expert_attacker_data, \
    eval_optimal_stops_remaining_expert_attacker_means, eval_optimal_stops_remaining_expert_attacker_stds, \
    eval_snort_severe_baseline_first_stop_step_expert_attacker_data, \
    eval_snort_severe_baseline_first_stop_step_expert_attacker_means, \
    eval_snort_severe_baseline_first_stop_step_expert_attacker_stds, \
    eval_snort_severe_baseline_second_stop_step_expert_attacker_data, \
    eval_snort_severe_baseline_second_stop_step_expert_attacker_means, \
    eval_snort_severe_baseline_second_stop_step_expert_attacker_stds, \
    eval_snort_severe_baseline_third_stop_step_expert_attacker_data, \
    eval_snort_severe_baseline_third_stop_step_expert_attacker_means, \
    eval_snort_severe_baseline_third_stop_step_expert_attacker_stds, \
    eval_snort_severe_baseline_fourth_stop_step_expert_attacker_data, \
    eval_snort_severe_baseline_fourth_stop_step_expert_attacker_means, \
    eval_snort_severe_baseline_fourth_stop_step_expert_attacker_stds, \
    eval_snort_severe_baseline_stops_remaining_expert_attacker_data, \
    eval_snort_severe_baseline_stops_remaining_expert_attacker_means, \
    eval_snort_severe_baseline_stops_remaining_expert_attacker_stds, \
    eval_step_baseline_first_stop_step_expert_attacker_data, \
    eval_step_baseline_first_stop_step_expert_attacker_means, \
    eval_step_baseline_first_stop_step_expert_attacker_stds, \
    eval_step_baseline_second_stop_step_expert_attacker_data, \
    eval_step_baseline_second_stop_step_expert_attacker_means, \
    eval_step_baseline_second_stop_step_expert_attacker_stds, \
    eval_step_baseline_third_stop_step_expert_attacker_data, \
    eval_step_baseline_third_stop_step_expert_attacker_means, \
    eval_step_baseline_third_stop_step_expert_attacker_stds, \
    eval_step_baseline_fourth_stop_step_expert_attacker_data, \
    eval_step_baseline_fourth_stop_step_expert_attacker_means, \
    eval_step_baseline_fourth_stop_step_expert_attacker_stds, \
    eval_step_baseline_stops_remaining_expert_attacker_data, \
    eval_step_baseline_stops_remaining_expert_attacker_means, \
    eval_step_baseline_stops_remaining_expert_attacker_stds, \
    eval_optimal_episode_steps_expert_attacker_data, eval_optimal_episode_steps_expert_attacker_means, \
    eval_optimal_episode_steps_expert_attacker_stds, \
    avg_eval_2_rewards_data_expert_attacker, avg_eval_2_rewards_means_expert_attacker, \
    avg_eval_2_rewards_stds_expert_attacker, \
    avg_eval_2_steps_data_expert_attacker, avg_eval_2_steps_means_expert_attacker, \
    avg_eval_2_steps_stds_expert_attacker, \
    avg_eval_2_caught_frac_data_expert_attacker, avg_eval_2_caught_frac_means_expert_attacker, \
    avg_eval_2_caught_frac_stds_expert_attacker, \
    avg_eval_2_early_stopping_frac_data_expert_attacker, avg_eval_2_early_stopping_means_expert_attacker, \
    avg_eval_2_early_stopping_stds_expert_attacker, avg_eval_2_intrusion_frac_data_expert_attacker, \
    avg_eval_2_intrusion_means_expert_attacker, \
    avg_eval_2_intrusion_stds_expert_attacker, \
    avg_eval_2_i_steps_data_expert_attacker, avg_eval_2_i_steps_means_expert_attacker, \
    avg_eval_2_i_steps_stds_expert_attacker, \
    avg_eval_2_uncaught_intrusion_steps_data_expert_attacker, \
    avg_eval_2_uncaught_intrusion_steps_means_expert_attacker, \
    avg_eval_2_uncaught_intrusion_steps_stds_expert_attacker, \
    avg_eval_2_optimal_defender_rewards_expert_attacker_data, \
    avg_eval_2_optimal_defender_rewards_expert_attacker_means, \
    avg_eval_2_optimal_defender_rewards_expert_attacker_stds, \
    eval_2_snort_severe_baseline_rewards_data_expert_attacker, \
    eval_2_snort_severe_baseline_rewards_means_expert_attacker, \
    eval_2_snort_severe_baseline_rewards_stds_expert_attacker, \
    eval_2_step_baseline_rewards_data_expert_attacker, \
    eval_2_step_baseline_rewards_means_expert_attacker, eval_2_step_baseline_rewards_stds_expert_attacker, \
    eval_2_snort_severe_baseline_steps_data_expert_attacker, \
    eval_2_snort_severe_baseline_steps_means_expert_attacker, \
    eval_2_snort_severe_baseline_steps_stds_expert_attacker, \
    eval_2_step_baseline_steps_data_expert_attacker, eval_2_step_baseline_steps_means_expert_attacker, \
    eval_2_step_baseline_steps_stds_expert_attacker, \
    eval_2_snort_severe_baseline_early_stopping_data_expert_attacker, \
    eval_2_snort_severe_baseline_early_stopping_means_expert_attacker, \
    eval_2_snort_severe_baseline_early_stopping_stds_expert_attacker, \
    eval_2_step_baseline_early_stopping_data_expert_attacker, \
    eval_2_step_baseline_early_stopping_means_expert_attacker, \
    eval_2_step_baseline_early_stopping_stds_expert_attacker, \
    eval_2_snort_severe_baseline_caught_attacker_data_expert_attacker, \
    eval_2_snort_severe_baseline_caught_attacker_means_expert_attacker, \
    eval_2_snort_severe_baseline_caught_attacker_stds_expert_attacker, \
    eval_2_step_baseline_caught_attacker_data_expert_attacker, \
    eval_2_step_baseline_caught_attacker_means_expert_attacker, \
    eval_2_step_baseline_caught_attacker_stds_expert_attacker, \
    eval_2_snort_severe_baseline_uncaught_intrusion_steps_data_expert_attacker, \
    eval_2_snort_severe_baseline_uncaught_intrusion_steps_means_expert_attacker, \
    eval_2_snort_severe_baseline_uncaught_intrusion_steps_stds_expert_attacker, \
    eval_2_step_baseline_uncaught_intrusion_steps_data_expert_attacker, \
    eval_2_step_baseline_uncaught_intrusion_steps_means_expert_attacker, \
    eval_2_step_baseline_uncaught_intrusion_steps_stds_expert_attacker, \
    eval_2_defender_first_stop_step_expert_attacker_data, \
    eval_2_defender_first_stop_step_expert_attacker_means, eval_2_defender_first_stop_step_expert_attacker_stds, \
    eval_2_defender_second_stop_step_expert_attacker_data, \
    eval_2_defender_second_stop_step_expert_attacker_means, eval_2_defender_second_stop_step_expert_attacker_stds, \
    eval_2_defender_third_stop_step_expert_attacker_data, eval_2_defender_third_stop_step_expert_attacker_means, \
    eval_2_defender_third_stop_step_expert_attacker_stds, eval_2_defender_fourth_stop_step_expert_attacker_data, \
    eval_2_defender_fourth_stop_step_expert_attacker_means, eval_2_defender_fourth_stop_step_expert_attacker_stds, \
    eval_2_defender_stops_remaining_expert_attacker_data, eval_2_defender_stops_remaining_expert_attacker_means, \
    eval_2_defender_stops_remaining_expert_attacker_stds, eval_2_optimal_first_stop_step_expert_attacker_data, \
    eval_2_optimal_first_stop_step_expert_attacker_means, eval_2_optimal_first_stop_step_expert_attacker_stds, \
    eval_2_optimal_second_stop_step_expert_attacker_data, eval_2_optimal_second_stop_step_expert_attacker_means, \
    eval_2_optimal_second_stop_step_expert_attacker_stds, eval_2_optimal_third_stop_step_expert_attacker_data, \
    eval_2_optimal_third_stop_step_expert_attacker_means, eval_2_optimal_third_stop_step_expert_attacker_stds, \
    eval_2_optimal_fourth_stop_step_expert_attacker_data, eval_2_optimal_fourth_stop_step_expert_attacker_means, \
    eval_2_optimal_fourth_stop_step_expert_attacker_stds, eval_2_optimal_stops_remaining_expert_attacker_data, \
    eval_2_optimal_stops_remaining_expert_attacker_means, eval_2_optimal_stops_remaining_expert_attacker_stds, \
    eval_2_snort_severe_baseline_first_stop_step_expert_attacker_data, \
    eval_2_snort_severe_baseline_first_stop_step_expert_attacker_means, \
    eval_2_snort_severe_baseline_first_stop_step_expert_attacker_stds, \
    eval_2_snort_severe_baseline_second_stop_step_expert_attacker_data, \
    eval_2_snort_severe_baseline_second_stop_step_expert_attacker_means, \
    eval_2_snort_severe_baseline_second_stop_step_expert_attacker_stds, \
    eval_2_snort_severe_baseline_third_stop_step_expert_attacker_data, \
    eval_2_snort_severe_baseline_third_stop_step_expert_attacker_means, \
    eval_2_snort_severe_baseline_third_stop_step_expert_attacker_stds, \
    eval_2_snort_severe_baseline_fourth_stop_step_expert_attacker_data, \
    eval_2_snort_severe_baseline_fourth_stop_step_expert_attacker_means, \
    eval_2_snort_severe_baseline_fourth_stop_step_expert_attacker_stds, \
    eval_2_snort_severe_baseline_stops_remaining_expert_attacker_data, \
    eval_2_snort_severe_baseline_stops_remaining_expert_attacker_means, \
    eval_2_snort_severe_baseline_stops_remaining_expert_attacker_stds, \
    eval_2_step_baseline_first_stop_step_expert_attacker_data, \
    eval_2_step_baseline_first_stop_step_expert_attacker_means, \
    eval_2_step_baseline_first_stop_step_expert_attacker_stds, \
    eval_2_step_baseline_second_stop_step_expert_attacker_data, \
    eval_2_step_baseline_second_stop_step_expert_attacker_means, \
    eval_2_step_baseline_second_stop_step_expert_attacker_stds, \
    eval_2_step_baseline_third_stop_step_expert_attacker_data, \
    eval_2_step_baseline_third_stop_step_expert_attacker_means, \
    eval_2_step_baseline_third_stop_step_expert_attacker_stds, \
    eval_2_step_baseline_fourth_stop_step_expert_attacker_data, \
    eval_2_step_baseline_fourth_stop_step_expert_attacker_means, \
    eval_2_step_baseline_fourth_stop_step_expert_attacker_stds, \
    eval_2_step_baseline_stops_remaining_expert_attacker_data, \
    eval_2_step_baseline_stops_remaining_expert_attacker_means, \
    eval_2_step_baseline_stops_remaining_expert_attacker_stds, \
    eval_2_optimal_episode_steps_expert_attacker_data, eval_2_optimal_episode_steps_expert_attacker_means, \
    eval_2_optimal_episode_steps_expert_attacker_stds \
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
        avg_train_uncaught_intrusion_steps_data_novice_attacker,
        avg_train_uncaught_intrusion_steps_means_novice_attacker,
        avg_train_uncaught_intrusion_steps_stds_novice_attacker,
        avg_train_optimal_defender_rewards_novice_attacker_data,
        avg_train_optimal_defender_rewards_novice_attacker_means,
        avg_train_optimal_defender_rewards_novice_attacker_stds,
        train_snort_severe_baseline_rewards_data_novice_attacker,
        train_snort_severe_baseline_rewards_means_novice_attacker,
        train_snort_severe_baseline_rewards_stds_novice_attacker, train_step_baseline_rewards_data_novice_attacker,
        train_step_baseline_rewards_means_novice_attacker, train_step_baseline_rewards_stds_novice_attacker,
        train_snort_severe_baseline_steps_data_novice_attacker,
        train_snort_severe_baseline_steps_means_novice_attacker,
        train_snort_severe_baseline_steps_stds_novice_attacker,
        train_step_baseline_steps_data_novice_attacker, train_step_baseline_steps_means_novice_attacker,
        train_step_baseline_steps_stds_novice_attacker,
        train_snort_severe_baseline_early_stopping_data_novice_attacker,
        train_snort_severe_baseline_early_stopping_means_novice_attacker,
        train_snort_severe_baseline_early_stopping_stds_novice_attacker,
        train_step_baseline_early_stopping_data_novice_attacker,
        train_step_baseline_early_stopping_means_novice_attacker,
        train_step_baseline_early_stopping_stds_novice_attacker,
        train_snort_severe_baseline_caught_attacker_data_novice_attacker,
        train_snort_severe_baseline_caught_attacker_means_novice_attacker,
        train_snort_severe_baseline_caught_attacker_stds_novice_attacker,
        train_step_baseline_caught_attacker_data_novice_attacker,
        train_step_baseline_caught_attacker_means_novice_attacker,
        train_step_baseline_caught_attacker_stds_novice_attacker,
        train_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker,
        train_snort_severe_baseline_uncaught_intrusion_steps_means_novice_attacker,
        train_snort_severe_baseline_uncaught_intrusion_steps_stds_novice_attacker,
        train_step_baseline_uncaught_intrusion_steps_data_novice_attacker,
        train_step_baseline_uncaught_intrusion_steps_means_novice_attacker,
        train_step_baseline_uncaught_intrusion_steps_stds_novice_attacker,
        train_defender_first_stop_step_novice_attacker_data,
        train_defender_first_stop_step_novice_attacker_means, train_defender_first_stop_step_novice_attacker_stds,
        train_defender_second_stop_step_novice_attacker_data,
        train_defender_second_stop_step_novice_attacker_means, train_defender_second_stop_step_novice_attacker_stds,
        train_defender_third_stop_step_novice_attacker_data, train_defender_third_stop_step_novice_attacker_means,
        train_defender_third_stop_step_novice_attacker_stds, train_defender_fourth_stop_step_novice_attacker_data,
        train_defender_fourth_stop_step_novice_attacker_means, train_defender_fourth_stop_step_novice_attacker_stds,
        train_defender_stops_remaining_novice_attacker_data, train_defender_stops_remaining_novice_attacker_means,
        train_defender_stops_remaining_novice_attacker_stds, train_optimal_first_stop_step_novice_attacker_data,
        train_optimal_first_stop_step_novice_attacker_means, train_optimal_first_stop_step_novice_attacker_stds,
        train_optimal_second_stop_step_novice_attacker_data, train_optimal_second_stop_step_novice_attacker_means,
        train_optimal_second_stop_step_novice_attacker_stds, train_optimal_third_stop_step_novice_attacker_data,
        train_optimal_third_stop_step_novice_attacker_means, train_optimal_third_stop_step_novice_attacker_stds,
        train_optimal_fourth_stop_step_novice_attacker_data, train_optimal_fourth_stop_step_novice_attacker_means,
        train_optimal_fourth_stop_step_novice_attacker_stds, train_optimal_stops_remaining_novice_attacker_data,
        train_optimal_stops_remaining_novice_attacker_means, train_optimal_stops_remaining_novice_attacker_stds,
        train_snort_severe_baseline_first_stop_step_novice_attacker_data,
        train_snort_severe_baseline_first_stop_step_novice_attacker_means,
        train_snort_severe_baseline_first_stop_step_novice_attacker_stds,
        train_snort_severe_baseline_second_stop_step_novice_attacker_data,
        train_snort_severe_baseline_second_stop_step_novice_attacker_means,
        train_snort_severe_baseline_second_stop_step_novice_attacker_stds,
        train_snort_severe_baseline_third_stop_step_novice_attacker_data,
        train_snort_severe_baseline_third_stop_step_novice_attacker_means,
        train_snort_severe_baseline_third_stop_step_novice_attacker_stds,
        train_snort_severe_baseline_fourth_stop_step_novice_attacker_data,
        train_snort_severe_baseline_fourth_stop_step_novice_attacker_means,
        train_snort_severe_baseline_fourth_stop_step_novice_attacker_stds,
        train_snort_severe_baseline_stops_remaining_novice_attacker_data,
        train_snort_severe_baseline_stops_remaining_novice_attacker_means,
        train_snort_severe_baseline_stops_remaining_novice_attacker_stds,
        train_step_baseline_first_stop_step_novice_attacker_data,
        train_step_baseline_first_stop_step_novice_attacker_means,
        train_step_baseline_first_stop_step_novice_attacker_stds,
        train_step_baseline_second_stop_step_novice_attacker_data,
        train_step_baseline_second_stop_step_novice_attacker_means,
        train_step_baseline_second_stop_step_novice_attacker_stds,
        train_step_baseline_third_stop_step_novice_attacker_data,
        train_step_baseline_third_stop_step_novice_attacker_means,
        train_step_baseline_third_stop_step_novice_attacker_stds,
        train_step_baseline_fourth_stop_step_novice_attacker_data,
        train_step_baseline_fourth_stop_step_novice_attacker_means,
        train_step_baseline_fourth_stop_step_novice_attacker_stds,
        train_step_baseline_stops_remaining_novice_attacker_data,
        train_step_baseline_stops_remaining_novice_attacker_means,
        train_step_baseline_stops_remaining_novice_attacker_stds,
        train_optimal_episode_steps_novice_attacker_data, train_optimal_episode_steps_novice_attacker_means,
        train_optimal_episode_steps_novice_attacker_stds,
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
        avg_eval_i_steps_stds_novice_attacker,
        avg_eval_uncaught_intrusion_steps_data_novice_attacker,
        avg_eval_uncaught_intrusion_steps_means_novice_attacker,
        avg_eval_uncaught_intrusion_steps_stds_novice_attacker,
        avg_eval_optimal_defender_rewards_novice_attacker_data,
        avg_eval_optimal_defender_rewards_novice_attacker_means,
        avg_eval_optimal_defender_rewards_novice_attacker_stds,
        eval_snort_severe_baseline_rewards_data_novice_attacker,
        eval_snort_severe_baseline_rewards_means_novice_attacker,
        eval_snort_severe_baseline_rewards_stds_novice_attacker,
        eval_step_baseline_rewards_data_novice_attacker, eval_step_baseline_rewards_means_novice_attacker,
        eval_step_baseline_rewards_stds_novice_attacker,
        eval_snort_severe_baseline_steps_data_novice_attacker,
        eval_snort_severe_baseline_steps_means_novice_attacker,
        eval_snort_severe_baseline_steps_stds_novice_attacker,
        eval_step_baseline_steps_data_novice_attacker, eval_step_baseline_steps_means_novice_attacker,
        eval_step_baseline_steps_stds_novice_attacker,
        eval_snort_severe_baseline_early_stopping_data_novice_attacker,
        eval_snort_severe_baseline_early_stopping_means_novice_attacker,
        eval_snort_severe_baseline_early_stopping_stds_novice_attacker,
        eval_step_baseline_early_stopping_data_novice_attacker,
        eval_step_baseline_early_stopping_means_novice_attacker,
        eval_step_baseline_early_stopping_stds_novice_attacker,
        eval_snort_severe_baseline_caught_attacker_data_novice_attacker,
        eval_snort_severe_baseline_caught_attacker_means_novice_attacker,
        eval_snort_severe_baseline_caught_attacker_stds_novice_attacker,
        eval_step_baseline_caught_attacker_data_novice_attacker,
        eval_step_baseline_caught_attacker_means_novice_attacker,
        eval_step_baseline_caught_attacker_stds_novice_attacker,
        eval_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker,
        eval_snort_severe_baseline_uncaught_intrusion_steps_means_novice_attacker,
        eval_snort_severe_baseline_uncaught_intrusion_steps_stds_novice_attacker,
        eval_step_baseline_uncaught_intrusion_steps_data_novice_attacker,
        eval_step_baseline_uncaught_intrusion_steps_means_novice_attacker,
        eval_step_baseline_uncaught_intrusion_steps_stds_novice_attacker,
        eval_defender_first_stop_step_novice_attacker_data,
        eval_defender_first_stop_step_novice_attacker_means, eval_defender_first_stop_step_novice_attacker_stds,
        eval_defender_second_stop_step_novice_attacker_data,
        eval_defender_second_stop_step_novice_attacker_means, eval_defender_second_stop_step_novice_attacker_stds,
        eval_defender_third_stop_step_novice_attacker_data, eval_defender_third_stop_step_novice_attacker_means,
        eval_defender_third_stop_step_novice_attacker_stds, eval_defender_fourth_stop_step_novice_attacker_data,
        eval_defender_fourth_stop_step_novice_attacker_means, eval_defender_fourth_stop_step_novice_attacker_stds,
        eval_defender_stops_remaining_novice_attacker_data, eval_defender_stops_remaining_novice_attacker_means,
        eval_defender_stops_remaining_novice_attacker_stds, eval_optimal_first_stop_step_novice_attacker_data,
        eval_optimal_first_stop_step_novice_attacker_means, eval_optimal_first_stop_step_novice_attacker_stds,
        eval_optimal_second_stop_step_novice_attacker_data, eval_optimal_second_stop_step_novice_attacker_means,
        eval_optimal_second_stop_step_novice_attacker_stds, eval_optimal_third_stop_step_novice_attacker_data,
        eval_optimal_third_stop_step_novice_attacker_means, eval_optimal_third_stop_step_novice_attacker_stds,
        eval_optimal_fourth_stop_step_novice_attacker_data, eval_optimal_fourth_stop_step_novice_attacker_means,
        eval_optimal_fourth_stop_step_novice_attacker_stds, eval_optimal_stops_remaining_novice_attacker_data,
        eval_optimal_stops_remaining_novice_attacker_means, eval_optimal_stops_remaining_novice_attacker_stds,
        eval_snort_severe_baseline_first_stop_step_novice_attacker_data,
        eval_snort_severe_baseline_first_stop_step_novice_attacker_means,
        eval_snort_severe_baseline_first_stop_step_novice_attacker_stds,
        eval_snort_severe_baseline_second_stop_step_novice_attacker_data,
        eval_snort_severe_baseline_second_stop_step_novice_attacker_means,
        eval_snort_severe_baseline_second_stop_step_novice_attacker_stds,
        eval_snort_severe_baseline_third_stop_step_novice_attacker_data,
        eval_snort_severe_baseline_third_stop_step_novice_attacker_means,
        eval_snort_severe_baseline_third_stop_step_novice_attacker_stds,
        eval_snort_severe_baseline_fourth_stop_step_novice_attacker_data,
        eval_snort_severe_baseline_fourth_stop_step_novice_attacker_means,
        eval_snort_severe_baseline_fourth_stop_step_novice_attacker_stds,
        eval_snort_severe_baseline_stops_remaining_novice_attacker_data,
        eval_snort_severe_baseline_stops_remaining_novice_attacker_means,
        eval_snort_severe_baseline_stops_remaining_novice_attacker_stds,
        eval_step_baseline_first_stop_step_novice_attacker_data,
        eval_step_baseline_first_stop_step_novice_attacker_means,
        eval_step_baseline_first_stop_step_novice_attacker_stds,
        eval_step_baseline_second_stop_step_novice_attacker_data,
        eval_step_baseline_second_stop_step_novice_attacker_means,
        eval_step_baseline_second_stop_step_novice_attacker_stds,
        eval_step_baseline_third_stop_step_novice_attacker_data,
        eval_step_baseline_third_stop_step_novice_attacker_means,
        eval_step_baseline_third_stop_step_novice_attacker_stds,
        eval_step_baseline_fourth_stop_step_novice_attacker_data,
        eval_step_baseline_fourth_stop_step_novice_attacker_means,
        eval_step_baseline_fourth_stop_step_novice_attacker_stds,
        eval_step_baseline_stops_remaining_novice_attacker_data,
        eval_step_baseline_stops_remaining_novice_attacker_means,
        eval_step_baseline_stops_remaining_novice_attacker_stds,
        eval_optimal_episode_steps_novice_attacker_data, eval_optimal_episode_steps_novice_attacker_means,
        eval_optimal_episode_steps_novice_attacker_stds,
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
        avg_eval_2_i_steps_stds_novice_attacker,
        avg_eval_2_uncaught_intrusion_steps_data_novice_attacker,
        avg_eval_2_uncaught_intrusion_steps_means_novice_attacker,
        avg_eval_2_uncaught_intrusion_steps_stds_novice_attacker,
        avg_eval_2_optimal_defender_rewards_novice_attacker_data,
        avg_eval_2_optimal_defender_rewards_novice_attacker_means,
        avg_eval_2_optimal_defender_rewards_novice_attacker_stds,
        eval_2_snort_severe_baseline_rewards_data_novice_attacker,
        eval_2_snort_severe_baseline_rewards_means_novice_attacker,
        eval_2_snort_severe_baseline_rewards_stds_novice_attacker,
        eval_2_step_baseline_rewards_data_novice_attacker,
        eval_2_step_baseline_rewards_means_novice_attacker, eval_2_step_baseline_rewards_stds_novice_attacker,
        eval_2_snort_severe_baseline_steps_data_novice_attacker,
        eval_2_snort_severe_baseline_steps_means_novice_attacker,
        eval_2_snort_severe_baseline_steps_stds_novice_attacker,
        eval_2_step_baseline_steps_data_novice_attacker, eval_2_step_baseline_steps_means_novice_attacker,
        eval_2_step_baseline_steps_stds_novice_attacker,
        eval_2_snort_severe_baseline_early_stopping_data_novice_attacker,
        eval_2_snort_severe_baseline_early_stopping_means_novice_attacker,
        eval_2_snort_severe_baseline_early_stopping_stds_novice_attacker,
        eval_2_step_baseline_early_stopping_data_novice_attacker,
        eval_2_step_baseline_early_stopping_means_novice_attacker,
        eval_2_step_baseline_early_stopping_stds_novice_attacker,
        eval_2_snort_severe_baseline_caught_attacker_data_novice_attacker,
        eval_2_snort_severe_baseline_caught_attacker_means_novice_attacker,
        eval_2_snort_severe_baseline_caught_attacker_stds_novice_attacker,
        eval_2_step_baseline_caught_attacker_data_novice_attacker,
        eval_2_step_baseline_caught_attacker_means_novice_attacker,
        eval_2_step_baseline_caught_attacker_stds_novice_attacker,
        eval_2_snort_severe_baseline_uncaught_intrusion_steps_data_novice_attacker,
        eval_2_snort_severe_baseline_uncaught_intrusion_steps_means_novice_attacker,
        eval_2_snort_severe_baseline_uncaught_intrusion_steps_stds_novice_attacker,
        eval_2_step_baseline_uncaught_intrusion_steps_data_novice_attacker,
        eval_2_step_baseline_uncaught_intrusion_steps_means_novice_attacker,
        eval_2_step_baseline_uncaught_intrusion_steps_stds_novice_attacker,
        eval_2_defender_first_stop_step_novice_attacker_data,
        eval_2_defender_first_stop_step_novice_attacker_means, eval_2_defender_first_stop_step_novice_attacker_stds,
        eval_2_defender_second_stop_step_novice_attacker_data,
        eval_2_defender_second_stop_step_novice_attacker_means, eval_2_defender_second_stop_step_novice_attacker_stds,
        eval_2_defender_third_stop_step_novice_attacker_data, eval_2_defender_third_stop_step_novice_attacker_means,
        eval_2_defender_third_stop_step_novice_attacker_stds, eval_2_defender_fourth_stop_step_novice_attacker_data,
        eval_2_defender_fourth_stop_step_novice_attacker_means, eval_2_defender_fourth_stop_step_novice_attacker_stds,
        eval_2_defender_stops_remaining_novice_attacker_data, eval_2_defender_stops_remaining_novice_attacker_means,
        eval_2_defender_stops_remaining_novice_attacker_stds, eval_2_optimal_first_stop_step_novice_attacker_data,
        eval_2_optimal_first_stop_step_novice_attacker_means, eval_2_optimal_first_stop_step_novice_attacker_stds,
        eval_2_optimal_second_stop_step_novice_attacker_data, eval_2_optimal_second_stop_step_novice_attacker_means,
        eval_2_optimal_second_stop_step_novice_attacker_stds, eval_2_optimal_third_stop_step_novice_attacker_data,
        eval_2_optimal_third_stop_step_novice_attacker_means, eval_2_optimal_third_stop_step_novice_attacker_stds,
        eval_2_optimal_fourth_stop_step_novice_attacker_data, eval_2_optimal_fourth_stop_step_novice_attacker_means,
        eval_2_optimal_fourth_stop_step_novice_attacker_stds, eval_2_optimal_stops_remaining_novice_attacker_data,
        eval_2_optimal_stops_remaining_novice_attacker_means, eval_2_optimal_stops_remaining_novice_attacker_stds,
        eval_2_snort_severe_baseline_first_stop_step_novice_attacker_data,
        eval_2_snort_severe_baseline_first_stop_step_novice_attacker_means,
        eval_2_snort_severe_baseline_first_stop_step_novice_attacker_stds,
        eval_2_snort_severe_baseline_second_stop_step_novice_attacker_data,
        eval_2_snort_severe_baseline_second_stop_step_novice_attacker_means,
        eval_2_snort_severe_baseline_second_stop_step_novice_attacker_stds,
        eval_2_snort_severe_baseline_third_stop_step_novice_attacker_data,
        eval_2_snort_severe_baseline_third_stop_step_novice_attacker_means,
        eval_2_snort_severe_baseline_third_stop_step_novice_attacker_stds,
        eval_2_snort_severe_baseline_fourth_stop_step_novice_attacker_data,
        eval_2_snort_severe_baseline_fourth_stop_step_novice_attacker_means,
        eval_2_snort_severe_baseline_fourth_stop_step_novice_attacker_stds,
        eval_2_snort_severe_baseline_stops_remaining_novice_attacker_data,
        eval_2_snort_severe_baseline_stops_remaining_novice_attacker_means,
        eval_2_snort_severe_baseline_stops_remaining_novice_attacker_stds,
        eval_2_step_baseline_first_stop_step_novice_attacker_data,
        eval_2_step_baseline_first_stop_step_novice_attacker_means,
        eval_2_step_baseline_first_stop_step_novice_attacker_stds,
        eval_2_step_baseline_second_stop_step_novice_attacker_data,
        eval_2_step_baseline_second_stop_step_novice_attacker_means,
        eval_2_step_baseline_second_stop_step_novice_attacker_stds,
        eval_2_step_baseline_third_stop_step_novice_attacker_data,
        eval_2_step_baseline_third_stop_step_novice_attacker_means,
        eval_2_step_baseline_third_stop_step_novice_attacker_stds,
        eval_2_step_baseline_fourth_stop_step_novice_attacker_data,
        eval_2_step_baseline_fourth_stop_step_novice_attacker_means,
        eval_2_step_baseline_fourth_stop_step_novice_attacker_stds,
        eval_2_step_baseline_stops_remaining_novice_attacker_data,
        eval_2_step_baseline_stops_remaining_novice_attacker_means,
        eval_2_step_baseline_stops_remaining_novice_attacker_stds,
        eval_2_optimal_episode_steps_novice_attacker_data, eval_2_optimal_episode_steps_novice_attacker_means,
        eval_2_optimal_episode_steps_novice_attacker_stds,
        avg_train_rewards_data_experienced_attacker, avg_train_rewards_means_experienced_attacker,
        avg_train_rewards_stds_experienced_attacker,
        avg_train_steps_data_experienced_attacker, avg_train_steps_means_experienced_attacker,
        avg_train_steps_stds_experienced_attacker,
        avg_train_caught_frac_data_experienced_attacker, avg_train_caught_frac_means_experienced_attacker,
        avg_train_caught_frac_stds_experienced_attacker,
        avg_train_early_stopping_frac_data_experienced_attacker, avg_train_early_stopping_means_experienced_attacker,
        avg_train_early_stopping_stds_experienced_attacker, avg_train_intrusion_frac_data_experienced_attacker,
        avg_train_intrusion_means_experienced_attacker,
        avg_train_intrusion_stds_experienced_attacker,
        avg_train_i_steps_data_experienced_attacker, avg_train_i_steps_means_experienced_attacker,
        avg_train_i_steps_stds_experienced_attacker,
        avg_train_uncaught_intrusion_steps_data_experienced_attacker,
        avg_train_uncaught_intrusion_steps_means_experienced_attacker,
        avg_train_uncaught_intrusion_steps_stds_experienced_attacker,
        avg_train_optimal_defender_rewards_experienced_attacker_data,
        avg_train_optimal_defender_rewards_experienced_attacker_means,
        avg_train_optimal_defender_rewards_experienced_attacker_stds,
        train_snort_severe_baseline_rewards_data_experienced_attacker,
        train_snort_severe_baseline_rewards_means_experienced_attacker,
        train_snort_severe_baseline_rewards_stds_experienced_attacker, train_step_baseline_rewards_data_experienced_attacker,
        train_step_baseline_rewards_means_experienced_attacker, train_step_baseline_rewards_stds_experienced_attacker,
        train_snort_severe_baseline_steps_data_experienced_attacker,
        train_snort_severe_baseline_steps_means_experienced_attacker,
        train_snort_severe_baseline_steps_stds_experienced_attacker,
        train_step_baseline_steps_data_experienced_attacker, train_step_baseline_steps_means_experienced_attacker,
        train_step_baseline_steps_stds_experienced_attacker,
        train_snort_severe_baseline_early_stopping_data_experienced_attacker,
        train_snort_severe_baseline_early_stopping_means_experienced_attacker,
        train_snort_severe_baseline_early_stopping_stds_experienced_attacker,
        train_step_baseline_early_stopping_data_experienced_attacker,
        train_step_baseline_early_stopping_means_experienced_attacker,
        train_step_baseline_early_stopping_stds_experienced_attacker,
        train_snort_severe_baseline_caught_attacker_data_experienced_attacker,
        train_snort_severe_baseline_caught_attacker_means_experienced_attacker,
        train_snort_severe_baseline_caught_attacker_stds_experienced_attacker,
        train_step_baseline_caught_attacker_data_experienced_attacker,
        train_step_baseline_caught_attacker_means_experienced_attacker,
        train_step_baseline_caught_attacker_stds_experienced_attacker,
        train_snort_severe_baseline_uncaught_intrusion_steps_data_experienced_attacker,
        train_snort_severe_baseline_uncaught_intrusion_steps_means_experienced_attacker,
        train_snort_severe_baseline_uncaught_intrusion_steps_stds_experienced_attacker,
        train_step_baseline_uncaught_intrusion_steps_data_experienced_attacker,
        train_step_baseline_uncaught_intrusion_steps_means_experienced_attacker,
        train_step_baseline_uncaught_intrusion_steps_stds_experienced_attacker,
        train_defender_first_stop_step_experienced_attacker_data,
        train_defender_first_stop_step_experienced_attacker_means, train_defender_first_stop_step_experienced_attacker_stds,
        train_defender_second_stop_step_experienced_attacker_data,
        train_defender_second_stop_step_experienced_attacker_means, train_defender_second_stop_step_experienced_attacker_stds,
        train_defender_third_stop_step_experienced_attacker_data, train_defender_third_stop_step_experienced_attacker_means,
        train_defender_third_stop_step_experienced_attacker_stds, train_defender_fourth_stop_step_experienced_attacker_data,
        train_defender_fourth_stop_step_experienced_attacker_means, train_defender_fourth_stop_step_experienced_attacker_stds,
        train_defender_stops_remaining_experienced_attacker_data, train_defender_stops_remaining_experienced_attacker_means,
        train_defender_stops_remaining_experienced_attacker_stds, train_optimal_first_stop_step_experienced_attacker_data,
        train_optimal_first_stop_step_experienced_attacker_means, train_optimal_first_stop_step_experienced_attacker_stds,
        train_optimal_second_stop_step_experienced_attacker_data, train_optimal_second_stop_step_experienced_attacker_means,
        train_optimal_second_stop_step_experienced_attacker_stds, train_optimal_third_stop_step_experienced_attacker_data,
        train_optimal_third_stop_step_experienced_attacker_means, train_optimal_third_stop_step_experienced_attacker_stds,
        train_optimal_fourth_stop_step_experienced_attacker_data, train_optimal_fourth_stop_step_experienced_attacker_means,
        train_optimal_fourth_stop_step_experienced_attacker_stds, train_optimal_stops_remaining_experienced_attacker_data,
        train_optimal_stops_remaining_experienced_attacker_means, train_optimal_stops_remaining_experienced_attacker_stds,
        train_snort_severe_baseline_first_stop_step_experienced_attacker_data,
        train_snort_severe_baseline_first_stop_step_experienced_attacker_means,
        train_snort_severe_baseline_first_stop_step_experienced_attacker_stds,
        train_snort_severe_baseline_second_stop_step_experienced_attacker_data,
        train_snort_severe_baseline_second_stop_step_experienced_attacker_means,
        train_snort_severe_baseline_second_stop_step_experienced_attacker_stds,
        train_snort_severe_baseline_third_stop_step_experienced_attacker_data,
        train_snort_severe_baseline_third_stop_step_experienced_attacker_means,
        train_snort_severe_baseline_third_stop_step_experienced_attacker_stds,
        train_snort_severe_baseline_fourth_stop_step_experienced_attacker_data,
        train_snort_severe_baseline_fourth_stop_step_experienced_attacker_means,
        train_snort_severe_baseline_fourth_stop_step_experienced_attacker_stds,
        train_snort_severe_baseline_stops_remaining_experienced_attacker_data,
        train_snort_severe_baseline_stops_remaining_experienced_attacker_means,
        train_snort_severe_baseline_stops_remaining_experienced_attacker_stds,
        train_step_baseline_first_stop_step_experienced_attacker_data,
        train_step_baseline_first_stop_step_experienced_attacker_means,
        train_step_baseline_first_stop_step_experienced_attacker_stds,
        train_step_baseline_second_stop_step_experienced_attacker_data,
        train_step_baseline_second_stop_step_experienced_attacker_means,
        train_step_baseline_second_stop_step_experienced_attacker_stds,
        train_step_baseline_third_stop_step_experienced_attacker_data,
        train_step_baseline_third_stop_step_experienced_attacker_means,
        train_step_baseline_third_stop_step_experienced_attacker_stds,
        train_step_baseline_fourth_stop_step_experienced_attacker_data,
        train_step_baseline_fourth_stop_step_experienced_attacker_means,
        train_step_baseline_fourth_stop_step_experienced_attacker_stds,
        train_step_baseline_stops_remaining_experienced_attacker_data,
        train_step_baseline_stops_remaining_experienced_attacker_means,
        train_step_baseline_stops_remaining_experienced_attacker_stds,
        train_optimal_episode_steps_experienced_attacker_data, train_optimal_episode_steps_experienced_attacker_means,
        train_optimal_episode_steps_experienced_attacker_stds,
        avg_eval_rewards_data_experienced_attacker, avg_eval_rewards_means_experienced_attacker,
        avg_eval_rewards_stds_experienced_attacker,
        avg_eval_steps_data_experienced_attacker, avg_eval_steps_means_experienced_attacker,
        avg_eval_steps_stds_experienced_attacker,
        avg_eval_caught_frac_data_experienced_attacker, avg_eval_caught_frac_means_experienced_attacker,
        avg_eval_caught_frac_stds_experienced_attacker,
        avg_eval_early_stopping_frac_data_experienced_attacker, avg_eval_early_stopping_means_experienced_attacker,
        avg_eval_early_stopping_stds_experienced_attacker, avg_eval_intrusion_frac_data_experienced_attacker,
        avg_eval_intrusion_means_experienced_attacker,
        avg_eval_intrusion_stds_experienced_attacker,
        avg_eval_i_steps_data_experienced_attacker, avg_eval_i_steps_means_experienced_attacker,
        avg_eval_i_steps_stds_experienced_attacker,
        avg_eval_uncaught_intrusion_steps_data_experienced_attacker,
        avg_eval_uncaught_intrusion_steps_means_experienced_attacker,
        avg_eval_uncaught_intrusion_steps_stds_experienced_attacker,
        avg_eval_optimal_defender_rewards_experienced_attacker_data,
        avg_eval_optimal_defender_rewards_experienced_attacker_means,
        avg_eval_optimal_defender_rewards_experienced_attacker_stds,
        eval_snort_severe_baseline_rewards_data_experienced_attacker,
        eval_snort_severe_baseline_rewards_means_experienced_attacker,
        eval_snort_severe_baseline_rewards_stds_experienced_attacker,
        eval_step_baseline_rewards_data_experienced_attacker, eval_step_baseline_rewards_means_experienced_attacker,
        eval_step_baseline_rewards_stds_experienced_attacker,
        eval_snort_severe_baseline_steps_data_experienced_attacker,
        eval_snort_severe_baseline_steps_means_experienced_attacker,
        eval_snort_severe_baseline_steps_stds_experienced_attacker,
        eval_step_baseline_steps_data_experienced_attacker, eval_step_baseline_steps_means_experienced_attacker,
        eval_step_baseline_steps_stds_experienced_attacker,
        eval_snort_severe_baseline_early_stopping_data_experienced_attacker,
        eval_snort_severe_baseline_early_stopping_means_experienced_attacker,
        eval_snort_severe_baseline_early_stopping_stds_experienced_attacker,
        eval_step_baseline_early_stopping_data_experienced_attacker,
        eval_step_baseline_early_stopping_means_experienced_attacker,
        eval_step_baseline_early_stopping_stds_experienced_attacker,
        eval_snort_severe_baseline_caught_attacker_data_experienced_attacker,
        eval_snort_severe_baseline_caught_attacker_means_experienced_attacker,
        eval_snort_severe_baseline_caught_attacker_stds_experienced_attacker,
        eval_step_baseline_caught_attacker_data_experienced_attacker,
        eval_step_baseline_caught_attacker_means_experienced_attacker,
        eval_step_baseline_caught_attacker_stds_experienced_attacker,
        eval_snort_severe_baseline_uncaught_intrusion_steps_data_experienced_attacker,
        eval_snort_severe_baseline_uncaught_intrusion_steps_means_experienced_attacker,
        eval_snort_severe_baseline_uncaught_intrusion_steps_stds_experienced_attacker,
        eval_step_baseline_uncaught_intrusion_steps_data_experienced_attacker,
        eval_step_baseline_uncaught_intrusion_steps_means_experienced_attacker,
        eval_step_baseline_uncaught_intrusion_steps_stds_experienced_attacker,
        eval_defender_first_stop_step_experienced_attacker_data,
        eval_defender_first_stop_step_experienced_attacker_means, eval_defender_first_stop_step_experienced_attacker_stds,
        eval_defender_second_stop_step_experienced_attacker_data,
        eval_defender_second_stop_step_experienced_attacker_means, eval_defender_second_stop_step_experienced_attacker_stds,
        eval_defender_third_stop_step_experienced_attacker_data, eval_defender_third_stop_step_experienced_attacker_means,
        eval_defender_third_stop_step_experienced_attacker_stds, eval_defender_fourth_stop_step_experienced_attacker_data,
        eval_defender_fourth_stop_step_experienced_attacker_means, eval_defender_fourth_stop_step_experienced_attacker_stds,
        eval_defender_stops_remaining_experienced_attacker_data, eval_defender_stops_remaining_experienced_attacker_means,
        eval_defender_stops_remaining_experienced_attacker_stds, eval_optimal_first_stop_step_experienced_attacker_data,
        eval_optimal_first_stop_step_experienced_attacker_means, eval_optimal_first_stop_step_experienced_attacker_stds,
        eval_optimal_second_stop_step_experienced_attacker_data, eval_optimal_second_stop_step_experienced_attacker_means,
        eval_optimal_second_stop_step_experienced_attacker_stds, eval_optimal_third_stop_step_experienced_attacker_data,
        eval_optimal_third_stop_step_experienced_attacker_means, eval_optimal_third_stop_step_experienced_attacker_stds,
        eval_optimal_fourth_stop_step_experienced_attacker_data, eval_optimal_fourth_stop_step_experienced_attacker_means,
        eval_optimal_fourth_stop_step_experienced_attacker_stds, eval_optimal_stops_remaining_experienced_attacker_data,
        eval_optimal_stops_remaining_experienced_attacker_means, eval_optimal_stops_remaining_experienced_attacker_stds,
        eval_snort_severe_baseline_first_stop_step_experienced_attacker_data,
        eval_snort_severe_baseline_first_stop_step_experienced_attacker_means,
        eval_snort_severe_baseline_first_stop_step_experienced_attacker_stds,
        eval_snort_severe_baseline_second_stop_step_experienced_attacker_data,
        eval_snort_severe_baseline_second_stop_step_experienced_attacker_means,
        eval_snort_severe_baseline_second_stop_step_experienced_attacker_stds,
        eval_snort_severe_baseline_third_stop_step_experienced_attacker_data,
        eval_snort_severe_baseline_third_stop_step_experienced_attacker_means,
        eval_snort_severe_baseline_third_stop_step_experienced_attacker_stds,
        eval_snort_severe_baseline_fourth_stop_step_experienced_attacker_data,
        eval_snort_severe_baseline_fourth_stop_step_experienced_attacker_means,
        eval_snort_severe_baseline_fourth_stop_step_experienced_attacker_stds,
        eval_snort_severe_baseline_stops_remaining_experienced_attacker_data,
        eval_snort_severe_baseline_stops_remaining_experienced_attacker_means,
        eval_snort_severe_baseline_stops_remaining_experienced_attacker_stds,
        eval_step_baseline_first_stop_step_experienced_attacker_data,
        eval_step_baseline_first_stop_step_experienced_attacker_means,
        eval_step_baseline_first_stop_step_experienced_attacker_stds,
        eval_step_baseline_second_stop_step_experienced_attacker_data,
        eval_step_baseline_second_stop_step_experienced_attacker_means,
        eval_step_baseline_second_stop_step_experienced_attacker_stds,
        eval_step_baseline_third_stop_step_experienced_attacker_data,
        eval_step_baseline_third_stop_step_experienced_attacker_means,
        eval_step_baseline_third_stop_step_experienced_attacker_stds,
        eval_step_baseline_fourth_stop_step_experienced_attacker_data,
        eval_step_baseline_fourth_stop_step_experienced_attacker_means,
        eval_step_baseline_fourth_stop_step_experienced_attacker_stds,
        eval_step_baseline_stops_remaining_experienced_attacker_data,
        eval_step_baseline_stops_remaining_experienced_attacker_means,
        eval_step_baseline_stops_remaining_experienced_attacker_stds,
        eval_optimal_episode_steps_experienced_attacker_data, eval_optimal_episode_steps_experienced_attacker_means,
        eval_optimal_episode_steps_experienced_attacker_stds,
        avg_eval_2_rewards_data_experienced_attacker, avg_eval_2_rewards_means_experienced_attacker,
        avg_eval_2_rewards_stds_experienced_attacker,
        avg_eval_2_steps_data_experienced_attacker, avg_eval_2_steps_means_experienced_attacker,
        avg_eval_2_steps_stds_experienced_attacker,
        avg_eval_2_caught_frac_data_experienced_attacker, avg_eval_2_caught_frac_means_experienced_attacker,
        avg_eval_2_caught_frac_stds_experienced_attacker,
        avg_eval_2_early_stopping_frac_data_experienced_attacker, avg_eval_2_early_stopping_means_experienced_attacker,
        avg_eval_2_early_stopping_stds_experienced_attacker, avg_eval_2_intrusion_frac_data_experienced_attacker,
        avg_eval_2_intrusion_means_experienced_attacker,
        avg_eval_2_intrusion_stds_experienced_attacker,
        avg_eval_2_i_steps_data_experienced_attacker, avg_eval_2_i_steps_means_experienced_attacker,
        avg_eval_2_i_steps_stds_experienced_attacker,
        avg_eval_2_uncaught_intrusion_steps_data_experienced_attacker,
        avg_eval_2_uncaught_intrusion_steps_means_experienced_attacker,
        avg_eval_2_uncaught_intrusion_steps_stds_experienced_attacker,
        avg_eval_2_optimal_defender_rewards_experienced_attacker_data,
        avg_eval_2_optimal_defender_rewards_experienced_attacker_means,
        avg_eval_2_optimal_defender_rewards_experienced_attacker_stds,
        eval_2_snort_severe_baseline_rewards_data_experienced_attacker,
        eval_2_snort_severe_baseline_rewards_means_experienced_attacker,
        eval_2_snort_severe_baseline_rewards_stds_experienced_attacker,
        eval_2_step_baseline_rewards_data_experienced_attacker,
        eval_2_step_baseline_rewards_means_experienced_attacker, eval_2_step_baseline_rewards_stds_experienced_attacker,
        eval_2_snort_severe_baseline_steps_data_experienced_attacker,
        eval_2_snort_severe_baseline_steps_means_experienced_attacker,
        eval_2_snort_severe_baseline_steps_stds_experienced_attacker,
        eval_2_step_baseline_steps_data_experienced_attacker, eval_2_step_baseline_steps_means_experienced_attacker,
        eval_2_step_baseline_steps_stds_experienced_attacker,
        eval_2_snort_severe_baseline_early_stopping_data_experienced_attacker,
        eval_2_snort_severe_baseline_early_stopping_means_experienced_attacker,
        eval_2_snort_severe_baseline_early_stopping_stds_experienced_attacker,
        eval_2_step_baseline_early_stopping_data_experienced_attacker,
        eval_2_step_baseline_early_stopping_means_experienced_attacker,
        eval_2_step_baseline_early_stopping_stds_experienced_attacker,
        eval_2_snort_severe_baseline_caught_attacker_data_experienced_attacker,
        eval_2_snort_severe_baseline_caught_attacker_means_experienced_attacker,
        eval_2_snort_severe_baseline_caught_attacker_stds_experienced_attacker,
        eval_2_step_baseline_caught_attacker_data_experienced_attacker,
        eval_2_step_baseline_caught_attacker_means_experienced_attacker,
        eval_2_step_baseline_caught_attacker_stds_experienced_attacker,
        eval_2_snort_severe_baseline_uncaught_intrusion_steps_data_experienced_attacker,
        eval_2_snort_severe_baseline_uncaught_intrusion_steps_means_experienced_attacker,
        eval_2_snort_severe_baseline_uncaught_intrusion_steps_stds_experienced_attacker,
        eval_2_step_baseline_uncaught_intrusion_steps_data_experienced_attacker,
        eval_2_step_baseline_uncaught_intrusion_steps_means_experienced_attacker,
        eval_2_step_baseline_uncaught_intrusion_steps_stds_experienced_attacker,
        eval_2_defender_first_stop_step_experienced_attacker_data,
        eval_2_defender_first_stop_step_experienced_attacker_means, eval_2_defender_first_stop_step_experienced_attacker_stds,
        eval_2_defender_second_stop_step_experienced_attacker_data,
        eval_2_defender_second_stop_step_experienced_attacker_means, eval_2_defender_second_stop_step_experienced_attacker_stds,
        eval_2_defender_third_stop_step_experienced_attacker_data, eval_2_defender_third_stop_step_experienced_attacker_means,
        eval_2_defender_third_stop_step_experienced_attacker_stds, eval_2_defender_fourth_stop_step_experienced_attacker_data,
        eval_2_defender_fourth_stop_step_experienced_attacker_means, eval_2_defender_fourth_stop_step_experienced_attacker_stds,
        eval_2_defender_stops_remaining_experienced_attacker_data, eval_2_defender_stops_remaining_experienced_attacker_means,
        eval_2_defender_stops_remaining_experienced_attacker_stds, eval_2_optimal_first_stop_step_experienced_attacker_data,
        eval_2_optimal_first_stop_step_experienced_attacker_means, eval_2_optimal_first_stop_step_experienced_attacker_stds,
        eval_2_optimal_second_stop_step_experienced_attacker_data, eval_2_optimal_second_stop_step_experienced_attacker_means,
        eval_2_optimal_second_stop_step_experienced_attacker_stds, eval_2_optimal_third_stop_step_experienced_attacker_data,
        eval_2_optimal_third_stop_step_experienced_attacker_means, eval_2_optimal_third_stop_step_experienced_attacker_stds,
        eval_2_optimal_fourth_stop_step_experienced_attacker_data, eval_2_optimal_fourth_stop_step_experienced_attacker_means,
        eval_2_optimal_fourth_stop_step_experienced_attacker_stds, eval_2_optimal_stops_remaining_experienced_attacker_data,
        eval_2_optimal_stops_remaining_experienced_attacker_means, eval_2_optimal_stops_remaining_experienced_attacker_stds,
        eval_2_snort_severe_baseline_first_stop_step_experienced_attacker_data,
        eval_2_snort_severe_baseline_first_stop_step_experienced_attacker_means,
        eval_2_snort_severe_baseline_first_stop_step_experienced_attacker_stds,
        eval_2_snort_severe_baseline_second_stop_step_experienced_attacker_data,
        eval_2_snort_severe_baseline_second_stop_step_experienced_attacker_means,
        eval_2_snort_severe_baseline_second_stop_step_experienced_attacker_stds,
        eval_2_snort_severe_baseline_third_stop_step_experienced_attacker_data,
        eval_2_snort_severe_baseline_third_stop_step_experienced_attacker_means,
        eval_2_snort_severe_baseline_third_stop_step_experienced_attacker_stds,
        eval_2_snort_severe_baseline_fourth_stop_step_experienced_attacker_data,
        eval_2_snort_severe_baseline_fourth_stop_step_experienced_attacker_means,
        eval_2_snort_severe_baseline_fourth_stop_step_experienced_attacker_stds,
        eval_2_snort_severe_baseline_stops_remaining_experienced_attacker_data,
        eval_2_snort_severe_baseline_stops_remaining_experienced_attacker_means,
        eval_2_snort_severe_baseline_stops_remaining_experienced_attacker_stds,
        eval_2_step_baseline_first_stop_step_experienced_attacker_data,
        eval_2_step_baseline_first_stop_step_experienced_attacker_means,
        eval_2_step_baseline_first_stop_step_experienced_attacker_stds,
        eval_2_step_baseline_second_stop_step_experienced_attacker_data,
        eval_2_step_baseline_second_stop_step_experienced_attacker_means,
        eval_2_step_baseline_second_stop_step_experienced_attacker_stds,
        eval_2_step_baseline_third_stop_step_experienced_attacker_data,
        eval_2_step_baseline_third_stop_step_experienced_attacker_means,
        eval_2_step_baseline_third_stop_step_experienced_attacker_stds,
        eval_2_step_baseline_fourth_stop_step_experienced_attacker_data,
        eval_2_step_baseline_fourth_stop_step_experienced_attacker_means,
        eval_2_step_baseline_fourth_stop_step_experienced_attacker_stds,
        eval_2_step_baseline_stops_remaining_experienced_attacker_data,
        eval_2_step_baseline_stops_remaining_experienced_attacker_means,
        eval_2_step_baseline_stops_remaining_experienced_attacker_stds,
        eval_2_optimal_episode_steps_experienced_attacker_data, eval_2_optimal_episode_steps_experienced_attacker_means,
        eval_2_optimal_episode_steps_experienced_attacker_stds,
        avg_train_rewards_data_expert_attacker, avg_train_rewards_means_expert_attacker,
        avg_train_rewards_stds_expert_attacker,
        avg_train_steps_data_expert_attacker, avg_train_steps_means_expert_attacker,
        avg_train_steps_stds_expert_attacker,
        avg_train_caught_frac_data_expert_attacker, avg_train_caught_frac_means_expert_attacker,
        avg_train_caught_frac_stds_expert_attacker,
        avg_train_early_stopping_frac_data_expert_attacker, avg_train_early_stopping_means_expert_attacker,
        avg_train_early_stopping_stds_expert_attacker, avg_train_intrusion_frac_data_expert_attacker,
        avg_train_intrusion_means_expert_attacker,
        avg_train_intrusion_stds_expert_attacker,
        avg_train_i_steps_data_expert_attacker, avg_train_i_steps_means_expert_attacker,
        avg_train_i_steps_stds_expert_attacker,
        avg_train_uncaught_intrusion_steps_data_expert_attacker,
        avg_train_uncaught_intrusion_steps_means_expert_attacker,
        avg_train_uncaught_intrusion_steps_stds_expert_attacker,
        avg_train_optimal_defender_rewards_expert_attacker_data,
        avg_train_optimal_defender_rewards_expert_attacker_means,
        avg_train_optimal_defender_rewards_expert_attacker_stds,
        train_snort_severe_baseline_rewards_data_expert_attacker,
        train_snort_severe_baseline_rewards_means_expert_attacker,
        train_snort_severe_baseline_rewards_stds_expert_attacker, train_step_baseline_rewards_data_expert_attacker,
        train_step_baseline_rewards_means_expert_attacker, train_step_baseline_rewards_stds_expert_attacker,
        train_snort_severe_baseline_steps_data_expert_attacker,
        train_snort_severe_baseline_steps_means_expert_attacker,
        train_snort_severe_baseline_steps_stds_expert_attacker,
        train_step_baseline_steps_data_expert_attacker, train_step_baseline_steps_means_expert_attacker,
        train_step_baseline_steps_stds_expert_attacker,
        train_snort_severe_baseline_early_stopping_data_expert_attacker,
        train_snort_severe_baseline_early_stopping_means_expert_attacker,
        train_snort_severe_baseline_early_stopping_stds_expert_attacker,
        train_step_baseline_early_stopping_data_expert_attacker,
        train_step_baseline_early_stopping_means_expert_attacker,
        train_step_baseline_early_stopping_stds_expert_attacker,
        train_snort_severe_baseline_caught_attacker_data_expert_attacker,
        train_snort_severe_baseline_caught_attacker_means_expert_attacker,
        train_snort_severe_baseline_caught_attacker_stds_expert_attacker,
        train_step_baseline_caught_attacker_data_expert_attacker,
        train_step_baseline_caught_attacker_means_expert_attacker,
        train_step_baseline_caught_attacker_stds_expert_attacker,
        train_snort_severe_baseline_uncaught_intrusion_steps_data_expert_attacker,
        train_snort_severe_baseline_uncaught_intrusion_steps_means_expert_attacker,
        train_snort_severe_baseline_uncaught_intrusion_steps_stds_expert_attacker,
        train_step_baseline_uncaught_intrusion_steps_data_expert_attacker,
        train_step_baseline_uncaught_intrusion_steps_means_expert_attacker,
        train_step_baseline_uncaught_intrusion_steps_stds_expert_attacker,
        train_defender_first_stop_step_expert_attacker_data,
        train_defender_first_stop_step_expert_attacker_means, train_defender_first_stop_step_expert_attacker_stds,
        train_defender_second_stop_step_expert_attacker_data,
        train_defender_second_stop_step_expert_attacker_means, train_defender_second_stop_step_expert_attacker_stds,
        train_defender_third_stop_step_expert_attacker_data, train_defender_third_stop_step_expert_attacker_means,
        train_defender_third_stop_step_expert_attacker_stds, train_defender_fourth_stop_step_expert_attacker_data,
        train_defender_fourth_stop_step_expert_attacker_means, train_defender_fourth_stop_step_expert_attacker_stds,
        train_defender_stops_remaining_expert_attacker_data, train_defender_stops_remaining_expert_attacker_means,
        train_defender_stops_remaining_expert_attacker_stds, train_optimal_first_stop_step_expert_attacker_data,
        train_optimal_first_stop_step_expert_attacker_means, train_optimal_first_stop_step_expert_attacker_stds,
        train_optimal_second_stop_step_expert_attacker_data, train_optimal_second_stop_step_expert_attacker_means,
        train_optimal_second_stop_step_expert_attacker_stds, train_optimal_third_stop_step_expert_attacker_data,
        train_optimal_third_stop_step_expert_attacker_means, train_optimal_third_stop_step_expert_attacker_stds,
        train_optimal_fourth_stop_step_expert_attacker_data, train_optimal_fourth_stop_step_expert_attacker_means,
        train_optimal_fourth_stop_step_expert_attacker_stds, train_optimal_stops_remaining_expert_attacker_data,
        train_optimal_stops_remaining_expert_attacker_means, train_optimal_stops_remaining_expert_attacker_stds,
        train_snort_severe_baseline_first_stop_step_expert_attacker_data,
        train_snort_severe_baseline_first_stop_step_expert_attacker_means,
        train_snort_severe_baseline_first_stop_step_expert_attacker_stds,
        train_snort_severe_baseline_second_stop_step_expert_attacker_data,
        train_snort_severe_baseline_second_stop_step_expert_attacker_means,
        train_snort_severe_baseline_second_stop_step_expert_attacker_stds,
        train_snort_severe_baseline_third_stop_step_expert_attacker_data,
        train_snort_severe_baseline_third_stop_step_expert_attacker_means,
        train_snort_severe_baseline_third_stop_step_expert_attacker_stds,
        train_snort_severe_baseline_fourth_stop_step_expert_attacker_data,
        train_snort_severe_baseline_fourth_stop_step_expert_attacker_means,
        train_snort_severe_baseline_fourth_stop_step_expert_attacker_stds,
        train_snort_severe_baseline_stops_remaining_expert_attacker_data,
        train_snort_severe_baseline_stops_remaining_expert_attacker_means,
        train_snort_severe_baseline_stops_remaining_expert_attacker_stds,
        train_step_baseline_first_stop_step_expert_attacker_data,
        train_step_baseline_first_stop_step_expert_attacker_means,
        train_step_baseline_first_stop_step_expert_attacker_stds,
        train_step_baseline_second_stop_step_expert_attacker_data,
        train_step_baseline_second_stop_step_expert_attacker_means,
        train_step_baseline_second_stop_step_expert_attacker_stds,
        train_step_baseline_third_stop_step_expert_attacker_data,
        train_step_baseline_third_stop_step_expert_attacker_means,
        train_step_baseline_third_stop_step_expert_attacker_stds,
        train_step_baseline_fourth_stop_step_expert_attacker_data,
        train_step_baseline_fourth_stop_step_expert_attacker_means,
        train_step_baseline_fourth_stop_step_expert_attacker_stds,
        train_step_baseline_stops_remaining_expert_attacker_data,
        train_step_baseline_stops_remaining_expert_attacker_means,
        train_step_baseline_stops_remaining_expert_attacker_stds,
        train_optimal_episode_steps_expert_attacker_data, train_optimal_episode_steps_expert_attacker_means,
        train_optimal_episode_steps_expert_attacker_stds,
        avg_eval_rewards_data_expert_attacker, avg_eval_rewards_means_expert_attacker,
        avg_eval_rewards_stds_expert_attacker,
        avg_eval_steps_data_expert_attacker, avg_eval_steps_means_expert_attacker,
        avg_eval_steps_stds_expert_attacker,
        avg_eval_caught_frac_data_expert_attacker, avg_eval_caught_frac_means_expert_attacker,
        avg_eval_caught_frac_stds_expert_attacker,
        avg_eval_early_stopping_frac_data_expert_attacker, avg_eval_early_stopping_means_expert_attacker,
        avg_eval_early_stopping_stds_expert_attacker, avg_eval_intrusion_frac_data_expert_attacker,
        avg_eval_intrusion_means_expert_attacker,
        avg_eval_intrusion_stds_expert_attacker,
        avg_eval_i_steps_data_expert_attacker, avg_eval_i_steps_means_expert_attacker,
        avg_eval_i_steps_stds_expert_attacker,
        avg_eval_uncaught_intrusion_steps_data_expert_attacker,
        avg_eval_uncaught_intrusion_steps_means_expert_attacker,
        avg_eval_uncaught_intrusion_steps_stds_expert_attacker,
        avg_eval_optimal_defender_rewards_expert_attacker_data,
        avg_eval_optimal_defender_rewards_expert_attacker_means,
        avg_eval_optimal_defender_rewards_expert_attacker_stds,
        eval_snort_severe_baseline_rewards_data_expert_attacker,
        eval_snort_severe_baseline_rewards_means_expert_attacker,
        eval_snort_severe_baseline_rewards_stds_expert_attacker,
        eval_step_baseline_rewards_data_expert_attacker, eval_step_baseline_rewards_means_expert_attacker,
        eval_step_baseline_rewards_stds_expert_attacker,
        eval_snort_severe_baseline_steps_data_expert_attacker,
        eval_snort_severe_baseline_steps_means_expert_attacker,
        eval_snort_severe_baseline_steps_stds_expert_attacker,
        eval_step_baseline_steps_data_expert_attacker, eval_step_baseline_steps_means_expert_attacker,
        eval_step_baseline_steps_stds_expert_attacker,
        eval_snort_severe_baseline_early_stopping_data_expert_attacker,
        eval_snort_severe_baseline_early_stopping_means_expert_attacker,
        eval_snort_severe_baseline_early_stopping_stds_expert_attacker,
        eval_step_baseline_early_stopping_data_expert_attacker,
        eval_step_baseline_early_stopping_means_expert_attacker,
        eval_step_baseline_early_stopping_stds_expert_attacker,
        eval_snort_severe_baseline_caught_attacker_data_expert_attacker,
        eval_snort_severe_baseline_caught_attacker_means_expert_attacker,
        eval_snort_severe_baseline_caught_attacker_stds_expert_attacker,
        eval_step_baseline_caught_attacker_data_expert_attacker,
        eval_step_baseline_caught_attacker_means_expert_attacker,
        eval_step_baseline_caught_attacker_stds_expert_attacker,
        eval_snort_severe_baseline_uncaught_intrusion_steps_data_expert_attacker,
        eval_snort_severe_baseline_uncaught_intrusion_steps_means_expert_attacker,
        eval_snort_severe_baseline_uncaught_intrusion_steps_stds_expert_attacker,
        eval_step_baseline_uncaught_intrusion_steps_data_expert_attacker,
        eval_step_baseline_uncaught_intrusion_steps_means_expert_attacker,
        eval_step_baseline_uncaught_intrusion_steps_stds_expert_attacker,
        eval_defender_first_stop_step_expert_attacker_data,
        eval_defender_first_stop_step_expert_attacker_means, eval_defender_first_stop_step_expert_attacker_stds,
        eval_defender_second_stop_step_expert_attacker_data,
        eval_defender_second_stop_step_expert_attacker_means, eval_defender_second_stop_step_expert_attacker_stds,
        eval_defender_third_stop_step_expert_attacker_data, eval_defender_third_stop_step_expert_attacker_means,
        eval_defender_third_stop_step_expert_attacker_stds, eval_defender_fourth_stop_step_expert_attacker_data,
        eval_defender_fourth_stop_step_expert_attacker_means, eval_defender_fourth_stop_step_expert_attacker_stds,
        eval_defender_stops_remaining_expert_attacker_data, eval_defender_stops_remaining_expert_attacker_means,
        eval_defender_stops_remaining_expert_attacker_stds, eval_optimal_first_stop_step_expert_attacker_data,
        eval_optimal_first_stop_step_expert_attacker_means, eval_optimal_first_stop_step_expert_attacker_stds,
        eval_optimal_second_stop_step_expert_attacker_data, eval_optimal_second_stop_step_expert_attacker_means,
        eval_optimal_second_stop_step_expert_attacker_stds, eval_optimal_third_stop_step_expert_attacker_data,
        eval_optimal_third_stop_step_expert_attacker_means, eval_optimal_third_stop_step_expert_attacker_stds,
        eval_optimal_fourth_stop_step_expert_attacker_data, eval_optimal_fourth_stop_step_expert_attacker_means,
        eval_optimal_fourth_stop_step_expert_attacker_stds, eval_optimal_stops_remaining_expert_attacker_data,
        eval_optimal_stops_remaining_expert_attacker_means, eval_optimal_stops_remaining_expert_attacker_stds,
        eval_snort_severe_baseline_first_stop_step_expert_attacker_data,
        eval_snort_severe_baseline_first_stop_step_expert_attacker_means,
        eval_snort_severe_baseline_first_stop_step_expert_attacker_stds,
        eval_snort_severe_baseline_second_stop_step_expert_attacker_data,
        eval_snort_severe_baseline_second_stop_step_expert_attacker_means,
        eval_snort_severe_baseline_second_stop_step_expert_attacker_stds,
        eval_snort_severe_baseline_third_stop_step_expert_attacker_data,
        eval_snort_severe_baseline_third_stop_step_expert_attacker_means,
        eval_snort_severe_baseline_third_stop_step_expert_attacker_stds,
        eval_snort_severe_baseline_fourth_stop_step_expert_attacker_data,
        eval_snort_severe_baseline_fourth_stop_step_expert_attacker_means,
        eval_snort_severe_baseline_fourth_stop_step_expert_attacker_stds,
        eval_snort_severe_baseline_stops_remaining_expert_attacker_data,
        eval_snort_severe_baseline_stops_remaining_expert_attacker_means,
        eval_snort_severe_baseline_stops_remaining_expert_attacker_stds,
        eval_step_baseline_first_stop_step_expert_attacker_data,
        eval_step_baseline_first_stop_step_expert_attacker_means,
        eval_step_baseline_first_stop_step_expert_attacker_stds,
        eval_step_baseline_second_stop_step_expert_attacker_data,
        eval_step_baseline_second_stop_step_expert_attacker_means,
        eval_step_baseline_second_stop_step_expert_attacker_stds,
        eval_step_baseline_third_stop_step_expert_attacker_data,
        eval_step_baseline_third_stop_step_expert_attacker_means,
        eval_step_baseline_third_stop_step_expert_attacker_stds,
        eval_step_baseline_fourth_stop_step_expert_attacker_data,
        eval_step_baseline_fourth_stop_step_expert_attacker_means,
        eval_step_baseline_fourth_stop_step_expert_attacker_stds,
        eval_step_baseline_stops_remaining_expert_attacker_data,
        eval_step_baseline_stops_remaining_expert_attacker_means,
        eval_step_baseline_stops_remaining_expert_attacker_stds,
        eval_optimal_episode_steps_expert_attacker_data, eval_optimal_episode_steps_expert_attacker_means,
        eval_optimal_episode_steps_expert_attacker_stds,
        avg_eval_2_rewards_data_expert_attacker, avg_eval_2_rewards_means_expert_attacker,
        avg_eval_2_rewards_stds_expert_attacker,
        avg_eval_2_steps_data_expert_attacker, avg_eval_2_steps_means_expert_attacker,
        avg_eval_2_steps_stds_expert_attacker,
        avg_eval_2_caught_frac_data_expert_attacker, avg_eval_2_caught_frac_means_expert_attacker,
        avg_eval_2_caught_frac_stds_expert_attacker,
        avg_eval_2_early_stopping_frac_data_expert_attacker, avg_eval_2_early_stopping_means_expert_attacker,
        avg_eval_2_early_stopping_stds_expert_attacker, avg_eval_2_intrusion_frac_data_expert_attacker,
        avg_eval_2_intrusion_means_expert_attacker,
        avg_eval_2_intrusion_stds_expert_attacker,
        avg_eval_2_i_steps_data_expert_attacker, avg_eval_2_i_steps_means_expert_attacker,
        avg_eval_2_i_steps_stds_expert_attacker,
        avg_eval_2_uncaught_intrusion_steps_data_expert_attacker,
        avg_eval_2_uncaught_intrusion_steps_means_expert_attacker,
        avg_eval_2_uncaught_intrusion_steps_stds_expert_attacker,
        avg_eval_2_optimal_defender_rewards_expert_attacker_data,
        avg_eval_2_optimal_defender_rewards_expert_attacker_means,
        avg_eval_2_optimal_defender_rewards_expert_attacker_stds,
        eval_2_snort_severe_baseline_rewards_data_expert_attacker,
        eval_2_snort_severe_baseline_rewards_means_expert_attacker,
        eval_2_snort_severe_baseline_rewards_stds_expert_attacker,
        eval_2_step_baseline_rewards_data_expert_attacker,
        eval_2_step_baseline_rewards_means_expert_attacker, eval_2_step_baseline_rewards_stds_expert_attacker,
        eval_2_snort_severe_baseline_steps_data_expert_attacker,
        eval_2_snort_severe_baseline_steps_means_expert_attacker,
        eval_2_snort_severe_baseline_steps_stds_expert_attacker,
        eval_2_step_baseline_steps_data_expert_attacker, eval_2_step_baseline_steps_means_expert_attacker,
        eval_2_step_baseline_steps_stds_expert_attacker,
        eval_2_snort_severe_baseline_early_stopping_data_expert_attacker,
        eval_2_snort_severe_baseline_early_stopping_means_expert_attacker,
        eval_2_snort_severe_baseline_early_stopping_stds_expert_attacker,
        eval_2_step_baseline_early_stopping_data_expert_attacker,
        eval_2_step_baseline_early_stopping_means_expert_attacker,
        eval_2_step_baseline_early_stopping_stds_expert_attacker,
        eval_2_snort_severe_baseline_caught_attacker_data_expert_attacker,
        eval_2_snort_severe_baseline_caught_attacker_means_expert_attacker,
        eval_2_snort_severe_baseline_caught_attacker_stds_expert_attacker,
        eval_2_step_baseline_caught_attacker_data_expert_attacker,
        eval_2_step_baseline_caught_attacker_means_expert_attacker,
        eval_2_step_baseline_caught_attacker_stds_expert_attacker,
        eval_2_snort_severe_baseline_uncaught_intrusion_steps_data_expert_attacker,
        eval_2_snort_severe_baseline_uncaught_intrusion_steps_means_expert_attacker,
        eval_2_snort_severe_baseline_uncaught_intrusion_steps_stds_expert_attacker,
        eval_2_step_baseline_uncaught_intrusion_steps_data_expert_attacker,
        eval_2_step_baseline_uncaught_intrusion_steps_means_expert_attacker,
        eval_2_step_baseline_uncaught_intrusion_steps_stds_expert_attacker,
        eval_2_defender_first_stop_step_expert_attacker_data,
        eval_2_defender_first_stop_step_expert_attacker_means, eval_2_defender_first_stop_step_expert_attacker_stds,
        eval_2_defender_second_stop_step_expert_attacker_data,
        eval_2_defender_second_stop_step_expert_attacker_means, eval_2_defender_second_stop_step_expert_attacker_stds,
        eval_2_defender_third_stop_step_expert_attacker_data, eval_2_defender_third_stop_step_expert_attacker_means,
        eval_2_defender_third_stop_step_expert_attacker_stds, eval_2_defender_fourth_stop_step_expert_attacker_data,
        eval_2_defender_fourth_stop_step_expert_attacker_means, eval_2_defender_fourth_stop_step_expert_attacker_stds,
        eval_2_defender_stops_remaining_expert_attacker_data, eval_2_defender_stops_remaining_expert_attacker_means,
        eval_2_defender_stops_remaining_expert_attacker_stds, eval_2_optimal_first_stop_step_expert_attacker_data,
        eval_2_optimal_first_stop_step_expert_attacker_means, eval_2_optimal_first_stop_step_expert_attacker_stds,
        eval_2_optimal_second_stop_step_expert_attacker_data, eval_2_optimal_second_stop_step_expert_attacker_means,
        eval_2_optimal_second_stop_step_expert_attacker_stds, eval_2_optimal_third_stop_step_expert_attacker_data,
        eval_2_optimal_third_stop_step_expert_attacker_means, eval_2_optimal_third_stop_step_expert_attacker_stds,
        eval_2_optimal_fourth_stop_step_expert_attacker_data, eval_2_optimal_fourth_stop_step_expert_attacker_means,
        eval_2_optimal_fourth_stop_step_expert_attacker_stds, eval_2_optimal_stops_remaining_expert_attacker_data,
        eval_2_optimal_stops_remaining_expert_attacker_means, eval_2_optimal_stops_remaining_expert_attacker_stds,
        eval_2_snort_severe_baseline_first_stop_step_expert_attacker_data,
        eval_2_snort_severe_baseline_first_stop_step_expert_attacker_means,
        eval_2_snort_severe_baseline_first_stop_step_expert_attacker_stds,
        eval_2_snort_severe_baseline_second_stop_step_expert_attacker_data,
        eval_2_snort_severe_baseline_second_stop_step_expert_attacker_means,
        eval_2_snort_severe_baseline_second_stop_step_expert_attacker_stds,
        eval_2_snort_severe_baseline_third_stop_step_expert_attacker_data,
        eval_2_snort_severe_baseline_third_stop_step_expert_attacker_means,
        eval_2_snort_severe_baseline_third_stop_step_expert_attacker_stds,
        eval_2_snort_severe_baseline_fourth_stop_step_expert_attacker_data,
        eval_2_snort_severe_baseline_fourth_stop_step_expert_attacker_means,
        eval_2_snort_severe_baseline_fourth_stop_step_expert_attacker_stds,
        eval_2_snort_severe_baseline_stops_remaining_expert_attacker_data,
        eval_2_snort_severe_baseline_stops_remaining_expert_attacker_means,
        eval_2_snort_severe_baseline_stops_remaining_expert_attacker_stds,
        eval_2_step_baseline_first_stop_step_expert_attacker_data,
        eval_2_step_baseline_first_stop_step_expert_attacker_means,
        eval_2_step_baseline_first_stop_step_expert_attacker_stds,
        eval_2_step_baseline_second_stop_step_expert_attacker_data,
        eval_2_step_baseline_second_stop_step_expert_attacker_means,
        eval_2_step_baseline_second_stop_step_expert_attacker_stds,
        eval_2_step_baseline_third_stop_step_expert_attacker_data,
        eval_2_step_baseline_third_stop_step_expert_attacker_means,
        eval_2_step_baseline_third_stop_step_expert_attacker_stds,
        eval_2_step_baseline_fourth_stop_step_expert_attacker_data,
        eval_2_step_baseline_fourth_stop_step_expert_attacker_means,
        eval_2_step_baseline_fourth_stop_step_expert_attacker_stds,
        eval_2_step_baseline_stops_remaining_expert_attacker_data,
        eval_2_step_baseline_stops_remaining_expert_attacker_means,
        eval_2_step_baseline_stops_remaining_expert_attacker_stds,
        eval_2_optimal_episode_steps_expert_attacker_data, eval_2_optimal_episode_steps_expert_attacker_means,
        eval_2_optimal_episode_steps_expert_attacker_stds
    )
