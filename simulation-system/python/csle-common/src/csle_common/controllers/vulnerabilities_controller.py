import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.util.emulation_util import EmulationUtil
from csle_common.dao.emulation_config.vulnerability_type import VulnType
from csle_common.logging.log import Logger


class VulnerabilitiesController:
    """
    Class managing vulnerabilities in the emulation environments
    """

    @staticmethod
    def create_vulns(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Creates vulnerabilities in an emulation environment according to a specified vulnerabilities configuration

        :param emulation_env_config: the emulation environment configuration
        :return: None
        """
        vulnerabilities = emulation_env_config.vuln_config.node_vulnerability_configs
        for vuln in vulnerabilities:
            Logger.__call__().get_logger().info(f"Creating vulnerability on ip: {vuln.ip}, type: {vuln.vuln_type}")
            EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=vuln.ip)

            # Update sudoers file
            if vuln.vuln_type == VulnType.PRIVILEGE_ESCALATION:

                # Restore/Backup sudoers file
                cmd = "sudo cp /etc/sudoers.bak /etc/sudoers"
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_env_config.get_connection(ip=vuln.ip))

                # Install sudoers vulnerability
                if vuln.cve is not None and vuln.cve.lower() == constants.EXPLOIT_VULNERABILITES.CVE_2010_0426:
                    cmd = "sudo su root -c \"echo '{} ALL=NOPASSWD: sudoedit /etc/fstab' >> /etc/sudoers\""
                elif vuln.cve is not None and vuln.cve.lower() == constants.EXPLOIT_VULNERABILITES.CVE_2015_5602:
                    cmd = "sudo su root -c \"echo '{} ALL=NOPASSWD: sudoedit /home/*/*/esc.txt' >> /etc/sudoers\""
                else:
                    raise ValueError("CVE not recognized:{}".format(vuln.cve))

                for cr in vuln.credentials:
                    cmd = cmd.format(cr.username)
                    o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd,
                                                            conn=emulation_env_config.get_connection(ip=vuln.ip))
                    cmd = "sudo chmod 440 /etc/sudoers"
                    o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd,
                                                            conn=emulation_env_config.get_connection(ip=vuln.ip))
