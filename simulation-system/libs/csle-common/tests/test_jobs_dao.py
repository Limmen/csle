from csle_common.dao.jobs.data_collection_job_config import DataCollectionJobConfig
from csle_common.dao.emulation_config.emulation_trace import EmulationTrace
from csle_common.dao.emulation_observation.attacker.\
    emulation_attacker_observation_state import EmulationAttackerObservationState
from csle_common.dao.emulation_config.kafka_config import KafkaConfig
from csle_common.dao.emulation_config.node_container_config import NodeContainerConfig
from csle_common.dao.emulation_config.node_resources_config import NodeResourcesConfig
from csle_common.dao.emulation_config.node_firewall_config import NodeFirewallConfig
from csle_common.dao.emulation_config.kafka_topic import KafkaTopic
from csle_common.dao.emulation_config.container_network import ContainerNetwork
from csle_common.dao.emulation_config.node_network_config import NodeNetworkConfig
from csle_common.dao.emulation_config.default_network_firewall_config import DefaultNetworkFirewallConfig
from csle_collector.host_manager.dao.host_metrics import HostMetrics
from csle_collector.docker_stats_manager.dao.docker_stats import DockerStats
from csle_collector.ossec_ids_manager.dao.ossec_ids_alert_counters import OSSECIdsAlertCounters
from csle_common.dao.emulation_observation.defender.emulation_defender_observation_state import \
    EmulationDefenderObservationState
from csle_collector.client_manager.client_population_metrics import ClientPopulationMetrics
from csle_collector.snort_ids_manager.dao.snort_ids_alert_counters import SnortIdsAlertCounters
from csle_collector.snort_ids_manager.dao.snort_ids_rule_counters import SnortIdsRuleCounters
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.defender.emulation_defender_action_id import EmulationDefenderActionId
from csle_common.dao.emulation_action.defender.emulation_defender_action_type import EmulationDefenderActionType
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_type import EmulationAttackerActionType
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.jobs.system_identification_job_config import SystemIdentificationJobConfig
from csle_common.dao.system_identification.system_identification_config import SystemIdentificationConfig
from csle_common.dao.system_identification.system_model_type import SystemModelType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.jobs.training_job_config import TrainingJobConfig
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.experiment_result import ExperimentResult
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.player_type import PlayerType


class TestJobsDaoSuite:
    """
    Test suite for job data access objects (DAOs)
    """

    def test_data_collection_job_config(self) -> None:
        """
        Tests creation and dict conversion of the DataCollectionJobConfig DAO

        :return: None
        """

        ips = ["10.10.10.10", "20.20.20.20"]

        container_network = ContainerNetwork(name="test1", subnet_mask="0.0.0.0",
                                             bitmask="0.0.0.0", subnet_prefix="0.0.0.0")
        ips_and_networks = [("container_network_test", container_network)]
        container = NodeContainerConfig("test1", ips_and_networks=ips_and_networks, version="1.0", level="1",
                                        restart_policy="test1", suffix="test2", os="ubuntu")
        ips_and_network_configs = [("test2", NodeNetworkConfig())]
        resources = NodeResourcesConfig(container_name="test1", num_cpus=1,
                                        available_memory_gb=100, ips_and_network_configs=ips_and_network_configs)

        default_network_firewall_config = DefaultNetworkFirewallConfig(ip="1.1.1.1",
                                                                       default_gw="2.3.3.4",
                                                                       default_input="test",
                                                                       default_output="tets",
                                                                       default_forward="test",
                                                                       network=container_network)
        ips_gw_default_policy_networks = [default_network_firewall_config]
        firewall_config = NodeFirewallConfig(ips_gw_default_policy_networks=ips_gw_default_policy_networks,
                                             hostname="test1", output_accept={"test1", "test2"},
                                             forward_accept={"test1", "test2"}, output_drop={"test"},
                                             input_drop={"test2"}, forward_drop={"test3"},
                                             input_accept={"test"},
                                             routes={("test", "test")})
        topics = [
            KafkaTopic(name="test", num_partitions=1, num_replicas=2, attributes=["test"], retention_time_hours=1)]

        kafka_config = KafkaConfig(container=container, resources=resources, firewall_config=firewall_config,
                                   topics=topics, kafka_manager_log_file="test", kafka_manager_log_dir="test",
                                   kafka_manager_max_workers=10)
        emulation_defender_action = EmulationDefenderAction(id=EmulationDefenderActionId.CONTINUE, name="test",
                                                            cmds=["test", "test2"],
                                                            type=EmulationDefenderActionType.CONTINUE,
                                                            descr="test", ips=ips, index=1)
        emulation_attacker_action = EmulationAttackerAction(id=EmulationAttackerActionId.NETWORK_SERVICE_LOGIN,
                                                            name="test",
                                                            cmds=["test", "test2"],
                                                            type=EmulationAttackerActionType.PRIVILEGE_ESCALATION,
                                                            descr="test", ips=ips, index=1)

        emulation_defender_observation_state = (EmulationDefenderObservationState(
            kafka_config=kafka_config, client_population_metrics=ClientPopulationMetrics(), docker_stats=DockerStats(),
            snort_ids_alert_counters=SnortIdsAlertCounters(), ossec_ids_alert_counters=OSSECIdsAlertCounters(),
            aggregated_host_metrics=HostMetrics(), defender_actions=[emulation_defender_action],
            attacker_actions=[emulation_attacker_action],
            snort_ids_rule_counters=SnortIdsRuleCounters()
        ))
        emulation_trace = EmulationTrace(initial_attacker_observation_state=EmulationAttackerObservationState(
            catched_flags=1, agent_reachable={"yes"}),
            initial_defender_observation_state=emulation_defender_observation_state,
            emulation_name="test")
        emulation_defender_action = EmulationDefenderAction(id=EmulationDefenderActionId.CONTINUE, name="test",
                                                            cmds=["test", "test2"],
                                                            type=EmulationDefenderActionType.CONTINUE,
                                                            descr="test", ips=ips, index=1)
        data_collection_jobs_config = DataCollectionJobConfig(emulation_env_name="test", num_collected_steps=1,
                                                              progress_percentage=0.1,
                                                              attacker_sequence=[emulation_attacker_action],
                                                              pid=123, repeat_times=5, emulation_statistic_id=10,
                                                              num_sequences_completed=10, traces=[emulation_trace],
                                                              save_emulation_traces_every=1, num_cached_traces=10,
                                                              defender_sequence=[emulation_defender_action],
                                                              log_file_path="test/test", physical_host_ip="1.1.1.1")

        assert isinstance(data_collection_jobs_config.to_dict(), dict)
        assert isinstance(DataCollectionJobConfig.from_dict(data_collection_jobs_config.to_dict()),
                          DataCollectionJobConfig)
        assert (DataCollectionJobConfig.from_dict(data_collection_jobs_config.to_dict()).to_dict() ==
                data_collection_jobs_config.to_dict())
        assert (DataCollectionJobConfig.from_dict(data_collection_jobs_config.to_dict()) ==
                data_collection_jobs_config)

    def test_system_identification_job_config(self) -> None:
        """
        Tests creation and dict conversion of the SystemIdentificationJobConfig DAO

        :return: None
        """

        hparams = dict()
        hparams["test"] = HParam(value=1, name="test", descr="test")

        system_identification_config = SystemIdentificationConfig(
            model_type=SystemModelType.GAUSSIAN_MIXTURE, hparams=hparams,
            output_dir="test/test", title="test", log_every=10)

        system_identification_job_config = SystemIdentificationJobConfig(
            emulation_env_name="test",
            emulation_statistics_id=1, pid=123,
            log_file_path="test/test",
            system_identification_config=system_identification_config, physical_host_ip="1.1.1.1",
            progress_percentage=0.5)

        assert isinstance(system_identification_job_config.to_dict(), dict)
        assert isinstance(SystemIdentificationJobConfig.from_dict(system_identification_job_config.to_dict()),
                          SystemIdentificationJobConfig)
        assert (SystemIdentificationJobConfig.from_dict(system_identification_job_config.to_dict()).to_dict() ==
                system_identification_job_config.to_dict())
        assert (SystemIdentificationJobConfig.from_dict(system_identification_job_config.to_dict()) ==
                system_identification_job_config)

    def test_training_job_config(self) -> None:
        """
        Tests creation and dict conversion of the TrainingJobConfig DAO

        :return: None
        """

        hparams = dict()
        hparams["test"] = HParam(value=1, name="test", descr="test")
        experiment_config = ExperimentConfig(output_dir="test/test", title="test1", random_seeds=[1],
                                             agent_type=AgentType.PPO, hparams=hparams, log_every=10,
                                             player_type=PlayerType.DEFENDER, player_idx=2)

        training_job_config = TrainingJobConfig(simulation_env_name="test", progress_percentage=0.5,
                                                pid=1, emulation_env_name="test", num_cached_traces=1,
                                                log_file_path="test/test", descr="test", physical_host_ip="1.1.1.1",
                                                experiment_config=experiment_config,
                                                experiment_result=ExperimentResult(),
                                                simulation_traces=[SimulationTrace(simulation_env="test1")])

        assert isinstance(training_job_config.to_dict(), dict)
        assert isinstance(TrainingJobConfig.from_dict(training_job_config.to_dict()),
                          TrainingJobConfig)
        assert (TrainingJobConfig.from_dict(training_job_config.to_dict()).to_dict() ==
                training_job_config.to_dict())
        assert (TrainingJobConfig.from_dict(training_job_config.to_dict()) ==
                training_job_config)
