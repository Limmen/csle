from typing import Dict, Any, Union
from csle_common.dao.simulation_config.state_type import StateType
from csle_base.json_serializable import JSONSerializable


class State(JSONSerializable):
    """
    DTO representing the state of a simulation environment
    """

    def __init__(self, id: int, name: str, descr: str, state_type: StateType):
        """
        Initializes the DTO

        :param id: the id of the state
        :param name: the name of the state
        :param descr: a description of the state
        :param state_type: the state type
        """
        self.id = id
        self.name = name
        self.descr = descr
        self.state_type = state_type

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "State":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = State(id=d["id"], name=d["name"], descr=d["descr"], state_type=StateType(d["state_type"]))
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Union[str, int, StateType]] = {}
        d["id"] = self.id
        d["name"] = self.name
        d["descr"] = self.descr
        d["state_type"] = self.state_type.value
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"id:{self.id}, name:{self.name}, descr:{self.descr}, state_type: {self.state_type}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "State":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return State.from_dict(json.loads(json_str))
