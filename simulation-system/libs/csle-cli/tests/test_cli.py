from click.testing import CliRunner
from csle_cli.cli import ls


class TestCSLECliSuite:
    """
    Test suite for cli.py
    """

    def test_ls_all(self) -> None:
        """
        Tests the ls command for --all

        :return: None
        """
        runner = CliRunner()
        result = runner.invoke(ls, ["--all"])
        assert result.exit_code == 0

    def test_ls_containers(self) -> None:
        """
        Tests the ls command for containers

        :return: None
        """
        runner = CliRunner()
        result = runner.invoke(ls, ["containers", "--all"])
        assert result.exit_code == 0

        runner = CliRunner()
        result = runner.invoke(ls, ["containers", "--running"])
        assert result.exit_code == 0

        runner = CliRunner()
        result = runner.invoke(ls, ["containers", "--stopped"])
        assert result.exit_code == 0

    def test_ls_networks(self) -> None:
        """
        Tests the ls command for networks

        :return: None
        """
        runner = CliRunner()
        result = runner.invoke(ls, ["networks"])
        assert result.exit_code == 0

    def test_ls_emulations(self) -> None:
        """
        Tests the ls command for emulations

        :return: None
        """
        runner = CliRunner()
        result = runner.invoke(ls, ["emulations", "--all"])
        assert result.exit_code == 0

        runner = CliRunner()
        result = runner.invoke(ls, ["emulations", "--stopped"])
        assert result.exit_code == 0

    def test_ls_environments(self) -> None:
        """
        Tests the ls command for environments

        :return: None
        """
        runner = CliRunner()
        result = runner.invoke(ls, ["environments"])
        assert result.exit_code == 0

    def test_ls_prometheus(self) -> None:
        """
        Tests the ls command for prometheus

        :return: None
        """
        runner = CliRunner()
        result = runner.invoke(ls, ["prometheus"])
        assert result.exit_code == 0

    def test_ls_node_exporter(self) -> None:
        """
        Tests the ls command for node_exporter

        :return: None
        """
        runner = CliRunner()
        result = runner.invoke(ls, ["node_exporter"])
        assert result.exit_code == 0

    def test_ls_cadvisor(self) -> None:
        """
        Tests the ls command for cadvisor

        :return: None
        """
        runner = CliRunner()
        result = runner.invoke(ls, ["cadvisor"])
        assert result.exit_code == 0

    def test_ls_nginx(self) -> None:
        """
        Tests the ls command for nginx

        :return: None
        """
        runner = CliRunner()
        result = runner.invoke(ls, ["nginx"])
        assert result.exit_code == 0
