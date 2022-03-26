from typing import Tuple
import numpy as np
from csle_common.dao.network.env_state import EnvState
from csle_common.dao.network.env_config import CSLEEnvConfig
from csle_common.dao.action.attacker.attacker_action import AttackerAction
from csle_common.dao.action.attacker.attacker_action_type import AttackerActionType


class SimulatorUtil:
    """
    Class containing common utility functions for the simulator
    """

    @staticmethod
    def simulate_detection(a: AttackerAction, env_config: CSLEEnvConfig) -> Tuple[bool, int]:
        """
        Simulates probability that an attack is detected by a defender

        :param a: the action
        :param env_config: the environment config
        :return: boolean, true if detected otherwise false, reward
        """
        if env_config.simulate_detection:
            detected = False
            if a.type == AttackerActionType.EXPLOIT or a.type == AttackerActionType.RECON \
                    or a.type == AttackerActionType.PRIVILEGE_ESCALATION:
                # Base detection
                detected = np.random.rand() < (a.noise + env_config.base_detection_p)
            # Alerts detection
            if not detected:
                detected = np.random.rand() < (a.alerts[0] / env_config.attacker_max_alerts)
            r = env_config.attacker_detection_reward
            if not detected:
                r = 0
            return detected, r
        else:
            return False, 0



    @staticmethod
    def reachable_nodes(state: EnvState, env_config :CSLEEnvConfig) -> bool:
        """
        Checks whether a give node in the network is reachable

        :param state: the current state
        :param env_config: env_config
        :return: True or False
        """
        reachable_nodes = set()
        logged_in_machines = list(filter(lambda x: x.logged_in and x.tools_installed, state.attacker_obs_state.machines))
        for node in env_config.network_conf.nodes:
            if node.ip in env_config.network_conf.agent_reachable:
                reachable_nodes.add(node.ip)
            for machine in logged_in_machines:
                if node.ip in machine.reachable:
                    reachable_nodes.add(node.ip)
        return reachable_nodes

