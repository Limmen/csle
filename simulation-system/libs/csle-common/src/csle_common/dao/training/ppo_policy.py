from typing import List, Dict, Union, Any
import numpy as np
import numpy.typing as npt
import torch
import math
import iteround
from stable_baselines3 import PPO
from csle_common.dao.training.policy import Policy
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.simulation_config.state import State
from csle_common.dao.simulation_config.action import Action
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.policy_type import PolicyType
from csle_common.logging.log import Logger
from csle_common.models.ppo_network import PPONetwork


class PPOPolicy(Policy):
    """
    A neural network policy learned with PPO
    """

    def __init__(self, model: Union[None, PPO, PPONetwork], simulation_name: str, save_path: str,
                 player_type: PlayerType, states: List[State], actions: List[Action],
                 experiment_config: ExperimentConfig, avg_R: float):
        """
        Initializes the policy

        :param model: the PPO model
        :param simulation_name: the simulation name
        :param save_path: the path to save the model to
        :param states: list of states (required for computing stage policies)
        :param actions: list of actions
        :param experiment_config: the experiment configuration for training the policy
        :param avg_R: the average reward of the policy when evaluated in the simulation
        """
        super(PPOPolicy, self).__init__(agent_type=AgentType.PPO, player_type=player_type)
        self.model = model
        self.id = -1
        self.simulation_name = simulation_name
        self.save_path = save_path
        self.load()
        self.states = states
        self.actions = actions
        self.experiment_config = experiment_config
        self.avg_R = avg_R
        self.policy_type = PolicyType.PPO

    def action(self, o: Union[List[float], List[int]], deterministic: bool = True) \
            -> Union[int, float, npt.NDArray[Any]]:
        """
        Multi-threshold stopping policy

        :param o: the current observation
        :param deterministic: boolean flag indicating whether the action selection should be deterministic
        :return: the selected action
        """
        if self.model is None:
            raise ValueError("The model is None")
        if isinstance(self.model, PPO):
            a = self.model.predict(np.array(o), deterministic=deterministic)[0]
            try:
                return int(a)
            except Exception:
                return a
        elif isinstance(self.model, PPONetwork):
            action_tensor, _, _, _ = self.model.get_action_and_value(x=torch.tensor(o))
            try:
                return int(action_tensor.item())
            except Exception:
                return action_tensor.item()
        else:
            raise ValueError(f"Model: {self.model} not recognized")

    def probability(self, o: Union[List[float], List[int]], a: int) -> float:
        """
        Multi-threshold stopping policy

        :param o: the current observation
        :param o: the action
        :return: the probability of the action
        """
        if self.model is None:
            raise ValueError("The model is None")
        if isinstance(self.model, PPO):
            log_prob = self.model.policy.get_distribution(obs=torch.tensor([o]).to(self.model.device)).log_prob(
                torch.tensor(a).to(self.model.device)).item()
        elif isinstance(self.model, PPONetwork):
            _, log_prob, _, _ = self.model.get_action_and_value(x=torch.tensor(o), action=torch.tensor(a))
        else:
            raise ValueError(f"Model: {self.model} not recognized")
        prob = math.exp(log_prob)
        return prob

    def value(self, o: Union[List[float], List[int]]) -> float:
        """
        Gets the value of a given observation, computed by the critic network

        :param o: the observation to get the value of
        :return: V(o)
        """
        if self.model is None:
            raise ValueError("The model is None")
        if isinstance(self.model, PPO):
            return self.model.policy.predict_values(obs=torch.tensor(np.array([o])).to(self.model.device)).item()
        elif isinstance(self.model, PPONetwork):
            return self.model.get_value(x=torch.tensor(o)).item()
        else:
            raise ValueError(f"Model: {self.model} not recognized")

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the policy
        """
        d: Dict[str, Any] = {}
        d["id"] = self.id
        d["simulation_name"] = self.simulation_name
        d["save_path"] = self.save_path
        if self.model is not None:
            self.model.save(path=self.save_path)
            d["policy_kwargs"] = {}
            d["policy_kwargs"]["net_arch"] = []
            if isinstance(self.model, PPO):
                d["policy_kwargs"] = self.model.policy_kwargs
        else:
            d["policy_kwargs"] = {}
            d["policy_kwargs"]["net_arch"] = []
        d["states"] = list(map(lambda x: x.to_dict(), self.states))
        d["player_type"] = self.player_type
        d["actions"] = list(map(lambda x: x.to_dict(), self.actions))
        d["experiment_config"] = self.experiment_config.to_dict()
        d["agent_type"] = self.agent_type
        d["avg_R"] = self.avg_R
        d["policy_type"] = self.policy_type
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "PPOPolicy":
        """
        Converst a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = PPOPolicy(model=None, simulation_name=d["simulation_name"], save_path=d["save_path"],
                        states=list(map(lambda x: State.from_dict(x), d["states"])), player_type=d["player_type"],
                        actions=list(map(lambda x: Action.from_dict(x), d["actions"])),
                        experiment_config=ExperimentConfig.from_dict(d["experiment_config"]), avg_R=d["avg_R"])
        obj.id = d["id"]
        return obj

    def stage_policy(self, o: Union[List[int], List[float]]) -> List[List[float]]:
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
        stage_strategy.tolist()
        return list(stage_strategy.tolist())

    def _get_attacker_dist(self, obs) -> List[float]:
        """
        Utility function for getting the action distribution conditioned on a given observation

        :param obs: the observation to condition on
        :return: the conditional ation distribution
        """
        obs = np.array([obs])
        if self.model is None:
            raise ValueError("The model is None")
        if isinstance(self.model, PPO):
            actions, values, log_prob_tensor = self.model.policy.forward(obs=torch.tensor(obs).to(self.model.device))
            log_prob = float(log_prob_tensor.item())
            action = int(actions[0])
        elif isinstance(self.model, PPONetwork):
            action_tensor, log_prob, _, _ = self.model.get_action_and_value(x=torch.tensor(obs))
            action = int(action_tensor.item())
        else:
            raise ValueError(f"Model: {self.model} not recognized")
        if action == 1:
            stop_prob = math.exp(log_prob)
        else:
            stop_prob = 1 - math.exp(log_prob)
        return [1 - stop_prob, stop_prob]

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"model: {self.model}, id: {self.id}, simulation_name: {self.simulation_name}, " \
               f"save path: {self.save_path}, states: {self.states}, experiment_config: {self.experiment_config}," \
               f"avg_R: {self.avg_R}, policy type: {self.policy_type}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "PPOPolicy":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return PPOPolicy.from_dict(json.loads(json_str))

    def copy(self) -> "PPOPolicy":
        """
        :return: a copy of the DTO
        """
        return self.from_dict(self.to_dict())

    def load(self) -> None:
        """
        Attempts to load the policy from disk

        :return: None
        """
        if self.model is None and self.save_path != "":
            try:
                self.model = PPO.load(path=self.save_path)
            except Exception as e1:
                try:
                    self.model = PPONetwork.load(path=self.save_path)
                except Exception as e2:
                    Logger.__call__().get_logger().warning(
                        f"There was an exception loading the model from path: {self.save_path}, "
                        f"exception: {str(e1)}, {repr(e1)} {str(e2)}, {repr(e2)}")
