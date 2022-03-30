import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_observation.attacker.emulation_attacker_machine_observation_state \
    import EmulationAttackerMachineObservationState
from csle_common.util.env_dynamics_util import EnvDynamicsUtil
from csle_attacker.simulation.util.simulator_util import SimulatorUtil


class ShellSimulatorUtil:
    """
    Class containing utility functions for simulating shell actions
    """

    @staticmethod
    def simulate_service_login_helper(
            s: EmulationEnvState, a: EmulationAttackerAction,
            emulation_env_config: EmulationEnvConfig, service_name : str = constants.SSH.SERVICE_NAME) \
            -> EmulationEnvState:
        """
        Helper function for simulating login to various network services

        :param s: the current state
        :param a: the action to take
        :param emulation_env_config: the emulation env config
        :param service_name: the name of the service to login to
        :return: s_prime
        """
        new_obs_machines = []
        reachable_nodes = SimulatorUtil.reachable_nodes(state=s, emulation_env_config=emulation_env_config)
        discovered_nodes = list(map(lambda x: x.internal_ip, s.attacker_obs_state.machines))
        reachable_nodes = list(filter(lambda x: x in discovered_nodes, reachable_nodes))
        for c in emulation_env_config.containers_config.containers:
            if not c.reachable(reachable_ips=list(reachable_nodes)):
                continue
            new_m_obs = EmulationAttackerMachineObservationState(ips=c.get_ips())
            new_m_obs.reachable = emulation_env_config.containers_config.get_reachable_ips(container=c)
            credentials = None
            access = False
            for o_m in s.attacker_obs_state.machines:
                if o_m.ips == c.get_ips():
                    access = o_m.shell_access
                    credentials = o_m.shell_access_credentials
            if access:
                for service in emulation_env_config.services_config.get_services_for_ips(ips=c.get_ips()):
                    if service.name == service_name:
                        for cr in service.credentials:
                            for a_cr in credentials:
                                if a_cr.username == cr.username and a_cr.pw == cr.pw:
                                    new_m_obs.logged_in = True

                if new_m_obs.logged_in:
                    for cr in credentials:
                        cr_user = cr.username
                        if cr_user in emulation_env_config.users_config.get_root_usernames(ips=c.get_ips()) \
                                and service_name != constants.FTP.SERVICE_NAME:
                            new_m_obs.root = True
                    if new_m_obs.backdoor_installed:
                        new_m_obs.root = True
            new_m_obs.untried_credentials = False
            new_obs_machines.append(new_m_obs)

        attacker_machine_observations = EnvDynamicsUtil.merge_new_obs_with_old(s.attacker_obs_state.machines, new_obs_machines,
                                                             emulation_env_config=emulation_env_config, action=a)
        s_prime = s
        s_prime.attacker_obs_state.machines = attacker_machine_observations
        return s_prime

