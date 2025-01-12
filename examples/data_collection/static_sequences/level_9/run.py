from typing import List
import csle_common.constants.constants as constants
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_stopping_actions \
    import EmulationAttackerStoppingActions
from csle_common.dao.emulation_action.defender.emulation_defender_stopping_actions \
    import EmulationDefenderStoppingActions
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_system_identification.emulator import Emulator


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


def run() -> None:
    """
    Runs two static action sequences in the emulation csle-level9-070

    :return: None
    """
    executions = MetastoreFacade.list_emulation_executions_for_a_given_emulation(emulation_name="csle-level9-070")
    emulation_env_config = executions[0].emulation_env_config
    assert emulation_env_config is not None
    # attacker_sequence = novice_attacker_sequence(wait_steps=0, emulation_env_config=emulation_env_config)
    # attacker_sequence = experienced_attacker_sequence(wait_steps=0, emulation_env_config=emulation_env_config)
    attacker_sequence = expert_attacker_sequence(wait_steps=0, emulation_env_config=emulation_env_config)
    defender_sequence = passive_defender_sequence(length=len(attacker_sequence),
                                                  emulation_env_config=emulation_env_config)
    # em_statistic = MetastoreFacade.get_emulation_statistic(id=3)
    em_statistic = None
    Emulator.run_action_sequences(emulation_env_config=emulation_env_config, attacker_sequence=attacker_sequence,
                                  defender_sequence=defender_sequence, repeat_times=5000,
                                  sleep_time=emulation_env_config.kafka_config.time_step_len_seconds,
                                  descr="Intrusion data collected against expert attacker",
                                  save_emulation_traces_every=1,
                                  emulation_traces_to_save_with_data_collection_job=1,
                                  emulation_statistics=em_statistic, intrusion_start_p=0.8,
                                  intrusion_continue=1, restart_client_population=True)


# Program entrypoint
if __name__ == '__main__':
    run()
