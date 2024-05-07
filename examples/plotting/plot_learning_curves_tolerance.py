import matplotlib.pyplot as plt
import numpy as np
from csle_common.metastore.metastore_facade import MetastoreFacade

if __name__ == '__main__':
    fontsize: int = 14
    lw: float = 0.75
    alpha: float = 0.35
    file_name = "tolerance_curves"
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts,amsmath}')
    plt.rcParams['axes.linewidth'] = 0.8
    plt.rcParams.update({'font.size': fontsize})
    plt.rcParams['font.family'] = ['serif']
    fig, ax = plt.subplots(nrows=3, ncols=8, figsize=(18, 7.5))
    btrs = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
    cross_entropy_ids = [9, 10, 11, 12, 13, 14, 15, 16, 28, 39, 40, 41, 42, 43, 44, 45, 46, 47, 29, 48, 49, 32, 50]
    for i, id in enumerate(cross_entropy_ids):
        col = 0
        print(f"Parsing id: {id}, btr: {btrs[i]}")
        exp_exec = MetastoreFacade.get_experiment_execution(id=id)
        BTR = exp_exec.config.hparams["L"].value
        avg_costs = np.array(exp_exec.result.avg_metrics["running_average_return"]) / (BTR - 1)
        costs_stds = np.array(exp_exec.result.std_metrics["running_average_return"])
        optimal_costs = np.array(exp_exec.result.avg_metrics["average_upper_bound_return"]) / (BTR - 1)
        runtimes = np.array(exp_exec.result.avg_metrics["runtime"])
        optimal_costs = min(np.mean(optimal_costs), np.min(avg_costs))
        optimal_costs = [optimal_costs] * len(runtimes)
        if BTR <= 10:
            row = 0
        if BTR > 10 and BTR <= 18:
            row = 1
        else:
            row = 2
        ax[row][col].plot(runtimes, optimal_costs, label=r"lower bound", ls='dashed', color="black", lw=lw)
        ax[row][col].plot(runtimes, avg_costs, label=r"\textsc{cem}", ls='-', color="r", lw=lw)
        ax[row][col].fill_between(runtimes, np.maximum(np.array(optimal_costs), avg_costs - costs_stds),
                                  avg_costs + costs_stds, alpha=alpha, color="r", lw=lw)
        ax[row][col].spines['top'].set_visible(False)
        ax[row][col].spines['right'].set_visible(False)
        if BTR == 3:
            ax[0][col].set_ylabel(r"Average cost $J_i$", fontsize=fontsize)
        ax[row][col].set_title(r"$\Delta_{\mathrm{R}}=" + str(BTR) + "$", fontsize=fontsize)
        ax[row][col].tick_params(axis='both', which='major', labelsize=fontsize)
        ax[row][col].tick_params(axis='both', which='minor', labelsize=fontsize)
        if row == 2:
            ax[row][col].set_xlabel(r"Time (min)", fontsize=fontsize)
        col += 1
        if col >= 8:
            col = 0
    fig.tight_layout()
    fig.subplots_adjust(wspace=0.55, hspace=0.4, bottom=0.14)
    handles, labels = ax[0][0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.52, -0.02),
               ncol=8, fancybox=False, shadow=False, handletextpad=0.4, labelspacing=0.5, columnspacing=0.65,
               prop={'size': fontsize}, frameon=False)
    plt.show()
