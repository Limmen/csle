from csle_common.dao.network.emulation_env_state import EmulationEnvState
from csle_common.dao.network.emulation_env_agent_config import EmulationEnvAgentConfig


class SimulatorUtil:
    """
    Class containing common utility functions for the simulator
    """

    @staticmethod
    def reachable_nodes(state: EmulationEnvState, env_config :EmulationEnvAgentConfig) -> bool:
        """
        Checks whether a give node in the network is reachable

        :param state: the current state
        :param env_config: env_config
        :return: True or False
        """
        reachable_nodes = set()
        logged_in_machines = list(filter(lambda x: x.logged_in and x.tools_installed, state.attacker_obs_state.machines))
        for node in env_config.network_conf.nodes:
            if node.ips in env_config.network_conf.agent_reachable:
                reachable_nodes.add(node.ips)
            for machine in logged_in_machines:
                if node.ips in machine.reachable:
                    reachable_nodes.add(node.ips)
        return reachable_nodes

