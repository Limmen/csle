from typing import Any, Callable, Dict, Optional, Type, Union

import numpy as np
import torch as th
from gym import spaces
from torch.nn import functional as F

from gym_pycr_pwcrack.agents.openai_baselines.common.utils import explained_variance, get_schedule_fn
from gym_pycr_pwcrack.agents.openai_baselines.common.type_aliases import GymEnv, MaybeCallback
from gym_pycr_pwcrack.agents.openai_baselines.common.policies import ActorCriticPolicy
from gym_pycr_pwcrack.agents.openai_baselines.common.on_policy_algorithm import OnPolicyAlgorithm
from gym_pycr_pwcrack.agents.config.agent_config import AgentConfig


class PPO(OnPolicyAlgorithm):
    """
    Proximal Policy Optimization algorithm (PPO) (clip version)

    Paper: https://arxiv.org/abs/1707.06347
    Code: This implementation borrows code from OpenAI Spinning Up (https://github.com/openai/spinningup/)
    https://github.com/ikostrikov/pytorch-a2c-ppo-acktr-gail and
    and Stable Baselines (PPO2 from https://github.com/hill-a/stable-baselines)

    Introduction to PPO: https://spinningup.openai.com/en/latest/algorithms/ppo.html

    :param policy: (ActorCriticPolicy or str) The policy model to use (MlpPolicy, CnnPolicy, ...)
    :param env: (Gym environment or str) The environment to learn from (if registered in Gym, can be str)
    :param learning_rate: (float or callable) The learning rate, it can be a function
        of the current progress remaining (from 1 to 0)
    :param n_steps: (int) The number of steps to run for each environment per update
        (i.e. batch size is n_steps * n_env where n_env is number of environment copies running in parallel)
    :param batch_size: (int) Minibatch size
    :param n_epochs: (int) Number of epoch when optimizing the surrogate loss
    :param gamma: (float) Discount factor
    :param gae_lambda: (float) Factor for trade-off of bias vs variance for Generalized Advantage Estimator
    :param clip_range: (float or callable) Clipping parameter, it can be a function of the current progress
        remaining (from 1 to 0).
    :param clip_range_vf: (float or callable) Clipping parameter for the value function,
        it can be a function of the current progress remaining (from 1 to 0).
        This is a parameter specific to the OpenAI implementation. If None is passed (default),
        no clipping will be done on the value function.
        IMPORTANT: this clipping depends on the reward scaling.
    :param ent_coef: (float) Entropy coefficient for the loss calculation
    :param vf_coef: (float) Value function coefficient for the loss calculation
    :param max_grad_norm: (float) The maximum value for the gradient clipping
    :param use_sde: (bool) Whether to use generalized State Dependent Exploration (gSDE)
        instead of action noise exploration (default: False)
    :param sde_sample_freq: (int) Sample a new noise matrix every n steps when using gSDE
        Default: -1 (only sample at the beginning of the rollout)
    :param target_kl: (float) Limit the KL divergence between updates,
        because the clipping is not enough to prevent large update
        see issue #213 (cf https://github.com/hill-a/stable-baselines/issues/213)
        By default, there is no limit on the kl div.
    :param tensorboard_log: (str) the log location for tensorboard (if None, no logging)
    :param create_eval_env: (bool) Whether to create a second environment that will be
        used for evaluating the agent periodically. (Only available when passing string for the environment)
    :param policy_kwargs: (dict) additional arguments to be passed to the policy on creation
    :param verbose: (int) the verbosity level: 0 no output, 1 info, 2 debug
    :param seed: (int) Seed for the pseudo random generators
    :param device: (str or th.device) Device (cpu, cuda, ...) on which the code should be run.
        Setting it to auto, the code will be run on the GPU if possible.
    :param _init_setup_model: (bool) Whether or not to build the network at the creation of the instance
    """

    def __init__(
        self,
        policy: Union[str, Type[ActorCriticPolicy]],
        env: Union[GymEnv, str],
        learning_rate: Union[float, Callable] = 3e-4,
        n_steps: int = 2048,
        batch_size: Optional[int] = 64,
        n_epochs: int = 10,
        gamma: float = 0.99,
        gae_lambda: float = 0.95,
        clip_range: float = 0.2,
        clip_range_vf: Optional[float] = None,
        ent_coef: float = 0.0,
        vf_coef: float = 0.5,
        max_grad_norm: float = 0.5,
        use_sde: bool = False,
        sde_sample_freq: int = -1,
        target_kl: Optional[float] = None,
        create_eval_env: bool = False,
        policy_kwargs: Optional[Dict[str, Any]] = None,
        verbose: int = 0,
        seed: Optional[int] = None,
        device: Union[th.device, str] = "auto",
        _init_setup_model: bool = True,
        agent_config: AgentConfig = None,
        env_2: Union[GymEnv, str] = None
    ):

        super(PPO, self).__init__(
            policy,
            env,
            learning_rate=learning_rate,
            n_steps=n_steps,
            gamma=gamma,
            gae_lambda=gae_lambda,
            ent_coef=ent_coef,
            vf_coef=vf_coef,
            max_grad_norm=max_grad_norm,
            use_sde=use_sde,
            sde_sample_freq=sde_sample_freq,
            policy_kwargs=policy_kwargs,
            verbose=verbose,
            device=device,
            create_eval_env=create_eval_env,
            seed=seed,
            _init_setup_model=False,
            agent_config=agent_config,
            env_2=env_2
        )

        self.batch_size = batch_size
        self.n_epochs = n_epochs
        self.clip_range = clip_range
        self.clip_range_vf = clip_range_vf
        self.target_kl = target_kl

        if _init_setup_model:
            self._setup_model()

    def _setup_model(self) -> None:
        super(PPO, self)._setup_model()

        # Initialize schedules for policy/value clipping
        self.clip_range = get_schedule_fn(self.clip_range)
        if self.clip_range_vf is not None:
            if isinstance(self.clip_range_vf, (float, int)):
                assert self.clip_range_vf > 0, "`clip_range_vf` must be positive, " "pass `None` to deactivate vf clipping"

            self.clip_range_vf = get_schedule_fn(self.clip_range_vf)

    def train(self) -> None:
        """
        Update policy using the currently gathered
        rollout buffer.
        """
        # Update optimizer learning rate
        self._update_learning_rate(self.policy.optimizer)
        lr = self.policy.optimizer.param_groups[0]["lr"]
        # Compute current clip range
        clip_range = self.clip_range(self._current_progress_remaining)
        # Optional: clip range for the value function
        if self.clip_range_vf is not None:
            clip_range_vf = self.clip_range_vf(self._current_progress_remaining)

        entropy_losses, all_kl_divs = [], []
        pg_losses, value_losses = [], []
        clip_fractions = []

        # train for gradient_steps epochs
        for epoch in range(self.n_epochs):
            approx_kl_divs = []
            # Do a complete pass on the rollout buffer
            for rollout_data in self.rollout_buffer.get(self.batch_size):
                actions = rollout_data.actions
                if isinstance(self.action_space, spaces.Discrete):
                    # Convert discrete action from float to long
                    actions = rollout_data.actions.long().flatten()

                # Re-sample the noise matrix because the log_std has changed
                # TODO: investigate why there is no issue with the gradient
                # if that line is commented (as in SAC)
                if self.use_sde:
                    self.policy.reset_noise(self.batch_size)

                values, log_prob, entropy = self.policy.evaluate_actions(rollout_data.observations, actions)
                values = values.flatten()
                # Normalize advantage
                advantages = rollout_data.advantages
                advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

                # ratio between old and new policy, should be one at the first iteration
                ratio = th.exp(log_prob - rollout_data.old_log_prob)

                # clipped surrogate loss
                policy_loss_1 = advantages * ratio
                policy_loss_2 = advantages * th.clamp(ratio, 1 - clip_range, 1 + clip_range)
                policy_loss = -th.min(policy_loss_1, policy_loss_2).mean()

                # Logging
                pg_losses.append(policy_loss.item())
                clip_fraction = th.mean((th.abs(ratio - 1) > clip_range).float()).item()
                clip_fractions.append(clip_fraction)

                if self.clip_range_vf is None:
                    # No clipping
                    values_pred = values
                else:
                    # Clip the different between old and new value
                    # NOTE: this depends on the reward scaling
                    values_pred = rollout_data.old_values + th.clamp(
                        values - rollout_data.old_values, -clip_range_vf, clip_range_vf
                    )
                # Value loss using the TD(gae_lambda) target
                value_loss = F.mse_loss(rollout_data.returns, values_pred)
                value_losses.append(value_loss.item())

                # Entropy loss favor exploration
                if entropy is None:
                    # Approximate entropy when no analytical form
                    entropy_loss = -th.mean(-log_prob)
                else:
                    entropy_loss = -th.mean(entropy)

                entropy_losses.append(entropy_loss.item())

                loss = policy_loss + self.ent_coef * entropy_loss + self.vf_coef * value_loss

                # Optimization step
                self.policy.optimizer.zero_grad()
                loss.backward()
                # Clip grad norm
                th.nn.utils.clip_grad_norm_(self.policy.parameters(), self.max_grad_norm)
                self.policy.optimizer.step()
                approx_kl_divs.append(th.mean(rollout_data.old_log_prob - log_prob).detach().cpu().numpy())

            all_kl_divs.append(np.mean(approx_kl_divs))

            if self.target_kl is not None and np.mean(approx_kl_divs) > 1.5 * self.target_kl:
                print(f"Early stopping at step {epoch} due to reaching max kl: {np.mean(approx_kl_divs):.2f}")
                break

        self._n_updates += self.n_epochs
        explained_var = explained_variance(self.rollout_buffer.returns.flatten(), self.rollout_buffer.values.flatten())

        return np.mean(entropy_losses), np.mean(pg_losses), np.mean(value_losses), lr

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
        clip_range = self.clip_range(self._current_progress_remaining)
        # Optional: clip range for the value function
        if self.clip_range_vf is not None:
            clip_range_vf = self.clip_range_vf(self._current_progress_remaining)

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
            for rollout_data in self.rollout_buffer.get(self.batch_size):
                m_selection_actions = rollout_data.m_selection_actions
                if isinstance(self.env.envs[0].m_selection_action_space, spaces.Discrete):
                    # Convert discrete action from float to long
                    m_selection_actions = rollout_data.m_selection_actions.long().flatten()

                m_actions = rollout_data.m_actions
                if isinstance(self.env.envs[0].m_action_space, spaces.Discrete):
                    # Convert discrete action from float to long
                    m_actions = rollout_data.m_actions.long().flatten()

                # Re-sample the noise matrix because the log_std has changed
                # TODO: investigate why there is no issue with the gradient
                # if that line is commented (as in SAC)
                if self.use_sde:
                    self.m_selection_policy.reset_noise(self.batch_size)
                    self.m_action_policy.reset_noise(self.batch_size)

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

                if self.clip_range_vf is None:
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

                # Entropy loss favor exploration
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

                m_selection_loss = m_selection_policy_loss + self.ent_coef * m_selection_entropy_loss \
                                   + self.vf_coef * m_selection_value_loss
                m_action_loss = m_action_policy_loss + self.ent_coef * m_action_entropy_loss \
                                   + self.vf_coef * m_action_value_loss

                # Optimization step
                self.m_selection_policy.optimizer.zero_grad()
                m_selection_loss.backward()
                # Clip grad norm
                th.nn.utils.clip_grad_norm_(self.m_selection_policy.parameters(), self.max_grad_norm)
                self.m_selection_policy.optimizer.step()
                m_selection_approx_kl_divs.append(th.mean(rollout_data.m_selection_old_log_prob -
                                              m_selection_log_prob).detach().cpu().numpy())

                # Optimization step
                self.m_action_policy.optimizer.zero_grad()
                m_action_loss.backward()
                # Clip grad norm
                th.nn.utils.clip_grad_norm_(self.m_action_policy.parameters(), self.max_grad_norm)
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