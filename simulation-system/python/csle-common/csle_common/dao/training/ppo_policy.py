from typing import List, Dict, Union
import numpy as np
import torch
import math
from stable_baselines3 import PPO
from csle_common.dao.training.policy import Policy
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.simulation_config.state import State
from csle_common.dao.simulation_config.state_type import StateType
from csle_common.dao.simulation_config.action import Action


class PPOPolicy(Policy):
    """
    A neural network policy learned with PPO
    """

    def __init__(self, model, simulation_name: str, save_path: str, player_type: PlayerType, states : List[State],
                 actions: List[Action]):
        """
        Initializes the policy

        :param model: the PPO model
        :param simulation_name: the simulation name
        :param save_path: the path to save the model to
        :param states: list of states (required for computing stage policies)
        :param actions: list of actions
        """
        super(PPOPolicy, self).__init__(agent_type=AgentType.PPO, player_type=player_type)
        self.model = model
        self.id = -1
        self.simulation_name = simulation_name
        self.save_path = save_path
        if self.model is None:
            self.model = PPO.load(path = self.save_path)
        self.states = states
        self.actions = actions

    def action(self, o: List[float]) -> Union[int, List[int], np.ndarray]:
        """
        Multi-threshold stopping policy

        :param o: the current observation
        :return: the selected action
        """
        a, _ = self.model.predict(np.array(o), deterministic=False)
        return a

    def to_dict(self) -> Dict[str, Union[float, int, str]]:
        """
        :return: a dict representation of the policy
        """
        d = {}
        d["id"] = self.id
        d["simulation_name"] = self.simulation_name
        d["save_path"] = self.save_path
        if self.model is not None:
            d["policy_kwargs"] = self.model.policy_kwargs
        self.model.save(path = self.save_path)
        d["states"] = list(map(lambda x: x.to_dict(), self.states))
        d["player_type"] = self.player_type
        d["actions"] = list(map(lambda x: x.to_dict(), self.actions))
        return d

    @staticmethod
    def from_dict(d: Dict) -> "PPOPolicy":
        """
        Converst a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = PPOPolicy(model=None, simulation_name=d["simulation_name"], save_path=d["save_path"],
                        states=list(map(lambda x: State.from_dict(x), d["states"])), player_type=d["player_type"],
                        actions=list(map(lambda x: Action.from_dict(x), d["actions"])))
        obj.id = d["id"]
        return obj

    def stage_policy(self, o: Union[List[Union[int, float]], int, float]) -> List[List[float]]:
        """
        Gets the stage policy, i.e a |S|x|A| policy

        :param o: the latest observation
        :return: the |S|x|A| stage policy
        """
        b1 = o[1]
        l = int(o[0])
        if not self.player_type == PlayerType.ATTACKER:
            stage_policy = []
            for _ in self.states:
                stage_policy.append(self._get_attacker_dist(obs=o))
            return stage_policy
        else:
            stage_policy = []
            for s in self.states:
                if s.state_type != StateType.TERMINAL:
                    o = [l, b1, s.id]
                    stage_policy.append(self._get_attacker_dist(obs=o))
                else:
                    stage_policy.append([0.5, 0.5])
            return stage_policy

    def _get_attacker_dist(self, obs) -> List[float]:
        """
        Utility function for getting the action distribution conditioned on a given observation

        :param obs: the observation to condition on
        :return: the conditional ation distribution
        """
        obs = np.array([obs])
        # latent_pi, latent_vf, latent_sde = self._get_latent(obs)
        # Evaluate the values for the given observations
        # values = self.value_net(latent_vf)
        # distribution = self._get_action_dist_from_latent(latent_pi, latent_sde=latent_sde)

        dist = []
        # for a in self.actions:
        #     dist.append()

        actions, values, log_prob = self.model.policy.forward(obs=torch.tensor(obs).to(self.model.device))
        action = actions[0]
        if action == 1:
            stop_prob = math.exp(log_prob)
        else:
            stop_prob = 1-math.exp(log_prob)
        return [1-stop_prob, stop_prob]

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"model: {self.model}, id: {self.id}, simulation_name: {self.simulation_name}, " \
               f"save path: {self.save_path}, states: {self.states}"

