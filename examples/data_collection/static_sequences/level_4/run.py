from typing import List
import csle_common.constants.constants as constants
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_stopping_actions \
    import EmulationAttackerStoppingActions
from csle_common.dao.emulation_action.defender.emulation_defender_stopping_actions \
    import EmulationDefenderStoppingActions
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_system_identification.emulator import Emulator
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_nmap_actions import EmulationAttackerNMAPActions
from csle_common.dao.emulation_action.attacker.emulation_attacker_shell_actions import EmulationAttackerShellActions
from csle_common.dao.emulation_action.attacker.emulation_attacker_network_service_actions \
    import EmulationAttackerNetworkServiceActions


def expert_attacker_sequence(wait_steps: int, emulation_env_config: EmulationEnvConfig) \
        -> List[EmulationAttackerAction]:
    """
    Returns a list of attacker actions representing the expert attacker

    :param wait_steps: the number of steps that the attacker waits before starting the intrusion
    :param emulation_env_config: the emulation configuration
    :return: the list of attacker actions
    """
    wait_seq = [EmulationAttackerStoppingActions.CONTINUE(index=-1)] * wait_steps
    intrusion_seq = emulation_env_config.static_attacker_sequences[constants.STATIC_ATTACKERS.EXPERT]
    seq = wait_seq + intrusion_seq
    return seq


def experienced_attacker_sequence(wait_steps: int, emulation_env_config: EmulationEnvConfig) \
        -> List[EmulationAttackerAction]:
    """
    Returns a sequence of attacker actions representing the experienced attacker

    :param wait_steps: the number of steps to wait before the intrusion starts
    :param emulation_env_config: the emulation config
    :return: the list of emulation actions
    """
    wait_seq = [EmulationAttackerStoppingActions.CONTINUE(index=-1)] * wait_steps
    intrusion_seq = emulation_env_config.static_attacker_sequences[constants.STATIC_ATTACKERS.EXPERIENCED]
    seq = wait_seq + intrusion_seq
    return seq


def novice_attacker_sequence(wait_steps: int, emulation_env_config: EmulationEnvConfig) \
        -> List[EmulationAttackerAction]:
    """
    Returns a sequence of attacker actions representing the novice attacker

    :param wait_steps: the number of steps that the attacker waits before starting the intrusion
    :param emulation_env_config: the emulation config
    :return: the list of actions
    """
    wait_seq = [EmulationAttackerStoppingActions.CONTINUE(index=-1)] * wait_steps
    intrusion_seq = emulation_env_config.static_attacker_sequences[constants.STATIC_ATTACKERS.NOVICE]
    seq = wait_seq + intrusion_seq
    return seq


def passive_defender_sequence(length: int, emulation_env_config: EmulationEnvConfig) -> List[EmulationDefenderAction]:
    """
    Returns a sequence of actions representing a passive defender

    :param length: the length of the sequence
    :param emulation_env_config: the configuration of the emulation to run the sequence
    :return: a sequence of defender actions in the emulation
    """
    seq = [EmulationDefenderStoppingActions.CONTINUE(index=-1)] * length
    return seq


def passive_attacker_sequence(length: int, emulation_env_config: EmulationEnvConfig) -> List[EmulationAttackerAction]:
    """
    Returns a sequence of actions representing a passive attacker

    :param length: the length of the sequence
    :param emulation_env_config: the configuration of the emulation to run the sequence
    :return: a sequence of defender actions in the emulation
    """
    seq = [EmulationAttackerStoppingActions.CONTINUE(index=-1)] * length
    return seq


def run() -> None:
    """
    Runs two static action sequences in the emulation csle-level9-090

    :return: None
    """
    executions = MetastoreFacade.list_emulation_executions_for_a_given_emulation(emulation_name="csle-level4-070")
    emulation_env_config = executions[0].emulation_env_config
    assert emulation_env_config is not None
    trace_len = 30
    subnet_masks = emulation_env_config.topology_config.subnetwork_masks
    attacker_sequence = [EmulationAttackerNMAPActions.TCP_SYN_STEALTH_SCAN(index=-1, ips=subnet_masks),
                         EmulationAttackerNMAPActions.SSH_SAME_USER_PASS_DICTIONARY(index=0),
                         EmulationAttackerNMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(index=0),
                         EmulationAttackerNMAPActions.FTP_SAME_USER_PASS_DICTIONARY(index=0),
                         EmulationAttackerNMAPActions.TCP_SYN_STEALTH_SCAN(index=-1, ips=subnet_masks),
                         EmulationAttackerShellActions.SHELLSHOCK_EXPLOIT(index=0),
                         EmulationAttackerNMAPActions.SSH_SAME_USER_PASS_DICTIONARY(index=0),
                         EmulationAttackerNMAPActions.PING_SCAN(index=-1, ips=subnet_masks),
                         EmulationAttackerShellActions.SAMBACRY_EXPLOIT(index=0),
                         EmulationAttackerNetworkServiceActions.SERVICE_LOGIN(index=-1),
                         EmulationAttackerShellActions.DVWA_SQL_INJECTION(index=0),
                         EmulationAttackerShellActions.CVE_2015_1427_EXPLOIT(index=0)
                         ]
    defender_sequence = passive_defender_sequence(length=len(attacker_sequence),
                                                  emulation_env_config=emulation_env_config)
    # em_statistic = MetastoreFacade.get_emulation_statistic(id=3)
    em_statistic = None
    Emulator.run_action_sequences(emulation_env_config=emulation_env_config, attacker_sequence=attacker_sequence,
                                  defender_sequence=defender_sequence, repeat_times=5000,
                                  sleep_time=emulation_env_config.kafka_config.time_step_len_seconds,
                                  descr="Passive system observation",
                                  save_emulation_traces_every=1,
                                  emulation_traces_to_save_with_data_collection_job=1,
                                  emulation_statistics=em_statistic, intrusion_start_p=1,
                                  intrusion_continue=1, trace_len=trace_len)


# Program entrypoint
if __name__ == '__main__':
    run()
