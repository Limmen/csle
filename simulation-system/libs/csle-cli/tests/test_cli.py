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

    def test_ls_postgresql(self) -> None:
        """
        Tests the ls command for postgresql

        :return: None
        """
        runner = CliRunner()
        result = runner.invoke(ls, ["postgresql"])
        assert result.exit_code == 0

    def test_ls_docker(self) -> None:
        """
        Tests the ls command for docker

        :return: None
        """
        runner = CliRunner()
        result = runner.invoke(ls, ["docker"])
        assert result.exit_code == 0

    def test_ls_pgadmin(self) -> None:
        """
        Tests the ls command for pgadmin

        :return: None
        """
        runner = CliRunner()
        result = runner.invoke(ls, ["pgadmin"])
        assert result.exit_code == 0

    def test_ls_grafana(self) -> None:
        """
        Tests the ls command for grafana

        :return: None
        """
        runner = CliRunner()
        result = runner.invoke(ls, ["grafana"])
        assert result.exit_code == 0

    def test_ls_flask(self) -> None:
        """
        Tests the ls command for flask

        :return: None
        """
        runner = CliRunner()
        result = runner.invoke(ls, ["flask"])
        assert result.exit_code == 0

    def test_ls_statsmanager(self) -> None:
        """
        Tests the ls command for statsmanager

        :return: None
        """
        runner = CliRunner()
        result = runner.invoke(ls, ["statsmanager"])
        assert result.exit_code == 0

    def test_ls_simulations(self) -> None:
        """
        Tests the ls command for simulations

        :return: None
        """
        runner = CliRunner()
        result = runner.invoke(ls, ["simulations"])
        assert result.exit_code == 0

    def test_ls_emulation_executions(self) -> None:
        """
        Tests the ls command for emulation_executions

        :return: None
        """
        runner = CliRunner()
        result = runner.invoke(ls, ["emulation_executions"])
        assert result.exit_code == 0

    def test_ls_cluster(self) -> None:
        """
        Tests the ls command for clsuter

        :return: None
        """
        runner = CliRunner()
        result = runner.invoke(ls, ["cluster"])
        assert result.exit_code == 0

    def test_ls_images(self) -> None:
        """
        Tests the ls command for images

        :return: None
        """
        runner = CliRunner()
        result = runner.invoke(ls, ["images"])
        assert result.exit_code == 0
