import argparse
from pycr_common.util.experiments_util import util
from pycr_common.envs_model.config.generator.env_config_generator import EnvConfigGenerator


def parse_args():
    parser = argparse.ArgumentParser(description='Parse flags for command to apply to the generated envs')
    parser.add_argument("-c", "--cmd", help="command to apply", type=str)
    args = parser.parse_args()
    return args


def execute_cmd(cmd: str):
    path = util.default_output_dir()
    EnvConfigGenerator.execute_env_cmd(path=path, cmd=cmd)


if __name__ == '__main__':
    args = parse_args()
    cmd = args.cmd
    execute_cmd(cmd=cmd)