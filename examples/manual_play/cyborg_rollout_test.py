import numpy as np
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.ppo_policy import PPOPolicy
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.dao.blue_agent_action_type import BlueAgentActionType
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender


def rollout(env: CyborgScenarioTwoDefender, policy: PPOPolicy, time_horizon: int, samples: int, first_a: int) -> float:
    """
    Performs rollout

    :param env: the cyborg environment
    :param policy: the base policy
    :param time_horizon: the time horizon
    :param samples: the number of samples
    :param first_a: the first action
    :return: the average return
    """
    returns = []
    for i in range(samples):
        done = False
        o, _ = env.reset()
        R = 0
        t = 0
        while not done and t < time_horizon:
            if t == 0:
                a = first_a
            else:
                a = policy.action(o=o)
            o, r, done, _, info = env.step(a)
            R += r
            t += 1
        returns.append(R + policy.value(o))
    return float(np.mean(returns))


if __name__ == '__main__':
    ppo_policy = MetastoreFacade.get_ppo_policy(id=18)
    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=True, decoy_state=True,
        scanned_state=True, decoy_optimization=False)
    csle_cyborg_env = CyborgScenarioTwoDefender(config=config)
    time_horizon = 25
    samples = 500
    returns = []
    best_action = None
    best_val = -100
    for k, v in csle_cyborg_env.action_id_to_type_and_host.items():
        action_id = k
        type, host = v
        avg_return = rollout(env=csle_cyborg_env, policy=ppo_policy, time_horizon=time_horizon, samples=samples,
                             first_a=action_id)
        returns.append(avg_return)
        if avg_return > best_val:
            best_val = avg_return
            best_action = f"{BlueAgentActionType(type).name}, {host}"
        print(
            f"action: {BlueAgentActionType(type).name}, {host}, avg_return: {avg_return}, best_action: {best_action}, "
            f"best_val: {best_val}")
