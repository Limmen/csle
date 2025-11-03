from typing import List
from csle_collector.snort_ids_manager.dao.snort_ids_ip_alert_counters import SnortIdsIPAlertCounters
from csle_common.metastore.metastore_facade import MetastoreFacade
import csle_common.constants.constants as constants
from csle_cluster.cluster_manager.cluster_controller import ClusterController

if __name__ == '__main__':
    emulation = "csle-level9-090"
    sleep_time_seconds = 45
    executions = MetastoreFacade.list_emulation_executions_for_a_given_emulation(emulation_name=emulation)
    if len(executions) == 0:
        raise ValueError(f"There is no execution of an emulation with name: {emulation}")

    execution = executions[0]
    emulation_env_config = execution.emulation_env_config

    time_series = ClusterController.get_execution_time_series_data(
        ip=execution.emulation_env_config.kafka_config.container.physical_host_ip,
        port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT, minutes=60,
        ip_first_octet=execution.ip_first_octet, emulation=execution.emulation_env_config.name)
    print(list(time_series.snort_ids_ip_metrics.keys()))
    snort_ids_ip_alert_counters: List[SnortIdsIPAlertCounters] = time_series.snort_ids_ip_metrics[
        "csle_ftp_1_1-level9-15"]
    print(snort_ids_ip_alert_counters)
    print(snort_ids_ip_alert_counters[0].priority_alerts)
