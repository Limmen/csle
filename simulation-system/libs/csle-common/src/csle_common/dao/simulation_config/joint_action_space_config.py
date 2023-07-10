from typing import List, Dict, Any
from csle_common.dao.simulation_config.action_space_config import ActionSpaceConfig
from csle_base.json_serializable import JSONSerializable


class JointActionSpaceConfig(JSONSerializable):
    """
    DTO representing the joint action space of a simulation environment
    """

    def __init__(self, action_spaces: List[ActionSpaceConfig]):
        """
        Initializes the DTO

        :param action_spaces: the list of action spaces for each player
        """
        self.action_spaces = action_spaces

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "JointActionSpaceConfig":
        """
        Converts a dict representation into an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = JointActionSpaceConfig(
            action_spaces=list(map(lambda x: ActionSpaceConfig.from_dict(x), d["action_spaces"]))
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d = {}
        d["action_spaces"] = list(map(lambda x: x.to_dict(), self.action_spaces))
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the DTO
        """
        return f"action_spaces: {list(map(lambda x: str(x), self.action_spaces))}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "JointActionSpaceConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return JointActionSpaceConfig.from_dict(json.loads(json_str))
