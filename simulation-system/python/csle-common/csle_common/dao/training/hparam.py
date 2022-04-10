from typing import Union, List, Dict, Any


class HParam:
    """
    DTO class representing a hyperparameter
    """

    def __init__(self, value: Union[int, float, str, List], name: str, descr: str):
        """
        Initializes the DTO

        :param value: the value of the hyperparameter
        :param name: the name of the hyperparameter
        :param descr: the description of the hyperparameter
        """
        self.value = value
        self.name = name
        self.descr = descr

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["value"] = self.value
        d["name"] = self.name
        d["descr"] = self.descr
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "HParam":
        obj = HParam(
            value = d["value"], name=d["name"], descr=d["descr"]
        )
        return obj

