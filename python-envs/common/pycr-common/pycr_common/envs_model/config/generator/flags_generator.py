import random
from pycr_common.dao.container_config.vulnerabilities_config import VulnerabilitiesConfig
from pycr_common.dao.container_config.node_flags_config import NodeFlagsConfig
from pycr_common.dao.container_config.flags_config import FlagsConfig
from pycr_common.dao.container_config.vulnerability_type import VulnType
from pycr_common.util.experiments_util import util
from pycr_common.dao.network.emulation_config import EmulationConfig
from pycr_common.envs_model.logic.emulation.util.common.emulation_util import EmulationUtil
from pycr_common.envs_model.config.generator.generator_util import GeneratorUtil

class FlagsGenerator:


    @staticmethod
    def generate(vuln_cfg: VulnerabilitiesConfig, num_flags) -> FlagsConfig:
        vulnerabilities = vuln_cfg.vulnerabilities
        random.shuffle(vulnerabilities)
        flag_cfgs = []

        if num_flags > len(vulnerabilities):
            raise AssertionError("Too few vulnerable nodes")

        for i in range(num_flags):
            if vulnerabilities[i].vuln_type == VulnType.WEAK_PW:
                flag_dirs = ["/tmp/", "/home/" + vulnerabilities[i].username + "/"]
            else:
                flag_dirs = ["/tmp/"]
            dir_idx = random.randint(0, len(flag_dirs)-1)
            flag_dir = flag_dirs[dir_idx]
            flag_name = "flag" + str(i)
            filename = flag_name + ".txt"
            flags = [(flag_dir + filename, flag_name, flag_dir, i, True, 1)]
            flag_cfg = NodeFlagsConfig(ip=vulnerabilities[i].node_ip, flags=flags)
            flag_cfgs.append(flag_cfg)

        fl_cfg = FlagsConfig(flags = flag_cfgs)

        return fl_cfg

    @staticmethod
    def create_flags(flags_config: FlagsConfig, emulation_config: EmulationConfig):
        for flags_conf in flags_config.flags:
            GeneratorUtil.connect_admin(emulation_config=emulation_config, ip=flags_conf.ip)

            for flag in flags_conf.flags:
                path, content, dir, id, requires_root, score = flag
                cmd = "sudo rm -rf {}".format(path)
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
                cmd = "sudo touch {}".format(path)
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
                cmd = "echo '{}' >> {}".format(content, path)
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

            GeneratorUtil.disconnect_admin(emulation_config=emulation_config)


    @staticmethod
    def write_flags_config(flags_config: FlagsConfig, path: str = None) -> None:
        """
        Writes the default configuration to a json file

        :param path: the path to write the configuration to
        :return: None
        """
        path = util.default_flags_path(out_dir=path)
        util.write_flags_config_file(flags_config, path)

