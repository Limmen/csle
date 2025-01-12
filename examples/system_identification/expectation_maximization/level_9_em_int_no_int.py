import csle_common.constants.constants as constants
from csle_common.dao.system_identification.system_identification_config import SystemIdentificationConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.system_identification.system_model_type import SystemModelType
from csle_common.dao.training.hparam import HParam
from csle_system_identification.expectation_maximization.expectation_maximization_algorithm \
    import ExpectationMaximizationAlgorithm
import csle_system_identification.constants.constants as system_identification_constants

if __name__ == '__main__':
    emulation_env_config = MetastoreFacade.get_emulation_by_name("csle-level9-070")
    emulation_statistic = MetastoreFacade.get_emulation_statistic(id=3)
    system_identifcation_config = SystemIdentificationConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}em_level9_test",
        title="Expectation-Maximization level 9 test",
        model_type=SystemModelType.GAUSSIAN_MIXTURE,
        log_every=1,
        hparams={
            system_identification_constants.SYSTEM_IDENTIFICATION.CONDITIONAL_DISTRIBUTIONS: HParam(
                value=["no_intrusion", "intrusion"],
                name=system_identification_constants.SYSTEM_IDENTIFICATION.CONDITIONAL_DISTRIBUTIONS,
                descr="the conditional distributions to estimate"),
            system_identification_constants.EXPECTATION_MAXIMIZATION.NUM_MIXTURES_PER_CONDITIONAL: HParam(
                value=[2, 3], descr="the number of mixtures per conditional distributions to estimate with EM",
                name=system_identification_constants.EXPECTATION_MAXIMIZATION.NUM_MIXTURES_PER_CONDITIONAL),
            system_identification_constants.SYSTEM_IDENTIFICATION.METRICS: HParam(
                value=["alerts_weighted_by_priority"],
                name=system_identification_constants.SYSTEM_IDENTIFICATION.METRICS,
                descr="the metrics to estimate")
        }
    )
    algorithm = ExpectationMaximizationAlgorithm(emulation_env_config=emulation_env_config,
                                                 emulation_statistics=emulation_statistic,
                                                 system_identification_config=system_identifcation_config)
    system_model = algorithm.fit()
    samples = list(range(0, 15000))
    for metric_conds in system_model.conditional_metric_distributions:
        for metric_cond in metric_conds:
            intrusion_dist = metric_cond.generate_distributions_for_samples(samples=samples)
    MetastoreFacade.save_gaussian_mixture_system_model(gaussian_mixture_system_model=system_model)
