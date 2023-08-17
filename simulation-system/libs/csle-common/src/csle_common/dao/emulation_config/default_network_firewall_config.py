from typing import Union, Dict, Any
from csle_common.dao.emulation_config.container_network import ContainerNetwork
from csle_common.util.general_util import GeneralUtil
from csle_base.json_serializable import JSONSerializable


class DefaultNetworkFirewallConfig(JSONSerializable):
    """
    DTO representing a default firewall configuration
    """

    def __init__(self, ip: Union[str, None], default_gw: Union[str, None], default_input: str, default_output: str,
                 default_forward: str, network: ContainerNetwork):
        """
        Initializes the DTO

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

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "DefaultNetworkFirewallConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = DefaultNetworkFirewallConfig(
            ip=d["ip"], default_gw=d["default_gw"], default_input=d["default_input"],
            default_output=d["default_output"], default_forward=d["default_forward"],
            network=ContainerNetwork.from_dict(d["network"]))
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["ip"] = self.ip
        d["default_gw"] = self.default_gw
        d["default_input"] = self.default_input
        d["default_output"] = self.default_output
        d["default_forward"] = self.default_forward
        d["network"] = self.network.to_dict()
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"ip:{self.ip}, default_gw:{self.default_gw}, default_input:{self.default_input}, " \
               f"default_output:{self.default_output}, default_forward:{self.default_forward}, network:{self.network}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "DefaultNetworkFirewallConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return DefaultNetworkFirewallConfig.from_dict(json.loads(json_str))

    def copy(self) -> "DefaultNetworkFirewallConfig":
        """
        :return: a copy of the DTO
        """
        return DefaultNetworkFirewallConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "DefaultNetworkFirewallConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        if config.ip is not None:
            config.ip = GeneralUtil.replace_first_octet_of_ip(ip=config.ip, ip_first_octet=ip_first_octet)
        if config.default_gw is not None:
            config.default_gw = GeneralUtil.replace_first_octet_of_ip(ip=config.default_gw,
                                                                      ip_first_octet=ip_first_octet)
        config.network = config.network.create_execution_config(ip_first_octet=ip_first_octet)
        return config

    @staticmethod
    def schema() -> "DefaultNetworkFirewallConfig":
        """
        :return: get the schema of the DTO
        """
        return DefaultNetworkFirewallConfig(ip="", default_gw="", default_input="", default_output="",
                                            default_forward="", network=ContainerNetwork.schema())
