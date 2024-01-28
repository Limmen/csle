import numpy as np
import torch
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender
from gym_csle_cyborg.util.cyborg_env_util import CyborgEnvUtil
import csle_agents.constants.constants as constants
from csle_agents.agents.pomcp.pomcp_util import POMCPUtil
from csle_common.metastore.metastore_facade import MetastoreFacade
import math

if __name__ == '__main__':
    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=True, decoy_state=True,
        scanned_state=True, decoy_optimization=False, cache_visited_states=True)
    csle_cyborg_env = CyborgScenarioTwoDefender(config=config)
    actions = list(csle_cyborg_env.action_id_to_type_and_host.keys())
    torch.multiprocessing.set_start_method('spawn')
    returns = []
    num_episodes = 1
    A = csle_cyborg_env.get_action_space()
    # rollout_policy = MetastoreFacade.get_ppo_policy(id=98)
    # for episode in range(num_episodes):
    for ep in range(num_episodes):
        o, info = csle_cyborg_env.reset()
        s = info[constants.ENV_METRICS.STATE]
        obs_vec = CyborgEnvUtil.state_id_to_state_vector(state_id=info[constants.ENV_METRICS.OBSERVATION], observation=True)
        print(obs_vec)
        # print(csle_cyborg_env.get_true_table())
        total_R = 0
        for t in range(100):
            # a = POMCPUtil.rand_choice(A)
            a = 10
            o, r, done, _, info = csle_cyborg_env.step(action=a)
            obs_vec = CyborgEnvUtil.state_id_to_state_vector(state_id=info[constants.ENV_METRICS.OBSERVATION], observation=True)
            # print(obs_vec)
            # print(obs_vec)
            # print(csle_cyborg_env.get_true_table())
            print(csle_cyborg_env.get_table())
            print(csle_cyborg_env.get_last_action(agent="Red"))
            # print(f"action_success:{csle_cyborg_env.get_red_action_success()}")
            total_R += r
            # print(f"t: {t}, a: {a}, r: {r}, s: {s}, cumulative_R: {total_R},")
            # print(csle_cyborg_env.get_true_table())
            # print(csle_cyborg_env.get_last_action(agent="Red"))
            s = info[constants.ENV_METRICS.STATE]
            o_id = info[constants.ENV_METRICS.OBSERVATION]
        # returns.append(total_R)
        # print(f"average return: {np.mean(returns)}, ep {ep}/{num_episodes}")
