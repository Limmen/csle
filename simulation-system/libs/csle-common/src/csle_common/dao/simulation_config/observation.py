from typing import Union, Dict, Any


class Observation:
    """
    DTO class representing an observation in a simulation
    """

    def __init__(self, id: Union[int, float], val: int, descr: str):
        """
        Initializes the DTO

        :param id: the id of the observation
        :param val: in case the val and the id are different
        :param descr: a description of the observation
        """
        self.id = id
        self.val = val
        self.descr = descr

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Observation":
        """
        Converts a dict representation to an instance
        :param d: the dict to convert
        :return: the created instance
        """
        obj = Observation(
            id=d["id"], descr=d["descr"], val=d["val"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["id"] = self.id
        d["descr"] = self.descr
        d["val"] = self.val
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"id: {self.id}, descr: {self.descr}, val: {self.val}"
