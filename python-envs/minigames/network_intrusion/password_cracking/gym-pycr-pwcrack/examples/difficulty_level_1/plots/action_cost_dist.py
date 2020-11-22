import numpy as np
import zipfile
import matplotlib.pyplot as plt
from scipy import *
from gym_pycr_pwcrack.envs.config.simple.pycr_pwcrack_simple_base import PyCrPwCrackSimpleBase
from gym_pycr_pwcrack.dao.action.action_type import ActionType


def read_action_costs(zip_file: str, num_bins = 100):
    archive = zipfile.ZipFile(zip_file, 'r')
    files = archive.namelist()
    cost_files = list(filter(lambda x: "_cost.txt" in x, files))
    print("num cost_files:{}".format(len(cost_files)))
    costs  = []
    for cf in cost_files:
        cost_txt = archive.read(cf)
        try:
            cost=float(cost_txt.decode().replace("\n",""))
            costs.append(cost)
        except:
            pass
    bins = np.linspace(min(costs), max(costs), num_bins)
    digitized = np.digitize(costs, bins)
    return digitized

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

def plot_freq_dist(d1, d2, num_bins):
    # best fit of data
    #(mu, sigma) = norm.fit(data)
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 4.5))
    plt.rcParams.update({'font.size': 12})
    # Plot histogram of average episode lengths

    weights_1 = np.ones_like(d1) / float(len(d1))
    ax.hist(d1, bins=num_bins, weights=weights_1, color='cornflowerblue', alpha=0.75,
            label=r"$\upsilon_1$", stacked=True, log=True)

    # weights_2 = np.ones_like(d2) / float(len(d2))
    # ax.hist(d2, bins=num_bins, weights=weights_2, color='r', alpha=0.5,
    #         label=r"$\upsilon_2$", stacked=True, log=True)

    ax.set_title("Action Costs")
    ax.set_xlabel("Time Cost (s)", fontsize=20)
    ax.set_ylabel("Normalized Frequency", fontsize=20)
    #ax.set_xscale('log')
    #ax.legend()

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

    fig.tight_layout()
    plt.show()
    file_name = "action_cost_dist_plot"
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.close(fig)


if __name__ == '__main__':
    # plot_action_types_pie(PyCrPwCrackSimpleBase.all_actions_conf(
    #     num_nodes=PyCrPwCrackSimpleBase.num_nodes(),
    #     subnet_mask=PyCrPwCrackSimpleBase.subnet_mask(),
    #     hacker_ip=PyCrPwCrackSimpleBase.hacker_ip()
    # ))
    # d_1 = read_action_costs(zip_file="/home/kim/storage/workspace/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/level_1/agent_cache.zip", num_bins=100)
    # d_2 = read_action_costs(zip_file="/home/kim/storage/workspace/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/level_2/agent_cache.zip", num_bins=100)
    #plot_freq_dist(d1=d_1,d2=d_2, num_bins=100)
    d_1 = read_action_costs(
        zip_file="/home/kim/storage/workspace/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/level_2/agent_cache.zip",
        num_bins=100)
    d_2 = read_action_costs(
        zip_file="/home/kim/storage/workspace/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/level_2/ssh1_cache.zip",
        num_bins=100)
    d_3 = read_action_costs(
        zip_file="/home/kim/storage/workspace/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/level_2/ssh2_cache.zip",
        num_bins=100)
    d_4 = read_action_costs(
        zip_file="/home/kim/storage/workspace/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/level_2/ssh3_cache.zip",
        num_bins=100)
    d_5 = read_action_costs(
        zip_file="/home/kim/storage/workspace/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/level_2/telnet1_cache.zip",
        num_bins=100)
    d_6 = read_action_costs(
        zip_file="/home/kim/storage/workspace/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/level_2/telnet2_cache.zip",
        num_bins=100)
    d_7 = read_action_costs(
        zip_file="/home/kim/storage/workspace/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/level_2/telnet3_cache.zip",
        num_bins=100)

    # d_8 = read_action_costs(
    #     zip_file="/home/kim/storage/workspace/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/level_3/agent_cache.zip",
    #     num_bins=100)
    # d_9 = read_action_costs(
    #     zip_file="/home/kim/storage/workspace/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/level_3/ssh1_cache.zip",
    #     num_bins=100)
    # d_10 = read_action_costs(
    #     zip_file="/home/kim/storage/workspace/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/level_3/ssh2_cache.zip",
    #     num_bins=100)
    # d_11 = read_action_costs(
    #     zip_file="/home/kim/storage/workspace/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/level_3/ssh3_cache.zip",
    #     num_bins=100)
    # d_12 = read_action_costs(
    #     zip_file="/home/kim/storage/workspace/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/level_3/telnet1_cache.zip",
    #     num_bins=100)
    # d_13 = read_action_costs(
    #     zip_file="/home/kim/storage/workspace/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/level_3/telnet2_cache.zip",
    #     num_bins=100)
    # d_14 = read_action_costs(
    #     zip_file="/home/kim/storage/workspace/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/level_3/telnet3_cache.zip",
    #     num_bins=100)

    d_15 = read_action_costs(
        zip_file="/home/kim/storage/workspace/pycr/cluster-envs/minigames/network_intrusion/password_cracking/001/level_1/agent_cache.zip",
        num_bins=100)
    #print(d_1.shape)
    total = list(d_1) + list(d_2) + list(d_3) + list(d_4) + list(d_5) + list(d_6) + list(d_7) + list(d_15)
    plot_freq_dist(d1=total, d2=None, num_bins=100)
    #print(len(total))

