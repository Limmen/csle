from typing import List, Dict, Any
from csle_common.dao.simulation_config.state import State
from csle_base.json_serializable import JSONSerializable


class StateSpaceConfig(JSONSerializable):
    """
    DTO representing the state space configuration of a simulation environment
    """

    def __init__(self, states: List[State]):
        """
        Initializes the DTO

        :param states: the list of states
        """
        self.states = states

    def states_ids(self) -> List[int]:
        """
        :return: list of state ids
        """
        return list(map(lambda x: x.id, self.states))

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "StateSpaceConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = StateSpaceConfig(states=list(map(lambda x: State.from_dict(x), d["states"])))
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the DTO
        """
        d = {}
        d["states"] = list(map(lambda x: x.to_dict(), self.states))
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the DTO
        """
        return f"states: {list(map(lambda x: str(x), self.states))}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "StateSpaceConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return StateSpaceConfig.from_dict(json.loads(json_str))
