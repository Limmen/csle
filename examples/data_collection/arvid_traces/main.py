from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_cluster.cluster_manager.cluster_controller import ClusterController

if __name__ == '__main__':
    emulation = MetastoreFacade.get_emulation(name='csle-level4-010')
    execution = MetastoreFacade.get_execution(name='csle-level4-010', ip_first_octet=15)
    time_series = ClusterController.get_time_series(emulation=emulation, ip_first_octet=15, ip='172.31.212.93', port=50041, minutes=30)
    time_series.to_json_file('time_series.json')