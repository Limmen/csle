from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_cluster.cluster_manager.cluster_controller import ClusterController
from csle_common.dao.emulation_config.emulation_metrics_time_series import EmulationMetricsTimeSeries
import matplotlib.pyplot as plt

def plot(time_series: EmulationMetricsTimeSeries):
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts,amsmath}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['axes.titlepad'] = 0.02
    plt.rcParams['ytick.major.pad'] = 0.05
    plt.rcParams['axes.labelpad'] = 0.8
    plt.rcParams['axes.linewidth'] = 0.8
    fontsize = 16.5
    labelsize = 15
    ncols = 2
    nrows = 2
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(16, 13))
    rates = list(map(lambda x: x.rate, time_series.client_metrics))
    num_clients = list(map(lambda x: x.num_clients, time_series.client_metrics))
    print(rates)
    print(num_clients)


if __name__ == '__main__':
    emulation_name = "csle-level4-020"
    execution_id = 15
    execution = MetastoreFacade.get_emulation_execution(emulation_name=emulation_name, ip_first_octet=execution_id)
    time_series = ClusterController.get_execution_time_series_data(ip='172.31.212.92', port=50041, minutes=60*24,
                                                                   emulation=emulation_name,
                                                                   ip_first_octet=execution_id)
    print("got time series")
    plot(time_series=time_series)