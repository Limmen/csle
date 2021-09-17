from typing import Tuple
from gym_pycr_ctf.dao.network.env_state import EnvState
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.action.attacker.attacker_action import AttackerAction
from gym_pycr_ctf.dao.observation.attacker.attacker_machine_observation_state import AttackerMachineObservationState
from gym_pycr_ctf.envs_model.logic.common.env_dynamics_util import EnvDynamicsUtil
from gym_pycr_ctf.envs_model.logic.simulation.util.simulator_util import SimulatorUtil


class ShellSimulatorUtil:
    """
    Class containing utility functions for simulating shell actions
    """

    @staticmethod
    def simulate_service_login_helper(s: EnvState, a: AttackerAction, env_config: EnvConfig, service_name : str = "ssh") \
            -> Tuple[EnvState, float, bool]:
        """
        Helper function for simulating login to various network services

        :param s: the current state
        :param a: the action to take
        :param env_config: the env config
        :param service_name: the name of the service to login to
        :return: s_prime, reward
        """
        new_obs_machines = []
        reachable_nodes = SimulatorUtil.reachable_nodes(state=s, env_config=env_config)
        discovered_nodes = list(map(lambda x: x.ip, s.attacker_obs_state.machines))
        reachable_nodes = list(filter(lambda x: x in discovered_nodes, reachable_nodes))
        for node in env_config.network_conf.nodes:
            if node.ip not in reachable_nodes:
                continue
            new_m_obs = AttackerMachineObservationState(ip=node.ip)
            new_m_obs.reachable = node.reachable_nodes
            credentials = None
            access = False
            for o_m in s.attacker_obs_state.machines:
                if o_m.ip == node.ip:
                    access = o_m.shell_access
                    credentials = o_m.shell_access_credentials
            if access:
                for service in node.services:
                    if service.name == service_name:
                        for cr in service.credentials:
                            for a_cr in credentials:
                                if a_cr.username == cr.username and a_cr.pw == cr.pw:
                                    new_m_obs.logged_in = True

                if new_m_obs.logged_in:
                    for cr in credentials:
                        cr_user = cr.username
                        if cr_user in node.root_usernames and service_name != "ftp":
                            new_m_obs.root = True
            new_m_obs.untried_credentials = False
            new_obs_machines.append(new_m_obs)

        net_outcome = EnvDynamicsUtil.merge_new_obs_with_old(s.attacker_obs_state.machines, new_obs_machines,
                                                             env_config=env_config, action=a)
        s_prime = s
        s_prime.attacker_obs_state.machines = net_outcome.attacker_machine_observations
        reward = EnvDynamicsUtil.reward_function(net_outcome=net_outcome, env_config=env_config, action=a)
        done, d_reward = EnvDynamicsUtil.emulate_detection(net_outcome=net_outcome, action=a, env_config=env_config)
        if done:
            reward = d_reward
        s_prime.attacker_obs_state.detected = done
        return s_prime, reward, done

