from typing import Any, Callable, Dict, Optional, Type, Union
import time
import numpy as np
import torch as th
from gym import spaces
from torch.nn import functional as F

from pycr_common.dao.agent.base_train_agent_log_dto import BaseTrainAgentLogDTO
from pycr_common.dao.agent.base_rollout_data_dto import BaseRolloutDataDTO
from pycr_common.agents.openai_baselines.common.utils import explained_variance, get_schedule_fn
from pycr_common.agents.openai_baselines.common.type_aliases import GymEnv, MaybeCallback
from pycr_common.agents.openai_baselines.common.policies import ActorCriticPolicy
from pycr_common.agents.openai_baselines.common.on_policy_algorithm import OnPolicyAlgorithm
from pycr_common.agents.config.agent_config import AgentConfig
from pycr_common.dao.agent.train_mode import TrainMode
from pycr_common.envs_model.util.base_eval_util import BaseEvalUtil
from pycr_common.dao.experiment.base_experiment_result import BaseExperimentResult


class PPO(OnPolicyAlgorithm):
    """
    Proximal Policy Optimization algorithm (PPO) (clip version)

    Paper: https://arxiv.org/abs/1707.06347
    Code: This implementation borrows code from OpenAI Spinning Up (https://github.com/openai/spinningup/)
    https://github.com/ikostrikov/pytorch-a2c-ppo-acktr-gail and
    and Stable Baselines (PPO2 from https://github.com/hill-a/stable-baselines)

    Introduction to PPO: https://spinningup.openai.com/en/latest/algorithms/ppo.html

    :param attacker_policy: (ActorCriticPolicy or str) The policy model to use (MlpPolicy, CnnPolicy, ...)
    :param env: (Gym environment or str) The environment to learn from (if registered in Gym, can be str)
    :param attacker_learning_rate: (float or callable) The learning rate, it can be a function
        of the current progress remaining (from 1 to 0)
    :param n_steps: (int) The number of steps to run for each environment per update
        (i.e. batch size is n_steps * n_env where n_env is number of environment copies running in parallel)
    :param batch_size: (int) Minibatch size
    :param n_epochs: (int) Number of epoch when optimizing the surrogate loss
    :param attacker_gamma: (float) Discount factor
    :param attacker_gae_lambda: (float) Factor for trade-off of bias vs variance for Generalized Advantage Estimator
    :param attacker_clip_range: (float or callable) Clipping parameter, it can be a function of the current progress
        remaining (from 1 to 0).
    :param attacker_clip_range_vf: (float or callable) Clipping parameter for the value function,
        it can be a function of the current progress remaining (from 1 to 0).
        This is a parameter specific to the OpenAI implementation. If None is passed (default),
        no clipping will be done on the value function.
        IMPORTANT: this clipping depends on the reward scaling.
    :param attacker_ent_coef: (float) Entropy coefficient for the loss calculation
    :param attacker_vf_coef: (float) Value function coefficient for the loss calculation
    :param attacker_max_grad_norm: (float) The maximum value for the gradient clipping
    :param target_kl: (float) Limit the KL divergence between updates,
        because the clipping is not enough to prevent large update
        see issue #213 (cf https://github.com/hill-a/stable-baselines/issues/213)
        By default, there is no limit on the kl div.
    :param tensorboard_log: (str) the log location for tensorboard (if None, no logging)
    :param create_eval_env: (bool) Whether to create a second environment that will be
        used for evaluating the agent periodically. (Only available when passing string for the environment)
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
        attacker_learning_rate: Union[float, Callable] = 3e-4,
        defender_learning_rate: Union[float, Callable] = 3e-4,
        n_steps: int = 2048,
        batch_size: Optional[int] = 64,
        n_epochs: int = 10,
        attacker_gamma: float = 0.99,
        defender_gamma: float = 0.99,
        attacker_gae_lambda: float = 0.95,
        defender_gae_lambda: float = 0.95,
        attacker_clip_range: float = 0.2,
        defender_clip_range: float = 0.2,
        attacker_clip_range_vf: Optional[float] = None,
        defender_clip_range_vf: Optional[float] = None,
        attacker_ent_coef: float = 0.0,
        defender_ent_coef: float = 0.0,
        attacker_vf_coef: float = 0.5,
        defender_vf_coef: float = 0.5,
        attacker_max_grad_norm: float = 0.5,
        defender_max_grad_norm: float = 0.5,
        target_kl: Optional[float] = None,
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
        train_mode: TrainMode = TrainMode.TRAIN_ATTACKER,
        train_agent_log_dto: BaseTrainAgentLogDTO = None,
        rollout_data_dto: BaseRolloutDataDTO = None,
        eval_util: BaseEvalUtil = None,
        train_experiment_result: BaseExperimentResult = None,
        eval_experiment_result: BaseExperimentResult = None
    ):

        super(PPO, self).__init__(
            attacker_policy, defender_policy,
            env,
            attacker_learning_rate=attacker_learning_rate,
            defender_learning_rate=defender_learning_rate,
            n_steps=n_steps,
            attacker_gamma=attacker_gamma,
            defender_gamma=defender_gamma,
            attacker_gae_lambda=attacker_gae_lambda,
            defender_gae_lambda=defender_gae_lambda,
            attacker_ent_coef=attacker_ent_coef,
            defender_ent_coef=defender_ent_coef,
            attacker_vf_coef=attacker_vf_coef,
            defender_vf_coef=defender_vf_coef,
            attacker_max_grad_norm=attacker_max_grad_norm,
            defender_max_grad_norm=defender_max_grad_norm,
            attacker_policy_kwargs=attacker_policy_kwargs,
            defender_policy_kwargs=defender_policy_kwargs,
            verbose=verbose,
            device=device,
            create_eval_env=create_eval_env,
            seed=seed,
            _init_setup_model=False,
            attacker_agent_config=attacker_agent_config,
            defender_agent_config=defender_agent_config,
            env_2=env_2,
            train_mode=train_mode,
            train_agent_log_dto=train_agent_log_dto,
            rollout_data_dto=rollout_data_dto,
            eval_util=eval_util,
            train_experiment_result=train_experiment_result,
            eval_experiment_result=eval_experiment_result
        )

        self.batch_size = batch_size
        self.n_epochs = n_epochs
        self.attacker_clip_range = attacker_clip_range
        self.attacker_clip_range_vf = attacker_clip_range_vf
        self.defender_clip_range = defender_clip_range
        self.defender_clip_range_vf = defender_clip_range_vf
        self.target_kl = target_kl

        if _init_setup_model:
            self._setup_model()

    def _setup_model(self) -> None:
        super(PPO, self)._setup_model()

        # Initialize schedules for policy/value clipping for attacker
        self.attacker_clip_range = get_schedule_fn(self.attacker_clip_range)
        if self.attacker_clip_range_vf is not None:
            if isinstance(self.attacker_clip_range_vf, (float, int)):
                assert self.attacker_clip_range_vf > 0, "`clip_range_vf` must be positive, " "pass `None` to deactivate vf clipping"

            self.attacker_clip_range_vf = get_schedule_fn(self.attacker_clip_range_vf)

        # Initialize schedules for policy/value clipping for attacker
        self.defender_clip_range = get_schedule_fn(self.defender_clip_range)
        if self.defender_clip_range_vf is not None:
            if isinstance(self.defender_clip_range_vf, (float, int)):
                assert self.defender_clip_range_vf > 0, "`clip_range_vf` must be positive, " "pass `None` to deactivate vf clipping"

            self.defender_clip_range_vf = get_schedule_fn(self.defender_clip_range_vf)

    def train(self) -> None:
        """
        Update policy using the currently gathered
        rollout buffer.
        """
        # Update optimizer learning rate
        self._update_learning_rate(self.attacker_policy.optimizer)
        lr_attacker = self.attacker_policy.optimizer.param_groups[0]["lr"]

        self._update_learning_rate(self.defender_policy.optimizer)
        lr_defender = self.defender_policy.optimizer.param_groups[0]["lr"]

        # Compute current clip range
        attacker_clip_range = self.attacker_clip_range(self._current_progress_remaining)
        defender_clip_range = self.defender_clip_range(self._current_progress_remaining)

        # Optional: clip range for the value function
        attacker_clip_range_vf = None
        defender_clip_range_vf = None
        if self.attacker_clip_range_vf is not None:
            attacker_clip_range_vf = self.attacker_clip_range_vf(self._current_progress_remaining)

        if self.defender_clip_range_vf is not None:
            defender_clip_range_vf = self.defender_clip_range_vf(self._current_progress_remaining)

        entropy_losses_attacker, all_kl_divs_attacker = [], []
        pg_losses_attacker, value_losses_attacker = [], []
        clip_fractions_attacker = []
        grad_comp_times_attacker = []
        weight_update_times_attacker = []

        entropy_losses_defender, all_kl_divs_defender = [], []
        pg_losses_defender, value_losses_defender = [], []
        clip_fractions_defender = []
        grad_comp_times_defender = []
        weight_update_times_defender = []

        # train for gradient_steps epochs
        for epoch in range(self.n_epochs):

            if self.train_mode == TrainMode.TRAIN_ATTACKER or self.train_mode == TrainMode.SELF_PLAY:
                attacker_clip_range, pg_losses_attacker, clip_fractions_attacker, \
                attacker_clip_range_vf, value_losses_attacker, entropy_losses_attacker, \
                grad_comp_times_attacker, weight_update_times_attacker =  \
                    self.attacker_rollout_buffer_pass(
                    attacker_clip_range, pg_losses_attacker, clip_fractions_attacker,
                    attacker_clip_range_vf, value_losses_attacker, entropy_losses_attacker,
                    grad_comp_times_attacker, weight_update_times_attacker)

            if self.train_mode == TrainMode.TRAIN_DEFENDER or self.train_mode == TrainMode.SELF_PLAY:
                defender_clip_range, pg_losses_defender, clip_fractions_defender, \
                defender_clip_range_vf, value_losses_defender, entropy_losses_defender, \
                grad_comp_times_defender, weight_update_times_defender = \
                    self.defender_rollout_buffer_pass(
                        defender_clip_range, pg_losses_defender, clip_fractions_defender,
                        defender_clip_range_vf, value_losses_defender, entropy_losses_defender,
                        grad_comp_times_defender, weight_update_times_defender)


        self._n_updates += self.n_epochs
        if self.train_mode == TrainMode.TRAIN_ATTACKER or self.train_mode == TrainMode.SELF_PLAY:
            explained_var_attacker = \
                explained_variance(self.attacker_rollout_buffer.returns.flatten(),
                                   self.attacker_rollout_buffer.values.flatten())

        if self.train_mode == TrainMode.TRAIN_DEFENDER or self.train_mode == TrainMode.SELF_PLAY:
            explained_var_defender = \
                explained_variance(self.defender_rollout_buffer.returns.flatten(),
                                   self.defender_rollout_buffer.values.flatten())

        return np.mean(entropy_losses_attacker), \
               np.mean(pg_losses_attacker), np.mean(value_losses_attacker), \
               lr_attacker, grad_comp_times_attacker, weight_update_times_attacker, \
               np.mean(entropy_losses_defender), \
               np.mean(pg_losses_defender), np.mean(value_losses_defender), \
               lr_defender, grad_comp_times_defender, weight_update_times_defender

    def attacker_rollout_buffer_pass(self, attacker_clip_range, pg_losses_attacker, clip_fractions_attacker,
                                     attacker_clip_range_vf, value_losses_attacker, entropy_losses_attacker,
                                     grad_comp_times_attacker, weight_update_times_attacker):
        # Do a complete pass on the attacker's rollout buffer
        for rollout_data in self.attacker_rollout_buffer.get(self.batch_size):
            if self.attacker_agent_config.performance_analysis:
                start = time.time()

            actions = rollout_data.actions
            if isinstance(self.attacker_action_space, spaces.Discrete):
                # Convert discrete action from float to long
                actions = rollout_data.actions.long().flatten()

            values, log_prob, entropy = self.attacker_policy.evaluate_actions(rollout_data.observations, actions)
            values = values.flatten()
            # Normalize advantage
            advantages = rollout_data.advantages
            advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

            # ratio between old and new policy, should be one at the first iteration
            ratio = th.exp(log_prob - rollout_data.old_log_prob)

            # clipped surrogate loss
            policy_loss_1 = advantages * ratio
            policy_loss_2 = advantages * th.clamp(ratio, 1 - attacker_clip_range, 1 + attacker_clip_range)
            policy_loss = -th.min(policy_loss_1, policy_loss_2).mean()

            # Logging
            pg_losses_attacker.append(policy_loss.item())
            clip_fraction = th.mean((th.abs(ratio - 1) > attacker_clip_range).float()).item()
            clip_fractions_attacker.append(clip_fraction)

            if self.attacker_clip_range_vf is None:
                # No clipping
                values_pred = values
            else:
                # Clip the different between old and new value
                # NOTE: this depends on the reward scaling
                values_pred = rollout_data.old_values + th.clamp(
                    values - rollout_data.old_values, -attacker_clip_range_vf, attacker_clip_range_vf
                )
            # Value loss using the TD(gae_lambda) target
            value_loss = F.mse_loss(rollout_data.returns, values_pred)
            value_losses_attacker.append(value_loss.item())

            # Entropy loss favor exploration
            if entropy is None:
                # Approximate entropy when no analytical form
                entropy_loss = -th.mean(-log_prob)
            else:
                entropy_loss = -th.mean(entropy)

            entropy_losses_attacker.append(entropy_loss.item())

            loss = policy_loss + self.attacker_ent_coef * entropy_loss + self.attacker_vf_coef * value_loss

            # Optimization step
            self.attacker_policy.optimizer.zero_grad()
            loss.backward()
            if self.attacker_agent_config.performance_analysis:
                end = time.time()
                grad_comp_times_attacker.append(end - start)
            # Clip grad norm
            if self.attacker_agent_config.performance_analysis:
                start = time.time()
            th.nn.utils.clip_grad_norm_(self.attacker_policy.parameters(), self.attacker_max_grad_norm)
            self.attacker_policy.optimizer.step()
            if self.attacker_agent_config.performance_analysis:
                end = time.time()
                weight_update_times_attacker.append(end - start)

        return attacker_clip_range, pg_losses_attacker, clip_fractions_attacker, \
               attacker_clip_range_vf, value_losses_attacker, entropy_losses_attacker, \
               grad_comp_times_attacker, weight_update_times_attacker

    def defender_rollout_buffer_pass(self, defender_clip_range, pg_losses_defender, clip_fractions_defender,
                                     defender_clip_range_vf, value_losses_defender, entropy_losses_defender,
                                     grad_comp_times_defender, weight_update_times_defender):

        # Do a complete pass on the defender's rollout buffer
        for rollout_data in self.defender_rollout_buffer.get(self.batch_size):
            if self.defender_agent_config.performance_analysis:
                start = time.time()

            actions = rollout_data.actions
            if isinstance(self.defender_action_space, spaces.Discrete):
                # Convert discrete action from float to long
                actions = rollout_data.actions.long().flatten()

            values, log_prob, entropy = self.defender_policy.evaluate_actions(rollout_data.observations, actions)
            values = values.flatten()
            # Normalize advantage
            advantages = rollout_data.advantages
            advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

            # ratio between old and new policy, should be one at the first iteration
            ratio = th.exp(log_prob - rollout_data.old_log_prob)

            # clipped surrogate loss
            policy_loss_1 = advantages * ratio
            policy_loss_2 = advantages * th.clamp(ratio, 1 - defender_clip_range, 1 + defender_clip_range)
            policy_loss = -th.min(policy_loss_1, policy_loss_2).mean()

            # Logging
            pg_losses_defender.append(policy_loss.item())
            clip_fraction = th.mean((th.abs(ratio - 1) > defender_clip_range).float()).item()
            clip_fractions_defender.append(clip_fraction)

            if self.defender_clip_range_vf is None:
                # No clipping
                values_pred = values
            else:
                # Clip the different between old and new value
                # NOTE: this depends on the reward scaling
                values_pred = rollout_data.old_values + th.clamp(
                    values - rollout_data.old_values, -defender_clip_range_vf, defender_clip_range_vf
                )
            # Value loss using the TD(gae_lambda) target
            value_loss = F.mse_loss(rollout_data.returns, values_pred)
            value_losses_defender.append(value_loss.item())

            # Entropy loss favor exploration
            if entropy is None:
                # Approximate entropy when no analytical form
                entropy_loss = -th.mean(-log_prob)
            else:
                entropy_loss = -th.mean(entropy)

            entropy_losses_defender.append(entropy_loss.item())

            loss = policy_loss + self.defender_ent_coef * entropy_loss + self.defender_vf_coef * value_loss

            # Optimization step
            self.defender_policy.optimizer.zero_grad()
            loss.backward()
            if self.defender_agent_config.performance_analysis:
                end = time.time()
                grad_comp_times_defender.append(end - start)
            # Clip grad norm
            if self.defender_agent_config.performance_analysis:
                start = time.time()
            th.nn.utils.clip_grad_norm_(self.defender_policy.parameters(), self.defender_max_grad_norm)
            self.defender_policy.optimizer.step()
            if self.defender_agent_config.performance_analysis:
                end = time.time()
                weight_update_times_defender.append(end - start)

        return defender_clip_range, pg_losses_defender, clip_fractions_defender, \
               defender_clip_range_vf, value_losses_defender, entropy_losses_defender, \
               grad_comp_times_defender, weight_update_times_defender

    def train_ar(self) -> None:
        """
        Update policy using the currently gathered
        rollout buffer.
        """

        # Update optimizer learning rate
        self._update_learning_rate(self.m_selection_policy.optimizer)
        lr = self.m_selection_policy.optimizer.param_groups[0]["lr"]
        self._update_learning_rate(self.m_action_policy.optimizer)
        lr = self.m_action_policy.optimizer.param_groups[0]["lr"]

        # Compute current clip range
        clip_range = self.attacker_clip_range(self._current_progress_remaining)
        # Optional: clip range for the value function
        if self.attacker_clip_range_vf is not None:
            clip_range_vf = self.attacker_clip_range_vf(self._current_progress_remaining)

        entropy_losses_m_selection, all_kl_divs_m_selection = [], []
        pg_losses_m_selection, value_losses_m_selection = [], []
        clip_fractions_m_selection = []

        entropy_losses_m_, all_kl_divs_m = [], []
        pg_losses_m, value_losses_m = [], []
        clip_fractions_m = []

        # train for gradient_steps epochs
        for epoch in range(self.n_epochs):
            m_selection_approx_kl_divs = []
            m_action_approx_kl_divs = []
            # Do a complete pass on the rollout buffer
            for rollout_data in self.attacker_rollout_buffer.get(self.batch_size):
                m_selection_actions = rollout_data.m_selection_actions
                if isinstance(self.env.envs[0].m_selection_action_space, spaces.Discrete):
                    # Convert discrete action from float to long
                    m_selection_actions = rollout_data.m_selection_actions.long().flatten()

                m_actions = rollout_data.m_actions
                if isinstance(self.env.envs[0].m_action_space, spaces.Discrete):
                    # Convert discrete action from float to long
                    m_actions = rollout_data.m_actions.long().flatten()

                m_selection_values, m_selection_log_prob, m_selection_entropy = \
                    self.m_selection_policy.evaluate_actions(rollout_data.network_observations, m_selection_actions)
                m_selection_values = m_selection_values.flatten()
                # Normalize advantage
                m_selection_advantages = rollout_data.m_selection_advantages
                m_selection_advantages = (m_selection_advantages - m_selection_advantages.mean()) \
                                         / (m_selection_advantages.std() + 1e-8)

                m_action_values, m_action_log_prob, m_action_entropy = \
                    self.m_action_policy.evaluate_actions(rollout_data.machine_observations, m_actions)
                m_action_values = m_action_values.flatten()
                # Normalize advantage
                m_action_advantages = rollout_data.m_action_advantages
                m_action_advantages = (m_action_advantages - m_action_advantages.mean()) \
                                         / (m_action_advantages.std() + 1e-8)

                # ratio between old and new policy, should be one at the first iteration
                m_selection_ratio = th.exp(m_selection_log_prob - rollout_data.m_selection_old_log_prob)
                m_action_ratio = th.exp(m_action_log_prob - rollout_data.m_action_old_log_prob)

                # clipped surrogate loss
                m_selection_policy_loss_1 = m_selection_advantages * m_selection_ratio
                m_selection_policy_loss_2 = m_selection_advantages * th.clamp(m_selection_ratio, 1 - clip_range, 1 + clip_range)
                m_selection_policy_loss = -th.min(m_selection_policy_loss_1, m_selection_policy_loss_2).mean()

                m_action_policy_loss_1 = m_action_advantages * m_action_ratio
                m_action_policy_loss_2 = m_action_advantages * th.clamp(m_action_ratio, 1 - clip_range,
                                                                              1 + clip_range)
                m_action_policy_loss = -th.min(m_action_policy_loss_1, m_action_policy_loss_2).mean()

                # Logging
                pg_losses_m_selection.append(m_selection_policy_loss.item())
                clip_fraction = th.mean((th.abs(m_selection_ratio - 1) > clip_range).float()).item()
                clip_fractions_m_selection.append(clip_fraction)

                pg_losses_m.append(m_action_policy_loss.item())
                clip_fraction = th.mean((th.abs(m_action_ratio - 1) > clip_range).float()).item()
                clip_fractions_m.append(clip_fraction)

                if self.attacker_clip_range_vf is None:
                    # No clipping
                    m_selection_values_pred = m_selection_values
                    m_action_values_pred = m_action_values
                else:
                    # Clip the different between old and new value
                    # NOTE: this depends on the reward scaling
                    m_selection_values_pred = rollout_data.m_selection_old_values + th.clamp(
                        m_selection_values - rollout_data.m_selection_old_values, -clip_range_vf, clip_range_vf
                    )
                    m_action_values_pred = rollout_data.m_action_old_values + th.clamp(
                        m_action_values - rollout_data.m_action_old_values, -clip_range_vf, clip_range_vf
                    )

                # Value loss using the TD(gae_lambda) target
                m_selection_value_loss = F.mse_loss(rollout_data.m_selection_returns, m_selection_values_pred)
                value_losses_m_selection.append(m_selection_value_loss.item())

                m_action_value_loss = F.mse_loss(rollout_data.m_action_returns, m_action_values_pred)
                value_losses_m.append(m_action_value_loss.item())

                # Entropy loss to favor exploration
                if m_selection_entropy is None:
                    # Approximate entropy when no analytical form
                    m_selection_entropy_loss = -th.mean(-m_selection_log_prob)
                else:
                    m_selection_entropy_loss = -th.mean(m_selection_entropy)
                if m_action_entropy is None:
                    m_action_entropy_loss = -th.mean(-m_action_log_prob)
                else:
                    m_action_entropy_loss = -th.mean(m_action_entropy)

                entropy_losses_m_selection.append(m_selection_entropy_loss.item())
                entropy_losses_m_.append(m_action_entropy_loss.item())

                m_selection_loss = m_selection_policy_loss + self.attacker_ent_coef * m_selection_entropy_loss \
                                   + self.attacker_vf_coef * m_selection_value_loss
                m_action_loss = m_action_policy_loss + self.attacker_ent_coef * m_action_entropy_loss \
                                   + self.attacker_vf_coef * m_action_value_loss

                # Optimization step
                self.m_selection_policy.optimizer.zero_grad()
                m_selection_loss.backward()
                # Clip grad norm
                th.nn.utils.clip_grad_norm_(self.m_selection_policy.parameters(), self.attacker_max_grad_norm)
                self.m_selection_policy.optimizer.step()
                m_selection_approx_kl_divs.append(th.mean(rollout_data.m_selection_old_log_prob -
                                              m_selection_log_prob).detach().cpu().numpy())

                # Optimization step
                self.m_action_policy.optimizer.zero_grad()
                m_action_loss.backward()
                # Clip grad norm
                th.nn.utils.clip_grad_norm_(self.m_action_policy.parameters(), self.attacker_max_grad_norm)
                self.m_action_policy.optimizer.step()
                m_action_approx_kl_divs.append(th.mean(rollout_data.m_action_old_log_prob -
                                              m_action_log_prob).detach().cpu().numpy())

            all_kl_divs_m_selection.append(np.mean(m_selection_approx_kl_divs))
            all_kl_divs_m.append(np.mean(m_action_approx_kl_divs))

        self._n_updates += self.n_epochs
        #explained_var = explained_variance(self.rollout_buffer.returns.flatten(), self.rollout_buffer.values.flatten())

        return np.mean(entropy_losses_m_selection) + np.mean(entropy_losses_m_), \
               np.mean(pg_losses_m_selection) + np.mean(pg_losses_m), \
               np.mean(value_losses_m_selection) + np.mean(value_losses_m), lr

    def learn(
        self,
        total_timesteps: int,
        callback: MaybeCallback = None,
        log_interval: int = 1,
        eval_env: Optional[GymEnv] = None,
        eval_env_2: Optional[GymEnv] = None,
        eval_freq: int = -1,
        n_eval_episodes: int = 5,
        tb_log_name: str = "PPO",
        eval_log_path: Optional[str] = None,
        reset_num_timesteps: bool = True,
    ) -> "PPO":

        return super(PPO, self).learn(
            total_timesteps=total_timesteps,
            callback=callback,
            log_interval=log_interval,
            eval_env=eval_env,
            eval_env_2=eval_env_2,
            eval_freq=eval_freq,
            n_eval_episodes=n_eval_episodes,
            tb_log_name=tb_log_name,
            eval_log_path=eval_log_path,
            reset_num_timesteps=reset_num_timesteps,
        )