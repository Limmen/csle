"""
Utility functions for plotting training results of attacker
"""
from typing import Tuple
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_rewards_attacker(
        avg_train_rewards_data_v1, avg_train_rewards_means_v1, avg_train_rewards_stds_v1,
        avg_eval_2_rewards_data_v1, avg_eval_2_rewards_means_v1, avg_eval_2_rewards_stds_v1,
        ylim_rew, file_name, markevery=10, optimal_reward = 95, sample_step = 1,
        eval_only=False, plot_opt = False, iterations_per_step : int = 1):
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
    ax.plot(np.array(list(range(len(avg_train_rewards_means_v1[::sample_step]))))*sample_step*iterations_per_step,
            avg_train_rewards_means_v1[::sample_step], label=r"$\pi_{\theta}$ simulation",
            marker="s", ls='-', color="r",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(avg_train_rewards_means_v1[::sample_step]))))*sample_step*iterations_per_step,
                    avg_train_rewards_means_v1[::sample_step] - avg_train_rewards_stds_v1[::sample_step],
                    avg_train_rewards_means_v1[::sample_step] + avg_train_rewards_stds_v1[::sample_step],
                    alpha=0.35, color="r")


    ax.plot(np.array(list(range(len(avg_eval_2_rewards_means_v1[::sample_step])))) * sample_step*iterations_per_step,
            avg_eval_2_rewards_means_v1[::sample_step], label=r"$\pi_{\theta}$ emulation",
            marker="p", ls='-', color="#599ad3",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(avg_eval_2_rewards_means_v1[::sample_step])))) * sample_step*iterations_per_step,
                    avg_eval_2_rewards_means_v1[::sample_step] - avg_eval_2_rewards_stds_v1[::sample_step],
                    avg_eval_2_rewards_means_v1[::sample_step] + avg_eval_2_rewards_stds_v1[::sample_step],
                    alpha=0.35, color="#599ad3")

    if plot_opt:
        ax.plot(np.array(list(range(len(avg_train_rewards_means_v1))))*iterations_per_step,
                [optimal_reward] * len(avg_train_rewards_means_v1), label=r"upper bound $\pi^{*}$",
                color="black",
                linestyle="dashed")

    ax.set_title(r"Episodic rewards")
    ax.set_xlabel(r"\# Policy updates", fontsize=20)
    ax.set_ylabel(r"Avg episode rewards", fontsize=20)
    ax.set_xlim(0, len(avg_train_rewards_means_v1[::sample_step])*sample_step*iterations_per_step)
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
    # plt.close(fig)


def plot_caught_stopped_intruded(
        avg_train_caught_frac_data_v1, avg_train_caught_frac_means_v1,avg_train_caught_frac_stds_v1,
        avg_train_early_stopping_frac_data_v1, avg_train_early_stopping_means_v1, avg_train_early_stopping_stds_v1,
        avg_train_intrusion_frac_data_v1, avg_train_intrusion_means_v1, avg_train_intrusion_stds_v1,
        avg_eval_2_caught_frac_data_v1, avg_eval_2_caught_frac_means_v1,avg_eval_2_caught_frac_stds_v1,
        avg_eval_2_early_stopping_frac_data_v1, avg_eval_2_early_stopping_means_v1, avg_eval_2_early_stopping_stds_v1,
        avg_eval_2_intrusion_frac_data_v1, avg_eval_2_intrusion_means_v1, avg_eval_2_intrusion_stds_v1,
        ylim_rew, file_name, markevery=10, optimal_reward = 95, sample_step = 1,
        eval_only=False, plot_opt = False, iterations_per_step : int = 1):
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
    # ax.plot(np.array(list(range(len(avg_train_caught_frac_means_v1[::sample_step]))))*sample_step,
    #         avg_train_caught_frac_means_v1[::sample_step], label=r"$\mathbb{P}[detected]$ $\pi_{\theta}$ simulation",
    #         marker="s", ls='-', color="r",
    #         markevery=markevery)
    # ax.fill_between(np.array(list(range(len(avg_train_caught_frac_means_v1[::sample_step]))))*sample_step,
    #                 avg_train_caught_frac_means_v1[::sample_step] - avg_train_caught_frac_stds_v1[::sample_step],
    #                 avg_train_caught_frac_means_v1[::sample_step] + avg_train_caught_frac_stds_v1[::sample_step],
    #                 alpha=0.35, color="r")
    #
    # ax.plot(np.array(list(range(len(avg_train_intrusion_means_v1[::sample_step])))) * sample_step,
    #         avg_train_intrusion_means_v1[::sample_step], label=r"$\mathbb{P}[intrusion]$ $\pi_{\theta}$ simulation",
    #         marker="^", ls='-', color="#599ad3",
    #         markevery=markevery)
    # ax.fill_between(np.array(list(range(len(avg_train_intrusion_means_v1[::sample_step])))) * sample_step,
    #                 avg_train_intrusion_means_v1[::sample_step] - avg_train_intrusion_stds_v1[::sample_step],
    #                 avg_train_intrusion_means_v1[::sample_step] + avg_train_intrusion_stds_v1[::sample_step],
    #                 alpha=0.35, color="#599ad3")
    #"#f9a65a"


    # Eval
    ax.plot(np.array(list(range(len(avg_eval_2_caught_frac_means_v1[::sample_step])))) * sample_step*iterations_per_step,
            avg_eval_2_caught_frac_means_v1[::sample_step], label=r"$\mathbb{P}[detected]$ $\pi_{\theta}$ emulation",
            marker="*", ls='-', color="#661D98",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(avg_eval_2_caught_frac_means_v1[::sample_step])))) * sample_step*iterations_per_step,
                    avg_eval_2_caught_frac_means_v1[::sample_step] - avg_eval_2_caught_frac_stds_v1[::sample_step],
                    avg_eval_2_caught_frac_means_v1[::sample_step] + avg_eval_2_caught_frac_stds_v1[::sample_step],
                    alpha=0.35, color="#661D98")

    ax.plot(np.array(list(range(len(avg_eval_2_intrusion_means_v1[::sample_step])))) * sample_step*iterations_per_step,
            avg_eval_2_intrusion_means_v1[::sample_step], label=r"$\mathbb{P}[intrusion]$ $\pi_{\theta}$ emulation",
            marker="v", ls='-', color="#f9a65a",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(avg_eval_2_intrusion_means_v1[::sample_step])))) * sample_step*iterations_per_step,
                    avg_eval_2_intrusion_means_v1[::sample_step] - avg_eval_2_intrusion_stds_v1[::sample_step],
                    avg_eval_2_intrusion_means_v1[::sample_step] + avg_eval_2_intrusion_stds_v1[::sample_step],
                    alpha=0.35, color="#f9a65a")


    if plot_opt:
        ax.plot(np.array(list(range(len(avg_train_caught_frac_means_v1))))*iterations_per_step,
                [optimal_reward] * len(avg_train_caught_frac_means_v1), label="max",
                color="black",
                linestyle="dashed")

    ax.set_title(r"Probability of Intrusion and Detection")
    ax.set_xlabel(r"\# Policy updates", fontsize=20)
    ax.set_ylabel(r"Probability", fontsize=20)
    ax.set_xlim(0, len(avg_train_caught_frac_means_v1[::sample_step])*sample_step*iterations_per_step)
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
    # plt.close(fig)


def plot_costs_attacker(
        avg_train_costs_data_v1, avg_train_costs_means_v1, avg_train_costs_stds_v1,
        avg_eval_2_costs_data_v1, avg_eval_2_costs_means_v1, avg_eval_2_costs_stds_v1,
        ylim_rew, file_name, markevery=10, optimal_reward = 95, sample_step = 1,
        eval_only=False, plot_opt = False, iterations_per_step : int = 1):
    """
    Plots costs, flags % and costs of two different configurations
    """
    #matplotlib.style.use("seaborn")
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams.update({'font.size': 10})
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 5))

    # ylims = (0, 920)

    # Plot Avg Eval costs Gensim
    ax.plot(np.array(list(range(len(avg_train_costs_means_v1[::sample_step]))))*sample_step*iterations_per_step,
            avg_train_costs_means_v1[::sample_step], label=r"$\pi_{\theta}$ simulation",
            marker="s", ls='-', color="r",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(avg_train_costs_means_v1[::sample_step]))))*sample_step*iterations_per_step,
                    avg_train_costs_means_v1[::sample_step] - avg_train_costs_stds_v1[::sample_step],
                    avg_train_costs_means_v1[::sample_step] + avg_train_costs_stds_v1[::sample_step],
                    alpha=0.35, color="r")


    ax.plot(np.array(list(range(len(avg_eval_2_costs_means_v1[::sample_step])))) * sample_step*iterations_per_step,
            avg_eval_2_costs_means_v1[::sample_step], label=r"$\pi_{\theta}$ emulation",
            marker="p", ls='-', color="#599ad3",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(avg_eval_2_costs_means_v1[::sample_step])))) * sample_step*iterations_per_step,
                    avg_eval_2_costs_means_v1[::sample_step] - avg_eval_2_costs_stds_v1[::sample_step],
                    avg_eval_2_costs_means_v1[::sample_step] + avg_eval_2_costs_stds_v1[::sample_step],
                    alpha=0.35, color="#599ad3")

    if plot_opt:
        ax.plot(np.array(list(range(len(avg_train_costs_means_v1))))*iterations_per_step,
                [optimal_reward] * len(avg_train_costs_means_v1), label=r"upper bound $\pi^{*}$",
                color="black",
                linestyle="dashed")

    ax.set_title(r"Episodic Costs of the Attacker (time (s))")
    ax.set_xlabel(r"\# Policy updates", fontsize=20)
    ax.set_ylabel(r"Avg Episode Cost", fontsize=20)
    ax.set_xlim(0, len(avg_train_costs_means_v1[::sample_step])*sample_step*iterations_per_step)
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
    # plt.close(fig)



def plot_alerts_attacker(
        avg_train_alerts_data_v1, avg_train_alerts_means_v1, avg_train_alerts_stds_v1,
        avg_eval_2_alerts_data_v1, avg_eval_2_alerts_means_v1, avg_eval_2_alerts_stds_v1,
        ylim_rew, file_name, markevery=10, optimal_reward = 95, sample_step = 1,
        eval_only=False, plot_opt = False, iterations_per_step : int = 1):
    """
    Plots alerts, flags % and alerts of two different configurations
    """
    #matplotlib.style.use("seaborn")
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams.update({'font.size': 10})
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 5))

    # ylims = (0, 920)

    # Plot Avg Eval alerts Gensim
    ax.plot(np.array(list(range(len(avg_train_alerts_means_v1[::sample_step]))))*sample_step*iterations_per_step,
            avg_train_alerts_means_v1[::sample_step], label=r"$\pi_{\theta}$ simulation",
            marker="s", ls='-', color="r",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(avg_train_alerts_means_v1[::sample_step]))))*sample_step*iterations_per_step,
                    avg_train_alerts_means_v1[::sample_step] - avg_train_alerts_stds_v1[::sample_step],
                    avg_train_alerts_means_v1[::sample_step] + avg_train_alerts_stds_v1[::sample_step],
                    alpha=0.35, color="r")


    ax.plot(np.array(list(range(len(avg_eval_2_alerts_means_v1[::sample_step])))) * sample_step*iterations_per_step,
            avg_eval_2_alerts_means_v1[::sample_step], label=r"$\pi_{\theta}$ emulation",
            marker="p", ls='-', color="#599ad3",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(avg_eval_2_alerts_means_v1[::sample_step])))) * sample_step*iterations_per_step,
                    avg_eval_2_alerts_means_v1[::sample_step] - avg_eval_2_alerts_stds_v1[::sample_step],
                    avg_eval_2_alerts_means_v1[::sample_step] + avg_eval_2_alerts_stds_v1[::sample_step],
                    alpha=0.35, color="#599ad3")

    if plot_opt:
        ax.plot(np.array(list(range(len(avg_train_alerts_means_v1))))*iterations_per_step,
                [optimal_reward] * len(avg_train_alerts_means_v1), label=r"upper bound $\pi^{*}$",
                color="black",
                linestyle="dashed")

    ax.set_title(r"Episodic Alerts Generated by the Attacker (time (s))")
    ax.set_xlabel(r"\# Policy updates", fontsize=20)
    ax.set_ylabel(r"Avg Episode Cost", fontsize=20)
    ax.set_xlim(0, len(avg_train_alerts_means_v1[::sample_step])*sample_step*iterations_per_step)
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
    # plt.close(fig)


def plot_flags_attacker(
        avg_train_flags_data_v1, avg_train_flags_means_v1, avg_train_flags_stds_v1,
        avg_eval_2_flags_data_v1, avg_eval_2_flags_means_v1, avg_eval_2_flags_stds_v1,
        ylim_rew, file_name, markevery=10, optimal_reward = 95, sample_step = 1,
        eval_only=False, plot_opt = False, iterations_per_step : int = 1):
    """
    Plots flags, flags % and flags of two different configurations
    """
    #matplotlib.style.use("seaborn")
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams.update({'font.size': 10})
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 5))

    # ylims = (0, 920)

    # Plot Avg Eval flags Gensim
    ax.plot(np.array(list(range(len(avg_train_flags_means_v1[::sample_step]))))*sample_step*iterations_per_step,
            avg_train_flags_means_v1[::sample_step], label=r"$\pi_{\theta}$ simulation",
            marker="s", ls='-', color="r",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(avg_train_flags_means_v1[::sample_step]))))*sample_step*iterations_per_step,
                    avg_train_flags_means_v1[::sample_step] - avg_train_flags_stds_v1[::sample_step],
                    avg_train_flags_means_v1[::sample_step] + avg_train_flags_stds_v1[::sample_step],
                    alpha=0.35, color="r")


    ax.plot(np.array(list(range(len(avg_eval_2_flags_means_v1[::sample_step])))) * sample_step*iterations_per_step,
            avg_eval_2_flags_means_v1[::sample_step], label=r"$\pi_{\theta}$ emulation",
            marker="p", ls='-', color="#599ad3",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(avg_eval_2_flags_means_v1[::sample_step])))) * sample_step*iterations_per_step,
                    avg_eval_2_flags_means_v1[::sample_step] - avg_eval_2_flags_stds_v1[::sample_step],
                    avg_eval_2_flags_means_v1[::sample_step] + avg_eval_2_flags_stds_v1[::sample_step],
                    alpha=0.35, color="#599ad3")

    if plot_opt:
        ax.plot(np.array(list(range(len(avg_train_flags_means_v1))))*iterations_per_step,
                [optimal_reward] * len(avg_train_flags_means_v1), label=r"upper bound $\pi^{*}$",
                color="black",
                linestyle="dashed")

    ax.set_title(r"Fraction of flags captured")
    ax.set_xlabel(r"\# Policy updates", fontsize=20)
    ax.set_ylabel(r"Avg Fraction of Flags Captured per Episode", fontsize=20)
    ax.set_xlim(0, len(avg_train_flags_means_v1[::sample_step])*sample_step*iterations_per_step)
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
    # plt.close(fig)



def plot_steps_attacker(
        avg_train_steps_data_v1, avg_train_steps_means_v1, avg_train_steps_stds_v1,
        avg_eval_2_steps_data_v1, avg_eval_2_steps_means_v1, avg_eval_2_steps_stds_v1,
        ylim_rew, file_name, markevery=10, optimal_reward = 95, sample_step = 1,
        eval_only=False, plot_opt = False, iterations_per_step : int = 1):
    """
    Plots steps, steps % and steps of two different configurations
    """
    #matplotlib.style.use("seaborn")
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams.update({'font.size': 10})
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 5))

    # ylims = (0, 920)

    # Plot Avg Eval steps Gensim
    ax.plot(np.array(list(range(len(avg_train_steps_means_v1[::sample_step]))))*sample_step*iterations_per_step,
            avg_train_steps_means_v1[::sample_step], label=r"$\pi_{\theta}$ simulation",
            marker="s", ls='-', color="r",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(avg_train_steps_means_v1[::sample_step]))))*sample_step*iterations_per_step,
                    avg_train_steps_means_v1[::sample_step] - avg_train_steps_stds_v1[::sample_step],
                    avg_train_steps_means_v1[::sample_step] + avg_train_steps_stds_v1[::sample_step],
                    alpha=0.35, color="r")


    ax.plot(np.array(list(range(len(avg_eval_2_steps_means_v1[::sample_step])))) * sample_step*iterations_per_step,
            avg_eval_2_steps_means_v1[::sample_step], label=r"$\pi_{\theta}$ emulation",
            marker="p", ls='-', color="#599ad3",
            markevery=markevery)
    ax.fill_between(np.array(list(range(len(avg_eval_2_steps_means_v1[::sample_step])))) * sample_step*iterations_per_step,
                    avg_eval_2_steps_means_v1[::sample_step] - avg_eval_2_steps_stds_v1[::sample_step],
                    avg_eval_2_steps_means_v1[::sample_step] + avg_eval_2_steps_stds_v1[::sample_step],
                    alpha=0.35, color="#599ad3")

    if plot_opt:
        ax.plot(np.array(list(range(len(avg_train_steps_means_v1))))*iterations_per_step,
                [optimal_reward] * len(avg_train_steps_means_v1), label=r"upper bound $\pi^{*}$",
                color="black",
                linestyle="dashed")

    ax.set_title(r"\# Episode length")
    ax.set_xlabel(r"\# Policy updates", fontsize=20)
    ax.set_ylabel(r"\# Steps", fontsize=20)
    ax.set_xlim(0, len(avg_train_steps_means_v1[::sample_step])*sample_step*iterations_per_step)
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
    # plt.close(fig)



def plot_flags_int_r_steps_costs_alerts(
        avg_train_rewards_data_v1, avg_train_rewards_means_v1, avg_train_rewards_stds_v1,
        avg_eval_2_rewards_data_v1, avg_eval_2_rewards_means_v1, avg_eval_2_rewards_stds_v1,
        avg_train_caught_frac_data_v1, avg_train_caught_frac_means_v1,avg_train_caught_frac_stds_v1,
        avg_train_intrusion_frac_data_v1, avg_train_intrusion_means_v1, avg_train_intrusion_stds_v1,
        avg_eval_2_caught_frac_data_v1, avg_eval_2_caught_frac_means_v1,avg_eval_2_caught_frac_stds_v1,
        avg_eval_2_intrusion_frac_data_v1, avg_eval_2_intrusion_means_v1, avg_eval_2_intrusion_stds_v1,
        avg_train_flags_data_v1, avg_train_flags_means_v1, avg_train_flags_stds_v1,
        avg_eval_2_flags_data_v1, avg_eval_2_flags_means_v1, avg_eval_2_flags_stds_v1,
        avg_train_costs_data_v1, avg_train_costs_means_v1, avg_train_costs_stds_v1,
        avg_eval_2_costs_data_v1, avg_eval_2_costs_means_v1, avg_eval_2_costs_stds_v1,
        avg_train_alerts_data_v1, avg_train_alerts_means_v1, avg_train_alerts_stds_v1,
        avg_eval_2_alerts_data_v1, avg_eval_2_alerts_means_v1, avg_eval_2_alerts_stds_v1,
        avg_train_steps_data_v1, avg_train_steps_means_v1, avg_train_steps_stds_v1,
        avg_eval_2_steps_data_v1, avg_eval_2_steps_means_v1, avg_eval_2_steps_stds_v1,
        fontsize : int = 6.5, figsize: Tuple[int,int] =  (3.75, 3.4),
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
    fig, ax = plt.subplots(nrows=2, ncols=3, figsize=figsize)


    # Plot flags

    ax[0][0].plot(np.array(list(range(len(avg_train_flags_means_v1[::sample_step])))) * sample_step * iterations_per_step,
            avg_train_flags_means_v1[::sample_step]*100, label=r"$\pi_{\theta}$ simulation",
            marker="s", ls='-', color="r", markevery=markevery, markersize=markersize, lw=lw)
    ax[0][0].fill_between(
        np.array(list(range(len(avg_train_flags_means_v1[::sample_step])))) * sample_step * iterations_per_step,
        avg_train_flags_means_v1[::sample_step]*100 - avg_train_flags_stds_v1[::sample_step]*100,
        avg_train_flags_means_v1[::sample_step]*100 + avg_train_flags_stds_v1[::sample_step]*100,
        alpha=0.35, color="r", lw=lw)

    ax[0][0].plot(np.array(list(range(len(avg_eval_2_flags_means_v1[::sample_step])))) * sample_step * iterations_per_step,
            avg_eval_2_flags_means_v1[::sample_step]*100, label=r"$\pi_{\theta}$ emulation",
            marker="p", ls='-', color="#599ad3",
            markevery=markevery, markersize=markersize, lw=lw)
    ax[0][0].fill_between(
        np.array(list(range(len(avg_eval_2_flags_means_v1[::sample_step])))) * sample_step * iterations_per_step,
        avg_eval_2_flags_means_v1[::sample_step]*100 - avg_eval_2_flags_stds_v1[::sample_step]*100,
        avg_eval_2_flags_means_v1[::sample_step]*100 + avg_eval_2_flags_stds_v1[::sample_step]*100,
        alpha=0.35, color="#599ad3", lw=lw)

    ax[0][0].plot(np.array(list(range(len(avg_train_flags_means_v1)))) * iterations_per_step,
            [optimal_flag*100] * len(avg_train_flags_means_v1), label=r"upper bound",
            color="black", linestyle="dashed", markersize=markersize, dashes=(4, 2), lw=lw)

    ax[0][0].grid('on')
    # ax[0][0].set_xlabel("", fontsize=labelsize)
    #ax[0][0].set_ylabel(r"\% Flags captured", fontsize=labelsize)
    ax[0][0].set_xlabel(r"\# Policy updates", fontsize=labelsize)
    xlab = ax[0][0].xaxis.get_label()
    ylab = ax[0][0].yaxis.get_label()
    xlab.set_size(labelsize)
    ylab.set_size(fontsize)
    ax[0][0].tick_params(axis='both', which='major', labelsize=labelsize, length=2.2, width=0.6)
    ax[0][0].tick_params(axis='both', which='minor', labelsize=labelsize, length=2.2, width=0.6)
    ax[0][0].set_ylim(0, 105)
    ax[0][0].set_xlim(0, len(avg_train_rewards_means_v1[::sample_step]) * sample_step * iterations_per_step)
    ax[0][0].set_title(r"\% Flags captured per episode", fontsize=fontsize)


    # % intrusions

    ax[0][1].plot(
        np.array(list(range(len(avg_eval_2_caught_frac_means_v1[::sample_step])))) * sample_step * iterations_per_step,
        avg_eval_2_caught_frac_means_v1[::sample_step], label=r"$\mathbb{P}[detected]$ $\pi_{\theta}$ emulation",
        marker="*", ls='-', color="#599ad3",
        markevery=markevery, markersize=markersize, lw=lw)
    ax[0][1].fill_between(
        np.array(list(range(len(avg_eval_2_caught_frac_means_v1[::sample_step])))) * sample_step * iterations_per_step,
        avg_eval_2_caught_frac_means_v1[::sample_step] - avg_eval_2_caught_frac_stds_v1[::sample_step],
        avg_eval_2_caught_frac_means_v1[::sample_step] + avg_eval_2_caught_frac_stds_v1[::sample_step],
        alpha=0.35, color="#599ad3")

    ax[0][1].plot(np.array(list(range(len(avg_train_caught_frac_means_v1[::sample_step]))))*sample_step* iterations_per_step,
            avg_train_caught_frac_means_v1[::sample_step], label=r"$\mathbb{P}[detected]$ $\pi_{\theta}$ simulation",
            marker="s", ls='-', color="r",
            markevery=markevery, markersize=markersize, lw=lw)
    ax[0][1].fill_between(np.array(list(range(len(avg_train_caught_frac_means_v1[::sample_step]))))*sample_step* iterations_per_step,
                    avg_train_caught_frac_means_v1[::sample_step] - avg_train_caught_frac_stds_v1[::sample_step],
                    avg_train_caught_frac_means_v1[::sample_step] + avg_train_caught_frac_stds_v1[::sample_step],
                    alpha=0.35, color="r")

    # ax[0][1].plot(np.array(list(range(len(avg_train_flags_means_v1)))) * iterations_per_step,
    #               [0] * len(avg_train_flags_means_v1), label=r"upper bound",
    #               color="black", linestyle="dashed", markersize=markersize, dashes=(4, 2), lw=lw)

    ax[0][1].grid('on')
    # ax[0][0].set_xlabel("", fontsize=labelsize)
    #ax[0][1].set_ylabel(r"$\mathbb{P}[\text{detected}]$", fontsize=labelsize)
    ax[0][1].set_xlabel(r"\# Policy updates", fontsize=labelsize)
    xlab = ax[0][1].xaxis.get_label()
    ylab = ax[0][1].yaxis.get_label()
    xlab.set_size(labelsize)
    ylab.set_size(fontsize)
    ax[0][1].tick_params(axis='both', which='major', labelsize=labelsize, length=2.2, width=0.6)
    ax[0][1].tick_params(axis='both', which='minor', labelsize=labelsize, length=2.2, width=0.6)
    ax[0][1].set_ylim(0, 1.1)
    ax[0][1].set_xlim(0, len(avg_train_rewards_means_v1[::sample_step]) * sample_step * iterations_per_step)
    ax[0][1].set_title(r"$\mathbb{P}[\text{detected}]$", fontsize=fontsize)

    ax[0][2].plot(np.array(list(range(len(avg_train_rewards_means_v1[::sample_step])))) * sample_step * iterations_per_step,
            avg_train_rewards_means_v1[::sample_step], label=r"$\pi_{\theta}$ simulation",
            marker="s", ls='-', color="r",
            markevery=markevery, markersize=markersize, lw=lw)
    ax[0][2].fill_between(
        np.array(list(range(len(avg_train_rewards_means_v1[::sample_step])))) * sample_step * iterations_per_step,
        avg_train_rewards_means_v1[::sample_step] - avg_train_rewards_stds_v1[::sample_step],
        avg_train_rewards_means_v1[::sample_step] + avg_train_rewards_stds_v1[::sample_step],
        alpha=0.35, color="r")

    ax[0][2].plot(np.array(list(range(len(avg_eval_2_rewards_means_v1[::sample_step])))) * sample_step * iterations_per_step,
            avg_eval_2_rewards_means_v1[::sample_step], label=r"$\pi_{\theta}$ emulation",
            marker="p", ls='-', color="#599ad3", markevery=markevery, markersize=markersize, lw=lw)
    ax[0][2].fill_between(
        np.array(list(range(len(avg_eval_2_rewards_means_v1[::sample_step])))) * sample_step * iterations_per_step,
        avg_eval_2_rewards_means_v1[::sample_step] - avg_eval_2_rewards_stds_v1[::sample_step],
        avg_eval_2_rewards_means_v1[::sample_step] + avg_eval_2_rewards_stds_v1[::sample_step],
        alpha=0.35, color="#599ad3")

    ax[0][2].plot(np.array(list(range(len(avg_train_flags_means_v1)))) * iterations_per_step,
                  [optimal_reward] * len(avg_train_flags_means_v1), label=r"upper bound",
                  color="black", linestyle="dashed", markersize=markersize, dashes=(4, 2), lw=lw)

    ax[0][2].grid('on')
    #ax[0][2].set_ylabel(r"Reward", fontsize=labelsize)
    ax[0][2].set_xlabel(r"\# Policy updates", fontsize=labelsize)
    xlab = ax[0][2].xaxis.get_label()
    ylab = ax[0][2].yaxis.get_label()
    xlab.set_size(labelsize)
    ylab.set_size(fontsize)
    ax[0][2].tick_params(axis='both', which='major', labelsize=labelsize, length=2.2, width=0.6)
    ax[0][2].tick_params(axis='both', which='minor', labelsize=labelsize, length=2.2, width=0.6)
    ax[0][2].set_ylim(-300, 170)
    ax[0][2].set_xlim(0, len(avg_train_rewards_means_v1[::sample_step]) * sample_step * iterations_per_step)
    ax[0][2].set_title(r"Reward per episode", fontsize=fontsize)

    ax[1][0].plot(np.array(list(range(len(avg_train_steps_means_v1[::sample_step])))) * sample_step * iterations_per_step,
            avg_train_steps_means_v1[::sample_step], label=r"$\pi_{\theta}$ simulation",
            marker="s", ls='-', color="r", markevery=markevery, markersize=markersize, lw=lw)
    ax[1][0].fill_between(
        np.array(list(range(len(avg_train_steps_means_v1[::sample_step])))) * sample_step * iterations_per_step,
        avg_train_steps_means_v1[::sample_step] - avg_train_steps_stds_v1[::sample_step],
        avg_train_steps_means_v1[::sample_step] + avg_train_steps_stds_v1[::sample_step],
        alpha=0.35, color="r")

    ax[1][0].plot(np.array(list(range(len(avg_eval_2_steps_means_v1[::sample_step])))) * sample_step * iterations_per_step,
            avg_eval_2_steps_means_v1[::sample_step], label=r"$\pi_{\theta}$ emulation",
            marker="p", ls='-', color="#599ad3",markevery=markevery, markersize=markersize, lw=lw)
    ax[1][0].fill_between(
        np.array(list(range(len(avg_eval_2_steps_means_v1[::sample_step])))) * sample_step * iterations_per_step,
        avg_eval_2_steps_means_v1[::sample_step] - avg_eval_2_steps_stds_v1[::sample_step],
        avg_eval_2_steps_means_v1[::sample_step] + avg_eval_2_steps_stds_v1[::sample_step],
        alpha=0.35, color="#599ad3")

    ax[1][0].grid('on')
    #ax[1][0].set_ylabel(r"Length (steps)", fontsize=labelsize)
    ax[1][0].set_xlabel(r"\# Policy updates", fontsize=labelsize)
    xlab = ax[1][0].xaxis.get_label()
    ylab = ax[1][0].yaxis.get_label()
    xlab.set_size(labelsize)
    ylab.set_size(fontsize)
    ax[1][0].tick_params(axis='both', which='major', labelsize=labelsize, length=2.2, width=0.6)
    ax[1][0].tick_params(axis='both', which='minor', labelsize=labelsize, length=2.2, width=0.6)
    ax[1][0].set_ylim(0, 110)
    ax[1][0].set_xlim(0, len(avg_train_rewards_means_v1[::sample_step]) * sample_step * iterations_per_step)
    ax[1][0].set_title(r"Episode length (steps)", fontsize=fontsize)

    ax[1][1].plot(np.array(list(range(len(avg_train_costs_means_v1[::sample_step])))) * sample_step * iterations_per_step,
            avg_train_costs_means_v1[::sample_step], label=r"$\pi_{\theta}$ simulation",
            marker="s", ls='-', color="r", markevery=markevery, markersize=markersize, lw=lw)
    ax[1][1].fill_between(
        np.array(list(range(len(avg_train_costs_means_v1[::sample_step])))) * sample_step * iterations_per_step,
        avg_train_costs_means_v1[::sample_step] - avg_train_costs_stds_v1[::sample_step],
        avg_train_costs_means_v1[::sample_step] + avg_train_costs_stds_v1[::sample_step],
        alpha=0.35, color="r")

    ax[1][1].plot(np.array(list(range(len(avg_eval_2_costs_means_v1[::sample_step])))) * sample_step * iterations_per_step,
            avg_eval_2_costs_means_v1[::sample_step], label=r"$\pi_{\theta}$ emulation",
            marker="p", ls='-', color="#599ad3", markevery=markevery, markersize=markersize, lw=lw)
    ax[1][1].fill_between(
        np.array(list(range(len(avg_eval_2_costs_means_v1[::sample_step])))) * sample_step * iterations_per_step,
        avg_eval_2_costs_means_v1[::sample_step] - avg_eval_2_costs_stds_v1[::sample_step],
        avg_eval_2_costs_means_v1[::sample_step] + avg_eval_2_costs_stds_v1[::sample_step],
        alpha=0.35, color="#599ad3")

    ax[1][1].grid('on')
    #ax[1][1].set_ylabel(r"Length (seconds)", fontsize=labelsize)
    ax[1][1].set_xlabel(r"\# Policy updates", fontsize=labelsize)
    xlab = ax[1][1].xaxis.get_label()
    ylab = ax[1][1].yaxis.get_label()
    xlab.set_size(labelsize)
    ylab.set_size(fontsize)
    ax[1][1].tick_params(axis='both', which='major', labelsize=labelsize, length=2.2, width=0.6)
    ax[1][1].tick_params(axis='both', which='minor', labelsize=labelsize, length=2.2, width=0.6)
    ax[1][1].set_ylim(400, 8000)
    ax[1][1].set_xlim(0, len(avg_train_rewards_means_v1[::sample_step]) * sample_step * iterations_per_step)
    ax[1][1].set_title(r"Episode length (seconds)", fontsize=fontsize)

    ax[1][2].plot(np.array(list(range(len(avg_train_alerts_means_v1[::sample_step])))) * sample_step * iterations_per_step,
            avg_train_alerts_means_v1[::sample_step], label=r"$\pi_{\theta}$ simulation",
            marker="s", ls='-', color="r", markevery=markevery, markersize=markersize, lw=lw)
    ax[1][2].fill_between(
        np.array(list(range(len(avg_train_alerts_means_v1[::sample_step])))) * sample_step * iterations_per_step,
        avg_train_alerts_means_v1[::sample_step] - avg_train_alerts_stds_v1[::sample_step],
        avg_train_alerts_means_v1[::sample_step] + avg_train_alerts_stds_v1[::sample_step],
        alpha=0.35, color="r")

    ax[1][2].plot(np.array(list(range(len(avg_eval_2_alerts_means_v1[::sample_step])))) * sample_step * iterations_per_step,
            avg_eval_2_alerts_means_v1[::sample_step], label=r"$\pi_{\theta}$ emulation",
            marker="p", ls='-', color="#599ad3", markevery=markevery, markersize=markersize, lw=lw)
    ax[1][2].fill_between(
        np.array(list(range(len(avg_eval_2_alerts_means_v1[::sample_step])))) * sample_step * iterations_per_step,
        avg_eval_2_alerts_means_v1[::sample_step] - avg_eval_2_alerts_stds_v1[::sample_step],
        avg_eval_2_alerts_means_v1[::sample_step] + avg_eval_2_alerts_stds_v1[::sample_step],
        alpha=0.35, color="#599ad3")

    ax[1][2].grid('on')
    #ax[1][2].set_ylabel(r"\# IDS Alerts", fontsize=labelsize)
    ax[1][2].set_xlabel(r"\# Policy updates", fontsize=labelsize)
    xlab = ax[1][2].xaxis.get_label()
    ylab = ax[1][2].yaxis.get_label()
    xlab.set_size(labelsize)
    ylab.set_size(fontsize)
    ax[1][2].tick_params(axis='both', which='major', labelsize=labelsize, length=2.2, width=0.6)
    ax[1][2].tick_params(axis='both', which='minor', labelsize=labelsize, length=2.2, width=0.6)
    ax[1][2].set_ylim(0, 1700)
    ax[1][2].set_xlim(0, len(avg_train_rewards_means_v1[::sample_step]) * sample_step * iterations_per_step)
    ax[1][2].set_title(r"\# IDS Alerts per episode", fontsize=fontsize)

    handles, labels = ax[0][0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.52, 0.09),
               ncol=3, fancybox=True, shadow=True)

    fig.tight_layout()
    #fig.subplots_adjust(wspace=wspace, hspace=hspace, top=top, bottom=bottom)
    fig.subplots_adjust(wspace=wspace, hspace=hspace, bottom=bottom)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)

