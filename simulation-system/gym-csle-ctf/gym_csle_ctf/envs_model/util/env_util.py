from typing import Tuple, List
import math
from gym_csle_ctf.dao.network.env_config import CSLEEnvConfig
from gym_csle_ctf.dao.network.env_state import EnvState
from gym_csle_ctf.dao.action.attacker.attacker_action_id import AttackerActionId
from gym_csle_ctf.envs_model.logic.common.env_dynamics_util import EnvDynamicsUtil
from gym_csle_ctf.dao.action.attacker.attacker_action_type import AttackerActionType
from gym_csle_ctf.dao.action.attacker.attacker_action_outcome import AttackerActionOutcome


class EnvUtil:
    """
    Class with utility functions for the csle_CTF Environment
    """

    @staticmethod
    def is_defense_action_legal(defense_action_id: int, env_config: CSLEEnvConfig, env_state: EnvState) -> bool:
        """
        Checks if a given defense action is legal in the current state of the environment

        :param defense_action_id: the id of the action to check
        :param env_config: the environment config
        :param env_state: the environment state
        :param attacker_action: the id of the previous attack action
        :return: True if legal, else false
        """
        # return True
        # defense_action = env_config.defender_action_conf.actions[defense_action_id]
        # if env_state.attacker_obs_state.last_attacker_action is None and defense_action.id == DefenderActionId.STOP:
        #     return False
        # if env_state.attacker_obs_state.last_attacker_action is None and defense_action.id == DefenderActionId.CONTINUE:
        #     return True
        # if env_state.last_attacker_action is not None and env_state.last_attacker_action.id == AttackerActionId.CONTINUE \
        #         and defense_action.id == DefenderActionId.CONTINUE:
        #     return True
        # if env_state.last_attacker_action is not None and env_state.last_attacker_action.id != AttackerActionId.CONTINUE \
        #         and defense_action.id == DefenderActionId.STOP:
        #     return True
        return True

    @staticmethod
    def is_attack_action_legal(attack_action_id: int, env_config: CSLEEnvConfig, env_state: EnvState,
                               m_selection: bool = False,
                               m_action: bool = False, m_index: int = None) -> bool:
        """
        Checks if a given attack action is legal in the current state of the environment

        :param attack_action_id: the id of the action to check
        :param env_config: the environment config
        :param env_state: the environment state
        :param m_selection: boolean flag whether using AR policy m_selection or not
        :param m_action: boolean flag whether using AR policy m_action or not
        :param m_index: index of machine in case using AR policy
        :return: True if legal, else false
        """
        # If using AR policy
        if m_selection:
            return EnvUtil._is_attack_action_legal_m_selection(action_id=attack_action_id, env_config=env_config,
                                                                  env_state=env_state)
        elif m_action:
            return EnvUtil._is_attack_action_legal_m_action(action_id=attack_action_id, env_config=env_config,
                                                               env_state=env_state, machine_index=m_index)

        if not env_config.attacker_filter_illegal_actions:
            return True
        if attack_action_id > len(env_config.attacker_action_conf.actions) - 1:
            return False

        action = env_config.attacker_action_conf.actions[attack_action_id]
        ip = env_state.attacker_obs_state.get_action_ip(action)

        logged_in_ips_str = EnvDynamicsUtil.logged_in_ips_str(env_config=env_config, a=action, s=env_state,
                                                              full_ip_str=True)
        if (action.id, action.index, logged_in_ips_str) in env_state.attacker_obs_state.actions_tried:
            return False

        # Recon on subnet is always possible
        if action.type == AttackerActionType.RECON and action.subnet:
            return True

        # Recon on set of all found machines is always possible if there exists such machiens
        if action.type == AttackerActionType.RECON and action.index == -1 and len(
                env_state.attacker_obs_state.machines) > 0:
            return True

        # Optimal Stopping actions are always possible
        if action.type == AttackerActionType.STOP or action.type == AttackerActionType.CONTINUE:
            return True

        machine_discovered = False
        target_machine = None
        target_machines = []
        logged_in = False
        unscanned_filesystems = False
        untried_credentials = False
        root_login = False
        machine_root_login = False
        machine_logged_in = False
        uninstalled_tools = False
        machine_w_tools = False
        uninstalled_backdoor = False
        target_untried_credentials = False

        for m in env_state.attacker_obs_state.machines:
            if m_index == -1:
                target_machines.append(m)
                machine_discovered = True

            if m.logged_in:
                logged_in = True
                if not m.filesystem_searched:
                    unscanned_filesystems = True
                if m.root:
                    root_login = True
                    if not m.tools_installed and not m.install_tools_tried:
                        uninstalled_tools = True
                    else:
                        machine_w_tools = True
                    if m.tools_installed and not m.backdoor_installed and not m.backdoor_tried:
                        uninstalled_backdoor = True
            if m.ip == ip:
                machine_discovered = True
                target_machine = m
                if m.logged_in:
                    machine_logged_in = True
                    if m.root:
                        machine_root_login = True
                if m.untried_credentials:
                    target_untried_credentials = m.untried_credentials
            # if m.shell_access and not m.logged_in:
            #     untried_credentials = True
            if m.untried_credentials:
                untried_credentials = m.untried_credentials

        if action.subnet or action.id == AttackerActionId.NETWORK_SERVICE_LOGIN:
            machine_discovered = True

        # Privilege escalation only legal if machine discovered and logged in and not root
        if action.type == AttackerActionType.PRIVILEGE_ESCALATION and (not machine_discovered or not machine_logged_in
                                                                       or machine_root_login):
            return False

        # Exploit only legal if we have not already compromised the node
        if action.type == AttackerActionType.EXPLOIT and machine_logged_in and root_login:
            return False

        # Shell-access Exploit only legal if we do not already have untried credentials
        if action.type == AttackerActionType.EXPLOIT and action.action_outcome == AttackerActionOutcome.SHELL_ACCESS \
                and target_untried_credentials:
            return False

        # Priv-Esc Exploit only legal if we are already logged in and do not have root
        if action.type == AttackerActionType.EXPLOIT \
                and action.action_outcome == AttackerActionOutcome.PRIVILEGE_ESCALATION_ROOT \
                and (not machine_logged_in or root_login):
            return False

        # If IP is discovered, then IP specific action without other prerequisites is legal
        if machine_discovered and (action.type == AttackerActionType.RECON or action.type == AttackerActionType.EXPLOIT
                                   or action.type == AttackerActionType.PRIVILEGE_ESCALATION):
            if action.subnet and target_machine is None:
                return True
            if m_index is not None and m_index == -1:
                exploit_tried = all(
                    list(map(lambda x: env_state.attacker_obs_state.exploit_tried(a=action, m=x), target_machines)))
            else:
                exploit_tried = env_state.attacker_obs_state.exploit_tried(a=action, m=target_machine)
            if exploit_tried:
                return False
            return True

        # If nothing new to scan, find-flag is illegal
        if action.id == AttackerActionId.FIND_FLAG and not unscanned_filesystems:
            return False

        # If nothing new to backdoor, install backdoor is illegal
        if action.id == AttackerActionId.SSH_BACKDOOR and not uninstalled_backdoor:
            return False

        # If no new credentials, login to service is illegal
        if action.id == AttackerActionId.NETWORK_SERVICE_LOGIN and not untried_credentials:
            return False

        # Pivot recon possible if logged in on pivot machine with tools installed
        if machine_discovered and action.type == AttackerActionType.POST_EXPLOIT and logged_in and machine_w_tools:
            return True

        # If IP is discovered, and credentials are found and shell access, then post-exploit actions are legal
        if machine_discovered and action.type == AttackerActionType.POST_EXPLOIT \
                and ((target_machine is not None and target_machine.shell_access
                      and len(target_machine.shell_access_credentials) > 0)
                     or action.subnet or action.id == AttackerActionId.NETWORK_SERVICE_LOGIN):
            return True

        # Bash action not tied to specific IP only possible when having shell access and being logged in
        if action.id == AttackerActionId.FIND_FLAG and logged_in and unscanned_filesystems:
            return True

        # Bash action not tied to specific IP only possible when having shell access and being logged in and root
        if action.id == AttackerActionId.INSTALL_TOOLS and logged_in and root_login and uninstalled_tools:
            return True

        # Bash action not tied to specific IP only possible when having shell access and being logged in and root
        if action.id == AttackerActionId.SSH_BACKDOOR and logged_in and root_login and machine_w_tools and uninstalled_backdoor:
            return True

        return False

    @staticmethod
    def _is_attack_action_legal_m_selection(action_id: int, env_config: CSLEEnvConfig, env_state: EnvState) -> bool:
        """
        Utility method to check if a m_selection action is legal for AR policies

        :param action_id: the action id of the m_selection to  check
        :param env_config: the environment config
        :param env_state: the environment state
        :return: True if legal else False
        """
        # Subnet actions are always legal
        if action_id == env_config.num_nodes:
            return True

        # If machine is discovered then it is a legal action
        if action_id < len(env_state.attacker_obs_state.machines):
            m = env_state.attacker_obs_state.machines[action_id]
            if m is not None:
                return True

        return False

    @staticmethod
    def _is_attack_action_legal_m_action(action_id: int, env_config: CSLEEnvConfig, env_state: EnvState, machine_index: int) \
            -> bool:
        """
        Utility method to check if a machine-specific action is legal or not for AR-policies

        :param action_id: the machine-specific-action-id
        :param env_config: the environment config
        :param env_state: the environment state
        :param machine_index: index of the machine to apply the action to
        :return: True if legal else False
        """
        action_id_id = env_config.attacker_action_conf.action_ids[action_id]
        key = (action_id_id, machine_index)
        if key not in env_config.attacker_action_conf.action_lookup_d:
            return False
        action = env_config.attacker_action_conf.action_lookup_d[(action_id_id, machine_index)]
        logged_in = False
        for m in env_state.attacker_obs_state.machines:
            if m.logged_in:
                logged_in = True

        if machine_index == env_config.num_nodes:
            if action.subnet or action.index == env_config.num_nodes:
                # Recon an exploits are always legal
                if action.type == AttackerActionType.RECON or action.type == AttackerActionType.EXPLOIT:
                    return True
                # Bash action not tied to specific IP only possible when having shell access and being logged in
                if action.id == AttackerActionId.FIND_FLAG and logged_in:
                    return True
                return False
            else:
                return False
        else:
            if action.subnet or action.index == env_config.num_nodes:
                return False
            else:
                # Recon an exploits are always legal
                if action.type == AttackerActionType.RECON or action.type == AttackerActionType.EXPLOIT:
                    return True

                if machine_index < len(env_state.attacker_obs_state.machines):
                    env_state.attacker_obs_state.sort_machines()
                    target_machine = env_state.attacker_obs_state.machines[machine_index]

                    # If IP is discovered, and credentials are found and shell access, then post-exploit actions are legal
                    if action.type == AttackerActionType.POST_EXPLOIT and target_machine.shell_access \
                            and len(target_machine.shell_access_credentials) > 0:
                        return True

                    # Bash action not tied to specific IP only possible when having shell access and being logged in
                    if action.id == AttackerActionId.FIND_FLAG and logged_in:
                        return True
        return False

    @staticmethod
    def compute_optimal_defender_reward(s: EnvState, env_config: CSLEEnvConfig) -> Tuple[float, List[int], int]:
        """
        Computes the optimal defender reward

        :param s: the environment state
        :param env_config: the environment configuration
        :return: the optimal defender reward, the optimal stopping indexes, the optimal number of stops remaining
        """
        optimal_final_stopping_time = max(s.attacker_obs_state.intrusion_step + 1,
                                    env_config.maximum_number_of_defender_stop_actions -
                                    env_config.attacker_prevented_stops_remaining)
        optimal_stops_remaining = env_config.attacker_prevented_stops_remaining
        optimal_stopping_indexes = []
        for i in range(env_config.maximum_number_of_defender_stop_actions - 1, -1, -1):
            if i >= env_config.attacker_prevented_stops_remaining:
                j = i - env_config.attacker_prevented_stops_remaining
                opt_stop_index = max(1, optimal_final_stopping_time - j)
                optimal_stopping_indexes.append(opt_stop_index)
            else:
                optimal_stopping_indexes.append(-1)

        costs = 0
        for i in range(env_config.maximum_number_of_defender_stop_actions, -1, -1):
            if i < env_config.attacker_prevented_stops_remaining:
                break
            costs += env_config.multistop_costs[i]

        optimal_service_reward = 0
        optimal_service_reward = optimal_service_reward + env_config.defender_service_reward * \
                                 max(0, (optimal_final_stopping_time  -
                                  (env_config.maximum_number_of_defender_stop_actions -
                                   env_config.attacker_prevented_stops_remaining)))
        for i in range(env_config.maximum_number_of_defender_stop_actions, 0, -1):
            if i < env_config.attacker_prevented_stops_remaining:
                break
            elif i == env_config.attacker_prevented_stops_remaining:
                if env_config.attacker_prevented_stops_remaining > 0:
                    optimal_service_reward += (max(0, s.defender_obs_state.step - optimal_final_stopping_time + 1)) * \
                                              env_config.defender_service_reward / (
                                                  math.pow(2, env_config.maximum_number_of_defender_stop_actions - i))

        optimal_defender_reward = optimal_service_reward + env_config.defender_caught_attacker_reward + costs
        # print(f"optimal def rew:{optimal_defender_reward}, service:{optimal_service_reward}, "
        #       f"caught_attacker:{env_config.defender_caught_attacker_reward}, costs: {costs},"
        #       f"continue service step:{max(0, s.defender_obs_state.step - optimal_stopping_time + 1)},"
        #       f"service steps prior to first stop :{max(0, optimal_stopping_time - (env_config.maximum_number_of_defender_stop_actions - env_config.attacker_prevented_stops_remaining))},"
        #       f"optimal_stopping_step:{optimal_stopping_time},"
        #       f"intrusion step:{s.attacker_obs_state.intrusion_step},"
        #       f"number of stops:{(env_config.maximum_number_of_defender_stop_actions - env_config.attacker_prevented_stops_remaining)}")
        return optimal_defender_reward, optimal_stopping_indexes, optimal_stops_remaining