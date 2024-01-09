"""
MIT License

Copyright (c) 2019 CleanRL developers https://github.com/vwxyzjn/cleanrl
"""
from typing import List, Optional
import time
import torch
import torch.optim as optim
import gymnasium as gym
import os
import random
import tyro
import numpy as np
from stable_baselines3.common.buffers import ReplayBuffer
from torch.utils.tensorboard import SummaryWriter
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.training.experiment_config import ExperimentConfig
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
        # print(experiment_config.agent_type)
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
        # Algorithm specific arguments
        env_id: str = "CartPole-v1"
        """the id of the environment"""
        total_timesteps: int = 500000
        """total timesteps of the experiments"""
        learning_rate: float = 2.5e-4
        """the number of parallel game environments"""
        buffer_size: int = 10000
        """the replay memory buffer size"""
        gamma: float = 0.99
        """the discount factor gamma"""
        tau: float = 1.0
        """the target network update rate"""
        target_network_frequency: int = 500
        """the batch size of sample from the reply memory"""
        start_e: float = 1
        """the starting epsilon for exploration"""
        end_e: float = 0.05
        """the ending epsilon for exploration"""
        exploration_fraction: float = 0.5
        """the fraction of `total-timesteps` it takes from start-e to go end-e"""
        learning_starts: int = 10000
        """timestep to start learning"""
        train_frequency: int = 10
        """the frequency of training"""


    def linear_schedule(self, start_e: float, end_e: float, duration: int, t: int):
        slope = (end_e - start_e) / duration
        return max(slope * t + start_e, end_e)

    def make_env(self, seed, idx, run_name):
        def thunk():
            env = gym.make(self.env_id, config=self.config)
            env = gym.wrappers.RecordEpisodeStatistics(env)
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
            training_job_id = MetastoreFacade.save_training_job(training_job=self.training_job)
            self.training_job.id = training_job_id
        else:
            self.training_job.pid = pid
            self.training_job.progress_percentage = 0
            self.training_job.experiment_result = exp_result
            MetastoreFacade.update_training_job(training_job=self.training_job, id=self.training_job.id)

        # Setup experiment execution
        ts = time.time()
        simulation_name = self.simulation_env_config.name
        emulation_name = ""
        if self.emulation_env_config is not None:
            emulation_name = self.emulation_env_config.name
        self.exp_execution = ExperimentExecution(
            result=exp_result, config=self.experiment_config, timestamp=ts,
            emulation_name=emulation_name, simulation_name=simulation_name,
            descr=descr, log_file_path=self.training_job.log_file_path)
        exp_execution_id = MetastoreFacade.save_experiment_execution(self.exp_execution)
        self.exp_execution.id = exp_execution_id

        # Setup gym environment
        # config = self.simulation_env_config.simulation_env_input_config
        # orig_env: BaseEnv = gym.make(self.simulation_env_config.gym_env_name, config=config)

        # Training runs, one per seed
        for seed in self.experiment_config.random_seeds:

            # args = tyro.cli(Args)
            assert self.num_envs == 1, "vectorized envs are not supported at the moment"
            run_name = f"{self.env_id}__{self.exp_name}__{seed}__{int(time.time())}"
            writer = SummaryWriter(f"runs/{run_name}")
            # writer.add_text(
            #     "hyperparameters",
            #     "|param|value|\n|-|-|\n%s" % ("\n".join([f"|{key}|{value}|" for key, value in vars(args).items()])),
            # )

            # TRY NOT TO MODIFY: seeding
            random.seed(seed)
            np.random.seed(seed)
            torch.manual_seed(seed)
            torch.backends.cudnn.deterministic = self.torch_deterministic

            device = torch.device("cuda" if torch.cuda.is_available() and self.cuda else self.device)

            # env setup
            envs = gym.vector.SyncVectorEnv(
                [self.make_env(seed + i, i, run_name) for i in range(self.num_envs)]
            )
            assert isinstance(envs.single_action_space, gym.spaces.Discrete), "only discrete action space is supported"

            q_network = QNetwork(envs=envs, num_hl=self.num_hl, num_hl_neur=self.num_hl_neur).to(device)
            optimizer = optim.Adam(q_network.parameters(), lr=self.learning_rate)
            target_network = QNetwork(envs=envs, num_hl=self.num_hl, num_hl_neur=self.num_hl_neur).to(device)
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
                epsilon = self.linear_schedule(self.start_e, self.end_e, self.exploration_fraction * self.total_timesteps, global_step)
                if random.random() < epsilon:
                    actions = np.array([envs.single_action_space.sample() for _ in range(envs.num_envs)])
                else:
                    # TODO: HÄR ÄR PROBLEMET, FIXA
                    q_values = q_network(torch.Tensor(obs).to(device))
                    actions = torch.argmax(q_values, dim=1).cpu().numpy()

                # TRY NOT TO MODIFY: execute the game and log data.
                next_obs, rewards, terminations, truncations, infos = envs.step(actions)

                # TRY NOT TO MODIFY: record rewards for plotting purposes
                if "final_info" in infos:
                    for info in infos["final_info"]:
                        if info and "episode" in info:
                            print(f"global_step={global_step}, episodic_return={info['episode']['r']}")
                            writer.add_scalar("charts/episodic_return", info["episode"]["r"], global_step)
                            writer.add_scalar("charts/episodic_length", info["episode"]["l"], global_step)

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
                            target_max, _ = target_network(data.next_observations).max(dim=1)
                            td_target = data.rewards.flatten() + self.gamma * target_max * (1 - data.dones.flatten())
                        old_val = q_network(data.observations).gather(1, data.actions).squeeze()
                        loss = F.mse_loss(td_target, old_val)

                        if global_step % 100 == 0:
                            writer.add_scalar("losses/td_loss", loss, global_step)
                            writer.add_scalar("losses/q_values", old_val.mean().item(), global_step)
                            print("SPS:", int(global_step / (time.time() - start_time)))
                            writer.add_scalar("charts/SPS", int(global_step / (time.time() - start_time)), global_step)

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

            if self.save_model:
                model_path = f"runs/{run_name}/{self.exp_name}.cleanrl_model"
                torch.save(q_network.state_dict(), model_path)
                print(f"model saved to {model_path}")
                from dqn_clean_eval import evaluate

                episodic_returns = evaluate(
                    model_path,
                    self.make_env,
                    self.env_id,
                    eval_episodes=10,
                    run_name=f"{run_name}-eval",
                    Model=QNetwork,
                    device=device,
                    epsilon=0.05,
                )
                for idx, episodic_return in enumerate(episodic_returns):
                    writer.add_scalar("eval/episodic_return", episodic_return, idx)


            envs.close()
            writer.close()

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