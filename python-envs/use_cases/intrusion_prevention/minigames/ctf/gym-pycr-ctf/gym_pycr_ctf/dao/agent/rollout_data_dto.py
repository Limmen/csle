from typing import List
import pycr_common.constants.constants as constants
from pycr_common.dao.agent.base_rollout_data_dto import BaseRolloutDataDTO
from pycr_common.agents.config.agent_config import AgentConfig


class RolloutDataDTO(BaseRolloutDataDTO):
    """
    DTO with information from rollout in the env
    """
    def __init__(self, attacker_episode_rewards : List[float] = None, defender_episode_rewards : List[float] = None,
                 episode_steps : List[int] = None,
                 episode_flags : List[int]  = None, episode_caught : List[bool]  = None, episode_early_stopped: List[bool]  = None,
                 episode_successful_intrusion : List[bool]  = None,
                 episode_snort_severe_baseline_rewards : List[float]  = None,
                 episode_snort_warning_baseline_rewards : List[float] = None,
                 episode_snort_critical_baseline_rewards : List[float] = None,
                 episode_var_log_baseline_rewards : List[float] = None,
                 episode_step_baseline_rewards : List[float] = None,
                 episode_snort_severe_baseline_steps: List[int] = None,
                 episode_snort_warning_baseline_steps: List[int] = None,
                 episode_snort_critical_baseline_steps: List[int] = None,
                 episode_var_log_baseline_steps: List[int] = None,
                 episode_step_baseline_steps: List[int] = None,
                 episode_snort_severe_baseline_caught_attacker: List[bool] = None,
                 episode_snort_warning_baseline_caught_attacker: List[bool] = None,
                 episode_snort_critical_baseline_caught_attacker: List[bool] = None,
                 episode_var_log_baseline_caught_attacker: List[bool] = None,
                 episode_step_baseline_caught_attacker: List[bool] = None,
                 episode_snort_severe_baseline_early_stopping: List[bool] = None,
                 episode_snort_warning_baseline_early_stopping: List[bool] = None,
                 episode_snort_critical_baseline_early_stopping: List[bool] = None,
                 episode_var_log_baseline_early_stopping: List[bool] = None,
                 episode_step_baseline_early_stopping: List[bool] = None,
                 episode_snort_severe_baseline_uncaught_intrusion_steps: List[int] = None,
                 episode_snort_warning_baseline_uncaught_intrusion_steps: List[int] = None,
                 episode_snort_critical_baseline_uncaught_intrusion_steps: List[int] = None,
                 episode_var_log_baseline_uncaught_intrusion_steps: List[int] = None,
                 episode_step_baseline_uncaught_intrusion_steps: List[int] = None,
                 episode_flags_percentage: List[float] = None,
                 attacker_env_specific_rewards: List[float]  = None,
                 defender_env_specific_rewards: List[float]  = None,
                 env_specific_steps: dict  = None,
                 env_specific_flags: dict = None,
                 env_specific_flags_percentage: dict = None,
                 env_response_times: dict = None,
                 action_pred_times: List[float]  = None,
                 attacker_action_costs: List[float]  = None,
                 attacker_action_costs_norm: List[float] = None,
                 attacker_action_alerts: List[float] = None,
                 attacker_action_alerts_norm: List[float] = None,
                 episode_intrusion_steps: List[int]  = None,
                 uncaught_intrusion_steps: List[int] = None,
                 optimal_defender_reward: List[float] = None,
                 defender_stops_remaining: List[int]  = None,
                 defender_first_stop_step: List[int] = None,
                 defender_second_stop_step: List[int] = None,
                 defender_third_stop_step: List[int] = None,
                 defender_fourth_stop_step: List[int] = None,
                 episode_snort_severe_baseline_first_stop_step: List[int]  = None,
                 episode_snort_warning_baseline_first_stop_step: List[int] = None,
                 episode_snort_critical_baseline_first_stop_step: List[int] = None,
                 episode_var_log_baseline_first_stop_step: List[int] = None,
                 episode_step_baseline_first_stop_step: List[int] = None,
                 episode_snort_severe_baseline_second_stop_step: List[int] = None,
                 episode_snort_warning_baseline_second_stop_step: List[int] = None,
                 episode_snort_critical_baseline_second_stop_step: List[int] = None,
                 episode_var_log_baseline_second_stop_step: List[int] = None,
                 episode_step_baseline_second_stop_step: List[int] = None,
                 episode_snort_severe_baseline_third_stop_step: List[int] = None,
                 episode_snort_warning_baseline_third_stop_step: List[int] = None,
                 episode_snort_critical_baseline_third_stop_step: List[int] = None,
                 episode_var_log_baseline_third_stop_step: List[int] = None,
                 episode_step_baseline_third_stop_step: List[int] = None,
                 episode_snort_severe_baseline_fourth_stop_step: List[int] = None,
                 episode_snort_warning_baseline_fourth_stop_step: List[int] = None,
                 episode_snort_critical_baseline_fourth_stop_step: List[int] = None,
                 episode_var_log_baseline_fourth_stop_step: List[int] = None,
                 episode_step_baseline_fourth_stop_step: List[int] = None,
                 episode_snort_severe_baseline_stops_remaining: List[int] = None,
                 episode_snort_warning_baseline_stops_remaining: List[int] = None,
                 episode_snort_critical_baseline_stops_remaining: List[int] = None,
                 episode_var_log_baseline_stops_remaining: List[int] = None,
                 episode_step_baseline_stops_remaining: List[int] = None,
                 optimal_stops_remaining: List[int] = None,
                 optimal_first_stop_step: List[int] = None,
                 optimal_second_stop_step: List[int] = None,
                 optimal_third_stop_step: List[int] = None,
                 optimal_fourth_stop_step: List[int] = None,
                 optimal_defender_episode_steps: List[int]  = None
                 ):
        super(RolloutDataDTO, self).__init__()
        self.attacker_episode_rewards = attacker_episode_rewards
        self.defender_episode_rewards = defender_episode_rewards
        self.episode_steps = episode_steps
        self.episode_flags = episode_flags
        self.episode_caught = episode_caught
        self.episode_early_stopped = episode_early_stopped
        self.episode_successful_intrusion = episode_successful_intrusion
        self.episode_snort_severe_baseline_rewards = episode_snort_severe_baseline_rewards
        self.episode_snort_warning_baseline_rewards = episode_snort_warning_baseline_rewards
        self.episode_snort_critical_baseline_rewards = episode_snort_critical_baseline_rewards
        self.episode_var_log_baseline_rewards = episode_var_log_baseline_rewards
        self.episode_step_baseline_rewards = episode_step_baseline_rewards
        self.episode_snort_severe_baseline_steps = episode_snort_severe_baseline_steps
        self.episode_snort_warning_baseline_steps = episode_snort_warning_baseline_steps
        self.episode_snort_critical_baseline_steps = episode_snort_critical_baseline_steps
        self.episode_var_log_baseline_steps = episode_var_log_baseline_steps
        self.episode_step_baseline_steps = episode_step_baseline_steps
        self.episode_snort_severe_baseline_caught_attacker = episode_snort_severe_baseline_caught_attacker
        self.episode_snort_warning_baseline_caught_attacker = episode_snort_warning_baseline_caught_attacker
        self.episode_snort_critical_baseline_caught_attacker = episode_snort_critical_baseline_caught_attacker
        self.episode_var_log_baseline_caught_attacker = episode_var_log_baseline_caught_attacker
        self.episode_step_baseline_caught_attacker = episode_step_baseline_caught_attacker
        self.episode_snort_severe_baseline_early_stopping = episode_snort_severe_baseline_early_stopping
        self.episode_snort_warning_baseline_early_stopping = episode_snort_warning_baseline_early_stopping
        self.episode_snort_critical_baseline_early_stopping = episode_snort_critical_baseline_early_stopping
        self.episode_var_log_baseline_early_stopping = episode_var_log_baseline_early_stopping
        self.episode_step_baseline_early_stopping = episode_step_baseline_early_stopping
        self.episode_snort_severe_baseline_uncaught_intrusion_steps = episode_snort_severe_baseline_uncaught_intrusion_steps
        self.episode_snort_warning_baseline_uncaught_intrusion_steps = episode_snort_warning_baseline_uncaught_intrusion_steps
        self.episode_snort_critical_baseline_uncaught_intrusion_steps = episode_snort_critical_baseline_uncaught_intrusion_steps
        self.episode_var_log_baseline_uncaught_intrusion_steps = episode_var_log_baseline_uncaught_intrusion_steps
        self.episode_step_baseline_uncaught_intrusion_steps = episode_step_baseline_uncaught_intrusion_steps
        self.episode_flags_percentage = episode_flags_percentage
        self.attacker_env_specific_rewards = attacker_env_specific_rewards
        self.defender_env_specific_rewards = defender_env_specific_rewards
        self.env_specific_steps = env_specific_steps
        self.env_specific_flags = env_specific_flags
        self.env_specific_flags_percentage = env_specific_flags_percentage
        self.env_response_times = env_response_times
        self.action_pred_times = action_pred_times
        self.attacker_action_costs = attacker_action_costs
        self.attacker_action_costs_norm = attacker_action_costs_norm
        self.attacker_action_alerts = attacker_action_alerts
        self.attacker_action_alerts_norm = attacker_action_alerts_norm
        self.episode_intrusion_steps = episode_intrusion_steps
        self.uncaught_intrusion_steps = uncaught_intrusion_steps
        self.optimal_defender_reward = optimal_defender_reward
        self.defender_stops_remaining = defender_stops_remaining
        self.defender_first_stop_step = defender_first_stop_step
        self.defender_second_stop_step = defender_second_stop_step
        self.defender_third_stop_step = defender_third_stop_step
        self.defender_fourth_stop_step = defender_fourth_stop_step
        self.episode_snort_severe_baseline_first_stop_step = episode_snort_severe_baseline_first_stop_step
        self.episode_snort_warning_baseline_first_stop_step = episode_snort_warning_baseline_first_stop_step
        self.episode_snort_critical_baseline_first_stop_step = episode_snort_critical_baseline_first_stop_step
        self.episode_var_log_baseline_first_stop_step = episode_var_log_baseline_first_stop_step
        self.episode_step_baseline_first_stop_step = episode_step_baseline_first_stop_step
        self.episode_snort_severe_baseline_second_stop_step = episode_snort_severe_baseline_second_stop_step
        self.episode_snort_warning_baseline_second_stop_step = episode_snort_warning_baseline_second_stop_step
        self.episode_snort_critical_baseline_second_stop_step = episode_snort_critical_baseline_second_stop_step
        self.episode_var_log_baseline_second_stop_step = episode_var_log_baseline_second_stop_step
        self.episode_step_baseline_second_stop_step = episode_step_baseline_second_stop_step
        self.episode_snort_severe_baseline_third_stop_step = episode_snort_severe_baseline_third_stop_step
        self.episode_snort_warning_baseline_third_stop_step = episode_snort_warning_baseline_third_stop_step
        self.episode_snort_critical_baseline_third_stop_step = episode_snort_critical_baseline_third_stop_step
        self.episode_var_log_baseline_third_stop_step = episode_var_log_baseline_third_stop_step
        self.episode_step_baseline_third_stop_step = episode_step_baseline_third_stop_step
        self.episode_snort_severe_baseline_fourth_stop_step = episode_snort_severe_baseline_fourth_stop_step
        self.episode_snort_warning_baseline_fourth_stop_step = episode_snort_warning_baseline_fourth_stop_step
        self.episode_snort_critical_baseline_fourth_stop_step = episode_snort_critical_baseline_fourth_stop_step
        self.episode_var_log_baseline_fourth_stop_step = episode_var_log_baseline_fourth_stop_step
        self.episode_step_baseline_fourth_stop_step = episode_step_baseline_fourth_stop_step
        self.episode_snort_severe_baseline_stops_remaining = episode_snort_severe_baseline_stops_remaining
        self.episode_snort_warning_baseline_stops_remaining = episode_snort_warning_baseline_stops_remaining
        self.episode_snort_critical_baseline_stops_remaining = episode_snort_critical_baseline_stops_remaining
        self.episode_var_log_baseline_stops_remaining = episode_var_log_baseline_stops_remaining
        self.episode_step_baseline_stops_remaining = episode_step_baseline_stops_remaining
        self.optimal_stops_remaining = optimal_stops_remaining
        self.optimal_first_stop_step = optimal_first_stop_step
        self.optimal_second_stop_step = optimal_second_stop_step
        self.optimal_third_stop_step = optimal_third_stop_step
        self.optimal_fourth_stop_step = optimal_fourth_stop_step
        self.optimal_defender_episode_steps = optimal_defender_episode_steps

    def initialize(self) -> None:
        self.attacker_episode_rewards = []
        self.attacker_episode_rewards = []
        self.defender_episode_rewards = []
        self.episode_steps = []
        self.episode_flags = []
        self.episode_caught = []
        self.episode_early_stopped = []
        self.episode_successful_intrusion = []
        self.episode_snort_severe_baseline_rewards = []
        self.episode_snort_warning_baseline_rewards = []
        self.episode_snort_critical_baseline_rewards = []
        self.episode_var_log_baseline_rewards = []
        self.episode_step_baseline_rewards = []
        self.episode_snort_severe_baseline_steps = []
        self.episode_snort_warning_baseline_steps = []
        self.episode_snort_critical_baseline_steps = []
        self.episode_var_log_baseline_steps = []
        self.episode_step_baseline_steps = []
        self.episode_snort_severe_baseline_caught_attacker = []
        self.episode_snort_warning_baseline_caught_attacker = []
        self.episode_snort_critical_baseline_caught_attacker = []
        self.episode_var_log_baseline_caught_attacker = []
        self.episode_step_baseline_caught_attacker = []
        self.episode_snort_severe_baseline_early_stopping = []
        self.episode_snort_warning_baseline_early_stopping = []
        self.episode_snort_critical_baseline_early_stopping = []
        self.episode_var_log_baseline_early_stopping = []
        self.episode_step_baseline_early_stopping = []
        self.episode_snort_severe_baseline_uncaught_intrusion_steps = []
        self.episode_snort_warning_baseline_uncaught_intrusion_steps = []
        self.episode_snort_critical_baseline_uncaught_intrusion_steps = []
        self.episode_var_log_baseline_uncaught_intrusion_steps = []
        self.episode_step_baseline_uncaught_intrusion_steps = []
        self.episode_flags_percentage = []
        self.attacker_env_specific_rewards = {}
        self.defender_env_specific_rewards = {}
        self.env_specific_steps = {}
        self.env_specific_flags = {}
        self.env_specific_flags_percentage = {}
        self.env_response_times = []
        self.action_pred_times = []
        self.attacker_action_costs = []
        self.attacker_action_costs_norm = []
        self.attacker_action_alerts = []
        self.attacker_action_alerts_norm = []
        self.episode_intrusion_steps = []
        self.uncaught_intrusion_steps = []
        self.optimal_defender_reward = []
        self.defender_stops_remaining = []
        self.defender_first_stop_step = []
        self.defender_second_stop_step = []
        self.defender_third_stop_step = []
        self.defender_fourth_stop_step = []
        self.episode_snort_severe_baseline_first_stop_step = []
        self.episode_snort_warning_baseline_first_stop_step = []
        self.episode_snort_critical_baseline_first_stop_step = []
        self.episode_var_log_baseline_first_stop_step = []
        self.episode_step_baseline_first_stop_step = []
        self.episode_snort_severe_baseline_second_stop_step = []
        self.episode_snort_warning_baseline_second_stop_step = []
        self.episode_snort_critical_baseline_second_stop_step = []
        self.episode_var_log_baseline_second_stop_step = []
        self.episode_step_baseline_second_stop_step = []
        self.episode_snort_severe_baseline_third_stop_step = []
        self.episode_snort_warning_baseline_third_stop_step = []
        self.episode_snort_critical_baseline_third_stop_step = []
        self.episode_var_log_baseline_third_stop_step = []
        self.episode_step_baseline_third_stop_step = []
        self.episode_snort_severe_baseline_fourth_stop_step = []
        self.episode_snort_warning_baseline_fourth_stop_step = []
        self.episode_snort_critical_baseline_fourth_stop_step = []
        self.episode_var_log_baseline_fourth_stop_step = []
        self.episode_step_baseline_fourth_stop_step = []
        self.episode_snort_severe_baseline_stops_remaining = []
        self.episode_snort_warning_baseline_stops_remaining = []
        self.episode_snort_critical_baseline_stops_remaining = []
        self.episode_var_log_baseline_stops_remaining = []
        self.episode_step_baseline_stops_remaining = []
        self.optimal_stops_remaining = []
        self.optimal_first_stop_step = []
        self.optimal_second_stop_step = []
        self.optimal_third_stop_step = []
        self.optimal_fourth_stop_step = []
        self.optimal_defender_episode_steps = []


    def copy(self) -> "RolloutDataDTO":
        c = RolloutDataDTO(
            attacker_episode_rewards=self.attacker_episode_rewards,
            defender_episode_rewards=self.defender_episode_rewards,
            episode_steps = self.episode_steps,
            episode_flags = self.episode_flags,
            episode_successful_intrusion=self.episode_successful_intrusion,
            episode_snort_severe_baseline_rewards=self.episode_snort_severe_baseline_caught_attacker,
            episode_snort_warning_baseline_rewards = self.episode_snort_warning_baseline_rewards,
            episode_snort_critical_baseline_rewards = self.episode_snort_critical_baseline_rewards,
            episode_var_log_baseline_rewards = self.episode_var_log_baseline_rewards,
            episode_step_baseline_rewards = self.episode_step_baseline_rewards,
            episode_snort_severe_baseline_steps = self.episode_snort_severe_baseline_steps,
            episode_snort_warning_baseline_steps = self.episode_snort_warning_baseline_steps,
            episode_snort_critical_baseline_steps = self.episode_snort_critical_baseline_steps,
            episode_var_log_baseline_steps = self.episode_var_log_baseline_steps,
            episode_step_baseline_steps = self.episode_step_baseline_steps,
            episode_snort_severe_baseline_caught_attacker = self.episode_snort_severe_baseline_caught_attacker,
            episode_snort_warning_baseline_caught_attacker = self.episode_snort_warning_baseline_caught_attacker,
            episode_snort_critical_baseline_caught_attacker = self.episode_snort_critical_baseline_caught_attacker,
            episode_var_log_baseline_caught_attacker = self.episode_var_log_baseline_caught_attacker,
            episode_step_baseline_caught_attacker = self.episode_step_baseline_caught_attacker,
            episode_snort_severe_baseline_early_stopping = self.episode_snort_severe_baseline_early_stopping,
            episode_snort_warning_baseline_early_stopping = self.episode_snort_warning_baseline_early_stopping,
            episode_snort_critical_baseline_early_stopping = self.episode_snort_critical_baseline_early_stopping,
            episode_var_log_baseline_early_stopping = self.episode_var_log_baseline_early_stopping,
            episode_step_baseline_early_stopping = self.episode_step_baseline_early_stopping,
            episode_snort_severe_baseline_uncaught_intrusion_steps = self.episode_snort_severe_baseline_uncaught_intrusion_steps,
            episode_snort_warning_baseline_uncaught_intrusion_steps = self.episode_snort_warning_baseline_uncaught_intrusion_steps,
            episode_snort_critical_baseline_uncaught_intrusion_steps = self.episode_snort_critical_baseline_uncaught_intrusion_steps,
            episode_var_log_baseline_uncaught_intrusion_steps = self.episode_var_log_baseline_uncaught_intrusion_steps,
            episode_step_baseline_uncaught_intrusion_steps = self.episode_step_baseline_uncaught_intrusion_steps,
            episode_flags_percentage = self.episode_flags_percentage,
            attacker_env_specific_rewards = self.attacker_env_specific_rewards,
            defender_env_specific_rewards = self.defender_env_specific_rewards,
            env_specific_steps = self.env_specific_steps,
            env_specific_flags = self.env_specific_flags,
            env_specific_flags_percentage = self.env_specific_flags_percentage,
            env_response_times = self.env_response_times,
            action_pred_times = self.action_pred_times,
            attacker_action_costs = self.attacker_action_costs,
            attacker_action_costs_norm = self.attacker_action_costs_norm,
            attacker_action_alerts = self.attacker_action_alerts,
            attacker_action_alerts_norm = self.attacker_action_alerts_norm,
            episode_intrusion_steps = self.episode_intrusion_steps,
            uncaught_intrusion_steps = self.uncaught_intrusion_steps,
            optimal_defender_reward = self.optimal_defender_reward,
            defender_stops_remaining = self.defender_stops_remaining,
            defender_first_stop_step = self.defender_first_stop_step,
            defender_second_stop_step = self.defender_second_stop_step,
            defender_third_stop_step = self.defender_third_stop_step,
            defender_fourth_stop_step = self.defender_fourth_stop_step,
            episode_snort_severe_baseline_first_stop_step = self.episode_snort_severe_baseline_first_stop_step,
            episode_snort_warning_baseline_first_stop_step = self.episode_snort_warning_baseline_first_stop_step,
            episode_snort_critical_baseline_first_stop_step = self.episode_snort_critical_baseline_first_stop_step,
            episode_var_log_baseline_first_stop_step = self.episode_var_log_baseline_first_stop_step,
            episode_step_baseline_first_stop_step = self.episode_step_baseline_first_stop_step,
            episode_snort_severe_baseline_second_stop_step = self.episode_snort_severe_baseline_second_stop_step,
            episode_snort_warning_baseline_second_stop_step = self.episode_snort_warning_baseline_second_stop_step,
            episode_snort_critical_baseline_second_stop_step = self.episode_snort_critical_baseline_second_stop_step,
            episode_var_log_baseline_second_stop_step = self.episode_var_log_baseline_second_stop_step,
            episode_step_baseline_second_stop_step = self.episode_step_baseline_second_stop_step,
            episode_snort_severe_baseline_third_stop_step = self.episode_snort_severe_baseline_third_stop_step,
            episode_snort_warning_baseline_third_stop_step = self.episode_snort_warning_baseline_third_stop_step,
            episode_snort_critical_baseline_third_stop_step = self.episode_snort_critical_baseline_third_stop_step,
            episode_var_log_baseline_third_stop_step = self.episode_var_log_baseline_third_stop_step,
            episode_step_baseline_third_stop_step = self.episode_step_baseline_third_stop_step,
            episode_snort_severe_baseline_fourth_stop_step = self.episode_snort_severe_baseline_fourth_stop_step,
            episode_snort_warning_baseline_fourth_stop_step = self.episode_snort_warning_baseline_fourth_stop_step,
            episode_snort_critical_baseline_fourth_stop_step = self.episode_snort_critical_baseline_fourth_stop_step,
            episode_var_log_baseline_fourth_stop_step = self.episode_var_log_baseline_fourth_stop_step,
            episode_step_baseline_fourth_stop_step = self.episode_step_baseline_fourth_stop_step,
            episode_snort_severe_baseline_stops_remaining = self.episode_snort_severe_baseline_stops_remaining,
            episode_snort_warning_baseline_stops_remaining = self.episode_snort_warning_baseline_stops_remaining,
            episode_snort_critical_baseline_stops_remaining = self.episode_snort_critical_baseline_stops_remaining,
            episode_var_log_baseline_stops_remaining = self.episode_var_log_baseline_stops_remaining,
            episode_step_baseline_stops_remaining = self.episode_step_baseline_stops_remaining,
            optimal_stops_remaining = self.optimal_stops_remaining,
            optimal_first_stop_step = self.optimal_first_stop_step,
            optimal_second_stop_step = self.optimal_second_stop_step,
            optimal_third_stop_step = self.optimal_third_stop_step,
            optimal_fourth_stop_step = self.optimal_fourth_stop_step,
            optimal_defender_episode_steps = self.optimal_defender_episode_steps
        )
        return c

    def update_done(self, attacker_reward : List[float], defender_reward : List[float], steps: List[int]):
        self.attacker_episode_rewards.append(attacker_reward)
        self.defender_episode_rewards.append(defender_reward)
        self.episode_steps.append(steps)

    def update(self, attacker_rewards: List[float], defender_rewards: List[float], episode_steps: List[int],
               infos: List[dict], i: int, env_response_time: float, action_pred_time: float,
               attacker_agent_config: AgentConfig) -> None:
        self.attacker_episode_rewards.append(attacker_rewards)
        self.defender_episode_rewards.append(defender_rewards)
        self.episode_steps.append(infos[i][constants.INFO_DICT.EPISODE_LENGTH])
        self.episode_steps.append(episode_steps)
        self.episode_flags.append(infos[i][constants.INFO_DICT.FLAGS])
        self.episode_caught.append(infos[i][constants.INFO_DICT.CAUGHT_ATTACKER])
        self.episode_early_stopped.append(infos[i][constants.INFO_DICT.EARLY_STOPPED])
        self.episode_successful_intrusion.append(infos[i][constants.INFO_DICT.SUCCESSFUL_INTRUSION])
        self.episode_snort_severe_baseline_rewards.append(infos[i][constants.INFO_DICT.SNORT_SEVERE_BASELINE_REWARD])
        self.episode_snort_warning_baseline_rewards.append(infos[i][constants.INFO_DICT.SNORT_WARNING_BASELINE_REWARD])
        self.episode_snort_critical_baseline_rewards.append(infos[i][constants.INFO_DICT.SNORT_CRITICAL_BASELINE_REWARD])
        self.episode_var_log_baseline_rewards.append(infos[i][constants.INFO_DICT.VAR_LOG_BASELINE_REWARD])
        self.episode_step_baseline_rewards.append(infos[i][constants.INFO_DICT.STEP_BASELINE_REWARD])
        self.episode_snort_severe_baseline_steps.append(infos[i][constants.INFO_DICT.SNORT_SEVERE_BASELINE_STEP])
        self.episode_snort_warning_baseline_steps.append(infos[i][constants.INFO_DICT.SNORT_WARNING_BASELINE_STEP])
        self.episode_snort_critical_baseline_steps.append(infos[i][constants.INFO_DICT.SNORT_CRITICAL_BASELINE_STEP])
        self.episode_var_log_baseline_steps.append(infos[i][constants.INFO_DICT.VAR_LOG_BASELINE_STEP])
        self.episode_step_baseline_steps.append(infos[i][constants.INFO_DICT.STEP_BASELINE_STEP])
        self.episode_snort_severe_baseline_caught_attacker.append(infos[i][constants.INFO_DICT.SNORT_SEVERE_BASELINE_CAUGHT_ATTACKER])
        self.episode_snort_warning_baseline_caught_attacker.append(infos[i][constants.INFO_DICT.SNORT_WARNING_BASELINE_CAUGHT_ATTACKER])
        self.episode_snort_critical_baseline_caught_attacker.append(infos[i][constants.INFO_DICT.SNORT_CRITICAL_BASELINE_CAUGHT_ATTACKER])
        self.episode_var_log_baseline_caught_attacker.append(infos[i][constants.INFO_DICT.VAR_LOG_BASELINE_CAUGHT_ATTACKER])
        self.episode_step_baseline_caught_attacker.append(infos[i][constants.INFO_DICT.STEP_BASELINE_CAUGHT_ATTACKER])
        self.episode_snort_severe_baseline_early_stopping.append(infos[i][constants.INFO_DICT.SNORT_SEVERE_BASELINE_EARLY_STOPPING])
        self.episode_snort_warning_baseline_early_stopping.append(infos[i][constants.INFO_DICT.SNORT_WARNING_BASELINE_EARLY_STOPPING])
        self.episode_snort_critical_baseline_early_stopping.append(infos[i][constants.INFO_DICT.SNORT_CRITICAL_BASELINE_EARLY_STOPPING])
        self.episode_var_log_baseline_early_stopping.append(infos[i][constants.INFO_DICT.VAR_LOG_BASELINE_EARLY_STOPPING])
        self.episode_step_baseline_early_stopping.append(infos[i][constants.INFO_DICT.STEP_BASELINE_EARLY_STOPPING])
        self.episode_snort_severe_baseline_uncaught_intrusion_steps.append(infos[i][constants.INFO_DICT.SNORT_SEVERE_BASELINE_UNCAUGHT_INTRUSION_STEPS])
        self.episode_snort_warning_baseline_uncaught_intrusion_steps.append(infos[i][constants.INFO_DICT.SNORT_WARNING_BASELINE_UNCAUGHT_INTRUSION_STEPS])
        self.episode_snort_critical_baseline_uncaught_intrusion_steps.append(infos[i][constants.INFO_DICT.SNORT_CRITICAL_BASELINE_UNCAUGHT_INTRUSION_STEPS])
        self.episode_var_log_baseline_uncaught_intrusion_steps.append(infos[i][constants.INFO_DICT.VAR_LOG_BASELINE_UNCAUGHT_INTRUSION_STEPS])
        self.episode_step_baseline_uncaught_intrusion_steps.append(infos[i][constants.INFO_DICT.STEP_BASELINE_UNCAUGHT_INTRUSION_STEPS])
        self.attacker_action_costs.append(infos[i][constants.INFO_DICT.ATTACKER_COST])
        self.attacker_action_costs_norm.append(infos[i][constants.INFO_DICT.ATTACKER_COST_NORM])
        self.attacker_action_alerts.append(infos[i][constants.INFO_DICT.ATTACKER_ALERTS])
        self.attacker_action_alerts_norm.append(infos[i][constants.INFO_DICT.ATTACKER_ALERTS_NORM])
        self.episode_intrusion_steps.append(infos[i][constants.INFO_DICT.INTRUSION_STEP])
        self.uncaught_intrusion_steps.append(infos[i][constants.INFO_DICT.UNCAUGHT_INTRUSION_STEPS])
        self.optimal_defender_reward.append(infos[i][constants.INFO_DICT.OPTIMAL_DEFENDER_REWARD])
        self.defender_stops_remaining.append(infos[i][constants.INFO_DICT.DEFENDER_STOPS_REMAINING])
        self.defender_first_stop_step.append(infos[i][constants.INFO_DICT.DEFENDER_FIRST_STOP_STEP])
        self.defender_second_stop_step.append(infos[i][constants.INFO_DICT.DEFENDER_SECOND_STOP_STEP])
        self.defender_third_stop_step.append(infos[i][constants.INFO_DICT.DEFENDER_THIRD_STOP_STEP])
        self.defender_fourth_stop_step.append(infos[i][constants.INFO_DICT.DEFENDER_FOURTH_STOP_STEP])
        self.episode_snort_severe_baseline_first_stop_step.append(infos[i][constants.INFO_DICT.SNORT_SEVERE_BASELINE_FIRST_STOP_STEP])
        self.episode_snort_warning_baseline_first_stop_step.append(infos[i][constants.INFO_DICT.SNORT_WARNING_BASELINE_FIRST_STOP_STEP])
        self.episode_snort_critical_baseline_first_stop_step.append(infos[i][constants.INFO_DICT.SNORT_CRITICAL_BASELINE_FIRST_STOP_STEP])
        self.episode_var_log_baseline_first_stop_step.append(infos[i][constants.INFO_DICT.VAR_LOG_BASELINE_FIRST_STOP_STEP])
        self.episode_step_baseline_first_stop_step.append(infos[i][constants.INFO_DICT.STEP_BASELINE_FIRST_STOP_STEP])
        self.episode_snort_severe_baseline_second_stop_step.append(infos[i][constants.INFO_DICT.SNORT_SEVERE_BASELINE_SECOND_STOP_STEP])
        self.episode_snort_warning_baseline_second_stop_step.append(infos[i][constants.INFO_DICT.SNORT_WARNING_BASELINE_SECOND_STOP_STEP])
        self.episode_snort_critical_baseline_second_stop_step.append(infos[i][constants.INFO_DICT.SNORT_CRITICAL_BASELINE_SECOND_STOP_STEP])
        self.episode_var_log_baseline_second_stop_step.append(infos[i][constants.INFO_DICT.VAR_LOG_BASELINE_SECOND_STOP_STEP])
        self.episode_step_baseline_second_stop_step.append(infos[i][constants.INFO_DICT.STEP_BASELINE_SECOND_STOP_STEP])
        self.episode_snort_severe_baseline_third_stop_step.append(infos[i][constants.INFO_DICT.SNORT_SEVERE_BASELINE_THIRD_STOP_STEP])
        self.episode_snort_warning_baseline_third_stop_step.append(infos[i][constants.INFO_DICT.SNORT_WARNING_BASELINE_THIRD_STOP_STEP])
        self.episode_snort_critical_baseline_third_stop_step.append(infos[i][constants.INFO_DICT.SNORT_CRITICAL_BASELINE_THIRD_STOP_STEP])
        self.episode_var_log_baseline_third_stop_step.append(infos[i][constants.INFO_DICT.VAR_LOG_BASELINE_THIRD_STOP_STEP])
        self.episode_step_baseline_third_stop_step.append(infos[i][constants.INFO_DICT.STEP_BASELINE_THIRD_STOP_STEP])
        self.episode_snort_severe_baseline_fourth_stop_step.append(infos[i][constants.INFO_DICT.SNORT_SEVERE_BASELINE_FOURTH_STOP_STEP])
        self.episode_snort_warning_baseline_fourth_stop_step.append(infos[i][constants.INFO_DICT.SNORT_WARNING_BASELINE_FOURTH_STOP_STEP])
        self.episode_snort_critical_baseline_fourth_stop_step.append(infos[i][constants.INFO_DICT.SNORT_CRITICAL_BASELINE_FOURTH_STOP_STEP])
        self.episode_var_log_baseline_fourth_stop_step.append(infos[i][constants.INFO_DICT.VAR_LOG_BASELINE_FOURTH_STOP_STEP])
        self.episode_step_baseline_fourth_stop_step.append(infos[i][constants.INFO_DICT.STEP_BASELINE_FOURTH_STOP_STEP])
        self.episode_snort_severe_baseline_stops_remaining.append(infos[i][constants.INFO_DICT.SNORT_SEVERE_BASELINE_STOPS_REMAINING])
        self.episode_snort_warning_baseline_stops_remaining.append(infos[i][constants.INFO_DICT.SNORT_WARNING_BASELINE_STOPS_REMAINING])
        self.episode_snort_critical_baseline_stops_remaining.append(infos[i][constants.INFO_DICT.SNORT_CRITICAL_BASELINE_STOPS_REMAINING])
        self.episode_var_log_baseline_stops_remaining.append(infos[i][constants.INFO_DICT.VAR_LOG_BASELINE_STOPS_REMAINING])
        self.episode_step_baseline_stops_remaining.append(infos[i][constants.INFO_DICT.STEP_BASELINE_STOPS_REMAINING])
        self.optimal_stops_remaining.append(infos[i][constants.INFO_DICT.OPTIMAL_STOPS_REMAINING])
        self.optimal_first_stop_step.append(infos[i][constants.INFO_DICT.OPTIMAL_FIRST_STOP_STEP])
        self.optimal_second_stop_step.append(infos[i][constants.INFO_DICT.OPTIMAL_SECOND_STOP_STEP])
        self.optimal_third_stop_step.append(infos[i][constants.INFO_DICT.OPTIMAL_THIRD_STOP_STEP])
        self.optimal_fourth_stop_step.append(infos[i][constants.INFO_DICT.OPTIMAL_FOURTH_STOP_STEP])
        self.optimal_defender_episode_steps.append(infos[i][constants.INFO_DICT.OPTIMAL_DEFENDER_EPISODE_STEPS])

        if attacker_agent_config.env_config is not None:
            self.episode_flags_percentage.append(
                infos[i][constants.INFO_DICT.FLAGS] / attacker_agent_config.env_config.num_flags
            )  # TODO this does not work with DR
        else:
            # print("env config None?:{}".format(self.attacker_agent_config.env_config))
            self.episode_flags_percentage.append(
                infos[i][constants.INFO_DICT.FLAGS] / attacker_agent_config.env_configs[
                    infos[i][constants.INFO_DICT.IDX]].num_flags)

        if attacker_agent_config.performance_analysis:
            self.env_response_times.append(env_response_time)
            self.action_pred_times.append(action_pred_time)
            env_response_time = 0
            action_pred_time = 0

        self.update_env_specific_metrics(infos=infos, i=i, agent_config=attacker_agent_config)



    def update_env_specific_metrics(self, infos, i, agent_config: AgentConfig):

        if agent_config.env_config is not None:
            num_flags = agent_config.env_config.num_flags
            if agent_config.env_config.emulation_config is not None:
                agent_ip = agent_config.env_config.emulation_config.agent_ip
            else:
                agent_ip = agent_config.env_config.idx
        else:
            if agent_config.env_configs[i].emulation_config is not None:
                agent_ip = agent_config.env_configs[i].emulation_config.agent_ip
            else:
                agent_ip = agent_config.env_configs[i].idx
            num_flags = agent_config.env_configs[infos[i]["idx"]].num_flags

        if i < len(self.attacker_episode_rewards):
            if agent_ip not in self.attacker_env_specific_rewards:
                self.attacker_env_specific_rewards[agent_ip] = [self.attacker_episode_rewards[i]]
            else:
                self.attacker_env_specific_rewards[agent_ip].append(self.attacker_episode_rewards[i])

        if i < len(self.defender_episode_rewards):
            if agent_ip not in self.defender_env_specific_rewards:
                self.defender_env_specific_rewards[agent_ip] = [self.defender_episode_rewards[i]]
            else:
                self.defender_env_specific_rewards[agent_ip].append(self.defender_episode_rewards[i])

        if i < len(self.episode_steps):
            if agent_ip not in self.env_specific_steps:
                self.env_specific_steps[agent_ip] = [self.episode_steps[i]]
            else:
                self.env_specific_steps[agent_ip].append(self.episode_steps[i])

        if i < len(infos):
            if agent_ip not in self.env_specific_flags:
                self.env_specific_flags[agent_ip] = [infos[i]["flags"]]
            else:
                self.env_specific_flags[agent_ip].append(infos[i]["flags"])

        if i < len(infos):
            if agent_ip not in self.env_specific_flags_percentage:
                self.env_specific_flags_percentage[agent_ip] = [infos[i]["flags"] / num_flags]
            else:
                self.env_specific_flags_percentage[agent_ip].append(infos[i]["flags"] / num_flags)
