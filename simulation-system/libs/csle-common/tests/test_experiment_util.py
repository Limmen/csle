from unittest.mock import patch, MagicMock
from csle_common.util.experiment_util import ExperimentUtil
import csle_common.constants.constants as constants
import tempfile
import os
import shutil
import sys
import numpy as np
import random
import torch


class TestExperimentUtilSuite:
    """
    Test suite for experiment util
    """

    def test_get_subdir(self) -> None:
        """
        Test the function that constructs the subdir string from a given results dir, subdir, and random seed

        :return: None
        """
        output_dir = "output"
        results_dir = "results"
        subdir = "logs"
        seed = 10

        expected = "output/results/logs/10/"
        result = ExperimentUtil.get_subdir(output_dir=output_dir, results_dir=results_dir, subdir=subdir, seed=seed)

        assert expected == result

    def test_create_artifact_dirs(self) -> None:
        """
        Test the method that creates artifact directories if they do not already exist

        :return: None
        """
        temp_dir = tempfile.mkdtemp()
        try:
            random_seed = 10
            ExperimentUtil.create_artifact_dirs(output_dir=temp_dir, random_seed=random_seed)
            expected_dirs = [
                constants.EXPERIMENT.LOG_DIR,
                constants.EXPERIMENT.PLOTS_DIR,
                constants.EXPERIMENT.DATA_DIR,
                constants.EXPERIMENT.HYPERPARAMETERS_DIR,
                constants.EXPERIMENT.GIFS_DIR,
                constants.EXPERIMENT.TENSORBOARD_DIR,
                constants.EXPERIMENT.ENV_DATA_DIR,
            ]
            for subdir in expected_dirs:
                subdir_path = os.path.join(temp_dir, constants.EXPERIMENT.RESULTS_DIR, subdir, str(random_seed))
                assert os.path.exists(subdir_path), f"Directory {subdir_path} does not exist"

        finally:
            shutil.rmtree(temp_dir)

    def test_setup_experiment_logger(self, tmpdir) -> None:
        """
        Test the function that configures the logger for writing log-data of training

        :param tmpdir: temporary directory
        :return: None
        """
        logger_name = "test_logger"
        logdir = str(tmpdir.mkdir("logs"))
        time_str = "20240101-1234"

        logger = ExperimentUtil.setup_experiment_logger(name=logger_name, logdir=logdir, time_str=time_str)
        assert logger.name == logger_name

    @patch("io.open")
    def test_write_emulation_config_file(self, mock_open) -> None:
        """
        Test the function that writes a config object to a config file

        :param mock_open: mock_open
        :return: None
        """
        emulation_env_config = MagicMock()
        emulation_env_config.to_dict.return_value = {"key1": "value1", "key2": "value2"}
        ExperimentUtil.write_emulation_config_file(emulation_env_config=emulation_env_config, path="path")
        mock_open.assert_called()

    @patch("io.open")
    def test_write_simulation_config_file(self, mock_open) -> None:
        """
        Test the function that writes a config object to a config file

        :param mock_open: mock_open
        :return: None
        """
        simulation_env_config = MagicMock()
        simulation_env_config.to_dict.return_value = {"key1": "value1", "key2": "value2"}
        ExperimentUtil.write_simulation_config_file(simulation_env_config=simulation_env_config, path="path")
        mock_open.assert_called()

    @patch("builtins.open")
    def test_read_env_picture(self, mock_open) -> None:
        """
        Mock the method that reads the environment topology picture from a file

        :param mock_open: mock_open
        :return: None
        """
        mock_open.return_value.__enter__.return_value.read.return_value = b"fake_image_data"
        image_data = ExperimentUtil.read_env_picture("fake_path")
        assert image_data == b"fake_image_data"

    @patch.object(sys, "argv", ["file_name"])
    def test_parse_args(self) -> None:
        """
        Test the method that parses the commandline arguments with argparse

        :return: None
        """
        default_config_path = "default/path/to/config.json"
        args = ExperimentUtil.parse_args(default_config_path)
        assert args.configpath == default_config_path

    @patch.object(sys, "argv", ["/fake/path/to/script.py"])
    def test_get_script_path(self) -> None:
        """
        Test the method that returns the script path

        :return: None
        """
        expected_path = "/fake/path/to"
        script_path = ExperimentUtil.get_script_path()
        assert script_path == expected_path

    @patch("csle_common.util.experiment_util.ExperimentUtil.get_script_path")
    def test_default_output_dir(self, mock_get_script_path) -> None:
        """
        Test the method that returns the default output dir

        :param mock_get_script_path: mock_get_script_path
        :return: None
        """
        mock_get_script_path.return_value = "path"
        expected_path = "path"
        output_dir = ExperimentUtil.default_output_dir()
        assert output_dir == expected_path

    @patch("csle_common.util.experiment_util.ExperimentUtil.default_output_dir")
    def test_default_emulation_config_path(self, mock_default_output_dir) -> None:
        """
        Test the method that returns the default path to emulation config file

        :param mock_default_output_dir: mock_default_output_dir
        :return: None
        """
        mock_default_output_dir.return_value = "/fake/default/output/dir"
        constants.COMMANDS.DOT_DELIM = "."
        constants.DOCKER.EMULATION_ENV_CFG_PATH = "fake_emulation_config.json"
        expected_path = "/fake/default/output/dir/.fake_emulation_config.json"
        config_path = ExperimentUtil.default_emulation_config_path()
        assert config_path == expected_path

    @patch("csle_common.util.experiment_util.ExperimentUtil.default_output_dir")
    def test_default_simulation_config_path(self, mock_default_output_dir) -> None:
        """
        Test the method that returns the default path to simulation config file

        :param mock_default_output_dir: mock_default_output_dir
        :return: None
        """
        mock_default_output_dir.return_value = "/fake/default/output/dir"
        constants.COMMANDS.DOT_DELIM = "."
        constants.SIMULATION.SIMULATION_ENV_CFG_PATH = "fake_simulation_config.json"
        expected_path = "/fake/default/output/dir/.fake_simulation_config.json"
        config_path = ExperimentUtil.default_simulation_config_path()
        assert config_path == expected_path

    @patch("csle_common.util.experiment_util.ExperimentUtil.default_output_dir")
    def test_default_emulation_picture_path(self, mock_default_output_dir) -> None:
        """
        Test the method that returns the default path to emulation picture file

        :param mock_default_output_dir: mock_default_output_dir
        :return: None
        """
        mock_default_output_dir.return_value = "/fake/default/output/dir"
        constants.COMMANDS.DOT_DELIM = "."
        constants.DOCKER.EMULATION_ENV_IMAGE = "fake_emulation_picture.img"
        expected_path = "/fake/default/output/dir/.fake_emulation_picture.img"
        picture_path = ExperimentUtil.default_emulation_picture_path()
        assert picture_path == expected_path

    @patch("csle_common.util.experiment_util.ExperimentUtil.default_output_dir")
    def test_default_simulation_picture_path(self, mock_default_output_dir) -> None:
        """
        Test the method that returns the default path to simulation picture file

        :param mock_default_output_dir: mock_default_output_dir
        :return: None
        """
        mock_default_output_dir.return_value = "/fake/default/output/dir"
        constants.COMMANDS.DOT_DELIM = "."
        constants.DOCKER.SIMULATION_ENV_IMAGE = "fake_simulation_picture.img"
        expected_path = "/fake/default/output/dir/.fake_simulation_picture.img"
        picture_path = ExperimentUtil.default_simulation_picture_path()
        assert picture_path == expected_path

    @patch("csle_common.util.experiment_util.ExperimentUtil.default_output_dir")
    def test_default_containers_folders_path(self, mock_default_output_dir) -> None:
        """
        Test the method that returns the default path to container folders

        :param mock_default_output_dir: mock_default_output_dir
        :return: None
        """
        mock_default_output_dir.return_value = "/fake/default/output/dir"
        constants.COMMANDS.DOT_DELIM = "."
        constants.COMMANDS.SLASH_DELIM = "/"
        constants.DOCKER.CONTAINERS_DIR = "container"
        expected_path = "/fake/default/output/dir/./container"
        container_path = ExperimentUtil.default_containers_folders_path()
        assert container_path == expected_path

    @patch("csle_common.util.experiment_util.ExperimentUtil.default_output_dir")
    def default_makefile_template_path(self, mock_default_output_dir) -> None:
        """
        Test the method that returns the default path to makefile tempalte

        :param mock_default_output_dir: mock_default_output_dir
        :return: None
        """
        mock_default_output_dir.return_value = "/fake/default/output/dir"
        constants.COMMANDS.DOT_DELIM = "."
        constants.COMMANDS.SLASH_DELIM = "/"
        constants.DOCKER.MAKEFILE_TEMPLATE = "makefile"
        expected_path = "/fake/default/output/dir/./makefile"
        config_path = ExperimentUtil.default_makefile_template_path()
        assert config_path == expected_path

    @patch("csle_common.util.experiment_util.ExperimentUtil.default_output_dir")
    def default_makefile_path(self, mock_default_output_dir) -> None:
        """
        Test the method that returns the default path to makefile tempalte

        :param mock_default_output_dir: mock_default_output_dir
        :return: None
        """
        mock_default_output_dir.return_value = "/fake/default/output/dir"
        constants.COMMANDS.DOT_DELIM = "."
        constants.COMMANDS.SLASH_DELIM = "/"
        constants.DOCKER.MAKEFILE = "makefile"
        expected_path = "/fake/default/output/dir/./makefile"
        config_path = ExperimentUtil.default_makefile_path()
        assert config_path == expected_path

    def test_running_average_basic(self) -> None:
        """
        Test the method that used to compute the running average of the last N elements of a vector x

        :return: None
        """
        x = np.array([1, 2])
        N = 3
        result = ExperimentUtil.running_average(x, N)
        expected_result = 1
        assert result == expected_result

    def test_running_average_list(self) -> None:
        """
        Test the method that used to compute the running average of the last N elements of a vector x

        :return: None
        """
        x = [1, 2, 3, 4, 5]
        N = 3
        result = ExperimentUtil.running_average_list(x, N)
        expected_result = [1, 2, 2, 3, 3]
        assert np.allclose(result, expected_result)

    def test_mean_confidence_interval(self) -> None:
        """
        Test the method that compute confidence intervals

        :return: None
        """
        data = [1, 2, 3, 4, 5]
        m, _ = ExperimentUtil.mean_confidence_interval(data, 0.95)
        assert np.isclose(m, 3.0)

    def test_set_seed(self) -> None:
        """
        Test the method that sets the random seed

        :return: None
        """
        seed = 42

        ExperimentUtil.set_seed(seed)
        random_numbers1 = [random.random() for _ in range(5)]
        np_random_numbers1 = np.random.rand(5)
        torch_random_numbers1 = torch.rand(5)

        ExperimentUtil.set_seed(seed)
        random_numbers2 = [random.random() for _ in range(5)]
        np_random_numbers2 = np.random.rand(5)
        torch_random_numbers2 = torch.rand(5)

        assert random_numbers1 == random_numbers2
        assert np.allclose(np_random_numbers1, np_random_numbers2)
        assert torch.equal(torch_random_numbers1, torch_random_numbers2)

    def test_regress_lists(self) -> None:
        """
        Test the method that regress sublists.

        :return: None
        """
        lists = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]
        result = ExperimentUtil.regress_lists(lists)
        expected_result = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]
        assert np.allclose(result[0], expected_result[0])
        assert np.allclose(result[1], expected_result[1])
        assert np.allclose(result[2], expected_result[2])
