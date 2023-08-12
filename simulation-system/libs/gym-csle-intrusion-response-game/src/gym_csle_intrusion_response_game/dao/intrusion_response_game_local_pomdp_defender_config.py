from typing import Dict, Any
from csle_common.dao.simulation_config.simulation_env_input_config import SimulationEnvInputConfig
from csle_common.dao.training.policy import Policy
from csle_common.dao.training.random_policy import RandomPolicy
from csle_common.dao.training.multi_threshold_stopping_policy import MultiThresholdStoppingPolicy
from csle_common.dao.training.ppo_policy import PPOPolicy
from csle_common.dao.training.tabular_policy import TabularPolicy
from csle_common.dao.training.linear_threshold_stopping_policy import LinearThresholdStoppingPolicy
from csle_common.dao.training.linear_tabular_policy import LinearTabularPolicy
from csle_common.dao.training.mixed_linear_tabular import MixedLinearTabularPolicy
from csle_common.dao.training.mixed_ppo_policy import MixedPPOPolicy
from gym_csle_intrusion_response_game.dao.local_intrusion_response_game_config import LocalIntrusionResponseGameConfig


class IntrusionResponseGameLocalPOMDPDefenderConfig(SimulationEnvInputConfig):
    """
    DTO class representing the configuration of the local POMDP environment of the defender for a specific node
    when facing a static attacker strategy
    """

    def __init__(self, env_name: str, local_intrusion_response_game_config: LocalIntrusionResponseGameConfig,
                 attacker_strategy: Policy, defender_strategy: Policy = None):
        """
        Initializes the DTO

        :param env_name: the environment name
        :param local_intrusion_response_game_config: The underlying game config
        :param attacker_strategy: the attacker's strategy name
        """
        super().__init__()
        self.env_name = env_name
        self.local_intrusion_response_game_config = local_intrusion_response_game_config
        self.attacker_strategy = attacker_strategy
        self.defender_strategy = defender_strategy
        self.stopping_action = 3
        self.stopping_zone = 3

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "IntrusionResponseGameLocalPOMDPDefenderConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        attacker_strategy = None
        parse_functions = [MultiThresholdStoppingPolicy.from_dict, RandomPolicy.from_dict, PPOPolicy.from_dict,
                           TabularPolicy.from_dict, MixedLinearTabularPolicy.from_dict, MixedPPOPolicy.from_dict,
                           LinearTabularPolicy.from_dict, LinearThresholdStoppingPolicy.from_dict]
        for parse_fun in parse_functions:
            try:
                attacker_strategy = parse_fun(d["attacker_strategy"])
                break
            except Exception:
                pass
        if attacker_strategy is None:
            raise ValueError("Could not parse the attacker strategy")

        obj = IntrusionResponseGameLocalPOMDPDefenderConfig(
            local_intrusion_response_game_config=LocalIntrusionResponseGameConfig.from_dict(
                d["local_intrusion_response_game_config"]),
            attacker_strategy=attacker_strategy, env_name=d["env_name"])
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["local_intrusion_response_game_config"] = self.local_intrusion_response_game_config.to_dict()
        d["attacker_strategy"] = self.attacker_strategy.to_dict()
        d["env_name"] = self.env_name
        return d

    def __str__(self) -> str:
        """
        :return:  a string representation of the object
        """
        return f"local_intrusion_response_game_config: {self.local_intrusion_response_game_config}, " \
               f"attacker_strategy: {self.attacker_strategy}," \
               f"env_name: {self.env_name}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "IntrusionResponseGameLocalPOMDPDefenderConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return IntrusionResponseGameLocalPOMDPDefenderConfig.from_dict(json.loads(json_str))
