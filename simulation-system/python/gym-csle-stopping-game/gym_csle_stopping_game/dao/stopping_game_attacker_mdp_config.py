from typing import Dict, Any
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig
from csle_common.dao.simulation_config.simulation_env_input_config import SimulationEnvInputConfig


class StoppingGameAttackerMdpConfig(SimulationEnvInputConfig):
    """
    DTO class representing the configuration of the MDP environnment of the attacker
    when facing a static defender policy
    """

    def __init__(self, env_name: str, stopping_game_config: StoppingGameConfig, defender_strategy_name,
                 stopping_game_name: str = "csle-stopping-game-v1"):
        """
        Initalizes the DTO

        :param env_name: the environment name
        :param stopping_game_config: the underlying stopping game config
        :param defender_strategy_name: the static defender strategy name
        :param stopping_game_name: the underlying stopping game name
        """
        super().__init__()
        self.env_name = env_name
        self.stopping_game_config = stopping_game_config
        self.defender_strategy_name = defender_strategy_name
        self.stopping_game_name = stopping_game_name

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "StoppingGameAttackerMdpConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = StoppingGameAttackerMdpConfig(
            stopping_game_config=StoppingGameConfig.from_dict(d["stopping_game_config"]),
            defender_strategy_name=d["defender_strategy_name"],
            stopping_game_name=d["stopping_game_name"], env_name=d["env_name"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["stopping_game_config"] = self.stopping_game_config.to_dict()
        d["defender_strategy_name"] = self.defender_strategy_name
        d["stopping_game_name"] = self.stopping_game_name
        d["env_name"] = self.env_name
        return d

    def __str__(self):
        """
        :return: a string representation of the object
        """
        return f"stopping_game_config: {self.stopping_game_config}, defender_strategy:{self.defender_strategy_name}, " \
               f"stopping_game_name:{self.stopping_game_name}, env_name: {self.env_name}"