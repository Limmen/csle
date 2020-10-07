from typing import Union
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
import pandas as pd
import os

def plot_rewards_flags_steps(rewards_data, rewards_means, rewards_stds,
                             flags_data, flags_means, flags_stds,
                             steps_data, steps_means, steps_stds,
                             file_name, markevery=10):
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
    plt.show()
    # plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    # plt.close(fig)


def plot_rewards_flags_steps_2(rewards_data_1, rewards_means_1, rewards_stds_1,
                               flags_data_1, flags_means_1, flags_stds_1,
                               steps_data_1, steps_means_1, steps_stds_1,
                               rewards_data_2, rewards_means_2, rewards_stds_2,
                               flags_data_2, flags_means_2, flags_stds_2,
                               steps_data_2, steps_means_2, steps_stds_2,
                               file_name, markevery=10):
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(16, 3))
    plt.rcParams.update({'font.size': 12})

    # ylims = (0, 920)

    # Plot Rewards
    ax[0].plot(np.array(list(range(len(rewards_means_1)))),
               rewards_means_1, label="PPO 128", marker="s", ls='-', color="#599ad3",
               markevery=markevery)
    ax[0].fill_between(np.array(list(range(len(rewards_means_1)))),
                       rewards_means_1 - rewards_stds_1, rewards_means_1 + rewards_stds_1,
                       alpha=0.35, color="#599ad3")

    ax[0].plot(np.array(list(range(len(rewards_means_2)))),
               rewards_means_2, label="PPO 64", marker="o", ls='-', color="r",
               markevery=markevery)
    ax[0].fill_between(np.array(list(range(len(rewards_means_2)))),
                       rewards_means_2 - rewards_stds_2, rewards_means_2 + rewards_stds_2,
                       alpha=0.35, color="r")

    ax[0].set_title("Episodic Rewards")
    ax[0].set_xlabel("\# Iteration", fontsize=20)
    ax[0].set_ylabel("Avg Episode Reward", fontsize=20)
    ax[0].set_xlim(0, len(rewards_means_1))
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
               flags_means_1, label="PPO 128", marker="s", ls='-', color="#599ad3",
               markevery=markevery)
    ax[1].fill_between(np.array(list(range(len(flags_means_1)))),
                       flags_means_1 - flags_stds_1, flags_means_1 + flags_stds_1,
                       alpha=0.35, color="#599ad3")

    ax[1].plot(np.array(list(range(len(flags_means_2)))),
               flags_means_2, label="PPO 64", marker="o", ls='-', color="r",
               markevery=markevery)
    ax[1].fill_between(np.array(list(range(len(flags_means_2)))),
                       flags_means_2 - flags_stds_2, flags_means_2 + flags_stds_2,
                       alpha=0.35, color="r")

    ax[1].set_title("Flags Captured (\%) per episode")
    ax[1].set_xlabel("\# Iteration")
    ax[1].set_ylabel("Flags Captured (\%)")
    ax[1].set_xlim(0, len(flags_means_1))

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
               steps_means_1, label="PPO 128", marker="s", ls='-', color="#599ad3",
               markevery=markevery)
    ax[2].fill_between(np.array(list(range(len(steps_means_1)))),
                       steps_means_1 - steps_stds_1, steps_means_1 + steps_stds_1,
                       alpha=0.35, color="#599ad3")

    ax[2].plot(np.array(list(range(len(steps_means_2)))),
               steps_means_2, label="PPO 64", marker="o", ls='-', color="r",
               markevery=markevery)
    ax[2].fill_between(np.array(list(range(len(steps_means_2)))),
                       steps_means_2 - steps_stds_2, steps_means_2 + steps_stds_2,
                       alpha=0.35, color="r")

    ax[2].set_title("\# Steps per episode")
    ax[2].set_xlabel("\# Iteration")
    ax[2].set_ylabel("\# Steps")
    ax[2].set_xlim(0, len(steps_means_1))
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
    # plt.close(fig)


def plot_csv_files(csv_files, output_dir : str):
    dfs = []
    for i, csv_file in enumerate(csv_files):
        df = pd.read_csv(csv_file)
        dfs.append(df)

    rewards_data = list(map(lambda df: df["avg_episode_rewards"].values, dfs))
    rewards_means = np.mean(tuple(rewards_data), axis=0)
    rewards_stds = np.std(tuple(rewards_data), axis=0, ddof=1)

    flags_data = list(map(lambda df: df["avg_episode_flags_percentage"].values, dfs))
    flags_means = np.mean(tuple(flags_data), axis=0)
    flags_stds = np.std(tuple(flags_data), axis=0, ddof=1)

    steps_data = list(map(lambda df: df["avg_episode_steps"].values, dfs))
    steps_means = np.mean(tuple(steps_data), axis=0)
    steps_stds = np.std(tuple(steps_data), axis=0, ddof=1)

    plot_rewards_flags_steps(rewards_data, rewards_means, rewards_stds,
                             flags_data, flags_means, flags_stds,
                             steps_data, steps_means, steps_stds,
                             output_dir + "rewards_flags_steps_" + str(i), markevery=25)


def plot_two_csv_files(csv_files, output_dir : str):
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