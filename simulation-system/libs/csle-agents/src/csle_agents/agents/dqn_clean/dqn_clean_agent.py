"""
MIT License

Copyright (c) 2019 CleanRL developers https://github.com/vwxyzjn/cleanrl
"""
from typing import Union, List, Optional, Callable, Tuple
import time
import torch
import logging
import torch.optim as optim
import gymnasium as gym
import os
import random
import torch.nn.functional as F
import tyro
import numpy as np
from stable_baselines3.common.buffers import ReplayBuffer
from torch.utils.tensorboard import SummaryWriter
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.training.experiment_config import ExperimentConfig
from gymnasium.wrappers.record_episode_statistics import RecordEpisodeStatistics
from csle_common.dao.training.experiment_execution import ExperimentExecution
from csle_common.models.dqn_network import QNetwork
from csle_common.dao.training.experiment_result import ExperimentResult
from csle_common.dao.training.agent_type import AgentType
from csle_common.util.experiment_util import ExperimentUtil
from csle_common.logging.log import Logger
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.jobs.training_job_config import TrainingJobConfig
from csle_common.dao.training.dqn_policy import DQNPolicy
from csle_common.dao.simulation_config.state import State
from csle_common.dao.simulation_config.action import Action
from csle_common.dao.training.player_type import PlayerType
from csle_common.util.general_util import GeneralUtil
from csle_common.dao.simulation_config.base_env import BaseEnv
from csle_agents.agents.base.base_agent import BaseAgent
import csle_agents.constants.constants as agents_constants


class DQNCleanAgent(BaseAgent):
    """
    A DQN agent using the implementation from OpenAI baselines
    """
    def __init__(self, simulation_env_config: SimulationEnvConfig,
                 emulation_env_config: Optional[EmulationEnvConfig], experiment_config: ExperimentConfig,
                 training_job: Optional[TrainingJobConfig] = None, save_to_metastore: bool = True) -> None:
        """
        Initializes the agent

        :param simulation_env_config: the simulation environment configuration
        :param emulation_env_config: the emulation environment configuration
        :param experiment_config: the experiment configuration
        :param training_job: the training job configuration
        :param save_to_metastore: boolean flag indicating whether job information should be saved to the metastore
        """
        super(DQNCleanAgent, self).__init__(simulation_env_config=simulation_env_config,
                                            emulation_env_config=emulation_env_config,
                                            experiment_config=experiment_config)
        assert experiment_config.agent_type == AgentType.DQN_CLEAN
        self.training_job = training_job
        self.num_hl = self.experiment_config.hparams[constants.NEURAL_NETWORKS.NUM_HIDDEN_LAYERS].value
        self.num_hl_neur = self.experiment_config.hparams[constants.NEURAL_NETWORKS.NUM_NEURONS_PER_HIDDEN_LAYER].value
        self.config = self.simulation_env_config.simulation_env_input_config
        self.save_to_metastore = save_to_metastore
        self.exp_name: str = self.simulation_env_config.name
        self.env_id = self.simulation_env_config.gym_env_name
        self.torch_deterministic = True
        """if toggled, `torch.backends.cudnn.deterministic=False`"""
        self.cuda: bool = True
        self.learning_rate = self.experiment_config.hparams[agents_constants.COMMON.LEARNING_RATE].value
        """if toggled, cuda will be enabled by default"""
        """whether to capture videos of the agent performances (check out `videos` folder)"""
        self.start_e = 1
        self.end_e = 0.05
        self.num_envs = self.experiment_config.hparams[agents_constants.COMMON.NUM_PARALLEL_ENVS].value
        self.total_timesteps = self.experiment_config.hparams[
                    agents_constants.COMMON.NUM_TRAINING_TIMESTEPS].value

        self.batch_size = self.experiment_config.hparams[agents_constants.COMMON.BATCH_SIZE].value     
        self.gamma = self.experiment_config.hparams[agents_constants.COMMON.GAMMA].value
        self.tau = self.experiment_config.hparams[agents_constants.DQN_CLEAN.TAU].value
        self.exploration_fraction = self.experiment_config.hparams[agents_constants.DQN_CLEAN.EXP_FRAC].value
        self.learning_starts = self.experiment_config.hparams[agents_constants.DQN_CLEAN.LEARNING_STARTS].value
        self.train_frequency = self.experiment_config.hparams[agents_constants.DQN_CLEAN.TRAIN_FREQ].value
        self.target_network_frequency = self.experiment_config.hparams[agents_constants.DQN_CLEAN.T_N_FREQ].value
        self.buffer_size = self.experiment_config.hparams[agents_constants.DQN_CLEAN.BUFFER_SIZE].value
        self.save_model = self.experiment_config.hparams[agents_constants.DQN_CLEAN.SAVE_MODEL].value
        self.device = self.experiment_config.hparams[constants.NEURAL_NETWORKS.DEVICE].value
        self.orig_env: BaseEnv = gym.make(self.simulation_env_config.gym_env_name, config=self.config)
        # Algorithm specific arguments


    def linear_schedule(self, duration: int, t: int):
        slope = (self.end_e - self.start_e) / duration
        return max(slope * t + self.start_e, self.end_e)

    def make_env(self):
        """Helper function for creating an environment in training of the agent
        :return: environment creating function
        """
        def thunk():
            """
            The environment creating function
            """
            orig_env: BaseEnv = gym.make(self.simulation_env_config.gym_env_name, config=self.config)
            env = RecordEpisodeStatistics(orig_env)
            return env

        return thunk

    '''def make_env(self, seed, idx, run_name):
        def thunk():
            env = gym.make(self.env_id, config=self.config)
            env = gym.wrappers.RecordEpisodeStatistics(env)
            return env

        return thunk'''

    def train(self) -> ExperimentExecution:
        """
        Implements the training logic of the DQN algorithm

        :return: the experiment result
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
        descr = f"Training of policies with DQN using " \
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
        simulation_name = self.simulation_env_config.name
        emulation_name = ""
        if self.emulation_env_config is not None:
            emulation_name = self.emulation_env_config.name
        if self.emulation_env_config is not None:
            emulation_name = self.emulation_env_config.name
        self.exp_execution = ExperimentExecution(
            result=exp_result, config=self.experiment_config, timestamp=ts,
            emulation_name=emulation_name, simulation_name=simulation_name,
            descr=descr, log_file_path=self.training_job.log_file_path)
        exp_execution_id = -1
        if self.save_to_metastore:
            exp_execution_id = MetastoreFacade.save_experiment_execution(self.exp_execution)
        self.exp_execution.id = exp_execution_id


        # Training runs, one per seed
        for seed in self.experiment_config.random_seeds:
            assert self.num_envs == 1, "vectorized envs are not supported at the moment"
            run_name = f"{self.env_id}__{self.exp_name}__{seed}__{int(time.time())}"
            
            
            exp_result, env, model = self.run_dqn(exp_result=exp_result, seed=seed)


    def run_dqn(self, exp_result: ExperimentResult, seed: int) -> Tuple[ExperimentResult, BaseEnv, QNetwork]:
        """
        Runs DQN with given seed

        :param exp_result: the object to save the experiment results
        :param seed: the random seed
        :retur: the updated experiment results, the environment and the trained model
        """
        Logger.__call__().get_logger().info(f"[CleanPPO] Start training; seed: {seed}")
        # writer = SummaryWriter(f"runs/{run_name}")
        envs = gym.vector.SyncVectorEnv([self.make_env() for _ in range(self.num_envs)])
        assert isinstance(envs.single_action_space, gym.spaces.Discrete), "only discrete action space is supported"
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
        device = torch.device(agents_constants.DQN_CLEAN.CUDA if torch.cuda.is_available() and cuda else
                              self.experiment_config.hparams[constants.NEURAL_NETWORKS.DEVICE].value)

        q_network = QNetwork(envs=envs, num_hl=self.num_hl, num_hl_neur=self.num_hl_neur).to(device)
        optimizer = optim.Adam(q_network.parameters(), lr=self.learning_rate)
        target_network = QNetwork(envs=envs, num_hl=self.num_hl, num_hl_neur=self.num_hl_neur).to(device)

        # Seeding
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.backends.cudnn.deterministic = self.torch_deterministic

        target_network.load_state_dict(q_network.state_dict())

        rb = ReplayBuffer(
            self.buffer_size,
            envs.single_observation_space,
            envs.single_action_space,
            device,
            handle_timeout_termination=False,
        )
        start_time = time.time()

        # TRY NOT TO MODIFY: start the game
        obs, _ = envs.reset(seed=seed)
        for global_step in range(self.total_timesteps):
            # ALGO LOGIC: put action logic here
            epsilon = self.linear_schedule(self.exploration_fraction * self.total_timesteps, global_step)
            if random.random() < epsilon:
                actions = np.array([envs.single_action_space.sample() for _ in range(envs.num_envs)])
            else:
                q_values = q_network(torch.Tensor(obs).to(device))
                actions = torch.argmax(q_values, dim=1).cpu().numpy()

            values = torch.zeros((self.num_steps, self.num_envs)).to(device)
            dones = torch.zeros((self.num_steps, self.num_envs)).to(device)
            rewards = torch.zeros((self.num_steps, self.num_envs)).to(device)
            logprobs = torch.zeros((self.num_steps, self.num_envs)).to(device)

            # TRY NOT TO MODIFY: execute the game and log data.
            next_obs, rewards, terminations, truncations, infos = envs.step(actions)

            returns, advantages = self.generalized_advantage_estimation(model=q_network, next_obs=next_obs, rewards=rewards,
                                                                        device=device, next_done=next_done,
                                                                        dones=dones, values=values)

            # TRY NOT TO MODIFY: record rewards for plotting purposes
            if "final_info" in infos:
                for info in infos["final_info"]:
                    if info and "episode" in info:
                        print(f"global_step={global_step}, episodic_return={info['episode']['r']}")

            # TRY NOT TO MODIFY: save data to reply buffer; handle `final_observation`
            real_next_obs = next_obs.copy()
            for idx, trunc in enumerate(truncations):
                if trunc:
                    real_next_obs[idx] = infos["final_observation"][idx]
            rb.add(obs, real_next_obs, actions, rewards, terminations, infos)

            # TRY NOT TO MODIFY: CRUCIAL step easy to overlook
            obs = next_obs
            # ALGO LOGIC: training.
            if global_step > self.learning_starts:
                if global_step % self.train_frequency == 0:
                    data = rb.sample(self.batch_size)
                    with torch.no_grad():
                        target_max, _ = target_network(data.next_observations.to(dtype=torch.float32)).max(dim=1)
                        td_target = data.rewards.flatten() + self.gamma * target_max * (1 - data.dones.flatten())
                    old_val = q_network(data.observations.to(dtype=torch.float32)).gather(1, data.actions).squeeze()
                    loss = F.mse_loss(td_target, old_val)

                    if global_step % 100 == 0:
                        print("SPS:", int(global_step / (time.time() - start_time)))
                    # optimize the model
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()

                # update target network
                if global_step % self.target_network_frequency == 0:
                    for target_network_param, q_network_param in zip(target_network.parameters(), q_network.parameters()):
                        target_network_param.data.copy_(
                            self.tau * q_network_param.data + (1.0 - self.tau) * target_network_param.data
                        )
        # Logging
        time_elapsed_minutes = round((time.time() - start_time) / 60, 3)
        exp_result.all_metrics[seed][agents_constants.COMMON.RUNTIME].append(time_elapsed_minutes)
        avg_R = round(float(np.mean(returns.flatten().cpu().numpy())), 3)
        exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN].append(round(avg_R, 3))
        # avg_T = float(np.mean(horizons))
        # exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_TIME_HORIZON].append(
        #     round(avg_T, 3))
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
        # Logger.__call__().get_logger().info(
        #     f"[CleanPPO] Iteration: {iteration}/{self.num_iterations}, "
        #     f"avg R: {avg_R}, "
        #     f"R_avg_{self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value}:"
        #     f"{running_avg_J}, Avg T:{round(avg_T, 3)}, "
        #     f"Running_avg_{self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value}_T: "
        #     f"{round(running_avg_T, 3)}, "
        #     f"runtime: {time_elapsed_minutes} min")
        envs.close()
        base_env: BaseEnv = envs.envs[0].env.env.env
        return exp_result, base_env, q_network
                        
    def generalized_advantage_estimation(self, model: QNetwork, next_obs: torch.Tensor, rewards: torch.Tensor,
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
        Gets the hyperparameters

        :return: a list with the hyperparameter names
        """
        return [constants.NEURAL_NETWORKS.NUM_NEURONS_PER_HIDDEN_LAYER,
                constants.NEURAL_NETWORKS.NUM_HIDDEN_LAYERS,
                agents_constants.COMMON.LEARNING_RATE, agents_constants.COMMON.BATCH_SIZE,
                agents_constants.COMMON.GAMMA,
                agents_constants.COMMON.NUM_TRAINING_TIMESTEPS, agents_constants.COMMON.EVAL_EVERY,
                agents_constants.COMMON.EVAL_BATCH_SIZE,
                constants.NEURAL_NETWORKS.DEVICE,
                agents_constants.COMMON.SAVE_EVERY, agents_constants.DQN.EXPLORATION_INITIAL_EPS,
                agents_constants.DQN.EXPLORATION_FINAL_EPS, agents_constants.DQN.EXPLORATION_FRACTION,
                agents_constants.DQN.MLP_POLICY, agents_constants.DQN.MAX_GRAD_NORM,
                agents_constants.DQN.GRADIENT_STEPS, agents_constants.DQN.N_EPISODES_ROLLOUT,
                agents_constants.DQN.TARGET_UPDATE_INTERVAL, agents_constants.DQN.LEARNING_STARTS,
                agents_constants.DQN.BUFFER_SIZE, agents_constants.DQN.DQN_BATCH_SIZE]