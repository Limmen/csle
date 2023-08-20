import time
from csle_common.dao.datasets.statistics_dataset import StatisticsDataset
from csle_common.dao.datasets.traces_dataset import TracesDataset
from csle_common.dao.docker.docker_container_metadata import DockerContainerMetadata
from csle_common.dao.docker.docker_env_metadata import DockerEnvMetadata


class TestDaoSuite:
    """
    Test suite for data access objects
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
            name = "cont1", status="test", short_id="shortid", image_short_id="imgshort", image_tags=[], id="testid",
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
            name = "cont1", status="test", short_id="shortid", image_short_id="imgshort", image_tags=[], id="testid",
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
