from csle_common.dao.system_identification.empirical_conditional import EmpiricalConditional
from csle_common.dao.system_identification.empirical_system_model import EmpiricalSystemModel
from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
from csle_common.dao.system_identification.gaussian_mixture_conditional import GaussianMixtureConditional
from csle_common.dao.system_identification.gaussian_mixture_system_model import GaussianMixtureSystemModel
from csle_common.dao.system_identification.gp_conditional import GPConditional
from csle_common.dao.system_identification.gp_system_model import GPSystemModel
from csle_common.dao.system_identification.mcmc_posterior import MCMCPosterior
from csle_common.dao.system_identification.mcmc_system_model import MCMCSystemModel
from csle_common.dao.system_identification.system_identification_config import SystemIdentificationConfig


class TestSystemIdentificationDaoSuite:
    """
    Test suite for management data access objects (DAOs)
    """

    def test_empirical_conditional(self, example_empirical_conditional: EmpiricalConditional) -> None:
        """
        Tests creation and dict conversion of the EmpiricalConditional DAO

        :param example_empirical_conditional: an example EmpiricalConditional
        :return: None
        """
        assert isinstance(example_empirical_conditional.to_dict(), dict)
        assert isinstance(EmpiricalConditional.from_dict(example_empirical_conditional.to_dict()), EmpiricalConditional)
        assert (EmpiricalConditional.from_dict(example_empirical_conditional.to_dict()).to_dict() ==
                example_empirical_conditional.to_dict())
        assert EmpiricalConditional.from_dict(example_empirical_conditional.to_dict()) == example_empirical_conditional

    def test_empirical_system_model(self, example_empirical_system_model: EmpiricalSystemModel) -> None:
        """
        Tests creation and dict conversion of the EmpiricalSystemModel DAO

        :param example_empirical_system_model: an example EmpiricalSystemModel
        :return: None
        """
        assert isinstance(example_empirical_system_model.to_dict(), dict)
        assert isinstance(EmpiricalSystemModel.from_dict(example_empirical_system_model.to_dict()),
                          EmpiricalSystemModel)
        assert (EmpiricalSystemModel.from_dict(example_empirical_system_model.to_dict()).to_dict() ==
                example_empirical_system_model.to_dict())
        assert EmpiricalSystemModel.from_dict(example_empirical_system_model.to_dict()) == \
               example_empirical_system_model

    def test_emulation_statistics(self, example_emulation_statistics: EmulationStatistics) -> None:
        """
        Tests creation and dict conversion of the EmulationStatistics DAO

        :param example_emulation_statistics: an example EmulationStatistics
        :return: None
        """
        assert isinstance(example_emulation_statistics.to_dict(), dict)
        assert isinstance(EmulationStatistics.from_dict(example_emulation_statistics.to_dict()),
                          EmulationStatistics)
        assert (EmulationStatistics.from_dict(example_emulation_statistics.to_dict()).to_dict() ==
                example_emulation_statistics.to_dict())
        assert EmulationStatistics.from_dict(example_emulation_statistics.to_dict()) == example_emulation_statistics

    def test_gaussian_mixture_conditional(
            self, example_gaussian_mixture_conditional: GaussianMixtureConditional) -> None:
        """
        Tests creation and dict conversion of the GaussianMixtureConditional DAO

        :param example_gaussian_mixture_conditional: an example GaussianMixtureConditional
        :return: None
        """
        assert isinstance(example_gaussian_mixture_conditional.to_dict(), dict)
        assert isinstance(GaussianMixtureConditional.from_dict(example_gaussian_mixture_conditional.to_dict()),
                          GaussianMixtureConditional)
        assert (GaussianMixtureConditional.from_dict(example_gaussian_mixture_conditional.to_dict()).to_dict() ==
                example_gaussian_mixture_conditional.to_dict())
        assert (GaussianMixtureConditional.from_dict(example_gaussian_mixture_conditional.to_dict()) ==
                example_gaussian_mixture_conditional)

    def test_gaussian_mixture_system_model(
            self, example_gaussian_mixture_system_model: GaussianMixtureSystemModel) -> None:
        """
        Tests creation and dict conversion of the GaussianMixtureSystemModel DAO

        :param example_gaussian_mixture_conditional: an example GaussianMixtureConditional
        :return: None
        """
        assert isinstance(example_gaussian_mixture_system_model.to_dict(), dict)
        assert isinstance(GaussianMixtureSystemModel.from_dict(example_gaussian_mixture_system_model.to_dict()),
                          GaussianMixtureSystemModel)
        assert (GaussianMixtureSystemModel.from_dict(example_gaussian_mixture_system_model.to_dict()).to_dict() ==
                example_gaussian_mixture_system_model.to_dict())
        assert (GaussianMixtureSystemModel.from_dict(example_gaussian_mixture_system_model.to_dict()) ==
                example_gaussian_mixture_system_model)

    def test_gp_conditional(self, example_gp_conditional: GPConditional) -> None:
        """
        Tests creation and dict conversion of the GPConditional DAO

        :param example_gp_conditional: an example GPConditional
        :return: None
        """
        assert isinstance(example_gp_conditional.to_dict(), dict)
        assert isinstance(GPConditional.from_dict(example_gp_conditional.to_dict()),
                          GPConditional)
        assert GPConditional.from_dict(example_gp_conditional.to_dict()).to_dict() == example_gp_conditional.to_dict()
        assert GPConditional.from_dict(example_gp_conditional.to_dict()) == example_gp_conditional

    def test_gp_system_model(self, example_gp_system_model: GPSystemModel) -> None:
        """
        Tests creation and dict conversion of the GPSystemModel DAO

        :param example_gp_system_model: an example GPSystemModel
        :return: None
        """
        assert isinstance(example_gp_system_model.to_dict(), dict)
        assert isinstance(GPSystemModel.from_dict(example_gp_system_model.to_dict()), GPSystemModel)
        assert (GPSystemModel.from_dict(example_gp_system_model.to_dict()).to_dict() ==
                example_gp_system_model.to_dict())
        assert (GPSystemModel.from_dict(example_gp_system_model.to_dict()) == example_gp_system_model)

    def test_mcmc_posterior(self, example_mcmc_posterior: MCMCPosterior) -> None:
        """
        Tests creation and dict conversion of the MCMCPosterior DAO

        :param example_mcmc_posterior: an example MCMCPosterior
        :return: None
        """
        assert isinstance(example_mcmc_posterior.to_dict(), dict)
        assert isinstance(MCMCPosterior.from_dict(example_mcmc_posterior.to_dict()), MCMCPosterior)
        assert MCMCPosterior.from_dict(example_mcmc_posterior.to_dict()).to_dict() == example_mcmc_posterior.to_dict()
        assert MCMCPosterior.from_dict(example_mcmc_posterior.to_dict()) == example_mcmc_posterior

    def test_mcmc_system_model(self, example_mcmc_system_model: MCMCSystemModel) -> None:
        """
        Tests creation and dict conversion of the MCMCSystemModel DAO

        :param example_mcmc_system_model: an example MCMCSystemModel
        :return: None
        """
        assert isinstance(example_mcmc_system_model.to_dict(), dict)
        assert isinstance(MCMCSystemModel.from_dict(example_mcmc_system_model.to_dict()),
                          MCMCSystemModel)
        assert (MCMCSystemModel.from_dict(example_mcmc_system_model.to_dict()).to_dict() ==
                example_mcmc_system_model.to_dict())
        assert MCMCSystemModel.from_dict(example_mcmc_system_model.to_dict()) == example_mcmc_system_model

    def test_system_identification_config(
            self, example_system_identification_config: SystemIdentificationConfig) -> None:
        """
        Tests creation and dict conversion of the SystemIdentificationConfig DAO

        :param example_system_identification_config: an example SystemIdentificationConfig
        :return: None
        """
        assert isinstance(example_system_identification_config.to_dict(), dict)
        assert isinstance(SystemIdentificationConfig.from_dict(example_system_identification_config.to_dict()),
                          SystemIdentificationConfig)
        assert (SystemIdentificationConfig.from_dict(example_system_identification_config.to_dict()).to_dict() ==
                example_system_identification_config.to_dict())
        assert (SystemIdentificationConfig.from_dict(example_system_identification_config.to_dict()) ==
                example_system_identification_config)
