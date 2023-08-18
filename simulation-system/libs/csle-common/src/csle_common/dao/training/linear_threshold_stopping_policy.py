from typing import List, Dict, Tuple, Union, Optional, Any
import math
import numpy as np
from csle_common.dao.training.policy import Policy
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.simulation_config.state import State
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.simulation_config.action import Action
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.policy_type import PolicyType


class LinearThresholdStoppingPolicy(Policy):
    """
    A linear threshold stopping policy
    """

    def __init__(self, theta, simulation_name: str, L: int, states: List[State], player_type: PlayerType,
                 actions: List[Action], experiment_config: Optional[ExperimentConfig], avg_R: float,
                 agent_type: AgentType, opponent_strategy: Optional["LinearThresholdStoppingPolicy"] = None) -> None:
        """
        Initializes the policy

        :param theta: the threshold vector
        :param simulation_name: the simulation name
        :param attacker: whether it is an attacker or not
        :param L: the number of stop actions
        :param states: list of states (required for computing stage policies)
        :param actions: list of actions
        :param experiment_config: the experiment configuration used for training the policy
        :param avg_R: the average reward of the policy when evaluated in the simulation
        :param agent_type: the agent type
        :param opponent_strategy: optionally an opponent strategy
        """
        super(LinearThresholdStoppingPolicy, self).__init__(agent_type=agent_type, player_type=player_type)
        self.theta = theta
        self.id = -1
        self.simulation_name = simulation_name
        self.L = L
        self.states = states
        self.actions = actions
        self.experiment_config = experiment_config
        self.avg_R = avg_R
        self.opponent_strategy = opponent_strategy
        self.policy_type = PolicyType.LINEAR_THRESHOLD

    def action(self, o: List[float]) -> int:
        """
        Multi-threshold stopping policy

        :param o: the current observation
        :return: the selected action
        """
        if self.player_type == PlayerType.DEFENDER:
            a, _ = self._defender_action(o=o)
            return a
        else:
            raise NotImplementedError("Attacker not implemented yet")

    def probability(self, o: List[float], a: int) -> float:
        """
        Probability of a given action

        :param o: the current observation
        :param a: a given action
        :return: the probability of a
        """
        if self.player_type == PlayerType.DEFENDER:
            _, prob = self._defender_action(o=o)
            return prob
        else:
            raise NotImplementedError("Attacker not implemented yet")

    def stage_policy(self, o: Union[List[Union[int, float]], int, float]) -> List[List[float]]:
        """
        Gets the stage policy, i.e a |S|x|A| policy

        :param o: the latest observation
        :return: the |S|x|A| stage policy
        """
        raise NotImplementedError("Not implemented")

    def _defender_action(self, o) -> Tuple[int, float]:
        """
        Linear threshold stopping policy of the defender

        :param o: the input observation
        :return: the selected action (int) and its probability
        """
        coefficients = np.zeros(len(self.theta))
        theta = self.theta
        coefficients[-1] = math.pow(theta[-1], 2)
        coefficients[-2] = 1 + math.pow(theta[-2], 2)
        for i in range(0, len(theta) - 2):
            coefficients[i] = coefficients[-2] * math.pow(math.sin(theta[i]), 2)
        belief = o
        x = np.append(np.array([0, 1]), np.array(coefficients))
        y = np.append(np.array(belief), np.array([-1]))
        d = np.dot(x, y)
        if d > 0:
            return 1, 1
        else:
            return 0, 1

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the policy
        """
        d: Dict[str, Any] = {}
        d["theta"] = self.theta
        d["id"] = self.id
        d["simulation_name"] = self.simulation_name
        d["states"] = list(map(lambda x: x.to_dict(), self.states))
        d["actions"] = list(map(lambda x: x.to_dict(), self.actions))
        d["player_type"] = self.player_type
        d["agent_type"] = self.agent_type
        d["L"] = self.L
        if self.experiment_config is not None:
            d["experiment_config"] = self.experiment_config.to_dict()
        else:
            d["experiment_config"] = None
        d["avg_R"] = self.avg_R
        d["policy_type"] = self.policy_type
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "LinearThresholdStoppingPolicy":
        """
        Converst a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = LinearThresholdStoppingPolicy(
            theta=d["theta"], simulation_name=d["simulation_name"], L=d["L"],
            states=list(map(lambda x: State.from_dict(x), d["states"])), player_type=d["player_type"],
            actions=list(map(lambda x: Action.from_dict(x), d["actions"])),
            experiment_config=ExperimentConfig.from_dict(d["experiment_config"]), avg_R=d["avg_R"],
            agent_type=d["agent_type"])
        obj.id = d["id"]
        return obj

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"theta: {self.theta}, id: {self.id}, simulation_name: {self.simulation_name}, " \
               f"player_type: {self.player_type}, " \
               f"L:{self.L}, states: {self.states}, agent_type: {self.agent_type}, actions: {self.actions}," \
               f"experiment_config: {self.experiment_config}, avg_R: {self.avg_R}, policy_type: {self.policy_type}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "LinearThresholdStoppingPolicy":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return LinearThresholdStoppingPolicy.from_dict(json.loads(json_str))

    def copy(self) -> "LinearThresholdStoppingPolicy":
        """
        :return: a copy of the DTO
        """
        return self.from_dict(self.to_dict())
