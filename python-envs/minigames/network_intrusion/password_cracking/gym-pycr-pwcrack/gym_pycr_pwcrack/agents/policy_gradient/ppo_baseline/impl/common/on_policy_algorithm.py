import time
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

import gym
import numpy as np
import torch as th

from gym_pycr_pwcrack.agents.policy_gradient.ppo_baseline.impl.common.buffers import RolloutBuffer
from gym_pycr_pwcrack.agents.policy_gradient.ppo_baseline.impl.common.type_aliases import GymEnv, MaybeCallback
from gym_pycr_pwcrack.agents.policy_gradient.ppo_baseline.impl.common.vec_env import VecEnv
from gym_pycr_pwcrack.agents.policy_gradient.ppo_baseline.impl.common.callbacks import BaseCallback
from gym_pycr_pwcrack.agents.policy_gradient.ppo_baseline.impl.common.base_class import BaseAlgorithm
from gym_pycr_pwcrack.agents.policy_gradient.ppo_baseline.impl.common.policies import ActorCriticPolicy
from gym_pycr_pwcrack.agents.config.pg_agent_config import PolicyGradientAgentConfig

class OnPolicyAlgorithm(BaseAlgorithm):
    """
    The base for On-Policy algorithms (ex: A2C/PPO).

    :param policy: (ActorCriticPolicy or str) The policy model to use (MlpPolicy, CnnPolicy, ...)
    :param env: (Gym environment or str) The environment to learn from (if registered in Gym, can be str)
    :param learning_rate: (float or callable) The learning rate, it can be a function
        of the current progress remaining (from 1 to 0)
    :param n_steps: (int) The number of steps to run for each environment per update
        (i.e. batch size is n_steps * n_env where n_env is number of environment copies running in parallel)
    :param gamma: (float) Discount factor
    :param gae_lambda: (float) Factor for trade-off of bias vs variance for Generalized Advantage Estimator.
        Equivalent to classic advantage when set to 1.
    :param ent_coef: (float) Entropy coefficient for the loss calculation
    :param vf_coef: (float) Value function coefficient for the loss calculation
    :param max_grad_norm: (float) The maximum value for the gradient clipping
    :param use_sde: (bool) Whether to use generalized State Dependent Exploration (gSDE)
        instead of action noise exploration (default: False)
    :param sde_sample_freq: (int) Sample a new noise matrix every n steps when using gSDE
        Default: -1 (only sample at the beginning of the rollout)
    :param tensorboard_log: (str) the log location for tensorboard (if None, no logging)
    :param create_eval_env: (bool) Whether to create a second environment that will be
        used for evaluating the agent periodically. (Only available when passing string for the environment)
    :param monitor_wrapper: When creating an environment, whether to wrap it
        or not in a Monitor wrapper.
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
        learning_rate: Union[float, Callable],
        n_steps: int,
        gamma: float,
        gae_lambda: float,
        ent_coef: float,
        vf_coef: float,
        max_grad_norm: float,
        use_sde: bool,
        sde_sample_freq: int,
        tensorboard_log: Optional[str] = None,
        create_eval_env: bool = False,
        monitor_wrapper: bool = True,
        policy_kwargs: Optional[Dict[str, Any]] = None,
        verbose: int = 0,
        seed: Optional[int] = None,
        device: Union[th.device, str] = "auto",
        _init_setup_model: bool = True,
        pg_agent_config: PolicyGradientAgentConfig = None
    ):

        super(OnPolicyAlgorithm, self).__init__(
            policy=policy,
            env=env,
            policy_base=ActorCriticPolicy,
            learning_rate=learning_rate,
            policy_kwargs=policy_kwargs,
            verbose=verbose,
            device=device,
            use_sde=use_sde,
            sde_sample_freq=sde_sample_freq,
            create_eval_env=create_eval_env,
            support_multi_env=True,
            seed=seed,
            pg_agent_config = pg_agent_config
        )

        self.n_steps = n_steps
        self.gamma = gamma
        self.gae_lambda = gae_lambda
        self.ent_coef = ent_coef
        self.vf_coef = vf_coef
        self.max_grad_norm = max_grad_norm
        self.rollout_buffer = None
        self.iteration = 0
        self.num_episodes = 0
        self.num_episodes_total = 0

        if _init_setup_model:
            self._setup_model()

    def _setup_model(self) -> None:
        self._setup_lr_schedule()
        self.set_random_seed(self.seed)

        self.rollout_buffer = RolloutBuffer(
            self.n_steps,
            self.observation_space,
            self.action_space,
            self.device,
            gamma=self.gamma,
            gae_lambda=self.gae_lambda,
            n_envs=self.n_envs,
        )
        self.policy = self.policy_class(
            self.observation_space,
            self.action_space,
            self.lr_schedule,
            use_sde=self.use_sde,
            **self.policy_kwargs  # pytype:disable=not-instantiable
        )
        self.policy = self.policy.to(self.device)

    def collect_rollouts(
        self, env: VecEnv, callback: BaseCallback, rollout_buffer: RolloutBuffer, n_rollout_steps: int
    ) -> Union[bool, int, int]:
        """
        Collect rollouts using the current policy and fill a `RolloutBuffer`.

        :param env: (VecEnv) The training environment
        :param callback: (BaseCallback) Callback that will be called at each step
            (and at the beginning and end of the rollout)
        :param rollout_buffer: (RolloutBuffer) Buffer to fill with rollouts
        :param n_steps: (int) Number of experiences to collect per environment
        :return: (bool) True if function returned with at least `n_rollout_steps`
            collected, False if callback terminated rollout prematurely.
        """
        assert self._last_obs is not None, "No previous observation was provided"
        n_steps = 0
        rollout_buffer.reset()
        # Sample new weights for the state dependent exploration
        if self.use_sde:
            self.policy.reset_noise(env.num_envs)

        # Avg metrics
        episode_rewards = []
        episode_steps = []

        # Per episode metrics
        episode_reward = 0
        episode_step = 0

        callback.on_rollout_start()
        dones = False
        while n_steps < n_rollout_steps:
            if self.use_sde and self.sde_sample_freq > 0 and n_steps % self.sde_sample_freq == 0:
                # Sample a new noise matrix
                self.policy.reset_noise(env.num_envs)

            new_obs, rewards, dones, infos, values, log_probs, actions = self.step_policy(self.env, rollout_buffer)

            self.num_timesteps += env.num_envs

            # Give access to local variables
            callback.update_locals(locals())
            if callback.on_step(iteration=self.iteration) is False:
                episode_rewards.append(episode_reward)
                episode_steps.append(episode_step)
                return False, episode_rewards, episode_steps

            # Record step metrics
            self._update_info_buffer(infos)
            n_steps += 1
            self.num_timesteps += env.num_envs
            episode_reward += rewards
            episode_step += 1

            if dones:
                # Record episode metrics
                self.num_episodes += 1
                self.num_episodes_total += 1
                episode_rewards.append(episode_reward)
                episode_steps.append(episode_step)
                episode_reward = 0
                episode_step = 0

        rollout_buffer.compute_returns_and_advantage(values, dones=dones)

        callback.on_rollout_end()
        if not dones:
            episode_rewards.append(episode_reward)
            episode_steps.append(episode_step)
        return True, episode_rewards, episode_steps

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
        eval_freq: int = -1,
        n_eval_episodes: int = 5,
        tb_log_name: str = "OnPolicyAlgorithm",
        eval_log_path: Optional[str] = None,
        reset_num_timesteps: bool = True,
    ) -> "OnPolicyAlgorithm":

        self.pg_agent_config.logger.info("Setting up Training Configuration")
        print("Setting up Training Configuration")

        self.iteration = 0
        total_timesteps, callback = self._setup_learn(
            total_timesteps, eval_env, callback, eval_freq, n_eval_episodes, eval_log_path, reset_num_timesteps,
            tb_log_name
        )

        callback.on_training_start(locals(), globals())
        self.pg_agent_config.logger.info("Starting training, max time steps:{}".format(total_timesteps))
        self.pg_agent_config.logger.info(self.pg_agent_config.to_str())

        # Tracking metrics
        episode_rewards = []
        episode_rewards_a = []
        episode_steps = []
        episode_avg_loss = []
        episode_avg_loss_a = []
        lr = 0.0

        while self.iteration < self.pg_agent_config.num_iterations:

            continue_training, rollouts_rewards, rollouts_steps  = self.collect_rollouts(self.env, callback,
                                                                                         self.rollout_buffer,
                                                                                         n_rollout_steps=self.n_steps)

            episode_rewards.extend(rollouts_rewards)
            episode_steps.extend(rollouts_steps)

            if continue_training is False:
                break

            self.iteration += 1
            self._update_current_progress_remaining(self.num_timesteps, total_timesteps)

            if self.iteration % self.pg_agent_config.train_log_frequency == 0:
                self.log_metrics(iteration=self.iteration, result=self.train_result,
                                 episode_rewards=episode_rewards,
                                 episode_avg_loss=episode_avg_loss,
                                 eval=False, lr=self.lr_schedule(self.num_timesteps),
                                 total_num_episodes=self.num_episodes_total,
                                 episode_steps=episode_steps)
                episode_rewards = []
                episode_rewards_a = []
                episode_avg_loss = []
                episode_avg_loss = []
                episode_avg_loss_a = []
                episode_steps = []
                self.num_episodes = 0

            # Save models every <self.config.checkpoint_frequency> iterations
            if self.iteration % self.pg_agent_config.checkpoint_freq == 0:
                self.save_model()
                if self.pg_agent_config.save_dir is not None:
                    time_str = str(time.time())
                    self.train_result.to_csv(
                        self.pg_agent_config.save_dir + "/" + time_str + "_train_results_checkpoint.csv")
                    self.eval_result.to_csv(
                        self.pg_agent_config.save_dir + "/" + time_str + "_eval_results_checkpoint.csv")

            entropy_loss, pg_loss, value_loss, lr = self.train()
            episode_avg_loss.append(entropy_loss + pg_loss + value_loss)

        callback.on_training_end()

        return self

    def get_torch_variables(self) -> Tuple[List[str], List[str]]:
        """
        cf base class
        """
        state_dicts = ["policy", "policy.optimizer"]

        return state_dicts, []


    def step_policy(self, env, rollout_buffer):
        with th.no_grad():
            # Convert to pytorch tensor
            obs_tensor = th.as_tensor(self._last_obs).to(self.device)
            actions, values, log_probs = self.policy.forward(obs_tensor)
        actions = actions.cpu().numpy()

        # Rescale and perform action
        clipped_actions = actions
        # Clip the actions to avoid out of bound error
        if isinstance(self.action_space, gym.spaces.Box):
            clipped_actions = np.clip(actions, self.action_space.low, self.action_space.high)

        new_obs, rewards, dones, infos = env.step(clipped_actions)

        if isinstance(self.action_space, gym.spaces.Discrete):
            # Reshape in case of discrete action
            actions = actions.reshape(-1, 1)

        rollout_buffer.add(self._last_obs, actions, rewards, self._last_dones, values, log_probs)

        self._last_obs = new_obs
        self._last_dones = dones

        return new_obs, rewards, dones, infos, values, log_probs, actions


    def save_model(self) -> None:
        """
        Saves the PyTorch Model Weights

        :return: None
        """
        time_str = str(time.time())
        if self.pg_agent_config.save_dir is not None:
            path = self.pg_agent_config.save_dir + "/" + time_str + "_policy_network.zip"
            self.pg_agent_config.logger.info("Saving policy-network to: {}".format(path))
            self.save(path, exclude=["tensorboard_writer"])
        else:
            self.pg_agent_config.logger.warning("Save path not defined, not saving policy-networks to disk")
            print("Save path not defined, not saving policy-networks to disk")