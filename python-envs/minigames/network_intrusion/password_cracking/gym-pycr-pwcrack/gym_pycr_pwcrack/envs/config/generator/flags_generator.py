from typing import List
import random
from gym_pycr_pwcrack.dao.container_config.vulnerability_config import VulnerabilityConfig
from gym_pycr_pwcrack.dao.container_config.node_flags_config import NodeFlagsConfig
from gym_pycr_pwcrack.dao.container_config.flags_config import FlagsConfig
from gym_pycr_pwcrack.dao.container_config.vulnerability_type import VulnType

class FlagsGenerator:


    @staticmethod
    def generate(vulnerabilities: List[VulnerabilityConfig], num_flags) -> FlagsConfig:
        random.shuffle(vulnerabilities)
        flag_cfgs = []

        if num_flags > len(vulnerabilities):
            raise AssertionError("Too few vulnerable nodes")

        for i in range(num_flags):
            if vulnerabilities[i].vuln_type == VulnType.WEAK_PW:
                flag_dirs = ["/tmp/", "/home/" + vulnerabilities[i].username]
            else:
                flag_dirs = ["/tmp"]
            dir_idx = random.randint(0, len(flag_dirs)-1)
            flag_dir = flag_dirs[dir_idx]
            flag_name = "flag" + str(i)
            filename = flag_name + ".txt"
            flags = [(flag_dir + filename, flag_name)]
            flag_cfg = NodeFlagsConfig(ip=vulnerabilities[i].node_ip, flags=flags)
            flag_cfgs.append(flag_cfg)

        fl_cfg = FlagsConfig(flags = flag_cfgs)

        return fl_cfg

