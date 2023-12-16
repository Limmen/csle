from typing import Dict, Any
from gym_csle_apt_game.dao.apt_game_config import AptGameConfig
from csle_common.dao.simulation_config.simulation_env_input_config import SimulationEnvInputConfig
from csle_common.dao.training.policy import Policy
from csle_common.dao.training.random_policy import RandomPolicy
from csle_common.dao.training.multi_threshold_stopping_policy import MultiThresholdStoppingPolicy
from csle_common.dao.training.ppo_policy import PPOPolicy


class AptGameAttackerMdpConfig(SimulationEnvInputConfig):
    """
    DTO class representing the configuration of the MDP environnment of the attacker
    when facing a static defender policy
    """

    def __init__(self, env_name: str, apt_game_config: AptGameConfig, defender_strategy: Policy,
                 apt_game_name: str = "csle-apt-game-v1"):
        """
        Initializes the DTO

        :param env_name: the environment name
        :param apt_game_config: the underlying apt game config
        :param defender_strategy: the static defender strategy name
        :param apt_game_name: the underlying apt game name
        """
        super().__init__()
        self.env_name = env_name
        self.apt_game_config = apt_game_config
        self.defender_strategy = defender_strategy
        self.apt_game_name = apt_game_name

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AptGameAttackerMdpConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        try:
            defender_strategy = MultiThresholdStoppingPolicy.from_dict(d["defender_strategy"])
        except Exception:
            try:
                defender_strategy = RandomPolicy.from_dict(d["defender_strategy"])
            except Exception:
                defender_strategy = PPOPolicy.from_dict(d["defender_strategy"])
        obj = AptGameAttackerMdpConfig(
            apt_game_config=AptGameConfig.from_dict(d["apt_game_config"]),
            defender_strategy=defender_strategy,
            apt_game_name=d["apt_game_name"], env_name=d["env_name"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["apt_game_config"] = self.apt_game_config.to_dict()
        d["defender_strategy"] = self.defender_strategy.to_dict()
        d["apt_game_name"] = self.apt_game_name
        d["env_name"] = self.env_name
        return d

    def __str__(self):
        """
        :return: a string representation of the object
        """
        return f"apt_game_config: {self.apt_game_config}, defender_strategy:{self.defender_strategy}, " \
               f"apt_game_name:{self.apt_game_name}, env_name: {self.env_name}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "AptGameAttackerMdpConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return AptGameAttackerMdpConfig.from_dict(json.loads(json_str))
