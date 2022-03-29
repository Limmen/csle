from typing import Union
from csle_common.dao.emulation_config.container_network import ContainerNetwork


class DefaultNetworkFirewallConfig:
    """
    DTO representing a default firewall configuration
    """

    def __init__(self, ip: Union[str, None], default_gw: Union[str, None], default_input: str, default_output: str,
                 default_forward: str, network: ContainerNetwork):
        """
        Initialzies the DTO

        :param ip: the ip associated to the network
        :param default_gw: the default gateway for the network
        :param default_input: the default input policy for the network
        :param default_output: the default output policy for the network
        :param default_forward: the default forward policy for the network
        :param network: the network configuraiton
        """
        self.ip = ip
        self.default_gw = default_gw
        self.default_input = default_input
        self.default_output = default_output
        self.default_forward = default_forward
        self.network = network

    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["ip"] = self.ip
        d["default_gw"] = self.default_gw
        d["default_input"] = self.default_input
        d["default_output"] = self.default_output
        d["default_forward"] = self.default_forward
        d["network"] = self.network
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"ip:{self.ip}, default_gw:{self.default_gw}, default_input:{self.default_input}, " \
               f"default_output:{self.default_output}, default_forward:{self.default_forward}, network:{self.network}"
