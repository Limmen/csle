from typing import List, Optional
import os
from sklearn.mixture import GaussianMixture
from csle_system_identification.base.base_system_identification_algorithm import BaseSystemIdentificationAlgorithm
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
from csle_common.dao.system_identification.system_identification_config import SystemIdentificationConfig
from csle_common.dao.system_identification.gaussian_mixture_system_model import GaussianMixtureSystemModel
from csle_common.dao.system_identification.gaussian_mixture_conditional import GaussianMixtureConditional
from csle_common.dao.jobs.system_identification_job_config import SystemIdentificationJobConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.logging.log import Logger
from csle_common.util.general_util import GeneralUtil
import csle_system_identification.constants.constants as system_identification_constants


class ExpectationMaximizationAlgorithm(BaseSystemIdentificationAlgorithm):
    """
    Class that implements the system identification procedure using EM
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
        super(ExpectationMaximizationAlgorithm, self).__init__(
            emulation_env_config=emulation_env_config, emulation_statistics=emulation_statistics,
            system_identification_config=system_identification_config
        )
        self.system_identification_job = system_identification_job

    def fit(self) -> GaussianMixtureSystemModel:
        """
        Fits a Gaussian Mixture Distribution for each conditional and metric using the EM algorithm

        :return: the fitted model
        """
        if self.emulation_env_config is None:
            raise ValueError("Emulation config cannot be None")
        # Setup system identification job
        pid = os.getpid()
        descr = f"System identification through Expectation Maximization, " \
                f"emulation:{self.emulation_env_config.name}, statistic id: {self.emulation_statistics.id}"
        if self.system_identification_job is None:
            self.system_identification_job = SystemIdentificationJobConfig(
                emulation_env_name=self.emulation_env_config.name,
                emulation_statistics_id=self.emulation_statistics.id, pid=pid, progress_percentage=0,
                log_file_path=Logger.__call__().get_log_file_path(), descr=descr, system_model=None,
                system_identification_config=self.system_identification_config,
                physical_host_ip=GeneralUtil.get_host_ip()
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

        # Run the expectation maximization algorithm for each conditional and metric
        conditionals = self.system_identification_config.hparams[
            system_identification_constants.SYSTEM_IDENTIFICATION.CONDITIONAL_DISTRIBUTIONS].value
        metrics = self.system_identification_config.hparams[
            system_identification_constants.SYSTEM_IDENTIFICATION.METRICS].value
        Logger.__call__().get_logger().info(f"Starting execution of the Expectation-Maximization algorithm. "
                                            f"Emulation env name: {self.emulation_env_config.name}, "
                                            f"emulation_statistic_id: {self.emulation_statistics.id},"
                                            f"conditionals: {conditionals}, metrics: {metrics}")
        gaussian_conditional_mixtures = []
        for i, conditional in enumerate(conditionals):
            gaussian_conditional_metrics_mixtures = []
            for j, metric in enumerate(metrics):
                X = []
                X_set = set()
                counts = self.emulation_statistics.conditionals_counts[conditional][metric]
                for val, count in counts.items():
                    X.append([val])
                    X_set.add(val)
                num_components = self.system_identification_config.hparams[
                    system_identification_constants.EXPECTATION_MAXIMIZATION.NUM_MIXTURES_PER_CONDITIONAL].value[i]
                gmm = GaussianMixture(n_components=num_components).fit(X)
                gaussian_conditional_metrics_mixtures.append(
                    GaussianMixtureConditional.from_sklearn_gaussian_mixture(
                        gmm=gmm, conditional_name=conditional, num_components=num_components, dim=1,
                        metric_name=metric, sample_space=list(X_set)))
            gaussian_conditional_mixtures.append(gaussian_conditional_metrics_mixtures)

        model_descr = f"Model fitted through Expectation Maximization, " \
                      f"emulation:{self.emulation_env_config.name}, statistic id: {self.emulation_statistics.id}"
        model = GaussianMixtureSystemModel(emulation_env_name=self.emulation_env_config.name,
                                           emulation_statistic_id=self.emulation_statistics.id,
                                           conditional_metric_distributions=gaussian_conditional_mixtures,
                                           descr=model_descr)
        self.system_identification_job.system_model = model
        self.system_identification_job.progress_percentage = 100
        MetastoreFacade.update_system_identification_job(system_identification_job=self.system_identification_job,
                                                         id=self.system_identification_job.id)
        Logger.__call__().get_logger().info(f"Execution of the Expectation-Maximization algorithm complete."
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
            system_identification_constants.EXPECTATION_MAXIMIZATION.NUM_MIXTURES_PER_CONDITIONAL,
            system_identification_constants.SYSTEM_IDENTIFICATION.METRICS
        ]
