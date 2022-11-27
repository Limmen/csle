import subprocess
import csle_common.constants.constants as constants
from csle_common.dao.jobs.system_identification_job_config import SystemIdentificationJobConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_system_identification.expectation_maximization.expectation_maximization_algorithm import \
    ExpectationMaximizationAlgorithm
from csle_common.dao.system_identification.system_model_type import SystemModelType


class SystemIdentificationJobManager:
    """
    Class that manages system identification jobs in CSLE
    """

    @staticmethod
    def run_system_identification_job(job_config: SystemIdentificationJobConfig) -> None:
        """
        Runs a given system identification job

        :param job_config: the configuration of the job
        :return: None
        """
        emulation_env_config = None
        emulation_statistic = None
        if job_config.emulation_env_name is not None:
            emulation_env_config = MetastoreFacade.get_emulation_by_name(name=job_config.emulation_env_name)
        if job_config.emulation_statistics_id is not None:
            emulation_statistic = MetastoreFacade.get_emulation_statistic(id=job_config.emulation_statistics_id)
        if job_config.system_identification_config.model_type == SystemModelType.GAUSSIAN_MIXTURE:
            algorithm = ExpectationMaximizationAlgorithm(
                emulation_env_config=emulation_env_config, emulation_statistics=emulation_statistic,
                system_identification_config=job_config.system_identification_config,
                system_identification_job=job_config)
            algorithm.fit()

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
        p.communicate()
