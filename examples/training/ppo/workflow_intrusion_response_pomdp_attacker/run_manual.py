import numpy as np
import gym
from csle_common.metastore.metastore_facade import MetastoreFacade
import gym_csle_intrusion_response_game.constants.constants as env_constants
from gym_csle_intrusion_response_game.util.intrusion_response_game_util import IntrusionResponseGameUtil
from gym_csle_intrusion_response_game.dao.local_intrusion_response_game_config import LocalIntrusionResponseGameConfig
from csle_common.dao.training.tabular_policy import TabularPolicy
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.player_type import PlayerType

if __name__ == '__main__':
    simulation_env_config = MetastoreFacade.get_simulation_by_name(
        "csle-intrusion-response-game-workflow-pomdp-attacker-001")
    env = gym.make("csle-intrusion-response-game-workflow-pomdp-attacker-v1",
                   config=simulation_env_config.simulation_env_input_config)
    env.manual_play()
