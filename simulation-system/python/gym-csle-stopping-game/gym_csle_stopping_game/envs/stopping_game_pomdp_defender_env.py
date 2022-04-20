from typing import Tuple, List, Callable
import gym
import numpy as np
from csle_common.dao.simulation_config.base_env import BaseEnv
from gym_csle_stopping_game.dao.stopping_game_defender_pomdp_config import StoppingGameDefenderPomdpConfig
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace
from csle_common.dao.training.policy import Policy
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.emulation_config.emulation_simulation_trace import EmulationSimulationTrace
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from gym_csle_stopping_game.envs.stopping_game_env import StoppingGameEnv


class StoppingGamePomdpDefenderEnv(BaseEnv):
    """
    OpenAI Gym Env for the MDP of the defender when facing a static attacker
    """

    def __init__(self, config: StoppingGameDefenderPomdpConfig, attacker_strategy: Callable = None):
        """
        Initializes the environment

        :param config: the environment configuration
        :param attacker_strategy: the strategy of the static attacker
        """

        self.config = config
        self.stopping_game_env = gym.make(self.config.stopping_game_name, config=self.config.stopping_game_config)

        # Setup spaces
        self.observation_space = self.config.stopping_game_config.defender_observation_space()
        self.action_space = self.config.stopping_game_config.defender_action_space()

        # Setup static attacker strategy
        if attacker_strategy is None:
            self.static_attacker_strategy = StoppingGameUtil.get_static_attacker_strategy(
                attacker_strategy_name=self.config.attacker_strategy_name)
        else:
            self.static_attacker_strategy = attacker_strategy

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
        pi2 = self.static_attacker_strategy.action(self.latest_attacker_obs)

        # Step the game
        o, r, d, info = self.stopping_game_env.step((a1, pi2))
        self.latest_attacker_obs = o[1]
        defender_obs = o[0]

        return defender_obs, r[0], d, info

    def reset(self, soft : bool = False) -> np.ndarray:
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

    @staticmethod
    def emulation_evaluation(env: "StoppingGamePomdpDefenderEnv",
                             n_episodes: int, intrusion_seq: List[EmulationAttackerAction],
                             defender_policy: Policy,
                             emulation_env_config: EmulationEnvConfig, simulation_env_config: SimulationEnvConfig) \
            -> List[EmulationSimulationTrace]:
        return StoppingGameEnv.emulation_evaluation(
            env=env.stopping_game_env, n_episodes=n_episodes, intrusion_seq=intrusion_seq,
            defender_policy=defender_policy, attacker_policy=env.static_attacker_strategy,
            emulation_env_config=emulation_env_config,  simulation_env_config=simulation_env_config)

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
