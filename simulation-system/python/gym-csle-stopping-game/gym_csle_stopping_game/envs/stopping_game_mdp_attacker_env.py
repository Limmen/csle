from typing import Tuple, List
import gym
import numpy as np
from csle_common.dao.simulation_config.base_env import BaseEnv
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil
from gym_csle_stopping_game.dao.stopping_game_attacker_mdp_config import StoppingGameAttackerMdpConfig
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace


class StoppingGameMdpAttackerEnv(BaseEnv):
    """
    OpenAI Gym Env for the MDP of the attacker when facing a static defender
    """

    def __init__(self, config: StoppingGameAttackerMdpConfig):
        self.config = config
        self.stopping_game_env = gym.make(self.config.stopping_game_name, config=self.config.stopping_game_config)

        # Setup spaces
        self.observation_space = self.config.stopping_game_config.attacker_observation_space()
        self.action_space = self.config.stopping_game_config.attacker_action_space()

        # Setup static defender
        self.static_defender_strategy = StoppingGameUtil.get_static_defender_strategy(
            defender_strategy_name=self.config.defender_strategy_name)

        # Setup Config
        self.viewer = None
        self.metadata = {
            'render.modes': ['human', 'rgb_array'],
            'video.frames_per_second': 50  # Video rendering speed
        }

        self.latest_defender_obs = None
        # Reset
        self.reset()
        super().__init__()

    def step(self, pi2 : List[List[float]]) -> Tuple[np.ndarray, int, bool, dict]:
        """
        Takes a step in the environment by executing the given action

        :param pi2: attacker stage policy
        :return: (obs, reward, done, info)
        """
        pi2 = np.array(pi2)
        assert pi2.shape[0] == len(self.config.stopping_game_config.S)
        assert pi2.shape[1] == len(self.config.stopping_game_config.A1)

        # Get defender action from static strategy
        a1, _ = self.static_defender_strategy.action(o=self.latest_defender_obs)

        # Step the game
        o, r, d, info = self.stopping_game_env.step((a1, pi2))
        self.latest_defender_obs = o[0]
        attacker_obs = o[1]

        return attacker_obs, r[1], d, info

    def reset(self, soft : bool = False) -> Tuple[np.ndarray, np.ndarray]:
        """
        Resets the environment state, this should be called whenever step() returns <done>

        :return: initial observation
        """
        o = self.stopping_game_env.reset()
        self.latest_defender_obs = o[0]
        attacker_obs = o[1]
        return attacker_obs

    def render(self, mode: str = 'human'):
        """
        Renders the environment
        Supported rendering modes:
          -human: render to the current display or terminal and return nothing. Usually for human consumption.
          -rgb_array: Return an numpy.ndarray with shape (x, y, 3),
                      representing RGB values for an x-by-y pixel image, suitable
                      for turning into a video.
        :param mode: the rendering mode
        :return: True (if human mode) otherwise an rgb array
        """
        raise NotImplemented("Rendering is not implemented for this environment")

    def is_defense_action_legal(self, defense_action_id: int) -> bool:
        """
        Checks whether a defender action in the environment is legal or not

        :param defense_action_id: the id of the action
        :return: True or False
        """
        return True

    def is_attack_action_legal(self, attack_action_id: int) -> bool:
        """
        Checks whether an attacker action in the environment is legal or not

        :param attack_action_id: the id of the attacker action
        :return: True or False
        """
        return True

    def get_traces(self) -> List[SimulationTrace]:
        """
        :return: the list of simulation traces
        """
        return self.stopping_game_env.get_traces()

    def reset_traces(self) -> None:
        """
        Resets the list of traces

        :return: None
        """
        return self.stopping_game_env.reset_traces()

    def close(self) -> None:
        """
        Closes the viewer (cleanup)
        :return: None
        """
        if self.viewer:
            self.viewer.close()
            self.viewer = None
