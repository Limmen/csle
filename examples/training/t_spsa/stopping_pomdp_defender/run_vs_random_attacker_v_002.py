import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.training.tabular_policy import TabularPolicy
from csle_agents.agents.t_spsa.t_spsa_agent import TSPSAAgent
import csle_agents.constants.constants as agents_constants
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil


if __name__ == '__main__':
    emulation_env_config = MetastoreFacade.get_emulation_by_name("csle-level9-001")
    simulation_env_config = MetastoreFacade.get_simulation_by_name("csle-stopping-pomdp-defender-002")
    experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}tspsa_test", title="T-SPSA test",
        random_seeds=[399, 98912,999,555],
        agent_type=AgentType.T_SPSA,
        log_every=1,
        hparams={
            agents_constants.T_SPSA.N: HParam(value=200, name=agents_constants.T_SPSA.N,
                                              descr="the number of training iterations"),
            agents_constants.T_SPSA.c: HParam(
                value=10, name=agents_constants.T_SPSA.c,
                descr="scalar coefficient for determining perturbation sizes in T-SPSA"),
            agents_constants.T_SPSA.a: HParam(
                value=1, name=agents_constants.T_SPSA.a,
                descr="scalar coefficient for determining gradient step sizes in T-SPSA"),
            agents_constants.T_SPSA.A: HParam(
                value=100, name=agents_constants.T_SPSA.A,
                descr="scalar coefficient for determining gradient step sizes in T-SPSA"),
            agents_constants.T_SPSA.LAMBDA: HParam(
                value=0.602, name=agents_constants.T_SPSA.LAMBDA,
                descr="scalar coefficient for determining perturbation sizes in T-SPSA"),
            agents_constants.T_SPSA.EPSILON: HParam(
                value=0.101, name=agents_constants.T_SPSA.EPSILON,
                descr="scalar coefficient for determining gradient step sizes in T-SPSA"),
            agents_constants.T_SPSA.L: HParam(value=3, name="L", descr="the number of stop actions"),
            agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(value=100, name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                                                            descr="number of iterations to evaluate theta"),
            agents_constants.COMMON.SAVE_EVERY: HParam(value=1000, name=agents_constants.COMMON.SAVE_EVERY,
                                                       descr="how frequently to save the model"),
            agents_constants.COMMON.CONFIDENCE_INTERVAL: HParam(
                value=0.95, name=agents_constants.COMMON.CONFIDENCE_INTERVAL,
                descr="confidence interval"),
            agents_constants.COMMON.MAX_ENV_STEPS: HParam(
                value=500, name=agents_constants.COMMON.MAX_ENV_STEPS,
                descr="maximum number of steps in the environment (for envs with infinite horizon generally)"),
            agents_constants.T_SPSA.GRADIENT_BATCH_SIZE: HParam(
                value=1, name=agents_constants.T_SPSA.GRADIENT_BATCH_SIZE,
                descr="the batch size of the gradient estimator"),
            agents_constants.COMMON.RUNNING_AVERAGE: HParam(
                value=100, name=agents_constants.COMMON.RUNNING_AVERAGE,
                descr="the number of samples to include when computing the running avg")
        },
        player_type=PlayerType.DEFENDER, player_idx=0
    )
    simulation_env_config.simulation_env_input_config.attacker_strategy = TabularPolicy(
        player_type=PlayerType.ATTACKER,
        actions=simulation_env_config.joint_action_space_config.action_spaces[1].actions,
        simulation_name=simulation_env_config.name, value_function=None, q_table=None,
        lookup_table=[
            [0.8, 0.2],
            [1, 0],
            [1,0]
        ],
        agent_type=AgentType.RANDOM, avg_R=-1)
    agent = TSPSAAgent(emulation_env_config=emulation_env_config, simulation_env_config=simulation_env_config,
                       experiment_config=experiment_config)
    simulation_env_config.simulation_env_input_config.stopping_game_config.R = list(StoppingGameUtil.reward_tensor(
        R_INT=-10, R_COST=-10, R_SLA=0, R_ST=20, L=3))
    experiment_execution = agent.train()
    MetastoreFacade.save_experiment_execution(experiment_execution)
    for policy in experiment_execution.result.policies.values():
        MetastoreFacade.save_multi_threshold_stopping_policy(multi_threshold_stopping_policy=policy)
