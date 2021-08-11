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
        step_r = []
        snort_severe_s = []
        snort_warning_s = []
        snort_critical_s = []
        var_log_s = []
        step_s = []
        flags_list = []
        flags_percentage_list = []
        episode_caught_list = []
        episode_early_stopped_list = []
        episode_successful_intrusion_list = []
        attacker_cost_list = []
        attacker_cost_norm_list = []
        attacker_alerts_list = []
        attacker_alerts_norm_list = []
        intrusion_steps = []
        optimal_stopping_idx = 4

        for tau in trajectories:
            obs_tensor = torch.as_tensor(np.array(tau.defender_observations))
            actions, values = EvalUtil.predict(model, obs_tensor, env, deterministic=deterministic)
            reward, early_stopping, succ_intrusion, caught = EvalUtil.compute_reward(
                actions, env.env_config, optimal_stopping_idx=optimal_stopping_idx,
                steps=len(np.array(tau.defender_observations))
            )
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
            snort_warning_baseline_r, snort_warning_baseline_s = EvalUtil.compute_snort_warning_baseline(
                tau.defender_observations, env.env_config, optimal_stopping_idx=optimal_stopping_idx,
                steps=len(np.array(tau.defender_observations)))
            snort_severe_baseline_r, snort_severe_baseline_s = EvalUtil.compute_snort_severe_baseline(
                tau.defender_observations, env.env_config, optimal_stopping_idx=optimal_stopping_idx,
                steps=len(np.array(tau.defender_observations))
            )
            snort_critical_baseline_r, snort_critical_baseline_s = EvalUtil.compute_snort_critical_baseline(
                tau.defender_observations, env.env_config, optimal_stopping_idx=optimal_stopping_idx,
                steps=len(np.array(tau.defender_observations)))
            var_log_baseline_r, var_log_baseline_s = EvalUtil.compute_var_log_baseline(
                tau.defender_observations, env.env_config, optimal_stopping_idx=optimal_stopping_idx,
                steps=len(np.array(tau.defender_observations)))
            step_baseline_r, step_baseline_s = EvalUtil.compute_step_baseline(
                tau.defender_observations, env.env_config, optimal_stopping_idx=optimal_stopping_idx,
                steps=len(np.array(tau.defender_observations)))
            steps_l = EvalUtil.compute_steps(actions)
            rewards.append(reward)
            snort_severe_r.append(snort_severe_baseline_r)
            snort_severe_s.append(snort_severe_baseline_s)
            snort_warning_r.append(snort_warning_baseline_r)
            snort_warning_s.append(snort_warning_baseline_s)
            snort_critical_r.append(snort_critical_baseline_r)
            snort_critical_s.append(snort_critical_baseline_s)
            var_log_r.append(var_log_baseline_r)
            var_log_s.append(var_log_baseline_s)
            step_r.append(step_baseline_r)
            step_s.append(step_baseline_s)
            steps.append(steps_l)
            intrusion_steps.append(optimal_stopping_idx)

        return rewards, steps, snort_severe_r, snort_warning_r, snort_critical_r, \
               var_log_r, step_r, snort_severe_s, snort_warning_s, \
               snort_critical_s, var_log_s, step_s, \
               flags_list, flags_percentage_list, episode_caught_list, episode_early_stopped_list, \
               episode_successful_intrusion_list, attacker_cost_list, attacker_cost_norm_list, attacker_alerts_list, \
               attacker_alerts_norm_list, intrusion_steps


    @staticmethod
    def find_stopping_idx(actions) -> int:
        """
        Find the stopping idx of the model

        :param actions: the actions predicted by the model
        :return: the stopping idx (-1 if never stop)
        """
        for i in range(len(actions)):
            if actions[i] == 0:
                return i
        return -1


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
    def compute_reward(actions, env_config, optimal_stopping_idx : int = 6, steps: int = 100) -> float:
        """
        Utility function for computing the reward of a sequence of actions of the defender

        :param actions: the sequence of actions of the defender
        :param env_config: the environment config
        :param optimal_stopping_idx: the optimal stopping time
        :param steps: episode length
        :return: the reward
        """
        stopping_idx = EvalUtil.find_stopping_idx(actions)

        r = EvalUtil.stopping_reward(
            stopping_idx=stopping_idx, episode_length=steps,
            optimal_stopping_idx=optimal_stopping_idx,
            env_config=env_config)

        if stopping_idx < optimal_stopping_idx:
            return r, True, False, False

        if stopping_idx == -1:
            return r, False, True, False

        if stopping_idx >= optimal_stopping_idx:
            return r,  False, False, True

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
    def compute_snort_warning_baseline(tau, env_config, optimal_stopping_idx: int, steps : int = 100) -> Tuple[int, int]:
        """
        Utility function for computing the reward of the snort warning baseline

        :param tau: the trajectory of observations
        :param env_config: the environment configuration
        :param steps: number of steps of the episode
        :return: the reward
        """
        stopping_thresh = env_config.snort_warning_baseline_threshold
        stopping_idx = -1
        for i in range(len(tau)):
            if tau[i][3] > stopping_thresh:
                stopping_idx = i
                break

        return EvalUtil.stopping_reward(
            stopping_idx=stopping_idx, episode_length=steps, optimal_stopping_idx=optimal_stopping_idx,
            env_config=env_config), stopping_idx

    @staticmethod
    def compute_snort_severe_baseline(tau, env_config, optimal_stopping_idx: int = 6, steps : int = 100) -> Tuple[int, int]:
        """
        Utility function for computing the reward of the snort severe baseline

        :param tau: the trajectory
        :param env_config: the environment configuration
        :param steps: number of steps of the episode
        :return: the reward
        """
        stopping_thresh = env_config.snort_severe_baseline_threshold
        stopping_idx = -1
        for i in range(len(tau)):
            if tau[i][6] > stopping_thresh:
                stopping_idx = i
                break

        return EvalUtil.stopping_reward(
            stopping_idx=stopping_idx, episode_length=steps, optimal_stopping_idx=optimal_stopping_idx,
            env_config=env_config), stopping_idx

    @staticmethod
    def compute_snort_critical_baseline(tau, env_config, optimal_stopping_idx: int = 6, steps : int = 100)-> Tuple[int, int]:
        """
        Utility function for computing the reward of the snort critical baseline

        :param tau: the trajectory
        :param env_config: the environment configuration
        :param steps: number of steps of the episode
        :return: the reward
        """
        stopping_thresh = env_config.snort_critical_baseline_threshold
        stopping_idx = -1
        for i in range(len(tau)):
            if tau[i][6] > stopping_thresh:
                stopping_idx = i
                break

        return EvalUtil.stopping_reward(
            stopping_idx=stopping_idx, episode_length=steps, optimal_stopping_idx=optimal_stopping_idx,
            env_config=env_config), stopping_idx

    @staticmethod
    def compute_var_log_baseline(tau, env_config, optimal_stopping_idx: int = 6, steps: int = 100)-> Tuple[int, int]:
        """
        Utility function for computing the reward of the var_log baseline

        :param tau: the trajectory
        :param env_config: the environment configuration
        :param steps: number of steps of the episode
        :return: the reward
        """
        stopping_thresh = env_config.var_log_baseline_threshold
        stopping_idx = -1
        for i in range(len(tau)):
            if tau[i][7] > stopping_thresh:
                stopping_idx = i
                break

        return EvalUtil.stopping_reward(
            stopping_idx=stopping_idx, episode_length=steps, optimal_stopping_idx=optimal_stopping_idx,
            env_config=env_config), stopping_idx

    @staticmethod
    def compute_step_baseline(tau, env_config, optimal_stopping_idx: int = 6, steps: int = 100)-> Tuple[int, int]:
        """
        Utility function for computing the reward of the step baseline

        :param tau: the trajectory
        :param env_config: the environment configuration
        :param steps: number of steps of the episode
        :return: the reward
        """
        stopping_idx = env_config.step_baseline_threshold

        return EvalUtil.stopping_reward(
            stopping_idx=stopping_idx, episode_length=steps, optimal_stopping_idx=optimal_stopping_idx,
            env_config=env_config), stopping_idx


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


    @staticmethod
    def stopping_reward(stopping_idx, episode_length, optimal_stopping_idx, env_config) -> int:
        """
        Computes the reward of stopping at stopping_idx

        :param stopping_idx: the stopping time
        :param episode_length: the episode length
        :param optimal_stopping_idx: the optimal stopping time
        :param env_config: the environment configuration
        :return: the defender reward
        """
        if stopping_idx < optimal_stopping_idx:
            r = env_config.defender_service_reward * (stopping_idx - 1)
            r = r + env_config.defender_early_stopping_reward
            return r
        if stopping_idx == -1:
            r = env_config.defender_service_reward * (optimal_stopping_idx - 1)
            r = r + env_config.defender_intrusion_reward * (episode_length - optimal_stopping_idx)
            return r
        if stopping_idx >= optimal_stopping_idx:
            r = env_config.defender_service_reward * (optimal_stopping_idx - 1)
            r = r + env_config.defender_intrusion_reward * (stopping_idx - optimal_stopping_idx)
            r = r + env_config.defender_caught_attacker_reward
            return r
