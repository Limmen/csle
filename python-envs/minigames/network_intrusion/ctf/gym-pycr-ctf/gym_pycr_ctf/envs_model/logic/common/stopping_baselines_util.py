import numpy as np
from gym_pycr_ctf.dao.network.env_state import EnvState
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.agents.bots.custom_attacker_bot_agent import CustomAttackerBotAgent
from gym_pycr_ctf.envs_model.logic.transition_operator import TransitionOperator

class StoppingBaselinesUtil:
    """
    Class containing utility functions for computing metrics of baselines for Optimal Stopping
    """

    @staticmethod
    def compute_baseline_metrics(s: EnvState, s_prime: EnvState, env_config: EnvConfig):
        StoppingBaselinesUtil.snort_severe_baseline(s=s, s_prime=s_prime, env_config=env_config)
        StoppingBaselinesUtil.snort_warning_baseline(s=s, s_prime=s_prime, env_config=env_config)
        StoppingBaselinesUtil.snort_critical_baseline(s=s, s_prime=s_prime, env_config=env_config)
        StoppingBaselinesUtil.var_log_baseline(s=s, s_prime=s_prime, env_config=env_config)
        StoppingBaselinesUtil.step_baseline(s=s, s_prime=s_prime, env_config=env_config)


    @staticmethod
    def snort_severe_baseline(s: EnvState, s_prime: EnvState, env_config: EnvConfig):
        if not s_prime.defender_obs_state.snort_severe_baseline_stopped:
            if s_prime.defender_obs_state.num_severe_alerts_total > env_config.snort_severe_baseline_threshold:
                s_prime.defender_obs_state.snort_severe_baseline_stopped = True
                s_prime.defender_obs_state.snort_severe_baseline_step = s_prime.defender_obs_state.step
                if s.attacker_obs_state.ongoing_intrusion():
                    s_prime.defender_obs_state.snort_severe_baseline_reward += env_config.defender_caught_attacker_reward
                else:
                    s_prime.defender_obs_state.snort_severe_baseline_reward += env_config.defender_early_stopping_reward
            else:
                s_prime.defender_obs_state.snort_severe_baseline_reward += env_config.defender_service_reward
                if s.attacker_obs_state.ongoing_intrusion():
                    s_prime.defender_obs_state.snort_severe_baseline_reward += env_config.defender_intrusion_reward

    @staticmethod
    def snort_warning_baseline(s: EnvState, s_prime: EnvState, env_config: EnvConfig):
        if not s_prime.defender_obs_state.snort_warning_baseline_stopped:
            if s_prime.defender_obs_state.num_warning_alerts_recent > env_config.snort_warning_baseline_threshold:
                s_prime.defender_obs_state.snort_warning_baseline_stopped = True
                s_prime.defender_obs_state.snort_warning_baseline_step = s_prime.defender_obs_state.step
                if s.attacker_obs_state.ongoing_intrusion():
                    s_prime.defender_obs_state.snort_warning_baseline_reward += env_config.defender_caught_attacker_reward
                else:
                    s_prime.defender_obs_state.snort_warning_baseline_reward += env_config.defender_early_stopping_reward
            else:
                s_prime.defender_obs_state.snort_warning_baseline_reward += env_config.defender_service_reward
                if s.attacker_obs_state.ongoing_intrusion():
                    s_prime.defender_obs_state.snort_warning_baseline_reward += env_config.defender_intrusion_reward

    @staticmethod
    def snort_critical_baseline(s: EnvState, s_prime: EnvState, env_config: EnvConfig):
        if not s_prime.defender_obs_state.snort_critical_baseline_stopped:
            if s_prime.defender_obs_state.num_severe_alerts_total > env_config.snort_critical_baseline_threshold:
                s_prime.defender_obs_state.snort_critical_baseline_stopped = True
                s_prime.defender_obs_state.snort_critical_baseline_step = s_prime.defender_obs_state.step
                if s.attacker_obs_state.ongoing_intrusion():
                    s_prime.defender_obs_state.snort_critical_baseline_reward += env_config.defender_caught_attacker_reward
                else:
                    s_prime.defender_obs_state.snort_critical_baseline_reward += env_config.defender_early_stopping_reward
            else:
                s_prime.defender_obs_state.snort_critical_baseline_reward += env_config.defender_service_reward
                if s.attacker_obs_state.ongoing_intrusion():
                    s_prime.defender_obs_state.snort_critical_baseline_reward += env_config.defender_intrusion_reward

    @staticmethod
    def var_log_baseline(s: EnvState, s_prime: EnvState, env_config: EnvConfig):
        if not s_prime.defender_obs_state.var_log_baseline_stopped:
            sum_failed_logins = sum(list(map(lambda x: x.num_failed_login_attempts_recent,
                                             s_prime.defender_obs_state.machines)))
            if sum_failed_logins > env_config.var_log_baseline_threshold:
                s_prime.defender_obs_state.var_log_baseline_stopped = True
                s_prime.defender_obs_state.var_log_baseline_step = s_prime.defender_obs_state.step
                if s.attacker_obs_state.ongoing_intrusion():
                    s_prime.defender_obs_state.var_log_baseline_reward += env_config.defender_caught_attacker_reward
                else:
                    s_prime.defender_obs_state.var_log_baseline_reward += env_config.defender_early_stopping_reward
            else:
                s_prime.defender_obs_state.var_log_baseline_reward += env_config.defender_service_reward
                if s.attacker_obs_state.ongoing_intrusion():
                    s_prime.defender_obs_state.var_log_baseline_reward += env_config.defender_intrusion_reward

    @staticmethod
    def step_baseline(s: EnvState, s_prime: EnvState, env_config: EnvConfig):
        if not s_prime.defender_obs_state.step_baseline_stopped:
            if s_prime.defender_obs_state.step >= env_config.step_baseline_threshold:
                s_prime.defender_obs_state.step_baseline_stopped = True
                s_prime.defender_obs_state.step_baseline_step = env_config.step_baseline_threshold
                if s.attacker_obs_state.ongoing_intrusion():
                    s_prime.defender_obs_state.step_baseline_reward += env_config.defender_caught_attacker_reward
                else:
                    s_prime.defender_obs_state.step_baseline_reward += env_config.defender_early_stopping_reward
            else:
                s_prime.defender_obs_state.step_baseline_reward += env_config.defender_service_reward
                if s.attacker_obs_state.ongoing_intrusion():
                    s_prime.defender_obs_state.step_baseline_reward += env_config.defender_intrusion_reward


    @staticmethod
    def simulate_end_of_episode_performance(s_prime: EnvState, env_config: EnvConfig, done: bool,
                                            attacker_opponent: CustomAttackerBotAgent, env : "PyCRCTFEnv",
                                            s: EnvState):
        if env_config.snort_baseline_simulate and \
                attacker_opponent is not None and \
                (done and (not s_prime.defender_obs_state.snort_severe_baseline_stopped or
                           not s_prime.defender_obs_state.snort_warning_baseline_stopped
                           or not s_prime.defender_obs_state.snort_critical_baseline_stopped
                           or not s_prime.defender_obs_state.var_log_baseline_stopped
                           or not s_prime.defender_obs_state.step_baseline_stopped
                )):
            StoppingBaselinesUtil.simulate_baselines_vs_opponent(
                attacker_opponent=attacker_opponent, env_config=env_config, env=env, s=s)


    @staticmethod
    def simulate_baselines_vs_opponent(attacker_opponent : CustomAttackerBotAgent, env_config: EnvConfig,
                                       env : "PyCRCTFEnv", s: EnvState):
        defender_action = env_config.defender_action_conf.get_continue_action_idx()
        done = False
        i = 0
        while not done:
            i += 1
            attacker_action_id, attacker_done = attacker_opponent.action(
                env=env, filter_illegal=env_config.attacker_filter_illegal_actions)
            if i > 100:
                print("infinite loop..")

            # Prepare action for execution
            attack_action = env_config.attacker_action_conf.actions[attacker_action_id]
            attack_action.ip = s.attacker_obs_state.get_action_ip(attack_action)

            # Step in the environment
            s_prime, attacker_reward, done = TransitionOperator.attacker_transition(
                s=s, attacker_action=attack_action, env_config=env_config)
            done = done or attacker_done
            s = s_prime
            s.attacker_obs_state.last_attacker_action = attack_action

            # Update state
            if env_config.defender_update_state and not done:
                # Update defender's state
                s_prime, _, _ = TransitionOperator.defender_transition(
                    s=s, defender_action=env_config.defender_action_conf.state_update_action,
                    env_config=env_config, attacker_action=s.attacker_obs_state.last_attacker_action)
                s = s_prime

            # Extract observations
            defender_m_obs, defender_network_obs = s.get_defender_observation()
            attacker_m_obs, attacker_p_obs = s.get_attacker_observation()
            attacker_m_obs = np.append(np.array([env.attacker_agent_state.time_step]), attacker_m_obs.flatten())
            defender_obs = np.append(defender_network_obs, defender_m_obs.flatten())
            env.defender_last_obs = defender_obs
            env.attacker_last_obs = attacker_m_obs
            env.defender_time_step += 1
            env.attacker_agent_state.time_step += 1
            if attacker_action_id != 372:
                s.attacker_obs_state.step += 1

            StoppingBaselinesUtil.compute_baseline_metrics(s=s, s_prime=s_prime, env_config=env_config)

            if s_prime.defender_obs_state.snort_severe_baseline_stopped and \
                    s_prime.defender_obs_state.snort_warning_baseline_stopped \
                    and s_prime.defender_obs_state.snort_critical_baseline_stopped \
                    and s_prime.defender_obs_state.var_log_baseline_stopped \
                    and s_prime.defender_obs_state.step_baseline_stopped:
                done = True
            s = s_prime