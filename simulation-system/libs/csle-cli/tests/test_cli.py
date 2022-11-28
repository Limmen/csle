from click.testing import CliRunner
import logging
import pytest
from csle_cli.cli import ls


class TestCSLECliSuite(object):
    """
    Test suite for cli.py
    """

    pytest.logger = logging.getLogger("cli_tests")

    def test_ls(self) -> None:
        """
        Tests the ls command

        :return: None
        """
        runner = CliRunner()
        result = runner.invoke(ls, ["--all"])
        assert result.exit_code == 0
