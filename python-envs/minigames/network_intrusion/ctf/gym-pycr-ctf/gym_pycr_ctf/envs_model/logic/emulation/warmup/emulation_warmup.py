from gym_pycr_ctf.envs_model.logic.exploration.exploration_policy import ExplorationPolicy

class EmulationWarmup:


    @staticmethod
    def warmup(exp_policy: ExplorationPolicy, num_warmup_steps: int, env, render: bool = False):
        env.reset()
        for i in range(num_warmup_steps):
            if i % 10 == 0:
                print("Warmup {}%".format(float(i/num_warmup_steps)))
            attacker_action = exp_policy.action(env=env)
            defender_action = None
            action = (attacker_action, defender_action)
            obs, reward, done, info = env.step(action)

            if render:
                env.render()
            if done:
                env.reset()
        return obs