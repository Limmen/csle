from typing import Set
from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig


class SimulatorUtil:
    """
    Class containing common utility functions for the simulator
    """

    @staticmethod
    def reachable_nodes(state: EmulationEnvState, emulation_env_config: EmulationEnvConfig) -> Set[str]:
        """
        Checks whether a give node in the network is reachable

        :param state: the current state
        :param emulation_env_config: emulation env_config
        :return: True or False
        """
        reachable_nodes = set()
        agent_reachable = emulation_env_config.containers_config.get_agent_reachable_ips()
        logged_in_machines = list(filter(lambda x: x.logged_in and x.tools_installed, state.attacker_obs_state.machines))
        for c in emulation_env_config.containers_config.containers:
            for ip in c.get_ips():
                if ip in agent_reachable:
                    reachable_nodes.add(ip)
            for machine in logged_in_machines:
                for ip in c.get_ips():
                    if ip in machine.reachable:
                        reachable_nodes.add(ip)
        return reachable_nodes

