from typing import List, Union
import numpy as np
import matplotlib.pyplot as plt
from csle_common.metastore.metastore_facade import MetastoreFacade


def plot(f1_values, f1_0, f1_1, f1_kl, f1_total_KL,
         f2_values, f2_0, f2_1, f2_kl, f2_total_KL,
         f3_values, f3_0, f3_1, f3_kl, f3_total_KL,
         f4_values, f4_0, f4_1, f4_kl, f4_total_KL,
         f5_values, f5_0, f5_1, f5_kl, f5_total_KL,
         f6_values, f6_0, f6_1, f6_kl, f6_total_KL,
         file_name: str, fontsize: int = 18) -> None:
    """
    Plots KL divergence of feature distributions during intrusion and during normal operation

    :param f1_values: values of feature 1
    :param f1_0: distribution of feature 1 during normal operation
    :param f1_1: distribution of feature 1 during intrusion
    :param f1_kl: KL divergence of feature 1 during normal operation and intrusion for each value
    :param f1_total_KL: Total KL divergence of feature 1 during normal operation and intrusion
    :param f2_values: values of feature 2
    :param f2_0: distribution of feature 2 during normal operation
    :param f2_1: distribution of feature 2 during intrusion
    :param f2_kl: KL divergence of feature 2 during normal operation and intrusion for each value
    :param f2_total_KL: Total KL divergence of feature 2 during normal operation and intrusion
    :param f3_values: values of feature 3
    :param f3_0: distribution of feature 3 during normal operation
    :param f3_1: distribution of feature 3 during intrusion
    :param f3_kl: KL divergence of feature 3 during normal operation and intrusion for each value
    :param f3_total_KL: Total KL divergence of feature 3 during normal operation and intrusion
    :param f4_values: values of feature 4
    :param f4_0: distribution of feature 4 during normal operation
    :param f4_1: distribution of feature 4 during intrusion
    :param f4_kl: KL divergence of feature 4 during normal operation and intrusion for each value
    :param f4_total_KL: Total KL divergence of feature 4 during normal operation and intrusion
    :param f5_values: values of feature 5
    :param f5_0: distribution of feature 5 during normal operation
    :param f5_1: distribution of feature 5 during intrusion
    :param f5_kl: KL divergence of feature 5 during normal operation and intrusion for each value
    :param f5_total_KL: Total KL divergence of feature 5 during normal operation and intrusion
    :param f6_values: values of feature 6
    :param f6_0: distribution of feature 6 during normal operation
    :param f6_1: distribution of feature 6 during intrusion
    :param f6_kl: KL divergence of feature 6 during normal operation and intrusion for each value
    :param f6_total_KL: Total KL divergence of feature 6 during normal operation and intrusion
    :param file_name: filename to save the plot
    :param fontsize: fontsize for plotting
    :return: None
    """
    markevery = 10
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts,amsmath}')
    plt.rcParams['axes.linewidth'] = 0.8
    plt.rcParams.update({'font.size': fontsize})
    plt.rcParams['font.family'] = ['serif']
    fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(7.8, 5))
    ax[0][0].plot(f1_values, f1_0, label=r"$f_{O \mid s=0}$ (no intrusion)", ls='-', color="r", markevery=markevery,
                  markersize=2.5,
                  lw=1, alpha=0.5)
    ax[0][0].plot(f1_values, f1_1, label=r"$f_{O \mid s=1}$ (intrusion)", ls='-.',
                  color="blue", markevery=markevery, markersize=2.5, lw=1, alpha=0.5)
    ax[0][0].plot(f1_values, f1_kl, label=r"$D_{\mathrm{KL}}(f_{O \mid s=0} \parallel f_{O \mid s=1})$", ls='--',
                  color="black", markevery=markevery, markersize=2.5,
                  lw=1, alpha=0.2)
    ax[0][0].set_xlim(0, max(f1_values))
    ax[0][0].set_ylim(min(f1_kl), max(f1_kl))
    ax[0][0].spines['top'].set_visible(False)
    ax[0][0].spines['right'].set_visible(False)
    ax[0][0].set_yticks([])
    ax[0][0].set_ylabel(r"Probability/Divergence", fontsize=fontsize)
    ax[0][0].set_title(
        "Alerts weighted by priority\n" + r"$D_{\mathrm{KL}}(f_{O \mid s_t=0} \parallel f_{O \mid s_t=1})="
        + str(f1_total_KL) + "$", fontsize=fontsize)

    ax[0][1].plot(f2_values, f2_0, label=r"$f_{O \mid s_t=0}$", ls='-', color="r", markevery=markevery, markersize=2.5,
                  lw=1, alpha=0.5)
    ax[0][1].plot(f2_values, f2_1, label=r"$f_{O \mid s_t=1}$", ls='-.',
                  color="blue", markevery=markevery, markersize=2.5, lw=1, alpha=0.5)
    ax[0][1].plot(f2_values, f2_kl, label=r"$D_{\mathrm{KL}}(f_{O \mid s_t=0} \parallel f_{O \mid s_t=1})$", ls='--',
                  color="black", markevery=markevery, markersize=2.5,
                  lw=1, alpha=0.2)
    ax[0][1].set_ylim(min(f2_kl), max(f2_0))
    ax[0][1].spines['top'].set_visible(False)
    ax[0][1].spines['right'].set_visible(False)
    ax[0][1].set_yticks([])
    ax[0][1].set_ylabel("")
    ax[0][1].set_title("New failed login attempts\n" + r"$D_{\mathrm{KL}}(f_{O \mid s_t=0} \parallel f_{O \mid s_t=1})="
                       + str(f2_total_KL) + "$", fontsize=fontsize)

    ax[0][2].plot(f3_values, f3_0, label=r"$f_{O \mid s_t=0}$", ls='-', color="r", markevery=markevery, markersize=2.5,
                  lw=1, alpha=0.5)
    ax[0][2].plot(f3_values, f3_1, label=r"$f_{O \mid s_t=1}$", ls='-.',
                  color="blue", markevery=markevery, markersize=2.5, lw=1, alpha=0.5)
    ax[0][2].plot(f3_values, f3_kl, label=r"$D_{\mathrm{KL}}(f_{O \mid s_t=0} \parallel f_{O \mid s_t=1})$", ls='--',
                  color="black", markevery=markevery, markersize=2.5,
                  lw=1, alpha=0.2)
    ax[0][2].set_ylim(min(f3_kl), max(f3_0))
    ax[0][2].spines['top'].set_visible(False)
    ax[0][2].spines['right'].set_visible(False)
    ax[0][2].set_yticks([])
    ax[0][2].set_ylabel("")
    ax[0][2].set_title("\# New processes\n" + r"$D_{\mathrm{KL}}(f_{O \mid s_t=0} \parallel f_{O \mid s_t=1})="
                       + str(f3_total_KL) + "$", fontsize=fontsize)

    ax[1][0].plot(f4_values, f4_0, label=r"$f_{O \mid s_t=0}$", ls='-', color="r", markevery=markevery, markersize=2.5,
                  lw=1, alpha=0.5)
    ax[1][0].plot(f4_values, f4_1, label=r"$f_{O \mid s_t=1}$", ls='-.',
                  color="blue", markevery=markevery, markersize=2.5, lw=1, alpha=0.5)
    ax[1][0].plot(f4_values, f4_kl, label=r"$D_{\mathrm{KL}}(f_{O \mid s_t=0} \parallel f_{O \mid s_t=1})$", ls='--',
                  color="black", markevery=markevery, markersize=2.5,
                  lw=1, alpha=0.2)
    ax[1][0].set_ylim(min(f4_kl), max(f4_0))
    ax[1][0].spines['top'].set_visible(False)
    ax[1][0].spines['right'].set_visible(False)
    # ax[1][0].set_xlabel(r"O")
    ax[1][0].set_yticks([])
    ax[1][0].set_ylabel(r"Probability/Divergence", fontsize=fontsize)
    ax[1][0].set_title(
        r"New \textsc{tcp} connections" + "\n" + r"$D_{\mathrm{KL}}(f_{O \mid s_t=0} \parallel f_{O \mid s_t=1})="
        + str(f4_total_KL) + "$", fontsize=fontsize)

    ax[1][1].plot(f5_values, f5_0, label=r"$f_{O \mid s_t=0}$", ls='-', color="r", markevery=markevery, markersize=2.5,
                  lw=1, alpha=0.5)
    ax[1][1].plot(f5_values, f5_1, label=r"$f_{O \mid s_t=1}$", ls='-.',
                  color="blue", markevery=markevery, markersize=2.5, lw=1, alpha=0.5)
    ax[1][1].plot(f5_values, f5_kl, label=r"$D_{\mathrm{KL}}(f_{O \mid s_t=0} \parallel f_{O \mid s_t=1})$", ls='--',
                  color="black", markevery=markevery, markersize=2.5,
                  lw=1, alpha=0.2)
    ax[1][1].set_ylim(min(f5_kl), max(f5_0))
    ax[1][1].spines['top'].set_visible(False)
    ax[1][1].spines['right'].set_visible(False)
    ax[1][1].set_yticks([])
    ax[1][1].set_title(
        r"\# Blocks written to disk" + "\n" + r"$D_{\mathrm{KL}}(f_{O \mid s_t=0} \parallel f_{O \mid s_t=1})="
        + str(f5_total_KL) + "$", fontsize=fontsize)

    ax[1][2].plot(f6_values, f6_0, label=r"$f_{O \mid s_t=0}$", ls='-', color="r", markevery=markevery, markersize=2.5,
                  lw=1, alpha=0.5)
    ax[1][2].plot(f6_values, f6_1, label=r"$f_{O \mid s_t=1}$", ls='-.',
                  color="blue", markevery=markevery, markersize=2.5, lw=1, alpha=0.5)
    ax[1][2].plot(f6_values, f6_kl, label=r"$D_{\mathrm{KL}}(f_{O \mid s_t=0} \parallel f_{O \mid s_t=1})$", ls='--',
                  color="black", markevery=markevery, markersize=2.5,
                  lw=1, alpha=0.2)
    ax[1][2].set_ylim(min(f6_kl), max(f6_0))
    ax[1][2].spines['top'].set_visible(False)
    ax[1][2].spines['right'].set_visible(False)
    ax[1][2].set_yticks([])
    ax[1][2].set_title(
        r"\# Blocks read from disk" + "\n" + r"$D_{\mathrm{KL}}(f_{O \mid s_t=0} \parallel f_{O \mid s_t=1})="
        + str(f6_total_KL) + "$", fontsize=fontsize)

    handles, labels = ax[0][0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.52, 0.0835),
               ncol=8, fancybox=False, shadow=False, handletextpad=0.4, labelspacing=0.5, columnspacing=0.65,
               prop={'size': fontsize}, fontsize=fontsize)

    fig.tight_layout()
    fig.subplots_adjust(wspace=0.0, hspace=0.42, bottom=0.114)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight')
    fig.savefig(file_name + ".eps", format='eps', dpi=600, bbox_inches='tight')
    plt.show()


def KL(P, Q, list=False) -> Union[float, List[float]]:
    """
    Computes the KL divergence between two probability distributions

    :param P: the first probability distribution
    :param Q: the second probability distribution
    :param list: whether the result should be a list of Kls or just the sum
    :return: the KL divergence
    """
    if not list:
        return np.sum(P * np.log(P / Q))
    else:
        return P * np.log(P / Q)


if __name__ == '__main__':
    f1_0 = np.array([0.8, 0.1, 0.05, 0.05])
    f1_1 = np.array([0.9, 0.1, 0.0, 0.0])
    f1_values = list(range(len(f1_0)))
    f1_kl = KL(f1_0, f1_1, list=True)
    statistic = MetastoreFacade.get_emulation_statistic(id=3)

    # F1
    f1_0_d = statistic.conditionals_probs["no_intrusion"]["alerts_weighted_by_priority"]
    f1_1_d = statistic.conditionals_probs["intrusion"]["alerts_weighted_by_priority"]
    f1_values = list(set(list(f1_0_d.keys()) + list(f1_1_d.keys())))
    f1_values.sort()
    f1_0 = []
    f1_1 = []
    f1_values_2 = []
    for val in f1_values:
        if val >= 9000:
            continue
        if val in f1_0_d:
            f1_0.append(f1_0_d[val])
        else:
            f1_0.append(0.00001)
        if val in f1_1_d:
            f1_1.append(f1_1_d[val])
        else:
            f1_1.append(0.00001)
        f1_values_2.append(val)
    f1_0 = np.array(f1_0)
    f1_1 = np.array(f1_1)
    f1_kl = KL(f1_0, f1_1, list=True)
    f1_total_kl = round(KL(f1_0, f1_1, list=False), 2)
    f1_values = f1_values_2

    # F2
    f2_0_d = statistic.conditionals_probs["no_intrusion"]["num_failed_login_attempts"]
    f2_1_d = statistic.conditionals_probs["intrusion"]["num_failed_login_attempts"]
    f2_values = list(set(list(f2_0_d.keys()) + list(f2_1_d.keys())))
    f2_values.sort()
    f2_0 = []
    f2_1 = []
    f2_values_2 = []
    for val in f2_values:
        # if val >= 9000:
        #     continue
        if val in f2_0_d:
            f2_0.append(f2_0_d[val])
        else:
            f2_0.append(0.00001)
        if val in f2_1_d:
            f2_1.append(f2_1_d[val])
        else:
            f2_1.append(0.00001)
        f2_values_2.append(val)
    f2_0 = np.array(f2_0)
    f2_1 = np.array(f2_1)
    f2_kl = KL(f2_0, f2_1, list=True)
    f2_total_kl = round(KL(f2_0, f2_1, list=False), 2)
    f2_values = f2_values_2

    # F3
    f3_0_d = statistic.conditionals_probs["no_intrusion"]["num_processes"]
    f3_1_d = statistic.conditionals_probs["intrusion"]["num_processes"]
    f3_values = list(set(list(f3_0_d.keys()) + list(f3_1_d.keys())))
    f3_values.sort()
    f3_0 = []
    f3_1 = []
    f3_values_2 = []
    for val in f3_values:
        # if val >= 9000:
        #     continue
        if val in f3_0_d:
            f3_0.append(f3_0_d[val])
        else:
            f3_0.append(0.00001)
        if val in f3_1_d:
            f3_1.append(f3_1_d[val])
        else:
            f3_1.append(0.00001)
        f3_values_2.append(val)
    f3_0 = np.array(f3_0)
    f3_1 = np.array(f3_1)
    f3_kl = KL(f3_0, f3_1, list=True)
    f3_total_kl = round(KL(f3_0, f3_1, list=False), 2)
    f3_values = f3_values_2

    # F4
    f4_0_d = statistic.conditionals_probs["no_intrusion"]["num_open_connections"]
    f4_1_d = statistic.conditionals_probs["intrusion"]["num_open_connections"]
    f4_values = list(set(list(f4_0_d.keys()) + list(f4_1_d.keys())))
    f4_values.sort()
    f4_0 = []
    f4_1 = []
    f4_values_2 = []
    for val in f4_values:
        if val <= -100:
            continue
        if val in f4_0_d:
            f4_0.append(f4_0_d[val])
        else:
            f4_0.append(0.00001)
        if val in f4_1_d:
            f4_1.append(f4_1_d[val])
        else:
            f4_1.append(0.00001)
        f4_values_2.append(val)
    f4_0 = np.array(f4_0)
    f4_1 = np.array(f4_1)
    f4_kl = KL(f4_0, f4_1, list=True)
    f4_total_kl = round(KL(f4_0, f4_1, list=False), 2)
    f4_values = f4_values_2

    # F5
    f5_0_d = statistic.conditionals_probs["no_intrusion"]["blk_write"]
    f5_1_d = statistic.conditionals_probs["intrusion"]["blk_write"]
    f5_values = list(set(list(f5_0_d.keys()) + list(f5_1_d.keys())))
    f5_values.sort()
    f5_0 = []
    f5_1 = []
    f5_values_2 = []
    for val in f5_values:
        # if val <= -100:
        #     continue
        if val in f5_0_d:
            f5_0.append(f5_0_d[val])
        else:
            f5_0.append(0.00001)
        if val in f5_1_d:
            f5_1.append(f5_1_d[val])
        else:
            f5_1.append(0.00001)
        f5_values_2.append(val)
    f5_0 = np.array(f5_0)
    f5_1 = np.array(f5_1)
    f5_kl = KL(f5_0, f5_1, list=True)
    f5_total_kl = round(KL(f5_0, f5_1, list=False), 2)
    f5_values = f5_values_2

    # F6
    f6_0_d = statistic.conditionals_probs["no_intrusion"]["blk_read"]
    f6_1_d = statistic.conditionals_probs["intrusion"]["blk_read"]
    f6_values = list(set(list(f6_0_d.keys()) + list(f6_1_d.keys())))
    f6_values.sort()
    f6_0 = []
    f6_1 = []
    f6_values_2 = []
    for val in f6_values:
        # if val <= -100:
        #     continue
        if val in f6_0_d:
            f6_0.append(f6_0_d[val])
        else:
            f6_0.append(0.00001)
        if val in f6_1_d:
            f6_1.append(f6_1_d[val])
        else:
            f6_1.append(0.00001)
        f6_values_2.append(val)
    f6_0 = np.array(f6_0)
    f6_1 = np.array(f6_1)
    f6_kl = KL(f6_0, f6_1, list=True)
    f6_total_kl = round(KL(f6_0, f6_1, list=False), 2)
    f6_values = f6_values_2

    plot(f1_values=f1_values, f1_0=f1_0, f1_1=f1_1, f1_kl=f1_kl, f1_total_KL=f1_total_kl,
         f2_values=f2_values, f2_0=f2_0, f2_1=f2_1, f2_kl=f2_kl, f2_total_KL=f2_total_kl,
         f3_values=f3_values, f3_0=f3_0, f3_1=f3_1, f3_kl=f3_kl, f3_total_KL=f3_total_kl,
         f4_values=f4_values, f4_0=f4_0, f4_1=f4_1, f4_kl=f4_kl, f4_total_KL=f4_total_kl,
         f5_values=f5_values, f5_0=f5_0, f5_1=f5_1, f5_kl=f5_kl, f5_total_KL=f5_total_kl,
         f6_values=f6_values, f6_0=f6_0, f6_1=f6_1, f6_kl=f6_kl, f6_total_KL=f6_total_kl,
         file_name="kl", fontsize=12)
