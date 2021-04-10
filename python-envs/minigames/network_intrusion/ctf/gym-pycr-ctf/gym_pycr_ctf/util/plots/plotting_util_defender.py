"""
Utility functions for plotting training results
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_rewards_defender(
        avg_train_rewards_data_v1, avg_train_rewards_means_v1, avg_train_rewards_stds_v1,
        avg_eval_2_rewards_data_v1, avg_eval_2_rewards_means_v1, avg_eval_2_rewards_stds_v1,
        avg_train_snort_severe_baseline_data_v1, avg_train_snort_severe_baseline_means_v1, avg_train_snort_severe_baseline_stds_v1,
        avg_train_snort_warning_baseline_data_v1, avg_train_snort_warning_baseline_means_v1, avg_train_snort_warning_baseline_stds_v1,
        avg_train_snort_critical_baseline_data_v1, avg_train_snort_critical_baseline_means_v1, avg_train_snort_critical_baseline_stds_v1,
        avg_train_var_log_baseline_data_v1, avg_train_var_log_baseline_means_v1, avg_train_var_log_baseline_stds_v1,
        avg_eval_snort_severe_baseline_data_v1, avg_eval_snort_severe_baseline_means_v1, avg_eval_snort_severe_baseline_stds_v1,
        avg_eval_snort_warning_baseline_data_v1, avg_eval_snort_warning_baseline_means_v1, avg_eval_snort_warning_baseline_stds_v1,
        avg_eval_snort_critical_baseline_data_v1, avg_eval_snort_critical_baseline_means_v1, avg_eval_snort_critical_baseline_stds_v1,
        avg_eval_var_log_baseline_data_v1, avg_eval_var_log_baseline_means_v1, avg_eval_var_log_baseline_stds_v1,

        ylim_rew, file_name, markevery=10, optimal_reward = 95, sample_step = 1,
        eval_only=False, plot_opt = False):
    """
    Plots rewards, flags % and rewards of two different configurations
    """
    #matplotlib.style.use("seaborn")
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams.update({'font.size': 10})
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 5))

    # ylims = (0, 920)

    # Plot Avg Eval rewards Gensim
    ax.plot(np.array(list(range(len(avg_train_rewards_means_v1[::sample_step]))))*sample_step,
            avg_train_rewards_means_v1[::sample_step], label=r"$\pi_{\theta}$ simulation",
            marker="s", ls='-', color="r",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(avg_train_rewards_means_v1[::sample_step]))))*sample_step,
                    avg_train_rewards_means_v1[::sample_step] - avg_train_rewards_stds_v1[::sample_step],
                    avg_train_rewards_means_v1[::sample_step] + avg_train_rewards_stds_v1[::sample_step],
                    alpha=0.35, color="r")


    ax.plot(np.array(list(range(len(avg_eval_2_rewards_means_v1[::sample_step])))) * sample_step,
            avg_eval_2_rewards_means_v1[::sample_step], label=r"$\pi_{\theta}$ emulation",
            marker="p", ls='-', color="#599ad3",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(avg_eval_2_rewards_means_v1[::sample_step])))) * sample_step,
                    avg_eval_2_rewards_means_v1[::sample_step] - avg_eval_2_rewards_stds_v1[::sample_step],
                    avg_eval_2_rewards_means_v1[::sample_step] + avg_eval_2_rewards_stds_v1[::sample_step],
                    alpha=0.35, color="#599ad3")

    ax.plot(np.array(list(range(len(avg_train_snort_severe_baseline_means_v1[::sample_step])))) * sample_step,
            avg_train_snort_severe_baseline_means_v1[::sample_step], label=r"Snort-Severe simulation",
            marker="p", ls='-', color="#f9a65a",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(avg_train_snort_severe_baseline_means_v1[::sample_step])))) * sample_step,
                    avg_train_snort_severe_baseline_means_v1[::sample_step] - avg_train_snort_severe_baseline_stds_v1[::sample_step],
                    avg_train_snort_severe_baseline_means_v1[::sample_step] + avg_train_snort_severe_baseline_stds_v1[::sample_step],
                    alpha=0.35, color="#f9a65a")

    ax.plot(np.array(list(range(len(avg_train_snort_warning_baseline_means_v1[::sample_step])))) * sample_step,
            avg_train_snort_warning_baseline_means_v1[::sample_step], label=r"Snort-warning simulation",
            marker="p", ls='-', color="#661D98",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(avg_train_snort_warning_baseline_means_v1[::sample_step])))) * sample_step,
                    avg_train_snort_warning_baseline_means_v1[::sample_step] - avg_train_snort_warning_baseline_stds_v1[
                                                                              ::sample_step],
                    avg_train_snort_warning_baseline_means_v1[::sample_step] + avg_train_snort_warning_baseline_stds_v1[
                                                                              ::sample_step],
                    alpha=0.35, color="#661D98")

    ax.plot(np.array(list(range(len(avg_train_snort_critical_baseline_means_v1[::sample_step])))) * sample_step,
            avg_train_snort_critical_baseline_means_v1[::sample_step], label=r"Snort-critical simulation",
            marker="p", ls='-', color="#4DAF4A",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(avg_train_snort_critical_baseline_means_v1[::sample_step])))) * sample_step,
                    avg_train_snort_critical_baseline_means_v1[::sample_step] - avg_train_snort_critical_baseline_stds_v1[
                                                                               ::sample_step],
                    avg_train_snort_critical_baseline_means_v1[::sample_step] + avg_train_snort_critical_baseline_stds_v1[
                                                                               ::sample_step],
                    alpha=0.35, color="#4DAF4A")

    ax.plot(np.array(list(range(len(avg_train_var_log_baseline_means_v1[::sample_step])))) * sample_step,
            avg_train_var_log_baseline_means_v1[::sample_step], label=r"/var/log/auth simulation",
            marker="p", ls='-', color="#1B9E77",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(avg_train_var_log_baseline_means_v1[::sample_step])))) * sample_step,
                    avg_train_var_log_baseline_means_v1[
                    ::sample_step] - avg_train_var_log_baseline_stds_v1[
                                     ::sample_step],
                    avg_train_var_log_baseline_means_v1[
                    ::sample_step] + avg_train_var_log_baseline_stds_v1[
                                     ::sample_step],
                    alpha=0.35, color="#1B9E77")



    # Baselines eval

    ax.plot(np.array(list(range(len(avg_eval_snort_severe_baseline_means_v1[::sample_step])))) * sample_step,
            avg_eval_snort_severe_baseline_means_v1[::sample_step], label=r"Snort-Severe emulation",
            marker="p", ls='-', color="brown",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(avg_eval_snort_severe_baseline_means_v1[::sample_step])))) * sample_step,
                    avg_eval_snort_severe_baseline_means_v1[::sample_step] - avg_eval_snort_severe_baseline_stds_v1[
                                                                              ::sample_step],
                    avg_eval_snort_severe_baseline_means_v1[::sample_step] + avg_eval_snort_severe_baseline_stds_v1[
                                                                              ::sample_step],
                    alpha=0.35, color="brown")

    ax.plot(np.array(list(range(len(avg_eval_snort_warning_baseline_means_v1[::sample_step])))) * sample_step,
            avg_eval_snort_warning_baseline_means_v1[::sample_step], label=r"Snort-warning emulation",
            marker="p", ls='-', color="#FDB462",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(avg_eval_snort_warning_baseline_means_v1[::sample_step])))) * sample_step,
                    avg_eval_snort_warning_baseline_means_v1[::sample_step] - avg_eval_snort_warning_baseline_stds_v1[
                                                                               ::sample_step],
                    avg_eval_snort_warning_baseline_means_v1[::sample_step] + avg_eval_snort_warning_baseline_stds_v1[
                                                                               ::sample_step],
                    alpha=0.35, color="#FDB462")

    ax.plot(np.array(list(range(len(avg_eval_snort_critical_baseline_means_v1[::sample_step])))) * sample_step,
            avg_eval_snort_critical_baseline_means_v1[::sample_step], label=r"Snort-critical emulation",
            marker="p", ls='-', color="#B3DE69",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(avg_eval_snort_critical_baseline_means_v1[::sample_step])))) * sample_step,
                    avg_eval_snort_critical_baseline_means_v1[
                    ::sample_step] - avg_eval_snort_critical_baseline_stds_v1[
                                     ::sample_step],
                    avg_eval_snort_critical_baseline_means_v1[
                    ::sample_step] + avg_eval_snort_critical_baseline_stds_v1[
                                     ::sample_step],
                    alpha=0.35, color="#B3DE69")

    ax.plot(np.array(list(range(len(avg_eval_var_log_baseline_means_v1[::sample_step])))) * sample_step,
            avg_eval_var_log_baseline_means_v1[::sample_step], label=r"/var/log/auth emulation",
            marker="p", ls='-', color="#66A61E",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(avg_eval_var_log_baseline_means_v1[::sample_step])))) * sample_step,
                    avg_eval_var_log_baseline_means_v1[
                    ::sample_step] - avg_eval_var_log_baseline_stds_v1[
                                     ::sample_step],
                    avg_eval_var_log_baseline_means_v1[
                    ::sample_step] + avg_eval_var_log_baseline_stds_v1[
                                     ::sample_step],
                    alpha=0.35, color="#66A61E")


    if plot_opt:
        ax.plot(np.array(list(range(len(avg_train_rewards_means_v1)))),
                [optimal_reward] * len(avg_train_rewards_means_v1), label=r"upper bound $\pi^{*}$",
                color="black",
                linestyle="dashed")

    ax.set_title(r"Episodic rewards")
    ax.set_xlabel("\# Iteration", fontsize=20)
    ax.set_ylabel("Avg Episode Rewards", fontsize=20)
    ax.set_xlim(0, len(avg_train_rewards_means_v1[::sample_step])*sample_step)
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
    plt.show()
    # plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    # plt.close(fig)


def plot_caught_stopped_intruded(
        avg_train_caught_frac_data_v1, avg_train_caught_frac_means_v1,avg_train_caught_frac_stds_v1,
        avg_train_early_stopping_frac_data_v1, avg_train_early_stopping_means_v1, avg_train_early_stopping_stds_v1,
        avg_train_intrusion_frac_data_v1, avg_train_intrusion_means_v1, avg_train_intrusion_stds_v1,
        avg_eval_2_caught_frac_data_v1, avg_eval_2_caught_frac_means_v1,avg_eval_2_caught_frac_stds_v1,
        avg_eval_2_early_stopping_frac_data_v1, avg_eval_2_early_stopping_means_v1, avg_eval_2_early_stopping_stds_v1,
        avg_eval_2_intrusion_frac_data_v1, avg_eval_2_intrusion_means_v1, avg_eval_2_intrusion_stds_v1,
        ylim_rew, file_name, markevery=10, optimal_reward = 95, sample_step = 1,
        eval_only=False, plot_opt = False):
    """
    Plots rewards, flags % and rewards of two different configurations
    """
    #matplotlib.style.use("seaborn")
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['font.serif'] = ['Times New Roman']
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 5))
    plt.rcParams.update({'font.size': 10})

    # plt.rcParams['font.serif'] = ['Times New Roman']
    #fig, ax = plt.subplots(nrows=nrows + 1, ncols=ncols, figsize=figsize)
    #plt.rcParams.update({'font.size': fontsize})

    # ylims = (0, 920)

    # Train
    ax.plot(np.array(list(range(len(avg_train_caught_frac_means_v1[::sample_step]))))*sample_step,
            avg_train_caught_frac_means_v1[::sample_step], label=r"True Positive (TP)",
            marker="s", ls='-', color="r",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(avg_train_caught_frac_means_v1[::sample_step]))))*sample_step,
                    avg_train_caught_frac_means_v1[::sample_step] - avg_train_caught_frac_stds_v1[::sample_step],
                    avg_train_caught_frac_means_v1[::sample_step] + avg_train_caught_frac_stds_v1[::sample_step],
                    alpha=0.35, color="r")


    ax.plot(np.array(list(range(len(avg_train_early_stopping_means_v1[::sample_step])))) * sample_step,
            avg_train_early_stopping_means_v1[::sample_step], label=r"False Positive (FP)",
            marker="p", ls='-', color="#599ad3",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(avg_train_early_stopping_means_v1[::sample_step])))) * sample_step,
                    avg_train_early_stopping_means_v1[::sample_step] - avg_train_early_stopping_stds_v1[::sample_step],
                    avg_train_early_stopping_means_v1[::sample_step] + avg_train_early_stopping_stds_v1[::sample_step],
                    alpha=0.35, color="#599ad3")

    ax.plot(np.array(list(range(len(avg_train_intrusion_means_v1[::sample_step])))) * sample_step,
            avg_train_intrusion_means_v1[::sample_step], label=r"False Negative (FN)",
            marker="^", ls='-', color="#f9a65a",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(avg_train_intrusion_means_v1[::sample_step])))) * sample_step,
                    avg_train_intrusion_means_v1[::sample_step] - avg_train_intrusion_stds_v1[::sample_step],
                    avg_train_intrusion_means_v1[::sample_step] + avg_train_intrusion_stds_v1[::sample_step],
                    alpha=0.35, color="#f9a65a")


    # # Eval
    # ax.plot(np.array(list(range(len(avg_eval_2_caught_frac_means_v1[::sample_step])))) * sample_step,
    #         avg_eval_2_caught_frac_means_v1[::sample_step], label=r"Emulation - True Positive (TP)",
    #         marker="*", ls='-', color="#661D98",
    #         markevery=markevery)
    # ax.fill_between(np.array(list(range(len(avg_eval_2_caught_frac_means_v1[::sample_step])))) * sample_step,
    #                 avg_eval_2_caught_frac_means_v1[::sample_step] - avg_eval_2_caught_frac_stds_v1[::sample_step],
    #                 avg_eval_2_caught_frac_means_v1[::sample_step] + avg_eval_2_caught_frac_stds_v1[::sample_step],
    #                 alpha=0.35, color="#661D98")
    #
    # ax.plot(np.array(list(range(len(avg_eval_2_early_stopping_means_v1[::sample_step])))) * sample_step,
    #         avg_eval_2_early_stopping_means_v1[::sample_step], label=r"Emulation - False Positive (FP)",
    #         marker="+", ls='-', color="#4DAF4A",
    #         markevery=markevery)
    # ax.fill_between(np.array(list(range(len(avg_eval_2_early_stopping_means_v1[::sample_step])))) * sample_step,
    #                 avg_eval_2_early_stopping_means_v1[::sample_step] - avg_eval_2_early_stopping_stds_v1[::sample_step],
    #                 avg_eval_2_early_stopping_means_v1[::sample_step] + avg_eval_2_early_stopping_stds_v1[::sample_step],
    #                 alpha=0.35, color="#4DAF4A")
    #
    # ax.plot(np.array(list(range(len(avg_eval_2_intrusion_means_v1[::sample_step])))) * sample_step,
    #         avg_eval_2_intrusion_means_v1[::sample_step], label=r"Emulation - False Positive (FP)",
    #         marker="v", ls='-', color="#80B1D3",
    #         markevery=markevery)
    # ax.fill_between(np.array(list(range(len(avg_eval_2_intrusion_means_v1[::sample_step])))) * sample_step,
    #                 avg_eval_2_intrusion_means_v1[::sample_step] - avg_eval_2_intrusion_stds_v1[::sample_step],
    #                 avg_eval_2_intrusion_means_v1[::sample_step] + avg_eval_2_intrusion_stds_v1[::sample_step],
    #                 alpha=0.35, color="#80B1D3")


    if plot_opt:
        ax.plot(np.array(list(range(len(avg_train_caught_frac_means_v1)))),
                [optimal_reward] * len(avg_train_caught_frac_means_v1), label="max",
                color="black",
                linestyle="dashed")

    ax.set_title(r"TP (intrusion detected), FP (early stopping), FN (intrusion)")
    ax.set_xlabel(r"\# Iteration", fontsize=20)
    ax.set_ylabel(r"Fraction", fontsize=20)
    ax.set_xlim(0, len(avg_train_caught_frac_means_v1[::sample_step])*sample_step)
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
    plt.show()
    # plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    # plt.close(fig)