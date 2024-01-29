from typing import Tuple, Dict, List, Any, Union
import numpy as np
import numpy.typing as npt
import time
import math
import csle_common.constants.constants as constants
from csle_common.dao.simulation_config.base_env import BaseEnv
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace
from gym_csle_apt_game.util.apt_game_util import AptGameUtil
from gym_csle_apt_game.dao.apt_game_config import AptGameConfig
from gym_csle_apt_game.dao.apt_game_state import AptGameState
import gym_csle_apt_game.constants.constants as env_constants


class AptGameEnv(BaseEnv):
    """
    OpenAI Gym Env for the csle-apt-game
    """

    def __init__(self, config: AptGameConfig):
        """
        Initializes the environment

        :param config: the environment configuration
        """
        self.config = config

        # Initialize environment state
        self.state = AptGameState(b1=self.config.b1)

        # Setup spaces
        self.attacker_observation_space = self.config.attacker_observation_space()
        self.defender_observation_space = self.config.defender_observation_space()
        self.attacker_action_space = self.config.attacker_action_space()
        self.defender_action_space = self.config.defender_action_space()

        self.action_space = self.defender_action_space
        self.observation_space = self.defender_observation_space

        # Setup traces
        self.traces: List[SimulationTrace] = []
        self.trace = SimulationTrace(simulation_env=self.config.env_name)

        # Reset
        self.reset()
        super().__init__()

    def step(self, action_profile: Tuple[int, Tuple[npt.NDArray[Any], int]]) \
            -> Tuple[
                Tuple[npt.NDArray[Any], Tuple[npt.NDArray[Any], int]], Tuple[int, int], bool, bool, Dict[str, Any]]:
        """
        Takes a step in the environment by executing the given action

        :param action_profile: the actions to take (both players actions
        :return: (obs, reward, terminated, truncated, info)
        """

        # Setup initial values
        a1, a2_profile = action_profile
        pi2, a2 = a2_profile
        assert pi2.shape[0] == len(self.config.S)
        assert pi2.shape[1] == len(self.config.A1)
        done = False
        info: Dict[str, Any] = {}

        # Compute c, s', b',o'
        c = self.config.C[a1][self.state.s]
        self.state.s = AptGameUtil.sample_next_state(a1=a1, a2=a2, T=self.config.T, S=self.config.S, s=self.state.s)
        o = AptGameUtil.sample_next_observation(Z=self.config.Z, O=self.config.O, s_prime=self.state.s)
        o_idx = list(self.config.O).index(o)
        self.state.b = AptGameUtil.next_belief(o=o_idx, a1=a1, b=self.state.b, pi2=pi2, config=self.config, a2=a2,
                                               s=self.state.s)

        # Update time-step
        self.state.t += 1

        # Populate info dict
        info[env_constants.ENV_METRICS.STATE] = self.state.s
        info[env_constants.ENV_METRICS.DEFENDER_ACTION] = a1
        info[env_constants.ENV_METRICS.ATTACKER_ACTION] = a2
        info[env_constants.ENV_METRICS.OBSERVATION] = o
        info[env_constants.ENV_METRICS.TIME_STEP] = self.state.t

        # Get observations
        attacker_obs = self.state.attacker_observation()
        defender_obs = self.state.defender_observation()

        # Log trace
        self.trace.defender_rewards.append(c)
        self.trace.attacker_rewards.append(-c)
        self.trace.attacker_actions.append(a2)
        self.trace.defender_actions.append(a1)
        self.trace.infos.append(info)
        self.trace.states.append(self.state.s)
        self.trace.beliefs.append(self.state.b)
        self.trace.infrastructure_metrics.append(o)
        if not done:
            self.trace.attacker_observations.append(attacker_obs)
            self.trace.defender_observations.append(defender_obs)

        # Populate info
        info = self._info(info)

        return (defender_obs, attacker_obs), (c, -c), done, done, info

    def mean(self, prob_vector):
        """
        Utility function for getting the mean of a vector

        :param prob_vector: the vector to take the mean of
        :return: the mean
        """
        m = 0
        for i in range(len(prob_vector)):
            m += prob_vector[i] * i
        return m

    def _info(self, info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adds the cumulative reward and episode length to the info dict

        :param info: the info dict to update
        :return: the updated info dict
        """
        R = 0
        for i in range(len(self.trace.defender_rewards)):
            R += self.trace.defender_rewards[i] * math.pow(self.config.gamma, i)
        info[env_constants.ENV_METRICS.RETURN] = sum(self.trace.defender_rewards)
        info[env_constants.ENV_METRICS.TIME_HORIZON] = len(self.trace.defender_actions)
        return info

    def reset(self, seed: Union[None, int] = None, soft: bool = False, options: Union[Dict[str, Any], None] = None) \
            -> Tuple[Tuple[npt.NDArray[Any], Tuple[npt.NDArray[Any], int]], Dict[str, Any]]:
        """
        Resets the environment state, this should be called whenever step() returns <done>

        :param seed: the random seed
        :param soft: boolean flag indicating whether it is a soft reset or not
        :param options: optional configuration parameters
        :return: initial observation and info
        """
        super().reset(seed=seed)
        self.state.reset()
        if len(self.trace.attacker_rewards) > 0:
            self.traces.append(self.trace)
        self.trace = SimulationTrace(simulation_env=self.config.env_name)
        attacker_obs = self.state.attacker_observation()
        defender_obs = self.state.defender_observation()
        self.trace.attacker_observations.append(attacker_obs)
        self.trace.defender_observations.append(defender_obs)
        info: Dict[str, Any] = {}
        return (defender_obs, attacker_obs), info

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
        return self.traces

    def reset_traces(self) -> None:
        """
        Resets the list of traces

        :return: None
        """
        self.traces = []

    def __checkpoint_traces(self) -> None:
        """
        Checkpoints agent traces
        :return: None
        """
        ts = time.time()
        SimulationTrace.save_traces(traces_save_dir=constants.LOGGING.DEFAULT_LOG_DIR,
                                    traces=self.traces, traces_file=f"taus{ts}.json")

    def set_model(self, model) -> None:
        """
        Sets the model. Useful when using RL frameworks where the stage policy is not easy to extract

        :param model: the model
        :return: None
        """
        self.model = model

    def set_state(self, state: Union[AptGameState, int]) -> None:
        """
        Sets the state. Allows to simulate samples from specific states

        :param state: the state
        :return: None
        """
        if isinstance(state, AptGameState):
            self.state = state
        elif type(state) is int or type(state) is np.int64:
            self.state.s = state
        else:
            raise ValueError(f"state: {state} not valid")

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
                print(f"Attacker space: {self.action_space}")
            elif raw_input == "S":
                print(self.state)
            elif raw_input == "D":
                print(done)
            elif raw_input == "H":
                print(self.trace)
            elif raw_input == "R":
                print("Resetting the state")
                self.reset()
            else:
                action_profile = raw_input
                parts = action_profile.split(",")
                a1 = int(parts[0])
                a2 = int(parts[1])
                stage_policy = []
                for s in self.config.S:
                    if s != 2:
                        dist = [0.0, 0.0]
                        dist[a2] = 1.0
                        stage_policy.append(dist)
                    else:
                        stage_policy.append([0.5, 0.5])
                pi2 = np.array(stage_policy)
                _, _, done, _, _ = self.step(action_profile=(a1, (pi2, a2)))
