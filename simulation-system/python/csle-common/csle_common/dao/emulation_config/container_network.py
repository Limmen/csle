from typing import Dict, Any


class ContainerNetwork:
    """
    DTO representing an IP network of virtual containers
    """

    def __init__(self, name: str, subnet_mask: str, subnet_prefix: str):
        """
        Initializes the DTO

        :param name: the name of the network
        :param subnet_mask: the subnet mask of the network
        """
        self.name = name
        self.subnet_mask = subnet_mask
        self.subnet_prefix = subnet_prefix


    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ContainerNetwork":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = ContainerNetwork(
            name = d["name"], subnet_mask=d["subnet_mask"], subnet_prefix=d["subnet_prefix"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["name"] = self.name
        d["subnet_mask"] = self.subnet_mask
        d["subnet_prefix"] = self.subnet_prefix
        return d

    def __str__(self):
        """
        :return: a string representation of the object
        """
        return f"name:{self.name}, subnet_mask:{self.subnet_mask}, subnet_prefix: {self.subnet_prefix}"

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