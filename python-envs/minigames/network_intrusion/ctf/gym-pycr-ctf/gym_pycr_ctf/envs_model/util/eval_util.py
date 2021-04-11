from typing import Tuple, List
import torch
import numpy as np


class EvalUtil:
    """
    Utility class for evaluating policies
    """
    @staticmethod
    def eval_defender(env, model) -> Tuple[float, float, float, float, float, float]:
        """
        Evaluates a given model in the given environment

        :param env: the environment
        :param model: the model
        :return: (avg_reward, avg_steps, avg_baseline_severe_r, avg_baseline_warning_r,
                  avg_baseline_critical_r, avg_baseline_var_log_r)
        """
        tau_1, tau_2, tau_3 = EvalUtil.eval_taus()
        rewards = []
        steps = []
        snort_severe_r = []
        snort_warning_r = []
        snort_critical_r = []
        var_log_r = []


        obs_tensor = torch.as_tensor(np.array(tau_1))
        actions, values = EvalUtil.predict(model, obs_tensor, env)
        reward = EvalUtil.compute_reward(actions)
        snort_warning_baseline_r = EvalUtil.compute_snort_warning_baseline(tau_1, env.env_config)
        snort_severe_baseline_r = EvalUtil.compute_snort_severe_baseline(tau_1, env.env_config)
        snort_critical_baseline_r = EvalUtil.compute_snort_critical_baseline(tau_1, env.env_config)
        var_log_baseline = snort_warning_baseline_r
        steps_l = EvalUtil.compute_steps(actions)
        rewards.append(reward)
        snort_severe_r.append(snort_severe_baseline_r)
        snort_warning_r.append(snort_warning_baseline_r)
        snort_critical_r.append(snort_critical_baseline_r)
        var_log_r.append(var_log_baseline)
        steps.append(steps_l)

        obs_tensor = torch.as_tensor(np.array(tau_2))
        actions, values = EvalUtil.predict(model, obs_tensor, env)
        reward = EvalUtil.compute_reward(actions)
        snort_warning_baseline_r = EvalUtil.compute_snort_warning_baseline(tau_2, env.env_config)
        snort_severe_baseline_r = EvalUtil.compute_snort_severe_baseline(tau_2, env.env_config)
        snort_critical_baseline_r = EvalUtil.compute_snort_critical_baseline(tau_2, env.env_config)
        var_log_baseline = snort_warning_baseline_r
        steps_l = EvalUtil.compute_steps(actions)
        rewards.append(reward)
        snort_severe_r.append(snort_severe_baseline_r)
        snort_warning_r.append(snort_warning_baseline_r)
        snort_critical_r.append(snort_critical_baseline_r)
        var_log_r.append(var_log_baseline)
        steps.append(steps_l)

        obs_tensor = torch.as_tensor(np.array(tau_3))
        actions, values = EvalUtil.predict(model, obs_tensor, env)
        reward = EvalUtil.compute_reward(actions)
        snort_warning_baseline_r = EvalUtil.compute_snort_warning_baseline(tau_3, env.env_config)
        snort_severe_baseline_r = EvalUtil.compute_snort_severe_baseline(tau_3, env.env_config)
        snort_critical_baseline_r = EvalUtil.compute_snort_critical_baseline(tau_3, env.env_config)
        var_log_baseline = snort_warning_baseline_r
        steps_l = EvalUtil.compute_steps(actions)
        rewards.append(reward)
        snort_severe_r.append(snort_severe_baseline_r)
        snort_warning_r.append(snort_warning_baseline_r)
        snort_critical_r.append(snort_critical_baseline_r)
        var_log_r.append(var_log_baseline)
        steps.append(steps_l)

        avg_reward = np.mean(rewards)
        avg_steps = np.mean(steps)
        avg_baseline_severe_r = np.mean(snort_severe_r)
        avg_baseline_warning_r = np.mean(snort_warning_r)
        avg_baseline_critical_r = np.mean(snort_critical_r)
        avg_baseline_var_log_r = np.mean(var_log_r)

        return avg_reward, avg_steps, avg_baseline_severe_r, avg_baseline_warning_r, avg_baseline_critical_r, \
               avg_baseline_var_log_r


    @staticmethod
    def eval_taus() -> List[float]:
        """
        Returns a list of trajectories to use for evaluation

        :return: list of trajectories with observations
        """
        tau_1 = [
            [0., 0., 0., 0., 0., 0., 0., 0., 0.],
            [2., 4., 0., 2., 2., 4., 0., 2., 1.],
            [2., 4., 0., 2., 2., 4., 0., 2., 1.],
            [4., 8., 0., 4., 6., 12., 0., 6., 2.],
            [123., 266., 20., 103., 129., 278., 20., 109., 3.],
            [0., 0., 0., 0., 129., 278., 20., 109., 4.],
            [4., 8., 0., 4., 133., 286., 20., 113., 5.],
            [3., 6., 0., 3., 136., 292., 20., 116., 6.],
            [13., 30., 4., 9., 149., 322., 24., 125., 7.],
            [1., 2., 0., 1., 150., 324., 24., 126., 8.],
            [4., 8., 0., 4., 154., 332., 24., 130., 9.],
            [13., 30., 4., 9., 167., 362., 28., 139., 10.],
            [0., 0., 0., 0., 167., 362., 28., 139., 11.],
            [4., 8., 0., 4., 171., 370., 28., 143., 12.],
            [14., 32., 4., 10., 185., 402., 32., 153., 13.],
            [2., 4., 0., 2., 187., 406., 32., 155., 14.],
            [121., 262., 20., 101., 308., 668., 52., 256., 15.],
            [1., 2., 0., 1., 309., 670., 52., 257., 16.],
            [3., 6., 0., 3., 312., 676., 52., 260., 17.],
            [6., 12., 0., 6., 318., 688., 52., 266., 18.]
        ]

        tau_2 = [
            [0., 0., 0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0., 0., 1.],
            [5., 10., 0., 5., 5., 10., 0., 5., 2.],
            [123., 266., 20., 103., 128., 276., 20., 108., 3.],
            [2., 4., 0., 2., 130., 280., 20., 110., 4.],
            [3., 6., 0., 3., 133., 286., 20., 113., 5.],
            [4., 8., 0., 4., 137., 294., 20., 117., 6.],
            [14., 32., 4., 10., 151., 326., 24., 127., 7.],
            [1., 2., 0., 1., 152., 328., 24., 128., 8.],
            [4., 8., 0., 4., 156., 336., 24., 132., 9.],
            [13., 30., 4., 9., 169., 366., 28., 141., 10.],
            [1., 2., 0., 1., 170., 368., 28., 142., 11.],
            [3., 6., 0., 3., 173., 374., 28., 145., 12.],
            [15., 34., 4., 11., 188., 408., 32., 156., 13.],
            [7., 14., 0., 7., 195., 422., 32., 163., 14.],
            [122., 264., 20., 102., 317., 686., 52., 265., 15.],
            [1., 2., 0., 1., 318., 688., 52., 266., 16.],
            [3., 6., 0., 3., 321., 694., 52., 269., 17.],
            [3., 6., 0., 3., 324., 700., 52., 272., 18.]
        ]

        tau_3 = [
            [0., 0., 0., 0., 0., 0., 0., 0., 0.],
            [1., 2., 0., 1., 1., 2., 0., 1., 1.],
            [4., 8., 0., 4., 5., 10., 0., 5., 2.],
            [124., 268., 20., 104., 129., 278., 20., 109., 3.],
            [1., 2., 0., 1., 130., 280., 20., 110., 4.],
            [3., 6., 0., 3., 133., 286., 20., 113., 5.],
            [2., 4., 0., 2., 135., 290., 20., 115., 6.],
            [12., 28., 4., 8., 147., 318., 24., 123., 7.],
            [1., 2., 0., 1., 148., 320., 24., 124., 8.],
            [2., 4., 0., 2., 150., 324., 24., 126., 9.],
            [13., 30., 4., 9., 163., 354., 28., 135., 10.],
            [1., 2., 0., 1., 164., 356., 28., 136., 11.],
            [4., 8., 0., 4., 168., 364., 28., 140., 12.],
            [13., 30., 4., 9., 181., 394., 32., 149., 13.],
            [2., 4., 0., 2., 183., 398., 32., 151., 14.],
            [120., 260., 20., 100., 303., 658., 52., 251., 15.],
            [0., 0., 0., 0., 303., 658., 52., 251., 16.],
            [4., 8., 0., 4., 307., 666., 52., 255., 17.],
            [3., 6., 0., 3., 310., 672., 52., 258., 18.]
        ]

        return tau_1, tau_2, tau_3

    @staticmethod
    def compute_reward(actions) -> float:
        """
        Utility function for computing the reward of a sequence of actions of the defender

        :param actions: the sequence of actions of the defender
        :return: the reward
        """
        stopping_idx = -1
        for i in range(len(actions)):
            if actions[i] == 0:
                stopping_idx = i
                break
        r = 0
        if stopping_idx < 6:
            return -1
        if stopping_idx == -1:
            return -1
        if stopping_idx >= 6:
            return 10.0 / max(1, stopping_idx - 5)

    @staticmethod
    def compute_steps(actions) -> int:
        """
        Utility function for computing the steps in the environment of a sequence of actions of the defender

        :param actions: the sequence of actions of the defender
        :return: The number of steps
        """
        stopping_idx = -1
        for i in range(len(actions)):
            if actions[i] == 0:
                stopping_idx = i
                break
        if stopping_idx == -1:
            return len(actions)
        else:
            return stopping_idx

    @staticmethod
    def compute_snort_warning_baseline(tau, env_config) -> float:
        """
        Utility function for computing the reward of the snort warning baseline

        :param tau: the trajectory of observations
        :param env_config: the environment configuration
        :return: the reward
        """
        stopping_thresh = env_config.snort_warning_baseline_threshold
        stopping_idx = -1
        for i in range(len(tau)):
            if tau[i][3] > stopping_thresh:
                stopping_idx = i
                break

        if stopping_idx < 6:
            return -1
        if stopping_idx == -1:
            return -1
        if stopping_idx >= 6:
            return 10.0 / max(1, stopping_idx - 5)

    @staticmethod
    def compute_snort_severe_baseline(tau, env_config) -> float:
        """
        Utility function for computing the reward of the snort severe baseline

        :param tau: the trajectory
        :param env_config: the environment configuration
        :return: the reward
        """
        stopping_thresh = env_config.snort_severe_baseline_threshold
        stopping_idx = -1
        for i in range(len(tau)):
            if tau[i][2] > stopping_thresh:
                stopping_idx = i
                break

        if stopping_idx < 6:
            return -1
        if stopping_idx == -1:
            return -1
        if stopping_idx >= 6:
            return 10.0 / max(1, stopping_idx - 5)

    @staticmethod
    def compute_snort_critical_baseline(tau, env_config) -> float:
        """
        Utility function for computing the reward of the snort critical baseline

        :param tau: the trajectory
        :param env_config: the environment configuration
        :return: the reward
        """
        stopping_thresh = env_config.snort_critical_baseline_threshold
        stopping_idx = -1
        for i in range(len(tau)):
            if tau[i][2] > stopping_thresh:
                stopping_idx = i
                break

        if stopping_idx < 6:
            return -1
        if stopping_idx == -1:
            return -1
        if stopping_idx >= 6:
            return 10.0 / max(1, stopping_idx - 5)

    @staticmethod
    def predict(model, obs_tensor, env) -> Tuple[List[int], List[float]]:
        """
        Utility function for predicting the next action given a model, an environment, and a observation

        :param model: the model
        :param obs_tensor: the observation from the environment
        :param env: the environment
        :return: the predicted action and values
        """
        actions, values = model.predict(observation=obs_tensor, deterministic=True,
                                        state=obs_tensor, attacker=False,
                                        infos={},
                                        env_config=env.env_config,
                                        env_configs=None, env=env,
                                        env_idx=0,
                                        env_state=env.env_state
                                        )
        return actions, values
