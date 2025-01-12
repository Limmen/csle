import csle_common.constants.constants as constants
from csle_common.dao.system_identification.system_identification_config import SystemIdentificationConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.system_identification.system_model_type import SystemModelType
from csle_common.dao.training.hparam import HParam
from csle_system_identification.empirical.empirical_algorithm \
    import EmpiricalAlgorithm
import csle_system_identification.constants.constants as system_identification_constants

if __name__ == '__main__':
    emulation_env_config = MetastoreFacade.get_emulation_by_name("csle-level9-070")
    emulation_statistic = MetastoreFacade.get_emulation_statistic(id=1)
    system_identifcation_config = SystemIdentificationConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}empirical_level9_test",
        title="Empirical algorithm level 9 test",
        model_type=SystemModelType.EMPIRICAL_DISTRIBUTION,
        log_every=1,
        hparams={
            system_identification_constants.SYSTEM_IDENTIFICATION.CONDITIONAL_DISTRIBUTIONS: HParam(
                value=["no_intrusion", "intrusion"],
                name=system_identification_constants.SYSTEM_IDENTIFICATION.CONDITIONAL_DISTRIBUTIONS,
                descr="the conditional distributions to estimate"),
            system_identification_constants.SYSTEM_IDENTIFICATION.METRICS: HParam(
                value=["alerts_weighted_by_priority"],
                name=system_identification_constants.SYSTEM_IDENTIFICATION.METRICS,
                descr="the metrics to estimate")
        }
    )
    algorithm = EmpiricalAlgorithm(emulation_env_config=emulation_env_config,
                                   emulation_statistics=emulation_statistic,
                                   system_identification_config=system_identifcation_config)
    system_model = algorithm.fit()
    MetastoreFacade.save_empirical_system_model(empirical_system_model=system_model)
