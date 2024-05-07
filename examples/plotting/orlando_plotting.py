import matplotlib.pyplot as plt
import numpy as np
from csle_common.metastore.metastore_facade import MetastoreFacade


def plot_returns(returns_means, returns_stds, file_name: str, fontsize: int = 18) -> None:
    """
    Plots the returns

    :param returns_means: the average returns
    :param returns_stds: the average standard deviations
    :param file_name: the file name to save the resulting plots
    :param fontsize: the font size
    :return: None
    """
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts,amsmath}')
    plt.rcParams['axes.linewidth'] = 0.8
    plt.rcParams.update({'font.size': fontsize})
    plt.rcParams['font.family'] = ['serif']
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(11, 4))

    ax.plot(np.array(list(range(len(returns_means)))) * 200, returns_means, label=r"$\pi^{(i)}_D$ simulation",
            marker="o", ls='-', color="black", markevery=1, markersize=3, lw=0.75)
    ax.fill_between(np.array(list(range(len(returns_means)))) * 200, returns_means - returns_stds,
                    returns_means + returns_stds, alpha=0.35, color="black", lw=0.75)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlabel(r"iteration $k$")
    ax.set_ylabel(r"Avg cumulative reward")
    ax.set_title(r"\textsc{dqn-base}-1")
    fig.tight_layout()
    fig.subplots_adjust(wspace=0.0, hspace=0.75)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.show()


if __name__ == '__main__':
    dqn_results = [-2009, -2602, -2881, -1077, -1143, -1225, -1369, -1460, -1468, -1459, -1405, -1854, -6124, -6012,
                   -5604, -5844, -2591, -6072, -5849, -5910, -6297, -5940, -5832, -5815, -5871, -5744, -6074, -5326,
                   -6198, -5997, -5675, -5944, -5836, -6247, -5773, -5510, -5938, -1432, -6000, -5974, -6132, -5849,
                   -6104, -5926, -5611, -5637, -5774, -6577, -6267, -6146, -5769, -6129, -6001, -5720, -5714, -6088,
                   -6261, -6177, -5862, -1807, -5848]
    job_id = 86
    job = MetastoreFacade.get_training_job_config(id=job_id)
    experiment_result = job.experiment_result
    seeds = list(experiment_result.all_metrics.keys())
    seed = seeds[0]
    metrics = experiment_result.all_metrics[seed]
    returns = metrics["average_return"]
    folder = "/home/kim/orlando_results/12_jan/"
    result_file_name = "ppo_base_1.json"
    plot_file_name = "dqn_base_1"
    experiment_result.to_json_file(f"{folder}/{result_file_name}")
    plot_returns(returns_means=np.array(dqn_results), returns_stds=np.array([0] * len(dqn_results)),
                 file_name=f"{folder}{plot_file_name}")
