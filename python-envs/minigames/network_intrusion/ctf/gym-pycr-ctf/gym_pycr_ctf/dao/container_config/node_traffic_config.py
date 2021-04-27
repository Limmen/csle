from typing import List


class NodeTrafficConfig:
    """
    A DTO object representing the traffic configuration of an individual container in an emulatio
    """

    def __init__(self, ip: str, commands: List[str], jumphosts: List[str], target_hosts: List[str]):
        self.ip = ip
        self.commands = commands
        self.jumphosts = jumphosts
        self.target_hosts = target_hosts

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "ip:{}, commands:{}, jumphosts:{}, target_hosts:{}".format(
            self.ip, self.commands, self.jumphosts, self.target_hosts)