from gym_pycr_ctf.dao.defender_dynamics.defender_dynamics_model import DefenderDynamicsModel
from gym_pycr_ctf.envs.derived_envs.level4.emulation.pycr_ctf_level4_emulation_env import PyCrCTFLevel4Base
from gym_pycr_ctf.dao.action.attacker.attacker_action_id import AttackerActionId
from gym_pycr_ctf.dao.action.attacker.attacker_action import AttackerAction
import numpy as np
import matplotlib.pyplot as plt

def read_model():
    model_path = "/Users/kimham/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_4/hello_world/defender_dynamics_model.json"
    #model_path = "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_4/hello_world/defender_dynamics_model_server.json"
    defender_dynamics_model = DefenderDynamicsModel()
    defender_dynamics_model.read_model_path(model_path)
    defender_dynamics_model.normalize()
    return defender_dynamics_model

def plot_all():
    defender_dynamics_model = read_model()
    action_cfg = PyCrCTFLevel4Base.attacker_all_actions_conf(num_nodes=10, subnet_mask="test", hacker_ip = "test")
    total_row_dists, total_row_xks, total_row_a_ids, total_row_b_ids, total_row_short_titles, \
    total_row_x_labels, total_row_y_labels,row_labels = plot_machines_dynamics(defender_dynamics_model=defender_dynamics_model, action_cfg=action_cfg)

    ids_row_dists, ids_row_xks, ids_row_a_ids, ids_row_b_ids, ids_row_subtitles, ids_row_x_labels, ids_row_y_labels = \
        plot_ids_dynamics(defender_dynamics_model=defender_dynamics_model, action_cfg=action_cfg)

    plot_complete_model_full_span(total_row_dists, total_row_xks, total_row_a_ids, total_row_b_ids,
                                  total_row_short_titles,
                                  total_row_x_labels, total_row_y_labels,
                                  ids_row_dists, ids_row_xks, ids_row_a_ids, ids_row_b_ids, ids_row_subtitles,
                                  ids_row_x_labels, ids_row_y_labels,
                                  file_name="total_model_full",
                                  ncols=len(total_row_x_labels[0]),
                                  nrows=len(total_row_x_labels), figsize=(3, 2.2), fontsize=3.2, labelsize=2.5,
                                  suptitle="Estimated Emulation Dynamics", ms=0.4, title_fontsize=4.5, lw=0.2,
                                  row_labels=row_labels, wspace=0.03, hspace=0.18, top=0.92, num_colors=74)

def plot_machines_dynamics(defender_dynamics_model, action_cfg):
    total_row_dists = []
    total_row_xks = []
    total_row_a_ids = []
    total_row_b_ids = []
    total_row_subtitles = []
    total_row_x_labels = []
    total_row_y_labels = []
    total_row_short_titles = []
    row_labels=[]

    for machine_ip, v in defender_dynamics_model.machines_dynamics_model.items():
        row_dists, row_xks, row_a_ids, row_b_ids, row_subtitles, row_x_labels, row_y_labels, row_short_titles \
            = plot_machine_dynamics(machine_ip, v, action_cfg)
        total_row_dists.append(row_dists)
        total_row_xks.append(row_xks)
        total_row_a_ids.append(row_a_ids)
        total_row_b_ids.append(row_b_ids)
        total_row_subtitles.append(row_subtitles)
        total_row_x_labels.append(row_x_labels)
        total_row_y_labels.append(row_y_labels)
        row_labels.append(machine_ip)
        total_row_short_titles.append(row_short_titles)

    plot_complete_model(total_row_dists, total_row_xks, total_row_a_ids, total_row_b_ids, total_row_short_titles,
                        total_row_x_labels, total_row_y_labels, file_name="total_model_machines", ncols=len(total_row_x_labels[0]),
                        nrows=len(total_row_x_labels), figsize=(3,2.1), fontsize=3.5, labelsize=1.75,
                        suptitle="Estimated Dynamics of Nodes in the Emulation", ms=0.45, title_fontsize=4, lw=0.2,
                        row_labels=row_labels, wspace=0.00, hspace=0.00, top=0.925,
                        num_colors = 74)
    return total_row_dists, total_row_xks, total_row_a_ids, total_row_b_ids, total_row_short_titles,\
           total_row_x_labels, total_row_y_labels, row_labels


def plot_machine_dynamics(machine_ip, machine_dynamics, action_cfg):
    row_dists = []
    row_xks = []
    row_a_ids = []
    row_b_ids = []
    row_subtitles = []
    row_x_labels = []
    row_y_labels = []
    row_short_titles = []

    subtitle = "New TCP/UDP Connections"
    short_title = "Connections"
    xlabel = r"\# New TCP/UDP Connections"
    ylabel = r"$\mathbb{P}[ \cdot | (b_i, a_i)]$"
    total_dists, total_xks, total_a_ids, total_b_ids = plot_specific_dynamics(
        machine_dynamics.norm_num_new_open_connections, action_cfg,
        subtitle=subtitle,
        xlabel=xlabel,
        ylabel=ylabel,
        file_name=machine_ip + "_open_connections"
        )
    row_dists.append(total_dists)
    row_xks.append(total_xks)
    row_a_ids.append(total_a_ids)
    row_b_ids.append(total_b_ids)
    row_subtitles.append(subtitle)
    row_x_labels.append(xlabel)
    row_y_labels.append(ylabel)
    row_short_titles.append(short_title)

    subtitle = "New Failed Login Attempts"
    short_title = "Failed Logins"
    xlabel = r"\# New Failed Login Attempts"
    ylabel = r"$\mathbb{P}[ \cdot | (b_i, a_i)]$"
    total_dists, total_xks, total_a_ids, total_b_ids = plot_specific_dynamics(
        machine_dynamics.norm_num_new_failed_login_attempts, action_cfg,
        subtitle=subtitle,
        xlabel=xlabel,
        ylabel=ylabel,
        file_name=machine_ip + "_failed_logins"
    )
    row_dists.append(total_dists)
    row_xks.append(total_xks)
    row_a_ids.append(total_a_ids)
    row_b_ids.append(total_b_ids)
    row_subtitles.append(subtitle)
    row_x_labels.append(xlabel)
    row_y_labels.append(ylabel)
    row_short_titles.append(short_title)

    subtitle = "Created User Accounts"
    short_title = "Accounts"
    xlabel = r"\# Created User Accounts"
    ylabel = r"$\mathbb{P}[ \cdot | (b_i, a_i)]$"
    total_dists, total_xks, total_a_ids, total_b_ids = plot_specific_dynamics(
        machine_dynamics.norm_num_new_users, action_cfg,
        subtitle=subtitle,
        xlabel=xlabel,
        ylabel=ylabel,
        file_name=machine_ip + "_users"
    )
    row_dists.append(total_dists)
    row_xks.append(total_xks)
    row_a_ids.append(total_a_ids)
    row_b_ids.append(total_b_ids)
    row_subtitles.append(subtitle)
    row_x_labels.append(xlabel)
    row_y_labels.append(ylabel)
    row_short_titles.append(short_title)

    subtitle = "New Logged in Users"
    short_title = "Online Users"
    xlabel = r"\# New Logged in Users"
    ylabel = r"$\mathbb{P}[ \cdot | (b_i, a_i)]$"
    total_dists, total_xks, total_a_ids, total_b_ids = plot_specific_dynamics(
        machine_dynamics.norm_num_new_logged_in_users, action_cfg,
        subtitle=subtitle,
        xlabel=xlabel,
        ylabel=ylabel,
        file_name=machine_ip + "_logged_in_users"
    )
    row_dists.append(total_dists)
    row_xks.append(total_xks)
    row_a_ids.append(total_a_ids)
    row_b_ids.append(total_b_ids)
    row_subtitles.append(subtitle)
    row_x_labels.append(xlabel)
    row_y_labels.append(ylabel)
    row_short_titles.append(short_title)

    subtitle = "New Login Events"
    short_title="Logins"
    xlabel = r"\# Login Events"
    ylabel = r"$\mathbb{P}[ \cdot | (b_i, a_i)]$"
    total_dists, total_xks, total_a_ids, total_b_ids = plot_specific_dynamics(
        machine_dynamics.norm_num_new_login_events, action_cfg,
        subtitle=subtitle,
        xlabel=xlabel,
        ylabel=ylabel,
        file_name=machine_ip + "_login_events"
    )
    row_dists.append(total_dists)
    row_xks.append(total_xks)
    row_a_ids.append(total_a_ids)
    row_b_ids.append(total_b_ids)
    row_subtitles.append(subtitle)
    row_x_labels.append(xlabel)
    row_y_labels.append(ylabel)
    row_short_titles.append(short_title)

    subtitle = "Created Processes"
    short_title="Processes"
    xlabel = r"\# Created Processes"
    ylabel = r"$\mathbb{P}[ \cdot | (b_i, a_i)]$"
    total_dists, total_xks, total_a_ids, total_b_ids = plot_specific_dynamics(
        machine_dynamics.norm_num_new_processes, action_cfg,
        subtitle=subtitle,
        xlabel=xlabel,
        ylabel=ylabel,
        file_name=machine_ip + "_created_processes"
    )
    row_dists.append(total_dists)
    row_xks.append(total_xks)
    row_a_ids.append(total_a_ids)
    row_b_ids.append(total_b_ids)
    row_subtitles.append(subtitle)
    row_x_labels.append(xlabel)
    row_y_labels.append(ylabel)
    row_short_titles.append(short_title)

    # plot_ids_dynamics_two_row(row_dists, row_xks, row_a_ids, row_b_ids, row_subtitles, row_x_labels, row_y_labels,
    #                           machine_ip + "_row_dynamics", ncols=3, ip=machine_ip, figsize=(8, 4.5),
    #                           fontsize=8, labelsize=6, suptitle="Node IP: " + machine_ip)


    return row_dists, row_xks, row_a_ids, row_b_ids, row_subtitles, row_x_labels, row_y_labels, row_short_titles



def plot_ids_dynamics(defender_dynamics_model, action_cfg):
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

    # plot_ids_dynamics_two_row(row_dists, row_xks, row_a_ids, row_b_ids, row_subtitles, row_x_labels, row_y_labels,
    #                       "ids_dynamics_row", suptitle="IDS Dynamics"),
    return row_dists, row_xks, row_a_ids, row_b_ids, row_subtitles, row_x_labels, row_y_labels


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

        xk = np.arange(dist.support()[0], dist.support()[1]+1)
        xk = np.array(list(filter(lambda x: dist.pmf(x) > 0, xk.tolist())))
        total_xks.append(xk)
        total_dists.append(dist)

    # plot_multiple(total_dists, total_xks, min_support, max_support, total_a_ids, total_b_ids,
    #               subtitle=subtitle,
    #               xlabel=xlabel,
    #               ylabel=ylabel, file_name=file_name)

    return total_dists, total_xks, total_a_ids, total_b_ids


def plot_complete_model(dists, xks, a_ids, b_ids, subtitles, xlabels, ylabels, file_name, ncols=6,
                        figsize=(6, 4.5), fontsize=10, labelsize=6, suptitle="", nrows = 6, ms=2.5,
                        title_fontsize=8, lw=0.5, row_labels = None, wspace=0.03, hspace=0.07, top=0.9,
                        num_colors: int = 74):
    cm = plt.cm.get_cmap('RdYlBu_r')
    colors = plt.cm.viridis(np.linspace(0.3, 1,num_colors))[-num_colors:]
    colors = plt.cm.GnBu(np.linspace(0.3, 1, num_colors))[-num_colors:]

    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['axes.titlepad'] = 0
    plt.rcParams['xtick.major.pad'] = 0.5
    plt.rcParams['ytick.major.pad'] = 0.5
    plt.rcParams['axes.labelpad'] = 0.8
    plt.rcParams['axes.linewidth'] = 0.1
    # plt.rcParams['font.serif'] = ['Times New Roman']
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
    plt.rcParams.update({'font.size': fontsize})

    for row in range(nrows):
        rowtitles = subtitles[row]
        row_dists = dists[row]
        row_xks = xks[row]
        row_xlabels = xlabels[row]
        row_ylabels = ylabels[row]
        row_a_ids = a_ids[row]
        row_b_ids = b_ids[row]
        for col in range(ncols):
            title=rowtitles[col]
            for i in range(len(row_xks[col])):
                if i < 2:
                    label = "$(b_{" + str(row_b_ids[col][i]) + "},a_{" + str(row_a_ids[col][i]) + "})$"
                    ax[row][col].plot(row_xks[col][i], row_dists[col][i].pmf(row_xks[col][i]), 'ro', ms=ms, mec=colors[i], color=colors[i],
                            label=label)
                    ax[row][col].vlines(row_xks[col][i], 0, row_dists[col][i].pmf(row_xks[col][i]), colors=colors[i], linestyles='-', lw=lw)
                else:
                    label = "..."
                    if i > 2:
                        ax[row][col].plot(row_xks[col][i], row_dists[col][i].pmf(row_xks[col][i]), 'ro', ms=ms, mec=colors[i], color=colors[i])
                        ax[row][col].vlines(row_xks[col][i], 0, row_dists[col][i].pmf(row_xks[col][i]), colors=colors[i], linestyles='-', lw=lw)
                    else:
                        ax[row][col].plot(row_xks[col][i], row_dists[col][i].pmf(row_xks[col][i]), 'ro', ms=ms, mec=colors[i], color=colors[i],
                                label=label)
                        ax[row][col].vlines(row_xks[col][i], 0, row_dists[col][i].pmf(row_xks[col][i]), colors=colors[i], linestyles='-', lw=lw)
            if row==0:
                ax[row][col].set_title(title, fontsize=fontsize)
            #ax[row][col].set_xlabel(row_xlabels[col], fontsize=labelsize)
            if col == 0:
                ax[row][col].set_ylabel(row_labels[row], fontsize=fontsize)

            # set the grid on
            #ax[row][col].grid('on')

            # tweak the axis labels
            #xlab = ax[row][col].xaxis.get_label()
            ylab = ax[row][col].yaxis.get_label()
            #xlab.set_size(labelsize)
            ylab.set_size(fontsize)
            if row != nrows-1:
                ax[row][col].set_xticks([])
            if col != 0:
                ax[row][col].set_yticks([])
            ax[row][col].tick_params(axis='both', which='major', labelsize=labelsize, length=1.2, width=0.2)
            ax[row][col].tick_params(axis='both', which='minor', labelsize=labelsize, length=1.2, width=0.2)

            # change the color of the top and right spines to opaque gray
            ax[row][col].spines['right'].set_color((.8, .8, .8))
            ax[row][col].spines['top'].set_color((.8, .8, .8))

            ax[row][col].set_ylim(0, 1.1)


    # handles, labels = ax[0][0].get_legend_handles_labels()
    # fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.52, 0.08),
    #            ncol=4, fancybox=True, shadow=True)

    fig.suptitle(suptitle, fontsize=title_fontsize, fontweight="bold", fontname="Times New Roman Bold")

    fig.tight_layout()
    #fig.subplots_adjust(bottom=0.15,top=0.25)
    fig.subplots_adjust(wspace=wspace, hspace=hspace, top=top)
    #bottom=0.35
    #wspace=0.135, hspace=0.08
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.close(fig)
    #plt.show()




def plot_complete_model_full_span(dists, xks, a_ids, b_ids, subtitles, xlabels, ylabels,
                                  ids_row_dists, ids_row_xks, ids_row_a_ids, ids_row_b_ids, ids_row_subtitles,
                                  ids_row_x_labels, ids_row_y_labels,file_name, ncols=6,
                                  figsize=(6, 4.5), fontsize=10, labelsize=6, suptitle="", nrows = 6, ms=2.5,
                        title_fontsize=8, lw=0.5, row_labels = None, wspace=0.03, hspace=0.07, top=0.9,
                                  num_colors: int = 74):
    cm = plt.cm.get_cmap('RdYlBu_r')
    colors = plt.cm.GnBu(np.linspace(0.3, 1, num_colors))[-num_colors:]
    colors = plt.cm.viridis(np.linspace(0.3, 1, num_colors))[-num_colors:]

    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['axes.titlepad'] = 0
    plt.rcParams['xtick.major.pad'] = 0.5
    plt.rcParams['ytick.major.pad'] = 0.5
    plt.rcParams['axes.labelpad'] = 0.8
    plt.rcParams['axes.linewidth'] = 0.1

    # plt.rcParams['font.serif'] = ['Times New Roman']
    fig, ax = plt.subplots(nrows=nrows+1, ncols=ncols, figsize=figsize)
    plt.rcParams.update({'font.size': fontsize})

    plt.subplot(6, 6, (1,2))

    for i in range(len(ids_row_dists[0])):
        if i < 2:
            label = "$(b_{" + str(ids_row_b_ids[0][i]) + "},a_{" + str(ids_row_a_ids[0][i]) + "})$"
            plt.plot(ids_row_xks[0][i], ids_row_dists[0][i].pmf(ids_row_xks[0][i]), 'ro', ms=ms, mec=colors[i], color=colors[i],
                            label=label)
            plt.vlines(ids_row_xks[0][i], 0, ids_row_dists[0][i].pmf(ids_row_xks[0][i]), colors=colors[i], linestyles='-', lw=lw)
        else:
            label = "..."
            if i > 2:
                plt.plot(ids_row_xks[0][i], ids_row_dists[0][i].pmf(ids_row_xks[0][i]), 'ro', ms=ms, mec=colors[i],
                         color=colors[i])
                plt.vlines(ids_row_xks[0][i], 0, ids_row_dists[0][i].pmf(ids_row_xks[0][i]), colors=colors[i], linestyles='-',
                           lw=lw)
            else:
                plt.plot(ids_row_xks[0][i], ids_row_dists[0][i].pmf(ids_row_xks[0][i]), 'ro', ms=ms, mec=colors[i],
                         color=colors[i],
                         label=label)
                plt.vlines(ids_row_xks[0][i], 0, ids_row_dists[0][i].pmf(ids_row_xks[0][i]), colors=colors[i], linestyles='-',
                           lw=lw)
    plt.title("Alerts", fontsize=fontsize)
    plt.ylabel("IDS", fontsize=fontsize)
    #plt.yticks([])
    plt.yticks([])
    plt.xticks([])
    plt.tick_params(axis='both', which='major', labelsize=labelsize, length=2)
    plt.tick_params(axis='both', which='minor', labelsize=labelsize, length=2)
    plt.ylim(0, 1.1)

    plt.subplot(6, 6, (3, 4))

    for i in range(len(ids_row_dists[3])):
        if i < 2:
            label = "$(b_{" + str(ids_row_b_ids[3][i]) + "},a_{" + str(ids_row_a_ids[3][i]) + "})$"
            plt.plot(ids_row_xks[3][i], ids_row_dists[3][i].pmf(ids_row_xks[3][i]), 'ro', ms=ms, mec=colors[i],
                     color=colors[i],
                     label=label)
            plt.vlines(ids_row_xks[3][i], 0, ids_row_dists[3][i].pmf(ids_row_xks[3][i]), colors=colors[i],
                       linestyles='-', lw=lw)
        else:
            label = "..."
            if i > 2:
                plt.plot(ids_row_xks[3][i], ids_row_dists[3][i].pmf(ids_row_xks[3][i]), 'ro', ms=ms, mec=colors[i],
                         color=colors[i])
                plt.vlines(ids_row_xks[3][i], 0, ids_row_dists[3][i].pmf(ids_row_xks[3][i]), colors=colors[i],
                           linestyles='-',
                           lw=lw)
            else:
                plt.plot(ids_row_xks[3][i], ids_row_dists[3][i].pmf(ids_row_xks[3][i]), 'ro', ms=ms, mec=colors[i],
                         color=colors[i],
                         label=label)
                plt.vlines(ids_row_xks[3][i], 0, ids_row_dists[3][i].pmf(ids_row_xks[3][i]), colors=colors[i],
                           linestyles='-',
                           lw=lw)

    plt.title("Alert Priorities", fontsize=fontsize)
    plt.yticks([])
    plt.xticks([])
    plt.tick_params(axis='both', which='major', labelsize=labelsize)
    plt.tick_params(axis='both', which='minor', labelsize=labelsize)
    plt.ylim(0, 1.1)


    plt.subplot(6, 6, 5)
    for i in range(len(ids_row_dists[1])):
        if i < 2:
            label = "$(b_{" + str(ids_row_b_ids[1][i]) + "},a_{" + str(ids_row_a_ids[1][i]) + "})$"
            plt.plot(ids_row_xks[1][i], ids_row_dists[1][i].pmf(ids_row_xks[1][i]), 'ro', ms=ms, mec=colors[i],
                     color=colors[i],
                     label=label)
            plt.vlines(ids_row_xks[1][i], 0, ids_row_dists[1][i].pmf(ids_row_xks[1][i]), colors=colors[i],
                       linestyles='-', lw=lw)
        else:
            label = "..."
            if i > 2:
                plt.plot(ids_row_xks[1][i], ids_row_dists[1][i].pmf(ids_row_xks[1][i]), 'ro', ms=ms, mec=colors[i],
                         color=colors[i])
                plt.vlines(ids_row_xks[1][i], 0, ids_row_dists[1][i].pmf(ids_row_xks[1][i]), colors=colors[i],
                           linestyles='-',
                           lw=lw)
            else:
                plt.plot(ids_row_xks[1][i], ids_row_dists[1][i].pmf(ids_row_xks[1][i]), 'ro', ms=ms, mec=colors[i],
                         color=colors[i],
                         label=label)
                plt.vlines(ids_row_xks[1][i], 0, ids_row_dists[1][i].pmf(ids_row_xks[1][i]), colors=colors[i],
                           linestyles='-',
                           lw=lw)
    plt.title("Severe Alerts", fontsize=fontsize)
    plt.yticks([])
    plt.xticks([])
    plt.tick_params(axis='both', which='major', labelsize=labelsize)
    plt.tick_params(axis='both', which='minor', labelsize=labelsize)
    plt.ylim(0, 1.1)

    plt.subplot(6, 6, 6)
    for i in range(len(ids_row_dists[2])):
        if i < 2:
            label = "$(b_{" + str(ids_row_b_ids[2][i]) + "},a_{" + str(ids_row_a_ids[2][i]) + "})$"
            plt.plot(ids_row_xks[2][i], ids_row_dists[2][i].pmf(ids_row_xks[2][i]), 'ro', ms=ms, mec=colors[i],
                     color=colors[i],
                     label=label)
            plt.vlines(ids_row_xks[2][i], 0, ids_row_dists[2][i].pmf(ids_row_xks[2][i]), colors=colors[i],
                       linestyles='-', lw=lw)
        else:
            label = "..."
            if i > 2:
                plt.plot(ids_row_xks[2][i], ids_row_dists[2][i].pmf(ids_row_xks[2][i]), 'ro', ms=ms, mec=colors[i],
                         color=colors[i])
                plt.vlines(ids_row_xks[2][i], 0, ids_row_dists[2][i].pmf(ids_row_xks[2][i]), colors=colors[i],
                           linestyles='-',
                           lw=lw)
            else:
                plt.plot(ids_row_xks[2][i], ids_row_dists[2][i].pmf(ids_row_xks[2][i]), 'ro', ms=ms, mec=colors[i],
                         color=colors[i],
                         label=label)
                plt.vlines(ids_row_xks[2][i], 0, ids_row_dists[2][i].pmf(ids_row_xks[2][i]), colors=colors[i],
                           linestyles='-',
                           lw=lw)
    plt.title("Warning Alerts", fontsize=fontsize)
    plt.yticks([])
    plt.xticks([])
    plt.tick_params(axis='both', which='major', labelsize=labelsize, length=2)
    plt.tick_params(axis='both', which='minor', labelsize=labelsize, length=2)
    plt.ylim(0, 1.1)

    for row in range(1, nrows+1):
        rowtitles = subtitles[row-1]
        row_dists = dists[row-1]
        row_xks = xks[row-1]
        row_xlabels = xlabels[row-1]
        row_ylabels = ylabels[row-1]
        row_a_ids = a_ids[row-1]
        row_b_ids = b_ids[row-1]
        for col in range(ncols):
            title=rowtitles[col]
            #l = "r$(b_{" + b_ids[i] + "},a_{" + a_ids[i] + "})$"
            for i in range(len(row_xks[col])):
                if i < 2:
                    label = "$(b_{" + str(row_b_ids[col][i]) + "},a_{" + str(row_a_ids[col][i]) + "})$"
                    ax[row][col].plot(row_xks[col][i], row_dists[col][i].pmf(row_xks[col][i]), 'ro', ms=ms, mec=colors[i], color=colors[i],
                            label=label)
                    ax[row][col].vlines(row_xks[col][i], 0, row_dists[col][i].pmf(row_xks[col][i]), colors=colors[i], linestyles='-', lw=lw)
                else:
                    label = "..."
                    if i > 2:
                        ax[row][col].plot(row_xks[col][i], row_dists[col][i].pmf(row_xks[col][i]), 'ro', ms=ms, mec=colors[i], color=colors[i])
                        ax[row][col].vlines(row_xks[col][i], 0, row_dists[col][i].pmf(row_xks[col][i]), colors=colors[i], linestyles='-', lw=lw)
                    else:
                        ax[row][col].plot(row_xks[col][i], row_dists[col][i].pmf(row_xks[col][i]), 'ro', ms=ms, mec=colors[i], color=colors[i],
                                label=label)
                        ax[row][col].vlines(row_xks[col][i], 0, row_dists[col][i].pmf(row_xks[col][i]), colors=colors[i], linestyles='-', lw=lw)
            if row==1:
                ax[row][col].set_title(title, fontsize=fontsize)
            #ax[row][col].set_xlabel(row_xlabels[col], fontsize=labelsize)
            if col == 0:
                ax[row][col].set_ylabel(row_labels[row-1], fontsize=fontsize)

            # set the grid on
            #ax[row][col].grid('on')

            # tweak the axis labels
            #xlab = ax[row][col].xaxis.get_label()
            ylab = ax[row][col].yaxis.get_label()
            #xlab.set_size(labelsize)
            ylab.set_size(fontsize)
            #if row != nrows:
            ax[row][col].set_xticks([])
            #if col != 0:
            ax[row][col].set_yticks([])
            ax[row][col].tick_params(axis='both', which='major', labelsize=labelsize, length=2)
            ax[row][col].tick_params(axis='both', which='minor', labelsize=labelsize, length=2)

            # change the color of the top and right spines to opaque gray
            ax[row][col].spines['right'].set_color((.8, .8, .8))
            ax[row][col].spines['top'].set_color((.8, .8, .8))

            ax[row][col].set_ylim(0, 1.1)


    # handles, labels = ax[0][0].get_legend_handles_labels()
    # fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.52, 0.08),
    #            ncol=4, fancybox=True, shadow=True)

    fig.suptitle(suptitle, fontsize=title_fontsize, fontweight="bold", fontname="Times New Roman Bold")

    fig.tight_layout()
    #fig.subplots_adjust(bottom=0.15,top=0.25)
    fig.subplots_adjust(wspace=wspace, hspace=hspace, top=top)
    #bottom=0.35
    #wspace=0.135, hspace=0.08
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.close(fig)
    #plt.show()


def plot_ids_dynamics_two_row(dists, xks,
                              a_ids, b_ids,
                              subtitles,
                              xlabels, ylabels, file_name, ncols=2, ip=None,
                              figsize=(6, 4.5), fontsize=10, labelsize=6,
                              suptitle=""):
    cm = plt.cm.get_cmap('RdYlBu_r')
    colors = plt.cm.GnBu(np.linspace(0.3, 1, 45))[-45:]
    colors = plt.cm.viridis(np.linspace(0.3, 1, 45))[-45:]

    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    plt.rcParams['font.family'] = ['serif']
    # plt.rcParams['font.serif'] = ['Times New Roman']
    fig, ax = plt.subplots(nrows=2, ncols=ncols, figsize=figsize)
    plt.rcParams.update({'font.size': fontsize})

    k = 0
    row = 0
    for j in range(len(dists)):
        title = subtitles[j]
        if j > 2 and row == 0:
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

        ax[row][k].set_title(title, fontsize=fontsize)
        ax[row][k].set_xlabel(xlabels[j], fontsize=labelsize)
        ax[row][k].set_ylabel(ylabels[j], fontsize=labelsize)

        # set the grid on
        ax[row][k].grid('on')

        # tweak the axis labels
        xlab = ax[row][k].xaxis.get_label()
        ylab = ax[row][k].yaxis.get_label()
        xlab.set_size(labelsize)
        ylab.set_size(labelsize)
        ax[row][k].tick_params(axis='both', which='major', labelsize=labelsize, length=2)
        ax[row][k].tick_params(axis='both', which='minor', labelsize=labelsize, length=2)

        # change the color of the top and right spines to opaque gray
        ax[row][k].spines['right'].set_color((.8, .8, .8))
        ax[row][k].spines['top'].set_color((.8, .8, .8))

        ax[row][k].set_ylim(0, 1.1)

        k+=1

    handles, labels = ax[0][0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.52, 0.08),
               ncol=4, fancybox=True, shadow=True)

    fig.suptitle(suptitle, fontsize=12, fontweight="bold", fontname="Times New Roman Bold")

    fig.tight_layout()
    fig.subplots_adjust(bottom=0.15,top=0.85)
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