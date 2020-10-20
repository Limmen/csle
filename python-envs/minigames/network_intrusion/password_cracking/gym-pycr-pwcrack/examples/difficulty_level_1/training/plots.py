import pandas as pd
import numpy as np
from gym_pycr_pwcrack.util.experiments_util import plotting_util

def plot_rewards_steps_v1_v2_v3_v4():
    ppo_v1_df_0 = pd.read_csv(
        "./v1/cluster/ppo_baseline/results/data/0/1603190894.4870985_train.csv")
    ppo_v1_df_299 = pd.read_csv(
        "./v1/cluster/ppo_baseline/results/data/299/1603192393.1999376_train.csv")
    ppo_v1_df_399 = pd.read_csv(
        "./v1/cluster/ppo_baseline/results/data/399/1603193146.563139_train.csv")
    ppo_v1_df_499 = pd.read_csv(
        "./v1/cluster/ppo_baseline/results/data/499/1603193898.592786_train.csv")
    ppo_v1_df_999 = pd.read_csv(
        "./v1/cluster/ppo_baseline/results/data/999/1603191642.1174266_train.csv")
    ppo_dfs_v1 = [ppo_v1_df_0, ppo_v1_df_299, ppo_v1_df_399, ppo_v1_df_499, ppo_v1_df_999]

    ppo_v2_df_0 = pd.read_csv(
        "./v2/cluster/ppo_baseline/results/data/0/1603190962.0172794_train.csv")
    ppo_v2_df_299 = pd.read_csv(
        "./v2/cluster/ppo_baseline/results/data/299/1603192942.5795782_train.csv")
    ppo_v2_df_399 = pd.read_csv(
        "./v2/cluster/ppo_baseline/results/data/399/1603193927.5475442_train.csv")
    ppo_v2_df_499 = pd.read_csv(
        "./v2/cluster/ppo_baseline/results/data/499/1603194846.5371535_train.csv")
    ppo_v2_df_999 = pd.read_csv(
        "./v2/cluster/ppo_baseline/results/data/999/1603191952.1202796_train.csv")
    ppo_dfs_v2 = [ppo_v2_df_0, ppo_v2_df_299, ppo_v2_df_399, ppo_v2_df_499, ppo_v2_df_999]

    ppo_v3_df_0 = pd.read_csv(
        "./v3/cluster/ppo_baseline/results/data/0/1603196459.4714174_train.csv")
    ppo_v3_df_299 = pd.read_csv(
        "./v3/cluster/ppo_baseline/results/data/299/1603197949.3573668_train.csv")
    ppo_v3_df_399 = pd.read_csv(
        "./v3/cluster/ppo_baseline/results/data/399/1603198683.4438276_train.csv")
    ppo_v3_df_499 = pd.read_csv(
        "./v3/cluster/ppo_baseline/results/data/499/1603199419.1049101_train.csv")
    ppo_v3_df_999 = pd.read_csv(
        "./v3/cluster/ppo_baseline/results/data/999/1603197214.5385463_train.csv")
    ppo_dfs_v3 = [ppo_v3_df_0, ppo_v3_df_299, ppo_v3_df_399, ppo_v3_df_499, ppo_v3_df_999]

    ppo_v4_df_0 = pd.read_csv(
        "./v4/cluster/ppo_baseline/results/data/0/1603190715.7338402_train.csv")
    ppo_v4_df_299 = pd.read_csv(
        "./v4/cluster/ppo_baseline/results/data/299/1603192933.9591403_train.csv")
    ppo_v4_df_399 = pd.read_csv(
        "./v4/cluster/ppo_baseline/results/data/399/1603194281.0459163_train.csv")
    ppo_v4_df_499 = pd.read_csv(
        "./v4/cluster/ppo_baseline/results/data/499/1603195265.9069285_train.csv")
    ppo_v4_df_999 = pd.read_csv(
        "./v4/cluster/ppo_baseline/results/data/999/1603191648.747736_train.csv")
    ppo_dfs_v4 = [ppo_v4_df_0, ppo_v4_df_299, ppo_v4_df_399, ppo_v4_df_499, ppo_v4_df_999]

    rewards_data_v1 = list(map(lambda df: df["eval_avg_episode_rewards"].values, ppo_dfs_v1))
    rewards_means_v1 = np.mean(tuple(rewards_data_v1), axis=0)
    rewards_stds_v1 = np.std(tuple(rewards_data_v1), axis=0, ddof=1)

    flags_data_v1 = list(map(lambda df: df["eval_avg_episode_flags_percentage"].values, ppo_dfs_v1))
    flags_means_v1 = np.mean(tuple(flags_data_v1), axis=0)
    flags_stds_v1 = np.std(tuple(flags_data_v1), axis=0, ddof=1)

    steps_data_v1 = list(map(lambda df: df["eval_avg_episode_steps"].values, ppo_dfs_v1))
    steps_means_v1 = np.mean(tuple(steps_data_v1), axis=0)
    steps_stds_v1 = np.std(tuple(steps_data_v1), axis=0, ddof=1)

    rewards_data_v2 = list(map(lambda df: df["eval_avg_episode_rewards"].values, ppo_dfs_v2))
    rewards_means_v2 = np.mean(tuple(rewards_data_v2), axis=0)
    rewards_stds_v2 = np.std(tuple(rewards_data_v2), axis=0, ddof=1)

    flags_data_v2 = list(map(lambda df: df["eval_avg_episode_flags_percentage"].values, ppo_dfs_v2))
    flags_means_v2 = np.mean(tuple(flags_data_v2), axis=0)
    flags_stds_v2 = np.std(tuple(flags_data_v2), axis=0, ddof=1)

    steps_data_v2 = list(map(lambda df: df["eval_avg_episode_steps"].values, ppo_dfs_v2))
    steps_means_v2 = np.mean(tuple(steps_data_v2), axis=0)
    steps_stds_v2 = np.std(tuple(steps_data_v2), axis=0, ddof=1)

    rewards_data_v3 = list(map(lambda df: df["eval_avg_episode_rewards"].values, ppo_dfs_v3))
    rewards_means_v3 = np.mean(tuple(rewards_data_v3), axis=0)
    rewards_stds_v3 = np.std(tuple(rewards_data_v3), axis=0, ddof=1)

    flags_data_v3 = list(map(lambda df: df["eval_avg_episode_flags_percentage"].values, ppo_dfs_v3))
    flags_means_v3 = np.mean(tuple(flags_data_v3), axis=0)
    flags_stds_v3 = np.std(tuple(flags_data_v3), axis=0, ddof=1)

    steps_data_v3 = list(map(lambda df: df["eval_avg_episode_steps"].values, ppo_dfs_v3))
    steps_means_v3 = np.mean(tuple(steps_data_v3), axis=0)
    steps_stds_v3 = np.std(tuple(steps_data_v3), axis=0, ddof=1)

    rewards_data_v4 = list(map(lambda df: df["eval_avg_episode_rewards"].values, ppo_dfs_v4))
    rewards_means_v4 = np.mean(tuple(rewards_data_v4), axis=0)
    rewards_stds_v4 = np.std(tuple(rewards_data_v4), axis=0, ddof=1)

    flags_data_v4 = list(map(lambda df: df["eval_avg_episode_flags_percentage"].values, ppo_dfs_v4))
    flags_means_v4 = np.mean(tuple(flags_data_v4), axis=0)
    flags_stds_v4 = np.std(tuple(flags_data_v4), axis=0, ddof=1)

    steps_data_v4 = list(map(lambda df: df["eval_avg_episode_steps"].values, ppo_dfs_v4))
    steps_means_v4 = np.mean(tuple(steps_data_v4), axis=0)
    steps_stds_v4 = np.std(tuple(steps_data_v4), axis=0, ddof=1)

    ylim_rew = (min([min(rewards_means_v1 - rewards_stds_v1),
                     min(rewards_means_v2 - rewards_stds_v2),
                     min(rewards_means_v3 - rewards_stds_v3),
                     min(rewards_means_v4 - rewards_stds_v4)]),
                max([max(rewards_means_v1 + rewards_stds_v1),
                     max(rewards_means_v2 + rewards_stds_v2),
                     max(rewards_means_v3 + rewards_stds_v3),
                     max(rewards_means_v4 + rewards_stds_v4)]))
    ylim_step = (min([min(steps_means_v1 - steps_stds_v1),
                      min(steps_means_v2 - steps_stds_v2),
                      min(steps_means_v3 - steps_stds_v3),
                      min(steps_means_v4 - steps_stds_v4)]),
                 max([max(steps_means_v1 + steps_stds_v1),
                      max(steps_means_v2 + steps_stds_v2),
                      max(steps_means_v3 + steps_stds_v3),
                      max(steps_means_v4 + steps_stds_v4)]))

    plotting_util.plot_rewards_steps_4(rewards_data_v1[0:200], rewards_means_v1[0:200], rewards_stds_v1[0:200],
                         flags_data_v1[0:200], flags_means_v1[0:200], flags_stds_v1[0:200],
                         steps_data_v1[0:200], steps_means_v1[0:200], steps_stds_v1[0:200],
                         rewards_data_v2[0:200], rewards_means_v2[0:200], rewards_stds_v2[0:200],
                         flags_data_v2[0:200], flags_means_v2[0:200], flags_stds_v2[0:200],
                         steps_data_v2[0:200], steps_means_v2[0:200], steps_stds_v2[0:200],
                         rewards_data_v3[0:200], rewards_means_v3[0:200], rewards_stds_v3[0:200],
                         flags_data_v3[0:200], flags_means_v3[0:200], flags_stds_v3[0:200],
                         steps_data_v3[0:200], steps_means_v3[0:200], steps_stds_v3[0:200],

                         rewards_data_v4[0:200], rewards_means_v4[0:200], rewards_stds_v4[0:200],
                         flags_data_v4[0:200], flags_means_v4[0:200], flags_stds_v4[0:200],
                         steps_data_v4[0:200], steps_means_v4[0:200], steps_stds_v4[0:200],
                         "23 actions", "54 actions", "90 actions", "155 actions", ylim_rew, ylim_step,
                         "./steps_rewards_eval_v1_v2_v3_v4", markevery=10)

    ylim_rew = (0, 150)
    ylim_step = (7, 30)

    plotting_util.plot_rewards_steps_4(rewards_data_v1[0:200], rewards_means_v1[0:200], rewards_stds_v1[0:200],
                         flags_data_v1[0:200], flags_means_v1[0:200], flags_stds_v1[0:200],
                         steps_data_v1[0:200], steps_means_v1[0:200], steps_stds_v1[0:200],
                         rewards_data_v2[0:200], rewards_means_v2[0:200], rewards_stds_v2[0:200],
                         flags_data_v2[0:200], flags_means_v2[0:200], flags_stds_v2[0:200],
                         steps_data_v2[0:200], steps_means_v2[0:200], steps_stds_v2[0:200],
                         rewards_data_v3[0:200], rewards_means_v3[0:200], rewards_stds_v3[0:200],
                         flags_data_v3[0:200], flags_means_v3[0:200], flags_stds_v3[0:200],
                         steps_data_v3[0:200], steps_means_v3[0:200], steps_stds_v3[0:200],

                         rewards_data_v4[0:200], rewards_means_v4[0:200], rewards_stds_v4[0:200],
                         flags_data_v4[0:200], flags_means_v4[0:200], flags_stds_v4[0:200],
                         steps_data_v4[0:200], steps_means_v4[0:200], steps_stds_v4[0:200],

                         "23 actions", "54 actions", "90 actions", "155 actions", ylim_rew, ylim_step,
                         "./steps_rewards_eval_v1_v2_v3_v4_zoomedin", markevery=10)

    rewards_data_v1 = list(map(lambda df: df["avg_episode_rewards"].values, ppo_dfs_v1))
    rewards_means_v1 = np.mean(tuple(rewards_data_v1), axis=0)
    rewards_stds_v1 = np.std(tuple(rewards_data_v1), axis=0, ddof=1)

    flags_data_v1 = list(map(lambda df: df["avg_episode_flags_percentage"].values, ppo_dfs_v1))
    flags_means_v1 = np.mean(tuple(flags_data_v1), axis=0)
    flags_stds_v1 = np.std(tuple(flags_data_v1), axis=0, ddof=1)

    steps_data_v1 = list(map(lambda df: df["avg_episode_steps"].values, ppo_dfs_v1))
    steps_means_v1 = np.mean(tuple(steps_data_v1), axis=0)
    steps_stds_v1 = np.std(tuple(steps_data_v1), axis=0, ddof=1)

    rewards_data_v2 = list(map(lambda df: df["avg_episode_rewards"].values, ppo_dfs_v2))
    rewards_means_v2 = np.mean(tuple(rewards_data_v2), axis=0)
    rewards_stds_v2 = np.std(tuple(rewards_data_v2), axis=0, ddof=1)

    flags_data_v2 = list(map(lambda df: df["avg_episode_flags_percentage"].values, ppo_dfs_v2))
    flags_means_v2 = np.mean(tuple(flags_data_v2), axis=0)
    flags_stds_v2 = np.std(tuple(flags_data_v2), axis=0, ddof=1)

    steps_data_v2 = list(map(lambda df: df["avg_episode_steps"].values, ppo_dfs_v2))
    steps_means_v2 = np.mean(tuple(steps_data_v2), axis=0)
    steps_stds_v2 = np.std(tuple(steps_data_v2), axis=0, ddof=1)

    rewards_data_v3 = list(map(lambda df: df["avg_episode_rewards"].values, ppo_dfs_v3))
    rewards_means_v3 = np.mean(tuple(rewards_data_v3), axis=0)
    rewards_stds_v3 = np.std(tuple(rewards_data_v3), axis=0, ddof=1)

    flags_data_v3 = list(map(lambda df: df["avg_episode_flags_percentage"].values, ppo_dfs_v3))
    flags_means_v3 = np.mean(tuple(flags_data_v3), axis=0)
    flags_stds_v3 = np.std(tuple(flags_data_v3), axis=0, ddof=1)

    steps_data_v3 = list(map(lambda df: df["avg_episode_steps"].values, ppo_dfs_v3))
    steps_means_v3 = np.mean(tuple(steps_data_v3), axis=0)
    steps_stds_v3 = np.std(tuple(steps_data_v3), axis=0, ddof=1)

    rewards_data_v4 = list(map(lambda df: df["avg_episode_rewards"].values, ppo_dfs_v4))
    rewards_means_v4 = np.mean(tuple(rewards_data_v4), axis=0)
    rewards_stds_v4 = np.std(tuple(rewards_data_v4), axis=0, ddof=1)

    flags_data_v4 = list(map(lambda df: df["avg_episode_flags_percentage"].values, ppo_dfs_v4))
    flags_means_v4 = np.mean(tuple(flags_data_v4), axis=0)
    flags_stds_v4 = np.std(tuple(flags_data_v4), axis=0, ddof=1)

    steps_data_v4 = list(map(lambda df: df["avg_episode_steps"].values, ppo_dfs_v4))
    steps_means_v4 = np.mean(tuple(steps_data_v4), axis=0)
    steps_stds_v4 = np.std(tuple(steps_data_v4), axis=0, ddof=1)

    ylim_rew = (min([min(rewards_means_v1 - rewards_stds_v1),
                     min(rewards_means_v2 - rewards_stds_v2),
                     min(rewards_means_v3 - rewards_stds_v3),
                     min(rewards_means_v4 - rewards_stds_v4)]),
                max([max(rewards_means_v1 + rewards_stds_v1),
                     max(rewards_means_v2 + rewards_stds_v2),
                     max(rewards_means_v3 + rewards_stds_v3),
                     max(rewards_means_v4 + rewards_stds_v4)]))
    ylim_step = (min([min(steps_means_v1 - steps_stds_v1),
                      min(steps_means_v2 - steps_stds_v2),
                      min(steps_means_v3 - steps_stds_v3),
                      min(steps_means_v4 - steps_stds_v4)]),
                 max([max(steps_means_v1 + steps_stds_v1),
                      max(steps_means_v2 + steps_stds_v2),
                      max(steps_means_v3 + steps_stds_v3),
                      max(steps_means_v4 + steps_stds_v4)]))

    plotting_util.plot_rewards_steps_4(rewards_data_v1[0:200], rewards_means_v1[0:200], rewards_stds_v1[0:200],
                         flags_data_v1[0:200], flags_means_v1[0:200], flags_stds_v1[0:200],
                         steps_data_v1[0:200], steps_means_v1[0:200], steps_stds_v1[0:200],

                         rewards_data_v2[0:200], rewards_means_v2[0:200], rewards_stds_v2[0:200],
                         flags_data_v2[0:200], flags_means_v2[0:200], flags_stds_v2[0:200],
                         steps_data_v2[0:200], steps_means_v2[0:200], steps_stds_v2[0:200],

                         rewards_data_v3[0:200], rewards_means_v3[0:200], rewards_stds_v3[0:200],
                         flags_data_v3[0:200], flags_means_v3[0:200], flags_stds_v3[0:200],
                         steps_data_v3[0:200], steps_means_v3[0:200], steps_stds_v3[0:200],

                         rewards_data_v4[0:200], rewards_means_v4[0:200], rewards_stds_v4[0:200],
                         flags_data_v4[0:200], flags_means_v4[0:200], flags_stds_v4[0:200],
                         steps_data_v4[0:200], steps_means_v4[0:200], steps_stds_v4[0:200],

                         "23 actions", "54 actions", "90 actions", "155 actions", ylim_rew, ylim_step,
                         "./steps_rewards_v1_v2_v3_v4", markevery=10)


if __name__ == '__main__':
    plot_rewards_steps_v1_v2_v3_v4()

