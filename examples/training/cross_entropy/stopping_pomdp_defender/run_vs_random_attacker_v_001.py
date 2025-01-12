import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.cross_entropy.cross_entropy_agent import CrossEntropyAgent
import csle_agents.constants.constants as agents_constants
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil
from csle_common.dao.training.policy_type import PolicyType
from csle_agents.common.objective_type import ObjectiveType

if __name__ == '__main__':
    emulation_name = "csle-level9-070"
    emulation_env_config = MetastoreFacade.get_emulation_by_name(emulation_name)
    if emulation_env_config is None:
        raise ValueError(f"Could not find an emulation environment with the name: {emulation_name}")
    simulation_name = "csle-stopping-pomdp-defender-002"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}cross_entropy_test", title="Cross-entropy test",
        random_seeds=[399, 98912, 999],
        agent_type=AgentType.CROSS_ENTROPY,
        log_every=1,
        hparams={
            agents_constants.CROSS_ENTROPY.N: HParam(value=50, name=constants.T_SPSA.N,
                                                     descr="the number of training iterations"),
            agents_constants.CROSS_ENTROPY.L: HParam(value=3, name=agents_constants.CROSS_ENTROPY.L,
                                                     descr="the number of stop actions"),
            agents_constants.CROSS_ENTROPY.K: HParam(value=100, name=agents_constants.CROSS_ENTROPY.K,
                                                     descr="the number of samples in each iteration of CE"),
            agents_constants.CROSS_ENTROPY.LAMB: HParam(value=0.15, name=agents_constants.CROSS_ENTROPY.K,
                                                        descr="the number of samples to keep in each iteration of CE"),
            agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(value=50, name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                                                            descr="number of iterations to evaluate theta"),
            agents_constants.CROSS_ENTROPY.THETA1: HParam(value=[-3, -3, -3],
                                                          name=agents_constants.CROSS_ENTROPY.THETA1,
                                                          descr="initial thresholds"),
            agents_constants.COMMON.SAVE_EVERY: HParam(value=1000, name=agents_constants.COMMON.SAVE_EVERY,
                                                       descr="how frequently to save the model"),
            agents_constants.COMMON.CONFIDENCE_INTERVAL: HParam(
                value=0.95, name=agents_constants.COMMON.CONFIDENCE_INTERVAL,
                descr="confidence interval"),
            agents_constants.COMMON.MAX_ENV_STEPS: HParam(
                value=100, name=agents_constants.COMMON.MAX_ENV_STEPS,
                descr="maximum number of steps in the environment (for envs with infinite horizon generally)"),
            agents_constants.COMMON.RUNNING_AVERAGE: HParam(
                value=100, name=agents_constants.COMMON.RUNNING_AVERAGE,
                descr="the number of samples to include when computing the running avg"),
            agents_constants.COMMON.GAMMA: HParam(
                value=0.99, name=agents_constants.COMMON.GAMMA,
                descr="the discount factor"),
            agents_constants.CROSS_ENTROPY.POLICY_TYPE: HParam(
                value=PolicyType.MULTI_THRESHOLD, name=agents_constants.CROSS_ENTROPY.POLICY_TYPE,
                descr="policy type for the execution"),
            agents_constants.CROSS_ENTROPY.OBJECTIVE_TYPE: HParam(
                value=ObjectiveType.MAX, name=agents_constants.CROSS_ENTROPY.OBJECTIVE_TYPE,
                descr="Objective type")
        },
        player_type=PlayerType.DEFENDER, player_idx=0
    )
    agent = CrossEntropyAgent(emulation_env_config=emulation_env_config, simulation_env_config=simulation_env_config,
                              experiment_config=experiment_config)
    simulation_env_config.simulation_env_input_config.stopping_game_config.R = list(StoppingGameUtil.reward_tensor(
        R_INT=-1, R_COST=-2, R_SLA=0, R_ST=2, L=3))
    experiment_execution = agent.train()
    MetastoreFacade.save_experiment_execution(experiment_execution)
    for policy in experiment_execution.result.policies.values():
        if experiment_config.hparams[agents_constants.CROSS_ENTROPY.POLICY_TYPE].value == \
                PolicyType.MULTI_THRESHOLD:
            MetastoreFacade.save_multi_threshold_stopping_policy(multi_threshold_stopping_policy=policy)
        elif experiment_config.hparams[agents_constants.CROSS_ENTROPY.POLICY_TYPE].value \
                == PolicyType.LINEAR_THRESHOLD:
            MetastoreFacade.save_linear_threshold_stopping_policy(linear_threshold_stopping_policy=policy)
        else:
            raise ValueError("Policy type: "
                             f"{experiment_config.hparams[agents_constants.CROSS_ENTROPY.POLICY_TYPE].value} "
                             f"not recognized for cross entropy")
