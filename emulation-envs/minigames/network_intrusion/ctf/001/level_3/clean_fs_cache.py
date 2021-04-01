from gym_pycr_ctf.util.experiments_util import util
from gym_pycr_ctf.envs_model.config.generator.generator_util import GeneratorUtil

if __name__ == '__main__':
    containers_config = util.read_containers_config(util.default_containers_path())
    GeneratorUtil.clean_filesystem_cache(containers_config=containers_config)

