import numpy as np
import matplotlib.pyplot as plt
from csle_agents.agents.bayesian_optimization_emukit.bo import BOResults


def plot_bo_results_and_gp(bo_results: BOResults, file_name: str, fontsize: int = 18) -> None:
    """
    Plots the results of Bayesian optimization

    :param bo_results: a DTO with the results
    :param file_name: the file name to save the resulting plots
    :param fontsize: the font size
    :return: None
    """
    gp_mu_predictions, gp_var_predictions = bo_results.surrogate_model.predict(bo_results.X_objective)
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts,amsmath}')
    plt.rcParams['axes.linewidth'] = 0.8
    plt.rcParams.update({'font.size': fontsize})
    plt.rcParams['font.family'] = ['serif']
    fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(10, 9))
    ax[0].plot(bo_results.X, bo_results.Y, "ro", markersize=10, label="Observations")
    ax[0].plot(bo_results.X_objective[:, 0], bo_results.Y_objective[:, 0], label=r"$f(x)$", ls='-', color="black")
    ax[0].plot(bo_results.X_objective[:, 0], gp_mu_predictions[:, 0], "C0", label="Model")
    ax[0].fill_between(bo_results.X_objective[:, 0],
                       gp_mu_predictions[:, 0] + np.sqrt(gp_var_predictions)[:, 0],
                       gp_mu_predictions[:, 0] - np.sqrt(gp_var_predictions)[:, 0], color="C0", alpha=0.6)
    ax[0].fill_between(bo_results.X_objective[:, 0],
                       gp_mu_predictions[:, 0] + 2 * np.sqrt(gp_var_predictions)[:, 0],
                       gp_mu_predictions[:, 0] - 2 * np.sqrt(gp_var_predictions)[:, 0], color="C0", alpha=0.4)
    ax[0].fill_between(bo_results.X_objective[:, 0],
                       gp_mu_predictions[:, 0] + 3 * np.sqrt(gp_var_predictions)[:, 0],
                       gp_mu_predictions[:, 0] - 3 * np.sqrt(gp_var_predictions)[:, 0], color="C0", alpha=0.2)
    ax[0].spines['top'].set_visible(False)
    ax[0].spines['right'].set_visible(False)
    ax[0].set_xlabel(r"$x$")
    ax[0].legend(loc='upper center', bbox_to_anchor=(0.51, 1.4),
                 ncol=4, fancybox=True, shadow=False, handletextpad=0.4, labelspacing=0.5, columnspacing=0.65,
                 fontsize=fontsize)
    ax[1].plot(list(range(len(bo_results.X_best[:, 0]))), bo_results.Y_best[:, 0],
               label=r"$arg\min_{(x,y) \in \mathcal{D}} y$",
               ls='-', color="#599ad3", marker="s", markevery=1, markersize=7)
    ax[1].plot(list(range(len(bo_results.X_best[:, 0]))), [bo_results.y_opt] * len(bo_results.X_best[:, 0]),
               label=r"$y^{*}$", ls='dashed', color="black")
    ax[1].fill_between(list(range(len(bo_results.X_best[:, 0]))), bo_results.Y_best[:, 0],
                       [bo_results.y_opt] * len(bo_results.X_best[:, 0]), color="#599ad3", alpha=0.35,
                       label="regret")
    ax[1].set_xlabel(r"Stage $t$")
    ax[1].spines['top'].set_visible(False)
    ax[1].spines['right'].set_visible(False)
    ax[1].legend(loc='upper center', bbox_to_anchor=(0.51, 1.4),
                 ncol=4, fancybox=True, shadow=False, handletextpad=0.4, labelspacing=0.5, columnspacing=0.65,
                 fontsize=fontsize)

    ax[2].plot(list(range(len(bo_results.C[:, 0]))), bo_results.C[:, 0], label=r"$\sum_{t=1}^TCo(x)$",
               ls='-', color="#599ad3", marker="s", markevery=1, markersize=7)
    ax[2].plot(list(range(len(bo_results.C[:, 0]))), [bo_results.evaluation_budget] * len(bo_results.C[:, 0]),
               label=r"budget", ls='dashed', color="black")
    ax[2].set_xlabel(r"Stage $t$")
    ax[2].spines['top'].set_visible(False)
    ax[2].spines['right'].set_visible(False)
    ax[2].legend(loc='upper center', bbox_to_anchor=(0.51, 1.4),
                 ncol=4, fancybox=True, shadow=False, handletextpad=0.4, labelspacing=0.5, columnspacing=0.65,
                 fontsize=fontsize)
    fig.tight_layout()
    fig.subplots_adjust(wspace=0.0, hspace=0.75)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.show()
