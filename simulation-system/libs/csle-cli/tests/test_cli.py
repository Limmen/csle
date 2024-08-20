import logging
from typing import List
from click.testing import CliRunner
from csle_cli.cli import ls

from csle_cluster.cluster_manager.cluster_manager_pb2 import DockerContainerDTO


class TestCSLECliSuite:
    """
    Test suite for cli.py
    """

    def test_ls_all(self) -> None:
        """
        Tests the ls command

        :return: None
        """
        runner = CliRunner()
        result = runner.invoke(ls, ["--all"])
        assert result.exit_code == 0

    def test_ls_running_containers(self) -> None:
        """
        Tests the ls command

        :return: None
        """
        import csle_common.constants.constants as constants
        from csle_common.metastore.metastore_facade import MetastoreFacade
        from csle_cluster.cluster_manager.cluster_controller import ClusterController
        config = MetastoreFacade.get_config(id=1)
        running_containers: List[DockerContainerDTO] = []
        for node in config.cluster_config.cluster_nodes:
            running_containers_dto = ClusterController.list_all_running_containers(
                ip=node.ip, port=constants.GRPC_SERVERS.CLUSTER_MANAGER_PORT)
            running_containers_dtos = list(running_containers_dto.runningContainers)
            running_containers = running_containers + running_containers_dtos
        runner = CliRunner()
        result = runner.invoke(ls, ["containers"])
        cli_output = result.stdout_bytes.decode('utf-8')
        cli_output_lines = cli_output.strip().split('\n')
        number_of_containers_from_cli = 0
        for line in cli_output_lines:
            if "[running]" in line:
                number_of_containers_from_cli += 1

        assert number_of_containers_from_cli == len(running_containers)
        assert result.exit_code == 0
