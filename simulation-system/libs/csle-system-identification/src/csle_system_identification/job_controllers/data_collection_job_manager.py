import subprocess
import csle_common.constants.constants as constants
from csle_common.dao.jobs.data_collection_job_config import DataCollectionJobConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.controllers.container_controller import ContainerController
from csle_system_identification.emulator import Emulator


class DataCollectionJobManager:
    """
    Class that manages data collection jobs in CSLE
    """

    @staticmethod
    def run_data_collection_job(job_config: DataCollectionJobConfig) -> None:
        """
        Runs a given data collection job

        :param job_config: the configuration of the job
        :return: None
        """
        emulation_env_config = MetastoreFacade.get_emulation_by_name("csle-level9-030")
        assert emulation_env_config is not None
        assert ContainerController.is_emulation_running(emulation_env_config=emulation_env_config) is True
        em_statistic = MetastoreFacade.get_emulation_statistic(id=job_config.emulation_statistic_id)
        Emulator.run_action_sequences(
            emulation_env_config=emulation_env_config, attacker_sequence=job_config.attacker_sequence,
            defender_sequence=job_config.defender_sequence, repeat_times=job_config.repeat_times,
            sleep_time=emulation_env_config.kafka_config.time_step_len_seconds,
            descr=job_config.descr, emulation_statistics=em_statistic, data_collection_job=job_config,
            save_emulation_traces_every=job_config.save_emulation_traces_every,
            emulation_traces_to_save_with_data_collection_job=job_config.num_cached_traces)

    @staticmethod
    def start_data_collection_job_in_background(data_collection_job: DataCollectionJobConfig) \
            -> None:
        """
        Starts a system identification job with a given configuration in the background

        :param data_collection_job: the job configuration
        :return: None
        """
        cmd = constants.COMMANDS.START_SYSTEM_IDENTIFICATION_JOB.format(data_collection_job.id)
        p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
        p.communicate()
