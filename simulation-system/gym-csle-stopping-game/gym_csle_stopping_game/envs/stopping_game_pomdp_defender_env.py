from typing import Tuple

import gym
import numpy as np
from csle_common.dao.simulation_config.base_env import BaseEnv
from gym_csle_stopping_game.dao.stopping_game_defender_pomdp_config import StoppingGameDefenderPomdpConfig


class StoppingGamePomdpDefenderEnv(BaseEnv):
    """
    OpenAI Gym Env for the MDP of the defender when facing a static attacker
    """

    def __init__(self, config: StoppingGameDefenderPomdpConfig):
        self.config = config
        self.stopping_game_env = gym.make(self.config.stopping_game_name, config=self.config.stopping_game_config)

        # Setup spaces
        self.defender_observation_space = self.config.stopping_game_config.defender_observation_space()
        self.defender_action_space = self.config.stopping_game_config.defender_action_space()

        # Setup Config
        self.viewer = None
        self.metadata = {
            'render.modes': ['human', 'rgb_array'],
            'video.frames_per_second': 50  # Video rendering speed
        }

        self.latest_attacker_obs = None
        # Reset
        self.reset()
        super().__init__()

    def step(self, a1: int) -> Tuple[np.ndarray, int, bool, dict]:
        """
        Takes a step in the environment by executing the given action

        :param a1: defender action
        :return: (obs, reward, done, info)
        """
        # Get defender action from static strategy
        pi2 = self.config.attacker_strategy(self.latest_attacker_obs, self.config.stopping_game_config)

        # Step the game
        o, r, d, info = self.stopping_game_env.step((a1, pi2))
        self.latest_attacker_obs = o[1]
        defender_obs = o[0]

        return defender_obs, r[0], d, info

    def reset(self, soft : bool = False) -> Tuple[np.ndarray, np.ndarray]:
        """
        Resets the environment state, this should be called whenever step() returns <done>

        :return: initial observation
        """
        o = self.stopping_game_env.reset()
        self.latest_attacker_obs = o[1]
        defender_obs = o[0]
        return defender_obs

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

    def close(self) -> None:
        """
        Closes the viewer (cleanup)
        :return: None
        """
        if self.viewer:
            self.viewer.close()
            self.viewer = None
