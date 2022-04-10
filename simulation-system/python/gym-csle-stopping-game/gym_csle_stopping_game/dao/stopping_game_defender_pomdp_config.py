from typing import Dict, Any
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig
from csle_common.dao.simulation_config.simulation_env_input_config import SimulationEnvInputConfig


class StoppingGameDefenderPomdpConfig(SimulationEnvInputConfig):
    """
    DTO class representing the configuration of the POMDP environnment of the defender
    when facing a static attacker policy
    """

    def __init__(self, env_name: str, stopping_game_config: StoppingGameConfig, attacker_strategy_name,
                 stopping_game_name: str = "csle-stopping-game-v1"):
        """
        Initializes the DTO

        :param env_name: the environment name
        :param stopping_game_config: The underlying stopping game config
        :param attacker_strategy_name: the attacker's strategy name
        :param stopping_game_name: the name of the underlying stopping game
        """
        super().__init__()
        self.env_name = env_name
        self.stopping_game_config = stopping_game_config
        self.attacker_strategy_name = attacker_strategy_name
        self.stopping_game_name = stopping_game_name

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "StoppingGameDefenderPomdpConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = StoppingGameDefenderPomdpConfig(
            stopping_game_config=StoppingGameConfig.from_dict(d["stopping_game_config"]),
            attacker_strategy_name=d["attacker_strategy_name"], stopping_game_name=d["stopping_game_name"],
            env_name=d["env_name"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["stopping_game_config"] = self.stopping_game_config.to_dict()
        d["attacker_strategy_name"] = self.attacker_strategy_name
        d["stopping_game_name"] = self.stopping_game_name
        d["env_name"] = self.env_name
        return d

    def __str__(self):
        """
        :return:  a string representation of the object
        """
        return f"stopping_game_config: {self.stopping_game_config}, " \
               f"attacker_strategy_name: {self.attacker_strategy_name}, stopping_game_name: {self.stopping_game_name}," \
               f"env_name: {self.env_name}"