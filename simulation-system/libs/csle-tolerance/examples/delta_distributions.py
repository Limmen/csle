from csle_tolerance.util.intrusion_response_cmdp_util import IntrusionRecoveryCmdpUtil
from csle_tolerance.dao.intrusion_response_cmdp_config import IntrusionResponseCmdpConfig
from csle_tolerance.envs.intrusion_response_cmdp_env import IntrusionResponseCmdpEnv

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
        states=IntrusionRecoveryCmdpUtil.state_space(s_max=s_max), actions=IntrusionRecoveryCmdpUtil.action_space(),
        transition_tensor=IntrusionRecoveryCmdpUtil.transition_tensor(
            states=IntrusionRecoveryCmdpUtil.state_space(s_max=s_max), actions=IntrusionRecoveryCmdpUtil.action_space(),
            p_u=p_u, p_a=p_a, p_c=p_c, s_max=s_max),
        cost_tensor=IntrusionRecoveryCmdpUtil.cost_tensor(
            states=IntrusionRecoveryCmdpUtil.state_space(s_max=s_max), negate=negate_costs), seed=seed,
        f=f, constraint_cost_tensor=IntrusionRecoveryCmdpUtil.constraint_cost_tensor(
            states=IntrusionRecoveryCmdpUtil.state_space(s_max=s_max), f=f), epsilon_a=epsilon_a
    )
    env = IntrusionResponseCmdpEnv(config=config)

    table_names = ["datatablee", "datatableee", "datatableeee", "datatableeeee", "datatableeeeee", ]
    for k, s in enumerate([0, 10, 20]):
        probs = []
        s_primes = range(0, config.s_max + 1)
        for j in range(len(s_primes)):
            p = config.transition_tensor[0][s][s_primes[j]]
            probs.append(p)

        print("\pgfplotstableread{")
        for i in range(len(probs)):
            print(f"{s_primes[i]} {round(probs[i], 10):f}")
        print("}" + "\\" + table_names[k])
