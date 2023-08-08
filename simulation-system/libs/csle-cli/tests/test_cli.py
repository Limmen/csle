from click.testing import CliRunner
from csle_cli.cli import ls


class TestCSLECliSuite:
    """
    Test suite for cli.py
    """

    def test_ls(self) -> None:
        """
        Tests the ls command

        :return: None
        """
        runner = CliRunner()
        result = runner.invoke(ls, ["--all"])
        assert result.exit_code == 0
