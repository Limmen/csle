from csle_common.dao.emulation_config.node_beats_config import NodeBeatsConfig
from csle_common.dao.emulation_config.beats_config import BeatsConfig
from csle_common.dao.emulation_config.client_managers_info import ClientManagersInfo
from csle_common.dao.emulation_config.container_network import ContainerNetwork
from csle_common.dao.emulation_config.cluster_node import ClusterNode
from csle_common.dao.emulation_config.cluster_config import ClusterConfig
from csle_collector.client_manager.client_manager_pb2 import ClientsDTO


class TestEmulationConfigDaoSuite:
    """
    Test suite for datasets data access objects (DAOs)
    """

    def test_node_beats_config(self) -> None:
        """
        Tests creation and dict conversion of the NodeBeatsConfig DAO

        :return: None
        """
        node_beats_config = NodeBeatsConfig(
            ip="192.168.5.1", log_files_paths=["log1"], filebeat_modules=["mod1"], metricbeat_modules=["mod2"],
            heartbeat_hosts_to_monitor=["192.168.5.7"], kafka_input=False, start_heartbeat_automatically=True,
            start_packetbeat_automatically=True, start_metricbeat_automatically=True, start_filebeat_automatically=True
        )
        assert isinstance(node_beats_config.to_dict(), dict)
        assert isinstance(NodeBeatsConfig.from_dict(node_beats_config.to_dict()), NodeBeatsConfig)
        assert NodeBeatsConfig.from_dict(node_beats_config.to_dict()).to_dict() == node_beats_config.to_dict()
        assert NodeBeatsConfig.from_dict(node_beats_config.to_dict()) == node_beats_config

    def test_beats_config(self) -> None:
        """
        Tests creation and dict conversion of the BeatsConfig DAO

        :return: None
        """
        node_beats_config = NodeBeatsConfig(
            ip="192.168.5.1", log_files_paths=["log1"], filebeat_modules=["mod1"], metricbeat_modules=["mod2"],
            heartbeat_hosts_to_monitor=["192.168.5.7"], kafka_input=False, start_heartbeat_automatically=True,
            start_packetbeat_automatically=True, start_metricbeat_automatically=True, start_filebeat_automatically=True
        )
        beats_config = BeatsConfig(
            node_beats_configs=[node_beats_config], num_elastic_shards=19, reload_enabled=False
        )
        assert isinstance(beats_config.to_dict(), dict)
        assert isinstance(BeatsConfig.from_dict(beats_config.to_dict()), BeatsConfig)
        assert BeatsConfig.from_dict(beats_config.to_dict()).to_dict() == beats_config.to_dict()
        assert BeatsConfig.from_dict(beats_config.to_dict()) == beats_config

    def test_client_managers_info(self) -> None:
        """
        Tests creation and dict conversion of the client_managers_info_dto

        :return: None
        """
        client_manager_status = ClientsDTO(
            num_clients=19, client_process_active=True, producer_active=False, clients_time_step_len_seconds=30,
            producer_time_step_len_seconds=30)
        client_managers_info = ClientManagersInfo(
            ips=["192.168.25.12"], ports=[2333], emulation_name="test_em", execution_id=19,
            client_managers_running=[True], client_managers_statuses=[client_manager_status])
        assert isinstance(client_managers_info.to_dict(), dict)
        assert isinstance(ClientManagersInfo.from_dict(client_managers_info.to_dict()), ClientManagersInfo)
        assert ClientManagersInfo.from_dict(client_managers_info.to_dict()).to_dict() == client_managers_info.to_dict()
        assert ClientManagersInfo.from_dict(client_managers_info.to_dict()) == client_managers_info

    def test_container_network(self) -> None:
        """
        Tests creation and dict conversion of the ContainerNetwork DTO

        :return: None
        """
        container_network = ContainerNetwork(
            name="testnet", subnet_mask="/24", bitmask="255.255.255.0", subnet_prefix="192.168.5", interface="eth1")
        assert isinstance(container_network.to_dict(), dict)
        assert isinstance(ContainerNetwork.from_dict(container_network.to_dict()), ContainerNetwork)
        assert ContainerNetwork.from_dict(container_network.to_dict()).to_dict() == container_network.to_dict()
        assert ContainerNetwork.from_dict(container_network.to_dict()) == container_network

    def test_cluster_node(self) -> None:
        """
        Tests creation and dict conversion of the ClusterNode DTO

        :return: None
        """
        cluster_node = ClusterNode(ip="192.168.5.1", leader=False, cpus=123, gpus=5, RAM=128)
        assert isinstance(cluster_node.to_dict(), dict)
        assert isinstance(ClusterNode.from_dict(cluster_node.to_dict()), ClusterNode)
        assert ClusterNode.from_dict(cluster_node.to_dict()).to_dict() == cluster_node.to_dict()
        assert ClusterNode.from_dict(cluster_node.to_dict()) == cluster_node

    def test_cluster_config(self) -> None:
        """
        Tests creation and dict conversion of the ClusterConfig DTO

        :return: None
        """
        cluster_node = ClusterNode(ip="192.168.5.1", leader=False, cpus=123, gpus=5, RAM=128)
        cluster_config = ClusterConfig(cluster_nodes=[cluster_node])
        assert isinstance(cluster_config.to_dict(), dict)
        assert isinstance(ClusterConfig.from_dict(cluster_config.to_dict()), ClusterConfig)
        assert ClusterConfig.from_dict(cluster_config.to_dict()).to_dict() == cluster_config.to_dict()
        assert ClusterConfig.from_dict(cluster_config.to_dict()) == cluster_config