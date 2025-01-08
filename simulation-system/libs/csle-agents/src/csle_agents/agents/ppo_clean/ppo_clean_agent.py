"""
MIT License

Copyright (c) 2019 CleanRL developers https://github.com/vwxyzjn/cleanrl
"""

from typing import Union, List, Optional, Callable, Tuple, Any
import random
import time
import gymnasium as gym
from gymnasium.wrappers.common import RecordEpisodeStatistics
from gymnasium.spaces.discrete import Discrete
import os
import numpy as np
import torch
import torch.nn.utils.clip_grad as clip_grad
import torch.optim as optim
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.experiment_execution import ExperimentExecution
from csle_common.dao.training.experiment_result import ExperimentResult
from csle_common.dao.training.agent_type import AgentType
from csle_common.util.experiment_util import ExperimentUtil
from csle_common.logging.log import Logger
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.jobs.training_job_config import TrainingJobConfig
from csle_common.util.general_util import GeneralUtil
from csle_common.dao.simulation_config.base_env import BaseEnv
from csle_common.dao.training.ppo_policy import PPOPolicy
from csle_agents.agents.base.base_agent import BaseAgent
from csle_common.models.ppo_network import PPONetwork
import csle_agents.constants.constants as agents_constants


class PPOCleanAgent(BaseAgent):
    """
    A PPO agent using the implementation from CleanRL
    """

    def __init__(self, simulation_env_config: SimulationEnvConfig,
                 emulation_env_config: Union[None, EmulationEnvConfig], experiment_config: ExperimentConfig,
                 training_job: Optional[TrainingJobConfig] = None, save_to_metastore: bool = True) -> None:
        """
        Initializes the agent, and sets the hyperparameters as attributes of the class representing the agent.

        :param simulation_env_config: the simulation environment configuration
        :param emulation_env_config: the emulation environment configuration
        :param experiment_config: the experiment configuration
        :param training_job: the training job
        :param save_to_metastore: boolean flag indicating whether the results should be saved to the metastore or not
        """
        super(PPOCleanAgent, self).__init__(simulation_env_config=simulation_env_config,
                                            emulation_env_config=emulation_env_config,
                                            experiment_config=experiment_config)
        assert experiment_config.agent_type == AgentType.PPO_CLEAN
        self.training_job = training_job
        self.save_to_metastore = save_to_metastore
        self.num_steps = self.experiment_config.hparams[agents_constants.PPO_CLEAN.NUM_STEPS].value
        self.num_envs = self.experiment_config.hparams[agents_constants.COMMON.NUM_PARALLEL_ENVS].value
        self.batch_size = self.experiment_config.hparams[agents_constants.COMMON.BATCH_SIZE].value
        self.total_timesteps = self.experiment_config.hparams[
            agents_constants.COMMON.NUM_TRAINING_TIMESTEPS].value
        self.num_minibatches = self.experiment_config.hparams[agents_constants.PPO_CLEAN.NUM_MINIBATCHES].value
        self.minibatch_size = int(self.batch_size // self.num_minibatches)
        self.num_iterations = self.total_timesteps // self.batch_size
        self.update_epochs = self.experiment_config.hparams[agents_constants.PPO_CLEAN.UPDATE_EPOCHS].value
        self.clip_coef = self.experiment_config.hparams[agents_constants.PPO_CLEAN.CLIP_RANGE].value
        self.clip_vloss = self.experiment_config.hparams[agents_constants.PPO_CLEAN.CLIP_VLOSS].value
        self.norm_adv = self.experiment_config.hparams[agents_constants.PPO_CLEAN.NORM_ADV].value
        self.vf_coef = self.experiment_config.hparams[agents_constants.PPO_CLEAN.CLIP_RANGE_VF].value
        self.ent_coef = self.experiment_config.hparams[agents_constants.PPO_CLEAN.ENT_COEF].value
        self.max_grad_norm = self.experiment_config.hparams[agents_constants.PPO_CLEAN.MAX_GRAD_NORM].value
        self.target_kl = None
        if self.experiment_config.hparams[agents_constants.PPO_CLEAN.TARGET_KL].value != -1:
            self.target_kl = self.experiment_config.hparams[agents_constants.PPO_CLEAN.TARGET_KL].value
        self.anneal_lr = self.experiment_config.hparams[agents_constants.PPO_CLEAN.ANNEAL_LR].value
        self.gamma = self.experiment_config.hparams[agents_constants.COMMON.GAMMA].value
        self.gae_lambda = self.experiment_config.hparams[agents_constants.PPO_CLEAN.GAE_LAMBDA].value
        self.learning_rate = self.experiment_config.hparams[agents_constants.COMMON.LEARNING_RATE].value
        config = self.simulation_env_config.simulation_env_input_config
        self.orig_env: BaseEnv = gym.make(self.simulation_env_config.gym_env_name, config=config)

    def train(self) -> ExperimentExecution:
        """
        Runs the training process

        :return: the results
        """
        pid = os.getpid()

        # Setup experiment metrics
        exp_result = ExperimentResult()
        exp_result.plot_metrics.append(agents_constants.COMMON.AVERAGE_RETURN)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_RETURN)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON)
        exp_result.plot_metrics.append(agents_constants.COMMON.AVERAGE_TIME_HORIZON)
        exp_result.plot_metrics.append(agents_constants.COMMON.AVERAGE_UPPER_BOUND_RETURN)
        exp_result.plot_metrics.append(agents_constants.COMMON.AVERAGE_RANDOM_RETURN)
        exp_result.plot_metrics.append(agents_constants.COMMON.AVERAGE_HEURISTIC_RETURN)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNTIME)
        descr = f"Training of policies with Clean-PPO using " \
                f"simulation:{self.simulation_env_config.name}"

        # Setup training job
        if self.training_job is None:
            emulation_name = ""
            if self.emulation_env_config is not None:
                emulation_name = self.emulation_env_config.name
            self.training_job = TrainingJobConfig(
                simulation_env_name=self.simulation_env_config.name, experiment_config=self.experiment_config,
                progress_percentage=0, pid=pid, experiment_result=exp_result,
                emulation_env_name=emulation_name, simulation_traces=[],
                num_cached_traces=agents_constants.COMMON.NUM_CACHED_SIMULATION_TRACES,
                log_file_path=Logger.__call__().get_log_file_path(), descr=descr,
                physical_host_ip=GeneralUtil.get_host_ip())
            training_job_id = -1
            if self.save_to_metastore:
                training_job_id = MetastoreFacade.save_training_job(training_job=self.training_job)
            self.training_job.id = training_job_id
        else:
            self.training_job.pid = pid
            self.training_job.progress_percentage = 0
            self.training_job.experiment_result = exp_result
            if self.save_to_metastore:
                MetastoreFacade.update_training_job(training_job=self.training_job, id=self.training_job.id)

        # Setup experiment execution
        ts = time.time()
        emulation_name = ""
        if self.emulation_env_config is not None:
            emulation_name = self.emulation_env_config.name
        simulation_name = self.simulation_env_config.name
        self.exp_execution = ExperimentExecution(
            result=exp_result, config=self.experiment_config, timestamp=ts,
            emulation_name=emulation_name, simulation_name=simulation_name, descr=descr,
            log_file_path=self.training_job.log_file_path)
        exp_execution_id = -1
        if self.save_to_metastore:
            exp_execution_id = MetastoreFacade.save_experiment_execution(self.exp_execution)
        self.exp_execution.id = exp_execution_id

        # Training runs, one per seed
        for seed in self.experiment_config.random_seeds:

            # Train
            exp_result, env, model = self.run_ppo(exp_result=exp_result, seed=seed)

            # Save policy
            ts = time.time()
            save_path = f"{self.experiment_config.output_dir}/ppo_policy_seed_{seed}_{ts}.zip"
            model.save(save_path)
            policy = PPOPolicy(
                model=model, simulation_name=self.simulation_env_config.name, save_path=save_path,
                states=self.simulation_env_config.state_space_config.states,
                actions=self.simulation_env_config.joint_action_space_config.action_spaces[
                    self.experiment_config.player_idx].actions, player_type=self.experiment_config.player_type,
                experiment_config=self.experiment_config,
                avg_R=exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN][-1])
            exp_result.policies[seed] = policy

            # Save policy metadata
            if self.save_to_metastore:
                MetastoreFacade.save_ppo_policy(ppo_policy=policy)
                os.chmod(save_path, 0o777)

            # Save trace
            traces = env.get_traces()
            if len(traces) > 0 and self.save_to_metastore:
                MetastoreFacade.save_simulation_trace(traces[-1])
            env.reset_traces()

        # Calculate average and std metrics
        exp_result.avg_metrics = {}
        exp_result.std_metrics = {}
        for metric in exp_result.all_metrics[self.experiment_config.random_seeds[0]].keys():
            value_vectors = []
            for seed in self.experiment_config.random_seeds:
                value_vectors.append(exp_result.all_metrics[seed][metric])

            avg_metrics = []
            std_metrics = []
            for i in range(len(value_vectors[0])):
                seed_values = []
                for seed_idx in range(len(self.experiment_config.random_seeds)):
                    seed_values.append(value_vectors[seed_idx][i])
                avg_metrics.append(ExperimentUtil.mean_confidence_interval(
                    data=seed_values,
                    confidence=self.experiment_config.hparams[agents_constants.COMMON.CONFIDENCE_INTERVAL].value)[0])
                std_metrics.append(ExperimentUtil.mean_confidence_interval(
                    data=seed_values,
                    confidence=self.experiment_config.hparams[agents_constants.COMMON.CONFIDENCE_INTERVAL].value)[1])
            exp_result.avg_metrics[metric] = avg_metrics
            exp_result.std_metrics[metric] = std_metrics
        return self.exp_execution

    def run_ppo(self, exp_result: ExperimentResult, seed: int) -> Tuple[ExperimentResult, BaseEnv, PPONetwork]:
        """
        Runs PPO with a given seed

        :param exp_result: the object to save the experiment results
        :param seed: the random seed
        :return: the updated experiment results, the environment, and the trained model
        """
        Logger.__call__().get_logger().info(f"[CleanPPO] Start training; seed: {seed}")

        envs = gym.vector.SyncVectorEnv([self.make_env() for _ in range(self.num_envs)])

        # Setup training metrics
        exp_result.all_metrics[seed] = {}
        exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN] = []
        exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN] = []
        exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON] = []
        exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_TIME_HORIZON] = []
        exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_UPPER_BOUND_RETURN] = []
        exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RANDOM_RETURN] = []
        exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_HEURISTIC_RETURN] = []
        exp_result.all_metrics[seed][agents_constants.COMMON.RUNTIME] = []
        ExperimentUtil.set_seed(seed)
        cuda = False

        # Create neural network
        device = torch.device(agents_constants.PPO_CLEAN.CUDA if torch.cuda.is_available() and cuda else
                              self.experiment_config.hparams[constants.NEURAL_NETWORKS.DEVICE].value)
        num_hidden_layers = self.experiment_config.hparams[constants.NEURAL_NETWORKS.NUM_HIDDEN_LAYERS].value
        hidden_layer_dim = self.experiment_config.hparams[constants.NEURAL_NETWORKS.NUM_NEURONS_PER_HIDDEN_LAYER].value
        input_dim = np.array(envs.single_observation_space.shape).prod()
        env: BaseEnv = self.orig_env
        action_space: Discrete = env.action_space
        action_dim = int(action_space.n)
        model = PPONetwork(input_dim=input_dim, output_dim_critic=1, output_dim_action=action_dim,
                           num_hidden_layers=num_hidden_layers, hidden_layer_dim=hidden_layer_dim).to(device)

        # seeding
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.backends.cudnn.deterministic = True

        # Setup gym environment
        obs_shape: Tuple[int, ...] = (1,)
        action_shape: Tuple[int, ...] = (1,)
        if envs.single_observation_space.shape is not None:
            obs_shape = envs.single_observation_space.shape
        if envs.single_action_space.shape is not None:
            action_shape = envs.single_action_space.shape
        obs = torch.zeros((self.num_steps, self.num_envs) + obs_shape).to(device)
        actions = torch.zeros((self.num_steps, self.num_envs) + action_shape).to(device)
        logprobs = torch.zeros((self.num_steps, self.num_envs)).to(device)
        rewards = torch.zeros((self.num_steps, self.num_envs)).to(device)
        dones = torch.zeros((self.num_steps, self.num_envs)).to(device)
        values = torch.zeros((self.num_steps, self.num_envs)).to(device)
        horizons: List[int] = []

        # Initialize the environment and optimizers
        global_step = 0
        start_time = time.time()
        next_obs = torch.Tensor(envs.reset(seed=seed)[0]).to(device)
        next_done = torch.zeros(self.num_envs).to(device)
        optimizer = optim.Adam(model.parameters(), lr=self.learning_rate, eps=1e-5)

        # Training
        for iteration in range(1, self.num_iterations + 1):
            # Annealing the rate if instructed to do so.
            if self.anneal_lr:
                frac = 1.0 - (iteration - 1.0) / self.num_iterations
                lrnow = frac * self.learning_rate
                optimizer.param_groups[0]["lr"] = lrnow
            next_obs, next_done, global_step, horizons = \
                self.update_trajectory_buffers(global_step=global_step, envs=envs, obs=obs, dones=dones,
                                               actions=actions, rewards=rewards, device=device,
                                               logprobs=logprobs, values=values, model=model, next_obs=next_obs,
                                               next_done=next_done, horizons=horizons)

            returns, advantages = self.generalized_advantage_estimation(model=model, next_obs=next_obs, rewards=rewards,
                                                                        device=device, next_done=next_done,
                                                                        dones=dones, values=values)

            # flatten the batch
            b_obs = obs.reshape((-1,) + obs_shape)
            b_logprobs = logprobs.reshape(-1)
            b_actions = actions.reshape((-1,) + action_shape)
            b_advantages = advantages.reshape(-1)
            b_returns = returns.reshape(-1)
            b_values = values.reshape(-1)

            # Optimizing the policy and value network
            b_inds = np.arange(self.batch_size)
            clipfracs = []
            for epoch in range(self.update_epochs):
                np.random.shuffle(b_inds)
                for start in range(0, self.batch_size, self.minibatch_size):
                    end = start + self.minibatch_size
                    mb_inds = list(b_inds[start:end])

                    _, newlogprob, entropy, newvalue = \
                        model.get_action_and_value(b_obs[mb_inds], b_actions.long()[mb_inds])
                    logratio = newlogprob - b_logprobs[mb_inds]
                    ratio = logratio.exp()

                    with torch.no_grad():
                        # calculate approx_kl http://joschu.net/blog/kl-approx.html
                        approx_kl = ((ratio - 1) - logratio).mean()
                        clipfracs += [((ratio - 1.0).abs() > self.clip_coef).float().mean().item()]

                    mb_advantages = b_advantages[mb_inds]
                    if self.norm_adv:
                        mb_advantages = (mb_advantages - mb_advantages.mean()) / (mb_advantages.std() + 1e-8)

                    # Policy loss
                    pg_loss1 = -mb_advantages * ratio
                    pg_loss2 = -mb_advantages * torch.clamp(ratio, 1 - self.clip_coef, 1 + self.clip_coef)
                    pg_loss = torch.max(pg_loss1, pg_loss2).mean()

                    # Value loss
                    newvalue = newvalue.view(-1)
                    if self.clip_vloss:
                        v_loss_unclipped = (newvalue - b_returns[mb_inds]) ** 2
                        v_clipped = b_values[mb_inds] + torch.clamp(
                            newvalue - b_values[mb_inds],
                            -self.clip_coef,
                            self.clip_coef,
                        )
                        v_loss_clipped = (v_clipped - b_returns[mb_inds]) ** 2
                        v_loss_max = torch.max(v_loss_unclipped, v_loss_clipped)
                        v_loss = 0.5 * v_loss_max.mean()
                    else:
                        v_loss = 0.5 * ((newvalue - b_returns[mb_inds]) ** 2).mean()

                    # Entropy loss
                    entropy_loss = entropy.mean()

                    # Total loss
                    loss = pg_loss - self.ent_coef * entropy_loss + v_loss * self.vf_coef

                    # Backpropagation and update weights
                    optimizer.zero_grad()
                    loss.backward()
                    clip_grad.clip_grad_norm_(model.parameters(), self.max_grad_norm)
                    optimizer.step()

                if self.target_kl is not None and approx_kl > self.target_kl:
                    break

            # Logging
            time_elapsed_minutes = round((time.time() - start_time) / 60, 3)
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNTIME].append(time_elapsed_minutes)
            avg_R = round(float(np.mean(returns.flatten().cpu().numpy())), 3)
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN].append(round(avg_R, 3))
            avg_T = float(np.mean(horizons))
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_TIME_HORIZON].append(
                round(avg_T, 3))
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNTIME].append(time_elapsed_minutes)
            running_avg_J = ExperimentUtil.running_average(
                exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN],
                self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value)
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN].append(
                round(running_avg_J, 3))
            running_avg_T = ExperimentUtil.running_average(
                exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_TIME_HORIZON],
                self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value)
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON].append(
                round(running_avg_T, 3))
            Logger.__call__().get_logger().info(
                f"[CleanPPO] Iteration: {iteration}/{self.num_iterations}, "
                f"avg R: {avg_R}, "
                f"R_avg_{self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value}:"
                f"{running_avg_J}, Avg T:{round(avg_T, 3)}, "
                f"Running_avg_{self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value}_T: "
                f"{round(running_avg_T, 3)}, "
                f"runtime: {time_elapsed_minutes} min")

        envs.close()
        base_env: BaseEnv = envs.envs[0].env.env.env  # type: ignore
        return exp_result, base_env, model

    def make_env(self) -> Callable[[], RecordEpisodeStatistics[Any, Any]]:
        """
        Helper function for creating the environment to use for training

        :return: a function that creates the environment
        """

        def thunk() -> RecordEpisodeStatistics[Any, Any]:
            """
            Function for creating a new environment

            :return: the created environment
            """
            config = self.simulation_env_config.simulation_env_input_config
            orig_env: BaseEnv = gym.make(self.simulation_env_config.gym_env_name, config=config)
            env = RecordEpisodeStatistics(orig_env)
            return env

        return thunk

    def update_trajectory_buffers(self, global_step: int, envs: gym.vector.SyncVectorEnv, obs: torch.Tensor,
                                  dones: torch.Tensor, actions: torch.Tensor, rewards: torch.Tensor,
                                  device: torch.device, logprobs: torch.Tensor, values: torch.Tensor,
                                  model: PPONetwork, next_obs: torch.Tensor, next_done: torch.Tensor,
                                  horizons: List[int]) \
            -> Tuple[torch.Tensor, torch.Tensor, int, List[int]]:
        """
        Updates the buffers of trajectories collected from the environment

        :param global step: the global step in the iteration
        :param envs: list of environments
        :param obs: torch tensor of observations
        :param dones: tensor of done events
        :param actions: tensor of available actions
        :param rewards: tensor of available rewards
        :param device: the device acted upon
        :param logprobs: logarithmic probabilities
        :param horizons: list of time horizons
        :param values: tensor of values
        :param model: the neural network model
        :param next_obs: the next observation
        :param next_done: logical or operation between terminations and truncations
        :return: next_obs, next_done, global_step
        """
        step_dones = [0] * self.num_envs
        for step in range(0, self.num_steps):
            global_step += self.num_envs
            obs[step] = next_obs
            dones[step] = next_done
            for i, d in enumerate(next_done.cpu().numpy()):
                if float(d) == 1.0:
                    horizons.append(step - step_dones[i])
                    step_dones[i] = step
            with torch.no_grad():
                action, logprob, _, value = model.get_action_and_value(next_obs)
                values[step] = value.flatten()
            actions[step] = action
            logprobs[step] = logprob

            # Step the environment
            next_obs, reward, terminations, truncations, infos = envs.step(action.cpu().numpy()) # type: ignore
            next_done_np = np.logical_or(terminations, truncations)
            rewards[step] = torch.tensor(reward).to(device).view(-1)
            next_obs, next_done = torch.Tensor(next_obs).to(device), torch.Tensor(next_done_np).to(device)
        return next_obs, next_done, global_step, horizons

    def generalized_advantage_estimation(self, model: PPONetwork, next_obs: torch.Tensor, rewards: torch.Tensor,
                                         device: torch.device, next_done: torch.Tensor, dones: torch.Tensor,
                                         values: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Computes the generalized advantage estimation (i.e., exponentially weighted average of n-step returns)
        See (HIGH-DIMENSIONAL CONTINUOUS CONTROL USING GENERALIZED ADVANTAGE ESTIMATION, 2016, ICLR)

        :param device: the device acted upon
        :param values: tensor of values
        :param model: the neural network model
        :param rewards: tensor of available rewards
        :param next_obs: the next observation
        :param dones: tensor of done events
        :param next_done: logical or operation between terminations and truncations
        :return: returns, advantages
        """
        with torch.no_grad():
            next_value = model.get_value(next_obs).reshape(1, -1)
            advantages = torch.zeros_like(rewards).to(device)
            lastgaelam = 0
            for t in reversed(range(self.num_steps)):
                if t == self.num_steps - 1:
                    nextnonterminal = 1.0 - next_done
                    nextvalues = next_value
                else:
                    nextnonterminal = 1.0 - dones[t + 1]
                    nextvalues = values[t + 1]
                delta = rewards[t] + self.gamma * nextvalues * nextnonterminal - values[t]
                advantages[t] = lastgaelam = delta + self.gamma * self.gae_lambda * nextnonterminal * lastgaelam
            returns = advantages + values
            return returns, advantages

    def hparam_names(self) -> List[str]:
        """
        :return: a list with the hyperparameter names
        """
        return [constants.NEURAL_NETWORKS.NUM_NEURONS_PER_HIDDEN_LAYER,
                constants.NEURAL_NETWORKS.NUM_HIDDEN_LAYERS,
                agents_constants.PPO_CLEAN.NUM_MINIBATCHES,
                agents_constants.COMMON.NUM_PARALLEL_ENVS, agents_constants.COMMON.BATCH_SIZE,
                agents_constants.COMMON.NUM_TRAINING_TIMESTEPS, agents_constants.PPO_CLEAN.GAE_LAMBDA,
                agents_constants.PPO_CLEAN.CLIP_RANGE, agents_constants.COMMON.LEARNING_RATE,
                agents_constants.PPO_CLEAN.NORM_ADV, agents_constants.COMMON.GAMMA,
                agents_constants.PPO_CLEAN.CLIP_RANGE_VF, agents_constants.PPO_CLEAN.ENT_COEF,
                agents_constants.PPO_CLEAN.VF_COEF, agents_constants.PPO_CLEAN.UPDATE_EPOCHS,
                agents_constants.PPO_CLEAN.TARGET_KL, agents_constants.PPO_CLEAN.MAX_GRAD_NORM,
                agents_constants.COMMON.EVAL_EVERY, constants.NEURAL_NETWORKS.DEVICE,
                agents_constants.PPO_CLEAN.CLIP_VLOSS, agents_constants.PPO_CLEAN.ANNEAL_LR,
                agents_constants.COMMON.SAVE_EVERY]
