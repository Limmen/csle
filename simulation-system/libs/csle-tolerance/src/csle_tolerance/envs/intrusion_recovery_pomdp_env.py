from typing import Tuple, Any, Dict, List, Union
import time
import math
import gymnasium as gym
import numpy as np
from csle_common.dao.simulation_config.base_env import BaseEnv
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace
from csle_tolerance.dao.intrusion_recovery_pomdp_config import IntrusionRecoveryPomdpConfig
from csle_tolerance.util.intrusion_recovery_pomdp_util import IntrusionRecoveryPomdpUtil
from csle_tolerance.util.general_util import GeneralUtil
import csle_tolerance.constants.constants as env_constants
import csle_common.constants.constants as constants


class IntrusionRecoveryPomdpEnv(BaseEnv):
    """
    Gym Environment representing the Intrusion recovery POMDP
    """

    def __init__(self, config: IntrusionRecoveryPomdpConfig):
        """
        Initializes the environment

        :param config: the environment configuration
        """
        self.config = config

        # Setup spaces
        self.action_space = gym.spaces.Discrete(len(self.config.actions))
        self.observation_space = gym.spaces.Box(
            low=np.array([np.float64(1), np.float64(min(config.observations)), np.float64(0)]),
            high=np.array([np.float64(config.BTR), np.float64(max(config.observations)), np.float64(1)]),
            dtype=np.float64, shape=(3,))

        # Initialize state
        self.b = self.config.b1.copy()
        self.t = 1
        self.s = IntrusionRecoveryPomdpUtil.sample_initial_state(b1=self.b)
        self.o = 0

        # Setup traces
        self.traces: List[SimulationTrace] = []
        self.trace = SimulationTrace(simulation_env=self.config.gym_env_name)

        # Reset
        self.reset()
        super().__init__()

    def step(self, a: int) -> Tuple[List[Union[int, int, float]], float, bool, bool, Dict[str, Any]]:
        """
        Takes a step in the environment by executing the given action

        :param a: the action
        :return: (obs, reward, terminated, truncated, info)
        """
        done = False

        # Compute the cost
        c = self.config.cost_tensor[a][self.s]

        # Sample the next state
        self.s = GeneralUtil.sample_next_state(transition_tensor=self.config.transition_tensor,
                                               s=self.s, a=a, states=self.config.states)

        # Sample the next observation
        self.o = IntrusionRecoveryPomdpUtil.sample_next_observation(observation_tensor=self.config.observation_tensor,
                                                                    s_prime=self.s,
                                                                    observations=self.config.observations)

        # Update the belief
        self.b = IntrusionRecoveryPomdpUtil.next_belief(o=self.o, a=a, b=self.b, states=self.config.states,
                                                        observations=self.config.observations,
                                                        observation_tensor=self.config.observation_tensor,
                                                        transition_tensor=self.config.transition_tensor)

        # Increment time-step
        self.t += 1

        # Populate info dict
        info: Dict[str, Any] = {}
        info[env_constants.ENV_METRICS.STATE] = self.s
        info[env_constants.ENV_METRICS.DEFENDER_ACTION] = a
        info[env_constants.ENV_METRICS.OBSERVATION] = self.o
        info[env_constants.ENV_METRICS.TIME_STEP] = self.t

        # Log trace
        self.trace.defender_rewards.append(c)
        self.trace.attacker_rewards.append(-c)
        self.trace.attacker_actions.append(-1)
        self.trace.defender_actions.append(a)
        info = self._info(info)
        self.trace.infos.append(info)
        self.trace.states.append(self.s)
        self.trace.beliefs.append(self.b[1])
        self.trace.infrastructure_metrics.append(self.o)
        if not done:
            self.trace.attacker_observations.append(self.o)
            self.trace.defender_observations.append(self.o)

        # Check if done or not
        if self.t >= self.config.BTR or self.s == 2 or self.t > self.config.max_horizon:
            done = True

        t = self.t
        if self.config.BTR == np.inf or self.config.BTR >= 10000:
            t = 1
        return [t, self.b[1], self.o], c, done, done, info

    def reset(self, seed: Union[None, int] = None, soft: bool = False, options: Union[Dict[str, Any], None] = None) \
            -> Tuple[List[Union[int, int, float]], Dict[str, Any]]:
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
        self.b = self.config.b1.copy()
        self.t = 1
        self.s = IntrusionRecoveryPomdpUtil.sample_initial_state(b1=self.b)
        self.o = 0
        self.trace.beliefs.append(self.b)
        self.trace.states.append(self.s)
        self.trace.defender_observations.append(self.o)
        self.trace.attacker_observations.append(self.o)
        info: Dict[str, Any] = {}
        return [self.t, self.b[1], self.o], info

    def _info(self, info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adds the cumulative reward and episode length to the info dict

        :param info: the info dict to update
        :return: the updated info dict
        """
        R = 0
        for i in range(len(self.trace.defender_rewards)):
            R += self.trace.defender_rewards[i] * math.pow(self.config.discount_factor, i)
        info[env_constants.ENV_METRICS.RETURN] = R
        info[env_constants.ENV_METRICS.TIME_HORIZON] = len(self.trace.defender_actions)
        upper_bound_return = 0
        s = self.trace.states[0]
        for i in range(len(self.trace.states)):
            if s == 0 or s == 2:
                a = 0
            else:
                a = 1
            upper_bound_return += self.config.cost_tensor[a][s] * math.pow(self.config.discount_factor, i)
            if a != self.trace.defender_actions[i] or s != self.trace.states[i]:
                s = GeneralUtil.sample_next_state(transition_tensor=self.config.transition_tensor,
                                                  s=s, a=a, states=self.config.states)
            else:
                if i < len(self.trace.states) - 1:
                    s = self.trace.states[i + 1]
        info[env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN] = upper_bound_return
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
        An interactive loop to test the POMDP manually

        :return: None
        """
        b1 = self.config.b1
        done = False
        s = IntrusionRecoveryPomdpUtil.sample_initial_state(b1=b1)
        cumulative_costs = 0.0
        c = 0.0
        o = -1
        t = 1
        b = b1.copy()
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
                print(f"s: {s}, c: {c}, o: {o}, b: {b}")
            elif raw_input == "D":
                print(done)
            elif raw_input == "C":
                print(cumulative_costs)
            elif raw_input == "R":
                print("Resetting the state")
                s = IntrusionRecoveryPomdpUtil.sample_initial_state(b1=b1)
                done = False
                cumulative_costs = 0
                c = 0.0
                o = -1
                t = 1
                b = b1.copy()
            else:
                try:
                    a = int(raw_input)
                except Exception:
                    continue
                if t == self.config.T:
                    a = 1
                c = self.config.cost_tensor[a][s]
                print(f"s: {s}, a: {a}, c: {c}")
                s = GeneralUtil.sample_next_state(transition_tensor=self.config.transition_tensor, s=s, a=a,
                                                  states=self.config.states)
                o = IntrusionRecoveryPomdpUtil.sample_next_observation(
                    observation_tensor=self.config.observation_tensor, s_prime=s, observations=self.config.observations)
                b = IntrusionRecoveryPomdpUtil.next_belief(o=o, a=a, b=b, states=self.config.states,
                                                           observations=self.config.observations,
                                                           observation_tensor=self.config.observation_tensor,
                                                           transition_tensor=self.config.transition_tensor)
                if t < self.config.T:
                    t += 1
                cumulative_costs += c
                print(f"s: {s}, c: {c}, o: {o}, b: {b}, t: {t}")
