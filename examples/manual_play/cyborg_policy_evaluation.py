import numpy as np
from csle_common.metastore.metastore_facade import MetastoreFacade
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender

if __name__ == '__main__':
    ppo_policy = MetastoreFacade.get_ppo_policy(id=18)
    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=True, decoy_state=True,
        scanned_state=True, decoy_optimization=False)
    csle_cyborg_env = CyborgScenarioTwoDefender(config=config)

    num_evaluations = 100
    returns = []
    print("Starting policy evaluation")
    for i in range(num_evaluations):
        done = False
        o, _ = csle_cyborg_env.reset()
        R = 0
        while not done:
            a = ppo_policy.action(o=o)
            o, r, done, _, info = csle_cyborg_env.step(a)
            R += r
        returns.append(R)
        print(f"{i}/{num_evaluations}, avg R: {np.mean(returns)}")
