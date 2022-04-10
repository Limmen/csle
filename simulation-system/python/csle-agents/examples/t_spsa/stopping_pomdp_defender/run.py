from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_agents.t_spsa.t_spsa import TSPSA

if __name__ == '__main__':
    emulation_env_config = MetastoreFacade.get_emulation("csle-level9-001")
    simulation_env_config = MetastoreFacade.get_simulation("csle-stopping-pomdp-defender")
    experiment_config = ExperimentConfig(
        output_dir="/tmp/tspsa_test", title="T-SPSA test", random_seeds=[399], agent_type=AgentType.T_SPSA,
        hparams={
            "N": HParam(value=100, name="N", descr="the number of training iterations"),
            "c": HParam(value=10, name="c", descr="scalar coefficient for determining perturbation sizes in T-SPSA"),
            "a": HParam(value=50, name="a", descr="scalar coefficient for determining gradient step sizes in T-SPSA"),
            "A": HParam(value=100, name="A", descr="scalar coefficient for determining gradient step sizes in T-SPSA"),
            "lambda": HParam(value=0.602, name="lambda", descr="scalar coefficient for determining perturbation sizes "
                                                            "in T-SPSA"),
            "epsilon": HParam(value=0.101, name="epsilon", descr="scalar coefficient for determining "
                                                              "gradient step sizes in T-SPSA"),
            "L": HParam(value=3, name="L", descr="the number of stop actions")
        }
    )
    agent = TSPSA(emulation_env_config=emulation_env_config, simulation_env_config=simulation_env_config,
                  experiment_config=experiment_config)
