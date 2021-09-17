import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
from pycr_common.util.experiments_util import util

def parse_data():
    ppo_v1_df_0 = pd.read_csv(glob.glob("/home/kim/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_9/training/v5/generated_simulation/defender/ppo_baseline/results/data/0/1629455626.618311_train.csv")[0])
    # ppo_v1_df_71810 = pd.read_csv(glob.glob(base_path + "71810/*_train.csv")[0])
    # #ppo_v1_df_18910 = pd.read_csv(glob.glob(base_path + "18910/*_train.csv")[0])
    ppo_dfs_v1 = [ppo_v1_df_0]
    max_len = min(list(map(lambda x: len(x), ppo_dfs_v1)))

    running_avg = 10

    # Train avg
    defender_avg_train_rewards_data_v1 = list(
        map(lambda df: util.running_average_list(df["defender_avg_episode_rewards"].values[0:max_len], running_avg), ppo_dfs_v1))
    defender_avg_train_rewards_means_v1 = np.mean(tuple(defender_avg_train_rewards_data_v1), axis=0)
    defender_avg_train_rewards_stds_v1 = np.std(tuple(defender_avg_train_rewards_data_v1), axis=0, ddof=1)

    return defender_avg_train_rewards_data_v1, defender_avg_train_rewards_means_v1, defender_avg_train_rewards_stds_v1

def plot_train(defender_avg_train_rewards_data_v1, defender_avg_train_rewards_means_v1, defender_avg_train_rewards_stds_v1):

    print("plot")
    suffix = "gensim"
    ylim_rew = (-150, 170)
    max_iter = 275

    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams.update({'font.size': 10})
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 5))

    sample_step = 1
    markevery = 15
    iterations_per_step = 10
    file_name = "test_1"
    # ylims = (0, 920)

    ax.plot(np.array(list(range(len(defender_avg_train_rewards_means_v1[::sample_step])))) * sample_step* iterations_per_step,
            defender_avg_train_rewards_means_v1[::sample_step], label=r"$\pi_{\theta}$",
            marker="s", ls='-', color="r",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(defender_avg_train_rewards_means_v1[::sample_step])))) * sample_step * iterations_per_step,
                    defender_avg_train_rewards_means_v1[::sample_step] - defender_avg_train_rewards_stds_v1[::sample_step],
                    defender_avg_train_rewards_means_v1[::sample_step] + defender_avg_train_rewards_stds_v1[::sample_step],
                    alpha=0.35, color="r")

    ax.plot(np.array(list(range(len(defender_avg_train_rewards_means_v1[::sample_step])))) * iterations_per_step,
                  [160] * len(defender_avg_train_rewards_means_v1), label=r"upper bound",
                  color="black", linestyle="dashed", dashes=(4, 2))

    ax.set_title(r"Episodic rewards")
    ax.set_xlabel("\# Policy updates", fontsize=20)
    ax.set_ylabel("Avg Episode Rewards", fontsize=20)
    ax.set_xlim(0, len(defender_avg_train_rewards_means_v1[::sample_step]) * sample_step * iterations_per_step)
    # ax.set_ylim(ylim_rew[0], ylim_rew[1])
    # ax.set_ylim(ylim_rew)

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
    # ax.legend(loc="lower right")
    ax.xaxis.label.set_size(13.5)
    ax.yaxis.label.set_size(13.5)

    fig.tight_layout()
    plt.show()
    # plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    # plt.close(fig)



if __name__ == '__main__':
    base_path = "/home/kim/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_9/training/v5/generated_simulation/defender/ppo_baseline/results/data/"
    defender_avg_train_rewards_data_v1, defender_avg_train_rewards_means_v1, defender_avg_train_rewards_stds_v1 = parse_data()
    plot_train(defender_avg_train_rewards_data_v1, defender_avg_train_rewards_means_v1, defender_avg_train_rewards_stds_v1)


