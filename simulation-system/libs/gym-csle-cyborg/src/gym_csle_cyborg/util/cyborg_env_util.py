from typing import List, Tuple, Dict, Union, Any
import inspect
import itertools
from csle_cyborg.main import Main
from csle_cyborg.agents.wrappers.challenge_wrapper import ChallengeWrapper
import gym_csle_cyborg.constants.constants as env_constants
from gym_csle_cyborg.dao.blue_agent_action_type import BlueAgentActionType
from gym_csle_cyborg.dao.red_agent_action_type import RedAgentActionType
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.dao.activity_type import ActivityType
from gym_csle_cyborg.dao.compromised_type import CompromisedType
from gym_csle_cyborg.dao.exploit_type import ExploitType
from gym_csle_cyborg.dao.cyborg_wrapper_state import CyborgWrapperState


class CyborgEnvUtil:
    """
    Class with utility functions related to the cyborg environment
    """

    @staticmethod
    def create_cyborg_env(config: CSLECyborgConfig, red_agent_type: Union[RedAgentType, None] = None) \
            -> Tuple[ChallengeWrapper, RedAgentType, str]:
        """
        Creates a new cyborg environment

        :param config: the environment configuration
        :param red_agent_type: the type of red agent
        :return: the created environment, the red agent type, and the configuration path
        """
        cyborg_scenario_config_path = str(inspect.getfile(Main))
        cyborg_scenario_config_path = (f"{cyborg_scenario_config_path[:-7]}"
                                       f"{env_constants.CYBORG.SCENARIO_CONFIGS_DIR}"
                                       f"{env_constants.CYBORG.SCENARIO_CONFIG_PREFIX}{config.scenario}"
                                       f"{env_constants.CYBORG.SCENARIO_CONFIG_SUFFIX}")
        agents_dict, red_agent_type = config.get_agents_dict(agent=red_agent_type)
        cyborg = Main(env_constants.CYBORG.CYBORG_SCENARIO_2_DICT, env_constants.CYBORG.SIMULATION, agents=agents_dict)
        cyborg_challenge_env = ChallengeWrapper(env=cyborg, agent_name=env_constants.CYBORG.BLUE,
                                                max_steps=config.maximum_steps)
        return cyborg_challenge_env, red_agent_type, cyborg_scenario_config_path

    @staticmethod
    def update_red_agent(config: CSLECyborgConfig, current_red_agent: RedAgentType,
                         new_red_agent: Union[RedAgentType, None] = None) -> Union[ChallengeWrapper, None]:
        """
        Utiliy function for updating the red agent in the environment

        :param new_red_agent: the red agent to update to (if None the red agent will be sampled randomly)
        :param config: the csle configuration
        :return: the updated environment with the new agent or None if the environment was not updated
        """
        agents_dict, agent_type = config.get_agents_dict(agent=new_red_agent)
        if not agent_type.value == current_red_agent.value:
            cyborg_challenge_env, red_agent_type, cyborg_scenario_config_path = CyborgEnvUtil.create_cyborg_env(
                config=config, red_agent_type=new_red_agent)
            return cyborg_challenge_env
        return None

    @staticmethod
    def setup_cyborg_env(config: CSLECyborgConfig) \
            -> Tuple[str, ChallengeWrapper, List[str], Dict[str, int], List[str], Dict[str, int], Dict[
                int, Tuple[BlueAgentActionType, str]], Dict[Tuple[BlueAgentActionType, str], int], RedAgentType]:
        """
        Sets up the cyborg environment and associated metadata

        :param config: the environment configuration
        :return: The path to the Cyborg scenario config, the cyborg environment, the list of hostnames,
                 a dict hostname->host_id, a list of subnets, a dict subnet->subnet_id,
                 a dict action_id->(action_type,host), a dict (action_type, host) -> action_id
        """
        cyborg_challenge_env, red_agent_type, cyborg_scenario_config_path = \
            CyborgEnvUtil.create_cyborg_env(config=config, red_agent_type=None)
        cyborg_hostnames = list(cyborg_challenge_env.env.env.env.info.keys())
        cyborg_hostname_to_id = {}
        for i in range(len(cyborg_hostnames)):
            cyborg_hostname_to_id[cyborg_hostnames[i]] = i
        cyborg_subnets = list(set(list(
            map(lambda x: cyborg_challenge_env.env.env.env.info[x][env_constants.CYBORG.SUBNET_BLUE_TABLE_IDX],
                cyborg_hostnames))))
        cyborg_subnet_to_id = {}
        for i in range(len(cyborg_subnets)):
            cyborg_subnet_to_id[cyborg_subnets[i]] = i
        cyborg_action_id_to_type_and_host = {}
        cyborg_action_type_and_host_to_id = {}
        for i in range(len(cyborg_challenge_env.possible_actions)):
            action = cyborg_challenge_env.possible_actions[i]
            action_type_str = action.__class__.__name__.split('.')[-1]
            action_type = BlueAgentActionType.from_str(action_type_str)
            hostname = env_constants.CYBORG.ALL_HOSTNAME
            if env_constants.CYBORG.HOSTNAME in action.get_params():
                hostname = action.get_params()[env_constants.CYBORG.HOSTNAME]
            cyborg_action_id_to_type_and_host[i] = (action_type, hostname)
            cyborg_action_type_and_host_to_id[(action_type, hostname)] = i
        return (cyborg_scenario_config_path, cyborg_challenge_env, cyborg_hostnames, cyborg_hostname_to_id,
                cyborg_subnets, cyborg_subnet_to_id, cyborg_action_id_to_type_and_host,
                cyborg_action_type_and_host_to_id, red_agent_type)

    @staticmethod
    def get_decoy_action_types(scenario: int) -> List[BlueAgentActionType]:
        """
        Gets the list of decoy action types for a given cage scenario

        :param scenario: the cage scenario number
        :return: the list of blue agent decoy actions
        """
        if scenario == 2:
            return [
                BlueAgentActionType.DECOY_APACHE,
                BlueAgentActionType.DECOY_FEMITTER,
                BlueAgentActionType.DECOY_HARAKA_SMTP,
                BlueAgentActionType.DECOY_SMSS,
                BlueAgentActionType.DECOY_SSHD,
                BlueAgentActionType.DECOY_SVCHOST,
                BlueAgentActionType.DECOY_TOMCAT,
                BlueAgentActionType.DECOY_VSFTPD
            ]
        else:
            raise ValueError(f"Scenario: {scenario} not recognized")

    @staticmethod
    def get_decoy_actions_per_host(scenario: int) -> List[List[BlueAgentActionType]]:
        """
        Gets the list of decoy actions per host for a given cage scenario

        :param scenario: the cage scenario number
        :return: the list of lists of blue agent decoy actions per host
        """
        if scenario == 2:
            return [
                [BlueAgentActionType.DECOY_HARAKA_SMTP, BlueAgentActionType.DECOY_TOMCAT,
                 BlueAgentActionType.DECOY_APACHE, BlueAgentActionType.DECOY_VSFTPD],
                [BlueAgentActionType.DECOY_HARAKA_SMTP, BlueAgentActionType.DECOY_TOMCAT,
                 BlueAgentActionType.DECOY_VSFTPD, BlueAgentActionType.DECOY_APACHE],
                [BlueAgentActionType.DECOY_FEMITTER],
                [BlueAgentActionType.DECOY_FEMITTER],
                [], [], [],
                [BlueAgentActionType.DECOY_HARAKA_SMTP, BlueAgentActionType.DECOY_APACHE,
                 BlueAgentActionType.DECOY_TOMCAT, BlueAgentActionType.DECOY_VSFTPD],
                [],
                [BlueAgentActionType.DECOY_APACHE, BlueAgentActionType.DECOY_TOMCAT, BlueAgentActionType.DECOY_SMSS,
                 BlueAgentActionType.DECOY_SVCHOST],
                [BlueAgentActionType.DECOY_FEMITTER, BlueAgentActionType.DECOY_TOMCAT, BlueAgentActionType.DECOY_APACHE,
                 BlueAgentActionType.DECOY_SSHD],
                [BlueAgentActionType.DECOY_VSFTPD, BlueAgentActionType.DECOY_SSHD],
                [BlueAgentActionType.DECOY_VSFTPD]
            ]
        else:
            raise ValueError(f"Scenario: {scenario} not recognized")

    @staticmethod
    def get_action_dicts(scenario: int, reduced_action_space: bool, decoy_state: bool, decoy_optimization: bool) \
            -> Tuple[Dict[int, Tuple[BlueAgentActionType, str]], Dict[Tuple[BlueAgentActionType, str], int]]:
        """
        Gets action lookup dicts for a given scenario and the reduced action space

        :param scenario: the scenario
        :param reduced_action_space: boolean flag indicating whether the action sapce is reduced or not
        :param decoy_state: boolean flag indicating whether decoy state is included
        :param decoy_optimization: boolean flag indicating whether decoy optimization is used
        :return: a dict id -> (action_type, host) and a dict (action_type, host) -> id
        """
        if scenario == 2:
            action_id_to_type_and_host = {}
            type_and_host_to_action_id = {}
            if reduced_action_space and decoy_state and not decoy_optimization:
                action_id_to_type_and_host[0] = (BlueAgentActionType.RESTORE, env_constants.CYBORG.ENTERPRISE0)
                type_and_host_to_action_id[(BlueAgentActionType.RESTORE, env_constants.CYBORG.ENTERPRISE0)] = 0
                action_id_to_type_and_host[1] = (BlueAgentActionType.RESTORE, env_constants.CYBORG.ENTERPRISE1)
                type_and_host_to_action_id[(BlueAgentActionType.RESTORE, env_constants.CYBORG.ENTERPRISE1)] = 1
                action_id_to_type_and_host[2] = (BlueAgentActionType.RESTORE, env_constants.CYBORG.ENTERPRISE2)
                type_and_host_to_action_id[(BlueAgentActionType.RESTORE, env_constants.CYBORG.ENTERPRISE2)] = 2
                action_id_to_type_and_host[3] = (BlueAgentActionType.RESTORE, env_constants.CYBORG.OP_SERVER0)
                type_and_host_to_action_id[(BlueAgentActionType.RESTORE, env_constants.CYBORG.OP_SERVER0)] = 3
                action_id_to_type_and_host[4] = (BlueAgentActionType.ANALYZE, env_constants.CYBORG.ENTERPRISE0)
                type_and_host_to_action_id[(BlueAgentActionType.ANALYZE, env_constants.CYBORG.ENTERPRISE0)] = 4
                action_id_to_type_and_host[5] = (BlueAgentActionType.ANALYZE, env_constants.CYBORG.ENTERPRISE1)
                type_and_host_to_action_id[(BlueAgentActionType.ANALYZE, env_constants.CYBORG.ENTERPRISE1)] = 5
                action_id_to_type_and_host[6] = (BlueAgentActionType.ANALYZE, env_constants.CYBORG.ENTERPRISE2)
                type_and_host_to_action_id[(BlueAgentActionType.ANALYZE, env_constants.CYBORG.ENTERPRISE2)] = 6
                action_id_to_type_and_host[7] = (BlueAgentActionType.ANALYZE, env_constants.CYBORG.OP_SERVER0)
                type_and_host_to_action_id[(BlueAgentActionType.ANALYZE, env_constants.CYBORG.OP_SERVER0)] = 7
                action_id_to_type_and_host[8] = (BlueAgentActionType.REMOVE, env_constants.CYBORG.ENTERPRISE0)
                type_and_host_to_action_id[(BlueAgentActionType.REMOVE, env_constants.CYBORG.ENTERPRISE0)] = 8
                action_id_to_type_and_host[9] = (BlueAgentActionType.REMOVE, env_constants.CYBORG.ENTERPRISE1)
                type_and_host_to_action_id[(BlueAgentActionType.REMOVE, env_constants.CYBORG.ENTERPRISE1)] = 9
                action_id_to_type_and_host[10] = (BlueAgentActionType.REMOVE, env_constants.CYBORG.ENTERPRISE2)
                type_and_host_to_action_id[(BlueAgentActionType.REMOVE, env_constants.CYBORG.ENTERPRISE2)] = 10
                action_id_to_type_and_host[11] = (BlueAgentActionType.REMOVE, env_constants.CYBORG.OP_SERVER0)
                type_and_host_to_action_id[(BlueAgentActionType.REMOVE, env_constants.CYBORG.OP_SERVER0)] = 11
                action_id_to_type_and_host[12] = (BlueAgentActionType.ANALYZE, env_constants.CYBORG.USER1)
                type_and_host_to_action_id[(BlueAgentActionType.ANALYZE, env_constants.CYBORG.USER1)] = 12
                action_id_to_type_and_host[13] = (BlueAgentActionType.ANALYZE, env_constants.CYBORG.USER2)
                type_and_host_to_action_id[(BlueAgentActionType.ANALYZE, env_constants.CYBORG.USER2)] = 13
                action_id_to_type_and_host[14] = (BlueAgentActionType.ANALYZE, env_constants.CYBORG.USER3)
                type_and_host_to_action_id[(BlueAgentActionType.ANALYZE, env_constants.CYBORG.USER3)] = 14
                action_id_to_type_and_host[15] = (BlueAgentActionType.ANALYZE, env_constants.CYBORG.USER4)
                type_and_host_to_action_id[(BlueAgentActionType.ANALYZE, env_constants.CYBORG.USER4)] = 15
                action_id_to_type_and_host[16] = (BlueAgentActionType.RESTORE, env_constants.CYBORG.USER1)
                type_and_host_to_action_id[(BlueAgentActionType.RESTORE, env_constants.CYBORG.USER1)] = 16
                action_id_to_type_and_host[17] = (BlueAgentActionType.RESTORE, env_constants.CYBORG.USER2)
                type_and_host_to_action_id[(BlueAgentActionType.RESTORE, env_constants.CYBORG.USER2)] = 17
                action_id_to_type_and_host[18] = (BlueAgentActionType.RESTORE, env_constants.CYBORG.USER3)
                type_and_host_to_action_id[(BlueAgentActionType.RESTORE, env_constants.CYBORG.USER3)] = 18
                action_id_to_type_and_host[19] = (BlueAgentActionType.RESTORE, env_constants.CYBORG.USER4)
                type_and_host_to_action_id[(BlueAgentActionType.RESTORE, env_constants.CYBORG.USER4)] = 19
                action_id_to_type_and_host[20] = (BlueAgentActionType.RESTORE, env_constants.CYBORG.DEFENDER)
                type_and_host_to_action_id[(BlueAgentActionType.RESTORE, env_constants.CYBORG.DEFENDER)] = 20
                action_id_to_type_and_host[21] = (BlueAgentActionType.ANALYZE, env_constants.CYBORG.DEFENDER)
                type_and_host_to_action_id[(BlueAgentActionType.ANALYZE, env_constants.CYBORG.DEFENDER)] = 21
                action_id_to_type_and_host[22] = (BlueAgentActionType.REMOVE, env_constants.CYBORG.USER1)
                type_and_host_to_action_id[(BlueAgentActionType.REMOVE, env_constants.CYBORG.USER1)] = 22
                action_id_to_type_and_host[23] = (BlueAgentActionType.REMOVE, env_constants.CYBORG.USER2)
                type_and_host_to_action_id[(BlueAgentActionType.REMOVE, env_constants.CYBORG.USER2)] = 23
                action_id_to_type_and_host[24] = (BlueAgentActionType.REMOVE, env_constants.CYBORG.USER3)
                type_and_host_to_action_id[(BlueAgentActionType.REMOVE, env_constants.CYBORG.USER3)] = 24
                action_id_to_type_and_host[25] = (BlueAgentActionType.REMOVE, env_constants.CYBORG.USER4)
                type_and_host_to_action_id[(BlueAgentActionType.REMOVE, env_constants.CYBORG.USER4)] = 25
                action_id_to_type_and_host[26] = (BlueAgentActionType.REMOVE, env_constants.CYBORG.DEFENDER)
                type_and_host_to_action_id[(BlueAgentActionType.REMOVE, env_constants.CYBORG.DEFENDER)] = 26
                action_id_to_type_and_host[27] = (BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.ENTERPRISE0)
                type_and_host_to_action_id[(BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.ENTERPRISE0)] = 27
                action_id_to_type_and_host[28] = (BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.ENTERPRISE1)
                type_and_host_to_action_id[(BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.ENTERPRISE1)] = 28
                action_id_to_type_and_host[29] = (BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.ENTERPRISE2)
                type_and_host_to_action_id[(BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.ENTERPRISE2)] = 29
                action_id_to_type_and_host[30] = (BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.USER1)
                type_and_host_to_action_id[(BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.USER1)] = 30
                action_id_to_type_and_host[31] = (BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.USER2)
                type_and_host_to_action_id[(BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.USER2)] = 31
                action_id_to_type_and_host[32] = (BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.USER3)
                type_and_host_to_action_id[(BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.USER3)] = 32
                action_id_to_type_and_host[33] = (BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.USER4)
                type_and_host_to_action_id[(BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.USER4)] = 33
                action_id_to_type_and_host[34] = (BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.DEFENDER)
                type_and_host_to_action_id[(BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.DEFENDER)] = 34
                action_id_to_type_and_host[35] = (BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.OP_SERVER0)
                type_and_host_to_action_id[(BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.OP_SERVER0)] = 35
            elif decoy_optimization:
                action_id_to_type_and_host[0] = (BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.ENTERPRISE0)
                type_and_host_to_action_id[(BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.ENTERPRISE0)] = 0
                action_id_to_type_and_host[1] = (BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.ENTERPRISE1)
                type_and_host_to_action_id[(BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.ENTERPRISE1)] = 1
                action_id_to_type_and_host[2] = (BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.ENTERPRISE2)
                type_and_host_to_action_id[(BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.ENTERPRISE2)] = 2
                action_id_to_type_and_host[3] = (BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.OP_SERVER0)
                type_and_host_to_action_id[(BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.OP_SERVER0)] = 3
                action_id_to_type_and_host[4] = (BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.USER1)
                type_and_host_to_action_id[(BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.USER1)] = 4
                action_id_to_type_and_host[5] = (BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.USER2)
                type_and_host_to_action_id[(BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.USER2)] = 5
                action_id_to_type_and_host[6] = (BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.USER3)
                type_and_host_to_action_id[(BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.USER3)] = 6
                action_id_to_type_and_host[7] = (BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.USER4)
                type_and_host_to_action_id[(BlueAgentActionType.DECOY_FEMITTER, env_constants.CYBORG.USER4)] = 7
            return action_id_to_type_and_host, type_and_host_to_action_id
        else:
            raise ValueError(f"Scenario: {scenario} not recognized")

    @staticmethod
    def get_decoy_hosts(scenario: int) -> List[int]:
        """
        Gets the list of hosts to put decoys

        :param scenario: the cage scenario number
        :return: the list of decoy hosts
        """
        if scenario == 2:
            return [1, 2, 3, 7]
        else:
            raise ValueError(f"Scenario: {scenario} not recognized")

    @staticmethod
    def get_hosts(scenario: int) -> List[int]:
        """
        Gets the list of hosts

        :param scenario: the cage scenario number
        :return: the list of hosts
        """
        if scenario == 2:
            return [1, 2, 3, 7, 9, 10, 11, 12]
            # return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        else:
            raise ValueError(f"Scenario: {scenario} not recognized")

    @staticmethod
    def get_decoy_state_space(config: CSLECyborgConfig) -> Tuple[List[int], Dict[Any, int], Dict[int, Any]]:
        """
        Gets the numeric decoy state space

        :param config: the configuration of the scenario
        :return: the state space and a lookup table
        """
        if config.scenario == 2:
            decoy_actions = CyborgEnvUtil.get_decoy_actions_per_host(scenario=config.scenario)
            decoy_host_ids = CyborgEnvUtil.get_decoy_hosts(scenario=config.scenario)
            host_ids = CyborgEnvUtil.get_hosts(scenario=config.scenario)
            lookup_table = {}
            hosts_lookup_tables: Dict[int, Dict[Tuple[int, int], int]] = {}
            states = []
            host_states = []
            for host_id in host_ids:
                hosts_lookup_tables[host_id] = {}
                h_states = []
                h_state = 0
                for scanned in [0, 1]:
                    if host_id in decoy_host_ids:
                        decoy_a = decoy_actions[host_id]
                    else:
                        decoy_a = []
                    for host_state in range(len(decoy_a) + 1):
                        h_states.append(h_state)
                        hosts_lookup_tables[host_id][(scanned, host_state)] = h_state
                        h_state += 1
                host_states.append(h_states)
            state = 1
            all_states = list(itertools.product(*host_states))
            for s in all_states:
                states.append(state)
                lookup_table[s] = state
                state += 1
            return states, lookup_table, hosts_lookup_tables
        else:
            raise ValueError(f"Scenario: {config.scenario} not recognized")

    @staticmethod
    def state_to_vector(state: List[List[Any]], decoy_state: List[List[BlueAgentActionType]], host_ids: List[int],
                        scan_state: List[int], observation: bool = False) -> List[List[int]]:
        """
        Creates the state vector

        :param state: the state of the environment
        :param decoy_state: the decoy state
        :param scan_state: the scan state
        :param host_ids: the list of host ids
        :param observation: boolean flag indicating whether it is the true state or an observation of the state
        :return: the state vector
        """
        state_vector = []
        for host_id in host_ids:
            host_known = -1
            activity = -1
            if not observation:
                host_known = int(state[host_id][3])
                host_scanned = int(state[host_id][4])
                host_access = state[host_id][5]
            else:
                host_scanned = scan_state[host_id]
                activity = ActivityType.from_str(state[host_id][3]).value
                host_access = state[host_id][4]
            if host_access == env_constants.CYBORG.NO or host_access == env_constants.CYBORG.NONE:
                host_access = CompromisedType.NO.value
            if host_access == env_constants.CYBORG.USER:
                host_access = CompromisedType.USER.value
            if host_access == env_constants.CYBORG.PRIVILEGED:
                host_access = CompromisedType.PRIVILEGED.value
            if host_access == env_constants.CYBORG.UNKNOWN:
                host_access = CompromisedType.UNKNOWN.value
            host_decoy_state = len(decoy_state[host_id])
            if not observation:
                state_vector.append([host_known, host_scanned, host_access, host_decoy_state])
            else:
                state_vector.append([activity, host_scanned, host_access, host_decoy_state])
        return state_vector

    @staticmethod
    def state_vector_to_state_id(state_vector: List[List[int]], observation: bool = False) -> int:
        """
        Converts a state vector to an id

        :param state_vector: the state vector to convert
        :param observation: boolean flag indicating whether it is the true state or an observation of the state
        :return: the id
        """
        binary_id_str = ""
        host_bins = []
        for host_vec in state_vector:
            host_binary_id_str = ""
            for i, elem in enumerate(host_vec):
                if not observation:
                    if i == 0:
                        host_binary_id_str += format(elem, '01b')
                    if i == 1:
                        host_binary_id_str += format(elem, '01b')
                else:
                    if i == 0:
                        host_binary_id_str += format(elem, '02b')
                    if i == 1:
                        host_binary_id_str += format(elem, '02b')
                if i == 2:
                    host_binary_id_str += format(elem, '02b')
                if i == 3:
                    host_binary_id_str += format(elem, '03b')
            binary_id_str += host_binary_id_str
            host_bins.append(host_binary_id_str)
        state_id = int(binary_id_str, 2)
        return state_id

    @staticmethod
    def state_id_to_state_vector(state_id: int, observation: bool = False) -> List[List[int]]:
        """
        Converts a state id to a state vector

        :param state_id: the state id to convert
        :param observation: boolean flag indicating whether it is the true state or an observation of the state
        :return: the state vector
        """
        if not observation:
            binary_id_str = format(state_id, "091b")
            host_binary_ids_str = [binary_id_str[i:i + 7] for i in range(0, len(binary_id_str), 7)]
        else:
            binary_id_str = format(state_id, "0117b")
            host_binary_ids_str = [binary_id_str[i:i + 9] for i in range(0, len(binary_id_str), 9)]
        state_vector = []
        for host_bin in host_binary_ids_str:
            if not observation:
                known = int(host_bin[0:1], 2)
                scanned = int(host_bin[1:2], 2)
                access = int(host_bin[2:4], 2)
                decoy = int(host_bin[4:7], 2)
                host_vector = [known, scanned, access, decoy]
            else:
                activity = int(host_bin[0:2], 2)
                scanned = int(host_bin[2:4], 2)
                access = int(host_bin[4:6], 2)
                decoy = int(host_bin[6:9], 2)
                host_vector = [activity, scanned, access, decoy]
            state_vector.append(host_vector)
        return state_vector

    @staticmethod
    def host_scan_state_one_hot_encoding(host_scan_state: int) -> List[int]:
        """
        One-hot encoding of the host scan state

        :param host_scan_state: the host scan state to one-hot-encode
        :return: the encoded vector
        """
        if host_scan_state == 0:
            return [0, 0]
        elif host_scan_state == 1:
            return [0, 1]
        elif host_scan_state == 2:
            return [1, 1]
        else:
            raise ValueError(f"host scan state: {host_scan_state} not recognized")

    @staticmethod
    def host_decoy_state_one_hot_encoding(host_decoy_state: List[BlueAgentActionType], scenario: int) -> List[int]:
        """
        One-hot encoding of the host scan state

        :param host_decoy_state: the host scan state to one-hot-encode
        :param scenario: the scenario
        :return: the encoded vector
        """
        decoy_action_types = CyborgEnvUtil.get_decoy_action_types(scenario=scenario)
        encoded_state = [0] * len(decoy_action_types)
        for i, decoy_action_type in enumerate(decoy_action_types):
            if decoy_action_type in host_decoy_state:
                encoded_state[i] = 1
        return encoded_state

    @staticmethod
    def get_compromised_values() -> List[int]:
        """
        :return: the list of possible compromised values
        """
        return [CompromisedType.NO.value, CompromisedType.USER.value, CompromisedType.PRIVILEGED.value]

    @staticmethod
    def get_compromised_observation_values() -> List[int]:
        """
        :return: the list of possible compromised observation values
        """
        return [CompromisedType.NO.value, CompromisedType.USER.value, CompromisedType.PRIVILEGED.value,
                CompromisedType.UNKNOWN.value]

    @staticmethod
    def get_activity_values() -> List[int]:
        """
        :return: the list of possible activity values
        """
        return [ActivityType.NONE.value, ActivityType.SCAN.value, ActivityType.EXPLOIT.value]

    @staticmethod
    def get_cyborg_host_values() -> Dict[str, int]:
        """
        :return: a dict that maps hostnames to defender values
        """
        return {
            env_constants.CYBORG.DEFENDER: 3,
            env_constants.CYBORG.ENTERPRISE0: 3,
            env_constants.CYBORG.ENTERPRISE1: 3,
            env_constants.CYBORG.ENTERPRISE2: 4,
            env_constants.CYBORG.OP_HOST0: 5,
            env_constants.CYBORG.OP_HOST1: 5,
            env_constants.CYBORG.OP_HOST2: 5,
            env_constants.CYBORG.OP_SERVER0: 6,
            env_constants.CYBORG.USER0: 1,
            env_constants.CYBORG.USER1: 2,
            env_constants.CYBORG.USER2: 2,
            env_constants.CYBORG.USER3: 2,
            env_constants.CYBORG.USER4: 2
        }

    @staticmethod
    def get_red_agent_action_types() -> List[int]:
        """
        :return: a list of red agent action types
        """
        return [
            RedAgentActionType.DISCOVER_REMOTE_SYSTEMS, RedAgentActionType.DISCOVER_NETWORK_SERVICES,
            RedAgentActionType.EXPLOIT_REMOTE_SERVICE, RedAgentActionType.PRIVILEGE_ESCALATE, RedAgentActionType.IMPACT
        ]

    @staticmethod
    def get_host_compromised_costs() -> Dict[int, float]:
        """
        :return: a dict that maps host ids to compromised costs
        """
        return {0: 0, 1: -1, 2: -1, 3: -1, 4: -0.1, 5: -0.1, 6: -0.1, 7: -1, 8: 0, 9: -0.1, 10: -0.1, 11: -0.1,
                12: -0.1}

    @staticmethod
    def get_cyborg_hosts() -> List[str]:
        """
        :return: the list of cyborg hosts
        """
        return [
            env_constants.CYBORG.DEFENDER, env_constants.CYBORG.ENTERPRISE0, env_constants.CYBORG.ENTERPRISE1,
            env_constants.CYBORG.ENTERPRISE2, env_constants.CYBORG.OP_HOST0, env_constants.CYBORG.OP_HOST1,
            env_constants.CYBORG.OP_HOST2, env_constants.CYBORG.OP_SERVER0, env_constants.CYBORG.USER0,
            env_constants.CYBORG.USER1, env_constants.CYBORG.USER2, env_constants.CYBORG.USER3,
            env_constants.CYBORG.USER4
        ]

    @staticmethod
    def cyborg_host_to_subnet() -> Dict[int, int]:
        """
        :return: a dict that maps cyborg hosts to subnet identifiers
        """
        return {
            0: 1,
            1: 1,
            2: 1,
            3: 1,
            4: 2,
            5: 2,
            6: 2,
            7: 2,
            8: 0,
            9: 0,
            10: 0,
            11: 0,
            12: 0
        }

    @staticmethod
    def subnetworks() -> List[int]:
        """
        :return: a list of subnetworks
        """
        return [0, 1, 2]

    @staticmethod
    def cyborg_host_ports_map() -> Dict[int, List[Tuple[int, bool]]]:
        """
        :return: a map from host id to ports and whether they run as root or not
        """
        return {
            0: [(22, False)], 1: [(22, False)],
            2: [(22, False), (135, True), (3389, True), (445, True), (139, True), (80, False), (443, False)],
            3: [(22, False), (135, True), (3389, True), (445, True), (139, True), (80, False), (443, False)],
            4: [], 5: [], 6: [], 7: [(22, False)], 8: [], 9: [(22, False), (21, True)],
            10: [(445, True), (139, True), (135, True), (3389, False)],
            11: [(80, False), (3389, True), (443, False), (25, True)],
            12: [(22, False), (80, False), (3390, True), (443, False), (25, True)]
        }

    @staticmethod
    def cyborg_decoy_actions_to_port() -> Dict[int, List[int]]:
        """
        :return: a map from decoy type to port
        """
        return {
            BlueAgentActionType.DECOY_SSHD: [22],
            BlueAgentActionType.DECOY_APACHE: [80],
            BlueAgentActionType.DECOY_FEMITTER: [21],
            BlueAgentActionType.DECOY_HARAKA_SMTP: [25],
            BlueAgentActionType.DECOY_SMSS: [139],
            BlueAgentActionType.DECOY_SVCHOST: [3389],
            BlueAgentActionType.DECOY_TOMCAT: [443],
            BlueAgentActionType.DECOY_VSFTPD: [80]
        }

    @staticmethod
    def exploit_values() -> Dict[int, float]:
        """
        :return: a map from exploit type to value
        """
        return {
            ExploitType.ETERNAL_BLUE.value: 2.0,
            ExploitType.BLUE_KEEP.value: 1.0,
            ExploitType.HTTP_RFI.value: 3.0,
            ExploitType.HTTP_SRFI.value: 4.0,
            ExploitType.SSH_BRUTE_FORCE.value: 0.1,
            ExploitType.SQL_INJECTION.value: 5.0,
            ExploitType.HARAKA_RCE.value: 6.0,
            ExploitType.FTP_DIRECTORY_TRAVERSAL.value: 7.0
        }

    @staticmethod
    def exploit_ports() -> Dict[int, List[int]]:
        """
        :return: a map from exploit type to ports
        """
        return {
            ExploitType.ETERNAL_BLUE.value: [139],
            ExploitType.BLUE_KEEP.value: [3389],
            ExploitType.HTTP_RFI.value: [80],
            ExploitType.HTTP_SRFI.value: [443],
            ExploitType.SSH_BRUTE_FORCE.value: [22],
            ExploitType.SQL_INJECTION.value: [3390],
            ExploitType.HARAKA_RCE.value: [25],
            ExploitType.FTP_DIRECTORY_TRAVERSAL.value: [21]
        }

    @staticmethod
    def exploits() -> List[ExploitType]:
        """
        :return: list of exploits
        """
        return [
            ExploitType.ETERNAL_BLUE, ExploitType.BLUE_KEEP, ExploitType.HTTP_RFI, ExploitType.HTTP_SRFI,
            ExploitType.SSH_BRUTE_FORCE, ExploitType.SQL_INJECTION, ExploitType.HARAKA_RCE,
            ExploitType.FTP_DIRECTORY_TRAVERSAL
        ]

    @staticmethod
    def get_wrapper_state_from_cyborg(obs_vector: List[List[int]], t: int, scan_state: List[int],
                                      access_list: List[int], decoy_state: List[List[int]], cyborg_hosts: List[str],
                                      red_agent_state: int) -> CyborgWrapperState:
        """
        A best-effort construction of the wrapper state a cyborg observation

        :param obs_vector: the observation vector
        :param t: the time step
        :param scan_state: the scan state
        :param access_list: the access list
        :param decoy_state: the decoy state
        :param cyborg_hosts: the list of cyborg hosts
        :param red_agent_state: the red agent state
        :return: the wrapper state
        """
        op_server_restored = False
        privilege_escalation_detected = False
        bline_base_jump = False
        scanned_subnets = [0, 0, 0]
        for i in range(len(scan_state)):
            if i in [9, 10, 11, 12] and scan_state[i] > 0:
                scanned_subnets[0] = 1
            if i in [3, 4, 5, 6, 7] and scan_state[i] > 0:
                scanned_subnets[1] = 1
            if i in [4, 5, 6, 7] and scan_state[i] > 0:
                scanned_subnets[2] = 1
        red_action_targets = {}
        red_action_targets[0] = 0
        if scan_state[9] > 0:
            red_action_targets[1] = 9
            red_action_targets[2] = 9
            red_action_targets[3] = 9
            red_action_targets[4] = 2
            red_action_targets[5] = 2
            red_action_targets[6] = 2
        elif scan_state[10] > 0:
            red_action_targets[1] = 10
            red_action_targets[2] = 10
            red_action_targets[3] = 10
            red_action_targets[4] = 2
            red_action_targets[5] = 2
            red_action_targets[6] = 2
        elif scan_state[11] > 0:
            red_action_targets[1] = 11
            red_action_targets[2] = 11
            red_action_targets[3] = 11
            red_action_targets[4] = 1
            red_action_targets[5] = 1
            red_action_targets[6] = 1
        elif scan_state[12] > 0:
            red_action_targets[1] = 12
            red_action_targets[2] = 12
            red_action_targets[3] = 12
            red_action_targets[4] = 1
            red_action_targets[5] = 1
            red_action_targets[6] = 1
        red_action_targets[7] = 1
        red_action_targets[8] = 3
        red_action_targets[9] = 3
        red_action_targets[10] = 7
        red_action_targets[11] = 7
        red_action_targets[12] = 7
        s = []
        for i in range(len(cyborg_hosts)):
            known = 0
            scanned = min(scan_state[i], 1)
            if scanned:
                known = 1
            if t > 0 and i in [9, 10, 11, 12]:
                known = 1
            if red_agent_state >= 6 and i in [0, 1, 2, 3]:
                known = 1
            if red_agent_state >= 8 and i in [4, 5, 6, 7]:
                known = 1
            access = access_list[i]
            decoy = len(decoy_state[i])
            host_state = [known, scanned, access, decoy]
            s.append(host_state)
        malware_state = [0 for _ in range(len(scan_state))]
        ssh_access = [0 for _ in range(len(scan_state))]
        escalated = [0 for _ in range(len(scan_state))]
        exploited = [0 for _ in range(len(scan_state))]
        detected = [0 for _ in range(len(scan_state))]
        attacker_observed_decoy = [len(decoy_state[i]) for i in range(len(decoy_state))]
        red_agent_target = red_action_targets[red_agent_state]
        wrapper_state = CyborgWrapperState(s=s, scan_state=scan_state, op_server_restored=op_server_restored,
                                           obs=obs_vector,
                                           red_action_targets=red_action_targets,
                                           privilege_escalation_detected=privilege_escalation_detected,
                                           red_agent_state=red_agent_state, red_agent_target=red_agent_target,
                                           malware_state=malware_state,
                                           ssh_access=ssh_access, escalated=escalated, exploited=exploited,
                                           bline_base_jump=bline_base_jump, scanned_subnets=scanned_subnets,
                                           attacker_observed_decoy=attacker_observed_decoy, detected=detected)
        return wrapper_state
