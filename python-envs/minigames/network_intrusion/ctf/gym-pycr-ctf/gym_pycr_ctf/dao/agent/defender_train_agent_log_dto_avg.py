import numpy as np
import time
import gym_pycr_ctf.envs_model.logic.common.util as pycr_util
from gym_pycr_ctf.agents.config.agent_config import AgentConfig
from gym_pycr_ctf.dao.agent.tensorboard_data_dto import TensorboardDataDTO
from gym_pycr_ctf.dao.agent.train_mode import TrainMode


class DefenderTrainAgentLogDTOAvg:
    """
    DTO with average metrics of the defender for logging during training
    """

    def __init__(self, train_log_dto : "TrainAgentLogDTO", defender_agent_config : AgentConfig = None,
                 env=None, env_2 = None, eval: bool = False, train_mode : TrainMode = TrainMode.TRAIN_DEFENDER):
        """
        Class constructor, initializes the DTO

        :param train_log_dto: the DTO with the data to initialize with
        :param defender_agent_config: the config of the defender agent
        :param env: the environment
        :param env_2: the evaluation environment
        :param eval: whether this is an evaluation run or not
        :param train_mode: the training mode
        """
        self.train_mode = train_mode
        self.defender_agent_config = defender_agent_config
        self.train_log_dto = train_log_dto
        self.env = env
        self.env_2 = env_2
        self.eval = eval
        if not eval:
            self.result = self.train_log_dto.train_result
        else:
            self.result = self.train_log_dto.eval_result

        self.training_time = time.time() - self.train_log_dto.start_time
        self.training_time_hours = self.training_time / 3600

        self.avg_episode_rewards = np.mean(self.train_log_dto.defender_episode_rewards)
        self.avg_episode_steps = np.mean(self.train_log_dto.episode_steps)
        self.avg_episode_snort_severe_baseline_rewards = np.mean(self.train_log_dto.episode_snort_severe_baseline_rewards)
        self.avg_episode_snort_warning_baseline_rewards = np.mean(self.train_log_dto.episode_snort_warning_baseline_rewards)
        self.avg_episode_snort_critical_baseline_rewards = np.mean(self.train_log_dto.episode_snort_critical_baseline_rewards)
        self.avg_episode_var_log_baseline_rewards = np.mean(self.train_log_dto.episode_var_log_baseline_rewards)
        self.avg_episode_step_baseline_rewards = np.mean(self.train_log_dto.episode_step_baseline_rewards)
        self.avg_episode_snort_severe_baseline_steps = np.mean(self.train_log_dto.episode_snort_severe_baseline_steps)
        self.avg_episode_snort_warning_baseline_steps = np.mean(self.train_log_dto.episode_snort_warning_baseline_steps)
        self.avg_episode_snort_critical_baseline_steps = np.mean(self.train_log_dto.episode_snort_critical_baseline_steps)
        self.avg_episode_var_log_baseline_steps = np.mean(self.train_log_dto.episode_var_log_baseline_steps)
        self.avg_episode_step_baseline_steps = np.mean(self.train_log_dto.episode_step_baseline_steps)
        self.avg_episode_intrusion_steps = np.mean(self.train_log_dto.episode_intrusion_steps)
        self.avg_episode_snort_severe_baseline_caught_attacker = np.mean(
            self.train_log_dto.episode_snort_severe_baseline_caught_attacker)
        self.avg_episode_snort_warning_baseline_caught_attacker = np.mean(
            self.train_log_dto.episode_snort_warning_baseline_caught_attacker)
        self.avg_episode_snort_critical_baseline_caught_attacker = np.mean(
            self.train_log_dto.episode_snort_critical_baseline_caught_attacker)
        self.avg_episode_var_log_baseline_caught_attacker = np.mean(self.train_log_dto.episode_var_log_baseline_caught_attacker)
        self.avg_episode_step_baseline_caught_attacker = np.mean(self.train_log_dto.episode_step_baseline_caught_attacker)
        self.avg_episode_snort_severe_baseline_early_stopping = np.mean(
            self.train_log_dto.episode_snort_severe_baseline_early_stopping)
        self.avg_episode_snort_warning_baseline_early_stopping = np.mean(
            self.train_log_dto.episode_snort_warning_baseline_early_stopping)
        self.avg_episode_snort_critical_baseline_early_stopping = np.mean(
            self.train_log_dto.episode_snort_critical_baseline_early_stopping)
        self.avg_episode_var_log_baseline_early_stopping = np.mean(self.train_log_dto.episode_var_log_baseline_early_stopping)
        self.avg_episode_step_baseline_early_stopping = np.mean(self.train_log_dto.episode_step_baseline_early_stopping)
        self.avg_episode_snort_severe_baseline_uncaught_intrusion_steps = DefenderTrainAgentLogDTOAvg.compute_avg_uncaught_intrusion_steps(
            self.train_log_dto.episode_snort_severe_baseline_uncaught_intrusion_steps)
        self.avg_episode_snort_warning_baseline_uncaught_intrusion_steps = DefenderTrainAgentLogDTOAvg.compute_avg_uncaught_intrusion_steps(
            self.train_log_dto.episode_snort_warning_baseline_uncaught_intrusion_steps)
        self.avg_episode_snort_critical_baseline_uncaught_intrusion_steps = DefenderTrainAgentLogDTOAvg.compute_avg_uncaught_intrusion_steps(
            self.train_log_dto.episode_snort_critical_baseline_uncaught_intrusion_steps)
        self.avg_episode_var_log_baseline_uncaught_intrusion_steps = DefenderTrainAgentLogDTOAvg.compute_avg_uncaught_intrusion_steps(
            self.train_log_dto.episode_var_log_baseline_uncaught_intrusion_steps)
        self.avg_episode_step_baseline_uncaught_intrusion_steps = DefenderTrainAgentLogDTOAvg.compute_avg_uncaught_intrusion_steps(
            self.train_log_dto.episode_step_baseline_uncaught_intrusion_steps)
        self.avg_episode_costs = np.mean(self.train_log_dto.attacker_action_costs)
        self.avg_episode_costs_norm = np.mean(self.train_log_dto.attacker_action_costs_norm)
        self.avg_episode_alerts = np.mean(self.train_log_dto.attacker_action_alerts)
        self.avg_episode_alerts_norm = np.mean(self.train_log_dto.attacker_action_alerts_norm)
        self.avg_episode_flags = np.mean(self.train_log_dto.episode_flags)
        self.avg_episode_flags_percentage = np.mean(self.train_log_dto.episode_flags_percentage)
        self.avg_episode_uncaught_intrusion_steps = DefenderTrainAgentLogDTOAvg.compute_avg_uncaught_intrusion_steps(
            self.train_log_dto.uncaught_intrusion_steps)
        self.avg_episode_defender_stops_remaining = np.mean(self.train_log_dto.defender_stops_remaining)
        self.avg_episode_defender_first_stop_step = np.mean(self.train_log_dto.avg_episode_defender_first_stop_step)
        self.avg_episode_defender_second_stop_step = np.mean(self.train_log_dto.avg_episode_defender_second_stop_step)
        self.avg_episode_defender_third_stop_step = np.mean(self.train_log_dto.avg_episode_defender_third_stop_step)
        self.avg_episode_defender_fourth_stop_step = np.mean(self.train_log_dto.avg_episode_defender_fourth_stop_step)

        if self.train_log_dto.episode_caught is not None and self.train_log_dto.episode_early_stopped is not None \
                and self.train_log_dto.episode_successful_intrusion is not None:
            self.total_c_s_i = sum(list(map(lambda x: int(x), self.train_log_dto.episode_caught))) \
                          + sum(list(map(lambda x: int(x), self.train_log_dto.episode_early_stopped))) \
                          + sum(list(map(lambda x: int(x), self.train_log_dto.episode_successful_intrusion)))
        else:
            self.total_c_s_i = 1
        if self.train_log_dto.eval_episode_caught is not None and self.train_log_dto.eval_episode_early_stopped is not None \
                and self.train_log_dto.eval_episode_successful_intrusion is not None:
            self.eval_total_c_s_i = sum(list(map(lambda x: int(x), self.train_log_dto.eval_episode_caught))) \
                               + sum(list(map(lambda x: int(x), self.train_log_dto.eval_episode_early_stopped))) \
                               + sum(list(map(lambda x: int(x), self.train_log_dto.eval_episode_successful_intrusion)))
        else:
            self.eval_total_c_s_i = 1
        if self.train_log_dto.eval_2_episode_caught is not None and self.train_log_dto.eval_2_episode_early_stopped is not None \
                and self.train_log_dto.eval_2_episode_successful_intrusion is not None:
            self.eval_2_total_c_s_i = sum(list(map(lambda x: int(x), self.train_log_dto.eval_2_episode_caught))) \
                                 + sum(list(map(lambda x: int(x), self.train_log_dto.eval_2_episode_early_stopped))) \
                                 + sum(list(map(lambda x: int(x), self.train_log_dto.eval_2_episode_successful_intrusion)))
        else:
            self.eval_2_total_c_s_i = 1
        if self.train_log_dto.episode_caught is not None:
            self.episode_caught_frac = sum(list(map(lambda x: int(x), self.train_log_dto.episode_caught))) / max(1, self.total_c_s_i)
        else:
            self.episode_caught_frac = 0

        if self.train_log_dto.episode_early_stopped is not None:
            self.episode_early_stopped_frac = sum(list(map(lambda x: int(x),
                                                      self.train_log_dto.episode_early_stopped))) / max(1, self.total_c_s_i)
        else:
            self.episode_early_stopped_frac = 0

        if self.train_log_dto.episode_successful_intrusion is not None:
            self.episode_successful_intrusion_frac = sum(list(map(lambda x: int(x),
                                                             self.train_log_dto.episode_successful_intrusion))) / max(1,
                                                                                                                 self.total_c_s_i)
        else:
            self.episode_successful_intrusion_frac = 0

        if self.train_log_dto.eval_episode_caught is not None:
            self.eval_episode_caught_frac = sum(list(map(lambda x: int(x),
                                                    self.train_log_dto.eval_episode_caught))) / max(1, self.eval_total_c_s_i)
        else:
            self.eval_episode_caught_frac = 0

        if self.train_log_dto.eval_episode_successful_intrusion is not None:
            self.eval_episode_successful_intrusion_frac = sum(list(map(lambda x: int(x),
                                                                  self.train_log_dto.eval_episode_successful_intrusion))) / max(
                1, self.eval_total_c_s_i)
        else:
            self.eval_episode_successful_intrusion_frac = 0

        if self.train_log_dto.eval_episode_early_stopped is not None:
            self.eval_episode_early_stopped_frac = sum(list(map(lambda x: int(x),
                                                           self.train_log_dto.eval_episode_early_stopped))) / max(1,
                                                                                                             self.eval_total_c_s_i)
        else:
            self.eval_episode_early_stopped_frac = 0

        if self.train_log_dto.eval_2_episode_caught is not None:
            self.eval_2_episode_caught_frac = sum(list(map(lambda x: int(x),
                                                      self.train_log_dto.eval_2_episode_caught))) / max(1,
                                                                                                   self.eval_2_total_c_s_i)
        else:
            self.eval_2_episode_caught_frac = 0

        if self.train_log_dto.eval_2_episode_successful_intrusion is not None:
            self.eval_2_episode_successful_intrusion_frac = sum(list(map(lambda x: int(x),
                                                                    self.train_log_dto.eval_2_episode_successful_intrusion))) / max(
                1, self.eval_2_total_c_s_i)
        else:
            self.eval_2_episode_successful_intrusion_frac = 0

        if self.train_log_dto.eval_2_episode_early_stopped is not None:
            self.eval_2_episode_early_stopped_frac = sum(list(map(lambda x: int(x),
                                                             self.train_log_dto.eval_2_episode_early_stopped))) / max(1,
                                                                                                                 self.eval_2_total_c_s_i)
        else:
            self.eval_2_episode_early_stopped_frac = 0

        if not eval and self.train_log_dto.eval_episode_flags is not None:
            self.eval_avg_episode_flags = np.mean(self.train_log_dto.eval_episode_flags)
        else:
            self.eval_avg_episode_flags = 0.0
        if not eval and self.train_log_dto.eval_episode_flags_percentage is not None:
            self.eval_avg_episode_flags_percentage = np.mean(self.train_log_dto.eval_episode_flags_percentage)
        else:
            self.eval_avg_episode_flags_percentage = 0.0

        if not eval and self.train_log_dto.eval_2_episode_flags is not None:
            self.eval_2_avg_episode_flags = np.mean(self.train_log_dto.eval_2_episode_flags)
        else:
            self.eval_2_avg_episode_flags = 0.0
        if not eval and self.train_log_dto.eval_2_episode_flags_percentage is not None:
            self.eval_2_avg_episode_flags_percentage = np.mean(self.train_log_dto.eval_2_episode_flags_percentage)
        else:
            self.eval_2_avg_episode_flags_percentage = 0.0

        if not eval and self.train_log_dto.eval_episode_steps is not None:
            self.eval_avg_episode_steps = np.mean(self.train_log_dto.eval_episode_steps)
        else:
            self.eval_avg_episode_steps = 0.0

        if not eval and self.train_log_dto.eval_attacker_action_costs is not None:
            self.eval_avg_episode_costs = np.mean(self.train_log_dto.eval_attacker_action_costs)
        else:
            self.eval_avg_episode_costs = 0.0

        if not eval and self.train_log_dto.eval_attacker_action_costs_norm is not None:
            self.eval_avg_episode_costs_norm = np.mean(self.train_log_dto.eval_attacker_action_costs_norm)
        else:
            self.eval_avg_episode_costs_norm = 0.0

        if not eval and self.train_log_dto.eval_attacker_action_alerts is not None:
            self.eval_avg_episode_alerts = np.mean(self.train_log_dto.eval_attacker_action_alerts)
        else:
            self.eval_avg_episode_alerts = 0.0

        if not eval and self.train_log_dto.eval_attacker_action_alerts_norm is not None:
            self.eval_avg_episode_alerts_norm = np.mean(self.train_log_dto.eval_attacker_action_alerts_norm)
        else:
            self.eval_avg_episode_alerts_norm = 0.0

        if not eval and self.train_log_dto.defender_eval_2_episode_rewards is not None:
            self.eval_2_avg_episode_rewards = np.mean(self.train_log_dto.defender_eval_2_episode_rewards)
        else:
            self.eval_2_avg_episode_rewards = 0.0

        if not eval and self.train_log_dto.eval_2_uncaught_intrusion_steps is not None:
            self.eval_2_avg_episode_uncaught_intrusion_steps = DefenderTrainAgentLogDTOAvg.compute_avg_uncaught_intrusion_steps(
                self.train_log_dto.eval_2_uncaught_intrusion_steps)
        else:
            self.eval_2_avg_episode_uncaught_intrusion_steps = 0.0

        if not eval and self.train_log_dto.eval_2_optimal_defender_reward is not None:
            self.eval_2_avg_episode_optimal_defender_reward = np.mean(self.train_log_dto.eval_2_optimal_defender_reward)
        else:
            self.eval_2_avg_episode_optimal_defender_reward = 0.0

        if not eval and self.train_log_dto.eval_2_episode_snort_severe_baseline_rewards is not None:
            self.eval_2_avg_episode_snort_severe_baseline_rewards = np.mean(
                self.train_log_dto.eval_2_episode_snort_severe_baseline_rewards)
        else:
            self.eval_2_avg_episode_snort_severe_baseline_rewards = 0.0

        if not eval and self.train_log_dto.eval_2_episode_snort_warning_baseline_rewards is not None:
            self.eval_2_avg_episode_snort_warning_baseline_rewards = np.mean(
                self.train_log_dto.eval_2_episode_snort_warning_baseline_rewards)
        else:
            self.eval_2_avg_episode_snort_warning_baseline_rewards = 0.0

        if not eval and self.train_log_dto.eval_2_episode_snort_critical_baseline_rewards is not None:
            self.eval_2_avg_episode_snort_critical_baseline_rewards = np.mean(
                self.train_log_dto.eval_2_episode_snort_critical_baseline_rewards)
        else:
            self.eval_2_avg_episode_snort_critical_baseline_rewards = 0.0

        if not eval and self.train_log_dto.eval_2_episode_var_log_baseline_rewards is not None:
            self.eval_2_avg_episode_var_log_baseline_rewards = np.mean(self.train_log_dto.eval_2_episode_var_log_baseline_rewards)
        else:
            self.eval_2_avg_episode_var_log_baseline_rewards = 0.0

        if not eval and self.train_log_dto.eval_2_episode_step_baseline_rewards is not None:
            self.eval_2_avg_episode_step_baseline_rewards = np.mean(self.train_log_dto.eval_2_episode_step_baseline_rewards)
        else:
            self.eval_2_avg_episode_step_baseline_rewards = 0.0

        if not eval and self.train_log_dto.eval_2_episode_snort_severe_baseline_caught_attacker is not None:
            self.eval_2_avg_episode_snort_severe_baseline_caught_attacker = np.mean(
                self.train_log_dto.eval_2_episode_snort_severe_baseline_caught_attacker)
        else:
            self.eval_2_avg_episode_snort_severe_baseline_caught_attacker = 0.0

        if not eval and self.train_log_dto.eval_2_episode_snort_warning_baseline_caught_attacker is not None:
            self.eval_2_avg_episode_snort_warning_baseline_caught_attacker = np.mean(
                self.train_log_dto.eval_2_episode_snort_warning_baseline_caught_attacker)
        else:
            self.eval_2_avg_episode_snort_warning_baseline_caught_attacker = 0.0

        if not eval and self.train_log_dto.eval_2_episode_snort_critical_baseline_caught_attacker is not None:
            self.eval_2_avg_episode_snort_critical_baseline_caught_attacker = np.mean(
                self.train_log_dto.eval_2_episode_snort_critical_baseline_caught_attacker)
        else:
            self.eval_2_avg_episode_snort_critical_baseline_caught_attacker = 0.0

        if not eval and self.train_log_dto.eval_2_episode_var_log_baseline_caught_attacker is not None:
            self.eval_2_avg_episode_var_log_baseline_caught_attacker = np.mean(
                self.train_log_dto.eval_2_episode_var_log_baseline_caught_attacker)
        else:
            self.eval_2_avg_episode_var_log_baseline_caught_attacker = 0.0

        if not eval and self.train_log_dto.eval_2_episode_step_baseline_caught_attacker is not None:
            self.eval_2_avg_episode_step_baseline_caught_attacker = np.mean(
                self.train_log_dto.eval_2_episode_step_baseline_caught_attacker)
        else:
            self.eval_2_avg_episode_step_baseline_caught_attacker = 0.0
        if not eval and self.train_log_dto.eval_2_episode_snort_severe_baseline_early_stopping is not None:
            self.eval_2_avg_episode_snort_severe_baseline_early_stopping = np.mean(
                self.train_log_dto.eval_2_episode_snort_severe_baseline_early_stopping)
        else:
            self.eval_2_avg_episode_snort_severe_baseline_early_stopping = 0.0

        if not eval and self.train_log_dto.eval_2_episode_snort_warning_baseline_early_stopping is not None:
            self.eval_2_avg_episode_snort_warning_baseline_early_stopping = np.mean(
                self.train_log_dto.eval_2_episode_snort_warning_baseline_early_stopping)
        else:
            self.eval_2_avg_episode_snort_warning_baseline_early_stopping = 0.0

        if not eval and self.train_log_dto.eval_2_episode_snort_critical_baseline_early_stopping is not None:
            self.eval_2_avg_episode_snort_critical_baseline_early_stopping = np.mean(
                self.train_log_dto.eval_2_episode_snort_critical_baseline_early_stopping)
        else:
            self.eval_2_avg_episode_snort_critical_baseline_early_stopping = 0.0

        if not eval and self.train_log_dto.eval_2_episode_var_log_baseline_early_stopping is not None:
            self.eval_2_avg_episode_var_log_baseline_early_stopping = np.mean(
                self.train_log_dto.eval_2_episode_var_log_baseline_early_stopping)
        else:
            self.eval_2_avg_episode_var_log_baseline_early_stopping = 0.0

        if not eval and self.train_log_dto.eval_2_episode_step_baseline_early_stopping is not None:
            self.eval_2_avg_episode_step_baseline_early_stopping = np.mean(
                self.train_log_dto.eval_2_episode_step_baseline_early_stopping)
        else:
            self.eval_2_avg_episode_step_baseline_early_stopping = 0.0
        if not eval and self.train_log_dto.eval_2_episode_snort_severe_baseline_uncaught_intrusion_steps is not None:
            self.eval_2_avg_episode_snort_severe_baseline_uncaught_intrusion_steps = DefenderTrainAgentLogDTOAvg.compute_avg_uncaught_intrusion_steps(
                self.train_log_dto.eval_2_episode_snort_severe_baseline_uncaught_intrusion_steps)
        else:
            self.eval_2_avg_episode_snort_severe_baseline_uncaught_intrusion_steps = 0.0

        if not eval and self.train_log_dto.eval_2_episode_snort_warning_baseline_uncaught_intrusion_steps is not None:
            self.eval_2_avg_episode_snort_warning_baseline_uncaught_intrusion_steps = DefenderTrainAgentLogDTOAvg.compute_avg_uncaught_intrusion_steps(
                self.train_log_dto.eval_2_episode_snort_warning_baseline_uncaught_intrusion_steps)
        else:
            self.eval_2_avg_episode_snort_warning_baseline_uncaught_intrusion_steps = 0.0

        if not eval and self.train_log_dto.eval_2_episode_snort_critical_baseline_uncaught_intrusion_steps is not None:
            self.eval_2_avg_episode_snort_critical_baseline_uncaught_intrusion_steps = DefenderTrainAgentLogDTOAvg.compute_avg_uncaught_intrusion_steps(
                self.train_log_dto.eval_2_episode_snort_critical_baseline_uncaught_intrusion_steps)
        else:
            self.eval_2_avg_episode_snort_critical_baseline_uncaught_intrusion_steps = 0.0

        if not eval and self.train_log_dto.eval_2_episode_var_log_baseline_uncaught_intrusion_steps is not None:
            self.eval_2_avg_episode_var_log_baseline_uncaught_intrusion_steps = DefenderTrainAgentLogDTOAvg.compute_avg_uncaught_intrusion_steps(
                self.train_log_dto.eval_2_episode_var_log_baseline_uncaught_intrusion_steps)
        else:
            self.eval_2_avg_episode_var_log_baseline_uncaught_intrusion_steps = 0.0

        if not eval and self.train_log_dto.eval_2_episode_step_baseline_uncaught_intrusion_steps is not None:
            self.eval_2_avg_episode_step_baseline_uncaught_intrusion_steps = DefenderTrainAgentLogDTOAvg.compute_avg_uncaught_intrusion_steps(
                self.train_log_dto.eval_2_episode_step_baseline_uncaught_intrusion_steps)
        else:
            self.eval_2_avg_episode_step_baseline_uncaught_intrusion_steps = 0.0
        if not eval and self.train_log_dto.eval_2_episode_snort_severe_baseline_steps is not None:
            self.eval_2_avg_episode_snort_severe_baseline_steps = np.mean(
                self.train_log_dto.eval_2_episode_snort_severe_baseline_steps)
        else:
            self.eval_2_avg_episode_snort_severe_baseline_steps = 0.0

        if not eval and self.train_log_dto.eval_2_episode_snort_warning_baseline_steps is not None:
            self.eval_2_avg_episode_snort_warning_baseline_steps = np.mean(
                self.train_log_dto.eval_2_episode_snort_warning_baseline_steps)
        else:
            self.eval_2_avg_episode_snort_warning_baseline_steps = 0.0

        if not eval and self.train_log_dto.eval_2_episode_snort_critical_baseline_steps is not None:
            self.eval_2_avg_episode_snort_critical_baseline_steps = np.mean(
                self.train_log_dto.eval_2_episode_snort_critical_baseline_steps)
        else:
            self.eval_2_avg_episode_snort_critical_baseline_steps = 0.0

        if not eval and self.train_log_dto.eval_2_episode_var_log_baseline_steps is not None:
            self.eval_2_avg_episode_var_log_baseline_steps = np.mean(self.train_log_dto.eval_2_episode_var_log_baseline_steps)
        else:
            self.eval_2_avg_episode_var_log_baseline_steps = 0.0

        if not eval and self.train_log_dto.eval_2_episode_step_baseline_steps is not None:
            self.eval_2_avg_episode_step_baseline_steps = np.mean(self.train_log_dto.eval_2_episode_step_baseline_steps)
        else:
            self.eval_2_avg_episode_step_baseline_steps = 0.0

        if not eval and self.train_log_dto.eval_2_episode_intrusion_steps is not None:
            self.eval_2_avg_episode_intrusion_steps = np.mean(self.train_log_dto.eval_2_episode_intrusion_steps)
        else:
            self.eval_2_avg_episode_intrusion_steps = 0.0

        if not eval and self.train_log_dto.eval_2_episode_steps is not None:
            self.eval_2_avg_episode_steps = np.mean(self.train_log_dto.eval_2_episode_steps)
        else:
            self.eval_2_avg_episode_steps = 0.0

        if not eval and self.train_log_dto.eval_2_attacker_action_costs is not None:
            self.eval_2_avg_episode_costs = np.mean(self.train_log_dto.eval_2_attacker_action_costs)
        else:
            self.eval_2_avg_episode_costs = 0.0
        if not eval and self.train_log_dto.eval_2_attacker_action_costs_norm is not None:
            self.eval_2_avg_episode_costs_norm = np.mean(self.train_log_dto.eval_2_attacker_action_costs_norm)
        else:
            self.eval_2_avg_episode_costs_norm = 0.0
        if not eval and self.train_log_dto.eval_2_attacker_action_alerts is not None:
            self.eval_2_avg_episode_alerts = np.mean(self.train_log_dto.eval_2_attacker_action_alerts)
        else:
            self.eval_2_avg_episode_alerts = 0.0
        if not eval and self.train_log_dto.eval_2_attacker_action_alerts_norm is not None:
            self.eval_2_avg_episode_alerts_norm = np.mean(self.train_log_dto.eval_2_attacker_action_alerts_norm)
        else:
            self.eval_2_avg_episode_alerts_norm = 0.0

        if self.train_log_dto.rollout_times is not None:
            if len(self.train_log_dto.rollout_times) > 0:
                self.avg_rollout_times = np.mean(self.train_log_dto.rollout_times)
            else:
                self.avg_rollout_times = 0.0
        else:
            self.avg_rollout_times = 0.0
        if self.train_log_dto.env_response_times is not None and len(self.train_log_dto.env_response_times) > 0:
            if len(self.train_log_dto.env_response_times) > 0:
                self.avg_env_response_times = np.mean(self.train_log_dto.env_response_times)
            else:
                self.avg_env_response_times = 0.0
        else:
            self.avg_env_response_times = 0.0
        if self.train_log_dto.action_pred_times is not None and len(self.train_log_dto.action_pred_times) > 0:
            if len(self.train_log_dto.action_pred_times) > 0:
                self.avg_action_pred_times = np.mean(self.train_log_dto.action_pred_times)
            else:
                self.avg_action_pred_times = 0.0
        else:
            self.avg_action_pred_times = 0.0
        if self.train_log_dto.grad_comp_times is not None and len(self.train_log_dto.grad_comp_times) > 0:
            if len(self.train_log_dto.grad_comp_times) > 0:
                self.avg_grad_comp_times = np.mean(self.train_log_dto.grad_comp_times)
            else:
                self.avg_grad_comp_times = 0.0
        else:
            self.avg_grad_comp_times = 0.0
        if self.train_log_dto.weight_update_times is not None and len(self.train_log_dto.weight_update_times) > 0:
            if len(self.train_log_dto.weight_update_times):
                self.avg_weight_update_times = np.mean(self.train_log_dto.weight_update_times)
            else:
                self.avg_weight_update_times = 0.0
        else:
            self.avg_weight_update_times = 0.0

        if self.result.defender_avg_episode_rewards is not None:
            self.rolling_avg_rewards = pycr_util.running_average(self.result.defender_avg_episode_rewards + [self.avg_episode_rewards],
                                                            self.defender_agent_config.running_avg)
        else:
            self.rolling_avg_rewards = 0.0

        if self.result.avg_episode_steps is not None:
            self.rolling_avg_steps = pycr_util.running_average(self.result.avg_episode_steps + [self.avg_episode_steps],
                                                          self.defender_agent_config.running_avg)
        else:
            self.rolling_avg_steps = 0.0

        if self.train_log_dto.defender_lr is None:
            self.lr = 0.0
        else:
            self.lr = self.train_log_dto.defender_lr
        if not eval and self.train_log_dto.defender_episode_avg_loss is not None:
            self.avg_episode_loss = np.mean(self.train_log_dto.defender_episode_avg_loss)
        else:
            self.avg_episode_loss = 0.0

        if not eval and self.train_log_dto.defender_eval_episode_rewards is not None:
            self.eval_avg_episode_rewards = np.mean(self.train_log_dto.defender_eval_episode_rewards)
        else:
            self.eval_avg_episode_rewards = 0.0

        if not eval and self.train_log_dto.eval_uncaught_intrusion_steps is not None:
            self.eval_avg_episode_uncaught_intrusion_steps = DefenderTrainAgentLogDTOAvg.compute_avg_uncaught_intrusion_steps(
                self.train_log_dto.eval_uncaught_intrusion_steps)
        else:
            self.eval_avg_episode_uncaught_intrusion_steps = 0.0

        if not eval and self.train_log_dto.eval_optimal_defender_reward is not None:
            self.eval_avg_episode_optimal_defender_reward = np.mean(self.train_log_dto.eval_optimal_defender_reward)
        else:
            self.eval_avg_episode_optimal_defender_reward = 0.0

        if not eval and self.train_log_dto.eval_episode_snort_severe_baseline_rewards is not None:
            self.eval_avg_episode_snort_severe_baseline_rewards = np.mean(
                self.train_log_dto.eval_episode_snort_severe_baseline_rewards)
        else:
            self.eval_avg_episode_snort_severe_baseline_rewards = 0.0

        if not eval and self.train_log_dto.eval_episode_snort_warning_baseline_rewards is not None:
            self.eval_avg_episode_snort_warning_baseline_rewards = np.mean(
                self.train_log_dto.eval_episode_snort_warning_baseline_rewards)
        else:
            self.eval_avg_episode_snort_warning_baseline_rewards = 0.0

        if not eval and self.train_log_dto.eval_episode_snort_critical_baseline_rewards is not None:
            self.eval_avg_episode_snort_critical_baseline_rewards = np.mean(
                self.train_log_dto.eval_episode_snort_critical_baseline_rewards)
        else:
            self.eval_avg_episode_snort_critical_baseline_rewards = 0.0

        if not eval and self.train_log_dto.eval_episode_var_log_baseline_rewards is not None:
            self.eval_avg_episode_var_log_baseline_rewards = np.mean(
                self.train_log_dto.eval_episode_var_log_baseline_rewards)
        else:
            self.eval_avg_episode_var_log_baseline_rewards = 0.0

        if not eval and self.train_log_dto.eval_episode_step_baseline_rewards is not None:
            self.eval_avg_episode_step_baseline_rewards = np.mean(
                self.train_log_dto.eval_episode_step_baseline_rewards)
        else:
            self.eval_avg_episode_step_baseline_rewards = 0.0

        if not eval and self.train_log_dto.eval_episode_snort_severe_baseline_steps is not None:
            self.eval_avg_episode_snort_severe_baseline_steps = np.mean(
                self.train_log_dto.eval_episode_snort_severe_baseline_steps)
        else:
            self.eval_avg_episode_snort_severe_baseline_steps = 0.0

        if not eval and self.train_log_dto.eval_episode_snort_warning_baseline_steps is not None:
            self.eval_avg_episode_snort_warning_baseline_steps = np.mean(
                self.train_log_dto.eval_episode_snort_warning_baseline_steps)
        else:
            self.eval_avg_episode_snort_warning_baseline_steps = 0.0

        if not eval and self.train_log_dto.eval_episode_snort_critical_baseline_steps is not None:
            self.eval_avg_episode_snort_critical_baseline_steps = np.mean(
                self.train_log_dto.eval_episode_snort_critical_baseline_steps)
        else:
            self.eval_avg_episode_snort_critical_baseline_steps = 0.0

        if not eval and self.train_log_dto.eval_episode_var_log_baseline_steps is not None:
            self.eval_avg_episode_var_log_baseline_steps = np.mean(
                self.train_log_dto.eval_episode_var_log_baseline_steps)
        else:
            self.eval_avg_episode_var_log_baseline_steps = 0.0

        if not eval and self.train_log_dto.eval_episode_step_baseline_steps is not None:
            self.eval_avg_episode_step_baseline_steps = np.mean(
                self.train_log_dto.eval_episode_step_baseline_steps)
        else:
            self.eval_avg_episode_step_baseline_steps = 0.0
        if not eval and self.train_log_dto.eval_episode_snort_severe_baseline_caught_attacker is not None:
            self.eval_avg_episode_snort_severe_baseline_caught_attacker = np.mean(
                self.train_log_dto.eval_episode_snort_severe_baseline_caught_attacker)
        else:
            self.eval_avg_episode_snort_severe_baseline_caught_attacker = 0.0

        if not eval and self.train_log_dto.eval_episode_snort_warning_baseline_caught_attacker is not None:
            self.eval_avg_episode_snort_warning_baseline_caught_attacker = np.mean(
                self.train_log_dto.eval_episode_snort_warning_baseline_caught_attacker)
        else:
            self.eval_avg_episode_snort_warning_baseline_caught_attacker = 0.0

        if not eval and self.train_log_dto.eval_episode_snort_critical_baseline_caught_attacker is not None:
            self.eval_avg_episode_snort_critical_baseline_caught_attacker = np.mean(
                self.train_log_dto.eval_episode_snort_critical_baseline_caught_attacker)
        else:
            self.eval_avg_episode_snort_critical_baseline_caught_attacker = 0.0

        if not eval and self.train_log_dto.eval_episode_var_log_baseline_caught_attacker is not None:
            self.eval_avg_episode_var_log_baseline_caught_attacker = np.mean(
                self.train_log_dto.eval_episode_var_log_baseline_caught_attacker)
        else:
            self.eval_avg_episode_var_log_baseline_caught_attacker = 0.0

        if not eval and self.train_log_dto.eval_episode_step_baseline_caught_attacker is not None:
            self.eval_avg_episode_step_baseline_caught_attacker = np.mean(
                self.train_log_dto.eval_episode_step_baseline_caught_attacker)
        else:
            self.eval_avg_episode_step_baseline_caught_attacker = 0.0
        if not eval and self.train_log_dto.eval_episode_snort_severe_baseline_early_stopping is not None:
            self.eval_avg_episode_snort_severe_baseline_early_stopping = np.mean(
                self.train_log_dto.eval_episode_snort_severe_baseline_early_stopping)
        else:
            self.eval_avg_episode_snort_severe_baseline_early_stopping = 0.0

        if not eval and self.train_log_dto.eval_episode_snort_warning_baseline_early_stopping is not None:
            self.eval_avg_episode_snort_warning_baseline_early_stopping = np.mean(
                self.train_log_dto.eval_episode_snort_warning_baseline_early_stopping)
        else:
            self.eval_avg_episode_snort_warning_baseline_early_stopping = 0.0

        if not eval and self.train_log_dto.eval_episode_snort_critical_baseline_early_stopping is not None:
            self.eval_avg_episode_snort_critical_baseline_early_stopping = np.mean(
                self.train_log_dto.eval_episode_snort_critical_baseline_early_stopping)
        else:
            self.eval_avg_episode_snort_critical_baseline_early_stopping = 0.0

        if not eval and self.train_log_dto.eval_episode_var_log_baseline_early_stopping is not None:
            self.eval_avg_episode_var_log_baseline_early_stopping = np.mean(
                self.train_log_dto.eval_episode_var_log_baseline_early_stopping)
        else:
            self.eval_avg_episode_var_log_baseline_early_stopping = 0.0

        if not eval and self.train_log_dto.eval_episode_step_baseline_early_stopping is not None:
            self.eval_avg_episode_step_baseline_early_stopping = np.mean(
                self.train_log_dto.eval_episode_step_baseline_early_stopping)
        else:
            self.eval_avg_episode_step_baseline_early_stopping = 0.0
        if not eval and self.train_log_dto.eval_episode_snort_severe_baseline_uncaught_intrusion_steps is not None:
            self.eval_avg_episode_snort_severe_baseline_uncaught_intrusion_steps = DefenderTrainAgentLogDTOAvg.compute_avg_uncaught_intrusion_steps(
                self.train_log_dto.eval_episode_snort_severe_baseline_uncaught_intrusion_steps)
        else:
            self.eval_avg_episode_snort_severe_baseline_uncaught_intrusion_steps = 0.0

        if not eval and self.train_log_dto.eval_episode_snort_warning_baseline_uncaught_intrusion_steps is not None:
            self.eval_avg_episode_snort_warning_baseline_uncaught_intrusion_steps = DefenderTrainAgentLogDTOAvg.compute_avg_uncaught_intrusion_steps(
                self.train_log_dto.eval_episode_snort_warning_baseline_uncaught_intrusion_steps)
        else:
            self.eval_avg_episode_snort_warning_baseline_uncaught_intrusion_steps = 0.0

        if not eval and self.train_log_dto.eval_episode_snort_critical_baseline_uncaught_intrusion_steps is not None:
            self.eval_avg_episode_snort_critical_baseline_uncaught_intrusion_steps = DefenderTrainAgentLogDTOAvg.compute_avg_uncaught_intrusion_steps(
                self.train_log_dto.eval_episode_snort_critical_baseline_uncaught_intrusion_steps)
        else:
            self.eval_avg_episode_snort_critical_baseline_uncaught_intrusion_steps = 0.0

        if not eval and self.train_log_dto.eval_episode_var_log_baseline_uncaught_intrusion_steps is not None:
            self.eval_avg_episode_var_log_baseline_uncaught_intrusion_steps = DefenderTrainAgentLogDTOAvg.compute_avg_uncaught_intrusion_steps(
                self.train_log_dto.eval_episode_var_log_baseline_uncaught_intrusion_steps)
        else:
            self.eval_avg_episode_var_log_baseline_uncaught_intrusion_steps = 0.0

        if not eval and self.train_log_dto.eval_episode_step_baseline_uncaught_intrusion_steps is not None:
            self.eval_avg_episode_step_baseline_uncaught_intrusion_steps = DefenderTrainAgentLogDTOAvg.compute_avg_uncaught_intrusion_steps(
                self.train_log_dto.eval_episode_step_baseline_uncaught_intrusion_steps)
        else:
            self.eval_avg_episode_step_baseline_uncaught_intrusion_steps = 0.0

        if not eval and self.train_log_dto.eval_episode_intrusion_steps is not None:
            self.eval_avg_episode_intrusion_steps = np.mean(
                self.train_log_dto.eval_episode_intrusion_steps)
        else:
            self.eval_avg_episode_intrusion_steps = 0.0

        if not eval and self.train_log_dto.eval_defender_stops_remaining is not None:
            self.eval_avg_episode_defender_stops_remaining = np.mean(
                self.train_log_dto.eval_defender_stops_remaining)
        else:
            self.eval_avg_episode_defender_stops_remaining = 0.0

        if not eval and self.train_log_dto.eval_avg_episode_defender_first_stop_step is not None:
            self.eval_avg_episode_defender_first_stop_step = np.mean(
                self.train_log_dto.avg_episode_defender_first_stop_step)
        else:
            self.eval_avg_episode_defender_first_stop_step = 0.0

        if not eval and self.train_log_dto.eval_avg_episode_defender_second_stop_step is not None:
            self.eval_avg_episode_defender_second_stop_step = np.mean(
                self.train_log_dto.eval_avg_episode_defender_second_stop_step)
        else:
            self.eval_avg_episode_defender_second_stop_step = 0.0

        if not eval and self.train_log_dto.eval_avg_episode_defender_third_stop_step is not None:
            self.eval_avg_episode_defender_third_stop_step = np.mean(
                self.train_log_dto.eval_avg_episode_defender_third_stop_step)
        else:
            self.eval_avg_episode_defender_third_stop_step = 0.0

        if not eval and self.train_log_dto.eval_avg_episode_defender_fourth_stop_step is not None:
            self.eval_avg_episode_defender_fourth_stop_step = np.mean(
                self.train_log_dto.eval_avg_episode_defender_fourth_stop_step)
        else:
            self.eval_avg_episode_defender_fourth_stop_step = 0.0

        if not eval and self.train_log_dto.eval_2_defender_stops_remaining is not None:
            self.eval_2_avg_episode_defender_stops_remaining = np.mean(self.train_log_dto.eval_2_defender_stops_remaining)
        else:
            self.eval_2_avg_episode_defender_stops_remaining = 0.0

        if not eval and self.train_log_dto.eval_2_avg_episode_defender_first_stop_step is not None:
            self.eval_2_avg_episode_defender_first_stop_step = np.mean(self.train_log_dto.eval_2_avg_episode_defender_first_stop_step)
        else:
            self.eval_2_avg_episode_defender_first_stop_step = 0.0

        if not eval and self.train_log_dto.eval_2_avg_episode_defender_second_stop_step is not None:
            self.eval_2_avg_episode_defender_second_stop_step = np.mean(
                self.train_log_dto.eval_2_avg_episode_defender_second_stop_step)
        else:
            self.eval_2_avg_episode_defender_second_stop_step = 0.0

        if not eval and self.train_log_dto.eval_2_avg_episode_defender_third_stop_step is not None:
            self.eval_2_avg_episode_defender_third_stop_step = np.mean(
                self.train_log_dto.eval_2_avg_episode_defender_third_stop_step)
        else:
            self.eval_2_avg_episode_defender_third_stop_step = 0.0

        if not eval and self.train_log_dto.eval_2_avg_episode_defender_fourth_stop_step is not None:
            self.eval_2_avg_episode_defender_fourth_stop_step = np.mean(
                self.train_log_dto.eval_2_avg_episode_defender_fourth_stop_step)
        else:
            self.eval_2_avg_episode_defender_fourth_stop_step = 0.0


        # Regret & Pi* Metrics
        if self.defender_agent_config.log_regret:

            # Regret
            if self.env.env_config is not None:
                self.avg_regret = DefenderTrainAgentLogDTOAvg.compute_regret(opt_r=self.env.envs[0].env_config.pi_star_rew_defender,
                                                    r=self.avg_episode_rewards)
            else:
                self.avg_regret = 0.0

            if self.train_log_dto.defender_eval_episode_rewards is not None \
                    and self.train_log_dto.defender_eval_env_specific_rewards != {}:
                self.avg_eval_regret = DefenderTrainAgentLogDTOAvg.compute_regret(opt_r=self.env.envs[0].env_config.pi_star_rew_defender,
                                                         r=self.eval_avg_episode_rewards)
            else:
                self.avg_eval_regret = 0.0

            if self.train_log_dto.defender_eval_2_episode_rewards is not None \
                    and self.train_log_dto.defender_eval_2_env_specific_rewards != {}:
                self.avg_eval_2_regret = DefenderTrainAgentLogDTOAvg.compute_regret(opt_r=self.env.envs[0].env_config.pi_star_rew_defender,
                                                           r=self.eval_2_avg_episode_rewards)
            else:
                self.avg_eval_2_regret = 0.0

            # Opt frac
            if self.env.env_config is not None:
                self.avg_opt_frac = DefenderTrainAgentLogDTOAvg.compute_opt_frac(r=self.avg_episode_rewards,
                                                        opt_r=self.env.envs[0].env_config.pi_star_rew_defender)
            else:
                avg_opt_frac = 0.0

            if self.train_log_dto.defender_eval_episode_rewards is not None:
                self.eval_avg_opt_frac = self.eval_avg_episode_rewards / self.env.envs[0].env_config.pi_star_rew_defender
            else:
                self.eval_avg_opt_frac = 0.0

            if self.train_log_dto.defender_eval_2_episode_rewards is not None:
                self.eval_2_avg_opt_frac = self.eval_2_avg_episode_rewards / self.env.envs[0].env_config.pi_star_rew_defender
            else:
                self.eval_2_avg_opt_frac = 0.0

    def update_result(self) -> "TrainAgentLogDTO":
        """
        Updates the experiment result metrics

        :return: the updated train_log_dto which includes the updated experiment results
        """
        # Defender specific metrics
        self.result.defender_avg_episode_rewards.append(self.avg_episode_rewards)
        self.result.defender_avg_episode_loss.append(self.avg_episode_loss)
        self.result.defender_eval_avg_episode_rewards.append(self.eval_avg_episode_rewards)
        self.result.defender_eval_2_avg_episode_rewards.append(self.eval_2_avg_episode_rewards)
        self.result.defender_avg_regret.append(self.avg_regret)
        self.result.defender_avg_opt_frac.append(self.avg_opt_frac)
        self.result.defender_eval_avg_regret.append(self.avg_eval_regret)
        self.result.defender_eval_avg_opt_frac.append(self.eval_avg_opt_frac)
        self.result.snort_severe_baseline_rewards.append(self.avg_episode_snort_severe_baseline_rewards)
        self.result.snort_warning_baseline_rewards.append(self.avg_episode_snort_warning_baseline_rewards)
        self.result.eval_snort_severe_baseline_rewards.append(self.eval_avg_episode_snort_severe_baseline_rewards)
        self.result.eval_snort_warning_baseline_rewards.append(self.eval_avg_episode_snort_warning_baseline_rewards)
        self.result.eval_2_snort_severe_baseline_rewards.append(self.eval_2_avg_episode_snort_severe_baseline_rewards)
        self.result.eval_2_snort_warning_baseline_rewards.append(self.eval_2_avg_episode_snort_warning_baseline_rewards)
        self.result.snort_critical_baseline_rewards.append(self.avg_episode_snort_critical_baseline_rewards)
        self.result.var_log_baseline_rewards.append(self.avg_episode_var_log_baseline_rewards)
        self.result.eval_snort_critical_baseline_rewards.append(self.eval_avg_episode_snort_critical_baseline_rewards)
        self.result.eval_var_log_baseline_rewards.append(self.eval_avg_episode_var_log_baseline_rewards)
        self.result.eval_2_snort_critical_baseline_rewards.append(self.eval_2_avg_episode_snort_critical_baseline_rewards)
        self.result.eval_2_var_log_baseline_rewards.append(self.eval_2_avg_episode_var_log_baseline_rewards)
        self.result.defender_eval_2_avg_regret.append(self.avg_eval_2_regret)
        self.result.defender_eval_2_avg_opt_frac.append(self.eval_2_avg_opt_frac)
        self.result.snort_severe_baseline_steps.append(self.avg_episode_snort_severe_baseline_steps)
        self.result.snort_warning_baseline_steps.append(self.avg_episode_snort_warning_baseline_steps)
        self.result.eval_snort_severe_baseline_steps.append(self.eval_avg_episode_snort_severe_baseline_steps)
        self.result.eval_snort_warning_baseline_steps.append(self.eval_avg_episode_snort_warning_baseline_steps)
        self.result.eval_2_snort_severe_baseline_steps.append(self.eval_2_avg_episode_snort_severe_baseline_steps)
        self.result.eval_2_snort_warning_baseline_steps.append(self.eval_2_avg_episode_snort_warning_baseline_steps)
        self.result.snort_critical_baseline_steps.append(self.avg_episode_snort_critical_baseline_steps)
        self.result.var_log_baseline_steps.append(self.avg_episode_var_log_baseline_steps)
        self.result.eval_snort_critical_baseline_steps.append(self.eval_avg_episode_snort_critical_baseline_steps)
        self.result.eval_var_log_baseline_steps.append(self.eval_avg_episode_var_log_baseline_steps)
        self.result.eval_2_snort_critical_baseline_steps.append(self.eval_2_avg_episode_snort_critical_baseline_steps)
        self.result.eval_2_var_log_baseline_steps.append(self.eval_2_avg_episode_var_log_baseline_steps)
        self.result.step_baseline_steps.append(self.avg_episode_step_baseline_steps)
        self.result.eval_step_baseline_steps.append(self.eval_avg_episode_step_baseline_steps)
        self.result.eval_2_step_baseline_steps.append(self.eval_2_avg_episode_step_baseline_steps)
        self.result.step_baseline_rewards.append(self.avg_episode_step_baseline_rewards)
        self.result.eval_step_baseline_rewards.append(self.eval_avg_episode_step_baseline_rewards)
        self.result.eval_2_step_baseline_rewards.append(self.eval_2_avg_episode_step_baseline_rewards)
        self.result.snort_severe_baseline_caught_attacker.append(self.avg_episode_snort_severe_baseline_caught_attacker)
        self.result.snort_warning_baseline_caught_attacker.append(self.avg_episode_snort_warning_baseline_caught_attacker)
        self.result.eval_snort_severe_baseline_caught_attacker.append(self.eval_avg_episode_snort_severe_baseline_caught_attacker)
        self.result.eval_snort_warning_baseline_caught_attacker.append(
            self.eval_avg_episode_snort_warning_baseline_caught_attacker)
        self.result.eval_2_snort_severe_baseline_caught_attacker.append(
            self.eval_2_avg_episode_snort_severe_baseline_caught_attacker)
        self.result.eval_2_snort_warning_baseline_caught_attacker.append(
            self.eval_2_avg_episode_snort_warning_baseline_caught_attacker)
        self.result.snort_critical_baseline_caught_attacker.append(self.avg_episode_snort_critical_baseline_caught_attacker)
        self.result.var_log_baseline_caught_attacker.append(self.avg_episode_var_log_baseline_caught_attacker)
        self.result.eval_snort_critical_baseline_caught_attacker.append(
            self.eval_avg_episode_snort_critical_baseline_caught_attacker)
        self.result.eval_var_log_baseline_caught_attacker.append(self.eval_avg_episode_var_log_baseline_caught_attacker)
        self.result.eval_2_snort_critical_baseline_caught_attacker.append(
            self.eval_2_avg_episode_snort_critical_baseline_caught_attacker)
        self.result.eval_2_var_log_baseline_caught_attacker.append(self.eval_2_avg_episode_var_log_baseline_caught_attacker)
        self.result.step_baseline_caught_attacker.append(self.avg_episode_step_baseline_caught_attacker)
        self.result.eval_step_baseline_caught_attacker.append(self.eval_avg_episode_step_baseline_caught_attacker)
        self.result.eval_2_step_baseline_caught_attacker.append(self.eval_2_avg_episode_step_baseline_caught_attacker)
        self.result.snort_severe_baseline_early_stopping.append(self.avg_episode_snort_severe_baseline_early_stopping)
        self.result.snort_warning_baseline_early_stopping.append(self.avg_episode_snort_warning_baseline_early_stopping)
        self.result.eval_snort_severe_baseline_early_stopping.append(self.eval_avg_episode_snort_severe_baseline_early_stopping)
        self.result.eval_snort_warning_baseline_early_stopping.append(self.eval_avg_episode_snort_warning_baseline_early_stopping)
        self.result.eval_2_snort_severe_baseline_early_stopping.append(
            self.eval_2_avg_episode_snort_severe_baseline_early_stopping)
        self.result.eval_2_snort_warning_baseline_early_stopping.append(
            self.eval_2_avg_episode_snort_warning_baseline_early_stopping)
        self.result.snort_critical_baseline_early_stopping.append(self.avg_episode_snort_critical_baseline_early_stopping)
        self.result.var_log_baseline_early_stopping.append(self.avg_episode_var_log_baseline_early_stopping)
        self.result.eval_snort_critical_baseline_early_stopping.append(
            self.eval_avg_episode_snort_critical_baseline_early_stopping)
        self.result.eval_var_log_baseline_early_stopping.append(self.eval_avg_episode_var_log_baseline_early_stopping)
        self.result.eval_2_snort_critical_baseline_early_stopping.append(
            self.eval_2_avg_episode_snort_critical_baseline_early_stopping)
        self.result.eval_2_var_log_baseline_early_stopping.append(self.eval_2_avg_episode_var_log_baseline_early_stopping)
        self.result.step_baseline_early_stopping.append(self.avg_episode_step_baseline_early_stopping)
        self.result.eval_step_baseline_early_stopping.append(self.eval_avg_episode_step_baseline_early_stopping)
        self.result.eval_2_step_baseline_early_stopping.append(self.eval_2_avg_episode_step_baseline_early_stopping)
        self.result.snort_severe_baseline_uncaught_intrusion_steps.append(
            self.avg_episode_snort_severe_baseline_uncaught_intrusion_steps)
        self.result.snort_warning_baseline_uncaught_intrusion_steps.append(
            self.avg_episode_snort_warning_baseline_uncaught_intrusion_steps)
        self.result.eval_snort_severe_baseline_uncaught_intrusion_steps.append(
            self.eval_avg_episode_snort_severe_baseline_uncaught_intrusion_steps)
        self.result.eval_snort_warning_baseline_uncaught_intrusion_steps.append(
            self.eval_avg_episode_snort_warning_baseline_uncaught_intrusion_steps)
        self.result.eval_2_snort_severe_baseline_uncaught_intrusion_steps.append(
            self.eval_2_avg_episode_snort_severe_baseline_uncaught_intrusion_steps)
        self.result.eval_2_snort_warning_baseline_uncaught_intrusion_steps.append(
            self.eval_2_avg_episode_snort_warning_baseline_uncaught_intrusion_steps)
        self.result.snort_critical_baseline_uncaught_intrusion_steps.append(
            self.avg_episode_snort_critical_baseline_uncaught_intrusion_steps)
        self.result.var_log_baseline_uncaught_intrusion_steps.append(self.avg_episode_var_log_baseline_uncaught_intrusion_steps)
        self.result.eval_snort_critical_baseline_uncaught_intrusion_steps.append(
            self.eval_avg_episode_snort_critical_baseline_uncaught_intrusion_steps)
        self.result.eval_var_log_baseline_uncaught_intrusion_steps.append(
            self.eval_avg_episode_var_log_baseline_uncaught_intrusion_steps)
        self.result.eval_2_snort_critical_baseline_uncaught_intrusion_steps.append(
            self.eval_2_avg_episode_snort_critical_baseline_uncaught_intrusion_steps)
        self.result.eval_2_var_log_baseline_uncaught_intrusion_steps.append(
            self.eval_2_avg_episode_var_log_baseline_uncaught_intrusion_steps)
        self.result.step_baseline_uncaught_intrusion_steps.append(self.avg_episode_step_baseline_uncaught_intrusion_steps)
        self.result.eval_step_baseline_uncaught_intrusion_steps.append(
            self.eval_avg_episode_step_baseline_uncaught_intrusion_steps)
        self.result.eval_2_step_baseline_uncaught_intrusion_steps.append(
            self.eval_2_avg_episode_step_baseline_uncaught_intrusion_steps)
        self.result.avg_uncaught_intrusion_steps.append(self.avg_episode_uncaught_intrusion_steps)
        self.result.eval_avg_uncaught_intrusion_steps.append(self.eval_avg_episode_uncaught_intrusion_steps)
        self.result.eval_2_avg_uncaught_intrusion_steps.append(self.eval_2_avg_episode_uncaught_intrusion_steps)
        self.result.avg_optimal_defender_reward.append(self.avg_episode_optimal_defender_reward)
        self.result.eval_avg_optimal_defender_reward.append(self.eval_avg_episode_optimal_defender_reward)
        self.result.eval_2_avg_optimal_defender_reward.append(self.eval_2_avg_episode_optimal_defender_reward)
        self.result.avg_defender_stops_remaining.append(self.avg_episode_defender_stops_remaining)
        self.result.eval_avg_defender_stops_remaining.append(self.eval_avg_episode_defender_stops_remaining)
        self.result.eval_2_avg_defender_stops_remaining.append(self.eval_2_avg_episode_defender_stops_remaining)
        self.result.avg_defender_first_stop_step.append(self.avg_defender_first_stop_step)
        self.result.eval_avg_defender_first_stop_step.append(self.eval_avg_defender_first_stop_step)
        self.result.eval_2_avg_defender_first_stop_step.append(self.eval_2_avg_defender_first_stop_step)
        self.result.avg_defender_second_stop_step.append(self.avg_defender_second_stop_step)
        self.result.eval_avg_defender_second_stop_step.append(self.eval_avg_defender_second_stop_step)
        self.result.eval_2_avg_defender_second_stop_step.append(self.eval_2_avg_defender_second_stop_step)
        self.result.avg_defender_third_stop_step.append(self.avg_defender_third_stop_step)
        self.result.eval_avg_defender_third_stop_step.append(self.eval_avg_defender_third_stop_step)
        self.result.eval_2_avg_defender_third_stop_step.append(self.eval_2_avg_defender_third_stop_step)
        self.result.avg_defender_fourth_stop_step.append(self.avg_defender_fourth_stop_step)
        self.result.eval_avg_defender_fourth_stop_step.append(self.eval_avg_defender_fourth_stop_step)
        self.result.eval_2_avg_defender_fourth_stop_step.append(self.eval_2_avg_defender_fourth_stop_step)

        if self.train_log_dto.defender_train_episode_env_specific_rewards is not None:
            for key in self.train_log_dto.defender_train_episode_env_specific_rewards.keys():
                avg = np.mean(self.train_log_dto.defender_train_episode_env_specific_rewards[key])
                if key in self.result.defender_train_env_specific_rewards:
                    self.result.defender_train_env_specific_rewards[key].append(avg)
                else:
                    self.result.defender_train_env_specific_rewards[key] = [avg]

        if self.train_log_dto.defender_eval_env_specific_rewards is not None:
            for key in self.train_log_dto.defender_eval_env_specific_rewards.keys():
                avg = np.mean(self.train_log_dto.defender_eval_env_specific_rewards[key])
                if key in self.result.defender_eval_env_specific_rewards:
                    self.result.defender_eval_env_specific_rewards[key].append(avg)
                else:
                    self.result.defender_eval_env_specific_rewards[key] = [avg]

        if self.train_log_dto.defender_eval_2_env_specific_rewards is not None:
            for key in self.train_log_dto.defender_eval_2_env_specific_rewards.keys():
                avg = np.mean(self.train_log_dto.defender_eval_2_env_specific_rewards[key])
                if key in self.result.defender_eval_2_env_specific_rewards:
                    self.result.defender_eval_2_env_specific_rewards[key].append(avg)
                else:
                    self.result.defender_eval_2_env_specific_rewards[key] = [avg]

        # General metrics
        if not self.train_mode == TrainMode.SELF_PLAY:
            self.result.avg_episode_steps.append(self.avg_episode_steps)
            self.result.epsilon_values.append(self.defender_agent_config.epsilon)
            self.result.eval_avg_episode_steps.append(self.eval_avg_episode_steps)
            self.result.eval_2_avg_episode_steps.append(self.eval_2_avg_episode_steps)
            self.result.lr_list.append(self.train_log_dto.defender_lr)
            self.result.rollout_times.append(self.avg_rollout_times)
            self.result.env_response_times.append(self.avg_env_response_times)
            self.result.action_pred_times.append(self.avg_action_pred_times)
            self.result.grad_comp_times.append(self.avg_grad_comp_times)
            self.result.weight_update_times.append(self.avg_weight_update_times)
            self.result.caught_frac.append(self.episode_caught_frac)
            self.result.early_stopping_frac.append(self.episode_early_stopped_frac)
            self.result.intrusion_frac.append(self.episode_successful_intrusion_frac)
            self.result.eval_caught_frac.append(self.eval_episode_caught_frac)
            self.result.eval_early_stopping_frac.append(self.eval_episode_early_stopped_frac)
            self.result.eval_intrusion_frac.append(self.eval_episode_successful_intrusion_frac)
            self.result.eval_2_caught_frac.append(self.eval_2_episode_caught_frac)
            self.result.eval_2_early_stopping_frac.append(self.eval_2_episode_early_stopped_frac)
            self.result.eval_2_intrusion_frac.append(self.eval_2_episode_successful_intrusion_frac)
            self.result.attacker_action_costs.append(self.avg_episode_costs)
            self.result.attacker_action_costs_norm.append(self.avg_episode_costs_norm)
            self.result.attacker_action_alerts.append(self.avg_episode_alerts)
            self.result.attacker_action_alerts_norm.append(self.avg_episode_alerts_norm)
            self.result.eval_attacker_action_costs.append(self.eval_avg_episode_costs)
            self.result.eval_attacker_action_costs_norm.append(self.eval_avg_episode_costs_norm)
            self.result.eval_attacker_action_alerts.append(self.eval_avg_episode_alerts)
            self.result.eval_attacker_action_alerts_norm.append(self.eval_avg_episode_alerts_norm)
            self.result.eval_2_attacker_action_costs.append(self.eval_2_avg_episode_costs)
            self.result.eval_2_attacker_action_costs_norm.append(self.eval_2_avg_episode_costs_norm)
            self.result.eval_2_attacker_action_alerts.append(self.eval_2_avg_episode_alerts)
            self.result.eval_2_attacker_action_alerts_norm.append(self.eval_2_avg_episode_alerts_norm)
            self.result.avg_episode_flags.append(self.avg_episode_flags)
            self.result.avg_episode_flags_percentage.append(self.avg_episode_flags_percentage)
            self.result.eval_avg_episode_flags.append(self.eval_avg_episode_flags)
            self.result.eval_avg_episode_flags_percentage.append(self.eval_avg_episode_flags_percentage)
            self.result.eval_2_avg_episode_flags.append(self.eval_2_avg_episode_flags)
            self.result.eval_2_avg_episode_flags_percentage.append(self.eval_2_avg_episode_flags_percentage)
            self.result.intrusion_steps.append(self.avg_episode_intrusion_steps)
            self.result.eval_intrusion_steps.append(self.eval_avg_episode_intrusion_steps)
            self.result.eval_2_intrusion_steps.append(self.eval_2_avg_episode_intrusion_steps)

            if self.train_log_dto.train_env_specific_steps is not None:
                for key in self.train_log_dto.train_env_specific_steps.keys():
                    avg = np.mean(self.train_log_dto.train_env_specific_steps[key])
                    if key in self.result.train_env_specific_steps:
                        self.result.train_env_specific_steps[key].append(avg)
                    else:
                        self.result.train_env_specific_steps[key] = [avg]
            if self.train_log_dto.eval_env_specific_steps is not None:
                for key in self.train_log_dto.eval_env_specific_steps.keys():
                    avg = np.mean(self.train_log_dto.eval_env_specific_steps[key])
                    if key in self.result.eval_env_specific_steps:
                        self.result.eval_env_specific_steps[key].append(avg)
                    else:
                        self.result.eval_env_specific_steps[key] = [avg]
            if self.train_log_dto.eval_2_env_specific_steps is not None:
                for key in self.train_log_dto.eval_2_env_specific_steps.keys():
                    avg = np.mean(self.train_log_dto.eval_2_env_specific_steps[key])
                    if key in self.result.eval_2_env_specific_steps:
                        self.result.eval_2_env_specific_steps[key].append(avg)
                    else:
                        self.result.eval_2_env_specific_steps[key] = [avg]
            if not eval:
                self.train_log_dto.train_result = self.result
            else:
                self.train_log_dto.eval_result = self.result
            return self.train_log_dto

    @staticmethod
    def compute_opt_frac(r: float, opt_r: float) -> float:
        """
        Utility function for computing fraction of optimal reward

        :param r: reward
        :param opt_r: optimal reward
        :return: fraction of optimal reward
        """
        abs_difference = abs(opt_r - r)
        if (r >= 0 and opt_r >= 0) or (r <= 0 and opt_r <= 0):
            return r / opt_r
        elif r < 0 and opt_r > 0:
            return 1 / abs_difference
        else:
            return 1 / abs_difference

    @staticmethod
    def compute_regret(r: float, opt_r: float) -> float:
        """
        Utility function for computing the regret

        :param r: the reward
        :param opt_r: the optimal reward
        :return: the regret
        """
        return abs(opt_r - r)

    @staticmethod
    def compute_avg_uncaught_intrusion_steps(steps):
        """
        Utility function for computing the average number of uncaught intrusion steps from a list of steps

        :param steps: the list of uncaught intrusion steps
        :return: the average number of uncaught intrusion steps
        """
        # filtered_steps = np.array(list(filter(lambda x: x > 0, steps)))
        filtered_steps = steps
        if len(filtered_steps) > 0:
            return np.mean(filtered_steps)
        else:
            return 0.0

    @staticmethod
    def to_tensorboard_dto(avg_log_dto: "DefenderTrainAgentLogDTOAvg", eps: float, tensorboard_writer)\
            -> TensorboardDataDTO:
        """
        Converts the metrics in a DefenderTrainAgentLogDTOAvg into a TensorboardDataDTO

        :param avg_log_dto: the DTO to convert
        :param eps: the eps value
        :param tensorboard_writer: the tensorboard writer
        :return: the created tensorboardDTO
        """

        if eps is None:
            eps = 0.0

        tensorboard_data_dto = TensorboardDataDTO(
            iteration=avg_log_dto.train_log_dto.iteration, avg_episode_rewards=avg_log_dto.avg_episode_rewards,
            avg_episode_steps=avg_log_dto.avg_episode_steps,
            avg_episode_loss=avg_log_dto.avg_episode_loss, eps=eps, lr=avg_log_dto.lr, eval=avg_log_dto.eval,
            eval_avg_episode_rewards=avg_log_dto.eval_avg_episode_rewards, eval_avg_episode_steps=avg_log_dto.eval_avg_episode_steps,
            eval_2_avg_episode_rewards=avg_log_dto.eval_2_avg_episode_rewards,
            eval_2_avg_episode_steps=avg_log_dto.eval_2_avg_episode_steps,
            rolling_avg_episode_rewards=avg_log_dto.rolling_avg_rewards,
            rolling_avg_episode_steps=avg_log_dto.rolling_avg_steps,
            tensorboard_writer=tensorboard_writer,
            episode_caught_frac=avg_log_dto.episode_caught_frac,
            episode_early_stopped_frac=avg_log_dto.episode_early_stopped_frac,
            episode_successful_intrusion_frac=avg_log_dto.episode_successful_intrusion_frac,
            eval_episode_caught_frac=avg_log_dto.eval_episode_caught_frac,
            eval_episode_early_stopped_frac=avg_log_dto.eval_episode_early_stopped_frac,
            eval_episode_successful_intrusion_frac=avg_log_dto.eval_episode_successful_intrusion_frac,
            eval_2_episode_caught_frac=avg_log_dto.eval_2_episode_caught_frac,
            eval_2_episode_early_stopped_frac=avg_log_dto.eval_2_episode_early_stopped_frac,
            eval_2_episode_successful_intrusion_frac=avg_log_dto.eval_2_episode_successful_intrusion_frac,
            avg_regret=avg_log_dto.avg_regret, avg_opt_frac=avg_log_dto.avg_opt_frac,
            rolling_avg_rewards=avg_log_dto.rolling_avg_rewards,
            rolling_avg_steps=avg_log_dto.rolling_avg_steps,
            n_af=avg_log_dto.train_log_dto.n_af, n_d=avg_log_dto.train_log_dto.n_d, avg_episode_costs=avg_log_dto.avg_episode_costs,
            avg_episode_costs_norm=avg_log_dto.avg_episode_costs_norm,
            avg_episode_alerts=avg_log_dto.avg_episode_alerts, avg_episode_alerts_norm=avg_log_dto.avg_episode_alerts_norm,
            eval_avg_episode_costs=avg_log_dto.eval_avg_episode_costs, eval_avg_episode_costs_norm=avg_log_dto.eval_avg_episode_costs_norm,
            eval_avg_episode_alerts=avg_log_dto.eval_avg_episode_alerts, eval_avg_episode_alerts_norm=avg_log_dto.eval_avg_episode_alerts_norm,
            eval_2_avg_episode_costs=avg_log_dto.eval_2_avg_episode_costs,
            eval_2_avg_episode_costs_norm=avg_log_dto.eval_2_avg_episode_costs_norm,
            eval_2_avg_episode_alerts=avg_log_dto.eval_2_avg_episode_alerts,
            eval_2_avg_episode_alerts_norm=avg_log_dto.eval_2_avg_episode_alerts_norm,
            total_num_episodes=avg_log_dto.train_log_dto.total_num_episodes, avg_eval_regret=avg_log_dto.avg_eval_regret,
            eval_avg_opt_frac=avg_log_dto.eval_avg_opt_frac,
            epsilon=avg_log_dto.defender_agent_config.epsilon, training_time_hours=avg_log_dto.training_time_hours,
            avg_episode_snort_severe_baseline_rewards=avg_log_dto.avg_episode_snort_severe_baseline_rewards,
            avg_episode_snort_warning_baseline_rewards=avg_log_dto.avg_episode_snort_warning_baseline_rewards,
            eval_avg_episode_snort_severe_baseline_rewards=avg_log_dto.eval_avg_episode_snort_severe_baseline_rewards,
            eval_avg_episode_snort_warning_baseline_rewards=avg_log_dto.eval_avg_episode_snort_warning_baseline_rewards,
            eval_avg_2_episode_snort_severe_baseline_rewards=avg_log_dto.eval_2_avg_episode_snort_severe_baseline_rewards,
            eval_avg_2_episode_snort_warning_baseline_rewards=avg_log_dto.eval_2_avg_episode_snort_warning_baseline_rewards,
            avg_episode_snort_critical_baseline_rewards=avg_log_dto.avg_episode_snort_critical_baseline_rewards,
            avg_episode_var_log_baseline_rewards=avg_log_dto.avg_episode_var_log_baseline_rewards,
            avg_episode_step_baseline_rewards=avg_log_dto.avg_episode_step_baseline_rewards,
            eval_avg_episode_snort_critical_baseline_rewards=avg_log_dto.eval_avg_episode_snort_critical_baseline_rewards,
            eval_avg_episode_var_log_baseline_rewards=avg_log_dto.eval_avg_episode_var_log_baseline_rewards,
            eval_avg_episode_step_baseline_rewards=avg_log_dto.eval_avg_episode_step_baseline_rewards,
            eval_avg_2_episode_snort_critical_baseline_rewards=avg_log_dto.eval_2_avg_episode_snort_critical_baseline_rewards,
            eval_avg_2_episode_var_log_baseline_rewards=avg_log_dto.eval_2_avg_episode_var_log_baseline_rewards,
            eval_avg_2_episode_step_baseline_rewards=avg_log_dto.eval_2_avg_episode_step_baseline_rewards,
            avg_episode_snort_severe_baseline_steps=avg_log_dto.avg_episode_snort_severe_baseline_steps,
            avg_episode_snort_warning_baseline_steps=avg_log_dto.avg_episode_snort_warning_baseline_steps,
            eval_avg_episode_snort_severe_baseline_steps=avg_log_dto.eval_avg_episode_snort_severe_baseline_steps,
            eval_avg_episode_snort_warning_baseline_steps=avg_log_dto.eval_avg_episode_snort_warning_baseline_steps,
            eval_avg_2_episode_snort_severe_baseline_steps=avg_log_dto.eval_2_avg_episode_snort_severe_baseline_steps,
            eval_avg_2_episode_snort_warning_baseline_steps=avg_log_dto.eval_2_avg_episode_snort_warning_baseline_steps,
            avg_episode_snort_critical_baseline_steps=avg_log_dto.avg_episode_snort_critical_baseline_steps,
            avg_episode_var_log_baseline_steps=avg_log_dto.avg_episode_var_log_baseline_steps,
            avg_episode_step_baseline_steps=avg_log_dto.avg_episode_step_baseline_steps,
            eval_avg_episode_snort_critical_baseline_steps=avg_log_dto.eval_avg_episode_snort_critical_baseline_steps,
            eval_avg_episode_var_log_baseline_steps=avg_log_dto.eval_avg_episode_var_log_baseline_steps,
            eval_avg_episode_step_baseline_steps=avg_log_dto.eval_avg_episode_step_baseline_steps,
            eval_avg_2_episode_snort_critical_baseline_steps=avg_log_dto.eval_2_avg_episode_snort_critical_baseline_steps,
            eval_avg_2_episode_var_log_baseline_steps=avg_log_dto.eval_2_avg_episode_var_log_baseline_steps,
            eval_avg_2_episode_step_baseline_steps=avg_log_dto.eval_2_avg_episode_step_baseline_steps,
            avg_episode_snort_severe_baseline_caught_attacker=avg_log_dto.avg_episode_snort_severe_baseline_caught_attacker,
            avg_episode_snort_warning_baseline_caught_attacker=avg_log_dto.avg_episode_snort_warning_baseline_caught_attacker,
            eval_avg_episode_snort_severe_baseline_caught_attacker=avg_log_dto.eval_avg_episode_snort_severe_baseline_caught_attacker,
            eval_avg_episode_snort_warning_baseline_caught_attacker=avg_log_dto.eval_avg_episode_snort_warning_baseline_caught_attacker,
            eval_avg_2_episode_snort_severe_baseline_caught_attacker=avg_log_dto.eval_2_avg_episode_snort_severe_baseline_caught_attacker,
            eval_avg_2_episode_snort_warning_baseline_caught_attacker=avg_log_dto.eval_2_avg_episode_snort_warning_baseline_caught_attacker,
            avg_episode_snort_critical_baseline_caught_attacker=avg_log_dto.avg_episode_snort_critical_baseline_caught_attacker,
            avg_episode_var_log_baseline_caught_attacker=avg_log_dto.avg_episode_var_log_baseline_caught_attacker,
            avg_episode_step_baseline_caught_attacker=avg_log_dto.avg_episode_step_baseline_caught_attacker,
            eval_avg_episode_snort_critical_baseline_caught_attacker=avg_log_dto.eval_avg_episode_snort_critical_baseline_caught_attacker,
            eval_avg_episode_var_log_baseline_caught_attacker=avg_log_dto.eval_avg_episode_var_log_baseline_caught_attacker,
            eval_avg_episode_step_baseline_caught_attacker=avg_log_dto.eval_avg_episode_step_baseline_caught_attacker,
            eval_avg_2_episode_snort_critical_baseline_caught_attacker=avg_log_dto.eval_2_avg_episode_snort_critical_baseline_caught_attacker,
            eval_avg_2_episode_var_log_baseline_caught_attacker=avg_log_dto.eval_2_avg_episode_var_log_baseline_caught_attacker,
            eval_avg_2_episode_step_baseline_caught_attacker=avg_log_dto.eval_2_avg_episode_step_baseline_caught_attacker,
            avg_episode_snort_severe_baseline_early_stopping=avg_log_dto.avg_episode_snort_severe_baseline_early_stopping,
            avg_episode_snort_warning_baseline_early_stopping=avg_log_dto.avg_episode_snort_warning_baseline_early_stopping,
            eval_avg_episode_snort_severe_baseline_early_stopping=avg_log_dto.eval_avg_episode_snort_severe_baseline_early_stopping,
            eval_avg_episode_snort_warning_baseline_early_stopping=avg_log_dto.eval_avg_episode_snort_warning_baseline_early_stopping,
            eval_avg_2_episode_snort_severe_baseline_early_stopping=avg_log_dto.eval_2_avg_episode_snort_severe_baseline_early_stopping,
            eval_avg_2_episode_snort_warning_baseline_early_stopping=avg_log_dto.eval_2_avg_episode_snort_warning_baseline_early_stopping,
            avg_episode_snort_critical_baseline_early_stopping=avg_log_dto.avg_episode_snort_critical_baseline_early_stopping,
            avg_episode_var_log_baseline_early_stopping=avg_log_dto.avg_episode_var_log_baseline_early_stopping,
            avg_episode_step_baseline_early_stopping=avg_log_dto.avg_episode_step_baseline_early_stopping,
            eval_avg_episode_snort_critical_baseline_early_stopping=avg_log_dto.eval_avg_episode_snort_critical_baseline_early_stopping,
            eval_avg_episode_var_log_baseline_early_stopping=avg_log_dto.eval_avg_episode_var_log_baseline_early_stopping,
            eval_avg_episode_step_baseline_early_stopping=avg_log_dto.eval_avg_episode_step_baseline_early_stopping,
            eval_avg_2_episode_snort_critical_baseline_early_stopping=avg_log_dto.eval_2_avg_episode_snort_critical_baseline_early_stopping,
            eval_avg_2_episode_var_log_baseline_early_stopping=avg_log_dto.eval_2_avg_episode_var_log_baseline_early_stopping,
            eval_avg_2_episode_step_baseline_early_stopping=avg_log_dto.eval_2_avg_episode_step_baseline_early_stopping,
            avg_episode_snort_severe_baseline_uncaught_intrusion_steps=avg_log_dto.avg_episode_snort_severe_baseline_uncaught_intrusion_steps,
            avg_episode_snort_warning_baseline_uncaught_intrusion_steps=avg_log_dto.avg_episode_snort_warning_baseline_uncaught_intrusion_steps,
            eval_avg_episode_snort_severe_baseline_uncaught_intrusion_steps=avg_log_dto.eval_avg_episode_snort_severe_baseline_uncaught_intrusion_steps,
            eval_avg_episode_snort_warning_baseline_uncaught_intrusion_steps=avg_log_dto.eval_avg_episode_snort_warning_baseline_uncaught_intrusion_steps,
            eval_avg_2_episode_snort_severe_baseline_uncaught_intrusion_steps=avg_log_dto.eval_2_avg_episode_snort_severe_baseline_uncaught_intrusion_steps,
            eval_avg_2_episode_snort_warning_baseline_uncaught_intrusion_steps=avg_log_dto.eval_2_avg_episode_snort_warning_baseline_uncaught_intrusion_steps,
            avg_episode_snort_critical_baseline_uncaught_intrusion_steps=avg_log_dto.avg_episode_snort_critical_baseline_uncaught_intrusion_steps,
            avg_episode_var_log_baseline_uncaught_intrusion_steps=avg_log_dto.avg_episode_var_log_baseline_uncaught_intrusion_steps,
            avg_episode_step_baseline_uncaught_intrusion_steps=avg_log_dto.avg_episode_step_baseline_uncaught_intrusion_steps,
            eval_avg_episode_snort_critical_baseline_uncaught_intrusion_steps=avg_log_dto.eval_avg_episode_snort_critical_baseline_uncaught_intrusion_steps,
            eval_avg_episode_var_log_baseline_uncaught_intrusion_steps=avg_log_dto.eval_avg_episode_var_log_baseline_uncaught_intrusion_steps,
            eval_avg_episode_step_baseline_uncaught_intrusion_steps=avg_log_dto.eval_avg_episode_step_baseline_uncaught_intrusion_steps,
            eval_avg_2_episode_snort_critical_baseline_uncaught_intrusion_steps=avg_log_dto.eval_2_avg_episode_snort_critical_baseline_uncaught_intrusion_steps,
            eval_avg_2_episode_var_log_baseline_uncaught_intrusion_steps=avg_log_dto.eval_2_avg_episode_var_log_baseline_uncaught_intrusion_steps,
            eval_avg_2_episode_step_baseline_uncaught_intrusion_steps=avg_log_dto.eval_2_avg_episode_step_baseline_uncaught_intrusion_steps,
            avg_flags_catched=avg_log_dto.avg_episode_flags, avg_episode_flags_percentage=avg_log_dto.avg_episode_flags_percentage,
            eval_avg_episode_flags=avg_log_dto.eval_avg_episode_flags,
            eval_avg_episode_flags_percentage=avg_log_dto.eval_avg_episode_flags_percentage,
            eval_2_avg_episode_flags=avg_log_dto.eval_2_avg_episode_flags,
            eval_2_avg_episode_flags_percentage=avg_log_dto.eval_2_avg_episode_flags_percentage,
            avg_episode_intrusion_steps=avg_log_dto.avg_episode_intrusion_steps,
            eval_avg_episode_intrusion_steps=avg_log_dto.eval_avg_episode_intrusion_steps,
            eval_2_avg_episode_intrusion_steps=avg_log_dto.eval_2_avg_episode_intrusion_steps,
            avg_uncaught_intrusion_steps=avg_log_dto.avg_episode_uncaught_intrusion_steps,
            eval_avg_uncaught_intrusion_steps=avg_log_dto.eval_avg_episode_uncaught_intrusion_steps,
            eval_2_avg_uncaught_intrusion_steps=avg_log_dto.eval_2_avg_episode_uncaught_intrusion_steps,
            avg_optimal_defender_reward=avg_log_dto.avg_episode_optimal_defender_reward,
            eval_avg_optimal_defender_reward=avg_log_dto.eval_avg_episode_optimal_defender_reward,
            eval_2_avg_optimal_defender_reward=avg_log_dto.eval_2_avg_episode_optimal_defender_reward,
            avg_defender_stops_remaining=avg_log_dto.avg_episode_defender_stops_remaining,
            eval_avg_defender_stops_remaining=avg_log_dto.eval_avg_episode_defender_stops_remaining,
            eval_2_avg_defender_stops_remaining=avg_log_dto.eval_2_avg_episode_defender_stops_remaining,
            avg_defender_first_stop_step=avg_log_dto.avg_defender_first_stop_step,
            avg_defender_second_stop_step=avg_log_dto.avg_defender_second_stop_step,
            avg_defender_third_stop_step=avg_log_dto.avg_defender_third_stop_step,
            avg_defender_fourth_stop_step=avg_log_dto.avg_defender_fourth_stop_step,
            eval_avg_defender_first_stop_step=avg_log_dto.eval_avg_defender_first_stop_step,
            eval_avg_defender_second_stop_step=avg_log_dto.eval_avg_defender_second_stop_step,
            eval_avg_defender_third_stop_step=avg_log_dto.eval_avg_defender_third_stop_step,
            eval_avg_defender_fourth_stop_step=avg_log_dto.eval_avg_defender_fourth_stop_step,
            eval_2_avg_defender_first_stop_step=avg_log_dto.eval_2_avg_defender_first_stop_step,
            eval_2_avg_defender_second_stop_step=avg_log_dto.eval_2_avg_defender_second_stop_step,
            eval_2_avg_defender_third_stop_step=avg_log_dto.eval_2_avg_defender_third_stop_step,
            eval_2_avg_defender_fourth_stop_step=avg_log_dto.eval_2_avg_defender_fourth_stop_step
        )
        return tensorboard_data_dto
