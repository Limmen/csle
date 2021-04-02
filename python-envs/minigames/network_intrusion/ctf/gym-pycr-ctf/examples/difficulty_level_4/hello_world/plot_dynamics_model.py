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

    plot_specific_dynamics(defender_dynamics_model.norm_num_new_alerts, action_cfg,
                           subtitle="IDS Alerts",
                           xlabel=r"\# IDS Alerts",
                           ylabel=r"$\mathbb{P}[ \cdot | (b_i, a_i)]$",
                           file_name="ids_alerts"
                           )

    plot_specific_dynamics(defender_dynamics_model.norm_num_new_severe_alerts, action_cfg,
                           subtitle="Severe IDS Alerts",
                           xlabel=r"\# Severe IDS Alerts",
                           ylabel=r"$\mathbb{P}[ \cdot | (b_i, a_i)]$",
                           file_name="severe_ids_alerts"
                           )

    plot_specific_dynamics(defender_dynamics_model.norm_num_new_warning_alerts, action_cfg,
                           subtitle="Warning IDS Alerts",
                           xlabel=r"\# Warning IDS Alerts",
                           ylabel=r"$\mathbb{P}[ \cdot | (b_i, a_i)]$",
                           file_name="warning_ids_alerts"
                           )

    plot_specific_dynamics(defender_dynamics_model.norm_num_new_priority, action_cfg,
                           subtitle="IDS Alert Priorities",
                           xlabel=r"\# IDS Alert Priorities",
                           ylabel=r"$\mathbb{P}[ \cdot | (b_i, a_i)]$",
                           file_name="priority_ids_alerts"
                           )

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

    plot_multiple(total_dists, total_xks, min_support, max_support, total_a_ids, total_b_ids,
                  subtitle=subtitle,
                  xlabel=xlabel,
                  ylabel=ylabel, file_name=file_name)

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