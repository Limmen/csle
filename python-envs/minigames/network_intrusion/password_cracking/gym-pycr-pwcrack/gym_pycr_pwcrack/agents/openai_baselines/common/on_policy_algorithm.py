import time
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

import gym
import numpy as np
import torch as th

from gym_pycr_pwcrack.agents.openai_baselines.common.buffers import RolloutBuffer, RolloutBufferAR
from gym_pycr_pwcrack.agents.openai_baselines.common.type_aliases import GymEnv, MaybeCallback
from gym_pycr_pwcrack.agents.openai_baselines.common.vec_env import VecEnv
from gym_pycr_pwcrack.agents.openai_baselines.common.callbacks import BaseCallback
from gym_pycr_pwcrack.agents.openai_baselines.common.base_class import BaseAlgorithm
from gym_pycr_pwcrack.agents.openai_baselines.common.policies import ActorCriticPolicy
from gym_pycr_pwcrack.agents.config.agent_config import AgentConfig
from gym_pycr_pwcrack.agents.openai_baselines.common.evaluation import quick_evaluate_policy
from gym_pycr_pwcrack.agents.openai_baselines.common.vec_env.dummy_vec_env import DummyVecEnv
from gym_pycr_pwcrack.agents.openai_baselines.common.vec_env.subproc_vec_env import SubprocVecEnv

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
        create_eval_env: bool = False,
        policy_kwargs: Optional[Dict[str, Any]] = None,
        verbose: int = 0,
        seed: Optional[int] = None,
        device: Union[th.device, str] = "auto",
        _init_setup_model: bool = True,
        agent_config: AgentConfig = None,
        env_2: Union[GymEnv, str] = None
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
            agent_config = agent_config,
            env_2=env_2
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

        if not self.agent_config.ar_policy:
            self.rollout_buffer = RolloutBuffer(
                self.n_steps,
                self.observation_space,
                self.action_space,
                self.device,
                gamma=self.gamma,
                gae_lambda=self.gae_lambda,
                n_envs=self.n_envs,
            )
        else:
            self.rollout_buffer = RolloutBufferAR(
                self.n_steps,
                self.observation_space,
                self.action_space,
                self.device,
                gamma=self.gamma,
                gae_lambda=self.gae_lambda,
                n_envs=self.n_envs,
                agent_config = self.agent_config
            )
        if not self.agent_config.ar_policy:
            self.policy = self.policy_class(
                self.observation_space,
                self.action_space,
                self.lr_schedule,
                use_sde=self.use_sde,
                agent_config = self.agent_config,
                **self.policy_kwargs  # pytype:disable=not-instantiable
            )
            self.policy = self.policy.to(self.device)
        else:
            self.m_selection_policy = self.policy_class(
                self.env.envs[0].m_selection_observation_space,
                self.env.envs[0].m_selection_action_space,
                self.lr_schedule,
                use_sde=self.use_sde,
                agent_config=self.agent_config,
                m_selection = True,
                **self.policy_kwargs  # pytype:disable=not-instantiable
            )
            self.m_selection_policy = self.m_selection_policy.to(self.device)
            self.m_action_policy = self.policy_class(
                self.env.envs[0].m_action_observation_space,
                self.env.envs[0].m_action_space,
                self.lr_schedule,
                use_sde=self.use_sde,
                agent_config=self.agent_config,
                m_action = True,
                **self.policy_kwargs  # pytype:disable=not-instantiable
            )
            self.m_action_policy = self.m_action_policy.to(self.device)

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
        episode_flags = []
        episode_flags_percentage = []

        # Per episode metrics
        episode_reward = np.zeros(env.num_envs)
        episode_step = np.zeros(env.num_envs)

        callback.on_rollout_start()
        dones = False
        while n_steps < n_rollout_steps:
            if self.use_sde and self.sde_sample_freq > 0 and n_steps % self.sde_sample_freq == 0:
                # Sample a new noise matrix
                self.policy.reset_noise(env.num_envs)

            if not self.agent_config.ar_policy:
                new_obs, rewards, dones, infos, values, log_probs, actions = self.step_policy(env, rollout_buffer)
            else:
                new_obs, machine_obs, rewards, dones, infos, m_selection_values, m_action_values, m_selection_log_probs, \
                m_action_log_probs, m_selection_actions, m_actions = self.step_policy_ar(env, rollout_buffer)

            # Record step metrics
            self.num_timesteps += env.num_envs
            self._update_info_buffer(infos)
            n_steps += 1
            episode_reward += rewards
            episode_step += 1

            # Give access to local variables
            callback.update_locals(locals())
            if callback.on_step(iteration=self.iteration) is False:
                for i in range(env.num_envs):
                    episode_rewards.append(episode_reward[i])
                    episode_steps.append(episode_step[i])
                    episode_flags.append(infos[i]["flags"])
                    episode_flags_percentage.append(infos[i]["flags"]/self.agent_config.env_config.num_flags)
                return False, episode_rewards, episode_steps

            if dones.any:
                for i in range(len(dones)):
                    if dones[i]:
                        # Record episode metrics
                        self.num_episodes += 1
                        self.num_episodes_total += 1
                        episode_rewards.append(episode_reward[i])
                        episode_steps.append(episode_step[i])
                        episode_flags.append(infos[i]["flags"])
                        episode_flags_percentage.append(infos[i]["flags"] / self.agent_config.env_config.num_flags)
                        episode_reward[i] = 0
                        episode_step[i] = 0

        if not self.agent_config.ar_policy:
            rollout_buffer.compute_returns_and_advantage(values, dones=dones)
        else:
            rollout_buffer.compute_returns_and_advantage(m_selection_values, dones=dones, machine_action = False)
            rollout_buffer.compute_returns_and_advantage(m_action_values, dones=dones, machine_action=True)

        callback.on_rollout_end()
        for i in range(len(dones)):
            if not dones[i]:
                episode_rewards.append(episode_reward[i])
                episode_steps.append(episode_step[i])
        return True, episode_rewards, episode_steps, episode_flags, episode_flags_percentage

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

        self.agent_config.logger.info("Setting up Training Configuration")
        print("Setting up Training Configuration")

        self.iteration = 0
        total_timesteps, callback = self._setup_learn(
            total_timesteps, eval_env, eval_env_2, callback, eval_freq, n_eval_episodes, eval_log_path,
            reset_num_timesteps, tb_log_name
        )

        callback.on_training_start(locals(), globals())
        self.agent_config.logger.info("Starting training, max time steps:{}".format(total_timesteps))
        self.agent_config.logger.info(self.agent_config.to_str())

        # Tracking metrics
        episode_rewards = []
        episode_flags = []
        episode_steps = []
        episode_loss = []
        episode_flags_percentage = []
        lr = 0.0

        while self.iteration < self.agent_config.num_iterations:

            continue_training, rollouts_rewards, rollouts_steps, rollouts_flags, rollouts_flags_percentage = \
                self.collect_rollouts(self.env, callback, self.rollout_buffer, n_rollout_steps=self.n_steps)

            episode_rewards.extend(rollouts_rewards)
            episode_steps.extend(rollouts_steps)
            episode_flags.extend(rollouts_flags)
            episode_flags_percentage.extend(rollouts_flags_percentage)

            if continue_training is False:
                break

            self.iteration += 1
            self._update_current_progress_remaining(self.num_timesteps, total_timesteps)

            if self.iteration % self.agent_config.train_log_frequency == 0:
                episode_rewards_1, episode_steps_1, episode_flags_percentage_1, episode_flags_1, \
                eval_episode_rewards, eval_episode_steps, \
                eval_episode_flags_percentage, eval_episode_flags = None, None, None, None, None, None, None, None
                if self.agent_config.train_progress_deterministic_eval:
                    episode_rewards_1, episode_steps_1, episode_flags_percentage_1, episode_flags_1, \
                    eval_episode_rewards, eval_episode_steps, eval_episode_flags_percentage, eval_episode_flags = \
                        quick_evaluate_policy(model=self.policy, env=self.env,
                                              n_eval_episodes=self.agent_config.n_deterministic_eval_iter,
                                              deterministic=True, agent_config=self.agent_config,
                                              env_config=self.agent_config.env_config, env_2=self.env_2)
                    d = {}
                    if isinstance(self.env, SubprocVecEnv):
                        self._last_infos[0]["non_legal_actions"] = self.env.initial_illegal_actions
                n_af, n_d = 0,0
                if isinstance(self.env, DummyVecEnv):
                    n_af = self.env.envs[0].agent_state.num_all_flags
                    n_d = self.env.envs[0].agent_state.num_detections
                self.log_metrics(iteration=self.iteration, result=self.train_result,
                                 episode_rewards=episode_rewards,
                                 episode_avg_loss=episode_loss,
                                 eval=False, lr=self.lr_schedule(self.num_timesteps),
                                 total_num_episodes=self.num_episodes_total,
                                 episode_steps=episode_steps,
                                 episode_flags=episode_flags, episode_flags_percentage=episode_flags_percentage,
                                 progress_left = self._current_progress_remaining,
                                 n_af = n_af,
                                 n_d = n_d,
                                 eval_episode_rewards = episode_rewards_1, eval_episode_steps=episode_steps_1,
                                 eval_episode_flags=episode_flags_1,
                                 eval_episode_flags_percentage=episode_flags_percentage_1,
                                 eval_2_episode_rewards=eval_episode_rewards,
                                 eval_2_episode_steps=eval_episode_steps,
                                 eval_2_episode_flags=eval_episode_flags,
                                 eval_2_episode_flags_percentage=eval_episode_flags_percentage
                                 )
                episode_rewards = []
                episode_loss = []
                episode_flags = []
                episode_steps = []
                episode_flags_percentage = []
                self.num_episodes = 0

            # Save models every <self.config.checkpoint_frequency> iterations
            if self.iteration % self.agent_config.checkpoint_freq == 0:
                try:
                    self.save_model()
                except Exception as e:
                    print("There was an error saving the model: {}".format(str(e)))
                if self.agent_config.save_dir is not None:
                    time_str = str(time.time())
                    self.train_result.to_csv(
                        self.agent_config.save_dir + "/" + time_str + "_train_results_checkpoint.csv")
                    self.eval_result.to_csv(
                        self.agent_config.save_dir + "/" + time_str + "_eval_results_checkpoint.csv")

            if not self.agent_config.ar_policy:
                entropy_loss, pg_loss, value_loss, lr = self.train()
            else:
                entropy_loss, pg_loss, value_loss, lr = self.train_ar()
            episode_loss.append(entropy_loss + pg_loss + value_loss)

        callback.on_training_end()

        return self

    def get_torch_variables(self) -> Tuple[List[str], List[str]]:
        """
        cf base class
        """
        if not self.agent_config.ar_policy:
            state_dicts = ["policy", "policy.optimizer"]
        else:
            state_dicts = ["m_selection_policy", "m_selection_policy.optimizer",
                           "m_action_policy", "m_action_policy.optimizer"]

        return state_dicts, []


    def step_policy(self, env, rollout_buffer):
        with th.no_grad():
            # Convert to pytorch tensor
            obs_tensor = th.as_tensor(self._last_obs).to(self.device)
            actions, values, log_probs = self.policy.forward(obs_tensor,  env=env, infos=self._last_infos)
        actions = actions.cpu().numpy()

        # Rescale and perform action
        clipped_actions = actions
        # Clip the actions to avoid out of bound error
        if isinstance(self.action_space, gym.spaces.Box):
            clipped_actions = np.clip(actions, self.action_space.low, self.action_space.high)

        new_obs, rewards, dones, infos = env.step(clipped_actions)
        if len(new_obs.shape) == 3:
            new_obs = new_obs.reshape((new_obs.shape[0], self.observation_space.shape[0]))

        if isinstance(self.action_space, gym.spaces.Discrete):
            # Reshape in case of discrete action
            actions = actions.reshape(-1, 1)

        rollout_buffer.add(self._last_obs, actions, rewards, self._last_dones, values, log_probs)

        self._last_obs = new_obs
        self._last_dones = dones
        self._last_infos = infos

        return new_obs, rewards, dones, infos, values, log_probs, actions

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
            actions = env.envs[0].convert_ar_action(m_selection_actions[0], m_actions[0])
            actions = np.array([actions])

        new_obs, rewards, dones, infos = env.step(actions)

        if isinstance(self.env.envs[0].m_selection_action_space, gym.spaces.Discrete):
            # Reshape in case of discrete action
            m_selection_actions = m_selection_actions.reshape(-1, 1)
        
        if isinstance(self.env.envs[0].m_action_space, gym.spaces.Discrete):
            # Reshape in case of discrete action
            m_actions = m_actions.reshape(-1, 1)

        rollout_buffer.add(self._last_obs, machine_obs, m_selection_actions, m_actions, rewards, self._last_dones,
                           m_selection_values, m_action_values, m_selection_log_probs, m_action_log_probs)

        self._last_obs = new_obs
        self._last_dones = dones
        self._last_infos = infos

        return new_obs, machine_obs, rewards, dones, infos, m_selection_values, m_action_values, m_selection_log_probs, \
               m_action_log_probs, m_selection_actions, m_actions
