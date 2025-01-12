import csle_agents.constants.constants as agents_constants
import csle_common.constants.constants as constants
from csle_agents.agents.mcs.mcs_agent import MCSAgent
from csle_agents.common.objective_type import ObjectiveType
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.training.policy_type import PolicyType
from csle_common.metastore.metastore_facade import MetastoreFacade

if __name__ == "__main__":
    emulation_name = "csle-level1-070"
    emulation_env_config = MetastoreFacade.get_emulation_by_name(emulation_name)
    if emulation_env_config is None:
        raise ValueError(f"Could not find an emulation environment with the name: {emulation_name}")
    simulation_name = "csle-stopping-pomdp-defender-002"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}particle_swarm_test",
        title="Multilevel Coordinate Search",
        random_seeds=[399, 98912],
        agent_type=AgentType.MCS,
        log_every=1,
        hparams={
            agents_constants.MCS.STEP: HParam(value=1000, name=agents_constants.MCS.STEP, descr="step"),
            agents_constants.MCS.STEP1: HParam(value=10000, name=agents_constants.MCS.STEP1, descr="step1"),
            agents_constants.MCS.U: HParam(value=[-20, -20, -20], name=agents_constants.MCS.U,
                                           descr="initial lower corner"),
            agents_constants.MCS.LOCAL: HParam(value=50, name=agents_constants.MCS.LOCAL,
                                               descr="local value stating to which degree to perform local searches"),
            agents_constants.MCS.V: HParam(value=[20, 20, 20], name=agents_constants.MCS.V,
                                           descr="initial upper corner"),
            agents_constants.MCS.STOPPING_ACTIONS: HParam(
                value=3, name=agents_constants.MCS.L, descr="no. of stopping actions"),
            agents_constants.COMMON.MAX_ENV_STEPS: HParam(
                value=500, name=agents_constants.COMMON.MAX_ENV_STEPS,
                descr="maximum number of steps in the environment (for envs with infinite horizon generally)"),
            agents_constants.MCS.IINIT: HParam(
                value=0, name=agents_constants.MCS.IINIT, descr="simple initialization list"),
            agents_constants.MCS.GAMMA: HParam(
                value=2.220446049250313e-16, name=agents_constants.MCS.GAMMA, descr="MCS gamma value"),
            agents_constants.MCS.EPSILON: HParam(
                value=2.220446049250313e-16, name=agents_constants.MCS.EPSILON, descr="MCS epsilon value"),
            agents_constants.MCS.M: HParam(
                value=1, name=agents_constants.MCS.M, descr="m value"),
            agents_constants.MCS.PRT: HParam(
                value=1, name=agents_constants.MCS.PRT, descr="print level"),
            agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(
                value=10, name=agents_constants.COMMON.EVAL_BATCH_SIZE, descr="number of iterations to evaluate theta"),
            agents_constants.COMMON.SAVE_EVERY: HParam(
                value=1000, name=agents_constants.COMMON.SAVE_EVERY, descr="how frequently to save the model"),
            agents_constants.COMMON.CONFIDENCE_INTERVAL: HParam(
                value=0.95, name=agents_constants.COMMON.CONFIDENCE_INTERVAL, descr="confidence interval"),
            agents_constants.COMMON.RUNNING_AVERAGE: HParam(
                value=100, name=agents_constants.COMMON.RUNNING_AVERAGE,
                descr="the number of samples to include when computing the running avg"),
            agents_constants.COMMON.GAMMA: HParam(
                value=0.99, name=agents_constants.COMMON.GAMMA, descr="the discount factor"),
            agents_constants.MCS.POLICY_TYPE: HParam(
                value=PolicyType.MULTI_THRESHOLD, name=agents_constants.PARTICLE_SWARM.POLICY_TYPE,
                descr="policy type for the execution"),
            agents_constants.MCS.OBJECTIVE_TYPE: HParam(
                value=ObjectiveType.MAX, name=agents_constants.PARTICLE_SWARM.OBJECTIVE_TYPE, descr="Objective type"),
        },
        player_type=PlayerType.DEFENDER, player_idx=0,
    )
    agent = MCSAgent(
        simulation_env_config=simulation_env_config, emulation_env_config=emulation_env_config,
        experiment_config=experiment_config, save_to_metastore=False)
    experiment_execution = agent.train()
    # MetastoreFacade.save_experiment_execution(experiment_execution)
    # for policy in experiment_execution.result.policies.values():
    #     if experiment_config.hparams[agents_constants.PARTICLE_SWARM.POLICY_TYPE].value == PolicyType.MULTI_THRESHOLD:
    #         MetastoreFacade.save_multi_threshold_stopping_policy(multi_threshold_stopping_policy=policy)
    #     elif experiment_config.hparams[agents_constants.PARTICLE_SWARM.POLICY_TYPE].value \
    #             == PolicyType.LINEAR_THRESHOLD:
    #         MetastoreFacade.save_linear_threshold_stopping_policy(linear_threshold_stopping_policy=policy)
    #     else:
    #         raise ValueError("Policy type: "
    #                          f"{experiment_config.hparams[agents_constants.PARTICLE_SWARM.POLICY_TYPE].value} "
    #                          f"not recognized for MCS")
