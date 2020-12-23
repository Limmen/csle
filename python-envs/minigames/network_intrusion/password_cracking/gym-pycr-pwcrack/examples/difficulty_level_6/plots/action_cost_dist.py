import numpy as np
import zipfile
import matplotlib.pyplot as plt
import sys
from scipy import *
from gym_pycr_pwcrack.envs.config.level_1.pycr_pwcrack_level_1_base import PyCrPwCrackLevel1Base
from gym_pycr_pwcrack.dao.action.action_type import ActionType
from gym_pycr_pwcrack.dao.action.action_id import ActionId


def read_action_costs(zip_file: str, num_bins = 100, factors = None):
    archive = zipfile.ZipFile(zip_file, 'r')
    files = archive.namelist()
    cost_files = list(filter(lambda x: "_cost.txt" in x, files))
    print("num cost_files:{}".format(len(cost_files)))
    total_costs  = []
    costs_factors = []
    costs_factors.append([])
    for i in range(len(factors)):
        costs_factors.append([])
    for cf in cost_files:
        action_id_value = int(cf.rsplit('/', 1)[1].rsplit("_")[0])
        num_nodes = len(cf.rsplit('/', 1)[1].rsplit("_"))-3
        if num_nodes < 1:
            num_nodes = 1
        action_id = ActionId(action_id_value)
        cost_txt = archive.read(cf)
        try:
            cost=float(cost_txt.decode().replace("\n",""))
            total_costs.append(cost*num_nodes)
            costs_factors[0].append(cost*num_nodes)
            for i in range(len(factors)):
                costs_factors[i+1].append(cost * num_nodes*(factors[i]))
        except:
            pass
    max_max = int(max(map(lambda x: max(x), costs_factors)))
    arg_a = np.argmax(list(map(lambda x: max(x), costs_factors)))
    hist_range = (0, max_max)
    bins = np.linspace(min(total_costs), max(total_costs), max_max + 1)
    digitized_total = np.digitize(total_costs, bins)
    hist, bin_edges = np.histogram(costs_factors[arg_a], bins=99, density=False, range=hist_range)
    digitized_factors = list(map(lambda x: (np.histogram(x, range=(0, max_max), density=False, bins=bin_edges))[0], costs_factors))
    return digitized_total, digitized_factors, bin_edges, costs_factors

def read_action_alerts(zip_file: str, num_bins = 100):
    archive = zipfile.ZipFile(zip_file, 'r')
    files = archive.namelist()
    alerts_files = list(filter(lambda x: "_alerts.txt" in x, files))
    print("num alerts_files:{}".format(len(alerts_files)))
    total_alerts  = []
    total_priority = []
    for af in alerts_files:
        action_id_value = int(af.rsplit('/', 1)[1].rsplit("_")[0])
        action_id = ActionId(action_id_value)
        alert_txt = archive.read(af)
        try:
            alert_txt = alert_txt.decode().replace("\n", "")
            alert_parts = alert_txt.split(",")
            num_alerts = int(alert_parts[1])
            sum_priority = float(alert_parts[0])
            total_alerts.append(num_alerts)
            total_priority.append(sum_priority)
        except:
            pass
    return total_alerts, total_priority

def plot_action_types_pie(action_conf):
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    num_recon_actions = len(list(filter(lambda x: x.type == ActionType.RECON, action_conf.actions)))
    num_exploit_actions = len(list(filter(lambda x: x.type == ActionType.EXPLOIT, action_conf.actions)))
    num_post_exp_actions = len(list(filter(lambda x: x.type == ActionType.POST_EXPLOIT, action_conf.actions)))
    labels = 'Reconnaissance', 'Exploits', 'Post-Exploits'
    sizes = [num_recon_actions, num_exploit_actions, num_post_exp_actions]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    #plt.show()
    plt.tight_layout()
    file_name = "action_types_plot"
    plt.savefig(file_name + ".png", format="png", dpi=600)
    plt.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.close()

def plot_freq_dist(d1, d2, labels, title, num_bins, colors, xlabel, filename, bin_edges, data=None):
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['font.serif'] = ['Times New Roman']
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(5, 3.5))
    plt.rcParams.update({'font.size': 10})

    # Plot histogram of average episode lengths
    total_weights = []

    # total_x = []
    # for i in range(len(d2)):
    #     total_x.append(d2[i])
    #     weights = np.ones_like(d2[i]) / float(len(d2[i]))
    #     total_weights.append(weights)

    # ax.hist(data[3], bins=30, alpha=0.5, range=(0, 2300),
    #         label=labels[3], stacked=False, log=True, color=colors[3], density=True, edgecolor='black', ls="-.")
    # ax.hist(data[2], bins=30, alpha=0.5, range=(0, 2300),
    #         label=labels[2], stacked=False, log=True, color=colors[2], density=True, edgecolor='black', ls="dotted")
    # ax.hist(data[1], bins=30, alpha=0.5, range=(0, 2300),
    #         label=labels[1], stacked=False, log=True, color=colors[1], density=True, edgecolor='black', ls="dashed")
    print(data)
    ax.hist(data, bins=30, alpha=0.5, range=(0, 260),
            label=labels[0], stacked=False, log=True, color=colors[0], density=True, edgecolor='black')

    colors = ["#f9a65a", "#661D98", "#377EB8", "#4DAF4A", "#A65628", "#F781BF",
              '#D95F02', '#7570B3', '#E7298A', '#E6AB02', '#A6761D', '#666666',
              '#8DD3C7', '#CCEBC5', '#BEBADA', '#FB8072', "#FF7F00", '#80B1D3', '#FDB462', '#B3DE69', '#FCCDE5',
              '#D9D9D9', '#BC80BD', '#FFED6F', "blue", "#984EA3", "green", "#FFFF33", '#66A61E', '#FFFFB3',
              "purple", "orange", "browen", "ppink", "#1B9E77", "#E41A1C"]
    ax.set_title(title)
    ax.set_xlabel(xlabel, fontsize=20)
    ax.set_ylabel(r"Normalized Frequency", fontsize=20)

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
    ax.set_xlim((0, 260))

    if len(labels) > 1:
        ax.legend(loc="upper right")

    fig.tight_layout()
    plt.show()
    file_name = filename
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.close(fig)


if __name__ == '__main__':
    # plot_action_types_pie(PyCrPwCrackSimpleBase.all_actions_conf(
    #     num_nodes=PyCrPwCrackSimpleBase.num_nodes(),
    #     subnet_mask=PyCrPwCrackSimpleBase.subnet_mask(),
    #     hacker_ip=PyCrPwCrackSimpleBase.hacker_ip()
    # ))

    cm = plt.cm.get_cmap('RdYlBu_r')
    colors = plt.cm.GnBu(np.linspace(0.3, 1, 4))[-4:]
    colors = plt.cm.viridis(np.linspace(0.3, 1, 4))[-4:]

    # d_1 = read_action_costs(zip_file="/home/kim/storage/workspace/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/level_1/agent_cache.zip", num_bins=100)
    # d_2 = read_action_costs(zip_file="/home/kim/storage/workspace/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/level_2/agent_cache.zip", num_bins=100)
    #plot_freq_dist(d1=d_1,d2=d_2, num_bins=100)
    # d_1, d_factors, bin_edges, costs_factors = read_action_costs(
    #     zip_file="/home/kim/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/level_6/merged.zip",
    #     num_bins=100, factors=[2, 3, 4])
    # plot_freq_dist(d1=d_1, d2=d_factors, num_bins=100, labels=[r"$|\mathcal{N}|=25$", r"$|\mathcal{N}|=50$", r"$|\mathcal{N}|=75$", r"$|\mathcal{N}|=100$"],
    # title=r"Action execution times (costs)", xlabel=r"Time Cost (s)", colors=colors,
    # filename="action_cost_dist_plot", bin_edges=bin_edges, data=costs_factors)
    #
    # colors = ["r"]

    total_alerts, total_priority = read_action_alerts(
        zip_file="/home/kim/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/level_6/merged.zip",
        num_bins=250)
    #print(max(digitized_total))
    # plot_freq_dist(d1=None, d2=None,
    #                labels=[r"test"],title=r"Intrusion detection alerts per action", num_bins=30,
    #                colors=colors, xlabel=r"Number of triggered alerts",
    #                filename="action_alerts_dist_plot", data=total_alerts, bin_edges = None)

    #colors=["#599ad3"]
    plot_freq_dist(d1=None, d2=None,
                   labels=[r"test"], title=r"Intrusion detection alerts total priority $\sum_a p(a)$ per action", num_bins=30,
                   colors=colors, xlabel=r"Total priority of triggered alerts",
                   filename="action_alerts_priority_dist_plot", data=total_priority, bin_edges=None)

