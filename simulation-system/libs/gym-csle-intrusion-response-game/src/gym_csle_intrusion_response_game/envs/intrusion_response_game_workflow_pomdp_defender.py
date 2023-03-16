from typing import Tuple, List, Dict, Union
import numpy as np
import time
import math
import csle_common.constants.constants as constants
from csle_common.dao.simulation_config.base_env import BaseEnv
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace
from gym_csle_intrusion_response_game.dao.workflow_intrusion_response_pomdp_defender_config import \
    WorkflowIntrusionResponsePOMDPDefenderConfig
from gym_csle_intrusion_response_game.util.intrusion_response_game_util import IntrusionResponseGameUtil
from gym_csle_intrusion_response_game.envs.intrusion_response_game_local_pomdp_defender import \
    IntrusionResponseGameLocalPOMDPDefenderEnv
from gym_csle_intrusion_response_game.dao.intrusion_response_game_local_pomdp_defender_config import \
    IntrusionResponseGameLocalPOMDPDefenderConfig
from gym_csle_intrusion_response_game.dao.local_intrusion_response_game_config import LocalIntrusionResponseGameConfig
import gym_csle_intrusion_response_game.constants.constants as env_constants


class IntrusionResponseGameWorkflowPOMDPDefenderEnv(BaseEnv):
    """
    OpenAI Gym Env for the POMDP of the defender when facing a static attacker in the workflow game.

    (A PO-POSG, i.e a partially observed stochastic game with public observations) where the attacker strategy
    is fixed)
    """

    def __init__(self, config: WorkflowIntrusionResponsePOMDPDefenderConfig) -> None:
        """
        Initializes the environment

        :param config: the environment configuration
        """
        self.config = config
        self.local_envs = []
        for node in config.game_config.nodes:
            reachable = True
            S = IntrusionResponseGameUtil.local_state_space(number_of_zones=len(self.config.game_config.zones))
            states_to_idx = {}
            for i, s in enumerate(S):
                states_to_idx[(s[env_constants.STATES.D_STATE_INDEX], s[env_constants.STATES.A_STATE_INDEX])] = i
            S_A = IntrusionResponseGameUtil.local_attacker_state_space()
            S_D = IntrusionResponseGameUtil.local_defender_state_space(
                number_of_zones=len(self.config.game_config.zones))
            A1 = IntrusionResponseGameUtil.local_defender_actions(number_of_zones=len(self.config.game_config.zones))
            A2 = IntrusionResponseGameUtil.local_attacker_actions()
            O = IntrusionResponseGameUtil.local_observation_space(X_max=self.config.game_config.X_max)
            T = np.array([IntrusionResponseGameUtil.local_transition_tensor(
                S=S, A1=A1, A2=A2, Z_D=self.config.game_config.Z_D_P, A_P=self.config.game_config.A_P)])
            Z = IntrusionResponseGameUtil.local_observation_tensor_betabinom(S=S, A1=A1, A2=A2, O=O)
            Z_U = np.array([0, 1, 3, 3.5, 4])
            R = np.array(
                [IntrusionResponseGameUtil.local_reward_tensor(
                    eta=self.config.game_config.eta, C_D=self.config.game_config.C_D, A1=A1, A2=A2,
                    reachable=reachable, beta=self.config.game_config.beta, S=S, Z_U=Z_U,
                    initial_zone=self.config.game_config.initial_zones[node])])
            d_b1 = IntrusionResponseGameUtil.local_initial_defender_belief(S_A=S_A)
            a_b1 = IntrusionResponseGameUtil.local_initial_attacker_belief(
                S_D=S_D, initial_zone=self.config.game_config.initial_zones[node])
            initial_state = [self.config.game_config.initial_zones[node], 0]
            initial_state_idx = states_to_idx[(initial_state[env_constants.STATES.D_STATE_INDEX],
                                               initial_state[env_constants.STATES.A_STATE_INDEX])]
            local_game_config = LocalIntrusionResponseGameConfig(
                env_name="csle-intrusion-response-game-local-pomdp-defender-001",
                T=T, O=O, Z=Z, R=R, S=S, S_A=S_A, S_D=S_D, s_1_idx=initial_state_idx,
                zones=self.config.game_config.zones, A1=A1, A2=A2, d_b1=d_b1, a_b1=a_b1,
                gamma=self.config.game_config.gamma, beta=self.config.game_config.beta,
                C_D=self.config.game_config.C_D, A_P=self.config.game_config.A_P, Z_D_P=self.config.game_config.Z_D_P,
                Z_U=self.config.game_config.Z_U, eta=self.config.game_config.eta)
            local_pomdp_config = IntrusionResponseGameLocalPOMDPDefenderConfig(
                env_name="csle-intrusion-response-game-local-pomdp-defender-v1",
                local_intrusion_response_game_config=local_game_config,
                attacker_strategy=self.config.attacker_strategies[node])
            env = IntrusionResponseGameLocalPOMDPDefenderEnv(config=local_pomdp_config)
            self.local_envs.append(env)

        # Setup spaces
        self.observation_space = self.config.game_config.defender_observation_space()
        self.action_space = self.config.game_config.defender_action_space()

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

        # Get upper bound and random return estimate
        self.upper_bound_return = 0
        self.random_return = 0
        for env in self.local_envs:
            self.upper_bound_return += env.upper_bound_return
            self.random_return += env.random_return

        # State metrics
        self.t = 0

        # Reset
        self.reset()
        super().__init__()

    def step(self, a1: np.ndarray) -> Tuple[np.ndarray, float, bool, Dict[str, Union[float, int]]]:
        """
        Takes a step in the environment by executing the given action

        :param a1: defender action
        :return: (obs, reward, done, info)
        """
        done, info = False, {}

        r = 0
        defender_obs = []
        attacker_obs = []
        d_b = []
        s = []
        a2 = []

        # Step the envs
        for i, local_env in enumerate(self.local_envs):
            local_a1 = a1[i]
            local_o, local_r, local_done, _ = local_env.step(a1=local_a1)
            if local_done:
                done = True
            r = r + local_r
            defender_obs = defender_obs + local_o.tolist()
            s = s + local_env.state.state_vector().tolist()
            a2.append(local_env.trace.attacker_actions[-1])
            attacker_obs = attacker_obs + local_env.trace.attacker_observations[-1].tolist()
            d_b = d_b + local_env.trace.beliefs[-1].tolist()
        defender_obs = np.array(defender_obs)
        s = np.array(s)
        a2 = np.array(a2)
        d_b = np.array(d_b)

        # Update time-step
        self.t += 1

        # Populate info dict
        info[env_constants.ENV_METRICS.STATE] = s
        info[env_constants.ENV_METRICS.DEFENDER_ACTION] = a1
        info[env_constants.ENV_METRICS.ATTACKER_ACTION] = a2
        info[env_constants.ENV_METRICS.OBSERVATION] = defender_obs
        info[env_constants.ENV_METRICS.TIME_STEP] = self.t

        # Log trace
        self.trace.defender_rewards.append(r)
        self.trace.attacker_rewards.append(-r)
        self.trace.attacker_actions.append(a2)
        self.trace.defender_actions.append(a1)
        self.trace.infos.append(info)
        self.trace.states.append(s)
        self.trace.beliefs.append(d_b)
        self.trace.infrastructure_metrics.append(defender_obs)
        if not done:
            self.trace.attacker_observations.append(attacker_obs)
            self.trace.defender_observations.append(defender_obs)

        # Populate info
        info = self._info(info)

        return defender_obs, r, done, info

    def _info(self, info) -> Dict[str, Union[float, int]]:
        """
        Adds the cumulative reward and episode length to the info dict
        :param info: the info dict to update
        :return: the updated info dict
        """
        R = 0
        for i in range(len(self.trace.defender_rewards)):
            R += self.trace.defender_rewards[i] * math.pow(self.config.game_config.gamma, i)
        info[env_constants.ENV_METRICS.RETURN] = R
        info[env_constants.ENV_METRICS.TIME_HORIZON] = len(self.trace.defender_actions)
        info[env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN] = self.upper_bound_return
        info[env_constants.ENV_METRICS.AVERAGE_RANDOM_RETURN] = self.random_return
        return info

    def reset(self, soft: bool = False) -> np.ndarray:
        """
        Resets the environment state, this should be called whenever step() returns <done>

        :return: initial observation
        """
        self.t = 0
        defender_obs = []
        attacker_obs = []
        for local_env in self.local_envs:
            local_o = local_env.reset()
            defender_obs = defender_obs + local_o.tolist()
            attacker_obs = attacker_obs + local_env.trace.attacker_observations[-1].tolist()
        defender_obs = np.array(defender_obs)
        attacker_obs = np.array(attacker_obs)
        if len(self.trace.defender_rewards) > 0:
            self.traces.append(self.trace)
        self.trace = SimulationTrace(simulation_env=self.config.env_name)
        self.trace.attacker_observations.append(attacker_obs)
        self.trace.defender_observations.append(defender_obs)
        return defender_obs

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
        done = False
        o = self.reset()
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
                print(self.state)
            elif raw_input == "D":
                print(done)
            elif raw_input == "H":
                print(self.trace)
            elif raw_input == "R":
                print("Resetting the state")
                o = self.reset()
                print(f"o:{list(map(lambda x: round(x, 3), list(o.tolist())))}")
            else:
                a1 = np.array(list(map(lambda x: int(x), raw_input.split(","))))
                o, r, done, _ = self.step(a1=a1)
                print(f"o:{list(map(lambda x: round(x, 3), list(o.tolist())))}, r:{round(r, 2)}, done: {done}")
