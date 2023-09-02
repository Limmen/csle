from csle_common.dao.docker.docker_container_metadata import DockerContainerMetadata
from csle_common.dao.docker.docker_env_metadata import DockerEnvMetadata


class TestDockerDaoSuite:
    """
    Test suite for Docker data access objects (DAOs)
    """

    def test_docker_container_metadata(self, example_docker_container_metadata: DockerContainerMetadata) -> None:
        """
        Tests creation and dict conversion of the DockerContainerMetadata DAO

        :param example_docker_container_metadata: an example DockerContainerMetadata
        :return: None
        """
        assert isinstance(example_docker_container_metadata.to_dict(), dict)
        assert isinstance(DockerContainerMetadata.from_dict(example_docker_container_metadata.to_dict()),
                          DockerContainerMetadata)
        assert DockerContainerMetadata.from_dict(example_docker_container_metadata.to_dict()).to_dict() == \
               example_docker_container_metadata.to_dict()
        assert DockerContainerMetadata.from_dict(example_docker_container_metadata.to_dict()) == \
               example_docker_container_metadata

    def test_docker_env_metadata(self, example_docker_env_metadata: DockerEnvMetadata) -> None:
        """
        Tests creation and dict conversion of the DockerEnvMetadata DAO

        :param example_docker_env_metadata: an example DockerEnvMetadata
        :return: None
        """
        assert isinstance(example_docker_env_metadata.to_dict(), dict)
        assert isinstance(DockerEnvMetadata.from_dict(example_docker_env_metadata.to_dict()), DockerEnvMetadata)
        assert DockerEnvMetadata.from_dict(example_docker_env_metadata.to_dict()).to_dict() \
               == example_docker_env_metadata.to_dict()
        assert DockerEnvMetadata.from_dict(example_docker_env_metadata.to_dict()) == example_docker_env_metadata
