from typing import Dict, Any, List
from csle_common.dao.training.policy import Policy
from csle_common.dao.training.random_policy import RandomPolicy
from csle_common.dao.training.multi_threshold_stopping_policy import MultiThresholdStoppingPolicy
from csle_common.dao.training.ppo_policy import PPOPolicy
from csle_common.dao.training.tabular_policy import TabularPolicy
from gym_csle_intrusion_response_game.dao.workflow_intrusion_response_game_config \
    import WorkflowIntrusionResponseGameConfig
from csle_common.dao.simulation_config.simulation_env_input_config import SimulationEnvInputConfig


class WorkflowIntrusionResponsePOMDPDefenderConfig(SimulationEnvInputConfig):
    """
    DTO representing the configuration of a workflow intrusion response POMDP when the defender faces a static
    defender opponent
    """

    def __init__(self, env_name: str, game_config: WorkflowIntrusionResponseGameConfig,
                 attacker_strategies: List[Policy]):
        """
        Initializes teh DTO

        :param env_name: the name of the environment
        :param game_config: the workflow game configuration
        :param attacker_strategies: the list of attacker strategies for the local nodes in the workflow game
        """
        super().__init__()
        self.env_name = env_name
        self.game_config = game_config
        self.attacker_strategies = attacker_strategies

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation

        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["env_name"] = self.env_name
        d["game_config"] = self.game_config.to_dict()
        d["attacker_strategies"] = list(map(lambda x: x.to_dict(), self.attacker_strategies))
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "WorkflowIntrusionResponsePOMDPDefenderConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        attacker_strategies = []
        parse_functions = [MultiThresholdStoppingPolicy.from_dict, RandomPolicy.from_dict, PPOPolicy.from_dict,
                           TabularPolicy.from_dict]
        for strategy in d["attacker_strategies"]:
            for parse_fun in parse_functions:
                try:
                    attacker_strategy = parse_fun(strategy)
                    attacker_strategies.append(attacker_strategy)
                    break
                except Exception:
                    pass
            if attacker_strategies is None:
                raise ValueError("Could not parse the attacker strategy")

        obj = WorkflowIntrusionResponsePOMDPDefenderConfig(
            env_name=d["env_name"], game_config=WorkflowIntrusionResponseGameConfig.from_dict(d["game_config"]),
            attacker_strategies=attacker_strategies)
        return obj

    @staticmethod
    def from_json_file(json_file_path: str) -> "WorkflowIntrusionResponsePOMDPDefenderConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return WorkflowIntrusionResponsePOMDPDefenderConfig.from_dict(json.loads(json_str))
