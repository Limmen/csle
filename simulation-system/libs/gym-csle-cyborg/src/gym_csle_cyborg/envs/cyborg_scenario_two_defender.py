from typing import Tuple, Dict, List, Any, Union
from copy import deepcopy
import time
import numpy as np
from prettytable import PrettyTable
import numpy.typing as npt
import gymnasium as gym
import random
from csle_cyborg.agents.wrappers.challenge_wrapper import ChallengeWrapper
import csle_common.constants.constants as constants
from csle_common.dao.simulation_config.base_env import BaseEnv
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace
import gym_csle_cyborg.constants.constants as env_constants
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.blue_agent_action_type import BlueAgentActionType
from gym_csle_cyborg.dao.activity_type import ActivityType
from gym_csle_cyborg.dao.compromised_type import CompromisedType
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.dao.red_agent_action_type import RedAgentActionType
from gym_csle_cyborg.util.cyborg_env_util import CyborgEnvUtil


class CyborgScenarioTwoDefender(BaseEnv):
    """
    OpenAI Gym Env for CybORG scenario 2 from the defender's perspective
    """

    def __init__(self, config: CSLECyborgConfig):
        """
        Initializes the environment

        :param config: the environment configuration
        """
        self.config = config

        # Setup Cyborg Env
        (cyborg_scenario_config_path, cyborg_challenge_env, cyborg_hostnames, cyborg_hostname_to_id,
         cyborg_subnets, cyborg_subnet_to_id, cyborg_action_id_to_type_and_host, cyborg_action_type_and_host_to_id,
         red_agent_type) = CyborgEnvUtil.setup_cyborg_env(config=self.config)
        self.cyborg_scenario_config_path = cyborg_scenario_config_path
        self.cyborg_challenge_env = cyborg_challenge_env
        self.cyborg_hostnames = cyborg_hostnames
        self.cyborg_hostname_to_id = cyborg_hostname_to_id
        self.cyborg_subnets = cyborg_subnets
        self.cyborg_subnet_to_id = cyborg_subnet_to_id
        self.cyborg_action_id_to_type_and_host = cyborg_action_id_to_type_and_host
        self.cyborg_action_type_and_host_to_id = cyborg_action_type_and_host_to_id
        self.red_agent_type = red_agent_type

        # Setup defender decoy actions
        self.decoy_action_types = CyborgEnvUtil.get_decoy_action_types(scenario=self.config.scenario)
        self.decoy_actions_per_host = CyborgEnvUtil.get_decoy_actions_per_host(scenario=self.config.scenario)

        # Initialize defender state
        scan_state, decoy_state = CyborgScenarioTwoDefender.reset_scan_and_decoy_states(
            cyborg_hostnames=self.cyborg_hostnames)
        self.scan_state = scan_state
        self.decoy_state = decoy_state
        self.t = 1

        # Setup reduced action space
        action_id_to_type_and_host, type_and_host_to_action_id = CyborgEnvUtil.get_action_dicts(
            scenario=self.config.scenario, decoy_state=self.config.decoy_state,
            reduced_action_space=self.config.reduced_action_space, decoy_optimization=self.config.decoy_optimization)
        self.action_id_to_type_and_host = action_id_to_type_and_host
        self.type_and_host_to_action_id = type_and_host_to_action_id

        # Setup state space
        states, lookup_table, hosts_lookup_tables = CyborgEnvUtil.get_decoy_state_space(config=config)
        self.decoy_hosts = CyborgEnvUtil.get_decoy_hosts(scenario=config.scenario)
        self.decoy_state_space = states
        self.decoy_state_space_lookup = lookup_table
        self.decoy_state_space_hosts_lookup = hosts_lookup_tables

        # Setup gym spaces
        if self.config.scanned_state:
            self.defender_observation_space = gym.spaces.Box(
                -1, 2, ((6 + len(self.decoy_action_types)) * len(self.cyborg_hostnames),), np.float32)
        else:
            self.defender_observation_space = self.cyborg_challenge_env.observation_space
        if self.config.reduced_action_space:
            self.defender_action_space = gym.spaces.Discrete(len(list(self.action_id_to_type_and_host.keys())))
        else:
            self.defender_action_space = self.cyborg_challenge_env.action_space

        self.action_space = self.defender_action_space
        self.observation_space = self.defender_observation_space

        # Setup traces
        self.traces: List[SimulationTrace] = []
        self.trace = SimulationTrace(simulation_env=self.config.gym_env_name)

        # Lookup dict of states and observations
        self.visited_cyborg_states: Dict[int, Any] = {}
        self.visited_scanned_states: Dict[int, List[int]] = {}
        self.visited_decoy_states: Dict[int, List[List[BlueAgentActionType]]] = {}
        self.observation_id_to_tensor: Dict[int, npt.NDArray[Any]] = {}

        # Randomized ids
        self.users_ids_randomized = env_constants.CYBORG.USER_HOST_IDS.copy()
        self.enterprise_ids_randomized = env_constants.CYBORG.ENTERPRISE_HOST_IDS.copy()
        random.shuffle(self.users_ids_randomized)
        random.shuffle(self.enterprise_ids_randomized)

        # Reset
        self.initial_belief = {1: 1.0}
        self.reset()
        super().__init__()

    def step(self, action: int) -> Tuple[npt.NDArray[Any], float, bool, bool, Dict[str, Any]]:
        """
        Takes a step in the environment by executing the given action

        :param action_profile: the actions to take (both players actions
        :return: (obs, reward, terminated, truncated, info)
        """
        # Convert between different action spaces
        action, decoy_state = CyborgScenarioTwoDefender.encode_action(
            action=action, config=self.config, action_id_to_type_and_host=self.action_id_to_type_and_host,
            cyborg_action_type_and_host_to_id=self.cyborg_action_type_and_host_to_id,
            decoy_action_types=self.decoy_action_types, decoy_actions_per_host=self.decoy_actions_per_host,
            decoy_state=self.decoy_state, cyborg_hostname_to_id=self.cyborg_hostname_to_id,
            cyborg_action_id_to_type_and_host=self.cyborg_action_id_to_type_and_host)
        self.decoy_state = decoy_state

        o, r, done, _, info = self.cyborg_challenge_env.step(action=action)
        if not self.config.decoy_optimization:
            info, _, scan_state = \
                CyborgScenarioTwoDefender.populate_info(
                    info=dict(info), obs=o, trace=self.trace, env=self.cyborg_challenge_env,
                    cyborg_hostnames=self.cyborg_hostnames, scan_state=self.scan_state, decoy_state=self.decoy_state,
                    config=self.config, cyborg_hostname_to_id=self.cyborg_hostname_to_id,
                    visited_cyborg_states=self.visited_cyborg_states,
                    visited_scanned_states=self.visited_scanned_states, visited_decoy_states=self.visited_decoy_states,
                    reset=False)
            self.scan_state = scan_state
            o, observation_id_to_tensor = CyborgScenarioTwoDefender.encode_observation(
                config=self.config, info=info, decoy_state=self.decoy_state, scan_state=self.scan_state,
                decoy_state_space_lookup=self.decoy_state_space_lookup,
                decoy_state_space_hosts_lookup=self.decoy_state_space_hosts_lookup,
                observation_id_to_tensor=self.observation_id_to_tensor,
                o=o, users_ids_randomized=self.users_ids_randomized,
                enterprise_ids_randomized=self.enterprise_ids_randomized)
            self.observation_id_to_tensor = observation_id_to_tensor

        self.t += 1
        if self.t >= self.config.maximum_steps:
            done = True

        # Log trace
        if self.config.save_trace:
            self.trace = CyborgScenarioTwoDefender.log_trace(r=float(r),
                                                             trace=self.trace, o=o, done=done, action=action)

        return np.array(o), float(r), bool(done), bool(done), info

    def reset(self, seed: Union[None, int] = None, soft: bool = False, options: Union[Dict[str, Any], None] = None,
              new_red_agent: Union[RedAgentType, None] = None) -> Tuple[npt.NDArray[Any], Dict[str, Any]]:
        """
        Resets the environment state, this should be called whenever step() returns <done>

        :param seed: the random seed
        :param soft: boolean flag indicating whether it is a soft reset or not
        :param options: optional configuration parameters
        :param new_red_agent: optional red agent specification
        :return: initial observation and info
        """
        super().reset(seed=seed)
        updated_env = CyborgEnvUtil.update_red_agent(config=self.config, current_red_agent=self.red_agent_type,
                                                     new_red_agent=new_red_agent)
        if updated_env is not None:
            self.cyborg_challenge_env = updated_env
        o, info = self.cyborg_challenge_env.reset()
        scan_state, decoy_state = CyborgScenarioTwoDefender.reset_scan_and_decoy_states(
            cyborg_hostnames=self.cyborg_hostnames)
        self.scan_state = scan_state
        self.decoy_state = decoy_state
        info, initial_belief, scan_state = CyborgScenarioTwoDefender.populate_info(
            info=dict(info), obs=o, trace=self.trace, env=self.cyborg_challenge_env,
            cyborg_hostnames=self.cyborg_hostnames, scan_state=self.scan_state,
            decoy_state=self.decoy_state, config=self.config, cyborg_hostname_to_id=self.cyborg_hostname_to_id,
            visited_cyborg_states=self.visited_cyborg_states, visited_scanned_states=self.visited_scanned_states,
            visited_decoy_states=self.visited_decoy_states, reset=True)
        self.initial_belief = initial_belief
        self.scan_state = scan_state

        o, observation_id_to_tensor = CyborgScenarioTwoDefender.encode_observation(
            config=self.config, info=info, decoy_state=self.decoy_state, scan_state=self.scan_state,
            decoy_state_space_lookup=self.decoy_state_space_lookup,
            decoy_state_space_hosts_lookup=self.decoy_state_space_hosts_lookup,
            observation_id_to_tensor=self.observation_id_to_tensor, o=o,
            users_ids_randomized=self.users_ids_randomized, enterprise_ids_randomized=self.enterprise_ids_randomized)
        self.observation_id_to_tensor = observation_id_to_tensor

        self.t = 1
        if len(self.traces) > 100:
            self.reset_traces()
        if len(self.trace.defender_rewards) > 0:
            self.traces.append(self.trace)
        self.trace = SimulationTrace(simulation_env=self.config.gym_env_name)
        return np.array(o), info

    @staticmethod
    def populate_info(info: Dict[str, Any], obs: npt.NDArray[Any], trace: SimulationTrace, env: ChallengeWrapper,
                      cyborg_hostnames: List[str], scan_state: List[int], decoy_state: List[List[BlueAgentActionType]],
                      config: CSLECyborgConfig, cyborg_hostname_to_id: Dict[str, int],
                      visited_cyborg_states: Dict[int, Any], visited_scanned_states: Dict[int, Any],
                      visited_decoy_states: Dict[int, Any], reset: bool = False) \
            -> Tuple[Dict[str, Any], Dict[int, float], List[int]]:
        """
        Populates the info dict

        :param info: the info dict to populate
        :param obs: the latest obs
        :param trace: the current simulation trace
        :param env: the cyborg environment
        :param cyborg_hostnames: a list of cyborg hostnames
        :param scan_state: the current scan state
        :param decoy_state: the current decoy state
        :param config: the environment configuration
        :param cyborg_hostname_to_id: a dict to convert from hostname to id
        :param visited_cyborg_states: a cache of visited cyborg states
        :param visited_scanned_states: a cache of visited scanned states
        :param visited_decoy_states: a cache of visited decoy states
        :param reset: boolean flag indicating whether this was called from reset or not
        :return: the populated dict, the updated initial belief, and the updated scan state
        """
        info[env_constants.ENV_METRICS.RETURN] = sum(trace.defender_rewards)
        info[env_constants.ENV_METRICS.TIME_HORIZON] = len(trace.defender_actions)
        info[env_constants.CYBORG.BLUE_TABLE] = env.env.env.env.info
        info[env_constants.CYBORG.VECTOR_OBS_PER_HOST] = []
        info[env_constants.CYBORG.OBS_PER_HOST] = []
        idx = 0
        for i in range(len(cyborg_hostnames)):
            host_vector_obs = obs[idx:idx + 4].tolist()
            idx += 4
            host_obs = {}
            host_obs[env_constants.CYBORG.COMPROMISED] = env.env.env.env.info[
                cyborg_hostnames[i]][env_constants.CYBORG.COMPROMISED_BLUE_TABLE_IDX]
            host_obs[env_constants.CYBORG.COMPROMISED] = CompromisedType.from_str(
                host_obs[env_constants.CYBORG.COMPROMISED])
            host_obs[env_constants.CYBORG.ACTIVITY] = env.env.env.env.info[
                cyborg_hostnames[i]][env_constants.CYBORG.ACTIVITY_BLUE_TABLE_IDX]
            host_obs[env_constants.CYBORG.ACTIVITY] = ActivityType.from_str(host_obs[env_constants.CYBORG.ACTIVITY])
            if host_obs[env_constants.CYBORG.ACTIVITY] == ActivityType.SCAN:
                scan_state = [1 if x == 2 else x for x in scan_state]
                scan_state[i] = 2
            host_obs[env_constants.CYBORG.SCANNED_STATE] = scan_state[i]
            info[env_constants.CYBORG.OBS_PER_HOST].append(host_obs)
            for enc_value in CyborgEnvUtil.host_scan_state_one_hot_encoding(host_scan_state=scan_state[i]):
                host_vector_obs.append(enc_value)
            for enc_value in CyborgEnvUtil.host_decoy_state_one_hot_encoding(host_decoy_state=decoy_state[i],
                                                                             scenario=config.scenario):
                host_vector_obs.append(enc_value)
            info[env_constants.CYBORG.VECTOR_OBS_PER_HOST].append(host_vector_obs)
        state_id, state_vector = CyborgScenarioTwoDefender.state_id(
            cyborg_hostname_to_id=cyborg_hostname_to_id, decoy_state=decoy_state, scan_state=scan_state, env=env)
        obs_id = CyborgScenarioTwoDefender.observation_id(cyborg_hostname_to_id=cyborg_hostname_to_id,
                                                          decoy_state=decoy_state, scan_state=scan_state, env=env)
        initial_belief = {}
        if reset:
            initial_belief = {state_id: 1.0}
        info[env_constants.ENV_METRICS.STATE] = state_id
        info[env_constants.ENV_METRICS.STATE_VECTOR] = state_vector
        info[env_constants.ENV_METRICS.OBSERVATION] = obs_id
        if config.cache_visited_states and state_id not in visited_cyborg_states:
            agent_interfaces_copy = {}
            for k, v in env.env.env.env.env.env.environment_controller.agent_interfaces.items():
                agent_interfaces_copy[k] = v.copy()
            visited_cyborg_states[state_id] = \
                (deepcopy(env.env.env.env.env.env.environment_controller.state),
                 deepcopy(env.env.env.env.env.scanned_ips),
                 agent_interfaces_copy,
                 deepcopy(env.env.env.env.env.env.environment_controller.done),
                 deepcopy(env.env.env.env.env.env.environment_controller.reward),
                 deepcopy(env.env.env.env.env.env.environment_controller.actions),
                 deepcopy(env.env.env.env.env.env.environment_controller.steps),
                 deepcopy(env.env.env.env.env.env.environment_controller.hostname_ip_map),
                 deepcopy(env.env.env.env.env.env.environment_controller.subnet_cidr_map),
                 deepcopy(env.env.env.env.env.env.environment_controller.observation),
                 deepcopy(env.env.env.env.env.step_counter),
                 deepcopy(env.env.env.env.success),
                 deepcopy(env.env.env.env.baseline),
                 deepcopy(env.env.env.env.info),
                 deepcopy(env.env.env.env.blue_info),
                 deepcopy(env.step_counter),
                 deepcopy(env.env.env.env.env.env.environment_controller.INFO_DICT),
                 )
            visited_scanned_states[state_id] = deepcopy(scan_state)
            visited_decoy_states[state_id] = deepcopy(decoy_state)
        return info, initial_belief, scan_state

    def get_table(self) -> PrettyTable:
        """
        Gets the table observation

        :return: a table with the defender's observations
        """
        return CyborgScenarioTwoDefender.table(env=self.cyborg_challenge_env)

    def get_access_list(self) -> List[int]:
        """
        Gets the true access list

        :return: a list with the access states
        """
        return CyborgScenarioTwoDefender.access_list(env=self.cyborg_challenge_env)

    def get_bline_state(self) -> int:
        """
        Gets the state of the bline agent

        :param env: the cyborg environment
        :return: the bline state
        """
        return CyborgScenarioTwoDefender.bline_state(env=self.cyborg_challenge_env)

    @staticmethod
    def table(env: ChallengeWrapper) -> PrettyTable:
        """
        Gets the table observation

        :param env: the cyborg environment
        :return: a table with the defender's observations
        """
        defender_table: PrettyTable = env.env.env.env.get_table()
        return defender_table

    def get_true_table(self) -> PrettyTable:
        """
        Gets the true table state

        :return: a table with the true state of the game
        """
        return CyborgScenarioTwoDefender.true_table(env=self.cyborg_challenge_env)

    def get_subnetworks(self) -> List[str]:
        """
        Gets the subnetworks

        :return: a list of subnetworks
        """
        true_table_state = CyborgScenarioTwoDefender.true_table(env=self.cyborg_challenge_env)
        subnetworks = ["", "", ""]
        for row in true_table_state.rows:
            subnet = str(row[0])
            if "Enterprise" in str(row[2]):
                subnetworks[1] = subnet
            elif "User" in str(row[2]):
                subnetworks[0] = subnet
            elif "Op_Server0" in str(row[2]):
                subnetworks[2] = subnet
        return list(subnetworks)

    def get_ip_to_host_mapping(self) -> Dict[str, str]:
        """
        Gets a mapping from ip to host

        :return: a dictinary to map ip to host
        """
        true_table_state = CyborgScenarioTwoDefender.true_table(env=self.cyborg_challenge_env)
        ip_to_host_mapping = {}
        for row in true_table_state.rows:
            ip_to_host_mapping[row[1]] = str(row[2])
        return ip_to_host_mapping

    @staticmethod
    def true_table(env: ChallengeWrapper) -> PrettyTable:
        """
        Gets the true table state

        :return: a table with the true state of the game
        """
        true_table: PrettyTable = env.env.env.env.env.get_table()
        return true_table

    @staticmethod
    def access_list(env: ChallengeWrapper) -> List[int]:
        """
        Gets the true access list

        :return: a list with the access states
        """
        return list(env.env.env.env.env._create_numeric_access_table())

    @staticmethod
    def bline_state(env: ChallengeWrapper) -> int:
        """
        Gets the state of the bline agent

        :param env: the cyborg environment
        :return: the bline state
        """
        return int(env.env.env.env.env.env.environment_controller.get_bline_state())

    def get_ip_map(self) -> Dict[str, Any]:
        """
        Gets the map of hostnames to ips

        :return: a dict with hostnames to ips mappings
        """
        ip_map: Dict[str, Any] = self.cyborg_challenge_env.get_ip_map()
        return ip_map

    def get_rewards(self) -> Dict[str, Any]:
        """
        Gets the rewards

        :return: a dict with agent names to rewards mappings
        """
        rewards_map: Dict[str, Any] = self.cyborg_challenge_env.get_rewards()
        return rewards_map

    def get_observation(self, agent: str) -> Dict[str, Any]:
        """
        Gets the observation of an agent

        :param agent: the name of the agent to get the observation of (e.g., 'Red')
        :return: the observation of the agent
        """
        observation_map: Dict[str, Any] = self.cyborg_challenge_env.get_observation(agent=agent)
        return observation_map

    def get_last_action(self, agent: str) -> Any:
        """
        Gets the last action of an agent

        :param agent: the name of the agent to get the last action of of (e.g., 'Red')
        :return: the action of the agent
        """
        return self.cyborg_challenge_env.get_last_action(agent=agent)

    def get_attacker_action_type(self) -> RedAgentActionType:
        """
        Gets the action type of the last attacker action

        :return: the type id of the last attacker action
        """
        attacker_action = self.cyborg_challenge_env.get_last_action(agent="Red")
        return RedAgentActionType.from_str(str(attacker_action))

    def get_attacker_action_target(self) -> int:
        """
        Gets the target of the last attacker action

        :return: the target of the last attacker action
        """
        attacker_action = self.cyborg_challenge_env.get_last_action(agent="Red")
        ip_to_host_map = self.get_ip_to_host_mapping()
        subnets = self.get_subnetworks()
        action_type = self.get_attacker_action_type()
        if action_type == RedAgentActionType.EXPLOIT_REMOTE_SERVICE:
            return self.cyborg_hostnames.index(ip_to_host_map[str(attacker_action.ip_address)])
        elif action_type == RedAgentActionType.PRIVILEGE_ESCALATE:
            return self.cyborg_hostnames.index(attacker_action.hostname)
        elif action_type == RedAgentActionType.IMPACT:
            return self.cyborg_hostnames.index(attacker_action.hostname)
        elif action_type == RedAgentActionType.DISCOVER_NETWORK_SERVICES:
            return self.cyborg_hostnames.index(ip_to_host_map[str(attacker_action.ip_address)])
        elif action_type == RedAgentActionType.DISCOVER_REMOTE_SYSTEMS:
            return subnets.index(str(attacker_action.subnet))
        else:
            raise ValueError(f"Red action type: {action_type} not recognized")

    def get_true_state(self) -> Any:
        """
        Gets the true state of the environment

        :return: the true state of the environment
        """
        return self.cyborg_challenge_env.get_agent_state(agent="True")

    def get_actions_table(self) -> PrettyTable:
        """
        Gets a table with the actions

        :return: a table with the actions
        """
        table = PrettyTable(["t", env_constants.CYBORG.BLUE, env_constants.CYBORG.Green, env_constants.CYBORG.RED])
        actions = self.cyborg_challenge_env.env.env.env.env.env.environment_controller.actions
        for i in range(len(actions[env_constants.CYBORG.RED])):
            row = [str(i), str(actions[env_constants.CYBORG.BLUE][i]), str(actions[env_constants.CYBORG.Green][i]),
                   str(actions[env_constants.CYBORG.RED][i])]
            table.add_row(row)
        return table

    def get_host_decoy_state(self, host_id: int) -> int:
        """
        Gets the decoy state of a specific host

        :param host_id: the host to get the decoy state of
        :return: the decoy state
        """
        return len(self.decoy_state[host_id])

    def get_decoy_state(self) -> int:
        """
        Gets the current decoy state

        :return: the decoy state
        """
        return CyborgScenarioTwoDefender.decoy_state_id(
            config=self.config, decoy_state=self.decoy_state, scan_state=self.scan_state,
            decoy_state_space_lookup=self.decoy_state_space_lookup,
            decoy_state_space_hosts_lookup=self.decoy_state_space_hosts_lookup)

    @staticmethod
    def decoy_state_id(config: CSLECyborgConfig, decoy_state: List[List[BlueAgentActionType]], scan_state: List[int],
                       decoy_state_space_hosts_lookup: Dict[int, Any], decoy_state_space_lookup: Dict[Any, Any]) -> int:
        """
        Gets the current decoy state id

        :param config: the environment configuration
        :param decoy_state: the current decoy state
        :param scan_state: the current scan state
        :param decoy_state_space_hosts_lookup: a lookup dict from decoy state to host
        :param decoy_state_space_lookup: a lookup dict from decoy state to state id
        :return: the decoy state id
        """
        d_state = []
        for host_id in CyborgEnvUtil.get_hosts(scenario=config.scenario):
            dec_state = len(decoy_state[host_id])
            scanned = min(scan_state[host_id], 1)
            d_state.append(decoy_state_space_hosts_lookup[host_id][(scanned, dec_state)])
        return int(decoy_state_space_lookup[tuple(d_state)])

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

    def set_state(self, state: Any) -> None:
        """
        Sets the state. Allows to simulate samples from specific states

        :param state: the state
        :return: None
        """
        s = int(state)
        decoy_state, scan_state = CyborgScenarioTwoDefender.update_cyborg_state(
            s=s, env=self.cyborg_challenge_env, visited_cyborg_states=self.visited_cyborg_states,
            visited_decoy_states=self.visited_decoy_states, visited_scanned_states=self.visited_scanned_states)
        self.decoy_state = decoy_state
        self.scan_state = scan_state

    @staticmethod
    def update_cyborg_state(env: ChallengeWrapper, s: int, visited_cyborg_states: Dict[int, Any],
                            visited_decoy_states: Dict[int, List[List[BlueAgentActionType]]],
                            visited_scanned_states: Dict[int, List[int]]) \
            -> Tuple[List[List[BlueAgentActionType]], List[int]]:
        """
        Updates the cyborg state to a specific state

        :param env: the cyborg environment
        :param s: the state to update cyborg to
        :param visited_cyborg_states: a cache with previously visited cyborg states
        :param visited_decoy_states: a cache with previously visited decoy states
        :param visited_scanned_states: a cache with previously visited scanned states
        :return: the updated decoy state and updated scanned state
        """
        if s in visited_cyborg_states:
            env.env.env.env.env.env.environment_controller.state = deepcopy(visited_cyborg_states[s][0])
            env.env.env.env.env.scanned_ips = deepcopy(visited_cyborg_states[s][1])
            env.env.env.env.env.env.environment_controller.agent_interfaces = deepcopy(visited_cyborg_states[s][2])
            for k, v in env.env.env.env.env.env.environment_controller.agent_interfaces.items():
                v.action_space.create_action_params()
            env.env.env.env.env.env.environment_controller.done = (deepcopy(visited_cyborg_states[s][3]))
            env.env.env.env.env.env.environment_controller.reward = deepcopy(visited_cyborg_states[s][4])
            env.env.env.env.env.env.environment_controller.actions = deepcopy(visited_cyborg_states[s][5])
            env.env.env.env.env.env.environment_controller.steps = deepcopy(visited_cyborg_states[s][6])
            env.env.env.env.env.env.environment_controller.hostname_ip_map = deepcopy(visited_cyborg_states[s][7])
            env.env.env.env.env.env.environment_controller.subnet_cidr_map = deepcopy(visited_cyborg_states[s][8])
            obs = deepcopy(visited_cyborg_states[s][9])
            obs["Blue"].data["success"] = visited_cyborg_states[s][11]
            env.env.env.env.env.env.environment_controller.observation = obs
            env.env.env.env.env.step_counter = deepcopy(visited_cyborg_states[s][10])
            env.env.env.env.baseline = deepcopy(visited_cyborg_states[s][12])
            env.env.env.env.info = deepcopy(visited_cyborg_states[s][13])
            env.env.env.env.blue_info = deepcopy(visited_cyborg_states[s][14])
            env.step_counter = deepcopy(visited_cyborg_states[s][15])
            env.env.env.env.env.env.environment_controller.INFO_DICT = deepcopy(visited_cyborg_states[s][16])
            decoy_state = deepcopy(visited_decoy_states[s])
            scan_state = deepcopy(visited_scanned_states[s])
            env.env.env.env.env.observation_change(obs)
            env.env.env.env.observation_change(obs["Blue"])
            return decoy_state, scan_state
        else:
            raise ValueError(f"Unknown state: {s}, visited states: {list(visited_cyborg_states.keys())}")

    def get_observation_from_history(self, history: List[int]) -> List[Any]:
        """
        Utility function to get a defender observation from a history

        :param history: the history to get the observation form
        :return: the observation
        """
        obs_id = history[-1]
        obs = self.observation_id_to_tensor[obs_id]
        return list(obs)

    def get_action_space(self) -> List[int]:
        """
        Gets the action space of the defender

        :return: a list of action ids
        """
        if self.config.reduced_action_space:
            return list(self.action_id_to_type_and_host.keys())
        else:
            return list(self.cyborg_action_id_to_type_and_host.keys())

    def manual_play(self) -> None:
        """
        An interactive loop to test the environment manually

        :return: None
        """
        return None

    def get_observation_from_id(self, obs_id: int) -> List[List[int]]:
        """
        Converts an observation id to an observation vector

        :param obs_id: the id to convert
        :return: the observation vector
        """
        return CyborgEnvUtil.state_id_to_state_vector(state_id=obs_id, observation=True)

    def get_state_from_id(self, state_id: int) -> List[List[int]]:
        """
        Converts a state id to a state vector

        :param state_id: the id to convert
        :return: the observation vector
        """
        return CyborgEnvUtil.state_id_to_state_vector(state_id=state_id, observation=False)

    def get_observation_id_from_vector(self, observation_vector: List[Any]) -> int:
        """
        Converts an observation vector to an id

        :param observation_vector: the vector to convert
        :return: the observation id
        """
        return CyborgEnvUtil.state_vector_to_state_id(state_vector=observation_vector, observation=True)

    def get_observation_id(self) -> int:
        """
        :return: the current observation id
        """
        return CyborgScenarioTwoDefender.observation_id(
            cyborg_hostname_to_id=self.cyborg_hostname_to_id, decoy_state=self.decoy_state, scan_state=self.scan_state,
            env=self.cyborg_challenge_env)

    @staticmethod
    def observation_id(cyborg_hostname_to_id: Dict[str, int], decoy_state: List[List[BlueAgentActionType]],
                       scan_state: List[int], env: ChallengeWrapper) -> int:
        """
        Gets the current observation id

        :param cyborg_hostname_to_id: a dict to convert from hostname to id
        :param decoy_state: the current decoy state
        :param scan_state: the current scan state
        :param env: the environment
        :return: the current observation id
        """
        host_ids = list(cyborg_hostname_to_id.values())
        obs_vector = CyborgEnvUtil.state_to_vector(state=CyborgScenarioTwoDefender.table(env=env).rows,
                                                   decoy_state=decoy_state,
                                                   host_ids=host_ids, scan_state=scan_state, observation=True)
        obs_id = CyborgEnvUtil.state_vector_to_state_id(state_vector=obs_vector, observation=True)
        return obs_id

    def get_state_id(self) -> int:
        """
        :return: the current state id
        """
        return CyborgScenarioTwoDefender.state_id(
            cyborg_hostname_to_id=self.cyborg_hostname_to_id, decoy_state=self.decoy_state, scan_state=self.scan_state,
            env=self.cyborg_challenge_env)[0]

    @staticmethod
    def state_id(cyborg_hostname_to_id: Dict[str, int], decoy_state: List[List[BlueAgentActionType]],
                 scan_state: List[int], env: ChallengeWrapper) -> Tuple[int, List[List[int]]]:
        """
        Gets the current state id

        :param cyborg_hostname_to_id: a dict to convert from hostname to id
        :param decoy_state: the current decoy state
        :param scan_state: the current scan state
        :param env: the environment
        :return: the current state id and state vector
        """
        host_ids = list(cyborg_hostname_to_id.values())
        state_vector = CyborgEnvUtil.state_to_vector(state=CyborgScenarioTwoDefender.true_table(env=env).rows,
                                                     decoy_state=decoy_state,
                                                     host_ids=host_ids,
                                                     scan_state=scan_state)
        state_id = CyborgEnvUtil.state_vector_to_state_id(state_vector=state_vector)
        return state_id, state_vector

    def is_state_terminal(self, state: int) -> bool:
        """
        Checks whether a given state is terminal or not

        :param state: the state id
        :return: True if terminal, else False
        """
        return False

    def add_observation_vector(self, obs_vector: List[Any], obs_id: int) -> None:
        """
        Adds an observation vector to the history

        :param obs_vector: the observation vector to add
        :param obs_id: the id of the observation
        :return: None
        """
        if obs_id not in self.observation_id_to_tensor:
            self.observation_id_to_tensor[obs_id] = np.array(obs_vector)

    def get_red_action_success(self) -> bool:
        """
        Returns true if the last action by the red agent was successful, else false

        :return: true if the action was successful, else false.
        """
        return bool(self.cyborg_challenge_env.env.env.env.env.env.environment_controller.agent_interfaces["Red"].
                    agent.success)

    def get_red_base_jump(self) -> bool:
        """
        Returns true if the last action by the red agent was as base jump, else false

        :return: true if the action was a base jump, else false.
        """
        return bool(self.cyborg_challenge_env.env.env.env.env.env.environment_controller.agent_interfaces["Red"].
                    agent.base_jump)

    def get_red_action_state(self) -> int:
        """
        Returns the current action state of the red agent

        :return: the current action state of the red agent
        """
        return int(self.cyborg_challenge_env.env.env.env.env.env.environment_controller.agent_interfaces["Red"]
                   .agent.action)

    @staticmethod
    def encode_action(action: int, config: CSLECyborgConfig,
                      action_id_to_type_and_host: Dict[int, Tuple[BlueAgentActionType, str]],
                      cyborg_action_type_and_host_to_id: Dict[Tuple[BlueAgentActionType, str], int],
                      decoy_action_types: List[BlueAgentActionType], cyborg_hostname_to_id: Dict[str, int],
                      decoy_actions_per_host: List[List[BlueAgentActionType]],
                      decoy_state: List[List[BlueAgentActionType]],
                      cyborg_action_id_to_type_and_host: Dict[int, Tuple[BlueAgentActionType, str]]) \
            -> Tuple[int, List[List[BlueAgentActionType]]]:
        """
        Encodes an action into a cyborg action

        :param action: the action to encode
        :param config: the environment configuration
        :param action_id_to_type_and_host: a dict to convert from action id to type and host
        :param cyborg_action_type_and_host_to_id: a dict to convert from cyborg action id to type and host
        :param decoy_action_types: types of decoy actions
        :param cyborg_hostname_to_id: a dict to convert from cyborg hostname to id
        :param decoy_actions_per_host: a list of decoy actions per host
        :param decoy_state: the decoy state of the environment
        :param cyborg_action_id_to_type_and_host: a dict to convert from cyborg action id to action type and host
        :return: the encoded action and the updated decoy state
        """
        if config.reduced_action_space or config.decoy_optimization:
            action_type, host = action_id_to_type_and_host[action]
            action = cyborg_action_type_and_host_to_id[(action_type, host)]
            if action_type in decoy_action_types:
                host_id = cyborg_hostname_to_id[host]
                decoy_found = False
                for decoy_action in decoy_actions_per_host[host_id]:
                    if decoy_action not in decoy_state[host_id]:
                        action_type = decoy_action
                        action = cyborg_action_type_and_host_to_id[(action_type, host)]
                        decoy_state[host_id].append(action_type)
                        decoy_found = True
                        break
                if not decoy_found:
                    action_type = BlueAgentActionType.REMOVE
                    action = cyborg_action_type_and_host_to_id[(action_type, host)]
        action_type, host = cyborg_action_id_to_type_and_host[action]
        # Restore action removes decoys
        if action_type == BlueAgentActionType.RESTORE:
            host_id = cyborg_hostname_to_id[host]
            decoy_state[host_id] = []
        return action, decoy_state

    @staticmethod
    def encode_observation(config: CSLECyborgConfig, info: Dict[str, Any],
                           decoy_state: List[List[BlueAgentActionType]], scan_state: List[int],
                           decoy_state_space_hosts_lookup: Dict[int, Any],
                           decoy_state_space_lookup: Dict[Any, Any],
                           observation_id_to_tensor: Dict[int, npt.NDArray[Any]],
                           o: npt.NDArray[Any], users_ids_randomized: List[int], enterprise_ids_randomized: List[int]) \
            -> Tuple[npt.NDArray[Any], Dict[int, npt.NDArray[Any]]]:
        """
        Encodes the observation

        :param config: the environment configuraiton
        :param info: the current info dict with the observation details
        :param decoy_state: the current decoy state
        :param scan_state: the current scan state
        :param decoy_state_space_hosts_lookup: a lookup dict from decoy state id to host
        :param decoy_state_space_lookup: a lookup dict form decoy state to decoy state id
        :param observation_id_to_tensor: a lookup dict from observation id to tensor
        :param users_ids_randomized: shuffled user ids order
        :param enterprise_ids_randomized: shuffled enterprise ids order
        :param o: the observation to encode
        :return: the encoded observation and an updated observation_id_to_tensor dict
        """
        o = np.array(info[env_constants.CYBORG.VECTOR_OBS_PER_HOST])
        if config.randomize_topology:
            users_ids = env_constants.CYBORG.USER_HOST_IDS
            enterprise_ids = env_constants.CYBORG.ENTERPRISE_HOST_IDS
            import copy
            randomized_obs = copy.deepcopy(o.copy())
            for i in range(len(users_ids)):
                randomized_obs[users_ids[i]] = o[users_ids_randomized[i]]
            for i in range(len(enterprise_ids)):
                randomized_obs[enterprise_ids[i]] = o[enterprise_ids_randomized[i]]
            o = randomized_obs

        if config.scanned_state or config.decoy_state:
            o = o.flatten()

        if config.decoy_optimization:
            o = np.array([CyborgScenarioTwoDefender.decoy_state_id(
                config=config, decoy_state=decoy_state, scan_state=scan_state,
                decoy_state_space_lookup=decoy_state_space_lookup,
                decoy_state_space_hosts_lookup=decoy_state_space_hosts_lookup
            )])

        if config.cache_visited_states and info[env_constants.ENV_METRICS.OBSERVATION] not in observation_id_to_tensor:
            observation_id_to_tensor[info[env_constants.ENV_METRICS.OBSERVATION]] = np.array(o)

        return o, observation_id_to_tensor

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

    @staticmethod
    def reset_scan_and_decoy_states(cyborg_hostnames: List[str]) -> Tuple[List[int], List[List[BlueAgentActionType]]]:
        """
        Resets the scan and decoy states

        :param cyborg_hostnames: list of cyborg hostnames
        :return: the reset scan and decoy states
        """
        scan_state: List[int] = []
        decoy_state: List[List[BlueAgentActionType]] = []
        for i in range(len(cyborg_hostnames)):
            scan_state.append(env_constants.CYBORG.NOT_SCANNED)
            decoy_state.append([])
        return scan_state, decoy_state
