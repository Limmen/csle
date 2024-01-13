from typing import List, Tuple, Dict, Union
import inspect
from csle_cyborg.main import Main
from csle_cyborg.agents.wrappers.challenge_wrapper import ChallengeWrapper
import gym_csle_cyborg.constants.constants as env_constants
from gym_csle_cyborg.dao.blue_agent_action_type import BlueAgentActionType
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType


class CyborgEnvUtil:
    """
    Class with utility functions related to the cyborg environment
    """

    @staticmethod
    def update_red_agent(config: CSLECyborgConfig, current_red_agent: RedAgentType,
                         new_red_agent: Union[RedAgentType, None] = None) -> Union[ChallengeWrapper, None]:
        """
        Utiliy function for updating the red agent in the environment

        :param new_red_agent: the red agent to update to (if None the red agent will be sampled randomly)
        :param config: the csle configuration
        :return: the updated environment with the new agent or None if the environment was not updated
        """
        cyborg_scenario_config_path = str(inspect.getfile(Main))
        cyborg_scenario_config_path = (f"{cyborg_scenario_config_path[:-7]}"
                                       f"{env_constants.CYBORG.SCENARIO_CONFIGS_DIR}"
                                       f"{env_constants.CYBORG.SCENARIO_CONFIG_PREFIX}{config.scenario}"
                                       f"{env_constants.CYBORG.SCENARIO_CONFIG_SUFFIX}")
        agents_dict, agent_type = config.get_agents_dict(agent=new_red_agent)
        cyborg_challenge_env = None
        if not agent_type.value == current_red_agent.value:
            cyborg = Main(cyborg_scenario_config_path, env_constants.CYBORG.SIMULATION,
                          agents=agents_dict)
            cyborg_challenge_env = ChallengeWrapper(env=cyborg, agent_name=env_constants.CYBORG.BLUE,
                                                    max_steps=config.maximum_steps)
        return cyborg_challenge_env

    @staticmethod
    def setup_cyborg_env(config: CSLECyborgConfig) -> Tuple[
        str, ChallengeWrapper, List[str], Dict[str, int], List[str], Dict[str, int],
        Dict[int, Tuple[BlueAgentActionType, str]], Dict[Tuple[BlueAgentActionType, str], int],
        RedAgentType
    ]:
        """
        Sets up the cyborg environment and associated metadata

        :param config: the environment configuration
        :return: The path to the Cyborg scenario config, the cyborg environment, the list of hostnames,
                 a dict hostname->host_id, a list of subnets, a dict subnet->subnet_id,
                 a dict action_id->(action_type,host), a dict (action_type, host) -> action_id
        """
        cyborg_scenario_config_path = str(inspect.getfile(Main))
        cyborg_scenario_config_path = (f"{cyborg_scenario_config_path[:-7]}"
                                       f"{env_constants.CYBORG.SCENARIO_CONFIGS_DIR}"
                                       f"{env_constants.CYBORG.SCENARIO_CONFIG_PREFIX}{config.scenario}"
                                       f"{env_constants.CYBORG.SCENARIO_CONFIG_SUFFIX}")
        agents_dict, red_agent_type = config.get_agents_dict(agent=None)
        cyborg = Main(cyborg_scenario_config_path, env_constants.CYBORG.SIMULATION,
                      agents=agents_dict)
        cyborg_challenge_env = ChallengeWrapper(env=cyborg, agent_name=env_constants.CYBORG.BLUE,
                                                max_steps=config.maximum_steps)
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
                BlueAgentActionType.DECOY_HARAKA_SMPT,
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
                [BlueAgentActionType.DECOY_HARAKA_SMPT, BlueAgentActionType.DECOY_TOMCAT,
                 BlueAgentActionType.DECOY_APACHE, BlueAgentActionType.DECOY_VSFTPD],
                [BlueAgentActionType.DECOY_HARAKA_SMPT, BlueAgentActionType.DECOY_TOMCAT,
                 BlueAgentActionType.DECOY_VSFTPD, BlueAgentActionType.DECOY_APACHE],
                [BlueAgentActionType.DECOY_FEMITTER],
                [BlueAgentActionType.DECOY_FEMITTER],
                [], [], [],
                [BlueAgentActionType.DECOY_HARAKA_SMPT, BlueAgentActionType.DECOY_APACHE,
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
    def get_action_dicts(scenario: int) -> Tuple[Dict[int, Tuple[BlueAgentActionType, str]],
                                                 Dict[Tuple[BlueAgentActionType, str], int]]:
        """
        Gets action lookup dicts for a given scenario and the reduced action space

        :param scenario: the cage scenario number
        :return: a dict id -> (action_type, host) and a dict (action_type, host) -> id
        """
        if scenario == 2:
            action_id_to_type_and_host = {}
            type_and_host_to_action_id = {}
            action_id_to_type_and_host[0] = (BlueAgentActionType.RESTORE, "Enterprise0")
            type_and_host_to_action_id[(BlueAgentActionType.RESTORE, "Enterprise0")] = 0
            action_id_to_type_and_host[1] = (BlueAgentActionType.RESTORE, "Enterprise1")
            type_and_host_to_action_id[(BlueAgentActionType.RESTORE, "Enterprise1")] = 1
            action_id_to_type_and_host[2] = (BlueAgentActionType.RESTORE, "Enterprise2")
            type_and_host_to_action_id[(BlueAgentActionType.RESTORE, "Enterprise2")] = 2
            action_id_to_type_and_host[3] = (BlueAgentActionType.RESTORE, "Op_Server0")
            type_and_host_to_action_id[(BlueAgentActionType.RESTORE, "Op_Server0")] = 3
            action_id_to_type_and_host[4] = (BlueAgentActionType.ANALYZE, "Enterprise0")
            type_and_host_to_action_id[(BlueAgentActionType.ANALYZE, "Enterprise0")] = 4
            action_id_to_type_and_host[5] = (BlueAgentActionType.ANALYZE, "Enterprise1")
            type_and_host_to_action_id[(BlueAgentActionType.ANALYZE, "Enterprise1")] = 5
            action_id_to_type_and_host[6] = (BlueAgentActionType.ANALYZE, "Enterprise2")
            type_and_host_to_action_id[(BlueAgentActionType.ANALYZE, "Enterprise2")] = 6
            action_id_to_type_and_host[7] = (BlueAgentActionType.ANALYZE, "Op_Server0")
            type_and_host_to_action_id[(BlueAgentActionType.ANALYZE, "Op_Server0")] = 7
            action_id_to_type_and_host[8] = (BlueAgentActionType.REMOVE, "Enterprise0")
            type_and_host_to_action_id[(BlueAgentActionType.REMOVE, "Enterprise0")] = 8
            action_id_to_type_and_host[9] = (BlueAgentActionType.REMOVE, "Enterprise1")
            type_and_host_to_action_id[(BlueAgentActionType.REMOVE, "Enterprise1")] = 9
            action_id_to_type_and_host[10] = (BlueAgentActionType.REMOVE, "Enterprise2")
            type_and_host_to_action_id[(BlueAgentActionType.REMOVE, "Enterprise2")] = 10
            action_id_to_type_and_host[11] = (BlueAgentActionType.REMOVE, "Op_Server0")
            type_and_host_to_action_id[(BlueAgentActionType.REMOVE, "Op_Server0")] = 11
            action_id_to_type_and_host[12] = (BlueAgentActionType.ANALYZE, "User1")
            type_and_host_to_action_id[(BlueAgentActionType.ANALYZE, "User1")] = 12
            action_id_to_type_and_host[13] = (BlueAgentActionType.ANALYZE, "User2")
            type_and_host_to_action_id[(BlueAgentActionType.ANALYZE, "User2")] = 13
            action_id_to_type_and_host[14] = (BlueAgentActionType.ANALYZE, "User3")
            type_and_host_to_action_id[(BlueAgentActionType.ANALYZE, "User3")] = 14
            action_id_to_type_and_host[15] = (BlueAgentActionType.ANALYZE, "User4")
            type_and_host_to_action_id[(BlueAgentActionType.ANALYZE, "User4")] = 15
            action_id_to_type_and_host[16] = (BlueAgentActionType.RESTORE, "User1")
            type_and_host_to_action_id[(BlueAgentActionType.RESTORE, "User1")] = 16
            action_id_to_type_and_host[17] = (BlueAgentActionType.RESTORE, "User2")
            type_and_host_to_action_id[(BlueAgentActionType.RESTORE, "User2")] = 17
            action_id_to_type_and_host[18] = (BlueAgentActionType.RESTORE, "User3")
            type_and_host_to_action_id[(BlueAgentActionType.RESTORE, "User3")] = 18
            action_id_to_type_and_host[19] = (BlueAgentActionType.RESTORE, "User4")
            type_and_host_to_action_id[(BlueAgentActionType.RESTORE, "User4")] = 19
            action_id_to_type_and_host[20] = (BlueAgentActionType.RESTORE, "Defender")
            type_and_host_to_action_id[(BlueAgentActionType.RESTORE, "Defender")] = 20
            action_id_to_type_and_host[21] = (BlueAgentActionType.ANALYZE, "Defender")
            type_and_host_to_action_id[(BlueAgentActionType.ANALYZE, "Defender")] = 21
            action_id_to_type_and_host[22] = (BlueAgentActionType.REMOVE, "User1")
            type_and_host_to_action_id[(BlueAgentActionType.REMOVE, "User1")] = 22
            action_id_to_type_and_host[23] = (BlueAgentActionType.REMOVE, "User2")
            type_and_host_to_action_id[(BlueAgentActionType.REMOVE, "User2")] = 23
            action_id_to_type_and_host[24] = (BlueAgentActionType.REMOVE, "User3")
            type_and_host_to_action_id[(BlueAgentActionType.REMOVE, "User3")] = 24
            action_id_to_type_and_host[25] = (BlueAgentActionType.REMOVE, "User4")
            type_and_host_to_action_id[(BlueAgentActionType.REMOVE, "User4")] = 25
            action_id_to_type_and_host[26] = (BlueAgentActionType.REMOVE, "Defender")
            type_and_host_to_action_id[(BlueAgentActionType.REMOVE, "Defender")] = 26
            return action_id_to_type_and_host, type_and_host_to_action_id
        else:
            raise ValueError(f"Scenario: {scenario} not recognized")
