import time
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

import gym
import numpy as np
import torch as th

from gym_pycr_ctf.agents.openai_baselines.common.buffers import RolloutBuffer, RolloutBufferAR
from gym_pycr_ctf.agents.openai_baselines.common.type_aliases import GymEnv, MaybeCallback
from gym_pycr_ctf.agents.openai_baselines.common.vec_env import VecEnv
from gym_pycr_ctf.agents.openai_baselines.common.callbacks import BaseCallback
from gym_pycr_ctf.agents.openai_baselines.common.base_class import BaseAlgorithm
from gym_pycr_ctf.agents.openai_baselines.common.policies import ActorCriticPolicy
from gym_pycr_ctf.agents.config.agent_config import AgentConfig
from gym_pycr_ctf.agents.openai_baselines.common.evaluation import quick_evaluate_policy
from gym_pycr_ctf.agents.openai_baselines.common.vec_env.dummy_vec_env import DummyVecEnv
from gym_pycr_ctf.agents.openai_baselines.common.vec_env.subproc_vec_env import SubprocVecEnv
from gym_pycr_ctf.dao.agent.train_mode import TrainMode
from gym_pycr_ctf.envs_model.util.eval_util import EvalUtil
from gym_pycr_ctf.dao.agent.train_agent_log_dto import TrainAgentLogDTO
from gym_pycr_ctf.dao.agent.rollout_data_dto import RolloutDataDTO


class OnPolicyAlgorithm(BaseAlgorithm):
    """
    The base for On-Policy algorithms (ex: A2C/PPO).

    :param attacker_policy: (ActorCriticPolicy or str) The policy model to use (MlpPolicy, CnnPolicy, ...)
    :param defender_policy: (ActorCriticPolicy or str) The policy model to use (MlpPolicy, CnnPolicy, ...)
    :param env: (Gym environment or str) The environment to learn from (if registered in Gym, can be str)
    :param attacker_learning_rate: (float or callable) The learning rate, it can be a function
        of the current progress remaining (from 1 to 0)
    :param n_steps: (int) The number of steps to run for each environment per update
        (i.e. batch size is n_steps * n_env where n_env is number of environment copies running in parallel)
    :param attacker_gamma: (float) Discount factor
    :param attacker_gae_lambda: (float) Factor for trade-off of bias vs variance for Generalized Advantage Estimator.
        Equivalent to classic advantage when set to 1.
    :param attacker_ent_coef: (float) Entropy coefficient for the loss calculation
    :param attacker_vf_coef: (float) Value function coefficient for the loss calculation
    :param attacker_max_grad_norm: (float) The maximum value for the gradient clipping
    :param tensorboard_log: (str) the log location for tensorboard (if None, no logging)
    :param create_eval_env: (bool) Whether to create a second environment that will be
        used for evaluating the agent periodically. (Only available when passing string for the environment)
    :param monitor_wrapper: When creating an environment, whether to wrap it
        or not in a Monitor wrapper.
    :param attacker_policy_kwargs: (dict) additional arguments to be passed to the policy on creation
    :param verbose: (int) the verbosity level: 0 no output, 1 info, 2 debug
    :param seed: (int) Seed for the pseudo random generators
    :param device: (str or th.device) Device (cpu, cuda, ...) on which the code should be run.
        Setting it to auto, the code will be run on the GPU if possible.
    :param _init_setup_model: (bool) Whether or not to build the network at the creation of the instance
    """

    def __init__(
        self,
        attacker_policy: Union[str, Type[ActorCriticPolicy]],
        defender_policy: Union[str, Type[ActorCriticPolicy]],
        env: Union[GymEnv, str],
        attacker_learning_rate: Union[float, Callable],
        defender_learning_rate: Union[float, Callable],
        n_steps: int,
        attacker_gamma: float,
        defender_gamma: float,
        attacker_gae_lambda: float,
        defender_gae_lambda: float,
        attacker_ent_coef: float,
        defender_ent_coef: float,
        attacker_vf_coef: float,
        defender_vf_coef: float,
        attacker_max_grad_norm: float,
        defender_max_grad_norm: float,
        create_eval_env: bool = False,
        attacker_policy_kwargs: Optional[Dict[str, Any]] = None,
        defender_policy_kwargs: Optional[Dict[str, Any]] = None,
        verbose: int = 0,
        seed: Optional[int] = None,
        device: Union[th.device, str] = "auto",
        _init_setup_model: bool = True,
        attacker_agent_config: AgentConfig = None,
        defender_agent_config: AgentConfig = None,
        env_2: Union[GymEnv, str] = None,
        train_mode: TrainMode = TrainMode.TRAIN_ATTACKER
    ):

        super(OnPolicyAlgorithm, self).__init__(
            attacker_policy=attacker_policy,
            defender_policy=defender_policy,
            env=env,
            attacker_policy_base=ActorCriticPolicy,
            defender_policy_base=ActorCriticPolicy,
            attacker_learning_rate=attacker_learning_rate,
            defender_learning_rate=defender_learning_rate,
            attacker_policy_kwargs=attacker_policy_kwargs,
            defender_policy_kwargs=defender_policy_kwargs,
            verbose=verbose,
            device=device,
            create_eval_env=create_eval_env,
            support_multi_env=True,
            seed=seed,
            attacker_agent_config = attacker_agent_config,
            defender_agent_config=defender_agent_config,
            env_2=env_2,
            train_mode=train_mode
        )

        self.n_steps = n_steps
        self.attacker_gamma = attacker_gamma
        self.defender_gamma = defender_gamma
        self.attacker_gae_lambda = attacker_gae_lambda
        self.defender_gae_lambda = defender_gae_lambda
        self.attacker_ent_coef = attacker_ent_coef
        self.defender_ent_coef = defender_ent_coef
        self.attacker_vf_coef = attacker_vf_coef
        self.defender_vf_coef = defender_vf_coef
        self.attacker_max_grad_norm = attacker_max_grad_norm
        self.defender_max_grad_norm = defender_max_grad_norm
        self.attacker_rollout_buffer = None
        self.defender_rollout_buffer = None
        self.iteration = 0
        self.num_episodes = 0
        self.num_episodes_total = 0

        self.saved_log_dto = TrainAgentLogDTO()
        self.saved_log_dto.initialize()

        if _init_setup_model:
            self._setup_model()

    def _setup_model(self) -> None:
        self._setup_lr_schedule()
        self.set_random_seed(self.seed)

        if not self.attacker_agent_config.ar_policy:
            self.attacker_rollout_buffer = RolloutBuffer(
                self.n_steps,
                self.attacker_observation_space,
                self.attacker_action_space,
                self.device,
                gamma=self.attacker_gamma,
                gae_lambda=self.attacker_gae_lambda,
                n_envs=self.n_envs,
            )
        else:
            self.attacker_rollout_buffer = RolloutBufferAR(
                self.n_steps,
                self.attacker_observation_space,
                self.attacker_action_space,
                self.device,
                gamma=self.attacker_gamma,
                gae_lambda=self.attacker_gae_lambda,
                n_envs=self.n_envs,
                attacker_agent_config = self.attacker_agent_config
            )

        self.defender_rollout_buffer = RolloutBuffer(
            self.n_steps,
            self.defender_observation_space,
            self.defender_action_space,
            self.device,
            gamma=self.defender_gamma,
            gae_lambda=self.defender_gae_lambda,
            n_envs=self.n_envs,
        )

        if not hasattr(self.attacker_agent_config, 'ar_policy2') or not self.attacker_agent_config.ar_policy2:
            self.attacker_policy = self.attacker_policy_class(
                self.attacker_observation_space,
                self.attacker_action_space,
                self.attacker_lr_schedule,
                agent_config = self.attacker_agent_config,
                **self.attacker_policy_kwargs  # pytype:disable=not-instantiable
            )
            self.attacker_policy = self.attacker_policy.to(self.device)
        else:
            self.m_selection_policy = self.attacker_policy_class(
                self.env.envs[0].attacker_m_selection_observation_space,
                self.env.envs[0].attacker_m_selection_action_space,
                self.attacker_lr_schedule,
                agent_config=self.attacker_agent_config,
                m_selection = True,
                **self.attacker_policy_kwargs  # pytype:disable=not-instantiable
            )
            self.m_selection_policy = self.m_selection_policy.to(self.device)
            self.m_action_policy = self.attacker_policy_class(
                self.env.envs[0].attacker_m_action_observation_space,
                self.env.envs[0].attacker_m_action_space,
                self.attacker_lr_schedule,
                agent_config=self.attacker_agent_config,
                m_action = True,
                **self.attacker_policy_kwargs  # pytype:disable=not-instantiable
            )
            self.m_action_policy = self.m_action_policy.to(self.device)

        self.defender_policy = self.defender_policy_class(
            self.defender_observation_space,
            self.defender_action_space,
            self.defender_lr_schedule,
            agent_config=self.defender_agent_config,
            **self.attacker_policy_kwargs  # pytype:disable=not-instantiable
        )
        self.defender_policy = self.defender_policy.to(self.device)

    def collect_rollouts(
        self, env: VecEnv, callback: BaseCallback, attacker_rollout_buffer: RolloutBuffer,
            defender_rollout_buffer: RolloutBuffer,
            n_rollout_steps: int
    ) -> Union[bool, RolloutDataDTO]:
        """
        Collect rollouts using the current policy and fill a `RolloutBuffer`.

        :param env: (VecEnv) The training environment
        :param callback: (BaseCallback) Callback that will be called at each step
            (and at the beginning and end of the rollout)
        :param attacker_rollout_buffer: (RolloutBuffer) Buffer to fill with rollouts
        :param n_steps: (int) Number of experiences to collect per environment
        :return: (bool) True if function returned with at least `n_rollout_steps`
            collected, False if callback terminated rollout prematurely.
        """
        assert self._last_obs is not None, "No previous observation was provided"
        n_steps = 0

        # Reset rollout buffers
        attacker_rollout_buffer.reset()
        defender_rollout_buffer.reset()

        # Avg metrics
        rollout_data_dto = RolloutDataDTO()
        rollout_data_dto.initialize()

        # Per episode metrics
        episode_reward_attacker = np.zeros(env.num_envs)
        episode_reward_defender = np.zeros(env.num_envs)
        episode_step = np.zeros(env.num_envs)
        env_response_time = 0
        action_pred_time = 0

        callback.on_rollout_start()
        dones = False
        while n_steps < n_rollout_steps:


            if not self.attacker_agent_config.ar_policy:
                new_obs, attacker_rewards, dones, infos, attacker_values, attacker_log_probs, attacker_actions, \
                action_pred_time_s, env_step_time, defender_values, defender_log_probs, defender_actions, \
                defender_rewards = \
                    self.step_policy(env, attacker_rollout_buffer, defender_rollout_buffer)

                if self.attacker_agent_config.performance_analysis:
                    env_response_time += env_step_time
                    action_pred_time += action_pred_time_s
            else:
                new_obs, machine_obs, attacker_rewards, dones, infos, m_selection_values, m_action_values, m_selection_log_probs, \
                m_action_log_probs, m_selection_actions, m_actions = self.step_policy_ar(env, attacker_rollout_buffer)

            # Record step metrics
            self.num_timesteps += env.num_envs
            self._update_info_buffer(infos)
            n_steps += 1
            episode_reward_attacker += attacker_rewards
            episode_reward_defender += defender_rewards
            episode_step += 1
            if dones.any():
                for i in range(len(list(filter(lambda x: x, dones)))):
                    if dones[i]:
                        # Record episode metrics
                        self.num_episodes += 1
                        self.num_episodes_total += 1
                        rollout_data_dto.attacker_episode_rewards.append(episode_reward_attacker[i])
                        rollout_data_dto.defender_episode_rewards.append(episode_reward_defender[i])
                        rollout_data_dto.episode_steps.append(episode_step[i])
                        rollout_data_dto.episode_flags.append(infos[i]["flags"])
                        rollout_data_dto.episode_caught.append(infos[i]["caught_attacker"])
                        rollout_data_dto.episode_early_stopped.append(infos[i]["early_stopped"])
                        rollout_data_dto.episode_successful_intrusion.append(infos[i]["successful_intrusion"])
                        rollout_data_dto.episode_snort_severe_baseline_rewards.append(infos[i]["snort_severe_baseline_reward"])
                        rollout_data_dto.episode_snort_warning_baseline_rewards.append(infos[i]["snort_warning_baseline_reward"])
                        rollout_data_dto.episode_snort_critical_baseline_rewards.append(infos[i]["snort_critical_baseline_reward"])
                        rollout_data_dto.episode_var_log_baseline_rewards.append(infos[i]["var_log_baseline_reward"])
                        rollout_data_dto.attacker_action_costs.append(infos[i]["attacker_cost"])
                        rollout_data_dto.attacker_action_costs_norm.append(infos[i]["attacker_cost_norm"])
                        rollout_data_dto.attacker_action_alerts.append(infos[i]["attacker_alerts"])
                        rollout_data_dto.attacker_action_alerts_norm.append(infos[i]["attacker_alerts_norm"])
                        if self.attacker_agent_config.env_config is not None:
                            rollout_data_dto.episode_flags_percentage.append(
                                infos[i]["flags"] / self.attacker_agent_config.env_config.num_flags
                            ) # TODO this does not work with DR
                        else:
                            print("env config None?:{}".format(self.attacker_agent_config.env_config))
                            rollout_data_dto.episode_flags_percentage.append(
                                infos[i]["flags"] / self.attacker_agent_config.env_configs[infos[i]["idx"]].num_flags)

                        if self.attacker_agent_config.performance_analysis:
                            rollout_data_dto.env_response_times.append(env_response_time)
                            rollout_data_dto.action_pred_times.append(action_pred_time)
                            env_response_time = 0
                            action_pred_time = 0

                        rollout_data_dto.update_env_specific_metrics(infos=infos, i=i,
                                                                     agent_config=self.attacker_agent_config)
                        episode_reward_attacker[i] = 0
                        episode_reward_defender[i] = 0
                        episode_step[i] = 0

        if not self.attacker_agent_config.ar_policy:
            if self.train_mode == TrainMode.TRAIN_ATTACKER or self.train_mode == TrainMode.SELF_PLAY:
                attacker_rollout_buffer.compute_returns_and_advantage(attacker_values, dones=dones)
            if self.train_mode == TrainMode.TRAIN_DEFENDER or self.train_mode == TrainMode.SELF_PLAY:
                defender_rollout_buffer.compute_returns_and_advantage(defender_values, dones=dones)
        else:
            attacker_rollout_buffer.compute_returns_and_advantage(m_selection_values, dones=dones, machine_action = False)
            attacker_rollout_buffer.compute_returns_and_advantage(m_action_values, dones=dones, machine_action=True)

        callback.on_rollout_end()
        for i in range(len(dones)):
            if not dones[i]:
                rollout_data_dto.attacker_episode_rewards.append(episode_reward_attacker[i])
                rollout_data_dto.defender_episode_rewards.append(episode_reward_defender[i])
                rollout_data_dto.episode_steps.append(episode_step[i])
        return True, rollout_data_dto

    def train(self) -> None:
        """
        Consume current rollout data and update policy parameters.
        Implemented by individual algorithms.
        """
        raise NotImplementedError

    def learn(
        self,
        total_timesteps: int,
        callback: MaybeCallback = None,
        log_interval: int = 1,
        eval_env: Optional[GymEnv] = None,
        eval_env_2: Optional[GymEnv] = None,
        eval_freq: int = -1,
        n_eval_episodes: int = 5,
        tb_log_name: str = "OnPolicyAlgorithm",
        eval_log_path: Optional[str] = None,
        reset_num_timesteps: bool = True,
    ) -> "OnPolicyAlgorithm":

        if self.attacker_agent_config is not None and self.attacker_agent_config.logger is not None:
            self.attacker_agent_config.logger.info("Setting up Training Configuration")
        if self.defender_agent_config is not None and self.defender_agent_config.logger is not None:
            self.defender_agent_config.logger.info("Setting up Training Configuration")

        print("Setting up Training Configuration")

        self.iteration = 0
        total_timesteps, callback = self._setup_learn(
            total_timesteps, eval_env, eval_env_2, callback, eval_freq, n_eval_episodes, eval_log_path,
            reset_num_timesteps, tb_log_name
        )

        callback.on_training_start(locals(), globals())
        if self.attacker_agent_config is not None and self.attacker_agent_config.logger is not None:
            self.attacker_agent_config.logger.info("Starting training, max time steps:{}".format(total_timesteps))
            self.attacker_agent_config.logger.info(self.attacker_agent_config.to_str())
        if self.defender_agent_config is not None and self.defender_agent_config.logger is not None:
            self.defender_agent_config.logger.info("Starting training, max time steps:{}".format(total_timesteps))
            self.defender_agent_config.logger.info(self.attacker_agent_config.to_str())

        # Tracking metrics
        train_log_dto = TrainAgentLogDTO()
        train_log_dto.initialize()
        train_log_dto.train_result = self.train_result
        train_log_dto.eval_result = self.eval_result
        train_log_dto.iteration = self.iteration
        train_log_dto.start_time = self.training_start

        num_iterations = self.attacker_agent_config.num_iterations
        if self.train_mode == TrainMode.TRAIN_DEFENDER:
            num_iterations = self.defender_agent_config.num_iterations

        while self.iteration < num_iterations:

            if self.attacker_agent_config.performance_analysis:
                start = time.time()

            continue_training, rollout_data_dto = \
                self.collect_rollouts(self.env, callback, self.attacker_rollout_buffer,
                                      self.defender_rollout_buffer,
                                      n_rollout_steps=self.n_steps)

            if self.attacker_agent_config.performance_analysis:
                end = time.time()
                train_log_dto.rollout_times.append(end-start)
                train_log_dto.env_response_times.extend(rollout_data_dto.env_response_times)
                train_log_dto.action_pred_times.extend(rollout_data_dto.action_pred_times)

            train_log_dto.attacker_episode_rewards.extend(rollout_data_dto.attacker_episode_rewards)
            train_log_dto.defender_episode_rewards.extend(rollout_data_dto.defender_episode_rewards)
            train_log_dto.episode_steps.extend(rollout_data_dto.episode_steps)
            train_log_dto.episode_flags.extend(rollout_data_dto.episode_flags)
            train_log_dto.episode_caught.extend(rollout_data_dto.episode_caught)
            train_log_dto.episode_successful_intrusion.extend(rollout_data_dto.episode_successful_intrusion)
            train_log_dto.episode_early_stopped.extend(rollout_data_dto.episode_early_stopped)
            train_log_dto.episode_flags_percentage.extend(rollout_data_dto.episode_flags_percentage)
            train_log_dto.episode_snort_severe_baseline_rewards.extend(rollout_data_dto.episode_snort_severe_baseline_rewards)
            train_log_dto.episode_snort_warning_baseline_rewards.extend(rollout_data_dto.episode_snort_warning_baseline_rewards)
            train_log_dto.episode_snort_critical_baseline_rewards.extend(rollout_data_dto.episode_snort_critical_baseline_rewards)
            train_log_dto.episode_var_log_baseline_rewards.extend(rollout_data_dto.episode_var_log_baseline_rewards)
            train_log_dto.attacker_action_costs.extend(rollout_data_dto.attacker_action_costs)
            train_log_dto.attacker_action_costs_norm.extend(rollout_data_dto.attacker_action_costs_norm)
            train_log_dto.attacker_action_alerts.extend(rollout_data_dto.attacker_action_alerts)
            train_log_dto.attacker_action_alerts_norm.extend(rollout_data_dto.attacker_action_alerts_norm)

            for key in rollout_data_dto.attacker_env_specific_rewards.keys():
                if key in train_log_dto.attacker_train_episode_env_specific_rewards:
                    train_log_dto.attacker_train_episode_env_specific_rewards[key].extend(rollout_data_dto.attacker_env_specific_rewards[key])
                else:
                    train_log_dto.attacker_train_episode_env_specific_rewards[key] = rollout_data_dto.attacker_env_specific_rewards[key]
            for key in rollout_data_dto.defender_env_specific_rewards.keys():
                if key in train_log_dto.defender_train_episode_env_specific_rewards:
                    train_log_dto.defender_train_episode_env_specific_rewards[key].extend(rollout_data_dto.defender_env_specific_rewards[key])
                else:
                    train_log_dto.defender_train_episode_env_specific_rewards[key] = rollout_data_dto.defender_env_specific_rewards[key]
            for key in rollout_data_dto.env_specific_steps.keys():
                if key in train_log_dto.train_env_specific_steps:
                    train_log_dto.train_env_specific_steps[key].extend(rollout_data_dto.env_specific_steps[key])
                else:
                    train_log_dto.train_env_specific_steps[key] = rollout_data_dto.env_specific_steps[key]
            for key in rollout_data_dto.env_specific_flags.keys():
                if key in train_log_dto.train_env_specific_flags:
                    train_log_dto.train_env_specific_flags[key].extend(rollout_data_dto.env_specific_flags[key])
                else:
                    train_log_dto.train_env_specific_flags[key] = rollout_data_dto.env_specific_flags[key]
            for key in train_log_dto.train_env_specific_flags_percentage.keys():
                if key in train_log_dto.train_env_specific_flags_percentage:
                    train_log_dto.train_env_specific_flags_percentage[key].extend(rollout_data_dto.env_specific_flags_percentage[key])
                else:
                    train_log_dto.train_env_specific_flags_percentage[key] = rollout_data_dto.env_specific_flags_percentage[key]

            if continue_training is False:
                break

            self.iteration += 1
            train_log_dto.iteration = self.iteration
            callback.iteration += 1
            self._update_current_progress_remaining(self.num_timesteps, total_timesteps)

            if self.iteration % self.attacker_agent_config.quick_eval_freq == 0 or self.iteration == 1:
                env2 = self.env_2
            else:
                env2 = None

            if self.iteration % self.attacker_agent_config.train_log_frequency == 0 or self.iteration == 1:

                if self.attacker_agent_config.train_progress_deterministic_eval:
                    eval_conf = self.attacker_agent_config.env_config
                    env_configs = self.attacker_agent_config.env_configs
                    eval_env_configs = self.attacker_agent_config.eval_env_configs
                    if self.attacker_agent_config.domain_randomization:
                        if isinstance(self.env, DummyVecEnv):
                            eval_conf = self.env.env_config(0)
                            env_configs = self.env.env_configs()
                        if self.eval_env is not None:
                            eval_env_configs = self.eval_env.env_config
                    if self.attacker_agent_config.eval_env_config is not None:
                        eval_conf = self.attacker_agent_config.eval_env_config
                        if self.attacker_agent_config.domain_randomization:
                            if isinstance(self.env, DummyVecEnv):
                                eval_conf = self.eval_env.env_config(0)
                    if self.defender_agent_config is not None and self.defender_agent_config.static_eval_defender:
                        env2 = None
                    train_log_dto = quick_evaluate_policy(attacker_model=self.attacker_policy,
                                              defender_model=self.defender_policy,
                                              env=self.env,
                                              n_eval_episodes_train=self.attacker_agent_config.n_deterministic_eval_iter,
                                              n_eval_episodes_eval2=self.attacker_agent_config.n_quick_eval_iter,
                                              deterministic=self.attacker_agent_config.eval_deterministic,
                                              attacker_agent_config=self.attacker_agent_config,
                                              defender_agent_config=self.defender_agent_config,
                                              env_config=eval_conf, env_2=env2,
                                              env_configs=env_configs,
                                              eval_env_config=eval_conf,
                                              eval_envs_configs=eval_env_configs,
                                              train_mode = self.train_mode,
                                              train_dto=train_log_dto
                                              )
                    if env2 is not None:
                        self.saved_log_dto = train_log_dto.copy()
                    else:
                        train_log_dto.copy_saved_env_2(self.saved_log_dto)

                    if self.defender_agent_config is not None and self.defender_agent_config.static_eval_defender:
                        eval_2_defender_episode_rewards, eval_2_episode_steps, \
                        eval_2_episode_snort_severe_baseline_rewards, eval_2_episode_snort_warning_baseline_rewards, \
                        eval_2_episode_snort_critical_baseline_rewards, \
                        eval_2_episode_var_log_baseline_rewards, eval_2_flags_list, eval_2_flags_percentage_list, \
                        eval_2_episode_caught_list, eval_2_episode_early_stopped_list, \
                        eval_2_episode_successful_intrusion_list, eval_2_attacker_cost_list, \
                        eval_2_attacker_cost_norm_list, \
                        eval_2_attacker_alerts_list, eval_2_attacker_alerts_norm_list = \
                            EvalUtil.eval_defender(self.env.envs[0], self,
                                                   deterministic=self.attacker_agent_config.eval_deterministic)

                        train_log_dto.defender_eval_2_episode_rewards = eval_2_defender_episode_rewards
                        train_log_dto.eval_2_episode_steps = eval_2_episode_steps
                        train_log_dto.eval_2_episode_snort_severe_baseline_rewards = eval_2_episode_snort_severe_baseline_rewards
                        train_log_dto.eval_2_episode_snort_warning_baseline_rewards = eval_2_episode_snort_warning_baseline_rewards
                        train_log_dto.eval_2_episode_snort_critical_baseline_rewards = eval_2_episode_snort_critical_baseline_rewards
                        train_log_dto.eval_2_episode_var_log_baseline_rewards= eval_2_episode_var_log_baseline_rewards
                        train_log_dto.eval_2_episode_flags = eval_2_flags_list
                        train_log_dto.eval_2_episode_flags_percentage = eval_2_flags_percentage_list
                        train_log_dto.eval_2_episode_caught = eval_2_episode_caught_list
                        train_log_dto.eval_2_episode_early_stopped = eval_2_episode_early_stopped_list
                        train_log_dto.eval_2_episode_successful_intrusion = eval_2_episode_successful_intrusion_list
                        train_log_dto.eval_2_attacker_action_costs = eval_2_attacker_cost_list
                        train_log_dto.eval_2_attacker_action_costs_norm = eval_2_attacker_cost_norm_list
                        train_log_dto.eval_2_attacker_action_alerts = eval_2_attacker_alerts_list
                        train_log_dto.eval_2_attacker_action_alerts_norm = eval_2_attacker_alerts_norm_list

                    d = {}
                    if isinstance(self.env, SubprocVecEnv):
                        for i in range(self.env.num_envs):
                            self.env.eval_reset(i)
                            self._last_infos[i]["attacker_non_legal_actions"] = self.env.attacker_initial_illegal_actions
                            self._last_infos[i]["defender_non_legal_actions"] = self.env.defender_initial_illegal_actions
                n_af, n_d = 0,0
                if isinstance(self.env, DummyVecEnv):
                    n_af = self.env.envs[0].attacker_agent_state.num_all_flags
                    n_d = self.env.envs[0].attacker_agent_state.num_detections
                train_log_dto.n_af = n_af
                train_log_dto.n_d = n_d
                if self.train_mode == TrainMode.TRAIN_ATTACKER or self.train_mode == TrainMode.SELF_PLAY:
                    train_log_dto = self.log_metrics_attacker(train_log_dto=train_log_dto, eval=False)
                if self.train_mode == TrainMode.TRAIN_DEFENDER or self.train_mode == TrainMode.SELF_PLAY:
                    train_log_dto = self.log_metrics_defender(train_log_dto=train_log_dto, eval=False)
                self.train_result = train_log_dto.train_result
                self.eval_result = train_log_dto.eval_result
                train_log_dto.initialize()
                train_log_dto.train_result = self.train_result
                train_log_dto.eval_result = self.eval_result
                train_log_dto.iteration = self.iteration
                train_log_dto.start_time = self.training_start
                self.num_episodes = 0

            # Save models every <self.config.checkpoint_frequency> iterations
            if self.iteration % self.attacker_agent_config.checkpoint_freq == 0:
                try:
                    self.save_model(self.iteration)
                except Exception as e:
                    print("There was an error saving the model: {}".format(str(e)))
                if self.attacker_agent_config.save_dir is not None:
                    time_str = str(time.time())
                    self.train_result.to_csv(
                        self.attacker_agent_config.save_dir + "/" + time_str + "_train_results_checkpoint.csv")
                    self.eval_result.to_csv(
                        self.attacker_agent_config.save_dir + "/" + time_str + "_eval_results_checkpoint.csv")

            if not self.attacker_agent_config.ar_policy:
                entropy_loss_attacker, pg_loss_attacker, value_loss_attacker, lr_attacker, grad_comp_times_attacker, \
                weight_update_times_attacker, \
                entropy_loss_defender, pg_loss_defender, value_loss_defender, lr_defedner, grad_comp_times_defender, \
                weight_update_times_defender = self.train()

                if self.attacker_agent_config.performance_analysis:
                    grad_comp_times_attacker.append(np.sum(grad_comp_times_attacker))
                    weight_update_times_attacker.append(np.sum(weight_update_times_attacker))
            else:
                entropy_loss_attacker, pg_loss_attacker, value_loss_attacker, lr_attacker = self.train_ar()
            train_log_dto.attacker_episode_avg_loss.append(entropy_loss_attacker + pg_loss_attacker + value_loss_attacker)
            train_log_dto.defender_episode_avg_loss.append(entropy_loss_defender + pg_loss_defender + value_loss_defender)

        callback.on_training_end()

        return self

    def get_torch_variables(self) -> Tuple[List[str], List[str]]:
        """
        cf base class
        """
        if not self.attacker_agent_config.ar_policy:
            state_dicts = ["attacker_policy", "attacker_policy.optimizer", "defender_policy",
                           "defender_policy.optimizer"]
        else:
            state_dicts = ["m_selection_policy", "m_selection_policy.optimizer",
                           "m_action_policy", "m_action_policy.optimizer"]

        return state_dicts, []


    def step_policy(self, env, attacker_rollout_buffer, defender_rollout_buffer):
        action_pred_time = 0.0
        env_step_time = 0.0
        if self.attacker_agent_config.performance_analysis:
            start = time.time()

        with th.no_grad():
            # Convert to pytorch tensor
            if isinstance(self._last_obs, tuple):
                attacker_obs, defender_obs = self._last_obs
            else:
                attacker_obs = []
                defender_obs = []
                for i in range(len(self._last_obs)):
                    attacker_obs.append(self._last_obs[i][0])
                    defender_obs.append(self._last_obs[i][1])
                attacker_obs = np.array(attacker_obs)
                defender_obs = np.array(defender_obs)
                attacker_obs = attacker_obs.astype("float64")
                defender_obs = defender_obs.astype("float64")
            obs_tensor_attacker = th.as_tensor(attacker_obs).to(self.device)
            obs_tensor_defender = th.as_tensor(defender_obs).to(self.device)
            attacker_actions = None
            attacker_values = None
            attacker_log_probs = None
            defender_actions = None
            defender_values = None
            defender_log_probs = None
            if self.train_mode == TrainMode.TRAIN_ATTACKER or self.train_mode == TrainMode.SELF_PLAY:
                print("obs tensor attacker shape:{}".format(obs_tensor_attacker.shape))
                attacker_actions, attacker_values, attacker_log_probs = \
                    self.attacker_policy.forward(obs_tensor_attacker, env=env, infos=self._last_infos, attacker=True)
                attacker_actions = attacker_actions.cpu().numpy()
            if self.train_mode == TrainMode.TRAIN_DEFENDER or self.train_mode == TrainMode.SELF_PLAY:
                defender_actions, defender_values, defender_log_probs = \
                    self.defender_policy.forward(obs_tensor_defender, env=env, infos=self._last_infos,
                                                 attacker=False)
                defender_actions = defender_actions.cpu().numpy()

        if attacker_actions is None:
            attacker_actions = np.array([None]*len(defender_actions))

        if self.attacker_agent_config.performance_analysis:
            end = time.time()
            action_pred_time = end-start

        if defender_actions is None:
            defender_actions = np.array([None]*len(attacker_actions))

        # Perform action
        if self.attacker_agent_config.performance_analysis:
            start = time.time()

        actions = []
        for i in range(len(attacker_actions)):
            print("attacker actions len:{}, defender actions len:{}".format(len(attacker_actions), len(defender_actions)))
            actions.append((attacker_actions[i], defender_actions[i]))

        new_obs, rewards, dones, infos = env.step(actions)
        if self.attacker_agent_config.performance_analysis:
            end = time.time()
            env_step_time = end-start

        # if len(new_obs[0].shape) == 3:
        #     new_obs = new_obs.reshape((new_obs.shape[0], self.attacker_observation_space.shape[0]))

        if isinstance(self.attacker_action_space, gym.spaces.Discrete):
            # Reshape in case of discrete action
            attacker_actions = attacker_actions.reshape(-1, 1)

        if isinstance(self.defender_action_space, gym.spaces.Discrete):
            # Reshape in case of discrete action
            defender_actions = defender_actions.reshape(-1, 1)

        attacker_obs, defender_obs = self.get_attacker_and_defender_obs(self._last_obs)
        attacker_rewards, defender_rewards = self.get_attacker_and_defender_reward(rewards)
        if self.train_mode == TrainMode.TRAIN_ATTACKER or self.train_mode == TrainMode.SELF_PLAY:
            attacker_rollout_buffer.add(attacker_obs, attacker_actions, attacker_rewards, self._last_dones,
                                        attacker_values, attacker_log_probs)
        if self.train_mode == TrainMode.TRAIN_DEFENDER or self.train_mode == TrainMode.SELF_PLAY:
            defender_rollout_buffer.add(defender_obs, defender_actions, defender_rewards, self._last_dones,
                                        defender_values, defender_log_probs)

        print("new obs:{}".format(new_obs))
        print("new obs len:{}".format(len(new_obs)))
        print("new obs type:{}".format(type(new_obs)))
        self._last_obs = new_obs
        self._last_dones = dones
        self._last_infos = infos

        return new_obs, attacker_rewards, dones, infos, \
               attacker_values, attacker_log_probs, attacker_actions, action_pred_time, env_step_time, \
               defender_values, defender_log_probs, defender_actions, defender_rewards

    def step_policy_ar(self, env, rollout_buffer):
        with th.no_grad():
            # Convert to pytorch tensor
            network_obs_tensor = th.as_tensor(self._last_obs).to(self.device)
            m_selection_actions, m_selection_values, m_selection_log_probs = \
                self.m_selection_policy.forward(network_obs_tensor, env_config=env.envs[0].env_config,
                                                env_state=env.envs[0].env_state)
            m_selection_actions = m_selection_actions.cpu().numpy()
            network_obs_2 = network_obs_tensor.reshape((network_obs_tensor.shape[0], )
                                                       + self.env.envs[0].network_orig_shape)
            idx = m_selection_actions[0]
            if m_selection_actions[0] > 5:
                idx = 0
            machine_obs = network_obs_2[:, idx].reshape((network_obs_tensor.shape[0],) +
                                                                        self.env.envs[0].machine_orig_shape)
            machine_obs_tensor = th.as_tensor(machine_obs).to(self.device)
            m_actions, m_action_values, m_action_log_probs = \
                self.m_action_policy.forward(machine_obs_tensor, env_config=env.envs[0].env_config,
                                                env_state=env.envs[0].env_state, m_index=m_selection_actions[0])
            m_actions = m_actions.cpu().numpy()
            actions = env.envs[0].attacker_convert_ar_action(m_selection_actions[0], m_actions[0])
            actions = np.array([actions])

        new_obs, rewards, dones, infos = env.step(actions)

        if isinstance(self.env.envs[0].attacker_m_selection_action_space, gym.spaces.Discrete):
            # Reshape in case of discrete action
            m_selection_actions = m_selection_actions.reshape(-1, 1)
        
        if isinstance(self.env.envs[0].attacker_m_action_space, gym.spaces.Discrete):
            # Reshape in case of discrete action
            m_actions = m_actions.reshape(-1, 1)

        rollout_buffer.add(self._last_obs, machine_obs, m_selection_actions, m_actions, rewards, self._last_dones,
                           m_selection_values, m_action_values, m_selection_log_probs, m_action_log_probs)

        self._last_obs = new_obs
        self._last_dones = dones
        self._last_infos = infos

        return new_obs, machine_obs, rewards, dones, infos, m_selection_values, m_action_values, m_selection_log_probs, \
               m_action_log_probs, m_selection_actions, m_actions


    def get_attacker_and_defender_obs(self, obs):
        if isinstance(obs, tuple):
            return obs[0], obs[1]
        else:
            attacker_obs = []
            defender_obs = []
            for i in range(len(obs)):
                a_o = obs[i][0]
                d_o = obs[i][1]
                attacker_obs.append(a_o)
                defender_obs.append(d_o)
            attacker_obs = np.array(attacker_obs)
            defender_obs = np.array(defender_obs)
            attacker_obs = attacker_obs.astype("float64")
            defender_obs = defender_obs.astype("float64")
            return attacker_obs, defender_obs

    def get_attacker_and_defender_reward(self, rewards):
        if isinstance(rewards, tuple):
            return rewards[0], rewards[1]
        else:
            attacker_reward = []
            defender_reward = []
            for i in range(len(rewards)):
                a_r = rewards[i][0]
                d_r = rewards[i][1]
                attacker_reward.append(a_r)
                defender_reward.append(d_r)
            attacker_reward = np.array(attacker_reward)
            defender_reward = np.array(defender_reward)
            attacker_reward = attacker_reward.astype("float64")
            defender_reward = defender_reward.astype("float64")
            return attacker_reward, defender_reward
