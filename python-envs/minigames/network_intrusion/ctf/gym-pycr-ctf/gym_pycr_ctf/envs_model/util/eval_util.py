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
        uncaught_intrusion_steps_l = []
        opt_r_l = []
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
        snort_severe_ca = []
        snort_warning_ca = []
        snort_critical_ca = []
        var_log_ca = []
        step_ca = []
        snort_severe_es = []
        snort_warning_es = []
        snort_critical_es = []
        var_log_es = []
        step_es = []
        snort_severe_uit = []
        snort_warning_uit = []
        snort_critical_uit = []
        var_log_uit = []
        step_uit = []
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
        optimal_stopping_times = []
        model_stopping_times = []
        intrusion_start_obs_1=[]
        intrusion_start_obs_2 = []
        intrusion_start_obs_3 = []
        intrusion_start_obs_4 = []
        stopping_obs_l = []
        policy = model.defender_policy.copy()
        for tau in trajectories:
            if not EvalUtil.is_correct_attacker(tau):
                continue
            optimal_stopping_idx = np.random.geometric(p=0.2, size=1)[0]
            no_intrusion_obs = EvalUtil.get_observations_prior_to_intrusion(
                env=env, optimal_stopping_idx=optimal_stopping_idx)
            optimal_stopping_idx +=1
            opt_r_l.append(optimal_stopping_idx*env.env_config.defender_service_reward
                           + env.env_config.defender_caught_attacker_reward)
            obs, obs_intrusion = EvalUtil.merge_observations(no_intrusion_obs, tau)
            obs_tensor = torch.as_tensor(obs)
            actions, values = EvalUtil.predict(policy, obs_tensor, env, deterministic=deterministic)
            reward, early_stopping, succ_intrusion, caught, uncaught_intrusion_steps, stopping_time = \
                EvalUtil.compute_reward(
                actions, env.env_config, optimal_stopping_idx=optimal_stopping_idx,
                steps=len(np.array(tau.defender_observations))
            )
            stopping_obs = obs[stopping_time]
            flags, flags_percentage, attacker_cost, attacker_cost_norm, attacker_alerts, \
            attacker_alerts_norm = EvalUtil.compute_info_metrics(
                actions=actions, trajectory=tau, env_config=env.env_config)
            flags_list.append(flags)
            flags_percentage_list.append(flags_percentage)
            episode_caught_list.append(caught)
            episode_early_stopped_list.append(early_stopping)
            uncaught_intrusion_steps_l.append(uncaught_intrusion_steps)
            episode_successful_intrusion_list.append(succ_intrusion)
            attacker_cost_list.append(attacker_cost)
            attacker_cost_norm_list.append(attacker_cost_norm)
            attacker_alerts_list.append(attacker_alerts)
            attacker_alerts_norm_list.append(attacker_alerts_norm)
            snort_warning_baseline_r, snort_warning_baseline_ca, snort_warning_baseline_es, \
            snort_warning_baseline_uit, snort_warning_baseline_s = EvalUtil.compute_snort_warning_baseline(
                tau.defender_observations, env.env_config, optimal_stopping_idx=optimal_stopping_idx,
                steps=len(np.array(tau.defender_observations)))
            snort_severe_baseline_r, snort_severe_baseline_ca, snort_severe_baseline_es, \
            snort_severe_baseline_uit, snort_severe_baseline_s \
                = EvalUtil.compute_snort_severe_baseline(
                tau.defender_observations, env.env_config, optimal_stopping_idx=optimal_stopping_idx,
                steps=len(np.array(tau.defender_observations))
            )
            snort_critical_baseline_r, snort_critical_baseline_ca, snort_critical_baseline_es, \
            snort_critical_baseline_uit, snort_critical_baseline_s \
                = EvalUtil.compute_snort_critical_baseline(
                tau.defender_observations, env.env_config, optimal_stopping_idx=optimal_stopping_idx,
                steps=len(np.array(tau.defender_observations)))
            var_log_baseline_r, var_log_baseline_ca, var_log_baseline_es, \
            var_log_baseline_uit, var_log_baseline_s = EvalUtil.compute_var_log_baseline(
                tau.defender_observations, env.env_config, optimal_stopping_idx=optimal_stopping_idx,
                steps=len(np.array(tau.defender_observations)))
            step_baseline_r, step_baseline_ca, step_baseline_es, \
            step_baseline_uit, step_baseline_s \
                = EvalUtil.compute_step_baseline(
                tau.defender_observations, env.env_config, optimal_stopping_idx=optimal_stopping_idx,
                steps=len(np.array(tau.defender_observations)))
            steps_l = EvalUtil.compute_steps(actions)
            rewards.append(reward)
            snort_severe_r.append(snort_severe_baseline_r)
            snort_severe_s.append(snort_severe_baseline_s)
            snort_severe_ca.append(snort_severe_baseline_ca)
            snort_severe_es.append(snort_severe_baseline_es)
            snort_severe_uit.append(snort_severe_baseline_uit)
            snort_warning_r.append(snort_warning_baseline_r)
            snort_warning_s.append(snort_warning_baseline_s)
            snort_warning_ca.append(snort_warning_baseline_ca)
            snort_warning_es.append(snort_warning_baseline_es)
            snort_warning_uit.append(snort_warning_baseline_uit)
            snort_critical_r.append(snort_critical_baseline_r)
            snort_critical_s.append(snort_critical_baseline_s)
            snort_critical_ca.append(snort_critical_baseline_ca)
            snort_critical_es.append(snort_critical_baseline_es)
            snort_critical_uit.append(snort_critical_baseline_uit)
            var_log_r.append(var_log_baseline_r)
            var_log_s.append(var_log_baseline_s)
            var_log_ca.append(var_log_baseline_ca)
            var_log_es.append(var_log_baseline_es)
            var_log_uit.append(var_log_baseline_uit)
            step_r.append(step_baseline_r)
            step_s.append(step_baseline_s)
            step_ca.append(step_baseline_ca)
            step_es.append(step_baseline_es)
            step_uit.append(step_baseline_uit)
            steps.append(steps_l)
            optimal_stopping_times.append(optimal_stopping_idx)
            model_stopping_times.append(stopping_time)
            intrusion_start_obs_1.append(obs[optimal_stopping_idx])
            intrusion_start_obs_2.append(obs_intrusion[0])
            intrusion_start_obs_3.append(obs[optimal_stopping_idx+1])
            intrusion_start_obs_4.append(obs[optimal_stopping_idx + 2])
            stopping_obs_l.append(stopping_obs)
            intrusion_steps.append(optimal_stopping_idx)

        # print("E2_rewards:{}".format(rewards))
        # print("E2_optimal_stopping_times:{}".format(optimal_stopping_times))
        # print("E2_model_stopping_times:{}".format(model_stopping_times))
        # print("intrusion start obs 1:{}".format(intrusion_start_obs_1))
        # print("intrusion start obs 2:{}".format(intrusion_start_obs_2))
        # print("intrusion start obs 3:{}".format(intrusion_start_obs_3))
        # print("intrusion start obs 4:{}".format(intrusion_start_obs_4))
        # print("stopping obs:{}".format(stopping_obs_l))

        return rewards, steps, uncaught_intrusion_steps_l, opt_r_l, \
               snort_severe_r, snort_warning_r, snort_critical_r, \
               var_log_r, step_r, snort_severe_s, snort_warning_s, \
               snort_critical_s, var_log_s, step_s, \
               snort_severe_ca, snort_warning_ca, snort_critical_ca, var_log_ca, step_ca, \
               snort_severe_es, snort_warning_es, snort_critical_es, var_log_es, step_es, \
               snort_severe_uit, snort_warning_uit, snort_critical_uit, var_log_uit, step_uit, \
               flags_list, flags_percentage_list, episode_caught_list, episode_early_stopped_list, \
               episode_successful_intrusion_list, attacker_cost_list, attacker_cost_norm_list, attacker_alerts_list, \
               attacker_alerts_norm_list, intrusion_steps


    @staticmethod
    def get_observations_prior_to_intrusion(env : "PyCRCTFEnv", optimal_stopping_idx : int):
        """
        Get list of observations for the defender before the intrusion has started

        :param env: the environment
        :param optimal_stopping_idx: the intrusion start time
        :return: the list of observations
        """
        defender_dynamics_model = env.env_config.network_conf.defender_dynamics_model
        fx = defender_dynamics_model.norm_num_new_severe_alerts[(85, '172.18.9.191')]
        fy = defender_dynamics_model.norm_num_new_warning_alerts[(85, '172.18.9.191')]
        x,y,z = 0,0,0
        t = 1
        obs_l = [[0, 0, 0, t]]
        for i in range(0, optimal_stopping_idx):
            t +=1
            x_delta = fx.rvs(size=1)[0]
            y_delta = fy.rvs(size=1)[0]
            x += x_delta
            y += y_delta
            obs_l.append([x, y, z, t])

        return obs_l

    @staticmethod
    def is_correct_attacker(tau):
        if tau.attacker_actions[0] == -1 and tau.attacker_actions[1] == 372 and tau.attacker_actions[2] == 99:
            return True
        return False

    @staticmethod
    def merge_observations(obs_prior_to_intrusion, tau: Trajectory):
        obs_intrusion = []
        for i in range(len(tau.defender_observations)):
            if not (tau.attacker_actions[i] == -1 or tau.attacker_actions[i] == 372):
                obs_intrusion.append(tau.defender_observations[i])

        prior_intrusion_len = len(obs_prior_to_intrusion)
        obs = obs_prior_to_intrusion
        x = obs_prior_to_intrusion[-1][0]
        y = obs_prior_to_intrusion[-1][1]
        z = obs_prior_to_intrusion[-1][2]
        for i in range(len(obs_intrusion)):
            if len(obs_intrusion[i]) == 9:
                x += obs_intrusion[i][2]
                y += obs_intrusion[i][3]
                z = z
            elif len(obs_intrusion[i]) == 4:
                x += obs_intrusion[i][0]
                y += obs_intrusion[i][1]
                z += obs_intrusion[i][2]
            else:
                raise ValueError("Observation dimension does not match")
            t = prior_intrusion_len + i + 1
            obs.append([x,y,z,t])
        return obs, obs_intrusion


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
    def compute_reward(actions, env_config, optimal_stopping_idx : int = 6, steps: int = 100) \
            -> Tuple[int, bool, bool, bool, int, int]:
        """
        Utility function for computing the reward of a sequence of actions of the defender

        :param actions: the sequence of actions of the defender
        :param env_config: the environment config
        :param optimal_stopping_idx: the optimal stopping time
        :param steps: episode length
        :return: the reward
        """
        stopping_idx = EvalUtil.find_stopping_idx(actions)

        r, caught_attacker, early_stopping, uncaught_intrusion_steps, stopping_idx = EvalUtil.stopping_reward(
            stopping_idx=stopping_idx, episode_length=steps,
            optimal_stopping_idx=optimal_stopping_idx,
            env_config=env_config)

        succ_intrusion = (stopping_idx == -1)

        return r, early_stopping, succ_intrusion, caught_attacker, uncaught_intrusion_steps, stopping_idx

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
    def compute_snort_warning_baseline(tau, env_config, optimal_stopping_idx: int, steps : int = 100) \
            -> Tuple[int, bool, bool, int, int]:
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
            if tau[i][1] > stopping_thresh:
                stopping_idx = i
                break

        return EvalUtil.stopping_reward(
            stopping_idx=stopping_idx, episode_length=steps, optimal_stopping_idx=optimal_stopping_idx,
            env_config=env_config)

    @staticmethod
    def compute_snort_severe_baseline(tau, env_config, optimal_stopping_idx: int = 6, steps : int = 100) \
            -> Tuple[int, bool, bool, int, int]:
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
            if tau[i][0] > stopping_thresh:
                stopping_idx = i
                break

        return EvalUtil.stopping_reward(
            stopping_idx=stopping_idx, episode_length=steps, optimal_stopping_idx=optimal_stopping_idx,
            env_config=env_config)

    @staticmethod
    def compute_snort_critical_baseline(tau, env_config, optimal_stopping_idx: int = 6, steps : int = 100)\
            -> Tuple[int, bool, bool, int, int]:
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
            if tau[i][0] > stopping_thresh:
                stopping_idx = i
                break

        return EvalUtil.stopping_reward(
            stopping_idx=stopping_idx, episode_length=steps, optimal_stopping_idx=optimal_stopping_idx,
            env_config=env_config)

    @staticmethod
    def compute_var_log_baseline(tau, env_config, optimal_stopping_idx: int = 6, steps: int = 100) \
            -> Tuple[int, bool, bool, int, int]:
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
            if tau[i][2] > stopping_thresh:
                stopping_idx = i
                break

        return EvalUtil.stopping_reward(
            stopping_idx=stopping_idx, episode_length=steps, optimal_stopping_idx=optimal_stopping_idx,
            env_config=env_config)

    @staticmethod
    def compute_step_baseline(tau, env_config, optimal_stopping_idx: int = 6, steps: int = 100) \
            -> Tuple[int, bool, bool, int, int]:
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
            env_config=env_config)


    @staticmethod
    def predict(policy, obs_tensor, env, deterministic: bool = False) -> Tuple[List[int], List[float]]:
        """
        Utility function for predicting the next action given a model, an environment, and a observation

        :param policy: the policy
        :param obs_tensor: the observation from the environment
        :param env: the environment
        :param deterministic: whether to do deterministic predictions or not
        :return: the predicted action and values
        """
        # actions, values = model.predict(observation=obs_tensor, deterministic=deterministic,
        #                                 state=obs_tensor, attacker=False,
        #                                 infos={},
        #                                 env_config=env.env_config,
        #                                 env_configs=None, env=env,
        #                                 env_idx=0,
        #                                 env_state=env.env_state
        #                                 )
        actions = np.array([0]*len(obs_tensor))
        values = actions
        actions, values = policy.predict(obs_tensor, None, None, deterministic=deterministic,
                                                         env_config=env.env_config,
                                                         env_state=env.env_state, env_configs=None,
                                                         env=env, infos={}, env_idx=0, mask_actions=None,
                                                         attacker=False)
        return actions, values


    @staticmethod
    def stopping_reward(stopping_idx, episode_length, optimal_stopping_idx, env_config) \
            -> Tuple[int, bool, bool, int, int]:
        """
        Computes the reward of stopping at stopping_idx

        :param stopping_idx: the stopping time
        :param episode_length: the episode length
        :param optimal_stopping_idx: the optimal stopping time
        :param env_config: the environment configuration
        :return: the defender reward, caught_attacker, early_stopping, uncaught_intrusion_steps, stopping_idx
        """
        caught_attacker = False
        early_stopping = False
        uncaught_intrusion_steps = 0
        r = 0

        if stopping_idx < optimal_stopping_idx:
            r = env_config.defender_service_reward * (stopping_idx - 1)
            r = r + env_config.defender_early_stopping_reward
            early_stopping = True

        if stopping_idx == -1:
            r = env_config.defender_service_reward * (optimal_stopping_idx - 1)
            r = r + env_config.defender_intrusion_reward * (episode_length - optimal_stopping_idx)

        if stopping_idx >= optimal_stopping_idx:
            r = env_config.defender_service_reward * (optimal_stopping_idx - 1)
            r = r + env_config.defender_intrusion_reward * (stopping_idx - optimal_stopping_idx)
            r = r + env_config.defender_caught_attacker_reward
            caught_attacker = True
            uncaught_intrusion_steps = max(0, stopping_idx - optimal_stopping_idx)

        return r, caught_attacker, early_stopping, uncaught_intrusion_steps, stopping_idx
