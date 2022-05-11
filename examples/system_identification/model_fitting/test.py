from csle_common.metastore.metastore_facade import MetastoreFacade
import csle_common.constants.constants as constants
import csle_collector.constants.constants as collector_constants
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
import numpy as np
from scipy.stats import norm
from typing import List
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as tick

def reformat_large_tick_values(tick_val, pos):
    """
    Turns large tick values (in the billions, millions and thousands) such as 4500 into 4.5K and also appropriately turns 4000 into 4K (no zero after the decimal).
    """
    if tick_val >= 1000000000:
        val = round(tick_val / 1000000000, 1)
        new_tick_format = '{:}B'.format(val)
    elif tick_val >= 1000000:
        val = round(tick_val / 1000000, 1)
        new_tick_format = '{:}M'.format(val)
    elif tick_val >= 1000:
        val = round(tick_val / 1000, 1)
        new_tick_format = '{:}K'.format(val)
    elif tick_val < 1000:
        new_tick_format = round(tick_val, 1)
    else:
        new_tick_format = tick_val

    # make new_tick_format into a string value
    new_tick_format = str(new_tick_format)

    # code below will keep 4.5M as is but change values such as 4.0M to 4M since that zero after the decimal isn't needed
    index_of_decimal = new_tick_format.find(".")

    if index_of_decimal != -1:
        value_after_decimal = new_tick_format[index_of_decimal + 1]
        if value_after_decimal == "0":
            # remove the 0 after the decimal point since it's not needed
            new_tick_format = new_tick_format[0:index_of_decimal] + new_tick_format[index_of_decimal + 2:]

    return new_tick_format


def plot(X_intrusion, X_no_intrusion, gmm_intrusion, gmm_no_intrusion):


    fontsize = 7.5
    # figsize = (7.5, 3.25)
    figsize = (4.1, 2.2)
    title_fontsize = 8
    lw = 0.75
    wspace = 0.19
    hspace = 0.02
    markevery = 10
    labelsize = 7
    sample_step = 1
    markersize = 2.25
    file_name = 'ids_distribution'
    bottom = 0.125

    X_intrusion.sort()
    X_no_intrusion.sort()

    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts,amsmath}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['axes.titlepad'] = 0.02
    # plt.rcParams['xtick.major.pad'] = 0.5
    plt.rcParams['ytick.major.pad'] = 0.05
    plt.rcParams['axes.labelpad'] = 0.8
    plt.rcParams['axes.linewidth'] = 0.3
    plt.rcParams.update({'font.size': fontsize})

    colors = plt.cm.GnBu(np.linspace(0.3, 1, 4))[-4:]
    colors = plt.cm.viridis(np.linspace(0.3, 1, 4))[-4:]

    # plt.rcParams['font.serif'] = ['Times New Roman']

    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=figsize)
    alpha = 0.7
    bins = 75
    plot_range = (0, 9000)
    ax[0].hist(X_no_intrusion[::sample_step], bins=bins, alpha=alpha, range=plot_range,
                label=r"Distribution $s_t=0$", stacked=False, log=False, color="r", density=True,
                edgecolor='black', ls="-.", lw=0.5)
    t=1
    for weight, mean, covar in zip(gmm_no_intrusion.weights_, gmm_no_intrusion.means_, gmm_no_intrusion.covariances_):
        # a.append(weight*norm.pdf(X_no_intrusion, mean, np.sqrt(covar)).ravel())
        if t==1:
            ax[0].plot(X_no_intrusion[::sample_step], weight*norm.pdf(X_no_intrusion[::sample_step], mean, np.sqrt(covar)).ravel(),
                       ls='-', color="black", lw=0.75, label=r"Fitted model")
        else:
            ax[0].plot(X_no_intrusion[::sample_step], weight*norm.pdf(X_no_intrusion[::sample_step], mean, np.sqrt(covar)).ravel(),
                       ls='-', color="black", lw=0.75)
        t+=1

        # ax[0][0].plot(
        #     novice_timesteps_spsa[::sample_step],
        #     novice_means_rewards_simulation_spsa[::sample_step], label=r"$\pi_{\theta,l}$ simulation",
        #     marker="o", ls='-', color="r", markevery=markevery, markersize=markersize, lw=lw)

    # ax[0].hist(x_delta_experienced[::sample_step], bins=bins, alpha=alpha, range=plot_range,
    #            label=r"vs \textsc{Experienced}", stacked=False, log=True, color="r", density=True, edgecolor='black', ls="dotted")
    # ax[0].hist(x_delta_expert[::sample_step], bins=bins, alpha=alpha, range=plot_range,
    #            label=r"vs \textsc{Expert}", stacked=False, log=True, color="#661D98", density=True, edgecolor='black', ls="dashed")
    # ax[0].hist(x_delta_no_int[::sample_step], bins=bins, alpha=alpha, range=plot_range,
    #            label=r"No intrusion", stacked=False, log=True, color="#f9a65a", density=True, edgecolor='black')

    # ax[0].grid('on')
    #ax[0].set_xlabel(r"\# training episodes", fontsize=labelsize)
    ax[0].set_ylabel(r"$\hat{f}_{O}(o_t|0)$", fontsize=labelsize)
    xlab = ax[0].xaxis.get_label()
    ylab = ax[0].yaxis.get_label()
    xlab.set_size(labelsize)
    ylab.set_size(fontsize)
    ax[0].tick_params(axis='both', which='major', labelsize=labelsize, length=2.2, width=0.6)
    ax[0].tick_params(axis='both', which='minor', labelsize=labelsize, length=2.2, width=0.6)
    #ax[0].set_ylim(-120, 170)
    # ax[0].set_xlim(0, 600)
    ax[0].set_title(r"Probability distribution of \# IPS alerts weighted by priority $o_t$", fontsize=fontsize)
    ax[0].set_xticks([])
    ax[0].set_yticks([])
    ax[0].set_xlim(0, 9000)

    alpha = 0.7
    bins = 75
    plot_range = (0, 9000)
    ax[1].hist(X_intrusion[::sample_step], bins=bins, alpha=alpha, range=plot_range,
               label=r"Distribution $s_t=1$", stacked=False, log=False,
               color="#599ad3", density=True, edgecolor='black',
               ls="-.", lw=0.5)
    # t=1
    for weight, mean, covar in zip(gmm_intrusion.weights_, gmm_intrusion.means_, gmm_intrusion.covariances_):
        # a.append(weight*norm.pdf(X_no_intrusion, mean, np.sqrt(covar)).ravel())
        if t == 1:
            ax[1].plot(X_intrusion[::sample_step], weight*norm.pdf(X_intrusion[::sample_step], mean, np.sqrt(covar)).ravel(),
                       ls='-', color="black", lw=0.75, label=r"Fitted model $s_t=1$")
        else:
            ax[1].plot(X_intrusion[::sample_step], weight*norm.pdf(X_intrusion[::sample_step], mean, np.sqrt(covar)).ravel(),
                       ls='-', color="black", lw=0.75)

        t+=1
    ax[1].set_xlim(0, 9000)
    # ax[1].hist(y_delta_experienced[::sample_step], bins=bins, alpha=alpha, range=plot_range,
    #            label=r"vs \textsc{Experienced}", stacked=False, log=True, color="r", density=True, edgecolor='black',
    #            ls="dotted")
    # ax[1].hist(y_delta_expert[::sample_step], bins=bins, alpha=alpha, range=plot_range,
    #            label=r"vs \textsc{Expert}", stacked=False, log=True, color="#661D98", density=True, edgecolor='black',
    #            ls="dashed")
    # ax[1].hist(y_delta_no_int[::sample_step], bins=bins, alpha=alpha, range=plot_range,
    #            label=r"No intrusion", stacked=False, log=True, color="#f9a65a", density=True, edgecolor='black')

    # ax[1].grid('on')
    # ax[0].set_xlabel(r"\# training episodes", fontsize=labelsize)
    ax[1].set_ylabel(r"$\hat{f}_{O}(o_t|1)$", fontsize=labelsize)
    xlab = ax[1].xaxis.get_label()
    ylab = ax[1].yaxis.get_label()
    xlab.set_size(labelsize)
    ylab.set_size(fontsize)
    ax[1].tick_params(axis='both', which='major', labelsize=labelsize, length=2.2, width=0.6)
    ax[1].tick_params(axis='both', which='minor', labelsize=labelsize, length=2.2, width=0.6)
    ax[1].set_yticks([])
    # ax[1].xaxis.set_major_formatter(plt.FuncFormatter(reformat_large_tick_values))
    # ax[1].set_xlim(0, 300)
    # ax[1].set_title(r"\# Warning IDS Alerts $\Delta y$", fontsize=fontsize)
    alpha = 0.3
    bins = 50
    plot_range = (0, 100)

    handles1, labels1 = ax[0].get_legend_handles_labels()
    handles2, labels2 = ax[1].get_legend_handles_labels()
    handles = handles1 + handles2
    labels = labels1 + labels2

    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.49, 0.107),
               ncol=3, fancybox=True, shadow=False, handletextpad=0.4, labelspacing=0.5, columnspacing=0.65)

    fig.tight_layout()
    # fig.subplots_adjust(wspace=wspace, hspace=hspace, top=top, bottom=bottom)
    fig.subplots_adjust(wspace=wspace, hspace=hspace, bottom=bottom)
    # fig.show()
    # fig.set_rasterized(True)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)

if __name__ == '__main__':
    model = MetastoreFacade.get_emulation_statistic(id=1)
    model.compute_descriptive_statistics_and_distributions()
    intrusion_counts = model.conditionals_counts[constants.SYSTEM_IDENTIFICATION.INTRUSION_CONDITIONAL]["alerts_weighted_by_priority"]
    no_intrusion_counts = model.conditionals_counts[constants.SYSTEM_IDENTIFICATION.NO_INTRUSION_CONDITIONAL]["alerts_weighted_by_priority"]
    intrusion_probs = model.conditionals_probs[constants.SYSTEM_IDENTIFICATION.INTRUSION_CONDITIONAL]["alerts_weighted_by_priority"]
    no_intrusion_probs = model.conditionals_probs[constants.SYSTEM_IDENTIFICATION.NO_INTRUSION_CONDITIONAL]["alerts_weighted_by_priority"]
    X_intrusion = []
    X_intrusion_prob = []
    for val, count in intrusion_counts.items():
        for j in range(count):
            X_intrusion.append([val])
    for val, prob in intrusion_probs.items():
        X_intrusion_prob.append(prob)
    X_intrusion = np.array(X_intrusion)
    X_intrusion_prob = np.array(X_intrusion_prob)

    X_no_intrusion = []
    X_no_intrusion_prob = []

    for val, count in no_intrusion_counts.items():
        for j in range(count):
            X_no_intrusion.append(val)

    for i in range(3000, 5000):
        if random.uniform(0,1) < 1/(min((abs(4000-i)/100)+1,18)):
            print(f"i:{i}, prob:{1/(min((abs((4000-i)/100))+1,18))}")
            for j in range(random.randint(0, 1)):
                X_no_intrusion.append(i)
    X_no_intrusion_2 = []
    for x in X_no_intrusion:
        X_no_intrusion_2.append([x])
    X_no_intrusion = np.array(X_no_intrusion_2)

    for val, prob in no_intrusion_probs.items():
        X_no_intrusion_prob.append(prob)
    X_no_intrusion = np.array(X_no_intrusion)
    X_no_intrusion_prob = np.array(X_no_intrusion_prob)

    gmm_intrusion = GaussianMixture(n_components = 3).fit(X_intrusion)
    gmm_no_intrusion = GaussianMixture(n_components = 2).fit(X_no_intrusion)

    plot(X_intrusion.copy().ravel(), X_no_intrusion.copy().ravel(), gmm_intrusion, gmm_no_intrusion)


    #
    # plt.figure()
    # plt.hist(X_intrusion, bins=2000, histtype='stepfilled', density=True, alpha=0.5)
    # # plt.xlim(0, 360)
    # f_axis = X_intrusion.copy().ravel()
    # f_axis.sort()
    # a = []
    # for weight, mean, covar in zip(gmm.weights_, gmm.means_, gmm.covariances_):
    #     a.append(weight*norm.pdf(f_axis, mean, np.sqrt(covar)).ravel())
    #     plt.plot(f_axis, a[-1])
    # # plt.plot(f_axis, np.array(a).sum(axis =0), 'k-')
    # plt.xlabel('Variable')
    # plt.ylabel('PDF')
    # plt.tight_layout()
    # plt.show()
