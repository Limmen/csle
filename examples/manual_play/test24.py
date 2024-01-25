import random
import numpy as np
import torch
import json
import io
from csle_common.metastore.metastore_facade import MetastoreFacade
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgEnvUtil
import csle_agents.constants.constants as agents_constants
from csle_common.logging.log import Logger
from csle_agents.agents.pomcp.pomcp import POMCP


def my_value(o: int):
    obs_vector = CyborgEnvUtil.state_id_to_state_vector(state_id=o, observation=True)
    hosts = ['Defender', 'Enterprise0', 'Enterprise1', 'Enterprise2', 'Op_Host0', 'Op_Host1', 'Op_Host2',
             'Op_Server0', 'User0', 'User1', 'User2', 'User3', 'User4']
    host_values = [2,2,2,3,4,4,4,5,0,1,1,1,1]
    value = 0
    for i in range(len(hosts)):
        value -= obs_vector[i][2]*2*host_values[i]
        value += obs_vector[i][3]*0.1
    return value


if __name__ == '__main__':
    import io
    with io.open(f"/home/kim/particle_model.json", 'r', encoding='utf-8') as f:
        json_str = f.read()
        particle_model = json.loads(json_str)
    particle_model_1 = {}
    for k, v in particle_model.items():
        v_2 = [int(x) for x in v]
        particle_model_1[int(k)] = v_2
    particle_model = particle_model_1
    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=True, decoy_state=True,
        scanned_state=True, decoy_optimization=False, cache_visited_states=True)
    csle_cyborg_env = CyborgScenarioTwoDefender(config=config)
    N = 1000
    gamma = 1
    planning_time = 15
    ppo_policy_id = 98
    rollout_policy = MetastoreFacade.get_ppo_policy(id=ppo_policy_id)
    # value_function = rollout_policy.value
    value_function = test_value
    default_node_value = 2000
    max_particles = 30
    parallel_rollout = False
    num_evals_per_process = 1
    prior_weight = 1
    reinvigoration = False
    verbose = True
    num_processes = 1
    b1 = csle_cyborg_env.initial_belief
    c = 300
    A = csle_cyborg_env.get_action_space()
    max_env_steps = 100
    max_negative_samples = 20
    max_rollout_depth = 5
    max_planning_depth = 50
    ppo_returns = []
    pomcp_returns = []
    data = {}
    data["ppo_returns"] = []
    data["pomcp_returns"] = []
    seed = 399
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.backends.cudnn.deterministic = True

    for i in range(N):
        done = False
        action_sequence = []
        eval_env = CyborgScenarioTwoDefender(config=config)
        train_env = CyborgScenarioTwoDefender(config=config)
        base_policy_env = CyborgScenarioTwoDefender(config=config)

        _, info = eval_env.reset()
        s = info[agents_constants.COMMON.STATE]
        o, _ = train_env.reset()
        o2, _ = base_policy_env.reset()
        belief = b1.copy()
        pomcp = POMCP(A=A, gamma=gamma, env=train_env, c=c, initial_belief=belief,
                      planning_time=planning_time, max_particles=max_particles, rollout_policy=rollout_policy,
                      value_function=value_function, reinvigoration=reinvigoration, verbose=verbose,
                      default_node_value=default_node_value, parallel_rollout=parallel_rollout,
                      num_parallel_processes=num_processes, num_evals_per_process=num_evals_per_process,
                      prior_weight=prior_weight, particle_model = particle_model)
        R = 0
        R2 = 0
        t = 1
        Logger.__call__().get_logger().info(f"[POMCP] t: {t}, b: {belief}, s: {s}")

        while t <= max_env_steps:
            pomcp.solve(max_rollout_depth=max_rollout_depth, max_planning_depth=max_planning_depth)
            action = pomcp.get_action()
            rollout_action = rollout_policy.action(o=o2)
            o, r, done, _, info = eval_env.step(action)
            o2, r2, _, _, _ = base_policy_env.step(rollout_action)
            action_sequence.append(action)
            s_prime = info[agents_constants.COMMON.STATE]
            obs_id = info[agents_constants.COMMON.OBSERVATION]
            belief = pomcp.update_tree_with_new_samples(action_sequence=action_sequence, observation=obs_id,
                                                        max_negative_samples=max_negative_samples,
                                                        observation_vector=o)
            R += r
            R2 += r2
            t += 1
            # b = list(map(lambda x: belief[x], random.sample(list(belief.keys()), min(10, len(belief.keys())))))
            b_keys = list(filter(lambda x: belief[x] > 0, list(belief.keys())))
            b = [(x, belief[x]) for x in b_keys]
            Logger.__call__().get_logger().info(f"[POMCP] t: {t}, a: {action}, r: {r}, o: {obs_id}, "
                                                f"s_prime: {s_prime}, b: {b}, rollout action: {rollout_action}"
                                                f", action sequence: {action_sequence}")
            # Logger.__call__().get_logger().info("Actual state:")
            # Logger.__call__().get_logger().info(eval_env.get_true_table())
        pomcp_returns.append(float(R))
        ppo_returns.append(float(R2))
        data["ppo_returns"] = list(ppo_returns)
        data["pomcp_returns"] = list(pomcp_returns)
        Logger.__call__().get_logger().info(f"avg ppo returns: {np.mean(ppo_returns)}, "
                                            f"avg pomcp_returns: {np.mean(pomcp_returns)}")
        # json_str = json.dumps(data, indent=4, sort_keys=True)
        # with io.open(f"/home/kim/pomcp_eval_base_policy_id_{ppo_policy_id}_seed_{seed}.json", 'w', encoding='utf-8') as f:
        #     f.write(json_str)

