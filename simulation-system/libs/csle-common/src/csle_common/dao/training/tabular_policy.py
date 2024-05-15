from typing import Union, List, Dict, Any, Optional
import numpy as np
from numpy.typing import NDArray
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.training.policy import Policy
from csle_common.dao.simulation_config.action import Action
from csle_common.dao.training.policy_type import PolicyType


class TabularPolicy(Policy):
    """
    Object representing a tabular policy
    """

    def __init__(self, player_type: PlayerType, actions: List[Action], lookup_table: List[List[float]],
                 agent_type: AgentType, simulation_name: str, avg_R: float,
                 value_function: Optional[List[Any]] = None, q_table: Optional[List[Any]] = None) -> None:
        """
        Initializes the policy

        :param actions: list of actions
        :param player_type: the player type
        :param lookup_table: the lookup table that defines the policy
        :param value_function: the value function (optional)
        :param q_table: the Q-value function (optional)
        :param simulation_name: the name of the simulation
        :param avg_R: average reward obtained with the policy
        """
        super(TabularPolicy, self).__init__(agent_type=agent_type, player_type=player_type)
        self.actions = actions
        self.lookup_table = lookup_table
        self.value_function = value_function
        self.q_table = q_table
        self.simulation_name = simulation_name
        self.id = -1
        self.avg_R = avg_R
        self.policy_type = PolicyType.TABULAR

    def action(self, o: Union[int, float], deterministic: bool = True) -> Union[int, List[int], float, NDArray[Any]]:
        """
        Selects the next action

        :param o: the input observation
        :param deterministic: boolean flag indicating whether the action selection should be deterministic
        :return: the next action and its probability
        """
        return int(np.random.choice(np.arange(0, len(self.lookup_table[int(o)])), p=self.lookup_table[int(o)]))

    def probability(self, o: Union[int, float], a: int) -> float:
        """
        Calculates the probability of taking a given action for a given observation

        :param o: the input observation
        :param a: the action
        :return: p(a|o)
        """
        return self.lookup_table[int(o)][a]

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "TabularPolicy":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        dto = TabularPolicy(actions=list(map(lambda x: Action.from_dict(x), d["actions"])),
                            player_type=d["player_type"], agent_type=d["agent_type"],
                            lookup_table=d["lookup_table"], value_function=d["value_function"],
                            simulation_name=d["simulation_name"], avg_R=d["avg_R"],
                            q_table=d["q_table"])
        if "id" in d:
            dto.id = d["id"]
        return dto

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: A dict representation of the function
        """
        d: Dict[str, Any] = {}
        d["agent_type"] = self.agent_type
        d["player_type"] = self.player_type
        d["actions"] = list(map(lambda x: x.to_dict(), self.actions))
        d["lookup_table"] = self.lookup_table
        d["value_function"] = self.value_function
        d["simulation_name"] = self.simulation_name
        d["id"] = self.id
        d["avg_R"] = self.avg_R
        d["q_table"] = self.q_table
        d["policy_type"] = self.policy_type
        return d

    def stage_policy(self, o: Union[List[Union[int, float]], int, float]) -> List[List[float]]:
        """
        Gets the stage policy, i.e a |S|x|A| policy

        :param o: the latest observation
        :return: the |S|x|A| stage policy
        """
        return self.lookup_table

    def __str__(self) -> str:
        """
        :return: a string representation of the policy
        """
        return f"agent_type: {self.agent_type}, player_type: {self.player_type}, " \
               f"actions: {list(map(lambda x: str(x), self.actions))}, lookup_table: {self.lookup_table}, " \
               f"value_function: {self.value_function}, simulation_name: {self.simulation_name}, id: {self.id}, " \
               f"avg_R: {self.avg_R}, q_table: {self.q_table}, policy_type: {self.policy_type}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "TabularPolicy":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return TabularPolicy.from_dict(json.loads(json_str))

    def copy(self) -> "TabularPolicy":
        """
        :return: a copy of the DTO
        """
        return self.from_dict(self.to_dict())
