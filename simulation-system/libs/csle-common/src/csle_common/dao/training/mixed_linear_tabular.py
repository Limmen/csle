from typing import List, Dict, Union, Any
import numpy as np
from numpy.typing import NDArray
import iteround
from csle_common.dao.training.policy import Policy
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.simulation_config.state import State
from csle_common.dao.simulation_config.action import Action
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.policy_type import PolicyType
from csle_common.dao.training.linear_tabular_policy import LinearTabularPolicy


class MixedLinearTabularPolicy(Policy):
    """
    A mixed policy using an ensemble of linear tabulat policies
    """

    def __init__(self, simulation_name: str, player_type: PlayerType, states: List[State],
                 actions: List[Action], experiment_config: ExperimentConfig, avg_R: float):
        """
        Initializes the policy

        :param simulation_name: the simulation name
        :param states: list of states (required for computing stage policies)
        :param actions: list of actions
        :param experiment_config: the experiment configuration for training the policy
        :param avg_R: the average reward of the policy when evaluated in the simulation
        """
        super(MixedLinearTabularPolicy, self).__init__(agent_type=AgentType.DFSP_LOCAL, player_type=player_type)
        self.linear_tabular_policies: List[LinearTabularPolicy] = []
        self.id = -1
        self.simulation_name = simulation_name
        self.states = states
        self.actions = actions
        self.experiment_config = experiment_config
        self.avg_R = avg_R
        self.policy_type = PolicyType.MIXED_LINEAR_TABULAR

    def action(self, o: List[float]) -> Union[int, List[int], float, NDArray[Any]]:
        """
        Multi-threshold stopping policy

        :param o: the current observation
        :return: the selected action
        """
        policy = np.random.choice(self.linear_tabular_policies)
        a = policy.action(o=o)
        return float(a)

    def probability(self, o: List[float], a: int) -> int:
        """
        Probability of a given action

        :param o: the current observation
        :param a: a given action
        :return: the probability of a
        """
        return self.action(o=o) == a

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the policy
        """
        d: Dict[str, Any] = {}
        d["id"] = self.id
        d["simulation_name"] = self.simulation_name
        d["linear_tabular_policies"] = list(map(lambda x: x.to_dict(), self.linear_tabular_policies))
        d["states"] = list(map(lambda x: x.to_dict(), self.states))
        d["player_type"] = self.player_type
        d["actions"] = list(map(lambda x: x.to_dict(), self.actions))
        d["experiment_config"] = self.experiment_config.to_dict()
        d["agent_type"] = self.agent_type
        d["avg_R"] = self.avg_R
        d["policy_type"] = self.policy_type
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "MixedLinearTabularPolicy":
        """
        Converst a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        linear_tabular_policies = list(map(lambda x: x.from_dict(), d["linear_tabular_policies"]))
        obj = MixedLinearTabularPolicy(simulation_name=d["simulation_name"],
                                       states=list(map(lambda x: State.from_dict(x), d["states"])),
                                       player_type=d["player_type"],
                                       actions=list(map(lambda x: Action.from_dict(x), d["actions"])),
                                       experiment_config=ExperimentConfig.from_dict(d["experiment_config"]),
                                       avg_R=d["avg_R"])
        obj.linear_tabular_policies = linear_tabular_policies
        obj.id = d["id"]
        return obj

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"linear_tabular_policies: {self.linear_tabular_policies}, id: {self.id}, " \
               f"simulation_name: {self.simulation_name}, " \
               f"states: {self.states}, experiment_config: {self.experiment_config}," \
               f"avg_R: {self.avg_R}, policy type: {self.policy_type}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "MixedLinearTabularPolicy":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return MixedLinearTabularPolicy.from_dict(json.loads(json_str))

    def copy(self) -> "MixedLinearTabularPolicy":
        """
        :return: a copy of the DTO
        """
        return self.from_dict(self.to_dict())

    def stage_policy(self, o: Union[List[Union[int, float]], int, float]) -> List[List[float]]:
        """
        Returns the stage policy for a given observation

        :param o: the observation to return the stage policy for
        :return: the stage policy
        """
        stage_policies = []
        for policy in self.linear_tabular_policies:
            stage_policies.append(policy.stage_policy(o=o))
        stage_strategy = np.zeros((len(self.states), len(self.actions)))
        for i, s_a in enumerate(self.states):
            for j, a in enumerate(self.actions):
                stage_strategy[i][j] = sum([stage_policies[k][i][j]
                                            for k in range(len(stage_policies))]) / len(stage_policies)
            stage_strategy[i] = iteround.saferound(stage_strategy[i], 2)
        return list(stage_strategy.tolist())
