from typing import Dict, Any, List
from csle_common.dao.training.policy import Policy
from csle_common.dao.training.random_policy import RandomPolicy
from csle_common.dao.training.multi_threshold_stopping_policy import MultiThresholdStoppingPolicy
from csle_common.dao.training.ppo_policy import PPOPolicy
from csle_common.dao.training.tabular_policy import TabularPolicy
from gym_csle_intrusion_response_game.dao.workflow_intrusion_response_game_config \
    import WorkflowIntrusionResponseGameConfig
from csle_common.dao.simulation_config.simulation_env_input_config import SimulationEnvInputConfig


class WorkflowIntrusionResponsePOMDPAttackerConfig(SimulationEnvInputConfig):
    """
    DTO representing the configuration of a workflow intrusion response POMDP when the attacker faces a static
    defender opponent
    """

    def __init__(self, env_name: str, game_config: WorkflowIntrusionResponseGameConfig,
                 defender_strategies: List[Policy]):
        """
        Initializes teh DTO

        :param env_name: the name of the environment
        :param game_config: the workflow game configuration
        :param defender_strategies: the list of defender strategies for the local nodes in the workflow game
        """
        super().__init__()
        self.env_name = env_name
        self.game_config = game_config
        self.defender_strategies = defender_strategies

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["env_name"] = self.env_name
        d["game_config"] = self.game_config.to_dict()
        d["defender_strategies"] = list(map(lambda x: x.to_dict(), self.defender_strategies))
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "WorkflowIntrusionResponsePOMDPAttackerConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        defender_strategies = []
        parse_functions = [MultiThresholdStoppingPolicy.from_dict, RandomPolicy.from_dict, PPOPolicy.from_dict,
                           TabularPolicy.from_dict]
        for strategy in d["defender_strategies"]:
            for parse_fun in parse_functions:
                try:
                    defender_strategy = parse_fun(strategy)
                    defender_strategies.append(defender_strategy)
                    break
                except Exception:
                    pass
            if defender_strategies is None:
                raise ValueError("Could not parse the defender strategy")

        obj = WorkflowIntrusionResponsePOMDPAttackerConfig(
            env_name=d["env_name"], game_config=WorkflowIntrusionResponseGameConfig.from_dict(d["game_config"]),
            defender_strategies=defender_strategies)
        return obj

    @staticmethod
    def from_json_file(json_file_path: str) -> "WorkflowIntrusionResponsePOMDPAttackerConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return WorkflowIntrusionResponsePOMDPAttackerConfig.from_dict(json.loads(json_str))
