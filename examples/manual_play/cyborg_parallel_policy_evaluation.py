from csle_common.metastore.metastore_facade import MetastoreFacade
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender

if __name__ == '__main__':
    ppo_policy = MetastoreFacade.get_ppo_policy(id=18)
    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=True, decoy_state=True,
        scanned_state=True, decoy_optimization=False, cache_visited_states=True)
    csle_cyborg_env = CyborgScenarioTwoDefender(config=config)
    csle_cyborg_env.reset()
    num_evaluations = 10000
    max_horizon = 25
    returns = []
    print("Starting policy evaluation")
    import time

    start = time.time()
    print(list(csle_cyborg_env.visited_cyborg_states.keys()))
    avg_return = csle_cyborg_env.parallel_rollout(policy_id=1, num_processes=1, num_evals_per_process=100,
                                                  max_horizon=25, state_id=21474836480)
    print(avg_return)
    print(time.time() - start)
