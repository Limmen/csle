from typing import Tuple, List, Dict, Any, Union
import numpy as np
import numpy.typing as npt
import torch
import math
from csle_common.dao.simulation_config.base_env import BaseEnv
from csle_common.dao.training.mixed_multi_threshold_stopping_policy import MixedMultiThresholdStoppingPolicy
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace
from gym_csle_apt_game.dao.apt_game_attacker_mdp_config import AptGameAttackerMdpConfig
from gym_csle_apt_game.util.apt_game_util import AptGameUtil
from gym_csle_apt_game.envs.apt_game_env import AptGameEnv


class AptGameMdpAttackerEnv(BaseEnv):
    """
    OpenAI Gym Env for the MDP of the attacker when facing a static defender
    """

    def __init__(self, config: AptGameAttackerMdpConfig):
        """
        Initializes the environment

        :param config: the configuration of the environment
        """
        self.config = config
        self.apt_game_env: AptGameEnv = AptGameEnv(config=self.config.apt_game_config)

        # Setup spaces
        self.observation_space = self.config.apt_game_config.attacker_observation_space()
        self.action_space = self.config.apt_game_config.attacker_action_space()

        # Setup static defender
        self.static_defender_strategy = self.config.defender_strategy

        # Setup Config
        self.viewer: Union[None, Any] = None
        self.metadata = {
            'render.modes': ['human', 'rgb_array'],
            'video.frames_per_second': 50  # Video rendering speed
        }

        self.latest_defender_obs: Union[None, List[Any], npt.NDArray[Any]] = None
        self.latest_attacker_obs: Union[None, List[Any], npt.NDArray[Any], Tuple[npt.NDArray[Any], int]] = None
        self.model: Union[None, Any] = None

        # Reset
        self.reset()
        super().__init__()

    def step(self, pi2: Union[npt.NDArray[Any], int, float, int, np.float64]) \
            -> Tuple[npt.NDArray[Any], int, bool, bool, Dict[str, Any]]:
        """
        Takes a step in the environment by executing the given action

        :param pi2: attacker stage policy
        :return: (obs, reward, terminated, truncated, info)
        """
        if (type(pi2) is int or type(pi2) is float or type(pi2) is np.int64 or type(pi2) is np.int32 # type: ignore
                or type(pi2) is np.float64): # type: ignore
            a2 = pi2
            if self.latest_attacker_obs is None:
                raise ValueError("Attacker observation is None")
            pi2 = self.calculate_stage_policy(o=list(self.latest_attacker_obs), a2=int(a2))
        else:
            if self.model is not None:
                if self.latest_attacker_obs is None:
                    raise ValueError("Attacker observation is None")
                pi2 = self.calculate_stage_policy(o=list(self.latest_attacker_obs))
                a2 = AptGameUtil.sample_attacker_action(pi2=pi2, s=self.apt_game_env.state.s)
            else:
                pi2 = np.array(pi2)
                try:
                    if self.latest_attacker_obs is None:
                        raise ValueError("Attacker observation is None")
                    pi2 = self.calculate_stage_policy(o=list(self.latest_attacker_obs))
                except Exception:
                    pass
                a2 = AptGameUtil.sample_attacker_action(pi2=pi2, s=self.apt_game_env.state.s)

        assert pi2.shape[0] == len(self.config.apt_game_config.S)
        assert pi2.shape[1] == len(self.config.apt_game_config.A1)

        # Get defender action from static strategy
        a1 = self.static_defender_strategy.action(o=self.latest_defender_obs)

        # Step the game
        o, r, d, _, info = self.apt_game_env.step((int(a1), (pi2, int(a2))))
        self.latest_defender_obs = o[0]
        self.latest_attacker_obs = o[1]
        attacker_obs = o[1]
        attacker_obs_prime = np.array([1, sum(attacker_obs[0][1:]), 0])
        return attacker_obs_prime, r[0], d, d, info

    def reset(self, seed: Union[int, None] = None, soft: bool = False, options: Union[Dict[str, Any], None] = None) \
            -> Tuple[npt.NDArray[Any], Dict[str, Any]]:
        """
        Resets the environment state, this should be called whenever step() returns <done>

        :param seed: the random seed
        :param soft: boolean flag indicating whether it is a soft reset or not
        :param options: optional configuration parameters
        :return: initial observation
        """
        o, _ = self.apt_game_env.reset()
        self.latest_defender_obs = o[0]
        self.latest_attacker_obs = o[1]
        attacker_obs = o[1]
        attacker_obs_prime = np.array([1, sum(attacker_obs[0][1:]), 0])
        info: Dict[str, Any] = {}
        return attacker_obs_prime, info

    def set_model(self, model) -> None:
        """
        Sets the model. Useful when using RL frameworks where the stage policy is not easy to extract

        :param model: the model
        :return: None
        """
        self.model = model

    def set_state(self, state: Any) -> None:
        """
        Sets the state. Allows to simulate samples from specific states

        :param state: the state
        :return: None
        """
        self.apt_game_env.set_state(state=state)

    def calculate_stage_policy(self, o: List[Any], a2: int = 0) -> npt.NDArray[Any]:
        """
        Calculates the stage policy of a given model and observation

        :param o: the observation
        :return: the stage policy
        """
        if self.model is None:
            stage_policy = []
            for s in self.config.apt_game_config.S:
                if s != 2:
                    dist = [0.0, 0.0]
                    dist[a2] = 1.0
                    stage_policy.append(dist)
                else:
                    stage_policy.append([0.5, 0.5])
            return np.array(stage_policy)
        if isinstance(self.model, MixedMultiThresholdStoppingPolicy):
            return np.array(self.model.stage_policy(o=o))
        else:
            b1 = o[1]
            l = int(o[0])
            stage_policy = []
            for s in self.config.apt_game_config.S:
                if s != 2:
                    o = [l, b1, s]
                    stage_policy.append(self._get_attacker_dist(obs=o))
                else:
                    stage_policy.append([0.5, 0.5])
            return np.array(stage_policy)

    def _get_attacker_dist(self, obs: List[Any]) -> List[float]:
        """
        Utility function for getting the attacker's action distribution based on a given observation

        :param obs: the given observation
        :return:  the action distribution
        """
        np_obs = np.array([obs])
        if self.model is None:
            raise ValueError("Model is None")
        actions, values, log_prob = self.model.policy.forward(obs=torch.tensor(np_obs).to(self.model.device))
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
        return self.apt_game_env.get_traces()

    def reset_traces(self) -> None:
        """
        Resets the list of traces

        :return: None
        """
        return self.apt_game_env.reset_traces()

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
                print(self.apt_game_env.state)
            elif raw_input == "D":
                print(done)
            elif raw_input == "H":
                print(self.apt_game_env.trace)
            elif raw_input == "R":
                print("Resetting the state")
                self.reset()
            else:
                action_idx = int(raw_input)
                _, _, done, _, _ = self.step(pi2=action_idx)
