from typing import Tuple, List, Dict, Union, Any
import numpy as np
import numpy.typing as npt
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
            reachable = self.reachable(node)
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
            R = np.array(
                [IntrusionResponseGameUtil.local_reward_tensor(
                    eta=self.config.game_config.eta, C_D=self.config.game_config.C_D, A1=A1, A2=A2,
                    reachable=reachable, beta=self.config.game_config.beta, S=S, Z_U=self.config.game_config.Z_U,
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

        # Setup traces
        self.traces: List[SimulationTrace] = []
        self.trace = SimulationTrace(simulation_env=self.config.env_name)
        self.latest_attacker_obs: Union[npt.NDArray[Any], None] = None

        # Reset
        self.reset()

        # Get upper bound and random return estimate
        self.upper_bound_return = self.get_upper_bound_return(samples=100)
        self.random_return = self.get_random_baseline_return(samples=100)

        # State metrics
        self.t = 0

        # Reset
        self.reset()
        super().__init__()

    def step(self, a1: npt.NDArray[Any]) -> Tuple[npt.NDArray[Any], float, bool, bool, Dict[str, Any]]:
        """
        Takes a step in the environment by executing the given action

        :param a1: defender action
        :return: (obs, reward, terminated, truncated, info)
        """
        done = False
        info: Dict[str, Any] = {}

        r = 0.0
        defender_obs: List[Any] = []
        attacker_obs: List[Any] = []
        d_b: List[float] = []
        s: List[Any] = []
        a2 = []

        # Step the envs
        for i, local_env in enumerate(self.local_envs):
            reachable = self.reachable(i)
            local_a1 = a1[i]
            local_o, local_r, local_done, _, _ = local_env.step(a1=local_a1)
            if not reachable:
                local_r = local_env.config.local_intrusion_response_game_config.C_D[local_a1]
                local_o = np.array([local_o[0], 1, 0, 0])
            if local_done:
                done = True
            r = r + local_r
            defender_obs = defender_obs + list(local_o.tolist())
            s = s + local_env.state.state_vector().tolist()
            a2.append(local_env.trace.attacker_actions[-1])
            attacker_obs = attacker_obs + local_env.trace.attacker_observations[-1].tolist()
            d_b = d_b + local_env.trace.beliefs[-1].tolist()
        defender_obs_np = np.array(defender_obs)
        s_np = np.array(s)
        a2_np = np.array(a2)
        d_b_np = np.array(d_b)

        # Update time-step
        self.t += 1

        # Populate info dict
        info[env_constants.ENV_METRICS.STATE] = s_np
        info[env_constants.ENV_METRICS.DEFENDER_ACTION] = a1
        info[env_constants.ENV_METRICS.ATTACKER_ACTION] = a2_np
        info[env_constants.ENV_METRICS.OBSERVATION] = defender_obs_np
        info[env_constants.ENV_METRICS.TIME_STEP] = self.t

        # Log trace
        self.trace.defender_rewards.append(r)
        self.trace.attacker_rewards.append(-r)
        self.trace.attacker_actions.append(a2_np)
        self.trace.defender_actions.append(a1)
        self.trace.infos.append(info)
        self.trace.states.append(s)
        self.trace.beliefs.append(d_b_np)
        self.trace.infrastructure_metrics.append(defender_obs_np)
        if not done:
            self.trace.attacker_observations.append(attacker_obs)
            self.trace.defender_observations.append(defender_obs_np)

        # Populate info
        info = self._info(info)

        return defender_obs_np, r, done, done, info

    def get_upper_bound_return(self, samples: int = 100) -> float:
        """
        Utiltiy method for getting an upper bound on the average return

        :param samples: the number of sample returns to average
        :return: the estimated upper bound
        """
        max_horizon = 200
        returns = []
        for i in range(samples):
            o, _ = self.reset()
            done = False
            t = 0
            cumulative_reward = 0.0
            while not done and t <= max_horizon:
                r = 0.0
                for i, local_env in enumerate(self.local_envs):
                    reachable = self.reachable(i)
                    local_a1 = 0
                    if reachable and local_env.state.attacker_state() == env_constants.ATTACK_STATES.COMPROMISED:
                        local_a1 = 3
                    local_o, local_r, local_done, _, _ = local_env.step(a1=local_a1)
                    if not reachable:
                        local_r = 0
                    if local_done:
                        done = True
                    r = r + local_r
                cumulative_reward += r * math.pow(self.config.game_config.gamma, t)
                t += 1
            returns.append(cumulative_reward)
        return float(np.mean(np.array(returns)))

    def get_random_baseline_return(self, samples: int = 100) -> float:
        """
        Utiltiy method for getting the average return of a random strategy

        :param samples: the number of sample returns to average
        :return: the estimated upper bound
        """
        max_horizon = 200
        returns = []
        for i in range(samples):
            o, _ = self.reset()
            done = False
            t = 0
            cumulative_reward = 0.0
            while not done and t <= max_horizon:
                r = 0.0
                for i, local_env in enumerate(self.local_envs):
                    reachable = self.reachable(i)
                    local_a1 = np.random.choice(local_env.config.local_intrusion_response_game_config.A1)
                    local_o, local_r, local_done, _, _ = local_env.step(a1=local_a1)
                    if not reachable:
                        local_r = 0
                    if local_done:
                        done = True
                    r = r + local_r
                cumulative_reward += r * math.pow(self.config.game_config.gamma, t)
                t += 1
            returns.append(cumulative_reward)
        return float(np.mean(np.array(returns)))

    def reachable(self, node: int) -> bool:
        """
        Checks if a node is reachable from the gw

        :param node: the node to check
        :return: True if reachable otherwise False
        """
        num_nodes = len(self.config.game_config.nodes)
        A = self.config.game_config.adjacency_matrix.copy()
        for i, local_env in enumerate(self.local_envs):
            if local_env.state.defender_state() in [env_constants.DEFENDER_STATES.SHUTDOWN,
                                                    env_constants.DEFENDER_STATES.REDIRECT]:
                A[i] = [0] * num_nodes
        gw_reachable_nodes = self.config.game_config.gw_reachable
        A = np.array(A)
        for i in range(1, num_nodes + 1):
            A_n = np.linalg.matrix_power(A, i)
            for gw_reachable in gw_reachable_nodes:
                if A_n[gw_reachable][node] != 0:
                    return True
        return False

    def _info(self, info: Dict[str, Union[float, int]]) -> Dict[str, Union[float, int]]:
        """
        Adds the cumulative reward and episode length to the info dict
        :param info: the info dict to update
        :return: the updated info dict
        """
        R = 0.0
        for i in range(len(self.trace.defender_rewards)):
            R += self.trace.defender_rewards[i] * math.pow(self.config.game_config.gamma, i)
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
        self.t = 0
        defender_obs: List[Any] = []
        attacker_obs: List[Any] = []
        for local_env in self.local_envs:
            local_o, _ = local_env.reset()
            defender_obs = defender_obs + local_o.tolist()
            attacker_obs = attacker_obs + local_env.trace.attacker_observations[-1].tolist()
        defender_obs_np = np.array(defender_obs)
        attacker_obs_np = np.array(attacker_obs)
        if len(self.trace.defender_rewards) > 0:
            self.traces.append(self.trace)
        self.trace = SimulationTrace(simulation_env=self.config.env_name)
        self.trace.attacker_observations.append(attacker_obs_np)
        self.trace.defender_observations.append(defender_obs_np)
        info: Dict[str, Any] = {}
        return defender_obs_np, info

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
                print(self.state)
            elif raw_input == "D":
                print(done)
            elif raw_input == "H":
                print(self.trace)
            elif raw_input == "R":
                print("Resetting the state")
                o, _ = self.reset()
                print(f"o:{list(map(lambda x: round(x, 3), list(o.tolist())))}")
            else:
                a1 = np.array(list(map(lambda x: int(x), raw_input.split(","))))
                o, r, done, _, _ = self.step(a1=a1)
                print(f"o:{list(map(lambda x: round(x, 3), list(o.tolist())))}, r:{round(r, 2)}, done: {done}")
