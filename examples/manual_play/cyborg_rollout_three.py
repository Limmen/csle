import numpy as np
from csle_common.metastore.metastore_facade import MetastoreFacade
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender
import csle_agents.constants.constants as constants
from csle_agents.agents.pomcp.pomcp_util import POMCPUtil
import math

if __name__ == '__main__':
    ppo_policy = MetastoreFacade.get_ppo_policy(id=15)
    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=True, decoy_state=True,
        scanned_state=True, decoy_optimization=False, cache_visited_states=True)
    csle_cyborg_env = CyborgScenarioTwoDefender(config=config)
    #324519791598466012163466353442816
    # POMCPUtil.trajectory_simulation_particles(o=324519791598466012163474943377408,
    #                                           env=csle_cyborg_env, action_sequence=[31, 34, 28], num_particles=100)
    from gym_csle_cyborg.util.cyborg_env_util import CyborgEnvUtil
    vec = CyborgEnvUtil.state_id_to_state_vector(state_id=14507109835375640432425280, observation=False)
    print(vec)
    vec = CyborgEnvUtil.state_id_to_state_vector(state_id=16018267109893926900808000, observation=False)
    print(vec)

    print(csle_cyborg_env.cyborg_hostnames)
    #324519791598466012163474943377408
    # 324518553658426726783181790642176


    # o, _ = csle_cyborg_env.reset()
    # print(ppo_policy.probability(o=o, a=4))
    # import torch
    # actions = list(csle_cyborg_env.action_id_to_type_and_host.keys())
    # dist = ppo_policy.model.policy.get_distribution(obs=torch.tensor([o]).to(ppo_policy.model.device)).log_prob(torch.tensor(actions).to(ppo_policy.model.device)).cpu().detach().numpy()
    # import math
    # dist = list(map(lambda x: math.exp(x), dist))
    # print(dist)
    # print(max(dist))
    # print(actions[np.argmax(dist)])
    # print(csle_cyborg_env.action_id_to_type_and_host[actions[np.argmax(dist)]])
    # num_evaluations = 10000

    # max_horizon = 25
    # returns = []
    # print("Starting policy evaluation")
    # import time
    #
    # start = time.time()
    # # print(list(csle_cyborg_env.visited_cyborg_states.keys()))
    # avg_return = csle_cyborg_env.parallel_rollout(policy_id=5, num_processes=8, num_evals_per_process=13,
    #                                               max_horizon=25, state_id=21474836480)
    # print(avg_return)
    # print(time.time() - start)
    # history_visit_count = 10
    # c=20
    # for action_visit_count in range(1, 100):
    #     print(np.sqrt(np.log(history_visit_count) / action_visit_count)*c)
