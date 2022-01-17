import os
from csle_common.envs_model.config.generator.env_config_generator import EnvConfigGenerator
from csle_common.util.experiments_util import util


# Create container directories together with startup scripts
def create_container_directories():
    if not os.path.exists(util.default_containers_path()):
        raise ValueError(f"Could not find {util.default_containers_path()}, "
                         f"create the containers configuration file before running this script")
    containers_config = util.read_containers_config(util.default_containers_path())
    path = util.default_containers_folders_path()
    if not os.path.exists(path):
        EnvConfigGenerator.create_container_dirs(containers_config, path=util.default_output_dir(),
                                                 create_folder_makefile=False)


# Create container directories together with startup scripts
if __name__ == '__main__':
    create_container_directories()
