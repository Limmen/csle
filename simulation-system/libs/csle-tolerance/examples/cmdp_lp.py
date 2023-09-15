import numpy as np

from csle_tolerance.util.intrusion_response_cmdp_util import IntrusionRecoveryCmdpUtil
from csle_tolerance.dao.intrusion_response_cmdp_config import IntrusionResponseCmdpConfig
from csle_tolerance.envs.intrusion_response_cmdp_env import IntrusionResponseCmdpEnv
from csle_tolerance.algorithms.lp_cmdp import LpCmdp

if __name__ == '__main__':
    p_a = 0.4
    p_c = 0.01
    p_u = 0.4
    s_max = 20
    s = 2
    s_init = 10
    seed = 999
    f = 3
    epsilon_a = 0.2
    negate_costs = False
    config = IntrusionResponseCmdpConfig(
        p_a=p_a, p_c=p_c, p_u=p_u, s_max=s_max, initial_state=s_init, negate_costs=negate_costs,
        states = IntrusionRecoveryCmdpUtil.state_space(s_max=s_max), actions=IntrusionRecoveryCmdpUtil.action_space(),
        transition_tensor=IntrusionRecoveryCmdpUtil.transition_tensor(
            states=IntrusionRecoveryCmdpUtil.state_space(s_max=s_max), actions=IntrusionRecoveryCmdpUtil.action_space(),
            p_u=p_u, p_a=p_a, p_c=p_c, s_max=s_max),
        cost_tensor=IntrusionRecoveryCmdpUtil.cost_tensor(
            states=IntrusionRecoveryCmdpUtil.state_space(s_max=s_max), negate=negate_costs), seed=seed,
        f=f, constraint_cost_tensor=IntrusionRecoveryCmdpUtil.constraint_cost_tensor(
            states=IntrusionRecoveryCmdpUtil.state_space(s_max=s_max), f=f), epsilon_a=epsilon_a
    )
    env = IntrusionResponseCmdpEnv(config=config)

    # T = 1000000
    # env.reset()
    # costs = []
    # for t in range(T):
    #     s, c, _, done, _ = env.step(a=0)
    #     costs.append(c)
    # print(np.mean(costs))
    # import sys
    # sys.exit()

    availabilities = []
    feasibilities = []
    values = []
    thresholds = []
    for i in np.linspace(0.0, 1.0, int(1/0.01)):
        status, occupancy_measure, strategy, constraint_costs, objective_value = (
            LpCmdp.lp(actions=config.actions, states=config.states, cost_tensor=config.cost_tensor,
                  transition_tensor=config.transition_tensor, constraint_cost_tensors=[config.constraint_cost_tensor],
                  constraint_cost_thresholds=[i]))
        availabilities.append(constraint_costs[0])
        thresholds.append(i)
        values.append(objective_value)
        if status == "Infeasible":
            feasibilities.append(False)
        else:
            feasibilities.append(True)

    print(feasibilities)
    print(values)
    print(thresholds)
    print(availabilities)
    for i in range(len(thresholds)):
        print(f"{thresholds[i]:5f} {values[i]:5f} {feasibilities[i]}")

    # print(f"Expected availability: {constraint_costs[0]}")
    # for s in config.states:
    #     for a in config.actions:
    #         print(f"rho(A={a}, S={s})={round(occupancy_measure[s][a], 4)}, "
    #               f"pi*(A={a}|S={s})={round(strategy[s][a], 4)}")

