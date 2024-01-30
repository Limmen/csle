import copy
import random
import time
from typing import Tuple, Dict, List, Any, Union
import numpy as np
import numpy.typing as npt
import gymnasium as gym
from csle_common.dao.simulation_config.base_env import BaseEnv
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace
import csle_common.constants.constants as constants
import gym_csle_cyborg.constants.constants as env_constants
from gym_csle_cyborg.dao.blue_agent_action_type import BlueAgentActionType
from gym_csle_cyborg.dao.red_agent_action_type import RedAgentActionType
from gym_csle_cyborg.dao.activity_type import ActivityType
from gym_csle_cyborg.dao.compromised_type import CompromisedType
from gym_csle_cyborg.dao.exploit_type import ExploitType
from gym_csle_cyborg.util.cyborg_env_util import CyborgEnvUtil
from gym_csle_cyborg.dao.csle_cyborg_wrapper_config import CSLECyborgWrapperConfig


class CyborgScenarioTwoWrapper(BaseEnv):
    """
    A Wrapper Gym Environment for Cyborg scenario 2
    """

    def __init__(self, config: CSLECyborgWrapperConfig) -> None:
        """
        Initializes the environment

        :param config: the environment configuration
        """

        # Initialize metadata
        self.config = config
        action_id_to_type_and_host, type_and_host_to_action_id = CyborgEnvUtil.get_action_dicts(
            scenario=2, reduced_action_space=True, decoy_optimization=False, decoy_state=True)
        self.action_id_to_type_and_host = action_id_to_type_and_host
        self.type_and_host_to_action_id = type_and_host_to_action_id
        self.maximum_steps = self.config.maximum_steps
        self.initial_observation = CyborgScenarioTwoWrapper.initial_obs_vector()
        self.hosts = CyborgEnvUtil.get_cyborg_hosts()
        self.host_compromised_costs = CyborgEnvUtil.get_host_compromised_costs()
        self.red_agent_action_types = CyborgEnvUtil.get_red_agent_action_types()
        self.cyborg_host_values = CyborgEnvUtil.get_cyborg_host_values()
        self.red_agent_jumps = [0, 1, 2, 2, 2, 2, 5, 5, 5, 5, 9, 9, 9, 12, 13]
        self.action_id_to_type_and_host = action_id_to_type_and_host
        self.decoy_action_types = CyborgEnvUtil.get_decoy_action_types(scenario=2)
        self.decoy_actions_per_host = CyborgEnvUtil.get_decoy_actions_per_host(scenario=2)
        self.host_to_subnet = CyborgEnvUtil.cyborg_host_to_subnet()
        self.host_ports_map = CyborgEnvUtil.cyborg_host_ports_map()
        self.decoy_to_port = CyborgEnvUtil.cyborg_decoy_actions_to_port()
        self.exploit_values = CyborgEnvUtil.exploit_values()
        self.exploit_ports = CyborgEnvUtil.exploit_ports()
        self.exploits = CyborgEnvUtil.exploits()

        # Initialize state
        self.s = CyborgScenarioTwoWrapper.initial_state_vector()
        self.last_obs = CyborgScenarioTwoWrapper.initial_obs_vector()
        self.op_server_restored = False
        self.red_agent_state = 0
        self.red_agent_target = 0
        self.t = 1
        self.red_action_targets = {}
        self.red_action_targets[self.red_agent_state] = self.red_agent_target
        self.scan_state = [0 for _ in self.hosts]
        self.privilege_escalation_detected: Union[None, int] = None

        self.initial_particles = [
            (
                copy.deepcopy(self.s), copy.deepcopy(self.scan_state), self.op_server_restored,
                copy.deepcopy(self.last_obs), copy.deepcopy(self.red_action_targets),
                self.privilege_escalation_detected, self.red_agent_state, self.red_agent_target
            )
        ]

        # Setup gym spaces
        self.defender_observation_space = gym.spaces.Box(
            -1, 2, ((6 + len(self.decoy_action_types)) * len(self.hosts),), np.float32)
        self.defender_action_space = gym.spaces.Discrete(len(list(self.action_id_to_type_and_host.keys())))
        self.action_space = self.defender_action_space
        self.observation_space = self.defender_observation_space

        # Setup traces
        self.traces: List[SimulationTrace] = []
        self.trace = SimulationTrace(simulation_env=self.config.gym_env_name)

    def step(self, action: int) -> Tuple[npt.NDArray[Any], float, bool, bool, Dict[str, Any]]:
        """
        Takes a step in the environment

        :param action: the defender action
        :return: (obs, reward, terminated, truncated, info)
        """
        defender_action_type, defender_action_host = self.action_id_to_type_and_host[action]
        defender_action_host_id = self.hosts.index(defender_action_host)
        if defender_action_type == BlueAgentActionType.RESTORE and \
                defender_action_host == env_constants.CYBORG.OP_SERVER0:
            self.op_server_restored = True
        self.red_action_targets[self.red_agent_state] = self.red_agent_target
        if self.privilege_escalation_detected is not None:
            self.last_obs[self.privilege_escalation_detected][env_constants.CYBORG.HOST_STATE_ACCESS_IDX] = \
                CompromisedType.PRIVILEGED.value
            self.privilege_escalation_detected = None
        s_prime, last_obs = self.apply_defender_action_to_state(s=self.s, defender_action_type=defender_action_type,
                                                                defender_action_host_id=defender_action_host_id,
                                                                decoy_action_types=self.decoy_action_types,
                                                                decoy_actions_per_host=self.decoy_actions_per_host,
                                                                last_obs=self.last_obs)
        self.last_obs = last_obs
        next_red_action_type = CyborgScenarioTwoWrapper.get_red_agent_action_type_from_state(
            red_agent_state=self.red_agent_state)
        is_red_action_feasible = CyborgScenarioTwoWrapper.is_red_action_feasible(red_agent_state=self.red_agent_state,
                                                                                 s=s_prime,
                                                                                 target_host_id=self.red_agent_target)
        exploit_successful = True
        root = False
        decoy_state = s_prime[self.red_agent_target][env_constants.CYBORG.HOST_STATE_DECOY_IDX]
        decoy_r = 0
        if next_red_action_type == RedAgentActionType.EXPLOIT_REMOTE_SERVICE:
            exploit_action, root, decoy = CyborgScenarioTwoWrapper.next_exploit(
                target_host=self.red_agent_target, decoy_state=decoy_state, host_ports_map=self.host_ports_map,
                decoy_actions_per_host=self.decoy_actions_per_host, decoy_to_port=self.decoy_to_port,
                exploit_values=self.exploit_values, exploit_ports=self.exploit_ports, exploits=self.exploits
            )
            if decoy:
                exploit_successful = False
                decoy_r += decoy_state*0.1
            if self.hosts[self.red_agent_target] == env_constants.CYBORG.ENTERPRISE1 \
                    and exploit_action == ExploitType.ETERNAL_BLUE.value:
                exploit_successful = False
            if self.hosts[self.red_agent_target] == env_constants.CYBORG.ENTERPRISE2 \
                    and exploit_action == ExploitType.ETERNAL_BLUE.value:
                exploit_successful = False
            if self.hosts[self.red_agent_target] == env_constants.CYBORG.USER3 \
                    and exploit_action == ExploitType.BLUE_KEEP.value:
                exploit_successful = False
        red_base_jump = self.red_agent_state == 12 and not is_red_action_feasible
        if red_base_jump:
            next_red_agent_state = 1
            next_red_agent_target = self.red_action_targets[next_red_agent_state]
        else:
            if is_red_action_feasible and exploit_successful:
                next_red_agent_state = (self.red_agent_state + 1) if self.red_agent_state < 14 else 14
                next_red_agent_target = CyborgScenarioTwoWrapper.sample_next_red_agent_target(
                    red_agent_state=next_red_agent_state, red_agent_target=self.red_agent_target)
            else:
                next_red_agent_state = self.red_agent_jumps[self.red_agent_state]
                next_red_agent_target = self.red_action_targets[next_red_agent_state]

        activity = ActivityType.NONE
        if is_red_action_feasible:
            if next_red_action_type == RedAgentActionType.EXPLOIT_REMOTE_SERVICE:
                if exploit_successful:
                    exploit_access = CompromisedType.USER
                    if root:
                        exploit_access = CompromisedType.PRIVILEGED
                    detect = random.uniform(0, 1) < 0.95
                    s_prime, obs = CyborgScenarioTwoWrapper.apply_red_exploit(s=s_prime, exploit_access=exploit_access,
                                                                              target_host_id=self.red_agent_target,
                                                                              observation=self.last_obs, detect=detect)
                    self.last_obs = obs
                    if detect:
                        activity = ActivityType.EXPLOIT
                    else:
                        activity = ActivityType.SCAN
            elif next_red_action_type == RedAgentActionType.DISCOVER_REMOTE_SYSTEMS:
                s_prime = CyborgScenarioTwoWrapper.apply_red_network_scan(s=s_prime,
                                                                          target_subnetwork=self.red_agent_target)
            elif next_red_action_type == RedAgentActionType.DISCOVER_NETWORK_SERVICES:
                s_prime = CyborgScenarioTwoWrapper.apply_red_host_scan(s=s_prime, target_host_id=self.red_agent_target)
                activity = ActivityType.SCAN
            elif next_red_action_type == RedAgentActionType.PRIVILEGE_ESCALATE:
                if s_prime[self.red_agent_target][env_constants.CYBORG.HOST_STATE_ACCESS_IDX] \
                        != CompromisedType.PRIVILEGED.value:
                    self.privilege_escalation_detected = self.red_agent_target
                s_prime = CyborgScenarioTwoWrapper.apply_red_privilege_escalation(
                    s=s_prime, target_host_id=self.red_agent_target, red_agent_state=self.red_agent_state,
                    next_target_host_id=next_red_agent_target)
        self.s = s_prime
        self.red_agent_target = next_red_agent_target
        self.red_agent_state = next_red_agent_state

        obs, obs_tensor, scan_state = CyborgScenarioTwoWrapper.generate_observation(
            s=s_prime, scan_state=self.scan_state, decoy_action_types=self.decoy_action_types,
            decoy_actions_per_host=self.decoy_actions_per_host,
            last_obs=self.last_obs, activity=activity, red_agent_target=self.red_agent_target)
        r = self.reward_function(defender_action_type=defender_action_type, red_action_type=next_red_action_type,
                                 red_success=(is_red_action_feasible and exploit_successful))
        info: Dict[str, Any] = {}
        info[env_constants.ENV_METRICS.STATE] = (
            copy.deepcopy(s_prime), scan_state, self.op_server_restored,
            obs, copy.deepcopy(self.red_action_targets),
            self.privilege_escalation_detected, self.red_agent_state, self.red_agent_target
        )
        info[env_constants.ENV_METRICS.OBSERVATION] = CyborgEnvUtil.state_vector_to_state_id(
            state_vector=obs, observation=True
        )
        info[env_constants.ENV_METRICS.OBSERVATION_VECTOR] = obs
        self.scan_state = copy.deepcopy(scan_state)
        self.s = s_prime
        self.last_obs = copy.deepcopy(obs)
        done = False
        self.t += 1
        if self.t >= self.maximum_steps:
            done = True

        # Log trace
        if self.config.save_trace:
            self.trace = CyborgScenarioTwoWrapper.log_trace(
                r=float(r), trace=self.trace, o=info[env_constants.ENV_METRICS.OBSERVATION], done=done, action=action)
        if self.config.reward_shaping:
            r += decoy_r
        return np.array(obs_tensor), r, done, done, info

    def reset(self, seed: Union[None, int] = None, soft: bool = False, options: Union[Dict[str, Any], None] = None) \
            -> Tuple[npt.NDArray[Any], Dict[str, Any]]:
        """
        Resets the environment

        :param seed: the random seed
        :param soft: whether to do a soft reset or not
        :param options: reset options
        :return: the reset observation and info dict
        """
        self.s = self.initial_state_vector()
        self.op_server_restored = False
        self.privilege_escalation_detected = None
        self.red_agent_state = 0
        self.red_agent_target = 0
        self.scan_state = [0 for _ in self.hosts]
        self.t = 0
        self.red_action_targets = {}
        self.red_action_targets[self.red_agent_state] = self.red_agent_target
        obs_vec = self.initial_obs_vector()
        obs_tensor = self.initial_obs_tensor()
        self.last_obs = copy.deepcopy(obs_vec)
        info: Dict[str, Any] = {}
        info[env_constants.ENV_METRICS.STATE] = (
            copy.deepcopy(self.s), copy.deepcopy(self.scan_state), self.op_server_restored,
            copy.deepcopy(obs_vec), copy.deepcopy(self.red_action_targets),
            self.privilege_escalation_detected, self.red_agent_state, self.red_agent_target
        )
        info[env_constants.ENV_METRICS.OBSERVATION] = CyborgEnvUtil.state_vector_to_state_id(
            state_vector=obs_vec, observation=True
        )
        info[env_constants.ENV_METRICS.OBSERVATION_VECTOR] = obs_vec
        self.traces = []
        self.trace = SimulationTrace(simulation_env=self.config.gym_env_name)
        return np.array(obs_tensor), info

    def reward_function(self, defender_action_type: BlueAgentActionType,
                        red_action_type: RedAgentActionType, red_success: bool) -> float:
        """
        The reward function

        :param defender_action_type: the type of the defender's action
        :param red_action_type: the type of the attacker's action
        :param red_success: a boolean flag indicating whether the red agent's action was successful
        :return: the reward
        """
        r = 0.0
        if defender_action_type == BlueAgentActionType.RESTORE:
            r -= 1
        for i in range(len(self.s)):
            access_state = self.s[i][env_constants.CYBORG.HOST_STATE_ACCESS_IDX]
            if access_state == CompromisedType.PRIVILEGED:
                r += self.host_compromised_costs[i]
        if red_action_type == RedAgentActionType.IMPACT and red_success and not self.op_server_restored:
            r -= 10
        return r

    def set_state(self, state: Tuple[List[List[int]], List[int], bool, List[List[int]],
                                     Dict[int, int], bool, int, int]) -> None:
        """
        Sets the state of the environment

        :param s: the new state
        :return: None
        """
        self.s = copy.deepcopy(state[0])
        self.scan_state = copy.deepcopy(state[1])
        self.op_server_restored = state[2]
        self.last_obs = copy.deepcopy(state[3])
        self.red_action_targets = copy.deepcopy(state[4])
        self.privilege_escalation_detected = state[5]
        self.red_agent_state = state[6]
        self.red_agent_target = state[7]

    def get_observation_from_history(self, history: List[List[Any]]) -> List[Any]:
        """
        Gets an observation from the observation history

        :param history: the observation history
        :return: the latest observation from the history
        """
        obs_id = history[-1]
        obs_vec = CyborgEnvUtil.state_id_to_state_vector(state_id=obs_id, observation=True)
        obs_tensor = []
        for host in range(len(obs_vec)):
            obs_tensor.extend(CyborgScenarioTwoWrapper.host_obs_one_hot_encoding(
                host_obs=obs_vec[host], decoy_actions_per_host=self.decoy_actions_per_host,
                decoy_action_types=self.decoy_action_types, host_id=host
            ))
        return obs_tensor

    def is_state_terminal(self, state: int) -> bool:
        """
        Checks whether a given state is terminal or not

        :param state: the state id
        :return: True if terminal, else False
        """
        return False

    @staticmethod
    def initial_state_vector() -> List[List[int]]:
        """
        :return: gets the initial state vector
        """
        return [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
                [0, 0, 0, 0], [1, 0, 2, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    @staticmethod
    def initial_obs_vector() -> List[List[int]]:
        """
        :return: gets the initial observation vector
        """
        return [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
                [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    @staticmethod
    def initial_obs_tensor() -> List[int]:
        """
        :return: gets the initial observation tensor
        """
        return [0] * 14 * 13

    @staticmethod
    def get_red_agent_action_type_from_state(red_agent_state: int) -> RedAgentActionType:
        """
        Gets the red agent action type from the red agent state

        :param red_agent_state: the state of the red agent
        :return: the type of red agent action
        """
        if red_agent_state == 0:
            return RedAgentActionType.DISCOVER_REMOTE_SYSTEMS
        elif red_agent_state == 1:
            return RedAgentActionType.DISCOVER_NETWORK_SERVICES
        elif red_agent_state == 2:
            return RedAgentActionType.EXPLOIT_REMOTE_SERVICE
        elif red_agent_state == 3:
            return RedAgentActionType.PRIVILEGE_ESCALATE
        elif red_agent_state == 4:
            return RedAgentActionType.DISCOVER_NETWORK_SERVICES
        elif red_agent_state == 5:
            return RedAgentActionType.EXPLOIT_REMOTE_SERVICE
        elif red_agent_state == 6:
            return RedAgentActionType.PRIVILEGE_ESCALATE
        elif red_agent_state == 7:
            return RedAgentActionType.DISCOVER_REMOTE_SYSTEMS
        elif red_agent_state == 8:
            return RedAgentActionType.DISCOVER_NETWORK_SERVICES
        elif red_agent_state == 9:
            return RedAgentActionType.EXPLOIT_REMOTE_SERVICE
        elif red_agent_state == 10:
            return RedAgentActionType.PRIVILEGE_ESCALATE
        elif red_agent_state == 11:
            return RedAgentActionType.DISCOVER_NETWORK_SERVICES
        elif red_agent_state == 12:
            return RedAgentActionType.EXPLOIT_REMOTE_SERVICE
        elif red_agent_state == 13:
            return RedAgentActionType.PRIVILEGE_ESCALATE
        elif red_agent_state == 14:
            return RedAgentActionType.IMPACT
        else:
            raise ValueError(f"Invalid attacker state: {red_agent_state}")

    @staticmethod
    def red_agent_state_to_target_distribution(red_agent_state: int, last_target: int = -1) -> List[float]:
        """
        Gets a distribution over the next target of the red agent based on its current state and previous target

        :param red_agent_state: the state of the red agent
        :param last_target: the previous target of the red agent
        :return: a distribution over the next target of the red agent
        """
        if red_agent_state == 0:
            return [1.0, 0, 0]
        elif red_agent_state == 1:
            return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0.25, 0.25, 0.25, 0.25]
        elif red_agent_state in [2, 3, 5, 6, 9, 10, 12, 13, 14]:
            prob: List[float] = [0.0] * 13
            prob[last_target] = 1
            return prob
        elif red_agent_state == 4:
            if last_target == 12 or last_target == 11:
                return [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            elif last_target == 9 or last_target == 10:
                return [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            else:
                raise ValueError(f"Invalid last target: {last_target}")
        elif red_agent_state == 7:
            return [0, 1.0, 0]
        elif red_agent_state == 8:
            return [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif red_agent_state == 11:
            return [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        else:
            raise ValueError(f"Invalid attacker state: {red_agent_state}")

    @staticmethod
    def is_red_action_feasible(red_agent_state: int, s: List[List[int]], target_host_id: int) -> bool:
        """
        Checks whether a given red agent is feasible or not

        :param red_agent_state: the red agent state
        :param s: the current state
        :param target_host_id: the target host id
        :return: True if feasible, else False
        """
        if red_agent_state == 0:
            return True
        elif red_agent_state == 1:
            return s[target_host_id][env_constants.CYBORG.HOST_STATE_KNOWN_IDX] == 1
        elif red_agent_state == 2:
            return s[target_host_id][env_constants.CYBORG.HOST_STATE_SCANNED_IDX] == 1
        elif red_agent_state == 3:
            return s[target_host_id][env_constants.CYBORG.HOST_STATE_ACCESS_IDX] > 0
        elif red_agent_state == 4:
            return s[target_host_id][env_constants.CYBORG.HOST_STATE_KNOWN_IDX] == 1
        elif red_agent_state == 5:
            return s[target_host_id][env_constants.CYBORG.HOST_STATE_SCANNED_IDX] == 1
        elif red_agent_state == 6:
            return s[target_host_id][env_constants.CYBORG.HOST_STATE_ACCESS_IDX] > 0
        elif red_agent_state == 7:
            return (s[1][env_constants.CYBORG.HOST_STATE_ACCESS_IDX] > 0 or s[2][
                env_constants.CYBORG.HOST_STATE_ACCESS_IDX] > 0)
        elif red_agent_state == 8:
            return s[3][env_constants.CYBORG.HOST_STATE_KNOWN_IDX] == 1
        elif red_agent_state == 9:
            return s[3][env_constants.CYBORG.HOST_STATE_SCANNED_IDX] == 1
        elif red_agent_state == 10:
            return s[3][env_constants.CYBORG.HOST_STATE_ACCESS_IDX] > 0
        elif red_agent_state == 11:
            return (s[3][env_constants.CYBORG.HOST_STATE_ACCESS_IDX] == CompromisedType.PRIVILEGED.value
                    and s[7][env_constants.CYBORG.HOST_STATE_KNOWN_IDX] == 1)
        elif red_agent_state == 12:
            return (s[7][env_constants.CYBORG.HOST_STATE_SCANNED_IDX] == 1 and
                    s[3][env_constants.CYBORG.HOST_STATE_ACCESS_IDX] == CompromisedType.PRIVILEGED.value)
        elif red_agent_state == 13:
            return s[7][env_constants.CYBORG.HOST_STATE_ACCESS_IDX] > 0
        elif red_agent_state == 14:
            return s[7][env_constants.CYBORG.HOST_STATE_ACCESS_IDX] == 2
        else:
            raise ValueError(f"Invalid red agent state: {red_agent_state}")

    @staticmethod
    def apply_defender_action_to_state(s: List[List[int]], defender_action_type: BlueAgentActionType,
                                       defender_action_host_id: int, decoy_action_types: List[BlueAgentActionType],
                                       decoy_actions_per_host: List[List[BlueAgentActionType]],
                                       last_obs: List[List[int]]) -> Tuple[List[List[int]], List[List[int]]]:
        """
        Applies a given defender action to the state

        :param s: the state to apply the action to
        :param defender_action_type: the type of the defender's action
        :param defender_action_host_id: the id of the host that the defender targets
        :param decoy_action_types: a list of decoy action types
        :param decoy_actions_per_host: a list of decoy action types per host
        :param last_obs: the last observation
        :return: the updated state and observation
        """
        if (defender_action_type in decoy_action_types
                and s[defender_action_host_id][env_constants.CYBORG.HOST_STATE_DECOY_IDX] ==
                len(decoy_actions_per_host[defender_action_host_id])):
            defender_action_type = BlueAgentActionType.REMOVE
        if defender_action_type in decoy_action_types:
            s[defender_action_host_id][env_constants.CYBORG.HOST_STATE_DECOY_IDX] = min(
                s[defender_action_host_id][env_constants.CYBORG.HOST_STATE_DECOY_IDX] + 1,
                len(decoy_actions_per_host[defender_action_host_id]))
            last_obs[defender_action_host_id][env_constants.CYBORG.HOST_STATE_DECOY_IDX] = \
                s[defender_action_host_id][env_constants.CYBORG.HOST_STATE_DECOY_IDX]
        elif defender_action_type == BlueAgentActionType.RESTORE:
            s[defender_action_host_id][env_constants.CYBORG.HOST_STATE_ACCESS_IDX] = CompromisedType.NO.value
            s[defender_action_host_id][env_constants.CYBORG.HOST_STATE_DECOY_IDX] = 0
            last_obs[defender_action_host_id][env_constants.CYBORG.HOST_STATE_ACCESS_IDX] = CompromisedType.NO.value
            last_obs[defender_action_host_id][env_constants.CYBORG.HOST_STATE_DECOY_IDX] = 0
        elif defender_action_type == BlueAgentActionType.REMOVE:
            if s[defender_action_host_id][env_constants.CYBORG.HOST_STATE_ACCESS_IDX] == CompromisedType.USER.value:
                s[defender_action_host_id][env_constants.CYBORG.HOST_STATE_ACCESS_IDX] = CompromisedType.NO.value
                last_obs[defender_action_host_id][env_constants.CYBORG.HOST_STATE_ACCESS_IDX] = \
                    CompromisedType.UNKNOWN.value
        elif defender_action_type == BlueAgentActionType.ANALYZE:
            last_obs[defender_action_host_id][env_constants.CYBORG.HOST_STATE_ACCESS_IDX] = \
                s[defender_action_host_id][env_constants.CYBORG.HOST_STATE_ACCESS_IDX]
        return s, last_obs

    @staticmethod
    def sample_next_red_agent_target(red_agent_state: int, red_agent_target: int) -> int:
        """
        Samples the next red agent target

        :param red_agent_target: the current target of the red agent
        :param red_agent_state: the new state of the red agent
        :return: the next target host id of the red agent
        """
        target_dist = CyborgScenarioTwoWrapper.red_agent_state_to_target_distribution(
            red_agent_state=red_agent_state, last_target=red_agent_target)
        next_target = np.random.choice(np.arange(0, len(target_dist)), p=target_dist)
        return int(next_target)

    @staticmethod
    def apply_red_exploit(s: List[List[int]], exploit_access: CompromisedType, target_host_id: int,
                          observation: List[List[int]], detect: bool = False) \
            -> Tuple[List[List[int]], List[List[int]]]:
        """
        Applies a successful red exploit to the state

        :param s: the current state
        :param observation: the current observation
        :param exploit_access: the access type of the exploit
        :param target_host_id: the targeted host id
        :param detect: boolean flag indicating whether the exploit was detected or not
        :return: the updated state
        """
        s[target_host_id][env_constants.CYBORG.HOST_STATE_ACCESS_IDX] = \
            max(exploit_access.value, s[target_host_id][env_constants.CYBORG.HOST_STATE_ACCESS_IDX])
        if detect:
            access_val = CompromisedType.USER.value
            if observation[target_host_id][env_constants.CYBORG.HOST_STATE_ACCESS_IDX] \
                    == CompromisedType.PRIVILEGED.value:
                access_val = CompromisedType.PRIVILEGED.value
            observation[target_host_id][env_constants.CYBORG.HOST_STATE_ACCESS_IDX] = access_val
        return s, observation

    @staticmethod
    def apply_red_network_scan(s: List[List[int]], target_subnetwork: int) -> List[List[int]]:
        """
        Applies a successful red scan of a subnetwork to the state

        :param s: the current state
        :param obs: the current observation
        :param target_subnetwork: the targeted subnetwork id
        :return: the updated state
        """
        if target_subnetwork == 0:
            s[12][env_constants.CYBORG.HOST_STATE_KNOWN_IDX] = 1
            s[11][env_constants.CYBORG.HOST_STATE_KNOWN_IDX] = 1
            s[10][env_constants.CYBORG.HOST_STATE_KNOWN_IDX] = 1
            s[9][env_constants.CYBORG.HOST_STATE_KNOWN_IDX] = 1
        if target_subnetwork == 1:
            s[0][env_constants.CYBORG.HOST_STATE_KNOWN_IDX] = 1
            s[1][env_constants.CYBORG.HOST_STATE_KNOWN_IDX] = 1
            s[2][env_constants.CYBORG.HOST_STATE_KNOWN_IDX] = 1
            s[3][env_constants.CYBORG.HOST_STATE_KNOWN_IDX] = 1
        return s

    @staticmethod
    def apply_red_host_scan(s: List[List[int]], target_host_id: int) -> List[List[int]]:
        """
        Applies a successful red host scan to the state

        :param s: the current state
        :param target_host_id: the targeted host id
        :return: the updated state
        """
        s[target_host_id][env_constants.CYBORG.HOST_STATE_SCANNED_IDX] = 1
        return s

    @staticmethod
    def apply_red_privilege_escalation(s: List[List[int]], target_host_id: int, red_agent_state: int,
                                       next_target_host_id: int) -> List[List[int]]:
        """
        Applies a successful red privilege escalation to the state

        :param s: the current state
        :param target_host_id: the targeted host id
        :param red_agent_state: the state of the red agent
        :param next_target_host_id: the id of the next targeted host
        :return: the updated state
        """
        s[target_host_id][env_constants.CYBORG.HOST_STATE_ACCESS_IDX] = CompromisedType.PRIVILEGED.value
        if red_agent_state == 3 or red_agent_state == 10:
            s[next_target_host_id][env_constants.CYBORG.HOST_STATE_KNOWN_IDX] = 1
        return s

    @staticmethod
    def generate_observation(s: List[List[int]], scan_state: List[int], decoy_action_types: List[BlueAgentActionType],
                             decoy_actions_per_host: List[List[BlueAgentActionType]],
                             last_obs: List[List[int]], activity: ActivityType, red_agent_target: int) \
            -> Tuple[List[List[int]], List[int], List[int]]:
        """
        Generates the defender observation based on the current state

        :param s: the current state
        :param scan_state: the current scanned state
        :param red_agent_target: the target of the red agent
        :param decoy_action_types: the list of decoy action types
        :param decoy_actions_per_host: the list of decoy actions per host
        :param last_obs: the last observation
        :param activity: the observed activity
        :return: the latest observation, the one-hot encoded observation, and the updated scanned state
        """
        obs = []
        obs_tensor = []
        for host_id in range(len(s)):
            if host_id == 8:
                host_obs = [0, 0, 0, 0]
            else:
                compromised_obs = last_obs[host_id][env_constants.CYBORG.HOST_STATE_ACCESS_IDX]
                host_decoy_state = last_obs[host_id][env_constants.CYBORG.HOST_STATE_DECOY_IDX]
                host_activity = 0
                if host_id == red_agent_target:
                    host_activity = activity.value
                    if activity == ActivityType.SCAN:
                        scan_state = [1 if x == 2 else x for x in scan_state]
                        scan_state[host_id] = 2
                host_obs = [host_activity, scan_state[host_id], compromised_obs, host_decoy_state]
            obs.append(host_obs)
            obs_tensor.extend(CyborgScenarioTwoWrapper.host_obs_one_hot_encoding(
                host_obs=host_obs, decoy_action_types=decoy_action_types,
                decoy_actions_per_host=decoy_actions_per_host, host_id=host_id))
        return obs, obs_tensor, scan_state

    @staticmethod
    def host_obs_one_hot_encoding(host_obs: List[int], decoy_action_types: List[BlueAgentActionType],
                                  decoy_actions_per_host: List[List[BlueAgentActionType]], host_id: int) -> List[int]:
        """
        Gets a one-hot encoded version of a host observation

        :param host_obs: the host observation
        :param decoy_action_types: the list of decoy action types
        :param decoy_actions_per_host: the list of decoy action types per host
        :param host_id: the id of the host
        :return: the one hot encoded observation vector
        """
        one_hot_encoded_vector = []
        if host_obs[0] == ActivityType.NONE:
            one_hot_encoded_vector.extend([0, 0])
        elif host_obs[0] == ActivityType.SCAN:
            one_hot_encoded_vector.extend([1, 0])
        elif host_obs[0] == ActivityType.EXPLOIT:
            one_hot_encoded_vector.extend([1, 1])
        if host_obs[2] == CompromisedType.NO:
            one_hot_encoded_vector.extend([0, 0])
        elif host_obs[2] == CompromisedType.USER:
            one_hot_encoded_vector.extend([0, 1])
        elif host_obs[2] == CompromisedType.PRIVILEGED:
            one_hot_encoded_vector.extend([1, 1])
        elif host_obs[2] == CompromisedType.UNKNOWN:
            one_hot_encoded_vector.extend([1, 0])
        if host_obs[1] == 0:
            one_hot_encoded_vector.extend([0, 0])
        elif host_obs[1] == 1:
            one_hot_encoded_vector.extend([0, 1])
        elif host_obs[1] == 2:
            one_hot_encoded_vector.extend([1, 1])
        decoy_obs = [0] * len(decoy_action_types)
        for j in range(host_obs[3]):
            decoy_obs[decoy_action_types.index(decoy_actions_per_host[host_id][j])] = 1
        one_hot_encoded_vector.extend(decoy_obs)
        return one_hot_encoded_vector

    def get_action_space(self) -> List[int]:
        """
        Gets the action space of the defender

        :return: a list of action ids
        """
        return list(self.action_id_to_type_and_host.keys())

    @staticmethod
    def next_exploit(target_host: int, decoy_state: int, host_ports_map: Dict[int, List[Tuple[int, bool]]],
                     decoy_actions_per_host: List[List[BlueAgentActionType]], decoy_to_port: Dict[int, List[int]],
                     exploit_values: Dict[int, float], exploit_ports: Dict[int, List[int]],
                     exploits: List[ExploitType]) -> Tuple[int, bool, bool]:
        """
        Calculates the next exploit of the attacker

        :param target_host: the target of the attacker
        :param decoy_state: the decoy state of the targeted host
        :param host_ports_map: a map from host to ports
        :param decoy_actions_per_host: a list of decoy actions per host
        :param decoy_to_port: a map from decoy action to port
        :param exploit_values: a map of exploits to their values to the attacker
        :param exploit_ports: a map from exploit to required ports
        :param exploits: the list of exploits
        :return: the next exploit, whether it gives root or not, and whether it is a decoy or not
        """
        decoy_actions = decoy_actions_per_host[target_host]
        decoy_ports = []
        for i in range(decoy_state):
            decoy_ports.extend(decoy_to_port[decoy_actions[i]])
        ports = host_ports_map[target_host]
        feasible_exploits = []
        feasible_exploits_values = []
        feasible_exploit_access = []
        decoy_exploits = []
        for exploit in exploits:
            exploit_access = False
            exploit_feasible = False
            exploit_decoy = False
            for port_access in ports:
                port, access = port_access
                if port in exploit_ports[exploit.value]:
                    exploit_feasible = True
                    if not exploit_access:
                        exploit_access = access
            if not exploit_feasible:
                for port in decoy_ports:
                    if port in exploit_ports[exploit.value]:
                        exploit_decoy = True
                        exploit_feasible = True
            if exploit_feasible:
                feasible_exploits.append(exploit)
                feasible_exploits_values.append(exploit_values[exploit.value])
                feasible_exploit_access.append(exploit_access)
                decoy_exploits.append(exploit_decoy)
        if len(feasible_exploits) == 0:
            return -1, False, False
        top_choice = np.argmax(feasible_exploits_values)
        if len(feasible_exploits) == 1 or random.uniform(0, 1) < 0.75:
            return feasible_exploits[top_choice], feasible_exploit_access[top_choice], decoy_exploits[top_choice]
        else:
            alternatives = [x for x in list(range(len(feasible_exploits))) if x != top_choice]
            random_choice = np.random.choice(list(range(len(alternatives))))
            return (feasible_exploits[random_choice], feasible_exploit_access[random_choice],
                    decoy_exploits[random_choice])

    @staticmethod
    def log_trace(r: float, trace: SimulationTrace, o: npt.NDArray[Any], done: bool, action: int) -> SimulationTrace:
        """
        Logs information in a trace

        :param r: the reward
        :param trace: the trace
        :param o: the observation
        :param done: the done flag
        :param action: the action
        :return: the updated trace
        """
        trace.defender_rewards.append(float(r))
        trace.attacker_rewards.append(-float(r))
        trace.attacker_actions.append(0)
        trace.defender_actions.append(action)
        trace.infos.append({})
        trace.states.append(0.0)
        trace.beliefs.append(0.0)
        trace.infrastructure_metrics.append(o)
        if not done:
            trace.attacker_observations.append(o)
            trace.defender_observations.append(o)
        return trace

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
        return None
