from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_agents.t_spsa.t_spsa_agent import TSPSAAgent

if __name__ == '__main__':
    emulation_env_config = MetastoreFacade.get_emulation("csle-level9-001")
    simulation_env_config = MetastoreFacade.get_simulation("csle-stopping-pomdp-defender-001")
    experiment_config = ExperimentConfig(
        output_dir="/tmp/tspsa_test", title="T-SPSA test", random_seeds=[399, 98912], agent_type=AgentType.T_SPSA,
        log_every=10,
        hparams={
            "N": HParam(value=100, name="N", descr="the number of training iterations"),
            "c": HParam(value=10, name="c", descr="scalar coefficient for determining perturbation sizes in T-SPSA"),
            "a": HParam(value=1, name="a", descr="scalar coefficient for determining gradient step sizes in T-SPSA"),
            "A": HParam(value=100, name="A", descr="scalar coefficient for determining gradient step sizes in T-SPSA"),
            "lambda": HParam(value=0.602, name="lambda", descr="scalar coefficient for determining perturbation sizes "
                                                            "in T-SPSA"),
            "epsilon": HParam(value=0.101, name="epsilon", descr="scalar coefficient for determining "
                                                              "gradient step sizes in T-SPSA"),
            "L": HParam(value=3, name="L", descr="the number of stop actions"),
            "eval_batch_size": HParam(value=100, name="eval_batch_size", descr="number of iterations to evaluate theta"),
            "theta1": HParam(value=[-4,-4,-4], name="theta1", descr="initial thresholds")
        }
    )
    agent = TSPSAAgent(emulation_env_config=emulation_env_config, simulation_env_config=simulation_env_config,
                       experiment_config=experiment_config)
    experiment_execution = agent.train()
    MetastoreFacade.save_experiment_execution(experiment_execution)
    for policy in experiment_execution.result.policies.values():
        MetastoreFacade.save_tspsa_policy(t_spsa_policy=policy)
