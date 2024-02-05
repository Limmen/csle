import numpy as np
import torch
import random
import json
import io
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.ppo_policy import PPOPolicy
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender
from gym_csle_cyborg.envs.cyborg_scenario_two_wrapper import CyborgScenarioTwoWrapper
from gym_csle_cyborg.dao.csle_cyborg_wrapper_config import CSLECyborgWrapperConfig
from csle_agents.agents.pomcp.pomcp import POMCP
from csle_agents.agents.pomcp.pomcp_acquisition_function_type import POMCPAcquisitionFunctionType
import csle_agents.constants.constants as agents_constants
from csle_common.logging.log import Logger


if __name__ == '__main__':
    # ppo_policy = PPOPolicy(model=None, simulation_name="", save_path="")
    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=True, decoy_state=True,
        scanned_state=True, decoy_optimization=False, cache_visited_states=False)
    eval_env = CyborgScenarioTwoDefender(config=config)
    config = CSLECyborgWrapperConfig(maximum_steps=100, gym_env_name="",
                                     save_trace=False, reward_shaping=False, scenario=2)
    train_env = CyborgScenarioTwoWrapper(config=config)

    num_evaluations = 10
    max_horizon = 100
    returns = []
    seed = 215125
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    A = train_env.get_action_space()
    gamma = 0.75
    c = 1
    print("Starting policy evaluation")
    for i in range(num_evaluations):
        _, info = eval_env.reset()
        s = info[agents_constants.COMMON.STATE]
        train_env.reset()
        initial_particles = train_env.initial_particles
        max_particles = 1000
        planning_time = 30
        value_function = lambda x: 0
        reinvigoration = False
        rollout_policy= False
        verbose = False
        default_node_value = 0
        prior_weight= 1
        acquisition_function_type = POMCPAcquisitionFunctionType.UCB
        use_rollout_policy = False
        reinvigorated_particles_ratio = False
        prune_action_space = False
        prune_size= 3
        prior_confidence = 0
        pomcp = POMCP(A=A, gamma=gamma, env=train_env, c=c, initial_particles=initial_particles,
                      planning_time=planning_time, max_particles=max_particles, rollout_policy=rollout_policy,
                      value_function=value_function, reinvigoration=reinvigoration, verbose=verbose,
                      default_node_value=default_node_value, prior_weight=prior_weight,
                      acquisition_function_type=acquisition_function_type, c2=1500,
                      use_rollout_policy=use_rollout_policy, prior_confidence=prior_confidence,
                      reinvigorated_particles_ratio=reinvigorated_particles_ratio,
                      prune_action_space=prune_action_space, prune_size=prune_size)
        rollout_depth = 4
        planning_depth = 100
        R = 0
        t = 0
        action_sequence = []
        while t < max_horizon:
            pomcp.solve(max_rollout_depth=rollout_depth, max_planning_depth=planning_depth)
            action = pomcp.get_action()
            o, r, done, _, info = eval_env.step(action)
            action_sequence.append(action)
            s_prime = info[agents_constants.COMMON.STATE]
            obs_id = info[agents_constants.COMMON.OBSERVATION]
            pomcp.update_tree_with_new_samples(action_sequence=action_sequence, observation=obs_id)
            print(eval_env.get_true_table())
            print(eval_env.get_table())
            R += r
            t += 1
            Logger.__call__().get_logger().info(f"[POMCP] t: {t}, a: {action}, r: {r}, o: {obs_id}, "
                                                f"s_prime: {s_prime},"
                                                f", action sequence: {action_sequence}, R: {R}")
        returns.append(R)
        print(f"{i}/{num_evaluations}, avg R: {np.mean(returns)}, R: {R}")
        results = {}
        results["seed"] = seed
        results["training_time"] = 0
        results["returns"] = returns
        results["planning_time"] = 30
        json_str = json.dumps(results, indent=4, sort_keys=True)
        with io.open(f"/Users/kim/pomcp_{0}_30s.json", 'w', encoding='utf-8') as f:
            f.write(json_str)
