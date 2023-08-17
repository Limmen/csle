from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.system_identification.system_identification_config import SystemIdentificationConfig
from csle_common.dao.system_identification.system_model_type import SystemModelType
from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
import csle_system_identification.constants.constants as system_identification_constants
from csle_common.dao.training.hparam import HParam
from csle_system_identification.empirical.empirical_algorithm import EmpiricalAlgorithm


class TestEmpiricalAlgorithmSuite:
    """
    Test suite for empirical_algorithm.py
    """

    def test_init(self, get_ex_em_env: EmulationEnvConfig) -> None:
        """
        Tests initialization of the EmpiricalAlgorithm

        :return: None
        """
        sys_id_config = SystemIdentificationConfig(
            output_dir="test_dir", title="test init", model_type=SystemModelType.EMPIRICAL_DISTRIBUTION,
            log_every=1, hparams={
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
        stats = EmulationStatistics(emulation_name="test_em", descr="test")
        emp_alg = EmpiricalAlgorithm(emulation_env_config=get_ex_em_env, emulation_statistics=stats,
                                     system_identification_config=sys_id_config, system_identification_job=None)
        assert emp_alg.system_identification_job is None
        assert emp_alg.emulation_env_config is not None
        assert emp_alg.emulation_statistics is not None
        assert emp_alg.system_identification_config is not None
