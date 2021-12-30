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
import random
import scipy.stats
from pycr_common.dao.experiment.client_config import ClientConfig
from pycr_common.dao.experiment.runner_mode import RunnerMode
from pycr_common.dao.container_config.topology import Topology
from pycr_common.dao.container_config.users_config import UsersConfig
from pycr_common.dao.container_config.flags_config import FlagsConfig
from pycr_common.dao.container_config.vulnerabilities_config import VulnerabilitiesConfig
from pycr_common.dao.container_config.containers_config import ContainersConfig
from pycr_common.dao.container_config.traffic_config import TrafficConfig
import pycr_common.constants.constants as constants


def get_subdir(output_dir: str, results_dir: str, subdir: str, seed: int) -> str:
    """
    Utility function to construct the subdir string from a given results dir, subdir, and random seed

    :param output_dir: the base output directory
    :param results_dir: the base results dir
    :param subdir: the subdirectory (e.g. logs, data, tensorboard, etc)
    :param seed: the random seed
    :return: the directory path
    """
    return output_dir + constants.COMMANDS.SLASH_DELIM + results_dir + constants.COMMANDS.SLASH_DELIM + subdir \
           + constants.COMMANDS.SLASH_DELIM + str(seed) + constants.COMMANDS.SLASH_DELIM


def run_experiment(config: ClientConfig, random_seed: int, title :str = "v0") -> Tuple[str, str]:
    """
    Runs an individual experiment

    :param config: the config of the experiment
    :param random_seed: random seed
    :param title: title of the experiment
    :return: train_csv_path, eval_csv_path
    """
    from gym_pycr_ctf.runner.runner import Runner
    time_str = str(time.time())
    create_artifact_dirs(config.output_dir, random_seed)

    # Setup experiment logger
    logger = setup_experiment_logger(title, get_subdir(config.output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                       constants.EXPERIMENT.LOG_DIR, random_seed),
                                     time_str=time_str)

    # Setup experiment directories
    if config.attacker_agent_config is not None:
        config.attacker_agent_config.save_dir = get_subdir(config.output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                       constants.EXPERIMENT.DATA_DIR, random_seed)
        config.attacker_agent_config.video_dir = get_subdir(config.output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                       constants.EXPERIMENT.VIDEOS_DIR, random_seed)
        config.attacker_agent_config.gif_dir = get_subdir(config.output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                       constants.EXPERIMENT.GIFS_DIR, random_seed)
        config.attacker_agent_config.tensorboard_dir = get_subdir(config.output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                       constants.EXPERIMENT.TENSORBOARD_DIR, random_seed)
        config.env_checkpoint_dir = get_subdir(config.output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                       constants.EXPERIMENT.ENV_DATA_DIR, random_seed)
        config.attacker_agent_config.logger = logger
        config.attacker_agent_config.random_seed = random_seed
        config.attacker_agent_config.to_csv(
            config.output_dir + get_subdir(config.output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                       constants.EXPERIMENT.HYPERPARAMETERS_DIR, random_seed)
            + time_str + constants.FILE_PATTERNS.CSV_SUFFIX)

    if config.simulation_config is not None:
        config.simulation_config.gif_dir = get_subdir(config.output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                       constants.EXPERIMENT.GIFS_DIR, random_seed)
        config.simulation_config.video_dir = get_subdir(config.output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                       constants.EXPERIMENT.VIDEOS_DIR, random_seed)


    config.logger = logger
    config.random_seed = random_seed
    train_csv_path = ""
    eval_csv_path = ""
    if config.mode == RunnerMode.TRAIN_ATTACKER.value or config.mode == RunnerMode.TRAIN_DEFENDER.value \
            or config.mode == RunnerMode.SIMULATE.value:
        train_result, eval_result = Runner.run(config)
        if len(train_result.avg_episode_steps) > 0:
            train_csv_path = get_subdir(config.output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                       constants.EXPERIMENT.DATA_DIR, random_seed) \
                             + time_str + "_train" + constants.FILE_PATTERNS.CSV_SUFFIX
            train_result.to_csv(train_csv_path)
        if len(eval_result.avg_episode_steps) > 0:
            eval_csv_path = get_subdir(config.output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                       constants.EXPERIMENT.DATA_DIR, random_seed) \
                            + time_str + "_eval" + constants.FILE_PATTERNS.CSV_SUFFIX
            eval_result.to_csv(eval_csv_path)
        return train_csv_path, eval_csv_path
    else:
        Runner.run(config)


def create_artifact_dirs(output_dir: str, random_seed : int) -> None:
    """
    Creates artifact directories if they do not already exist

    :param output_dir: the base directory
    :param random_seed: the random seed of the experiment
    :return: None
    """
    if not os.path.exists(get_subdir(output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                       constants.EXPERIMENT.LOG_DIR, random_seed)):
        os.makedirs(get_subdir(output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                       constants.EXPERIMENT.LOG_DIR, random_seed))
    if not os.path.exists(get_subdir(output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                       constants.EXPERIMENT.PLOTS_DIR, random_seed)):
        os.makedirs(get_subdir(output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                       constants.EXPERIMENT.PLOTS_DIR, random_seed))
    if not os.path.exists(get_subdir(output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                       constants.EXPERIMENT.DATA_DIR, random_seed)):
        os.makedirs(get_subdir(output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                       constants.EXPERIMENT.DATA_DIR, random_seed))
    if not os.path.exists(get_subdir(output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                       constants.EXPERIMENT.HYPERPARAMETERS_DIR, random_seed)):
        os.makedirs(get_subdir(output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                       constants.EXPERIMENT.HYPERPARAMETERS_DIR, random_seed))
    if not os.path.exists(get_subdir(output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                       constants.EXPERIMENT.GIFS_DIR, random_seed)):
        os.makedirs(get_subdir(output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                       constants.EXPERIMENT.GIFS_DIR, random_seed))
    if not os.path.exists(get_subdir(output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                       constants.EXPERIMENT.TENSORBOARD_DIR, random_seed)):
        os.makedirs(get_subdir(output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                       constants.EXPERIMENT.TENSORBOARD_DIR, random_seed))
    if not os.path.exists(get_subdir(output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                       constants.EXPERIMENT.ENV_DATA_DIR, random_seed)):
        os.makedirs(get_subdir(output_dir, constants.EXPERIMENT.RESULTS_DIR,
                                                       constants.EXPERIMENT.ENV_DATA_DIR, random_seed))


def setup_experiment_logger(name: str, logdir: str, time_str = None):
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
    fh = logging.FileHandler(logdir + constants.COMMANDS.SLASH_DELIM + time_str + constants.COMMANDS.UNDERSCORE_DELIM
                             + name + constants.FILE_PATTERNS.LOG_SUFFIX, mode="w")
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

    :param containers_cfg: the containers_cfg obj to write
    :param path: the path to write the file
    :return: None
    """
    json_str = json.dumps(json.loads(jsonpickle.encode(containers_cfg)), indent=4, sort_keys=True)
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(json_str)


def write_traffic_config_file(traffic_cfg: TrafficConfig, path: str) -> None:
    """
    Writes a traffic config object to a config file

    :param traffic_cfg: the traffic_cfg obj to write
    :param path: the path to write the file
    :return: None
    """
    json_str = json.dumps(json.loads(jsonpickle.encode(traffic_cfg)), indent=4, sort_keys=True)
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


def read_containers_config(containers_config_path) -> ContainersConfig:
    """
    Reads containers_config of the experiment from a json file

    :param containers_config_path: the path to the containers_config file
    :return: the configuration
    """
    with io.open(containers_config_path, 'r', encoding='utf-8') as f:
        json_str = f.read()
    containers_cfg: ContainersConfig = jsonpickle.decode(json_str)
    return containers_cfg


def read_traffic_config(traffic_config_path) -> TrafficConfig:
    """
    Reads containers_config of the experiment from a json file

    :param containers_config_path: the path to the traffic_config file
    :return: the configuration
    """
    with io.open(traffic_config_path, 'r', encoding='utf-8') as f:
        json_str = f.read()
    traffic_cfg: TrafficConfig = jsonpickle.decode(json_str)
    return traffic_cfg


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
        config_path = os.path.join(default_output_dir(), constants.COMMANDS.DOT_DELIM +
                                   constants.EXPERIMENT.CONFIG_FILE_PATH)
    else:
        config_path = os.path.join(out_dir, constants.COMMANDS.DOT_DELIM + constants.EXPERIMENT.CONFIG_FILE_PATH)
    return config_path


def default_topology_path(out_dir : str = None) -> str:
    """
    :param out_dir: directory to write
    :return: the default path to topology file
    """
    if out_dir is None:
        config_path = os.path.join(default_output_dir(), constants.COMMANDS.DOT_DELIM
                                   + constants.DOCKER.CONTAINER_CONFIG_TOPOLOGY_CFG_PATH)
    else:
        config_path = os.path.join(out_dir, constants.COMMANDS.DOT_DELIM
                                   + constants.DOCKER.CONTAINER_CONFIG_TOPOLOGY_CFG_PATH)
    return config_path


def default_users_path(out_dir : str = None) -> str:
    """
    :param out_dir: directory to write
    :return: the default path to users file
    """
    if out_dir is None:
        config_path = os.path.join(default_output_dir(), constants.COMMANDS.DOT_DELIM
                                   + constants.DOCKER.CONTAINER_CONFIG_USERS_CFG_PATH)
    else:
        config_path = os.path.join(out_dir, constants.COMMANDS.DOT_DELIM
                                   + constants.DOCKER.CONTAINER_CONFIG_USERS_CFG_PATH)
    return config_path


def default_flags_path(out_dir : str = None) -> str:
    """
    :param out_dir: directory to write
    :return: the default path to flags file
    """
    if out_dir is None:
        config_path = os.path.join(default_output_dir(), constants.COMMANDS.DOT_DELIM
                                   + constants.DOCKER.CONTAINER_CONFIG_FLAGS_CFG_PATH)
    else:
        config_path = os.path.join(out_dir, constants.COMMANDS.DOT_DELIM
                                   + constants.DOCKER.CONTAINER_CONFIG_FLAGS_CFG_PATH)
    return config_path


def default_vulnerabilities_path(out_dir : str = None) -> str:
    """
    :param out_dir: directory to write
    :return: the default path to vuln file
    """
    if out_dir is None:
        config_path = os.path.join(default_output_dir(), constants.COMMANDS.DOT_DELIM
                                   + constants.DOCKER.CONTAINER_CONFIG_VULNERABILITIES_CFG_PATH)
    else:
        config_path = os.path.join(out_dir, constants.COMMANDS.DOT_DELIM
                                   + constants.DOCKER.CONTAINER_CONFIG_VULNERABILITIES_CFG_PATH)
    return config_path


def default_containers_path(out_dir : str = None) -> str:
    """
    :param out_dir: directory to write
    :return: the default path to containers config file
    """
    if out_dir is None:
        config_path = os.path.join(default_output_dir(), constants.COMMANDS.DOT_DELIM
                                   + constants.DOCKER.CONTAINER_CONFIG_CFG_PATH)
    else:
        config_path = os.path.join(out_dir, constants.COMMANDS.DOT_DELIM
                                   + constants.DOCKER.CONTAINER_CONFIG_CFG_PATH)
    return config_path

def default_traffic_path(out_dir : str = None) -> str:
    """
    :param out_dir: directory to write
    :return: the default path to traffic config file
    """
    if out_dir is None:
        config_path = os.path.join(default_output_dir(), constants.COMMANDS.DOT_DELIM
                                   + constants.DOCKER.CONTAINER_CONFIG_TRAFFIC_CFG_PATH)
    else:
        config_path = os.path.join(out_dir, constants.COMMANDS.DOT_DELIM
                                   + constants.DOCKER.CONTAINER_CONFIG_TRAFFIC_CFG_PATH)
    return config_path


def default_containers_folders_path(out_dir : str = None) -> str:
    """
    :param out_dir: directory to write
    :return: the default path to container folders
    """
    if out_dir is None:
        config_path = os.path.join(default_output_dir(), constants.COMMANDS.DOT_DELIM
                                   + constants.COMMANDS.SLASH_DELIM
                                   + constants.DOCKER.CONTAINERS_DIR)
    else:
        config_path = os.path.join(out_dir, constants.DOCKER.CONTAINERS_DIR)
    return config_path


def default_container_makefile_template_path(out_dir : str = None) -> str:
    """
    :param out_dir: directory to write
    :return: the default path to makefile tempalte
    """
    if out_dir is None:
        config_path = os.path.join(default_output_dir(), constants.COMMANDS.DOT_DELIM
                                   + constants.COMMANDS.SLASH_DELIM +
                                   constants.DOCKER.CONTAINER_MAKEFILE_TEMPLATE)
    else:
        config_path = os.path.join(out_dir, constants.DOCKER.CONTAINER_MAKEFILE_TEMPLATE)
    return config_path


def default_makefile_template_path(out_dir : str = None) -> str:
    """
    :param out_dir: directory to write
    :return: the default path to makefile tempalte
    """
    if out_dir is None:
        config_path = os.path.join(default_output_dir(), constants.COMMANDS.DOT_DELIM
                                   + constants.COMMANDS.SLASH_DELIM
                                   + constants.DOCKER.MAKEFILE_TEMPLATE)
    else:
        config_path = os.path.join(out_dir, constants.COMMANDS.DOT_DELIM
                                   + constants.COMMANDS.SLASH_DELIM + constants.DOCKER.MAKEFILE_TEMPLATE)
    return config_path


def default_makefile_path(out_dir : str = None) -> str:
    """
    :param out_dir: directory to write
    :return: the default path to makefile tempalte
    """
    if out_dir is None:
        config_path = os.path.join(default_output_dir(), constants.COMMANDS.DOT_DELIM
                                   + constants.COMMANDS.SLASH_DELIM +
                                   constants.DOCKER.Makefile)
    else:
        config_path = os.path.join(out_dir, constants.COMMANDS.DOT_DELIM
                                   + constants.COMMANDS.SLASH_DELIM + constants.DOCKER.MAKEFILE)
    return config_path


def round_batch_size(x: int) -> int:
    """
    Round of batch size

    :param x: the batch size
    :return: the rounded batch size
    """
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


def add(x):
    x_prime = []
    random_vec = x[0:10]
    for i in range(len(x)):
        if i < 30:
            for j in range(2):
                idx = random.randint(max(0,i-3),i+1)
                x_prime.append(x[idx])
                # else:
                #     x_prime.append(x[i])
        else:
            x_prime.append(x[i])
    return x_prime


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
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, h