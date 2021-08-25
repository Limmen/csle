from matplotlib.collections import PolyCollection
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
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


def get_trajectory(xlist, ylist):
    return [(xlist[0], 0.), *zip(xlist[1:-1], ylist[1:-1]), (xlist[-1], 0.)]

def plot():
    fontsize = 14
    labelsize = 12
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts,amsmath}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['axes.titlepad'] = 5
    plt.rcParams['xtick.major.pad'] = 0.05
    plt.rcParams['ytick.major.pad'] = 0.05
    plt.rcParams['axes.labelpad'] = 0.0
    plt.rcParams['axes.linewidth'] = 0.2
    plt.rcParams.update({'font.size': 6.5})
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams.update({'font.size': fontsize})
    plt.rcParams.update({'figure.autolayout': True})

    fig = plt.figure(figsize=(6, 4))
    ax = fig.gca(projection='3d')

    # ys_l, zs_l, zs_error_l = load_data()
    ys_l = []
    zs_l = []
    zs_error_l = []
    novice_results, experienced_results, expert_results = load_data()
    for i in range(len(novice_results)):
        stds, rewards, label, batch_size, neurons = novice_results[i]
        if neurons == 128 and batch_size != 2000:
            zs_l.append(rewards)
            zs_error_l.append(stds)
            ys_l.append(list(range(0, len(rewards))))
    print(len(ys_l))
    print(len(zs_l))
    # xs_l = [1000, 4000, 8000, 12000]
    xs_l = [12000, 8000, 4000, 1000]
    # for i in range(len(xs_l)):
    #     ys = np.linspace(start=0, stop=1000, num=100)
    #     zs = np.random.rand(len(ys))*150
    #     ys_l.append(ys)
    #     zs_l.append(zs)

    colors = ["#599ad3", "r", "#661D98", "#f9a65a","#E7298A", "black",
               "#377EB8", "#4DAF4A", "#A65628", "#F781BF",
              '#D95F02', '#7570B3', '#E6AB02', '#A6761D', '#666666',
              '#8DD3C7', '#CCEBC5', '#BEBADA','#FB8072', "#FF7F00", '#80B1D3', '#FDB462', '#B3DE69', '#FCCDE5',
              '#D9D9D9', '#BC80BD', '#FFED6F', "blue", "#984EA3", "green", "#FFFF33", '#66A61E', '#FFFFB3',
              "purple", "orange", "browen", "ppink", "#1B9E77", "#E41A1C"]
    # colors = plt.cm.viridis(np.linspace(0.3, 1, len(xs_l)))[-len(xs_l):]

    for i in range(0, len(xs_l), 1):
        ax.plot(xs=np.array(ys_l[i])*100, ys=np.maximum(-200, zs_l[i]), zs=xs_l[i], zdir='x',
                label='ys=0, zdir=z', color=colors[i], linewidth=2)
        # for j in range(0, len(ys_l[i]), 10):
        #     error = min(zs_error_l[i][j], 100)
        #     print(zs_l[i][j] + error)
        #     ax.plot(zs=[xs_l[i], xs_l[i]], xs=[ys_l[i][j]*100, ys_l[i][j]*100], ys=[max(0, zs_l[i][j] + error),
        #                                                                             max(0, zs_l[i][j] - error)],
        #             marker="_", color=colors[i], zdir='y',
        #              markersize=3, linewidth=1, alpha=0.85)

    ax.set_xlabel(r'batch size')
    ax.set_ylabel(r'\# policy updates')
    ax.set_zlabel('Reward')
    ax.set_xlim(1000, 12000)
    ax.set_ylim(0, 40000)
    ax.set_zlim(-200, 1000)

    ax.xaxis.labelpad = 5
    ax.yaxis.labelpad = 5
    ax.zaxis.labelpad = -5

    ax.yaxis.set_major_formatter(tick.FuncFormatter(reformat_large_tick_values))
    # ax.set_xticks(np.arange(-1, 4, 1))
    ax.set_yticks(np.arange(0, 40000, 10000))
    # ax.set_xticks(xs_l)
    xlab = ax.xaxis.get_label()
    ylab = ax.yaxis.get_label()
    zlab = ax.zaxis.get_label()
    xlab.set_size(fontsize)
    ylab.set_size(fontsize)
    zlab.set_size(fontsize)
    ax.tick_params(axis='both', which='major', labelsize=labelsize, length=2.2, width=0.6)
    ax.tick_params(axis='both', which='minor', labelsize=labelsize, length=2.2, width=0.6)

    fig.tight_layout()
    # plt.subplots_adjust(bottom=0.55)
    fig.savefig("hparam_tuning_2" + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)

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
