from gym_pycr_pwcrack.envs.logic.exploration.exploration_policy import ExplorationPolicy

class ClusterWarmup:


    @staticmethod
    def warmup(exp_policy: ExplorationPolicy, num_warmup_steps: int, env, render: bool = False):
        env.reset()
        for i in range(num_warmup_steps):
            if i % 10 == 0:
                print("Warmup {}%".format(float(i/num_warmup_steps)))
            action = exp_policy.action(env=env)
            obs, reward, done, info = env.step(action)

            if render:
                env.render()
            if done:
                env.reset()
        return obs