from typing import List, Optional
import os
from pymc import Model
import pymc as pm
import numpy as np
from sklearn.neighbors import KernelDensity
from csle_system_identification.base.base_system_identification_algorithm import BaseSystemIdentificationAlgorithm
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
from csle_common.dao.system_identification.system_identification_config import SystemIdentificationConfig
from csle_common.dao.system_identification.mcmc_system_model import MCMCSystemModel
from csle_common.dao.system_identification.mcmc_posterior import MCMCPosterior
from csle_common.dao.jobs.system_identification_job_config import SystemIdentificationJobConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.logging.log import Logger
from csle_common.util.general_util import GeneralUtil
import csle_system_identification.constants.constants as system_identification_constants


class MCMCAlgorithm(BaseSystemIdentificationAlgorithm):
    """
    Class that implements the system identification procedure using MCMC
    """

    def __init__(self, emulation_env_config: EmulationEnvConfig, emulation_statistics: EmulationStatistics,
                 system_identification_config: SystemIdentificationConfig,
                 bayesian_model: Model,
                 system_identification_job: Optional[SystemIdentificationJobConfig] = None):
        """
        Initializes the algorithm

        :param emulation_env_config: the configuration of the emulation environment
        :param emulation_statistics: the statistics to fit
        :param bayesian_models: Bayesian model
        :param system_identification_config: configuration of EM
        :param system_identification_job: system identification job config (optional)
        """
        super(MCMCAlgorithm, self).__init__(
            emulation_env_config=emulation_env_config, emulation_statistics=emulation_statistics,
            system_identification_config=system_identification_config
        )
        self.system_identification_job = system_identification_job
        self.bayesian_model = bayesian_model

    def fit(self) -> MCMCSystemModel:
        """
        Fits a posterior model through Markov-Chain Monte-Carlo

        :return: the fitted model
        """
        if self.emulation_env_config is None:
            raise ValueError("Emulation config cannot be None")

        # Setup system identification job
        pid = os.getpid()
        descr = f"System identification through Markov Chain Monte-Carlo, " \
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
        conditional = self.system_identification_config.hparams[
            system_identification_constants.SYSTEM_IDENTIFICATION.CONDITIONAL_DISTRIBUTION].value
        metric = self.system_identification_config.hparams[
            system_identification_constants.SYSTEM_IDENTIFICATION.METRIC].value
        parameters = self.system_identification_config.hparams[system_identification_constants.MCMC.PARAMETERS].value
        draws = self.system_identification_config.hparams[system_identification_constants.MCMC.DRAWS].value
        chains = self.system_identification_config.hparams[system_identification_constants.MCMC.CHAINS].value
        Logger.__call__().get_logger().info(f"Starting execution of the Markov Chain Monte-Carlo algorithm. "
                                            f"Emulation env name: {self.emulation_env_config.name}, "
                                            f"emulation_statistic_id: {self.emulation_statistics.id},"
                                            f"conditional: {conditional}, metric: {metric}, "
                                            f"parameters: {parameters}, draws: {draws}, chains: {chains}")
        posteriors = []
        observation_counts = self.emulation_statistics.conditionals_counts[conditional][metric]
        observations = []
        for val, count in observation_counts.items():
            for i in range(count):
                observations.append(val)
        with self.bayesian_model:
            trace = pm.sample(draws=draws, return_inferencedata=False, chains=chains)
            for param in parameters:
                param_trace = trace.get_values(varname=param)
                sample_space = np.unique(param_trace)
                sample_space = np.sort(sample_space)
                kde = KernelDensity(kernel='gaussian', bandwidth=0.2).fit(param_trace.reshape(len(param_trace), -1))
                densities = kde.score_samples(sample_space.reshape(len(sample_space), -1))
                posterior = MCMCPosterior(posterior_name=param, samples=param_trace, densities=densities,
                                          sample_space=sample_space)
                posteriors.append(posterior)
        model_descr = f"Model fitted through Markov Chain Monte-Carlo, " \
                      f"emulation:{self.emulation_env_config.name}, statistic id: {self.emulation_statistics.id}"
        model = MCMCSystemModel(
            emulation_env_name=self.emulation_env_config.name,
            emulation_statistic_id=self.emulation_statistics.id,
            posteriors=posteriors,
            descr=model_descr
        )
        self.system_identification_job.system_model = model
        self.system_identification_job.progress_percentage = 100
        MetastoreFacade.update_system_identification_job(system_identification_job=self.system_identification_job,
                                                         id=self.system_identification_job.id)
        Logger.__call__().get_logger().info(f"Execution of the Markov Chain Monte-Carlo algorithm complete."
                                            f"Emulation env name: {self.emulation_env_config.name}, "
                                            f"emulation_statistic_id: {self.emulation_statistics.id},"
                                            f"conditional: {conditional}, metric: {metric}, parameters: {parameters}")
        return model

    def hparam_names(self) -> List[str]:
        """
        :return: the names of the necessary hyperparameters
        """
        return [
            system_identification_constants.SYSTEM_IDENTIFICATION.CONDITIONAL_DISTRIBUTION,
            system_identification_constants.SYSTEM_IDENTIFICATION.METRIC,
            system_identification_constants.MCMC.PARAMETERS,
            system_identification_constants.MCMC.DRAWS,
            system_identification_constants.MCMC.CHAINS
        ]
