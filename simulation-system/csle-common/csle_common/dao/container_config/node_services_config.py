from typing import List
from csle_common.dao.network.network_service import NetworkService


class NodeServicesConfig:
    """
    A DTO object representing the services configuration of a node in an emulation environment
    """

    def __init__(self, ip: str, services : List[NetworkService]):
        """
        Initializes the DTO

        :param users: the list of node users configuration
        """
        self.ip = ip
        self.services = services

    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["services"] = list(map(lambda x: x.to_dict(), self.services))
        d["ip"] = self.ip
        return d

    @staticmethod
    def from_dict(d) -> "NodeServicesConfig":
        """
        Convert a dict representation to a DTO representation

        :return: a dto representation of the object
        """
        dto = NodeServicesConfig(ip = d["ip"],
                                 services=list(map(lambda x: NetworkService.from_dict(x), d["services"])))
        return dto

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "ip:{}, services:{}".format(self.ip, ",".join(list(map(lambda x: str(x), self.services))))