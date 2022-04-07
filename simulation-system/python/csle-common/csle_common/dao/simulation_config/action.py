from typing import Union, Dict, Any


class Action:
    """
    DTO representing an action in a simulation environment
    """

    def __init__(self, id: Union[int, float], descr: str):
        """
        Initializes the DTO

        :param id: the id of the action
        :param descr: the description of the action
        """
        self.id = id
        self.descr = descr

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Action":
        """
        Converts a dict representation of the DTO into an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = Action(
            id=d["id"], descr=d["descr"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the DTO
        """
        d = {}
        d["id"] = self.id
        d["descr"] = self.descr
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the DTO
        """
        return f"id:{self.id}, descr:{self.descr}"
