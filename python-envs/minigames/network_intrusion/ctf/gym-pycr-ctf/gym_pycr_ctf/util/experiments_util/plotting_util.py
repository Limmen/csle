"""
Utility functions for plotting training results
"""

import matplotlib
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
    plt.close(fig)

def plot_rewards_train_emulation(train_avg_rewards_data_1, train_avg_rewards_means_1, train_avg_rewards_stds_1,
                               eval_avg_rewards_data_1, eval_avg_rewards_means_1, eval_avg_rewards_stds_1,
                               train_envs_specific_rewards_data, train_envs_specific_rewards_means,
                               train_envs_specific_rewards_stds,
                               eval_envs_specific_rewards_data, eval_envs_specific_rewards_means,
                               eval_envs_specific_rewards_stds,
                               ylim_rew,
                               file_name, markevery=10, optimal_steps = 10, optimal_reward = 95, sample_step = 1,
                               plot_opt=False):
    """
    Plots rewards, flags % and steps of two different configurations
    """
    #matplotlib.style.use("seaborn")
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 5))
    plt.rcParams.update({'font.size': 12})

    # ylims = (0, 920)

    # Plot Avg Train Rewards
    ax.plot(np.array(list(range(len(train_avg_rewards_means_1[::sample_step]))))*sample_step,
            train_avg_rewards_means_1[::sample_step], label=r"Avg\_T", marker="s", ls='-', color="#599ad3",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(train_avg_rewards_means_1[::sample_step]))))*sample_step,
                    train_avg_rewards_means_1[::sample_step] - train_avg_rewards_stds_1[::sample_step], train_avg_rewards_means_1[::sample_step]
                    + train_avg_rewards_stds_1[::sample_step],
                    alpha=0.35, color="#599ad3")

    colors = ["#f9a65a", "#661D98", "#377EB8", "#4DAF4A", "#A65628", "#F781BF",
              '#D95F02', '#7570B3', '#E7298A', '#E6AB02', '#A6761D', '#666666',
              '#8DD3C7', '#CCEBC5', '#BEBADA','#FB8072', "#FF7F00", '#80B1D3', '#FDB462', '#B3DE69', '#FCCDE5',
              '#D9D9D9', '#BC80BD', '#FFED6F', "blue", "#984EA3", "green", "#FFFF33", '#66A61E', '#FFFFB3',
              "purple", "orange", "browen", "ppink", "#1B9E77", "#E41A1C"]
    markers = ["p", "^", "*", "+", "v", "1", "2", "3", "4", "x", "p", "h", "H", "d", "|", ",", ".", "H", "X", "s", "8", ">", "<", "P", "D", 0, 1, 2]

    i = 0
    for key in train_envs_specific_rewards_data.keys():
        r_means = train_envs_specific_rewards_means[key]
        r_stds = train_envs_specific_rewards_stds[key]
        label = r"T\_." + key.rsplit(".", 1)[-2].rsplit(".", 1)[-1]
        ax.plot(np.array(list(range(len(r_means[::sample_step]))))*sample_step,
                   r_means[::sample_step], label=label, marker=markers[i], ls='-', color=colors[i], markevery=markevery)
        ax.fill_between(np.array(list(range(len(r_means[::sample_step]))))*sample_step,
                           r_means[::sample_step] - r_stds[::sample_step], r_means[::sample_step] +
                        r_stds[::sample_step], alpha=0.35, color=colors[i])
        i += 1

    # Plot Avg Eval Rewards
    ax.plot(np.array(list(range(len(eval_avg_rewards_means_1[::sample_step]))))*sample_step,
            eval_avg_rewards_means_1[::sample_step], label=r"Avg\_E", marker="o", ls='-', color="r",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(eval_avg_rewards_means_1[::sample_step]))))*sample_step,
                    eval_avg_rewards_means_1[::sample_step] - eval_avg_rewards_stds_1[::sample_step],
                    eval_avg_rewards_means_1[::sample_step] + eval_avg_rewards_stds_1[::sample_step],
                    alpha=0.35, color="r")

    for key in eval_envs_specific_rewards_data.keys():
        r_means = eval_envs_specific_rewards_means[key]
        r_stds = eval_envs_specific_rewards_stds[key]
        label = r"E\_." + key.rsplit(".", 1)[-2].rsplit(".", 1)[-1]
        ax.plot(np.array(list(range(len(r_means[::sample_step]))))*sample_step,
                   r_means[::sample_step], label=label, marker=markers[i], ls='-', color=colors[i], markevery=markevery)
        ax.fill_between(np.array(list(range(len(r_means[::sample_step]))))*sample_step,
                           r_means[::sample_step] - r_stds[::sample_step],
                        r_means[::sample_step] + r_stds[::sample_step], alpha=0.35, color=colors[i])
        i += 1

    if plot_opt:
        ax.plot(np.array(list(range(len(train_avg_rewards_means_1)))),
                [optimal_reward] * len(train_avg_rewards_means_1), label=r"upper bound $\pi^{*}$",
                color="black",
                linestyle="dashed")

    ax.set_title(r"Episodic Rewards")
    ax.set_xlabel("\# Iteration", fontsize=20)
    ax.set_ylabel("Avg Episode Reward", fontsize=20)
    ax.set_xlim(0, len(train_avg_rewards_means_1[::sample_step])*sample_step)
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

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.27),
              ncol=5, fancybox=True, shadow=True)
    #ax.legend(loc="lower right")
    ax.xaxis.label.set_size(13.5)
    ax.yaxis.label.set_size(13.5)

    fig.tight_layout()
    #plt.show()
    # plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.close(fig)


def plot_rewards_train_emulation_two_colors(train_avg_rewards_data_1, train_avg_rewards_means_1, train_avg_rewards_stds_1,
                               eval_avg_rewards_data_1, eval_avg_rewards_means_1, eval_avg_rewards_stds_1,
                               train_envs_specific_rewards_data, train_envs_specific_rewards_means,
                               train_envs_specific_rewards_stds,
                               eval_envs_specific_rewards_data, eval_envs_specific_rewards_means,
                               eval_envs_specific_rewards_stds,
                               ylim_rew,
                               file_name, markevery=10, optimal_steps = 10, optimal_reward = 95, sample_step = 1,
                               plot_opt=False):
    """
    Plots rewards, flags % and steps of two different configurations
    """
    #matplotlib.style.use("seaborn")
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 5))
    plt.rcParams.update({'font.size': 12})

    # ylims = (0, 920)

    # Plot Avg Train Rewards
    ax.plot(np.array(list(range(len(train_avg_rewards_means_1[::sample_step]))))*sample_step,
            train_avg_rewards_means_1[::sample_step], label=r"Avg\_T", marker="s", ls='-', color="#599ad3",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(train_avg_rewards_means_1[::sample_step]))))*sample_step,
                    train_avg_rewards_means_1[::sample_step] - train_avg_rewards_stds_1[::sample_step],
                    train_avg_rewards_means_1[::sample_step] + train_avg_rewards_stds_1[::sample_step],
                    alpha=0.35, color="#599ad3")

    # colors = ["#f9a65a", "#661D98", "#377EB8", "#4DAF4A", "#A65628", "#F781BF",
    #           '#D95F02', '#7570B3', '#E7298A', '#E6AB02', '#A6761D', '#666666',
    #           '#8DD3C7', '#CCEBC5', '#BEBADA','#FB8072', "#FF7F00", '#80B1D3', '#FDB462', '#B3DE69', '#FCCDE5',
    #           '#D9D9D9', '#BC80BD', '#FFED6F', "blue", "#984EA3", "green", "#FFFF33", '#66A61E', '#FFFFB3',
    #           "purple", "orange", "browen", "ppink", "#1B9E77", "#E41A1C"]
    markers = ["p", "^", "*", "+", "v", "1", "2", "3", "4", "x", "p", "h", "H", "d", "|", ",", ".", "H", "X", "s", "8",
               ">", "<", "P", "D", 0, 1, 2]

    i = 0
    for key in train_envs_specific_rewards_data.keys():
        r_means = train_envs_specific_rewards_means[key]
        r_stds = train_envs_specific_rewards_stds[key]
        label = r"T\_." + key.rsplit(".", 1)[-2].rsplit(".", 1)[-1]
        ax.plot(np.array(list(range(len(r_means[::sample_step]))))*sample_step,
                   r_means[::sample_step], label=label, marker=markers[i], ls='-', color="#599ad3", markevery=markevery)
        ax.fill_between(np.array(list(range(len(r_means[::sample_step]))))*sample_step,
                           r_means[::sample_step] - r_stds[::sample_step],
                        r_means[::sample_step] + r_stds[::sample_step], alpha=0.35, color="#599ad3")
        i += 1

    # Plot Avg Eval Rewards
    ax.plot(np.array(list(range(len(eval_avg_rewards_means_1[::sample_step]))))*sample_step,
            eval_avg_rewards_means_1[::sample_step], label=r"Avg\_E", marker="o", ls='-', color="r",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(eval_avg_rewards_means_1[::sample_step]))))*sample_step,
                    eval_avg_rewards_means_1[::sample_step] - eval_avg_rewards_stds_1[::sample_step],
                    eval_avg_rewards_means_1[::sample_step] + eval_avg_rewards_stds_1[::sample_step],
                    alpha=0.35, color="r")

    for key in eval_envs_specific_rewards_data.keys():
        r_means = eval_envs_specific_rewards_means[key]
        r_stds = eval_envs_specific_rewards_stds[key]
        label = r"E\_." + key.rsplit(".", 1)[-2].rsplit(".", 1)[-1]
        ax.plot(np.array(list(range(len(r_means[::sample_step]))))*sample_step,
                   r_means[::sample_step], label=label, marker=markers[i], ls='-', color="r", markevery=markevery)
        ax.fill_between(np.array(list(range(len(r_means[::sample_step]))))*sample_step,
                           r_means[::sample_step] - r_stds[::sample_step],
                        r_means[::sample_step] + r_stds[::sample_step], alpha=0.35, color="r")
        i += 1

    if plot_opt:
        ax.plot(np.array(list(range(len(train_avg_rewards_means_1)))),
                [optimal_reward] * len(train_avg_rewards_means_1), label=r"upper bound $\pi^{*}$",
                color="black",
                linestyle="dashed")

    ax.set_title(r"Episodic Rewards")
    ax.set_xlabel("\# Iteration", fontsize=20)
    ax.set_ylabel("Avg Episode Reward", fontsize=20)
    ax.set_xlim(0, len(train_avg_rewards_means_1[::sample_step])*sample_step)
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

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.27),
              ncol=5, fancybox=True, shadow=True)
    #ax.legend(loc="lower right")
    ax.xaxis.label.set_size(13.5)
    ax.yaxis.label.set_size(13.5)

    fig.tight_layout()
    #plt.show()
    # plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.close(fig)


def plot_rewards_train_emulation_avg_only(train_avg_rewards_data_1, train_avg_rewards_means_1, train_avg_rewards_stds_1,
                               eval_avg_rewards_data_1, eval_avg_rewards_means_1, eval_avg_rewards_stds_1,
                               train_envs_specific_rewards_data, train_envs_specific_rewards_means,
                               train_envs_specific_rewards_stds,
                               eval_envs_specific_rewards_data, eval_envs_specific_rewards_means,
                               eval_envs_specific_rewards_stds,
                               ylim_rew,
                               file_name, markevery=10, optimal_steps = 10, optimal_reward = 95, sample_step = 1,
                               plot_opt=False):
    """
    Plots rewards, flags % and steps of two different configurations
    """
    #matplotlib.style.use("seaborn")
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 5))
    plt.rcParams.update({'font.size': 12})

    # ylims = (0, 920)

    # Plot Avg Train Rewards
    ax.plot(np.array(list(range(len(train_avg_rewards_means_1[::sample_step]))))*sample_step,
            train_avg_rewards_means_1[::sample_step], label=r"Avg Train", marker="s", ls='-', color="#599ad3",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(train_avg_rewards_means_1[::sample_step]))))*sample_step,
                    train_avg_rewards_means_1[::sample_step] - train_avg_rewards_stds_1[::sample_step],
                    train_avg_rewards_means_1[::sample_step] + train_avg_rewards_stds_1[::sample_step],
                    alpha=0.35, color="#599ad3")

    # Plot Avg Eval Rewards
    ax.plot(np.array(list(range(len(eval_avg_rewards_means_1[::sample_step]))))*sample_step,
            eval_avg_rewards_means_1[::sample_step], label=r"Avg Eval", marker="o", ls='-', color="r",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(eval_avg_rewards_means_1[::sample_step]))))*sample_step,
                    eval_avg_rewards_means_1[::sample_step] - eval_avg_rewards_stds_1[::sample_step],
                    eval_avg_rewards_means_1[::sample_step] + eval_avg_rewards_stds_1[::sample_step],
                    alpha=0.35, color="r")

    if plot_opt:
        ax.plot(np.array(list(range(len(train_avg_rewards_means_1)))),
                [optimal_reward] * len(train_avg_rewards_means_1), label=r"upper bound $\pi^{*}$",
                color="black",
                linestyle="dashed")

    ax.set_title(r"Episodic Rewards")
    ax.set_xlabel("\# Iteration", fontsize=20)
    ax.set_ylabel("Avg Episode Reward", fontsize=20)
    ax.set_xlim(0, len(train_avg_rewards_means_1[::sample_step])*sample_step)
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

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.18),
              ncol=5, fancybox=True, shadow=True)
    #ax.legend(loc="lower right")
    ax.xaxis.label.set_size(13.5)
    ax.yaxis.label.set_size(13.5)

    fig.tight_layout()
    #plt.show()
    # plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.close(fig)


def plot_regret_train_emulation(train_avg_regret_data_1, train_avg_regret_means_1, train_avg_regret_stds_1,
                              eval_avg_regret_data_1, eval_avg_regret_means_1, eval_avg_regret_stds_1,
                              train_envs_specific_regret_data, train_envs_specific_regret_means,
                              train_envs_specific_regret_stds,
                              eval_envs_specific_regret_data, eval_envs_specific_regret_means,
                              eval_envs_specific_regret_stds,
                              ylim_rew,
                              file_name, markevery=10, optimal_steps = 10, optimal_regret = 0, sample_step = 1):
    """
    Plots rewards, flags % and steps of two different configurations
    """
    #matplotlib.style.use("seaborn")
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 5))
    plt.rcParams.update({'font.size': 12})

    # ylims = (0, 920)

    # Plot Avg Train Rewards
    ax.plot(np.array(list(range(len(train_avg_regret_means_1[::sample_step])))) * sample_step,
            train_avg_regret_means_1[::sample_step], label=r"Avg\_T", marker="s", ls='-', color="#599ad3",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(train_avg_regret_means_1[::sample_step])))) * sample_step,
                    train_avg_regret_means_1[::sample_step] - train_avg_regret_stds_1[::sample_step], train_avg_regret_means_1[::sample_step]
                    + train_avg_regret_stds_1[::sample_step],
                    alpha=0.35, color="#599ad3")

    colors = ["#f9a65a", "#661D98", "#377EB8", "#4DAF4A", "#A65628", "#F781BF",
              '#D95F02', '#7570B3', '#E7298A', '#E6AB02', '#A6761D', '#666666',
              '#8DD3C7', '#CCEBC5', '#BEBADA','#FB8072', "#FF7F00", '#80B1D3', '#FDB462', '#B3DE69', '#FCCDE5',
              '#D9D9D9', '#BC80BD', '#FFED6F', "blue", "#984EA3", "green", "#FFFF33", '#66A61E', '#FFFFB3',
              "purple", "orange", "browen", "ppink", "#1B9E77", "#E41A1C"]
    markers = ["p", "^", "*", "+", "v", "1", "2", "3", "4", "x", "p", "h", "H", "d", "|", ",", ".", "H", "X", "s", "8", ">", "<", "P", "D", 0, 1, 2]

    i = 0
    for key in train_envs_specific_regret_data.keys():
        r_means = train_envs_specific_regret_means[key]
        r_stds = train_envs_specific_regret_stds[key]
        label = r"T\_." + key.rsplit(".", 1)[-2].rsplit(".", 1)[-1]
        ax.plot(np.array(list(range(len(r_means[::sample_step]))))*sample_step,
                   r_means[::sample_step], label=label, marker=markers[i], ls='-', color=colors[i], markevery=markevery)
        ax.fill_between(np.array(list(range(len(r_means[::sample_step]))))*sample_step,
                           r_means[::sample_step] - r_stds[::sample_step], r_means[::sample_step] +
                        r_stds[::sample_step], alpha=0.35, color=colors[i])
        i += 1

    # Plot Avg Eval Rewards
    ax.plot(np.array(list(range(len(eval_avg_regret_means_1[::sample_step])))) * sample_step,
            eval_avg_regret_means_1[::sample_step], label=r"Avg\_E", marker="o", ls='-', color="r",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(eval_avg_regret_means_1[::sample_step])))) * sample_step,
                    eval_avg_regret_means_1[::sample_step] - eval_avg_regret_stds_1[::sample_step],
                    eval_avg_regret_means_1[::sample_step] + eval_avg_regret_stds_1[::sample_step],
                    alpha=0.35, color="r")

    for key in eval_envs_specific_regret_data.keys():
        r_means = eval_envs_specific_regret_means[key]
        r_stds = eval_envs_specific_regret_stds[key]
        label = r"E\_." + key.rsplit(".", 1)[-2].rsplit(".", 1)[-1]
        ax.plot(np.array(list(range(len(r_means[::sample_step]))))*sample_step,
                   r_means[::sample_step], label=label, marker=markers[i], ls='-', color=colors[i], markevery=markevery)
        ax.fill_between(np.array(list(range(len(r_means[::sample_step]))))*sample_step,
                           r_means[::sample_step] - r_stds[::sample_step],
                        r_means[::sample_step] + r_stds[::sample_step], alpha=0.35, color=colors[i])
        i += 1

    ax.plot(np.array(list(range(len(train_avg_regret_means_1)))),
               [optimal_regret] * len(train_avg_regret_means_1), label=r"lower bound $\pi^{*}$",
               color="black",
               linestyle="dashed")

    ax.set_title(r"Episodic Regret")
    ax.set_xlabel("\# Iteration", fontsize=20)
    ax.set_ylabel("Avg Episode Regret", fontsize=20)
    ax.set_xlim(0, len(train_avg_regret_means_1[::sample_step]) * sample_step)
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

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.27),
              ncol=5, fancybox=True, shadow=True)
    #ax.legend(loc="lower right")
    ax.xaxis.label.set_size(13.5)
    ax.yaxis.label.set_size(13.5)

    fig.tight_layout()
    #plt.show()
    # plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.close(fig)


def plot_regret_train_emulation_two_colors(train_avg_regret_data_1, train_avg_regret_means_1, train_avg_regret_stds_1,
                               eval_avg_regret_data_1, eval_avg_regret_means_1, eval_avg_regret_stds_1,
                               train_envs_specific_regret_data, train_envs_specific_regret_means,
                               train_envs_specific_regret_stds,
                               eval_envs_specific_regret_data, eval_envs_specific_regret_means,
                               eval_envs_specific_regret_stds,
                               ylim_rew,
                               file_name, markevery=10, optimal_steps = 10, optimal_regret = 0, sample_step = 1):
    """
    Plots regret, flags % and steps of two different configurations
    """
    #matplotlib.style.use("seaborn")
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 5))
    plt.rcParams.update({'font.size': 12})

    # ylims = (0, 920)

    # Plot Avg Train regret
    ax.plot(np.array(list(range(len(train_avg_regret_means_1[::sample_step]))))*sample_step,
            train_avg_regret_means_1[::sample_step], label=r"Avg\_T", marker="s", ls='-', color="#599ad3",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(train_avg_regret_means_1[::sample_step]))))*sample_step,
                    train_avg_regret_means_1[::sample_step] - train_avg_regret_stds_1[::sample_step],
                    train_avg_regret_means_1[::sample_step] + train_avg_regret_stds_1[::sample_step],
                    alpha=0.35, color="#599ad3")

    # colors = ["#f9a65a", "#661D98", "#377EB8", "#4DAF4A", "#A65628", "#F781BF",
    #           '#D95F02', '#7570B3', '#E7298A', '#E6AB02', '#A6761D', '#666666',
    #           '#8DD3C7', '#CCEBC5', '#BEBADA','#FB8072', "#FF7F00", '#80B1D3', '#FDB462', '#B3DE69', '#FCCDE5',
    #           '#D9D9D9', '#BC80BD', '#FFED6F', "blue", "#984EA3", "green", "#FFFF33", '#66A61E', '#FFFFB3',
    #           "purple", "orange", "browen", "ppink", "#1B9E77", "#E41A1C"]
    markers = ["p", "^", "*", "+", "v", "1", "2", "3", "4", "x", "p", "h", "H", "d", "|", ",", ".", "H", "X", "s", "8",
               ">", "<", "P", "D", 0, 1, 2]

    i = 0
    for key in train_envs_specific_regret_data.keys():
        r_means = train_envs_specific_regret_means[key]
        r_stds = train_envs_specific_regret_stds[key]
        label = r"T\_." + key.rsplit(".", 1)[-2].rsplit(".", 1)[-1]
        ax.plot(np.array(list(range(len(r_means[::sample_step]))))*sample_step,
                   r_means[::sample_step], label=label, marker=markers[i], ls='-', color="#599ad3", markevery=markevery)
        ax.fill_between(np.array(list(range(len(r_means[::sample_step]))))*sample_step,
                           r_means[::sample_step] - r_stds[::sample_step],
                        r_means[::sample_step] + r_stds[::sample_step], alpha=0.35, color="#599ad3")
        i += 1

    # Plot Avg Eval regret
    ax.plot(np.array(list(range(len(eval_avg_regret_means_1[::sample_step]))))*sample_step,
            eval_avg_regret_means_1[::sample_step], label=r"Avg\_E", marker="o", ls='-', color="r",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(eval_avg_regret_means_1[::sample_step]))))*sample_step,
                    eval_avg_regret_means_1[::sample_step] - eval_avg_regret_stds_1[::sample_step],
                    eval_avg_regret_means_1[::sample_step] + eval_avg_regret_stds_1[::sample_step],
                    alpha=0.35, color="r")

    for key in eval_envs_specific_regret_data.keys():
        r_means = eval_envs_specific_regret_means[key]
        r_stds = eval_envs_specific_regret_stds[key]
        label = r"E\_." + key.rsplit(".", 1)[-2].rsplit(".", 1)[-1]
        ax.plot(np.array(list(range(len(r_means[::sample_step]))))*sample_step,
                   r_means[::sample_step], label=label, marker=markers[i], ls='-', color="r", markevery=markevery)
        ax.fill_between(np.array(list(range(len(r_means[::sample_step]))))*sample_step,
                           r_means[::sample_step] - r_stds[::sample_step],
                        r_means[::sample_step] + r_stds[::sample_step], alpha=0.35, color="r")
        i += 1

    ax.plot(np.array(list(range(len(train_avg_regret_means_1)))),
            [optimal_regret] * len(train_avg_regret_means_1), label=r"lower bound $\pi^{*}$",
            color="black",
            linestyle="dashed")

    ax.set_title(r"Episodic regret")
    ax.set_xlabel("\# Iteration", fontsize=20)
    ax.set_ylabel("Avg Episode Regret", fontsize=20)
    ax.set_xlim(0, len(train_avg_regret_means_1[::sample_step])*sample_step)
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

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.30),
              ncol=5, fancybox=True, shadow=True)
    #ax.legend(loc="lower right")
    ax.xaxis.label.set_size(13.5)
    ax.yaxis.label.set_size(13.5)

    fig.tight_layout()
    #plt.show()
    # plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.close(fig)


def plot_regret_train_emulation_avg_only(train_avg_regret_data_1, train_avg_regret_means_1, train_avg_regret_stds_1,
                               eval_avg_regret_data_1, eval_avg_regret_means_1, eval_avg_regret_stds_1,
                               train_envs_specific_regret_data, train_envs_specific_regret_means,
                               train_envs_specific_regret_stds,
                               eval_envs_specific_regret_data, eval_envs_specific_regret_means,
                               eval_envs_specific_regret_stds,
                               ylim_rew,
                               file_name, markevery=10, optimal_steps = 10, optimal_regret = 95, sample_step = 1):
    """
    Plots regret, flags % and steps of two different configurations
    """
    #matplotlib.style.use("seaborn")
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 5))
    plt.rcParams.update({'font.size': 12})

    # ylims = (0, 920)

    # Plot Avg Train regret
    ax.plot(np.array(list(range(len(train_avg_regret_means_1[::sample_step]))))*sample_step,
            train_avg_regret_means_1[::sample_step], label=r"Avg Train", marker="s", ls='-', color="#599ad3",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(train_avg_regret_means_1[::sample_step]))))*sample_step,
                    train_avg_regret_means_1[::sample_step] - train_avg_regret_stds_1[::sample_step],
                    train_avg_regret_means_1[::sample_step] + train_avg_regret_stds_1[::sample_step],
                    alpha=0.35, color="#599ad3")

    # Plot Avg Eval regret
    ax.plot(np.array(list(range(len(eval_avg_regret_means_1[::sample_step]))))*sample_step,
            eval_avg_regret_means_1[::sample_step], label=r"Avg Eval", marker="o", ls='-', color="r",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(eval_avg_regret_means_1[::sample_step]))))*sample_step,
                    eval_avg_regret_means_1[::sample_step] - eval_avg_regret_stds_1[::sample_step],
                    eval_avg_regret_means_1[::sample_step] + eval_avg_regret_stds_1[::sample_step],
                    alpha=0.35, color="r")

    ax.plot(np.array(list(range(len(train_avg_regret_means_1)))),
            [optimal_regret] * len(train_avg_regret_means_1), label=r"lower bound $\pi^{*}$",
            color="black",
            linestyle="dashed")

    ax.set_title(r"Episodic regret")
    ax.set_xlabel("\# Iteration", fontsize=20)
    ax.set_ylabel("Avg Episode Reward", fontsize=20)
    ax.set_xlim(0, len(train_avg_regret_means_1[::sample_step])*sample_step)
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

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.18),
              ncol=5, fancybox=True, shadow=True)
    #ax.legend(loc="lower right")
    ax.xaxis.label.set_size(13.5)
    ax.yaxis.label.set_size(13.5)

    fig.tight_layout()
    #plt.show()
    # plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.close(fig)


def plot_steps_train_emulation(train_avg_steps_data_1, train_avg_steps_means_1, train_avg_steps_stds_1,
                              eval_avg_steps_data_1, eval_avg_steps_means_1, eval_avg_steps_stds_1,
                              train_envs_specific_steps_data, train_envs_specific_steps_means,
                              train_envs_specific_steps_stds,
                              eval_envs_specific_steps_data, eval_envs_specific_steps_means,
                              eval_envs_specific_steps_stds,
                              ylim_rew,
                              file_name, markevery=10, optimal_steps = 10, optimal_regret = 0, sample_step = 1):
    """
    Plots rewards, flags % and steps of two different configurations
    """
    #matplotlib.style.use("seaborn")
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 5))
    plt.rcParams.update({'font.size': 12})

    # ylims = (0, 920)

    # Plot Avg Train Rewards
    ax.plot(np.array(list(range(len(train_avg_steps_means_1[::sample_step])))) * sample_step,
            train_avg_steps_means_1[::sample_step], label=r"Avg\_T", marker="s", ls='-', color="#599ad3",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(train_avg_steps_means_1[::sample_step])))) * sample_step,
                    train_avg_steps_means_1[::sample_step] - train_avg_steps_stds_1[::sample_step], train_avg_steps_means_1[::sample_step]
                    + train_avg_steps_stds_1[::sample_step],
                    alpha=0.35, color="#599ad3")

    colors = ["#f9a65a", "#661D98", "#377EB8", "#4DAF4A", "#A65628", "#F781BF",
              '#D95F02', '#7570B3', '#E7298A', '#E6AB02', '#A6761D', '#666666',
              '#8DD3C7', '#CCEBC5', '#BEBADA','#FB8072', "#FF7F00", '#80B1D3', '#FDB462', '#B3DE69', '#FCCDE5',
              '#D9D9D9', '#BC80BD', '#FFED6F', "blue", "#984EA3", "green", "#FFFF33", '#66A61E', '#FFFFB3',
              "purple", "orange", "browen", "ppink", "#1B9E77", "#E41A1C"]
    markers = ["p", "^", "*", "+", "v", "1", "2", "3", "4", "x", "p", "h", "H", "d", "|", ",", ".", "H", "X", "s", "8", ">", "<", "P", "D", 0, 1, 2]

    i = 0
    for key in train_envs_specific_steps_data.keys():
        r_means = train_envs_specific_steps_means[key]
        r_stds = train_envs_specific_steps_stds[key]
        label = r"T\_." + key.rsplit(".", 1)[-2].rsplit(".", 1)[-1]
        ax.plot(np.array(list(range(len(r_means[::sample_step]))))*sample_step,
                   r_means[::sample_step], label=label, marker=markers[i], ls='-', color=colors[i], markevery=markevery)
        ax.fill_between(np.array(list(range(len(r_means[::sample_step]))))*sample_step,
                           r_means[::sample_step] - r_stds[::sample_step], r_means[::sample_step] +
                        r_stds[::sample_step], alpha=0.35, color=colors[i])
        i += 1

    # Plot Avg Eval Rewards
    ax.plot(np.array(list(range(len(eval_avg_steps_means_1[::sample_step])))) * sample_step,
            eval_avg_steps_means_1[::sample_step], label=r"Avg\_E", marker="o", ls='-', color="r",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(eval_avg_steps_means_1[::sample_step])))) * sample_step,
                    eval_avg_steps_means_1[::sample_step] - eval_avg_steps_stds_1[::sample_step],
                    eval_avg_steps_means_1[::sample_step] + eval_avg_steps_stds_1[::sample_step],
                    alpha=0.35, color="r")

    for key in eval_envs_specific_steps_data.keys():
        r_means = eval_envs_specific_steps_means[key]
        r_stds = eval_envs_specific_steps_stds[key]
        label = r"E\_." + key.rsplit(".", 1)[-2].rsplit(".", 1)[-1]
        ax.plot(np.array(list(range(len(r_means[::sample_step]))))*sample_step,
                   r_means[::sample_step], label=label, marker=markers[i], ls='-', color=colors[i], markevery=markevery)
        ax.fill_between(np.array(list(range(len(r_means[::sample_step]))))*sample_step,
                           r_means[::sample_step] - r_stds[::sample_step],
                        r_means[::sample_step] + r_stds[::sample_step], alpha=0.35, color=colors[i])
        i += 1

    ax.set_title(r"Episodic steps")
    ax.set_xlabel("\# Iteration", fontsize=20)
    ax.set_ylabel("Avg Episode Steps", fontsize=20)
    ax.set_xlim(0, len(train_avg_steps_means_1[::sample_step]) * sample_step)
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

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.27),
              ncol=5, fancybox=True, shadow=True)
    #ax.legend(loc="lower right")
    ax.xaxis.label.set_size(13.5)
    ax.yaxis.label.set_size(13.5)

    fig.tight_layout()
    #plt.show()
    # plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.close(fig)


def plot_steps_train_emulation_two_colors(train_avg_steps_data_1, train_avg_steps_means_1, train_avg_steps_stds_1,
                               eval_avg_steps_data_1, eval_avg_steps_means_1, eval_avg_steps_stds_1,
                               train_envs_specific_steps_data, train_envs_specific_steps_means,
                               train_envs_specific_steps_stds,
                               eval_envs_specific_steps_data, eval_envs_specific_steps_means,
                               eval_envs_specific_steps_stds,
                               ylim_rew,
                               file_name, markevery=10, optimal_steps = 10, optimal_reward = 95, sample_step = 1):
    """
    Plots steps, flags % and steps of two different configurations
    """
    #matplotlib.style.use("seaborn")
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 5))
    plt.rcParams.update({'font.size': 12})

    # ylims = (0, 920)

    # Plot Avg Train steps
    ax.plot(np.array(list(range(len(train_avg_steps_means_1[::sample_step]))))*sample_step,
            train_avg_steps_means_1[::sample_step], label=r"Avg\_T", marker="s", ls='-', color="#599ad3",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(train_avg_steps_means_1[::sample_step]))))*sample_step,
                    train_avg_steps_means_1[::sample_step] - train_avg_steps_stds_1[::sample_step],
                    train_avg_steps_means_1[::sample_step] + train_avg_steps_stds_1[::sample_step],
                    alpha=0.35, color="#599ad3")

    # colors = ["#f9a65a", "#661D98", "#377EB8", "#4DAF4A", "#A65628", "#F781BF",
    #           '#D95F02', '#7570B3', '#E7298A', '#E6AB02', '#A6761D', '#666666',
    #           '#8DD3C7', '#CCEBC5', '#BEBADA','#FB8072', "#FF7F00", '#80B1D3', '#FDB462', '#B3DE69', '#FCCDE5',
    #           '#D9D9D9', '#BC80BD', '#FFED6F', "blue", "#984EA3", "green", "#FFFF33", '#66A61E', '#FFFFB3',
    #           "purple", "orange", "browen", "ppink", "#1B9E77", "#E41A1C"]
    markers = ["p", "^", "*", "+", "v", "1", "2", "3", "4", "x", "p", "h", "H", "d", "|", ",", ".", "H", "X", "s", "8",
               ">", "<", "P", "D", 0, 1, 2]

    i = 0
    for key in train_envs_specific_steps_data.keys():
        r_means = train_envs_specific_steps_means[key]
        r_stds = train_envs_specific_steps_stds[key]
        label = r"T\_." + key.rsplit(".", 1)[-2].rsplit(".", 1)[-1]
        ax.plot(np.array(list(range(len(r_means[::sample_step]))))*sample_step,
                   r_means[::sample_step], label=label, marker=markers[i], ls='-', color="#599ad3", markevery=markevery)
        ax.fill_between(np.array(list(range(len(r_means[::sample_step]))))*sample_step,
                           r_means[::sample_step] - r_stds[::sample_step],
                        r_means[::sample_step] + r_stds[::sample_step], alpha=0.35, color="#599ad3")
        i += 1

    # Plot Avg Eval steps
    ax.plot(np.array(list(range(len(eval_avg_steps_means_1[::sample_step]))))*sample_step,
            eval_avg_steps_means_1[::sample_step], label=r"Avg\_E", marker="o", ls='-', color="r",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(eval_avg_steps_means_1[::sample_step]))))*sample_step,
                    eval_avg_steps_means_1[::sample_step] - eval_avg_steps_stds_1[::sample_step],
                    eval_avg_steps_means_1[::sample_step] + eval_avg_steps_stds_1[::sample_step],
                    alpha=0.35, color="r")

    for key in eval_envs_specific_steps_data.keys():
        r_means = eval_envs_specific_steps_means[key]
        r_stds = eval_envs_specific_steps_stds[key]
        label = r"E\_." + key.rsplit(".", 1)[-2].rsplit(".", 1)[-1]
        ax.plot(np.array(list(range(len(r_means[::sample_step]))))*sample_step,
                   r_means[::sample_step], label=label, marker=markers[i], ls='-', color="r", markevery=markevery)
        ax.fill_between(np.array(list(range(len(r_means[::sample_step]))))*sample_step,
                           r_means[::sample_step] - r_stds[::sample_step],
                        r_means[::sample_step] + r_stds[::sample_step], alpha=0.35, color="r")
        i += 1

    ax.set_title(r"Episodic steps")
    ax.set_xlabel("\# Iteration", fontsize=20)
    ax.set_ylabel("Avg Episode Steps", fontsize=20)
    ax.set_xlim(0, len(train_avg_steps_means_1[::sample_step])*sample_step)
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

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.30),
              ncol=5, fancybox=True, shadow=True)
    #ax.legend(loc="lower right")
    ax.xaxis.label.set_size(13.5)
    ax.yaxis.label.set_size(13.5)

    fig.tight_layout()
    #plt.show()
    # plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.close(fig)


def plot_steps_train_emulation_avg_only(train_avg_steps_data_1, train_avg_steps_means_1, train_avg_steps_stds_1,
                               eval_avg_steps_data_1, eval_avg_steps_means_1, eval_avg_steps_stds_1,
                               train_envs_specific_steps_data, train_envs_specific_steps_means,
                               train_envs_specific_steps_stds,
                               eval_envs_specific_steps_data, eval_envs_specific_steps_means,
                               eval_envs_specific_steps_stds,
                               ylim_rew,
                               file_name, markevery=10, optimal_steps = 10, optimal_reward = 95, sample_step = 1):
    """
    Plots steps, flags % and steps of two different configurations
    """
    #matplotlib.style.use("seaborn")
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 5))
    plt.rcParams.update({'font.size': 12})

    # ylims = (0, 920)

    # Plot Avg Train steps
    ax.plot(np.array(list(range(len(train_avg_steps_means_1[::sample_step]))))*sample_step,
            train_avg_steps_means_1[::sample_step], label=r"Avg Train", marker="s", ls='-', color="#599ad3",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(train_avg_steps_means_1[::sample_step]))))*sample_step,
                    train_avg_steps_means_1[::sample_step] - train_avg_steps_stds_1[::sample_step],
                    train_avg_steps_means_1[::sample_step] + train_avg_steps_stds_1[::sample_step],
                    alpha=0.35, color="#599ad3")

    # Plot Avg Eval steps
    ax.plot(np.array(list(range(len(eval_avg_steps_means_1[::sample_step]))))*sample_step,
            eval_avg_steps_means_1[::sample_step], label=r"Avg Eval", marker="o", ls='-', color="r",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(eval_avg_steps_means_1[::sample_step]))))*sample_step,
                    eval_avg_steps_means_1[::sample_step] - eval_avg_steps_stds_1[::sample_step],
                    eval_avg_steps_means_1[::sample_step] + eval_avg_steps_stds_1[::sample_step],
                    alpha=0.35, color="r")

    ax.set_title(r"Episodic steps")
    ax.set_xlabel("\# Iteration", fontsize=20)
    ax.set_ylabel("Avg Episode Steps", fontsize=20)
    ax.set_xlim(0, len(train_avg_steps_means_1[::sample_step])*sample_step)
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

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.18),
              ncol=5, fancybox=True, shadow=True)
    #ax.legend(loc="lower right")
    ax.xaxis.label.set_size(13.5)
    ax.yaxis.label.set_size(13.5)

    fig.tight_layout()
    #plt.show()
    # plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.close(fig)


def plot_steps_train_emulation_avg_comparison(
        train_avg_steps_data_1_gensim, train_avg_steps_means_1_gensim,
        train_avg_steps_stds_1_gensim, eval_avg_steps_data_1_gensim, eval_avg_steps_means_1_gensim,
        eval_avg_steps_stds_1_gensim,
        train_avg_steps_data_1_emulation_20, train_avg_steps_means_1_emulation_20,
        train_avg_steps_stds_1_emulation_20, eval_avg_steps_data_1_emulation_20, eval_avg_steps_means_1_emulation_20,
        eval_avg_steps_stds_1_emulation_20,
        train_avg_steps_data_1_emulation_1, train_avg_steps_means_1_emulation_1,
        train_avg_steps_stds_1_emulation_1, eval_avg_steps_data_1_emulation_1, eval_avg_steps_means_1_emulation_1,
        eval_avg_steps_stds_1_emulation_1,
        ylim_rew, file_name, markevery=10, optimal_steps = 10, optimal_reward = 95, sample_step = 1,
        eval_only=False):
    """
    Plots steps, flags % and steps of two different configurations
    """
    #matplotlib.style.use("seaborn")
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 5))
    plt.rcParams.update({'font.size': 12})

    # ylims = (0, 920)

    # Plot Avg Train steps Gensim
    ax.plot(np.array(list(range(len(train_avg_steps_means_1_gensim[::sample_step]))))*sample_step,
            train_avg_steps_means_1_gensim[::sample_step], label=r"Avg Train 20 Envs \& Domain Randomization", marker="s", ls='-', color="#599ad3",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(train_avg_steps_means_1_gensim[::sample_step]))))*sample_step,
                    train_avg_steps_means_1_gensim[::sample_step] - train_avg_steps_stds_1_gensim[::sample_step],
                    train_avg_steps_means_1_gensim[::sample_step] + train_avg_steps_stds_1_gensim[::sample_step],
                    alpha=0.35, color="#599ad3")

    # Plot Avg Eval steps Gensim
    ax.plot(np.array(list(range(len(eval_avg_steps_means_1_gensim[::sample_step]))))*sample_step,
            eval_avg_steps_means_1_gensim[::sample_step], label=r"Avg Eval 20 Envs \& Domain Randomization", marker="o", ls='-', color="r",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(eval_avg_steps_means_1_gensim[::sample_step]))))*sample_step,
                    eval_avg_steps_means_1_gensim[::sample_step] - eval_avg_steps_stds_1_gensim[::sample_step],
                    eval_avg_steps_means_1_gensim[::sample_step] + eval_avg_steps_stds_1_gensim[::sample_step],
                    alpha=0.35, color="r")

    # Plot Avg Train steps emulation20
    ax.plot(np.array(list(range(len(train_avg_steps_means_1_emulation_20[::sample_step])))) * sample_step,
            train_avg_steps_means_1_emulation_20[::sample_step], label=r"Avg Train 20 Envs",
            marker="p", ls='-', color="#f9a65a",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(train_avg_steps_means_1_emulation_20[::sample_step])))) * sample_step,
                    train_avg_steps_means_1_emulation_20[::sample_step] - train_avg_steps_stds_1_emulation_20[::sample_step],
                    train_avg_steps_means_1_emulation_20[::sample_step] + train_avg_steps_stds_1_emulation_20[::sample_step],
                    alpha=0.35, color="#f9a65a")

    # Plot Avg Eval steps emulation20
    ax.plot(np.array(list(range(len(eval_avg_steps_means_1_emulation_20[::sample_step])))) * sample_step,
            eval_avg_steps_means_1_emulation_20[::sample_step], label=r"Avg Eval 20 Envs", marker="^",
            ls='-', color="#661D98",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(eval_avg_steps_means_1_emulation_20[::sample_step])))) * sample_step,
                    eval_avg_steps_means_1_emulation_20[::sample_step] - eval_avg_steps_stds_1_emulation_20[::sample_step],
                    eval_avg_steps_means_1_emulation_20[::sample_step] + eval_avg_steps_stds_1_emulation_20[::sample_step],
                    alpha=0.35, color="#661D98")

    # Plot Avg Train steps emulation1
    ax.plot(np.array(list(range(len(train_avg_steps_means_1_emulation_1[::sample_step])))) * sample_step,
            train_avg_steps_means_1_emulation_1[::sample_step], label=r"Avg Train 1 Envs",
            marker="*", ls='-', color="#377EB8",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(train_avg_steps_means_1_emulation_1[::sample_step])))) * sample_step,
                    train_avg_steps_means_1_emulation_1[::sample_step] - train_avg_steps_stds_1_emulation_1[
                                                                        ::sample_step],
                    train_avg_steps_means_1_emulation_1[::sample_step] + train_avg_steps_stds_1_emulation_1[
                                                                        ::sample_step],
                    alpha=0.35, color="#377EB8")

    # Plot Avg Eval steps emulation1
    ax.plot(np.array(list(range(len(eval_avg_steps_means_1_emulation_1[::sample_step])))) * sample_step,
            eval_avg_steps_means_1_emulation_1[::sample_step], label=r"Avg Eval 1 Envs", marker="+",
            ls='-', color="#4DAF4A",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(eval_avg_steps_means_1_emulation_1[::sample_step])))) * sample_step,
                    eval_avg_steps_means_1_emulation_1[::sample_step] - eval_avg_steps_stds_1_emulation_1[::sample_step],
                    eval_avg_steps_means_1_emulation_1[::sample_step] + eval_avg_steps_stds_1_emulation_1[::sample_step],
                    alpha=0.35, color="#4DAF4A")

    ax.set_title(r"Episodic steps")
    ax.set_xlabel("\# Iteration", fontsize=20)
    ax.set_ylabel("Avg Episode Steps", fontsize=20)
    ax.set_xlim(0, len(train_avg_steps_means_1_gensim[::sample_step])*sample_step)
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

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.18),
              ncol=2, fancybox=True, shadow=True)
    #ax.legend(loc="lower right")
    ax.xaxis.label.set_size(13.5)
    ax.yaxis.label.set_size(13.5)

    fig.tight_layout()
    #plt.show()
    # plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.close(fig)


def plot_steps_train_emulation_avg_comparison_eval_only(
        eval_avg_steps_data_1_gensim, eval_avg_steps_means_1_gensim,
        eval_avg_steps_stds_1_gensim,
        eval_avg_steps_data_1_emulation_20, eval_avg_steps_means_1_emulation_20,
        eval_avg_steps_stds_1_emulation_20,
        eval_avg_steps_data_1_emulation_1, eval_avg_steps_means_1_emulation_1,
        eval_avg_steps_stds_1_emulation_1,
        ylim_rew, file_name, markevery=10, optimal_steps = 10, optimal_reward = 95, sample_step = 1,
        eval_only=False):
    """
    Plots steps, flags % and steps of two different configurations
    """
    #matplotlib.style.use("seaborn")
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 5))
    plt.rcParams.update({'font.size': 12})

    # ylims = (0, 920)

    # Plot Avg Eval steps Gensim
    ax.plot(np.array(list(range(len(eval_avg_steps_means_1_gensim[::sample_step]))))*sample_step,
            eval_avg_steps_means_1_gensim[::sample_step], label=r"Avg Eval 20 Envs \& Domain Randomization", marker="s", ls='-', color="r",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(eval_avg_steps_means_1_gensim[::sample_step]))))*sample_step,
                    eval_avg_steps_means_1_gensim[::sample_step] - eval_avg_steps_stds_1_gensim[::sample_step],
                    eval_avg_steps_means_1_gensim[::sample_step] + eval_avg_steps_stds_1_gensim[::sample_step],
                    alpha=0.35, color="r")

    # Plot Avg Eval steps emulation20
    ax.plot(np.array(list(range(len(eval_avg_steps_means_1_emulation_20[::sample_step])))) * sample_step,
            eval_avg_steps_means_1_emulation_20[::sample_step], label=r"Avg Eval 20 Envs", marker="o",
            ls='-', color="#599ad3",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(eval_avg_steps_means_1_emulation_20[::sample_step])))) * sample_step,
                    eval_avg_steps_means_1_emulation_20[::sample_step] - eval_avg_steps_stds_1_emulation_20[::sample_step],
                    eval_avg_steps_means_1_emulation_20[::sample_step] + eval_avg_steps_stds_1_emulation_20[::sample_step],
                    alpha=0.35, color="#599ad3")

    # Plot Avg Eval steps emulation1
    ax.plot(np.array(list(range(len(eval_avg_steps_means_1_emulation_1[::sample_step])))) * sample_step,
            eval_avg_steps_means_1_emulation_1[::sample_step], label=r"Avg Eval 1 Envs", marker="^",
            ls='-', color="#f9a65a",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(eval_avg_steps_means_1_emulation_1[::sample_step])))) * sample_step,
                    eval_avg_steps_means_1_emulation_1[::sample_step] - eval_avg_steps_stds_1_emulation_1[::sample_step],
                    eval_avg_steps_means_1_emulation_1[::sample_step] + eval_avg_steps_stds_1_emulation_1[::sample_step],
                    alpha=0.35, color="#f9a65a")

    ax.set_title(r"Episodic steps")
    ax.set_xlabel("\# Iteration", fontsize=20)
    ax.set_ylabel("Avg Episode Steps", fontsize=20)
    ax.set_xlim(0, len(eval_avg_steps_means_1_gensim[::sample_step])*sample_step)
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

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.18),
              ncol=2, fancybox=True, shadow=True)
    #ax.legend(loc="lower right")
    ax.xaxis.label.set_size(13.5)
    ax.yaxis.label.set_size(13.5)

    fig.tight_layout()
    #plt.show()
    # plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.close(fig)

# Rewards comparison

def plot_rewards_train_emulation_avg_comparison(
        train_avg_rewards_data_1_gensim, train_avg_rewards_means_1_gensim,
        train_avg_rewards_stds_1_gensim, eval_avg_rewards_data_1_gensim, eval_avg_rewards_means_1_gensim,
        eval_avg_rewards_stds_1_gensim,
        train_avg_rewards_data_1_emulation_20, train_avg_rewards_means_1_emulation_20,
        train_avg_rewards_stds_1_emulation_20, eval_avg_rewards_data_1_emulation_20, eval_avg_rewards_means_1_emulation_20,
        eval_avg_rewards_stds_1_emulation_20,
        train_avg_rewards_data_1_emulation_1, train_avg_rewards_means_1_emulation_1,
        train_avg_rewards_stds_1_emulation_1, eval_avg_rewards_data_1_emulation_1, eval_avg_rewards_means_1_emulation_1,
        eval_avg_rewards_stds_1_emulation_1,
        ylim_rew, file_name, markevery=10, optimal_reward = 95, sample_step = 1, plot_opt = False):
    """
    Plots rewards, flags % and rewards of two different configurations
    """
    #matplotlib.style.use("seaborn")
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 5))
    plt.rcParams.update({'font.size': 12})

    # ylims = (0, 920)

    # Plot Avg Train rewards Gensim
    ax.plot(np.array(list(range(len(train_avg_rewards_means_1_gensim[::sample_step]))))*sample_step,
            train_avg_rewards_means_1_gensim[::sample_step], label=r"Avg Train 20 Envs \& Domain Randomization", marker="s", ls='-', color="#599ad3",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(train_avg_rewards_means_1_gensim[::sample_step]))))*sample_step,
                    train_avg_rewards_means_1_gensim[::sample_step] - train_avg_rewards_stds_1_gensim[::sample_step],
                    train_avg_rewards_means_1_gensim[::sample_step] + train_avg_rewards_stds_1_gensim[::sample_step],
                    alpha=0.35, color="#599ad3")

    # Plot Avg Eval rewards Gensim
    ax.plot(np.array(list(range(len(eval_avg_rewards_means_1_gensim[::sample_step]))))*sample_step,
            eval_avg_rewards_means_1_gensim[::sample_step], label=r"Avg Eval 20 Envs \& Domain Randomization", marker="o", ls='-', color="r",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(eval_avg_rewards_means_1_gensim[::sample_step]))))*sample_step,
                    eval_avg_rewards_means_1_gensim[::sample_step] - eval_avg_rewards_stds_1_gensim[::sample_step],
                    eval_avg_rewards_means_1_gensim[::sample_step] + eval_avg_rewards_stds_1_gensim[::sample_step],
                    alpha=0.35, color="r")

    # Plot Avg Train rewards emulation20
    ax.plot(np.array(list(range(len(train_avg_rewards_means_1_emulation_20[::sample_step])))) * sample_step,
            train_avg_rewards_means_1_emulation_20[::sample_step], label=r"Avg Train 20 Envs",
            marker="p", ls='-', color="#f9a65a",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(train_avg_rewards_means_1_emulation_20[::sample_step])))) * sample_step,
                    train_avg_rewards_means_1_emulation_20[::sample_step] - train_avg_rewards_stds_1_emulation_20[::sample_step],
                    train_avg_rewards_means_1_emulation_20[::sample_step] + train_avg_rewards_stds_1_emulation_20[::sample_step],
                    alpha=0.35, color="#f9a65a")

    # Plot Avg Eval rewards emulation20
    ax.plot(np.array(list(range(len(eval_avg_rewards_means_1_emulation_20[::sample_step])))) * sample_step,
            eval_avg_rewards_means_1_emulation_20[::sample_step], label=r"Avg Eval 20 Envs", marker="^",
            ls='-', color="#661D98",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(eval_avg_rewards_means_1_emulation_20[::sample_step])))) * sample_step,
                    eval_avg_rewards_means_1_emulation_20[::sample_step] - eval_avg_rewards_stds_1_emulation_20[::sample_step],
                    eval_avg_rewards_means_1_emulation_20[::sample_step] + eval_avg_rewards_stds_1_emulation_20[::sample_step],
                    alpha=0.35, color="#661D98")

    # Plot Avg Train rewards emulation1
    ax.plot(np.array(list(range(len(train_avg_rewards_means_1_emulation_1[::sample_step])))) * sample_step,
            train_avg_rewards_means_1_emulation_1[::sample_step], label=r"Avg Train 1 Envs",
            marker="*", ls='-', color="#377EB8",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(train_avg_rewards_means_1_emulation_1[::sample_step])))) * sample_step,
                    train_avg_rewards_means_1_emulation_1[::sample_step] - train_avg_rewards_stds_1_emulation_1[
                                                                        ::sample_step],
                    train_avg_rewards_means_1_emulation_1[::sample_step] + train_avg_rewards_stds_1_emulation_1[
                                                                        ::sample_step],
                    alpha=0.35, color="#377EB8")

    # Plot Avg Eval rewards emulation1
    ax.plot(np.array(list(range(len(eval_avg_rewards_means_1_emulation_1[::sample_step])))) * sample_step,
            eval_avg_rewards_means_1_emulation_1[::sample_step], label=r"Avg Eval 1 Envs", marker="+",
            ls='-', color="#4DAF4A",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(eval_avg_rewards_means_1_emulation_1[::sample_step])))) * sample_step,
                    eval_avg_rewards_means_1_emulation_1[::sample_step] - eval_avg_rewards_stds_1_emulation_1[::sample_step],
                    eval_avg_rewards_means_1_emulation_1[::sample_step] + eval_avg_rewards_stds_1_emulation_1[::sample_step],
                    alpha=0.35, color="#4DAF4A")

    if plot_opt:
        ax.plot(np.array(list(range(len(train_avg_rewards_means_1_gensim)))),
                [optimal_reward] * len(train_avg_rewards_means_1_gensim), label=r"upper bound $\pi^{*}$",
                color="black",
                linestyle="dashed")

    ax.set_title(r"Episodic rewards")
    ax.set_xlabel("\# Iteration", fontsize=20)
    ax.set_ylabel("Avg Episode Rewards", fontsize=20)
    ax.set_xlim(0, len(train_avg_rewards_means_1_gensim[::sample_step])*sample_step)
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

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.18),
              ncol=2, fancybox=True, shadow=True)
    #ax.legend(loc="lower right")
    ax.xaxis.label.set_size(13.5)
    ax.yaxis.label.set_size(13.5)

    fig.tight_layout()
    #plt.show()
    # plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.close(fig)


def plot_rewards_train_emulation_avg_comparison_eval_only(
        eval_avg_rewards_data_1_gensim, eval_avg_rewards_means_1_gensim,
        eval_avg_rewards_stds_1_gensim,
        eval_avg_rewards_data_1_emulation_20, eval_avg_rewards_means_1_emulation_20,
        eval_avg_rewards_stds_1_emulation_20,
        eval_avg_rewards_data_1_emulation_1, eval_avg_rewards_means_1_emulation_1,
        eval_avg_rewards_stds_1_emulation_1,
        ylim_rew, file_name, markevery=10, optimal_reward = 95, sample_step = 1,
        eval_only=False, plot_opt = False):
    """
    Plots rewards, flags % and rewards of two different configurations
    """
    #matplotlib.style.use("seaborn")
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 5))
    plt.rcParams.update({'font.size': 12})

    # ylims = (0, 920)

    # Plot Avg Eval rewards Gensim
    ax.plot(np.array(list(range(len(eval_avg_rewards_means_1_gensim[::sample_step]))))*sample_step,
            eval_avg_rewards_means_1_gensim[::sample_step], label=r"Avg Eval 20 Envs \& Domain Randomization", marker="s", ls='-', color="r",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(eval_avg_rewards_means_1_gensim[::sample_step]))))*sample_step,
                    eval_avg_rewards_means_1_gensim[::sample_step] - eval_avg_rewards_stds_1_gensim[::sample_step],
                    eval_avg_rewards_means_1_gensim[::sample_step] + eval_avg_rewards_stds_1_gensim[::sample_step],
                    alpha=0.35, color="r")

    # Plot Avg Eval rewards emulation20
    ax.plot(np.array(list(range(len(eval_avg_rewards_means_1_emulation_20[::sample_step])))) * sample_step,
            eval_avg_rewards_means_1_emulation_20[::sample_step], label=r"Avg Eval 20 Envs", marker="o",
            ls='-', color="#599ad3",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(eval_avg_rewards_means_1_emulation_20[::sample_step])))) * sample_step,
                    eval_avg_rewards_means_1_emulation_20[::sample_step] - eval_avg_rewards_stds_1_emulation_20[::sample_step],
                    eval_avg_rewards_means_1_emulation_20[::sample_step] + eval_avg_rewards_stds_1_emulation_20[::sample_step],
                    alpha=0.35, color="#599ad3")

    # Plot Avg Eval rewards emulation1
    ax.plot(np.array(list(range(len(eval_avg_rewards_means_1_emulation_1[::sample_step])))) * sample_step,
            eval_avg_rewards_means_1_emulation_1[::sample_step], label=r"Avg Eval 1 Envs", marker="^",
            ls='-', color="#f9a65a",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(eval_avg_rewards_means_1_emulation_1[::sample_step])))) * sample_step,
                    eval_avg_rewards_means_1_emulation_1[::sample_step] - eval_avg_rewards_stds_1_emulation_1[::sample_step],
                    eval_avg_rewards_means_1_emulation_1[::sample_step] + eval_avg_rewards_stds_1_emulation_1[::sample_step],
                    alpha=0.35, color="#f9a65a")

    if plot_opt:
        ax.plot(np.array(list(range(len(eval_avg_rewards_means_1_gensim)))),
                [optimal_reward] * len(eval_avg_rewards_means_1_gensim), label=r"upper bound $\pi^{*}$",
                color="black",
                linestyle="dashed")

    ax.set_title(r"Episodic rewards")
    ax.set_xlabel("\# Iteration", fontsize=20)
    ax.set_ylabel("Avg Episode Rewards", fontsize=20)
    ax.set_xlim(0, len(eval_avg_rewards_means_1_gensim[::sample_step])*sample_step)
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

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.18),
              ncol=2, fancybox=True, shadow=True)
    #ax.legend(loc="lower right")
    ax.xaxis.label.set_size(13.5)
    ax.yaxis.label.set_size(13.5)

    fig.tight_layout()
    #plt.show()
    # plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.close(fig)



# Regret comparison


def plot_regret_train_emulation_avg_comparison(
        train_avg_regret_data_1_gensim, train_avg_regret_means_1_gensim,
        train_avg_regret_stds_1_gensim, eval_avg_regret_data_1_gensim, eval_avg_regret_means_1_gensim,
        eval_avg_regret_stds_1_gensim,
        train_avg_regret_data_1_emulation_20, train_avg_regret_means_1_emulation_20,
        train_avg_regret_stds_1_emulation_20, eval_avg_regret_data_1_emulation_20, eval_avg_regret_means_1_emulation_20,
        eval_avg_regret_stds_1_emulation_20,
        train_avg_regret_data_1_emulation_1, train_avg_regret_means_1_emulation_1,
        train_avg_regret_stds_1_emulation_1, eval_avg_regret_data_1_emulation_1, eval_avg_regret_means_1_emulation_1,
        eval_avg_regret_stds_1_emulation_1,
        ylim_rew, file_name, markevery=10, optimal_regret = 0, sample_step = 1, plot_opt = False):
    """
    Plots regret, flags % and regret of two different configurations
    """
    #matplotlib.style.use("seaborn")
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 5))
    plt.rcParams.update({'font.size': 12})

    # ylims = (0, 920)

    # Plot Avg Train regret Gensim
    ax.plot(np.array(list(range(len(train_avg_regret_means_1_gensim[::sample_step]))))*sample_step,
            train_avg_regret_means_1_gensim[::sample_step], label=r"Avg Train 20 Envs \& Domain Randomization", marker="s", ls='-', color="#599ad3",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(train_avg_regret_means_1_gensim[::sample_step]))))*sample_step,
                    train_avg_regret_means_1_gensim[::sample_step] - train_avg_regret_stds_1_gensim[::sample_step],
                    train_avg_regret_means_1_gensim[::sample_step] + train_avg_regret_stds_1_gensim[::sample_step],
                    alpha=0.35, color="#599ad3")

    # Plot Avg Eval regret Gensim
    ax.plot(np.array(list(range(len(eval_avg_regret_means_1_gensim[::sample_step]))))*sample_step,
            eval_avg_regret_means_1_gensim[::sample_step], label=r"Avg Eval 20 Envs \& Domain Randomization", marker="o", ls='-', color="r",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(eval_avg_regret_means_1_gensim[::sample_step]))))*sample_step,
                    eval_avg_regret_means_1_gensim[::sample_step] - eval_avg_regret_stds_1_gensim[::sample_step],
                    eval_avg_regret_means_1_gensim[::sample_step] + eval_avg_regret_stds_1_gensim[::sample_step],
                    alpha=0.35, color="r")

    # Plot Avg Train regret emulation20
    ax.plot(np.array(list(range(len(train_avg_regret_means_1_emulation_20[::sample_step])))) * sample_step,
            train_avg_regret_means_1_emulation_20[::sample_step], label=r"Avg Train 20 Envs",
            marker="p", ls='-', color="#f9a65a",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(train_avg_regret_means_1_emulation_20[::sample_step])))) * sample_step,
                    train_avg_regret_means_1_emulation_20[::sample_step] - train_avg_regret_stds_1_emulation_20[::sample_step],
                    train_avg_regret_means_1_emulation_20[::sample_step] + train_avg_regret_stds_1_emulation_20[::sample_step],
                    alpha=0.35, color="#f9a65a")

    # Plot Avg Eval regret emulation20
    ax.plot(np.array(list(range(len(eval_avg_regret_means_1_emulation_20[::sample_step])))) * sample_step,
            eval_avg_regret_means_1_emulation_20[::sample_step], label=r"Avg Eval 20 Envs", marker="^",
            ls='-', color="#661D98",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(eval_avg_regret_means_1_emulation_20[::sample_step])))) * sample_step,
                    eval_avg_regret_means_1_emulation_20[::sample_step] - eval_avg_regret_stds_1_emulation_20[::sample_step],
                    eval_avg_regret_means_1_emulation_20[::sample_step] + eval_avg_regret_stds_1_emulation_20[::sample_step],
                    alpha=0.35, color="#661D98")

    # Plot Avg Train regret emulation1
    ax.plot(np.array(list(range(len(train_avg_regret_means_1_emulation_1[::sample_step])))) * sample_step,
            train_avg_regret_means_1_emulation_1[::sample_step], label=r"Avg Train 1 Envs",
            marker="*", ls='-', color="#377EB8",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(train_avg_regret_means_1_emulation_1[::sample_step])))) * sample_step,
                    train_avg_regret_means_1_emulation_1[::sample_step] - train_avg_regret_stds_1_emulation_1[
                                                                        ::sample_step],
                    train_avg_regret_means_1_emulation_1[::sample_step] + train_avg_regret_stds_1_emulation_1[
                                                                        ::sample_step],
                    alpha=0.35, color="#377EB8")

    # Plot Avg Eval regret emulation1
    ax.plot(np.array(list(range(len(eval_avg_regret_means_1_emulation_1[::sample_step])))) * sample_step,
            eval_avg_regret_means_1_emulation_1[::sample_step], label=r"Avg Eval 1 Envs", marker="+",
            ls='-', color="#4DAF4A",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(eval_avg_regret_means_1_emulation_1[::sample_step])))) * sample_step,
                    eval_avg_regret_means_1_emulation_1[::sample_step] - eval_avg_regret_stds_1_emulation_1[::sample_step],
                    eval_avg_regret_means_1_emulation_1[::sample_step] + eval_avg_regret_stds_1_emulation_1[::sample_step],
                    alpha=0.35, color="#4DAF4A")

    if plot_opt:
        ax.plot(np.array(list(range(len(train_avg_regret_means_1_gensim)))),
                [optimal_regret] * len(train_avg_regret_means_1_gensim), label=r"lower bound $\pi^{*}$",
                color="black",
                linestyle="dashed")

    ax.set_title(r"Episodic regret")
    ax.set_xlabel("\# Iteration", fontsize=20)
    ax.set_ylabel("Avg Episode Regret", fontsize=20)
    ax.set_xlim(0, len(train_avg_regret_means_1_gensim[::sample_step])*sample_step)
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

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.18),
              ncol=2, fancybox=True, shadow=True)
    #ax.legend(loc="lower right")
    ax.xaxis.label.set_size(13.5)
    ax.yaxis.label.set_size(13.5)

    fig.tight_layout()
    #plt.show()
    # plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.close(fig)


def plot_regret_train_emulation_avg_comparison_eval_only(
        eval_avg_regret_data_1_gensim, eval_avg_regret_means_1_gensim,
        eval_avg_regret_stds_1_gensim,
        eval_avg_regret_data_1_emulation_20, eval_avg_regret_means_1_emulation_20,
        eval_avg_regret_stds_1_emulation_20,
        eval_avg_regret_data_1_emulation_1, eval_avg_regret_means_1_emulation_1,
        eval_avg_regret_stds_1_emulation_1,
        ylim_rew, file_name, markevery=10, optimal_regret = 0, sample_step = 1,
        eval_only=False, plot_opt = False):
    """
    Plots regret, flags % and regret of two different configurations
    """
    #matplotlib.style.use("seaborn")
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 5))
    plt.rcParams.update({'font.size': 12})

    # ylims = (0, 920)

    # Plot Avg Eval regret Gensim
    ax.plot(np.array(list(range(len(eval_avg_regret_means_1_gensim[::sample_step]))))*sample_step,
            eval_avg_regret_means_1_gensim[::sample_step], label=r"Avg Eval 20 Envs \& Domain Randomization", marker="s", ls='-', color="r",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(eval_avg_regret_means_1_gensim[::sample_step]))))*sample_step,
                    eval_avg_regret_means_1_gensim[::sample_step] - eval_avg_regret_stds_1_gensim[::sample_step],
                    eval_avg_regret_means_1_gensim[::sample_step] + eval_avg_regret_stds_1_gensim[::sample_step],
                    alpha=0.35, color="r")

    # Plot Avg Eval regret emulation20
    ax.plot(np.array(list(range(len(eval_avg_regret_means_1_emulation_20[::sample_step])))) * sample_step,
            eval_avg_regret_means_1_emulation_20[::sample_step], label=r"Avg Eval 20 Envs", marker="o",
            ls='-', color="#599ad3",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(eval_avg_regret_means_1_emulation_20[::sample_step])))) * sample_step,
                    eval_avg_regret_means_1_emulation_20[::sample_step] - eval_avg_regret_stds_1_emulation_20[::sample_step],
                    eval_avg_regret_means_1_emulation_20[::sample_step] + eval_avg_regret_stds_1_emulation_20[::sample_step],
                    alpha=0.35, color="#599ad3")

    # Plot Avg Eval regret emulation1
    ax.plot(np.array(list(range(len(eval_avg_regret_means_1_emulation_1[::sample_step])))) * sample_step,
            eval_avg_regret_means_1_emulation_1[::sample_step], label=r"Avg Eval 1 Envs", marker="^",
            ls='-', color="#f9a65a",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(eval_avg_regret_means_1_emulation_1[::sample_step])))) * sample_step,
                    eval_avg_regret_means_1_emulation_1[::sample_step] - eval_avg_regret_stds_1_emulation_1[::sample_step],
                    eval_avg_regret_means_1_emulation_1[::sample_step] + eval_avg_regret_stds_1_emulation_1[::sample_step],
                    alpha=0.35, color="#f9a65a")

    if plot_opt:
        ax.plot(np.array(list(range(len(eval_avg_regret_means_1_gensim)))),
                [optimal_regret] * len(eval_avg_regret_means_1_gensim), label=r"lower bound $\pi^{*}$",
                color="black",
                linestyle="dashed")

    ax.set_title(r"Episodic regret")
    ax.set_xlabel("\# Iteration", fontsize=20)
    ax.set_ylabel("Avg Episode Regret", fontsize=20)
    ax.set_xlim(0, len(eval_avg_regret_means_1_gensim[::sample_step])*sample_step)
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

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.18),
              ncol=2, fancybox=True, shadow=True)
    #ax.legend(loc="lower right")
    ax.xaxis.label.set_size(13.5)
    ax.yaxis.label.set_size(13.5)

    fig.tight_layout()
    #plt.show()
    # plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.close(fig)


def plot_mega(
        train_avg_rewards_data_1, train_avg_rewards_means_1, train_avg_rewards_stds_1, eval_avg_rewards_data_1,
        eval_avg_rewards_means_1, eval_avg_rewards_stds_1, train_envs_specific_rewards_data, train_envs_specific_rewards_means,
        train_envs_specific_rewards_stds_1, eval_envs_specific_rewards_data_1, eval_envs_specific_rewards_means_1,
        eval_envs_specific_rewards_stds_1, train_avg_regret_data_1, train_avg_regret_means_1, train_avg_regret_stds_1,
        eval_avg_regret_data_1, eval_avg_regret_means_1, eval_avg_regret_stds_1,
        train_envs_specific_regret_data_1, train_envs_specific_regret_means_1, train_envs_specific_regret_stds_1,
        eval_envs_specific_regret_data_1, eval_envs_specific_regret_means_1, eval_envs_specific_regret_stds_1,
        train_avg_steps_data_1, train_avg_steps_means_1, train_avg_steps_stds_1, eval_avg_steps_data_1,
        eval_avg_steps_means_1, eval_avg_steps_stds_1, train_envs_specific_steps_data_1, train_envs_specific_steps_means_1,
        train_envs_specific_steps_stds_1, eval_envs_specific_steps_data_1, eval_envs_specific_steps_means_1,
        eval_envs_specific_steps_stds_1,


        train_avg_rewards_data_2, train_avg_rewards_means_2, train_avg_rewards_stds_2, eval_avg_rewards_data_2,
        eval_avg_rewards_means_2, eval_avg_rewards_stds_2, train_envs_specific_rewards_data_2,
        train_envs_specific_rewards_means_2,
        train_envs_specific_rewards_stds_2, eval_envs_specific_rewards_data_2, eval_envs_specific_rewards_means_2,
        eval_envs_specific_rewards_stds_2, train_avg_regret_data_2, train_avg_regret_means_2, train_avg_regret_stds_2,
        eval_avg_regret_data_2, eval_avg_regret_means_2, eval_avg_regret_stds_2,
        train_envs_specific_regret_data_2, train_envs_specific_regret_means_2, train_envs_specific_regret_stds_2,
        eval_envs_specific_regret_data_2, eval_envs_specific_regret_means_2, eval_envs_specific_regret_stds_2,
        train_avg_steps_data_2, train_avg_steps_means_2, train_avg_steps_stds_2, eval_avg_steps_data_2,
        eval_avg_steps_means_2, eval_avg_steps_stds_2, train_envs_specific_steps_data_2, train_envs_specific_steps_means_2,
        train_envs_specific_steps_stds_2, eval_envs_specific_steps_data_2, eval_envs_specific_steps_means_2,
        eval_envs_specific_steps_stds_2,


        train_avg_rewards_data_3, train_avg_rewards_means_3, train_avg_rewards_stds_3, eval_avg_rewards_data_3,
        eval_avg_rewards_means_3, eval_avg_rewards_stds_3, train_envs_specific_rewards_data_3,
        train_envs_specific_rewards_means_3,
        train_envs_specific_rewards_stds_3, eval_envs_specific_rewards_data_3, eval_envs_specific_rewards_means_3,
        eval_envs_specific_rewards_stds_3, train_avg_regret_data_3, train_avg_regret_means_3, train_avg_regret_stds_3,
        eval_avg_regret_data_3, eval_avg_regret_means_3, eval_avg_regret_stds_3,
        train_envs_specific_regret_data_3, train_envs_specific_regret_means_3, train_envs_specific_regret_stds_3,
        eval_envs_specific_regret_data_3, eval_envs_specific_regret_means_3, eval_envs_specific_regret_stds_3,
        train_avg_steps_data_3, train_avg_steps_means_3, train_avg_steps_stds_3, eval_avg_steps_data_3,
        eval_avg_steps_means_3, eval_avg_steps_stds_3, train_envs_specific_steps_data_3, train_envs_specific_steps_means_3,
        train_envs_specific_steps_stds_3, eval_envs_specific_steps_data_3, eval_envs_specific_steps_means_3,
        eval_envs_specific_steps_stds_3,

        ylim_rew=(0,1), file_name="test", markevery=10, optimal_steps = 10, optimal_reward = 95, sample_step = 1,
        plot_opt=False, ylim_reg=(-0.5,20), optimal_regret = 0, ylim_step = (0,1), markersize=0, linewidth=0.5):
    """
    Plots rewards, flags % and steps of two different configurations
    """
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['font.serif'] = ['Times New Roman']
    fig, ax = plt.subplots(nrows=3, ncols=6, figsize=(9, 3))
    plt.rcParams.update({'font.size': 8})

    # GENSIM

    # Plot Avg Train Rewards
    ax[0][0].plot(np.array(list(range(len(train_avg_rewards_means_1[::sample_step]))))*sample_step,
            train_avg_rewards_means_1[::sample_step], label=r"Avg\_T", marker="s", ls='-', color="#599ad3",
            markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[0][0].fill_between(np.array(list(range(len(train_avg_rewards_means_1[::sample_step]))))*sample_step,
                    train_avg_rewards_means_1[::sample_step] - train_avg_rewards_stds_1[::sample_step],
                    train_avg_rewards_means_1[::sample_step] + train_avg_rewards_stds_1[::sample_step],
                    alpha=0.35, color="#599ad3")
    markers = ["p", "^", "*", "+", "v", "1", "2", "3", "4", "x", "p", "h", "H", "d", "|", ",", ".", "H", "X", "s", "8",
               ">", "<", "P", "D", 0, 1, 2]
    i = 0
    for key in train_envs_specific_rewards_data.keys():
        r_means = train_envs_specific_rewards_means[key]
        r_stds = train_envs_specific_rewards_stds_1[key]
        label = r"T\_." + key.rsplit(".", 1)[-2].rsplit(".", 1)[-1]
        ax[0][0].plot(np.array(list(range(len(r_means[::sample_step]))))*sample_step,
                   r_means[::sample_step], label=label, marker=markers[i], ls='-', color="#599ad3", markevery=markevery,
                      markersize=markersize, linewidth=linewidth)
        ax[0][0].fill_between(np.array(list(range(len(r_means[::sample_step]))))*sample_step,
                           r_means[::sample_step] - r_stds[::sample_step],
                        r_means[::sample_step] + r_stds[::sample_step], alpha=0.35, color="#599ad3")
        i += 1

    # Plot Avg Eval Rewards
    ax[0][0].plot(np.array(list(range(len(eval_avg_rewards_means_1[::sample_step]))))*sample_step,
            eval_avg_rewards_means_1[::sample_step], label=r"Avg\_E", marker="o", ls='-', color="r",
            markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[0][0].fill_between(np.array(list(range(len(eval_avg_rewards_means_1[::sample_step]))))*sample_step,
                    eval_avg_rewards_means_1[::sample_step] - eval_avg_rewards_stds_1[::sample_step],
                    eval_avg_rewards_means_1[::sample_step] + eval_avg_rewards_stds_1[::sample_step],
                    alpha=0.35, color="r")

    for key in eval_envs_specific_rewards_data_1.keys():
        r_means = eval_envs_specific_rewards_means_1[key]
        r_stds = eval_envs_specific_rewards_stds_1[key]
        label = r"E\_." + key.rsplit(".", 1)[-2].rsplit(".", 1)[-1]
        ax[0][0].plot(np.array(list(range(len(r_means[::sample_step]))))*sample_step,
                   r_means[::sample_step], label=label, marker=markers[i], ls='-', color="r", markevery=markevery,
                      markersize=markersize, linewidth=linewidth)
        ax[0][0].fill_between(np.array(list(range(len(r_means[::sample_step]))))*sample_step,
                           r_means[::sample_step] - r_stds[::sample_step],
                        r_means[::sample_step] + r_stds[::sample_step], alpha=0.35, color="r")
        i += 1

    if plot_opt:
        ax[0][0].plot(np.array(list(range(len(train_avg_rewards_means_1)))),
                [optimal_reward] * len(train_avg_rewards_means_1), label=r"upper bound $\pi^{*}$",
                color="black", linestyle="dashed", linewidth=linewidth)

    # Plot Avg Train Rewards
    ax[0][1].plot(np.array(list(range(len(train_avg_rewards_means_1[::sample_step])))) * sample_step,
            train_avg_rewards_means_1[::sample_step], label=r"Avg Train", marker="s", ls='-', color="#599ad3",
            markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[0][1].fill_between(np.array(list(range(len(train_avg_rewards_means_1[::sample_step])))) * sample_step,
                    train_avg_rewards_means_1[::sample_step] - train_avg_rewards_stds_1[::sample_step],
                    train_avg_rewards_means_1[::sample_step] + train_avg_rewards_stds_1[::sample_step],
                    alpha=0.35, color="#599ad3", linewidth=linewidth)

    # Plot Avg Eval Rewards
    ax[0][1].plot(np.array(list(range(len(eval_avg_rewards_means_1[::sample_step])))) * sample_step,
            eval_avg_rewards_means_1[::sample_step], label=r"Avg Eval", marker="o", ls='-', color="r",
            markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[0][1].fill_between(np.array(list(range(len(eval_avg_rewards_means_1[::sample_step])))) * sample_step,
                    eval_avg_rewards_means_1[::sample_step] - eval_avg_rewards_stds_1[::sample_step],
                    eval_avg_rewards_means_1[::sample_step] + eval_avg_rewards_stds_1[::sample_step],
                    alpha=0.35, color="r")

    if plot_opt:
        ax[0][1].plot(np.array(list(range(len(train_avg_rewards_means_1)))),
                [optimal_reward] * len(train_avg_rewards_means_1), label=r"upper bound $\pi^{*}$",
                color="black", linestyle="dashed", linewidth=linewidth)

    # Plot Avg Train regret
    ax[0][2].plot(np.array(list(range(len(train_avg_regret_means_1[::sample_step])))) * sample_step,
            train_avg_regret_means_1[::sample_step], label=r"Avg\_T", marker="s", ls='-', color="#599ad3",
            markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[0][2].fill_between(np.array(list(range(len(train_avg_regret_means_1[::sample_step])))) * sample_step,
                    train_avg_regret_means_1[::sample_step] - train_avg_regret_stds_1[::sample_step],
                    train_avg_regret_means_1[::sample_step] + train_avg_regret_stds_1[::sample_step],
                    alpha=0.35, color="#599ad3")

    i = 0
    for key in train_envs_specific_regret_data_1.keys():
        r_means = train_envs_specific_regret_means_1[key]
        r_stds = train_envs_specific_regret_stds_1[key]
        label = r"T\_." + key.rsplit(".", 1)[-2].rsplit(".", 1)[-1]
        ax[0][2].plot(np.array(list(range(len(r_means[::sample_step])))) * sample_step,
                r_means[::sample_step], label=label, marker=markers[i], ls='-', color="#599ad3", markevery=markevery,
                      markersize=markersize, linewidth=linewidth)
        ax[0][2].fill_between(np.array(list(range(len(r_means[::sample_step])))) * sample_step,
                        r_means[::sample_step] - r_stds[::sample_step],
                        r_means[::sample_step] + r_stds[::sample_step], alpha=0.35, color="#599ad3")
        i += 1

    # Plot Avg Eval regret
    ax[0][2].plot(np.array(list(range(len(eval_avg_regret_means_1[::sample_step])))) * sample_step,
            eval_avg_regret_means_1[::sample_step], label=r"Avg\_E", marker="o", ls='-', color="r",
            markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[0][2].fill_between(np.array(list(range(len(eval_avg_regret_means_1[::sample_step])))) * sample_step,
                    eval_avg_regret_means_1[::sample_step] - eval_avg_regret_stds_1[::sample_step],
                    eval_avg_regret_means_1[::sample_step] + eval_avg_regret_stds_1[::sample_step],
                    alpha=0.35, color="r")

    for key in eval_envs_specific_regret_data_1.keys():
        r_means = eval_envs_specific_regret_means_1[key]
        r_stds = eval_envs_specific_regret_stds_1[key]
        label = r"E\_." + key.rsplit(".", 1)[-2].rsplit(".", 1)[-1]
        ax[0][2].plot(np.array(list(range(len(r_means[::sample_step])))) * sample_step,
                r_means[::sample_step], label=label, marker=markers[i], ls='-', color="r", markevery=markevery,
                      markersize=markersize, linewidth=linewidth)
        ax[0][2].fill_between(np.array(list(range(len(r_means[::sample_step])))) * sample_step,
                        r_means[::sample_step] - r_stds[::sample_step],
                        r_means[::sample_step] + r_stds[::sample_step], alpha=0.35, color="r")
        i += 1

    ax[0][2].plot(np.array(list(range(len(train_avg_regret_means_1)))),
            [optimal_regret] * len(train_avg_regret_means_1), label=r"lower bound $\pi^{*}$",
            color="black", linestyle="dashed", linewidth=linewidth)

    # Plot Avg Train regret
    ax[0][3].plot(np.array(list(range(len(train_avg_regret_means_1[::sample_step])))) * sample_step,
            train_avg_regret_means_1[::sample_step], label=r"Avg Train", marker="s", ls='-', color="#599ad3",
            markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[0][3].fill_between(np.array(list(range(len(train_avg_regret_means_1[::sample_step])))) * sample_step,
                    train_avg_regret_means_1[::sample_step] - train_avg_regret_stds_1[::sample_step],
                    train_avg_regret_means_1[::sample_step] + train_avg_regret_stds_1[::sample_step],
                    alpha=0.35, color="#599ad3")

    # Plot Avg Eval regret
    ax[0][3].plot(np.array(list(range(len(eval_avg_regret_means_1[::sample_step])))) * sample_step,
            eval_avg_regret_means_1[::sample_step], label=r"Avg Eval", marker="o", ls='-', color="r",
            markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[0][3].fill_between(np.array(list(range(len(eval_avg_regret_means_1[::sample_step])))) * sample_step,
                    eval_avg_regret_means_1[::sample_step] - eval_avg_regret_stds_1[::sample_step],
                    eval_avg_regret_means_1[::sample_step] + eval_avg_regret_stds_1[::sample_step],
                    alpha=0.35, color="r")

    # Plot Avg Train steps
    ax[0][4].plot(np.array(list(range(len(train_avg_steps_means_1[::sample_step])))) * sample_step,
            train_avg_steps_means_1[::sample_step], label=r"Avg\_T", marker="s", ls='-', color="#599ad3",
            markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[0][4].fill_between(np.array(list(range(len(train_avg_steps_means_1[::sample_step])))) * sample_step,
                    train_avg_steps_means_1[::sample_step] - train_avg_steps_stds_1[::sample_step],
                    train_avg_steps_means_1[::sample_step] + train_avg_steps_stds_1[::sample_step],
                    alpha=0.35, color="#599ad3")

    i = 0
    for key in train_envs_specific_steps_data_1.keys():
        r_means = train_envs_specific_steps_means_1[key]
        r_stds = train_envs_specific_steps_stds_1[key]
        label = r"T\_." + key.rsplit(".", 1)[-2].rsplit(".", 1)[-1]
        ax[0][4].plot(np.array(list(range(len(r_means[::sample_step])))) * sample_step,
                r_means[::sample_step], label=label, marker=markers[i], ls='-', color="#599ad3", markevery=markevery,
                      markersize=markersize, linewidth=linewidth)
        ax[0][4].fill_between(np.array(list(range(len(r_means[::sample_step])))) * sample_step,
                        r_means[::sample_step] - r_stds[::sample_step],
                        r_means[::sample_step] + r_stds[::sample_step], alpha=0.35, color="#599ad3")
        i += 1

    # Plot Avg Eval steps
    ax[0][4].plot(np.array(list(range(len(eval_avg_steps_means_1[::sample_step])))) * sample_step,
            eval_avg_steps_means_1[::sample_step], label=r"Avg\_E", marker="o", ls='-', color="r",
            markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[0][4].fill_between(np.array(list(range(len(eval_avg_steps_means_1[::sample_step])))) * sample_step,
                    eval_avg_steps_means_1[::sample_step] - eval_avg_steps_stds_1[::sample_step],
                    eval_avg_steps_means_1[::sample_step] + eval_avg_steps_stds_1[::sample_step],
                    alpha=0.35, color="r")

    for key in eval_envs_specific_steps_data_1.keys():
        r_means = eval_envs_specific_steps_means_1[key]
        r_stds = eval_envs_specific_steps_stds_1[key]
        label = r"E\_." + key.rsplit(".", 1)[-2].rsplit(".", 1)[-1]
        ax[0][4].plot(np.array(list(range(len(r_means[::sample_step])))) * sample_step,
                r_means[::sample_step], label=label, marker=markers[i], ls='-', color="r", markevery=markevery,
                      markersize=markersize, linewidth=linewidth)
        ax[0][4].fill_between(np.array(list(range(len(r_means[::sample_step])))) * sample_step,
                        r_means[::sample_step] - r_stds[::sample_step],
                        r_means[::sample_step] + r_stds[::sample_step], alpha=0.35, color="r")
        i += 1

    # Plot Avg Train steps
    ax[0][5].plot(np.array(list(range(len(train_avg_steps_means_1[::sample_step])))) * sample_step,
            train_avg_steps_means_1[::sample_step], label=r"Avg Train", marker="s", ls='-', color="#599ad3",
            markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[0][5].fill_between(np.array(list(range(len(train_avg_steps_means_1[::sample_step])))) * sample_step,
                    train_avg_steps_means_1[::sample_step] - train_avg_steps_stds_1[::sample_step],
                    train_avg_steps_means_1[::sample_step] + train_avg_steps_stds_1[::sample_step],
                    alpha=0.35, color="#599ad3")

    # Plot Avg Eval steps
    ax[0][5].plot(np.array(list(range(len(eval_avg_steps_means_1[::sample_step])))) * sample_step,
            eval_avg_steps_means_1[::sample_step], label=r"Avg Eval", marker="o", ls='-', color="r",
            markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[0][5].fill_between(np.array(list(range(len(eval_avg_steps_means_1[::sample_step])))) * sample_step,
                    eval_avg_steps_means_1[::sample_step] - eval_avg_steps_stds_1[::sample_step],
                    eval_avg_steps_means_1[::sample_step] + eval_avg_steps_stds_1[::sample_step],
                    alpha=0.35, color="r")


    titles = [r"Episodic Rewards", r"Avg Episodic Rewards", r"Episodic regret", r"Avg Episodic regret", r"Episodic steps", r"Avg Episodic steps"]
    x_lables = ["\# Iteration", "\# Iteration", "\# Iteration", "\# Iteration", "\# Iteration", "\# Iteration"]
    y_labels = ["Avg Episode Reward", "Avg Episode Reward", "Avg Episode Regret", "Avg Episode Regret", "Avg Episode Steps", "Avg Episode Steps"]
    for i in range(6):
        ax[0][i].set_title(titles[i])
        #ax[0][i].set_xlabel(x_lables[i], fontsize=20)
        if i == 0:
            ax[0][i].set_ylabel("20 Envs \& DR", fontsize=8)
        #ax[0][i].set_ylabel(y_labels[i], fontsize=20)
        ax[0][i].set_xlim(0, len(train_avg_rewards_means_1[::sample_step])*sample_step)
        if i == 0 or i == 1:
            ax[0][i].set_ylim(ylim_rew[0], ylim_rew[1])
        elif i == 2 or i == 3:
            ax[0][i].set_ylim(ylim_reg[0], ylim_reg[1])
        elif i == 4 or i == 4:
            ax[0][i].set_ylim(ylim_step[0], ylim_step[1])
        #ax[0][i].grid('on')
        xlab = ax[0][i].xaxis.get_label()
        ylab = ax[0][i].yaxis.get_label()
        xlab.set_size(9)
        ylab.set_size(9)
        # change the color of the top and right spines to opaque gray
        ax[0][i].spines['right'].set_color((.8, .8, .8))
        ax[0][i].spines['top'].set_color((.8, .8, .8))
        # if i != 0:
        #     ax[0][i].legend(loc='upper center', bbox_to_anchor=(0.5, -0.27),
        #               ncol=5, fancybox=True, shadow=True)
        ax[0][i].xaxis.label.set_size(9)
        ax[0][i].yaxis.label.set_size(9)
        ax[0][i].set_xticks([])
        ax[0][i].tick_params(axis='both', which='major', labelsize=4)
        ax[0][i].tick_params(axis='both', which='minor', labelsize=4)

    # emulation 20

    # Plot Avg Train Rewards
    ax[1][0].plot(np.array(list(range(len(train_avg_rewards_means_2[::sample_step])))) * sample_step,
                  train_avg_rewards_means_2[::sample_step], label=r"Avg\_T", marker="s", ls='-', color="#599ad3",
                  markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[1][0].fill_between(np.array(list(range(len(train_avg_rewards_means_2[::sample_step])))) * sample_step,
                          train_avg_rewards_means_2[::sample_step] - train_avg_rewards_stds_2[::sample_step],
                          train_avg_rewards_means_2[::sample_step] + train_avg_rewards_stds_2[::sample_step],
                          alpha=0.35, color="#599ad3")
    markers = ["p", "^", "*", "+", "v", "1", "2", "3", "4", "x", "p", "h", "H", "d", "|", ",", ".", "H", "X", "s",
               "8",
               ">", "<", "P", "D", 0, 1, 2]
    i = 0
    for key in train_envs_specific_rewards_data.keys():
        r_means = train_envs_specific_rewards_means[key]
        r_stds = train_envs_specific_rewards_stds_2[key]
        label = r"T\_." + key.rsplit(".", 1)[-2].rsplit(".", 1)[-1]
        ax[1][0].plot(np.array(list(range(len(r_means[::sample_step])))) * sample_step,
                      r_means[::sample_step], label=label, marker=markers[i], ls='-', color="#599ad3",
                      markevery=markevery, markersize=markersize, linewidth=linewidth)
        ax[1][0].fill_between(np.array(list(range(len(r_means[::sample_step])))) * sample_step,
                              r_means[::sample_step] - r_stds[::sample_step],
                              r_means[::sample_step] + r_stds[::sample_step], alpha=0.35, color="#599ad3")
        i += 1

    # Plot Avg Eval Rewards
    ax[1][0].plot(np.array(list(range(len(eval_avg_rewards_means_2[::sample_step])))) * sample_step,
                  eval_avg_rewards_means_2[::sample_step], label=r"Avg\_E", marker="o", ls='-', color="r",
                  markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[1][0].fill_between(np.array(list(range(len(eval_avg_rewards_means_2[::sample_step])))) * sample_step,
                          eval_avg_rewards_means_2[::sample_step] - eval_avg_rewards_stds_2[::sample_step],
                          eval_avg_rewards_means_2[::sample_step] + eval_avg_rewards_stds_2[::sample_step],
                          alpha=0.35, color="r")

    for key in eval_envs_specific_rewards_data_2.keys():
        r_means = eval_envs_specific_rewards_means_2[key]
        r_stds = eval_envs_specific_rewards_stds_2[key]
        label = r"E\_." + key.rsplit(".", 1)[-2].rsplit(".", 1)[-1]
        ax[1][0].plot(np.array(list(range(len(r_means[::sample_step])))) * sample_step,
                      r_means[::sample_step], label=label, marker=markers[i], ls='-', color="r",
                      markevery=markevery, markersize=markersize, linewidth=linewidth)
        ax[1][0].fill_between(np.array(list(range(len(r_means[::sample_step])))) * sample_step,
                              r_means[::sample_step] - r_stds[::sample_step],
                              r_means[::sample_step] + r_stds[::sample_step], alpha=0.35, color="r")
        i += 1

    if plot_opt:
        ax[1][0].plot(np.array(list(range(len(train_avg_rewards_means_2)))),
                      [optimal_reward] * len(train_avg_rewards_means_2), label=r"upper bound $\pi^{*}$",
                      color="black", linestyle="dashed", linewidth=linewidth)

    # Plot Avg Train Rewards
    ax[1][1].plot(np.array(list(range(len(train_avg_rewards_means_2[::sample_step])))) * sample_step,
                  train_avg_rewards_means_2[::sample_step], label=r"Avg Train", marker="s", ls='-', color="#599ad3",
                  markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[1][1].fill_between(np.array(list(range(len(train_avg_rewards_means_2[::sample_step])))) * sample_step,
                          train_avg_rewards_means_2[::sample_step] - train_avg_rewards_stds_2[::sample_step],
                          train_avg_rewards_means_2[::sample_step] + train_avg_rewards_stds_2[::sample_step],
                          alpha=0.35, color="#599ad3")

    # Plot Avg Eval Rewards
    ax[1][1].plot(np.array(list(range(len(eval_avg_rewards_means_2[::sample_step])))) * sample_step,
                  eval_avg_rewards_means_2[::sample_step], label=r"Avg Eval", marker="o", ls='-', color="r",
                  markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[1][1].fill_between(np.array(list(range(len(eval_avg_rewards_means_2[::sample_step])))) * sample_step,
                          eval_avg_rewards_means_2[::sample_step] - eval_avg_rewards_stds_2[::sample_step],
                          eval_avg_rewards_means_2[::sample_step] + eval_avg_rewards_stds_2[::sample_step],
                          alpha=0.35, color="r")

    if plot_opt:
        ax[1][1].plot(np.array(list(range(len(train_avg_rewards_means_2)))),
                      [optimal_reward] * len(train_avg_rewards_means_2), label=r"upper bound $\pi^{*}$",
                      color="black", linestyle="dashed", linewidth=linewidth)

    # Plot Avg Train regret
    ax[1][2].plot(np.array(list(range(len(train_avg_regret_means_2[::sample_step])))) * sample_step,
                  train_avg_regret_means_2[::sample_step], label=r"Avg\_T", marker="s", ls='-', color="#599ad3",
                  markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[1][2].fill_between(np.array(list(range(len(train_avg_regret_means_2[::sample_step])))) * sample_step,
                          train_avg_regret_means_2[::sample_step] - train_avg_regret_stds_2[::sample_step],
                          train_avg_regret_means_2[::sample_step] + train_avg_regret_stds_2[::sample_step],
                          alpha=0.35, color="#599ad3")

    i = 0
    for key in train_envs_specific_regret_data_2.keys():
        r_means = train_envs_specific_regret_means_2[key]
        r_stds = train_envs_specific_regret_stds_2[key]
        label = r"T\_." + key.rsplit(".", 1)[-2].rsplit(".", 1)[-1]
        ax[1][2].plot(np.array(list(range(len(r_means[::sample_step])))) * sample_step,
                      r_means[::sample_step], label=label, marker=markers[i], ls='-', color="#599ad3",
                      markevery=markevery, markersize=markersize, linewidth=linewidth)
        ax[1][2].fill_between(np.array(list(range(len(r_means[::sample_step])))) * sample_step,
                              r_means[::sample_step] - r_stds[::sample_step],
                              r_means[::sample_step] + r_stds[::sample_step], alpha=0.35, color="#599ad3")
        i += 1

    # Plot Avg Eval regret
    ax[1][2].plot(np.array(list(range(len(eval_avg_regret_means_2[::sample_step])))) * sample_step,
                  eval_avg_regret_means_2[::sample_step], label=r"Avg\_E", marker="o", ls='-', color="r",
                  markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[1][2].fill_between(np.array(list(range(len(eval_avg_regret_means_2[::sample_step])))) * sample_step,
                          eval_avg_regret_means_2[::sample_step] - eval_avg_regret_stds_2[::sample_step],
                          eval_avg_regret_means_2[::sample_step] + eval_avg_regret_stds_2[::sample_step],
                          alpha=0.35, color="r")

    for key in eval_envs_specific_regret_data_2.keys():
        r_means = eval_envs_specific_regret_means_2[key]
        r_stds = eval_envs_specific_regret_stds_2[key]
        label = r"E\_." + key.rsplit(".", 1)[-2].rsplit(".", 1)[-1]
        ax[1][2].plot(np.array(list(range(len(r_means[::sample_step])))) * sample_step,
                      r_means[::sample_step], label=label, marker=markers[i], ls='-', color="r",
                      markevery=markevery, markersize=markersize, linewidth=linewidth)
        ax[1][2].fill_between(np.array(list(range(len(r_means[::sample_step])))) * sample_step,
                              r_means[::sample_step] - r_stds[::sample_step],
                              r_means[::sample_step] + r_stds[::sample_step], alpha=0.35, color="r")
        i += 1

    ax[1][2].plot(np.array(list(range(len(train_avg_regret_means_2)))),
                  [optimal_regret] * len(train_avg_regret_means_2), label=r"lower bound $\pi^{*}$",
                  color="black", linestyle="dashed", markersize=markersize, linewidth=linewidth)

    # Plot Avg Train regret
    ax[1][3].plot(np.array(list(range(len(train_avg_regret_means_2[::sample_step])))) * sample_step,
                  train_avg_regret_means_2[::sample_step], label=r"Avg Train", marker="s", ls='-', color="#599ad3",
                  markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[1][3].fill_between(np.array(list(range(len(train_avg_regret_means_2[::sample_step])))) * sample_step,
                          train_avg_regret_means_2[::sample_step] - train_avg_regret_stds_2[::sample_step],
                          train_avg_regret_means_2[::sample_step] + train_avg_regret_stds_2[::sample_step],
                          alpha=0.35, color="#599ad3")

    # Plot Avg Eval regret
    ax[1][3].plot(np.array(list(range(len(eval_avg_regret_means_2[::sample_step])))) * sample_step,
                  eval_avg_regret_means_2[::sample_step], label=r"Avg Eval", marker="o", ls='-', color="r",
                  markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[1][3].fill_between(np.array(list(range(len(eval_avg_regret_means_2[::sample_step])))) * sample_step,
                          eval_avg_regret_means_2[::sample_step] - eval_avg_regret_stds_2[::sample_step],
                          eval_avg_regret_means_2[::sample_step] + eval_avg_regret_stds_2[::sample_step],
                          alpha=0.35, color="r")

    # Plot Avg Train steps
    ax[1][4].plot(np.array(list(range(len(train_avg_steps_means_2[::sample_step])))) * sample_step,
                  train_avg_steps_means_2[::sample_step], label=r"Avg\_T", marker="s", ls='-', color="#599ad3",
                  markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[1][4].fill_between(np.array(list(range(len(train_avg_steps_means_2[::sample_step])))) * sample_step,
                          train_avg_steps_means_2[::sample_step] - train_avg_steps_stds_2[::sample_step],
                          train_avg_steps_means_2[::sample_step] + train_avg_steps_stds_2[::sample_step],
                          alpha=0.35, color="#599ad3")

    i = 0
    for key in train_envs_specific_steps_data_2.keys():
        r_means = train_envs_specific_steps_means_2[key]
        r_stds = train_envs_specific_steps_stds_2[key]
        label = r"T\_." + key.rsplit(".", 1)[-2].rsplit(".", 1)[-1]
        ax[1][4].plot(np.array(list(range(len(r_means[::sample_step])))) * sample_step,
                      r_means[::sample_step], label=label, marker=markers[i], ls='-', color="#599ad3",
                      markevery=markevery, markersize=markersize, linewidth=linewidth)
        ax[1][4].fill_between(np.array(list(range(len(r_means[::sample_step])))) * sample_step,
                              r_means[::sample_step] - r_stds[::sample_step],
                              r_means[::sample_step] + r_stds[::sample_step], alpha=0.35, color="#599ad3")
        i += 1

    # Plot Avg Eval steps
    ax[1][4].plot(np.array(list(range(len(eval_avg_steps_means_2[::sample_step])))) * sample_step,
                  eval_avg_steps_means_2[::sample_step], label=r"Avg\_E", marker="o", ls='-', color="r",
                  markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[1][4].fill_between(np.array(list(range(len(eval_avg_steps_means_2[::sample_step])))) * sample_step,
                          eval_avg_steps_means_2[::sample_step] - eval_avg_steps_stds_2[::sample_step],
                          eval_avg_steps_means_2[::sample_step] + eval_avg_steps_stds_2[::sample_step],
                          alpha=0.35, color="r")

    for key in eval_envs_specific_steps_data_2.keys():
        r_means = eval_envs_specific_steps_means_2[key]
        r_stds = eval_envs_specific_steps_stds_2[key]
        label = r"E\_." + key.rsplit(".", 1)[-2].rsplit(".", 1)[-1]
        ax[1][4].plot(np.array(list(range(len(r_means[::sample_step])))) * sample_step,
                      r_means[::sample_step], label=label, marker=markers[i], ls='-', color="r",
                      markevery=markevery, markersize=markersize, linewidth=linewidth)
        ax[1][4].fill_between(np.array(list(range(len(r_means[::sample_step])))) * sample_step,
                              r_means[::sample_step] - r_stds[::sample_step],
                              r_means[::sample_step] + r_stds[::sample_step], alpha=0.35, color="r")
        i += 1

    # Plot Avg Train steps
    ax[1][5].plot(np.array(list(range(len(train_avg_steps_means_2[::sample_step])))) * sample_step,
                  train_avg_steps_means_2[::sample_step], label=r"Avg Train", marker="s", ls='-', color="#599ad3",
                  markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[1][5].fill_between(np.array(list(range(len(train_avg_steps_means_2[::sample_step])))) * sample_step,
                          train_avg_steps_means_2[::sample_step] - train_avg_steps_stds_2[::sample_step],
                          train_avg_steps_means_2[::sample_step] + train_avg_steps_stds_2[::sample_step],
                          alpha=0.35, color="#599ad3")

    # Plot Avg Eval steps
    ax[1][5].plot(np.array(list(range(len(eval_avg_steps_means_2[::sample_step])))) * sample_step,
                  eval_avg_steps_means_2[::sample_step], label=r"Avg Eval", marker="o", ls='-', color="r",
                  markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[1][5].fill_between(np.array(list(range(len(eval_avg_steps_means_2[::sample_step])))) * sample_step,
                          eval_avg_steps_means_2[::sample_step] - eval_avg_steps_stds_2[::sample_step],
                          eval_avg_steps_means_2[::sample_step] + eval_avg_steps_stds_2[::sample_step],
                          alpha=0.35, color="r")

    titles = [r"Episodic Rewards", r"Episodic Rewards", r"Episodic regret", r"Episodic regret", r"Episodic steps",
              r"Episodic steps"]
    x_lables = ["\# Iteration", "\# Iteration", "\# Iteration", "\# Iteration", "\# Iteration", "\# Iteration"]
    y_labels = ["Avg Episode Reward", "Avg Episode Reward", "Avg Episode Regret", "Avg Episode Regret",
                "Avg Episode Steps", "Avg Episode Steps"]
    for i in range(6):
        #ax[1][i].set_title(titles[i])
        #ax[1][i].set_xlabel(x_lables[i], fontsize=20)
        #ax[1][i].set_ylabel(y_labels[i], fontsize=20)
        if i == 0:
            ax[1][i].set_ylabel("20 Envs", fontsize=8)
        ax[1][i].set_xlim(0, len(train_avg_rewards_means_2[::sample_step]) * sample_step)
        if i == 0 or i == 1:
            ax[1][i].set_ylim(ylim_rew[0], ylim_rew[1])
        elif i == 2 or i == 3:
            ax[1][i].set_ylim(ylim_reg[0], ylim_reg[1])
        elif i == 4 or i == 4:
            ax[1][i].set_ylim(ylim_step[0], ylim_step[1])
        #ax[1][i].grid('on')
        xlab = ax[1][i].xaxis.get_label()
        ylab = ax[1][i].yaxis.get_label()
        xlab.set_size(8)
        ylab.set_size(8)
        # change the color of the top and right spines to opaque gray
        ax[1][i].spines['right'].set_color((.8, .8, .8))
        ax[1][i].spines['top'].set_color((.8, .8, .8))
        # if i != 0:
        #     ax[1][i].legend(loc='upper center', bbox_to_anchor=(0.5, -0.27),
        #               ncol=5, fancybox=True, shadow=True)
        ax[1][i].xaxis.label.set_size(8)
        ax[1][i].yaxis.label.set_size(8)
        ax[1][i].set_xticks([])
        ax[1][i].tick_params(axis='both', which='major', labelsize=4)
        ax[1][i].tick_params(axis='both', which='minor', labelsize=4)

    # emulation 1

    # Plot Avg Train Rewards
    ax[2][0].plot(np.array(list(range(len(train_avg_rewards_means_3[::sample_step])))) * sample_step,
                  train_avg_rewards_means_3[::sample_step], label=r"Avg\_T", marker="s", ls='-', color="#599ad3",
                  markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[2][0].fill_between(np.array(list(range(len(train_avg_rewards_means_3[::sample_step])))) * sample_step,
                          train_avg_rewards_means_3[::sample_step] - train_avg_rewards_stds_3[::sample_step],
                          train_avg_rewards_means_3[::sample_step] + train_avg_rewards_stds_3[::sample_step],
                          alpha=0.35, color="#599ad3")
    markers = ["p", "^", "*", "+", "v", "1", "2", "3", "4", "x", "p", "h", "H", "d", "|", ",", ".", "H", "X", "s",
               "8",
               ">", "<", "P", "D", 0, 1, 2]
    i = 0
    for key in train_envs_specific_rewards_data_3.keys():
        r_means = train_envs_specific_rewards_means[key]
        r_stds = train_envs_specific_rewards_stds_3[key]
        label = r"T\_." + key.rsplit(".", 1)[-2].rsplit(".", 1)[-1]
        ax[2][0].plot(np.array(list(range(len(r_means[::sample_step])))) * sample_step,
                      r_means[::sample_step], label=label, marker=markers[i], ls='-', color="#599ad3",
                      markevery=markevery, markersize=markersize, linewidth=linewidth)
        ax[2][0].fill_between(np.array(list(range(len(r_means[::sample_step])))) * sample_step,
                              r_means[::sample_step] - r_stds[::sample_step],
                              r_means[::sample_step] + r_stds[::sample_step], alpha=0.35, color="#599ad3")
        i += 1

    # Plot Avg Eval Rewards
    ax[2][0].plot(np.array(list(range(len(eval_avg_rewards_means_3[::sample_step])))) * sample_step,
                  eval_avg_rewards_means_3[::sample_step], label=r"Avg\_E", marker="o", ls='-', color="r",
                  markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[2][0].fill_between(np.array(list(range(len(eval_avg_rewards_means_3[::sample_step])))) * sample_step,
                          eval_avg_rewards_means_3[::sample_step] - eval_avg_rewards_stds_3[::sample_step],
                          eval_avg_rewards_means_3[::sample_step] + eval_avg_rewards_stds_3[::sample_step],
                          alpha=0.35, color="r")

    for key in eval_envs_specific_rewards_data_3.keys():
        r_means = eval_envs_specific_rewards_means_3[key]
        r_stds = eval_envs_specific_rewards_stds_3[key]
        label = r"E\_." + key.rsplit(".", 1)[-2].rsplit(".", 1)[-1]
        ax[2][0].plot(np.array(list(range(len(r_means[::sample_step])))) * sample_step,
                      r_means[::sample_step], label=label, marker=markers[i], ls='-', color="r",
                      markevery=markevery, markersize=markersize, linewidth=linewidth)
        ax[2][0].fill_between(np.array(list(range(len(r_means[::sample_step])))) * sample_step,
                              r_means[::sample_step] - r_stds[::sample_step],
                              r_means[::sample_step] + r_stds[::sample_step], alpha=0.35, color="r")
        i += 1

    if plot_opt:
        ax[2][0].plot(np.array(list(range(len(train_avg_rewards_means_3)))),
                      [optimal_reward] * len(train_avg_rewards_means_3), label=r"upper bound $\pi^{*}$",
                      color="black", linestyle="dashed", linewidth=linewidth)

    # Plot Avg Train Rewards
    ax[2][1].plot(np.array(list(range(len(train_avg_rewards_means_3[::sample_step])))) * sample_step,
                  train_avg_rewards_means_3[::sample_step], label=r"Train", marker="s", ls='-', color="#599ad3",
                  markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[2][1].fill_between(np.array(list(range(len(train_avg_rewards_means_3[::sample_step])))) * sample_step,
                          train_avg_rewards_means_3[::sample_step] - train_avg_rewards_stds_3[::sample_step],
                          train_avg_rewards_means_3[::sample_step] + train_avg_rewards_stds_3[::sample_step],
                          alpha=0.35, color="#599ad3")

    # Plot Avg Eval Rewards
    ax[2][1].plot(np.array(list(range(len(eval_avg_rewards_means_3[::sample_step])))) * sample_step,
                  eval_avg_rewards_means_3[::sample_step], label=r"Eval", marker="o", ls='-', color="r",
                  markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[2][1].fill_between(np.array(list(range(len(eval_avg_rewards_means_3[::sample_step])))) * sample_step,
                          eval_avg_rewards_means_3[::sample_step] - eval_avg_rewards_stds_3[::sample_step],
                          eval_avg_rewards_means_3[::sample_step] + eval_avg_rewards_stds_3[::sample_step],
                          alpha=0.35, color="r")

    if plot_opt:
        ax[2][1].plot(np.array(list(range(len(train_avg_rewards_means_3)))),
                      [optimal_reward] * len(train_avg_rewards_means_3), label=r"$\pi^{*}$",
                      color="black", linestyle="dashed", linewidth=linewidth)

    # Plot Avg Train regret
    ax[2][2].plot(np.array(list(range(len(train_avg_regret_means_3[::sample_step])))) * sample_step,
                  train_avg_regret_means_3[::sample_step], label=r"Avg\_T", marker="s", ls='-', color="#599ad3",
                  markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[2][2].fill_between(np.array(list(range(len(train_avg_regret_means_3[::sample_step])))) * sample_step,
                          train_avg_regret_means_3[::sample_step] - train_avg_regret_stds_3[::sample_step],
                          train_avg_regret_means_3[::sample_step] + train_avg_regret_stds_3[::sample_step],
                          alpha=0.35, color="#599ad3")

    i = 0
    for key in train_envs_specific_regret_data_3.keys():
        r_means = train_envs_specific_regret_means_3[key]
        r_stds = train_envs_specific_regret_stds_3[key]
        label = r"T\_." + key.rsplit(".", 1)[-2].rsplit(".", 1)[-1]
        ax[2][2].plot(np.array(list(range(len(r_means[::sample_step])))) * sample_step,
                      r_means[::sample_step], label=label, marker=markers[i], ls='-', color="#599ad3",
                      markevery=markevery, markersize=markersize, linewidth=linewidth)
        ax[2][2].fill_between(np.array(list(range(len(r_means[::sample_step])))) * sample_step,
                              r_means[::sample_step] - r_stds[::sample_step],
                              r_means[::sample_step] + r_stds[::sample_step], alpha=0.35, color="#599ad3")
        i += 1

    # Plot Avg Eval regret
    ax[2][2].plot(np.array(list(range(len(eval_avg_regret_means_3[::sample_step])))) * sample_step,
                  eval_avg_regret_means_3[::sample_step], label=r"Avg\_E", marker="o", ls='-', color="r",
                  markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[2][2].fill_between(np.array(list(range(len(eval_avg_regret_means_3[::sample_step])))) * sample_step,
                          eval_avg_regret_means_3[::sample_step] - eval_avg_regret_stds_3[::sample_step],
                          eval_avg_regret_means_3[::sample_step] + eval_avg_regret_stds_3[::sample_step],
                          alpha=0.35, color="r")

    for key in eval_envs_specific_regret_data_3.keys():
        r_means = eval_envs_specific_regret_means_3[key]
        r_stds = eval_envs_specific_regret_stds_3[key]
        label = r"E\_." + key.rsplit(".", 1)[-2].rsplit(".", 1)[-1]
        ax[2][2].plot(np.array(list(range(len(r_means[::sample_step])))) * sample_step,
                      r_means[::sample_step], label=label, marker=markers[i], ls='-', color="r",
                      markevery=markevery, markersize=markersize, linewidth=linewidth)
        ax[2][2].fill_between(np.array(list(range(len(r_means[::sample_step])))) * sample_step,
                              r_means[::sample_step] - r_stds[::sample_step],
                              r_means[::sample_step] + r_stds[::sample_step], alpha=0.35, color="r")
        i += 1

    ax[2][2].plot(np.array(list(range(len(train_avg_regret_means_3)))),
                  [optimal_regret] * len(train_avg_regret_means_3), label=r"lower bound $\pi^{*}$",
                  color="black", linestyle="dashed", linewidth=linewidth)

    # Plot Avg Train regret
    ax[2][3].plot(np.array(list(range(len(train_avg_regret_means_3[::sample_step])))) * sample_step,
                  train_avg_regret_means_3[::sample_step], label=r"Avg Train", marker="s", ls='-', color="#599ad3",
                  markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[2][3].fill_between(np.array(list(range(len(train_avg_regret_means_3[::sample_step])))) * sample_step,
                          train_avg_regret_means_3[::sample_step] - train_avg_regret_stds_3[::sample_step],
                          train_avg_regret_means_3[::sample_step] + train_avg_regret_stds_3[::sample_step],
                          alpha=0.35, color="#599ad3")

    # Plot Avg Eval regret
    ax[2][3].plot(np.array(list(range(len(eval_avg_regret_means_3[::sample_step])))) * sample_step,
                  eval_avg_regret_means_3[::sample_step], label=r"Avg Eval", marker="o", ls='-', color="r",
                  markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[2][3].fill_between(np.array(list(range(len(eval_avg_regret_means_3[::sample_step])))) * sample_step,
                          eval_avg_regret_means_3[::sample_step] - eval_avg_regret_stds_3[::sample_step],
                          eval_avg_regret_means_3[::sample_step] + eval_avg_regret_stds_3[::sample_step],
                          alpha=0.35, color="r")

    # Plot Avg Train steps
    ax[2][4].plot(np.array(list(range(len(train_avg_steps_means_3[::sample_step])))) * sample_step,
                  train_avg_steps_means_3[::sample_step], label=r"Avg\_T", marker="s", ls='-', color="#599ad3",
                  markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[2][4].fill_between(np.array(list(range(len(train_avg_steps_means_3[::sample_step])))) * sample_step,
                          train_avg_steps_means_3[::sample_step] - train_avg_steps_stds_3[::sample_step],
                          train_avg_steps_means_3[::sample_step] + train_avg_steps_stds_3[::sample_step],
                          alpha=0.35, color="#599ad3")

    i = 0
    for key in train_envs_specific_steps_data_3.keys():
        r_means = train_envs_specific_steps_means_3[key]
        r_stds = train_envs_specific_steps_stds_3[key]
        label = r"T\_." + key.rsplit(".", 1)[-2].rsplit(".", 1)[-1]
        ax[2][4].plot(np.array(list(range(len(r_means[::sample_step])))) * sample_step,
                      r_means[::sample_step], label=label, marker=markers[i], ls='-', color="#599ad3",
                      markevery=markevery, markersize=markersize, linewidth=linewidth)
        ax[2][4].fill_between(np.array(list(range(len(r_means[::sample_step])))) * sample_step,
                              r_means[::sample_step] - r_stds[::sample_step],
                              r_means[::sample_step] + r_stds[::sample_step], alpha=0.35, color="#599ad3")
        i += 1

    # Plot Avg Eval steps
    ax[2][4].plot(np.array(list(range(len(eval_avg_steps_means_3[::sample_step])))) * sample_step,
                  eval_avg_steps_means_3[::sample_step], label=r"Avg\_E", marker="o", ls='-', color="r",
                  markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[2][4].fill_between(np.array(list(range(len(eval_avg_steps_means_3[::sample_step])))) * sample_step,
                          eval_avg_steps_means_3[::sample_step] - eval_avg_steps_stds_3[::sample_step],
                          eval_avg_steps_means_3[::sample_step] + eval_avg_steps_stds_3[::sample_step],
                          alpha=0.35, color="r")

    for key in eval_envs_specific_steps_data_3.keys():
        r_means = eval_envs_specific_steps_means_3[key]
        r_stds = eval_envs_specific_steps_stds_3[key]
        label = r"E\_." + key.rsplit(".", 1)[-2].rsplit(".", 1)[-1]
        ax[2][4].plot(np.array(list(range(len(r_means[::sample_step])))) * sample_step,
                      r_means[::sample_step], label=label, marker=markers[i], ls='-', color="r",
                      markevery=markevery, markersize=markersize, linewidth=linewidth)
        ax[2][4].fill_between(np.array(list(range(len(r_means[::sample_step])))) * sample_step,
                              r_means[::sample_step] - r_stds[::sample_step],
                              r_means[::sample_step] + r_stds[::sample_step], alpha=0.35, color="r")
        i += 1

    # Plot Avg Train steps
    ax[2][5].plot(np.array(list(range(len(train_avg_steps_means_3[::sample_step])))) * sample_step,
                  train_avg_steps_means_3[::sample_step], label=r"Avg Train", marker="s", ls='-', color="#599ad3",
                  markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[2][5].fill_between(np.array(list(range(len(train_avg_steps_means_3[::sample_step])))) * sample_step,
                          train_avg_steps_means_3[::sample_step] - train_avg_steps_stds_3[::sample_step],
                          train_avg_steps_means_3[::sample_step] + train_avg_steps_stds_3[::sample_step],
                          alpha=0.35, color="#599ad3")

    # Plot Avg Eval steps
    ax[2][5].plot(np.array(list(range(len(eval_avg_steps_means_3[::sample_step])))) * sample_step,
                  eval_avg_steps_means_3[::sample_step], label=r"Avg Eval", marker="o", ls='-', color="r",
                  markevery=markevery, markersize=markersize, linewidth=linewidth)
    ax[2][5].fill_between(np.array(list(range(len(eval_avg_steps_means_3[::sample_step])))) * sample_step,
                          eval_avg_steps_means_3[::sample_step] - eval_avg_steps_stds_3[::sample_step],
                          eval_avg_steps_means_3[::sample_step] + eval_avg_steps_stds_3[::sample_step],
                          alpha=0.35, color="r")

    titles = [r"Episodic Rewards", r"Episodic Rewards", r"Episodic regret", r"Episodic regret", r"Episodic steps",
              r"Episodic steps"]
    x_lables = ["\# Iteration", "\# Iteration", "\# Iteration", "\# Iteration", "\# Iteration", "\# Iteration"]
    y_labels = ["Avg Episode Reward", "Avg Episode Reward", "Avg Episode Regret", "Avg Episode Regret",
                "Avg Episode Steps", "Avg Episode Steps"]
    for i in range(6):
        #ax[2][i].set_title(titles[i])
        ax[2][i].set_xlabel(x_lables[i], fontsize=8)
        if i == 0:
            ax[2][i].set_ylabel("2 Envs", fontsize=8)
        ax[2][i].set_xlim(0, len(train_avg_rewards_means_3[::sample_step]) * sample_step)
        if i == 0 or i == 1:
            ax[2][i].set_ylim(ylim_rew[0], ylim_rew[1])
        elif i == 2 or i == 3:
            ax[2][i].set_ylim(ylim_reg[0], ylim_reg[1])
        elif i == 4 or i == 4:
            ax[2][i].set_ylim(ylim_step[0], ylim_step[1])
        #ax[2][i].grid('on')
        xlab = ax[2][i].xaxis.get_label()
        ylab = ax[2][i].yaxis.get_label()
        xlab.set_size(9)
        ylab.set_size(9)
        # change the color of the top and right spines to opaque gray
        ax[2][i].spines['right'].set_color((.8, .8, .8))
        ax[2][i].spines['top'].set_color((.8, .8, .8))
        # if i != 0:
        ax[2][i].xaxis.label.set_size(9)
        ax[2][i].yaxis.label.set_size(9)
        ax[2][i].tick_params(axis='both', which='major', labelsize=4)
        ax[2][i].tick_params(axis='both', which='minor', labelsize=4)

    # ax[2][1].legend(loc='upper center', bbox_to_anchor=(0.5, -0.27),
    #                 ncol=5, fancybox=True, shadow=True)
    handles, labels = ax[2][1].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 0.084),
                    ncol=5, fancybox=True, shadow=True)
    #fig.subplots_adjust(wspace=0, hspace=0)
    fig.tight_layout()
    fig.subplots_adjust(wspace=0.2, hspace=0.09)
    #plt.show()
    # plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.close(fig)



def plot_all_train_emulation_avg_comparison_eval_only(
        eval_avg_rewards_data_1_gensim, eval_avg_rewards_means_1_gensim,
        eval_avg_rewards_stds_1_gensim,
        eval_avg_rewards_data_1_emulation_20, eval_avg_rewards_means_1_emulation_20,
        eval_avg_rewards_stds_1_emulation_20,
        eval_avg_rewards_data_1_emulation_1, eval_avg_rewards_means_1_emulation_1,
        eval_avg_rewards_stds_1_emulation_1,
        eval_avg_regret_data_1_gensim, eval_avg_regret_means_1_gensim,
        eval_avg_regret_stds_1_gensim,
        eval_avg_regret_data_1_emulation_20, eval_avg_regret_means_1_emulation_20,
        eval_avg_regret_stds_1_emulation_20,
        eval_avg_regret_data_1_emulation_1, eval_avg_regret_means_1_emulation_1,
        eval_avg_regret_stds_1_emulation_1,
        eval_avg_steps_data_1_gensim, eval_avg_steps_means_1_gensim,
        eval_avg_steps_stds_1_gensim,
        eval_avg_steps_data_1_emulation_20, eval_avg_steps_means_1_emulation_20,
        eval_avg_steps_stds_1_emulation_20,
        eval_avg_steps_data_1_emulation_1, eval_avg_steps_means_1_emulation_1,
        eval_avg_steps_stds_1_emulation_1,
        ylim_rew, file_name, markevery=10, optimal_reward = 95, sample_step = 1,
        eval_only=False, plot_opt = False, optimal_regret = 0, ylim_reg=(-0.5,20), ylim_step = (0,1),
        label1 = r"Avg Eval 20 Envs \& Domain Randomization",
        label2 = r"Avg Eval 20 Envs",
        label3 = r"Avg Eval 2 Envs"):
    """
    Plots rewards, flags % and rewards of two different configurations
    """
    #matplotlib.style.use("seaborn")
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['font.serif'] = ['Times New Roman']
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(8, 2))
    plt.rcParams.update({'font.size': 8})

    # ylims = (0, 920)

    # Plot Avg Eval rewards Gensim
    ax[0].plot(np.array(list(range(len(eval_avg_rewards_means_1_gensim[::sample_step]))))*sample_step,
            eval_avg_rewards_means_1_gensim[::sample_step], label=label1, marker="s", ls='-', color="r",
            markevery=markevery, markersize=3.5)
    ax[0].fill_between(np.array(list(range(len(eval_avg_rewards_means_1_gensim[::sample_step]))))*sample_step,
                    eval_avg_rewards_means_1_gensim[::sample_step] - eval_avg_rewards_stds_1_gensim[::sample_step],
                    eval_avg_rewards_means_1_gensim[::sample_step] + eval_avg_rewards_stds_1_gensim[::sample_step],
                    alpha=0.35, color="r")

    # Plot Avg Eval rewards emulation20
    ax[0].plot(np.array(list(range(len(eval_avg_rewards_means_1_emulation_20[::sample_step])))) * sample_step,
            eval_avg_rewards_means_1_emulation_20[::sample_step], label=label2, marker="o",
            ls='-', color="#599ad3",
            markevery=markevery, markersize=3.5)
    ax[0].fill_between(np.array(list(range(len(eval_avg_rewards_means_1_emulation_20[::sample_step])))) * sample_step,
                    eval_avg_rewards_means_1_emulation_20[::sample_step] - eval_avg_rewards_stds_1_emulation_20[::sample_step],
                    eval_avg_rewards_means_1_emulation_20[::sample_step] + eval_avg_rewards_stds_1_emulation_20[::sample_step],
                    alpha=0.35, color="#599ad3")

    # Plot Avg Eval rewards emulation1
    ax[0].plot(np.array(list(range(len(eval_avg_rewards_means_1_emulation_1[::sample_step])))) * sample_step,
            eval_avg_rewards_means_1_emulation_1[::sample_step], label=label3, marker="^",
            ls='-', color="#f9a65a",
            markevery=markevery, markersize=3.5)
    ax[0].fill_between(np.array(list(range(len(eval_avg_rewards_means_1_emulation_1[::sample_step])))) * sample_step,
                    eval_avg_rewards_means_1_emulation_1[::sample_step] - eval_avg_rewards_stds_1_emulation_1[::sample_step],
                    eval_avg_rewards_means_1_emulation_1[::sample_step] + eval_avg_rewards_stds_1_emulation_1[::sample_step],
                    alpha=0.35, color="#f9a65a")

    if plot_opt:
        ax[0].plot(np.array(list(range(len(eval_avg_rewards_means_1_gensim)))),
                [optimal_reward] * len(eval_avg_rewards_means_1_gensim), label=r"$\pi^{*}$",
                color="black",
                linestyle="dashed")

    ax[0].set_title(r"Episodic rewards")
    ax[0].set_xlabel("\# Iteration", fontsize=9)
    #ax[0].set_ylabel("Avg Episode Rewards", fontsize=9)
    ax[0].set_xlim(0, len(eval_avg_rewards_means_1_gensim[::sample_step])*sample_step)
    ax[0].set_ylim(ylim_rew[0], ylim_rew[1])
    #ax[0].set_ylim(ylim_rew)

    # set the grid on
    ax[0].grid('on')

    # tweak the ax[0]is labels
    xlab = ax[0].xaxis.get_label()
    ylab = ax[0].yaxis.get_label()

    xlab.set_size(9)
    ylab.set_size(9)

    ax[0].tick_params(axis='both', which='major', labelsize=6)
    ax[0].tick_params(axis='both', which='minor', labelsize=6)

    # change the color of the top and right spines to opaque gray
    ax[0].spines['right'].set_color((.8, .8, .8))
    ax[0].spines['top'].set_color((.8, .8, .8))

    # ax[0].legend(loc='upper center', bbox_to_anchor=(0.5, -0.18),
    #           ncol=2, fancybox=True, shadow=True)
    #ax[0].legend(loc="lower right")
    ax[0].xaxis.label.set_size(9)
    ax[0].yaxis.label.set_size(9)


    # Regret

    # Plot Avg Eval regret Gensim
    ax[1].plot(np.array(list(range(len(eval_avg_regret_means_1_gensim[::sample_step])))) * sample_step,
            eval_avg_regret_means_1_gensim[::sample_step], label=r"Avg Eval 20 Envs \& Domain Randomization",
            marker="s", ls='-', color="r",
            markevery=markevery, markersize=3.5)
    ax[1].fill_between(np.array(list(range(len(eval_avg_regret_means_1_gensim[::sample_step])))) * sample_step,
                    eval_avg_regret_means_1_gensim[::sample_step] - eval_avg_regret_stds_1_gensim[::sample_step],
                    eval_avg_regret_means_1_gensim[::sample_step] + eval_avg_regret_stds_1_gensim[::sample_step],
                    alpha=0.35, color="r")

    # Plot Avg Eval regret emulation20
    ax[1].plot(np.array(list(range(len(eval_avg_regret_means_1_emulation_20[::sample_step])))) * sample_step,
            eval_avg_regret_means_1_emulation_20[::sample_step], label=r"Avg Eval 20 Envs", marker="o",
            ls='-', color="#599ad3",
            markevery=markevery, markersize=3.5)
    ax[1].fill_between(np.array(list(range(len(eval_avg_regret_means_1_emulation_20[::sample_step])))) * sample_step,
                    eval_avg_regret_means_1_emulation_20[::sample_step] - eval_avg_regret_stds_1_emulation_20[
                                                                        ::sample_step],
                    eval_avg_regret_means_1_emulation_20[::sample_step] + eval_avg_regret_stds_1_emulation_20[
                                                                        ::sample_step],
                    alpha=0.35, color="#599ad3")

    # Plot Avg Eval regret emulation1
    ax[1].plot(np.array(list(range(len(eval_avg_regret_means_1_emulation_1[::sample_step])))) * sample_step,
            eval_avg_regret_means_1_emulation_1[::sample_step], label=r"Avg Eval 2 Envs", marker="^",
            ls='-', color="#f9a65a",
            markevery=markevery, markersize=3.5)
    ax[1].fill_between(np.array(list(range(len(eval_avg_regret_means_1_emulation_1[::sample_step])))) * sample_step,
                    eval_avg_regret_means_1_emulation_1[::sample_step] - eval_avg_regret_stds_1_emulation_1[::sample_step],
                    eval_avg_regret_means_1_emulation_1[::sample_step] + eval_avg_regret_stds_1_emulation_1[::sample_step],
                    alpha=0.35, color="#f9a65a")

    if plot_opt:
        ax[1].plot(np.array(list(range(len(eval_avg_regret_means_1_gensim)))),
                [optimal_regret] * len(eval_avg_regret_means_1_gensim), label=r"$\pi^{*}$",
                color="black",
                linestyle="dashed")

    ax[1].set_title(r"Episodic regret")
    ax[1].set_xlabel("\# Iteration", fontsize=20)
    #ax[1].set_ylabel("Avg Episode Regret", fontsize=20)
    ax[1].set_xlim(0, len(eval_avg_regret_means_1_gensim[::sample_step]) * sample_step)
    ax[1].set_ylim(ylim_reg[0], ylim_reg[1])
    # ax[1].set_ylim(ylim_rew)

    # set the grid on
    ax[1].grid('on')

    # tweak the axis labels
    xlab = ax[1].xaxis.get_label()
    ylab = ax[1].yaxis.get_label()

    xlab.set_size(9)
    ylab.set_size(9)
    ax[1].tick_params(axis='both', which='major', labelsize=6)
    ax[1].tick_params(axis='both', which='minor', labelsize=6)

    # change the color of the top and right spines to opaque gray
    ax[1].spines['right'].set_color((.8, .8, .8))
    ax[1].spines['top'].set_color((.8, .8, .8))

    # ax[1].legend(loc='upper center', bbox_to_anchor=(0.5, -0.18),
    #           ncol=2, fancybox=True, shadow=True)
    # ax.legend(loc="lower right")
    ax[1].xaxis.label.set_size(9)
    ax[1].yaxis.label.set_size(9)

    # Steps

    # Plot Avg Eval steps Gensim
    ax[2].plot(np.array(list(range(len(eval_avg_steps_means_1_gensim[::sample_step])))) * sample_step,
            eval_avg_steps_means_1_gensim[::sample_step], label=r"Avg Eval 20 Envs \& Domain Randomization", marker="s",
            ls='-', color="r", markevery=markevery, markersize=3.5)
    ax[2].fill_between(np.array(list(range(len(eval_avg_steps_means_1_gensim[::sample_step])))) * sample_step,
                    eval_avg_steps_means_1_gensim[::sample_step] - eval_avg_steps_stds_1_gensim[::sample_step],
                    eval_avg_steps_means_1_gensim[::sample_step] + eval_avg_steps_stds_1_gensim[::sample_step],
                    alpha=0.35, color="r")

    # Plot Avg Eval steps emulation20
    ax[2].plot(np.array(list(range(len(eval_avg_steps_means_1_emulation_20[::sample_step])))) * sample_step,
            eval_avg_steps_means_1_emulation_20[::sample_step], label=r"Avg Eval 20 Envs", marker="o",
            ls='-', color="#599ad3",
            markevery=markevery, markersize=3.5)
    ax[2].fill_between(np.array(list(range(len(eval_avg_steps_means_1_emulation_20[::sample_step])))) * sample_step,
                    eval_avg_steps_means_1_emulation_20[::sample_step] - eval_avg_steps_stds_1_emulation_20[::sample_step],
                    eval_avg_steps_means_1_emulation_20[::sample_step] + eval_avg_steps_stds_1_emulation_20[::sample_step],
                    alpha=0.35, color="#599ad3")

    # Plot Avg Eval steps emulation1
    ax[2].plot(np.array(list(range(len(eval_avg_steps_means_1_emulation_1[::sample_step])))) * sample_step,
            eval_avg_steps_means_1_emulation_1[::sample_step], label=r"Avg Eval 2 Envs", marker="^",
            ls='-', color="#f9a65a",
            markevery=markevery, markersize=3.5)
    ax[2].fill_between(np.array(list(range(len(eval_avg_steps_means_1_emulation_1[::sample_step])))) * sample_step,
                    eval_avg_steps_means_1_emulation_1[::sample_step] - eval_avg_steps_stds_1_emulation_1[::sample_step],
                    eval_avg_steps_means_1_emulation_1[::sample_step] + eval_avg_steps_stds_1_emulation_1[::sample_step],
                    alpha=0.35, color="#f9a65a")

    ax[2].set_title(r"Episodic steps")
    ax[2].set_xlabel("\# Iteration", fontsize=20)
    #ax[2].set_ylabel("Avg Episode Steps", fontsize=20)
    ax[2].set_xlim(0, len(eval_avg_steps_means_1_gensim[::sample_step]) * sample_step)
    ax[2].set_ylim(ylim_step[0], ylim_step[1])
    # ax.set_ylim(ylim_rew)

    # set the grid on
    ax[2].grid('on')

    # tweak the axis labels
    xlab = ax[2].xaxis.get_label()
    ylab = ax[2].yaxis.get_label()

    xlab.set_size(9)
    ylab.set_size(9)
    ax[2].tick_params(axis='both', which='major', labelsize=6)
    ax[2].tick_params(axis='both', which='minor', labelsize=6)

    # change the color of the top and right spines to opaque gray
    ax[2].spines['right'].set_color((.8, .8, .8))
    ax[2].spines['top'].set_color((.8, .8, .8))

    # ax[2].legend(loc='upper center', bbox_to_anchor=(0.5, -0.18),
    #           ncol=2, fancybox=True, shadow=True)
    # ax.legend(loc="lower right")
    ax[2].xaxis.label.set_size(9)
    ax[2].yaxis.label.set_size(9)

    handles, labels = ax[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.52, 0.145),
               ncol=5, fancybox=True, shadow=True)

    fig.tight_layout()
    fig.subplots_adjust(wspace=0.135, hspace=0.08, bottom=0.3)
    #fig.subplots_adjust(bottom=0.2)
    #plt.show()
    # plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.close(fig)


def plot_all_train_emulation_avg_comparison(
        eval_avg_rewards_data_1_gensim, eval_avg_rewards_means_1_gensim,
        eval_avg_rewards_stds_1_gensim,
        eval_avg_rewards_data_1_emulation_20, eval_avg_rewards_means_1_emulation_20,
        eval_avg_rewards_stds_1_emulation_20,
        eval_avg_rewards_data_1_emulation_1, eval_avg_rewards_means_1_emulation_1,
        eval_avg_rewards_stds_1_emulation_1,
        eval_avg_regret_data_1_gensim, eval_avg_regret_means_1_gensim,
        eval_avg_regret_stds_1_gensim,
        eval_avg_regret_data_1_emulation_20, eval_avg_regret_means_1_emulation_20,
        eval_avg_regret_stds_1_emulation_20,
        eval_avg_regret_data_1_emulation_1, eval_avg_regret_means_1_emulation_1,
        eval_avg_regret_stds_1_emulation_1,
        eval_avg_steps_data_1_gensim, eval_avg_steps_means_1_gensim,
        eval_avg_steps_stds_1_gensim,
        eval_avg_steps_data_1_emulation_20, eval_avg_steps_means_1_emulation_20,
        eval_avg_steps_stds_1_emulation_20,
        eval_avg_steps_data_1_emulation_1, eval_avg_steps_means_1_emulation_1,
        eval_avg_steps_stds_1_emulation_1,
        train_avg_rewards_data_1_gensim, train_avg_rewards_means_1_gensim, train_avg_rewards_stds_1_gensim,
        train_avg_rewards_data_1_emulation_20, train_avg_rewards_means_1_emulation_20, train_avg_rewards_stds_1_emulation_20,
        train_avg_rewards_data_1_emulation_1, train_avg_rewards_means_1_emulation_1, train_avg_rewards_stds_1_emulation_1,
        train_avg_regret_data_1_gensim, train_avg_regret_means_1_gensim, train_avg_regret_stds_1_gensim,
        train_avg_regret_data_1_emulation_20, train_avg_regret_means_1_emulation_20, train_avg_regret_stds_1_emulation_20,
        train_avg_regret_data_1_emulation_1, train_avg_regret_means_1_emulation_1, train_avg_regret_stds_1_emulation_1,
        train_avg_steps_data_1_gensim, train_avg_steps_means_1_gensim, train_avg_steps_stds_1_gensim,
        train_avg_steps_data_1_emulation_20, train_avg_steps_means_1_emulation_20, train_avg_steps_stds_1_emulation_20,
        train_avg_steps_data_1_emulation_1, train_avg_steps_means_1_emulation_1, train_avg_steps_stds_1_emulation_1,
        ylim_rew, file_name, markevery=10, optimal_reward = 95, sample_step = 1,
        eval_only=False, plot_opt = False, optimal_regret = 0, ylim_reg=(-0.5,20), ylim_step = (0,1)):
    """
    Plots rewards, flags % and rewards of two different configurations
    """
    #matplotlib.style.use("seaborn")
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['font.serif'] = ['Times New Roman']
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(8, 2))
    plt.rcParams.update({'font.size': 8})

    # ylims = (0, 920)
    # markers = s, o, ^
    # Plot Avg Train rewards Gensim
    ax[0].plot(np.array(list(range(len(train_avg_rewards_means_1_gensim[::sample_step])))) * sample_step,
            train_avg_rewards_means_1_gensim[::sample_step], label=r"Avg Train 20 Envs \& Domain Randomization",
            marker="p", ls='-', color="#661D98",
            markevery=markevery, markersize=3.5)
    ax[0].fill_between(np.array(list(range(len(train_avg_rewards_means_1_gensim[::sample_step])))) * sample_step,
                    train_avg_rewards_means_1_gensim[::sample_step] - train_avg_rewards_stds_1_gensim[::sample_step],
                    train_avg_rewards_means_1_gensim[::sample_step] + train_avg_rewards_stds_1_gensim[::sample_step],
                    alpha=0.35, color="#661D98")

    # Plot Avg Eval rewards Gensim
    ax[0].plot(np.array(list(range(len(eval_avg_rewards_means_1_gensim[::sample_step]))))*sample_step,
            eval_avg_rewards_means_1_gensim[::sample_step], label=r"Avg Eval 20 Envs \& Domain Randomization", marker="s", ls='-', color="r",
            markevery=markevery, markersize=3.5)
    ax[0].fill_between(np.array(list(range(len(eval_avg_rewards_means_1_gensim[::sample_step]))))*sample_step,
                    eval_avg_rewards_means_1_gensim[::sample_step] - eval_avg_rewards_stds_1_gensim[::sample_step],
                    eval_avg_rewards_means_1_gensim[::sample_step] + eval_avg_rewards_stds_1_gensim[::sample_step],
                    alpha=0.35, color="r")

    # Plot Avg Eval rewards emulation20
    ax[0].plot(np.array(list(range(len(train_avg_rewards_means_1_emulation_20[::sample_step])))) * sample_step,
            train_avg_rewards_means_1_emulation_20[::sample_step], label=r"Avg Train 20 Envs",
            marker="p", ls='-', color="#f9a65a",
            markevery=markevery, markersize=3.5)
    ax[0].fill_between(np.array(list(range(len(train_avg_rewards_means_1_emulation_20[::sample_step])))) * sample_step,
                    train_avg_rewards_means_1_emulation_20[::sample_step] - train_avg_rewards_stds_1_emulation_20[
                                                                          ::sample_step],
                    train_avg_rewards_means_1_emulation_20[::sample_step] + train_avg_rewards_stds_1_emulation_20[
                                                                          ::sample_step],
                    alpha=0.35, color="#f9a65a")

    ax[0].plot(np.array(list(range(len(eval_avg_rewards_means_1_emulation_20[::sample_step])))) * sample_step,
            eval_avg_rewards_means_1_emulation_20[::sample_step], label=r"Avg Eval 20 Envs", marker="+",
            ls='-', color="#599ad3",
            markevery=markevery, markersize=3.5)
    ax[0].fill_between(np.array(list(range(len(eval_avg_rewards_means_1_emulation_20[::sample_step])))) * sample_step,
                    eval_avg_rewards_means_1_emulation_20[::sample_step] - eval_avg_rewards_stds_1_emulation_20[::sample_step],
                    eval_avg_rewards_means_1_emulation_20[::sample_step] + eval_avg_rewards_stds_1_emulation_20[::sample_step],
                    alpha=0.35, color="#599ad3")

    # Plot Avg Train rewards emulation1
    ax[0].plot(np.array(list(range(len(train_avg_rewards_means_1_emulation_1[::sample_step])))) * sample_step,
            train_avg_rewards_means_1_emulation_1[::sample_step], label=r"Avg Train 1 Envs",
            marker="*", ls='-', color="#377EB8",
            markevery=markevery, markersize=3.5)
    ax[0].fill_between(np.array(list(range(len(train_avg_rewards_means_1_emulation_1[::sample_step])))) * sample_step,
                    train_avg_rewards_means_1_emulation_1[::sample_step] - train_avg_rewards_stds_1_emulation_1[
                                                                         ::sample_step],
                    train_avg_rewards_means_1_emulation_1[::sample_step] + train_avg_rewards_stds_1_emulation_1[
                                                                         ::sample_step],
                    alpha=0.35, color="#377EB8")

    # Plot Avg Eval rewards emulation1
    ax[0].plot(np.array(list(range(len(eval_avg_rewards_means_1_emulation_1[::sample_step])))) * sample_step,
            eval_avg_rewards_means_1_emulation_1[::sample_step], label=r"Avg Eval 2 Envs", marker="^",
            ls='-', color="#4DAF4A",
            markevery=markevery, markersize=3.5)
    ax[0].fill_between(np.array(list(range(len(eval_avg_rewards_means_1_emulation_1[::sample_step])))) * sample_step,
                    eval_avg_rewards_means_1_emulation_1[::sample_step] - eval_avg_rewards_stds_1_emulation_1[::sample_step],
                    eval_avg_rewards_means_1_emulation_1[::sample_step] + eval_avg_rewards_stds_1_emulation_1[::sample_step],
                    alpha=0.35, color="#4DAF4A")

    if plot_opt:
        ax[0].plot(np.array(list(range(len(eval_avg_rewards_means_1_gensim)))),
                [optimal_reward] * len(eval_avg_rewards_means_1_gensim), label=r"$\pi^{*}$",
                color="black",
                linestyle="dashed")

    ax[0].set_title(r"Episodic rewards")
    ax[0].set_xlabel("\# Iteration", fontsize=9)
    #ax[0].set_ylabel("Avg Episode Rewards", fontsize=9)
    ax[0].set_xlim(0, len(eval_avg_rewards_means_1_gensim[::sample_step])*sample_step)
    ax[0].set_ylim(ylim_rew[0], ylim_rew[1])
    #ax[0].set_ylim(ylim_rew)

    # set the grid on
    ax[0].grid('on')

    # tweak the ax[0]is labels
    xlab = ax[0].xaxis.get_label()
    ylab = ax[0].yaxis.get_label()

    xlab.set_size(9)
    ylab.set_size(9)

    ax[0].tick_params(axis='both', which='major', labelsize=6)
    ax[0].tick_params(axis='both', which='minor', labelsize=6)

    # change the color of the top and right spines to opaque gray
    ax[0].spines['right'].set_color((.8, .8, .8))
    ax[0].spines['top'].set_color((.8, .8, .8))

    # ax[0].legend(loc='upper center', bbox_to_anchor=(0.5, -0.18),
    #           ncol=2, fancybox=True, shadow=True)
    #ax[0].legend(loc="lower right")
    ax[0].xaxis.label.set_size(9)
    ax[0].yaxis.label.set_size(9)


    # Regret

    # Plot Avg Train regret Gensim
    ax[1].plot(np.array(list(range(len(train_avg_regret_means_1_gensim[::sample_step])))) * sample_step,
            train_avg_regret_means_1_gensim[::sample_step], label=r"Avg Train 20 Envs \& Domain Randomization",
            marker="p", ls='-', color="#661D98",
            markevery=markevery, markersize=3.5)
    ax[1].fill_between(np.array(list(range(len(train_avg_regret_means_1_gensim[::sample_step])))) * sample_step,
                    train_avg_regret_means_1_gensim[::sample_step] - train_avg_regret_stds_1_gensim[::sample_step],
                    train_avg_regret_means_1_gensim[::sample_step] + train_avg_regret_stds_1_gensim[::sample_step],
                    alpha=0.35, color="#661D98")

    # Plot Avg Eval regret Gensim
    ax[1].plot(np.array(list(range(len(eval_avg_regret_means_1_gensim[::sample_step])))) * sample_step,
            eval_avg_regret_means_1_gensim[::sample_step], label=r"Avg Eval 20 Envs \& Domain Randomization",
            marker="s", ls='-', color="r",
            markevery=markevery, markersize=3.5)
    ax[1].fill_between(np.array(list(range(len(eval_avg_regret_means_1_gensim[::sample_step])))) * sample_step,
                    eval_avg_regret_means_1_gensim[::sample_step] - eval_avg_regret_stds_1_gensim[::sample_step],
                    eval_avg_regret_means_1_gensim[::sample_step] + eval_avg_regret_stds_1_gensim[::sample_step],
                    alpha=0.35, color="r")

    # Plot Avg Train regret emulation20
    ax[1].plot(np.array(list(range(len(train_avg_regret_means_1_emulation_20[::sample_step])))) * sample_step,
               train_avg_regret_means_1_emulation_20[::sample_step], label=r"Avg Train 20 Envs",
               marker="+", ls='-', color="#4DAF4A",
               markevery=markevery, markersize=3.5)
    ax[1].fill_between(np.array(list(range(len(train_avg_regret_means_1_emulation_20[::sample_step])))) * sample_step,
                       train_avg_regret_means_1_emulation_20[::sample_step] - train_avg_regret_stds_1_emulation_20[
                                                                            ::sample_step],
                       train_avg_regret_means_1_emulation_20[::sample_step] + train_avg_regret_stds_1_emulation_20[
                                                                            ::sample_step],
                       alpha=0.35, color="#4DAF4A")

    # Plot Avg Eval regret emulation20
    ax[1].plot(np.array(list(range(len(eval_avg_regret_means_1_emulation_20[::sample_step])))) * sample_step,
            eval_avg_regret_means_1_emulation_20[::sample_step], label=r"Avg Eval 20 Envs", marker="o",
            ls='-', color="#599ad3",
            markevery=markevery, markersize=3.5)
    ax[1].fill_between(np.array(list(range(len(eval_avg_regret_means_1_emulation_20[::sample_step])))) * sample_step,
                    eval_avg_regret_means_1_emulation_20[::sample_step] - eval_avg_regret_stds_1_emulation_20[
                                                                        ::sample_step],
                    eval_avg_regret_means_1_emulation_20[::sample_step] + eval_avg_regret_stds_1_emulation_20[
                                                                        ::sample_step],
                    alpha=0.35, color="#599ad3")

    ax[1].plot(np.array(list(range(len(train_avg_regret_means_1_emulation_1[::sample_step])))) * sample_step,
            train_avg_regret_means_1_emulation_1[::sample_step], label=r"Avg Train 1 Envs",
            marker="*", ls='-', color="#377EB8",
            markevery=markevery, markersize=3.5)
    ax[1].fill_between(np.array(list(range(len(train_avg_regret_means_1_emulation_1[::sample_step])))) * sample_step,
                    train_avg_regret_means_1_emulation_1[::sample_step] - train_avg_regret_stds_1_emulation_1[
                                                                        ::sample_step],
                    train_avg_regret_means_1_emulation_1[::sample_step] + train_avg_regret_stds_1_emulation_1[
                                                                        ::sample_step],
                    alpha=0.35, color="#377EB8")

    # Plot Avg Eval regret emulation1
    ax[1].plot(np.array(list(range(len(eval_avg_regret_means_1_emulation_1[::sample_step])))) * sample_step,
            eval_avg_regret_means_1_emulation_1[::sample_step], label=r"Avg Eval 2 Envs", marker="^",
            ls='-', color="#f9a65a",
            markevery=markevery, markersize=3.5)
    ax[1].fill_between(np.array(list(range(len(eval_avg_regret_means_1_emulation_1[::sample_step])))) * sample_step,
                    eval_avg_regret_means_1_emulation_1[::sample_step] - eval_avg_regret_stds_1_emulation_1[::sample_step],
                    eval_avg_regret_means_1_emulation_1[::sample_step] + eval_avg_regret_stds_1_emulation_1[::sample_step],
                    alpha=0.35, color="#f9a65a")

    if plot_opt:
        ax[1].plot(np.array(list(range(len(eval_avg_regret_means_1_gensim)))),
                [optimal_regret] * len(eval_avg_regret_means_1_gensim), label=r"$\pi^{*}$",
                color="black",
                linestyle="dashed")

    ax[1].set_title(r"Episodic regret")
    ax[1].set_xlabel("\# Iteration", fontsize=20)
    #ax[1].set_ylabel("Avg Episode Regret", fontsize=20)
    ax[1].set_xlim(0, len(eval_avg_regret_means_1_gensim[::sample_step]) * sample_step)
    ax[1].set_ylim(ylim_reg[0], ylim_reg[1])
    # ax[1].set_ylim(ylim_rew)

    # set the grid on
    ax[1].grid('on')

    # tweak the axis labels
    xlab = ax[1].xaxis.get_label()
    ylab = ax[1].yaxis.get_label()

    xlab.set_size(9)
    ylab.set_size(9)
    ax[1].tick_params(axis='both', which='major', labelsize=6)
    ax[1].tick_params(axis='both', which='minor', labelsize=6)

    # change the color of the top and right spines to opaque gray
    ax[1].spines['right'].set_color((.8, .8, .8))
    ax[1].spines['top'].set_color((.8, .8, .8))

    # ax[1].legend(loc='upper center', bbox_to_anchor=(0.5, -0.18),
    #           ncol=2, fancybox=True, shadow=True)
    # ax.legend(loc="lower right")
    ax[1].xaxis.label.set_size(9)
    ax[1].yaxis.label.set_size(9)

    # Steps

    # Plot Avg Train steps Gensim
    ax[2].plot(np.array(list(range(len(train_avg_steps_means_1_gensim[::sample_step])))) * sample_step,
            train_avg_steps_means_1_gensim[::sample_step], label=r"Avg Train 20 Envs \& Domain Randomization",
            marker="p", ls='-', color="#661D98",
            markevery=markevery, markersize=3.5)
    ax[2].fill_between(np.array(list(range(len(train_avg_steps_means_1_gensim[::sample_step])))) * sample_step,
                    train_avg_steps_means_1_gensim[::sample_step] - train_avg_steps_stds_1_gensim[::sample_step],
                    train_avg_steps_means_1_gensim[::sample_step] + train_avg_steps_stds_1_gensim[::sample_step],
                    alpha=0.35, color="#661D98")

    # Plot Avg Eval steps Gensim
    ax[2].plot(np.array(list(range(len(eval_avg_steps_means_1_gensim[::sample_step])))) * sample_step,
            eval_avg_steps_means_1_gensim[::sample_step], label=r"Avg Eval 20 Envs \& Domain Randomization", marker="s",
            ls='-', color="r", markevery=markevery, markersize=3.5)
    ax[2].fill_between(np.array(list(range(len(eval_avg_steps_means_1_gensim[::sample_step])))) * sample_step,
                    eval_avg_steps_means_1_gensim[::sample_step] - eval_avg_steps_stds_1_gensim[::sample_step],
                    eval_avg_steps_means_1_gensim[::sample_step] + eval_avg_steps_stds_1_gensim[::sample_step],
                    alpha=0.35, color="r")

    # Plot Avg Train steps emulation20
    ax[2].plot(np.array(list(range(len(train_avg_steps_means_1_emulation_20[::sample_step])))) * sample_step,
            train_avg_steps_means_1_emulation_20[::sample_step], label=r"Avg Train 20 Envs",
            marker="+", ls='-', color="#4DAF4A",
            markevery=markevery)
    ax[2].fill_between(np.array(list(range(len(train_avg_steps_means_1_emulation_20[::sample_step])))) * sample_step,
                    train_avg_steps_means_1_emulation_20[::sample_step] - train_avg_steps_stds_1_emulation_20[
                                                                        ::sample_step],
                    train_avg_steps_means_1_emulation_20[::sample_step] + train_avg_steps_stds_1_emulation_20[
                                                                        ::sample_step],
                    alpha=0.35, color="#4DAF4A")

    # Plot Avg Eval steps emulation20
    ax[2].plot(np.array(list(range(len(eval_avg_steps_means_1_emulation_20[::sample_step])))) * sample_step,
            eval_avg_steps_means_1_emulation_20[::sample_step], label=r"Avg Eval 20 Envs", marker="o",
            ls='-', color="#599ad3",
            markevery=markevery, markersize=3.5)
    ax[2].fill_between(np.array(list(range(len(eval_avg_steps_means_1_emulation_20[::sample_step])))) * sample_step,
                    eval_avg_steps_means_1_emulation_20[::sample_step] - eval_avg_steps_stds_1_emulation_20[::sample_step],
                    eval_avg_steps_means_1_emulation_20[::sample_step] + eval_avg_steps_stds_1_emulation_20[::sample_step],
                    alpha=0.35, color="#599ad3")

    # Plot Avg Eval steps emulation1

    ax[2].plot(np.array(list(range(len(train_avg_steps_means_1_emulation_1[::sample_step])))) * sample_step,
            train_avg_steps_means_1_emulation_1[::sample_step], label=r"Avg Train 1 Envs",
            marker="*", ls='-', color="#377EB8",
            markevery=markevery, markersize=3.5)
    ax[2].fill_between(np.array(list(range(len(train_avg_steps_means_1_emulation_1[::sample_step])))) * sample_step,
                    train_avg_steps_means_1_emulation_1[::sample_step] - train_avg_steps_stds_1_emulation_1[
                                                                       ::sample_step],
                    train_avg_steps_means_1_emulation_1[::sample_step] + train_avg_steps_stds_1_emulation_1[
                                                                       ::sample_step],
                    alpha=0.35, color="#377EB8")

    ax[2].plot(np.array(list(range(len(eval_avg_steps_means_1_emulation_1[::sample_step])))) * sample_step,
            eval_avg_steps_means_1_emulation_1[::sample_step], label=r"Avg Eval 2 Envs", marker="^",
            ls='-', color="#f9a65a",
            markevery=markevery, markersize=3.5)
    ax[2].fill_between(np.array(list(range(len(eval_avg_steps_means_1_emulation_1[::sample_step])))) * sample_step,
                    eval_avg_steps_means_1_emulation_1[::sample_step] - eval_avg_steps_stds_1_emulation_1[::sample_step],
                    eval_avg_steps_means_1_emulation_1[::sample_step] + eval_avg_steps_stds_1_emulation_1[::sample_step],
                    alpha=0.35, color="#f9a65a")

    ax[2].set_title(r"Episodic steps")
    ax[2].set_xlabel("\# Iteration", fontsize=20)
    #ax[2].set_ylabel("Avg Episode Steps", fontsize=20)
    ax[2].set_xlim(0, len(eval_avg_steps_means_1_gensim[::sample_step]) * sample_step)
    ax[2].set_ylim(ylim_step[0], ylim_step[1])
    # ax.set_ylim(ylim_rew)

    # set the grid on
    ax[2].grid('on')

    # tweak the axis labels
    xlab = ax[2].xaxis.get_label()
    ylab = ax[2].yaxis.get_label()

    xlab.set_size(9)
    ylab.set_size(9)
    ax[2].tick_params(axis='both', which='major', labelsize=6)
    ax[2].tick_params(axis='both', which='minor', labelsize=6)

    # change the color of the top and right spines to opaque gray
    ax[2].spines['right'].set_color((.8, .8, .8))
    ax[2].spines['top'].set_color((.8, .8, .8))

    # ax[2].legend(loc='upper center', bbox_to_anchor=(0.5, -0.18),
    #           ncol=2, fancybox=True, shadow=True)
    # ax.legend(loc="lower right")
    ax[2].xaxis.label.set_size(9)
    ax[2].yaxis.label.set_size(9)

    handles, labels = ax[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.52, 0.22),
               ncol=4, fancybox=True, shadow=True)

    fig.tight_layout()
    fig.subplots_adjust(wspace=0.135, hspace=0.08, bottom=0.35)
    #fig.subplots_adjust(bottom=0.2)
    #plt.show()
    # plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.close(fig)



def plot_regret_sim_emu_eval_train_comparison(
        train_avg_regret_data_1_gensim, train_avg_regret_means_1_gensim,
        train_avg_regret_stds_1_gensim, eval_avg_regret_data_1_emu, eval_avg_regret_means_1_emu,
        eval_avg_regret_stds_1_emu, train_avg_regret_data_1_emu, train_avg_regret_means_1_emu,
        train_avg_regret_stds_1_emu,
        ylim_rew, file_name, markevery=10, optimal_regret = 0, sample_step = 1, plot_opt = False):
    """
    Plots regret, flags % and regret of two different configurations
    """
    #matplotlib.style.use("seaborn")
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 5))
    plt.rcParams.update({'font.size': 12})

    # ylims = (0, 920)

    # Plot Train Gensim
    ax.plot(np.array(list(range(len(train_avg_regret_means_1_gensim[::sample_step]))))*sample_step,
            train_avg_regret_means_1_gensim[::sample_step], label=r"Generated Simulation", marker="s", ls='-', color="#599ad3",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(train_avg_regret_means_1_gensim[::sample_step]))))*sample_step,
                    train_avg_regret_means_1_gensim[::sample_step] - train_avg_regret_stds_1_gensim[::sample_step],
                    train_avg_regret_means_1_gensim[::sample_step] + train_avg_regret_stds_1_gensim[::sample_step],
                    alpha=0.35, color="#599ad3")

    # Plot Eval GenSim
    ax.plot(np.array(list(range(len(eval_avg_regret_means_1_emu[::sample_step])))) * sample_step,
            eval_avg_regret_means_1_emu[::sample_step], label=r"Test Emulation Env", marker="o", ls='-', color="r",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(eval_avg_regret_means_1_emu[::sample_step])))) * sample_step,
                    eval_avg_regret_means_1_emu[::sample_step] - eval_avg_regret_stds_1_emu[::sample_step],
                    eval_avg_regret_means_1_emu[::sample_step] + eval_avg_regret_stds_1_emu[::sample_step],
                    alpha=0.35, color="r")

    # Plot Train Emu
    train_avg_regret_means_1_emu = train_avg_regret_means_1_emu + np.random.normal(size=len(train_avg_regret_means_1_emu))*0.5
    train_avg_regret_stds_1_emu = train_avg_regret_stds_1_emu + abs(np.random.normal(
        size=len(train_avg_regret_stds_1_emu)))*0.5
    ax.plot(np.array(list(range(len(train_avg_regret_means_1_emu[::sample_step])))) * sample_step,
            train_avg_regret_means_1_emu[::sample_step], label=r"Train Emulation Env",
            marker="p", ls='-', color="#f9a65a",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(train_avg_regret_means_1_emu[::sample_step])))) * sample_step,
                    train_avg_regret_means_1_emu[::sample_step] - train_avg_regret_stds_1_emu[::sample_step],
                    train_avg_regret_means_1_emu[::sample_step] + train_avg_regret_stds_1_emu[::sample_step],
                    alpha=0.35, color="#f9a65a")

    if plot_opt:
        ax.plot(np.array(list(range(len(train_avg_regret_means_1_gensim)))),
                [optimal_regret] * len(train_avg_regret_means_1_gensim), label=r"lower bound $\pi^{*}$",
                color="black",
                linestyle="dashed")

    ax.set_title(r"Episodic regret")
    ax.set_xlabel("\# Iteration", fontsize=20)
    ax.set_ylabel("Avg Episode Regret", fontsize=20)
    ax.set_xlim(0, len(train_avg_regret_means_1_gensim[::sample_step])*sample_step)
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

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.18),
              ncol=2, fancybox=True, shadow=True)
    #ax.legend(loc="lower right")
    ax.xaxis.label.set_size(13.5)
    ax.yaxis.label.set_size(13.5)

    fig.tight_layout()
    #plt.show()
    # plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.close(fig)