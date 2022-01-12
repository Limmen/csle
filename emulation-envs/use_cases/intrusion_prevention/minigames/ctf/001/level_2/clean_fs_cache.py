from pycr_common.util.experiments_util import util
from pycr_common.envs_model.config.generator.generator_util import GeneratorUtil

# Cleans the file-system cache in the emulation
if __name__ == '__main__':
    containers_config = util.read_containers_config(util.default_containers_path())
    GeneratorUtil.clean_filesystem_cache(containers_config=containers_config)

