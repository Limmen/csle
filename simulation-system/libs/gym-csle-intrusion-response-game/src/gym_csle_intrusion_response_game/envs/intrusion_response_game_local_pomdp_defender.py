from typing import Tuple, List, Dict, Union
import numpy as np
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
    OpenAI Gym Env for the MDP of the defender when facing a static attacker
    """

    def __init__(self, config: IntrusionResponseGameLocalPOMDPDefenderConfig):
        """
        Initializes the environment

        :param config: the environment configuration
        :param attacker_strategy: the strategy of the static attacker
        """
        self.config = config

        # Initialize environment state
        self.state = IntrusionResponseGameStateLocal(b1=self.config.intrusion_response_game_config.d_b1,
                                                     S=self.config.intrusion_response_game_config.S)

        # Setup spaces
        self.observation_space = self.config.intrusion_response_game_config.defender_observation_space()
        self.action_space = self.config.intrusion_response_game_config.defender_action_space()

        # Setup static attacker strategy
        self.static_attacker_strategy = self.config.attacker_strategy

        # Setup Config
        self.viewer = None
        self.metadata = {
            'render.modes': ['human', 'rgb_array'],
            'video.frames_per_second': 50  # Video rendering speed
        }

        # Setup traces
        self.traces = []
        self.trace = SimulationTrace(simulation_env=self.config.env_name)

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
        # Get attacker action from static strategy
        # pi2 = np.array(self.static_attacker_strategy.stage_policy(self.latest_attacker_obs))
        # a2 = StoppingGameUtil.sample_attacker_action(pi2=pi2, s=self.stopping_game_env.state.s)
        done = False
        info = {}
        eps = np.random.uniform(0., 1.)
        if eps < 0.7:
            a2 = 0
        else:
            if self.state.s[1] == 0:
                a2 = 1
            else:
                a2 = np.random.choice(np.array([2,3]), p=[1/2,1/2])

        s_idx = list(self.config.intrusion_response_game_config.S.tolist()).index(list(self.state.s.tolist()))
        r = self.config.intrusion_response_game_config.R[a1][a2][s_idx]
        state_idx = IntrusionResponseGameUtil.sample_next_state(
            a1=a1, a2=a2, T=self.config.intrusion_response_game_config.T,
            S=self.config.intrusion_response_game_config.S, s_idx=s_idx)
        self.state.s = self.config.intrusion_response_game_config.S[state_idx]
        s_idx = list(self.config.intrusion_response_game_config.S.tolist()).index(list(self.state.s.tolist()))

        o = max(self.config.intrusion_response_game_config.O)
        if self.state.s[0] == -1 and self.state.s[1] == -1:
            done = True
        else:
            o = IntrusionResponseGameUtil.sample_next_observation(
                Z=self.config.intrusion_response_game_config.Z,
                O=self.config.intrusion_response_game_config.O,
                s_prime_idx=s_idx, a1=a1, a2=a2)

        # Update time-step
        self.state.t += 1

        # Populate info dict
        info[env_constants.ENV_METRICS.STATE] = self.state.s
        info[env_constants.ENV_METRICS.DEFENDER_ACTION] = a1
        info[env_constants.ENV_METRICS.ATTACKER_ACTION] = a2
        info[env_constants.ENV_METRICS.OBSERVATION] = o
        info[env_constants.ENV_METRICS.TIME_STEP] = self.state.t

        # Log trace
        self.trace.defender_rewards.append(r)
        self.trace.attacker_rewards.append(-r)
        self.trace.attacker_actions.append(a2)
        self.trace.defender_actions.append(a1)
        self.trace.infos.append(info)
        self.trace.states.append(self.state.s)
        self.trace.beliefs.append(self.state.b[1])
        self.trace.infrastructure_metrics.append(o)
        if not done:
            self.trace.attacker_observations.append(o)
            self.trace.defender_observations.append(o)

        # Populate info
        info = self._info(info)

        return o, r, done, info

    def _info(self, info) -> Dict[str, Union[float, int]]:
        """
        Adds the cumulative reward and episode length to the info dict
        :param info: the info dict to update
        :return: the updated info dict
        """
        R = 0
        for i in range(len(self.trace.defender_rewards)):
            R += self.trace.defender_rewards[i] * math.pow(self.config.intrusion_response_game_config.gamma, i)
        info[env_constants.ENV_METRICS.RETURN] = sum(self.trace.defender_rewards)
        info[env_constants.ENV_METRICS.TIME_HORIZON] = len(self.trace.defender_actions)
        upper_bound_return = 0
        info[env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN] = upper_bound_return
        return info

    def reset(self, soft: bool = False) -> Tuple[np.ndarray, np.ndarray]:
        """
        Resets the environment state, this should be called whenever step() returns <done>

        :return: initial observation
        """
        self.state.reset()
        if len(self.trace.attacker_rewards) > 0:
            self.traces.append(self.trace)
        self.trace = SimulationTrace(simulation_env=self.config.env_name)
        s_idx = list(self.config.intrusion_response_game_config.S.tolist()).index(list(self.state.s.tolist()))
        o = IntrusionResponseGameUtil.sample_next_observation(
            Z=self.config.intrusion_response_game_config.Z,
            O=self.config.intrusion_response_game_config.O,
            s_prime_idx=s_idx, a1=0, a2=0)
        self.trace.attacker_observations.append(o)
        self.trace.defender_observations.append(o)
        return o

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
        return