import numpy as np
import matplotlib.pyplot as plt
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.util.plotting_util import PlottingUtil


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
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 6))
    ax.plot(list(range(len(returns_means))), returns_means, label=r"$\pi^{(i)}_D$ simulation",
            marker="o", ls='-', color="r", markevery=1, markersize=3, lw=0.75)
    ax.fill_between(list(range(len(returns_means))), returns_means - returns_stds,
                    returns_means + returns_stds, alpha=0.35, color="r", lw=0.75)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlabel(r"iteration $k$")
    ax.set_ylabel(r"Avg cumulative reward")
    ax.legend(loc='upper center', bbox_to_anchor=(0.51, -0.15),
              ncol=4, fancybox=True, shadow=False, handletextpad=0.4, labelspacing=0.5, columnspacing=0.65,
              fontsize=fontsize)
    ax.set_title("Local defender $\pi^{(i)}_D$ against random attacker")
    fig.tight_layout()
    fig.subplots_adjust(wspace=0.0, hspace=0.75)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.show()


if __name__ == '__main__':
    experiment = MetastoreFacade.get_experiment_execution(id=132)
    metric = "running_average_return"
    returns = []
    confidence = 0.95
    running_avg = 30
    # avg_rewards_data = np.array(avg_rewards_data_novice_ppo).reshape(max_len, num_seeds)
    seeds = list(experiment.result.all_metrics.keys())
    # seeds = [seeds[0]]
    print(seeds)
    for seed in seeds:
        returns.append(PlottingUtil.running_average(experiment.result.all_metrics[seed][metric], running_avg))
    returns = np.array(returns)
    returns = returns.reshape((returns.shape[1], len(seeds)))
    avg_returns_means = np.array(list(map(lambda x: PlottingUtil.mean_confidence_interval(
        data=x, confidence=confidence)[0], returns)))
    avg_returns_stds = np.array(list(map(lambda x: PlottingUtil.mean_confidence_interval(
        data=x, confidence=confidence)[1], returns)))
    print(returns.shape)
    print(avg_returns_stds)
    plot_returns(returns_means=avg_returns_means, returns_stds=avg_returns_stds, file_name="returns")
