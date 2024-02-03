import numpy as np
import torch
import random
from csle_common.metastore.metastore_facade import MetastoreFacade
from gym_csle_cyborg.envs.cyborg_scenario_two_wrapper import CyborgScenarioTwoWrapper
from gym_csle_cyborg.dao.csle_cyborg_wrapper_config import CSLECyborgWrapperConfig
from gym_csle_cyborg.dao.cyborg_wrapper_state import CyborgWrapperState
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender
from gym_csle_cyborg.util.cyborg_env_util import CyborgEnvUtil
import gym_csle_cyborg.constants.constants as env_constants
from gym_csle_cyborg.dao.blue_agent_action_type import BlueAgentActionType

def is_obs_feasible(env, action_sequence, obs, state_sequence):
    i = 0
    match = False
    while i < 50000 and not match:
        o, _ = env.reset()
        t = 0
        oid = 0
        while t < len(action_sequence):
            a = action_sequence[t]
            o, r, done, _, info = env.step(a)
            # state_id = info[env_constants.ENV_METRICS.STATE]
            oid = info[env_constants.ENV_METRICS.OBSERVATION]
            t += 1
        if oid == obs:
            match = True
        i += 1
    if not match:
        obs_vec = CyborgEnvUtil.state_id_to_state_vector(state_id=obs, observation=True)
        print(f"Could not find match for {obs_vec}, \n actionsequence: {action_sequence} \n state sequence: {state_sequence}")

if __name__ == '__main__':
    ppo_policy = MetastoreFacade.get_ppo_policy(id=58)
    config = CSLECyborgWrapperConfig(maximum_steps=100, gym_env_name="",
                                     save_trace=False, reward_shaping=False)
    env = CyborgScenarioTwoWrapper(config=config)
    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=True, decoy_state=True,
        scanned_state=True, decoy_optimization=False, cache_visited_states=False)
    csle_cyborg_env = CyborgScenarioTwoDefender(config=config)
    num_evaluations = 10000
    max_horizon = 100
    returns = []
    seed = 215125
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    A = env.get_action_space()
    print("Starting policy evaluation")
    for i in range(num_evaluations):
        o, _ = csle_cyborg_env.reset()
        R = 0
        t = 0
        action_sequence = []
        state_sequence = []
        while t < max_horizon:
            a = np.random.choice(A)
            o, r, done, _, info = csle_cyborg_env.step(a)
            state_id = info[env_constants.ENV_METRICS.STATE]
            oid = info[env_constants.ENV_METRICS.OBSERVATION]
            action_sequence.append(a)
            state_sequence.append(state_id)
            is_obs_feasible(env=env, action_sequence=action_sequence, obs=oid, state_sequence=state_sequence)
            print(t)
            # s = CyborgEnvUtil.state_id_to_state_vector(state_id=state_id)
            # obs = CyborgEnvUtil.state_id_to_state_vector(state_id=oid, observation=True)
            R += r
            t += 1
        returns.append(R)
        print(f"{i}/{num_evaluations}, avg R: {np.mean(returns)}, R: {R}")

