from typing import Dict, Any


class State:
    """
    DTO representing the state of a simulation environment
    """

    def __init__(self, id: int, name: str, descr: str):
        """
        Initializes the DTO

        :param id: the id of the state
        :param name: the name of the state
        :param descr: a description of the state
        """
        self.id = id
        self.name = name
        self.descr = descr

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "State":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = State(
            id=d["id"], name=d["name"], descr=d["descr"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["id"] = self.id
        d["name"] = self.name
        d["descr"] = self.descr
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"id:{self.id}, name:{self.name}, descr:{self.descr}"