from typing import List


class NodeTrafficConfig:
    """
    A DTO object representing the traffic configuration of an individual container in an emulatio
    """

    def __init__(self, ip: str, commands: List[str], jumphosts: List[str], target_hosts: List[str],
                 client: bool = False):
        """
        Creates a NodeTrafficConfig DTO Object

        :param ip: the ip of the node that generate the traffic
        :param commands: the commands used to generate the traffic
        :param jumphosts: the jumphosts used (optional)
        :param target_hosts: the targets of the traffic
        :param client: whether it is an external client or internal node
        """
        self.ip = ip
        self.commands = commands
        self.jumphosts = jumphosts
        self.target_hosts = target_hosts
        self.client = client

    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["ip"] = self.ip
        d["commands"] = self.commands
        d["jumphosts"] = self.jumphosts
        d["target_hosts"] = self.target_hosts
        d["client"] = self.client
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "ip:{}, commands:{}, jumphosts:{}, target_hosts:{}, client:{}".format(
            self.ip, self.commands, self.jumphosts, self.target_hosts, self.client)