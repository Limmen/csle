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
import numpy as np
from gym_pycr_ctf.dao.experiment.client_config import ClientConfig
from gym_pycr_ctf.dao.experiment.runner_mode import RunnerMode
from gym_pycr_ctf.dao.container_config.topology import Topology
from gym_pycr_ctf.dao.container_config.users_config import UsersConfig
from gym_pycr_ctf.dao.container_config.flags_config import FlagsConfig
from gym_pycr_ctf.dao.container_config.vulnerabilities_config import VulnerabilitiesConfig
from gym_pycr_ctf.dao.container_config.containers_config import ContainersConfig

def run_experiment(config: ClientConfig, random_seed: int, title :str = "v0") -> Tuple[str, str]:
    """
    Runs an inidividual experiment

    :param config: the config of the experiment
    :param random_seed: random seed
    :param title: title of the experiment
    :return: train_csv_path, eval_csv_path
    """
    from gym_pycr_ctf.runner.runner import Runner
    time_str = str(time.time())
    create_artefact_dirs(config.output_dir, random_seed)
    logger = setup_logger(title, config.output_dir + "/results/logs/" +
                               str(random_seed) + "/",
                               time_str=time_str)
    if config.agent_config is not None:
        config.agent_config.save_dir = default_output_dir() + "/results/data/" + str(random_seed) + "/"
        config.agent_config.video_dir = default_output_dir() + "/results/videos/" + str(random_seed) + "/"
        config.agent_config.gif_dir = default_output_dir() + "/results/gifs/" + str(random_seed) + "/"
        config.agent_config.tensorboard_dir = default_output_dir() + "/results/tensorboard/" \
                                                 + str(random_seed) + "/"
        config.env_checkpoint_dir = default_output_dir() + "/results/env_data/" + str(random_seed) + "/"
        config.agent_config.logger = logger
        config.agent_config.random_seed = random_seed
        config.agent_config.to_csv(
            config.output_dir + "/results/hyperparameters/" + str(random_seed) + "/" + time_str + ".csv")

    if config.simulation_config is not None:
        config.simulation_config.gif_dir = default_output_dir() + "/results/gifs/" + str(random_seed) + "/"
        config.simulation_config.video_dir = default_output_dir() + "/results/videos/" + str(random_seed) + "/"


    config.logger = logger
    config.random_seed = random_seed
    train_csv_path = ""
    eval_csv_path = ""
    if config.mode == RunnerMode.TRAIN_ATTACKER.value or config.mode == RunnerMode.SIMULATE.value:
        train_result, eval_result = Runner.run(config)
        if len(train_result.avg_episode_steps) > 0:
            train_csv_path = config.output_dir + "/results/data/" + str(random_seed) + "/" + time_str + "_train" + ".csv"
            train_result.to_csv(train_csv_path)
        if len(eval_result.avg_episode_steps) > 0:
            eval_csv_path = config.output_dir + "/results/data/" + str(random_seed) + "/" + time_str + "_eval" + ".csv"
            eval_result.to_csv(eval_csv_path)
        return train_csv_path, eval_csv_path
    else:
        Runner.run(config)


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


def write_topology_file(topology: Topology, path: str) -> None:
    """
    Writes a config object to a config file

    :param topology: the topology to write
    :param path: the path to write the file
    :return: None
    """
    json_str = json.dumps(json.loads(jsonpickle.encode(topology)), indent=4, sort_keys=True)
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(json_str)

def write_users_config_file(users_config: UsersConfig, path: str) -> None:
    """
    Writes a config object to a config file

    :param users_config: the users_config obj to write
    :param path: the path to write the file
    :return: None
    """
    json_str = json.dumps(json.loads(jsonpickle.encode(users_config)), indent=4, sort_keys=True)
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(json_str)

def write_flags_config_file(flags_config: FlagsConfig, path: str) -> None:
    """
    Writes a config object to a config file

    :param flags_config: the flags_config obj to write
    :param path: the path to write the file
    :return: None
    """
    json_str = json.dumps(json.loads(jsonpickle.encode(flags_config)), indent=4, sort_keys=True)
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(json_str)


def write_vulns_config_file(vulns_cfg: VulnerabilitiesConfig, path: str) -> None:
    """
    Writes a config object to a config file

    :param vulns_cfg: the vulns_cfg obj to write
    :param path: the path to write the file
    :return: None
    """
    json_str = json.dumps(json.loads(jsonpickle.encode(vulns_cfg)), indent=4, sort_keys=True)
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(json_str)


def write_containers_config_file(containers_cfg: ContainersConfig, path: str) -> None:
    """
    Writes a config object to a config file

    :param containers_cfg: the vulns_cfg obj to write
    :param path: the path to write the file
    :return: None
    """
    json_str = json.dumps(json.loads(jsonpickle.encode(containers_cfg)), indent=4, sort_keys=True)
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

def read_topology(topology_path) -> Topology:
    """
    Reads topology of the experiment from a json file

    :param topology_path: the path to the topology file
    :return: the configuration
    """
    with io.open(topology_path, 'r', encoding='utf-8') as f:
        json_str = f.read()
    topology: Topology = jsonpickle.decode(json_str)
    return topology


def read_users_config(users_config_path) -> UsersConfig:
    """
    Reads users_config of the experiment from a json file

    :param users_config_path: the path to the users_config file
    :return: the configuration
    """
    with io.open(users_config_path, 'r', encoding='utf-8') as f:
        json_str = f.read()
    users_config: UsersConfig = jsonpickle.decode(json_str)
    return users_config

def read_flags_config(flags_config_path) -> FlagsConfig:
    """
    Reads flags_config of the experiment from a json file

    :param flags_config_path: the path to the users_config file
    :return: the configuration
    """
    with io.open(flags_config_path, 'r', encoding='utf-8') as f:
        json_str = f.read()
    flags_config: FlagsConfig = jsonpickle.decode(json_str)
    return flags_config


def read_vulns_config(vulns_config_path) -> VulnerabilitiesConfig:
    """
    Reads vulns_config of the experiment from a json file

    :param vulns_config_path: the path to the vulns_config file
    :return: the configuration
    """
    with io.open(vulns_config_path, 'r', encoding='utf-8') as f:
        json_str = f.read()
    vulns_cfg: VulnerabilitiesConfig = jsonpickle.decode(json_str)
    return vulns_cfg


def read_containers_config(containers_config_path) -> VulnerabilitiesConfig:
    """
    Reads containers_config of the experiment from a json file

    :param containers_config_path: the path to the vulns_config file
    :return: the configuration
    """
    with io.open(containers_config_path, 'r', encoding='utf-8') as f:
        json_str = f.read()
    containers_cfg: ContainersConfig = jsonpickle.decode(json_str)
    return containers_cfg


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
    parser.add_argument("-rd", "--resultdirs", help="List of comma-separated result dirs to combine for plotting", type=str)
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


def default_config_path(out_dir : str = None) -> str:
    """
    :param out_dir: directory to write
    :return: the default path to configuration file
    """
    if out_dir is None:
        config_path = os.path.join(default_output_dir(), './config.json')
    else:
        config_path = os.path.join(out_dir, './config.json')
    return config_path

def default_topology_path(out_dir : str = None) -> str:
    """
    :param out_dir: directory to write
    :return: the default path to topology file
    """
    if out_dir is None:
        config_path = os.path.join(default_output_dir(), './topology.json')
    else:
        config_path = os.path.join(out_dir, './topology.json')
    return config_path

def default_users_path(out_dir : str = None) -> str:
    """
    :param out_dir: directory to write
    :return: the default path to users file
    """
    if out_dir is None:
        config_path = os.path.join(default_output_dir(), './users.json')
    else:
        config_path = os.path.join(out_dir, './users.json')
    return config_path

def default_flags_path(out_dir : str = None) -> str:
    """
    :param out_dir: directory to write
    :return: the default path to flags file
    """
    if out_dir is None:
        config_path = os.path.join(default_output_dir(), './flags.json')
    else:
        config_path = os.path.join(out_dir, './flags.json')
    return config_path

def default_vulnerabilities_path(out_dir : str = None) -> str:
    """
    :param out_dir: directory to write
    :return: the default path to vuln file
    """
    if out_dir is None:
        config_path = os.path.join(default_output_dir(), './vulnerabilities.json')
    else:
        config_path = os.path.join(out_dir, './vulnerabilities.json')
    return config_path

def default_containers_path(out_dir : str = None) -> str:
    """
    :param out_dir: directory to write
    :return: the default path to containers config file
    """
    if out_dir is None:
        config_path = os.path.join(default_output_dir(), './containers.json')
    else:
        config_path = os.path.join(out_dir, './containers.json')
    return config_path

def default_containers_folders_path(out_dir : str = None) -> str:
    """
    :param out_dir: directory to write
    :return: the default path to container folders
    """
    if out_dir is None:
        config_path = os.path.join(default_output_dir(), './containers')
    else:
        config_path = os.path.join(out_dir, 'containers')
    return config_path

def default_container_makefile_template_path(out_dir : str = None) -> str:
    """
    :param out_dir: directory to write
    :return: the default path to makefile tempalte
    """
    if out_dir is None:
        config_path = os.path.join(default_output_dir(), './Container_Makefile_template')
    else:
        config_path = os.path.join(out_dir, 'Container_Makefile_template')
    return config_path

def default_makefile_template_path(out_dir : str = None) -> str:
    """
    :param out_dir: directory to write
    :return: the default path to makefile tempalte
    """
    if out_dir is None:
        config_path = os.path.join(default_output_dir(), './Makefile_template')
    else:
        config_path = os.path.join(out_dir, './Makefile_template')
    return config_path

def default_makefile_path(out_dir : str = None) -> str:
    """
    :param out_dir: directory to write
    :return: the default path to makefile tempalte
    """
    if out_dir is None:
        config_path = os.path.join(default_output_dir(), './Makefile')
    else:
        config_path = os.path.join(out_dir, './Makefile')
    return config_path

def round_batch_size(x: int):
    return x if x % 100 == 0 else x + 100 - x%100


def running_average(x, N):
    ''' Function used to compute the running average
        of the last N elements of a vector x
    '''
    if len(x) >= N:
        y = np.copy(x)
        y[N-1:] = np.convolve(x, np.ones((N, )) / N, mode='valid')
    else:
        y = np.zeros_like(x)
    return y

def running_average(x, N):
    ''' Function used to compute the running average
        of the last N elements of a vector x
    '''
    if len(x) >= N:
        y = np.copy(x)
        y[N-1:] = np.convolve(x, np.ones((N, )) / N, mode='valid')
    else:
        y = [x[-1]]
    return y[-1]

def running_average_list(x, N):
    ''' Function used to compute the running average
        of the last N elements of a vector x
    '''
    if len(x) >= N:
        y = np.copy(x)
        y[N-1:] = np.convolve(x, np.ones((N, )) / N, mode='valid')
    else:
        y = np.zeros_like(x)
    return y