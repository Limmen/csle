import time
from csle_common.dao.datasets.statistics_dataset import StatisticsDataset
from csle_common.dao.datasets.traces_dataset import TracesDataset
from csle_common.dao.docker.docker_container_metadata import DockerContainerMetadata
from csle_common.dao.docker.docker_env_metadata import DockerEnvMetadata
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_outcome import EmulationAttackerActionOutcome
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_type import EmulationAttackerActionType
from csle_common.dao.emulation_action.defender.emulation_defender_action_id import EmulationDefenderActionId
from csle_common.dao.emulation_action.defender.emulation_defender_action_outcome import EmulationDefenderActionOutcome
from csle_common.dao.emulation_action.defender.emulation_defender_action_type import EmulationDefenderActionType
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_config import EmulationAttackerActionConfig
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_action.defender.emulation_defender_action_config import EmulationDefenderActionConfig


class TestDaoSuite:
    """
    Test suite for data access objects (DAOs)
    """

    def test_traces_dataset(self) -> None:
        """
        Tests creation and dict conversion of the TracesDataset DAO

        :return: None
        """
        dataset = TracesDataset(name="test_dataset", description="test_descr", download_count=100,
                                file_path="test_path", url="test_url", date_added=time.time(),
                                size_in_gb=5, compressed_size_in_gb=17, citation="test_citation",
                                num_files=50, file_format="json", added_by="testadded", columns="col1,col2",
                                data_schema={}, num_attributes_per_time_step=10, num_traces=15)
        assert isinstance(dataset.to_dict(), dict)
        assert isinstance(TracesDataset.from_dict(dataset.to_dict()), TracesDataset)
        assert TracesDataset.from_dict(dataset.to_dict()).to_dict() == dataset.to_dict()
        assert TracesDataset.from_dict(dataset.to_dict()) == dataset

    def test_statistics_dataset(self) -> None:
        """
        Tests creation and dict conversion of the StatisticsDataset DAO

        :return: None
        """
        dataset = StatisticsDataset(name="test_dataset", description="test_descr", download_count=100,
                                    file_path="test_path", url="test_url", date_added=time.time(), num_measurements=100,
                                    num_metrics=10, size_in_gb=5, compressed_size_in_gb=17, citation="test_citation",
                                    num_files=50, file_format="json", added_by="testadded", conditions="cond1,cond2",
                                    metrics="metric1,metric2", num_conditions=10)
        assert isinstance(dataset.to_dict(), dict)
        assert isinstance(StatisticsDataset.from_dict(dataset.to_dict()), StatisticsDataset)
        assert StatisticsDataset.from_dict(dataset.to_dict()).to_dict() == dataset.to_dict()
        assert StatisticsDataset.from_dict(dataset.to_dict()) == dataset

    def test_docker_container_metadata(self) -> None:
        """
        Tests creation and dict conversion of the DockerContainerMetadata DAO

        :return: None
        """
        container_metadata = DockerContainerMetadata(
            name="cont1", status="test", short_id="shortid", image_short_id="imgshort", image_tags=[], id="testid",
            created="1 Aug", ip="testIp", network_id=5, gateway="gw", mac="mymac", ip_prefix_len=16,
            name2="secondname", level="level1", hostname="host1", image_name="img1", net="mynet", dir="mydir",
            config_path="mycfg", container_handle=None, kafka_container="kafkacont", emulation="myem")
        assert isinstance(container_metadata.to_dict(), dict)
        assert isinstance(DockerContainerMetadata.from_dict(container_metadata.to_dict()), DockerContainerMetadata)
        assert DockerContainerMetadata.from_dict(container_metadata.to_dict()).to_dict() == container_metadata.to_dict()
        assert DockerContainerMetadata.from_dict(container_metadata.to_dict()) == container_metadata

    def test_docker_env_metadata(self) -> None:
        """
        Tests creation and dict conversion of the DockerEnvMetadata DAO

        :return: None
        """
        container = DockerContainerMetadata(
            name="cont1", status="test", short_id="shortid", image_short_id="imgshort", image_tags=[], id="testid",
            created="1 Aug", ip="testIp", network_id=5, gateway="gw", mac="mymac", ip_prefix_len=16,
            name2="secondname", level="level1", hostname="host1", image_name="img1", net="mynet", dir="mydir",
            config_path="mycfg", container_handle=None, kafka_container="kafkacont", emulation="myem")
        docker_env_metadata = DockerEnvMetadata(
            containers=[container], name="myenv", subnet_prefix="myprefix", subnet_mask="mymask", level="mylevel",
            config=None, kafka_config=None)
        assert isinstance(docker_env_metadata.to_dict(), dict)
        assert isinstance(DockerEnvMetadata.from_dict(docker_env_metadata.to_dict()), DockerEnvMetadata)
        assert DockerEnvMetadata.from_dict(docker_env_metadata.to_dict()).to_dict() == docker_env_metadata.to_dict()
        assert DockerEnvMetadata.from_dict(docker_env_metadata.to_dict()) == docker_env_metadata

    def test_emulation_attacker_action(self) -> None:
        """
        Tests creation and dict conversion of the EmulationAttackerAction DAO

        :return: None
        """
        emulation_attacker_action = EmulationAttackerAction(
            id=EmulationAttackerActionId.CONTINUE, name="test", cmds=["cmd1"],
            type=EmulationAttackerActionType.CONTINUE, descr="testtest", ips=["ip1"], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, vulnerability="test", alt_cmds=["altcmd1"],
            backdoor=False, execution_time=0.0, ts=0.0
        )
        assert isinstance(emulation_attacker_action.to_dict(), dict)
        assert isinstance(EmulationAttackerAction.from_dict(emulation_attacker_action.to_dict()),
                          EmulationAttackerAction)
        assert EmulationAttackerAction.from_dict(emulation_attacker_action.to_dict()).to_dict() == \
               emulation_attacker_action.to_dict()
        assert EmulationAttackerAction.from_dict(emulation_attacker_action.to_dict()) == emulation_attacker_action

    def test_emulation_attacker_action_config(self) -> None:
        """
        Tests creation and dict conversion of the EmulationAttackerActionConfig DAO

        :return: None
        """
        emulation_attacker_action = EmulationAttackerAction(
            id=EmulationAttackerActionId.CONTINUE, name="test", cmds=["cmd1"],
            type=EmulationAttackerActionType.CONTINUE, descr="testtest", ips=["ip1"], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, vulnerability="test", alt_cmds=["altcmd1"],
            backdoor=False, execution_time=0.0, ts=0.0
        )
        emulation_attacker_action_config = EmulationAttackerActionConfig(
            num_indices=10, actions=[emulation_attacker_action],
            nmap_action_ids=[EmulationAttackerActionId.NMAP_VULNERS_ALL],
            network_service_action_ids=[EmulationAttackerActionId.TCP_SYN_STEALTH_SCAN_HOST],
            shell_action_ids=[EmulationAttackerActionId.CVE_2015_1427_EXPLOIT],
            nikto_action_ids=[EmulationAttackerActionId.NIKTO_WEB_HOST_SCAN],
            masscan_action_ids=[EmulationAttackerActionId.MASSCAN_ALL_SCAN],
            stopping_action_ids=[EmulationAttackerActionId.STOP, EmulationAttackerActionId.CONTINUE])
        assert isinstance(emulation_attacker_action_config.to_dict(), dict)
        assert isinstance(EmulationAttackerActionConfig.from_dict(emulation_attacker_action_config.to_dict()),
                          EmulationAttackerActionConfig)
        assert EmulationAttackerActionConfig.from_dict(emulation_attacker_action_config.to_dict()).to_dict() == \
               emulation_attacker_action_config.to_dict()
        assert EmulationAttackerActionConfig.from_dict(emulation_attacker_action_config.to_dict()) == \
               emulation_attacker_action_config

    def test_emulation_defender_action(self) -> None:
        """
        Tests creation and dict conversion of the EmulationDefenderAction DAO

        :return: None
        """
        emulation_defender_action = EmulationDefenderAction(
            id=EmulationDefenderActionId.STOP, name="testname", cmds=["cmd1"],
            type=EmulationDefenderActionType.CONTINUE, ips=["ip1", "ip2"], index=0,
            action_outcome=EmulationDefenderActionOutcome.CONTINUE, alt_cmds=["alt1"], execution_time=0.0,
            ts=0.0, descr="testdescr")
        assert isinstance(emulation_defender_action.to_dict(), dict)
        assert isinstance(EmulationDefenderAction.from_dict(emulation_defender_action.to_dict()),
                          EmulationDefenderAction)
        assert EmulationDefenderAction.from_dict(emulation_defender_action.to_dict()).to_dict() == \
               emulation_defender_action.to_dict()
        assert EmulationDefenderAction.from_dict(emulation_defender_action.to_dict()) == emulation_defender_action

    def test_emulation_defender_action_config(self) -> None:
        """
        Tests creation and dict conversion of the EmulationDefenderActionConfig DAO

        :return: None
        """
        emulation_defender_action = EmulationDefenderAction(
            id=EmulationDefenderActionId.STOP, name="testname", cmds=["cmd1"],
            type=EmulationDefenderActionType.CONTINUE, ips=["ip1", "ip2"], index=0,
            action_outcome=EmulationDefenderActionOutcome.CONTINUE, alt_cmds=["alt1"], execution_time=0.0,
            ts=0.0, descr="testdescr")
        emulation_defender_action_config = EmulationDefenderActionConfig(
            num_indices=10, actions=[emulation_defender_action],
            stopping_action_ids=[EmulationDefenderActionId.STOP, EmulationDefenderActionId.CONTINUE],
            multiple_stop_actions=[],
            multiple_stop_actions_ids=[EmulationDefenderActionId.STOP, EmulationDefenderActionId.CONTINUE])
        assert isinstance(emulation_defender_action_config.to_dict(), dict)
        assert isinstance(EmulationDefenderActionConfig.from_dict(emulation_defender_action_config.to_dict()),
                          EmulationDefenderActionConfig)
        assert EmulationDefenderActionConfig.from_dict(emulation_defender_action_config.to_dict()).to_dict() == \
               emulation_defender_action_config.to_dict()
        assert EmulationDefenderActionConfig.from_dict(emulation_defender_action_config.to_dict()) == \
               emulation_defender_action_config
