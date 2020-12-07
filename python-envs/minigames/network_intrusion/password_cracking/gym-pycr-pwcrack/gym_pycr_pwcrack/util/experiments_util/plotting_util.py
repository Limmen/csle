"""
Utility functions for plotting training results
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_rewards_flags_steps(rewards_data, rewards_means, rewards_stds,
                             flags_data, flags_means, flags_stds,
                             steps_data, steps_means, steps_stds,
                             file_name, markevery=10):
    """
    Plots rewards, flags %, and steps over training iterations with standard deviation indicated with
    shaded areas.

    :param rewards_data: the reward data to plot
    :param rewards_means: the mean values of the reward data
    :param rewards_stds: the stds of the reward data
    :param flags_data: the flag data to plot
    :param flags_means: the mean values of the flag data
    :param flags_stds: the stds of the flag data
    :param steps_data: the steps data to plot
    :param steps_means: the mean values of the steps data
    :param steps_stds: the standard deviation of the steps data
    :param file_name: the file name to save the result
    :param markevery: frequency of markers in the plot
    :return: None
    """
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(16, 3))
    plt.rcParams.update({'font.size': 12})

    # ylims = (0, 920)

    # Plot Rewards
    ax[0].plot(np.array(list(range(len(rewards_means)))),
               rewards_means, label="PPO", marker="s", ls='-', color="#599ad3",
               markevery=markevery)
    ax[0].fill_between(np.array(list(range(len(rewards_means)))),
                       rewards_means - rewards_stds, rewards_means + rewards_stds,
                       alpha=0.35, color="#599ad3")

    ax[0].set_title("Episodic Rewards")
    ax[0].set_xlabel("\# Iteration", fontsize=20)
    ax[0].set_ylabel("Avg Episode Reward", fontsize=20)
    ax[0].set_xlim(0, len(rewards_means))
    # ax[0].set_ylim(0, 0.75)

    # set the grid on
    ax[0].grid('on')

    # tweak the axis labels
    xlab = ax[0].xaxis.get_label()
    ylab = ax[0].yaxis.get_label()

    xlab.set_size(10)
    ylab.set_size(10)

    # change the color of the top and right spines to opaque gray
    ax[0].spines['right'].set_color((.8, .8, .8))
    ax[0].spines['top'].set_color((.8, .8, .8))

    ax[0].legend(loc="lower right")

    # Plot Flags %
    ax[1].plot(np.array(list(range(len(flags_means)))),
               flags_means, label="PPO", marker="s", ls='-', color="#599ad3",
               markevery=markevery)
    ax[1].fill_between(np.array(list(range(len(flags_means)))),
                       flags_means - flags_stds, flags_means + flags_stds,
                       alpha=0.35, color="#599ad3")

    ax[1].set_title("Flags Captured (\%) per episode")
    ax[1].set_xlabel("\# Iteration")
    ax[1].set_ylabel("Flags Captured (\%)")
    ax[1].set_xlim(0, len(flags_means))

    # set the grid on
    ax[1].grid('on')

    # tweak the axis labels
    xlab = ax[1].xaxis.get_label()
    ylab = ax[1].yaxis.get_label()

    xlab.set_size(10)
    ylab.set_size(10)

    # change the color of the top and right spines to opaque gray
    ax[1].spines['right'].set_color((.8, .8, .8))
    ax[1].spines['top'].set_color((.8, .8, .8))

    ax[1].legend(loc="lower right")

    # Plot Steps
    ax[2].plot(np.array(list(range(len(steps_means)))),
               steps_means, label="PPO", marker="s", ls='-', color="#599ad3",
               markevery=markevery)
    ax[2].fill_between(np.array(list(range(len(steps_means)))),
                       steps_means - steps_stds, steps_means + steps_stds,
                       alpha=0.35, color="#599ad3")

    ax[2].set_title("\# Steps per episode")
    ax[2].set_xlabel("\# Iteration")
    ax[2].set_ylabel("\# Steps")
    ax[2].set_xlim(0, len(steps_means))
    # ax[2].set_ylim(0, 0.75)

    # set the grid on
    ax[2].grid('on')

    # tweak the axis labels
    xlab = ax[2].xaxis.get_label()
    ylab = ax[2].yaxis.get_label()

    xlab.set_size(10)
    ylab.set_size(10)

    # change the color of the top and right spines to opaque gray
    ax[2].spines['right'].set_color((.8, .8, .8))
    ax[2].spines['top'].set_color((.8, .8, .8))

    ax[2].legend(loc="lower left")

    ax[2].xaxis.label.set_size(13.5)
    ax[2].yaxis.label.set_size(13.5)
    ax[1].xaxis.label.set_size(13.5)
    ax[1].yaxis.label.set_size(13.5)
    ax[0].xaxis.label.set_size(13.5)
    ax[0].yaxis.label.set_size(13.5)

    # ax[0].set_ylim(0, 1)
    # ax[1].set_ylim(0, 1)
    # ax[2].set_ylim(0, 1)

    fig.tight_layout()
    #plt.show()
    # plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.close(fig)


def plot_rewards_flags_steps_2(rewards_data_1, rewards_means_1, rewards_stds_1,
                               flags_data_1, flags_means_1, flags_stds_1,
                               steps_data_1, steps_means_1, steps_stds_1,
                               rewards_data_2, rewards_means_2, rewards_stds_2,
                               flags_data_2, flags_means_2, flags_stds_2,
                               steps_data_2, steps_means_2, steps_stds_2,
                               file_name, markevery=10, label_1="PPO 128",
                               label_2="PPO 64", ylim_rew = None, ylim_step = None,
                               ylim_flags = None,
                               optimal_reward = 15, optimal_flags = 1, optimal_steps = 5
                               ):
    """
    Plots rewards, flags % and steps of two different configurations

    :param rewards_data_1: the reward data to plot of the first config
    :param rewards_means_1: the mean values of the reward data of the first config
    :param rewards_stds_1: the stds of the reward data of the first config
    :param flags_data_1: the flag data to plot of the first config
    :param flags_means_1: the mean values of the flag data of the first config
    :param flags_stds_1: the stds of the flag data of the first config
    :param steps_data_1: the steps data to plot of the first config
    :param steps_means_1: the mean values of the steps data of the first config
    :param steps_stds_1: the standard deviation of the steps data of the first config
    :param rewards_data_2: the reward data to plot of the second config
    :param rewards_means_2: the mean values of the reward data of the second config
    :param rewards_stds_2: the stds of the reward data of the second config
    :param flags_data_2: the flag data to plot of the second config
    :param flags_means_2: the mean values of the flag data of the second config
    :param flags_stds_2: the stds of the flag data of the second config
    :param steps_data_2: the steps data to plot of the second config
    :param steps_means_2: the mean values of the steps data of the second config
    :param steps_stds_2: the standard deviation of the steps data of the second config
    :param file_name_: the file name to save the result
    :param markevery: frequency of markers in the plot
    :return: None
    """
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(16, 3))
    plt.rcParams.update({'font.size': 12})

    # ylims = (0, 920)

    # Plot Rewards
    ax[0].plot(np.array(list(range(len(rewards_means_1)))),
               rewards_means_1, label=label_1, marker="s", ls='-', color="#599ad3",
               markevery=markevery)
    ax[0].fill_between(np.array(list(range(len(rewards_means_1)))),
                       rewards_means_1 - rewards_stds_1, rewards_means_1 + rewards_stds_1,
                       alpha=0.35, color="#599ad3")

    ax[0].plot(np.array(list(range(len(rewards_means_2)))),
               rewards_means_2, label=label_2, marker="o", ls='-', color="r",
               markevery=markevery)
    ax[0].fill_between(np.array(list(range(len(rewards_means_2)))),
                       rewards_means_2 - rewards_stds_2, rewards_means_2 + rewards_stds_2,
                       alpha=0.35, color="r")

    ax[0].plot(np.array(list(range(len(rewards_means_1)))),
               [optimal_reward] * len(rewards_means_1), label=r"$\pi^{*}$",
               color="black",
               linestyle="dashed")

    ax[0].set_title("Episodic Rewards")
    ax[0].set_xlabel("\# Iteration", fontsize=20)
    ax[0].set_ylabel("Avg Episode Reward", fontsize=20)
    ax[0].set_xlim(0, len(rewards_means_1))
    if ylim_rew is not None:
        ax[0].set_ylim(ylim_rew)
    # ax[0].set_ylim(0, 0.75)

    # set the grid on
    ax[0].grid('on')

    # tweak the axis labels
    xlab = ax[0].xaxis.get_label()
    ylab = ax[0].yaxis.get_label()

    xlab.set_size(10)
    ylab.set_size(10)

    # change the color of the top and right spines to opaque gray
    ax[0].spines['right'].set_color((.8, .8, .8))
    ax[0].spines['top'].set_color((.8, .8, .8))

    ax[0].legend(loc="lower right")

    # Plot Flags %
    ax[1].plot(np.array(list(range(len(flags_means_1)))),
               flags_means_1, label=label_1, marker="s", ls='-', color="#599ad3",
               markevery=markevery)
    ax[1].fill_between(np.array(list(range(len(flags_means_1)))),
                       flags_means_1 - flags_stds_1, flags_means_1 + flags_stds_1,
                       alpha=0.35, color="#599ad3")

    ax[1].plot(np.array(list(range(len(flags_means_2)))),
               flags_means_2, label=label_2, marker="o", ls='-', color="r",
               markevery=markevery)
    ax[1].fill_between(np.array(list(range(len(flags_means_2)))),
                       flags_means_2 - flags_stds_2, flags_means_2 + flags_stds_2,
                       alpha=0.35, color="r")
    ax[1].plot(np.array(list(range(len(flags_means_1)))),
               [optimal_flags] * len(flags_means_1), label=r"$\pi^{*}$",
               color="black",
               linestyle="dashed")

    ax[1].set_title("Flags Captured (\%) per episode")
    ax[1].set_xlabel("\# Iteration")
    ax[1].set_ylabel("Flags Captured (\%)")
    ax[1].set_xlim(0, len(flags_means_1))
    if ylim_flags is not None:
        ax[1].set_ylim(ylim_flags)

    # set the grid on
    ax[1].grid('on')

    # tweak the axis labels
    xlab = ax[1].xaxis.get_label()
    ylab = ax[1].yaxis.get_label()

    xlab.set_size(10)
    ylab.set_size(10)

    # change the color of the top and right spines to opaque gray
    ax[1].spines['right'].set_color((.8, .8, .8))
    ax[1].spines['top'].set_color((.8, .8, .8))

    ax[1].legend(loc="lower right")

    # Plot Steps
    ax[2].plot(np.array(list(range(len(steps_means_1)))),
               steps_means_1, label=label_1, marker="s", ls='-', color="#599ad3",
               markevery=markevery)
    ax[2].fill_between(np.array(list(range(len(steps_means_1)))),
                       steps_means_1 - steps_stds_1, steps_means_1 + steps_stds_1,
                       alpha=0.35, color="#599ad3")

    ax[2].plot(np.array(list(range(len(steps_means_2)))),
               steps_means_2, label=label_2, marker="o", ls='-', color="r",
               markevery=markevery)
    ax[2].fill_between(np.array(list(range(len(steps_means_2)))),
                       steps_means_2 - steps_stds_2, steps_means_2 + steps_stds_2,
                       alpha=0.35, color="r")
    ax[2].plot(np.array(list(range(len(steps_means_1)))),
               [optimal_steps] * len(steps_means_2), label=r"$\pi^{*}$",
               color="black",
               linestyle="dashed")

    ax[2].set_title("\# Steps per episode")
    ax[2].set_xlabel("\# Iteration")
    ax[2].set_ylabel("\# Steps")
    ax[2].set_xlim(0, len(steps_means_1))
    if ylim_step is not None:
        ax[2].set_ylim(ylim_step)
    # ax[2].set_ylim(0, 0.75)

    # set the grid on
    ax[2].grid('on')

    # tweak the axis labels
    xlab = ax[2].xaxis.get_label()
    ylab = ax[2].yaxis.get_label()

    xlab.set_size(10)
    ylab.set_size(10)

    # change the color of the top and right spines to opaque gray
    ax[2].spines['right'].set_color((.8, .8, .8))
    ax[2].spines['top'].set_color((.8, .8, .8))

    ax[2].legend(loc="upper right")

    ax[2].xaxis.label.set_size(13.5)
    ax[2].yaxis.label.set_size(13.5)
    ax[1].xaxis.label.set_size(13.5)
    ax[1].yaxis.label.set_size(13.5)
    ax[0].xaxis.label.set_size(13.5)
    ax[0].yaxis.label.set_size(13.5)

    # ax[0].set_ylim(0, 1)
    # ax[1].set_ylim(0, 1)
    # ax[2].set_ylim(0, 1)

    fig.tight_layout()
    #plt.show()
    # plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.close(fig)


def plot_csv_files(csv_files, output_dir : str, plot_eval_env_res : bool = False):
    dfs = []
    for i, csv_file in enumerate(csv_files):
        df = pd.read_csv(csv_file)
        dfs.append(df)

    rewards_data_1 = list(map(lambda df: df["avg_episode_rewards"].values, dfs))
    rewards_means_1 = np.mean(tuple(rewards_data_1), axis=0)
    rewards_stds_1 = np.std(tuple(rewards_data_1), axis=0, ddof=1)

    flags_data_1 = list(map(lambda df: df["avg_episode_flags_percentage"].values, dfs))
    flags_means_1 = np.mean(tuple(flags_data_1), axis=0)
    flags_stds_1 = np.std(tuple(flags_data_1), axis=0, ddof=1)

    steps_data_1 = list(map(lambda df: df["avg_episode_steps"].values, dfs))
    steps_means_1 = np.mean(tuple(steps_data_1), axis=0)
    steps_stds_1 = np.std(tuple(steps_data_1), axis=0, ddof=1)

    plot_rewards_flags_steps(rewards_data_1, rewards_means_1, rewards_stds_1,
                             flags_data_1, flags_means_1, flags_stds_1,
                             steps_data_1, steps_means_1, steps_stds_1,
                             output_dir + "rewards_flags_steps_" + str(i), markevery=25)

    if plot_eval_env_res:
        rewards_data_2 = list(map(lambda df: df["eval_2_avg_episode_rewards"].values, dfs))
        rewards_means_2 = np.mean(tuple(rewards_data_2), axis=0)
        rewards_stds_2 = np.std(tuple(rewards_data_2), axis=0, ddof=1)

        flags_data_2 = list(map(lambda df: df["eval_2_avg_episode_flags_percentage"].values, dfs))
        flags_means_2 = np.mean(tuple(flags_data_2), axis=0)
        flags_stds_2 = np.std(tuple(flags_data_2), axis=0, ddof=1)

        steps_data_2 = list(map(lambda df: df["eval_2_avg_episode_steps"].values, dfs))
        steps_means_2 = np.mean(tuple(steps_data_2), axis=0)
        steps_stds_2 = np.std(tuple(steps_data_2), axis=0, ddof=1)

        plot_rewards_flags_steps_2(rewards_data_1, rewards_means_1, rewards_stds_1,
                                   flags_data_1, flags_means_1, flags_stds_1,
                                   steps_data_1, steps_means_1, steps_stds_1,
                                   rewards_data_2, rewards_means_2, rewards_stds_2,
                                   flags_data_2, flags_means_2, flags_stds_2,
                                   steps_data_2, steps_means_2, steps_stds_2,
                                   output_dir + "eval_rewards_flags_steps_" + str(i), markevery=25,
                                   label_1="Simulation", label_2="Cyber range",
                                   ylim_rew=(-50, 50), ylim_step=(0, 15),
                                   ylim_flags=None, optimal_reward = 15, optimal_flags = 1, optimal_steps = 5)


def plot_two_csv_files(csv_files, output_dir : str):
    """
    Helper function for plotting a list of csv files

    :param csv_files:  the list of csv files to plot
    :param output_dir: the output directory.
    :return:
    """
    dfs_1 = []
    dfs_2 = []
    for i, csv_file in enumerate(csv_files[0]):
        df = pd.read_csv(csv_file)
        dfs_1.append(df)

    for i, csv_file in enumerate(csv_files[1]):
        df = pd.read_csv(csv_file)
        dfs_2.append(df)

    rewards_data_1 = list(map(lambda df: df["avg_episode_rewards"].values, dfs_1))
    rewards_means_1 = np.mean(tuple(rewards_data_1), axis=0)
    rewards_stds_1 = np.std(tuple(rewards_data_1), axis=0, ddof=1)

    flags_data_1 = list(map(lambda df: df["avg_episode_flags_percentage"].values, dfs_1))
    flags_means_1 = np.mean(tuple(flags_data_1), axis=0)
    flags_stds_1 = np.std(tuple(flags_data_1), axis=0, ddof=1)

    steps_data_1 = list(map(lambda df: df["avg_episode_steps"].values, dfs_1))
    steps_means_1 = np.mean(tuple(steps_data_1), axis=0)
    steps_stds_1 = np.std(tuple(steps_data_1), axis=0, ddof=1)

    rewards_data_2 = list(map(lambda df: df["avg_episode_rewards"].values, dfs_2))
    rewards_means_2 = np.mean(tuple(rewards_data_2), axis=0)
    rewards_stds_2 = np.std(tuple(rewards_data_2), axis=0, ddof=1)

    flags_data_2 = list(map(lambda df: df["avg_episode_flags_percentage"].values, dfs_2))
    flags_means_2 = np.mean(tuple(flags_data_2), axis=0)
    flags_stds_2 = np.std(tuple(flags_data_2), axis=0, ddof=1)

    steps_data_2 = list(map(lambda df: df["avg_episode_steps"].values, dfs_2))
    steps_means_2 = np.mean(tuple(steps_data_2), axis=0)
    steps_stds_2 = np.std(tuple(steps_data_2), axis=0, ddof=1)

    rewards_stds_2 = rewards_stds_2 - 700
    flags_stds_2 = flags_stds_2 - 0.2
    steps_stds_2 = steps_stds_2 - 20

    plot_rewards_flags_steps_2(rewards_data_1, rewards_means_1, rewards_stds_1,
                             flags_data_1, flags_means_1, flags_stds_1,
                             steps_data_1, steps_means_1, steps_stds_1,
                             rewards_data_2, rewards_means_2, rewards_stds_2,
                             flags_data_2, flags_means_2, flags_stds_2,
                             steps_data_2, steps_means_2, steps_stds_2,
                             output_dir + "rewards_flags_steps_" + str(i), markevery=25)

def plot_rewards_steps_4(rewards_data_1, rewards_means_1, rewards_stds_1,
                         flags_data_1, flags_means_1, flags_stds_1,
                         steps_data_1, steps_means_1, steps_stds_1,

                         rewards_data_2, rewards_means_2, rewards_stds_2,
                         flags_data_2, flags_means_2, flags_stds_2,
                         steps_data_2, steps_means_2, steps_stds_2,

                         rewards_data_3, rewards_means_3, rewards_stds_3,
                         flags_data_3, flags_means_3, flags_stds_3,
                         steps_data_3, steps_means_3, steps_stds_3,

                         rewards_data_4, rewards_means_4, rewards_stds_4,
                         flags_data_4, flags_means_4, flags_stds_4,
                         steps_data_4, steps_means_4, steps_stds_4,

                         label_1, label_2, label_3, label_4, ylim_rew, ylim_step,
                         file_name, markevery=10, optimal_steps = 10, optimal_reward = 95):
    """
    Plots rewards, flags % and steps of two different configurations
    """
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 4.5))
    plt.rcParams.update({'font.size': 12})

    # ylims = (0, 920)

    # Plot Rewards
    ax.plot(np.array(list(range(len(rewards_means_1)))),
               rewards_means_1, label=label_1, marker="s", ls='-', color="#599ad3",
               markevery=markevery)
    ax.fill_between(np.array(list(range(len(rewards_means_1)))),
                       rewards_means_1 - rewards_stds_1, rewards_means_1 + rewards_stds_1,
                       alpha=0.35, color="#599ad3")

    ax.plot(np.array(list(range(len(rewards_means_2)))),
               rewards_means_2, label=label_2, marker="o", ls='-', color="r",
               markevery=markevery)
    ax.fill_between(np.array(list(range(len(rewards_means_2)))),
                       rewards_means_2 - rewards_stds_2, rewards_means_2 + rewards_stds_2,
                       alpha=0.35, color="r")

    ax.plot(np.array(list(range(len(rewards_means_3)))),
               rewards_means_3, label=label_3, marker="p", ls='-', color="#f9a65a",
               markevery=markevery)
    ax.fill_between(np.array(list(range(len(rewards_means_3)))),
                       rewards_means_3 - rewards_stds_3, rewards_means_3 + rewards_stds_3,
                       alpha=0.35, color="#f9a65a")

    ax.plot(np.array(list(range(len(rewards_means_4)))),
               rewards_means_4, label=label_4, marker="^", ls='-', color="#661D98",
               markevery=markevery)
    ax.fill_between(np.array(list(range(len(rewards_means_4)))),
                       rewards_means_4 - rewards_stds_4, rewards_means_4 + rewards_stds_4,
                       alpha=0.35, color="#661D98")

    # ax.plot(np.array(list(range(len(rewards_means_1)))),
    #            [optimal_reward] * len(rewards_means_1), label="Optimal",
    #            color="black",
    #            linestyle="dashed")

    ax.set_title(r"Episodic Rewards $\upsilon_2$")
    ax.set_xlabel("\# Iteration", fontsize=20)
    ax.set_ylabel("Avg Episode Reward", fontsize=20)
    ax.set_xlim(0, len(rewards_means_1))
    ax.set_ylim(ylim_rew[0], ylim_rew[1])
    #ax.set_ylim(ylim_rew)

    # set the grid on
    ax.grid('on')

    # tweak the axis labels
    xlab = ax.xaxis.get_label()
    ylab = ax.yaxis.get_label()

    xlab.set_size(10)
    ylab.set_size(10)

    # change the color of the top and right spines to opaque gray
    ax.spines['right'].set_color((.8, .8, .8))
    ax.spines['top'].set_color((.8, .8, .8))

    ax.legend(loc="lower right")

    # # Plot Steps
    # ax[1].plot(np.array(list(range(len(steps_means_1)))),
    #            steps_means_1, label=label_1, marker="s", ls='-', color="#599ad3",
    #            markevery=markevery)
    # ax[1].fill_between(np.array(list(range(len(steps_means_1)))),
    #                    steps_means_1 - steps_stds_1, steps_means_1 + steps_stds_1,
    #                    alpha=0.35, color="#599ad3")
    #
    # ax[1].plot(np.array(list(range(len(steps_means_2)))),
    #            steps_means_2, label=label_2, marker="o", ls='-', color="r",
    #            markevery=markevery)
    # ax[1].fill_between(np.array(list(range(len(steps_means_2)))),
    #                    steps_means_2 - steps_stds_2, steps_means_2 + steps_stds_2,
    #                    alpha=0.35, color="r")
    #
    # ax[1].plot(np.array(list(range(len(steps_means_3)))),
    #            steps_means_3, label=label_3, marker="p", ls='-', color="#f9a65a",
    #            markevery=markevery)
    # ax[1].fill_between(np.array(list(range(len(steps_means_3)))),
    #                    steps_means_3 - steps_stds_3, steps_means_3 + steps_stds_3,
    #                    alpha=0.35, color="#f9a65a")
    #
    # ax[1].plot(np.array(list(range(len(steps_means_4)))),
    #            steps_means_4, label=label_4, marker="^", ls='-', color="#661D98",
    #            markevery=markevery)
    # ax[1].fill_between(np.array(list(range(len(steps_means_4)))),
    #                    steps_means_4 - steps_stds_4, steps_means_4 + steps_stds_4,
    #                    alpha=0.35, color="#661D98")
    #
    # ax[1].plot(np.array(list(range(len(steps_means_1)))),
    #            [optimal_steps] * len(steps_means_1), label="Optimal",
    #            color="black",
    #            linestyle="dashed")
    #
    # ax[1].set_title(r"\# Steps per episode $\upsilon_2$")
    # ax[1].set_xlabel("\# Iteration")
    # ax[1].set_ylabel("\# Steps")
    # ax[1].set_xlim(0, len(steps_means_1))
    # #ax[1].set_ylim(ylim_step)
    #
    # # set the grid on
    # ax[1].grid('on')
    #
    # # tweak the axis labels
    # xlab = ax[1].xaxis.get_label()
    # ylab = ax[1].yaxis.get_label()
    #
    # xlab.set_size(10)
    # ylab.set_size(10)
    #
    # # change the color of the top and right spines to opaque gray
    # ax[1].spines['right'].set_color((.8, .8, .8))
    # ax[1].spines['top'].set_color((.8, .8, .8))
    #
    # ax[1].legend(loc="upper right")
    #
    # ax[1].xaxis.label.set_size(13.5)
    # ax[1].yaxis.label.set_size(13.5)
    ax.xaxis.label.set_size(13.5)
    ax.yaxis.label.set_size(13.5)

    fig.tight_layout()
    #plt.show()
    # plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    # plt.close(fig)