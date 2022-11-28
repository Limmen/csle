from typing import List, Dict, Any
from csle_common.dao.emulation_config.node_firewall_config import NodeFirewallConfig
from csle_common.util.general_util import GeneralUtil


class TopologyConfig:
    """
    A DTO representing the topology configuration of an emulation environment
    """

    def __init__(self, node_configs: List[NodeFirewallConfig], subnetwork_masks: List[str]):
        """
        Initializes the DTO

        :param node_configs: the list of node configurations
        :param subnetwork: the subnetwork
        """
        self.node_configs = node_configs
        self.subnetwork_masks = subnetwork_masks

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "TopologyConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = TopologyConfig(
            node_configs=list(map(lambda x: NodeFirewallConfig.from_dict(x), d["node_configs"])),
            subnetwork_masks=d["subnetwork_masks"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["subnetwork_masks"] = self.subnetwork_masks
        d["node_configs"] = list(map(lambda x: x.to_dict(), self.node_configs))
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"node configs:{','.join(list(map(lambda x: str(x), self.node_configs)))}, " \
               f"subnetwork_masks:{','.join(self.subnetwork_masks)}"

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

    def copy(self) -> "TopologyConfig":
        """
        :return: a copy of the DTO
        """
        return TopologyConfig.from_dict(self.to_dict())

    def create_execution_config(self, ip_first_octet: int) -> "TopologyConfig":
        """
        Creates a new config for an execution

        :param ip_first_octet: the first octet of the IP of the new execution
        :return: the new config
        """
        config = self.copy()
        config.subnetwork_masks = list(map(lambda x: GeneralUtil.replace_first_octet_of_ip(
            ip=x, ip_first_octet=ip_first_octet), config.subnetwork_masks))
        config.node_configs = list(map(lambda x: x.create_execution_config(ip_first_octet=ip_first_octet),
                                       config.node_configs))
        return config
