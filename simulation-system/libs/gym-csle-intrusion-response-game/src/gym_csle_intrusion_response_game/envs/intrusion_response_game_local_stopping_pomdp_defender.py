from typing import Tuple, List, Dict, Union, Any
import numpy as np
import numpy.typing as npt
import time
import math
import csle_common.constants.constants as constants
from csle_common.dao.simulation_config.base_env import BaseEnv
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace
from gym_csle_intrusion_response_game.dao.intrusion_response_game_local_pomdp_defender_config import \
    IntrusionResponseGameLocalPOMDPDefenderConfig
from gym_csle_intrusion_response_game.util.intrusion_response_game_util import IntrusionResponseGameUtil
import gym_csle_intrusion_response_game.constants.constants as env_constants


class IntrusionResponseGameLocalStoppingPOMDPDefenderEnv(BaseEnv):
    """
    OpenAI Gym Env for the POMDP of the defender when facing a static attacker.

    (A Partially observed Dynkin game where the attacker strategy is fixed)
    """

    def __init__(self, config: IntrusionResponseGameLocalPOMDPDefenderConfig) -> None:
        """
        Initializes the environment

        :param config: the environment configuration
        """
        a1 = config.stopping_action
        self.zone = config.stopping_zone
        if config is None:
            raise ValueError("Configuration cannot be None")
        self.config = config

        self.Z = IntrusionResponseGameUtil.local_stopping_pomdp_observation_tensor(
            S=self.config.local_intrusion_response_game_config.S,
            A2=self.config.local_intrusion_response_game_config.A2,
            Z=self.config.local_intrusion_response_game_config.Z,
            S_A=self.config.local_intrusion_response_game_config.S_A,
            a1=a1, zone=self.zone, O=self.config.local_intrusion_response_game_config.O
        )

        self.R = IntrusionResponseGameUtil.local_stopping_pomdp_reward_tensor(
            S=self.config.local_intrusion_response_game_config.S,
            A2=self.config.local_intrusion_response_game_config.A2,
            R=self.config.local_intrusion_response_game_config.R[0],
            S_A=self.config.local_intrusion_response_game_config.S_A,
            a1=a1, zone=self.zone)

        self.T = IntrusionResponseGameUtil.local_stopping_pomdp_transition_tensor(
            S=self.config.local_intrusion_response_game_config.S,
            A2=self.config.local_intrusion_response_game_config.A2,
            T=self.config.local_intrusion_response_game_config.T[0],
            S_A=self.config.local_intrusion_response_game_config.S_A,
            a1=a1
        )

        # Initialize environment state
        self.s = 0
        self.b = self.config.local_intrusion_response_game_config.d_b1
        self.a_b = self.config.local_intrusion_response_game_config.a_b1

        # Setup spaces
        self.observation_space = self.config.local_intrusion_response_game_config.defender_observation_space_stopping()
        self.action_space = self.config.local_intrusion_response_game_config.defender_action_space_stopping()

        # Setup static attacker strategy
        self.static_attacker_strategy = self.config.attacker_strategy
        self.static_defender_strategy = self.config.defender_strategy

        # Setup traces
        self.traces: List[SimulationTrace] = []
        self.trace = SimulationTrace(simulation_env=self.config.env_name)
        self.latest_attacker_obs: Union[None, List[Any]] = None
        self.latest_obs = 0
        self.latest_a2 = 0

        # Reset
        self.reset()

        # Get upper bound and random return estimate
        self.upper_bound_return = 0
        self.random_return = 0
        self.t = 0
        self.intrusion_length = 0
        self.upper_bound_return = 0
        # self.upper_bound_return = self.get_upper_bound_return(samples=100)

        # Reset
        self.reset()
        super().__init__()

    def step(self, a1: Union[int, List[int]]) \
            -> Tuple[npt.NDArray[Any], float, bool, bool, Dict[str, Union[float, int]]]:
        """
        Takes a step in the environment by executing the given action

        :param a1: defender action
        :return: (obs, reward, terminated, truncated, info)
        """
        done = False
        info: Dict[str, Any] = {}

        # Extract the defender action
        if isinstance(a1, list):
            a1 = a1[0]
        a1 = int(a1)

        # Get attacker action from static strategy
        pi2 = np.array(self.static_attacker_strategy.stage_policy(self.latest_attacker_obs))
        a2 = IntrusionResponseGameUtil.sample_attacker_action(pi2=pi2, s=self.s)
        self.latest_a2 = a2

        # Compute the reward
        r = self.R[a1][a2][self.s + 1]

        # Sample the next state
        S = np.append([-1], self.config.local_intrusion_response_game_config.S_A)
        s_a = self.s
        s_idx_prime = IntrusionResponseGameUtil.sample_next_state(
            a1=a1, a2=a2, T=self.T, S=S,
            s_idx=self.s + 1)

        # Sample the next observation
        o = IntrusionResponseGameUtil.sample_next_observation(
            Z=self.Z, O=self.config.local_intrusion_response_game_config.O,
            s_prime_idx=s_idx_prime, a1=a1, a2=a2)
        self.latest_obs = o

        # Move to the next state
        self.s = s_idx_prime - 1

        # Check if game is done
        if self.s == -1:
            done = True
        if a1 == 1:
            done = True

        if not done:
            S = self.config.local_intrusion_response_game_config.S_A
            # Update the beliefs
            self.b = IntrusionResponseGameUtil.next_stopping_belief(
                o=o, a1=a1, b=self.b, pi2=pi2, S=S, Z=self.Z,
                O=self.config.local_intrusion_response_game_config.O,
                T=self.T,
                A2=self.config.local_intrusion_response_game_config.A2, a2=a2, s=self.s)
            try:
                pi1 = np.array(self.static_defender_strategy.stage_policy(self.latest_defender_obs))
                self.a_b = IntrusionResponseGameUtil.next_local_attacker_belief(
                    o=o, a1=a1, a_b=self.a_b, pi1=pi1, config=self.config.local_intrusion_response_game_config,
                    a2=a2, s_d=self.zone, s_a_prime=self.s,
                    s_a=s_a)
            except Exception:
                pass

        # Update metrics
        self.t += 1
        if self.s == env_constants.ATTACK_STATES.COMPROMISED:
            self.intrusion_length += 1

        # Populate info dict
        info[env_constants.ENV_METRICS.STATE] = self.s
        info[env_constants.ENV_METRICS.DEFENDER_ACTION] = a1
        info[env_constants.ENV_METRICS.ATTACKER_ACTION] = a2
        info[env_constants.ENV_METRICS.OBSERVATION] = o
        info[env_constants.ENV_METRICS.TIME_STEP] = self.t
        info[env_constants.ENV_METRICS.INTRUSION_LENGTH] = self.intrusion_length
        info[env_constants.ENV_METRICS.WEIGHTED_INTRUSION_PREDICTION_DISTANCE] = 0
        info[env_constants.ENV_METRICS.START_POINT_CORRECT] = 0
        info[env_constants.ENV_METRICS.INTRUSION_START] = 0
        info[env_constants.ENV_METRICS.INTRUSION_END] = 0

        # Get observations
        defender_obs = self.b
        self.latest_attacker_obs = [self.s] + list(self.a_b)
        self.latest_defender_obs: List[Any] = [self.zone] + list(self.b)

        # Log trace
        self.trace.defender_rewards.append(r)
        self.trace.attacker_rewards.append(-r)
        self.trace.attacker_actions.append(a2)
        self.trace.defender_actions.append(a1)
        self.trace.infos.append(info)
        self.trace.states.append(self.s)
        self.trace.beliefs.append(self.b)
        self.trace.infrastructure_metrics.append(o)
        if not done:
            self.trace.attacker_observations.append(defender_obs)
            self.trace.defender_observations.append(defender_obs)

        # Populate info
        info = self._info(info)
        return defender_obs, r, done, done, info

    def _info(self, info: Dict[str, Union[float, int]]) -> Dict[str, Union[float, int]]:
        """
        Adds the cumulative reward and episode length to the info dict
        :param info: the info dict to update
        :return: the updated info dict
        """
        R = 0
        for i in range(len(self.trace.defender_rewards)):
            R += self.trace.defender_rewards[i] * math.pow(self.config.local_intrusion_response_game_config.gamma, i)
        info[env_constants.ENV_METRICS.RETURN] = R
        info[env_constants.ENV_METRICS.TIME_HORIZON] = len(self.trace.defender_actions)
        info[env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN] = self.upper_bound_return
        info[env_constants.ENV_METRICS.AVERAGE_RANDOM_RETURN] = self.random_return
        return info

    def get_upper_bound_return(self, samples: int = 100) -> float:
        """
        Utiltiy method for getting an upper bound on the average return

        :param samples: the number of sample returns to average
        :return: the estimated upper bound
        """
        max_horizon = 1000
        returns = []
        for i in range(samples):
            _, _ = self.reset()
            done = False
            t = 0
            cumulative_reward = 0.0
            while not done and t <= max_horizon:
                a1 = 0
                if self.s == 2:
                    a1 = 1
                o, r, done, _, info = self.step(a1)
                cumulative_reward += r * math.pow(self.config.local_intrusion_response_game_config.gamma, t)
                t += 1
            returns.append(cumulative_reward)
        return float(np.mean(np.array(returns)))

    def reset(self, seed: Union[None, int] = None, soft: bool = False, options: Union[Dict[str, Any], None] = None) \
            -> Tuple[npt.NDArray[Any], Dict[str, Any]]:
        """
        Resets the environment state, this should be called whenever step() returns <done>

        :param seed: the random seed
        :param soft: boolean flag indicating whether it is a soft reset or not
        :param options: optional configuration parameters
        :return: initial observation
        """
        super().reset(seed=seed)
        self.s = 0
        self.intrusion_length = 0
        self.b = self.config.local_intrusion_response_game_config.d_b1
        if len(self.trace.attacker_rewards) > 0:
            self.traces.append(self.trace)
        self.trace = SimulationTrace(simulation_env=self.config.env_name)
        attacker_obs = self.b
        defender_obs = self.b
        self.latest_attacker_obs = [self.s] + list(self.a_b)
        self.latest_defender_obs = [self.zone] + list(self.b)
        self.trace.attacker_observations.append(attacker_obs)
        self.trace.defender_observations.append(defender_obs)
        info: Dict[str, Any] = {}
        return defender_obs, info

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

    def manual_play(self) -> None:
        """
        An interactive loop to test the environment manually

        :return: None
        """
        done = False
        o, _ = self.reset()
        print(f"o:{list(map(lambda x: round(x, 3), list(o.tolist())))}")
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
                print(self.s)
            elif raw_input == "D":
                print(done)
            elif raw_input == "H":
                print(self.trace)
            elif raw_input == "R":
                print("Resetting the state")
                o, _ = self.reset()
                print(f"o:{list(map(lambda x: round(x, 3), list(o.tolist())))}")
            else:
                a1 = int(raw_input)
                o, r, done, _, _ = self.step(a1=a1)
                print(f"o:{list(map(lambda x: round(x, 3), list(o.tolist())))}, r:{round(r, 2)}, done: {done}, "
                      f"a1: {a1}, s:{self.s}, o:{self.latest_obs}, a2: {self.latest_a2}")
