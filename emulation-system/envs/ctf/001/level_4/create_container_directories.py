import os
from csle_common.envs_model.config.generator.env_config_generator import EnvConfigGenerator
from csle_common.util.experiments_util import util
import create_resource_constraints
import create_containers_config
from csle_common.envs_model.config.generator.resource_constraints_generator import ResourceConstraintsGenerator
from csle_common.envs_model.config.generator.container_generator import ContainerGenerator


# Create container directories together with startup scripts
def create_container_directories(level: int = 4, version: str = "0.0.1") -> None:
    """
    Creates the container directories and scripts

    :param level: the level parameter of the emulation
    :param version: the version of the emulation
    :return: None
    """
    network_id = level
    level = str(level)
    if not os.path.exists(util.default_containers_path()):
        containers_cfg = create_containers_config.default_containers_config(
            network_id=network_id, level=level, version=version)
        ContainerGenerator.write_containers_config(containers_cfg, path=util.default_output_dir())

    containers_config = util.read_containers_config(util.default_containers_path())

    if not os.path.exists(util.default_resources_path()):
        ResourceConstraintsGenerator.write_resources_config(
            resources_config=create_resource_constraints.default_resource_constraints(
                network_id=network_id))
    resources_config = util.read_resources_config(util.default_resources_path())

    path = util.default_containers_folders_path()
    if not os.path.exists(path):
        EnvConfigGenerator.create_container_dirs(containers_config, resources_config=resources_config,
                                                 path=util.default_output_dir(),
                                                 create_folder_makefile=False)


# Create container directories together with startup scripts
if __name__ == '__main__':
    create_container_directories(level=4, version="0.0.1")
