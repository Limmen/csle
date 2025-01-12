from typing import List
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_action.defender.emulation_defender_stopping_actions \
    import EmulationDefenderStoppingActions
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.emulation_action.attacker.emulation_attacker_nmap_actions import EmulationAttackerNMAPActions
from csle_common.dao.emulation_action.attacker.emulation_attacker_shell_actions import EmulationAttackerShellActions
from csle_system_identification.emulator import Emulator


def passive_defender_sequence(length: int, emulation_env_config: EmulationEnvConfig) -> List[EmulationDefenderAction]:
    """
    Returns a sequence of actions representing a passive defender

    :param length: the length of the sequence
    :param emulation_env_config: the configuration of the emulation to run the sequence
    :return: a sequence of defender actions in the emulation
    """
    seq = [EmulationDefenderStoppingActions.CONTINUE(index=-1)] * length
    return seq


def run() -> None:
    """
    Runs two static action sequences in the emulation csle-level9-070

    :return: None
    """
    executions = MetastoreFacade.list_emulation_executions_for_a_given_emulation(emulation_name="csle-level10-070")
    emulation_env_config = executions[0].emulation_env_config
    assert emulation_env_config is not None
    attacker_sequence = [
        EmulationAttackerNMAPActions.TCP_SYN_STEALTH_SCAN(index=-1,
                                                          ips=emulation_env_config.topology_config.subnetwork_masks),
        EmulationAttackerNMAPActions.TELNET_SAME_USER_PASS_DICTIONARY(index=1),
        EmulationAttackerNMAPActions.PING_SCAN(index=-1,
                                               ips=emulation_env_config.topology_config.subnetwork_masks),
        EmulationAttackerNMAPActions.SSH_SAME_USER_PASS_DICTIONARY(index=3),
        EmulationAttackerShellActions.CVE_2015_5602_PRIV_ESC(index=3),
        EmulationAttackerNMAPActions.TCP_SYN_STEALTH_SCAN(index=-1,
                                                          ips=emulation_env_config.topology_config.subnetwork_masks),
        EmulationAttackerShellActions.SAMBACRY_EXPLOIT(index=4),
        EmulationAttackerNMAPActions.TCP_SYN_STEALTH_SCAN(index=-1,
                                                          ips=emulation_env_config.topology_config.subnetwork_masks),
        EmulationAttackerShellActions.SHELLSHOCK_EXPLOIT(index=6),
        EmulationAttackerNMAPActions.PING_SCAN(index=-1,
                                               ips=emulation_env_config.topology_config.subnetwork_masks),
        EmulationAttackerShellActions.CVE_2015_3306_EXPLOIT(index=7),
        EmulationAttackerNMAPActions.TCP_SYN_STEALTH_SCAN(index=-1,
                                                          ips=emulation_env_config.topology_config.subnetwork_masks),
        EmulationAttackerShellActions.DVWA_SQL_INJECTION(index=8),
        EmulationAttackerNMAPActions.PING_SCAN(index=-1,
                                               ips=emulation_env_config.topology_config.subnetwork_masks),
        EmulationAttackerNMAPActions.SSH_SAME_USER_PASS_DICTIONARY(index=9),
        EmulationAttackerShellActions.CVE_2010_0426_PRIV_ESC(index=6),
        EmulationAttackerNMAPActions.TCP_SYN_STEALTH_SCAN(index=-1,
                                                          ips=emulation_env_config.topology_config.subnetwork_masks),
        EmulationAttackerShellActions.CVE_2016_10033_EXPLOIT(index=10),
        EmulationAttackerNMAPActions.PING_SCAN(index=-1, ips=emulation_env_config.topology_config.subnetwork_masks),
        EmulationAttackerNMAPActions.SSH_SAME_USER_PASS_DICTIONARY(index=11),
        EmulationAttackerNMAPActions.TCP_SYN_STEALTH_SCAN(index=-1,
                                                          ips=emulation_env_config.topology_config.subnetwork_masks),
        EmulationAttackerNMAPActions.FTP_SAME_USER_PASS_DICTIONARY(index=12),
        EmulationAttackerNMAPActions.PING_SCAN(index=-1, ips=emulation_env_config.topology_config.subnetwork_masks)
    ]
    defender_sequence = passive_defender_sequence(length=len(attacker_sequence),
                                                  emulation_env_config=emulation_env_config)
    em_statistic = None
    Emulator.run_action_sequences(emulation_env_config=emulation_env_config, attacker_sequence=attacker_sequence,
                                  defender_sequence=defender_sequence, repeat_times=5000,
                                  sleep_time=emulation_env_config.kafka_config.time_step_len_seconds,
                                  descr="Intrusion data for tolerance",
                                  save_emulation_traces_every=1,
                                  emulation_traces_to_save_with_data_collection_job=1,
                                  emulation_statistics=em_statistic, intrusion_start_p=1,
                                  intrusion_continue=1, restart_client_population=False)


# Program entrypoint
if __name__ == '__main__':
    run()
