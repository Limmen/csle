import pandas as pd
import numpy as np
from gym_pycr_ctf.util.experiments_util import plotting_util

def plot_rewards_steps_v1_v2_v3_v4():
    ppo_v1_df_0 = pd.read_csv(
        "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_2/training/v1/cluster/ppo_baseline/results/data/0/1607354276.1132252_train.csv")
    # ppo_v1_df_299 = pd.read_csv(
    #     "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_2/training/v1/cluster/ppo_baseline/results/data/299/1605649635.7844296_train.csv")
    # ppo_v1_df_399 = pd.read_csv(
    #     "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_2/training/v1/cluster/ppo_baseline/results/data/399/1605649873.5459857_train.csv")
    # ppo_v1_df_499 = pd.read_csv(
    #     "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_2/training/v1/cluster/ppo_baseline/results/data/499/1605650125.7917361_train.csv")
    ppo_v1_df_999 = pd.read_csv(
        "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_2/training/v1/cluster/ppo_baseline/results/data/999/1607354503.7336388_train.csv")
    #ppo_dfs_v1 = [ppo_v1_df_0, ppo_v1_df_299, ppo_v1_df_399, ppo_v1_df_499, ppo_v1_df_999]
    ppo_dfs_v1 = [ppo_v1_df_0, ppo_v1_df_999]

    ppo_v2_df_0 = pd.read_csv(
        "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_2/training/v2/cluster/ppo_baseline/results/data/0/1607355028.841213_train.csv")
    # ppo_v2_df_299 = pd.read_csv(
    #     "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_1/training/v2/cluster/ppo_baseline/results/data/299/1605644643.7108836_train.csv")
    # ppo_v2_df_399 = pd.read_csv(
    #     "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_1/training/v2/cluster/ppo_baseline/results/data/399/1605644824.44998_train.csv")
    # ppo_v2_df_499 = pd.read_csv(
    #     "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_1/training/v2/cluster/ppo_baseline/results/data/499/1605644994.556923_train.csv")
    ppo_v2_df_999 = pd.read_csv(
        "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_2/training/v2/cluster/ppo_baseline/results/data/999/1607355714.2383244_train.csv")
    #ppo_dfs_v2 = [ppo_v2_df_0, ppo_v2_df_299, ppo_v2_df_399, ppo_v2_df_499, ppo_v2_df_999]
    ppo_dfs_v2 = [ppo_v2_df_0, ppo_v2_df_999]

    ppo_v3_df_0 = pd.read_csv(
        "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_2/training/v3/cluster/ppo_baseline/results/data/0/1607356532.8185706_train.csv")
    # ppo_v3_df_299 = pd.read_csv(
    #     "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_2/training/v3/cluster/ppo_baseline/results/data/299/1606178418.5719573_train.csv")
    # ppo_v3_df_399 = pd.read_csv(
    #     "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_1/training/v3/cluster/ppo_baseline/results/data/399/1605646489.2817347_train.csv")
    # ppo_v3_df_499 = pd.read_csv(
    #     "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_1/training/v3/cluster/ppo_baseline/results/data/499/1605646692.2049596_train.csv")
    ppo_v3_df_999 = pd.read_csv(
        "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_2/training/v3/cluster/ppo_baseline/results/data/999/1607357679.6717246_train.csv")
    #ppo_dfs_v3 = [ppo_v3_df_0, ppo_v3_df_299, ppo_v3_df_399, ppo_v3_df_499, ppo_v3_df_999]
    ppo_dfs_v3 = [ppo_v3_df_0, ppo_v3_df_999]

    # ppo_v4_df_0 = pd.read_csv(
    #     "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_2/training/v4/cluster/ppo_baseline/results/data/299/1606202341.2206078_train.csv")
    ppo_v4_df_299 = pd.read_csv(
        "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_2/training/v4/cluster/ppo_baseline/results/data/0/1607359002.5806754_train.csv")
    # ppo_v4_df_399 = pd.read_csv(
    #     "./v4/cluster/ppo_baseline/results/data/399/1603194281.0459163_train.csv")
    # ppo_v4_df_499 = pd.read_csv(
    #     "./v4/cluster/ppo_baseline/results/data/499/1603195265.9069285_train.csv")
    ppo_v4_df_999 = pd.read_csv(
        "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_2/training/v4/cluster/ppo_baseline/results/data/999/1607361151.7426789_train.csv")
    #ppo_dfs_v4 = [ppo_v4_df_0, ppo_v4_df_299, ppo_v4_df_399, ppo_v4_df_499, ppo_v4_df_999]
    ppo_dfs_v4 = [ppo_v4_df_299, ppo_v4_df_999]

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

    # ylim_rew = (min([min(rewards_means_v1 - rewards_stds_v1)]),
    #             max([max(rewards_means_v1 + rewards_stds_v1)]))
    # ylim_step = (min([min(steps_means_v1 - steps_stds_v1)]),
    #              max([max(steps_means_v1 + steps_stds_v1)]))

    ylim_rew = (-100, max([max(rewards_means_v1 + rewards_stds_v1),
                     max(rewards_means_v2 + rewards_stds_v2),
                     max(rewards_means_v3 + rewards_stds_v3),
                     max(rewards_means_v4 + rewards_stds_v4)]))

    plotting_util.plot_rewards_steps_4(rewards_data_v1[0:200], rewards_means_v1[0:200], rewards_stds_v1[0:200],
                         flags_data_v1[0:200], flags_means_v1[0:200], flags_stds_v1[0:200],
                         steps_data_v1[0:200], steps_means_v1[0:200], steps_stds_v1[0:200],

                        #None, None, None, None, None, None, None, None, None,
                         rewards_data_v2[0:200], rewards_means_v2[0:200], rewards_stds_v2[0:200],
                         flags_data_v2[0:200], flags_means_v2[0:200], flags_stds_v2[0:200],
                         steps_data_v2[0:200], steps_means_v2[0:200], steps_stds_v2[0:200],

                        #None, None, None, None, None, None, None, None, None,
                         rewards_data_v3[0:200], rewards_means_v3[0:200], rewards_stds_v3[0:200],
                         flags_data_v3[0:200], flags_means_v3[0:200], flags_stds_v3[0:200],
                         steps_data_v3[0:200], steps_means_v3[0:200], steps_stds_v3[0:200],

                        #None, None, None, None, None, None, None, None, None,
                         rewards_data_v4[0:200], rewards_means_v4[0:200], rewards_stds_v4[0:200],
                         flags_data_v4[0:200], flags_means_v4[0:200], flags_stds_v4[0:200],
                         steps_data_v4[0:200], steps_means_v4[0:200], steps_stds_v4[0:200],

                         "42 actions", "100 actions", "172 actions", "303 actions", ylim_rew, ylim_step,
                         "./steps_rewards_eval_v1_v2_v3_v4_medium", markevery=10, optimal_steps=5, optimal_reward=16)


    ylim_rew = (min([min(rewards_means_v1 - rewards_stds_v1)]),
                max([max(rewards_means_v1 + rewards_stds_v1)]))
    ylim_step = (min([min(steps_means_v1 - steps_stds_v1)]),
                 max([max(steps_means_v1 + steps_stds_v1)]))

    # plotting_util.plot_rewards_steps_4(rewards_data_v1[0:200], rewards_means_v1[0:200], rewards_stds_v1[0:200],
    #                      flags_data_v1[0:200], flags_means_v1[0:200], flags_stds_v1[0:200],
    #                      steps_data_v1[0:200], steps_means_v1[0:200], steps_stds_v1[0:200],
    #                      rewards_data_v2[0:200], rewards_means_v2[0:200], rewards_stds_v2[0:200],
    #                      flags_data_v2[0:200], flags_means_v2[0:200], flags_stds_v2[0:200],
    #                      steps_data_v2[0:200], steps_means_v2[0:200], steps_stds_v2[0:200],
    #                      rewards_data_v3[0:200], rewards_means_v3[0:200], rewards_stds_v3[0:200],
    #                      flags_data_v3[0:200], flags_means_v3[0:200], flags_stds_v3[0:200],
    #                      steps_data_v3[0:200], steps_means_v3[0:200], steps_stds_v3[0:200],
    #
    #                     None, None, None, None, None, None, None, None, None,
    #                      # rewards_data_v4[0:200], rewards_means_v4[0:200], rewards_stds_v4[0:200],
    #                      # flags_data_v4[0:200], flags_means_v4[0:200], flags_stds_v4[0:200],
    #                      # steps_data_v4[0:200], steps_means_v4[0:200], steps_stds_v4[0:200],
    #
    #                      "23 actions", "54 actions", "90 actions", "155 actions", ylim_rew, ylim_step,
    #                      "./steps_rewards_eval_v1_v2_v3_v4_zoomedin", markevery=10, optimal_steps=5, optimal_reward=16)

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

    # ylim_rew = (min([min(rewards_means_v1 - rewards_stds_v1),
    #                  min(rewards_means_v2 - rewards_stds_v2),
    #                  min(rewards_means_v3 - rewards_stds_v3)]),
    #             max([max(rewards_means_v1 + rewards_stds_v1),
    #                  max(rewards_means_v2 + rewards_stds_v2),
    #                  max(rewards_means_v3 + rewards_stds_v3)]))
    # ylim_step = (min([min(steps_means_v1 - steps_stds_v1),
    #                   min(steps_means_v2 - steps_stds_v2),
    #                   min(steps_means_v3 - steps_stds_v3)]),
    #              max([max(steps_means_v1 + steps_stds_v1),
    #                   max(steps_means_v2 + steps_stds_v2),
    #                   max(steps_means_v3 + steps_stds_v3)]))

    ylim_rew = (-100, max([max(rewards_means_v1 + rewards_stds_v1),
                        max(rewards_means_v2 + rewards_stds_v2),
                        max(rewards_means_v3 + rewards_stds_v3),
                        max(rewards_means_v4 + rewards_stds_v4)]))

    plotting_util.plot_rewards_steps_4(rewards_data_v1[0:200], rewards_means_v1[0:200], rewards_stds_v1[0:200],
                         flags_data_v1[0:200], flags_means_v1[0:200], flags_stds_v1[0:200],
                         steps_data_v1[0:200], steps_means_v1[0:200], steps_stds_v1[0:200],
                        #None, None, None, None, None, None, None, None, None,
                         rewards_data_v2[0:200], rewards_means_v2[0:200], rewards_stds_v2[0:200],
                         flags_data_v2[0:200], flags_means_v2[0:200], flags_stds_v2[0:200],
                         steps_data_v2[0:200], steps_means_v2[0:200], steps_stds_v2[0:200],

                        #None, None, None, None, None, None, None, None, None,
                         rewards_data_v3[0:200], rewards_means_v3[0:200], rewards_stds_v3[0:200],
                         flags_data_v3[0:200], flags_means_v3[0:200], flags_stds_v3[0:200],
                         steps_data_v3[0:200], steps_means_v3[0:200], steps_stds_v3[0:200],
                        #None, None, None, None, None, None, None, None, None,
                         rewards_data_v4[0:200], rewards_means_v4[0:200], rewards_stds_v4[0:200],
                         flags_data_v4[0:200], flags_means_v4[0:200], flags_stds_v4[0:200],
                         steps_data_v4[0:200], steps_means_v4[0:200], steps_stds_v4[0:200],
                         "42 actions", "100 actions", "172 actions", "303 actions", ylim_rew, ylim_step,
                         "./steps_rewards_v1_v2_v3_v4_medium", markevery=10, optimal_steps=5, optimal_reward=16)


if __name__ == '__main__':
    plot_rewards_steps_v1_v2_v3_v4()

