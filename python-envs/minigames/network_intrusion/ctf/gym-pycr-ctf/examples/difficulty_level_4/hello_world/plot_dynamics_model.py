from gym_pycr_ctf.dao.defender_dynamics.defender_dynamics_model import DefenderDynamicsModel
from gym_pycr_ctf.envs.derived_envs.level4.emulation.pycr_ctf_level4_emulation_env import PyCrCTFLevel4Base
from gym_pycr_ctf.dao.action.attacker.attacker_action_id import AttackerActionId
from gym_pycr_ctf.dao.action.attacker.attacker_action import AttackerAction
import numpy as np
import matplotlib.pyplot as plt

def read_model():
    model_path = "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_4/hello_world/defender_dynamics_model.json"
    defender_dynamics_model = DefenderDynamicsModel()
    defender_dynamics_model.read_model_path(model_path)
    defender_dynamics_model.normalize()
    return defender_dynamics_model

def plot_all():
    defender_dynamics_model = read_model()
    action_cfg = PyCrCTFLevel4Base.attacker_all_actions_conf(num_nodes=10, subnet_mask="test", hacker_ip = "test")

    # for k,v in defender_dynamics_model.norm_num_new_alerts.items():
    #     action_id_val = k[0]
    #     action_id = AttackerActionId(action_id_val)
    #     action_dto = action_cfg.get_action_by_id(action_id=action_id)
    #     logged_in_ips = k[1]
    #     print(len(logged_in_ips.split("_")))
    #     print(logged_in_ips.split("_"))
    #     dist = defender_dynamics_model.norm_num_new_alerts[k]
    #     xk = np.arange(dist.support()[0], dist.support()[1])
    #     xk = np.array(list(filter(lambda x: dist.pmf(x) > 0, xk.tolist())))
    #     plot(dist, xk, k, action_dto, logged_in_ips, subtitle="IDS Alerts",
    #          xlabel=r"\# IDS Alerts",
    #          ylabel=r"$\mathbb[P][alerts]$")

    total_xks = []
    total_dists = []
    total_a_ids = []
    total_b_ids = []
    min_support = 0
    max_support = 0

    action_ids = {}
    action_count = 0
    state_ids = {}
    state_count = 0

    # for k, v in defender_dynamics_model.norm_num_new_alerts.items():
    #     action_id_val = k[0]
    #     action_id = AttackerActionId(action_id_val)
    #     action_dto = action_cfg.get_action_by_id(action_id=action_id)
    #     logged_in_ips = k[1]
    #
    #     if action_id_val not in action_ids:
    #         action_ids[action_id_val] = action_count
    #         action_count += 1
    #
    #     if logged_in_ips not in total_b_ids:
    #         state_ids[logged_in_ips] = state_count
    #         state_count += 1
    #
    #     total_a_ids.append(action_ids[action_id_val])
    #     total_b_ids.append(state_ids[logged_in_ips])
    #
    #     dist = defender_dynamics_model.norm_num_new_alerts[k]
    #     if dist.support()[0] < min_support:
    #         min_support = dist.support()[0]
    #     if dist.support()[0] > max_support:
    #         max_support = dist.support()[1]
    #
    #     xk = np.arange(dist.support()[0], dist.support()[1])
    #     xk = np.array(list(filter(lambda x: dist.pmf(x) > 0, xk.tolist())))
    #     total_xks.append(xk)
    #     total_dists.append(dist)
    #
    # plot_multiple(total_dists, total_xks, min_support, max_support, total_a_ids, total_b_ids,
    #               subtitle="IDS Alerts",
    #      xlabel=r"\# IDS Alerts",
    #      ylabel=r"$\mathbb{P}[ \cdot | (b_i, a_i)]$", file_name="ids_alerts")

    row_dists = []
    row_xks = []
    row_a_ids = []
    row_b_ids = []
    row_subtitles = []
    row_x_labels = []
    row_y_labels = []

    subtitle = "IDS Alerts"
    xlabel = r"\# IDS Alerts"
    ylabel = r"$\mathbb{P}[ \cdot | (b_i, a_i)]$"
    total_dists, total_xks, total_a_ids, total_b_ids = plot_specific_dynamics(defender_dynamics_model.norm_num_new_alerts, action_cfg,
                           subtitle=subtitle,
                           xlabel=xlabel,
                           ylabel=ylabel,
                           file_name="ids_alerts"
                           )
    row_dists.append(total_dists)
    row_xks.append(total_xks)
    row_a_ids.append(total_a_ids)
    row_b_ids.append(total_b_ids)
    row_subtitles.append(subtitle)
    row_x_labels.append(xlabel)
    row_y_labels.append(ylabel)

    subtitle = "Severe IDS Alerts"
    xlabel = r"\# Severe IDS Alerts"
    ylabel = r"$\mathbb{P}[ \cdot | (b_i, a_i)]$"
    total_dists, total_xks, total_a_ids, total_b_ids = plot_specific_dynamics(defender_dynamics_model.norm_num_new_severe_alerts, action_cfg,
                           subtitle=subtitle,
                           xlabel=xlabel,
                           ylabel=ylabel,
                           file_name="severe_ids_alerts"
                           )

    row_dists.append(total_dists)
    row_xks.append(total_xks)
    row_a_ids.append(total_a_ids)
    row_b_ids.append(total_b_ids)
    row_subtitles.append(subtitle)
    row_x_labels.append(xlabel)
    row_y_labels.append(ylabel)

    subtitle = "Warning IDS Alerts"
    xlabel = r"\# Warning IDS Alerts"
    ylabel = r"$\mathbb{P}[ \cdot | (b_i, a_i)]$"
    total_dists, total_xks, total_a_ids, total_b_ids= plot_specific_dynamics(defender_dynamics_model.norm_num_new_warning_alerts, action_cfg,
                           subtitle=subtitle,
                           xlabel=xlabel,
                           ylabel=ylabel,
                           file_name="warning_ids_alerts"
                           )

    row_dists.append(total_dists)
    row_xks.append(total_xks)
    row_a_ids.append(total_a_ids)
    row_b_ids.append(total_b_ids)
    row_subtitles.append(subtitle)
    row_x_labels.append(xlabel)
    row_y_labels.append(ylabel)

    subtitle = "IDS Alert Priorities"
    xlabel = r"\# IDS Alert Priorities"
    ylabel = r"$\mathbb{P}[ \cdot | (b_i, a_i)]$"
    total_dists, total_xks, total_a_ids, total_b_ids= plot_specific_dynamics(defender_dynamics_model.norm_num_new_priority, action_cfg,
                           subtitle=subtitle,
                           xlabel=xlabel,
                           ylabel=ylabel,
                           file_name="priority_ids_alerts"
                           )

    row_dists.append(total_dists)
    row_xks.append(total_xks)
    row_a_ids.append(total_a_ids)
    row_b_ids.append(total_b_ids)
    row_subtitles.append(subtitle)
    row_x_labels.append(xlabel)
    row_y_labels.append(ylabel)

    plot_ids_dynamics_two_row(row_dists, row_xks, row_a_ids, row_b_ids, row_subtitles, row_x_labels, row_y_labels,
                          "ids_dynamics_row")


def plot_specific_dynamics(data_dict, action_cfg, subtitle, xlabel, ylabel, file_name):
    total_xks = []
    total_dists = []
    total_a_ids = []
    total_b_ids = []
    min_support = 0
    max_support = 0

    action_ids = {}
    action_count = 0
    state_ids = {}
    state_count = 0

    for k, v in data_dict.items():
        action_id_val = k[0]
        action_id = AttackerActionId(action_id_val)
        action_dto = action_cfg.get_action_by_id(action_id=action_id)
        logged_in_ips = k[1]

        if action_id_val not in action_ids:
            action_ids[action_id_val] = action_count
            action_count += 1

        if logged_in_ips not in total_b_ids:
            state_ids[logged_in_ips] = state_count
            state_count += 1

        total_a_ids.append(action_ids[action_id_val])
        total_b_ids.append(state_ids[logged_in_ips])

        dist = data_dict[k]
        if dist.support()[0] < min_support:
            min_support = dist.support()[0]
        if dist.support()[0] > max_support:
            max_support = dist.support()[1]

        xk = np.arange(dist.support()[0], dist.support()[1])
        xk = np.array(list(filter(lambda x: dist.pmf(x) > 0, xk.tolist())))
        total_xks.append(xk)
        total_dists.append(dist)

    # plot_multiple(total_dists, total_xks, min_support, max_support, total_a_ids, total_b_ids,
    #               subtitle=subtitle,
    #               xlabel=xlabel,
    #               ylabel=ylabel, file_name=file_name)

    return total_dists, total_xks, total_a_ids, total_b_ids

def plot_ids_dynamics_two_row(dists, xks,
                              a_ids, b_ids,
                              subtitles,
                              xlabels, ylabels, file_name):
    cm = plt.cm.get_cmap('RdYlBu_r')
    colors = plt.cm.GnBu(np.linspace(0.3, 1, 45))[-45:]
    colors = plt.cm.viridis(np.linspace(0.3, 1, 45))[-45:]

    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    plt.rcParams['font.family'] = ['serif']
    # plt.rcParams['font.serif'] = ['Times New Roman']
    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(6, 4.5))
    plt.rcParams.update({'font.size': 10})

    k = 0
    row = 0
    for j in range(len(dists)):
        title = r"PMF: $\mathbb{P}[b^{\prime} | b, a]$ - " + subtitles[j]
        if j > 1 and row == 0:
            row = 1
            k = 0


        #l = "r$(b_{" + b_ids[i] + "},a_{" + a_ids[i] + "})$"
        for i in range(len(xks[j])):
            if i < 2:
                label = "$(b_{" + str(b_ids[j][i]) + "},a_{" + str(a_ids[j][i]) + "})$"
                ax[row][k].plot(xks[j][i], dists[j][i].pmf(xks[j][i]), 'ro', ms=8, mec=colors[i], color=colors[i],
                        label=label)
                ax[row][k].vlines(xks[j][i], 0, dists[j][i].pmf(xks[j][i]), colors=colors[i], linestyles='-', lw=2)
            else:
                label = "..."
                if i > 2:
                    ax[row][k].plot(xks[j][i], dists[j][i].pmf(xks[j][i]), 'ro', ms=8, mec=colors[i], color=colors[i])
                    ax[row][k].vlines(xks[j][i], 0, dists[j][i].pmf(xks[j][i]), colors=colors[i], linestyles='-', lw=2)
                else:
                    ax[row][k].plot(xks[j][i], dists[j][i].pmf(xks[j][i]), 'ro', ms=8, mec=colors[i], color=colors[i],
                            label=label)
                    ax[row][k].vlines(xks[j][i], 0, dists[j][i].pmf(xks[j][i]), colors=colors[i], linestyles='-', lw=2)

        ax[row][k].set_title(title)
        ax[row][k].set_xlabel(xlabels[j], fontsize=20)
        ax[row][k].set_ylabel(ylabels[j], fontsize=20)

        # set the grid on
        ax[row][k].grid('on')

        # tweak the axis labels
        xlab = ax[row][k].xaxis.get_label()
        ylab = ax[row][k].yaxis.get_label()

        xlab.set_size(9)
        ylab.set_size(9)
        ax[row][k].tick_params(axis='both', which='major', labelsize=6)
        ax[row][k].tick_params(axis='both', which='minor', labelsize=6)

        # change the color of the top and right spines to opaque gray
        ax[row][k].spines['right'].set_color((.8, .8, .8))
        ax[row][k].spines['top'].set_color((.8, .8, .8))

        # ax[2].legend(loc='upper center', bbox_to_anchor=(0.5, -0.18),
        #           ncol=2, fancybox=True, shadow=True)
        # ax.legend(loc="lower right")
        ax[row][k].xaxis.label.set_size(9)
        ax[row][k].yaxis.label.set_size(9)

        # # remove tick marks
        # ax[j].axis.set_tick_params(size=0)
        # ax[j].yaxis.set_tick_params(size=0)
        #
        # # change the color of the top and right spines to opaque gray
        # ax[j].spines['right'].set_color((.8, .8, .8))
        # ax[j].spines['top'].set_color((.8, .8, .8))


        ax[row][k].set_ylim(0, 1.1)

        k+=1
        # ax.set_xlim((0, 260))
        #ax.set_xlim(min_support-2 , max_support+2)
        #if len(labels) > 1:
        #ax.legend(loc="upper right")
    # ax[2].legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
    #           ncol=3, fancybox=True, shadow=True)

    handles, labels = ax[0][0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.52, 0.08),
               ncol=4, fancybox=True, shadow=True)

    fig.tight_layout()
    fig.subplots_adjust(bottom=0.15)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.close(fig)
    #plt.show()


def plot_multiple(dists, xks, min_support, max_support,
                  a_ids, b_ids,
                  subtitle : str,
                  xlabel: str, ylabel: str, file_name: str):
    cm = plt.cm.get_cmap('RdYlBu_r')
    colors = plt.cm.GnBu(np.linspace(0.3, 1, 45))[-45:]
    colors = plt.cm.viridis(np.linspace(0.3, 1, 45))[-45:]

    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    plt.rcParams['font.family'] = ['serif']
    # plt.rcParams['font.serif'] = ['Times New Roman']
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(4.5, 4))
    plt.rcParams.update({'font.size': 10})
    title = r"PMF: $\mathbb{P}[b^{\prime} | b, a]$ - " + subtitle

    #l = "r$(b_{" + b_ids[i] + "},a_{" + a_ids[i] + "})$"
    for i in range(len(xks)):
        if i < 2:
            label = "$(b_{" + str(b_ids[i]) + "},a_{" + str(a_ids[i]) + "})$"
            ax.plot(xks[i], dists[i].pmf(xks[i]), 'ro', ms=8, mec=colors[i], color=colors[i],
                    label=label)
            ax.vlines(xks[i], 0, dists[i].pmf(xks[i]), colors=colors[i], linestyles='-', lw=2)
        else:
            label = "..."
            if i > 2:
                ax.plot(xks[i], dists[i].pmf(xks[i]), 'ro', ms=8, mec=colors[i], color=colors[i])
                ax.vlines(xks[i], 0, dists[i].pmf(xks[i]), colors=colors[i], linestyles='-', lw=2)
            else:
                ax.plot(xks[i], dists[i].pmf(xks[i]), 'ro', ms=8, mec=colors[i], color=colors[i],
                        label=label)
                ax.vlines(xks[i], 0, dists[i].pmf(xks[i]), colors=colors[i], linestyles='-', lw=2)

    ax.set_title(title)
    ax.set_xlabel(xlabel, fontsize=20)
    ax.set_ylabel(ylabel, fontsize=20)

    # set the grid on
    ax.grid('on')

    # remove tick marks
    ax.xaxis.set_tick_params(size=0)
    ax.yaxis.set_tick_params(size=0)

    # change the color of the top and right spines to opaque gray
    ax.spines['right'].set_color((.8, .8, .8))
    ax.spines['top'].set_color((.8, .8, .8))

    # tweak the axis labels
    xlab = ax.xaxis.get_label()
    ylab = ax.yaxis.get_label()
    xlab.set_size(10)
    ylab.set_size(10)
    #ax.margins(x=1)
    ax.set_ylim(0, 1.1)
    # ax.set_xlim((0, 260))
    #ax.set_xlim(min_support-2 , max_support+2)
    #if len(labels) > 1:
    #ax.legend(loc="upper right")
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
              ncol=3, fancybox=True, shadow=True)

    fig.tight_layout()
    ax.xmargin = 10
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.close(fig)
    #plt.show()


def plot(dist, xk, k, action_dto: AttackerAction, logged_in_ips, subtitle : str,
         xlabel: str, ylabel: str):
    cm = plt.cm.get_cmap('RdYlBu_r')
    colors = plt.cm.GnBu(np.linspace(0.3, 1, 4))[-4:]
    colors = plt.cm.viridis(np.linspace(0.3, 1, 4))[-4:]

    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    plt.rcParams['font.family'] = ['serif']
    # plt.rcParams['font.serif'] = ['Times New Roman']
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(5, 3.5))
    plt.rcParams.update({'font.size': 10})
    title = "PMF: {} - {}".format(action_dto.name, subtitle)

    ax.plot(xk, dist.pmf(xk), 'ro', ms=8, mec=colors[0], color=colors[0])
    ax.vlines(xk, 0, dist.pmf(xk), colors=colors[0], linestyles='-', lw=2)

    ax.set_title(title)
    ax.set_xlabel(xlabel, fontsize=20)
    ax.set_ylabel(ylabel, fontsize=20)

    # set the grid on
    ax.grid('on')

    # remove tick marks
    ax.xaxis.set_tick_params(size=0)
    ax.yaxis.set_tick_params(size=0)

    # change the color of the top and right spines to opaque gray
    ax.spines['right'].set_color((.8, .8, .8))
    ax.spines['top'].set_color((.8, .8, .8))

    # tweak the axis labels
    xlab = ax.xaxis.get_label()
    ylab = ax.yaxis.get_label()
    xlab.set_size(10)
    ylab.set_size(10)
    # ax.set_xlim((0, 260))
    ax.set_xlim((dist.support()[0]-1, dist.support()[1]+1))

    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    plot_all()