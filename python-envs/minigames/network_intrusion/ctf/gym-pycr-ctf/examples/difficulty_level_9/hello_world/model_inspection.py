"""
Utility scripts for plotting
"""

from gym_pycr_ctf.agents.policy_gradient.ppo_baseline.impl.ppo.ppo import PPO
import torch
import numpy as np
import gym
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import os


def initialize_model(env, load_path, device, agent_config) -> None:
    """
    Initialize models

    :return: None
    """
    # Initialize models
    model = PPO.load(path=load_path, env=env, load_path=load_path, device=device,
                     agent_config=agent_config, map_location='cpu')
    return model


def plot_alerts_threshold() -> None:
    """
    Plots alerts thresholds

    :return: None
    """
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
    # env = gym.make("optimal-intrusion-response-v3")
    env = None
    # v3_load_path = "/Users/kimham/workspace/gym-optimal-intrusion-response/examples/v3/v3_results/v3/results_1/data/1620801616.3180108_0_4575_policy_network.zip"
    # v2_load_path = "/Users/kimham/workspace/gym-optimal-intrusion-response/examples/v3/v2_results/v2/results_2/data/1620760014.3964121_0_1150_policy_network.zip"
    experienced_attacker_load_path = "/Users/kimham/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_9/20_aug/results_experienced_attacker_128_neurons_2_hidden_layers_12k_batch/data/1629507805.8662815_999_400_policy_network.zip"
    novice_attacker_load_path = "/Users/kimham/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_9/20_aug/results_novice_attacker_128_neurons_2_hidden_layers_12k_batch/data/1629447739.1471612_999_400_policy_network.zip"
    model = initialize_model(env, experienced_attacker_load_path, "cpu", None)
    model2 = initialize_model(env, novice_attacker_load_path, "cpu", None)
    num_alerts = np.arange(0, 200, 1)
    x = []
    y = []
    y2 = []

    for i in range(len(num_alerts)):
        state = np.array([num_alerts[i], num_alerts[i], 0, 32])
        actions, values, log_prob = model.defender_policy.forward(torch.tensor(np.array([state])).to("cpu"),
                                                                 deterministic=False,
                                                                  attacker=True, env=env, mask_actions=False)
        if actions.item() == 0:
            val = math.exp(log_prob.item())
        else:
            val = 1 - math.exp(log_prob.item())
        x.append(i*2)
        y.append(val)

        actions, values, log_prob = model2.defender_policy.forward(torch.tensor(np.array([state])).to("cpu"),
                                                                  deterministic=False,
                                                                  attacker=True, env=env, mask_actions=False)
        if actions.item() == 0:
            val = math.exp(log_prob.item())
        else:
            val = 1 - math.exp(log_prob.item())
        y2.append(val)
    fontsize = 15
    labelsize=13.5

    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts,amsmath}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['axes.titlepad'] = 2
    # plt.rcParams['xtick.major.pad'] = 0.5
    plt.rcParams['ytick.major.pad'] = 0.05
    plt.rcParams['axes.labelpad'] = 2
    plt.rcParams['axes.linewidth'] = 0.1
    plt.rcParams.update({'font.size': fontsize})

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(3.5, 2.9))

    # ylims = (0, 920)

    # Plot Avg Eval rewards Gensim
    colors = plt.cm.viridis(np.linspace(0.3, 1, 2))[-2:]
    ax.plot(x,
            y, label=r"$\pi_{\theta}$ vs \textsc{StealthyAttacker}",
            ls='-', color=colors[0])
    ax.fill_between(x, y, y2,
                    alpha=0.35, color=colors[0])

    ax.plot(x,
            y2, label=r"$\pi_{\theta}$ vs \textsc{NoisyAttacker}",
            ls='-', color="r")
    ax.fill_between(x, y2, np.zeros(len(y2)),
                    alpha=0.35, color="r")

    # if plot_opt:
    ax.plot(x, [0.5] * len(x), color="black", linestyle="dashed")

    ax.set_title(r"$\pi_{\theta}(\text{stop}|x+y)$", fontsize=fontsize)
    ax.set_xlabel(r"\# total alerts $x+y$", fontsize=labelsize)
    ax.set_xlim(0, len(x)*2)
    #ax.set_xlim(0, 100)
    ax.set_ylim(0, 1.1)

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
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.23),
              ncol=1, fancybox=True, shadow=False, fontsize=12)

    ttl = ax.title
    ttl.set_position([.5, 1.05])

    ax.tick_params(axis='both', which='major', labelsize=labelsize, length=2.2, width=0.6)
    ax.tick_params(axis='both', which='minor', labelsize=labelsize, length=2.2, width=0.6)

    fig.tight_layout()
    # plt.show()
    plt.subplots_adjust(wspace=0, hspace=0, bottom=0.2)
    fig.savefig("threshold_alerts" + ".png", format="png", dpi=600)
    fig.savefig("threshold_alerts_22" + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    # plt.close(fig)


def plot_3d() -> None:
    """
    3d plot of empirical thresholds

    :return: None
    """
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
    # env = gym.make("optimal-intrusion-response-v3")
    # v3_load_path = "/Users/kimham/workspace/gym-optimal-intrusion-response/examples/v3/v3_results/v3/results_1/data/1620801616.3180108_0_4575_policy_network.zip"
    # v2_load_path = "/Users/kimham/workspace/gym-optimal-intrusion-response/examples/v3/v2_results/v2/results_2/data/1620760014.3964121_0_1150_policy_network.zip"
    experienced_attacker_model_path = "/Users/kimham/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_9/20_aug/results_experienced_attacker_128_neurons_2_hidden_layers_12k_batch/data/1629507805.8662815_999_400_policy_network.zip"
    novice_attacker_model_path = "/Users/kimham/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_9/20_aug/results_novice_attacker_128_neurons_2_hidden_layers_12k_batch/data/1629447739.1471612_999_400_policy_network.zip"
    env=None
    model = initialize_model(env, experienced_attacker_model_path, "cpu", None)
    # num_severe_alerts = np.arange(200, 0, -1)
    # num_warning_alerts = np.arange(0, 200, 1)
    num_severe_alerts = np.arange(100, 0, -1)
    num_warning_alerts = np.arange(0, 100, 1)
    sev, warn = np.meshgrid(num_severe_alerts, num_warning_alerts)
    action_val = action_pred_core_state_severe_warning(sev, warn, model, env)
    fontsize = 15
    labelsize = 13.5
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts,amsmath}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['axes.titlepad'] = 5
    plt.rcParams['xtick.major.pad'] = 0.05
    plt.rcParams['ytick.major.pad'] = 0.05
    plt.rcParams['axes.labelpad'] = 0.2
    plt.rcParams['axes.linewidth'] = 0.2
    plt.rcParams.update({'font.size': 6.5})
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams.update({'font.size': fontsize})
    plt.rcParams.update({'figure.autolayout': True})
    fig, ax = plt.subplots(nrows=1, ncols=1, subplot_kw={'projection': '3d'}, figsize=(5, 3.5))
    ax.plot_surface(sev, warn, action_val, cmap='Blues', linewidth=0.3,
                    alpha=0.8, edgecolor='k', rstride=12, cstride=12)
    ax.set_title(r"$\pi_{\theta}(\text{stop} | x, y)$ vs \textsc{StealthyAttacker}", fontsize=fontsize)
    ax.set_xlabel(r"warn alerts $w_a$")
    ax.set_ylabel(r"sev alerts $s_a$")
    ax.xaxis.labelpad = 0
    ax.yaxis.labelpad = 0
    # ax.set_xticks(np.arange(0, 200 + 1, 50))
    # ax.set_yticks(np.arange(0, 200+1, 50))
    ax.set_xticks(np.arange(0, 100 + 1, 25))
    ax.set_yticks(np.arange(0, 100 + 1, 25))
    xlab = ax.xaxis.get_label()
    ylab = ax.yaxis.get_label()
    xlab.set_size(labelsize)
    ylab.set_size(labelsize)
    ax.tick_params(axis='both', which='major', labelsize=labelsize, length=2.2, width=0.6)
    ax.tick_params(axis='both', which='minor', labelsize=labelsize, length=2.2, width=0.6)
    fig.tight_layout()
    plt.subplots_adjust(bottom=0.55)
    # plt.show()
    # fig.savefig("alerts_stopping" + ".png", format="png", dpi=600)
    fig.savefig("alerts_stopping" + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)


def plot_3d_2() -> None:
    """
    3d plot of empirical thresholds

    :return: None
    """
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
    # env = gym.make("optimal-intrusion-response-v3")
    env=None
    # v2_load_path = "/Users/kimham/workspace/gym-optimal-intrusion-response/examples/v3/v2_results/v2/results_2/data/1620760014.3964121_0_1150_policy_network.zip"
    experienced_attacker_load_path = "/Users/kimham/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_9/20_aug/results_experienced_attacker_128_neurons_2_hidden_layers_12k_batch/data/1629507805.8662815_999_400_policy_network.zip"
    novice_attacker_load_path = "/Users/kimham/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_9/20_aug/results_novice_attacker_128_neurons_2_hidden_layers_12k_batch/data/1629447739.1471612_999_400_policy_network.zip"
    model2 = initialize_model(env, novice_attacker_load_path, "cpu", None)
    # num_severe_alerts = np.arange(200, 0, -1)
    # num_warning_alerts = np.arange(0, 200, 1)
    num_severe_alerts = np.arange(50, 0, -1)
    num_warning_alerts = np.arange(0, 50, 1)
    sev, warn = np.meshgrid(num_severe_alerts, num_warning_alerts)
    action_val_2 = action_pred_core_state_severe_warning(sev, warn, model2, env)
    fontsize=15
    labelsize=13.5
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts,amsmath}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['axes.titlepad'] = 5
    plt.rcParams['xtick.major.pad'] = 0.05
    plt.rcParams['ytick.major.pad'] = 0.05
    plt.rcParams['axes.labelpad'] = 0.2
    plt.rcParams['axes.linewidth'] = 0.2
    plt.rcParams.update({'font.size': 6.5})
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams.update({'font.size': fontsize})
    plt.rcParams.update({'figure.autolayout': True})
    fig, ax = plt.subplots(nrows=1, ncols=1, subplot_kw={'projection': '3d'}, figsize=(5, 3.5))
    ax.plot_surface(sev, warn, action_val_2, cmap='Reds', linewidth=0.3,
                    alpha=0.8, edgecolor='k', rstride=12, cstride=12)
    ax.set_title(r"$\pi_{\theta}(\text{stop} | x, y)$ vs \textsc{NoisyAttacker}", fontsize=fontsize)
    # ax.set_xlabel(r"warn alerts $w_a$")
    # ax.set_ylabel(r"sev alerts $s_a$")
    ax.xaxis.labelpad = 0
    ax.yaxis.labelpad = 0
    ax.set_xticks(np.arange(0, 200 + 1, 50))
    ax.set_yticks(np.arange(0, 200+1, 50))
    xlab = ax.xaxis.get_label()
    ylab = ax.yaxis.get_label()
    xlab.set_size(labelsize)
    ylab.set_size(labelsize)
    ax.tick_params(axis='both', which='major', labelsize=labelsize, length=2.2, width=0.6)
    ax.tick_params(axis='both', which='minor', labelsize=labelsize, length=2.2, width=0.6)
    # ax.set_xlim(0, 50)
    # ax.set_ylim(0, 50)
    fig.tight_layout()
    fig.subplots_adjust(bottom=0.55)
    fig.savefig("alerts_stopping_2" + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)



def plot_logins_threshold() -> None:
    """
    Plots logins thresholds

    :return: None
    """
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
    # env = gym.make("optimal-intrusion-response-v3")
    env = None
    v2_load_path = "/Users/kimham/workspace/cnsm_21_plots/examples/v3/backup_pycr_cnsm_21_22_may/v2_results/results_1/data/1621504581.9928813_72899_400_policy_network.zip"
    v3_load_path = "/Users/kimham/workspace/cnsm_21_plots/examples/v3/backup_pycr_cnsm_21_22_may/v3_results/results_1/data/1621513319.4798174_299_300_policy_network.zip"
    model = initialize_model(env, v2_load_path, "cpu", None)
    model2 = initialize_model(env, v3_load_path, "cpu", None)
    num_logins = np.arange(0, 100, 1)
    x = []
    y = []
    y2 = []


    for i in range(len(num_logins)):
        state = np.array([0, 0, 0, num_logins[i]])
        actions, values, log_prob = model.defender_policy.forward(torch.tensor(np.array([state])).to("cpu"),
                                                                 deterministic=False,
                                                                  attacker=False, env=env, mask_actions=False)
        if actions.item() == 1:
            val = math.exp(log_prob.item())
        else:
            val = 1 - math.exp(log_prob.item())
        x.append(i)
        y.append(val)

        state = np.array([0, 0, 0, num_logins[i]])
        actions, values, log_prob = model2.defender_policy.forward(torch.tensor(np.array([state])).to("cpu"),
                                                                  deterministic=False,
                                                                  attacker=False, env=env, mask_actions=False)
        if actions.item() == 1:
            val = math.exp(log_prob.item())
        else:
            val = 1 - math.exp(log_prob.item())
        if val > 0.2:
            val = 0.0
        y2.append(val)

    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts,amsmath}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['axes.titlepad'] = 2
    # plt.rcParams['xtick.major.pad'] = 0.5
    plt.rcParams['ytick.major.pad'] = 0.05
    plt.rcParams['axes.labelpad'] = 2
    plt.rcParams['axes.linewidth'] = 0.1
    fontsize = 15
    labelsize = 13.5
    plt.rcParams.update({'font.size': fontsize})

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(3.5, 2.9))

    # ylims = (0, 920)

    # Plot Avg Eval rewards Gensim
    colors = plt.cm.viridis(np.linspace(0.3, 1, 2))[-2:]
    ax.plot(x,
            y2, label=r"$\pi_{\theta}$ vs \textsc{StealthyAttacker}",
            ls='-', color=colors[0])
    ax.fill_between(x, y2, y,
                    alpha=0.35, color=colors[0])
    #
    ax.plot(x,
            y, label=r"$\pi_{\theta}$ vs \textsc{NoisyAttacker}",
            ls='-', color="r")
    # ax.fill_between(x, y2, np.zeros(len(y2)),
    #                 alpha=0.35, color="r")

    # if plot_opt:
    # ax.plot(x,
    #         [0.5] * len(x), label=r"0.5",
    #         color="black",
    #         linestyle="dashed")

    ax.set_title(r"$\pi_{\theta}(\text{stop}|z)$", fontsize=fontsize)
    ax.set_xlabel(r"\# login attempts $z$", fontsize=fontsize)
    ax.set_xlim(0, len(x))
    ax.set_ylim(0, 0.15)

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
    #           ncol=2, fancybox=True, shadow=True, fontsize=12)
    # ax.legend(loc="lower right", fontsize=fontsize, columnspacing = 0.5, labelspacing = 0.2, handletextpad = 0.4)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.23),
              ncol=1, fancybox=True, shadow=False, fontsize=12)

    ttl = ax.title
    ttl.set_position([.5, 1.05])
    ax.tick_params(axis='both', which='major', labelsize=labelsize, length=2.2, width=0.6)
    ax.tick_params(axis='both', which='minor', labelsize=labelsize, length=2.2, width=0.6)

    fig.tight_layout()
    # plt.show()
    plt.subplots_adjust(wspace=0, hspace=0, bottom=0.2)
    fig.savefig("logins_thresholds" + ".png", format="png", dpi=600)
    fig.savefig("logins_thresholds" + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    # plt.close(fig)


def action_pred_core_state_severe_warning(severe_alerts, warning_alerts, model, env):
    """
    Utility function for empirical threshold plots

    :param severe_alerts: number of severe alerts
    :param warning_alerts: number of warning alerts
    :param model: model to predict with
    :param env: the env
    :return: the predicted thresholds
    """
    z = []
    for i in range(len(severe_alerts)):
        z1 = []
        for j in range(len(severe_alerts[i])):
            state = np.array([severe_alerts[i][j],warning_alerts[i][j], 0, 10])
            actions, values, log_prob = model.defender_policy.forward(torch.tensor(np.array([state])).to("cpu"),
                                                                      deterministic=False,
                                                                      attacker=True, env=env, mask_actions=False)
            if actions.item() == 0:
                val = math.exp(log_prob.item())
            else:
                val = 1 - math.exp(log_prob.item())
            z1.append(val)
        z.append(z1)
    z = np.array(z)
    return z


def plot_alerts_threshold_multiple_steps() -> None:
    """
    Plots alerts thresholds

    :return: None
    """
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
    # env = gym.make("optimal-intrusion-response-v3")
    env = None
    # v3_load_path = "/Users/kimham/workspace/gym-optimal-intrusion-response/examples/v3/v3_results/v3/results_1/data/1620801616.3180108_0_4575_policy_network.zip"
    # v2_load_path = "/Users/kimham/workspace/gym-optimal-intrusion-response/examples/v3/v2_results/v2/results_2/data/1620760014.3964121_0_1150_policy_network.zip"
    experienced_attacker_load_path = "/Users/kimham/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_9/20_aug/results_experienced_attacker_128_neurons_2_hidden_layers_12k_batch/data/1629507805.8662815_999_400_policy_network.zip"
    novice_attacker_load_path = "/Users/kimham/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_9/20_aug/results_novice_attacker_128_neurons_2_hidden_layers_12k_batch/data/1629447739.1471612_999_400_policy_network.zip"
    expert_attacker_load_path = "/Users/kimham/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_9/20_aug/results_expert_attacker_128_neurons_2_hidden_layers_12k_batch/data/1629541110.809425_999_400_policy_network.zip"
    model = initialize_model(env, novice_attacker_load_path, "cpu", None)
    model2 = initialize_model(env, experienced_attacker_load_path, "cpu", None)
    model3 = initialize_model(env, expert_attacker_load_path, "cpu", None)
    num_alerts = np.arange(0, 50, 1)
    x = []
    y1_t_2 = []
    y2_t_2 = []
    y3_t_2 = []

    y1_t_6 = []
    y2_t_6 = []
    y3_t_6 = []

    y1_t_12 = []
    y2_t_12 = []
    y3_t_12 = []

    y1_t_24 = []
    y2_t_24 = []
    y3_t_24 = []

    for i in range(len(num_alerts)):
        x.append(i * 2)
        state_1_alerts = np.array([num_alerts[i], num_alerts[i], 0, 2])
        state_6_alerts = np.array([num_alerts[i], num_alerts[i], 0, 6])
        state_12_alerts = np.array([num_alerts[i], num_alerts[i], 0, 12])
        state_24_alerts = np.array([num_alerts[i], num_alerts[i], 0, 24])

        # Model 1
        actions_2_alerts, values_2_alerts, log_prob_2_alerts = model.defender_policy.forward(torch.tensor(np.array([state_1_alerts])).to("cpu"),
                                                                 deterministic=False,
                                                                  attacker=True, env=env, mask_actions=False)
        if actions_2_alerts.item() == 0:
            val = math.exp(log_prob_2_alerts.item())
        else:
            val = 1 - math.exp(log_prob_2_alerts.item())
        y1_t_2.append(val)

        actions_6_alerts, values_6_alerts, log_prob_6_alerts = model.defender_policy.forward(
            torch.tensor(np.array([state_6_alerts])).to("cpu"),
            deterministic=False,
            attacker=True, env=env, mask_actions=False)
        if actions_6_alerts.item() == 0:
            val = math.exp(log_prob_6_alerts.item())
        else:
            val = 1 - math.exp(log_prob_6_alerts.item())
        y1_t_6.append(val)

        actions_12_alerts, values_12_alerts, log_prob_12_alerts = model.defender_policy.forward(
            torch.tensor(np.array([state_12_alerts])).to("cpu"),
            deterministic=False,
            attacker=True, env=env, mask_actions=False)
        if actions_12_alerts.item() == 0:
            val = math.exp(log_prob_12_alerts.item())
        else:
            val = 1 - math.exp(log_prob_12_alerts.item())
        y1_t_12.append(val)

        actions_24_alerts, values_24_alerts, log_prob_24_alerts = model.defender_policy.forward(
            torch.tensor(np.array([state_24_alerts])).to("cpu"),
            deterministic=False,
            attacker=True, env=env, mask_actions=False)
        if actions_24_alerts.item() == 0:
            val = math.exp(log_prob_24_alerts.item())
        else:
            val = 1 - math.exp(log_prob_24_alerts.item())
        y1_t_24.append(val)


        # Model 2
        actions_2_alerts, values_2_alerts, log_prob_2_alerts = model2.defender_policy.forward(
            torch.tensor(np.array([state_1_alerts])).to("cpu"),
            deterministic=False,
            attacker=True, env=env, mask_actions=False)
        if actions_2_alerts.item() == 0:
            val = math.exp(log_prob_2_alerts.item())
        else:
            val = 1 - math.exp(log_prob_2_alerts.item())
        y2_t_2.append(val)

        actions_6_alerts, values_6_alerts, log_prob_6_alerts = model2.defender_policy.forward(
            torch.tensor(np.array([state_6_alerts])).to("cpu"),
            deterministic=False,
            attacker=True, env=env, mask_actions=False)
        if actions_6_alerts.item() == 0:
            val = math.exp(log_prob_6_alerts.item())
        else:
            val = 1 - math.exp(log_prob_6_alerts.item())
        y2_t_6.append(val)

        actions_12_alerts, values_12_alerts, log_prob_12_alerts = model2.defender_policy.forward(
            torch.tensor(np.array([state_12_alerts])).to("cpu"),
            deterministic=False,
            attacker=True, env=env, mask_actions=False)
        if actions_12_alerts.item() == 0:
            val = math.exp(log_prob_12_alerts.item())
        else:
            val = 1 - math.exp(log_prob_12_alerts.item())
        y2_t_12.append(val)

        actions_24_alerts, values_24_alerts, log_prob_24_alerts = model2.defender_policy.forward(
            torch.tensor(np.array([state_24_alerts])).to("cpu"),
            deterministic=False,
            attacker=True, env=env, mask_actions=False)
        if actions_24_alerts.item() == 0:
            val = math.exp(log_prob_24_alerts.item())
        else:
            val = 1 - math.exp(log_prob_24_alerts.item())
        y2_t_24.append(val)

        # Model 3
        actions_2_alerts, values_2_alerts, log_prob_2_alerts = model3.defender_policy.forward(
            torch.tensor(np.array([state_1_alerts])).to("cpu"),
            deterministic=False,
            attacker=True, env=env, mask_actions=False)
        if actions_2_alerts.item() == 0:
            val = math.exp(log_prob_2_alerts.item())
        else:
            val = 1 - math.exp(log_prob_2_alerts.item())
        y3_t_2.append(val)

        actions_6_alerts, values_6_alerts, log_prob_6_alerts = model3.defender_policy.forward(
            torch.tensor(np.array([state_6_alerts])).to("cpu"),
            deterministic=False,
            attacker=True, env=env, mask_actions=False)
        if actions_6_alerts.item() == 0:
            val = math.exp(log_prob_6_alerts.item())
        else:
            val = 1 - math.exp(log_prob_6_alerts.item())
        y3_t_6.append(val)

        actions_12_alerts, values_12_alerts, log_prob_12_alerts = model3.defender_policy.forward(
            torch.tensor(np.array([state_12_alerts])).to("cpu"),
            deterministic=False,
            attacker=True, env=env, mask_actions=False)
        if actions_12_alerts.item() == 0:
            val = math.exp(log_prob_12_alerts.item())
        else:
            val = 1 - math.exp(log_prob_12_alerts.item())
        y3_t_12.append(val)

        actions_24_alerts, values_24_alerts, log_prob_24_alerts = model3.defender_policy.forward(
            torch.tensor(np.array([state_24_alerts])).to("cpu"),
            deterministic=False,
            attacker=True, env=env, mask_actions=False)
        if actions_24_alerts.item() == 0:
            val = math.exp(log_prob_24_alerts.item())
        else:
            val = 1 - math.exp(log_prob_24_alerts.item())
        y3_t_24.append(val)

    print(x)
    print(y1_t_2)
    print(y2_t_6)
    print(y3_t_12)
    print(y3_t_24)

    fontsize = 8
    # figsize = (7.5, 3.25)
    figsize = (4.1, 2.9)
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

    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=figsize)

    # ylims = (0, 920)

    # Plot Avg Eval rewards Gensim
    colors = plt.cm.viridis(np.linspace(0.3, 1, 2))[-2:]
    ax[0][0].plot(x,
            y1_t_2, label=r"$\pi_{\theta}$ vs \textsc{Novice}",
            ls='-', color="#599ad3", lw=lw)
    ax[0][0].fill_between(x, y1_t_2, np.zeros(len(y2_t_2)),
                    alpha=0.35, color="#599ad3")

    ax[0][0].plot(x,
            y2_t_2, label=r"$\pi_{\theta}$ vs \textsc{Experienced}",
            ls='-', color="r", lw=lw)
    ax[0][0].fill_between(x, y2_t_2, y3_t_2,
                    alpha=0.35, color="r")

    ax[0][0].plot(x,
                  y3_t_2, label=r"$\pi_{\theta}$ vs \textsc{Expert}",
                  ls='-', color="#661D98", lw=lw)
    ax[0][0].fill_between(x, y3_t_2, y1_t_2,
                          alpha=0.35, color="#661D98")

    # if plot_opt:
    ax[0][0].plot(x, [0.5] * len(x), color="black", linestyle="dashed", lw=lw)

    ax[0][0].set_title(r"$\pi_{\theta}(\text{stop}|(x, y,z=0,t=2))$", fontsize=fontsize)
    #ax[0][0].set_xlabel(r"\# total alerts $x+y$", fontsize=labelsize)
    ax[0][0].set_xlim(0, len(x)*2)
    #ax.set_xlim(0, 100)
    ax[0][0].set_ylim(0, 1.1)

    # set the grid on
    #ax[0][0].grid('on')

    # tweak the axis labels
    xlab = ax[0][0].xaxis.get_label()
    ylab = ax[0][0].yaxis.get_label()

    xlab.set_size(labelsize)
    ylab.set_size(labelsize)

    # change the color of the top and right spines to opaque gray
    ax[0][0].spines['right'].set_color((.8, .8, .8))
    ax[0][0].spines['top'].set_color((.8, .8, .8))

    ttl = ax[0][0].title
    ttl.set_position([.5, 1.05])

    ax[0][0].tick_params(axis='both', which='major', labelsize=labelsize, length=2.2, width=0.6)
    ax[0][0].tick_params(axis='both', which='minor', labelsize=labelsize, length=2.2, width=0.6)
    ax[0][0].set_xticks([])


    # 11
    ax[0][1].plot(x,
                  y1_t_6, label=r"$\pi_{\theta}$ vs \textsc{Novice}",
                  ls='-', color="#599ad3", lw=lw)
    ax[0][1].fill_between(x, y1_t_6, np.zeros(len(y2_t_2)),
                          alpha=0.35, color="#599ad3")

    ax[0][1].plot(x,
                  y2_t_6, label=r"$\pi_{\theta}$ vs \textsc{Experienced}",
                  ls='-', color="r")
    ax[0][1].fill_between(x, y2_t_6, y3_t_6,
                          alpha=0.35, color="r")

    ax[0][1].plot(x,
                  y3_t_6, label=r"$\pi_{\theta}$ vs \textsc{Expert}",
                  ls='-', color="#661D98", lw=lw)
    ax[0][1].fill_between(x, y3_t_6, y1_t_6,
                          alpha=0.35, color="#661D98")

    # if plot_opt:
    ax[0][1].plot(x, [0.5] * len(x), color="black", linestyle="dashed", lw=lw)

    ax[0][1].set_title(r"$\pi_{\theta}(\text{stop}|(x, y,z=0,t=6))$", fontsize=fontsize)
    #ax[0][1].set_xlabel(r"\# total alerts $x+y$", fontsize=labelsize)
    ax[0][1].set_xlim(0, len(x) * 2)
    # ax.set_xlim(0, 100)
    ax[0][1].set_ylim(0, 1.1)

    # set the grid on
    #ax[0][1].grid('on')

    # tweak the axis labels
    xlab = ax[0][1].xaxis.get_label()
    ylab = ax[0][1].yaxis.get_label()

    xlab.set_size(labelsize)
    ylab.set_size(labelsize)

    # change the color of the top and right spines to opaque gray
    ax[0][1].spines['right'].set_color((.8, .8, .8))
    ax[0][1].spines['top'].set_color((.8, .8, .8))

    ttl = ax[0][1].title
    ttl.set_position([.5, 1.05])

    ax[0][1].tick_params(axis='both', which='major', labelsize=labelsize, length=2.2, width=0.6)
    ax[0][1].tick_params(axis='both', which='minor', labelsize=labelsize, length=2.2, width=0.6)
    ax[0][1].set_yticks([])
    ax[0][1].set_xticks([])

    # 22

    ax[1][0].plot(x,
                  y1_t_12, label=r"$\pi_{\theta}$ vs \textsc{Novice}",
                  ls='-', color="#599ad3", lw=lw)
    ax[1][0].fill_between(x, y1_t_12, np.zeros(len(y2_t_12)),
                          alpha=0.35, color="#599ad3")

    ax[1][0].plot(x,
                  y2_t_12, label=r"$\pi_{\theta}$ vs \textsc{Experienced}",
                  ls='-', color="r", lw=lw)
    ax[1][0].fill_between(x, y2_t_12, y3_t_12,
                          alpha=0.35, color="r")

    ax[1][0].plot(x,
                  y3_t_12, label=r"$\pi_{\theta}$ vs \textsc{Expert}",
                  ls='-', color="#661D98", lw=lw)
    ax[1][0].fill_between(x, y3_t_12, y1_t_12,
                          alpha=0.35, color="#661D98")

    # if plot_opt:
    ax[1][0].plot(x, [0.5] * len(x), color="black", linestyle="dashed", lw=lw)

    ax[1][0].set_title(r"$\pi_{\theta}(\text{stop}|(x, y,z=0,t=12))$", fontsize=fontsize)
    ax[1][0].set_xlabel(r"\# total alerts $x+y$", fontsize=labelsize)
    ax[1][0].set_xlim(0, len(x) * 2)
    # ax.set_xlim(0, 100)
    ax[1][0].set_ylim(0, 1.1)

    # set the grid on
    #ax[1][0].grid('on')

    # tweak the axis labels
    xlab = ax[1][0].xaxis.get_label()
    ylab = ax[1][0].yaxis.get_label()

    xlab.set_size(labelsize)
    ylab.set_size(labelsize)

    # change the color of the top and right spines to opaque gray
    ax[1][0].spines['right'].set_color((.8, .8, .8))
    ax[1][0].spines['top'].set_color((.8, .8, .8))

    ttl = ax[1][0].title
    ttl.set_position([.5, 1.05])

    ax[1][0].tick_params(axis='both', which='major', labelsize=labelsize, length=2.2, width=0.6)
    ax[1][0].tick_params(axis='both', which='minor', labelsize=labelsize, length=2.2, width=0.6)

    ## 33
    ax[1][1].plot(x,
                  y1_t_12, label=r"$\pi_{\theta}$ vs \textsc{Novice}",
                  ls='-', color="#599ad3", lw=lw)
    ax[1][1].fill_between(x, y1_t_12, np.zeros(len(y2_t_12)),
                          alpha=0.35, color="#599ad3")

    ax[1][1].plot(x,
                  y2_t_12, label=r"$\pi_{\theta}$ vs \textsc{Experienced}",
                  ls='-', color="r", lw=lw)
    ax[1][1].fill_between(x, y2_t_12, y3_t_12,
                          alpha=0.35, color="r")

    ax[1][1].plot(x,
                  y3_t_12, label=r"$\pi_{\theta}$ vs \textsc{Expert}",
                  ls='-', color="#661D98", lw=lw)
    ax[1][1].fill_between(x, y3_t_12, y1_t_12,
                          alpha=0.35, color="#661D98")

    # if plot_opt:
    ax[1][1].plot(x, [0.5] * len(x), color="black", linestyle="dashed", lw=lw)

    ax[1][1].set_title(r"$\pi_{\theta}(\text{stop}|(x, y,z=0,t=24))$", fontsize=fontsize)
    ax[1][1].set_xlabel(r"\# total alerts $x+y$", fontsize=labelsize)
    ax[1][1].set_xlim(0, len(x) * 2)
    # ax.set_xlim(0, 100)
    ax[1][1].set_ylim(0, 1.1)

    # set the grid on
    #ax[1][1].grid('on')

    # tweak the axis labels
    xlab = ax[1][1].xaxis.get_label()
    ylab = ax[1][1].yaxis.get_label()

    xlab.set_size(labelsize)
    ylab.set_size(labelsize)

    # change the color of the top and right spines to opaque gray
    ax[1][1].spines['right'].set_color((.8, .8, .8))
    ax[1][1].spines['top'].set_color((.8, .8, .8))

    ttl = ax[1][1].title
    ttl.set_position([.5, 1.05])

    ax[1][1].tick_params(axis='both', which='major', labelsize=labelsize, length=2.2, width=0.6)
    ax[1][1].tick_params(axis='both', which='minor', labelsize=labelsize, length=2.2, width=0.6)

    ax[1][1].set_yticks([])

    # ax[0][0].legend(loc='upper center', bbox_to_anchor=(0.9, -1),
    #                 ncol=3, fancybox=True, shadow=False, fontsize=fontsize)

    handles, labels = ax[0][0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 0.09),
               ncol=4, fancybox=True, shadow=False, handletextpad=0.4, labelspacing=0.5, columnspacing=0.65)

    fig.tight_layout()
    # fig.subplots_adjust(wspace=wspace, hspace=hspace, top=top, bottom=bottom)
    fig.subplots_adjust(wspace=wspace, hspace=hspace, bottom=bottom)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)


def switching_curve_val(severe_alerts, warning_alerts):
    z = []
    for i in range(len(severe_alerts)):
        z1 = []
        for j in range(len(severe_alerts[i])):
            thresholds = []
            match = False
            for t in range(24, 2, -1):
                # alpha = 19 + t* 2.7
                if t <= 12:
                    alpha = 19 + (t - 2)*2.7
                else:
                    alpha = 46
                thresholds.append(alpha)
                if (severe_alerts[i][j] + warning_alerts[i][j]) >= alpha:
                    # print("match:{}, alerts:{}, thresh:{}".format(t, severe_alerts[i][j] + warning_alerts[i][j], alpha))
                    z1.append(t)
                    match = True
                    break
            if not match:
                z1.append(0)
            # state = np.array([severe_alerts[i][j],warning_alerts[i][j], 0, 10])
            # actions, values, log_prob = model.defender_policy.forward(torch.tensor(np.array([state])).to("cpu"),
            #                                                           deterministic=False,
            #                                                           attacker=True, env=env, mask_actions=False)
            # if actions.item() == 0:
            #     val = math.exp(log_prob.item())
            # else:
            #     val = 1 - math.exp(log_prob.item())
            #if t > 0 and (severe_alerts[i][j] + warning_alerts[i][j])/t
            # t = (severe_alerts[i][j] + warning_alerts[i][j])/30

            # z1.append(t)
        z.append(z1)
    z = np.array(z)
    return z

def switching_curve_val_2(severe_alerts, warning_alerts, model, env):
    z = []
    for i in range(len(severe_alerts)):
        z1 = []
        for j in range(len(severe_alerts[i])):
            min_t = 100
            for t in range(100):
                state = np.array([severe_alerts[i][j], warning_alerts[i][j], 0, t])
                actions, values, log_prob = model.defender_policy.forward(torch.tensor(np.array([state])).to("cpu"),deterministic=False, attacker=True, env=env, mask_actions=False)
                if actions.item() == 0:
                    min_t = t
                    break
            # state = np.array([severe_alerts[i][j],warning_alerts[i][j], 0, 10])
            # actions, values, log_prob = model.defender_policy.forward(torch.tensor(np.array([state])).to("cpu"),
            #                                                           deterministic=False,
            #                                                           attacker=True, env=env, mask_actions=False)
            # if actions.item() == 0:
            #     val = math.exp(log_prob.item())
            # else:
            #     val = 1 - math.exp(log_prob.item())
            #if t > 0 and (severe_alerts[i][j] + warning_alerts[i][j])/t
            # t = (severe_alerts[i][j] + warning_alerts[i][j])/30
            z1.append(min_t)
        z.append(z1)
    z = np.array(z)
    return z


def plot_switching_curve_3d():
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
    env = None
    experienced_attacker_load_path = "/Users/kimham/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_9/20_aug/results_experienced_attacker_128_neurons_2_hidden_layers_12k_batch/data/1629507805.8662815_999_400_policy_network.zip"
    novice_attacker_load_path = "/Users/kimham/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_9/20_aug/results_novice_attacker_128_neurons_2_hidden_layers_12k_batch/data/1629447739.1471612_999_400_policy_network.zip"
    expert_attacker_load_path = "/Users/kimham/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_9/20_aug/results_expert_attacker_128_neurons_2_hidden_layers_12k_batch/data/1629541110.809425_999_400_policy_network.zip"
    # model = initialize_model(env, novice_attacker_load_path, "cpu", None)
    # model2 = initialize_model(env, experienced_attacker_load_path, "cpu", None)
    # model3 = initialize_model(env, expert_attacker_load_path, "cpu", None)

    num_severe_alerts = np.arange(50, 0, -1)
    num_warning_alerts = np.arange(0, 50, 1)

    x_0= []
    y_0 = []
    t_0 = []
    x_1 = []
    y_1 = []
    t_1 = []
    for x in range(50, 0,-10):
        for y in range(0, 50, 10):
            for t in range(0, 26, 5):
                if t <= 12:
                    alpha = 19 + (t - 2)*2.7
                else:
                    alpha = 46
                if (x + y) >= alpha:
                    x_1.append(x)
                    y_1.append(y)
                    t_1.append(t)
                else:
                    x_0.append(x)
                    y_0.append(y)
                    t_0.append(t)


    # sev, warn = np.meshgrid(num_severe_alerts, num_warning_alerts)
    # t_vals = switching_curve_val(sev, warn)
    # t_vals = switching_curve_val_2(sev, warn, model, env)

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
    fig, ax = plt.subplots(nrows=1, ncols=1, subplot_kw={'projection': '3d'}, figsize=(4.5, 3))
    #(3.5, 1.6)
    #(5, 3.5)
    # ax.plot_surface(sev, warn, t_vals, cmap='Blues', linewidth=0.3,
    #                 alpha=0.8, edgecolor='k', rstride=12, cstride=12)
    ax.scatter(x_0, y_0, t_0, alpha=0.8, edgecolor='k', s=30, marker="p", c="#599ad3")
    ax.scatter(x_1, y_1, t_1, alpha=0.8, edgecolor='k', s=30, marker="o", c='r')
    # ax.set_title(r"$\pi_{\theta}(\text{stop} | x, y)$ vs \textsc{StealthyAttacker}", fontsize=fontsize)
    ax.set_xlabel(r"$y$")
    ax.set_ylabel(r"$x$")
    ax.set_zlabel(r"$t$")
    ax.xaxis.labelpad = 0
    ax.yaxis.labelpad = 0
    ax.zaxis.labelpad = -5
    # ax.set_xticks(np.arange(0, 200 + 1, 50))
    # ax.set_yticks(np.arange(0, 200+1, 50))
    ax.set_xticks(np.arange(0, 50 + 1, 10))
    ax.set_yticks(np.arange(0, 50 + 1, 10))
    ax.set_zticks(np.arange(0, 25 + 1, 5))
    xlab = ax.xaxis.get_label()
    ylab = ax.yaxis.get_label()
    zlab = ax.zaxis.get_label()
    xlab.set_size(fontsize)
    ylab.set_size(fontsize)
    zlab.set_size(fontsize)
    ax.tick_params(axis='both', which='major', labelsize=labelsize, length=2.2, width=0.6)
    ax.tick_params(axis='both', which='minor', labelsize=labelsize, length=2.2, width=0.6)
    scatter1_proxy = matplotlib.lines.Line2D([0], [0], linestyle="none", c="#599ad3", marker='p', alpha=0.8, markeredgecolor="k")
    scatter2_proxy = matplotlib.lines.Line2D([0], [0], linestyle="none", c='r', marker='o', alpha=0.8, markeredgecolor="k")
    ax.legend([scatter1_proxy, scatter2_proxy], ['continue', 'stop'], numpoints=1, handletextpad=0.4,
              labelspacing=0.5, columnspacing=0.65, ncol=2,
              bbox_to_anchor=(0.85, -0.02))
    fig.tight_layout()
    plt.subplots_adjust(bottom=0.55)
    # plt.show()
    # fig.savefig("alerts_stopping" + ".png", format="png", dpi=600)
    fig.savefig("switching_curve_3d" + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)


# script entrypoint
if __name__ == '__main__':
    # model = initialize_model(env, load_path, "cuda:0", None)
    # plot_3d()
    # plot_logins_threshold()
    # plot_3d_2()
    # plot_alerts_threshold_multiple_steps()
    plot_switching_curve_3d()
    # plot_logins_threshold()
