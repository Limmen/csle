import numpy as np
import csle_common.constants.constants as constants
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.training.tabular_policy import TabularPolicy
from csle_common.dao.simulation_config.action import Action
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil
from csle_agents.agents.pi.pi_agent import PIAgent
from csle_common.dao.training.experiment_config import ExperimentConfig
import csle_agents.constants.constants as agents_constants
from csle_common.dao.training.hparam import HParam
from gym_csle_stopping_game.envs.stopping_game_pomdp_defender_env import StoppingGamePomdpDefenderEnv
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig
from gym_csle_stopping_game.dao.stopping_game_defender_pomdp_config import StoppingGameDefenderPomdpConfig

if __name__ == '__main__':
    simulation_name = "csle-stopping-pomdp-defender-002"
    attacker_actions = [Action(id=0, descr="-"), Action(id=1, descr="")]
    attacker_strategy = TabularPolicy(
        actions=attacker_actions,
        player_type=PlayerType.ATTACKER, lookup_table=[
            [0.9, 0.1],
            [1, 0],
            [0.5, 0.5]
        ], agent_type=AgentType.POLICY_ITERATION, avg_R=-1, simulation_name=simulation_name)
    R_INT = -1
    R_COST = -1
    R_SLA = 0
    R_ST = 1
    L = 1
    gamma = 0.99
    S = StoppingGameUtil.state_space()
    A = StoppingGameUtil.defender_actions()
    T = StoppingGameUtil.transition_tensor(L=1)
    R = StoppingGameUtil.reward_tensor(R_INT=R_INT, R_COST=R_COST, R_SLA=R_SLA, R_ST=R_ST, L=L)
    num_observations = 10
    O = StoppingGameUtil.observation_space(n=num_observations)
    Z = StoppingGameUtil.observation_tensor(len(range(0, num_observations)))

    config = StoppingGameConfig(env_name="stopping pomdp", T=T, O=O, Z=Z, R=R, S=S, A1=A, A2=A, L=1, R_INT=R_INT,
                                R_COST=R_COST, R_SLA=R_SLA, R_ST=R_ST, b1=StoppingGameUtil.b1(), save_dir="",
                                checkpoint_traces_freq=99999, gamma=0.99, compute_beliefs=True, save_trace=False)
    pomdp_config = StoppingGameDefenderPomdpConfig(
        env_name="stopping_pomdp", stopping_game_config=config, attacker_strategy=attacker_strategy)
    env = StoppingGamePomdpDefenderEnv(config=pomdp_config)

    T = StoppingGameUtil.reduce_T_attacker(T, attacker_strategy)
    R = StoppingGameUtil.reduce_R_attacker(R, attacker_strategy)
    Z = StoppingGameUtil.reduce_Z_attacker(Z, attacker_strategy)
    aggregation_resolution = 10
    aggregate_belief_space, A, belief_T, belief_R = StoppingGameUtil.aggregate_belief_mdp_defender(
        aggregation_resolution=aggregation_resolution, T=T, R=R, Z=Z, S=S, A=A, O=O)
    initial_policy = []
    for i in range(len(aggregate_belief_space)):
        initial_policy.append([1, 0])

    experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}pi_test",
        title="Policy iteration computation",
        random_seeds=[399], agent_type=AgentType.POLICY_ITERATION,
        log_every=1,
        hparams={
            agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(value=100,
                                                            name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                                                            descr="number of iterations to evaluate"),
            agents_constants.COMMON.EVAL_EVERY: HParam(value=1,
                                                       name=agents_constants.COMMON.EVAL_EVERY,
                                                       descr="how frequently to run evaluation"),
            agents_constants.COMMON.SAVE_EVERY: HParam(value=1000, name=agents_constants.COMMON.SAVE_EVERY,
                                                       descr="how frequently to save the model"),
            agents_constants.COMMON.CONFIDENCE_INTERVAL: HParam(
                value=0.95, name=agents_constants.COMMON.CONFIDENCE_INTERVAL,
                descr="confidence interval"),
            agents_constants.COMMON.RUNNING_AVERAGE: HParam(
                value=100, name=agents_constants.COMMON.RUNNING_AVERAGE,
                descr="the number of samples to include when computing the running avg"),
            agents_constants.COMMON.GAMMA: HParam(
                value=gamma, name=agents_constants.COMMON.GAMMA,
                descr="the discount factor"),
            agents_constants.PI.TRANSITION_TENSOR: HParam(
                value=list(T.tolist()), name=agents_constants.PI.TRANSITION_TENSOR,
                descr="the transition tensor"),
            agents_constants.PI.REWARD_TENSOR: HParam(
                value=list(R.tolist()), name=agents_constants.PI.REWARD_TENSOR,
                descr="the reward tensor"),
            agents_constants.PI.NUM_STATES: HParam(
                value=len(aggregate_belief_space), name=agents_constants.PI.NUM_STATES,
                descr="the number of states"),
            agents_constants.PI.NUM_ACTIONS: HParam(
                value=len(A), name=agents_constants.PI.NUM_ACTIONS,
                descr="the number of actions"),
            agents_constants.PI.N: HParam(
                value=100, name=agents_constants.PI.N,
                descr="the number of iterations"),
            agents_constants.PI.INITIAL_POLICY: HParam(
                value=initial_policy, name=agents_constants.PI.INITIAL_POLICY,
                descr="the initial policy")
        },
        player_type=PlayerType.ATTACKER, player_idx=1
    )

    initial_eval_state = list(aggregate_belief_space.tolist()).index([1, 0, 0])
    agent = PIAgent(simulation_env_config=None, experiment_config=experiment_config, create_log_dir=False, env=env,
                    env_eval=False, max_eval_length=50, initial_eval_state=initial_eval_state)
    policy, v, avg_returns, running_avg_returns = (
        agent.pi(P=belief_T, policy=np.array(initial_policy), N=100, gamma=gamma, R=belief_R,
                 num_states=len(aggregate_belief_space),
                 num_actions=len(A)))
    for i in range(len(aggregate_belief_space)):
        print(f"belief: {aggregate_belief_space[i]}, action: {np.argmax(policy[i])}")

    print(f"avg reward: {v[initial_eval_state]}")
