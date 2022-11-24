"""
Utility functions for training with the csle environments
"""
import io
import json
import logging
import time
import argparse
import os
import sys
import numpy as np
import random
import torch
import scipy.stats
from csle_common.dao.emulation_config.containers_config import ContainersConfig
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.encoding.np_encoder import NpEncoder
import csle_common.constants.constants as constants


class ExperimentUtil:
    """
    Class with utility functions related to training
    """

    @staticmethod
    def get_subdir(output_dir: str, results_dir: str, subdir: str, seed: int) -> str:
        """
        Utility function to construct the subdir string from a given results dir, subdir, and random seed

        :param output_dir: the base output directory
        :param results_dir: the base results dir
        :param subdir: the subdirectory (e.g. logs, data, tensorboard, etc)
        :param seed: the random seed
        :return: the directory path
        """
        return (output_dir + constants.COMMANDS.SLASH_DELIM + results_dir + constants.COMMANDS.SLASH_DELIM + subdir
                + constants.COMMANDS.SLASH_DELIM + str(seed) + constants.COMMANDS.SLASH_DELIM)

    @staticmethod
    def create_artifact_dirs(output_dir: str, random_seed: int) -> None:
        """
        Creates artifact directories if they do not already exist

        :param output_dir: the base directory
        :param random_seed: the random seed of the experiment
        :return: None
        """
        if not os.path.exists(ExperimentUtil.get_subdir(output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                        constants.EXPERIMENT.LOG_DIR, random_seed)):
            os.makedirs(ExperimentUtil.get_subdir(output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                  constants.EXPERIMENT.LOG_DIR, random_seed))
        if not os.path.exists(ExperimentUtil.get_subdir(output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                        constants.EXPERIMENT.PLOTS_DIR, random_seed)):
            os.makedirs(ExperimentUtil.get_subdir(output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                  constants.EXPERIMENT.PLOTS_DIR, random_seed))
        if not os.path.exists(ExperimentUtil.get_subdir(output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                        constants.EXPERIMENT.DATA_DIR, random_seed)):
            os.makedirs(ExperimentUtil.get_subdir(output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                  constants.EXPERIMENT.DATA_DIR, random_seed))
        if not os.path.exists(ExperimentUtil.get_subdir(output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                        constants.EXPERIMENT.HYPERPARAMETERS_DIR, random_seed)):
            os.makedirs(ExperimentUtil.get_subdir(output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                  constants.EXPERIMENT.HYPERPARAMETERS_DIR, random_seed))
        if not os.path.exists(ExperimentUtil.get_subdir(output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                        constants.EXPERIMENT.GIFS_DIR, random_seed)):
            os.makedirs(ExperimentUtil.get_subdir(output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                  constants.EXPERIMENT.GIFS_DIR, random_seed))
        if not os.path.exists(ExperimentUtil.get_subdir(output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                        constants.EXPERIMENT.TENSORBOARD_DIR, random_seed)):
            os.makedirs(ExperimentUtil.get_subdir(output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                  constants.EXPERIMENT.TENSORBOARD_DIR, random_seed))
        if not os.path.exists(ExperimentUtil.get_subdir(output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                        constants.EXPERIMENT.ENV_DATA_DIR, random_seed)):
            os.makedirs(ExperimentUtil.get_subdir(output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                  constants.EXPERIMENT.ENV_DATA_DIR, random_seed))

    @staticmethod
    def setup_experiment_logger(name: str, logdir: str, time_str: str = None):
        """
        Configures the logger for writing log-data of training

        :param name: name of the logger
        :param logdir: directory to save log files
        :param time_str: time string for file names
        :return: None
        """
        # create formatter
        formatter = logging.Formatter('%(asctime)s,%(message)s')
        # log to console
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)

        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        # log to file
        if time_str is None:
            time_str = str(time.time())
        fh = logging.FileHandler(logdir + constants.COMMANDS.SLASH_DELIM + time_str +
                                 constants.COMMANDS.UNDERSCORE_DELIM +
                                 name + constants.FILE_PATTERNS.LOG_SUFFIX, mode="w")
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)

        # add the handlers to the logger
        logger.addHandler(fh)
        return logger

    @staticmethod
    def write_emulation_config_file(emulation_env_config: EmulationEnvConfig, path: str) -> None:
        """
        Writes a config object to a config file

        :param emulation_env_config: the emulation env config object
        :param path: the path to write the file
        :return: None
        """
        json_str = json.dumps(emulation_env_config.to_dict(), indent=4, sort_keys=True)
        with io.open(path, 'w', encoding='utf-8') as f:
            f.write(json_str)

    @staticmethod
    def write_simulation_config_file(simulation_env_config: SimulationEnvConfig, path: str) -> None:
        """
        Writes a config object to a config file

        :param simulation_env_config: the simulation env config object
        :param path: the path to write the file
        :return: None
        """
        json_str = json.dumps(simulation_env_config.to_dict(), indent=4, sort_keys=True, cls=NpEncoder)
        with io.open(path, 'w', encoding='utf-8') as f:
            f.write(json_str)

    @staticmethod
    def read_emulation_env_config(emulation_env_config_path) -> EmulationEnvConfig:
        """
        Reads emulation env config from a json file

        :param emulation_env_config_path: the path to the emulation env config file
        :return: the emulation env configuration
        """
        with io.open(emulation_env_config_path, 'r', encoding='utf-8') as f:
            json_str = f.read()
        emulation_env_config: EmulationEnvConfig = EmulationEnvConfig.from_dict(json.loads(json_str))
        return emulation_env_config

    @staticmethod
    def read_simulation_env_config(simulation_env_config_path) -> SimulationEnvConfig:
        """
        Reads simulation env config from a json file

        :param simulation_env_config_path: the path to the simulation env config file
        :return: the simulation env configuration
        """
        with io.open(simulation_env_config_path, 'r', encoding='utf-8') as f:
            json_str = f.read()
        simulation_env_config: SimulationEnvConfig = SimulationEnvConfig.from_dict(json.loads(json_str))
        return simulation_env_config

    @staticmethod
    def read_env_picture(env_picture_path) -> bytes:
        """
        Reads the environment topology picture from a file

        :param env_picture_path: the path to picture
        :return: the emulation env configuration
        """
        with open(env_picture_path, "rb") as image_file:
            image_data = image_file.read()
            return image_data

    @staticmethod
    def read_containers_config(containers_config_path) -> ContainersConfig:
        """
        Reads containers_config of the experiment from a json file

        :param containers_config_path: the path to the containers_config file
        :return: the configuration
        """
        with io.open(containers_config_path, 'r', encoding='utf-8') as f:
            json_str = f.read()
        containers_cfg: ContainersConfig = ContainersConfig.from_dict(json.loads(json_str))
        return containers_cfg

    @staticmethod
    def parse_args(default_config_path):
        """
        Parses the commandline arguments with argparse

        :param default_config_path: default path to config file
        """
        parser = argparse.ArgumentParser(description='Parse flags to configure the json parsing')
        parser.add_argument("-cp", "--configpath", help="Path to configuration file",
                            default=default_config_path, type=str)
        parser.add_argument("-po", "--plotonly", help="Boolean parameter, if true, only plot",
                            action="store_true")
        parser.add_argument("-nc", "--noconfig", help="Boolean parameter, if true always override config",
                            action="store_true")
        parser.add_argument("-cs", "--csvfile", help="CSV file for plotting", type=str)
        parser.add_argument("-rd", "--resultdirs", help="List of comma-separated result dirs to combine for plotting",
                            type=str)
        args = parser.parse_args()
        return args

    @staticmethod
    def get_script_path():
        """
        :return: the script path
        """
        return os.path.dirname(os.path.realpath(sys.argv[0]))

    @staticmethod
    def default_output_dir() -> str:
        """
        :return: the default output dir
        """
        script_dir = ExperimentUtil.get_script_path()
        return script_dir

    @staticmethod
    def default_emulation_config_path(out_dir: str = None) -> str:
        """
        :param out_dir: directory to write
        :return: the default path to emulation config file
        """
        if out_dir is None:
            config_path = os.path.join(ExperimentUtil.default_output_dir(), constants.COMMANDS.DOT_DELIM
                                       + constants.DOCKER.EMULATION_ENV_CFG_PATH)
        else:
            config_path = os.path.join(out_dir, constants.COMMANDS.DOT_DELIM
                                       + constants.DOCKER.EMULATION_ENV_CFG_PATH)
        return config_path

    @staticmethod
    def default_simulation_config_path(out_dir: str = None) -> str:
        """
        :param out_dir: directory to write
        :return: the default path to simulatio config file
        """
        if out_dir is None:
            config_path = os.path.join(ExperimentUtil.default_output_dir(), constants.COMMANDS.DOT_DELIM
                                       + constants.SIMULATION.SIMULATION_ENV_CFG_PATH)
        else:
            config_path = os.path.join(out_dir, constants.COMMANDS.DOT_DELIM
                                       + constants.SIMULATION.SIMULATION_ENV_CFG_PATH)
        return config_path

    @staticmethod
    def default_emulation_picture_path(out_dir: str = None) -> str:
        """
        :param out_dir: directory to write
        :return: the default path to emulation img file
        """
        if out_dir is None:
            img_path = os.path.join(ExperimentUtil.default_output_dir(), (constants.COMMANDS.DOT_DELIM +
                                                                          constants.DOCKER.EMULATION_ENV_IMAGE))
        else:
            img_path = os.path.join(out_dir, constants.COMMANDS.DOT_DELIM + constants.DOCKER.EMULATION_ENV_IMAGE)
        return img_path

    @staticmethod
    def default_simulation_picture_path(out_dir: str = None) -> str:
        """
        :param out_dir: directory to write
        :return: the default path to simulatio img file
        """
        if out_dir is None:
            img_path = os.path.join(ExperimentUtil.default_output_dir(), constants.COMMANDS.DOT_DELIM
                                    + constants.DOCKER.SIMULATION_ENV_IMAGE)
        else:
            img_path = os.path.join(out_dir, constants.COMMANDS.DOT_DELIM
                                    + constants.DOCKER.SIMULATION_ENV_IMAGE)
        return img_path

    @staticmethod
    def default_containers_folders_path(out_dir: str = None) -> str:
        """
        :param out_dir: directory to write
        :return: the default path to container folders
        """
        if out_dir is None:
            config_path = os.path.join(ExperimentUtil.default_output_dir(), constants.COMMANDS.DOT_DELIM
                                       + constants.COMMANDS.SLASH_DELIM
                                       + constants.DOCKER.CONTAINERS_DIR)
        else:
            config_path = os.path.join(out_dir, constants.DOCKER.CONTAINERS_DIR)
        return config_path

    @staticmethod
    def default_makefile_template_path(out_dir: str = None) -> str:
        """
        :param out_dir: directory to write
        :return: the default path to makefile tempalte
        """
        if out_dir is None:
            config_path = os.path.join(ExperimentUtil.default_output_dir(), constants.COMMANDS.DOT_DELIM
                                       + constants.COMMANDS.SLASH_DELIM
                                       + constants.DOCKER.MAKEFILE_TEMPLATE)
        else:
            config_path = os.path.join(out_dir, constants.COMMANDS.DOT_DELIM
                                       + constants.COMMANDS.SLASH_DELIM + constants.DOCKER.MAKEFILE_TEMPLATE)
        return config_path

    @staticmethod
    def default_makefile_path(out_dir: str = None) -> str:
        """
        :param out_dir: directory to write
        :return: the default path to makefile tempalte
        """
        if out_dir is None:
            config_path = os.path.join(ExperimentUtil.default_output_dir(), constants.COMMANDS.DOT_DELIM
                                       + constants.COMMANDS.SLASH_DELIM +
                                       constants.DOCKER.MAKEFILE)
        else:
            config_path = os.path.join(out_dir, constants.COMMANDS.DOT_DELIM
                                       + constants.COMMANDS.SLASH_DELIM + constants.DOCKER.MAKEFILE)
        return config_path

    @staticmethod
    def running_average(x, N):
        ''' Function used to compute the running average
            of the last N elements of a vector x
        '''
        if len(x) < N:
            N = len(x)
        if len(x) >= N:
            y = np.copy(x)
            y[N - 1:] = np.convolve(x, np.ones((N, )) / N, mode='valid')
        else:
            y = np.zeros_like(x)
        return round(y[-1], 2)

    @staticmethod
    def running_average_list(x, N):
        ''' Function used to compute the running average
            of the last N elements of a vector x
        '''
        if len(x) < N:
            N = len(x)
        if len(x) >= N:
            y = np.copy(x)
            y[N - 1:] = np.convolve(x, np.ones((N, )) / N, mode='valid')
        else:
            y = np.zeros_like(x)
        return y

    @staticmethod
    def mean_confidence_interval(data, confidence=0.95):
        """
        Compute confidence intervals

        :param data: the data
        :param confidence: the interval confidence
        :return: the mean, the lower confidence interval, the upper confidence interval
        """
        a = 1.0 * np.array(data)
        n = len(a)
        m, se = np.mean(a), scipy.stats.sem(a)
        h = se * scipy.stats.t.ppf((1 + confidence) / 2., n - 1)
        return m, h

    @staticmethod
    def set_seed(seed: int) -> None:
        """
        Sets the random seed

        :param seed: the seed to set
        :return: None
        """
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
