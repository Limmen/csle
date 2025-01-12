from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_cluster.cluster_manager.cluster_controller import ClusterController
from csle_common.dao.emulation_config.emulation_metrics_time_series import EmulationMetricsTimeSeries
import numpy as np
import matplotlib.pyplot as plt


def plot(time_series: EmulationMetricsTimeSeries, time_step_len_seconds: int = 30) -> None:
    """
    Plots time series with infrastructure metrics

    :param time_series: the time series to plot
    :param time_step_len_seconds: the time-step length of the series
    :return: None
    """
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts,amsmath}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['axes.titlepad'] = 0.02
    plt.rcParams['ytick.major.pad'] = 0.05
    plt.rcParams['axes.labelpad'] = 0.8
    plt.rcParams['axes.linewidth'] = 0.8
    ncols = 1
    nrows = 6
    colors = plt.cm.viridis(np.linspace(0.3, 1, 2))[-2:]
    file_name = "time_series_plot"
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(8, 8))
    rates = list(map(lambda x: x.rate, time_series.client_metrics))[100:1100]
    time = list(map(lambda x: (x * time_step_len_seconds / 60) / 60, range(len(rates))))
    num_clients = list(map(lambda x: x.num_clients, time_series.client_metrics))[100:1100]
    ids_alerts = list(map(lambda x: x.alerts_weighted_by_priority, time_series.agg_snort_ids_metrics))
    logins = list(map(lambda x: x.num_failed_login_attempts, time_series.aggregated_host_metrics))
    connections = list(map(lambda x: x.num_open_connections, time_series.aggregated_host_metrics))
    processes = list(map(lambda x: x.pids, time_series.aggregated_docker_stats))

    ax[0].plot(time, rates, ls='-', color=colors[0], lw=0.75)
    ax[0].spines['top'].set_visible(False)
    ax[0].spines['right'].set_visible(False)
    ax[0].set_ylabel(r"Arrival rate")
    ax[0].set_title(r"Arrival rate $\lambda(t)$")
    ax[0].set_xlim(min(time), max(time))
    ax[0].set_xticks([])

    ax[1].plot(time, num_clients, ls='-', color=colors[0], lw=0.75)
    ax[1].spines['top'].set_visible(False)
    ax[1].spines['right'].set_visible(False)
    ax[1].set_ylabel(r"\# Clients ($N$)")
    ax[1].set_title(r"\# Clients ($N$)")
    ax[1].set_xlim(min(time), max(time))
    ax[1].set_xticks([])

    ax[2].plot(time, ids_alerts[len(ids_alerts) - len(time):], ls='-', color=colors[0], lw=0.75)
    ax[2].spines['top'].set_visible(False)
    ax[2].spines['right'].set_visible(False)
    ax[2].set_ylabel(r"\# IDS alerts")
    ax[2].set_title(r"\# IDS alerts")
    ax[2].set_xlim(min(time), max(time))
    ax[2].set_xticks([])

    ax[3].plot(time, logins[len(logins) - len(time):], ls='-', color=colors[0], lw=0.75)
    ax[3].spines['top'].set_visible(False)
    ax[3].spines['right'].set_visible(False)
    ax[3].set_ylabel(r"\# Login events")
    ax[3].set_title(r"\# Login events")
    ax[3].set_xlim(min(time), max(time))
    ax[3].set_xticks([])

    ax[4].plot(time, connections[len(connections) - len(time):], ls='-', color=colors[0], lw=0.75)
    ax[4].spines['top'].set_visible(False)
    ax[4].spines['right'].set_visible(False)
    ax[4].set_ylabel(r"\# TCP connections")
    ax[4].set_title(r"\# TCP connections")
    ax[4].set_xlim(min(time), max(time))
    ax[4].set_xticks([])

    ax[5].plot(time, processes[len(processes) - len(time):], ls='-', color=colors[0], lw=0.75)
    ax[5].spines['top'].set_visible(False)
    ax[5].spines['right'].set_visible(False)
    ax[5].set_ylabel(r"\# Processes")
    ax[5].set_title(r"\# Processes")
    ax[5].set_xlim(min(time), max(time))
    ax[5].set_xlabel(r"$t$ (hours)")

    fig.tight_layout()

    fig.subplots_adjust(wspace=0.0, hspace=0.2)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.show()


if __name__ == '__main__':
    emulation_name = "csle-level4-070"
    execution_id = 15
    execution = MetastoreFacade.get_emulation_execution(emulation_name=emulation_name, ip_first_octet=execution_id)
    time_series = ClusterController.get_execution_time_series_data(ip='172.31.212.92', port=50041, minutes=60 * 24,
                                                                   emulation=emulation_name,
                                                                   ip_first_octet=execution_id)
    time_series.to_json_file("/home/kim/arvid_time_series_plot_2.json")
    plot(time_series=time_series)
