import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.lp_cmdp.linear_programming_cmdp_agent import LinearProgrammingCMDPAgent
import csle_agents.constants.constants as agents_constants
from csle_tolerance.dao.intrusion_response_cmdp_config import IntrusionResponseCmdpConfig
from csle_tolerance.util.intrusion_response_cmdp_util import IntrusionResponseCmdpUtil

if __name__ == '__main__':
    simulation_name = "csle-tolerance-intrusion-response-cmdp-defender-001"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    s_max = 512
    p_u = 0.4
    p_a = 0.4
    p_c = 0.01
    epsilon_a = 0.2
    discount_factor = 1
    negate_costs = False
    initial_state = 10
    f = 3
    seed = 999
    simulation_env_name = "csle-tolerance-intrusion-response-cmdp-defender-001"
    transition_tensor = IntrusionResponseCmdpUtil.transition_tensor(
        states=IntrusionResponseCmdpUtil.state_space(s_max=s_max),
        actions=IntrusionResponseCmdpUtil.action_space(), p_a=p_a, p_c=p_c, p_u=p_u, s_max=s_max)
    cost_tensor = IntrusionResponseCmdpUtil.cost_tensor(
        states=IntrusionResponseCmdpUtil.state_space(s_max=s_max), negate=negate_costs)
    constraint_cost_tensor = IntrusionResponseCmdpUtil.constraint_cost_tensor(
        states=IntrusionResponseCmdpUtil.state_space(s_max=s_max), f=f)
    config = IntrusionResponseCmdpConfig(
        p_a=p_a, p_c=p_c, p_u=p_u, s_max=s_max, transition_tensor=transition_tensor, cost_tensor=cost_tensor,
        negate_costs=negate_costs, seed=seed, states=IntrusionResponseCmdpUtil.state_space(s_max=s_max),
        actions=IntrusionResponseCmdpUtil.action_space(), initial_state=initial_state,
        constraint_cost_tensor=constraint_cost_tensor, f=f, epsilon_a=epsilon_a,
        simulation_env_name=simulation_env_name,
        gym_env_name="csle-tolerance-intrusion-response-cmdp-v1", discount_factor=discount_factor
    )

    experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}fp_test",
        title="Linear programming for constrained MDPs",
        random_seeds=[399, 98912], agent_type=AgentType.LINEAR_PROGRAMMING_CMDP,
        log_every=1, br_log_every=5000,
        hparams={
            agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(value=1,
                                                            name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                                                            descr="number of iterations to evaluate theta"),
            agents_constants.COMMON.SAVE_EVERY: HParam(
                value=10000, name=agents_constants.COMMON.SAVE_EVERY, descr="how frequently to save the model"),
            agents_constants.COMMON.CONFIDENCE_INTERVAL: HParam(
                value=0.95, name=agents_constants.COMMON.CONFIDENCE_INTERVAL,
                descr="confidence interval"),
            agents_constants.COMMON.MAX_ENV_STEPS: HParam(
                value=500, name=agents_constants.COMMON.MAX_ENV_STEPS,
                descr="maximum number of steps in the environment (for envs with infinite horizon generally)"),
            agents_constants.COMMON.RUNNING_AVERAGE: HParam(
                value=40, name=agents_constants.COMMON.RUNNING_AVERAGE,
                descr="the number of samples to include when computing the running avg"),
            agents_constants.COMMON.GAMMA: HParam(
                value=config.discount_factor, name=agents_constants.COMMON.GAMMA,
                descr="the discount factor gamma"),
            agents_constants.LP_FOR_CMDPs.STATES: HParam(
                value=config.states, name=agents_constants.LP_FOR_CMDPs.STATES,
                descr="the state space"),
            agents_constants.LP_FOR_CMDPs.ACTIONS: HParam(
                value=config.actions, name=agents_constants.LP_FOR_CMDPs.ACTIONS,
                descr="the action space"),
            agents_constants.LP_FOR_CMDPs.COST_TENSOR: HParam(
                value=config.cost_tensor, name=agents_constants.LP_FOR_CMDPs.COST_TENSOR,
                descr="the cost tensor"),
            agents_constants.LP_FOR_CMDPs.TRANSITION_TENSOR: HParam(
                value=config.transition_tensor, name=agents_constants.LP_FOR_CMDPs.TRANSITION_TENSOR,
                descr="the transition tensor"),
            agents_constants.LP_FOR_CMDPs.CONSTRAINT_COST_TENSORS: HParam(
                value=[config.constraint_cost_tensor], name=agents_constants.LP_FOR_CMDPs.CONSTRAINT_COST_TENSORS,
                descr="the constraint cost tensor"),
            agents_constants.LP_FOR_CMDPs.CONSTRAINT_COST_THRESHOLDS: HParam(
                value=[config.epsilon_a],
                name=agents_constants.LP_FOR_CMDPs.CONSTRAINT_COST_THRESHOLDS,
                descr="the constraint cost thresholds")
        },
        player_type=PlayerType.DEFENDER, player_idx=1
    )
    import time

    start = time.time()
    agent = LinearProgrammingCMDPAgent(simulation_env_config=simulation_env_config,
                                       experiment_config=experiment_config, save_to_metastore=False)
    experiment_execution = agent.train()
    end = time.time()
    print(round(end - start, 4))
    # MetastoreFacade.save_experiment_execution(experiment_execution)
    # for policy in experiment_execution.result.policies.values():
    #     MetastoreFacade.save_tabular_policy(tabular_policy=policy)
