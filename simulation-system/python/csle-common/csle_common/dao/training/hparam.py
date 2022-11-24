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
        obj = HParam(value=d["value"], name=d["name"], descr=d["descr"])
        return obj

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
