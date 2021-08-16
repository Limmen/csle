from gym_pycr_ctf.agents.config.agent_config import AgentConfig

class RolloutDataDTO:
    """
    DTO with information from rollout in the env
    """
    def __init__(self, attacker_episode_rewards = None, defender_episode_rewards = None, episode_steps = None,
                 episode_flags = None, episode_caught = None, episode_early_stopped = None,
                 episode_successful_intrusion = None,
                 episode_snort_severe_baseline_rewards = None,
                 episode_snort_warning_baseline_rewards = None,
                 episode_snort_critical_baseline_rewards = None,
                 episode_var_log_baseline_rewards = None,
                 episode_step_baseline_rewards=None,
                 episode_snort_severe_baseline_steps=None,
                 episode_snort_warning_baseline_steps=None,
                 episode_snort_critical_baseline_steps=None,
                 episode_var_log_baseline_steps=None,
                 episode_step_baseline_steps=None,
                 episode_snort_severe_baseline_caught_attacker=None,
                 episode_snort_warning_baseline_caught_attacker=None,
                 episode_snort_critical_baseline_caught_attacker=None,
                 episode_var_log_baseline_caught_attacker=None,
                 episode_step_baseline_caught_attacker=None,
                 episode_snort_severe_baseline_early_stopping=None,
                 episode_snort_warning_baseline_early_stopping=None,
                 episode_snort_critical_baseline_early_stopping=None,
                 episode_var_log_baseline_early_stopping=None,
                 episode_step_baseline_early_stopping=None,
                 episode_snort_severe_baseline_uncaught_intrusion_steps=None,
                 episode_snort_warning_baseline_uncaught_intrusion_steps=None,
                 episode_snort_critical_baseline_uncaught_intrusion_steps=None,
                 episode_var_log_baseline_uncaught_intrusion_steps=None,
                 episode_step_baseline_uncaught_intrusion_steps=None,
                 episode_flags_percentage = None,
                 attacker_env_specific_rewards = None,
                 defender_env_specific_rewards = None,
                 env_specific_steps = None,
                 env_specific_flags = None,
                 env_specific_flags_percentage = None,
                 env_response_times = None,
                 action_pred_times = None,
                 attacker_action_costs = None,
                 attacker_action_costs_norm=None,
                 attacker_action_alerts=None,
                 attacker_action_alerts_norm=None,
                 episode_intrusion_steps = None,
                 uncaught_intrusion_steps=None,
                 optimal_defender_reward=None
                 ):
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

    def initialize(self):
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
