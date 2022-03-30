from typing import List
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_stopping_actions \
    import EmulationAttackerStoppingActions
from csle_common.dao.emulation_action.defender.emulation_defender_stopping_actions \
    import EmulationDefenderStoppingActions
from csle_common.dao.emulation_action.attacker.emulation_attacker_nmap_actions import EmulationAttackerNMAPActions
from csle_common.dao.emulation_action.attacker.emulation_attacker_shell_actions import EmulationAttackerShellActions
from csle_common.dao.emulation_action.attacker.emulation_attacker_network_service_actions \
    import EmulationAttackerNetworkServiceActions
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.controllers.container_manager import ContainerManager
from csle_eval.emulator import Emulator


def novice_attacker_sequence(wait_steps: int, emulation_env_config: EmulationEnvConfig) -> List[EmulationAttackerAction]:
    num_nodes = len(emulation_env_config.containers_config.containers)
    subnet_masks = emulation_env_config.topology_config.subnetwork_masks
    wait_seq = [EmulationAttackerStoppingActions.CONTINUE(index=num_nodes + 1)] * wait_steps
    intrusion_seq = [
        EmulationAttackerNMAPActions.TCP_SYN_STEALTH_SCAN(index=num_nodes + 1, ips=subnet_masks, subnet=True),
        EmulationAttackerNMAPActions.SSH_SAME_USER_PASS_DICTIONARY(index=0, subnet=False),
        EmulationAttackerNMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(index=1, subnet=False),
        EmulationAttackerNMAPActions.FTP_SAME_USER_PASS_DICTIONARY(index=10, subnet=False),
        EmulationAttackerNetworkServiceActions.SERVICE_LOGIN(index=num_nodes + 1),
        EmulationAttackerShellActions.INSTALL_TOOLS(index=num_nodes + 1),
        EmulationAttackerShellActions.SSH_BACKDOOR(index=num_nodes + 1),
        EmulationAttackerNMAPActions.TCP_SYN_STEALTH_SCAN(index=num_nodes + 1, ips=subnet_masks, subnet=True),
        EmulationAttackerShellActions.SHELLSHOCK_EXPLOIT(index=24),
        EmulationAttackerNetworkServiceActions.SERVICE_LOGIN(index=num_nodes + 1),
        EmulationAttackerShellActions.INSTALL_TOOLS(index=num_nodes + 1),
        EmulationAttackerNMAPActions.SSH_SAME_USER_PASS_DICTIONARY(index=25, subnet=False),
        EmulationAttackerNetworkServiceActions.SERVICE_LOGIN(index=num_nodes + 1),
        EmulationAttackerShellActions.CVE_2010_0426_PRIV_ESC(index=25),
        EmulationAttackerNMAPActions.TCP_SYN_STEALTH_SCAN(index=num_nodes + 1, ips=subnet_masks, subnet=True)
    ]
    seq = wait_seq + intrusion_seq
    return seq


def passive_defender_sequence(length: int, emulation_env_config: EmulationEnvConfig) -> List[EmulationDefenderAction]:
    num_nodes = len(emulation_env_config.containers_config.containers)
    seq = [EmulationDefenderStoppingActions.CONTINUE(index=num_nodes + 1)] * length
    return seq


def run():
    emulation_env_config = MetastoreFacade.get_emulation("csle-level9-001")
    assert emulation_env_config is not None
    assert ContainerManager.is_emulation_running(emulation_env_config=emulation_env_config) is True
    attacker_sequence = novice_attacker_sequence(wait_steps=0, emulation_env_config=emulation_env_config)
    defender_sequence = passive_defender_sequence(length=len(attacker_sequence),
                                                  emulation_env_config=emulation_env_config)
    Emulator.run_action_sequences(emulation_env_config=emulation_env_config, attacker_sequence=attacker_sequence,
                                  defender_sequence=defender_sequence, repeat_times= 1, sleep_time= 15)


if __name__ == '__main__':
    run()