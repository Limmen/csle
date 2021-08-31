import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.stats import geom

def plot_geo_only() -> None:
    """
    Plots the thresholds
    :return: None
    """
    times = np.arange(1, 101, 1)
    intrusion_idx = 29
    continue_rew = 10
    stopping_rew = 200
    intrusion_rew = -100
    early_stopping_rew = -100
    stopping_costs = [-100, -50, -25, -12.5, 0]
    stops_remaining = 4
    stopping_reward_lt_4 = []
    continue_reward_lt_4 = []
    stopping_reward_lt_3 = []
    continue_reward_lt_3 = []
    stopping_reward_lt_2 = []
    continue_reward_lt_2 = []
    stopping_reward_lt_1 = []
    continue_reward_lt_1 = []

    stopping_time_y_lt_4 = []
    stopping_time_y_lt_3 = []
    stopping_time_y_lt_2 = []
    stopping_time_y_lt_1 = []
    temp_lt_4 = -110
    temp_lt_3 = -110
    temp_lt_2 = -110
    temp_lt_1 = -110
    for i in range(len(times)):
        if i <= intrusion_idx:
            continue_reward_lt_4.append(continue_rew/(math.pow(2, 0)))
            continue_reward_lt_3.append(continue_rew / (math.pow(2, 1)))
            continue_reward_lt_2.append(continue_rew / (math.pow(2, 2)))
            continue_reward_lt_1.append(continue_rew / (math.pow(2, 3)))
            stopping_reward_lt_4.append(stopping_costs[4])
            stopping_reward_lt_3.append(stopping_costs[3])
            stopping_reward_lt_2.append(stopping_costs[2])
            stopping_reward_lt_1.append(stopping_costs[1])
        else:
            stopping_reward_lt_4.append(stopping_costs[4])
            stopping_reward_lt_3.append(stopping_costs[3])
            stopping_reward_lt_2.append(stopping_costs[2] + stopping_rew)
            stopping_reward_lt_1.append(stopping_costs[1])
            continue_reward_lt_4.append(continue_rew / (math.pow(2, 0)) + intrusion_rew)
            continue_reward_lt_3.append(continue_rew / (math.pow(2, 1)) + intrusion_rew)
            continue_reward_lt_2.append(continue_rew / (math.pow(2, 2))+ intrusion_rew)
            continue_reward_lt_1.append(continue_rew / (math.pow(2, 3)))

        temp_lt_4 = temp_lt_4 + 310/ len(times)
        stopping_time_y_lt_4.append(temp_lt_4)

        temp_lt_3 = temp_lt_4 + 310 / len(times)
        stopping_time_y_lt_3.append(temp_lt_3)

        temp_lt_2 = temp_lt_4 + 310 / len(times)
        stopping_time_y_lt_2.append(temp_lt_2)

        temp_lt_1 = temp_lt_4 + 310 / len(times)
        stopping_time_y_lt_1.append(temp_lt_1)

    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts,amsmath}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['axes.titlepad'] = 0.02
    # plt.rcParams['xtick.major.pad'] = 0.5
    plt.rcParams['ytick.major.pad'] = 0.05
    plt.rcParams['axes.labelpad'] = 0.8
    plt.rcParams['axes.linewidth'] = 0.8
    fontsize=16.5
    labelsize=15
    # plt.rcParams.update({'font.size': 10})

    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(8, 6))

    ax[0][0].plot(times,
               stopping_reward_lt_4, label=r"Stop reward",
               ls='-', color="#E7298A", marker="s", markevery=5, markersize=4.5, linewidth=2.0)
    ax[0][0].plot(times,
               continue_reward_lt_4, label=r"Continue reward",
               ls='-', color="#661D98", marker="d", markevery=5, markersize=4.5, linewidth=2.0)
    ax[0][0].plot([intrusion_idx] * len(times),
               stopping_time_y_lt_4, label=r"Intrusion starts",
               color="black", linestyle="dashed", linewidth=2.0)

    # set the grid on
    # ax[0][0].grid('on')

    ax[0][0].set_title(r"$r(s_t, a_t)$, $l_t=4$", fontsize=fontsize)
    #ax[0][0].set_xlabel(r"time-step $t$", fontsize=fontsize)
    #ax.set_ylabel(r"$r(s_t, i)$", fontsize=fontsize)

    ax[0][0].axhline(y=0, color='k', linewidth=0.5)
    ax[0][0].set_xlim(1, 101)
    ax[0][0].set_ylim(-110, 200)

    a = ax[0][0].get_xticks().tolist()
    a[-2] = r'$100$'
    # ax[0][0].set_xticks([1, 20, 40, 60, 80, 100])
    ax[0][0].set_xticks([])

    # tweak the axis labels
    xlab = ax[0][0].xaxis.get_label()
    ylab = ax[0][0].yaxis.get_label()

    xlab.set_size(fontsize)
    ylab.set_size(fontsize)

    # change the color of the top and right spines to opaque gray
    ax[0][0].spines['right'].set_color((.8, .8, .8))
    ax[0][0].spines['top'].set_color((.8, .8, .8))

    ax[0][0].tick_params(axis='both', which='major', labelsize=labelsize, length=2.2, width=0.6)
    ax[0][0].tick_params(axis='both', which='minor', labelsize=labelsize, length=2.2, width=0.6)

    # a1

    ax[0][1].plot(times,
                  stopping_reward_lt_3, label=r"Stop reward",
                  ls='-', color="#E7298A", marker="s", markevery=5, markersize=4.5, linewidth=2.0)
    ax[0][1].plot(times,
                  continue_reward_lt_3, label=r"Continue reward",
                  ls='-', color="#661D98", marker="d", markevery=5, markersize=4.5, linewidth=2.0)
    ax[0][1].plot([intrusion_idx] * len(times),
                  stopping_time_y_lt_3, label=r"Intrusion starts",
                  color="black", linestyle="dashed", linewidth=2.0)

    # set the grid on
    # ax[0][1].grid('on')

    ax[0][1].set_title(r"$r(s_t, a_t)$, $l_t=3$", fontsize=fontsize)
    #ax[0][1].set_xlabel(r"time-step $t$", fontsize=fontsize)
    # ax.set_ylabel(r"$r(s_t, i)$", fontsize=fontsize)

    ax[0][1].axhline(y=0, color='k', linewidth=0.5)
    ax[0][1].set_xlim(1, 101)
    ax[0][1].set_ylim(-110, 200)

    a = ax[0][1].get_xticks().tolist()
    a[-2] = r'$100$'
    # ax[0][1].set_xticks([1, 20, 40, 60, 80, 100])
    ax[0][1].set_xticks([])
    ax[0][1].set_yticks([])

    # tweak the axis labels
    xlab = ax[0][1].xaxis.get_label()
    ylab = ax[0][1].yaxis.get_label()

    xlab.set_size(fontsize)
    ylab.set_size(fontsize)

    # change the color of the top and right spines to opaque gray
    ax[0][1].spines['right'].set_color((.8, .8, .8))
    ax[0][1].spines['top'].set_color((.8, .8, .8))

    ax[0][1].tick_params(axis='both', which='major', labelsize=labelsize, length=2.2, width=0.6)
    ax[0][1].tick_params(axis='both', which='minor', labelsize=labelsize, length=2.2, width=0.6)

    # a2

    ax[1][0].plot(times,
                  stopping_reward_lt_2, label=r"Stop reward",
                  ls='-', color="#E7298A", marker="s", markevery=5, markersize=4.5, linewidth=2.0)
    ax[1][0].plot(times,
                  continue_reward_lt_2, label=r"Continue reward",
                  ls='-', color="#661D98", marker="d", markevery=5, markersize=4.5, linewidth=2.0)
    ax[1][0].plot([intrusion_idx] * len(times),
                  stopping_time_y_lt_2, label=r"Intrusion starts",
                  color="black", linestyle="dashed", linewidth=2.0)

    # set the grid on
    # ax[1][0].grid('on')

    ax[1][0].set_title(r"$r(s_t, a_t)$, $l_t=2$", fontsize=fontsize)
    ax[1][0].set_xlabel(r"time-step $t$", fontsize=fontsize)
    # ax.set_ylabel(r"$r(s_t, i)$", fontsize=fontsize)

    ax[1][0].axhline(y=0, color='k', linewidth=0.5)
    ax[1][0].set_xlim(1, 101)
    ax[1][0].set_ylim(-110, 200)

    a = ax[1][0].get_xticks().tolist()
    a[-2] = r'$100$'
    ax[1][0].set_xticks([1, 20, 40, 60, 80, 100])

    # tweak the axis labels
    xlab = ax[1][0].xaxis.get_label()
    ylab = ax[1][0].yaxis.get_label()

    xlab.set_size(fontsize)
    ylab.set_size(fontsize)

    # change the color of the top and right spines to opaque gray
    ax[1][0].spines['right'].set_color((.8, .8, .8))
    ax[1][0].spines['top'].set_color((.8, .8, .8))

    ax[1][0].tick_params(axis='both', which='major', labelsize=labelsize, length=2.2, width=0.6)
    ax[1][0].tick_params(axis='both', which='minor', labelsize=labelsize, length=2.2, width=0.6)

    # a3

    ax[1][1].plot(times,
                  stopping_reward_lt_1, label=r"Stop reward",
                  ls='-', color="#E7298A", marker="s", markevery=5, markersize=4.5, linewidth=2.0)
    ax[1][1].plot(times,
                  continue_reward_lt_1, label=r"Continue reward",
                  ls='-', color="#661D98", marker="d", markevery=5, markersize=4.5, linewidth=2.0)
    ax[1][1].plot([intrusion_idx] * len(times),
                  stopping_time_y_lt_1, label=r"Intrusion starts",
                  color="black", linestyle="dashed", linewidth=2.0)

    # set the grid on
    # ax[1][1].grid('on')

    ax[1][1].set_title(r"$r(s_t, a_t)$, $l_t=1$", fontsize=fontsize)
    ax[1][1].set_xlabel(r"time-step $t$", fontsize=fontsize)
    # ax.set_ylabel(r"$r(s_t, i)$", fontsize=fontsize)

    ax[1][1].axhline(y=0, color='k', linewidth=0.5)
    ax[1][1].set_xlim(1, 101)
    ax[1][1].set_ylim(-110, 200)

    a = ax[1][1].get_xticks().tolist()
    a[-2] = r'$100$'
    ax[1][1].set_xticks([1, 20, 40, 60, 80, 100])
    ax[1][1].set_yticks([])

    # tweak the axis labels
    xlab = ax[1][1].xaxis.get_label()
    ylab = ax[1][1].yaxis.get_label()

    xlab.set_size(fontsize)
    ylab.set_size(fontsize)

    # change the color of the top and right spines to opaque gray
    ax[1][1].spines['right'].set_color((.8, .8, .8))
    ax[1][1].spines['top'].set_color((.8, .8, .8))

    ax[1][1].tick_params(axis='both', which='major', labelsize=labelsize, length=2.2, width=0.6)
    ax[1][1].tick_params(axis='both', which='minor', labelsize=labelsize, length=2.2, width=0.6)

    # ttl = ax.title
    # ttl.set_position([.5, 1.05])
    handles, labels = ax[1][1].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.505, 0.089),
               ncol=5, fancybox=True, shadow=False, handletextpad=0.4, labelspacing=0.5, columnspacing=0.65,
               fontsize=fontsize)

    fig.tight_layout()
    plt.subplots_adjust(wspace=0.05, hspace=0.14, bottom=0.14)

    # plt.show()
    # plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig("reward_fun_multistop" + ".png", format="png", dpi=600)
    fig.savefig("reward_fun_multistop" + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    # plt.close(fig)

if __name__ == '__main__':
    plot_geo_only()
