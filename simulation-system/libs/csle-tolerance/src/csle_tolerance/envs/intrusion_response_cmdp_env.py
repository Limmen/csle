from typing import Tuple, Any, Dict, Union, List
import math
import time
import gymnasium as gym
import numpy as np
from csle_common.dao.simulation_config.base_env import BaseEnv
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace
import csle_common.constants.constants as constants
from csle_tolerance.dao.intrusion_response_cmdp_config import IntrusionResponseCmdpConfig
from csle_tolerance.util.general_util import GeneralUtil
import csle_tolerance.constants.constants as env_constants


class IntrusionResponseCmdpEnv(BaseEnv):
    """
    Gym Environment representing the intrusion response CMDP
    """

    def __init__(self, config: IntrusionResponseCmdpConfig):
        """
        Initializes the environment

        :param config: the environment configuration
        """
        self.config = config

        # Setup spaces
        self.action_space = gym.spaces.Discrete(len(self.config.actions))
        self.observation_space = gym.spaces.Box(low=np.int32(min(self.config.states)),
                                                high=np.int32(max(self.config.states)), dtype=np.int32, shape=(1,))

        # Initialize state
        self.t = 1
        self.s = self.config.initial_state

        # Setup traces
        self.traces: List[SimulationTrace] = []
        self.trace = SimulationTrace(simulation_env=self.config.gym_env_name)

        # Reset
        self.reset()
        super().__init__()

    def step(self, a: int) -> Tuple[int, float, bool, bool, Dict[str, Any]]:
        """
        Takes a step in the environment by executing the given action

        :param a: the action
        :return: (obs, reward, terminated, truncated, info)
        """
        done = False

        # Cost
        c = self.config.cost_tensor[self.s]

        # Sample next state
        self.s = GeneralUtil.sample_next_state(transition_tensor=self.config.transition_tensor,
                                               s=self.s, a=a, states=self.config.states)

        # Update time-step
        self.t += 1

        # Populate info dict
        info: Dict[str, Any] = {}
        info[env_constants.ENV_METRICS.STATE] = self.s
        info[env_constants.ENV_METRICS.DEFENDER_ACTION] = a
        info[env_constants.ENV_METRICS.OBSERVATION] = self.s
        info[env_constants.ENV_METRICS.TIME_STEP] = self.t
        info = self._info(info)

        # Log trace
        self.trace.defender_rewards.append(-c)
        self.trace.attacker_rewards.append(c)
        self.trace.attacker_actions.append(-1)
        self.trace.defender_actions.append(a)
        self.trace.infos.append(info)
        self.trace.states.append(self.s)
        self.trace.beliefs.append(0.0)
        self.trace.infrastructure_metrics.append(self.s)
        if not done:
            self.trace.attacker_observations.append(self.s)
            self.trace.defender_observations.append(self.s)

        return self.s, c, done, done, info

    def reset(self, seed: Union[None, int] = None, soft: bool = False, options: Union[Dict[str, Any], None] = None) \
            -> Tuple[int, Dict[str, Any]]:
        """
        Resets the environment state, this should be called whenever step() returns <done>

        :param seed: the random seed
        :param soft: boolean flag indicating whether it is a soft reset or not
        :param options: optional configuration parameters
        :return: initial observation and info
        """
        super().reset(seed=seed)
        if len(self.trace.defender_rewards) > 0:
            self.traces.append(self.trace)
        self.trace = SimulationTrace(simulation_env=self.config.simulation_env_name)
        self.t = 1
        self.s = self.config.initial_state
        self.trace.beliefs.append(0.0)
        self.trace.states.append(self.s)
        self.trace.defender_observations.append(self.s)
        self.trace.attacker_observations.append(self.s)
        info: Dict[str, Any] = {}
        return self.s, info

    def _info(self, info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adds the cumulative reward and episode length to the info dict

        :param info: the info dict to update
        :return: the updated info dict
        """
        R = 0
        for i in range(len(self.trace.defender_rewards)):
            R += self.trace.defender_rewards[i] * math.pow(self.config.discount_factor, i)
        info[env_constants.ENV_METRICS.RETURN] = sum(self.trace.defender_rewards)
        info[env_constants.ENV_METRICS.TIME_HORIZON] = len(self.trace.defender_actions)
        return info

    def render(self, mode: str = 'human'):
        """
        Renders the environment.  Supported rendering modes: (1) human; and (2) rgb_array

        :param mode: the rendering mode
        :return: True (if human mode) otherwise an rgb array
        """
        raise NotImplementedError("Rendering is not implemented for this environment")

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

    def set_state(self, state: int) -> None:
        """
        Sets the state. Allows to simulate samples from specific states

        :param state: the state
        :return: None
        """
        self.s = state

    def manual_play(self) -> None:
        """
        An interactive loop to test the CMDP manually

        :return: None
        """
        s = self.config.initial_state
        done = False
        cumulative_costs = 0.0
        c = 0.0
        t = 1
        while True:
            raw_input = input("> ")
            raw_input = raw_input.strip()
            if raw_input == "help":
                print("Enter an action id to execute the action, "
                      "press R to reset,"
                      "press S to print the set of states"
                      "press A to print the set of actions"
                      "press s to print the current state, press A to print the actions, "
                      "press D to check if done"
                      "press C to check the cumulative costs"
                      "press H to print the history of actions")
            elif raw_input == "A":
                print(self.config.actions)
            elif raw_input == "S":
                print(self.config.states)
            elif raw_input == "s":
                print(f"s: {s}, c: {c}")
            elif raw_input == "D":
                print(done)
            elif raw_input == "C":
                print(cumulative_costs)
            elif raw_input == "R":
                print("Resetting the state")
                s = self.config.initial_state
                done = False
                cumulative_costs = 0
                c = 0.0
                t = 1
            else:
                try:
                    a = int(raw_input)
                except Exception:
                    continue
                c = self.config.cost_tensor[s]
                print(f"s: {s}, a: {a}, c: {c}")
                s = GeneralUtil.sample_next_state(transition_tensor=self.config.transition_tensor, s=s, a=a,
                                                  states=self.config.states)
                t += 1
                cumulative_costs += c
                print(f"s: {s}, c: {c}, t: {t}")
