import random
from csle_common.dao.emulation_config.vulnerabilities_config import VulnerabilitiesConfig
from csle_common.dao.emulation_config.node_flags_config import NodeFlagsConfig
from csle_common.dao.emulation_config.flags_config import FlagsConfig
from csle_common.dao.emulation_config.vulnerability_type import VulnType
from csle_common.util.experiment_util import ExperimentUtil
from csle_common.dao.emulation_config.flag import Flag
from csle_common.domain_randomization.vuln_generator import VulnerabilityGenerator
from csle_common.domain_randomization.topology_generator import TopologyGenerator
import csle_common.constants.constants as constants


class FlagsGenerator:
    """
    A Utility Class for generating flag configuration files
    """

    @staticmethod
    def generate(vuln_cfg: VulnerabilitiesConfig, num_flags) -> FlagsConfig:
        """
        Generates a flag configuration according to a specific vulnerabilities config and number of flags

        :param vuln_cfg: the vulnerabilities config
        :param num_flags: the number of flags
        :return: The created flags configuration
        """
        vulnerabilities = vuln_cfg.node_vulnerability_configs
        random.shuffle(vulnerabilities)
        flag_cfgs = []

        if num_flags > len(vulnerabilities):
            raise AssertionError("Too few vulnerable nodes")

        for i in range(num_flags):
            if vulnerabilities[i].vuln_type == VulnType.WEAK_PW:
                flag_dirs = [constants.COMMANDS.SLASH_DELIM + constants.COMMANDS.TMP_DIR +
                             constants.COMMANDS.SLASH_DELIM]
                for cred in vulnerabilities[i].credentials:
                    flag_dirs.append(constants.COMMANDS.SLASH_DELIM + constants.COMMANDS.HOME_DIR +
                                     constants.COMMANDS.SLASH_DELIM + cred.username +
                                     constants.COMMANDS.SLASH_DELIM)
            else:
                flag_dirs = [constants.COMMANDS.SLASH_DELIM + constants.COMMANDS.TMP_DIR +
                             constants.COMMANDS.SLASH_DELIM]
            dir_idx = random.randint(0, len(flag_dirs)-1)
            flag_dir = flag_dirs[dir_idx]
            flag_name = "flag" + str(i)
            filename = flag_name + constants.FILE_PATTERNS.TXT_FILE_SUFFIX
            flags = [Flag(name=flag_name, dir=flag_dir, id=i, path=flag_dir+filename,
                          requires_root=True, score=1)]
            flag_cfg = NodeFlagsConfig(ip=vulnerabilities[i].ip, flags=flags)
            flag_cfgs.append(flag_cfg)

        fl_cfg = FlagsConfig(node_flag_configs= flag_cfgs)

        return fl_cfg
