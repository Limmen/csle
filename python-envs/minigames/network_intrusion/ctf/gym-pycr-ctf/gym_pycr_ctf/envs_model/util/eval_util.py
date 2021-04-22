from typing import Tuple, List
import torch
import numpy as np
from gym_pycr_ctf.dao.network.trajectory import Trajectory


class EvalUtil:
    """
    Utility class for evaluating policies
    """
    @staticmethod
    def eval_defender(env, model, deterministic: bool = False):
        """
        Evaluates a given model in the given environment

        :param env: the environment
        :param model: the model
        :param deterministic: whether to do deterministic predictions or not
        :return: (avg_reward, avg_steps, avg_baseline_severe_r, avg_baseline_warning_r,
                  avg_baseline_critical_r, avg_baseline_var_log_r)
        """
        trajectories = EvalUtil.eval_taus(env.env_config.emulation_config.save_dynamics_model_dir)
        rewards = []
        steps = []
        snort_severe_r = []
        snort_warning_r = []
        snort_critical_r = []
        var_log_r = []
        flags_list = []
        flags_percentage_list = []
        episode_caught_list = []
        episode_early_stopped_list = []
        episode_successful_intrusion_list = []
        attacker_cost_list = []
        attacker_cost_norm_list = []
        attacker_alerts_list = []
        attacker_alerts_norm_list = []
        optimal_stopping_idx = 4

        for tau in trajectories:
            obs_tensor = torch.as_tensor(np.array(tau.defender_observations))
            actions, values = EvalUtil.predict(model, obs_tensor, env, deterministic=deterministic)
            reward, early_stopping, succ_intrusion, caught = EvalUtil.compute_reward(
                actions, env.env_config, optimal_stopping_idx=optimal_stopping_idx)
            flags, flags_percentage, attacker_cost, attacker_cost_norm, attacker_alerts, \
            attacker_alerts_norm = EvalUtil.compute_info_metrics(
                actions=actions, trajectory=tau, env_config=env.env_config)
            flags_list.append(flags)
            flags_percentage_list.append(flags_percentage)
            episode_caught_list.append(caught)
            episode_early_stopped_list.append(early_stopping)
            episode_successful_intrusion_list.append(succ_intrusion)
            attacker_cost_list.append(attacker_cost)
            attacker_cost_norm_list.append(attacker_cost_norm)
            attacker_alerts_list.append(attacker_alerts)
            attacker_alerts_norm_list.append(attacker_alerts_norm)
            snort_warning_baseline_r = EvalUtil.compute_snort_warning_baseline(
                tau.defender_observations, env.env_config, optimal_stopping_idx=optimal_stopping_idx)
            snort_severe_baseline_r = EvalUtil.compute_snort_severe_baseline(tau.defender_observations, env.env_config,
                                                                             optimal_stopping_idx=optimal_stopping_idx)
            snort_critical_baseline_r = EvalUtil.compute_snort_critical_baseline(
                tau.defender_observations, env.env_config, optimal_stopping_idx=optimal_stopping_idx)
            var_log_baseline = snort_warning_baseline_r
            steps_l = EvalUtil.compute_steps(actions)
            rewards.append(reward)
            snort_severe_r.append(snort_severe_baseline_r)
            snort_warning_r.append(snort_warning_baseline_r)
            snort_critical_r.append(snort_critical_baseline_r)
            var_log_r.append(var_log_baseline)
            steps.append(steps_l)

        return rewards, steps, snort_severe_r, snort_warning_r, snort_critical_r, \
               var_log_r, flags_list, flags_percentage_list, episode_caught_list, episode_early_stopped_list, \
               episode_successful_intrusion_list, attacker_cost_list, attacker_cost_norm_list, attacker_alerts_list, \
               attacker_alerts_norm_list


    @staticmethod
    def find_stopping_idx(actions) -> int:
        stopping_idx = -1
        for i in range(len(actions)):
            if actions[i] == 0:
                stopping_idx = i
                break
        return stopping_idx


    @staticmethod
    def eval_taus(dir_path) -> List[Trajectory]:
        """
        Returns a list of trajectories to use for evaluation

        :param dir_path: the directory to load the trajectories from
        :return: list of trajectories with observations
        """
        trajectories = Trajectory.load_trajectories(dir_path)
        return trajectories

    @staticmethod
    def compute_reward(actions, env_config, optimal_stopping_idx : int = 6) -> float:
        """
        Utility function for computing the reward of a sequence of actions of the defender

        :param actions: the sequence of actions of the defender
        :param env_config: the environment config
        :return: the reward
        """
        stopping_idx = EvalUtil.find_stopping_idx(actions)
        r = 0
        print("stopping id:{}".format(stopping_idx, actions))
        if stopping_idx < optimal_stopping_idx:
            return env_config.defender_early_stopping, True, False, False
        if stopping_idx == -1:
            return env_config.defender_intrusion_reward, False, True, False
        if stopping_idx >= optimal_stopping_idx:
            return env_config.defender_caught_attacker_reward / max(1, stopping_idx - 5),  False, False, True

    @staticmethod
    def compute_steps(actions) -> int:
        """
        Utility function for computing the steps in the environment of a sequence of actions of the defender

        :param actions: the sequence of actions of the defender
        :return: The number of steps
        """
        stopping_idx = EvalUtil.find_stopping_idx(actions)
        if stopping_idx == -1:
            return len(actions)
        else:
            return stopping_idx

    @staticmethod
    def compute_info_metrics(actions, trajectory: Trajectory, env_config) -> int:
        flags = 0
        flags_percentage = 0
        #episode_caught = 0
        #episode_early_stopped = 0
        #episode_successful_intrusion = 0
        attacker_cost = 0
        attacker_cost_norm = 0
        attacker_alerts = 0
        attacker_alerts_norm = 0
        stopping_idx = EvalUtil.find_stopping_idx(actions)
        for i in range(len(trajectory.infos)):
            if i == stopping_idx or trajectory.dones[i]:
                if i > 0:
                    flags = trajectory.infos[i]["flags"]
                    flags_percentage = flags / env_config.num_flags
                    #episode_caught = trajectory.infos[i]["caught_attacker"]
                    #episode_early_stopped = trajectory.infos[i]["episode_early_stopped"]
                    #episode_successful_intrusion = trajectory.infos[i]["successful_intrusion"]
                    attacker_cost = trajectory.infos[i]["attacker_cost"]
                    attacker_cost_norm = trajectory.infos[i]["attacker_cost_norm"]
                    attacker_alerts = trajectory.infos[i]["attacker_alerts"]
                    attacker_alerts_norm = trajectory.infos[i]["attacker_alerts_norm"]
                    break
                else:
                    break
        return flags, flags_percentage, attacker_cost, attacker_cost_norm, attacker_alerts, attacker_alerts_norm

    @staticmethod
    def compute_snort_warning_baseline(tau, env_config, optimal_stopping_idx: int) -> float:
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

        if stopping_idx < optimal_stopping_idx:
            return env_config.defender_early_stopping
        if stopping_idx == -1:
            return env_config.defender_intrusion_reward
        if stopping_idx >= optimal_stopping_idx:
            return env_config.defender_caught_attacker_reward / max(1, stopping_idx - 5)

    @staticmethod
    def compute_snort_severe_baseline(tau, env_config, optimal_stopping_idx: int = 6) -> float:
        """
        Utility function for computing the reward of the snort severe baseline

        :param tau: the trajectory
        :param env_config: the environment configuration
        :return: the reward
        """
        stopping_thresh = env_config.snort_severe_baseline_threshold
        stopping_idx = -1
        for i in range(len(tau)):
            if tau[i][6] > stopping_thresh:
                stopping_idx = i
                break

        if stopping_idx < optimal_stopping_idx:
            return env_config.defender_early_stopping
        if stopping_idx == -1:
            return env_config.defender_intrusion_reward
        if stopping_idx >= optimal_stopping_idx:
            return env_config.defender_caught_attacker_reward / max(1, stopping_idx - 5)

    @staticmethod
    def compute_snort_critical_baseline(tau, env_config, optimal_stopping_idx: int = 6) -> float:
        """
        Utility function for computing the reward of the snort critical baseline

        :param tau: the trajectory
        :param env_config: the environment configuration
        :return: the reward
        """
        stopping_thresh = env_config.snort_critical_baseline_threshold
        stopping_idx = -1
        for i in range(len(tau)):
            if tau[i][6] > stopping_thresh:
                stopping_idx = i
                break

        if stopping_idx < optimal_stopping_idx:
            return env_config.defender_early_stopping
        if stopping_idx == -1:
            return env_config.defender_intrusion_reward
        if stopping_idx >= optimal_stopping_idx:
            return env_config.defender_caught_attacker_reward / max(1, stopping_idx - 5)

    @staticmethod
    def predict(model, obs_tensor, env, deterministic: bool = False) -> Tuple[List[int], List[float]]:
        """
        Utility function for predicting the next action given a model, an environment, and a observation

        :param model: the model
        :param obs_tensor: the observation from the environment
        :param env: the environment
        :param deterministic: whether to do deterministic predictions or not
        :return: the predicted action and values
        """
        actions, values = model.predict(observation=obs_tensor, deterministic=deterministic,
                                        state=obs_tensor, attacker=False,
                                        infos={},
                                        env_config=env.env_config,
                                        env_configs=None, env=env,
                                        env_idx=0,
                                        env_state=env.env_state
                                        )
        return actions, values
