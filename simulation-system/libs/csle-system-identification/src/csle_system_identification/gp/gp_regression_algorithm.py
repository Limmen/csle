from typing import List, Optional
import os
import torch
import gpytorch
from csle_system_identification.base.base_system_identification_algorithm import BaseSystemIdentificationAlgorithm
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
from csle_common.dao.system_identification.system_identification_config import SystemIdentificationConfig
from csle_common.dao.system_identification.gp_system_model import GPSystemModel
from csle_common.dao.system_identification.gp_conditional import GPConditional
from csle_common.dao.jobs.system_identification_job_config import SystemIdentificationJobConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.logging.log import Logger
from csle_common.util.general_util import GeneralUtil
import csle_system_identification.constants.constants as system_identification_constants
from csle_common.dao.system_identification.gp_regression_model_with_gauissan_noise import \
    GPRegressionModelWithGaussianNoise


class GPRegressionAlgorithm(BaseSystemIdentificationAlgorithm):
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
        super(GPRegressionAlgorithm, self).__init__(
            emulation_env_config=emulation_env_config, emulation_statistics=emulation_statistics,
            system_identification_config=system_identification_config
        )
        self.system_identification_job = system_identification_job

    def fit(self) -> GPSystemModel:
        """
        Fits a Gaussian Process for each conditional and metric using the GP regression algorithm

        :return: the fitted model
        """
        if self.emulation_env_config is None:
            raise ValueError("Emulation config cannot be None")

        # Setup system identification job
        pid = os.getpid()
        descr = f"System identification through Gaussian Process Regression, " \
                f"emulation:{self.emulation_env_config.name}, statistic id: {self.emulation_statistics.id}"
        if self.system_identification_job is None:
            self.system_identification_job = SystemIdentificationJobConfig(
                emulation_env_name=self.emulation_env_config.name,
                emulation_statistics_id=self.emulation_statistics.id, pid=pid, progress_percentage=0,
                log_file_path=Logger.__call__().get_log_file_path(), descr=descr, system_model=None,
                system_identification_config=self.system_identification_config,
                physical_host_ip=GeneralUtil.get_host_ip())
            system_identification_job_id = MetastoreFacade.save_system_identification_job(
                system_identification_job=self.system_identification_job)
            self.system_identification_job.id = system_identification_job_id
        else:
            self.system_identification_job.pid = pid
            self.system_identification_job.progress_percentage = 0
            self.system_identification_job.system_model = None
            MetastoreFacade.update_system_identification_job(system_identification_job=self.system_identification_job,
                                                             id=self.system_identification_job.id)

        # Run the GP regression algorithm for each conditional and metric
        conditionals = self.system_identification_config.hparams[
            system_identification_constants.SYSTEM_IDENTIFICATION.CONDITIONAL_DISTRIBUTIONS].value
        metrics = self.system_identification_config.hparams[
            system_identification_constants.SYSTEM_IDENTIFICATION.METRICS].value
        Logger.__call__().get_logger().info(f"Starting execution of the Gaussian Process regression algorithm. "
                                            f"Emulation env name: {self.emulation_env_config.name}, "
                                            f"emulation_statistic_id: {self.emulation_statistics.id},"
                                            f"conditionals: {conditionals}, metrics: {metrics}")
        gp_conditionals = []
        max_val = 0
        for i, conditional in enumerate(conditionals):
            for j, metric in enumerate(metrics):
                counts = self.emulation_statistics.conditionals_counts[conditional][metric]
                for val, count in counts.items():
                    if val > max_val:
                        max_val = val
        sample_space = list(range(0, max_val))
        self.emulation_statistics.compute_descriptive_statistics_and_distributions()

        for i, conditional in enumerate(conditionals):
            gp_conditionals_metrics = []
            for j, metric in enumerate(metrics):
                observed_x = []
                observed_y = []
                for val, prob in self.emulation_statistics.conditionals_probs[conditional][metric].items():
                    observed_x.append(val)
                    observed_y.append(prob)

                observed_x_tensor = torch.tensor(observed_x)
                observed_y_tensor = torch.tensor(observed_y)

                # initialize likelihood and model, the Gaussian likelihood assumes observed data points
                # have zero mean gaussian noise
                likelihood = gpytorch.likelihoods.GaussianLikelihood()
                model = GPRegressionModelWithGaussianNoise(observed_x_tensor, observed_y_tensor, likelihood)

                # get into train mode
                model.train()
                likelihood.train()

                # Includes GaussianLikelihood parameters
                lr = self.system_identification_config.hparams[
                    system_identification_constants.GAUSSIAN_PROCESS_REGRESSION.LEARNING_RATE].value
                optimizer = torch.optim.Adam(model.parameters(), lr=lr)

                # "Loss" for GPs - the marginal log likelihood
                mll = gpytorch.mlls.ExactMarginalLogLikelihood(likelihood, model)

                training_iter = self.system_identification_config.hparams[
                    system_identification_constants.GAUSSIAN_PROCESS_REGRESSION.TRAINING_ITERATIONS].value

                # Find optimal model hyperparameters by minimizing the negative marignal likelihood loss
                # through gradient descent.
                for i in range(training_iter):
                    # Zero gradients from previous iteration
                    optimizer.zero_grad()
                    # Output from model
                    output = model(observed_x_tensor)
                    # Calc loss and backprop gradients
                    loss = -mll(output, observed_y_tensor)
                    loss.backward()

                    Logger.__call__().get_logger().info(
                        f"[GP-Regression] iter:{i+1}/{training_iter}, loss:{loss.item()}, "
                        f"learned lengthscale param: {model.covar_module.base_kernel.lengthscale.item()}, "
                        f"learned likehood noise: {model.likelihood.noise.item()}")

                    # Gradient descent step
                    optimizer.step()
                gp_conditionals_metrics.append(GPConditional(
                    conditional_name=conditional, metric_name=metric, sample_space=sample_space,
                    observed_x=observed_x, observed_y=observed_y,
                    scale_parameter=model.covar_module.base_kernel.lengthscale.item(),
                    noise_parameter=model.likelihood.noise.item()
                ))
            gp_conditionals.append(gp_conditionals_metrics)

        model_descr = f"Model fitted through GP regression, " \
                      f"emulation:{self.emulation_env_config.name}, statistic id: {self.emulation_statistics.id}"
        model = GPSystemModel(
            emulation_env_name=self.emulation_env_config.name, emulation_statistic_id=self.emulation_statistics.id,
            conditional_metric_distributions=gp_conditionals, descr=model_descr)
        self.system_identification_job.system_model = model
        self.system_identification_job.progress_percentage = 100
        MetastoreFacade.update_system_identification_job(system_identification_job=self.system_identification_job,
                                                         id=self.system_identification_job.id)
        Logger.__call__().get_logger().info(f"Execution of the Gaussian process algorithm complete."
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
            system_identification_constants.SYSTEM_IDENTIFICATION.METRICS,
            system_identification_constants.GAUSSIAN_PROCESS_REGRESSION.LEARNING_RATE,
            system_identification_constants.GAUSSIAN_PROCESS_REGRESSION.TRAINING_ITERATIONS
        ]
