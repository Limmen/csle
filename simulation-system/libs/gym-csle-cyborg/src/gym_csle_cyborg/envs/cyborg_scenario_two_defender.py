from typing import Tuple, Dict, List, Any, Union
from copy import deepcopy
import time
import numpy as np
from prettytable import PrettyTable
import numpy.typing as npt
import gymnasium as gym
import csle_common.constants.constants as constants
from csle_common.dao.simulation_config.base_env import BaseEnv
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace
import gym_csle_cyborg.constants.constants as env_constants
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.blue_agent_action_type import BlueAgentActionType
from gym_csle_cyborg.dao.activity_type import ActivityType
from gym_csle_cyborg.dao.compromised_type import CompromisedType
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
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
        self.scan_state: List[int] = []
        self.decoy_state: List[List[BlueAgentActionType]] = []
        for i in range(len(self.cyborg_hostnames)):
            self.scan_state.append(env_constants.CYBORG.NOT_SCANNED)
            self.decoy_state.append([])
        self.t = 1

        # Setup reduced action space
        action_id_to_type_and_host, type_and_host_to_action_id = CyborgEnvUtil.get_action_dicts(config=self.config)
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
            self.defender_observation_space = gym.spaces.Box(-1, 2, (5 * len(self.cyborg_hostnames),), np.float32)
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

        # Lookup dict of states
        self.visited_cyborg_states: Dict[int, Any] = {}
        self.visited_scanned_states: Dict[int, List[int]] = {}
        self.visited_decoy_states: Dict[int, List[List[BlueAgentActionType]]] = {}

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
        if self.config.reduced_action_space or self.config.decoy_optimization:
            action_type, host = self.action_id_to_type_and_host[action]
            action = self.cyborg_action_type_and_host_to_id[(action_type, host)]
            if action_type in self.decoy_action_types:
                host_id = self.cyborg_hostname_to_id[host]
                decoy_found = False
                for decoy_action in self.decoy_actions_per_host[host_id]:
                    if decoy_action not in self.decoy_state[host_id]:
                        action_type = decoy_action
                        action = self.cyborg_action_type_and_host_to_id[(action_type, host)]
                        self.decoy_state[host_id].append(action_type)
                        decoy_found = True
                        break
                if not decoy_found:
                    action_type = BlueAgentActionType.REMOVE
                    action = self.cyborg_action_type_and_host_to_id[(action_type, host)]

        o, r, done, _, info = self.cyborg_challenge_env.step(action=action)
        info = self.populate_info(info=dict(info), obs=o)

        # Add scanned state to observation
        if self.config.scanned_state:
            o = np.array(info[env_constants.CYBORG.VECTOR_OBS_PER_HOST]).flatten()

        if self.config.decoy_optimization:
            o = np.array([self.get_decoy_state()])

        self.t += 1
        if self.t >= self.config.maximum_steps:
            done = True

        # Log trace
        self.trace.defender_rewards.append(float(r))
        self.trace.attacker_rewards.append(-float(r))
        self.trace.attacker_actions.append(0)
        self.trace.defender_actions.append(action)
        self.trace.infos.append({})
        self.trace.states.append(0.0)
        self.trace.beliefs.append(0.0)
        self.trace.infrastructure_metrics.append(o)
        if not done:
            self.trace.attacker_observations.append(o)
            self.trace.defender_observations.append(o)

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
        self.scan_state = []
        self.decoy_state = []
        for i in range(len(self.cyborg_hostnames)):
            self.scan_state.append(env_constants.CYBORG.NOT_SCANNED)
            self.decoy_state.append([])
        info = self.populate_info(info=dict(info), obs=o, reset=True)
        if self.config.scanned_state:
            o = np.array(info[env_constants.CYBORG.VECTOR_OBS_PER_HOST]).flatten()
        if self.config.decoy_optimization:
            o = np.array([self.get_decoy_state()])
        self.t = 1
        if len(self.traces) > 100:
            self.reset_traces()
        if len(self.trace.defender_rewards) > 0:
            self.traces.append(self.trace)
        self.trace = SimulationTrace(simulation_env=self.config.gym_env_name)
        return np.array(o), info

    def populate_info(self, info: Dict[str, Any], obs: npt.NDArray[Any], reset: bool = False) -> Dict[str, Any]:
        """
        Populates the info dict

        :param obs: the latest obs
        :param info: the dict to populate
        :param reset: boolean flag indicating whether this was called from reset or not
        :return: the populated dict
        """
        info[env_constants.ENV_METRICS.RETURN] = sum(self.trace.defender_rewards)
        info[env_constants.ENV_METRICS.TIME_HORIZON] = len(self.trace.defender_actions)
        info[env_constants.CYBORG.BLUE_TABLE] = self.cyborg_challenge_env.env.env.env.info
        info[env_constants.CYBORG.VECTOR_OBS_PER_HOST] = []
        info[env_constants.CYBORG.OBS_PER_HOST] = []
        idx = 0
        for i in range(len(self.cyborg_hostnames)):
            host_vector_obs = obs[idx:idx + 4].tolist()
            idx += 4
            host_obs = {}
            host_obs[env_constants.CYBORG.COMPROMISED] = self.cyborg_challenge_env.env.env.env.info[
                self.cyborg_hostnames[i]][env_constants.CYBORG.COMPROMISED_BLUE_TABLE_IDX]
            host_obs[env_constants.CYBORG.COMPROMISED] = CompromisedType.from_str(
                host_obs[env_constants.CYBORG.COMPROMISED])
            host_obs[env_constants.CYBORG.ACTIVITY] = self.cyborg_challenge_env.env.env.env.info[
                self.cyborg_hostnames[i]][env_constants.CYBORG.ACTIVITY_BLUE_TABLE_IDX]
            host_obs[env_constants.CYBORG.ACTIVITY] = ActivityType.from_str(host_obs[env_constants.CYBORG.ACTIVITY])
            if host_obs[env_constants.CYBORG.ACTIVITY] == ActivityType.SCAN:
                self.scan_state = [1 if x == 2 else x for x in self.scan_state]
                self.scan_state[i] = 2
            host_obs[env_constants.CYBORG.SCANNED_STATE] = self.scan_state[i]
            info[env_constants.CYBORG.OBS_PER_HOST].append(host_obs)
            host_vector_obs.append(self.scan_state[i])
            info[env_constants.CYBORG.VECTOR_OBS_PER_HOST].append(host_vector_obs)
        host_ids = list(self.cyborg_hostname_to_id.values())
        state_vector = CyborgEnvUtil.state_to_vector(state=self.get_true_table().rows,
                                                     decoy_state=self.decoy_state,
                                                     host_ids=host_ids,
                                                     scan_state=self.scan_state)
        state_id = CyborgEnvUtil.state_vector_to_state_id(state_vector=state_vector)
        if reset:
            self.initial_belief = {state_id: 1}
        obs_vector = CyborgEnvUtil.state_to_vector(state=self.get_table().rows,
                                                   decoy_state=self.decoy_state,
                                                   host_ids=host_ids, scan_state=self.scan_state, observation=True)
        obs_id = CyborgEnvUtil.state_vector_to_state_id(state_vector=obs_vector, observation=True)
        info[env_constants.ENV_METRICS.STATE] = state_id
        info[env_constants.ENV_METRICS.OBSERVATION] = obs_id
        if state_id not in self.visited_cyborg_states:
            agent_interfaces_copy = {}
            for k, v in self.cyborg_challenge_env.env.env.env.env.env.environment_controller.agent_interfaces.items():
                agent_interfaces_copy[k] = v.copy()
            self.visited_cyborg_states[state_id] = \
                (deepcopy(self.cyborg_challenge_env.env.env.env.env.env.environment_controller.state),
                 deepcopy(self.cyborg_challenge_env.env.env.env.env.scanned_ips),
                 agent_interfaces_copy,
                 deepcopy(self.cyborg_challenge_env.env.env.env.env.env.environment_controller.done),
                 deepcopy(self.cyborg_challenge_env.env.env.env.env.env.environment_controller.reward),
                 deepcopy(self.cyborg_challenge_env.env.env.env.env.env.environment_controller.actions),
                 deepcopy(self.cyborg_challenge_env.env.env.env.env.env.environment_controller.step),
                 deepcopy(self.cyborg_challenge_env.env.env.env.env.env.environment_controller.hostname_ip_map),
                 deepcopy(self.cyborg_challenge_env.env.env.env.env.env.environment_controller.subnet_cidr_map),
                 deepcopy(self.cyborg_challenge_env.env.env.env.env.env.environment_controller.observation),
                 deepcopy(self.cyborg_challenge_env.env.env.env.env.step_counter),
                 deepcopy(self.cyborg_challenge_env.env.env.env.success),
                 deepcopy(self.cyborg_challenge_env.env.env.env.baseline),
                 deepcopy(self.cyborg_challenge_env.env.env.env.info),
                 deepcopy(self.cyborg_challenge_env.env.env.env.blue_info)
                 )
            self.visited_scanned_states[state_id] = deepcopy(self.scan_state)
            self.visited_decoy_states[state_id] = deepcopy(self.decoy_state)
        return info

    def get_table(self) -> PrettyTable:
        """
        Gets the table observation

        :return: a table with the defender's observations
        """
        defender_table: PrettyTable = self.cyborg_challenge_env.env.env.env.get_table()
        return defender_table

    def get_true_table(self) -> PrettyTable:
        """
        Gets the true table state

        :return: a table with the true state of the game
        """
        true_table: PrettyTable = self.cyborg_challenge_env.env.env.env.env.get_table()
        return true_table

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
                   str(actions[env_constants.CYBORG.RED][i]), ]
            table.add_row(row)
        return table

    def get_decoy_state(self) -> int:
        """
        Gets the current decoy state

        :return: the decoy state
        """
        d_state = []
        for host_id in CyborgEnvUtil.get_hosts(scenario=self.config.scenario):
            dec_state = len(self.decoy_state[host_id])
            scanned = min(self.scan_state[host_id], 1)
            d_state.append(self.decoy_state_space_hosts_lookup[host_id][(scanned, dec_state)])
        return self.decoy_state_space_lookup[tuple(d_state)]

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
        if s in self.visited_cyborg_states:
            self.cyborg_challenge_env.env.env.env.env.env.environment_controller.state = \
                deepcopy(self.visited_cyborg_states[s][0])
            self.cyborg_challenge_env.env.env.env.env.scanned_ips = deepcopy(self.visited_cyborg_states[s][1])
            self.cyborg_challenge_env.env.env.env.env.env.environment_controller.agent_interfaces \
                = deepcopy(self.visited_cyborg_states[s][2])
            for k, v in self.cyborg_challenge_env.env.env.env.env.env.environment_controller.agent_interfaces.items():
                v.action_space.create_action_params()
            self.cyborg_challenge_env.env.env.env.env.env.environment_controller.done = (
                deepcopy(self.visited_cyborg_states[s][3]))
            self.cyborg_challenge_env.env.env.env.env.env.environment_controller.reward = \
                deepcopy(self.visited_cyborg_states[s][4])
            self.cyborg_challenge_env.env.env.env.env.env.environment_controller.actions = \
                deepcopy(self.visited_cyborg_states[s][5])
            self.cyborg_challenge_env.env.env.env.env.env.environment_controller.step = \
                deepcopy(self.visited_cyborg_states[s][6])
            self.cyborg_challenge_env.env.env.env.env.env.environment_controller.hostname_ip_map = \
                deepcopy(self.visited_cyborg_states[s][7])
            self.cyborg_challenge_env.env.env.env.env.env.environment_controller.subnet_cidr_map = \
                deepcopy(self.visited_cyborg_states[s][8])
            obs = deepcopy(self.visited_cyborg_states[s][9])
            obs["Blue"].data["success"] = self.visited_cyborg_states[s][11]
            self.cyborg_challenge_env.env.env.env.env.env.environment_controller.observation = obs
            self.cyborg_challenge_env.env.env.env.env.step_counter = deepcopy(self.visited_cyborg_states[s][10])
            self.cyborg_challenge_env.env.env.env.baseline = deepcopy(self.visited_cyborg_states[s][12])
            self.cyborg_challenge_env.env.env.env.info = deepcopy(self.visited_cyborg_states[s][13])
            self.cyborg_challenge_env.env.env.env.blue_info = deepcopy(self.visited_cyborg_states[s][14])
            self.decoy_state = deepcopy(self.visited_decoy_states[s])
            self.scan_state = deepcopy(self.visited_scanned_states[s])
            self.cyborg_challenge_env.env.env.env.env.observation_change(obs)
            self.cyborg_challenge_env.env.env.env.observation_change(obs["Blue"])
        else:
            raise NotImplementedError(f"Unknown state: {s}")

    def get_observation_from_history(self, history: List[int]) -> List[Any]:
        """
        Utility function to get a defender observation from a history

        :param history: the history to get the observation form
        :return: the observation
        """
        obs_id = history[-1]
        obs = CyborgEnvUtil.state_id_to_state_vector(state_id=obs_id, observation=True)
        return obs

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
