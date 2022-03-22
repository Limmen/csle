from typing import Tuple, List
import torch
import numpy as np
import math
import csle_common.constants.constants as constants
from csle_common.dao.network.trajectory import Trajectory
from csle_common.envs_model.util.base_eval_util import BaseEvalUtil
from gym_csle_ctf.dao.network.env_config import CSLEEnvConfig
from gym_csle_ctf.dao.agent.train_agent_log_dto import TrainAgentLogDTO


class EvalUtil(BaseEvalUtil):
    """
    Utility class for evaluating policies
    """
    @staticmethod
    def eval_defender(env, model, train_log_dto: TrainAgentLogDTO, deterministic: bool = False) -> TrainAgentLogDTO:
        """
        Evaluates a given model in the given environment

        :param env: the environment
        :param model: the model
        :param train_log_dto: the train log dto to populate
        :param deterministic: whether to do deterministic predictions or not
        :return: the updated train agent log dto
        """
        stops_remaining_l = []
        trajectories = EvalUtil.eval_taus(env.env_config.emulation_config.save_dynamics_model_dir)
        rewards = []
        steps = []
        optimal_steps = []
        uncaught_intrusion_steps_l = []
        opt_r_l = []
        snort_severe_r = []
        snort_warning_r = []
        snort_critical_r = []
        var_log_r = []
        step_r = []
        snort_severe_stop_1 = []
        snort_warning_stop_1 = []
        snort_critical_stop_1 = []
        var_log_stop_1 = []
        step_stop_1 = []
        snort_severe_stop_2 = []
        snort_warning_stop_2 = []
        snort_critical_stop_2 = []
        var_log_stop_2 = []
        step_stop_2 = []
        snort_severe_stop_3 = []
        snort_warning_stop_3 = []
        snort_critical_stop_3 = []
        var_log_stop_3 = []
        step_stop_3 = []
        snort_severe_stop_4 = []
        snort_warning_stop_4 = []
        snort_critical_stop_4 = []
        var_log_stop_4 = []
        step_stop_4 = []
        snort_severe_stops_remaining_l = []
        snort_warning_stops_remaining_l = []
        snort_critical_stops_remaining_l = []
        var_log_stops_remaining_l = []
        step_stops_remaining_l = []
        snort_severe_steps_l = []
        snort_warning_steps_l = []
        snort_critical_steps_l = []
        var_log_steps_l = []
        step_steps_l = []
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
        optimal_stop_1 = []
        optimal_stop_2 = []
        optimal_stop_3 = []
        optimal_stop_4 = []
        optimal_stops_remaining_l = []
        model_stopping_times_1 = []
        model_stopping_times_2 = []
        model_stopping_times_3 = []
        model_stopping_times_4 = []
        intrusion_start_obs_1=[]
        intrusion_start_obs_2 = []
        intrusion_start_obs_3 = []
        intrusion_start_obs_4 = []
        stopping_obs_l = []
        policy = model.defender_policy.copy()
        merged_taus = []
        optimal_costs = 0
        for i in range(env.env_config.maximum_number_of_defender_stop_actions-1, -1, -1):
            optimal_costs += env.env_config.multistop_costs[i]
            if i == env.env_config.attacker_prevented_stops_remaining:
                break
        for tau in trajectories:
            if not EvalUtil.is_correct_attacker(tau, env):
                continue
            intrusion_start_time = np.random.geometric(p=0.2, size=1)[0]
            no_intrusion_obs = EvalUtil.get_observations_prior_to_intrusion(
                env=env, intrusion_start_time=intrusion_start_time)
            intrusion_prevented_obs = EvalUtil.get_observations_prior_to_intrusion(
                env=env, intrusion_start_time=intrusion_start_time + len(tau.defender_observations))
            optimal_stopping_time = max(intrusion_start_time + 1, env.env_config.maximum_number_of_defender_stop_actions - env.env_config.attacker_prevented_stops_remaining)
            optimal_stopping_indexes = []
            for i in range(env.env_config.maximum_number_of_defender_stop_actions-1, -1, -1):
                if i >= env.env_config.attacker_prevented_stops_remaining:
                    j = i-env.env_config.attacker_prevented_stops_remaining
                    opt_stop_index = max(1, optimal_stopping_time-j)
                    optimal_stopping_indexes.append(opt_stop_index)
                else:
                    optimal_stopping_indexes.append(-1)

            obs, obs_intrusion = EvalUtil.merge_observations(no_intrusion_obs, tau, env_config=env.env_config)

            optimal_service_reward = 0
            optimal_service_reward = optimal_service_reward + env.env_config.defender_service_reward * \
                                     max(0, (optimal_stopping_time -
                                      (env.env_config.maximum_number_of_defender_stop_actions -
                                       env.env_config.attacker_prevented_stops_remaining)))

            for i in range(env.env_config.maximum_number_of_defender_stop_actions, 0, -1):
                if i < env.env_config.attacker_prevented_stops_remaining:
                    break
                elif i == env.env_config.attacker_prevented_stops_remaining:
                    if env.env_config.attacker_prevented_stops_remaining > 0:
                        optimal_service_reward += (max(0, len(obs) - optimal_stopping_time + 1)) * \
                                                  env.env_config.defender_service_reward / (
                                                      math.pow(2,
                                                               env.env_config.maximum_number_of_defender_stop_actions - i))

            opt_r_l.append(optimal_service_reward + optimal_costs + env.env_config.defender_caught_attacker_reward)

            actions, values = EvalUtil.predict(policy, obs, env, deterministic=deterministic, intrusion_prevented_obs=intrusion_prevented_obs)
            reward, early_stopping, succ_intrusion, caught, uncaught_intrusion_steps, stopping_indexes = \
                EvalUtil.compute_reward(
                actions, env.env_config, optimal_stopping_indexes=optimal_stopping_indexes,
                steps=len(obs), intrusion_time=intrusion_start_time
            )
            stopping_obs_1 = obs[int(stopping_indexes[0])]
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
            snort_warning_baseline_uit, snort_warning_baseline_s_indexes, snort_warning_baseline_succ_intrusion = \
                EvalUtil.compute_snort_warning_baseline(
                tau.defender_observations, env.env_config, optimal_stopping_indexes=optimal_stopping_indexes,
                steps=len(obs), intrusion_time=intrusion_start_time)
            snort_severe_baseline_r, snort_severe_baseline_ca, snort_severe_baseline_es, \
            snort_severe_baseline_uit, snort_severe_baseline_s_indexes, snort_warning_baseline_succ_intrusion \
                = EvalUtil.compute_snort_severe_baseline(
                tau.defender_observations, env.env_config, optimal_stopping_indexes=optimal_stopping_indexes,
                steps=len(obs), intrusion_time=intrusion_start_time
            )
            snort_critical_baseline_r, snort_critical_baseline_ca, snort_critical_baseline_es, \
            snort_critical_baseline_uit, snort_critical_baseline_s_indexes, snort_warning_baseline_succ_intrusion \
                = EvalUtil.compute_snort_critical_baseline(
                tau.defender_observations, env.env_config, optimal_stopping_indexes=optimal_stopping_indexes,
                steps=len(np.array(tau.defender_observations)), intrusion_time=intrusion_start_time)
            var_log_baseline_r, var_log_baseline_ca, var_log_baseline_es, \
            var_log_baseline_uit, var_log_baseline_s_indexes, snort_warning_baseline_succ_intrusion = \
                EvalUtil.compute_var_log_baseline(
                tau.defender_observations, env.env_config, optimal_stopping_indexes=optimal_stopping_indexes,
                steps=len(obs), intrusion_time=intrusion_start_time)
            step_baseline_r, step_baseline_ca, step_baseline_es, \
            step_baseline_uit, step_baseline_indexes, snort_warning_baseline_succ_intrusion \
                = EvalUtil.compute_step_baseline(
                tau.defender_observations, env.env_config, optimal_stopping_indexes=optimal_stopping_indexes,
                steps=len(obs), intrusion_time=intrusion_start_time)
            steps_l = EvalUtil.compute_steps(actions, env_config=env.env_config)
            stops_remaining = EvalUtil.compute_stops_remaining(stopping_indexes)
            snort_severe_baseline_stops_remaining = EvalUtil.compute_stops_remaining(snort_severe_baseline_s_indexes)
            snort_warning_baseline_stops_remaining = EvalUtil.compute_stops_remaining(snort_warning_baseline_s_indexes)
            snort_critical_baseline_stops_remaining = EvalUtil.compute_stops_remaining(snort_critical_baseline_s_indexes)
            var_log_baseline_stops_remaining = EvalUtil.compute_stops_remaining(var_log_baseline_s_indexes)
            step_baseline_stops_remaining = EvalUtil.compute_stops_remaining(step_baseline_indexes)
            snort_severe_baseline_step = EvalUtil.compute_steps_baseline(obs, snort_severe_baseline_s_indexes)
            snort_warning_baseline_step = EvalUtil.compute_steps_baseline(obs, snort_warning_baseline_s_indexes)
            snort_critical_baseline_step = EvalUtil.compute_steps_baseline(obs, snort_critical_baseline_s_indexes)
            var_log_baseline_step = EvalUtil.compute_steps_baseline(obs, var_log_baseline_s_indexes)
            step_baseline_step = EvalUtil.compute_steps_baseline(obs, step_baseline_indexes)

            optimal_stops_remaining =env.env_config.attacker_prevented_stops_remaining
            rewards.append(reward)
            snort_severe_r.append(snort_severe_baseline_r)
            snort_severe_stop_1.append(int(snort_severe_baseline_s_indexes[0])+1)
            snort_severe_stop_2.append(int(snort_severe_baseline_s_indexes[1])+1)
            snort_severe_stop_3.append(int(snort_severe_baseline_s_indexes[2])+1)
            snort_severe_stop_4.append(int(snort_severe_baseline_s_indexes[3])+1)
            snort_severe_stops_remaining_l.append(snort_severe_baseline_stops_remaining)
            snort_severe_steps_l.append(snort_severe_baseline_step)
            snort_severe_ca.append(snort_severe_baseline_ca)
            snort_severe_es.append(snort_severe_baseline_es)
            snort_severe_uit.append(snort_severe_baseline_uit)
            snort_warning_r.append(snort_warning_baseline_r)
            snort_warning_stop_1.append(int(snort_warning_baseline_s_indexes[0])+1)
            snort_warning_stop_2.append(int(snort_warning_baseline_s_indexes[1])+1)
            snort_warning_stop_3.append(int(snort_warning_baseline_s_indexes[2])+1)
            snort_warning_stop_4.append(int(snort_warning_baseline_s_indexes[3])+1)
            snort_warning_stops_remaining_l.append(snort_warning_baseline_stops_remaining)
            snort_warning_steps_l.append(snort_warning_baseline_step)
            snort_warning_ca.append(snort_warning_baseline_ca)
            snort_warning_es.append(snort_warning_baseline_es)
            snort_warning_uit.append(snort_warning_baseline_uit)
            snort_critical_r.append(snort_critical_baseline_r)
            snort_critical_stop_1.append(int(snort_critical_baseline_s_indexes[0])+1)
            snort_critical_stop_2.append(int(snort_critical_baseline_s_indexes[1])+1)
            snort_critical_stop_3.append(int(snort_critical_baseline_s_indexes[2])+1)
            snort_critical_stop_4.append(int(snort_critical_baseline_s_indexes[3])+1)
            snort_critical_steps_l.append(snort_critical_baseline_step)
            snort_critical_stops_remaining_l.append(snort_critical_baseline_stops_remaining)
            snort_critical_ca.append(snort_critical_baseline_ca)
            snort_critical_es.append(snort_critical_baseline_es)
            snort_critical_uit.append(snort_critical_baseline_uit)
            var_log_r.append(var_log_baseline_r)
            var_log_stop_1.append(int(var_log_baseline_s_indexes[0])+1)
            var_log_stop_2.append(int(var_log_baseline_s_indexes[1])+1)
            var_log_stop_3.append(int(var_log_baseline_s_indexes[2])+1)
            var_log_stop_4.append(int(var_log_baseline_s_indexes[3])+1)
            var_log_steps_l.append(var_log_baseline_step)
            var_log_stops_remaining_l.append(var_log_baseline_stops_remaining)
            var_log_ca.append(var_log_baseline_ca)
            var_log_es.append(var_log_baseline_es)
            var_log_uit.append(var_log_baseline_uit)
            step_r.append(step_baseline_r)
            step_stop_1.append(int(step_baseline_indexes[0])+1)
            step_stop_2.append(int(step_baseline_indexes[1])+1)
            step_stop_3.append(int(step_baseline_indexes[2])+1)
            step_stop_4.append(int(step_baseline_indexes[3])+1)
            step_stops_remaining_l.append(step_baseline_stops_remaining)
            step_steps_l.append(step_baseline_step)
            step_ca.append(step_baseline_ca)
            step_es.append(step_baseline_es)
            step_uit.append(step_baseline_uit)
            steps.append(steps_l)
            if env.env_config.attacker_prevented_stops_remaining == 0:
                optimal_steps.append(optimal_stopping_indexes[-1])
            else:
                optimal_steps.append(len(obs))
            optimal_stopping_times.append(optimal_stopping_time)
            model_stopping_times_1.append(stopping_indexes[0]+1)
            model_stopping_times_2.append(stopping_indexes[1]+1)
            model_stopping_times_3.append(stopping_indexes[2]+1)
            model_stopping_times_4.append(stopping_indexes[3]+1)
            optimal_stop_1.append(optimal_stopping_indexes[0]+1)
            optimal_stop_2.append(optimal_stopping_indexes[1]+1)
            optimal_stop_3.append(optimal_stopping_indexes[2]+1)
            optimal_stop_4.append(optimal_stopping_indexes[3]+1)
            optimal_stops_remaining_l.append(optimal_stops_remaining)
            intrusion_start_obs_1.append(obs[optimal_stopping_time])
            intrusion_start_obs_2.append(obs_intrusion[0])
            intrusion_start_obs_3.append(obs[optimal_stopping_time+1])
            intrusion_start_obs_4.append(obs[optimal_stopping_time + 2])
            stopping_obs_l.append(stopping_obs_1)
            intrusion_steps.append(optimal_stopping_time)
            merged_taus.append(obs)
            stops_remaining_l.append(stops_remaining)

        # print("E2_rewards:{}".format(rewards))
        # print("E2_optimal_stopping_times:{}".format(optimal_stopping_times))
        # print("E2_model_stopping_times:{}".format(model_stopping_times))
        # print("intrusion start obs 1:{}".format(intrusion_start_obs_1))
        # print("intrusion start obs 2:{}".format(intrusion_start_obs_2))
        # print("intrusion start obs 3:{}".format(intrusion_start_obs_3))
        # print("intrusion start obs 4:{}".format(intrusion_start_obs_4))
        # print("stopping obs:{}".format(stopping_obs_l))
        # print("merged tau:{}".format(merged_taus))

        eval_2_defender_episode_rewards, eval_2_episode_steps, eval_2_uncaught_intrusion_steps, \
        eval_2_optimal_defender_reward, \
        eval_2_episode_snort_severe_baseline_rewards, eval_2_episode_snort_warning_baseline_rewards, \
        eval_2_episode_snort_critical_baseline_rewards, \
        eval_2_episode_var_log_baseline_rewards, eval_2_episode_step_baseline_rewards, \
        eval_2_episode_snort_severe_baseline_steps, eval_2_episode_snort_warning_baseline_steps, \
        eval_2_episode_snort_critical_baseline_steps, \
        eval_2_episode_var_log_baseline_steps, eval_2_episode_step_baseline_steps, \
        eval_2_episode_snort_severe_baseline_caught_attacker, \
        eval_2_episode_snort_warning_baseline_caught_attacker, \
        eval_2_episode_snort_critical_baseline_caught_attacker, \
        eval_2_episode_var_log_baseline_caught_attacker, \
        eval_2_episode_step_baseline_caught_attacker, \
        eval_2_episode_snort_severe_baseline_early_stopping, \
        eval_2_episode_snort_warning_baseline_early_stopping, \
        eval_2_episode_snort_critical_baseline_early_stopping, \
        eval_2_episode_var_log_baseline_early_stopping, eval_2_episode_step_baseline_early_stopping, \
        eval_2_episode_snort_severe_baseline_uncaught_intrusion_steps, \
        eval_2_episode_snort_warning_baseline_uncaught_intrusion_steps, \
        eval_2_episode_snort_critical_baseline_uncaught_intrusion_steps, \
        eval_2_episode_var_log_baseline_uncaught_intrusion_steps, \
        eval_2_episode_step_baseline_uncaught_intrusion_steps, \
        eval_2_flags_list, eval_2_flags_percentage_list, \
        eval_2_episode_caught_list, eval_2_episode_early_stopped_list, \
        eval_2_episode_successful_intrusion_list, eval_2_attacker_cost_list, \
        eval_2_attacker_cost_norm_list, \
        eval_2_attacker_alerts_list, eval_2_attacker_alerts_norm_list, eval_2_episode_intrusion_steps, \
        eval_2_defender_first_stop_step, eval_2_defender_second_stop_step, \
        eval_2_defender_third_stop_step, eval_2_defender_fourth_stop_step, \
        eval_2_defender_stops_remaining, \
        eval_2_episode_snort_severe_baseline_first_stop_step, \
        eval_2_episode_snort_warning_baseline_first_stop_step, eval_2_episode_snort_critical_baseline_first_stop_step, \
        eval_2_episode_var_log_baseline_first_stop_step, eval_2_episode_step_baseline_first_stop_step, \
        eval_2_episode_snort_severe_baseline_second_stop_step, \
        eval_2_episode_snort_warning_baseline_second_stop_step, eval_2_episode_snort_critical_baseline_second_stop_step, \
        eval_2_episode_var_log_baseline_second_stop_step, eval_2_episode_step_baseline_second_stop_step, \
        eval_2_episode_snort_severe_baseline_third_stop_step, \
        eval_2_episode_snort_warning_baseline_third_stop_step, eval_2_episode_snort_critical_baseline_third_stop_step, \
        eval_2_episode_var_log_baseline_third_stop_step, eval_2_episode_step_baseline_third_stop_step, \
        eval_2_episode_snort_severe_baseline_fourth_stop_step, \
        eval_2_episode_snort_warning_baseline_fourth_stop_step, eval_2_episode_snort_critical_baseline_fourth_stop_step, \
        eval_2_episode_var_log_baseline_fourth_stop_step, eval_2_episode_step_baseline_fourth_stop_step, \
        eval_2_episode_snort_severe_baseline_stops_remaining, \
        eval_2_episode_snort_warning_baseline_stops_remaining, eval_2_episode_snort_critical_baseline_stops_remaining, \
        eval_2_episode_var_log_baseline_stops_remaining, eval_2_episode_step_baseline_stops_remaining, \
        eval_2_optimal_first_stop_step, eval_2_optimal_second_stop_step, eval_2_optimal_third_stop_step, \
        eval_2_optimal_fourth_stop_step, eval_2_optimal_stops_remaining, eval_2_optimal_defender_episode_steps = \
            rewards, steps, uncaught_intrusion_steps_l, opt_r_l, \
            snort_severe_r, snort_warning_r, snort_critical_r, \
            var_log_r, step_r, snort_severe_steps_l, snort_warning_steps_l, \
            snort_critical_steps_l, var_log_steps_l, step_steps_l, \
            snort_severe_ca, snort_warning_ca, snort_critical_ca, var_log_ca, step_ca, \
            snort_severe_es, snort_warning_es, snort_critical_es, var_log_es, step_es, \
            snort_severe_uit, snort_warning_uit, snort_critical_uit, var_log_uit, step_uit, \
            flags_list, flags_percentage_list, episode_caught_list, episode_early_stopped_list, \
            episode_successful_intrusion_list, attacker_cost_list, attacker_cost_norm_list, attacker_alerts_list, \
            attacker_alerts_norm_list, intrusion_steps, model_stopping_times_1, model_stopping_times_2, \
            model_stopping_times_3, model_stopping_times_4, stops_remaining_l, \
            snort_severe_stop_1, snort_warning_stop_1, snort_critical_stop_1, var_log_stop_1, step_stop_1, \
            snort_severe_stop_2, snort_warning_stop_2, snort_critical_stop_2, var_log_stop_2, step_stop_2, \
            snort_severe_stop_3, snort_warning_stop_3, snort_critical_stop_3, var_log_stop_3, step_stop_3, \
            snort_severe_stop_4, snort_warning_stop_4, snort_critical_stop_4, var_log_stop_4, step_stop_4, \
            snort_severe_stops_remaining_l, snort_warning_stops_remaining_l, snort_critical_stops_remaining_l, \
            var_log_stops_remaining_l, step_stops_remaining_l, optimal_stop_1, optimal_stop_2, optimal_stop_3, \
            optimal_stop_4, optimal_stops_remaining_l, optimal_steps

        train_log_dto.defender_eval_2_episode_rewards = eval_2_defender_episode_rewards
        train_log_dto.eval_2_episode_steps = eval_2_episode_steps
        train_log_dto.eval_2_episode_snort_severe_baseline_rewards = eval_2_episode_snort_severe_baseline_rewards
        train_log_dto.eval_2_episode_snort_warning_baseline_rewards = eval_2_episode_snort_warning_baseline_rewards
        train_log_dto.eval_2_episode_snort_critical_baseline_rewards = eval_2_episode_snort_critical_baseline_rewards
        train_log_dto.eval_2_episode_var_log_baseline_rewards = eval_2_episode_var_log_baseline_rewards
        train_log_dto.eval_2_episode_step_baseline_rewards = eval_2_episode_step_baseline_rewards
        train_log_dto.eval_2_episode_snort_severe_baseline_steps = eval_2_episode_snort_severe_baseline_steps
        train_log_dto.eval_2_episode_snort_warning_baseline_steps = eval_2_episode_snort_warning_baseline_steps
        train_log_dto.eval_2_episode_snort_critical_baseline_steps = eval_2_episode_snort_critical_baseline_steps
        train_log_dto.eval_2_episode_var_log_baseline_steps = eval_2_episode_var_log_baseline_steps
        train_log_dto.eval_2_episode_step_baseline_steps = eval_2_episode_step_baseline_steps
        train_log_dto.eval_2_episode_snort_severe_baseline_caught_attacker = eval_2_episode_snort_severe_baseline_caught_attacker
        train_log_dto.eval_2_episode_snort_warning_baseline_caught_attacker = eval_2_episode_snort_warning_baseline_caught_attacker
        train_log_dto.eval_2_episode_snort_critical_baseline_caught_attacker = eval_2_episode_snort_critical_baseline_caught_attacker
        train_log_dto.eval_2_episode_var_log_baseline_caught_attacker = eval_2_episode_var_log_baseline_caught_attacker
        train_log_dto.eval_2_episode_step_baseline_caught_attacker = eval_2_episode_step_baseline_caught_attacker
        train_log_dto.eval_2_episode_snort_severe_baseline_early_stopping = eval_2_episode_snort_severe_baseline_early_stopping
        train_log_dto.eval_2_episode_snort_warning_baseline_early_stopping = eval_2_episode_snort_warning_baseline_early_stopping
        train_log_dto.eval_2_episode_snort_critical_baseline_early_stopping = eval_2_episode_snort_critical_baseline_early_stopping
        train_log_dto.eval_2_episode_var_log_baseline_early_stopping = eval_2_episode_var_log_baseline_early_stopping
        train_log_dto.eval_2_episode_step_baseline_early_stopping = eval_2_episode_step_baseline_early_stopping
        train_log_dto.eval_2_episode_snort_severe_baseline_uncaught_intrusion_steps = eval_2_episode_snort_severe_baseline_uncaught_intrusion_steps
        train_log_dto.eval_2_episode_snort_warning_baseline_uncaught_intrusion_steps = eval_2_episode_snort_warning_baseline_uncaught_intrusion_steps
        train_log_dto.eval_2_episode_snort_critical_baseline_uncaught_intrusion_steps = eval_2_episode_snort_critical_baseline_uncaught_intrusion_steps
        train_log_dto.eval_2_episode_var_log_baseline_uncaught_intrusion_steps = eval_2_episode_var_log_baseline_uncaught_intrusion_steps
        train_log_dto.eval_2_episode_step_baseline_uncaught_intrusion_steps = eval_2_episode_step_baseline_uncaught_intrusion_steps
        train_log_dto.eval_2_episode_flags = eval_2_flags_list
        train_log_dto.eval_2_episode_flags_percentage = eval_2_flags_percentage_list
        train_log_dto.eval_2_episode_caught = eval_2_episode_caught_list
        train_log_dto.eval_2_episode_early_stopped = eval_2_episode_early_stopped_list
        train_log_dto.eval_2_episode_successful_intrusion = eval_2_episode_successful_intrusion_list
        train_log_dto.eval_2_attacker_action_costs = eval_2_attacker_cost_list
        train_log_dto.eval_2_attacker_action_costs_norm = eval_2_attacker_cost_norm_list
        train_log_dto.eval_2_attacker_action_alerts = eval_2_attacker_alerts_list
        train_log_dto.eval_2_attacker_action_alerts_norm = eval_2_attacker_alerts_norm_list
        train_log_dto.eval_2_episode_intrusion_steps = eval_2_episode_intrusion_steps
        train_log_dto.eval_2_uncaught_intrusion_steps = eval_2_uncaught_intrusion_steps
        train_log_dto.eval_2_optimal_defender_reward = eval_2_optimal_defender_reward
        train_log_dto.eval_2_defender_first_stop_step = eval_2_defender_first_stop_step
        train_log_dto.eval_2_defender_second_stop_step = eval_2_defender_second_stop_step
        train_log_dto.eval_2_defender_third_stop_step = eval_2_defender_third_stop_step
        train_log_dto.eval_2_defender_fourth_stop_step = eval_2_defender_fourth_stop_step
        train_log_dto.eval_2_defender_stops_remaining = eval_2_defender_stops_remaining
        train_log_dto.eval_2_episode_snort_severe_baseline_first_stop_step = eval_2_episode_snort_severe_baseline_first_stop_step
        train_log_dto.eval_2_episode_snort_warning_baseline_first_stop_step = eval_2_episode_snort_warning_baseline_first_stop_step
        train_log_dto.eval_2_episode_snort_critical_baseline_first_stop_step = eval_2_episode_snort_critical_baseline_first_stop_step
        train_log_dto.eval_2_episode_var_log_baseline_first_stop_step = eval_2_episode_var_log_baseline_first_stop_step
        train_log_dto.eval_2_episode_step_baseline_first_stop_step = eval_2_episode_step_baseline_first_stop_step
        train_log_dto.eval_2_episode_snort_severe_baseline_second_stop_step = eval_2_episode_snort_severe_baseline_second_stop_step
        train_log_dto.eval_2_episode_snort_warning_baseline_second_stop_step = eval_2_episode_snort_warning_baseline_second_stop_step
        train_log_dto.eval_2_episode_snort_critical_baseline_second_stop_step = eval_2_episode_snort_critical_baseline_second_stop_step
        train_log_dto.eval_2_episode_var_log_baseline_second_stop_step = eval_2_episode_var_log_baseline_second_stop_step
        train_log_dto.eval_2_episode_step_baseline_second_stop_step = eval_2_episode_step_baseline_second_stop_step
        train_log_dto.eval_2_episode_snort_severe_baseline_third_stop_step = eval_2_episode_snort_severe_baseline_third_stop_step
        train_log_dto.eval_2_episode_snort_warning_baseline_third_stop_step = eval_2_episode_snort_warning_baseline_third_stop_step
        train_log_dto.eval_2_episode_snort_critical_baseline_third_stop_step = eval_2_episode_snort_critical_baseline_third_stop_step
        train_log_dto.eval_2_episode_var_log_baseline_third_stop_step = eval_2_episode_var_log_baseline_third_stop_step
        train_log_dto.eval_2_episode_step_baseline_third_stop_step = eval_2_episode_step_baseline_third_stop_step
        train_log_dto.eval_2_episode_snort_severe_baseline_fourth_stop_step = eval_2_episode_snort_severe_baseline_fourth_stop_step
        train_log_dto.eval_2_episode_snort_warning_baseline_fourth_stop_step = eval_2_episode_snort_warning_baseline_fourth_stop_step
        train_log_dto.eval_2_episode_snort_critical_baseline_fourth_stop_step = eval_2_episode_snort_critical_baseline_fourth_stop_step
        train_log_dto.eval_2_episode_var_log_baseline_fourth_stop_step = eval_2_episode_var_log_baseline_fourth_stop_step
        train_log_dto.eval_2_episode_step_baseline_fourth_stop_step = eval_2_episode_step_baseline_fourth_stop_step
        train_log_dto.eval_2_episode_snort_severe_baseline_stops_remaining = eval_2_episode_snort_severe_baseline_stops_remaining
        train_log_dto.eval_2_episode_snort_warning_baseline_stops_remaining = eval_2_episode_snort_warning_baseline_stops_remaining
        train_log_dto.eval_2_episode_snort_critical_baseline_stops_remaining = eval_2_episode_snort_critical_baseline_stops_remaining
        train_log_dto.eval_2_episode_var_log_baseline_stops_remaining = eval_2_episode_var_log_baseline_stops_remaining
        train_log_dto.eval_2_episode_step_baseline_stops_remaining = eval_2_episode_step_baseline_stops_remaining
        train_log_dto.eval_2_optimal_first_stop_step = eval_2_optimal_first_stop_step
        train_log_dto.eval_2_optimal_second_stop_step = eval_2_optimal_second_stop_step
        train_log_dto.eval_2_optimal_third_stop_step = eval_2_optimal_third_stop_step
        train_log_dto.eval_2_optimal_fourth_stop_step = eval_2_optimal_fourth_stop_step
        train_log_dto.eval_2_optimal_stops_remaining = eval_2_optimal_stops_remaining
        train_log_dto.eval_2_optimal_defender_episode_steps = eval_2_optimal_defender_episode_steps

        return train_log_dto


    @staticmethod
    def get_observations_prior_to_intrusion(env : "CSLECTFEnv", intrusion_start_time : int):
        """
        Get list of observations for the defender before the intrusion has started

        :param env: the environment
        :param intrusion_start_time: the intrusion start time
        :return: the list of observations
        """
        defender_dynamics_model = env.env_config.network_conf.defender_dynamics_model
        fx = defender_dynamics_model.norm_num_new_severe_alerts[(85, '172.18.9.191')]
        fy = defender_dynamics_model.norm_num_new_warning_alerts[(85, '172.18.9.191')]
        x,y,z = 0,0,0
        t = 1
        if env.env_config.multiple_stopping_environment:
            obs_l = [[0, 0, 0, t, env.env_config.maximum_number_of_defender_stop_actions]]
        else:
            obs_l = [[0, 0, 0, t]]
        for i in range(0, intrusion_start_time-1):
            t +=1
            x_delta = fx.rvs(size=1)[0]
            y_delta = fy.rvs(size=1)[0]
            x += x_delta
            y += y_delta
            if env.env_config.multiple_stopping_environment:
                obs_l.append([x, y, z, t, env.env_config.maximum_number_of_defender_stop_actions])
            else:
                obs_l.append([x, y, z, t])

        return obs_l

    @staticmethod
    def is_correct_attacker(tau, env) -> bool:
        """
        Checks if the trajectory was generated using the correct attacker and environment configuration for eval

        :param tau: the trajectory
        :param env: the environment
        :return: True if the attacker is correct, false otherwise
        """
        if (tau.attacker_actions[0] == -1
                and tau.attacker_actions[1] == env.env_config.attacker_static_opponent.continue_action
                and tau.attacker_actions[2] == env.env_config.attacker_static_opponent.strategy[0]
                and tau.attacker_actions[3] == env.env_config.attacker_static_opponent.strategy[1]
                and tau.attacker_actions[4] == env.env_config.attacker_static_opponent.strategy[2]
                and tau.attacker_actions[5] == env.env_config.attacker_static_opponent.strategy[3]
        ):
            return True
        return False

    @staticmethod
    def merge_observations(obs_prior_to_intrusion, tau: Trajectory, env_config: CSLEEnvConfig) -> Tuple[List[int], List[List[int]]]:
        """
        Merges observations sampled before the intrusion started with observations sampled afterwards

        :param obs_prior_to_intrusion: the observations sampled before the intrusion
        :param tau: the trajectory of the observations when the intrusion has started
        :param env_config: the environment configuration
        :return: The final observation and the complete list of defender observations
        """
        obs_intrusion = []
        for i in range(len(tau.defender_observations)):
            if not (tau.attacker_actions[i] == -1 or tau.attacker_actions[i] == 372):
                obs_intrusion.append(tau.defender_observations[i])

        prior_intrusion_len = len(obs_prior_to_intrusion)
        obs = obs_prior_to_intrusion
        x = obs_prior_to_intrusion[-1][0]
        y = obs_prior_to_intrusion[-1][1]
        z = obs_prior_to_intrusion[-1][2]
        for i in range(len(obs_intrusion)-1):
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
            if env_config.multiple_stopping_environment:
                obs.append([x,y,z,t, env_config.maximum_number_of_defender_stop_actions])
            else:
                obs.append([x, y, z, t])
        return obs, obs_intrusion

    @staticmethod
    def find_stopping_indexes(actions, env_config : CSLEEnvConfig) -> int:
        """
        Find the stopping idx of the model

        :param actions: the actions predicted by the model
        :param env_config: the environment configuraton
        :return: the stopping idx (-1 if never stop)
        """
        stops_remaining = env_config.maximum_number_of_defender_stop_actions
        stop_indexes = np.empty(env_config.maximum_number_of_defender_stop_actions)
        stop_indexes.fill(-1)
        for i in range(len(actions)):
            if actions[i] == 0 and stops_remaining > 0:
                stop_indexes[env_config.maximum_number_of_defender_stop_actions-stops_remaining] = i
                stops_remaining -= 1
        return stop_indexes

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
    def compute_reward(actions, env_config, optimal_stopping_indexes : List[int], steps: int = 100,
                       intrusion_time: int = 6) \
            -> Tuple[int, bool, bool, bool, int, int]:
        """
        Utility function for computing the reward of a sequence of actions of the defender

        :param actions: the sequence of actions of the defender
        :param env_config: the environment config
        :param optimal_stopping_indexes: the optimal stopping times
        :param steps: episode length
        :return: the reward
        """
        stopping_indexes = EvalUtil.find_stopping_indexes(actions, env_config=env_config)

        r, caught_attacker, early_stopping, uncaught_intrusion_steps, stopping_indexes, succ_intrusion = \
            EvalUtil.stopping_reward(
            stopping_indexes=stopping_indexes, episode_length=steps,
            optimal_stopping_indexes=optimal_stopping_indexes,
            env_config=env_config, intrusion_time=intrusion_time)

        return r, early_stopping, succ_intrusion, caught_attacker, uncaught_intrusion_steps, stopping_indexes

    @staticmethod
    def compute_steps(actions, env_config: CSLEEnvConfig) -> int:
        """
        Utility function for computing the steps in the environment of a sequence of actions of the defender

        :param actions: the sequence of actions of the defender
        :param env_config: env_config
        :return: The number of steps
        """
        stopping_indexes = EvalUtil.find_stopping_indexes(actions, env_config=env_config)
        if stopping_indexes[-1] == -1:
            return len(actions)
        else:
            return stopping_indexes[-1]

    @staticmethod
    def compute_steps_baseline(obs, stopping_indexes) -> int:
        """
        Utility function for computing the steps in the environment of a baseline

        :param obs: the list of observations of the episode
        :param stopping_indexes: the stopping indexes
        :return: The number of steps
        """
        if stopping_indexes[-1] == -1:
            return len(obs)
        else:
            return stopping_indexes[-1]

    @staticmethod
    def compute_stops_remaining(stopping_indexes : List[int]) -> int:
        """
        Utility function for computing the number of stops remaning for the defender

        :param stopping_indexes: the sequence of actions of the defender
        :return: The number of stops remaining
        """
        stops_remaining = len(list(filter(lambda x: x == -1, stopping_indexes)))
        return stops_remaining


    @staticmethod
    def compute_stopping_times(actions, env_config: CSLEEnvConfig) -> int:
        """
        Utility function for computing the stopping times in the environment of a sequence of actions of the defender

        :param actions: the sequence of actions of the defender
        :param env_config: env_config
        :return: The number of steps
        """
        stopping_indexes = EvalUtil.find_stopping_indexes(actions, env_config=env_config)
        return stopping_indexes

    @staticmethod
    def compute_info_metrics(actions, trajectory: Trajectory, env_config : CSLEEnvConfig) -> int:
        flags = 0
        flags_percentage = 0
        #episode_caught = 0
        #episode_early_stopped = 0
        #episode_successful_intrusion = 0
        attacker_cost = 0
        attacker_cost_norm = 0
        attacker_alerts = 0
        attacker_alerts_norm = 0
        stopping_indexes = EvalUtil.find_stopping_indexes(actions, env_config=env_config)
        for i in range(len(trajectory.infos)):
            if i == stopping_indexes[-1] or trajectory.dones[i]:
                if i > 0:
                    flags = trajectory.infos[i]["flags"]
                    flags_percentage = flags / env_config.num_flags
                    #episode_caught = trajectory.infos[i]["caught_attacker"]
                    #episode_early_stopped = trajectory.infos[i]["episode_early_stopped"]
                    #episode_successful_intrusion = trajectory.infos[i]["successful_intrusion"]
                    attacker_cost = trajectory.infos[i][constants.INFO_DICT.ATTACKER_COST]
                    attacker_cost_norm = trajectory.infos[i][constants.INFO_DICT.ATTACKER_COST_NORM]
                    attacker_alerts = trajectory.infos[i][constants.INFO_DICT.ATTACKER_ALERTS]
                    attacker_alerts_norm = trajectory.infos[i][constants.INFO_DICT.ATTACKER_ALERTS_NORM]
                    break
                else:
                    break
        return flags, flags_percentage, attacker_cost, attacker_cost_norm, attacker_alerts, attacker_alerts_norm

    @staticmethod
    def compute_snort_warning_baseline(tau, env_config, optimal_stopping_indexes: List[int], steps : int = 100,
                                       intrusion_time : int = 6) \
            -> Tuple[int, bool, bool, int, int]:
        """
        Utility function for computing the reward of the snort warning baseline

        :param tau: the trajectory of observations
        :param env_config: the environment configuration
        :param steps: number of steps of the episode
        :return: the reward
        """
        stopping_thresh = env_config.snort_warning_baseline_threshold
        stopping_indexes = np.empty(env_config.maximum_number_of_defender_stop_actions)
        stopping_indexes.fill(-1)
        prev_stop_val = 0
        stops_remaining = env_config.maximum_number_of_defender_stop_actions
        for i in range(len(tau)):
            if (tau[i][1]-prev_stop_val) > stopping_thresh and stops_remaining > 0:
                stopping_indexes[env_config.maximum_number_of_defender_stop_actions - stops_remaining] = i
                stops_remaining -= 1
                prev_stop_val = tau[i][1]

        return EvalUtil.stopping_reward(
            stopping_indexes=stopping_indexes, episode_length=steps, optimal_stopping_indexes=optimal_stopping_indexes,
            env_config=env_config, intrusion_time=intrusion_time)

    @staticmethod
    def compute_snort_severe_baseline(tau, env_config, optimal_stopping_indexes: int = 6, steps : int = 100,
                                      intrusion_time: int = 6) \
            -> Tuple[int, bool, bool, int, int]:
        """
        Utility function for computing the reward of the snort severe baseline

        :param tau: the trajectory
        :param env_config: the environment configuration
        :param steps: number of steps of the episode
        :return: the reward
        """
        stopping_thresh = env_config.snort_severe_baseline_threshold
        stopping_indexes = np.empty(env_config.maximum_number_of_defender_stop_actions)
        stopping_indexes.fill(-1)
        prev_stop_val = 0
        stops_remaining = env_config.maximum_number_of_defender_stop_actions
        for i in range(len(tau)):
            if (tau[i][0] - prev_stop_val) > stopping_thresh and stops_remaining > 0:
                stopping_indexes[env_config.maximum_number_of_defender_stop_actions - stops_remaining] = i
                stops_remaining -= 1
                prev_stop_val = tau[i][0]

        return EvalUtil.stopping_reward(
            stopping_indexes=stopping_indexes, episode_length=steps, optimal_stopping_indexes=optimal_stopping_indexes,
            env_config=env_config, intrusion_time=intrusion_time)

    @staticmethod
    def compute_snort_critical_baseline(tau, env_config, optimal_stopping_indexes: List[int], steps : int = 100,
                                        intrusion_time: int = 6)\
            -> Tuple[int, bool, bool, int, int]:
        """
        Utility function for computing the reward of the snort critical baseline

        :param tau: the trajectory
        :param env_config: the environment configuration
        :param steps: number of steps of the episode
        :return: the reward
        """
        stopping_thresh = env_config.snort_critical_baseline_threshold
        stopping_indexes = np.empty(env_config.maximum_number_of_defender_stop_actions)
        stopping_indexes.fill(-1)
        prev_stop_val = 0
        stops_remaining = env_config.maximum_number_of_defender_stop_actions
        for i in range(len(tau)):
            if (tau[i][0] - prev_stop_val) > stopping_thresh and stops_remaining > 0:
                stopping_indexes[env_config.maximum_number_of_defender_stop_actions-stops_remaining] = i
                stops_remaining -= 1
                prev_stop_val = tau[0][1]

        return EvalUtil.stopping_reward(
            stopping_indexes=stopping_indexes, episode_length=steps, optimal_stopping_indexes=optimal_stopping_indexes,
            env_config=env_config, intrusion_time=intrusion_time)

    @staticmethod
    def compute_var_log_baseline(tau, env_config, optimal_stopping_indexes: List[int] = 6, steps: int = 100,
                                 intrusion_time: int = 6) \
            -> Tuple[int, bool, bool, int, int]:
        """
        Utility function for computing the reward of the var_log baseline

        :param tau: the trajectory
        :param env_config: the environment configuration
        :param steps: number of steps of the episode
        :return: the reward
        """
        stopping_thresh = env_config.var_log_baseline_threshold
        stopping_indexes = np.empty(env_config.maximum_number_of_defender_stop_actions)
        stopping_indexes.fill(-1)
        prev_stop_val = 0
        stops_remaining = env_config.maximum_number_of_defender_stop_actions
        for i in range(len(tau)):
            if (tau[i][2] - prev_stop_val) > stopping_thresh and stops_remaining > 0:
                stopping_indexes[env_config.maximum_number_of_defender_stop_actions - stops_remaining] = i
                stops_remaining -= 1
                prev_stop_val = tau[i][2]

        return EvalUtil.stopping_reward(
            stopping_indexes=stopping_indexes, episode_length=steps, optimal_stopping_indexes=optimal_stopping_indexes,
            env_config=env_config, intrusion_time=intrusion_time)

    @staticmethod
    def compute_step_baseline(tau, env_config, optimal_stopping_indexes: List[int], steps: int = 100,
                              intrusion_time: int = 6) \
            -> Tuple[int, bool, bool, int, int]:
        """
        Utility function for computing the reward of the step baseline

        :param tau: the trajectory
        :param env_config: the environment configuration
        :param steps: number of steps of the episode
        :return: the reward
        """
        stopping_indexes = np.empty(env_config.maximum_number_of_defender_stop_actions)
        stopping_indexes.fill(-1)
        for i in range(0, len(stopping_indexes)):
            stopping_indexes[i] = env_config.step_baseline_threshold - (len(stopping_indexes)-i)+1

        return EvalUtil.stopping_reward(
            stopping_indexes=stopping_indexes, episode_length=steps, optimal_stopping_indexes=optimal_stopping_indexes,
            env_config=env_config, intrusion_time=intrusion_time)


    @staticmethod
    def predict(policy, obs, env, deterministic: bool = False, intrusion_prevented_obs = None) -> Tuple[List[int], List[float]]:
        """
        Utility function for predicting the next action given a model, an environment, and a observation

        :param policy: the policy
        :param obs: the observation from the environment
        :param env: the environment
        :param deterministic: whether to do deterministic predictions or not
        :param intrusion_prevented_obs: observations when intrusion has been prevented
        :return: the predicted action and values
        """
        stops_left = obs[0][-1]
        actions_l = []
        values_l = []
        stop_subtract_1 = [0,0,0]
        stop_subtract_2 = [0, 0, 0]
        for i in range(len(obs)):
            obs_temp_1 = np.copy(obs[i])
            obs_temp_1[0] = obs_temp_1[0] - stop_subtract_1[0]
            obs_temp_1[1] = obs_temp_1[1] - stop_subtract_1[1]
            obs_temp_1[2] = obs_temp_1[2] - stop_subtract_1[2]
            obs_temp_1[-1]= stops_left

            obs_temp_2 = np.copy(intrusion_prevented_obs[i])
            obs_temp_2[0] = obs_temp_2[0] - stop_subtract_2[0]
            obs_temp_2[1] = obs_temp_2[1] - stop_subtract_2[1]
            obs_temp_2[2] = obs_temp_2[2] - stop_subtract_2[2]
            obs_temp_2[-1] = stops_left

            if stops_left == env.env_config.maximum_number_of_defender_stop_actions:
                obs_temp_1[0]= -1
                obs_temp_1[1] = -1
                obs_temp_1[2] = -1
                obs_temp_2[0] = -1
                obs_temp_2[1] = -1
                obs_temp_2[2] = -1

            if stops_left > env.env_config.attacker_prevented_stops_remaining:
                obs_tensor_i = torch.as_tensor([obs_temp_1])
            else:
                obs_tensor_i = torch.as_tensor([obs_temp_2])

            actions, values = policy.predict(obs_tensor_i, None, None, deterministic=deterministic,
                                             env_config=env.env_config,
                                             env_state=env.env_state, env_configs=None,
                                             env=env, infos={}, env_idx=0, mask_actions=None,
                                             attacker=False)
            if actions[0] == 0 and stops_left > 0:
                stops_left -= 1
                temp_1 = np.copy(obs_temp_1)
                stop_subtract_1[0] = temp_1[0] + stop_subtract_1[0]
                stop_subtract_1[1] = temp_1[1] + stop_subtract_1[1]
                stop_subtract_1[2] = temp_1[2] + stop_subtract_1[2]
                temp_2 = np.copy(obs_temp_2)
                stop_subtract_2[0] = temp_2[0] + stop_subtract_2[0]
                stop_subtract_2[1] = temp_2[1] + stop_subtract_2[1]
                stop_subtract_2[2] = temp_2[2] + stop_subtract_2[2]
            actions_l.append(actions[0])
            if values is not None:
                values_l.append(values[0])
            else:
                values_l.append(None)
        return actions_l, values_l


    @staticmethod
    def stopping_reward(stopping_indexes, episode_length, optimal_stopping_indexes, env_config, intrusion_time: int) \
            -> Tuple[int, bool, bool, int, int, bool]:
        """
        Computes the reward of stopping at stopping_idx

        :param stopping_indexes: the stopping time
        :param episode_length: the episode length
        :param optimal_stopping_indexes: the optimal stopping time
        :param env_config: the environment configuration
        :param intrusion_time: the time of the intrusion
        :return: the defender reward, caught_attacker, early_stopping, uncaught_intrusion_steps, stopping_indexes,
                 succ_intrusion
        """
        caught_attacker = False
        early_stopping = False
        uncaught_intrusion_steps = 0
        r = 0

        agent_costs = 0
        agent_final_stop_idx = stopping_indexes[-1]
        agent_stop_prevent_attacker_idx = stopping_indexes[
            env_config.maximum_number_of_defender_stop_actions-1
            -max(0, env_config.attacker_prevented_stops_remaining)]
        for i in range(env_config.maximum_number_of_defender_stop_actions-1, -1, -1):
            if stopping_indexes[i] == -1:
                break
            agent_costs += env_config.multistop_costs[i]

        optimal_final_stop_idx = optimal_stopping_indexes[-1]
        optimal_stop_prevent_attacker_idx = optimal_stopping_indexes[
            env_config.maximum_number_of_defender_stop_actions-1 - env_config.attacker_prevented_stops_remaining]
        optimal_costs = 0
        for i in range(env_config.maximum_number_of_defender_stop_actions-1, -1, -1):
            optimal_costs += env_config.multistop_costs[i]
            if i == env_config.attacker_prevented_stops_remaining:
                break

        stops_remaining = 4
        agent_costs = 0
        agent_service_reward = 0
        agent_caught_reward = 0
        agent_intrusion_reward = 0
        num_service_steps = 0
        for i in range(episode_length-1):
            if stops_remaining > 0 \
                    and stopping_indexes[env_config.maximum_number_of_defender_stop_actions-stops_remaining] != -1 \
                    and i == (stopping_indexes[env_config.maximum_number_of_defender_stop_actions-stops_remaining]):
                stops_remaining -= 1
                agent_costs += env_config.multistop_costs[stops_remaining]
                if stops_remaining == env_config.attacker_prevented_stops_remaining:
                    if (i+1) > intrusion_time:
                        agent_caught_reward += env_config.defender_caught_attacker_reward
                        caught_attacker =  True
                        if early_stopping:
                            print("setting CA to true despite ES, stops remaining:{}, prevented stops:{}".format(
                                stops_remaining, env_config.attacker_prevented_stops_remaining))
                    else:
                        early_stopping = True
                        if caught_attacker:
                            print("setting ES to true despite caught A, stops remaining: {}, prevented stops: {}".format(stops_remaining, env_config.attacker_prevented_stops_remaining))
            else:
                if stops_remaining > 0:
                    agent_service_reward += env_config.defender_service_reward/(math.pow(2, env_config.maximum_number_of_defender_stop_actions-stops_remaining))
                    num_service_steps += 1
                    if stops_remaining > env_config.attacker_prevented_stops_remaining and (i+1) > intrusion_time:
                        agent_intrusion_reward += env_config.defender_intrusion_reward

        r = agent_costs + agent_service_reward + agent_caught_reward + agent_intrusion_reward

        succ_intrusion = agent_stop_prevent_attacker_idx == -1
        # print("stopping_indexes:{}, optimal_stopping_indexes:{}, r:{}, intrusion_time:{}, agent_costs:{}, "
        #       "agent_service_reward:{}, agent_intrusion_loss:{}, agent_attacker_caught_reward:{},"
        #       "optimal_stop_prevent_attacker_idx:{}, episode length:{}, successful_intrusion:{}, num_service_steps:{}, "
        #       "early_stopping:{}, caught:{}".format(
        #     stopping_indexes, optimal_stopping_indexes, r, intrusion_time, agent_costs, agent_service_reward,
        #     agent_intrusion_reward, agent_caught_reward, optimal_final_stop_idx, episode_length, succ_intrusion,
        #     num_service_steps, early_stopping, caught_attacker))

        uncaught_intrusion_steps = max(0, agent_stop_prevent_attacker_idx - intrusion_time)
        #print(f"uuit:{uncaught_intrusion_steps}, intrusion time:{intrusion_time}, stop time:{agent_stop_prevent_attacker_idx}")

        # if stopping_indexes < optimal_stopping_indexes:
        #     r = env_config.defender_service_reward * (stopping_indexes - 1)
        #     r = r + env_config.defender_early_stopping_reward
        #     early_stopping = True
        #
        # if stopping_indexes == -1:
        #     r = env_config.defender_service_reward * (optimal_stopping_indexes - 1)
        #     r = r + env_config.defender_intrusion_reward * (episode_length - optimal_stopping_indexes)
        #
        # if stopping_indexes >= optimal_stopping_indexes:
        #     r = env_config.defender_service_reward * (optimal_stopping_indexes - 1)
        #     r = r + env_config.defender_intrusion_reward * (stopping_indexes - optimal_stopping_indexes)
        #     r = r + env_config.defender_caught_attacker_reward
        #     caught_attacker = True
        #     uncaught_intrusion_steps = max(0, stopping_indexes - optimal_stopping_indexes)

        return r, caught_attacker, early_stopping, uncaught_intrusion_steps, stopping_indexes, succ_intrusion
