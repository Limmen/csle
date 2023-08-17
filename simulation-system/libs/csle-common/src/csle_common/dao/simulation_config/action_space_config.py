from typing import List, Dict, Any
from csle_common.dao.simulation_config.value_type import ValueType
from csle_common.dao.simulation_config.action import Action
from csle_base.json_serializable import JSONSerializable


class ActionSpaceConfig(JSONSerializable):
    """
    DTO Class representing the action space configuration of a player in a simulation environment
    """

    def __init__(self, actions: List[Action], player_id: int, action_type: ValueType, descr: str = ""):
        """
        Initializes the DTO

        :param actions: the list of actions
        :param action_type: the type of the actions
        :param descr: a description of the action space
        :param player_id: the id of the player
        """
        self.actions = actions
        self.action_type = action_type
        self.descr = descr
        self.player_id = player_id

    def actions_ids(self) -> List[int]:
        """
        :return: a list of action ids
        """
        return list(map(lambda x: x.id, self.actions))

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ActionSpaceConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = ActionSpaceConfig(
            actions=list(map(lambda x: Action.from_dict(x), d["actions"])),
            action_type=d["action_type"], descr=d["descr"], player_id=d["player_id"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["actions"] = list(map(lambda x: x.to_dict(), self.actions))
        d["action_type"] = self.action_type
        d["descr"] = self.descr
        d["player_id"] = self.player_id
        return d

    def __str__(self):
        """
        :return: a string representation of the object
        """
        return f"actions:{list(map(lambda x: str(x), self.actions))}, action_type: {self.action_type}, " \
               f"descr: {self.descr}, player_id: {self.player_id}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "ActionSpaceConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return ActionSpaceConfig.from_dict(json.loads(json_str))
