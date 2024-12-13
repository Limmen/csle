from typing import List, Tuple, Dict, Any
import numpy.typing as npt
from gym_csle_cyborg.dao.activity_type import ActivityType
from csle_agents.agents.pomcp.pomcp_acquisition_function_type import POMCPAcquisitionFunctionType
from gym_csle_cyborg.dao.csle_cyborg_wrapper_config import CSLECyborgWrapperConfig
from gym_csle_cyborg.envs.cyborg_scenario_two_wrapper import CyborgScenarioTwoWrapper
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.util.cyborg_env_util import CyborgEnvUtil
from csle_agents.agents.pomcp.pomcp import POMCP
from gym_csle_cyborg.dao.blue_agent_action_type import BlueAgentActionType
import gym_csle_cyborg.constants.constants as env_constants
from csle_common.util.experiment_util import ExperimentUtil


class CPOMCP:
    """
    Causal Partially Observable Monte-Carlo Planning (C-POMCP). A planning agent for Cage-2.
    Paper:  https://arxiv.org/abs/2407.11070. Author: Kim Hammar (ORLANDO Siemens/KTH).
    """

    def __init__(self, ckpt_dir=None):
        """
        Initializes the agent

        :param ckpt_dir:
        """
        ExperimentUtil.set_seed(1258192)
        self.gamma = 0.99
        self.c = 0.5
        self.c2 = 15000
        self.planning_time = 10
        self.max_particles = 500
        self.rollout_policy = lambda x, deterministic: 35
        self.value_function = lambda x: 0
        self.reinvigoration = False
        self.verbose = False
        self.default_node_value = 0
        self.prior_weight = 5
        self.prior_confidence = 0
        self.reinvigorated_particles_ratio = 0.0
        self.prune_action_space = False
        self.prune_size = 3
        self.acquisition_function_type = POMCPAcquisitionFunctionType.UCB
        self.use_rollout_policy = False
        self.rollout_depth = 4
        self.planning_depth = 50
        self.train_env_config = CSLECyborgWrapperConfig(
            gym_env_name="csle-cyborg-scenario-two-wrapper-v1", maximum_steps=100, save_trace=False, scenario=2,
            reward_shaping=True, red_agent_type=RedAgentType.B_LINE_AGENT)
        self.train_env = CyborgScenarioTwoWrapper(config=self.train_env_config)
        self.cyborg_config = CSLECyborgConfig(
            gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
            maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=True, scanned_state=True,
            decoy_state=True, decoy_optimization=False, cache_visited_states=True, save_trace=False,
            randomize_topology=False)
        (cyborg_scenario_config_path, cyborg_challenge_env, cyborg_hostnames, cyborg_hostname_to_id,
         cyborg_subnets, cyborg_subnet_to_id, cyborg_action_id_to_type_and_host, cyborg_action_type_and_host_to_id,
         red_agent_type) = CyborgEnvUtil.setup_cyborg_env(config=self.cyborg_config)
        self.cyborg_scenario_config_path = cyborg_scenario_config_path
        self.cyborg_challenge_env = cyborg_challenge_env
        self.cyborg_hostnames = cyborg_hostnames
        self.cyborg_hostname_to_id = cyborg_hostname_to_id
        self.cyborg_subnets = cyborg_subnets
        self.cyborg_subnet_to_id = cyborg_subnet_to_id
        self.cyborg_action_id_to_type_and_host = cyborg_action_id_to_type_and_host
        self.cyborg_action_type_and_host_to_id = cyborg_action_type_and_host_to_id
        self.red_agent_type = red_agent_type
        self.decoy_action_types = CyborgEnvUtil.get_decoy_action_types(scenario=self.cyborg_config.scenario)
        self.decoy_actions_per_host = CyborgEnvUtil.get_decoy_actions_per_host(scenario=self.cyborg_config.scenario)
        self.end_episode()

    def get_action(self, obs, action_space=None) -> int:
        """
        Gets the next action

        :param obs: the latest observation
        :param action_space: the action space
        :return: the next action (integer)
        """
        if self.t > 1:
            obs_id, scan_state = CPOMCP.update_scan_state(
                obs=obs, cyborg_hostnames=self.cyborg_hostnames,
                scan_state=self.scan_state, decoy_state=self.decoy_state)
            self.scan_state = scan_state
            self.pomcp.update_tree_with_new_samples(action_sequence=self.action_sequence, observation=obs_id,
                                                    t=self.t - 1)
        self.pomcp.solve(max_rollout_depth=self.rollout_depth, max_planning_depth=self.planning_depth, t=self.t)
        action = self.pomcp.get_action()
        self.action_sequence.append(action)
        cyborg_action, decoy_state = CPOMCP.encode_action(
            action=action, action_id_to_type_and_host=self.action_id_to_type_and_host,
            cyborg_action_type_and_host_to_id=self.cyborg_action_type_and_host_to_id,
            decoy_action_types=self.decoy_action_types, decoy_actions_per_host=self.decoy_actions_per_host,
            decoy_state=self.decoy_state, cyborg_hostname_to_id=self.cyborg_hostname_to_id,
            cyborg_action_id_to_type_and_host=self.cyborg_action_id_to_type_and_host)
        self.decoy_state = decoy_state
        self.t += 1
        return cyborg_action

    def end_episode(self) -> bool:
        """
        Cleans up the state for a new episode

        :return: True
        """
        self.action_sequence = []
        self.t = 1
        self.train_env.reset()
        self.pomcp = POMCP(
            A=self.train_env.get_action_space(), gamma=self.gamma, env=self.train_env, c=self.c,
            initial_particles=self.train_env.initial_particles, planning_time=self.planning_time,
            max_particles=self.max_particles, rollout_policy=self.rollout_policy, value_function=self.value_function,
            reinvigoration=self.reinvigoration, verbose=self.verbose, default_node_value=self.default_node_value,
            prior_weight=self.prior_weight, acquisition_function_type=self.acquisition_function_type, c2=self.c2,
            use_rollout_policy=self.use_rollout_policy, prior_confidence=self.prior_confidence,
            reinvigorated_particles_ratio=self.reinvigorated_particles_ratio,
            prune_action_space=self.prune_action_space, prune_size=self.prune_size)
        scan_state, decoy_state = CPOMCP.reset_scan_and_decoy_states(
            cyborg_hostnames=self.cyborg_hostnames)
        self.scan_state = scan_state
        self.decoy_state = decoy_state
        action_id_to_type_and_host, type_and_host_to_action_id = CyborgEnvUtil.get_action_dicts(
            scenario=self.cyborg_config.scenario, decoy_state=self.cyborg_config.decoy_state,
            reduced_action_space=self.cyborg_config.reduced_action_space,
            decoy_optimization=self.cyborg_config.decoy_optimization)
        self.action_id_to_type_and_host = action_id_to_type_and_host
        self.type_and_host_to_action_id = type_and_host_to_action_id
        states, lookup_table, hosts_lookup_tables = CyborgEnvUtil.get_decoy_state_space(config=self.cyborg_config)
        self.decoy_hosts = CyborgEnvUtil.get_decoy_hosts(scenario=self.cyborg_config.scenario)
        self.decoy_state_space = states
        self.decoy_state_space_lookup = lookup_table
        self.decoy_state_space_hosts_lookup = hosts_lookup_tables
        self.observation_id_to_tensor: Dict[int, npt.NDArray[Any]] = {}
        self.initial_belief = {1: 1.0}
        return True

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

    @staticmethod
    def encode_action(action: int, action_id_to_type_and_host: Dict[int, Tuple[BlueAgentActionType, str]],
                      cyborg_action_type_and_host_to_id: Dict[Tuple[BlueAgentActionType, str], int],
                      decoy_action_types: List[BlueAgentActionType], cyborg_hostname_to_id: Dict[str, int],
                      decoy_actions_per_host: List[List[BlueAgentActionType]],
                      decoy_state: List[List[BlueAgentActionType]],
                      cyborg_action_id_to_type_and_host: Dict[int, Tuple[BlueAgentActionType, str]]) \
            -> Tuple[int, List[List[BlueAgentActionType]]]:
        """
        Encodes an action into a cyborg action

        :param action: the action to encode
        :param action_id_to_type_and_host: a dict to convert from action id to type and host
        :param cyborg_action_type_and_host_to_id: a dict to convert from cyborg action id to type and host
        :param decoy_action_types: types of decoy actions
        :param cyborg_hostname_to_id: a dict to convert from cyborg hostname to id
        :param decoy_actions_per_host: a list of decoy actions per host
        :param decoy_state: the decoy state of the environment
        :param cyborg_action_id_to_type_and_host: a dict to convert from cyborg action id to action type and host
        :return: the encoded action and the updated decoy state
        """
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
    def update_scan_state(obs: npt.NDArray[Any], cyborg_hostnames: List[str], scan_state: List[int],
                          decoy_state: List[List[BlueAgentActionType]]) -> Tuple[int, List[int]]:
        """
        Updates the scan state

        :param obs: the latest cyborg observation
        :param cyborg_hostnames: the hostnames
        :param scan_state: the scane state
        :param decoy_state: the decoy state
        :return: The observation id and the updated scan state
        """
        obs_per_host = []
        idx = 0
        for i in range(len(cyborg_hostnames)):
            host_vector_obs = obs[idx:idx + 4].tolist()
            idx += 4
            host_obs = {}
            if host_vector_obs[2:] == [1, 1]:
                host_obs[env_constants.CYBORG.COMPROMISED] = 2
            elif host_vector_obs[2:] == [0, 1]:
                host_obs[env_constants.CYBORG.COMPROMISED] = 1
            elif host_vector_obs[2:] == [1, 0]:
                host_obs[env_constants.CYBORG.COMPROMISED] = 3
            else:
                host_obs[env_constants.CYBORG.COMPROMISED] = 0

            if host_vector_obs[0:2] == [1, 1]:
                host_obs[env_constants.CYBORG.ACTIVITY] = 2
            elif host_vector_obs[0:2] == [0, 1] or host_vector_obs[0:2] == [1, 0]:
                host_obs[env_constants.CYBORG.ACTIVITY] = 1
            else:
                host_obs[env_constants.CYBORG.ACTIVITY] = 0

            if host_obs[env_constants.CYBORG.ACTIVITY] == ActivityType.SCAN:
                scan_state = [1 if x == 2 else x for x in scan_state]
                scan_state[i] = 2
            host_obs[env_constants.CYBORG.SCANNED_STATE] = scan_state[i]
            host_obs[env_constants.CYBORG.DECOY_STATE] = len(decoy_state[i])
            obs_per_host.append(host_obs)
        obs_id = CPOMCP.observation_id(obs_per_host=obs_per_host)
        return obs_id, scan_state

    @staticmethod
    def observation_id(obs_per_host) -> int:
        """
        Gets the current observation id

        :param cyborg_hostname_to_id: a dict to convert from hostname to id
        :param decoy_state: the current decoy state
        :param scan_state: the current scan state
        :param env: the environment
        :return: the current observation id
        """
        host_obs_vecs = []
        for i in range(len(obs_per_host)):
            vec = [obs_per_host[i][env_constants.CYBORG.ACTIVITY], obs_per_host[i][env_constants.CYBORG.SCANNED_STATE],
                   obs_per_host[i][env_constants.CYBORG.COMPROMISED], obs_per_host[i][env_constants.CYBORG.DECOY_STATE]]
            host_obs_vecs.append(vec)
        obs_id = CyborgEnvUtil.state_vector_to_state_id(state_vector=host_obs_vecs, observation=True)
        return obs_id
