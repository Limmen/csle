from typing import List, Dict, Union, Any
import numpy as np
import numpy.typing as npt
from csle_common.dao.training.policy import Policy
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.simulation_config.state import State
from csle_common.dao.simulation_config.action import Action
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.policy_type import PolicyType
from csle_common.dao.training.ppo_policy import PPOPolicy


class MixedPPOPolicy(Policy):
    """
    A mixed policy using an ensemble of neural network policies learned through PPO
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
        super(MixedPPOPolicy, self).__init__(agent_type=AgentType.PPO, player_type=player_type)
        self.ppo_policies: List[PPOPolicy] = []
        self.id = -1
        self.simulation_name = simulation_name
        self.states = states
        self.actions = actions
        self.experiment_config = experiment_config
        self.avg_R = avg_R
        self.policy_type = PolicyType.MIXED_PPO_POLICY

    def action(self, o: List[float]) -> Union[int, npt.NDArray[Any]]:
        """
        Multi-threshold stopping policy

        :param o: the current observation
        :return: the selected action
        """
        policy: PPOPolicy = np.random.choice(self.ppo_policies)
        a = policy.action(o=o)
        return a

    def probability(self, o: List[float], a: int) -> float:
        """
        Probability of a given action

        :param o: the current observation
        :param a: a given action
        :return: the probability of a
        """
        return float(self.action(o=o) == a)

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the policy
        """
        d: Dict[str, Any] = {}
        d["id"] = self.id
        d["simulation_name"] = self.simulation_name
        d["ppo_policies"] = list(map(lambda x: x.to_dict(), self.ppo_policies))
        d["states"] = list(map(lambda x: x.to_dict(), self.states))
        d["player_type"] = self.player_type
        d["actions"] = list(map(lambda x: x.to_dict(), self.actions))
        d["experiment_config"] = self.experiment_config.to_dict()
        d["agent_type"] = self.agent_type
        d["avg_R"] = self.avg_R
        d["policy_type"] = self.policy_type
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "MixedPPOPolicy":
        """
        Converst a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        ppo_policies = list(map(lambda x: x.from_dict(), d["ppo_policies"]))
        obj = MixedPPOPolicy(simulation_name=d["simulation_name"],
                             states=list(map(lambda x: State.from_dict(x), d["states"])),
                             player_type=PlayerType(d["player_type"]),
                             actions=list(map(lambda x: Action.from_dict(x), d["actions"])),
                             experiment_config=ExperimentConfig.from_dict(d["experiment_config"]), avg_R=d["avg_R"])
        obj.ppo_policies = ppo_policies
        obj.id = d["id"]
        return obj

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"ppo_policies: {self.ppo_policies}, id: {self.id}, simulation_name: {self.simulation_name}, " \
               f"states: {self.states}, experiment_config: {self.experiment_config}," \
               f"avg_R: {self.avg_R}, policy type: {self.policy_type}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "MixedPPOPolicy":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return MixedPPOPolicy.from_dict(json.loads(json_str))

    def copy(self) -> "MixedPPOPolicy":
        """
        :return: a copy of the DTO
        """
        return self.from_dict(self.to_dict())

    def stage_policy(self, o: Union[List[int], List[float]]) -> List[List[float]]:
        """
        Returns the stage policy for a given observation

        :param o: the observation to return the stage policy for
        :return: the stage policy
        """
        stage_policies = []
        for policy in self.ppo_policies:
            stage_policies.append(policy.stage_policy(o=o))
        stage_strategy: List[List[float]] = []
        for i, s_a in enumerate(self.states):
            state_strategy = []
            for j, a in enumerate(self.actions):
                state_strategy.append(round(sum([stage_policies[k][i][j]
                                                 for k in range(len(stage_policies))]) / len(stage_policies), 2))

            stage_strategy.append(state_strategy)
        return stage_strategy
