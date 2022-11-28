from typing import Tuple, List, Union
import gym
import numpy as np
import torch
import math
from csle_common.dao.simulation_config.base_env import BaseEnv
from csle_common.dao.training.mixed_multi_threshold_stopping_policy import MixedMultiThresholdStoppingPolicy
from gym_csle_stopping_game.dao.stopping_game_attacker_mdp_config import StoppingGameAttackerMdpConfig
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil
import gym_csle_stopping_game.constants.constants as env_constants


class StoppingGameMdpAttackerEnv(BaseEnv):
    """
    OpenAI Gym Env for the MDP of the attacker when facing a static defender
    """

    def __init__(self, config: StoppingGameAttackerMdpConfig):
        """
        Initializes the environment

        :param config: the configuration of the environment
        """
        self.config = config
        self.stopping_game_env = gym.make(self.config.stopping_game_name, config=self.config.stopping_game_config)

        # Setup spaces
        self.observation_space = self.config.stopping_game_config.attacker_observation_space()
        self.action_space = self.config.stopping_game_config.attacker_action_space()

        # Setup static defender
        self.static_defender_strategy = self.config.defender_strategy

        # Setup Config
        self.viewer = None
        self.metadata = {
            'render.modes': ['human', 'rgb_array'],
            'video.frames_per_second': 50  # Video rendering speed
        }

        self.latest_defender_obs = None
        self.latest_attacker_obs = None
        self.model = None

        # Reset
        self.reset()
        super().__init__()

    def step(self, pi2: Union[List[List[float]], int, float, np.int64, np.float]) \
            -> Tuple[np.ndarray, int, bool, dict]:
        """
        Takes a step in the environment by executing the given action

        :param pi2: attacker stage policy
        :return: (obs, reward, done, info)
        """
        if type(pi2) is int or type(pi2) is float or type(pi2) is np.int64 or type(pi2) is np.float:
            a2 = pi2
            pi2 = self.calculate_stage_policy(o=self.latest_attacker_obs, a2=a2)
        else:
            if self.model is not None:
                pi2 = self.calculate_stage_policy(o=self.latest_attacker_obs)
                a2 = StoppingGameUtil.sample_attacker_action(pi2=pi2, s=self.stopping_game_env.state.s)
            else:
                pi2 = np.array(pi2)
                if (not pi2.shape[0] == len(self.config.stopping_game_config.S)
                        or pi2.shape[1] != len(self.config.stopping_game_config.A1)) and self.model is not None:
                    pi2 = self.calculate_stage_policy(o=self.latest_attacker_obs)
                a2 = StoppingGameUtil.sample_attacker_action(pi2=pi2, s=self.stopping_game_env.state.s)

        # a2 = pi2
        # pi2 = np.array([
        #     [0.5,0.5],
        #     [0.5,0.5],
        #     [0.5,0.5]
        # ])
        assert pi2.shape[0] == len(self.config.stopping_game_config.S)
        assert pi2.shape[1] == len(self.config.stopping_game_config.A1)

        # Get defender action from static strategy
        a1 = self.static_defender_strategy.action(o=self.latest_defender_obs)

        # Step the game
        o, r, d, info = self.stopping_game_env.step((a1, (pi2, a2)))
        self.latest_defender_obs = o[0]
        self.latest_attacker_obs = o[1]
        attacker_obs = o[1]

        info[env_constants.ENV_METRICS.RETURN] = -info[env_constants.ENV_METRICS.RETURN]
        info[env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN] = \
            -info[env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN]

        return attacker_obs, r[1], d, info

    def reset(self, soft: bool = False) -> Tuple[np.ndarray, np.ndarray]:
        """
        Resets the environment state, this should be called whenever step() returns <done>

        :return: initial observation
        """
        o = self.stopping_game_env.reset()
        self.latest_defender_obs = o[0]
        self.latest_attacker_obs = o[1]
        attacker_obs = o[1]
        return attacker_obs

    def set_model(self, model) -> None:
        """
        Sets the model. Useful when using RL frameworks where the stage policy is not easy to extract

        :param model: the model
        :return: None
        """
        self.model = model

    def calculate_stage_policy(self, o: List, a2: int = 0) -> np.ndarray:
        """
        Calculates the stage policy of a given model and observation

        :param o: the observation
        :return: the stage policy
        """
        if self.model is None:
            stage_policy = []
            for s in self.config.stopping_game_config.S:
                if s != 2:
                    dist = [0, 0]
                    dist[a2] = 1
                    stage_policy.append(dist)
                else:
                    stage_policy.append([0.5, 0.5])
            return np.array(stage_policy)
        if isinstance(self.model, MixedMultiThresholdStoppingPolicy):
            stage_policy = np.array(self.model.stage_policy(o=o))
            return stage_policy
        else:
            b1 = o[1]
            l = int(o[0])
            stage_policy = []
            for s in self.config.stopping_game_config.S:
                if s != 2:
                    o = [l, b1, s]
                    stage_policy.append(self._get_attacker_dist(obs=o))
                else:
                    stage_policy.append([0.5, 0.5])
            stage_policy = np.array(stage_policy)
            return stage_policy

    def _get_attacker_dist(self, obs: List) -> List:
        """
        Utility function for getting the attacker's action distribution based on a given observation

        :param obs: the given observation
        :return:  the action distribution
        """
        obs = np.array([obs])
        actions, values, log_prob = self.model.policy.forward(obs=torch.tensor(obs).to(self.model.device))
        action = actions[0]
        if action == 1:
            stop_prob = math.exp(log_prob)
        else:
            stop_prob = 1 - math.exp(log_prob)
        return [1 - stop_prob, stop_prob]

    def render(self, mode: str = 'human'):
        """
        Renders the environment.  Supported rendering modes: (1) human; and (2) rgb_array

        :param mode: the rendering mode
        :return: True (if human mode) otherwise an rgb array
        """
        raise NotImplementedError("Rendering is not implemented for this environment")

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

    def manual_play(self) -> None:
        """
        An interactive loop to test the environment manually

        :return: None
        """
        done = False
        while True:
            raw_input = input("> ")
            raw_input = raw_input.strip()
            if raw_input == "help":
                print("Enter an action id to execute the action, "
                      "press R to reset,"
                      "press S to print the state, press A to print the actions, "
                      "press D to check if done"
                      "press H to print the history of actions")
            elif raw_input == "A":
                print(f"Action space: {self.action_space}")
            elif raw_input == "S":
                print(self.stopping_game_env.state)
            elif raw_input == "D":
                print(done)
            elif raw_input == "H":
                print(self.stopping_game_env.trace)
            elif raw_input == "R":
                print("Resetting the state")
                self.reset()
            else:
                action_idx = int(raw_input)
                _, _, done, _ = self.step(pi2=action_idx)
