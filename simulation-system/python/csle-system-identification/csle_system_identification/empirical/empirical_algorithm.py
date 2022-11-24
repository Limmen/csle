from typing import List, Optional
import os
import numpy as np
from csle_system_identification.base.base_system_identification_algorithm import BaseSystemIdentificationAlgorithm
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
from csle_common.dao.system_identification.system_identification_config import SystemIdentificationConfig
from csle_common.dao.system_identification.empirical_system_model import EmpiricalSystemModel
from csle_common.dao.system_identification.empirical_conditional import EmpiricalConditional
from csle_common.dao.jobs.system_identification_job_config import SystemIdentificationJobConfig
import csle_system_identification.constants.constants as system_identification_constants
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.logging.log import Logger


class EmpiricalAlgorithm(BaseSystemIdentificationAlgorithm):
    """
    Class that implements the system identification procedure using empirical distributions
    """

    def __init__(self, emulation_env_config: EmulationEnvConfig, emulation_statistics: EmulationStatistics,
                 system_identification_config: SystemIdentificationConfig,
                 system_identification_job: Optional[SystemIdentificationJobConfig] = None):
        """
        Initializes the algorithm

        :param emulation_env_config: the configuration of the emulation environment
        :param emulation_statistics: the statistics to fit
        :param system_identification_config: configuration of EM
        :param system_identification_job: system identification job config (optional)
        """
        super(EmpiricalAlgorithm, self).__init__(
            emulation_env_config=emulation_env_config, emulation_statistics=emulation_statistics,
            system_identification_config=system_identification_config
        )
        self.system_identification_job = system_identification_job

    def fit(self) -> EmpiricalSystemModel:
        """
        Fits an empirical distribution for each conditional and metric

        :return: the fitted model
        """
        # Setup system identification job
        pid = os.getpid()
        descr = f"System identification through empirical distributions, " \
                f"emulation:{self.emulation_env_config.name}, statistic id: {self.emulation_statistics.id}"
        if self.system_identification_job is None:
            self.system_identification_job = SystemIdentificationJobConfig(
                emulation_env_name=self.emulation_env_config.name,
                emulation_statistics_id=self.emulation_statistics.id, pid=pid, progress_percentage=0,
                log_file_path=Logger.__call__().get_log_file_path(), descr=descr, system_model=None,
                system_identification_config=self.system_identification_config
            )
            system_identification_job_id = MetastoreFacade.save_system_identification_job(
                system_identification_job=self.system_identification_job)
            self.system_identification_job.id = system_identification_job_id
        else:
            self.system_identification_job.pid = pid
            self.system_identification_job.progress_percentage = 0
            self.system_identification_job.system_model = None
            MetastoreFacade.update_system_identification_job(system_identification_job=self.system_identification_job,
                                                             id=self.system_identification_job.id)

        # Fit the empirical distributions for each conditional and metric
        conditionals = self.system_identification_config.hparams[
            system_identification_constants.SYSTEM_IDENTIFICATION.CONDITIONAL_DISTRIBUTIONS].value
        metrics = self.system_identification_config.hparams[
            system_identification_constants.SYSTEM_IDENTIFICATION.METRICS].value
        Logger.__call__().get_logger().info(f"Starting execution of the empirical algorithm. "
                                            f"Emulation env name: {self.emulation_env_config.name}, "
                                            f"emulation_statistic_id: {self.emulation_statistics.id},"
                                            f"conditionals: {conditionals}, metrics: {metrics}")
        empirical_conditionals = []
        complete_sample_space = set()
        for i, conditional in enumerate(conditionals):
            for j, metric in enumerate(metrics):
                counts = self.emulation_statistics.conditionals_counts[conditional][metric]
                for val, count in counts.items():
                    complete_sample_space.add(val)

        for i, conditional in enumerate(conditionals):
            empirical_conditionals_metrics = []
            for j, metric in enumerate(metrics):
                self.emulation_statistics.compute_descriptive_statistics_and_distributions()
                sample_space = list(complete_sample_space)
                probs = list(np.zeros(len(complete_sample_space)))
                for val, prob in self.emulation_statistics.conditionals_probs[conditional][metric].items():
                    idx = sample_space.index(val)
                    probs[idx] = prob
                empirical_conditionals_metrics.append(EmpiricalConditional(
                    conditional_name=conditional, metric_name=metric, sample_space=sample_space,
                    probabilities=probs
                ))
            empirical_conditionals.append(empirical_conditionals_metrics)

        model_descr = f"Model fitted through empirical algorithm, " \
                      f"emulation:{self.emulation_env_config.name}, statistic id: {self.emulation_statistics.id}"
        model = EmpiricalSystemModel(
            emulation_env_name=self.emulation_env_config.name, emulation_statistic_id=self.emulation_statistics.id,
            conditional_metric_distributions=empirical_conditionals, descr=model_descr)
        self.system_identification_job.system_model = model
        self.system_identification_job.progress_percentage = 100
        MetastoreFacade.update_system_identification_job(system_identification_job=self.system_identification_job,
                                                         id=self.system_identification_job.id)
        Logger.__call__().get_logger().info(f"Execution of the empirical algorithm complete."
                                            f"Emulation env name: {self.emulation_env_config.name}, "
                                            f"emulation_statistic_id: {self.emulation_statistics.id},"
                                            f"conditionals: {conditionals}, metrics: {metrics}")
        return model

    def hparam_names(self) -> List[str]:
        """
        :return: the names of the necessary hyperparameters
        """
        return [
            system_identification_constants.SYSTEM_IDENTIFICATION.CONDITIONAL_DISTRIBUTIONS,
            system_identification_constants.SYSTEM_IDENTIFICATION.METRICS
        ]
