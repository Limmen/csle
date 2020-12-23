from gym_pycr_pwcrack.util.experiments_util import util
from gym_pycr_pwcrack.envs.config.generator.generator_util import GeneratorUtil

if __name__ == '__main__':
    containers_config = util.read_containers_config(util.default_containers_path())
    GeneratorUtil.zip_and_download_filesystem_cache(containers_config)

