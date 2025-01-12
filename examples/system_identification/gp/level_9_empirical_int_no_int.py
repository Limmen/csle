import csle_common.constants.constants as constants
from csle_common.dao.system_identification.system_identification_config import SystemIdentificationConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.system_identification.system_model_type import SystemModelType
from csle_common.dao.training.hparam import HParam
from csle_system_identification.gp.gp_regression_algorithm \
    import GPRegressionAlgorithm
import csle_system_identification.constants.constants as system_identification_constants

if __name__ == '__main__':
    emulation_env_config = MetastoreFacade.get_emulation_by_name("csle-level9-070")
    emulation_statistic = MetastoreFacade.get_emulation_statistic(id=10)
    system_identifcation_config = SystemIdentificationConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}gp_level9_test",
        title="GP regression algorithm level 9 test",
        model_type=SystemModelType.GAUSSIAN_PROCESS,
        log_every=1,
        hparams={
            system_identification_constants.SYSTEM_IDENTIFICATION.CONDITIONAL_DISTRIBUTIONS: HParam(
                value=["no_intrusion", "intrusion"],
                name=system_identification_constants.SYSTEM_IDENTIFICATION.CONDITIONAL_DISTRIBUTIONS,
                descr="the conditional distributions to estimate"),
            system_identification_constants.SYSTEM_IDENTIFICATION.METRICS: HParam(
                value=["alerts_weighted_by_priority"],
                name=system_identification_constants.SYSTEM_IDENTIFICATION.METRICS,
                descr="the metrics to estimate"),
            system_identification_constants.GAUSSIAN_PROCESS_REGRESSION.LEARNING_RATE: HParam(
                value=0.001,
                name=system_identification_constants.GAUSSIAN_PROCESS_REGRESSION.LEARNING_RATE,
                descr="the learning rate for learning hparams of the GP"),
            system_identification_constants.GAUSSIAN_PROCESS_REGRESSION.TRAINING_ITERATIONS: HParam(
                value=10,
                name=system_identification_constants.GAUSSIAN_PROCESS_REGRESSION.TRAINING_ITERATIONS,
                descr="training iterations to learn hparams of the GP")
        }
    )
    algorithm = GPRegressionAlgorithm(
        emulation_env_config=emulation_env_config, emulation_statistics=emulation_statistic,
        system_identification_config=system_identifcation_config)
    system_model = algorithm.fit()
    MetastoreFacade.save_gp_system_model(gp_system_model=system_model)
