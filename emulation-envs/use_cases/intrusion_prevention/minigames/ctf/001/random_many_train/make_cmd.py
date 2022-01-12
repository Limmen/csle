import argparse
from pycr_common.util.experiments_util import util
from pycr_common.envs_model.config.generator.env_config_generator import EnvConfigGenerator


def parse_args():
    """
    Parses the script arguments

    :return: the parsed scripted arguments
    """
    parser = argparse.ArgumentParser(description='Parse flags for command to apply to the generated envs')
    parser.add_argument("-c", "--cmd", help="command to apply", type=str)
    args = parser.parse_args()
    return args


def execute_cmd(cmd: str) -> None:
    """
    Executes a given script command

    :param cmd: the command to run
    :return:
    """
    path = util.default_output_dir()
    EnvConfigGenerator.execute_env_cmd(path=path, cmd=cmd)


# Executes a given script command
if __name__ == '__main__':
    args = parse_args()
    cmd = args.cmd
    execute_cmd(cmd=cmd)