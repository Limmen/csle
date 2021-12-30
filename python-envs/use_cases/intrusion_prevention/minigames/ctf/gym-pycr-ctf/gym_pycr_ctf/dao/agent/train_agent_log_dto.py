from typing import List
import time
import pycr_common.constants.constants as constants
from pycr_common.dao.agent.base_train_agent_log_dto import BaseTrainAgentLogDTO
from pycr_common.dao.agent.train_mode import TrainMode
from pycr_common.agents.config.agent_config import AgentConfig
from pycr_common.agents.config.agent_config import AgentConfig
from gym_pycr_ctf.dao.experiment.experiment_result import ExperimentResult
from gym_pycr_ctf.dao.network.env_config import PyCREnvConfig
from gym_pycr_ctf.dao.agent.rollout_data_dto import RolloutDataDTO
from gym_pycr_ctf.dao.agent.attacker_train_agent_log_dto_avg import AttackerTrainAgentLogDTOAvg
from gym_pycr_ctf.dao.agent.defender_train_agent_log_dto_avg import DefenderTrainAgentLogDTOAvg
from gym_pycr_ctf.envs.pycr_ctf_env import PyCRCTFEnv


class TrainAgentLogDTO(BaseTrainAgentLogDTO):
    """
    DTO with information for logging during training
    """
    def __init__(self, iteration: int = 0, train_result : ExperimentResult = None, eval_result: ExperimentResult = None,
                 attacker_episode_rewards: List[float] = None,
                 attacker_episode_avg_loss: List[float] = None,
                 attacker_lr: float = 0.0,
                 defender_episode_rewards: List[float] = None,
                 defender_episode_avg_loss: List[float] = None,
                 defender_lr: float = 0.0,
                 total_num_episodes : int = 1,
                 episode_steps : List[int] = None, episode_flags : List[int] = None,
                 eval: bool = False, episode_flags_percentage: List[float] = None, progress_left : float = 0.0,
                 n_af : int = 0, n_d : int = 0,
                 attacker_eval_episode_rewards: List[int] = None,
                 defender_eval_episode_rewards: List[int] = None,
                 eval_episode_steps : List[int] = None, eval_episode_flags : List[int] = None,
                 eval_episode_flags_percentage : List[float]= None,
                 attacker_eval_2_episode_rewards : List[int] = None,
                 defender_eval_2_episode_rewards: List[int] = None,
                 eval_2_episode_steps: List[int] = None, eval_2_episode_flags: List[int] = None,
                 eval_2_episode_flags_percentage: List[float] = None,
                 attacker_train_episode_env_specific_rewards: dict = None,
                 defender_train_episode_env_specific_rewards: dict = None,
                 train_env_specific_steps: dict = None,
                 train_env_specific_flags: dict = None,
                 train_env_specific_flags_percentage: dict = None,
                 attacker_eval_env_specific_rewards: dict = None,
                 defender_eval_env_specific_rewards: dict = None,
                 eval_env_specific_steps: dict = None,
                 eval_env_specific_flags: dict = None,
                 eval_env_specific_flags_percentage: dict = None,
                 attacker_eval_2_env_specific_rewards: dict = None,
                 defender_eval_2_env_specific_rewards: dict = None,
                 eval_2_env_specific_steps: dict = None,
                 eval_2_env_specific_flags: dict = None,
                 eval_2_env_specific_flags_percentage: dict = None,
                 rollout_times : List[float] = None, env_response_times: List[float]= None,
                 action_pred_times : List[float] = None, grad_comp_times : List[float] = None,
                 weight_update_times : List[float]= None,
                 episode_caught : List[int] = None, episode_early_stopped : List[int] = None,
                 episode_successful_intrusion : List[int] = None,
                 eval_episode_caught : List[int] = None,
                 eval_episode_early_stopped : List[int] = None,
                 eval_episode_successful_intrusion : List[int] = None,
                 eval_2_episode_caught: List[int] = None,
                 eval_2_episode_early_stopped: List[int] = None,
                 eval_2_episode_successful_intrusion: List[int] = None,
                 episode_snort_severe_baseline_rewards : List[int] = None,
                 episode_snort_warning_baseline_rewards: List[int] = None,
                 eval_episode_snort_severe_baseline_rewards: List[int] = None,
                 eval_episode_snort_warning_baseline_rewards: List[int] = None,
                 eval_2_episode_snort_severe_baseline_rewards: List[int] = None,
                 eval_2_episode_snort_warning_baseline_rewards: List[int] = None,
                 episode_snort_critical_baseline_rewards: List[int] = None,
                 episode_var_log_baseline_rewards: List[int] = None,
                 eval_episode_snort_critical_baseline_rewards: List[int] = None,
                 eval_episode_var_log_baseline_rewards: List[int] = None,
                 eval_2_episode_snort_critical_baseline_rewards: List[int] = None,
                 eval_2_episode_var_log_baseline_rewards: List[int] = None,
                 episode_snort_severe_baseline_steps: List[int] = None,
                 episode_snort_warning_baseline_steps: List[int] = None,
                 eval_episode_snort_severe_baseline_steps: List[int] = None,
                 eval_episode_snort_warning_baseline_steps: List[int] = None,
                 eval_2_episode_snort_severe_baseline_steps: List[int] = None,
                 eval_2_episode_snort_warning_baseline_steps: List[int] = None,
                 episode_snort_critical_baseline_steps: List[int] = None,
                 episode_var_log_baseline_steps: List[int] = None,
                 eval_episode_snort_critical_baseline_steps: List[int] = None,
                 eval_episode_var_log_baseline_steps: List[int] = None,
                 eval_2_episode_snort_critical_baseline_steps: List[int] = None,
                 eval_2_episode_var_log_baseline_steps: List[int] = None,
                 episode_step_baseline_rewards : List[int] = None,
                 episode_step_baseline_steps: List[int] = None,
                 eval_episode_step_baseline_rewards: List[int] = None,
                 eval_episode_step_baseline_steps: List[int] = None,
                 eval_2_episode_step_baseline_rewards: List[int] = None,
                 eval_2_episode_step_baseline_steps: List[int] = None,
                 attacker_action_costs :List[float] = None,
                 attacker_action_costs_norm :List[float] = None,
                 attacker_action_alerts :List[float] = None,
                 attacker_action_alerts_norm :List[float] = None,
                 eval_attacker_action_costs: List[float] = None,
                 eval_attacker_action_costs_norm: List[float] = None,
                 eval_attacker_action_alerts: List[float] = None,
                 eval_attacker_action_alerts_norm: List[float] = None,
                 eval_2_attacker_action_costs: List[float] = None,
                 eval_2_attacker_action_costs_norm: List[float] = None,
                 eval_2_attacker_action_alerts: List[float] = None,
                 eval_2_attacker_action_alerts_norm: List[float] = None,
                 start_time: float = 0.0,
                 episode_intrusion_steps: List[int] = None,
                 eval_episode_intrusion_steps: List[int] = None,
                 eval_2_episode_intrusion_steps: List[int] = None,
                 episode_snort_severe_baseline_caught_attacker: List[int] = None,
                 episode_snort_warning_baseline_caught_attacker: List[int] = None,
                 eval_episode_snort_severe_baseline_caught_attacker: List[int] = None,
                 eval_episode_snort_warning_baseline_caught_attacker: List[int] = None,
                 eval_2_episode_snort_severe_baseline_caught_attacker: List[int] = None,
                 eval_2_episode_snort_warning_baseline_caught_attacker: List[int] = None,
                 episode_snort_critical_baseline_caught_attacker: List[int] = None,
                 episode_var_log_baseline_caught_attacker: List[int] = None,
                 eval_episode_snort_critical_baseline_caught_attacker: List[int] = None,
                 eval_episode_var_log_baseline_caught_attacker: List[int] = None,
                 eval_2_episode_snort_critical_baseline_caught_attacker: List[int] = None,
                 eval_2_episode_var_log_baseline_caught_attacker: List[int] = None,
                 episode_step_baseline_caught_attacker: List[int] = None,
                 eval_episode_step_baseline_caught_attacker: List[int] = None,
                 eval_2_episode_step_baseline_caught_attacker: List[int] = None,
                 episode_snort_severe_baseline_early_stopping: List[int] = None,
                 episode_snort_warning_baseline_early_stopping: List[int] = None,
                 eval_episode_snort_severe_baseline_early_stopping: List[int] = None,
                 eval_episode_snort_warning_baseline_early_stopping: List[int] = None,
                 eval_2_episode_snort_severe_baseline_early_stopping: List[int] = None,
                 eval_2_episode_snort_warning_baseline_early_stopping: List[int] = None,
                 episode_snort_critical_baseline_early_stopping: List[int] = None,
                 episode_var_log_baseline_early_stopping: List[int] = None,
                 eval_episode_snort_critical_baseline_early_stopping: List[int] = None,
                 eval_episode_var_log_baseline_early_stopping: List[int] = None,
                 eval_2_episode_snort_critical_baseline_early_stopping: List[int] = None,
                 eval_2_episode_var_log_baseline_early_stopping: List[int] = None,
                 episode_step_baseline_early_stopping: List[int] = None,
                 eval_episode_step_baseline_early_stopping: List[int] = None,
                 eval_2_episode_step_baseline_early_stopping: List[int] = None,
                 episode_snort_severe_baseline_uncaught_intrusion_steps: List[int] = None,
                 episode_snort_warning_baseline_uncaught_intrusion_steps: List[int] = None,
                 eval_episode_snort_severe_baseline_uncaught_intrusion_steps: List[int] = None,
                 eval_episode_snort_warning_baseline_uncaught_intrusion_steps: List[int] = None,
                 eval_2_episode_snort_severe_baseline_uncaught_intrusion_steps: List[int] = None,
                 eval_2_episode_snort_warning_baseline_uncaught_intrusion_steps: List[int] = None,
                 episode_snort_critical_baseline_uncaught_intrusion_steps: List[int] = None,
                 episode_var_log_baseline_uncaught_intrusion_steps: List[int] = None,
                 eval_episode_snort_critical_baseline_uncaught_intrusion_steps: List[int] = None,
                 eval_episode_var_log_baseline_uncaught_intrusion_steps: List[int] = None,
                 eval_2_episode_snort_critical_baseline_uncaught_intrusion_steps: List[int] = None,
                 eval_2_episode_var_log_baseline_uncaught_intrusion_steps: List[int] = None,
                 episode_step_baseline_uncaught_intrusion_steps: List[int] = None,
                 eval_episode_step_baseline_uncaught_intrusion_steps: List[int] = None,
                 eval_2_episode_step_baseline_uncaught_intrusion_steps: List[int] = None,
                 uncaught_intrusion_steps : List[int] = None,
                 eval_uncaught_intrusion_steps: List[int] = None,
                 eval_2_uncaught_intrusion_steps: List[int] = None,
                 optimal_defender_reward: List[int] = None,
                 eval_optimal_defender_reward: List[int] = None,
                 eval_2_optimal_defender_reward: List[int] = None,
                 defender_stops_remaining : List[int] = None,
                 eval_defender_stops_remaining: List[int] = None,
                 eval_2_defender_stops_remaining: List[int] = None,
                 defender_first_stop_step: List[int] = None,
                 eval_defender_first_stop_step: List[int] = None,
                 eval_2_defender_first_stop_step: List[int] = None,
                 defender_second_stop_step: List[int] = None,
                 eval_defender_second_stop_step: List[int] = None,
                 eval_2_defender_second_stop_step: List[int] = None,
                 defender_third_stop_step: List[int] = None,
                 eval_defender_third_stop_step: List[int] = None,
                 eval_2_defender_third_stop_step: List[int] = None,
                 defender_fourth_stop_step: List[int] = None,
                 eval_defender_fourth_stop_step: List[int] = None,
                 eval_2_defender_fourth_stop_step: List[int] = None,
                 episode_snort_severe_baseline_first_stop_step: List[int] = None,
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
                 eval_episode_snort_severe_baseline_first_stop_step: List[int] = None,
                 eval_episode_snort_warning_baseline_first_stop_step: List[int] = None,
                 eval_episode_snort_critical_baseline_first_stop_step: List[int] = None,
                 eval_episode_var_log_baseline_first_stop_step: List[int] = None,
                 eval_episode_step_baseline_first_stop_step: List[int] = None,
                 eval_episode_snort_severe_baseline_second_stop_step: List[int] = None,
                 eval_episode_snort_warning_baseline_second_stop_step: List[int] = None,
                 eval_episode_snort_critical_baseline_second_stop_step: List[int] = None,
                 eval_episode_var_log_baseline_second_stop_step: List[int] = None,
                 eval_episode_step_baseline_second_stop_step: List[int] = None,
                 eval_episode_snort_severe_baseline_third_stop_step: List[int] = None,
                 eval_episode_snort_warning_baseline_third_stop_step: List[int] = None,
                 eval_episode_snort_critical_baseline_third_stop_step: List[int] = None,
                 eval_episode_var_log_baseline_third_stop_step: List[int] = None,
                 eval_episode_step_baseline_third_stop_step: List[int] = None,
                 eval_episode_snort_severe_baseline_fourth_stop_step: List[int] = None,
                 eval_episode_snort_warning_baseline_fourth_stop_step: List[int] = None,
                 eval_episode_snort_critical_baseline_fourth_stop_step: List[int] = None,
                 eval_episode_var_log_baseline_fourth_stop_step: List[int] = None,
                 eval_episode_step_baseline_fourth_stop_step: List[int] = None,
                 eval_episode_snort_severe_baseline_stops_remaining: List[int] = None,
                 eval_episode_snort_warning_baseline_stops_remaining: List[int] = None,
                 eval_episode_snort_critical_baseline_stops_remaining: List[int] = None,
                 eval_episode_var_log_baseline_stops_remaining: List[int] = None,
                 eval_episode_step_baseline_stops_remaining: List[int] = None,
                 eval_2_episode_snort_severe_baseline_first_stop_step: List[int] = None,
                 eval_2_episode_snort_warning_baseline_first_stop_step: List[int] = None,
                 eval_2_episode_snort_critical_baseline_first_stop_step: List[int] = None,
                 eval_2_episode_var_log_baseline_first_stop_step: List[int] = None,
                 eval_2_episode_step_baseline_first_stop_step: List[int] = None,
                 eval_2_episode_snort_severe_baseline_second_stop_step: List[int] = None,
                 eval_2_episode_snort_warning_baseline_second_stop_step: List[int] = None,
                 eval_2_episode_snort_critical_baseline_second_stop_step: List[int] = None,
                 eval_2_episode_var_log_baseline_second_stop_step: List[int] = None,
                 eval_2_episode_step_baseline_second_stop_step: List[int] = None,
                 eval_2_episode_snort_severe_baseline_third_stop_step: List[int] = None,
                 eval_2_episode_snort_warning_baseline_third_stop_step: List[int] = None,
                 eval_2_episode_snort_critical_baseline_third_stop_step: List[int] = None,
                 eval_2_episode_var_log_baseline_third_stop_step: List[int] = None,
                 eval_2_episode_step_baseline_third_stop_step: List[int] = None,
                 eval_2_episode_snort_severe_baseline_fourth_stop_step: List[int] = None,
                 eval_2_episode_snort_warning_baseline_fourth_stop_step: List[int] = None,
                 eval_2_episode_snort_critical_baseline_fourth_stop_step: List[int] = None,
                 eval_2_episode_var_log_baseline_fourth_stop_step: List[int] = None,
                 eval_2_episode_step_baseline_fourth_stop_step: List[int] = None,
                 eval_2_episode_snort_severe_baseline_stops_remaining: List[int] = None,
                 eval_2_episode_snort_warning_baseline_stops_remaining: List[int] = None,
                 eval_2_episode_snort_critical_baseline_stops_remaining: List[int] = None,
                 eval_2_episode_var_log_baseline_stops_remaining: List[int] = None,
                 eval_2_episode_step_baseline_stops_remaining: List[int] = None,
                 optimal_stops_remaining: List[int] = None,
                 eval_optimal_stops_remaining: List[int] = None,
                 eval_2_optimal_stops_remaining: List[int] = None,
                 optimal_first_stop_step: List[int] = None,
                 eval_optimal_first_stop_step: List[int] = None,
                 eval_2_optimal_first_stop_step: List[int] = None,
                 optimal_second_stop_step: List[int] = None,
                 eval_optimal_second_stop_step: List[int] = None,
                 eval_2_optimal_second_stop_step: List[int] = None,
                 optimal_third_stop_step: List[int] = None,
                 eval_optimal_third_stop_step: List[int] = None,
                 eval_2_optimal_third_stop_step: List[int] = None,
                 optimal_fourth_stop_step: List[int] = None,
                 eval_optimal_fourth_stop_step: List[int] = None,
                 eval_2_optimal_fourth_stop_step: List[int] = None,
                 optimal_defender_episode_steps: List[int] = None,
                 eval_optimal_defender_episode_steps: List[int] = None,
                 eval_2_optimal_defender_episode_steps: List[int] = None
                 ):
        """
        Initializes the DTO

        :param iteration: the iteration
        :param train_result: the accumulated training result
        :param eval_result: the accumulated evaluation result
        :param attacker_episode_rewards: the list of attacker rewards
        :param attacker_episode_avg_loss: the list of losses of the attacker
        :param attacker_lr: the list of learning rates of the attacker
        :param defender_episode_rewards: the list of rewards of the defender
        :param defender_episode_avg_loss: the list of losses of the defender
        :param defender_lr: the list of learning rates of the defender
        :param total_num_episodes: the total number of episodes
        :param episode_steps: the list of episode steps
        :param episode_flags: the list of episode flags
        :param eval: boolean flag whether this is an evaluation or not
        :param episode_flags_percentage: a list of percentages of flags captured
        :param progress_left: fraction of progress left
        :param n_af: number of times all flags were captured
        :param n_d: number of times the attacker was detected
        :param attacker_eval_episode_rewards: list of rewards of the attacker
        :param defender_eval_episode_rewards: list of rewards of the defender
        :param eval_episode_steps: list of evaluation steps
        :param eval_episode_flags: list of evalation flags
        :param eval_episode_flags_percentage: list of flags percentages
        :param attacker_eval_2_episode_rewards: list of attacker episode rewards in the second eval environment
        :param defender_eval_2_episode_rewards: list of defender episode rewards in the second eval environment
        :param eval_2_episode_steps: list of steps in the second eval environment
        :param eval_2_episode_flags: list of flags captured in the second eval environment
        :param eval_2_episode_flags_percentage: list of percentages of flags captured
        :param attacker_train_episode_env_specific_rewards: list of attacker rewards captured per environment
        :param defender_train_episode_env_specific_rewards: list of defender rewards captured per environment
        :param train_env_specific_steps: list of steps per environment
        :param train_env_specific_flags: list of flags per environment
        :param train_env_specific_flags_percentage: list of percetanges of flags captured per environment
        :param attacker_eval_env_specific_rewards: list of attacker rewards per eval environment
        :param defender_eval_env_specific_rewards: list of defende rewards per eval environment
        :param eval_env_specific_steps: list of steps per eval environment
        :param eval_env_specific_flags: list of flags captured per eval environment
        :param eval_env_specific_flags_percentage: list of percentages of flags captured per environment
        :param attacker_eval_2_env_specific_rewards: list of attacker rewards captured for each eval2 environment
        :param defender_eval_2_env_specific_rewards: list of defender rewards captured for each eval2 environment
        :param eval_2_env_specific_steps: list of steps for each eval2 environment
        :param eval_2_env_specific_flags: list of flags for each eval2 environment
        :param eval_2_env_specific_flags_percentage: list of percentages of flags captured for each eval2 environment
        :param rollout_times: list of rollout times
        :param env_response_times: list of environment response times
        :param action_pred_times: list of times it takes to predict actions
        :param grad_comp_times: list of times for computing gradients
        :param weight_update_times: list of times for updating the weights
        :param episode_caught: list of boolean indicators whether the attacker was caught
        :param episode_early_stopped: list of boolean indicators whether the defender stopped too early
        :param episode_successful_intrusion: list of boolean indicators whether the attacker made a successful intrusion
        :param eval_episode_caught: list of boolean indicators whether the attacker was caught in the eval environment
        :param eval_episode_early_stopped: list of boolean indicators whether the defender stopped too early
                                           in the eval environment
        :param eval_episode_successful_intrusion: list of boolean indicators whether the attacker made a successful
                                           intrusion in the eval environment
        :param eval_2_episode_caught: list of boolean indicators whether the attacker was caught
                                           in the eval2 environment
        :param eval_2_episode_early_stopped: list of boolean indicators whether the defender stopped too early
                                           in the eval2 environment
        :param eval_2_episode_successful_intrusion: list of boolean indicators whether the attacker made a successful
                                           intrusion in the eval2 environment
        :param episode_snort_severe_baseline_rewards: list of rewards of the snort_severe_baseline
        :param episode_snort_warning_baseline_rewards: list of rewards of the snort_warning_baseline
        :param eval_episode_snort_severe_baseline_rewards: list of eval rewards of the snort_severe_baseline
        :param eval_episode_snort_warning_baseline_rewards: list of eval rewards of the snort_warning_baseline
        :param eval_2_episode_snort_severe_baseline_rewards: list of eval2 rewards of the snort_severe_baseline
        :param eval_2_episode_snort_warning_baseline_rewards: list of eval2 rewards of the snort_severe_baseline
        :param episode_snort_critical_baseline_rewards: list of rewards of the snort_critical_baseline
        :param episode_var_log_baseline_rewards: list of rewards of the var_log_baseline
        :param eval_episode_snort_critical_baseline_rewards: list of eval rewards of the snort_critical_baseline
        :param eval_episode_var_log_baseline_rewards: list of eval rewards of the var_log_baseline
        :param eval_2_episode_snort_critical_baseline_rewards: list of eval2 rewards of the snort_critical_baseline
        :param eval_2_episode_var_log_baseline_rewards: list of eval2 rewards of the var_log_baseline
        :param episode_snort_severe_baseline_steps: list of steps of the snort_severe_baseline
        :param episode_snort_warning_baseline_steps: list of steps of the snort_warning_baseline
        :param eval_episode_snort_severe_baseline_steps: list of eval steps of the snort_severe_baseline
        :param eval_episode_snort_warning_baseline_steps: list of eval steps of the snort_warning_baseline
        :param eval_2_episode_snort_severe_baseline_steps: list of eval2 steps of the snort_severe_baseline
        :param eval_2_episode_snort_warning_baseline_steps: list of eval2 steps of the snort_warning_baseline
        :param episode_snort_critical_baseline_steps: list of eval2 steps of the snort_critical_baseline
        :param episode_var_log_baseline_steps: list of steps of the var_log_baseline
        :param eval_episode_snort_critical_baseline_steps: list of eval steps of the snort_critical_baseline
        :param eval_episode_var_log_baseline_steps: list of eval steps of the var_log_baseline
        :param eval_2_episode_snort_critical_baseline_steps: list of eval2 steps of the snort_critical_baseline
        :param eval_2_episode_var_log_baseline_steps: list of eval2 steps of the var_log_baseline
        :param episode_step_baseline_rewards: list of rewards of the step_baseline
        :param episode_step_baseline_steps: list of steps of the step_baseline
        :param eval_episode_step_baseline_rewards: list of eval rewards of the step_baseline
        :param eval_episode_step_baseline_steps: list of eval steps of the step_baseline
        :param eval_2_episode_step_baseline_rewards: list of eval2 rewards of the step_baseline
        :param eval_2_episode_step_baseline_steps: list of eval2 steps of the step_baseline
        :param attacker_action_costs: list of costs of the attacker
        :param attacker_action_costs_norm: list of normalized costs of the attacker
        :param attacker_action_alerts: list of alerts of the attacker
        :param attacker_action_alerts_norm: list of normalized alerts of the attacker
        :param eval_attacker_action_costs: list of eval costs of the attacker
        :param eval_attacker_action_costs_norm: list of eval normalized costs of the attacker
        :param eval_attacker_action_alerts: list of eval alerts of the attacker
        :param eval_attacker_action_alerts_norm: list of normalized eval alerts of the attacker
        :param eval_2_attacker_action_costs: list of eval2 costs of the attacker
        :param eval_2_attacker_action_costs_norm: list of normalized eval2 costs of the attacker
        :param eval_2_attacker_action_alerts: list of eval2 alerts of the attacker
        :param eval_2_attacker_action_alerts_norm: list of noramlized eval2 costs of the attacker
        :param start_time: the start time of the training step
        :param episode_intrusion_steps: list of intrusion steps
        :param eval_episode_intrusion_steps: list of eval intrusion steps
        :param eval_2_episode_intrusion_steps: list of eval2 intrusion stepsb
        :param episode_snort_severe_baseline_caught_attacker: list of boolean flags indicating that
                                                              the attacker was caught by the snort_severe_baseline
        :param episode_snort_warning_baseline_caught_attacker: list of boolean flags indicating that
                                                              the attacker was caught by the snort_warning_baseline
        :param eval_episode_snort_severe_baseline_caught_attacker: list of eval boolean flags indicating that
                                                              the attacker was caught by the snort_severe_baseline
        :param eval_episode_snort_warning_baseline_caught_attacker: list of eval boolean flags indicating that
                                                              the attacker was caught by the snort_warning_baseline
        :param eval_2_episode_snort_severe_baseline_caught_attacker: list of eval2 boolean flags indicating that
                                                              the attacker was caught by the snort_severe_baselinea
        :param eval_2_episode_snort_warning_baseline_caught_attacker: list of eval2 boolean flags indicating that
                                                              the attacker was caught by the snort_warning_baseline
        :param episode_snort_critical_baseline_caught_attacker: list of boolean flags indicating that
                                                              the attacker was caught by the snort_critical baseline
        :param episode_var_log_baseline_caught_attacker: list of boolean flags indicating that
                                                              the attacker was caught by the var_log_baseline
        :param eval_episode_snort_critical_baseline_caught_attacker: list of eval boolean flags indicating that
                                                              the attacker was caught by the snort_critical_baseline
        :param eval_episode_var_log_baseline_caught_attacker: list of eval boolean flags indicating that
                                                              the attacker was caught by the var_log_baseline
        :param eval_2_episode_snort_critical_baseline_caught_attacker: list of eval2 boolean flags indicating that
                                                              the attacker was caught by the snort_critical_baseline
        :param eval_2_episode_var_log_baseline_caught_attacker: list of eval2 boolean flags indicating that
                                                              the attacker was caught by the var_log_baseline
        :param episode_step_baseline_caught_attacker: list of boolean flags indicating that
                                                              the attacker was caught by the step_baseline
        :param eval_episode_step_baseline_caught_attacker: list of eval boolean flags indicating that
                                                              the attacker was caught by the step_baseline
        :param eval_2_episode_step_baseline_caught_attacker: list of eval2 boolean flags indicating that
                                                              the attacker was caught by the step_baseline
        :param episode_snort_severe_baseline_early_stopping: list of boolean flags indicating that
                                                              the snort_severe_baseline defender stopped too early
        :param episode_snort_warning_baseline_early_stopping: list of boolean flags indicating that
                                                              the snort_warning_baseline defender stopped too early
        :param eval_episode_snort_severe_baseline_early_stopping: list of eval boolean flags indicating that
                                                              the snort_severe_baseline defender stopped too early
        :param eval_episode_snort_warning_baseline_early_stopping: list eval of boolean flags indicating that
                                                              the snort_warning_baseline defender stopped too early
        :param eval_2_episode_snort_severe_baseline_early_stopping: list of eval2 boolean flags indicating that
                                                              the snort_severe_baseline defender stopped too early
        :param eval_2_episode_snort_warning_baseline_early_stopping: list of eval2 boolean flags indicating that
                                                              the snort_warning_baseline defender stopped too early
        :param episode_snort_critical_baseline_early_stopping: list of boolean flags indicating that
                                                              the snort_critical_baseline defender stopped too early
        :param episode_var_log_baseline_early_stopping: list of boolean flags indicating that
                                                              the var_log_baseline defender stopped too early
        :param eval_episode_snort_critical_baseline_early_stopping: list of eval boolean flags indicating that
                                                              the snort_critical_baseline defender stopped too early
        :param eval_episode_var_log_baseline_early_stopping: list of eval boolean flags indicating that
                                                              the var_log_baseline defender stopped too early
        :param eval_2_episode_snort_critical_baseline_early_stopping: list of eval2 boolean flags indicating that
                                                              the snort_critical_baseline defender stopped too early
        :param eval_2_episode_var_log_baseline_early_stopping: list of eval2 boolean flags indicating that
                                                              the var_log_baseline defender stopped too early
        :param episode_step_baseline_early_stopping: list of boolean flags indicating that
                                                              the step_baseline defender stopped too early
        :param eval_episode_step_baseline_early_stopping: list of eval boolean flags indicating that
                                                              the step_baseline defender stopped too early
        :param eval_2_episode_step_baseline_early_stopping: list of eval2 boolean flags indicating that
                                                              the step_baseline defender stopped too early
        :param episode_snort_severe_baseline_uncaught_intrusion_steps: list of uncaught intrusion steps of
                                                                       the snort_severe_baseline
        :param episode_snort_warning_baseline_uncaught_intrusion_steps: list of uncaught intrusion steps of
                                                                       the snort_warning_baseline
        :param eval_episode_snort_severe_baseline_uncaught_intrusion_steps: list of eval uncaught intrusion steps of
                                                                       the snort_severe_baseline
        :param eval_episode_snort_warning_baseline_uncaught_intrusion_steps: list of eval uncaught intrusion steps of
                                                                       the snort_warning_baseline
        :param eval_2_episode_snort_severe_baseline_uncaught_intrusion_steps: list of eval2 uncaught intrusion steps of
                                                                       the snort_severe_baseline
        :param eval_2_episode_snort_warning_baseline_uncaught_intrusion_steps: list of eval2 uncaught intrusion steps of
                                                                       the snort_warning_baseline
        :param episode_snort_critical_baseline_uncaught_intrusion_steps: list of uncaught intrusion steps of
                                                                       the snort_critical_baseline
        :param episode_var_log_baseline_uncaught_intrusion_steps: list of uncaught intrusion steps of
                                                                       the var_log_baseline
        :param eval_episode_snort_critical_baseline_uncaught_intrusion_steps: list of eval uncaught intrusion steps of
                                                                       the snort_critical_baseline
        :param eval_episode_var_log_baseline_uncaught_intrusion_steps: list of eval uncaught intrusion steps of
                                                                       the var_log_baseline
        :param eval_2_episode_snort_critical_baseline_uncaught_intrusion_steps: list of eval2 uncaught intrusion steps of
                                                                       the snort_critical_baseline
        :param eval_2_episode_var_log_baseline_uncaught_intrusion_steps: list of eval2 uncaught intrusion steps of
                                                                       the var_log_baseline
        :param episode_step_baseline_uncaught_intrusion_steps: list of uncaught intrusion steps of
                                                                       the step baseline
        :param eval_episode_step_baseline_uncaught_intrusion_steps: list of eval uncaught intrusion steps of
                                                                       the step baseline
        :param eval_2_episode_step_baseline_uncaught_intrusion_steps: list of eval2 uncaught intrusion steps of
                                                                       the step baseline
        :param uncaught_intrusion_steps: list of uncaught intrusion steps
        :param eval_uncaught_intrusion_steps: list of eval uncaught intrusion steps
        :param eval_2_uncaught_intrusion_steps: list of eval2 uncaught intrusion steps
        :param optimal_defender_reward: list of optimal defender rewardsb
        :param eval_optimal_defender_reward: list of eval optimal defender rewardsb
        :param eval_2_optimal_defender_reward: list of eval2 optimal defender rewardsb
        :param defender_stops_remaining: list of optimal defender stops remaining
        :param eval_defender_stops_remaining: list of eval optimal defender stops remaining
        :param eval_2_defender_stops_remaining: list of eval2 optimal defender stops remaining
        :param defender_first_stop_step: list of optimal defender first stop step
        :param eval_defender_first_stop_step: list of eval optimal defender first stop step
        :param eval_2_defender_first_stop_step: list of eval2 optimal defender first stop step
        :param defender_second_stop_step: list of optimal defender second stop step
        :param eval_defender_second_stop_step: list of eval optimal defender second stop step
        :param eval_2_defender_second_stop_step: list of eval2 optimal defender second stop step
        :param defender_third_stop_step: list of optimal defender third stop step
        :param eval_defender_third_stop_step: list of eval optimal defender third stop step
        :param eval_2_defender_third_stop_step: list of eval2 optimal defender third stop step
        :param defender_fourth_stop_step: list of optimal defender fourth stop step
        :param eval_defender_fourth_stop_step: list of eval optimal defender fourth stop step
        :param eval_2_defender_fourth_stop_step: list of eval2 optimal defender fourth stop step
        :param episode_snort_severe_baseline_first_stop_step: list of snort_severe_baseline first stop step
        :param episode_snort_warning_baseline_first_stop_step: list of snort_warning_baseline first stop step
        :param episode_snort_critical_baseline_first_stop_step: list of snort_critical_baseline first stop step
        :param episode_var_log_baseline_first_stop_step: list of var_log_baseline first stop step
        :param episode_step_baseline_first_stop_step: list of step_baseline first stop step
        :param episode_snort_severe_baseline_second_stop_step: list of snort_severe_baseline second stop step
        :param episode_snort_warning_baseline_second_stop_step: list of snort_warning_baseline second stop step
        :param episode_snort_critical_baseline_second_stop_step: list of snort_critical_baseline second stop step
        :param episode_var_log_baseline_second_stop_step: list of var_log_baseline second stop step
        :param episode_step_baseline_second_stop_step: list of step_baseline second stop step
        :param episode_snort_severe_baseline_third_stop_step: list of snort_severe_baseline third stop step
        :param episode_snort_warning_baseline_third_stop_step: list of snort_warning_baseline third stop step
        :param episode_snort_critical_baseline_third_stop_step: list of snort_critical_baseline third stop step
        :param episode_var_log_baseline_third_stop_step: list of var_log_baseline third stop step
        :param episode_step_baseline_third_stop_step: list of step_baseline third stop step
        :param episode_snort_severe_baseline_fourth_stop_step: list of snort_severe_baseline fourth stop step
        :param episode_snort_warning_baseline_fourth_stop_step: list of snort_warning_baseline fourth stop step
        :param episode_snort_critical_baseline_fourth_stop_step: list of snort_critical_baseline fourth stop step
        :param episode_var_log_baseline_fourth_stop_step: list of var_log_baseline fourth stop step
        :param episode_step_baseline_fourth_stop_step: list of step_baseline fourth stop step
        :param episode_snort_severe_baseline_stops_remaining: list of snort_severe_baseline stops remaining
        :param episode_snort_warning_baseline_stops_remaining: list of snort_warning_baseline stops remaining
        :param episode_snort_critical_baseline_stops_remaining: list of snort_critical_baseline stops remaining
        :param episode_var_log_baseline_stops_remaining: list of var_log_baseline stops remaining
        :param episode_step_baseline_stops_remaining: list of step_baseline stops remaining
        :param eval_episode_snort_severe_baseline_first_stop_step: eval list of snort_severe_baseline first stop step
        :param eval_episode_snort_warning_baseline_first_stop_step: eval list of snort_warning_baseline first stop step
        :param eval_episode_snort_critical_baseline_first_stop_step: eval list of snort_critical_baseline first stop step
        :param eval_episode_var_log_baseline_first_stop_step: eval list of var_log_baseline first stop step
        :param eval_episode_step_baseline_first_stop_step: eval list of step_baseline first stop step
        :param eval_episode_snort_severe_baseline_second_stop_step: eval list of snort_severe_baseline second stop step
        :param eval_episode_snort_warning_baseline_second_stop_step: eval list of snort_warning_baseline second stop step
        :param eval_episode_snort_critical_baseline_second_stop_step: eval list of snort_critical_baseline second stop step
        :param eval_episode_var_log_baseline_second_stop_step: eval list of var_log_baseline second stop step
        :param eval_episode_step_baseline_second_stop_step: eval list of step_baseline second stop step
        :param eval_episode_snort_severe_baseline_third_stop_step: eval list of snort_severe_baseline third stop step
        :param eval_episode_snort_warning_baseline_third_stop_step: eval list of snort_warning_baseline third stop step
        :param eval_episode_snort_critical_baseline_third_stop_step: eval list of snort_critical_baseline third stop step
        :param eval_episode_var_log_baseline_third_stop_step: eval list of var_log_baseline third stop step
        :param eval_episode_step_baseline_third_stop_step: eval list of step_baseline third stop step
        :param eval_episode_snort_severe_baseline_fourth_stop_step: eval list of snort_severe_baseline fourth stop step
        :param eval_episode_snort_warning_baseline_fourth_stop_step: eval list of snort_warning_baseline fourth stop step
        :param eval_episode_snort_critical_baseline_fourth_stop_step: eval list of snort_critical_baseline fourth stop step
        :param eval_episode_var_log_baseline_fourth_stop_step: eval list of var_log_baseline fourth stop step
        :param eval_episode_step_baseline_fourth_stop_step: eval list of step_baseline fourth stop step
        :param eval_episode_snort_severe_baseline_stops_remaining: eval list of snort_severe_baseline stops remaining
        :param eval_episode_snort_warning_baseline_stops_remaining: eval list of snort_warning_baseline stops remaining
        :param eval_episode_snort_critical_baseline_stops_remaining: eval list of snort_critical_baseline stops remaining
        :param eval_episode_var_log_baseline_stops_remaining: eval list of var_log_baseline stops remaining
        :param eval_episode_step_baseline_stops_remaining: eval list of step_baseline stops remaining
        :param eval_2_episode_snort_severe_baseline_first_stop_step: eval2 list of snort_severe_baseline first stop step
        :param eval_2_episode_snort_warning_baseline_first_stop_step: eval2 list of snort_warning_baseline first stop step
        :param eval_2_episode_snort_critical_baseline_first_stop_step: eval2 list of snort_critical_baseline first stop step
        :param eval_2_episode_var_log_baseline_first_stop_step: eval2 list of var_log_baseline first stop step
        :param eval_2_episode_step_baseline_first_stop_step: eval2 list of step_baseline first stop step
        :param eval_2_episode_snort_severe_baseline_second_stop_step: eval2 list of snort_severe_baseline second stop step
        :param eval_2_episode_snort_warning_baseline_second_stop_step: eval2 list of snort_warning_baseline second stop step
        :param eval_2_episode_snort_critical_baseline_second_stop_step: eval2 list of snort_critical_baseline second stop step
        :param eval_2_episode_var_log_baseline_second_stop_step: eval2 list of var_log_baseline second stop step
        :param eval_2_episode_step_baseline_second_stop_step: eval2 list of step_baseline second stop step
        :param eval_2_episode_snort_severe_baseline_third_stop_step: eval2 list of snort_severe_baseline third stop step
        :param eval_2_episode_snort_warning_baseline_third_stop_step: eval2 list of snort_warning_baseline third stop step
        :param eval_2_episode_snort_critical_baseline_third_stop_step: eval2 list of snort_critical_baseline third stop step
        :param eval_2_episode_var_log_baseline_third_stop_step: eval2 list of var_log_baseline third stop step
        :param eval_2_episode_step_baseline_third_stop_step: eval2 list of step_baseline third stop step
        :param eval_2_episode_snort_severe_baseline_fourth_stop_step: eval2 list of snort_severe_baseline fourth stop step
        :param eval_2_episode_snort_warning_baseline_fourth_stop_step: eval2 list of snort_warning_baseline fourth stop step
        :param eval_2_episode_snort_critical_baseline_fourth_stop_step: eval2 list of snort_critical_baseline fourth stop step
        :param eval_2_episode_var_log_baseline_fourth_stop_step: eval2 list of var_log_baseline fourth stop step
        :param eval_2_episode_step_baseline_fourth_stop_step: eval2 list of step_baseline fourth stop step
        :param eval_2_episode_snort_severe_baseline_stops_remaining: eval2 list of snort_severe_baseline stops remaining
        :param eval_2_episode_snort_warning_baseline_stops_remaining: eval2 list of snort_warning_baseline stops remaining
        :param eval_2_episode_snort_critical_baseline_stops_remaining: eval2 list of snort_critical_baseline stops remaining
        :param eval_2_episode_var_log_baseline_stops_remaining: eval2 list of var_log_baseline stops remaining
        :param eval_2_episode_step_baseline_stops_remaining: eval2 list of step_baseline stops remaining
        :param optimal_stops_remaining: optimal number of stops remaining
        :param eval_optimal_stops_remaining: eval optimal number of stops remaining
        :param eval_2_optimal_stops_remaining: eval2 optimal number of stops remaining
        :param optimal_first_stop_step: optimal time of first stop
        :param eval_optimal_first_stop_step: eval optimal time of first stop
        :param eval_2_optimal_first_stop_step: eval2 optimal time of first stop
        :param optimal_second_stop_step: optimal time of second stop
        :param eval_optimal_second_stop_step: eval optimal time of second stop
        :param eval_2_optimal_second_stop_step: eval2 optimal time of second stop
        :param optimal_third_stop_step: optimal time of third stop
        :param eval_optimal_third_stop_step: eval optimal time of third stop
        :param eval_2_optimal_third_stop_step: eval2 optimal time of third stop
        :param optimal_fourth_stop_step: eval optimal time of fourth stop
        :param eval_optimal_fourth_stop_step: eval optimal time of fourth stop
        :param eval_2_optimal_fourth_stop_step: eval2 optimal time of fourth stop
        :param optimal_defender_episode_steps: optimal episode length
        :param eval_optimal_defender_episode_steps: eval optimal episode length
        :param eval_2_optimal_defender_episode_steps: eval2 optimal episode length
        """
        super(TrainAgentLogDTO, self).__init__(iteration = iteration)
        self.train_result = train_result
        self.eval_result = eval_result
        self.attacker_episode_rewards = attacker_episode_rewards
        self.attacker_episode_avg_loss = attacker_episode_avg_loss
        self.attacker_lr = attacker_lr
        self.defender_episode_rewards = defender_episode_rewards
        self.defender_episode_avg_loss = defender_episode_avg_loss
        self.defender_lr = defender_lr
        self.total_num_episodes = total_num_episodes
        self.episode_steps = episode_steps
        self.episode_flags = episode_flags
        self.eval = eval
        self.episode_flags_percentage = episode_flags_percentage
        self.progress_left = progress_left
        self.n_af = n_af
        self.n_d = n_d
        self.attacker_eval_episode_rewards = attacker_eval_episode_rewards
        self.defender_eval_episode_rewards = defender_eval_episode_rewards
        self.eval_episode_steps = eval_episode_steps
        self.eval_episode_flags = eval_episode_flags
        self.eval_episode_flags_percentage = eval_episode_flags_percentage
        self.attacker_eval_2_episode_rewards = attacker_eval_2_episode_rewards
        self.defender_eval_2_episode_rewards = defender_eval_2_episode_rewards
        self.eval_2_episode_steps = eval_2_episode_steps
        self.eval_2_episode_flags = eval_2_episode_flags
        self.eval_2_episode_flags_percentage = eval_2_episode_flags_percentage
        self.attacker_train_episode_env_specific_rewards = attacker_train_episode_env_specific_rewards
        self.defender_train_episode_env_specific_rewards = defender_train_episode_env_specific_rewards
        self.train_env_specific_steps = train_env_specific_steps
        self.train_env_specific_flags = train_env_specific_flags
        self.train_env_specific_flags_percentage = train_env_specific_flags_percentage
        self.attacker_eval_env_specific_rewards = attacker_eval_env_specific_rewards
        self.defender_eval_env_specific_rewards = defender_eval_env_specific_rewards
        self.eval_env_specific_steps = eval_env_specific_steps
        self.eval_env_specific_flags = eval_env_specific_flags
        self.eval_env_specific_flags_percentage = eval_env_specific_flags_percentage
        self.attacker_eval_2_env_specific_rewards = attacker_eval_2_env_specific_rewards
        self.defender_eval_2_env_specific_rewards = defender_eval_2_env_specific_rewards
        self.eval_2_env_specific_steps = eval_2_env_specific_steps
        self.eval_2_env_specific_flags = eval_2_env_specific_flags
        self.eval_2_env_specific_flags_percentage = eval_2_env_specific_flags_percentage
        self.rollout_times = rollout_times
        self.env_response_times = env_response_times
        self.action_pred_times = action_pred_times
        self.grad_comp_times = grad_comp_times
        self.weight_update_times = weight_update_times
        self.episode_caught = episode_caught
        self.episode_early_stopped = episode_early_stopped
        self.episode_successful_intrusion = episode_successful_intrusion
        self.eval_episode_caught = eval_episode_caught
        self.eval_episode_early_stopped = eval_episode_early_stopped
        self.eval_episode_successful_intrusion = eval_episode_successful_intrusion
        self.eval_2_episode_caught = eval_2_episode_caught
        self.eval_2_episode_early_stopped = eval_2_episode_early_stopped
        self.eval_2_episode_successful_intrusion = eval_2_episode_successful_intrusion
        self.episode_snort_severe_baseline_rewards = episode_snort_severe_baseline_rewards
        self.episode_snort_warning_baseline_rewards = episode_snort_warning_baseline_rewards
        self.eval_episode_snort_severe_baseline_rewards = eval_episode_snort_severe_baseline_rewards
        self.eval_episode_snort_warning_baseline_rewards = eval_episode_snort_warning_baseline_rewards
        self.eval_2_episode_snort_severe_baseline_rewards = eval_2_episode_snort_severe_baseline_rewards
        self.eval_2_episode_snort_warning_baseline_rewards = eval_2_episode_snort_warning_baseline_rewards
        self.episode_snort_critical_baseline_rewards = episode_snort_critical_baseline_rewards
        self.episode_var_log_baseline_rewards = episode_var_log_baseline_rewards
        self.eval_episode_snort_critical_baseline_rewards = eval_episode_snort_critical_baseline_rewards
        self.eval_episode_var_log_baseline_rewards = eval_episode_var_log_baseline_rewards
        self.eval_2_episode_var_log_baseline_rewards = eval_2_episode_var_log_baseline_rewards
        self.eval_2_episode_snort_critical_baseline_rewards = eval_2_episode_snort_critical_baseline_rewards
        self.episode_snort_severe_baseline_steps = episode_snort_severe_baseline_steps
        self.episode_snort_warning_baseline_steps = episode_snort_warning_baseline_steps
        self.eval_episode_snort_severe_baseline_steps = eval_episode_snort_severe_baseline_steps
        self.eval_episode_snort_warning_baseline_steps = eval_episode_snort_warning_baseline_steps
        self.eval_2_episode_snort_severe_baseline_steps = eval_2_episode_snort_severe_baseline_steps
        self.eval_2_episode_snort_warning_baseline_steps = eval_2_episode_snort_warning_baseline_steps
        self.episode_snort_critical_baseline_steps = episode_snort_critical_baseline_steps
        self.episode_var_log_baseline_steps = episode_var_log_baseline_steps
        self.eval_episode_snort_critical_baseline_steps = eval_episode_snort_critical_baseline_steps
        self.eval_episode_var_log_baseline_steps = eval_episode_var_log_baseline_steps
        self.eval_2_episode_var_log_baseline_steps = eval_2_episode_var_log_baseline_steps
        self.eval_2_episode_snort_critical_baseline_steps = eval_2_episode_snort_critical_baseline_steps
        self.attacker_action_costs = attacker_action_costs
        self.attacker_action_costs_norm = attacker_action_costs_norm
        self.attacker_action_alerts = attacker_action_alerts
        self.attacker_action_alerts_norm = attacker_action_alerts_norm
        self.eval_attacker_action_costs = eval_attacker_action_costs
        self.eval_attacker_action_costs_norm = eval_attacker_action_costs_norm
        self.eval_attacker_action_alerts = eval_attacker_action_alerts
        self.eval_attacker_action_alerts_norm = eval_attacker_action_alerts_norm
        self.eval_2_attacker_action_costs = eval_2_attacker_action_costs
        self.eval_2_attacker_action_costs_norm = eval_2_attacker_action_costs_norm
        self.eval_2_attacker_action_alerts = eval_2_attacker_action_alerts
        self.eval_2_attacker_action_alerts_norm = eval_2_attacker_action_alerts_norm
        self.start_time = start_time
        self.episode_step_baseline_rewards = episode_step_baseline_rewards
        self.episode_step_baseline_steps = episode_step_baseline_steps
        self.eval_episode_step_baseline_rewards = eval_episode_step_baseline_rewards
        self.eval_episode_step_baseline_steps = eval_episode_step_baseline_steps
        self.eval_2_episode_step_baseline_rewards = eval_2_episode_step_baseline_rewards
        self.eval_2_episode_step_baseline_steps = eval_2_episode_step_baseline_steps
        self.episode_intrusion_steps = episode_intrusion_steps
        self.eval_episode_intrusion_steps = eval_episode_intrusion_steps
        self.eval_2_episode_intrusion_steps = eval_2_episode_intrusion_steps
        self.episode_snort_severe_baseline_caught_attacker = episode_snort_severe_baseline_caught_attacker
        self.episode_snort_warning_baseline_caught_attacker = episode_snort_warning_baseline_caught_attacker
        self.eval_episode_snort_severe_baseline_caught_attacker = eval_episode_snort_severe_baseline_caught_attacker
        self.eval_episode_snort_warning_baseline_caught_attacker = eval_episode_snort_warning_baseline_caught_attacker
        self.eval_2_episode_snort_severe_baseline_caught_attacker = eval_2_episode_snort_severe_baseline_caught_attacker
        self.eval_2_episode_snort_warning_baseline_caught_attacker = eval_2_episode_snort_warning_baseline_caught_attacker
        self.episode_snort_critical_baseline_caught_attacker = episode_snort_critical_baseline_caught_attacker
        self.episode_var_log_baseline_caught_attacker = episode_var_log_baseline_caught_attacker
        self.eval_episode_snort_critical_baseline_caught_attacker = eval_episode_snort_critical_baseline_caught_attacker
        self.eval_episode_var_log_baseline_caught_attacker = eval_episode_var_log_baseline_caught_attacker
        self.eval_2_episode_var_log_baseline_caught_attacker = eval_2_episode_var_log_baseline_caught_attacker
        self.eval_2_episode_snort_critical_baseline_caught_attacker = eval_2_episode_snort_critical_baseline_caught_attacker
        self.episode_step_baseline_caught_attacker = episode_step_baseline_caught_attacker
        self.eval_episode_step_baseline_caught_attacker = eval_episode_step_baseline_caught_attacker
        self.eval_2_episode_step_baseline_caught_attacker = eval_2_episode_step_baseline_caught_attacker
        self.episode_snort_severe_baseline_early_stopping = episode_snort_severe_baseline_early_stopping
        self.episode_snort_warning_baseline_early_stopping = episode_snort_warning_baseline_early_stopping
        self.eval_episode_snort_severe_baseline_early_stopping = eval_episode_snort_severe_baseline_early_stopping
        self.eval_episode_snort_warning_baseline_early_stopping = eval_episode_snort_warning_baseline_early_stopping
        self.eval_2_episode_snort_severe_baseline_early_stopping = eval_2_episode_snort_severe_baseline_early_stopping
        self.eval_2_episode_snort_warning_baseline_early_stopping = eval_2_episode_snort_warning_baseline_early_stopping
        self.episode_snort_critical_baseline_early_stopping = episode_snort_critical_baseline_early_stopping
        self.episode_var_log_baseline_early_stopping = episode_var_log_baseline_early_stopping
        self.eval_episode_snort_critical_baseline_early_stopping = eval_episode_snort_critical_baseline_early_stopping
        self.eval_episode_var_log_baseline_early_stopping = eval_episode_var_log_baseline_early_stopping
        self.eval_2_episode_var_log_baseline_early_stopping = eval_2_episode_var_log_baseline_early_stopping
        self.eval_2_episode_snort_critical_baseline_early_stopping = eval_2_episode_snort_critical_baseline_early_stopping
        self.episode_step_baseline_early_stopping = episode_step_baseline_early_stopping
        self.eval_episode_step_baseline_early_stopping = eval_episode_step_baseline_early_stopping
        self.eval_2_episode_step_baseline_early_stopping = eval_2_episode_step_baseline_early_stopping
        self.episode_snort_severe_baseline_uncaught_intrusion_steps = episode_snort_severe_baseline_uncaught_intrusion_steps
        self.episode_snort_warning_baseline_uncaught_intrusion_steps = episode_snort_warning_baseline_uncaught_intrusion_steps
        self.eval_episode_snort_severe_baseline_uncaught_intrusion_steps = eval_episode_snort_severe_baseline_uncaught_intrusion_steps
        self.eval_episode_snort_warning_baseline_uncaught_intrusion_steps = eval_episode_snort_warning_baseline_uncaught_intrusion_steps
        self.eval_2_episode_snort_severe_baseline_uncaught_intrusion_steps = eval_2_episode_snort_severe_baseline_uncaught_intrusion_steps
        self.eval_2_episode_snort_warning_baseline_uncaught_intrusion_steps = eval_2_episode_snort_warning_baseline_uncaught_intrusion_steps
        self.episode_snort_critical_baseline_uncaught_intrusion_steps = episode_snort_critical_baseline_uncaught_intrusion_steps
        self.episode_var_log_baseline_uncaught_intrusion_steps = episode_var_log_baseline_uncaught_intrusion_steps
        self.eval_episode_snort_critical_baseline_uncaught_intrusion_steps = eval_episode_snort_critical_baseline_uncaught_intrusion_steps
        self.eval_episode_var_log_baseline_uncaught_intrusion_steps = eval_episode_var_log_baseline_uncaught_intrusion_steps
        self.eval_2_episode_var_log_baseline_uncaught_intrusion_steps = eval_2_episode_var_log_baseline_uncaught_intrusion_steps
        self.eval_2_episode_snort_critical_baseline_uncaught_intrusion_steps = eval_2_episode_snort_critical_baseline_uncaught_intrusion_steps
        self.episode_step_baseline_uncaught_intrusion_steps = episode_step_baseline_uncaught_intrusion_steps
        self.eval_episode_step_baseline_uncaught_intrusion_steps = eval_episode_step_baseline_uncaught_intrusion_steps
        self.eval_2_episode_step_baseline_uncaught_intrusion_steps = eval_2_episode_step_baseline_uncaught_intrusion_steps
        self.uncaught_intrusion_steps = uncaught_intrusion_steps
        self.eval_uncaught_intrusion_steps = eval_uncaught_intrusion_steps
        self.eval_2_uncaught_intrusion_steps = eval_2_uncaught_intrusion_steps
        self.optimal_defender_reward = optimal_defender_reward
        self.eval_optimal_defender_reward = eval_optimal_defender_reward
        self.eval_2_optimal_defender_reward = eval_2_optimal_defender_reward
        self.defender_stops_remaining = defender_stops_remaining
        self.eval_defender_stops_remaining = eval_defender_stops_remaining
        self.eval_2_defender_stops_remaining = eval_2_defender_stops_remaining
        self.defender_first_stop_step = defender_first_stop_step
        self.eval_defender_first_stop_step = eval_defender_first_stop_step
        self.eval_2_defender_first_stop_step = eval_2_defender_first_stop_step
        self.defender_second_stop_step = defender_second_stop_step
        self.eval_defender_second_stop_step = eval_defender_second_stop_step
        self.eval_2_defender_second_stop_step = eval_2_defender_second_stop_step
        self.defender_third_stop_step = defender_third_stop_step
        self.eval_defender_third_stop_step = eval_defender_third_stop_step
        self.eval_2_defender_third_stop_step = eval_2_defender_third_stop_step
        self.defender_fourth_stop_step = defender_fourth_stop_step
        self.eval_defender_fourth_stop_step = eval_defender_fourth_stop_step
        self.eval_2_defender_fourth_stop_step = eval_2_defender_fourth_stop_step
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
        self.eval_episode_snort_severe_baseline_first_stop_step = eval_episode_snort_severe_baseline_first_stop_step
        self.eval_episode_snort_warning_baseline_first_stop_step = eval_episode_snort_warning_baseline_first_stop_step
        self.eval_episode_snort_critical_baseline_first_stop_step = eval_episode_snort_critical_baseline_first_stop_step
        self.eval_episode_var_log_baseline_first_stop_step = eval_episode_var_log_baseline_first_stop_step
        self.eval_episode_step_baseline_first_stop_step = eval_episode_step_baseline_first_stop_step
        self.eval_episode_snort_severe_baseline_second_stop_step = eval_episode_snort_severe_baseline_second_stop_step
        self.eval_episode_snort_warning_baseline_second_stop_step = eval_episode_snort_warning_baseline_second_stop_step
        self.eval_episode_snort_critical_baseline_second_stop_step = eval_episode_snort_critical_baseline_second_stop_step
        self.eval_episode_var_log_baseline_second_stop_step = eval_episode_var_log_baseline_second_stop_step
        self.eval_episode_step_baseline_second_stop_step = eval_episode_step_baseline_second_stop_step
        self.eval_episode_snort_severe_baseline_third_stop_step = eval_episode_snort_severe_baseline_third_stop_step
        self.eval_episode_snort_warning_baseline_third_stop_step = eval_episode_snort_warning_baseline_third_stop_step
        self.eval_episode_snort_critical_baseline_third_stop_step = eval_episode_snort_critical_baseline_third_stop_step
        self.eval_episode_var_log_baseline_third_stop_step = eval_episode_var_log_baseline_third_stop_step
        self.eval_episode_step_baseline_third_stop_step = eval_episode_step_baseline_third_stop_step
        self.eval_episode_snort_severe_baseline_fourth_stop_step = eval_episode_snort_severe_baseline_fourth_stop_step
        self.eval_episode_snort_warning_baseline_fourth_stop_step = eval_episode_snort_warning_baseline_fourth_stop_step
        self.eval_episode_snort_critical_baseline_fourth_stop_step = eval_episode_snort_critical_baseline_fourth_stop_step
        self.eval_episode_var_log_baseline_fourth_stop_step = eval_episode_var_log_baseline_fourth_stop_step
        self.eval_episode_step_baseline_fourth_stop_step = eval_episode_step_baseline_fourth_stop_step
        self.eval_episode_snort_severe_baseline_stops_remaining = eval_episode_snort_severe_baseline_stops_remaining
        self.eval_episode_snort_warning_baseline_stops_remaining = eval_episode_snort_warning_baseline_stops_remaining
        self.eval_episode_snort_critical_baseline_stops_remaining = eval_episode_snort_critical_baseline_stops_remaining
        self.eval_episode_var_log_baseline_stops_remaining = eval_episode_var_log_baseline_stops_remaining
        self.eval_episode_step_baseline_stops_remaining = eval_episode_step_baseline_stops_remaining
        self.eval_2_episode_snort_severe_baseline_first_stop_step = eval_2_episode_snort_severe_baseline_first_stop_step
        self.eval_2_episode_snort_warning_baseline_first_stop_step = eval_2_episode_snort_warning_baseline_first_stop_step
        self.eval_2_episode_snort_critical_baseline_first_stop_step = eval_2_episode_snort_critical_baseline_first_stop_step
        self.eval_2_episode_var_log_baseline_first_stop_step = eval_2_episode_var_log_baseline_first_stop_step
        self.eval_2_episode_step_baseline_first_stop_step = eval_2_episode_step_baseline_first_stop_step
        self.eval_2_episode_snort_severe_baseline_second_stop_step = eval_2_episode_snort_severe_baseline_second_stop_step
        self.eval_2_episode_snort_warning_baseline_second_stop_step = eval_2_episode_snort_warning_baseline_second_stop_step
        self.eval_2_episode_snort_critical_baseline_second_stop_step = eval_2_episode_snort_critical_baseline_second_stop_step
        self.eval_2_episode_var_log_baseline_second_stop_step = eval_2_episode_var_log_baseline_second_stop_step
        self.eval_2_episode_step_baseline_second_stop_step = eval_2_episode_step_baseline_second_stop_step
        self.eval_2_episode_snort_severe_baseline_third_stop_step = eval_2_episode_snort_severe_baseline_third_stop_step
        self.eval_2_episode_snort_warning_baseline_third_stop_step = eval_2_episode_snort_warning_baseline_third_stop_step
        self.eval_2_episode_snort_critical_baseline_third_stop_step = eval_2_episode_snort_critical_baseline_third_stop_step
        self.eval_2_episode_var_log_baseline_third_stop_step = eval_2_episode_var_log_baseline_third_stop_step
        self.eval_2_episode_step_baseline_third_stop_step = eval_2_episode_step_baseline_third_stop_step
        self.eval_2_episode_snort_severe_baseline_fourth_stop_step = eval_2_episode_snort_severe_baseline_fourth_stop_step
        self.eval_2_episode_snort_warning_baseline_fourth_stop_step = eval_2_episode_snort_warning_baseline_fourth_stop_step
        self.eval_2_episode_snort_critical_baseline_fourth_stop_step = eval_2_episode_snort_critical_baseline_fourth_stop_step
        self.eval_2_episode_var_log_baseline_fourth_stop_step = eval_2_episode_var_log_baseline_fourth_stop_step
        self.eval_2_episode_step_baseline_fourth_stop_step = eval_2_episode_step_baseline_fourth_stop_step
        self.eval_2_episode_snort_severe_baseline_stops_remaining = eval_2_episode_snort_severe_baseline_stops_remaining
        self.eval_2_episode_snort_warning_baseline_stops_remaining = eval_2_episode_snort_warning_baseline_stops_remaining
        self.eval_2_episode_snort_critical_baseline_stops_remaining = eval_2_episode_snort_critical_baseline_stops_remaining
        self.eval_2_episode_var_log_baseline_stops_remaining = eval_2_episode_var_log_baseline_stops_remaining
        self.eval_2_episode_step_baseline_stops_remaining = eval_2_episode_step_baseline_stops_remaining
        self.optimal_stops_remaining = optimal_stops_remaining
        self.eval_optimal_stops_remaining = eval_optimal_stops_remaining
        self.eval_2_optimal_stops_remaining = eval_2_optimal_stops_remaining
        self.optimal_first_stop_step = optimal_first_stop_step
        self.eval_optimal_first_stop_step = eval_optimal_first_stop_step
        self.eval_2_optimal_first_stop_step = eval_2_optimal_first_stop_step
        self.optimal_second_stop_step = optimal_second_stop_step
        self.eval_optimal_second_stop_step = eval_optimal_second_stop_step
        self.eval_2_optimal_second_stop_step = eval_2_optimal_second_stop_step
        self.optimal_third_stop_step = optimal_third_stop_step
        self.eval_optimal_third_stop_step = eval_optimal_third_stop_step
        self.eval_2_optimal_third_stop_step = eval_2_optimal_third_stop_step
        self.optimal_fourth_stop_step = optimal_fourth_stop_step
        self.eval_optimal_fourth_stop_step = eval_optimal_fourth_stop_step
        self.eval_2_optimal_fourth_stop_step = eval_2_optimal_fourth_stop_step
        self.optimal_defender_episode_steps = optimal_defender_episode_steps
        self.eval_optimal_defender_episode_steps = eval_optimal_defender_episode_steps
        self.eval_2_optimal_defender_episode_steps = eval_2_optimal_defender_episode_steps

    def initialize(self) -> None:
        """
        :return: Initialize log variables
        """
        self.start_time = 0.0
        self.iteration = 0
        self.train_result = ExperimentResult()
        self.eval_result = ExperimentResult()
        self.attacker_episode_rewards = []
        self.attacker_episode_avg_loss = []
        self.attacker_lr = 0.0
        self.defender_episode_rewards = []
        self.defender_episode_avg_loss = []
        self.defender_lr = 0.0
        self.total_num_episodes = 1
        self.episode_steps = []
        self.episode_flags = []
        self.eval = False
        self.episode_flags_percentage = []
        self.progress_left = 0.0
        self.n_af = 0
        self.n_d = 0
        self.attacker_eval_episode_rewards = []
        self.defender_eval_episode_rewards = []
        self.eval_episode_steps = []
        self.eval_episode_flags = []
        self.eval_episode_flags_percentage = []
        self.attacker_eval_2_episode_rewards = []
        self.defender_eval_2_episode_rewards = []
        self.eval_2_episode_steps = []
        self.eval_2_episode_flags = []
        self.eval_2_episode_flags_percentage = []
        self.attacker_train_episode_env_specific_rewards = {}
        self.defender_train_episode_env_specific_rewards = {}
        self.train_env_specific_steps = {}
        self.train_env_specific_flags = {}
        self.train_env_specific_flags_percentage = {}
        self.attacker_eval_env_specific_rewards = {}
        self.defender_eval_env_specific_rewards = {}
        self.eval_env_specific_steps = {}
        self.eval_env_specific_flags = {}
        self.eval_env_specific_flags_percentage = {}
        self.attacker_eval_2_env_specific_rewards = {}
        self.defender_eval_2_env_specific_rewards = {}
        self.eval_2_env_specific_steps = {}
        self.eval_2_env_specific_flags = {}
        self.eval_2_env_specific_flags_percentage = {}
        self.rollout_times = []
        self.env_response_times = []
        self.action_pred_times = []
        self.grad_comp_times = []
        self.weight_update_times = []
        self.episode_caught = []
        self.episode_early_stopped = []
        self.episode_successful_intrusion = []
        self.eval_episode_caught = []
        self.eval_episode_early_stopped = []
        self.eval_episode_successful_intrusion = []
        self.eval_2_episode_caught = []
        self.eval_2_episode_early_stopped = []
        self.eval_2_episode_successful_intrusion = []
        self.snort_severe_baseline_rewards = []
        self.snort_warning_baseline_rewards = []
        self.eval_snort_severe_baseline_rewards = []
        self.eval_snort_warning_baseline_rewards = []
        self.eval_2_episode_snort_severe_baseline_rewards = []
        self.eval_2_episode_snort_warning_baseline_rewards = []
        self.episode_snort_critical_baseline_rewards = []
        self.episode_var_log_baseline_rewards = []
        self.eval_episode_snort_critical_baseline_rewards = []
        self.eval_episode_var_log_baseline_rewards = []
        self.eval_2_episode_snort_critical_baseline_rewards = []
        self.eval_2_episode_var_log_baseline_rewards = []
        self.episode_snort_warning_baseline_rewards = []
        self.episode_snort_severe_baseline_rewards = []
        self.eval_episode_snort_severe_baseline_rewards = []
        self.eval_episode_snort_warning_baseline_rewards = []
        self.snort_severe_baseline_steps = []
        self.snort_warning_baseline_steps = []
        self.eval_snort_severe_baseline_steps = []
        self.eval_snort_warning_baseline_steps = []
        self.eval_2_episode_snort_severe_baseline_steps = []
        self.eval_2_episode_snort_warning_baseline_steps = []
        self.episode_snort_critical_baseline_steps = []
        self.episode_var_log_baseline_steps = []
        self.eval_episode_snort_critical_baseline_steps = []
        self.eval_episode_var_log_baseline_steps = []
        self.eval_2_episode_snort_critical_baseline_steps = []
        self.eval_2_episode_var_log_baseline_steps = []
        self.episode_snort_warning_baseline_steps = []
        self.episode_snort_severe_baseline_steps = []
        self.eval_episode_snort_severe_baseline_steps = []
        self.eval_episode_snort_warning_baseline_steps = []
        self.attacker_action_costs = []
        self.attacker_action_costs_norm = []
        self.attacker_action_alerts = []
        self.attacker_action_alerts_norm = []
        self.eval_attacker_action_costs = []
        self.eval_attacker_action_costs_norm = []
        self.eval_attacker_action_alerts = []
        self.eval_attacker_action_alerts_norm = []
        self.eval_2_attacker_action_costs = []
        self.eval_2_attacker_action_costs_norm = []
        self.eval_2_attacker_action_alerts = []
        self.eval_2_attacker_action_alerts_norm = []
        self.episode_step_baseline_rewards = []
        self.episode_step_baseline_steps = []
        self.eval_episode_step_baseline_rewards = []
        self.eval_episode_step_baseline_steps = []
        self.eval_2_episode_step_baseline_rewards = []
        self.eval_2_episode_step_baseline_steps = []
        self.episode_intrusion_steps = []
        self.eval_episode_intrusion_steps = []
        self.eval_2_episode_intrusion_steps = []
        self.snort_severe_baseline_caught_attacker = []
        self.snort_warning_baseline_caught_attacker = []
        self.eval_snort_severe_baseline_caught_attacker = []
        self.eval_snort_warning_baseline_caught_attacker = []
        self.eval_2_episode_snort_severe_baseline_caught_attacker = []
        self.eval_2_episode_snort_warning_baseline_caught_attacker = []
        self.episode_snort_critical_baseline_caught_attacker = []
        self.episode_var_log_baseline_caught_attacker = []
        self.eval_episode_snort_critical_baseline_caught_attacker = []
        self.eval_episode_var_log_baseline_caught_attacker = []
        self.eval_2_episode_snort_critical_baseline_caught_attacker = []
        self.eval_2_episode_var_log_baseline_caught_attacker = []
        self.episode_snort_warning_baseline_caught_attacker = []
        self.episode_snort_severe_baseline_caught_attacker = []
        self.eval_episode_snort_severe_baseline_caught_attacker = []
        self.eval_episode_snort_warning_baseline_caught_attacker = []
        self.episode_step_baseline_caught_attacker = []
        self.eval_episode_step_baseline_caught_attacker = []
        self.eval_2_episode_step_baseline_caught_attacker = []
        self.snort_severe_baseline_early_stopping = []
        self.snort_warning_baseline_early_stopping = []
        self.eval_snort_severe_baseline_early_stopping = []
        self.eval_snort_warning_baseline_early_stopping = []
        self.eval_2_episode_snort_severe_baseline_early_stopping = []
        self.eval_2_episode_snort_warning_baseline_early_stopping = []
        self.episode_snort_critical_baseline_early_stopping = []
        self.episode_var_log_baseline_early_stopping = []
        self.eval_episode_snort_critical_baseline_early_stopping = []
        self.eval_episode_var_log_baseline_early_stopping = []
        self.eval_2_episode_snort_critical_baseline_early_stopping = []
        self.eval_2_episode_var_log_baseline_early_stopping = []
        self.episode_snort_warning_baseline_early_stopping = []
        self.episode_snort_severe_baseline_early_stopping = []
        self.eval_episode_snort_severe_baseline_early_stopping = []
        self.eval_episode_snort_warning_baseline_early_stopping = []
        self.episode_step_baseline_early_stopping = []
        self.eval_episode_step_baseline_early_stopping = []
        self.eval_2_episode_step_baseline_early_stopping = []
        self.snort_severe_baseline_uncaught_intrusion_steps = []
        self.snort_warning_baseline_uncaught_intrusion_steps = []
        self.eval_snort_severe_baseline_uncaught_intrusion_steps = []
        self.eval_snort_warning_baseline_uncaught_intrusion_steps = []
        self.eval_2_episode_snort_severe_baseline_uncaught_intrusion_steps = []
        self.eval_2_episode_snort_warning_baseline_uncaught_intrusion_steps = []
        self.episode_snort_critical_baseline_uncaught_intrusion_steps = []
        self.episode_var_log_baseline_uncaught_intrusion_steps = []
        self.eval_episode_snort_critical_baseline_uncaught_intrusion_steps = []
        self.eval_episode_var_log_baseline_uncaught_intrusion_steps = []
        self.eval_2_episode_snort_critical_baseline_uncaught_intrusion_steps = []
        self.eval_2_episode_var_log_baseline_uncaught_intrusion_steps = []
        self.episode_snort_warning_baseline_uncaught_intrusion_steps = []
        self.episode_snort_severe_baseline_uncaught_intrusion_steps = []
        self.eval_episode_snort_severe_baseline_uncaught_intrusion_steps = []
        self.eval_episode_snort_warning_baseline_uncaught_intrusion_steps = []
        self.episode_step_baseline_uncaught_intrusion_steps = []
        self.eval_episode_step_baseline_uncaught_intrusion_steps = []
        self.eval_2_episode_step_baseline_uncaught_intrusion_steps = []
        self.uncaught_intrusion_steps = []
        self.eval_uncaught_intrusion_steps = []
        self.eval_2_uncaught_intrusion_steps = []
        self.optimal_defender_reward = []
        self.eval_optimal_defender_reward = []
        self.eval_2_optimal_defender_reward = []
        self.defender_stops_remaining = []
        self.eval_defender_stops_remaining = []
        self.eval_2_defender_stops_remaining = []
        self.defender_first_stop_step = []
        self.eval_defender_first_stop_step = []
        self.eval_2_defender_first_stop_step = []
        self.defender_second_stop_step = []
        self.eval_defender_second_stop_step = []
        self.eval_2_defender_second_stop_step = []
        self.defender_third_stop_step = []
        self.eval_defender_third_stop_step = []
        self.eval_2_defender_third_stop_step = []
        self.defender_fourth_stop_step = []
        self.eval_defender_fourth_stop_step = []
        self.eval_2_defender_fourth_stop_step = []
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
        self.eval_episode_snort_severe_baseline_first_stop_step = []
        self.eval_episode_snort_warning_baseline_first_stop_step = []
        self.eval_episode_snort_critical_baseline_first_stop_step = []
        self.eval_episode_var_log_baseline_first_stop_step = []
        self.eval_episode_step_baseline_first_stop_step = []
        self.eval_episode_snort_severe_baseline_second_stop_step = []
        self.eval_episode_snort_warning_baseline_second_stop_step = []
        self.eval_episode_snort_critical_baseline_second_stop_step = []
        self.eval_episode_var_log_baseline_second_stop_step = []
        self.eval_episode_step_baseline_second_stop_step = []
        self.eval_episode_snort_severe_baseline_third_stop_step = []
        self.eval_episode_snort_warning_baseline_third_stop_step = []
        self.eval_episode_snort_critical_baseline_third_stop_step = []
        self.eval_episode_var_log_baseline_third_stop_step = []
        self.eval_episode_step_baseline_third_stop_step = []
        self.eval_episode_snort_severe_baseline_fourth_stop_step = []
        self.eval_episode_snort_warning_baseline_fourth_stop_step = []
        self.eval_episode_snort_critical_baseline_fourth_stop_step = []
        self.eval_episode_var_log_baseline_fourth_stop_step = []
        self.eval_episode_step_baseline_fourth_stop_step = []
        self.eval_episode_snort_severe_baseline_stops_remaining = []
        self.eval_episode_snort_warning_baseline_stops_remaining = []
        self.eval_episode_snort_critical_baseline_stops_remaining = []
        self.eval_episode_var_log_baseline_stops_remaining = []
        self.eval_episode_step_baseline_stops_remaining = []
        self.eval_2_episode_snort_severe_baseline_first_stop_step = []
        self.eval_2_episode_snort_warning_baseline_first_stop_step = []
        self.eval_2_episode_snort_critical_baseline_first_stop_step = []
        self.eval_2_episode_var_log_baseline_first_stop_step = []
        self.eval_2_episode_step_baseline_first_stop_step = []
        self.eval_2_episode_snort_severe_baseline_second_stop_step = []
        self.eval_2_episode_snort_warning_baseline_second_stop_step = []
        self.eval_2_episode_snort_critical_baseline_second_stop_step = []
        self.eval_2_episode_var_log_baseline_second_stop_step = []
        self.eval_2_episode_step_baseline_second_stop_step = []
        self.eval_2_episode_snort_severe_baseline_third_stop_step = []
        self.eval_2_episode_snort_warning_baseline_third_stop_step = []
        self.eval_2_episode_snort_critical_baseline_third_stop_step = []
        self.eval_2_episode_var_log_baseline_third_stop_step = []
        self.eval_2_episode_step_baseline_third_stop_step = []
        self.eval_2_episode_snort_severe_baseline_fourth_stop_step = []
        self.eval_2_episode_snort_warning_baseline_fourth_stop_step = []
        self.eval_2_episode_snort_critical_baseline_fourth_stop_step = []
        self.eval_2_episode_var_log_baseline_fourth_stop_step = []
        self.eval_2_episode_step_baseline_fourth_stop_step = []
        self.eval_2_episode_snort_severe_baseline_stops_remaining = []
        self.eval_2_episode_snort_warning_baseline_stops_remaining = []
        self.eval_2_episode_snort_critical_baseline_stops_remaining = []
        self.eval_2_episode_var_log_baseline_stops_remaining = []
        self.eval_2_episode_step_baseline_stops_remaining = []
        self.optimal_stops_remaining = []
        self.eval_optimal_stops_remaining = []
        self.eval_2_optimal_stops_remaining = []
        self.optimal_first_stop_step = []
        self.eval_optimal_first_stop_step = []
        self.eval_2_optimal_first_stop_step = []
        self.optimal_second_stop_step = []
        self.eval_optimal_second_stop_step = []
        self.eval_2_optimal_second_stop_step = []
        self.optimal_third_stop_step = []
        self.eval_optimal_third_stop_step = []
        self.eval_2_optimal_third_stop_step = []
        self.optimal_fourth_stop_step = []
        self.eval_optimal_fourth_stop_step = []
        self.eval_2_optimal_fourth_stop_step = []
        self.optimal_defender_episode_steps = []
        self.eval_optimal_defender_episode_steps = []
        self.eval_2_optimal_defender_episode_steps = []

    def copy(self) -> "TrainAgentLogDTO":
        """        
        :return: a copy of the object  
        """
        c = TrainAgentLogDTO()
        c.iteration = self.iteration
        c.train_result = self.train_result
        c.eval_result = self.eval_result
        c.attacker_episode_rewards = self.attacker_episode_rewards
        c.attacker_episode_avg_loss = self.attacker_episode_avg_loss
        c.attacker_lr = self.attacker_lr
        c.defender_episode_rewards = self.defender_episode_rewards
        c.defender_episode_avg_loss = self.defender_episode_avg_loss
        c.defender_lr = self.defender_lr
        c.total_num_episodes = self.total_num_episodes
        c.episode_steps = self.episode_steps
        c.episode_flags = self.episode_flags
        c.eval = self.eval
        c.episode_flags_percentage = self.episode_flags_percentage
        c.progress_left = self.progress_left
        c.n_af = self.n_af
        c.n_d = self.n_d
        c.attacker_eval_episode_rewards = self.attacker_eval_episode_rewards
        c.defender_eval_episode_rewards = self.defender_eval_episode_rewards
        c.eval_episode_steps = self.eval_episode_steps
        c.eval_episode_flags = self.eval_episode_flags
        c.eval_episode_flags_percentage = self.eval_episode_flags_percentage
        c.attacker_eval_2_episode_rewards = self.attacker_eval_2_episode_rewards
        c.defender_eval_2_episode_rewards = self.defender_eval_2_episode_rewards
        c.eval_2_episode_steps = self.eval_2_episode_steps
        c.eval_2_episode_flags = self.eval_2_episode_flags
        c.eval_2_episode_flags_percentage = self.eval_2_episode_flags_percentage
        c.attacker_train_episode_env_specific_rewards = self.attacker_train_episode_env_specific_rewards
        c.defender_train_episode_env_specific_rewards = self.defender_train_episode_env_specific_rewards
        c.train_env_specific_steps = self.train_env_specific_steps
        c.train_env_specific_flags = self.train_env_specific_flags
        c.train_env_specific_flags_percentage = self.train_env_specific_flags_percentage
        c.attacker_eval_env_specific_rewards = self.attacker_eval_env_specific_rewards
        c.defender_eval_env_specific_rewards = self.defender_eval_env_specific_rewards
        c.eval_env_specific_steps = self.eval_env_specific_steps
        c.eval_env_specific_flags = self.eval_env_specific_flags
        c.eval_env_specific_flags_percentage = self.eval_env_specific_flags_percentage
        c.attacker_eval_2_env_specific_rewards = self.attacker_eval_2_env_specific_rewards
        c.defender_eval_2_env_specific_rewards = self.defender_eval_2_env_specific_rewards
        c.eval_2_env_specific_steps = self.eval_2_env_specific_steps
        c.eval_2_env_specific_flags = self.eval_2_env_specific_flags
        c.eval_2_env_specific_flags_percentage = self.eval_2_env_specific_flags_percentage
        c.rollout_times = self.rollout_times
        c.env_response_times = self.env_response_times
        c.action_pred_times = self.action_pred_times
        c.grad_comp_times = self.grad_comp_times
        c.weight_update_times = self.weight_update_times
        c.episode_caught = self.episode_caught
        c.episode_early_stopped = self.episode_early_stopped
        c.episode_successful_intrusion = self.episode_successful_intrusion
        c.eval_episode_caught = self.eval_episode_caught
        c.eval_episode_early_stopped = self.eval_episode_early_stopped
        c.eval_episode_successful_intrusion = self.eval_episode_successful_intrusion
        c.eval_2_episode_caught = self.eval_2_episode_caught
        c.eval_2_episode_early_stopped = self.eval_2_episode_early_stopped
        c.eval_2_episode_successful_intrusion = self.eval_2_episode_successful_intrusion
        c.episode_snort_severe_baseline_rewards = self.episode_snort_severe_baseline_rewards
        c.episode_snort_warning_baseline_rewards = self.episode_snort_warning_baseline_rewards
        c.eval_episode_snort_severe_baseline_rewards = self.eval_episode_snort_severe_baseline_rewards
        c.eval_episode_snort_warning_baseline_rewards = self.eval_episode_snort_warning_baseline_rewards
        c.eval_2_episode_snort_severe_baseline_rewards = self.eval_2_episode_snort_severe_baseline_rewards
        c.eval_2_episode_snort_warning_baseline_rewards = self.eval_2_episode_snort_warning_baseline_rewards
        c.episode_snort_critical_baseline_rewards = self.episode_snort_critical_baseline_rewards
        c.episode_var_log_baseline_rewards = self.episode_var_log_baseline_rewards
        c.eval_episode_snort_critical_baseline_rewards = self.eval_episode_snort_critical_baseline_rewards
        c.eval_episode_var_log_baseline_rewards = self.eval_episode_var_log_baseline_rewards
        c.eval_2_episode_var_log_baseline_rewards = self.eval_2_episode_var_log_baseline_rewards
        c.eval_2_episode_snort_critical_baseline_rewards = self.eval_2_episode_snort_critical_baseline_rewards
        c.episode_snort_severe_baseline_steps = self.episode_snort_severe_baseline_steps
        c.episode_snort_warning_baseline_steps = self.episode_snort_warning_baseline_steps
        c.eval_episode_snort_severe_baseline_steps = self.eval_episode_snort_severe_baseline_steps
        c.eval_episode_snort_warning_baseline_steps = self.eval_episode_snort_warning_baseline_steps
        c.eval_2_episode_snort_severe_baseline_steps = self.eval_2_episode_snort_severe_baseline_steps
        c.eval_2_episode_snort_warning_baseline_steps = self.eval_2_episode_snort_warning_baseline_steps
        c.episode_snort_critical_baseline_steps = self.episode_snort_critical_baseline_steps
        c.episode_var_log_baseline_steps = self.episode_var_log_baseline_steps
        c.eval_episode_snort_critical_baseline_steps = self.eval_episode_snort_critical_baseline_steps
        c.eval_episode_var_log_baseline_steps = self.eval_episode_var_log_baseline_steps
        c.eval_2_episode_var_log_baseline_steps = self.eval_2_episode_var_log_baseline_steps
        c.eval_2_episode_snort_critical_baseline_steps = self.eval_2_episode_snort_critical_baseline_steps
        c.attacker_action_costs = self.attacker_action_costs
        c.attacker_action_costs_norm = self.attacker_action_costs_norm
        c.attacker_action_alerts = self.attacker_action_alerts
        c.attacker_action_alerts_norm = self.attacker_action_alerts_norm
        c.eval_attacker_action_costs = self.eval_attacker_action_costs
        c.eval_attacker_action_costs_norm = self.eval_attacker_action_costs_norm
        c.eval_attacker_action_alerts = self.eval_attacker_action_alerts
        c.eval_attacker_action_alerts_norm = self.eval_attacker_action_alerts_norm
        c.eval_2_attacker_action_costs = self.eval_2_attacker_action_costs
        c.eval_2_attacker_action_costs_norm = self.eval_2_attacker_action_costs_norm
        c.eval_2_attacker_action_alerts = self.eval_2_attacker_action_alerts
        c.eval_2_attacker_action_alerts_norm = self.eval_2_attacker_action_alerts_norm
        c.start_time = self.start_time
        c.episode_step_baseline_rewards = self.episode_step_baseline_rewards
        c.episode_step_baseline_steps = self.episode_step_baseline_steps
        c.eval_episode_step_baseline_rewards = self.eval_episode_step_baseline_rewards
        c.eval_episode_step_baseline_steps = self.eval_episode_step_baseline_steps
        c.eval_2_episode_step_baseline_rewards = self.eval_2_episode_step_baseline_rewards
        c.eval_2_episode_step_baseline_steps = self.eval_2_episode_step_baseline_steps
        c.episode_intrusion_steps = self.episode_intrusion_steps
        c.eval_episode_intrusion_steps = self.eval_episode_intrusion_steps
        c.eval_2_episode_intrusion_steps = self.eval_2_episode_intrusion_steps
        c.episode_snort_severe_baseline_caught_attacker = self.episode_snort_severe_baseline_caught_attacker
        c.episode_snort_warning_baseline_caught_attacker = self.episode_snort_warning_baseline_caught_attacker
        c.eval_episode_snort_severe_baseline_caught_attacker = self.eval_episode_snort_severe_baseline_caught_attacker
        c.eval_episode_snort_warning_baseline_caught_attacker = self.eval_episode_snort_warning_baseline_caught_attacker
        c.eval_2_episode_snort_severe_baseline_caught_attacker = self.eval_2_episode_snort_severe_baseline_caught_attacker
        c.eval_2_episode_snort_warning_baseline_caught_attacker = self.eval_2_episode_snort_warning_baseline_caught_attacker
        c.episode_snort_critical_baseline_caught_attacker = self.episode_snort_critical_baseline_caught_attacker
        c.episode_var_log_baseline_caught_attacker = self.episode_var_log_baseline_caught_attacker
        c.eval_episode_snort_critical_baseline_caught_attacker = self.eval_episode_snort_critical_baseline_caught_attacker
        c.eval_episode_var_log_baseline_caught_attacker = self.eval_episode_var_log_baseline_caught_attacker
        c.eval_2_episode_var_log_baseline_caught_attacker = self.eval_2_episode_var_log_baseline_caught_attacker
        c.eval_2_episode_snort_critical_baseline_caught_attacker = self.eval_2_episode_snort_critical_baseline_caught_attacker
        c.episode_step_baseline_caught_attacker = self.episode_step_baseline_caught_attacker
        c.eval_episode_step_baseline_caught_attacker = self.eval_episode_step_baseline_caught_attacker
        c.eval_2_episode_step_baseline_caught_attacker = self.eval_2_episode_step_baseline_caught_attacker
        c.episode_snort_severe_baseline_early_stopping = self.episode_snort_severe_baseline_early_stopping
        c.episode_snort_warning_baseline_early_stopping = self.episode_snort_warning_baseline_early_stopping
        c.eval_episode_snort_severe_baseline_early_stopping = self.eval_episode_snort_severe_baseline_early_stopping
        c.eval_episode_snort_warning_baseline_early_stopping = self.eval_episode_snort_warning_baseline_early_stopping
        c.eval_2_episode_snort_severe_baseline_early_stopping = self.eval_2_episode_snort_severe_baseline_early_stopping
        c.eval_2_episode_snort_warning_baseline_early_stopping = self.eval_2_episode_snort_warning_baseline_early_stopping
        c.episode_snort_critical_baseline_early_stopping = self.episode_snort_critical_baseline_early_stopping
        c.episode_var_log_baseline_early_stopping = self.episode_var_log_baseline_early_stopping
        c.eval_episode_snort_critical_baseline_early_stopping = self.eval_episode_snort_critical_baseline_early_stopping
        c.eval_episode_var_log_baseline_early_stopping = self.eval_episode_var_log_baseline_early_stopping
        c.eval_2_episode_var_log_baseline_early_stopping = self.eval_2_episode_var_log_baseline_early_stopping
        c.eval_2_episode_snort_critical_baseline_early_stopping = self.eval_2_episode_snort_critical_baseline_early_stopping
        c.episode_step_baseline_early_stopping = self.episode_step_baseline_early_stopping
        c.eval_episode_step_baseline_early_stopping = self.eval_episode_step_baseline_early_stopping
        c.eval_2_episode_step_baseline_early_stopping = self.eval_2_episode_step_baseline_early_stopping
        c.episode_snort_severe_baseline_uncaught_intrusion_steps = self.episode_snort_severe_baseline_uncaught_intrusion_steps
        c.episode_snort_warning_baseline_uncaught_intrusion_steps = self.episode_snort_warning_baseline_uncaught_intrusion_steps
        c.eval_episode_snort_severe_baseline_uncaught_intrusion_steps = self.eval_episode_snort_severe_baseline_uncaught_intrusion_steps
        c.eval_episode_snort_warning_baseline_uncaught_intrusion_steps = self.eval_episode_snort_warning_baseline_uncaught_intrusion_steps
        c.eval_2_episode_snort_severe_baseline_uncaught_intrusion_steps = self.eval_2_episode_snort_severe_baseline_uncaught_intrusion_steps
        c.eval_2_episode_snort_warning_baseline_uncaught_intrusion_steps = self.eval_2_episode_snort_warning_baseline_uncaught_intrusion_steps
        c.episode_snort_critical_baseline_uncaught_intrusion_steps = self.episode_snort_critical_baseline_uncaught_intrusion_steps
        c.episode_var_log_baseline_uncaught_intrusion_steps = self.episode_var_log_baseline_uncaught_intrusion_steps
        c.eval_episode_snort_critical_baseline_uncaught_intrusion_steps = self.eval_episode_snort_critical_baseline_uncaught_intrusion_steps
        c.eval_episode_var_log_baseline_uncaught_intrusion_steps = self.eval_episode_var_log_baseline_uncaught_intrusion_steps
        c.eval_2_episode_var_log_baseline_uncaught_intrusion_steps = self.eval_2_episode_var_log_baseline_uncaught_intrusion_steps
        c.eval_2_episode_snort_critical_baseline_uncaught_intrusion_steps = self.eval_2_episode_snort_critical_baseline_uncaught_intrusion_steps
        c.episode_step_baseline_uncaught_intrusion_steps = self.episode_step_baseline_uncaught_intrusion_steps
        c.eval_episode_step_baseline_uncaught_intrusion_steps = self.eval_episode_step_baseline_uncaught_intrusion_steps
        c.eval_2_episode_step_baseline_uncaught_intrusion_steps = self.eval_2_episode_step_baseline_uncaught_intrusion_steps
        c.uncaught_intrusion_steps = self.uncaught_intrusion_steps
        c.eval_uncaught_intrusion_steps = self.eval_uncaught_intrusion_steps
        c.eval_2_uncaught_intrusion_steps = self.eval_2_uncaught_intrusion_steps
        c.optimal_defender_reward = self.optimal_defender_reward
        c.eval_optimal_defender_reward = self.eval_optimal_defender_reward
        c.eval_2_optimal_defender_reward = self.eval_2_optimal_defender_reward
        c.defender_stops_remaining = self.defender_stops_remaining
        c.eval_defender_stops_remaining = self.eval_defender_stops_remaining
        c.eval_2_defender_stops_remaining = self.eval_2_defender_stops_remaining
        c.defender_first_stop_step = self.defender_first_stop_step
        c.eval_defender_first_stop_step = self.eval_defender_first_stop_step
        c.eval_2_defender_first_stop_step = self.eval_2_defender_first_stop_step
        c.defender_second_stop_step = self.defender_second_stop_step
        c.eval_defender_second_stop_step = self.eval_defender_second_stop_step
        c.eval_2_defender_second_stop_step = self.eval_2_defender_second_stop_step
        c.defender_third_stop_step = self.defender_third_stop_step
        c.eval_defender_third_stop_step = self.eval_defender_third_stop_step
        c.eval_2_defender_third_stop_step = self.eval_2_defender_third_stop_step
        c.defender_fourth_stop_step = self.defender_fourth_stop_step
        c.eval_defender_fourth_stop_step = self.eval_defender_fourth_stop_step
        c.eval_2_defender_fourth_stop_step = self.eval_2_defender_fourth_stop_step
        c.episode_snort_severe_baseline_first_stop_step = self.episode_snort_severe_baseline_first_stop_step
        c.episode_snort_warning_baseline_first_stop_step = self.episode_snort_warning_baseline_first_stop_step
        c.episode_snort_critical_baseline_first_stop_step = self.episode_snort_critical_baseline_first_stop_step
        c.episode_var_log_baseline_first_stop_step = self.episode_var_log_baseline_first_stop_step
        c.episode_step_baseline_first_stop_step = self.episode_step_baseline_first_stop_step
        c.episode_snort_severe_baseline_second_stop_step = self.episode_snort_severe_baseline_second_stop_step
        c.episode_snort_warning_baseline_second_stop_step = self.episode_snort_warning_baseline_second_stop_step
        c.episode_snort_critical_baseline_second_stop_step = self.episode_snort_critical_baseline_second_stop_step
        c.episode_var_log_baseline_second_stop_step = self.episode_var_log_baseline_second_stop_step
        c.episode_step_baseline_second_stop_step = self.episode_step_baseline_second_stop_step
        c.episode_snort_severe_baseline_third_stop_step = self.episode_snort_severe_baseline_third_stop_step
        c.episode_snort_warning_baseline_third_stop_step = self.episode_snort_warning_baseline_third_stop_step
        c.episode_snort_critical_baseline_third_stop_step = self.episode_snort_critical_baseline_third_stop_step
        c.episode_var_log_baseline_third_stop_step = self.episode_var_log_baseline_third_stop_step
        c.episode_step_baseline_third_stop_step = self.episode_step_baseline_third_stop_step
        c.episode_snort_severe_baseline_fourth_stop_step = self.episode_snort_severe_baseline_fourth_stop_step
        c.episode_snort_warning_baseline_fourth_stop_step = self.episode_snort_warning_baseline_fourth_stop_step
        c.episode_snort_critical_baseline_fourth_stop_step = self.episode_snort_critical_baseline_fourth_stop_step
        c.episode_var_log_baseline_fourth_stop_step = self.episode_var_log_baseline_fourth_stop_step
        c.episode_step_baseline_fourth_stop_step = self.episode_step_baseline_fourth_stop_step
        c.episode_snort_severe_baseline_stops_remaining = self.episode_snort_severe_baseline_stops_remaining
        c.episode_snort_warning_baseline_stops_remaining = self.episode_snort_warning_baseline_stops_remaining
        c.episode_snort_critical_baseline_stops_remaining = self.episode_snort_critical_baseline_stops_remaining
        c.episode_var_log_baseline_stops_remaining = self.episode_var_log_baseline_stops_remaining
        c.episode_step_baseline_stops_remaining = self.episode_step_baseline_stops_remaining
        c.eval_episode_snort_severe_baseline_first_stop_step = self.eval_episode_snort_severe_baseline_first_stop_step
        c.eval_episode_snort_warning_baseline_first_stop_step = self.eval_episode_snort_warning_baseline_first_stop_step
        c.eval_episode_snort_critical_baseline_first_stop_step = self.eval_episode_snort_critical_baseline_first_stop_step
        c.eval_episode_var_log_baseline_first_stop_step = self.eval_episode_var_log_baseline_first_stop_step
        c.eval_episode_step_baseline_first_stop_step = self.eval_episode_step_baseline_first_stop_step
        c.eval_episode_snort_severe_baseline_second_stop_step = self.eval_episode_snort_severe_baseline_second_stop_step
        c.eval_episode_snort_warning_baseline_second_stop_step = self.eval_episode_snort_warning_baseline_second_stop_step
        c.eval_episode_snort_critical_baseline_second_stop_step = self.eval_episode_snort_critical_baseline_second_stop_step
        c.eval_episode_var_log_baseline_second_stop_step = self.eval_episode_var_log_baseline_second_stop_step
        c.eval_episode_step_baseline_second_stop_step = self.eval_episode_step_baseline_second_stop_step
        c.eval_episode_snort_severe_baseline_third_stop_step = self.eval_episode_snort_severe_baseline_third_stop_step
        c.eval_episode_snort_warning_baseline_third_stop_step = self.eval_episode_snort_warning_baseline_third_stop_step
        c.eval_episode_snort_critical_baseline_third_stop_step = self.eval_episode_snort_critical_baseline_third_stop_step
        c.eval_episode_var_log_baseline_third_stop_step = self.eval_episode_var_log_baseline_third_stop_step
        c.eval_episode_step_baseline_third_stop_step = self.eval_episode_step_baseline_third_stop_step
        c.eval_episode_snort_severe_baseline_fourth_stop_step = self.eval_episode_snort_severe_baseline_fourth_stop_step
        c.eval_episode_snort_warning_baseline_fourth_stop_step = self.eval_episode_snort_warning_baseline_fourth_stop_step
        c.eval_episode_snort_critical_baseline_fourth_stop_step = self.eval_episode_snort_critical_baseline_fourth_stop_step
        c.eval_episode_var_log_baseline_fourth_stop_step = self.eval_episode_var_log_baseline_fourth_stop_step
        c.eval_episode_step_baseline_fourth_stop_step = self.eval_episode_step_baseline_fourth_stop_step
        c.eval_episode_snort_severe_baseline_stops_remaining = self.eval_episode_snort_severe_baseline_stops_remaining
        c.eval_episode_snort_warning_baseline_stops_remaining = self.eval_episode_snort_warning_baseline_stops_remaining
        c.eval_episode_snort_critical_baseline_stops_remaining = self.eval_episode_snort_critical_baseline_stops_remaining
        c.eval_episode_var_log_baseline_stops_remaining = self.eval_episode_var_log_baseline_stops_remaining
        c.eval_episode_step_baseline_stops_remaining = self.eval_episode_step_baseline_stops_remaining
        c.eval_2_episode_snort_severe_baseline_first_stop_step = self.eval_2_episode_snort_severe_baseline_first_stop_step
        c.eval_2_episode_snort_warning_baseline_first_stop_step = self.eval_2_episode_snort_warning_baseline_first_stop_step
        c.eval_2_episode_snort_critical_baseline_first_stop_step = self.eval_2_episode_snort_critical_baseline_first_stop_step
        c.eval_2_episode_var_log_baseline_first_stop_step = self.eval_2_episode_var_log_baseline_first_stop_step
        c.eval_2_episode_step_baseline_first_stop_step = self.eval_2_episode_step_baseline_first_stop_step
        c.eval_2_episode_snort_severe_baseline_second_stop_step = self.eval_2_episode_snort_severe_baseline_second_stop_step
        c.eval_2_episode_snort_warning_baseline_second_stop_step = self.eval_2_episode_snort_warning_baseline_second_stop_step
        c.eval_2_episode_snort_critical_baseline_second_stop_step = self.eval_2_episode_snort_critical_baseline_second_stop_step
        c.eval_2_episode_var_log_baseline_second_stop_step = self.eval_2_episode_var_log_baseline_second_stop_step
        c.eval_2_episode_step_baseline_second_stop_step = self.eval_2_episode_step_baseline_second_stop_step
        c.eval_2_episode_snort_severe_baseline_third_stop_step = self.eval_2_episode_snort_severe_baseline_third_stop_step
        c.eval_2_episode_snort_warning_baseline_third_stop_step = self.eval_2_episode_snort_warning_baseline_third_stop_step
        c.eval_2_episode_snort_critical_baseline_third_stop_step = self.eval_2_episode_snort_critical_baseline_third_stop_step
        c.eval_2_episode_var_log_baseline_third_stop_step = self.eval_2_episode_var_log_baseline_third_stop_step
        c.eval_2_episode_step_baseline_third_stop_step = self.eval_2_episode_step_baseline_third_stop_step
        c.eval_2_episode_snort_severe_baseline_fourth_stop_step = self.eval_2_episode_snort_severe_baseline_fourth_stop_step
        c.eval_2_episode_snort_warning_baseline_fourth_stop_step = self.eval_2_episode_snort_warning_baseline_fourth_stop_step
        c.eval_2_episode_snort_critical_baseline_fourth_stop_step = self.eval_2_episode_snort_critical_baseline_fourth_stop_step
        c.eval_2_episode_var_log_baseline_fourth_stop_step = self.eval_2_episode_var_log_baseline_fourth_stop_step
        c.eval_2_episode_step_baseline_fourth_stop_step = self.eval_2_episode_step_baseline_fourth_stop_step
        c.eval_2_episode_snort_severe_baseline_stops_remaining = self.eval_2_episode_snort_severe_baseline_stops_remaining
        c.eval_2_episode_snort_warning_baseline_stops_remaining = self.eval_2_episode_snort_warning_baseline_stops_remaining
        c.eval_2_episode_snort_critical_baseline_stops_remaining = self.eval_2_episode_snort_critical_baseline_stops_remaining
        c.eval_2_episode_var_log_baseline_stops_remaining = self.eval_2_episode_var_log_baseline_stops_remaining
        c.eval_2_episode_step_baseline_stops_remaining = self.eval_2_episode_step_baseline_stops_remaining
        c.optimal_stops_remaining = self.optimal_stops_remaining
        c.eval_optimal_stops_remaining = self.eval_optimal_stops_remaining
        c.eval_2_optimal_stops_remaining = self.eval_2_optimal_stops_remaining
        c.optimal_first_stop_step = self.optimal_first_stop_step
        c.eval_optimal_first_stop_step = self.eval_optimal_first_stop_step
        c.eval_2_optimal_first_stop_step = self.eval_2_optimal_first_stop_step
        c.optimal_second_stop_step = self.optimal_second_stop_step
        c.eval_optimal_second_stop_step = self.eval_optimal_second_stop_step
        c.eval_2_optimal_second_stop_step = self.eval_2_optimal_second_stop_step
        c.optimal_third_stop_step = self.optimal_third_stop_step
        c.eval_optimal_third_stop_step = self.eval_optimal_third_stop_step
        c.eval_2_optimal_third_stop_step = self.eval_2_optimal_third_stop_step
        c.optimal_fourth_stop_step = self.optimal_fourth_stop_step
        c.eval_optimal_fourth_stop_step = self.eval_optimal_fourth_stop_step
        c.eval_2_optimal_fourth_stop_step = self.eval_2_optimal_fourth_stop_step
        c.optimal_defender_episode_steps = self.optimal_defender_episode_steps
        c.eval_optimal_defender_episode_steps = self.eval_optimal_defender_episode_steps
        c.eval_2_optimal_defender_episode_steps = self.eval_2_optimal_defender_episode_steps
        return c

    def copy_saved_env_2(self, saved_log_dto : "TrainAgentLogDTO") -> None:
        """
        Copies the eval_2 variables from a different object

        :param saved_log_dto: the object to copy from
        :return: None
        """
        self.attacker_eval_2_episode_rewards = saved_log_dto.attacker_eval_2_episode_rewards
        self.defender_eval_2_episode_rewards = saved_log_dto.defender_eval_2_episode_rewards
        self.eval_2_episode_steps = saved_log_dto.eval_2_episode_steps
        self.eval_2_episode_flags_percentage = saved_log_dto.eval_2_episode_flags_percentage
        self.eval_2_episode_flags = saved_log_dto.eval_2_episode_flags
        self.eval_2_episode_caught = saved_log_dto.eval_2_episode_caught
        self.eval_2_episode_early_stopped = saved_log_dto.eval_2_episode_early_stopped
        self.eval_2_episode_successful_intrusion = saved_log_dto.eval_2_episode_successful_intrusion
        self.eval_2_episode_snort_severe_baseline_rewards = saved_log_dto.eval_2_episode_snort_severe_baseline_rewards
        self.eval_2_episode_snort_warning_baseline_rewards = saved_log_dto.eval_2_episode_snort_warning_baseline_rewards
        self.eval_2_episode_snort_critical_baseline_rewards = saved_log_dto.eval_2_episode_snort_critical_baseline_rewards
        self.eval_2_episode_var_log_baseline_rewards = saved_log_dto.eval_2_episode_var_log_baseline_rewards
        self.eval_2_episode_step_baseline_rewards = saved_log_dto.eval_2_episode_step_baseline_rewards
        self.attacker_eval_2_env_specific_rewards = saved_log_dto.attacker_eval_2_env_specific_rewards
        self.defender_eval_2_env_specific_rewards = saved_log_dto.defender_eval_2_env_specific_rewards
        self.eval_2_episode_snort_severe_baseline_steps = saved_log_dto.eval_2_episode_snort_severe_baseline_steps
        self.eval_2_episode_snort_warning_baseline_steps = saved_log_dto.eval_2_episode_snort_warning_baseline_steps
        self.eval_2_episode_snort_critical_baseline_steps = saved_log_dto.eval_2_episode_snort_critical_baseline_steps
        self.eval_2_episode_var_log_baseline_steps = saved_log_dto.eval_2_episode_var_log_baseline_steps
        self.eval_2_episode_step_baseline_steps = saved_log_dto.eval_2_episode_step_baseline_steps
        self.eval_2_env_specific_steps = saved_log_dto.eval_2_env_specific_steps
        self.eval_2_env_specific_flags = saved_log_dto.eval_2_env_specific_flags
        self.eval_2_env_specific_flags_percentage = saved_log_dto.eval_2_env_specific_flags_percentage
        self.eval_2_attacker_action_costs = saved_log_dto.eval_2_attacker_action_costs
        self.eval_2_attacker_action_costs_norm = saved_log_dto.eval_2_attacker_action_costs_norm
        self.eval_2_attacker_action_alerts = saved_log_dto.eval_2_attacker_action_alerts
        self.eval_2_attacker_action_alerts_norm = saved_log_dto.eval_2_attacker_action_alerts_norm
        self.eval_2_episode_intrusion_steps = saved_log_dto.eval_2_episode_intrusion_steps
        self.eval_2_episode_snort_severe_baseline_caught_attacker = saved_log_dto.eval_2_episode_snort_severe_baseline_caught_attacker
        self.eval_2_episode_snort_warning_baseline_caught_attacker = saved_log_dto.eval_2_episode_snort_warning_baseline_caught_attacker
        self.eval_2_episode_snort_critical_baseline_caught_attacker = saved_log_dto.eval_2_episode_snort_critical_baseline_caught_attacker
        self.eval_2_episode_var_log_baseline_caught_attacker = saved_log_dto.eval_2_episode_var_log_baseline_caught_attacker
        self.eval_2_episode_step_baseline_caught_attacker = saved_log_dto.eval_2_episode_step_baseline_caught_attacker
        self.eval_2_episode_snort_severe_baseline_early_stopping = saved_log_dto.eval_2_episode_snort_severe_baseline_early_stopping
        self.eval_2_episode_snort_warning_baseline_early_stopping = saved_log_dto.eval_2_episode_snort_warning_baseline_early_stopping
        self.eval_2_episode_snort_critical_baseline_early_stopping = saved_log_dto.eval_2_episode_snort_critical_baseline_early_stopping
        self.eval_2_episode_var_log_baseline_early_stopping = saved_log_dto.eval_2_episode_var_log_baseline_early_stopping
        self.eval_2_episode_step_baseline_early_stopping = saved_log_dto.eval_2_episode_step_baseline_early_stopping
        self.eval_2_episode_snort_severe_baseline_uncaught_intrusion_steps = saved_log_dto.eval_2_episode_snort_severe_baseline_uncaught_intrusion_steps
        self.eval_2_episode_snort_warning_baseline_uncaught_intrusion_steps = saved_log_dto.eval_2_episode_snort_warning_baseline_uncaught_intrusion_steps
        self.eval_2_episode_snort_critical_baseline_uncaught_intrusion_steps = saved_log_dto.eval_2_episode_snort_critical_baseline_uncaught_intrusion_steps
        self.eval_2_episode_var_log_baseline_uncaught_intrusion_steps = saved_log_dto.eval_2_episode_var_log_baseline_uncaught_intrusion_steps
        self.eval_2_episode_step_baseline_uncaught_intrusion_steps = saved_log_dto.eval_2_episode_step_baseline_uncaught_intrusion_steps
        self.eval_2_uncaught_intrusion_steps = saved_log_dto.eval_2_uncaught_intrusion_steps
        self.eval_2_optimal_defender_reward = saved_log_dto.eval_2_optimal_defender_reward
        self.eval_2_defender_stops_remaining = saved_log_dto.defender_stops_remaining
        self.eval_2_defender_first_stop_step = saved_log_dto.eval_2_defender_first_stop_step
        self.eval_2_defender_second_stop_step = saved_log_dto.eval_2_defender_second_stop_step
        self.eval_2_defender_third_stop_step = saved_log_dto.eval_2_defender_third_stop_step
        self.eval_2_defender_fourth_stop_step = saved_log_dto.eval_2_defender_fourth_stop_step
        self.eval_2_episode_snort_severe_baseline_first_stop_step = saved_log_dto.eval_2_episode_snort_severe_baseline_first_stop_step
        self.eval_2_episode_snort_warning_baseline_first_stop_step = saved_log_dto.eval_2_episode_snort_warning_baseline_first_stop_step
        self.eval_2_episode_snort_critical_baseline_first_stop_step = saved_log_dto.eval_2_episode_snort_critical_baseline_first_stop_step
        self.eval_2_episode_var_log_baseline_first_stop_step = saved_log_dto.eval_2_episode_var_log_baseline_first_stop_step
        self.eval_2_episode_step_baseline_first_stop_step = saved_log_dto.eval_2_episode_step_baseline_first_stop_step
        self.eval_2_episode_snort_severe_baseline_second_stop_step = saved_log_dto.eval_2_episode_snort_severe_baseline_second_stop_step
        self.eval_2_episode_snort_warning_baseline_second_stop_step = saved_log_dto.eval_2_episode_snort_warning_baseline_second_stop_step
        self.eval_2_episode_snort_critical_baseline_second_stop_step = saved_log_dto.eval_2_episode_snort_critical_baseline_second_stop_step
        self.eval_2_episode_var_log_baseline_second_stop_step = saved_log_dto.eval_2_episode_var_log_baseline_second_stop_step
        self.eval_2_episode_step_baseline_second_stop_step = saved_log_dto.eval_2_episode_step_baseline_second_stop_step
        self.eval_2_episode_snort_severe_baseline_third_stop_step = saved_log_dto.eval_2_episode_snort_severe_baseline_third_stop_step
        self.eval_2_episode_snort_warning_baseline_third_stop_step = saved_log_dto.eval_2_episode_snort_warning_baseline_third_stop_step
        self.eval_2_episode_snort_critical_baseline_third_stop_step = saved_log_dto.eval_2_episode_snort_critical_baseline_third_stop_step
        self.eval_2_episode_var_log_baseline_third_stop_step = saved_log_dto.eval_2_episode_var_log_baseline_third_stop_step
        self.eval_2_episode_step_baseline_third_stop_step = saved_log_dto.eval_2_episode_step_baseline_third_stop_step
        self.eval_2_episode_snort_severe_baseline_fourth_stop_step = saved_log_dto.eval_2_episode_snort_severe_baseline_fourth_stop_step
        self.eval_2_episode_snort_warning_baseline_fourth_stop_step = saved_log_dto.eval_2_episode_snort_warning_baseline_fourth_stop_step
        self.eval_2_episode_snort_critical_baseline_fourth_stop_step = saved_log_dto.eval_2_episode_snort_critical_baseline_fourth_stop_step
        self.eval_2_episode_var_log_baseline_fourth_stop_step = saved_log_dto.eval_2_episode_var_log_baseline_fourth_stop_step
        self.eval_2_episode_step_baseline_fourth_stop_step = saved_log_dto.eval_2_episode_step_baseline_fourth_stop_step
        self.eval_2_episode_snort_severe_baseline_stops_remaining = saved_log_dto.eval_2_episode_snort_severe_baseline_stops_remaining
        self.eval_2_episode_snort_warning_baseline_stops_remaining = saved_log_dto.eval_2_episode_snort_warning_baseline_stops_remaining
        self.eval_2_episode_snort_critical_baseline_stops_remaining = saved_log_dto.eval_2_episode_snort_critical_baseline_stops_remaining
        self.eval_2_episode_var_log_baseline_stops_remaining = saved_log_dto.eval_2_episode_var_log_baseline_stops_remaining
        self.eval_2_episode_step_baseline_stops_remaining = saved_log_dto.eval_2_episode_step_baseline_stops_remaining
        self.eval_2_optimal_stops_remaining = saved_log_dto.optimal_stops_remaining
        self.eval_2_optimal_first_stop_step = saved_log_dto.eval_2_optimal_first_stop_step
        self.eval_2_optimal_second_stop_step = saved_log_dto.eval_2_optimal_second_stop_step
        self.eval_2_optimal_third_stop_step = saved_log_dto.eval_2_optimal_third_stop_step
        self.eval_2_optimal_fourth_stop_step = saved_log_dto.eval_2_optimal_fourth_stop_step
        self.eval_2_optimal_defender_episode_steps = saved_log_dto.eval_2_optimal_defender_episode_steps

    def eval_update_env_specific_metrics(self, env_config : PyCREnvConfig, infos : dict, i: int) -> int:
        """
        Utility function for updating env-specific eval metrics

        :param env_config: the environment configuration
        :param infos: info dicts
        :param i: the iteration
        :return: None
        """
        if env_config.emulation_config is not None:
            agent_ip = env_config.emulation_config.agent_ip
        else:
            agent_ip = env_config.idx
        num_flags = env_config.num_flags

        if agent_ip not in self.attacker_eval_env_specific_rewards:
            self.attacker_eval_env_specific_rewards[agent_ip] = [self.attacker_episode_rewards]
        else:
            self.attacker_eval_env_specific_rewards[agent_ip].append(self.attacker_episode_rewards)

        if agent_ip not in self.defender_eval_env_specific_rewards:
            self.defender_eval_env_specific_rewards[agent_ip] = [self.defender_episode_rewards]
        else:
            self.defender_eval_env_specific_rewards[agent_ip].append(self.defender_episode_rewards)

        if agent_ip not in self.eval_env_specific_steps:
            self.eval_env_specific_steps[agent_ip] = [self.episode_steps]
        else:
            self.eval_env_specific_steps[agent_ip].append(self.episode_steps)

        if agent_ip not in self.eval_env_specific_flags:
            self.eval_env_specific_flags[agent_ip] = [infos["flags"]]
        else:
            self.eval_env_specific_flags[agent_ip].append(infos["flags"])

        if agent_ip not in self.eval_env_specific_flags_percentage:
            self.eval_env_specific_flags_percentage[agent_ip] = [infos["flags"] / num_flags]
        else:
            self.eval_env_specific_flags_percentage[agent_ip].append(infos["flags"] / num_flags)

    def eval_2_update_env_specific_metrics(self, env_config : PyCREnvConfig, infos : dict, i : int) -> None:
        """
        Updates env-specific eval 2 metrics

        :param env_config: the environment configuration
        :param infos: info dicts
        :param i: the iteration
        :return: None
        """

        if env_config.emulation_config is not None:
            agent_ip = env_config.emulation_config.agent_ip
        else:
            agent_ip = env_config.idx
        num_flags = env_config.num_flags

        if agent_ip not in self.attacker_eval_2_env_specific_rewards:
            self.attacker_eval_2_env_specific_rewards[agent_ip] = [self.attacker_episode_rewards]
        else:
            self.attacker_eval_2_env_specific_rewards[agent_ip].append(self.attacker_episode_rewards)

        if agent_ip not in self.defender_eval_2_env_specific_rewards:
            self.defender_eval_2_env_specific_rewards[agent_ip] = [self.defender_episode_rewards]
        else:
            self.defender_eval_2_env_specific_rewards[agent_ip].append(self.defender_episode_rewards)

        if agent_ip not in self.eval_2_env_specific_steps:
            self.eval_2_env_specific_steps[agent_ip] = [self.episode_steps]
        else:
            self.eval_2_env_specific_steps[agent_ip].append(self.episode_steps)

        if agent_ip not in self.eval_2_env_specific_flags:
            self.eval_2_env_specific_flags[agent_ip] = [infos["flags"]]
        else:
            self.eval_2_env_specific_flags[agent_ip].append(infos["flags"])

        if agent_ip not in self.eval_2_env_specific_flags_percentage:
            self.eval_2_env_specific_flags_percentage[agent_ip] = [infos["flags"] / num_flags]
        else:
            self.eval_2_env_specific_flags_percentage[agent_ip].append(infos["flags"] / num_flags)



    def eval_update(self, attacker_episode_reward, defender_episode_reward, _info: dict, episode_length: int,
                    env_conf: PyCREnvConfig, i: int) -> None:
        """
        Updates the eval metrics of the DTO with new data

        :param attacker_episode_reward: the attacker episode reward
        :param defender_episode_reward: the defender episode reward
        :param _info: the list of info dicts
        :param episode_length: the length of the episode
        :param env_conf: the environment configuration
        :param i: the index i
        :return: None
        """
        self.attacker_eval_episode_rewards.append(attacker_episode_reward)
        self.defender_eval_episode_rewards.append(defender_episode_reward)
        self.eval_episode_steps.append(episode_length)
        self.eval_episode_flags.append(_info[constants.INFO_DICT.FLAGS])
        self.eval_episode_caught.append(_info[constants.INFO_DICT.CAUGHT_ATTACKER])
        self.eval_episode_early_stopped.append(_info[constants.INFO_DICT.EARLY_STOPPED])
        self.eval_episode_successful_intrusion.append(_info[constants.INFO_DICT.SUCCESSFUL_INTRUSION])
        self.eval_episode_snort_severe_baseline_rewards.append(_info[constants.INFO_DICT.SNORT_SEVERE_BASELINE_REWARD])
        self.eval_episode_snort_warning_baseline_rewards.append(_info[
                                                                    constants.INFO_DICT.SNORT_WARNING_BASELINE_REWARD])
        self.eval_episode_snort_critical_baseline_rewards.append(_info[
                                                                     constants.INFO_DICT.SNORT_CRITICAL_BASELINE_REWARD])
        self.eval_episode_var_log_baseline_rewards.append(_info[constants.INFO_DICT.VAR_LOG_BASELINE_REWARD])
        self.eval_episode_step_baseline_rewards.append(_info[constants.INFO_DICT.STEP_BASELINE_REWARD])
        self.eval_episode_snort_severe_baseline_steps.append(_info[constants.INFO_DICT.SNORT_SEVERE_BASELINE_STEP])
        self.eval_episode_snort_warning_baseline_steps.append(_info[constants.INFO_DICT.SNORT_WARNING_BASELINE_STEP])
        self.eval_episode_snort_critical_baseline_steps.append(_info[constants.INFO_DICT.SNORT_CRITICAL_BASELINE_STEP])
        self.eval_episode_var_log_baseline_steps.append(_info[constants.INFO_DICT.VAR_LOG_BASELINE_STEP])
        self.eval_episode_step_baseline_steps.append(_info[constants.INFO_DICT.STEP_BASELINE_STEP])
        self.eval_episode_snort_severe_baseline_caught_attacker.append(_info[
                                                                           constants.INFO_DICT.SNORT_SEVERE_BASELINE_CAUGHT_ATTACKER])
        self.eval_episode_snort_warning_baseline_caught_attacker.append(_info[
                                                                            constants.INFO_DICT.SNORT_WARNING_BASELINE_CAUGHT_ATTACKER])
        self.eval_episode_snort_critical_baseline_caught_attacker.append(_info[
                                                                             constants.INFO_DICT.SNORT_CRITICAL_BASELINE_CAUGHT_ATTACKER])
        self.eval_episode_var_log_baseline_caught_attacker.append(_info[
                                                                      constants.INFO_DICT.VAR_LOG_BASELINE_CAUGHT_ATTACKER])
        self.eval_episode_step_baseline_caught_attacker.append(_info[constants.INFO_DICT.STEP_BASELINE_CAUGHT_ATTACKER])
        self.eval_episode_snort_severe_baseline_early_stopping.append(_info[
                                                                          constants.INFO_DICT.SNORT_SEVERE_BASELINE_EARLY_STOPPING])
        self.eval_episode_snort_warning_baseline_early_stopping.append(_info[
                                                                           constants.INFO_DICT.SNORT_WARNING_BASELINE_EARLY_STOPPING])
        self.eval_episode_snort_critical_baseline_early_stopping.append(_info[
                                                                            constants.INFO_DICT.SNORT_CRITICAL_BASELINE_EARLY_STOPPING])
        self.eval_episode_var_log_baseline_early_stopping.append(_info[
                                                                     constants.INFO_DICT.VAR_LOG_BASELINE_EARLY_STOPPING])
        self.eval_episode_step_baseline_early_stopping.append(_info[constants.INFO_DICT.STEP_BASELINE_EARLY_STOPPING])
        self.eval_episode_snort_severe_baseline_uncaught_intrusion_steps.append(_info[
                                                                                    constants.INFO_DICT.SNORT_SEVERE_BASELINE_UNCAUGHT_INTRUSION_STEPS])
        self.eval_episode_snort_warning_baseline_uncaught_intrusion_steps.append(_info[
                                                                                     constants.INFO_DICT.SNORT_WARNING_BASELINE_UNCAUGHT_INTRUSION_STEPS])
        self.eval_episode_snort_critical_baseline_uncaught_intrusion_steps.append(_info[
                                                                                      constants.INFO_DICT.SNORT_CRITICAL_BASELINE_UNCAUGHT_INTRUSION_STEPS])
        self.eval_episode_var_log_baseline_uncaught_intrusion_steps.append(_info[
                                                                               constants.INFO_DICT.VAR_LOG_BASELINE_UNCAUGHT_INTRUSION_STEPS])
        self.eval_episode_step_baseline_uncaught_intrusion_steps.append(_info[
                                                                            constants.INFO_DICT.STEP_BASELINE_UNCAUGHT_INTRUSION_STEPS])
        self.eval_episode_flags_percentage.append(_info[constants.INFO_DICT.FLAGS] / env_conf.num_flags)
        self.eval_attacker_action_costs.append(_info[constants.INFO_DICT.ATTACKER_COST])
        self.eval_attacker_action_costs_norm.append(_info[constants.INFO_DICT.ATTACKER_COST_NORM])
        self.eval_attacker_action_alerts.append(_info[constants.INFO_DICT.ATTACKER_ALERTS])
        self.eval_attacker_action_alerts_norm.append(_info[constants.INFO_DICT.ATTACKER_ALERTS_NORM])
        self.eval_episode_intrusion_steps.append(_info[constants.INFO_DICT.INTRUSION_STEP])
        self.eval_uncaught_intrusion_steps.append(_info[constants.INFO_DICT.UNCAUGHT_INTRUSION_STEPS])
        self.eval_optimal_defender_reward.append(_info[constants.INFO_DICT.OPTIMAL_DEFENDER_REWARD])
        self.eval_defender_stops_remaining.append(_info[constants.INFO_DICT.DEFENDER_STOPS_REMAINING])
        self.eval_defender_first_stop_step.append(_info[constants.INFO_DICT.DEFENDER_FIRST_STOP_STEP])
        self.eval_defender_second_stop_step.append(_info[constants.INFO_DICT.DEFENDER_SECOND_STOP_STEP])
        self.eval_defender_third_stop_step.append(_info[constants.INFO_DICT.DEFENDER_THIRD_STOP_STEP])
        self.eval_defender_fourth_stop_step.append(_info[constants.INFO_DICT.DEFENDER_FOURTH_STOP_STEP])
        self.eval_episode_snort_severe_baseline_first_stop_step.append(_info[
                                                                           constants.INFO_DICT.SNORT_SEVERE_BASELINE_FIRST_STOP_STEP])
        self.eval_episode_snort_warning_baseline_first_stop_step.append(_info[
                                                                            constants.INFO_DICT.SNORT_WARNING_BASELINE_FIRST_STOP_STEP])
        self.eval_episode_snort_critical_baseline_first_stop_step.append(_info[
                                                                             constants.INFO_DICT.SNORT_CRITICAL_BASELINE_FIRST_STOP_STEP])
        self.eval_episode_var_log_baseline_first_stop_step.append(_info[
                                                                      constants.INFO_DICT.VAR_LOG_BASELINE_FIRST_STOP_STEP])
        self.eval_episode_step_baseline_first_stop_step.append(_info[constants.INFO_DICT.STEP_BASELINE_FIRST_STOP_STEP])
        self.eval_episode_snort_severe_baseline_second_stop_step.append(_info[
                                                                            constants.INFO_DICT.SNORT_SEVERE_BASELINE_SECOND_STOP_STEP])
        self.eval_episode_snort_warning_baseline_second_stop_step.append(_info[
                                                                             constants.INFO_DICT.SNORT_WARNING_BASELINE_SECOND_STOP_STEP])
        self.eval_episode_snort_critical_baseline_second_stop_step.append(_info[
                                                                              constants.INFO_DICT.SNORT_CRITICAL_BASELINE_SECOND_STOP_STEP])
        self.eval_episode_var_log_baseline_second_stop_step.append(_info[
                                                                       constants.INFO_DICT.VAR_LOG_BASELINE_SECOND_STOP_STEP])
        self.eval_episode_step_baseline_second_stop_step.append(_info[
                                                                    constants.INFO_DICT.STEP_BASELINE_SECOND_STOP_STEP])
        self.eval_episode_snort_severe_baseline_third_stop_step.append(_info[
                                                                           constants.INFO_DICT.SNORT_SEVERE_BASELINE_THIRD_STOP_STEP])
        self.eval_episode_snort_warning_baseline_third_stop_step.append(_info[
                                                                            constants.INFO_DICT.SNORT_WARNING_BASELINE_THIRD_STOP_STEP])
        self.eval_episode_snort_critical_baseline_third_stop_step.append(_info[
                                                                             constants.INFO_DICT.SNORT_CRITICAL_BASELINE_THIRD_STOP_STEP])
        self.eval_episode_var_log_baseline_third_stop_step.append(_info[
                                                                      constants.INFO_DICT.VAR_LOG_BASELINE_THIRD_STOP_STEP])
        self.eval_episode_step_baseline_third_stop_step.append(_info[constants.INFO_DICT.STEP_BASELINE_THIRD_STOP_STEP])
        self.eval_episode_snort_severe_baseline_fourth_stop_step.append(_info[
                                                                            constants.INFO_DICT.SNORT_SEVERE_BASELINE_FOURTH_STOP_STEP])
        self.eval_episode_snort_warning_baseline_fourth_stop_step.append(_info[
                                                                             constants.INFO_DICT.SNORT_WARNING_BASELINE_FOURTH_STOP_STEP])
        self.eval_episode_snort_critical_baseline_fourth_stop_step.append(_info[
                                                                              constants.INFO_DICT.SNORT_CRITICAL_BASELINE_FOURTH_STOP_STEP])
        self.eval_episode_var_log_baseline_fourth_stop_step.append(_info[
                                                                       constants.INFO_DICT.VAR_LOG_BASELINE_FOURTH_STOP_STEP])
        self.eval_episode_step_baseline_fourth_stop_step.append(_info[
                                                                    constants.INFO_DICT.STEP_BASELINE_FOURTH_STOP_STEP])
        self.eval_episode_snort_severe_baseline_stops_remaining.append(_info[
                                                                           constants.INFO_DICT.SNORT_SEVERE_BASELINE_STOPS_REMAINING])
        self.eval_episode_snort_warning_baseline_stops_remaining.append(_info[
                                                                            constants.INFO_DICT.SNORT_WARNING_BASELINE_STOPS_REMAINING])
        self.eval_episode_snort_critical_baseline_stops_remaining.append(_info[
                                                                             constants.INFO_DICT.SNORT_CRITICAL_BASELINE_STOPS_REMAINING])
        self.eval_episode_var_log_baseline_stops_remaining.append(_info[
                                                                      constants.INFO_DICT.VAR_LOG_BASELINE_STOPS_REMAINING])
        self.eval_episode_step_baseline_stops_remaining.append(_info[constants.INFO_DICT.STEP_BASELINE_STOPS_REMAINING])
        self.eval_optimal_stops_remaining.append(_info[constants.INFO_DICT.OPTIMAL_STOPS_REMAINING])
        self.eval_optimal_first_stop_step.append(_info[constants.INFO_DICT.OPTIMAL_FIRST_STOP_STEP])
        self.eval_optimal_second_stop_step.append(_info[constants.INFO_DICT.OPTIMAL_SECOND_STOP_STEP])
        self.eval_optimal_third_stop_step.append(_info[constants.INFO_DICT.OPTIMAL_THIRD_STOP_STEP])
        self.eval_optimal_fourth_stop_step.append(_info[constants.INFO_DICT.OPTIMAL_FOURTH_STOP_STEP])
        self.eval_optimal_defender_episode_steps.append(_info[constants.INFO_DICT.OPTIMAL_DEFENDER_EPISODE_STEPS])
        self.eval_update_env_specific_metrics(env_conf, _info, i)

    def eval_2_update(self, attacker_episode_reward, defender_episode_reward, _info: dict, episode_length: int,
                      env_conf: PyCREnvConfig, i: int) -> None:
        """
        Updates the eval2 metrics of the DTO with data from an evaluation episode

        :param attacker_episode_reward: the attacker episode reward
        :param defender_episode_reward: the defender episode reward
        :param _info: the info dicts
        :param episode_length: the episode length
        :param env_conf: the environment configuration
        :param i: the index
        :return: None
        """
        self.attacker_eval_2_episode_rewards.append(attacker_episode_reward)
        self.defender_eval_2_episode_rewards.append(defender_episode_reward)
        self.eval_2_episode_steps.append(episode_length)
        self.eval_2_episode_flags.append(_info[constants.INFO_DICT.FLAGS])
        self.eval_2_episode_caught.append(_info[constants.INFO_DICT.CAUGHT_ATTACKER])
        self.eval_2_episode_early_stopped.append(_info[constants.INFO_DICT.EARLY_STOPPED])
        self.eval_2_episode_successful_intrusion.append(_info[constants.INFO_DICT.SUCCESSFUL_INTRUSION])
        self.eval_2_episode_snort_severe_baseline_rewards.append(_info[
                                                                     constants.INFO_DICT.SNORT_SEVERE_BASELINE_REWARD])
        self.eval_2_episode_snort_warning_baseline_rewards.append(_info[
                                                                      constants.INFO_DICT.SNORT_WARNING_BASELINE_REWARD])
        self.eval_2_episode_snort_critical_baseline_rewards.append(_info[
                                                                       constants.INFO_DICT.SNORT_CRITICAL_BASELINE_REWARD])
        self.eval_2_episode_step_baseline_rewards.append(_info[constants.INFO_DICT.STEP_BASELINE_REWARD])
        self.eval_2_episode_snort_severe_baseline_steps.append(_info[constants.INFO_DICT.SNORT_SEVERE_BASELINE_STEP])
        self.eval_2_episode_snort_warning_baseline_steps.append(_info[constants.INFO_DICT.SNORT_WARNING_BASELINE_STEP])
        self.eval_2_episode_snort_critical_baseline_steps.append(_info[
                                                                     constants.INFO_DICT.SNORT_CRITICAL_BASELINE_STEP])
        self.eval_2_episode_var_log_baseline_steps.append(_info[constants.INFO_DICT.VAR_LOG_BASELINE_STEP])
        self.eval_2_episode_step_baseline_steps.append(_info[constants.INFO_DICT.STEP_BASELINE_STEP])
        self.eval_2_episode_snort_severe_baseline_caught_attacker.append(_info[
                                                                             constants.INFO_DICT.SNORT_SEVERE_BASELINE_CAUGHT_ATTACKER])
        self.eval_2_episode_snort_warning_baseline_caught_attacker.append(_info[
                                                                              constants.INFO_DICT.SNORT_WARNING_BASELINE_CAUGHT_ATTACKER])
        self.eval_2_episode_snort_critical_baseline_caught_attacker.append(_info[
                                                                               constants.INFO_DICT.SNORT_CRITICAL_BASELINE_CAUGHT_ATTACKER])
        self.eval_2_episode_var_log_baseline_caught_attacker.append(_info[
                                                                        constants.INFO_DICT.VAR_LOG_BASELINE_CAUGHT_ATTACKER])
        self.eval_2_episode_step_baseline_caught_attacker.append(_info[
                                                                     constants.INFO_DICT.STEP_BASELINE_CAUGHT_ATTACKER])
        self.eval_2_episode_snort_severe_baseline_early_stopping.append(_info[
                                                                            constants.INFO_DICT.SNORT_SEVERE_BASELINE_EARLY_STOPPING])
        self.eval_2_episode_snort_warning_baseline_early_stopping.append(_info[
                                                                             constants.INFO_DICT.SNORT_WARNING_BASELINE_EARLY_STOPPING])
        self.eval_2_episode_snort_critical_baseline_early_stopping.append(_info[
                                                                              constants.INFO_DICT.SNORT_CRITICAL_BASELINE_EARLY_STOPPING])
        self.eval_2_episode_var_log_baseline_early_stopping.append(_info[
                                                                       constants.INFO_DICT.VAR_LOG_BASELINE_EARLY_STOPPING])
        self.eval_2_episode_step_baseline_early_stopping.append(_info[constants.INFO_DICT.STEP_BASELINE_EARLY_STOPPING])
        self.eval_2_episode_snort_severe_baseline_uncaught_intrusion_steps.append(_info[
                                                                                      constants.INFO_DICT.SNORT_SEVERE_BASELINE_UNCAUGHT_INTRUSION_STEPS])
        self.eval_2_episode_snort_warning_baseline_uncaught_intrusion_steps.append(_info[
                                                                                       constants.INFO_DICT.SNORT_WARNING_BASELINE_UNCAUGHT_INTRUSION_STEPS])
        self.eval_2_episode_snort_critical_baseline_uncaught_intrusion_steps.append(_info[
                                                                                        constants.INFO_DICT.SNORT_CRITICAL_BASELINE_UNCAUGHT_INTRUSION_STEPS])
        self.eval_2_episode_var_log_baseline_uncaught_intrusion_steps.append(_info[
                                                                                 constants.INFO_DICT.VAR_LOG_BASELINE_UNCAUGHT_INTRUSION_STEPS])
        self.eval_2_episode_step_baseline_uncaught_intrusion_steps.append(_info[
                                                                              constants.INFO_DICT.STEP_BASELINE_UNCAUGHT_INTRUSION_STEPS])
        self.eval_2_episode_var_log_baseline_rewards.append(_info[constants.INFO_DICT.VAR_LOG_BASELINE_REWARD])
        self.eval_2_episode_flags_percentage.append(_info[constants.INFO_DICT.FLAGS] / env_conf.num_flags)
        self.eval_2_attacker_action_costs.append(_info[constants.INFO_DICT.ATTACKER_COST])
        self.eval_2_attacker_action_costs_norm.append(_info[constants.INFO_DICT.ATTACKER_COST_NORM])
        self.eval_2_attacker_action_alerts.append(_info[constants.INFO_DICT.ATTACKER_ALERTS])
        self.eval_2_attacker_action_alerts_norm.append(_info[constants.INFO_DICT.ATTACKER_ALERTS_NORM])
        self.eval_2_episode_intrusion_steps.append(_info[constants.INFO_DICT.INTRUSION_STEP])
        self.eval_2_uncaught_intrusion_steps.append(_info[constants.INFO_DICT.UNCAUGHT_INTRUSION_STEPS])
        self.eval_2_optimal_defender_reward.append(_info[constants.INFO_DICT.OPTIMAL_DEFENDER_REWARD])
        self.eval_2_defender_stops_remaining.append(_info[constants.INFO_DICT.DEFENDER_STOPS_REMAINING])
        self.eval_2_defender_first_stop_step.append(_info[constants.INFO_DICT.DEFENDER_FIRST_STOP_STEP])
        self.eval_2_defender_second_stop_step.append(_info[constants.INFO_DICT.DEFENDER_SECOND_STOP_STEP])
        self.eval_2_defender_third_stop_step.append(_info[constants.INFO_DICT.DEFENDER_THIRD_STOP_STEP])
        self.eval_2_defender_fourth_stop_step.append(_info[constants.INFO_DICT.DEFENDER_FOURTH_STOP_STEP])
        self.eval_2_episode_snort_severe_baseline_first_stop_step.append(_info[
                                                                             constants.INFO_DICT.SNORT_SEVERE_BASELINE_FIRST_STOP_STEP])
        self.eval_2_episode_snort_warning_baseline_first_stop_step.append(_info[
                                                                              constants.INFO_DICT.SNORT_WARNING_BASELINE_FIRST_STOP_STEP])
        self.eval_2_episode_snort_critical_baseline_first_stop_step.append(_info[
                                                                               constants.INFO_DICT.SNORT_CRITICAL_BASELINE_FIRST_STOP_STEP])
        self.eval_2_episode_var_log_baseline_first_stop_step.append(_info[
                                                                        constants.INFO_DICT.VAR_LOG_BASELINE_FIRST_STOP_STEP])
        self.eval_2_episode_step_baseline_first_stop_step.append(_info[
                                                                     constants.INFO_DICT.STEP_BASELINE_FIRST_STOP_STEP])
        self.eval_2_episode_snort_severe_baseline_second_stop_step.append(_info[
                                                                              constants.INFO_DICT.SNORT_SEVERE_BASELINE_SECOND_STOP_STEP])
        self.eval_2_episode_snort_warning_baseline_second_stop_step.append(_info[
                                                                               constants.INFO_DICT.SNORT_WARNING_BASELINE_SECOND_STOP_STEP])
        self.eval_2_episode_snort_critical_baseline_second_stop_step.append(_info[
                                                                                constants.INFO_DICT.SNORT_CRITICAL_BASELINE_SECOND_STOP_STEP])
        self.eval_2_episode_var_log_baseline_second_stop_step.append(_info[
                                                                         constants.INFO_DICT.VAR_LOG_BASELINE_SECOND_STOP_STEP])
        self.eval_2_episode_step_baseline_second_stop_step.append(_info[
                                                                      constants.INFO_DICT.STEP_BASELINE_SECOND_STOP_STEP])
        self.eval_2_episode_snort_severe_baseline_third_stop_step.append(_info[
                                                                             constants.INFO_DICT.SNORT_SEVERE_BASELINE_THIRD_STOP_STEP])
        self.eval_2_episode_snort_warning_baseline_third_stop_step.append(_info[
                                                                              constants.INFO_DICT.SNORT_WARNING_BASELINE_THIRD_STOP_STEP])
        self.eval_2_episode_snort_critical_baseline_third_stop_step.append(_info[
                                                                               constants.INFO_DICT.SNORT_CRITICAL_BASELINE_THIRD_STOP_STEP])
        self.eval_2_episode_var_log_baseline_third_stop_step.append(_info[
                                                                        constants.INFO_DICT.VAR_LOG_BASELINE_THIRD_STOP_STEP])
        self.eval_2_episode_step_baseline_third_stop_step.append(_info[
                                                                     constants.INFO_DICT.STEP_BASELINE_THIRD_STOP_STEP])
        self.eval_2_episode_snort_severe_baseline_fourth_stop_step.append(_info[
                                                                              constants.INFO_DICT.SNORT_SEVERE_BASELINE_FOURTH_STOP_STEP])
        self.eval_2_episode_snort_warning_baseline_fourth_stop_step.append(_info[
                                                                               constants.INFO_DICT.SNORT_WARNING_BASELINE_FOURTH_STOP_STEP])
        self.eval_2_episode_snort_critical_baseline_fourth_stop_step.append(_info[
                                                                                constants.INFO_DICT.SNORT_CRITICAL_BASELINE_FOURTH_STOP_STEP])
        self.eval_2_episode_var_log_baseline_fourth_stop_step.append(_info[
                                                                         constants.INFO_DICT.VAR_LOG_BASELINE_FOURTH_STOP_STEP])
        self.eval_2_episode_step_baseline_fourth_stop_step.append(_info[
                                                                      constants.INFO_DICT.STEP_BASELINE_FOURTH_STOP_STEP])
        self.eval_2_episode_snort_severe_baseline_stops_remaining.append(_info[
                                                                             constants.INFO_DICT.SNORT_SEVERE_BASELINE_STOPS_REMAINING])
        self.eval_2_episode_snort_warning_baseline_stops_remaining.append(_info[
                                                                              constants.INFO_DICT.SNORT_WARNING_BASELINE_STOPS_REMAINING])
        self.eval_2_episode_snort_critical_baseline_stops_remaining.append(_info[
                                                                               constants.INFO_DICT.SNORT_CRITICAL_BASELINE_STOPS_REMAINING])
        self.eval_2_episode_var_log_baseline_stops_remaining.append(_info[
                                                                        constants.INFO_DICT.VAR_LOG_BASELINE_STOPS_REMAINING])
        self.eval_2_episode_step_baseline_stops_remaining.append(_info[
                                                                     constants.INFO_DICT.STEP_BASELINE_STOPS_REMAINING])
        self.eval_2_optimal_stops_remaining.append(_info[constants.INFO_DICT.OPTIMAL_STOPS_REMAINING])
        self.eval_2_optimal_first_stop_step.append(_info[constants.INFO_DICT.OPTIMAL_FIRST_STOP_STEP])
        self.eval_2_optimal_second_stop_step.append(_info[constants.INFO_DICT.OPTIMAL_SECOND_STOP_STEP])
        self.eval_2_optimal_third_stop_step.append(_info[constants.INFO_DICT.OPTIMAL_THIRD_STOP_STEP])
        self.eval_2_optimal_fourth_stop_step.append(_info[constants.INFO_DICT.OPTIMAL_FOURTH_STOP_STEP])
        self.eval_2_optimal_defender_episode_steps.append(_info[constants.INFO_DICT.OPTIMAL_DEFENDER_EPISODE_STEPS])
        self.eval_2_update_env_specific_metrics(env_conf, _info, i)


    def update(self, rollout_data_dto: RolloutDataDTO, start, attacker_agent_config: AgentConfig) -> None:
        """
        Updates the DTO with new data from a rollout

        :param rollout_data_dto: a DTO with the rollout data
        :param start: the time-step where the episode started
        :param attacker_agent_config: the agent config
        :return: None
        """

        if attacker_agent_config.performance_analysis:
            end = time.time()
            self.rollout_times.append(end - start)
            self.env_response_times.extend(rollout_data_dto.env_response_times)
            self.action_pred_times.extend(rollout_data_dto.action_pred_times)

        self.attacker_episode_rewards.extend(rollout_data_dto.attacker_episode_rewards)
        self.defender_episode_rewards.extend(rollout_data_dto.defender_episode_rewards)
        self.episode_steps.extend(rollout_data_dto.episode_steps)
        self.episode_flags.extend(rollout_data_dto.episode_flags)
        self.episode_caught.extend(rollout_data_dto.episode_caught)
        self.episode_successful_intrusion.extend(rollout_data_dto.episode_successful_intrusion)
        self.episode_early_stopped.extend(rollout_data_dto.episode_early_stopped)
        self.episode_flags_percentage.extend(rollout_data_dto.episode_flags_percentage)
        self.episode_snort_severe_baseline_rewards.extend(rollout_data_dto.episode_snort_severe_baseline_rewards)
        self.episode_snort_warning_baseline_rewards.extend(rollout_data_dto.episode_snort_warning_baseline_rewards)
        self.episode_snort_critical_baseline_rewards.extend(rollout_data_dto.episode_snort_critical_baseline_rewards)
        self.episode_var_log_baseline_rewards.extend(rollout_data_dto.episode_var_log_baseline_rewards)
        self.episode_step_baseline_rewards.extend(rollout_data_dto.episode_step_baseline_rewards)
        self.episode_snort_severe_baseline_steps.extend(rollout_data_dto.episode_snort_severe_baseline_steps)
        self.episode_snort_warning_baseline_steps.extend(rollout_data_dto.episode_snort_warning_baseline_steps)
        self.episode_snort_critical_baseline_steps.extend(rollout_data_dto.episode_snort_critical_baseline_steps)
        self.episode_var_log_baseline_steps.extend(rollout_data_dto.episode_var_log_baseline_steps)
        self.episode_step_baseline_steps.extend(rollout_data_dto.episode_step_baseline_steps)
        self.attacker_action_costs.extend(rollout_data_dto.attacker_action_costs)
        self.attacker_action_costs_norm.extend(rollout_data_dto.attacker_action_costs_norm)
        self.attacker_action_alerts.extend(rollout_data_dto.attacker_action_alerts)
        self.attacker_action_alerts_norm.extend(rollout_data_dto.attacker_action_alerts_norm)
        self.episode_intrusion_steps.extend(rollout_data_dto.episode_intrusion_steps)
        self.episode_snort_severe_baseline_caught_attacker.extend(rollout_data_dto.episode_snort_severe_baseline_caught_attacker)
        self.episode_snort_warning_baseline_caught_attacker.extend(rollout_data_dto.episode_snort_warning_baseline_caught_attacker)
        self.episode_snort_critical_baseline_caught_attacker.extend(rollout_data_dto.episode_snort_critical_baseline_caught_attacker)
        self.episode_var_log_baseline_caught_attacker.extend(rollout_data_dto.episode_var_log_baseline_caught_attacker)
        self.episode_step_baseline_caught_attacker.extend(rollout_data_dto.episode_step_baseline_caught_attacker)
        self.episode_snort_severe_baseline_early_stopping.extend(rollout_data_dto.episode_snort_severe_baseline_early_stopping)
        self.episode_snort_warning_baseline_early_stopping.extend(rollout_data_dto.episode_snort_warning_baseline_early_stopping)
        self.episode_snort_critical_baseline_early_stopping.extend(rollout_data_dto.episode_snort_critical_baseline_early_stopping)
        self.episode_var_log_baseline_early_stopping.extend(rollout_data_dto.episode_var_log_baseline_early_stopping)
        self.episode_step_baseline_early_stopping.extend(rollout_data_dto.episode_step_baseline_early_stopping)
        self.episode_snort_severe_baseline_uncaught_intrusion_steps.extend(rollout_data_dto.episode_snort_severe_baseline_uncaught_intrusion_steps)
        self.episode_snort_warning_baseline_uncaught_intrusion_steps.extend(rollout_data_dto.episode_snort_warning_baseline_uncaught_intrusion_steps)
        self.episode_snort_critical_baseline_uncaught_intrusion_steps.extend(rollout_data_dto.episode_snort_critical_baseline_uncaught_intrusion_steps)
        self.episode_var_log_baseline_uncaught_intrusion_steps.extend(rollout_data_dto.episode_var_log_baseline_uncaught_intrusion_steps)
        self.episode_step_baseline_uncaught_intrusion_steps.extend(rollout_data_dto.episode_step_baseline_uncaught_intrusion_steps)
        self.uncaught_intrusion_steps.extend(rollout_data_dto.uncaught_intrusion_steps)
        self.optimal_defender_reward.extend(rollout_data_dto.optimal_defender_reward)
        self.defender_stops_remaining.extend(rollout_data_dto.defender_stops_remaining)
        self.defender_first_stop_step.extend(rollout_data_dto.defender_first_stop_step)
        self.defender_second_stop_step.extend(rollout_data_dto.defender_second_stop_step)
        self.defender_third_stop_step.extend(rollout_data_dto.defender_third_stop_step)
        self.defender_fourth_stop_step.extend(rollout_data_dto.defender_fourth_stop_step)
        self.episode_snort_severe_baseline_first_stop_step.extend(rollout_data_dto.episode_snort_severe_baseline_first_stop_step)
        self.episode_snort_warning_baseline_first_stop_step.extend(rollout_data_dto.episode_snort_warning_baseline_first_stop_step)
        self.episode_snort_critical_baseline_first_stop_step.extend(rollout_data_dto.episode_snort_critical_baseline_first_stop_step)
        self.episode_var_log_baseline_first_stop_step.extend(rollout_data_dto.episode_var_log_baseline_first_stop_step)
        self.episode_step_baseline_first_stop_step.extend(rollout_data_dto.episode_step_baseline_first_stop_step)
        self.episode_snort_severe_baseline_second_stop_step.extend(rollout_data_dto.episode_snort_severe_baseline_second_stop_step)
        self.episode_snort_warning_baseline_second_stop_step.extend(rollout_data_dto.episode_snort_warning_baseline_second_stop_step)
        self.episode_snort_critical_baseline_second_stop_step.extend(rollout_data_dto.episode_snort_critical_baseline_second_stop_step)
        self.episode_var_log_baseline_second_stop_step.extend(rollout_data_dto.episode_var_log_baseline_second_stop_step)
        self.episode_step_baseline_second_stop_step.extend(rollout_data_dto.episode_step_baseline_second_stop_step)
        self.episode_snort_severe_baseline_third_stop_step.extend(rollout_data_dto.episode_snort_severe_baseline_third_stop_step)
        self.episode_snort_warning_baseline_third_stop_step.extend(rollout_data_dto.episode_snort_warning_baseline_third_stop_step)
        self.episode_snort_critical_baseline_third_stop_step.extend(rollout_data_dto.episode_snort_critical_baseline_third_stop_step)
        self.episode_var_log_baseline_third_stop_step.extend(rollout_data_dto.episode_var_log_baseline_third_stop_step)
        self.episode_step_baseline_third_stop_step.extend(rollout_data_dto.episode_step_baseline_third_stop_step)
        self.episode_snort_severe_baseline_fourth_stop_step.extend(rollout_data_dto.episode_snort_severe_baseline_fourth_stop_step)
        self.episode_snort_warning_baseline_fourth_stop_step.extend(rollout_data_dto.episode_snort_warning_baseline_fourth_stop_step)
        self.episode_snort_critical_baseline_fourth_stop_step.extend(rollout_data_dto.episode_snort_critical_baseline_fourth_stop_step)
        self.episode_var_log_baseline_fourth_stop_step.extend(rollout_data_dto.episode_var_log_baseline_fourth_stop_step)
        self.episode_step_baseline_fourth_stop_step.extend(rollout_data_dto.episode_step_baseline_fourth_stop_step)
        self.episode_snort_severe_baseline_stops_remaining.extend(rollout_data_dto.episode_snort_severe_baseline_stops_remaining)
        self.episode_snort_warning_baseline_stops_remaining.extend(rollout_data_dto.episode_snort_warning_baseline_stops_remaining)
        self.episode_snort_critical_baseline_stops_remaining.extend(rollout_data_dto.episode_snort_critical_baseline_stops_remaining)
        self.episode_var_log_baseline_stops_remaining.extend(rollout_data_dto.episode_var_log_baseline_stops_remaining)
        self.episode_step_baseline_stops_remaining.extend(rollout_data_dto.episode_step_baseline_stops_remaining)
        self.optimal_stops_remaining.extend(rollout_data_dto.optimal_stops_remaining)
        self.optimal_first_stop_step.extend(rollout_data_dto.optimal_first_stop_step)
        self.optimal_second_stop_step.extend(rollout_data_dto.optimal_second_stop_step)
        self.optimal_third_stop_step.extend(rollout_data_dto.optimal_third_stop_step)
        self.optimal_fourth_stop_step.extend(rollout_data_dto.optimal_fourth_stop_step)
        self.optimal_defender_episode_steps.extend(rollout_data_dto.optimal_defender_episode_steps)

        for key in rollout_data_dto.attacker_env_specific_rewards.keys():
            if key in self.attacker_train_episode_env_specific_rewards:
                self.attacker_train_episode_env_specific_rewards[key].extend(
                    rollout_data_dto.attacker_env_specific_rewards[key])
            else:
                self.attacker_train_episode_env_specific_rewards[key] = \
                rollout_data_dto.attacker_env_specific_rewards[key]
        for key in rollout_data_dto.defender_env_specific_rewards.keys():
            if key in self.defender_train_episode_env_specific_rewards:
                self.defender_train_episode_env_specific_rewards[key].extend(
                    rollout_data_dto.defender_env_specific_rewards[key])
            else:
                self.defender_train_episode_env_specific_rewards[key] = \
                rollout_data_dto.defender_env_specific_rewards[key]
        for key in rollout_data_dto.env_specific_steps.keys():
            if key in self.train_env_specific_steps:
                self.train_env_specific_steps[key].extend(rollout_data_dto.env_specific_steps[key])
            else:
                self.train_env_specific_steps[key] = rollout_data_dto.env_specific_steps[key]
        for key in rollout_data_dto.env_specific_flags.keys():
            if key in self.train_env_specific_flags:
                self.train_env_specific_flags[key].extend(rollout_data_dto.env_specific_flags[key])
            else:
                self.train_env_specific_flags[key] = rollout_data_dto.env_specific_flags[key]
        for key in self.train_env_specific_flags_percentage.keys():
            if key in self.train_env_specific_flags_percentage:
                self.train_env_specific_flags_percentage[key].extend(rollout_data_dto.env_specific_flags_percentage[key])
            else:
                self.train_env_specific_flags_percentage[key] = rollout_data_dto.env_specific_flags_percentage[key]



    def get_avg_attacker_dto(self, attacker_agent_config: AgentConfig, env: PyCRCTFEnv, env_2: PyCRCTFEnv, eval : bool):
        """
        Returns a DTO where all of the attacker metrics are averaged

        :param attacker_agent_config: the training configuration
        :param env: the training environment
        :param env_2: the evaluation environment
        :param eval: a boolean flag whether it is an evaluation episode or not
        :return: the DTO with the average metrics
        """
        return AttackerTrainAgentLogDTOAvg(train_log_dto=self,
                                    attacker_agent_config=attacker_agent_config,
                                    env=env, env_2=env_2, eval=eval)

    def get_avg_defender_dto(self, defender_agent_config: AgentConfig, env: PyCRCTFEnv, env_2: PyCRCTFEnv, eval : bool,
                             train_mode: TrainMode):
        """
        Returns a DTO where all of the defender metrics are averaged

        :param defender_agent_config: the training configuration
        :param env: the training environment
        :param env_2: the evaluation environment
        :param eval: a boolean flag whether it is an evaluation episode or not
        :param train_mode: the training mode
        :return: the DTO with the averaged metrics
        """
        return DefenderTrainAgentLogDTOAvg(
            train_log_dto=self, defender_agent_config=defender_agent_config, env=env, env_2=env_2, eval=eval,
            train_mode=train_mode)