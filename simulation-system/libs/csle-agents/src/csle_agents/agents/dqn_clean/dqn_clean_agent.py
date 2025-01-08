"""
MIT License

Copyright (c) 2019 CleanRL developers https://github.com/vwxyzjn/cleanrl
"""
from typing import List, Optional, Tuple, Any, Callable
import time
import torch
import torch.optim as optim
import gymnasium as gym
import os
import random
import torch.nn.functional as F
import numpy as np
from stable_baselines3.common.buffers import ReplayBuffer
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.training.experiment_config import ExperimentConfig
from gymnasium.wrappers.common import RecordEpisodeStatistics
from csle_common.dao.training.experiment_execution import ExperimentExecution
from csle_common.models.q_network import QNetwork
from csle_common.dao.training.experiment_result import ExperimentResult
from csle_common.dao.training.agent_type import AgentType
from csle_common.util.experiment_util import ExperimentUtil
from csle_common.logging.log import Logger
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.jobs.training_job_config import TrainingJobConfig
from csle_common.dao.training.dqn_policy import DQNPolicy
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
        self.cuda: bool = True
        self.learning_rate = self.experiment_config.hparams[agents_constants.COMMON.LEARNING_RATE].value
        self.start_e = 1
        self.end_e = 0.05
        self.num_envs = self.experiment_config.hparams[agents_constants.COMMON.NUM_PARALLEL_ENVS].value
        self.total_timesteps = self.experiment_config.hparams[agents_constants.COMMON.NUM_TRAINING_TIMESTEPS].value
        self.batch_size = self.experiment_config.hparams[agents_constants.COMMON.BATCH_SIZE].value
        self.num_iterations = self.total_timesteps // self.batch_size
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

    def linear_schedule(self, duration: int, t: int) -> float:
        """
        Linear exploration rate decay sechdule

        :param duration: the duration of training
        :param t: the current time
        :return: the new exploration rate
        """
        slope = (self.end_e - self.start_e) / duration
        return max(slope * t + self.start_e, self.end_e)

    def make_env(self) -> Callable[[], RecordEpisodeStatistics[Any, Any]]:
        """
        Helper function for creating an environment in training of the agent

        :return: environment creating function
        """

        def thunk() -> RecordEpisodeStatistics[Any, Any]:
            """
            The environment creating function
            """
            orig_env: BaseEnv = gym.make(self.simulation_env_config.gym_env_name, config=self.config)
            env = RecordEpisodeStatistics(orig_env)
            return env

        return thunk

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
        descr = f"Training of policies with Clean-DQN using " \
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
            # Train
            exp_result, env, model = self.run_dqn(exp_result=exp_result, seed=seed)

            # Save policy
            ts = time.time()
            save_path = f"{self.experiment_config.output_dir}/DQN_policy_seed_{seed}_{ts}.zip"
            model.save(save_path)
            action_space = \
                self.simulation_env_config.joint_action_space_config.action_spaces[
                    self.experiment_config.player_idx].actions
            policy = DQNPolicy(model=model, simulation_name=self.simulation_env_config.name,
                               save_path=save_path, player_type=self.experiment_config.player_type,
                               states=self.simulation_env_config.state_space_config.states,
                               actions=action_space,
                               experiment_config=self.experiment_config,
                               avg_R=exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN][-1])

            if self.save_to_metastore:
                MetastoreFacade.save_dqn_policy(dqn_policy=policy)
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

    def run_dqn(self, exp_result: ExperimentResult, seed: int) -> Tuple[ExperimentResult, BaseEnv, QNetwork]:
        """
        Runs DQN with given seed

        :param exp_result: the object to save the experiment results
        :param seed: the random seed
        :retur: the updated experiment results, the environment and the trained model
        """
        Logger.__call__().get_logger().info(f"[CleanDQN] Start training; seed: {seed}")
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
        input_dim = np.array(envs.single_observation_space.shape).prod()
        q_network = QNetwork(input_dim=input_dim, num_hidden_layers=self.num_hl,
                             hidden_layer_dim=self.num_hl_neur, agent_type=self.experiment_config.agent_type).to(device)
        optimizer = optim.Adam(q_network.parameters(), lr=self.learning_rate)
        target_network = QNetwork(input_dim=input_dim, num_hidden_layers=self.num_hl,
                                  hidden_layer_dim=self.num_hl_neur,
                                  agent_type=self.experiment_config.agent_type).to(device)

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

        obs: List[float] = envs.reset(seed=seed)[0]
        R: List[Any] = []
        T = []
        i = 0
        for global_step in range(self.total_timesteps):
            i += 1
            # ALGO LOGIC: put action logic here
            epsilon = self.linear_schedule(self.exploration_fraction * self.total_timesteps, global_step)
            if random.random() < epsilon:
                actions = np.array([envs.single_action_space.sample() for _ in range(envs.num_envs)])
            else:

                q_values = q_network(torch.Tensor(obs).to(device))
                actions = torch.argmax(q_values, dim=1).cpu().numpy()
                e_name = "csle-stopping-game-pomdp-defender-v1"
                if self.simulation_env_config.simulation_env_input_config.env_name == e_name:
                    actions[0] = random.randrange(0, 2)

            # Take a step in the environment
            next_obs, rewards, terminations, truncations, infos = envs.step(actions) # type: ignore

            # Record rewards for logging purposes
            if "final_info" in infos:
                R_sum = 0
                T_sum = 0
                for info in infos["final_info"]:
                    R_sum += info["R"]
                    T_sum += info["T"]
                R.append(R_sum)
                T.append(T_sum)

            # Save data to replay buffer
            real_next_obs = next_obs.copy()
            for idx, trunc in enumerate(truncations):
                if trunc and "final_observation" in infos:
                    real_next_obs[idx] = infos["final_observation"][idx]
            rb.add(obs, real_next_obs, actions, rewards, terminations, infos)  # type: ignore

            # Move to the next observation
            obs = next_obs

            # Optimizing the neural network based on data from the replay buffer
            if global_step > self.learning_starts:
                if global_step % self.train_frequency == 0:
                    data = rb.sample(self.batch_size)
                    with torch.no_grad():
                        target_max, _ = target_network(data.next_observations.to(dtype=torch.float32)).max(dim=1)
                        td_target = data.rewards.flatten() + self.gamma * target_max * (1 - data.dones.flatten())
                    old_val = q_network(data.observations.to(dtype=torch.float32)).gather(1, data.actions).squeeze()
                    loss = F.mse_loss(td_target, old_val)

                    # optimize the model
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()

                # update target network
                if global_step % self.target_network_frequency == 0:
                    for target_network_param, q_network_param in zip(target_network.parameters(),
                                                                     q_network.parameters()):
                        target_network_param.data.copy_(
                            self.tau * q_network_param.data + (1.0 - self.tau) * target_network_param.data
                        )
            # Logging
            if global_step > 10 and global_step % self.experiment_config.log_every == 0:
                time_elapsed_minutes = round((time.time() - start_time) / 60, 3)
                exp_result.all_metrics[seed][agents_constants.COMMON.RUNTIME].append(time_elapsed_minutes)
                avg_R = round(float(np.mean(R)), 3)
                exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN].append(round(avg_R, 3))
                avg_T = round(float(np.mean(T)), 3)
                exp_result.all_metrics[seed][
                    agents_constants.COMMON.AVERAGE_TIME_HORIZON].append(round(avg_T, 3))
                running_avg_J = ExperimentUtil.running_average(
                    exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN],
                    self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value
                )
                running_avg_T = ExperimentUtil.running_average(
                    exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_TIME_HORIZON],
                    self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value)
                exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN].append(
                    round(running_avg_J, 3))
                Logger.__call__().get_logger().info(
                    f"[CleanDQN] Iteration: {global_step}/{self.total_timesteps}, "
                    f"avg R: {avg_R}, "
                    f"R_avg_{self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value}:"
                    f"{running_avg_J}, Avg T:{round(avg_T, 3)}, "
                    f"Running_avg_{self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value}_T: "
                    f"{round(running_avg_T, 3)}, "
                    f"runtime: {time_elapsed_minutes} min")
        envs.close()

        base_env: BaseEnv = envs.envs[0].env.env.env  # type: ignore
        return exp_result, base_env, q_network

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
