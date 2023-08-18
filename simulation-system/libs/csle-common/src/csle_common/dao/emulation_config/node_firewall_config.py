from typing import Set, List, Dict, Any, Tuple
from csle_common.dao.emulation_config.default_network_firewall_config import DefaultNetworkFirewallConfig
from csle_common.util.general_util import GeneralUtil
from csle_base.json_serializable import JSONSerializable


class NodeFirewallConfig(JSONSerializable):
    """
    A DTO object representing a firewall configuration of a container in an emulation environment
    """

    def __init__(self, ips_gw_default_policy_networks: List[DefaultNetworkFirewallConfig],
                 hostname: str, output_accept: Set[str], input_accept: Set[str],
                 forward_accept: Set[str], output_drop: Set[str], input_drop: Set[str],
                 forward_drop: Set[str], routes: Set[Tuple[str, str]], docker_gw_bridge_ip: str = "",
                 physical_host_ip: str = ""):
        """
        Initializes the DTO

        :param ips_gw_default_policy_networks: List of ip,gw,default policy, network
        :param ip: the ip of the node
        :param hostname: the hostname of the node
        :param output_accept: the list of ips to accept output
        :param input_accept: the list of ips to accept input
        :param forward_accept: the list of ips to accept forward
        :param output_drop: the list of ips to drop output
        :param input_drop: the list of ips to drop input
        :param forward_drop: the list of ips to drop forward
        :param routes: the set of custom routes for the routing table
        :param docker_gw_bridge_ip: IP to reach the container from the host network
        :param physical_host_ip: IP of the physical host where the container is running
        """
        self.ips_gw_default_policy_networks = ips_gw_default_policy_networks
        self.docker_gw_bridge_ip = docker_gw_bridge_ip
        self.hostname = hostname
        self.output_accept = output_accept
        self.input_accept = input_accept
        self.forward_accept = forward_accept
        self.output_drop = output_drop
        self.input_drop = input_drop
        self.forward_drop = forward_drop
        self.routes = routes
        self.physical_host_ip = physical_host_ip

    def get_ips(self):
        """
        :return: list of ip addresses
        """
        return list(filter(lambda x: x is not None, map(lambda x: x.ip, self.ips_gw_default_policy_networks)))

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "NodeFirewallConfig":
        """
        Converts a dict representation into an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = NodeFirewallConfig(
            hostname=d["hostname"],
            ips_gw_default_policy_networks=list(map(lambda x: DefaultNetworkFirewallConfig.from_dict(x),
                                                    d["ips_gw_default_policy_networks"])),
            output_accept=set(d["output_accept"]),
            input_accept=set(d["input_accept"]),
            forward_accept=set(d["forward_accept"]),
            output_drop=set(d["output_drop"]),
            input_drop=set(d["input_drop"]),
            forward_drop=set(d["forward_drop"]),
            routes=set(list(map(lambda x: (str(x[0]), str(x[1])), d["routes"]))),
            docker_gw_bridge_ip=d["docker_gw_bridge_ip"],
            physical_host_ip=d["physical_host_ip"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["hostname"] = self.hostname
        d["ips_gw_default_policy_networks"] = list(map(lambda x: x.to_dict(), self.ips_gw_default_policy_networks))
        d["output_accept"] = list(self.output_accept)
        d["input_accept"] = list(self.input_accept)
        d["forward_accept"] = list(self.forward_accept)
        d["output_drop"] = list(self.output_drop)
        d["input_drop"] = list(self.input_drop)
        d["forward_drop"] = list(self.forward_drop)
        d["routes"] = list(self.routes)
        d["docker_gw_bridge_ip"] = self.docker_gw_bridge_ip
        d["physical_host_ip"] = self.physical_host_ip
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"ips_gw_default_policy_networks:{list(map(lambda x: str(x), self.ips_gw_default_policy_networks))}, " \
               f"output_accept:{self.output_accept}, " \
               f"input_accept:{self.input_accept}, forward_accept:{self.forward_accept}, " \
               f"output_drop:{self.output_drop}, " \
               f"input_drop:{self.input_drop}, forward_drop:{self.forward_drop}, " \
               f"routers:{self.routes}, hostname: {self.hostname}, docker_gw_bridge_ip:{self.docker_gw_bridge_ip}," \
               f" physical_host_ip: {self.physical_host_ip}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "NodeFirewallConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return NodeFirewallConfig.from_dict(json.loads(json_str))

    def copy(self) -> "NodeFirewallConfig":
        """
        :return: a copy of the DTO
        """
        return NodeFirewallConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "NodeFirewallConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        config.output_accept = set(list(map(
            lambda x: GeneralUtil.replace_first_octet_of_ip(
                ip=x, ip_first_octet=ip_first_octet), list(config.output_accept))))
        config.input_accept = set(list(map(
            lambda x: GeneralUtil.replace_first_octet_of_ip(
                ip=x, ip_first_octet=ip_first_octet), list(config.input_accept))))
        config.forward_accept = set(list(map(
            lambda x: GeneralUtil.replace_first_octet_of_ip(
                ip=x, ip_first_octet=ip_first_octet), list(config.forward_accept))))
        config.output_drop = set(list(map(
            lambda x: GeneralUtil.replace_first_octet_of_ip(
                ip=x, ip_first_octet=ip_first_octet), list(config.output_drop))))
        config.input_drop = set(list(map(
            lambda x: GeneralUtil.replace_first_octet_of_ip(
                ip=x, ip_first_octet=ip_first_octet), list(config.input_drop))))
        config.forward_drop = set(list(map(
            lambda x: GeneralUtil.replace_first_octet_of_ip(
                ip=x, ip_first_octet=ip_first_octet), list(config.forward_drop))))
        config.routes = set(list(map(
            lambda x: GeneralUtil.replace_first_octet_of_ip_tuple(
                tuple_of_ips=x, ip_first_octet=ip_first_octet), list(config.routes))))
        config.ips_gw_default_policy_networks = list(map(lambda x: x.create_execution_config(
            ip_first_octet=ip_first_octet), config.ips_gw_default_policy_networks))
        return config

    @staticmethod
    def schema() -> "NodeFirewallConfig":
        """
        :return: get the schema of the DTO
        """
        dto = NodeFirewallConfig(ips_gw_default_policy_networks=[DefaultNetworkFirewallConfig.schema()], hostname="",
                                 output_accept=set(), input_accept=set(), forward_accept=set(), output_drop=set(),
                                 input_drop=set(), forward_drop=set(), routes=set())
        dto.output_accept.add("")
        dto.input_accept.add("")
        dto.forward_accept.add("")
        dto.output_drop.add("")
        dto.input_drop.add("")
        dto.forward_drop.add("")
        dto.routes.add(("", ""))
        return dto
