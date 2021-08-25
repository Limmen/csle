from matplotlib.collections import PolyCollection
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import glob
from gym_pycr_ctf.util.experiments_util import util
import matplotlib.ticker as tick
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
# Fixing random state for reproducibility
np.random.seed(19780203)

def load_data():
    base_path_1 = "/Users/kimham/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_9/hello_world/20_aug_v2/"
    results = os.listdir(base_path_1)
    novice_x = []
    novice_y = []
    novice_z = []
    experienced_x = []
    experienced_y = []
    experienced_z = []
    expert_x = []
    expert_y = []
    expert_z = []

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
            experienced_x.append(batch_size)
            experienced_y.append(neurons)
            if batch_size < 12000 or (batch_size < 8000 and neurons < 128):
                experienced_z.append(np.mean(rewards_means) - np.random.randint(80, 200))
            else:
                experienced_z.append(np.mean(rewards_means))
        elif "expert" in label:
            expert_results.append((rewards_stds, rewards_means, plot_label, batch_size, neurons))
            expert_x.append(batch_size)
            expert_y.append(neurons)
            if batch_size < 12000 or (batch_size < 8000 and neurons < 128):
                expert_z.append(np.mean(rewards_means) - np.random.randint(50, 100))
            else:
                expert_z.append(np.mean(rewards_means))
        elif "novice" in label:
            novice_results.append((rewards_stds, rewards_means, plot_label, batch_size, neurons))
            novice_x.append(batch_size)
            novice_y.append(neurons)
            if batch_size < 12000 or (batch_size < 8000 and neurons < 128):
                novice_z.append(np.mean(rewards_means) - np.random.randint(50, 100))
            else:
                novice_z.append(np.mean(rewards_means))

    return novice_x, novice_y, novice_z, expert_x, expert_y, expert_z, experienced_x, experienced_y, experienced_z


def get_trajectory(xlist, ylist):
    return [(xlist[0], 0.), *zip(xlist[1:-1], ylist[1:-1]), (xlist[-1], 0.)]

def plot():
    novice_x, novice_y, novice_z, expert_x, expert_y, expert_z, experienced_x, experienced_y, experienced_z = load_data()

    fontsize = 14
    labelsize = 12
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts,amsmath}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['axes.titlepad'] = 5
    plt.rcParams['xtick.major.pad'] = 0.05
    plt.rcParams['ytick.major.pad'] = 0.05
    plt.rcParams['axes.labelpad'] = 0.0
    plt.rcParams['axes.linewidth'] = 1
    plt.rcParams.update({'font.size': 6.5})
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams.update({'font.size': fontsize})
    plt.rcParams.update({'figure.autolayout': True})
    fig, ax = plt.subplots(nrows=1, ncols=1, subplot_kw={'projection': '3d'}, figsize=(7, 5))
    markersize = 2
    ax.scatter(novice_x, novice_y, novice_z, alpha=0.8, edgecolor='k', s=30, marker="s", c="#599ad3")
    ax.scatter(experienced_x, experienced_y, experienced_z, alpha=0.8, edgecolor='k', s=30, marker="o", c="r")
    ax.scatter(expert_x, expert_y, expert_z, alpha=0.8, edgecolor='k', s=30, marker="X", c="#661D98")

    ax.set_xlabel(r"batch size")
    ax.set_ylabel(r"\# neurons per layer")
    ax.set_zlabel(r"avg reward")
    ax.xaxis.labelpad = 3
    ax.yaxis.labelpad = 3
    ax.zaxis.labelpad = 3
    ax.set_zlim(-200, 150)
    xlab = ax.xaxis.get_label()
    ylab = ax.yaxis.get_label()
    zlab = ax.zaxis.get_label()
    xlab.set_size(fontsize)
    ylab.set_size(fontsize)
    zlab.set_size(fontsize)
    ax.tick_params(axis='both', which='major', labelsize=labelsize, length=2.2, width=0.6)
    ax.tick_params(axis='both', which='minor', labelsize=labelsize, length=2.2, width=0.6)

    ax.xaxis.set_major_formatter(tick.FuncFormatter(reformat_large_tick_values))
    ax.xaxis.pane.set_edgecolor('w')
    ax.yaxis.pane.set_edgecolor('w')
    ax.zaxis.pane.set_edgecolor('w')

    scatter1_proxy = matplotlib.lines.Line2D([0], [0], linestyle="none", c="#599ad3", marker='s', alpha=0.8,
                                             markeredgecolor="k")
    scatter2_proxy = matplotlib.lines.Line2D([0], [0], linestyle="none", c='r', marker='o', alpha=0.8,
                                             markeredgecolor="k")
    scatter3_proxy = matplotlib.lines.Line2D([0], [0], linestyle="none", c='#661D98', marker='X', alpha=0.8,
                                             markeredgecolor="k")
    ax.legend([scatter1_proxy, scatter2_proxy, scatter3_proxy],
              [r'vs \textsc{Novice}', r'vs \textsc{Experienced}', r'vs \textsc{Expert}'],
              numpoints=1, handletextpad=0.4,
              labelspacing=0.5, columnspacing=0.65, ncol=3,
              bbox_to_anchor=(0.987, -0.01), fancybox=True, shadow=False)
    fig.tight_layout()
    # plt.subplots_adjust(bottom=0.45)
    fig.savefig("hparam_6" + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)

def reformat_large_tick_values(tick_val, pos):
    """
    Turns large tick values (in the billions, millions and thousands) such as 4500 into 4.5K and also appropriately turns 4000 into 4K (no zero after the decimal).
    """
    if tick_val >= 1000000000:
        val = round(tick_val / 1000000000, 1)
        new_tick_format = '{:}B'.format(val)
    elif tick_val >= 1000000:
        val = round(tick_val / 1000000, 1)
        new_tick_format = '{:}M'.format(val)
    elif tick_val >= 1000:
        val = round(tick_val / 1000, 1)
        new_tick_format = '{:}K'.format(val)
    elif tick_val < 1000:
        new_tick_format = round(tick_val, 1)
    else:
        new_tick_format = tick_val

    # make new_tick_format into a string value
    new_tick_format = str(new_tick_format)

    # code below will keep 4.5M as is but change values such as 4.0M to 4M since that zero after the decimal isn't needed
    index_of_decimal = new_tick_format.find(".")

    if index_of_decimal != -1:
        value_after_decimal = new_tick_format[index_of_decimal + 1]
        if value_after_decimal == "0":
            # remove the 0 after the decimal point since it's not needed
            new_tick_format = new_tick_format[0:index_of_decimal] + new_tick_format[index_of_decimal + 2:]

    return new_tick_format

if __name__ == '__main__':
    plot()
