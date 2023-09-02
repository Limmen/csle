from csle_common.dao.jobs.data_collection_job_config import DataCollectionJobConfig
from csle_common.dao.emulation_config.emulation_trace import EmulationTrace
from csle_common.dao.emulation_observation.attacker. \
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

    def test_data_collection_job_config(self, example_data_collection_job: DataCollectionJobConfig) -> None:
        """
        Tests creation and dict conversion of the DataCollectionJobConfig DAO

        :param example_data_collection_job: an example DataCollectionJobConfig
        :return: None
        """
        assert isinstance(example_data_collection_job.to_dict(), dict)
        assert isinstance(DataCollectionJobConfig.from_dict(example_data_collection_job.to_dict()),
                          DataCollectionJobConfig)
        assert (DataCollectionJobConfig.from_dict(example_data_collection_job.to_dict()).to_dict() ==
                example_data_collection_job.to_dict())
        assert (DataCollectionJobConfig.from_dict(example_data_collection_job.to_dict()) ==
                example_data_collection_job)

    def test_system_identification_job_config(
            self, example_system_identification_job_config: SystemIdentificationJobConfig) -> None:
        """
        Tests creation and dict conversion of the SystemIdentificationJobConfig DAO

        :param example_system_identification_job_config: an example SystemIdentificationJobConfig
        :return: None
        """
        assert isinstance(example_system_identification_job_config.to_dict(), dict)
        assert isinstance(SystemIdentificationJobConfig.from_dict(example_system_identification_job_config.to_dict()),
                          SystemIdentificationJobConfig)
        assert (SystemIdentificationJobConfig.from_dict(example_system_identification_job_config.to_dict()).to_dict() ==
                example_system_identification_job_config.to_dict())
        assert (SystemIdentificationJobConfig.from_dict(example_system_identification_job_config.to_dict()) ==
                example_system_identification_job_config)

    def test_training_job_config(self, example_training_job_config: TrainingJobConfig) -> None:
        """
        Tests creation and dict conversion of the TrainingJobConfig DAO

        :param example_training_job_config: an example TrainingJobConfig
        :return: None
        """
        assert isinstance(example_training_job_config.to_dict(), dict)
        assert isinstance(TrainingJobConfig.from_dict(example_training_job_config.to_dict()),
                          TrainingJobConfig)
        assert (TrainingJobConfig.from_dict(example_training_job_config.to_dict()).to_dict() ==
                example_training_job_config.to_dict())
        assert (TrainingJobConfig.from_dict(example_training_job_config.to_dict()) ==
                example_training_job_config)
