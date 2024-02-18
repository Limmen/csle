from typing import List, Dict, Tuple
import numpy as np
import torch
import random
import json
import io
from gym_csle_cyborg.util.cyborg_env_util import CyborgEnvUtil
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender
from gym_csle_cyborg.envs.cyborg_scenario_two_wrapper import CyborgScenarioTwoWrapper
from gym_csle_cyborg.dao.csle_cyborg_wrapper_config import CSLECyborgWrapperConfig
from csle_agents.agents.pomcp.pomcp import POMCP
from csle_agents.agents.pomcp.pomcp_acquisition_function_type import POMCPAcquisitionFunctionType
import csle_agents.constants.constants as agents_constants
from csle_common.dao.training.ppo_policy import PPOPolicy
from csle_common.dao.training.player_type import PlayerType
from csle_common.logging.log import Logger
from gym_csle_cyborg.dao.blue_agent_action_type import BlueAgentActionType
from gym_csle_cyborg.dao.cyborg_wrapper_state import CyborgWrapperState
import gym_csle_cyborg.constants.constants as env_constants

def heuristic_value(o: List[int]):
    host_costs = CyborgEnvUtil.get_host_compromised_costs()
    val = 0
    for i in range(len(o)):
        if o[i][2] > 0:
            val += host_costs[i]
        # if o[i][2] == 1:
        #     val -= host_costs[i]*1
        # if o[i][2] == 2 or o[i][2] == 3:
        #     val -= host_costs[hosts[i]]*2
        # if o[0] == 0:
        #     val += 1
        # if o[i][1] > 0 and o[i][3] > 0:
        #     val += host_values[hosts[i]]
    return val

# def base_policy(o: List[int]):
#     host_values = CyborgEnvUtil.get_cyborg_host_values()
#     a = 31
#     known_max_values = -1
#     for i in range(len(o)):
#         if i[1] == 2:
#             last_scanned = i
#     if last


if __name__ == '__main__':
    # ppo_policy = PPOPolicy(model=None, simulation_name="",
    #                        save_path="/tmp/csle/ppo_test_1707078811.4761195/ppo_model1630_1707115775.1994205.zip",
    #                        player_type=PlayerType.DEFENDER, actions=[], states=[], experiment_config=None, avg_R=0)
    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.MEANDER_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=True, decoy_state=True,
        scanned_state=True, decoy_optimization=False, cache_visited_states=False)
    eval_env = CyborgScenarioTwoDefender(config=config)
    config = CSLECyborgWrapperConfig(maximum_steps=100, gym_env_name="",
                                     save_trace=False, reward_shaping=False, scenario=2,
                                     red_agent_type=RedAgentType.MEANDER_AGENT)
    train_env = CyborgScenarioTwoWrapper(config=config)

    num_evaluations = 100
    max_horizon = 100
    returns = []
    seed = 80808081
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    A = train_env.get_action_space()
    # gamma = 0.75
    gamma = 0.99
    c = 0.5
    print("Starting policy evaluation")
    for i in range(num_evaluations):
        _, info = eval_env.reset()
        s = info[agents_constants.COMMON.STATE]
        train_env.reset()
        initial_particles = train_env.initial_particles
        max_particles = 1000
        planning_time = 15
        # value_function = lambda x: 0
        value_function = heuristic_value
        reinvigoration = False
        rollout_policy = None
        # rollout_policy = ppo_policy
        verbose = False
        default_node_value = 0
        prior_weight = 1
        acquisition_function_type = POMCPAcquisitionFunctionType.UCB
        use_rollout_policy = False
        reinvigorated_particles_ratio = 0.0
        prune_action_space = False
        prune_size = 3
        prior_confidence = 0
        pomcp = POMCP(A=A, gamma=gamma, env=train_env, c=c, initial_particles=initial_particles,
                      planning_time=planning_time, max_particles=max_particles, rollout_policy=rollout_policy,
                      value_function=value_function, reinvigoration=reinvigoration, verbose=verbose,
                      default_node_value=default_node_value, prior_weight=prior_weight,
                      acquisition_function_type=acquisition_function_type, c2=1500,
                      use_rollout_policy=use_rollout_policy, prior_confidence=prior_confidence,
                      reinvigorated_particles_ratio=reinvigorated_particles_ratio,
                      prune_action_space=prune_action_space, prune_size=prune_size)
        # rollout_depth = 4
        rollout_depth = 25
        # rollout_depth = 50
        # rollout_depth = 20
        planning_depth = 50
        R = 0
        t = 0
        action_sequence = []
        hosts = list(range(len(train_env.hosts)))
        while t < max_horizon:
            pomcp.solve(max_rollout_depth=rollout_depth, max_planning_depth=planning_depth, t=t)
            action = pomcp.get_action()
            # if len(action_sequence) > 1:
            #     if action != 28 and action_sequence[-1] == 1:
            #         action = 28
            #     if action != 27 and action_sequence[-1] == 0:
            #         action = 27
            o, r, done, _, info = eval_env.step(action)
            action_sequence.append(action)
            s_prime = info[agents_constants.COMMON.STATE]
            obs_id = info[agents_constants.COMMON.OBSERVATION]
            print(eval_env.get_true_table())
            print(eval_env.get_table())
            print(eval_env.get_actions_table())
            print(action)
            print(CyborgEnvUtil.state_id_to_state_vector(state_id=s_prime))
            print(CyborgEnvUtil.state_id_to_state_vector(state_id=obs_id, observation=True))
            print(pomcp.tree.root.sample_state())
            print(pomcp.tree.root.sample_state())
            print(pomcp.tree.root.sample_state())
            target = 0
            if action_sequence[-1] == 1 or action_sequence[-1] == 0:
                target = 6
            pomcp.update_tree_with_new_samples(action_sequence=action_sequence, observation=obs_id, t=t+1)
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
        results["planning_time"] = planning_time
        results["c"] = c
        results["gamma"] = gamma
        results["rollout_depth"] = rollout_depth
        results["planning_depth"] = planning_depth
        results["max_particles"] = max_particles
        results["default_node_value"] = default_node_value
        results["value_function"] = "heuristic"
        results["rollout_policy"] = "-"
        results["use_rollout_policy"] = int(use_rollout_policy)
        results["acquisition"] = acquisition_function_type.value
        # json_str = json.dumps(results, indent=4, sort_keys=True)
        # with io.open(f"/Users/kim/p_orig_0_47s_T_50_seed_{seed}.json", 'w', encoding='utf-8') as f:
        #     f.write(json_str)
