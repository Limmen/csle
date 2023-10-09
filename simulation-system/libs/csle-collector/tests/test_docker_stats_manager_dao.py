from csle_collector.docker_stats_manager.dao.docker_stats import DockerStats


class TestDockerStatsManagerDaoSuite:
    """
    Test suite for datasets data access objects (DAOs) in docker_stats_manager
    """

    def test_docker_stats(self, example_docker_stats: DockerStats) -> None:
        """
        Tests creation and dict conversion of the DockerStats DAO

        :param example_docker_stats: an example DockerStats
        :return: None
        """
        assert isinstance(example_docker_stats.to_dict(), dict)
        assert isinstance(DockerStats.from_dict(example_docker_stats.to_dict()), DockerStats)
        assert (DockerStats.from_dict(example_docker_stats.to_dict()).to_dict() == example_docker_stats.to_dict())
        assert (DockerStats.from_dict(example_docker_stats.to_dict()) == example_docker_stats)
