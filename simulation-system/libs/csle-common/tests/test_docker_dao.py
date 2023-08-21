from csle_common.dao.docker.docker_container_metadata import DockerContainerMetadata
from csle_common.dao.docker.docker_env_metadata import DockerEnvMetadata


class TestDockerDaoSuite:
    """
    Test suite for Docker data access objects (DAOs)
    """

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
