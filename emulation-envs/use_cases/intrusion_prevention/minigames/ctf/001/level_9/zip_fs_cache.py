from pycr_common.util.experiments_util import util
from pycr_common.envs_model.config.generator.generator_util import GeneratorUtil

# Creates a zip of the filesystem cache
if __name__ == '__main__':
    containers_config = util.read_containers_config(util.default_containers_path())
    GeneratorUtil.zip_and_download_filesystem_cache(containers_config)

