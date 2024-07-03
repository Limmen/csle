import subprocess
from unittest.mock import patch, MagicMock
from csle_common.controllers.installation_controller import InstallationController


class TestInstallationControllerSuite:
    """
    Test suite for installation_controller
    """

    @patch("subprocess.Popen")
    def test_install_all_emulations(self, mock_popen) -> None:
        """
        Test the method that installs all emulations in the metastore

        :param mock_popen: mock Popen method
        :return: None
        """
        # mock the process returned by 'subprocess.Popen', which includes 'stdout' and 'poll'
        mock_process = MagicMock()
        mock_process.stdout.read.side_effect = [b"c", b"d", b"", b"$"]
        mock_process.poll.side_effect = [None, None, None, 0]  # return 0, means stop running
        mock_popen.return_value = mock_process
        InstallationController.install_all_emulations()
        mock_popen.assert_called_once_with(
            "cd $CSLE_HOME/emulation-system/envs/ && make install", stdout=subprocess.PIPE, shell=True)
        assert mock_process.stdout.read.call_count == 4
        assert mock_process.poll.call_count == 4

    @patch("subprocess.Popen")
    def test_install_emulation(self, mock_popen) -> None:
        """
        Test the method that installs a given emulation in the metastore

        :param mock_popen: mock Popen method
        :return: None
        """
        # mock the process returned by 'subprocess.Popen', which includes 'stdout' and 'poll'
        mock_process = MagicMock()
        mock_process.stdout.read.side_effect = [b"c", b"d", b"", b"$"]
        mock_process.poll.side_effect = [None, None, None, 0]  # return 0, means stop running
        mock_popen.return_value = mock_process
        InstallationController.install_emulation(emulation_name="name")
        mock_popen.assert_called_once_with(
            "cd $CSLE_HOME/emulation-system/envs/ && make install_name", stdout=subprocess.PIPE, shell=True)
        assert mock_process.stdout.read.call_count == 4
        assert mock_process.poll.call_count == 4

    @patch("subprocess.Popen")
    def test_uninstall_emulation(self, mock_popen) -> None:
        """
        Test the method that uninstalls a given emulation in the metastore

        :param mock_popen: mock Popen method
        :return: None
        """
        # mock the process returned by 'subprocess.Popen', which includes 'stdout' and 'poll'
        mock_process = MagicMock()
        mock_process.stdout.read.side_effect = [b"c", b"d", b"", b"$"]
        mock_process.poll.side_effect = [None, None, None, 0]  # return 0, means stop running
        mock_popen.return_value = mock_process
        InstallationController.uninstall_emulation(emulation_name="name")
        mock_popen.assert_called_once_with(
            "cd $CSLE_HOME/emulation-system/envs/ && make uninstall_name", stdout=subprocess.PIPE, shell=True)
        assert mock_process.stdout.read.call_count == 4
        assert mock_process.poll.call_count == 4

    @patch("subprocess.Popen")
    def test_uninstall_emulations(self, mock_popen) -> None:
        """
        Test the method that uninstalls all emulations in the metastore

        :param mock_popen: mock Popen method
        :return: None
        """
        # mock the process returned by 'subprocess.Popen', which includes 'stdout' and 'poll'
        mock_process = MagicMock()
        mock_process.stdout.read.side_effect = [b"c", b"d", b"", b"$"]
        mock_process.poll.side_effect = [None, None, None, 0]  # return 0, means stop running
        mock_popen.return_value = mock_process
        InstallationController.uninstall_all_emulations()
        mock_popen.assert_called_once_with("cd $CSLE_HOME/emulation-system/envs/ && make uninstall",
                                           stdout=subprocess.PIPE, shell=True)
        assert mock_process.stdout.read.call_count == 4
        assert mock_process.poll.call_count == 4

    @patch("subprocess.Popen")
    def test_install_all_simulations(self, mock_popen) -> None:
        """
        Test the method that installs all simulations in the metastore

        :param mock_popen: mock Popen method
        :return: None
        """
        # mock the process returned by 'subprocess.Popen', which includes 'stdout' and 'poll'
        mock_process = MagicMock()
        mock_process.stdout.read.side_effect = [b"c", b"d", b"", b"$"]
        mock_process.poll.side_effect = [None, None, None, 0]  # return 0, means stop running
        mock_popen.return_value = mock_process
        InstallationController.install_all_simulations()
        mock_popen.assert_called_once_with(
            "cd $CSLE_HOME/simulation-system/envs/ && make install", stdout=subprocess.PIPE, shell=True)
        assert mock_process.stdout.read.call_count == 4
        assert mock_process.poll.call_count == 4

    @patch("subprocess.Popen")
    def test_install_simulation(self, mock_popen) -> None:
        """
        Test the method that installs a given simulation in the metastore

        :param mock_popen: mock Popen method
        :return: None
        """
        # mock the process returned by 'subprocess.Popen', which includes 'stdout' and 'poll'
        mock_process = MagicMock()
        mock_process.stdout.read.side_effect = [b"c", b"d", b"", b"$"]
        mock_process.poll.side_effect = [None, None, None, 0]  # return 0, means stop running
        mock_popen.return_value = mock_process
        InstallationController.install_simulation(simulation_name="name")
        mock_popen.assert_called_once_with(
            "cd $CSLE_HOME/simulation-system/envs/ && make install_name",
            stdout=subprocess.PIPE, shell=True)
        assert mock_process.stdout.read.call_count == 4
        assert mock_process.poll.call_count == 4

    @patch("subprocess.Popen")
    def test_uninstall_simulation(self, mock_popen) -> None:
        """
        Test the method that uninstalls a given simulation in the metastore

        :param mock_popen: mock Popen method
        :return: None
        """
        # mock the process returned by 'subprocess.Popen', which includes 'stdout' and 'poll'
        mock_process = MagicMock()
        mock_process.stdout.read.side_effect = [b"c", b"d", b"", b"$"]
        mock_process.poll.side_effect = [None, None, None, 0]  # return 0, means stop running
        mock_popen.return_value = mock_process
        InstallationController.uninstall_simulation(simulation_name="name")
        mock_popen.assert_called_once_with(
            "cd $CSLE_HOME/simulation-system/envs/ && make uninstall_name", stdout=subprocess.PIPE, shell=True)
        assert mock_process.stdout.read.call_count == 4
        assert mock_process.poll.call_count == 4

    @patch("subprocess.Popen")
    def test_uninstall_all_simulations(self, mock_popen) -> None:
        """
        Test the method that uninstalls all simulations in the metastore

        :param mock_popen: mock Popen method
        :return: None
        """
        # mock the process returned by 'subprocess.Popen', which includes 'stdout' and 'poll'
        mock_process = MagicMock()
        mock_process.stdout.read.side_effect = [b"c", b"d", b"", b"$"]
        mock_process.poll.side_effect = [None, None, None, 0]  # return 0, means stop running
        mock_popen.return_value = mock_process
        InstallationController.uninstall_all_simulations()
        mock_popen.assert_called_once_with(
            "cd $CSLE_HOME/simulation-system/envs/ && make uninstall", stdout=subprocess.PIPE, shell=True)
        assert mock_process.stdout.read.call_count == 4
        assert mock_process.poll.call_count == 4

    @patch("subprocess.Popen")
    def test_install_derived_images(self, mock_popen) -> None:
        """
        Test the method that installs all derived Docker images

        :param mock_popen: mock Popen method
        :return: None
        """
        # mock the process returned by 'subprocess.Popen', which includes 'stdout' and 'poll'
        mock_process = MagicMock()
        mock_process.stdout.read.side_effect = [b"c", b"d", b"", b"$"]
        mock_process.poll.side_effect = [None, None, None, 0]  # return 0, means stop running
        mock_popen.return_value = mock_process
        InstallationController.install_derived_images()
        mock_popen.assert_called_once_with(
            "cd $CSLE_HOME/emulation-system/derived_images/ && make build", stdout=subprocess.PIPE, shell=True)
        assert mock_process.stdout.read.call_count == 4
        assert mock_process.poll.call_count == 4

    @patch("subprocess.Popen")
    def test_uninstall_derived_images(self, mock_popen) -> None:
        """
        Test the method that uninstalls all derived Docker images

        :param mock_popen: mock Popen method

        :return: None
        """
        # mock the process returned by 'subprocess.Popen', which includes 'stdout' and 'poll'
        mock_process = MagicMock()
        mock_process.stdout.read.side_effect = [b"c", b"d", b"", b"$"]
        mock_process.poll.side_effect = [None, None, None, 0]  # return 0, means stop running
        mock_popen.return_value = mock_process
        InstallationController.uninstall_derived_images()
        mock_popen.assert_called_once_with(
            "cd $CSLE_HOME/emulation-system/derived_images/ && make rm_image", stdout=subprocess.PIPE, shell=True)
        assert mock_process.stdout.read.call_count == 4
        assert mock_process.poll.call_count == 4

    @patch("subprocess.Popen")
    def test_uninstall_derived_image(self, mock_popen) -> None:
        """
        Test the method that uninstalls a given derived Docker images

        :param mock_popen: mock Popen method
        :return: None
        """
        # mock the process returned by 'subprocess.Popen', which includes 'stdout' and 'poll'
        mock_process = MagicMock()
        mock_process.stdout.read.side_effect = [b"c", b"d", b"", b"$"]
        mock_process.poll.side_effect = [None, None, None, 0]  # return 0, means stop running
        mock_popen.return_value = mock_process
        InstallationController.uninstall_derived_image(image_name="image")
        mock_popen.assert_called_once_with(
            "cd $CSLE_HOME/emulation-system/derived_images/ && make rm_image", stdout=subprocess.PIPE, shell=True)
        assert mock_process.stdout.read.call_count == 4
        assert mock_process.poll.call_count == 4

    @patch("subprocess.Popen")
    def test_install_base_images(self, mock_popen) -> None:
        """
        Test the method that installs all base Docker images

        :param mock_popen: mock Popen method
        :return: None
        """
        # mock the process returned by 'subprocess.Popen', which includes 'stdout' and 'poll'
        mock_process = MagicMock()
        mock_process.stdout.read.side_effect = [b"c", b"d", b"", b"$"]
        mock_process.poll.side_effect = [None, None, None, 0]  # return 0, means stop running
        mock_popen.return_value = mock_process
        InstallationController.install_base_images()
        mock_popen.assert_called_once_with(
            "cd $CSLE_HOME/emulation-system/base_images/ && make build", stdout=subprocess.PIPE, shell=True)
        assert mock_process.stdout.read.call_count == 4
        assert mock_process.poll.call_count == 4

    @patch("subprocess.Popen")
    def test_install_base_image(self, mock_popen) -> None:
        """
        Test the method that installs a given base Docker images

        :param mock_popen: mock Popen method
        :return: None
        """
        # mock the process returned by 'subprocess.Popen', which includes 'stdout' and 'poll'
        mock_process = MagicMock()
        mock_process.stdout.read.side_effect = [b"c", b"d", b"", b"$"]
        mock_process.poll.side_effect = [None, None, None, 0]  # return 0, means stop running
        mock_popen.return_value = mock_process
        InstallationController.install_base_image(image_name="name")
        mock_popen.assert_called_once_with(
            "cd $CSLE_HOME/emulation-system/base_images/ && make name", stdout=subprocess.PIPE, shell=True)
        assert mock_process.stdout.read.call_count == 4
        assert mock_process.poll.call_count == 4

    @patch("subprocess.Popen")
    def test_uninstall_base_images(self, mock_popen) -> None:
        """
        Test the method that uninstalls all base Docker images

        :param mock_popen: mock Popen method

        :return: None
        """
        # mock the process returned by 'subprocess.Popen', which includes 'stdout' and 'poll'
        mock_process = MagicMock()
        mock_process.stdout.read.side_effect = [b"c", b"d", b"", b"$"]
        mock_process.poll.side_effect = [None, None, None, 0]  # return 0, means stop running
        mock_popen.return_value = mock_process
        InstallationController.uninstall_base_images()
        mock_popen.assert_called_once_with(
            "cd $CSLE_HOME/emulation-system/base_images/ && make rm_image", stdout=subprocess.PIPE, shell=True)
        assert mock_process.stdout.read.call_count == 4
        assert mock_process.poll.call_count == 4

    @patch("subprocess.Popen")
    def test_uninstall_base_image(self, mock_popen) -> None:
        """
        Test the method that uninstalls a given base Docker images

        :param mock_popen: mock Popen method
        :return: None
        """
        # mock the process returned by 'subprocess.Popen', which includes 'stdout' and 'poll'
        mock_process = MagicMock()
        mock_process.stdout.read.side_effect = [b"c", b"d", b"", b"$"]
        mock_process.poll.side_effect = [None, None, None, 0]  # return 0, means stop running
        mock_popen.return_value = mock_process
        InstallationController.uninstall_base_image(image_name="name")
        mock_popen.assert_called_once_with(
            "cd $CSLE_HOME/emulation-system/base_images/ && make rm_name", stdout=subprocess.PIPE, shell=True)
        assert mock_process.stdout.read.call_count == 4
        assert mock_process.poll.call_count == 4

    @patch("subprocess.Popen")
    def test_uninstall_metastore(self, mock_popen) -> None:
        """
        Test the method that uninstalls the metastore

        :param mock_popen: mock Popen method
        :return: None
        """
        # mock the process returned by 'subprocess.Popen', which includes 'stdout' and 'poll'
        mock_process = MagicMock()
        mock_process.stdout.read.side_effect = [b"c", b"d", b"", b"$"]
        mock_process.poll.side_effect = [None, None, None, 0]  # return 0, means stop running
        mock_popen.return_value = mock_process
        InstallationController.uninstall_metastore()
        mock_popen.assert_called_once_with("cd $CSLE_HOME/metastore/ && make clean", stdout=subprocess.PIPE, shell=True)
        assert mock_process.stdout.read.call_count == 4
        assert mock_process.poll.call_count == 4

    @patch("subprocess.Popen")
    def test_install_metastore(self, mock_popen) -> None:
        """
        Test the method that installs the metastore

        :param mock_popen: mock Popen method
        :return: None
        """
        # mock the process returned by 'subprocess.Popen', which includes 'stdout' and 'poll'
        mock_process = MagicMock()
        mock_process.stdout.read.side_effect = [b"c", b"d", b"", b"$"]
        mock_process.poll.side_effect = [None, None, None, 0]  # return 0, means stop running
        mock_popen.return_value = mock_process
        InstallationController.install_metastore()
        mock_popen.assert_called_once_with("cd $CSLE_HOME/metastore/ && make build", stdout=subprocess.PIPE, shell=True)
        assert mock_process.stdout.read.call_count == 4
        assert mock_process.poll.call_count == 4
