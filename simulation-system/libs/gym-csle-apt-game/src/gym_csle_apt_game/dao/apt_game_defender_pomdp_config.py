from typing import Dict, Any
from gym_csle_apt_game.dao.apt_game_config import AptGameConfig
from csle_common.dao.simulation_config.simulation_env_input_config import SimulationEnvInputConfig
from csle_common.dao.training.policy import Policy
from csle_common.dao.training.random_policy import RandomPolicy
from csle_common.dao.training.multi_threshold_stopping_policy import MultiThresholdStoppingPolicy
from csle_common.dao.training.ppo_policy import PPOPolicy
from csle_common.dao.training.tabular_policy import TabularPolicy


class AptGameDefenderPomdpConfig(SimulationEnvInputConfig):
    """
    DTO class representing the configuration of the POMDP environnment of the defender
    when facing a static attacker policy
    """

    def __init__(self, env_name: str, apt_game_config: AptGameConfig, attacker_strategy: Policy,
                 apt_game_name: str = "csle-apt-game-v1"):
        """
        Initializes the DTO

        :param env_name: the environment name
        :param apt_game_config: The underlying apt game config
        :param attacker_strategy: the attacker's strategy name
        :param apt_game_name: the name of the underlying apt game
        """
        super().__init__()
        self.env_name = env_name
        self.apt_game_config = apt_game_config
        self.attacker_strategy = attacker_strategy
        self.apt_game_name = apt_game_name

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "AptGameDefenderPomdpConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        try:
            attacker_strategy = MultiThresholdStoppingPolicy.from_dict(d["attacker_strategy"])
        except Exception:
            try:
                attacker_strategy = RandomPolicy.from_dict(d["attacker_strategy"])
            except Exception:
                try:
                    attacker_strategy = PPOPolicy.from_dict(d["attacker_strategy"])
                except Exception:
                    attacker_strategy = TabularPolicy.from_dict(d["attacker_strategy"])

        obj = AptGameDefenderPomdpConfig(
            apt_game_config=AptGameConfig.from_dict(d["apt_game_config"]),
            attacker_strategy=attacker_strategy, apt_game_name=d["apt_game_name"],
            env_name=d["env_name"]
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["apt_game_config"] = self.apt_game_config.to_dict()
        d["attacker_strategy"] = self.attacker_strategy.to_dict()
        d["apt_game_name"] = self.apt_game_name
        d["env_name"] = self.env_name
        return d

    def __str__(self):
        """
        :return:  a string representation of the object
        """
        return f"APT stopping defender pomdp config; apt_game_config: {self.apt_game_config}, " \
               f"attacker_strategy: {self.attacker_strategy}, apt_game_name: {self.apt_game_name}," \
               f"env_name: {self.env_name}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "AptGameDefenderPomdpConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return AptGameDefenderPomdpConfig.from_dict(json.loads(json_str))
