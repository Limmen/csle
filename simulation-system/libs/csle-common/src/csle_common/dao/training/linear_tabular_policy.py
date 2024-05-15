from typing import List, Dict, Union, Optional, Any
import iteround
import numpy as np
from numpy.typing import NDArray
from csle_common.dao.training.policy import Policy
from csle_common.dao.training.linear_threshold_stopping_policy import LinearThresholdStoppingPolicy
from csle_common.dao.training.tabular_policy import TabularPolicy
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.simulation_config.state import State
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.simulation_config.action import Action
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.policy_type import PolicyType


class LinearTabularPolicy(Policy):
    """
    A linear tabular policy that uses a linear threshold line to decide when to take action and a tabular policy to
    decide which action to take
    """

    def __init__(self, stopping_policy: LinearThresholdStoppingPolicy, action_policy: TabularPolicy,
                 simulation_name: str, states: List[State], player_type: PlayerType,
                 actions: List[Action], experiment_config: Optional[ExperimentConfig], avg_R: float,
                 agent_type: AgentType) -> None:
        """
        Initializes the policy

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
        super(LinearTabularPolicy, self).__init__(agent_type=agent_type, player_type=player_type)
        self.stopping_policy = stopping_policy
        self.action_policy = action_policy
        self.id = -1
        self.simulation_name = simulation_name
        self.states = states
        self.actions = actions
        self.experiment_config = experiment_config
        self.avg_R = avg_R
        self.policy_type = PolicyType.LINEAR_TABULAR

    def action(self, o: List[float], deterministic: bool = True) -> Union[int, List[int], float, NDArray[Any]]:
        """
        Multi-threshold stopping policy

        :param o: the current observation
        :param deterministic: boolean flag indicating whether the action selection should be deterministic
        :return: the selected action
        """
        stop = self.stopping_policy.action(o=o[1:])
        if stop == 1:
            return self.action_policy.action(o=int(o[0]))
        else:
            return 0

    def probability(self, o: List[float], a: int) -> int:
        """
        Probability of a given action

        :param o: the current observation
        :param a: a given action
        :return: the probability of a
        """
        taken_action = self.action(o=o)
        return taken_action == a

    def stage_policy(self, o: Any) -> Any:
        """
        Gets the stage policy, i.e a |S|x|A| policy

        :param o: the latest observation
        :return: the |S|x|A| stage policy
        """
        stage_strategy = np.zeros((len(self.states), len(self.actions)))
        for i, s_a in enumerate(self.states):
            o[0] = s_a
            for j, a in enumerate(self.actions):
                stage_strategy[i][j] = self.probability(o=o, a=j)
            stage_strategy[i] = iteround.saferound(stage_strategy[i], 2)
            assert round(sum(stage_strategy[i]), 3) == 1
        return stage_strategy.tolist()

    def to_dict(self) -> Dict[str, List[float]]:
        """
        :return: a dict representation of the policy
        """
        d: Dict[str, Any] = {}
        d["stopping_policy"] = self.stopping_policy.to_dict()
        d["action_policy"] = self.action_policy.to_dict()
        d["id"] = self.id
        d["simulation_name"] = self.simulation_name
        d["states"] = list(map(lambda x: x.to_dict(), self.states))
        d["actions"] = list(map(lambda x: x.to_dict(), self.actions))
        d["player_type"] = self.player_type
        d["agent_type"] = self.agent_type
        if self.experiment_config is not None:
            d["experiment_config"] = self.experiment_config.to_dict()
        else:
            d["experiment_config"] = None
        d["avg_R"] = self.avg_R
        d["policy_type"] = self.policy_type
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "LinearTabularPolicy":
        """
        Converst a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = LinearTabularPolicy(
            stopping_policy=LinearThresholdStoppingPolicy.from_dict(d["stopping_policy"]),
            action_policy=TabularPolicy.from_dict(d["action_policy"]),
            simulation_name=d["simulation_name"],
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
        return f"stopping_policy: {self.stopping_policy}, action_policy: {self.action_policy}, " \
               f"id: {self.id}, simulation_name: {self.simulation_name}, " \
               f"player_type: {self.player_type}, " \
               f"states: {self.states}, agent_type: {self.agent_type}, actions: {self.actions}," \
               f"experiment_config: {self.experiment_config}, avg_R: {self.avg_R}, policy_type: {self.policy_type}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "LinearTabularPolicy":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return LinearTabularPolicy.from_dict(json.loads(json_str))

    def copy(self) -> "LinearTabularPolicy":
        """
        :return: a copy of the DTO
        """
        return self.from_dict(self.to_dict())
