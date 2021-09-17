from pycr_common.agents.policy_gradient.ppo_baseline.impl.ppo.ppo import PPO
import torch
import numpy as np
import gym
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import os

def plot_quickest_detection() -> None:
    fontsize = 7.5
    # figsize = (7.5, 3.25)
    figsize = (3.5, 1.6)
    title_fontsize = 8
    wspace = 0.05
    hspace = 0.2
    markevery = 1
    labelsize = 7
    sample_step = 5
    markersize = 2.25
    file_name = "threshold_alerts_multiple_steps"
    bottom = 0.15
    lw = 1.0

    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts,amsmath}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['axes.titlepad'] = 0.02
    # plt.rcParams['xtick.major.pad'] = 0.5
    plt.rcParams['ytick.major.pad'] = 0.05
    plt.rcParams['axes.labelpad'] = 0.8
    plt.rcParams['axes.linewidth'] = 0.2
    plt.rcParams.update({'font.size': fontsize})

    x = list(range(1,10))
    y = [0, 0, 3, 7, 7, 45, 45, 71, 77]

    temp = [0, 9.6, 9.6*2, 9.6*3, 9.6*4, 9.6*5, 9.6*6, 9.6*7, 9.6*8]

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)

    # Plot Avg Eval rewards Gensim
    colors = plt.cm.viridis(np.linspace(0.3, 1, 2))[-2:]
    ax.plot(x,
            y, label=r"$x+y$",
            ls='-', color=colors[0], alpha=0.75, markersize=3, marker="p", markevery=1, lw=lw)

    # if plot_opt:
    ax.plot(x, [30] * 9, color="black", lw=lw, label=r"$x+y=30$")

    ax.plot([5] * len(x), temp, color="black", linestyle="dashed", lw=lw, label="intrusion start")

    ax.set_title(r"Threshold-based Stopping Policy", fontsize=fontsize)
    ax.set_xlabel(r"$t$", fontsize=labelsize)
    ax.set_xlim(1, 9)
    ax.set_ylim(0, 77)
    # ax.set_ylim(0, 1.1)

    # set the grid on
    ax.grid('on')

    # tweak the axis labels
    xlab = ax.xaxis.get_label()
    ylab = ax.yaxis.get_label()

    xlab.set_size(labelsize)
    ylab.set_size(labelsize)

    # change the color of the top and right spines to opaque gray
    ax.spines['right'].set_color((.8, .8, .8))
    ax.spines['top'].set_color((.8, .8, .8))

    # ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.18),
    #           ncol=2, fancybox=True, shadow=True, fontsize=13.5)
    # ax.legend(loc="lower right", fontsize=12)
    ax.legend(loc='upper left',
              ncol=1, fancybox=False, shadow=False, fontsize=fontsize)

    ttl = ax.title
    ttl.set_position([.5, 1.05])

    ax.tick_params(axis='both', which='major', labelsize=labelsize, length=2.2, width=0.6)
    ax.tick_params(axis='both', which='minor', labelsize=labelsize, length=2.2, width=0.6)

    fig.tight_layout()
    # plt.show()
    plt.subplots_adjust(wspace=0, hspace=0, bottom=0.2)
    fig.savefig("quickest_detection" + ".png", format="png", dpi=600)
    fig.savefig("quickest_detection" + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    # plt.close(fig)

if __name__ == '__main__':
    plot_quickest_detection()