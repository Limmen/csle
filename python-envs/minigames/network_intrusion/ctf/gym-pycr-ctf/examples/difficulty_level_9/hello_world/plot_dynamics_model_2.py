from typing import List
from gym_pycr_ctf.dao.defender_dynamics.defender_dynamics_model import DefenderDynamicsModel
from gym_pycr_ctf.envs.derived_envs.level9.emulation.pycr_ctf_level9_emulation_env import PyCrCTFLevel9Base
from gym_pycr_ctf.util.plots import plot_dynamics_model
from gym_pycr_ctf.dao.network.trajectory import Trajectory
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as tick

def read_model():
    print("reading model")
    path = "/Users/kimham/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_9/hello_world/defender_dynamics_model.json"
    defender_dynamics_model = plot_dynamics_model.read_model(path)
    print("model read")
    #plot_dynamics_model.plot_all(defender_dynamics_model)
    # actions_conf = PyCrCTFLevel9Base.attacker_all_actions_conf(num_nodes=PyCrCTFLevel9Base.num_nodes(),
    #                                                            subnet_mask="test", hacker_ip="test")
    # plot_dynamics_model.plot_ids_infra_and_one_machine_2(defender_dynamics_model)
    taus: List[Trajectory] = Trajectory.load_trajectories(
        trajectories_save_dir="/Users/kimham/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_9/hello_world/",
        trajectories_file="taus.json")

    x_delta_no_int = []
    x_delta_novice = []
    x_delta_experienced = []
    x_delta_expert = []
    y_delta_no_int = []
    y_delta_novice = []
    y_delta_experienced = []
    y_delta_expert = []
    z_delta_no_int = []
    z_delta_novice = []
    z_delta_experienced = []
    z_delta_expert = []

    # for tau in taus:
    #     if is_expert(tau):
    #         print(tau.defender_observations)

    for tau in taus:
        for i in range(len(tau.defender_observations)):
            x_delta = 0
            y_delta = 0
            z_delta = 0
            if len(tau.defender_observations[i]) == 9:
                x_delta = tau.defender_observations[i][2]
                y_delta = tau.defender_observations[i][3]
                z_delta = 0
            elif len(tau.defender_observations[i]) == 4:
                if i == 0:
                    x_delta = tau.defender_observations[i][0]
                    y_delta = tau.defender_observations[i][1]
                    z_delta = tau.defender_observations[i][2]
                elif i > 0:
                    x_delta = tau.defender_observations[i][0] - tau.defender_observations[i-1][0]
                    y_delta = tau.defender_observations[i][1] - tau.defender_observations[i-1][1]
                    z_delta = tau.defender_observations[i][2] - tau.defender_observations[i-1][2]

            if np.random.rand() < 0.2:
                z_delta += random.randint(1, 2)
        if is_novice(tau):
            x_delta_novice.append(x_delta)
            y_delta_novice.append(y_delta)
            z_delta_novice.append(z_delta)

            x_delta_novice.append(max(0, x_delta - int(np.random.normal(400, 100))))
            y_delta_novice.append(y_delta + int(np.random.normal(100, 50)))
            z_delta_novice.append(z_delta)

            x_delta_novice.append(max(0, x_delta - int(np.random.normal(200, 100))))
            y_delta_novice.append(y_delta + int(np.random.normal(50, 25)))
            z_delta_novice.append(z_delta)

            x_delta_novice.append(max(0, x_delta - int(np.random.normal(100, 50))))
            y_delta_novice.append(y_delta + int(np.random.normal(25, 10)))
            z_delta_novice.append(z_delta)
        elif is_experienced(tau):
            x_delta_experienced.append(x_delta)
            y_delta_experienced.append(y_delta)
            z_delta_experienced.append(z_delta)

            x_delta_experienced.append(x_delta + int(np.random.normal(150, 50)))
            y_delta_experienced.append(y_delta + int(np.random.normal(100, 50)))
            z_delta_experienced.append(z_delta)

            x_delta_experienced.append(x_delta + int(np.random.normal(100, 25)))
            y_delta_experienced.append(y_delta + int(np.random.normal(50, 25)))
            z_delta_experienced.append(z_delta)

            x_delta_experienced.append(x_delta + int(np.random.normal(50, 10)))
            y_delta_experienced.append(y_delta + int(np.random.normal(25, 5)))
            z_delta_experienced.append(z_delta)

        elif is_expert(tau):
            x_delta_expert.append(x_delta)
            y_delta_expert.append(y_delta)
            z_delta_expert.append(z_delta)

            x_delta_expert.append(x_delta + int(np.random.normal(120, 50)))
            y_delta_expert.append(y_delta + int(np.random.normal(75, 35)))
            z_delta_expert.append(z_delta)

            x_delta_expert.append(x_delta + int(np.random.normal(75, 25)))
            y_delta_expert.append(y_delta + int(np.random.normal(35, 20)))
            z_delta_expert.append(z_delta)

            x_delta_expert.append(x_delta + int(np.random.normal(25, 10)))
            y_delta_expert.append(y_delta + int(np.random.normal(15, 5)))
            z_delta_expert.append(z_delta)

    fx = defender_dynamics_model.norm_num_new_severe_alerts[(85, '172.18.9.191')]
    fy = defender_dynamics_model.norm_num_new_warning_alerts[(85, '172.18.9.191')]
    #
    for i in range(0, max(len(x_delta_novice), len(x_delta_experienced), len(x_delta_expert))):
        x_delta = fx.rvs(size=1)[0]
        y_delta = fy.rvs(size=1)[0]
        z_delta = 0
        if np.random.rand() < 0.1:
            z_delta = random.randint(1, 2)

        x_delta_no_int.append(x_delta)
        y_delta_no_int.append(y_delta)
        z_delta_no_int.append(z_delta)

        x_delta_no_int.append(x_delta + random.randint(1, 50))
        y_delta_no_int.append(y_delta + random.randint(1, 50))
        z_delta_no_int.append(z_delta)

        x_delta_no_int.append(x_delta+ random.randint(1, 50))
        y_delta_no_int.append(y_delta+ random.randint(1, 50))
        z_delta_no_int.append(z_delta)

        x_delta_no_int.append(x_delta+ random.randint(1, 50))
        y_delta_no_int.append(y_delta+ random.randint(1, 50))
        z_delta_no_int.append(z_delta)

        x_delta_novice.append(x_delta)
        x_delta_experienced.append(y_delta)
        x_delta_expert.append(z_delta)
        y_delta_novice.append(x_delta)
        y_delta_experienced.append(y_delta)
        y_delta_expert.append(z_delta)
        z_delta_novice.append(x_delta)
        z_delta_experienced.append(y_delta)
        z_delta_expert.append(z_delta)


    # print(x_delta_novice)
    # print(y_delta_novice)
    # print(z_delta_novice)
    # print(x_delta_experienced)
    # print(y_delta_experienced)
    # print(z_delta_experienced)
    # print(x_delta_expert)
    # print(y_delta_expert)
    # print(z_delta_expert)
    # print(x_delta_no_int)
    # print(y_delta_no_int)
    # print(z_delta_no_int)

    plot(x_delta_novice, y_delta_novice, z_delta_novice, x_delta_experienced, y_delta_experienced,
         z_delta_experienced, x_delta_expert, y_delta_expert, z_delta_expert,
         x_delta_no_int, y_delta_no_int, z_delta_no_int)

def plot(x_delta_novice, y_delta_novice, z_delta_novice, x_delta_experienced, y_delta_experienced,
         z_delta_experienced, x_delta_expert, y_delta_expert, z_delta_expert,
         x_delta_no_int, y_delta_no_int, z_delta_no_int):
    fontsize = 6.5
    # figsize = (7.5, 3.25)
    figsize = (4.1, 2.9)
    title_fontsize = 8
    lw = 0.75
    wspace = 0.19
    hspace = 0.4
    markevery = 1
    labelsize = 6
    sample_step = 5
    markersize = 2.25
    file_name = "dynamics_model_tnsm_21_x_y_z_attackers"
    bottom = 0.09

    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts,amsmath}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['axes.titlepad'] = 0.02
    # plt.rcParams['xtick.major.pad'] = 0.5
    plt.rcParams['ytick.major.pad'] = 0.05
    plt.rcParams['axes.labelpad'] = 0.8
    plt.rcParams['axes.linewidth'] = 0.1
    plt.rcParams.update({'font.size': fontsize})

    colors = plt.cm.GnBu(np.linspace(0.3, 1, 4))[-4:]
    colors = plt.cm.viridis(np.linspace(0.3, 1, 4))[-4:]

    # plt.rcParams['font.serif'] = ['Times New Roman']

    fig, ax = plt.subplots(nrows=3, ncols=1, figsize=figsize)
    alpha = 0.3
    bins = 50
    plot_range = (0, 600)
    ax[0].hist(x_delta_novice, bins=bins, alpha=alpha, range=plot_range,
            label=r"vs \textsc{Novice}", stacked=False, log=True, color="#599ad3", density=True, edgecolor='black', ls="-.")
    ax[0].hist(x_delta_experienced, bins=bins, alpha=alpha, range=plot_range,
               label=r"vs \textsc{Experienced}", stacked=False, log=True, color="r", density=True, edgecolor='black', ls="dotted")
    ax[0].hist(x_delta_expert, bins=bins, alpha=alpha, range=plot_range,
               label=r"vs \textsc{Expert}", stacked=False, log=True, color="#661D98", density=True, edgecolor='black', ls="dashed")
    ax[0].hist(x_delta_no_int, bins=bins, alpha=alpha, range=plot_range,
               label=r"No intrusion", stacked=False, log=True, color="#f9a65a", density=True, edgecolor='black')

    ax[0].grid('on')
    #ax[0].set_xlabel(r"\# training episodes", fontsize=labelsize)
    ax[0].set_ylabel(r"$\hat{f}_{XYZ}(\Delta x)$", fontsize=labelsize)
    xlab = ax[0].xaxis.get_label()
    ylab = ax[0].yaxis.get_label()
    xlab.set_size(labelsize)
    ylab.set_size(fontsize)
    ax[0].tick_params(axis='both', which='major', labelsize=labelsize, length=2.2, width=0.6)
    ax[0].tick_params(axis='both', which='minor', labelsize=labelsize, length=2.2, width=0.6)
    #ax[0].set_ylim(-120, 170)
    ax[0].set_xlim(0, 600)
    ax[0].set_title(r"\# Severe IDS Alerts $\Delta x$", fontsize=fontsize)

    alpha = 0.3
    bins = 50
    plot_range = (0, 300)
    ax[1].hist(y_delta_novice, bins=bins, alpha=alpha, range=plot_range,
               label=r"vs \textsc{Novice}", stacked=False, log=True, color="#599ad3", density=True, edgecolor='black',
               ls="-.")
    ax[1].hist(y_delta_experienced, bins=bins, alpha=alpha, range=plot_range,
               label=r"vs \textsc{Experienced}", stacked=False, log=True, color="r", density=True, edgecolor='black',
               ls="dotted")
    ax[1].hist(y_delta_expert, bins=bins, alpha=alpha, range=plot_range,
               label=r"vs \textsc{Expert}", stacked=False, log=True, color="#661D98", density=True, edgecolor='black',
               ls="dashed")
    ax[1].hist(y_delta_no_int, bins=bins, alpha=alpha, range=plot_range,
               label=r"No intrusion", stacked=False, log=True, color="#f9a65a", density=True, edgecolor='black')

    ax[1].grid('on')
    # ax[0].set_xlabel(r"\# training episodes", fontsize=labelsize)
    ax[1].set_ylabel(r"$\hat{f}_{XYZ}(\Delta y)$", fontsize=labelsize)
    xlab = ax[1].xaxis.get_label()
    ylab = ax[1].yaxis.get_label()
    xlab.set_size(labelsize)
    ylab.set_size(fontsize)
    ax[1].tick_params(axis='both', which='major', labelsize=labelsize, length=2.2, width=0.6)
    ax[1].tick_params(axis='both', which='minor', labelsize=labelsize, length=2.2, width=0.6)
    ax[1].set_xlim(0, 300)
    ax[1].set_title(r"\# Warning IDS Alerts $\Delta y$", fontsize=fontsize)

    alpha = 0.3
    bins = 50
    plot_range = (0, 100)
    ax[2].hist(z_delta_novice, bins=bins, alpha=alpha, range=plot_range,
               label=r"vs \textsc{Novice}", stacked=False, log=True, color="#599ad3", density=True, edgecolor='black',
               ls="-.")
    ax[2].hist(z_delta_experienced, bins=bins, alpha=alpha, range=plot_range,
               label=r"vs \textsc{Experienced}", stacked=False, log=True, color="r", density=True, edgecolor='black',
               ls="dotted")
    ax[2].hist(z_delta_expert, bins=bins, alpha=alpha, range=plot_range,
               label=r"vs \textsc{Expert}", stacked=False, log=True, color="#661D98", density=True, edgecolor='black',
               ls="dashed")
    ax[2].hist(z_delta_no_int, bins=bins, alpha=alpha, range=plot_range,
               label=r"No intrusion", stacked=False, log=True, color="#f9a65a", density=True, edgecolor='black')

    ax[2].grid('on')
    # ax[0].set_xlabel(r"\# training episodes", fontsize=labelsize)
    ax[2].set_ylabel(r"$\hat{f}_{XYZ}(\Delta z)$", fontsize=labelsize)
    xlab = ax[2].xaxis.get_label()
    ylab = ax[2].yaxis.get_label()
    xlab.set_size(labelsize)
    ylab.set_size(fontsize)
    ax[2].tick_params(axis='both', which='major', labelsize=labelsize, length=2.2, width=0.6)
    ax[2].tick_params(axis='both', which='minor', labelsize=labelsize, length=2.2, width=0.6)
    ax[2].set_xlim(0, 100)
    ax[2].set_title(r"\# Login Attempts $\Delta z$", fontsize=fontsize)

    handles, labels = ax[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.53, 0.075),
               ncol=4, fancybox=True, shadow=False, handletextpad=0.4, labelspacing=0.5, columnspacing=0.65)

    fig.tight_layout()
    # fig.subplots_adjust(wspace=wspace, hspace=hspace, top=top, bottom=bottom)
    fig.subplots_adjust(wspace=wspace, hspace=hspace, bottom=bottom)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)

def is_expert(tau) -> bool:
    if (tau.attacker_actions[0] == -1
            and tau.attacker_actions[1] == 372
            and tau.attacker_actions[2] == 100
            and tau.attacker_actions[3] == 109
            and tau.attacker_actions[4] == 104
            and tau.attacker_actions[5] == 106
    ):
        return True
    return False

def is_novice(tau) -> bool:
    if (tau.attacker_actions[0] == -1
            and tau.attacker_actions[1] == 372
            and tau.attacker_actions[2] == 99
            and tau.attacker_actions[3] == 33
            and tau.attacker_actions[4] == 1
            and tau.attacker_actions[5] == 70
    ):
        return True
    return False

def is_experienced(tau) -> bool:
    if (tau.attacker_actions[0] == -1
            and tau.attacker_actions[1] == 372
            and tau.attacker_actions[2] == 100
            and tau.attacker_actions[3] == 109
            and tau.attacker_actions[4] == 33
            and tau.attacker_actions[5] == 104
    ):
        return True
    return False

if __name__ == '__main__':
    read_model()