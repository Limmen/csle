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
        Tests the ls command for containers

        :return: None
        """
        runner = CliRunner()
        result = runner.invoke(ls, ["networks"])
        assert result.exit_code == 0

    def test_ls_emulations(self) -> None:
        """
        Tests the ls command for containers

        :return: None
        """
        runner = CliRunner()
        result = runner.invoke(ls, ["emulations", "--all"])
        assert result.exit_code == 0

        runner = CliRunner()
        result = runner.invoke(ls, ["emulations", "--stopped"])
        assert result.exit_code == 0
