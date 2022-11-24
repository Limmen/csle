from typing import Dict, Any
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig
from csle_common.dao.simulation_config.simulation_env_input_config import SimulationEnvInputConfig
from csle_common.dao.training.policy import Policy
from csle_common.dao.training.random_policy import RandomPolicy
from csle_common.dao.training.multi_threshold_stopping_policy import MultiThresholdStoppingPolicy
from csle_common.dao.training.ppo_policy import PPOPolicy


class StoppingGameAttackerMdpConfig(SimulationEnvInputConfig):
    """
    DTO class representing the configuration of the MDP environnment of the attacker
    when facing a static defender policy
    """

    def __init__(self, env_name: str, stopping_game_config: StoppingGameConfig, defender_strategy: Policy,
                 stopping_game_name: str = "csle-stopping-game-v1"):
        """
        Initializes the DTO

        :param env_name: the environment name
        :param stopping_game_config: the underlying stopping game config
        :param defender_strategy: the static defender strategy name
        :param stopping_game_name: the underlying stopping game name
        """
        super().__init__()
        self.env_name = env_name
        self.stopping_game_config = stopping_game_config
        self.defender_strategy = defender_strategy
        self.stopping_game_name = stopping_game_name

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "StoppingGameAttackerMdpConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        defender_strategy = None
        try:
            defender_strategy = MultiThresholdStoppingPolicy.from_dict(d["defender_strategy"])
        except Exception:
            try:
                defender_strategy = RandomPolicy.from_dict(d["defender_strategy"])
            except Exception:
                defender_strategy = PPOPolicy.from_dict(d["defender_strategy"])
        obj = StoppingGameAttackerMdpConfig(
            stopping_game_config=StoppingGameConfig.from_dict(d["stopping_game_config"]),
            defender_strategy=defender_strategy,
            stopping_game_name=d["stopping_game_name"], env_name=d["env_name"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["stopping_game_config"] = self.stopping_game_config.to_dict()
        d["defender_strategy"] = self.defender_strategy.to_dict()
        d["stopping_game_name"] = self.stopping_game_name
        d["env_name"] = self.env_name
        return d

    def __str__(self):
        """
        :return: a string representation of the object
        """
        return f"stopping_game_config: {self.stopping_game_config}, defender_strategy:{self.defender_strategy}, " \
               f"stopping_game_name:{self.stopping_game_name}, env_name: {self.env_name}"
