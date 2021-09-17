import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.stats import geom

def plot_geo_only() -> None:
    """
    Plots the thresholds
    :return: None
    """
    times = np.arange(1, 101, 1)


    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts,amsmath}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['axes.titlepad'] = 0.02
    # plt.rcParams['xtick.major.pad'] = 0.5
    plt.rcParams['ytick.major.pad'] = 0.05
    plt.rcParams['axes.labelpad'] = 0.8
    plt.rcParams['axes.linewidth'] = 0.8
    fontsize=16.5
    labelsize=15
    # plt.rcParams.update({'font.size': 10})

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 3.7))

    # ylims = (0, 920)

    # Plot Avg Eval rewards Gensim
    colors = plt.cm.viridis(np.linspace(0.3, 1, 2))[-2:]

    p = 0.2
    x = geom.rvs(p, size=2000)
    # x = np.random.randn(200)
    colors = plt.cm.viridis(np.linspace(0.3, 1, 2))[-2:]
    kwargs = {'cumulative': True}

    n, bins, patches = ax.hist(x, cumulative=True, density=True, bins=20, alpha=0.5, color=colors[0], edgecolor='black')

    theoretical_y = []
    for i in bins:
        theoretical_y.append(geom.cdf(i, p))

    ax.plot(bins, theoretical_y, 'k--', label='Theoretical', linewidth=2.5)

    # set the grid on
    # ax.grid('on')

    ax.set_title(r"$I_t \sim Ge(p=0.2)$", fontsize=fontsize)
    ax.set_xlabel(r"intrusion start time $t$", fontsize=fontsize)
    ax.set_ylabel(r"$CDF_{I_t}(t)$", fontsize=fontsize)
    ax.set_xlim(1, 29)

    # tweak the axis labels
    xlab = ax.xaxis.get_label()
    ylab = ax.yaxis.get_label()

    xlab.set_size(fontsize)
    ylab.set_size(fontsize)

    # change the color of the top and right spines to opaque gray
    ax.spines['right'].set_color((.8, .8, .8))
    ax.spines['top'].set_color((.8, .8, .8))

    ax.tick_params(axis='both', which='major', labelsize=labelsize, length=2.2, width=0.6)
    ax.tick_params(axis='both', which='minor', labelsize=labelsize, length=2.2, width=0.6)

    # ttl = ax.title
    # ttl.set_position([.5, 1.05])

    fig.tight_layout()
    plt.subplots_adjust(wspace=0.22, hspace=0)
    # plt.show()
    # plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig("geo_only_2" + ".png", format="png", dpi=600)
    fig.savefig("geo_only_2" + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    # plt.close(fig)

if __name__ == '__main__':
    plot_geo_only()
