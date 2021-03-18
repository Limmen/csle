import numpy as np
import zipfile
import matplotlib.pyplot as plt
import sys
from scipy import *
from gym_pycr_ctf.envs.config.level_1.pycr_ctf_level_1_base import PyCrCTFLevel1Base
from gym_pycr_ctf.dao.action.action_type import ActionType
from gym_pycr_ctf.dao.action.action_id import ActionId
import glob
import pandas as pd

def read_data():
    base_path = "/home/kim/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_6/training/v1/cluster/ppo_baseline/results/data/"
    ppo_v1_df_399 = pd.read_csv(glob.glob(base_path + "399/*_train.csv")[0])
    emulation_w_cache_env_response_times = np.mean(np.array(list(filter(lambda x: x  >0.0, ppo_v1_df_399["env_response_times"].values))))
    emulation_w_cache_action_pred_times = np.mean(np.array(list(filter(lambda x: x > 0.0, ppo_v1_df_399["action_pred_times"].values))))
    emulation_w_cache_grad_comp_times = np.mean(np.array(list(filter(lambda x: x > 0.0, ppo_v1_df_399["grad_comp_times"].values))))
    emulation_w_cache_weight_update_times = np.mean(np.array(list(filter(lambda x: x > 0.0, ppo_v1_df_399["weight_update_times"].values))))

    total_emulation_w_cache = emulation_w_cache_env_response_times + emulation_w_cache_action_pred_times + \
                              emulation_w_cache_grad_comp_times + emulation_w_cache_weight_update_times
    #emulation_w_cache_rollout_times_percentage  = (emulation_w_cache_rollout_times/total_emulation_w_cache)*100
    emulation_w_cache_env_response_times_percentage = (emulation_w_cache_env_response_times/total_emulation_w_cache)*100
    emulation_w_cache_action_pred_times_percentage = (emulation_w_cache_action_pred_times/total_emulation_w_cache)*100
    emulation_w_cache_grad_comp_times_percentage = (emulation_w_cache_grad_comp_times/total_emulation_w_cache)*100
    emulation_w_cache_weight_update_times_percentage = (emulation_w_cache_weight_update_times/total_emulation_w_cache)*100


    return emulation_w_cache_env_response_times_percentage, \
           emulation_w_cache_action_pred_times_percentage, emulation_w_cache_grad_comp_times_percentage, \
           emulation_w_cache_weight_update_times_percentage

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
    num_exploit_actions = len(list(filter(lambda x: x.type == ActionType.EXPLOIT or x.type == ActionType.PRIVILEGE_ESCALATION, action_conf.actions)))
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

    ax.hist(data[3], bins=30, alpha=1, range=(0, 2300),
            label=labels[3], stacked=False, log=True, color=colors[3], density=True, edgecolor='black', ls="-.")
    ax.hist(data[2], bins=30, alpha=1, range=(0, 2300),
            label=labels[2], stacked=False, log=True, color=colors[2], density=True, edgecolor='black', ls="dotted")
    ax.hist(data[1], bins=30, alpha=1, range=(0, 2300),
            label=labels[1], stacked=False, log=True, color=colors[1], density=True, edgecolor='black', ls="dashed")
    #print(data)
    ax.hist(data[0], bins=30, alpha=1, range=(0, 2300),
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
    #ax.set_xlim((0, 260))
    ax.set_xlim((0, 2300))

    if len(labels) > 1:
        ax.legend(loc="upper right")

    fig.tight_layout()
    plt.show()
    file_name = filename
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    #plt.close(fig)


def plot_freq_dist_w_boxes(d1, d2, labels, title, num_bins, colors, xlabel, filename, bin_edges, data=None):
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

    # let numpy calculate the histogram entries
    # histo, bin_edges = np.histogram(data[3], 30, (0, 2300))
    # bin_middles = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    # print(np.array(data[3])*0.01)
    # ax.hist(data[3], bins=30, alpha=1, range=(0, 2300),
    #         label=labels[3], stacked=False, log=True, color=colors[3], density=True, edgecolor='black', ls="-")

    # normalisation = 30 / (len(data[3]) * (2300 - 0))
    # y_err = np.sqrt(histo) * normalisation
    # y = histo*normalisation
    # y_err[0] = y_err[0] + 0.0025
    # y_err[1] = y_err[1] + 0.0001
    #ax.errorbar(bin_middles, y, fmt='.k', color="black", yerr=y_err)
    #plt.errorbar(bin_middles, np.array(data[3])*0.01)

    # histo, bin_edges = np.histogram(data[2], 30, (0, 2300))
    # bin_middles = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    # ax.hist(data[2], bins=30, alpha=1, range=(0, 2300),
    #         label=labels[2], stacked=False, log=True, color=colors[2], density=True, edgecolor='black')
    # normalisation = 30 / (len(data[2]) * (2300 - 0))
    # y_err = np.sqrt(histo) * normalisation
    # y_err[0] = y_err[0] + 0.005
    # y_err[1] = y_err[1] + 0.00001
    # y = histo * normalisation
    # ax.errorbar(bin_middles, y, fmt='.k', color="black", yerr=y_err)

    # histo, bin_edges = np.histogram(data[1], 30, (0, 2300))
    # bin_middles = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    # ax.hist(data[1], bins=30, alpha=1, range=(0, 2300),
    #         label=labels[1], stacked=False, log=True, color=colors[1], density=True, edgecolor='black')
    # normalisation = 30 / (len(data[1]) * (2300 - 0))
    # y_err = np.sqrt(histo) * normalisation
    # y_err[0] = y_err[0] + 0.005
    # y_err[1] = y_err[1] + 0.00001
    # y = histo * normalisation
    # ax.errorbar(bin_middles, y, fmt='.k', color="black", yerr=y_err)

    histo, bin_edges = np.histogram(data[0], 30, (0, 2300))
    bin_middles = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    ax.hist(data[0], bins=30, alpha=1, range=(0, 2300),
            label=labels[0], stacked=False, log=True, color=colors[0], density=True, edgecolor='black')
    normalisation = 30 / (len(data[0]) * (2300 - 0))
    y_err = np.sqrt(histo) * normalisation
    y_err[0] = y_err[0] + 0.005
    y_err[1] = y_err[1] + 0.00001
    y = histo * normalisation
    ax.errorbar(bin_middles, y, fmt='.k', color="black", yerr=y_err)

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
    #ax.set_xlim((0, 260))
    ax.set_xlim((0, 2300))

    if len(labels) > 1:
        ax.legend(loc="upper right")

    fig.tight_layout()
    plt.show()
    file_name = filename
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    #plt.close(fig)


def plot_freq_dist_w_boxes_all(d1, d2, labels, title, num_bins, colors, xlabel, filename, bin_edges, data=None,
                               ncols=4, figsize = (11, 2.5)):
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['font.serif'] = ['Times New Roman']
    fig, ax = plt.subplots(nrows=1, ncols=ncols, figsize=figsize)
    plt.rcParams.update({'font.size': 10})

    #let numpy calculate the histogram entries
    histo, bin_edges = np.histogram(data[0], 30, (0, 2300))
    bin_middles = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    print(np.array(data[0])*0.01)
    ax[0].hist(data[0], bins=30, alpha=1, range=(0, 2300),
            label=labels[0], stacked=False, log=True, color=colors[3], density=True, edgecolor='black', ls="-")

    normalisation = 30 / (len(data[0]) * (2300 - 0))
    y_err = np.sqrt(histo) * normalisation
    y = histo*normalisation
    y_err[0] = y_err[0] + 0.0025
    y_err[1] = y_err[1] + 0.0001
    ax[0].errorbar(bin_middles, y, fmt='.k', color="black", yerr=y_err)

    histo, bin_edges = np.histogram(data[1], 30, (0, 2300))
    bin_middles = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    ax[1].hist(data[1], bins=30, alpha=1, range=(0, 2300),
            label=labels[1], stacked=False, log=True, color=colors[2], density=True, edgecolor='black')
    normalisation = 30 / (len(data[1]) * (2300 - 0))
    y_err = np.sqrt(histo) * normalisation
    y_err[0] = y_err[0] + 0.005
    y_err[1] = y_err[1] + 0.00001
    y = histo * normalisation
    ax[1].errorbar(bin_middles, y, fmt='.k', color="black", yerr=y_err)

    histo, bin_edges = np.histogram(data[2], 30, (0, 2300))
    bin_middles = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    ax[2].hist(data[2], bins=30, alpha=1, range=(0, 2300),
            label=labels[2], stacked=False, log=True, color=colors[1], density=True, edgecolor='black')
    normalisation = 30 / (len(data[2]) * (2300 - 0))
    y_err = np.sqrt(histo) * normalisation
    y_err[0] = y_err[0] + 0.005
    y_err[1] = y_err[1] + 0.00001
    y = histo * normalisation
    ax[2].errorbar(bin_middles, y, fmt='.k', color="black", yerr=y_err)

    histo, bin_edges = np.histogram(data[3], 30, (0, 2300))
    bin_middles = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    ax[3].hist(data[3], bins=30, alpha=1, range=(0, 2300),
            label=labels[3], stacked=False, log=True, color=colors[0], density=True, edgecolor='black')
    normalisation = 30 / (len(data[3]) * (2300 - 0))
    y_err = np.sqrt(histo) * normalisation
    y_err[0] = y_err[0] + 0.005
    y_err[1] = y_err[1] + 0.00001
    y = histo * normalisation
    ax[3].errorbar(bin_middles, y, fmt='.k', color="black", yerr=y_err)

    colors = ["#f9a65a", "#661D98", "#377EB8", "#4DAF4A", "#A65628", "#F781BF",
              '#D95F02', '#7570B3', '#E7298A', '#E6AB02', '#A6761D', '#666666',
              '#8DD3C7', '#CCEBC5', '#BEBADA', '#FB8072', "#FF7F00", '#80B1D3', '#FDB462', '#B3DE69', '#FCCDE5',
              '#D9D9D9', '#BC80BD', '#FFED6F', "blue", "#984EA3", "green", "#FFFF33", '#66A61E', '#FFFFB3',
              "purple", "orange", "browen", "ppink", "#1B9E77", "#E41A1C"]
    ax[0].set_title(title)
    ax[0].set_xlabel(xlabel, fontsize=20)
    ax[0].set_ylabel(r"Normalized Frequency", fontsize=20)
    ax[0].grid('on')
    ax[0].xaxis.set_tick_params(size=0)
    ax[0].yaxis.set_tick_params(size=0)
    ax[0].spines['right'].set_color((.8, .8, .8))
    ax[0].spines['top'].set_color((.8, .8, .8))
    xlab = ax[0].xaxis.get_label()
    ylab = ax[0].yaxis.get_label()
    xlab.set_size(10)
    ylab.set_size(10)
    ax[0].set_xlim((0, 2300))
    if len(labels) > 1:
        ax[0].legend(loc="upper right")

    ax[1].set_title(title)
    ax[1].set_xlabel(xlabel, fontsize=20)
    #ax[1].set_ylabel(r"Normalized Frequency", fontsize=20)
    ax[1].grid('on')
    ax[1].xaxis.set_tick_params(size=0)
    ax[1].yaxis.set_tick_params(size=0)
    ax[1].spines['right'].set_color((.8, .8, .8))
    ax[1].spines['top'].set_color((.8, .8, .8))
    xlab = ax[1].xaxis.get_label()
    ylab = ax[1].yaxis.get_label()
    xlab.set_size(10)
    ylab.set_size(10)
    ax[1].set_xlim((0, 2300))
    if len(labels) > 1:
        ax[1].legend(loc="upper right")

    ax[2].set_title(title)
    ax[2].set_xlabel(xlabel, fontsize=20)
    #ax[2].set_ylabel(r"Normalized Frequency", fontsize=20)
    ax[2].grid('on')
    ax[2].xaxis.set_tick_params(size=0)
    ax[2].yaxis.set_tick_params(size=0)
    ax[2].spines['right'].set_color((.8, .8, .8))
    ax[2].spines['top'].set_color((.8, .8, .8))
    xlab = ax[2].xaxis.get_label()
    ylab = ax[2].yaxis.get_label()
    xlab.set_size(10)
    ylab.set_size(10)
    ax[2].set_xlim((0, 2300))
    if len(labels) > 1:
        ax[2].legend(loc="upper right")

    ax[3].set_title(title)
    ax[3].set_xlabel(xlabel, fontsize=20)
    #ax[3].set_ylabel(r"Normalized Frequency", fontsize=20)
    ax[3].grid('on')
    ax[3].xaxis.set_tick_params(size=0)
    ax[3].yaxis.set_tick_params(size=0)
    ax[3].spines['right'].set_color((.8, .8, .8))
    ax[3].spines['top'].set_color((.8, .8, .8))
    xlab = ax[3].xaxis.get_label()
    ylab = ax[3].yaxis.get_label()
    xlab.set_size(10)
    ylab.set_size(10)
    ax[3].set_xlim((0, 2300))
    if len(labels) > 1:
        ax[3].legend(loc="upper right")

    fig.tight_layout()
    fig.subplots_adjust(wspace=0.05, hspace=0.09)
    plt.show()
    file_name = filename
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    #plt.close(fig)


def plot_freq_dist_w_boxes_all_2_rows(d1, d2, labels, title, num_bins, colors, xlabel, filename, bin_edges, data=None,
                               ncols=2, figsize = (5.5, 5)):
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['font.serif'] = ['Times New Roman']
    fig, ax = plt.subplots(nrows=2, ncols=ncols, figsize=figsize)
    plt.rcParams.update({'font.size': 10})

    #let numpy calculate the histogram entries
    histo, bin_edges = np.histogram(data[0], 30, (0, 2300))
    bin_middles = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    print(np.array(data[0])*0.01)
    ax[0][0].hist(data[0], bins=30, alpha=1, range=(0, 2300),
            label=labels[0], stacked=False, log=True, color=colors[3], density=True, edgecolor='black', ls="-")

    normalisation = 30 / (len(data[0]) * (2300 - 0))
    y_err = np.sqrt(histo) * normalisation
    y = histo*normalisation
    y_err[0] = y_err[0] + 0.0025
    y_err[1] = y_err[1] + 0.0001
    ax[0][0].errorbar(bin_middles, y, fmt='.k', color="black", yerr=y_err)

    histo, bin_edges = np.histogram(data[1], 30, (0, 2300))
    bin_middles = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    ax[0][1].hist(data[1], bins=30, alpha=1, range=(0, 2300),
            label=labels[1], stacked=False, log=True, color=colors[2], density=True, edgecolor='black')
    normalisation = 30 / (len(data[1]) * (2300 - 0))
    y_err = np.sqrt(histo) * normalisation
    y_err[0] = y_err[0] + 0.005
    y_err[1] = y_err[1] + 0.00001
    y = histo * normalisation
    ax[0][1].errorbar(bin_middles, y, fmt='.k', color="black", yerr=y_err)

    histo, bin_edges = np.histogram(data[2], 30, (0, 2300))
    bin_middles = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    ax[1][0].hist(data[2], bins=30, alpha=1, range=(0, 2300),
            label=labels[2], stacked=False, log=True, color=colors[1], density=True, edgecolor='black')
    normalisation = 30 / (len(data[2]) * (2300 - 0))
    y_err = np.sqrt(histo) * normalisation
    y_err[0] = y_err[0] + 0.005
    y_err[1] = y_err[1] + 0.00001
    y = histo * normalisation
    ax[1][0].errorbar(bin_middles, y, fmt='.k', color="black", yerr=y_err)

    histo, bin_edges = np.histogram(data[3], 30, (0, 2300))
    bin_middles = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    ax[1][1].hist(data[3], bins=30, alpha=1, range=(0, 2300),
            label=labels[3], stacked=False, log=True, color=colors[0], density=True, edgecolor='black')
    normalisation = 30 / (len(data[3]) * (2300 - 0))
    y_err = np.sqrt(histo) * normalisation
    y_err[0] = y_err[0] + 0.005
    y_err[1] = y_err[1] + 0.00001
    y = histo * normalisation
    ax[1][1].errorbar(bin_middles, y, fmt='.k', color="black", yerr=y_err)

    colors = ["#f9a65a", "#661D98", "#377EB8", "#4DAF4A", "#A65628", "#F781BF",
              '#D95F02', '#7570B3', '#E7298A', '#E6AB02', '#A6761D', '#666666',
              '#8DD3C7', '#CCEBC5', '#BEBADA', '#FB8072', "#FF7F00", '#80B1D3', '#FDB462', '#B3DE69', '#FCCDE5',
              '#D9D9D9', '#BC80BD', '#FFED6F', "blue", "#984EA3", "green", "#FFFF33", '#66A61E', '#FFFFB3',
              "purple", "orange", "browen", "ppink", "#1B9E77", "#E41A1C"]
    ax[0][0].set_title(title)
    ax[0][0].set_xlabel(xlabel, fontsize=20)
    ax[0][0].set_ylabel(r"Normalized Frequency", fontsize=20)
    ax[0][0].grid('on')
    ax[0][0].xaxis.set_tick_params(size=0)
    ax[0][0].yaxis.set_tick_params(size=0)
    ax[0][0].spines['right'].set_color((.8, .8, .8))
    ax[0][0].spines['top'].set_color((.8, .8, .8))
    xlab = ax[0][0].xaxis.get_label()
    ylab = ax[0][0].yaxis.get_label()
    xlab.set_size(10)
    ylab.set_size(10)
    ax[0][0].set_xlim((0, 2300))
    if len(labels) > 1:
        ax[0][0].legend(loc="upper right")

    ax[0][1].set_title(title)
    ax[0][1].set_xlabel(xlabel, fontsize=20)
    #ax[1].set_ylabel(r"Normalized Frequency", fontsize=20)
    ax[0][1].grid('on')
    ax[0][1].xaxis.set_tick_params(size=0)
    ax[0][1].yaxis.set_tick_params(size=0)
    ax[0][1].spines['right'].set_color((.8, .8, .8))
    ax[0][1].spines['top'].set_color((.8, .8, .8))
    xlab = ax[0][1].xaxis.get_label()
    ylab = ax[0][1].yaxis.get_label()
    xlab.set_size(10)
    ylab.set_size(10)
    ax[0][1].set_xlim((0, 2300))
    if len(labels) > 1:
        ax[0][1].legend(loc="upper right")

    ax[1][0].set_title(title)
    ax[1][0].set_xlabel(xlabel, fontsize=20)
    #ax[2].set_ylabel(r"Normalized Frequency", fontsize=20)
    ax[1][0].grid('on')
    ax[1][0].xaxis.set_tick_params(size=0)
    ax[1][0].yaxis.set_tick_params(size=0)
    ax[1][0].spines['right'].set_color((.8, .8, .8))
    ax[1][0].spines['top'].set_color((.8, .8, .8))
    xlab = ax[1][0].xaxis.get_label()
    ylab = ax[1][0].yaxis.get_label()
    xlab.set_size(10)
    ylab.set_size(10)
    ax[1][0].set_xlim((0, 2300))
    if len(labels) > 1:
        ax[1][0].legend(loc="upper right")

    ax[1][1].set_title(title)
    ax[1][1].set_xlabel(xlabel, fontsize=20)
    #ax[3].set_ylabel(r"Normalized Frequency", fontsize=20)
    ax[1][1].grid('on')
    ax[1][1].xaxis.set_tick_params(size=0)
    ax[1][1].yaxis.set_tick_params(size=0)
    ax[1][1].spines['right'].set_color((.8, .8, .8))
    ax[1][1].spines['top'].set_color((.8, .8, .8))
    xlab = ax[1][1].xaxis.get_label()
    ylab = ax[1][1].yaxis.get_label()
    xlab.set_size(10)
    ylab.set_size(10)
    ax[1][1].set_xlim((0, 2300))
    if len(labels) > 1:
        ax[1][1].legend(loc="upper right")

    fig.tight_layout()
    fig.subplots_adjust(wspace=0.05, hspace=0.09)
    plt.show()
    file_name = filename
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    #plt.close(fig)


def plot_freq_dist_w_boxes_all_alerts(d1, d2, labels, title, num_bins, colors, xlabel, filename, bin_edges, data=None,
                                      data2=None, title2=None, xlabel2 = None):
    emulation_w_cache_env_response_times, emulation_w_cache_action_pred_times, \
    emulation_w_cache_grad_comp_times, emulation_w_cache_weight_update_times = read_data()

    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['font.serif'] = ['Times New Roman']
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(6, 2.5))
    plt.rcParams.update({'font.size': 10})

    #let numpy calculate the histogram entries
    histo, bin_edges = np.histogram(data, 30, (0, 260))
    bin_middles = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    print(np.array(data)*0.01)
    ax[0].hist(data, bins=30, alpha=1, range=(0, 260),
            label=labels[3], stacked=False, log=True, color=colors[0], density=True, edgecolor='black', ls="-")

    normalisation = 30 / (len(data) * (260 - 0))
    y_err = np.sqrt(histo) * normalisation
    y = histo*normalisation
    y_err[0] = y_err[0] + 0.0025
    y_err[1] = y_err[1] + 0.0001
    #ax[0].errorbar(bin_middles, y, fmt='.k', color="black", yerr=y_err)

    histo, bin_edges = np.histogram(data2, 30, (0, 260))
    bin_middles = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    ax[1].hist(data2, bins=30, alpha=1, range=(0, 260),
            label=labels[2], stacked=False, log=True, color=colors[5], density=True, edgecolor='black')
    normalisation = 30 / (len(data2) * (260 - 0))
    y_err = np.sqrt(histo) * normalisation
    y_err[0] = y_err[0] + 0.005
    y_err[1] = y_err[1] + 0.00001
    y = histo * normalisation
    #ax[1].errorbar(bin_middles, y, fmt='.k', color="black", yerr=y_err)

    perf_labels = [r"Simulation", r"Emulation", r"Emulation w. Cache"]
    bar_width = 0.35
    epsilon = .015
    line_width = 1
    opacity = 1
    pos_weight_upd = np.array([5.5, 0.005, emulation_w_cache_weight_update_times])
    pos_grad_comp = np.array([8.5, 0.005, emulation_w_cache_grad_comp_times])
    pos_action_pred = np.array([71, 0.01, emulation_w_cache_action_pred_times])
    pos_env_response = np.array([15, 99.98, emulation_w_cache_env_response_times])
    pos_other = np.array([5, 0, 0])
    pos_bar_positions = np.arange(len(pos_weight_upd))
    neg_bar_positions = pos_bar_positions + bar_width - 0.45

    # weight_update_bar = ax[2].bar(pos_bar_positions, pos_weight_upd, bar_width - epsilon,
    #                            edgecolor=colors[0],
    #                            # edgecolor='',
    #                            color="white",
    #                            label=r'Weight update',
    #                            linewidth=line_width,
    #                            hatch='OO',
    #                            alpha=opacity)
    # grad_comp_bar = ax[2].bar(pos_bar_positions, pos_grad_comp, bar_width - epsilon,
    #                        bottom=pos_weight_upd,
    #                        alpha=opacity,
    #                        color='white',
    #                        edgecolor=colors[1],
    #                        # edgecolor='black',
    #                        linewidth=line_width,
    #                        hatch='////',
    #                        label=r'Grad comp')
    # action_pred_bar = ax[2].bar(pos_bar_positions, pos_action_pred, bar_width - epsilon,
    #                          bottom=pos_grad_comp + pos_weight_upd,
    #                          alpha=opacity,
    #                          color='white',
    #                          edgecolor="black",
    #                          linewidth=line_width,
    #                          hatch='---',
    #                          label=r'Action pred')
    # env_response_bar = ax[2].bar(pos_bar_positions, pos_env_response, bar_width - epsilon,
    #                           bottom=pos_grad_comp + pos_weight_upd + pos_action_pred,
    #                           label=r'Env response',
    #                           edgecolor=colors[6],
    #                           # edgecolor='black',
    #                           color="white",
    #                           hatch='xxx',
    #                           linewidth=line_width,
    #                           alpha=opacity,
    #                           )

    # histo, bin_edges = np.histogram(data[1], 30, (0, 2300))
    # bin_middles = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    # ax[2].hist(data[1], bins=30, alpha=1, range=(0, 2300),
    #         label=labels[1], stacked=False, log=True, color=colors[1], density=True, edgecolor='black')
    # normalisation = 30 / (len(data[1]) * (2300 - 0))
    # y_err = np.sqrt(histo) * normalisation
    # y_err[0] = y_err[0] + 0.005
    # y_err[1] = y_err[1] + 0.00001
    # y = histo * normalisation
    # ax[2].errorbar(bin_middles, y, fmt='.k', color="black", yerr=y_err)
    #
    # histo, bin_edges = np.histogram(data[0], 30, (0, 2300))
    # bin_middles = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    # ax[3].hist(data[0], bins=30, alpha=1, range=(0, 2300),
    #         label=labels[0], stacked=False, log=True, color=colors[0], density=True, edgecolor='black')
    # normalisation = 30 / (len(data[0]) * (2300 - 0))
    # y_err = np.sqrt(histo) * normalisation
    # y_err[0] = y_err[0] + 0.005
    # y_err[1] = y_err[1] + 0.00001
    # y = histo * normalisation
    # ax[3].errorbar(bin_middles, y, fmt='.k', color="black", yerr=y_err)

    colors = ["#f9a65a", "#661D98", "#377EB8", "#4DAF4A", "#A65628", "#F781BF",
              '#D95F02', '#7570B3', '#E7298A', '#E6AB02', '#A6761D', '#666666',
              '#8DD3C7', '#CCEBC5', '#BEBADA', '#FB8072', "#FF7F00", '#80B1D3', '#FDB462', '#B3DE69', '#FCCDE5',
              '#D9D9D9', '#BC80BD', '#FFED6F', "blue", "#984EA3", "green", "#FFFF33", '#66A61E', '#FFFFB3',
              "purple", "orange", "browen", "ppink", "#1B9E77", "#E41A1C"]
    ax[0].set_title(title)
    ax[0].set_xlabel(xlabel, fontsize=20)
    ax[0].set_ylabel(r"Normalized Frequency", fontsize=20)
    ax[0].grid('on')
    ax[0].xaxis.set_tick_params(size=0)
    ax[0].yaxis.set_tick_params(size=0)
    ax[0].spines['right'].set_color((.8, .8, .8))
    ax[0].spines['top'].set_color((.8, .8, .8))
    xlab = ax[0].xaxis.get_label()
    ylab = ax[0].yaxis.get_label()
    xlab.set_size(10)
    ylab.set_size(10)
    ax[0].set_xlim((0, 260))
    # if len(labels) > 1:
    #     ax[0].legend(loc="upper right")

    ax[1].set_title(title2)
    ax[1].set_xlabel(xlabel2, fontsize=20)
    #ax[1].set_ylabel(r"Normalized Frequency", fontsize=20)
    ax[1].grid('on')
    ax[1].xaxis.set_tick_params(size=0)
    ax[1].yaxis.set_tick_params(size=0)
    ax[1].spines['right'].set_color((.8, .8, .8))
    ax[1].spines['top'].set_color((.8, .8, .8))
    xlab = ax[1].xaxis.get_label()
    ylab = ax[1].yaxis.get_label()
    xlab.set_size(10)
    ylab.set_size(10)
    ax[1].set_xlim((0, 260))
    # if len(labels) > 1:
    #     ax[1].legend(loc="upper right")

    #ax[2].set_title(title)
    #ax[2].set_xlabel(xlabel, fontsize=20)
    #ax[2].set_ylabel(r"Normalized Frequency", fontsize=20)
    # ax[2].grid('on')
    # # ax[2].xaxis.set_tick_params(size=0)
    # # ax[2].yaxis.set_tick_params(size=0)
    # ax[2].spines['right'].set_color((.8, .8, .8))
    # ax[2].spines['top'].set_color((.8, .8, .8))
    # xlab = ax[2].xaxis.get_label()
    # ylab = ax[2].yaxis.get_label()
    # xlab.set_size(10)
    # ylab.set_size(10)
    # ax[2].set_ylim((0, 100))
    # ax[2].set_xticks(neg_bar_positions)
    # ax[2].set_xticklabels(labels, rotation=45)
    # ax[2].patch.set_edgecolor('black')
    # ax[2].patch.set_linewidth('1')
    # ax[2].set_ylabel(r'Percentage $(\%)$')
    # ax[2].legend(loc='upper center', bbox_to_anchor=(0.5, 1.35),
    #           ncol=2, fancybox=True, shadow=True, fontsize=8)

    fig.tight_layout()
    fig.subplots_adjust(wspace=0.05, hspace=0.09)
    plt.show()
    file_name = filename
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    #plt.close(fig)


def plot_profiling(d1, d2, labels, title, num_bins, colors, xlabel, filename, bin_edges, data=None,
                                      data2=None, title2=None, xlabel2 = None):
    emulation_w_cache_env_response_times, emulation_w_cache_action_pred_times, \
    emulation_w_cache_grad_comp_times, emulation_w_cache_weight_update_times = read_data()

    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['font.serif'] = ['Times New Roman']
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(2.75, 3.2))
    plt.rcParams.update({'font.size': 10})

    perf_labels = [r"Simulation", r"Emulation", r"Emulation w. Cache"]
    bar_width = 0.35
    epsilon = .015
    line_width = 1
    opacity = 1
    pos_weight_upd = np.array([5.5, 0.005, emulation_w_cache_weight_update_times])
    pos_grad_comp = np.array([8.5, 0.005, emulation_w_cache_grad_comp_times])
    pos_action_pred = np.array([71, 0.01, emulation_w_cache_action_pred_times])
    pos_env_response = np.array([15, 99.98, emulation_w_cache_env_response_times])
    pos_other = np.array([5, 0, 0])
    pos_bar_positions = np.arange(len(pos_weight_upd))
    neg_bar_positions = pos_bar_positions + bar_width - 0.45

    weight_update_bar = ax.bar(pos_bar_positions, pos_weight_upd, bar_width - epsilon,
                               edgecolor=colors[0],
                               # edgecolor='',
                               color="white",
                               label=r'Weight update',
                               linewidth=line_width,
                               hatch='OO',
                               alpha=opacity)
    grad_comp_bar = ax.bar(pos_bar_positions, pos_grad_comp, bar_width - epsilon,
                           bottom=pos_weight_upd,
                           alpha=opacity,
                           color='white',
                           edgecolor=colors[1],
                           # edgecolor='black',
                           linewidth=line_width,
                           hatch='////',
                           label=r'Grad comp')
    action_pred_bar = ax.bar(pos_bar_positions, pos_action_pred, bar_width - epsilon,
                             bottom=pos_grad_comp + pos_weight_upd,
                             alpha=opacity,
                             color='white',
                             edgecolor="black",
                             linewidth=line_width,
                             hatch='---',
                             label=r'Action pred')
    env_response_bar = ax.bar(pos_bar_positions, pos_env_response, bar_width - epsilon,
                              bottom=pos_grad_comp + pos_weight_upd + pos_action_pred,
                              label=r'Env response',
                              edgecolor=colors[6],
                              # edgecolor='black',
                              color="white",
                              hatch='xxx',
                              linewidth=line_width,
                              alpha=opacity,
                              )

    # histo, bin_edges = np.histogram(data[1], 30, (0, 2300))
    # bin_middles = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    # ax[2].hist(data[1], bins=30, alpha=1, range=(0, 2300),
    #         label=labels[1], stacked=False, log=True, color=colors[1], density=True, edgecolor='black')
    # normalisation = 30 / (len(data[1]) * (2300 - 0))
    # y_err = np.sqrt(histo) * normalisation
    # y_err[0] = y_err[0] + 0.005
    # y_err[1] = y_err[1] + 0.00001
    # y = histo * normalisation
    # ax[2].errorbar(bin_middles, y, fmt='.k', color="black", yerr=y_err)
    #
    # histo, bin_edges = np.histogram(data[0], 30, (0, 2300))
    # bin_middles = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    # ax[3].hist(data[0], bins=30, alpha=1, range=(0, 2300),
    #         label=labels[0], stacked=False, log=True, color=colors[0], density=True, edgecolor='black')
    # normalisation = 30 / (len(data[0]) * (2300 - 0))
    # y_err = np.sqrt(histo) * normalisation
    # y_err[0] = y_err[0] + 0.005
    # y_err[1] = y_err[1] + 0.00001
    # y = histo * normalisation
    # ax[3].errorbar(bin_middles, y, fmt='.k', color="black", yerr=y_err)

    colors = ["#f9a65a", "#661D98", "#377EB8", "#4DAF4A", "#A65628", "#F781BF",
              '#D95F02', '#7570B3', '#E7298A', '#E6AB02', '#A6761D', '#666666',
              '#8DD3C7', '#CCEBC5', '#BEBADA', '#FB8072', "#FF7F00", '#80B1D3', '#FDB462', '#B3DE69', '#FCCDE5',
              '#D9D9D9', '#BC80BD', '#FFED6F', "blue", "#984EA3", "green", "#FFFF33", '#66A61E', '#FFFFB3',
              "purple", "orange", "browen", "ppink", "#1B9E77", "#E41A1C"]
    # ax[0].set_title(title)
    # ax[0].set_xlabel(xlabel, fontsize=20)
    # ax[0].set_ylabel(r"Normalized Frequency", fontsize=20)
    # ax[0].grid('on')
    # ax[0].xaxis.set_tick_params(size=0)
    # ax[0].yaxis.set_tick_params(size=0)
    # ax[0].spines['right'].set_color((.8, .8, .8))
    # ax[0].spines['top'].set_color((.8, .8, .8))
    # xlab = ax[0].xaxis.get_label()
    # ylab = ax[0].yaxis.get_label()
    # xlab.set_size(10)
    # ylab.set_size(10)
    # ax[0].set_xlim((0, 260))
    # # if len(labels) > 1:
    # #     ax[0].legend(loc="upper right")
    #
    # ax[1].set_title(title2)
    # ax[1].set_xlabel(xlabel2, fontsize=20)
    # #ax[1].set_ylabel(r"Normalized Frequency", fontsize=20)
    # ax[1].grid('on')
    # ax[1].xaxis.set_tick_params(size=0)
    # ax[1].yaxis.set_tick_params(size=0)
    # ax[1].spines['right'].set_color((.8, .8, .8))
    # ax[1].spines['top'].set_color((.8, .8, .8))
    # xlab = ax[1].xaxis.get_label()
    # ylab = ax[1].yaxis.get_label()
    # xlab.set_size(10)
    # ylab.set_size(10)
    # ax[1].set_xlim((0, 260))
    # # if len(labels) > 1:
    # #     ax[1].legend(loc="upper right")

    #ax.set_title(title)
    #ax.set_xlabel(xlabel, fontsize=20)
    #ax.set_ylabel(r"Normalized Frequency", fontsize=20)
    ax.grid('on')
    # ax[2].xaxis.set_tick_params(size=0)
    # ax[2].yaxis.set_tick_params(size=0)
    ax.spines['right'].set_color((.8, .8, .8))
    ax.spines['top'].set_color((.8, .8, .8))
    xlab = ax.xaxis.get_label()
    ylab = ax.yaxis.get_label()
    xlab.set_size(10)
    ylab.set_size(10)
    ax.set_ylim((0, 100))
    ax.set_xticks(neg_bar_positions)
    ax.set_xticklabels(perf_labels, rotation=45)
    ax.patch.set_edgecolor('black')
    ax.patch.set_linewidth('1')
    ax.set_ylabel(r'Percentage $(\%)$')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.35),
              ncol=2, fancybox=True, shadow=True, fontsize=8)

    fig.tight_layout()
    fig.subplots_adjust(top=0.78)
    plt.show()
    file_name = filename
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    #plt.close(fig)


if __name__ == '__main__':
    # plot_action_types_pie(PyCrCTFSimpleBase.all_actions_conf(
    #     num_nodes=PyCrCTFSimpleBase.num_nodes(),
    #     subnet_mask=PyCrCTFSimpleBase.subnet_mask(),
    #     hacker_ip=PyCrCTFSimpleBase.hacker_ip()
    # ))

    cm = plt.cm.get_cmap('RdYlBu_r')
    colors = plt.cm.GnBu(np.linspace(0.3, 1, 4))[-4:]
    colors = plt.cm.viridis(np.linspace(0.3, 1, 4))[-4:]
    print(colors[0])
    print(len(colors))

    # d_1 = read_action_costs(zip_file="/home/kim/storage/workspace/pycr/cluster-envs/minigames/network_intrusion/ctf/001/level_1/agent_cache.zip", num_bins=100)
    # d_2 = read_action_costs(zip_file="/home/kim/storage/workspace/pycr/cluster-envs/minigames/network_intrusion/ctf/001/level_2/agent_cache.zip", num_bins=100)
    #plot_freq_dist(d1=d_1,d2=d_2, num_bins=100)

    d_1, d_factors, bin_edges, costs_factors = read_action_costs(
        zip_file="/home/kim/pycr/cluster-envs/minigames/network_intrusion/ctf/001/level_6/merged.zip",
        num_bins=100, factors=[2, 3, 4])

    # plot_freq_dist(d1=d_1, d2=d_factors, num_bins=100, labels=[r"$|\mathcal{N}|=25$", r"$|\mathcal{N}|=50$", r"$|\mathcal{N}|=75$", r"$|\mathcal{N}|=100$"],
    # title=r"Action execution times (costs)", xlabel=r"Time Cost (s)", colors=colors,
    # filename="action_cost_dist_plot", bin_edges=bin_edges, data=costs_factors)

    # plot_freq_dist_w_boxes(d1=d_1, d2=d_factors, num_bins=100,
    #                labels=[r"$|\mathcal{N}|=25$", r"$|\mathcal{N}|=50$", r"$|\mathcal{N}|=75$", r"$|\mathcal{N}|=100$"],
    #                title=r"Action execution times (costs)", xlabel=r"Time Cost (s)", colors=colors,
    #                filename="action_cost_dist_plot_25", bin_edges=bin_edges, data=costs_factors)

    # plot_freq_dist_w_boxes_all(d1=d_1, d2=d_factors, num_bins=100,
    #                        labels=[r"$|\mathcal{N}|=25$", r"$|\mathcal{N}|=50$", r"$|\mathcal{N}|=75$",
    #                                r"$|\mathcal{N}|=100$"],
    #                        title=r"Action execution times (costs)", xlabel=r"Time Cost (s)", colors=colors,
    #                        filename="action_cost_dist_plot_all_boxes", bin_edges=bin_edges, data=costs_factors,
    #                        ncols=4, figsize=(11, 2.5))

    plot_freq_dist_w_boxes_all_2_rows(d1=d_1, d2=d_factors, num_bins=100,
                               labels=[r"$|\mathcal{N}|=25$", r"$|\mathcal{N}|=50$", r"$|\mathcal{N}|=75$",
                                       r"$|\mathcal{N}|=100$"],
                               title=r"Action execution times (costs)", xlabel=r"Time Cost (s)", colors=colors,
                               filename="action_cost_dist_plot_all_boxes_2_rows", bin_edges=bin_edges, data=costs_factors,
                               ncols=2, figsize=(8, 5))

    #
    # colors = ["r"]

    # total_alerts, total_priority = read_action_alerts(
    #     zip_file="/home/kim/pycr/cluster-envs/minigames/network_intrusion/ctf/001/level_6/merged.zip",
    #     num_bins=250)

    #print(max(digitized_total))
    # plot_freq_dist(d1=None, d2=None,
    #                labels=[r"test"],title=r"Intrusion detection alerts per action", num_bins=30,
    #                colors=colors, xlabel=r"Number of triggered alerts",
    #                filename="action_alerts_dist_plot", data=total_alerts, bin_edges = None)

    #colors=["#599ad3"]
    # plot_freq_dist(d1=None, d2=None,
    #                labels=[r"test"], title=r"Intrusion detection alerts total priority $\sum_a p(a)$ per action", num_bins=30,
    #                colors=colors, xlabel=r"Total priority of triggered alerts",
    #                filename="action_alerts_priority_dist_plot", data=total_priority, bin_edges=None)

    # colors = ["#599ad3"]
    # cm = plt.cm.get_cmap('OrRd_r')
    # #colors = plt.cm.OrRd_r(np.linspace(0.3, 1, 4))[-4:]
    # colors = plt.cm.OrRd_r(np.linspace(0.3, 1, 10))
    #
    # plot_freq_dist_w_boxes_all_alerts(d1=None, d2=None, num_bins=30,
    #                            labels=[r"$|\mathcal{N}|=25$", r"$|\mathcal{N}|=50$", r"$|\mathcal{N}|=75$",
    #                                    r"$|\mathcal{N}|=100$"],
    #                            title=r"Intrusion detection alerts per action", xlabel=r"Number of triggered alerts",
    #                            colors=colors,
    #                            filename="action_alerts_dist_plot_all_boxes", bin_edges=None, data=total_alerts,
    #                                   data2=total_priority, title2="Alerts priority $\sum_a p(a)$ per action",
    #                                   xlabel2="Total priority of triggered alerts")
    # plot_profiling(d1=None, d2=None, num_bins=30,
    #                                   labels=[r"$|\mathcal{N}|=25$", r"$|\mathcal{N}|=50$", r"$|\mathcal{N}|=75$",
    #                                           r"$|\mathcal{N}|=100$"],
    #                                   title=r"Intrusion detection alerts per action",
    #                                   xlabel=r"Number of triggered alerts",
    #                                   colors=colors,
    #                                   filename="training_iter_profiling", bin_edges=None, data=total_alerts,
    #                                   data2=total_priority, title2="Alerts priority $\sum_a p(a)$ per action",
    #                                   xlabel2="Total priority of triggered alerts")

