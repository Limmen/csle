from typing import Union, Dict, Any
from csle_common.dao.emulation_config.container_network import ContainerNetwork
from csle_common.util.general_util import GeneralUtil


class DefaultNetworkFirewallConfig:
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
        :return: a dict representation of the object
        """
        d = {}
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

    def to_json_str(self) -> str:
        """
        Converts the DTO into a json string

        :return: the json string representation of the DTO
        """
        import json
        json_str = json.dumps(self.to_dict(), indent=4, sort_keys=True)
        return json_str

    def to_json_file(self, json_file_path: str) -> None:
        """
        Saves the DTO to a json file

        :param json_file_path: the json file path to save  the DTO to
        :return: None
        """
        import io
        json_str = self.to_json_str()
        with io.open(json_file_path, 'w', encoding='utf-8') as f:
            f.write(json_str)

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
