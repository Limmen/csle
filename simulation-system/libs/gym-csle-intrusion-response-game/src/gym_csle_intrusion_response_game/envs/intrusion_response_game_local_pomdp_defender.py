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
from gym_csle_intrusion_response_game.dao.intrusion_response_game_state_local import IntrusionResponseGameStateLocal
import gym_csle_intrusion_response_game.constants.constants as env_constants


class IntrusionResponseGameLocalPOMDPDefenderEnv(BaseEnv):
    """
    OpenAI Gym Env for the POMDP of the defender when facing a static attacker.

    (A PO-POSG, i.e a partially observed stochastic game with public observations) where the attacker strategy
    is fixed)
    """

    def __init__(self, config: IntrusionResponseGameLocalPOMDPDefenderConfig) -> None:
        """
        Initializes the environment

        :param config: the environment configuration
        """
        if config is None:
            raise ValueError("Configuration cannot be None")
        self.config = config

        # Initialize environment state
        self.state = IntrusionResponseGameStateLocal(
            d_b1=self.config.local_intrusion_response_game_config.d_b1,
            a_b1=self.config.local_intrusion_response_game_config.a_b1,
            S=self.config.local_intrusion_response_game_config.S,
            S_A=self.config.local_intrusion_response_game_config.S_A,
            S_D=self.config.local_intrusion_response_game_config.S_D,
            s_1_idx=self.config.local_intrusion_response_game_config.s_1_idx)

        # Setup spaces
        self.observation_space = self.config.local_intrusion_response_game_config.defender_observation_space()
        self.action_space = self.config.local_intrusion_response_game_config.defender_action_space()

        # Setup static attacker strategy
        self.static_attacker_strategy = self.config.attacker_strategy
        self.static_defender_strategy = self.config.defender_strategy

        # Setup traces
        self.traces: List[SimulationTrace] = []
        self.trace = SimulationTrace(simulation_env=self.config.env_name)
        self.latest_attacker_obs: Union[npt.NDArray[Any], None] = None
        self.latest_defender_obs: Union[npt.NDArray[Any], None] = None
        self.latest_attacker_action: Union[None, int] = None

        # Reset
        self.reset()

        # Get upper bound and random return estimate
        self.upper_bound_return = 0
        self.random_return = 0
        # self.upper_bound_return = self.get_upper_bound_return(samples=5)
        # self.random_return = self.get_random_baseline_return(samples=5)

        # Reset
        self.reset()
        super().__init__()

    def get_random_baseline_return(self, samples: int = 100) -> float:
        """
        Utiltiy function for estimating the average return of a random defender strategy

        :param samples: the number of samples to use for estimation
        :return: the estimated return
        """
        max_horizon = 1000
        returns = []
        for i in range(samples):
            self.reset()
            done = False
            t = 0
            cumulative_reward = 0.0
            while not done and t <= max_horizon:
                a1 = np.random.choice(self.config.local_intrusion_response_game_config.A1)
                o, r, done, _, info = self.step(a1)
                cumulative_reward += r * math.pow(self.config.local_intrusion_response_game_config.gamma, t)
                t += 1
            returns.append(cumulative_reward)
        return float(np.mean(np.array(returns)))

    def get_upper_bound_return(self, samples: int = 100) -> float:
        """
        Utiltiy method for getting an upper bound on the average return

        :param samples: the number of sample returns to average
        :return: the estimated upper bound
        """
        max_horizon = 1000
        returns = []
        initial_zone = self.config.local_intrusion_response_game_config.S[
            self.config.local_intrusion_response_game_config.s_1_idx][env_constants.STATES.D_STATE_INDEX]
        for i in range(samples):
            o, _ = self.reset()
            done = False
            t = 0
            cumulative_reward = 0.0
            while not done and t <= max_horizon:
                a1 = 0
                if self.state.attacker_state() == env_constants.ATTACK_STATES.COMPROMISED:
                    a1 = initial_zone
                o, r, done, _, info = self.step(a1)
                cumulative_reward += r * math.pow(self.config.local_intrusion_response_game_config.gamma, t)
                t += 1
            returns.append(cumulative_reward)
        return float(np.mean(np.array(returns)))

    def step(self, a1: Union[int, List[int]]) \
            -> Tuple[npt.NDArray[Any], float, bool, bool, Dict[str, Union[float, int]]]:
        """
        Takes a step in the environment by executing the given action

        :param a1: defender action
        :return: (obs, reward, terminated, truncated, info)
        """
        done, info = False, {}

        # Extract the defender action
        if isinstance(a1, list):
            a1 = a1[0]
        a1 = int(a1)

        # Get attacker action from static strategy
        pi2 = np.array(self.static_attacker_strategy.stage_policy(self.latest_attacker_obs))
        a2 = IntrusionResponseGameUtil.sample_attacker_action(pi2=pi2, s=self.state.attacker_state())
        self.latest_attacker_action = a2

        # Save current defender state (needed later for updating the belief)
        s_d = self.state.defender_state()

        # Compute the reward
        r = self.config.local_intrusion_response_game_config.R[0][a1][a2][self.state.s_idx]

        # Sample the next state
        s_idx_prime = IntrusionResponseGameUtil.sample_next_state(
            a1=a1, a2=a2, T=self.config.local_intrusion_response_game_config.T[0],
            S=self.config.local_intrusion_response_game_config.S, s_idx=self.state.s_idx)

        # Sample the next observation
        o = IntrusionResponseGameUtil.sample_next_observation(
            Z=self.config.local_intrusion_response_game_config.Z,
            O=self.config.local_intrusion_response_game_config.O,
            s_prime_idx=s_idx_prime, a1=a1, a2=a2)

        # Move to the next state
        self.state.s_idx = s_idx_prime

        # Check if game is done
        if IntrusionResponseGameUtil.is_local_state_terminal(self.state.state_vector()):
            done = True

        if not done:
            try:
                # Update the beliefs
                self.state.d_b = IntrusionResponseGameUtil.next_local_defender_belief(
                    o=o, a1=a1, d_b=self.state.d_b, pi2=pi2, config=self.config.local_intrusion_response_game_config,
                    a2=a2, s_a=self.state.attacker_state(),
                    s_d_prime=self.state.defender_state(), s_d=s_d)
                pi1 = np.array(self.static_defender_strategy.stage_policy(self.latest_defender_obs))
                self.state.a_b = IntrusionResponseGameUtil.next_local_attacker_belief(
                    o=o, a1=a1, a_b=self.state.a_b, pi1=pi1, config=self.config.local_intrusion_response_game_config,
                    a2=a2, s_d=self.state.defender_state(), s_a_prime=self.state.attacker_state(),
                    s_a=self.state.attacker_state())
            except Exception:
                pass

        # Update time-step
        self.state.t += 1

        # Populate info dict
        info[env_constants.ENV_METRICS.STATE] = self.state.state_vector()
        info[env_constants.ENV_METRICS.DEFENDER_ACTION] = a1
        info[env_constants.ENV_METRICS.ATTACKER_ACTION] = a2
        info[env_constants.ENV_METRICS.OBSERVATION] = o
        info[env_constants.ENV_METRICS.TIME_STEP] = self.state.t

        # Get observations
        attacker_obs = self.state.attacker_observation()
        defender_obs = self.state.defender_observation()
        self.latest_attacker_obs = attacker_obs
        self.latest_defender_obs = defender_obs

        # Log trace
        self.trace.defender_rewards.append(r)
        self.trace.attacker_rewards.append(-r)
        self.trace.attacker_actions.append(a2)
        self.trace.defender_actions.append(a1)
        self.trace.infos.append(info)
        self.trace.states.append(self.state.s_idx)
        self.trace.beliefs.append(self.state.d_b)
        self.trace.infrastructure_metrics.append(o)
        if not done:
            self.trace.attacker_observations.append(attacker_obs)
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
        self.state.reset()
        if len(self.trace.attacker_rewards) > 0:
            self.traces.append(self.trace)
        self.trace = SimulationTrace(simulation_env=self.config.env_name)
        attacker_obs = self.state.attacker_observation()
        defender_obs = self.state.defender_observation()
        self.latest_attacker_obs = attacker_obs
        self.latest_defender_obs = defender_obs
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

    def manual_play(self) -> None:
        """
        An interactive loop to test the environment manually

        :return: None
        """
        done = False
        o, _ = self.reset()
        print(f"o:{list(map(lambda x: round(float(x), 3), list(o)))}")
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
                print(self.state)
            elif raw_input == "D":
                print(done)
            elif raw_input == "H":
                print(self.trace)
            elif raw_input == "R":
                print("Resetting the state")
                o, _ = self.reset()
                print(f"o:{list(map(lambda x: round(float(x), 3), list(o)))}")
            else:
                a1 = int(raw_input)
                o, r, done, _, _ = self.step(a1=a1)
                print(f"o:{list(map(lambda x: round(float(x), 3), list(o)))}, r:{round(r, 2)}, done: {done}")

    def pomdp_solver_file(self) -> str:
        """
        Gets the POMDP environment specification based on the format at http://www.pomdp.org/code/index.html,
        for the defender's local problem against a static attacker

        :return: the file content string
        """
        return IntrusionResponseGameUtil.get_local_defender_pomdp_solver_file(
            S=self.config.local_intrusion_response_game_config.S,
            A1=self.config.local_intrusion_response_game_config.A1,
            A2=self.config.local_intrusion_response_game_config.A2,
            O=self.config.local_intrusion_response_game_config.O,
            T=self.config.local_intrusion_response_game_config.T,
            R=self.config.local_intrusion_response_game_config.R,
            Z=self.config.local_intrusion_response_game_config.Z,
            static_attacker_strategy=self.config.attacker_strategy,
            s_1_idx=self.config.local_intrusion_response_game_config.s_1_idx,
            discount_factor=self.config.local_intrusion_response_game_config.gamma
        )

    def get_local_stopping_mdp_transition_tensor(self) -> npt.NDArray[Any]:
        """
        :return: the local MDP transition tensor of the optimal stopping formulation
        """
        return IntrusionResponseGameUtil.local_stopping_mdp_transition_tensor(
            S=self.config.local_intrusion_response_game_config.S,
            A1=self.config.local_intrusion_response_game_config.A1,
            A2=self.config.local_intrusion_response_game_config.A2,
            T=self.config.local_intrusion_response_game_config.T[0],
            S_D=self.config.local_intrusion_response_game_config.S_D
        )

    def get_local_stopping_mdp_reward_tensor(self) -> npt.NDArray[Any]:
        """
        :return: the local MDP reward tensor of the optimal stopping formulation
        """
        return IntrusionResponseGameUtil.local_stopping_mdp_reward_tensor(
            S=self.config.local_intrusion_response_game_config.S,
            A1=self.config.local_intrusion_response_game_config.A1,
            A2=self.config.local_intrusion_response_game_config.A2,
            R=self.config.local_intrusion_response_game_config.R[0],
            S_D=self.config.local_intrusion_response_game_config.S_D
        )

    def get_local_stopping_pomdp_transition_tensor(self, a1: int) -> npt.NDArray[Any]:
        """
        :param a1: the defender action
        :return: the local POMDP transition tensor of the optimal stopping formulation
        """
        return IntrusionResponseGameUtil.local_stopping_pomdp_transition_tensor(
            S=self.config.local_intrusion_response_game_config.S,
            A2=self.config.local_intrusion_response_game_config.A2,
            T=self.config.local_intrusion_response_game_config.T[0],
            S_A=self.config.local_intrusion_response_game_config.S_A,
            a1=a1
        )

    def get_local_stopping_pomdp_reward_tensor(self, a1: int, zone: int) -> npt.NDArray[Any]:
        """
        :param a1: the defender action
        :param zone: the zone
        :return: the local MDP reward tensor of the optimal stopping formulation
        """
        return IntrusionResponseGameUtil.local_stopping_pomdp_reward_tensor(
            S=self.config.local_intrusion_response_game_config.S,
            A2=self.config.local_intrusion_response_game_config.A2,
            R=self.config.local_intrusion_response_game_config.R[0],
            S_A=self.config.local_intrusion_response_game_config.S_A,
            a1=a1, zone=zone
        )

    def get_local_stopping_pomdp_obs_tensor(self, a1: int, zone: int) -> npt.NDArray[Any]:
        """
        :param a1: the defender action
        :param zone: the zone
        :return: the local MDP reward tensor of the optimal stopping formulation
        """
        return IntrusionResponseGameUtil.local_stopping_pomdp_observation_tensor(
            S=self.config.local_intrusion_response_game_config.S,
            A2=self.config.local_intrusion_response_game_config.A2,
            Z=self.config.local_intrusion_response_game_config.Z,
            S_A=self.config.local_intrusion_response_game_config.S_A,
            a1=a1, zone=zone, O=self.config.local_intrusion_response_game_config.O
        )

    def set_model(self, model) -> None:
        """
        Sets the model. Useful when using RL frameworks where the stage policy is not easy to extract

        :param model: the model
        :return: None
        """
        self.model = model

    def set_state(self, state: IntrusionResponseGameStateLocal) -> None:
        """
        Sets the state. Allows to simulate samples from specific states

        :param state: the state
        :return: None
        """
        self.state = state
