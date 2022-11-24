from typing import Dict, Any


class PlayerConfig:
    """
    DTO representing the configuration of a player in a simulation environment in CSLE
    """

    def __init__(self, name: str, id: int, descr: str = ""):
        """
        Initializes the DTO

        :param name: the name of the player
        :param id: the id of the player
        :param descr: the description of the player
        """
        self.name = name
        self.id = id
        self.descr = descr

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "PlayerConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = PlayerConfig(name=d["name"], id=int(d["id"]), descr=d["descr"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["name"] = self.name
        d["id"] = self.id
        d["descr"] = self.descr
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"name: {self.name}, id: {self.id}, descr: {self.descr}"
