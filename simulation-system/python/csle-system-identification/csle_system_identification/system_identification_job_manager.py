import subprocess
import csle_common.constants.constants as constants
from csle_common.dao.jobs.system_identification_job_config import SystemIdentificationJobConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.controllers.container_manager import ContainerManager
from csle_system_identification.emulator import Emulator


class SystemIdentificationJobManager:
    """
    Class that manages system identification jobs in CSLE
    """

    @staticmethod
    def run_system_identification_job(job_config: SystemIdentificationJobConfig) -> None:
        """
        Runs a given training job

        :param job_config: the configuration of the job
        :return: None
        """
        emulation_env_config = MetastoreFacade.get_emulation("csle-level9-001")
        assert emulation_env_config is not None
        assert ContainerManager.is_emulation_running(emulation_env_config=emulation_env_config) is True
        em_statistic = MetastoreFacade.get_emulation_statistic(id=job_config.emulation_statistic_id)
        Emulator.run_action_sequences(emulation_env_config=emulation_env_config,
                                      attacker_sequence=job_config.attacker_sequence,
                                      defender_sequence=job_config.defender_sequence,
                                      repeat_times=job_config.repeat_times,
                                      sleep_time=emulation_env_config.log_sink_config.time_step_len_seconds,
                                      descr=job_config.descr, emulation_statistics=em_statistic,
                                      system_identification_job=job_config)

    @staticmethod
    def start_system_identification_job_in_background(system_identification_job: SystemIdentificationJobConfig) \
            -> None:
        """
        Starts a system identification job with a given configuration in the background

        :param system_identification_job: the job configuration
        :return: None
        """
        cmd = constants.COMMANDS.START_SYSTEM_IDENTIFICATION_JOB.format(system_identification_job.id)
        p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
        (output, err) = p.communicate()