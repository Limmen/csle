"""
Utility functions for experiments with the pycr environments
"""
from typing import Tuple
import io
import json
import jsonpickle
import logging
import time
import argparse
import os
import sys
from gym_pycr_pwcrack.dao.experiment.client_config import ClientConfig
from gym_pycr_pwcrack.runner.runner import Runner

def run_experiment(config: ClientConfig, random_seed: int, title :str = "v0") -> Tuple[str, str]:
    """
    Runs an inidividual experiment

    :param config: the config of the experiment
    :param random_seed: random seed
    :param title: title of the experiment
    :return: train_csv_path, eval_csv_path
    """
    time_str = str(time.time())
    create_artefact_dirs(config.output_dir, random_seed)
    logger = setup_logger(title, config.output_dir + "/results/logs/" +
                               str(random_seed) + "/",
                               time_str=time_str)
    config.pg_agent_config.save_dir = default_output_dir() + "/results/data/" + str(random_seed) + "/"
    config.pg_agent_config.video_dir = default_output_dir() + "/results/videos/" + str(random_seed) + "/"
    config.pg_agent_config.gif_dir = default_output_dir() + "/results/gifs/" + str(random_seed) + "/"
    config.pg_agent_config.tensorboard_dir = default_output_dir() + "/results/tensorboard/" \
                                             + str(random_seed) + "/"
    config.env_checkpoint_dir = default_output_dir() + "/results/env_data/" + str(random_seed) + "/"
    config.logger = logger
    config.pg_agent_config.logger = logger
    config.pg_agent_config.random_seed = random_seed
    config.random_seed = random_seed
    config.pg_agent_config.to_csv(
        config.output_dir + "/results/hyperparameters/" + str(random_seed) + "/" + time_str + ".csv")
    train_csv_path = ""
    eval_csv_path = ""
    train_result, eval_result = Runner.run(config)
    if len(train_result.avg_episode_steps) > 0 and len(eval_result.avg_episode_steps) > 0:
        train_csv_path = config.output_dir + "/results/data/" + str(random_seed) + "/" + time_str + "_train" + ".csv"
        train_result.to_csv(train_csv_path)
        eval_csv_path = config.output_dir + "/results/data/" + str(random_seed) + "/" + time_str + "_eval" + ".csv"
        eval_result.to_csv(eval_csv_path)
    return train_csv_path, eval_csv_path


def create_artefact_dirs(output_dir: str, random_seed : int) -> None:
    """
    Creates artefact directories if they do not already exist

    :param output_dir: the base directory
    :param random_seed: the random seed of the experiment
    :return: None
    """
    if not os.path.exists(output_dir + "/results/logs/" + str(random_seed) + "/"):
        os.makedirs(output_dir + "/results/logs/" + str(random_seed) + "/")
    if not os.path.exists(output_dir + "/results/plots/" + str(random_seed) + "/"):
        os.makedirs(output_dir + "/results/plots/" + str(random_seed) + "/")
    if not os.path.exists(output_dir + "/results/data/" + str(random_seed) + "/"):
        os.makedirs(output_dir + "/results/data/" + str(random_seed) + "/")
    if not os.path.exists(output_dir + "/results/hyperparameters/" + str(random_seed) + "/"):
        os.makedirs(output_dir + "/results/hyperparameters/" + str(random_seed) + "/")
    if not os.path.exists(output_dir + "/results/gifs/" + str(random_seed) + "/"):
        os.makedirs(output_dir + "/results/gifs/" + str(random_seed) + "/")
    if not os.path.exists(output_dir + "/results/tensorboard/" + str(random_seed) + "/"):
        os.makedirs(output_dir + "/results/tensorboard/" + str(random_seed) + "/")
    if not os.path.exists(output_dir + "/results/env_data/" + str(random_seed) + "/"):
        os.makedirs(output_dir + "/results/env_data/" + str(random_seed) + "/")



def setup_logger(name: str, logdir: str, time_str = None):
    """
    Configures the logger for writing log-data of experiments

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
    fh = logging.FileHandler(logdir + "/" + time_str + "_" + name + ".log", mode="w")
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    return logger


def write_config_file(config: ClientConfig, path: str) -> None:
    """
    Writes a config object to a config file

    :param config: the config to write
    :param path: the path to write the file
    :return: None
    """
    json_str = json.dumps(json.loads(jsonpickle.encode(config)), indent=4, sort_keys=True)
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(json_str)


def read_config(config_path) -> ClientConfig:
    """
    Reads configuration of the experiment from a json file

    :param config_path: the path to the configuration file
    :return: the configuration
    """
    with io.open(config_path, 'r', encoding='utf-8') as f:
        json_str = f.read()
    client_config: ClientConfig = jsonpickle.decode(json_str)
    return client_config


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
    args = parser.parse_args()
    return args


def get_script_path():
    """
    :return: the script path
    """
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def default_output_dir() -> str:
    """
    :return: the default output dir
    """
    script_dir = get_script_path()
    return script_dir


def default_config_path() -> str:
    """
    :return: the default path to configuration file
    """
    config_path = os.path.join(default_output_dir(), './config.json')
    return config_path