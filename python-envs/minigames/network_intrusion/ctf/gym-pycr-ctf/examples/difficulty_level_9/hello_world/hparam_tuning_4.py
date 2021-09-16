import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob
from gym_pycr_ctf.util.experiments_util import util
import matplotlib.ticker as tick
import os
# Fixing random state for reproducibility
np.random.seed(19780203)


def load_data():
    base_path_1 = "/Users/kimham/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_9/hello_world/20_aug_v2/"
    results = os.listdir(base_path_1)
    expert_results = []
    novice_results = []
    experienced_results = []
    for r in results:
        label = r
        attacker = "vs \textsc{Novice}"
        if "experienced" in label:
            attacker = "vs \textsc{Experienced}"
        elif "expert" in label:
            attacker = "vs \textsc{Expert}"
        batch_size = 12000
        batch_label = "B=12K"
        if "8k" in label:
            batch_size = 8000
            batch_label = "B=8K"

        if "4k" in label:
            batch_size = 4000
            batch_label = "B=4K"

        if "1k" in label:
            batch_size = 1000
            batch_label = "B=1K"

        neurons= 128
        neurons_label = "N=128"

        if "64" in label:
            neurons = 64
            neurons_label = "N=64"

        if "128" in label:
            neurons = 128
            neurons_label = "N=128"

        if "32" in label:
            neurons = 32
            neurons_label = "N=32"

        plot_label = batch_label + "," + neurons_label
        d_0 = pd.read_csv(glob.glob(base_path_1 + label + "/data/" + "0/*_train.csv")[0])
        d_399 = pd.read_csv(glob.glob(base_path_1 + label + "/data/"+ "399/*_train.csv")[0])
        d_999 = pd.read_csv(glob.glob(base_path_1 + label + "/data/" "999/*_train.csv")[0])
        dfs = [d_0, d_399, d_999]
        max_len = min(list(map(lambda x: len(x), dfs)))

        running_avg = 1
        confidence = 0.95
        num_seeds = len(dfs)

        # Train Avg Novice
        rewards_data = list(
            map(lambda df: util.running_average_list(df["defender_avg_episode_rewards"].values[0:max_len], running_avg),
                dfs))

        rewards_data = np.array(rewards_data).reshape(max_len,
                                                                                                          num_seeds)
        rewards_stds = np.array(list(
            map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[1],
                rewards_data)))
        rewards_means = np.array(list(
            map(lambda x: util.mean_confidence_interval(data=x, confidence=confidence)[0],
                rewards_data)))

        if "experienced" in label:
            experienced_results.append((rewards_stds, rewards_means, plot_label, batch_size, neurons))
        elif "expert" in label:
            expert_results.append((rewards_stds, rewards_means, plot_label, batch_size, neurons))
        elif "novice" in label:
            novice_results.append((rewards_stds, rewards_means, plot_label, batch_size, neurons))

    return novice_results, experienced_results, expert_results


def plot(results,
        fontsize : int = 6.5, figsize =  (3.75, 3.4),
        title_fontsize=8, lw=0.5, wspace=0.02, hspace=0.3, top=0.9,
        labelsize=6, markevery=10, optimal_reward = 95, sample_step = 1,
        eval_only=False, plot_opt = False, iterations_per_step : int = 1, optimal_int = 1.0,
        optimal_flag = 1.0, file_name = "test", markersize=5, bottom=0.02):

    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts,amsmath}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['axes.titlepad'] = 0.02
    # plt.rcParams['xtick.major.pad'] = 0.5
    plt.rcParams['ytick.major.pad'] = 0.05
    plt.rcParams['axes.labelpad'] = 0.8
    plt.rcParams['axes.linewidth'] = 0.1
    plt.rcParams.update({'font.size': fontsize})

    # plt.rcParams['font.serif'] = ['Times New Roman']
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    lw = 0.75
    colors = plt.cm.viridis(np.linspace(0.3, 1, len(results)))[-len(results):]
    markers = ["p", "^", "*", "+", "v", "1", "2", "3", "4", "x", "p", "h", "H", "d", "|", ",", ".", "H", "X", "s", "8",
               ">", "<", "P", "D", 0, 1, 2]

    for i in range(len(results)):
        stds, rewards, label, batch_size, neurons = results[i]
        ax.plot(
            np.array(list(range(
                len(rewards[::sample_step])))) * sample_step * iterations_per_step,
            rewards[::sample_step], label=r"" + label,
            marker=markers[i], ls='-', color=colors[i], markevery=markevery, markersize=markersize, lw=lw)
        ax.fill_between(
            np.array(list(range(
                len(rewards[::sample_step])))) * sample_step * iterations_per_step,
            rewards[::sample_step] - stds[::sample_step],
            rewards[::sample_step] + stds[::sample_step], alpha=0.35, color=colors[i], lw=lw)

    ax.grid('on')
    # ax[0][0].set_xlabel("", fontsize=labelsize)
    # ax[0][0].set_ylabel(r"\% Flags captured", fontsize=labelsize)
    ax.set_xlabel(r"\# training episodes", fontsize=labelsize)
    xlab = ax.xaxis.get_label()
    ylab = ax.yaxis.get_label()
    xlab.set_size(labelsize)
    ylab.set_size(fontsize)
    ax.tick_params(axis='both', which='major', labelsize=labelsize, length=2.2, width=0.6)
    ax.tick_params(axis='both', which='minor', labelsize=labelsize, length=2.2, width=0.6)
    ax.set_ylim(-500, 150)
    ax.set_xlim(0, 40000)
    ax.set_title(r"Reward per episode", fontsize=fontsize)
    ax.xaxis.set_major_formatter(tick.FuncFormatter(reformat_large_tick_values))

    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.505, 0.165),
               ncol=4, fancybox=True, shadow=False, handletextpad=0.4, labelspacing=0.5, columnspacing=0.65)

    fig.tight_layout()
    #fig.subplots_adjust(wspace=wspace, hspace=hspace, top=top, bottom=bottom)
    fig.subplots_adjust(wspace=wspace, hspace=hspace, bottom=bottom)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)


if __name__ == '__main__':
    novice_results, experienced_results, expert_results = load_data()
    figsize = (4.1, 2.9)
    plot(novice_results,
         wspace=0.17, hspace=0.4, top=0.0, fontsize=6.5, figsize=figsize, title_fontsize=8,
         bottom=0.28, labelsize=6, markevery=1, optimal_reward=100, sample_step=5,
         eval_only=False, plot_opt=False, iterations_per_step=100, optimal_int=1.0,
         file_name="hparam_tuning_5", markersize=2.25
         )
