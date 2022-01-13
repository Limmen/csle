from csle_common.util.experiments_util import util
from csle_common.envs_model.config.generator.generator_util import GeneratorUtil

# Uploads a file system cache to the emulation
if __name__ == '__main__':
    containers_config = util.read_containers_config(util.default_containers_path())
    GeneratorUtil.upload_and_unzip_filesystem_cache(containers_config)

