from typing import List, Dict, Union
from stable_baselines3 import PPO
from csle_common.dao.training.policy import Policy
from csle_common.dao.training.agent_type import AgentType


class PPOPolicy(Policy):
    """
    A neural network policy learned with PPO
    """

    def __init__(self, model, simulation_name: str, save_path: str):
        """
        Intializes the policy

        :param model: the PPO model
        :param simulation_name: the simulation name
        :param save_path: the path to save the model to
        """
        super(PPOPolicy, self).__init__(agent_type=AgentType.PPO)
        self.model = model
        self.id = -1
        self.simulation_name = simulation_name
        self.save_path = save_path
        if self.model is None:
            self.model = PPO.load(path = self.save_path)

    def action(self, o: List[float]) -> int:
        """
        Multi-threshold stopping policy

        :param o: the current observation
        :return: the selected action
        """
        a, _ = self.model.predict(o, deterministic=False)
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
        return d

    @staticmethod
    def from_dict(d: Dict) -> "PPOPolicy":
        """
        Converst a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = PPOPolicy(model=None, simulation_name=d["simulation_name"], save_path=d["save_path"])
        obj.id = d["id"]
        return obj

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"model: {self.model}, id: {self.id}, simulation_name: {self.simulation_name}, " \
               f"save path: {self.save_path}"

