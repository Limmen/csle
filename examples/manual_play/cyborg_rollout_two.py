import numpy as np
from csle_common.metastore.metastore_facade import MetastoreFacade
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.envs.cyborg_scenario_two_defender import CyborgScenarioTwoDefender
import csle_agents.constants.constants as constants
from csle_agents.agents.pomcp.pomcp_util import POMCPUtil
import math

if __name__ == '__main__':
    ppo_policy = MetastoreFacade.get_ppo_policy(id=22)
    config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=True, decoy_state=True,
        scanned_state=True, decoy_optimization=False, cache_visited_states=True)
    csle_cyborg_env = CyborgScenarioTwoDefender(config=config)
    actions = list(csle_cyborg_env.action_id_to_type_and_host.keys())
    # for i in range(25):
    import torch

    torch.multiprocessing.set_start_method('spawn')
    action_sequence = []
    returns = []
    num_episodes = 100
    for episode in range(num_episodes):
        o, info = csle_cyborg_env.reset()
        s = info[constants.ENV_METRICS.STATE]
        particles = [s]
        belief = POMCPUtil.convert_samples_to_distribution(particles)
        total_R = 0
        for t in range(100):
            action_values = []
            dist = ppo_policy.model.policy.get_distribution(obs=torch.tensor([o]).to(ppo_policy.model.device)).log_prob(
                torch.tensor(actions).to(ppo_policy.model.device)).cpu().detach().numpy()
            dist = list(map(lambda i: (math.exp(dist[i]), actions[i]), list(range(len(dist)))))
            rollout_actions = list(map(lambda x: x[1], sorted(dist, reverse=True, key=lambda x: x[0])[:3]))
            if 34 in rollout_actions:
                rollout_actions.remove(34)
            for i, a in enumerate(rollout_actions):
                R = 0
                for fictitious_state, prob in belief.items():
                    r = csle_cyborg_env.parallel_rollout(policy_id=15, num_processes=1, num_evals_per_process=1,
                                                         max_horizon=1, state_id=fictitious_state)
                    R += r * prob
                action_values.append(R)
            print(action_values)
            a_idx = np.argmax(action_values)
            a = rollout_actions[a_idx]
            o, r, done, _, info = csle_cyborg_env.step(action=a)
            total_R += r
            print(f"t: {t}, a: {a}, r: {r}, s: {s}, cumulative_R: {total_R}, b: {belief}")
            action_sequence.append(a)
            s = info[constants.ENV_METRICS.STATE]
            o_id = info[constants.ENV_METRICS.OBSERVATION]
            particles = POMCPUtil.trajectory_simulation_particles(
                o=o_id, env=csle_cyborg_env, action_sequence=action_sequence, num_particles=10, verbose=True)
            belief = POMCPUtil.convert_samples_to_distribution(particles)
        returns.append(total_R)
        print(f"average return: {np.mean(returns)}")
