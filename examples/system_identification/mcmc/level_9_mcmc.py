import pymc as pm
import csle_common.constants.constants as constants
from csle_common.dao.system_identification.system_identification_config import SystemIdentificationConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.system_identification.system_model_type import SystemModelType
from csle_common.dao.training.hparam import HParam
from csle_system_identification.mcmc.mcmc import MCMCAlgorithm
import csle_system_identification.constants.constants as system_identification_constants

if __name__ == '__main__':
    emulation_env_config = MetastoreFacade.get_emulation_by_name("csle-level9-070")
    emulation_statistic = MetastoreFacade.get_emulation_statistic(id=1)
    system_identifcation_config = SystemIdentificationConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}mcmc_level9_test",
        title="MCMC algorithm level 9 test",
        model_type=SystemModelType.EMPIRICAL_DISTRIBUTION,
        log_every=1,
        hparams={
            system_identification_constants.SYSTEM_IDENTIFICATION.CONDITIONAL_DISTRIBUTION: HParam(
                value="no_intrusion",
                name=system_identification_constants.SYSTEM_IDENTIFICATION.CONDITIONAL_DISTRIBUTION,
                descr="the conditional distribution with the observations"),
            system_identification_constants.SYSTEM_IDENTIFICATION.METRIC: HParam(
                value="alerts_weighted_by_priority",
                name=system_identification_constants.SYSTEM_IDENTIFICATION.METRIC,
                descr="the metric that is observed"),
            system_identification_constants.MCMC.PARAMETERS: HParam(
                value=["mu", "sigma"],
                name=system_identification_constants.MCMC.PARAMETERS,
                descr="the parameters of the Bayesian model"),
            system_identification_constants.MCMC.CHAINS: HParam(
                value=4,
                name=system_identification_constants.MCMC.CHAINS,
                descr="the number of MCMC chains for fitting"),
            system_identification_constants.MCMC.DRAWS: HParam(
                value=1000,
                name=system_identification_constants.MCMC.DRAWS,
                descr="the number of draws of the posterior")
        }
    )
    observation_counts = emulation_statistic.conditionals_counts["no_intrusion"]["alerts_weighted_by_priority"]
    observations = []
    for val, count in observation_counts.items():
        for i in range(count):
            observations.append(val)
    bayesian_model = pm.Model()
    with bayesian_model:
        mu = pm.Flat("mu")
        sigma = pm.HalfFlat("sigma")
        Y_obs = pm.Normal("Y_obs", mu=mu, sigma=sigma, observed=observations)
    algorithm = MCMCAlgorithm(emulation_env_config=emulation_env_config,
                              emulation_statistics=emulation_statistic,
                              bayesian_model=bayesian_model,
                              system_identification_config=system_identifcation_config)
    system_model = algorithm.fit()
    MetastoreFacade.save_mcmc_system_model(mcmc_system_model=system_model)
