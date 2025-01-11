from typing import List
import numpy as np
import time
from gym_csle_cyborg.envs.cyborg_scenario_two_wrapper import CyborgScenarioTwoWrapper
from gym_csle_cyborg.dao.csle_cyborg_wrapper_config import CSLECyborgWrapperConfig
from csle_agents.agents.pomcp.pomcp import POMCP
from csle_agents.agents.pomcp.pomcp_acquisition_function_type import POMCPAcquisitionFunctionType
import csle_agents.constants.constants as agents_constants
from csle_common.logging.log import Logger
from gym_csle_cyborg.util.cyborg_env_util import CyborgEnvUtil
from gym_csle_cyborg.dao.red_agent_type import RedAgentType


def heuristic_value(o: List[List[int]]) -> float:
    """
    A heuristic value function

    :param o: the observation vector
    :return: the value
    """
    host_costs = CyborgEnvUtil.get_host_compromised_costs()
    val = 0
    for i in range(len(o)):
        if o[i][2] > 0:
            val += host_costs[i]
    return val


if __name__ == '__main__':
    config = CSLECyborgWrapperConfig(
        gym_env_name="csle-cyborg-scenario-two-wrapper-v1", maximum_steps=100, save_trace=False, scenario=2,
        reward_shaping=True, red_agent_type=RedAgentType.B_LINE_AGENT)
    eval_env = CyborgScenarioTwoWrapper(config=config)
    train_env = CyborgScenarioTwoWrapper(config=config)
    action_id_to_type_and_host, type_and_host_to_action_id \
        = CyborgEnvUtil.get_action_dicts(scenario=2, reduced_action_space=True, decoy_state=True,
                                         decoy_optimization=False)

    N = 5000
    rollout_policy = lambda x, deterministic: 35
    value_function = heuristic_value
    A = train_env.get_action_space()
    gamma = 0.99
    reinvigoration = False
    reinvigorated_particles_ratio = 0.0
    initial_particles = train_env.initial_particles
    planning_time = 3.75
    prune_action_space = False
    max_particles = 1000
    max_planning_depth = 50
    max_rollout_depth = 4
    c = 0.5
    c2 = 15000
    use_rollout_policy = False
    prior_weight = 5
    prior_confidence = 0
    acquisition_function_type = POMCPAcquisitionFunctionType.UCB
    log_steps_frequency = 1
    max_negative_samples = 20
    default_node_value = 0
    verbose = False
    eval_batch_size = 100
    max_env_steps = 100
    prune_size = 3
    start = time.time()

    # Run N episodes
    returns = []
    for i in range(N):
        done = False
        action_sequence = []
        _, info = eval_env.reset()
        s = info[agents_constants.COMMON.STATE]
        train_env.reset()
        pomcp = POMCP(A=A, gamma=gamma, env=train_env, c=c, initial_particles=initial_particles,
                      planning_time=planning_time, max_particles=max_particles, rollout_policy=rollout_policy,
                      value_function=value_function, reinvigoration=reinvigoration, verbose=verbose,
                      default_node_value=default_node_value, prior_weight=prior_weight,
                      acquisition_function_type=acquisition_function_type, c2=c2,
                      use_rollout_policy=use_rollout_policy, prior_confidence=prior_confidence,
                      reinvigorated_particles_ratio=reinvigorated_particles_ratio,
                      prune_action_space=prune_action_space, prune_size=prune_size)
        R = 0
        t = 1

        # Run episode
        while not done and t <= max_env_steps:
            rollout_depth = max_rollout_depth
            planning_depth = max_planning_depth
            pomcp.solve(max_rollout_depth=rollout_depth, max_planning_depth=planning_depth, t=t)
            action = pomcp.get_action()
            o, _, done, _, info = eval_env.step(action)
            r = info[agents_constants.COMMON.REWARD]
            action_sequence.append(action)
            s_prime = info[agents_constants.COMMON.STATE]
            obs_id = info[agents_constants.COMMON.OBSERVATION]
            pomcp.update_tree_with_new_samples(action_sequence=action_sequence, observation=obs_id, t=t)
            R += r
            t += 1
            if t % log_steps_frequency == 0:
                Logger.__call__().get_logger().info(f"[POMCP] t: {t}, a: {action_id_to_type_and_host[action]}, r: {r}, "
                                                    f"action sequence: {action_sequence}, R: {round(R, 2)}")

        # Logging
        returns.append(R)
        progress = round((i + 1) / N, 2)
        time_elapsed_minutes = round((time.time() - start) / 60, 3)
        Logger.__call__().get_logger().info(
            f"[POMCP] episode: {i}, J:{R}, "
            f"J_avg: {np.mean(returns)}, "
            f"progress: {round(progress * 100, 2)}%, "
            f"runtime: {time_elapsed_minutes} min")
