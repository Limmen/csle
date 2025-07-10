from typing import Union, List, Dict, Optional, Any
import math
import time
import gymnasium as gym
import os
import torch
import numpy as np
import gym_csle_stopping_game.constants.constants as env_constants
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.experiment_execution import ExperimentExecution
from csle_common.dao.training.experiment_result import ExperimentResult
from csle_common.dao.training.agent_type import AgentType
from csle_common.util.experiment_util import ExperimentUtil
from csle_common.logging.log import Logger
from csle_common.dao.training.fnn_with_softmax_policy import FNNWithSoftmaxPolicy
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.jobs.training_job_config import TrainingJobConfig
from csle_common.models.fnn_w_softmax import FNNwithSoftmax
from csle_common.util.general_util import GeneralUtil
from csle_common.dao.simulation_config.base_env import BaseEnv
from csle_agents.agents.base.base_agent import BaseAgent
import csle_agents.constants.constants as agents_constants


class ReinforceAgent(BaseAgent):
    """
    Reinforce Agent
    """

    def __init__(self, simulation_env_config: SimulationEnvConfig,
                 emulation_env_config: Union[None, EmulationEnvConfig],
                 experiment_config: ExperimentConfig, env: Optional[BaseEnv] = None,
                 training_job: Optional[TrainingJobConfig] = None, save_to_metastore: bool = True):
        """
        Initializes the Reinforce Agent

        :param simulation_env_config: the simulation env config
        :param emulation_env_config: the emulation env config
        :param experiment_config: the experiment config
        :param env: (optional) the gym environment to use for simulation
        :param training_job: (optional) a training job configuration
        :param save_to_metastore: boolean flag that can be set to avoid saving results and progress to the metastore
        """
        super().__init__(simulation_env_config=simulation_env_config, emulation_env_config=emulation_env_config,
                         experiment_config=experiment_config)
        assert experiment_config.agent_type == AgentType.REINFORCE
        self.env = env
        self.training_job = training_job
        self.save_to_metastore = save_to_metastore
        self.machine_eps = np.finfo(np.float64).eps.item()

    def train(self) -> ExperimentExecution:
        """
        Performs the policy training for the given random seeds using reinforce

        :return: the training metrics and the trained policies
        """
        pid = os.getpid()

        # Initialize metrics
        exp_result = ExperimentResult()
        exp_result.plot_metrics.append(agents_constants.COMMON.AVERAGE_RETURN)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_RETURN)
        exp_result.plot_metrics.append(agents_constants.COMMON.POLICY_LOSSES)
        exp_result.plot_metrics.append(env_constants.ENV_METRICS.INTRUSION_LENGTH)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_LENGTH)
        exp_result.plot_metrics.append(env_constants.ENV_METRICS.INTRUSION_START)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_START)
        exp_result.plot_metrics.append(env_constants.ENV_METRICS.TIME_HORIZON)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON)
        exp_result.plot_metrics.append(env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN)
        exp_result.plot_metrics.append(env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN)

        descr = f"Training of policies with the random search algorithm using " \
                f"simulation:{self.simulation_env_config.name}"
        for seed in self.experiment_config.random_seeds:
            exp_result.all_metrics[seed] = {}
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.POLICY_LOSSES] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_START] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_LENGTH] = []
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_START] = []
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_LENGTH] = []
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.TIME_HORIZON] = []
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN] = []
            exp_result.all_metrics[seed][
                env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN] = []

        # Initialize training job
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
            if self.save_to_metastore:
                training_job_id = MetastoreFacade.save_training_job(training_job=self.training_job)
                self.training_job.id = training_job_id
        else:
            self.training_job.pid = pid
            self.training_job.progress_percentage = 0
            self.training_job.experiment_result = exp_result
            if self.save_to_metastore:
                MetastoreFacade.update_training_job(training_job=self.training_job, id=self.training_job.id)

        # Initialize execution result
        ts = time.time()
        emulation_name = ""
        if self.emulation_env_config is not None:
            emulation_name = self.emulation_env_config.name
        simulation_name = self.simulation_env_config.name
        self.exp_execution = ExperimentExecution(result=exp_result, config=self.experiment_config, timestamp=ts,
                                                 emulation_name=emulation_name, simulation_name=simulation_name,
                                                 descr=descr, log_file_path=self.training_job.log_file_path)
        if self.save_to_metastore:
            exp_execution_id = MetastoreFacade.save_experiment_execution(self.exp_execution)
            self.exp_execution.id = exp_execution_id

        config = self.simulation_env_config.simulation_env_input_config
        if self.env is None:
            self.env = gym.make(self.simulation_env_config.gym_env_name, config=config)
        for seed in self.experiment_config.random_seeds:
            ExperimentUtil.set_seed(seed)
            exp_result = self.reinforce(exp_result=exp_result, seed=seed, training_job=self.training_job,
                                        random_seeds=self.experiment_config.random_seeds)

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
                if type(value_vectors[0][0]) is int or type(value_vectors[0][0]) is float \
                        or type(value_vectors[0][0]) is np.int64 or type(value_vectors[0][0]) is np.float64:
                    seed_values = []
                    for seed_idx in range(len(self.experiment_config.random_seeds)):
                        seed_values.append(value_vectors[seed_idx][i])
                    avg = ExperimentUtil.mean_confidence_interval(
                        data=seed_values,
                        confidence=self.experiment_config.hparams[agents_constants.COMMON.CONFIDENCE_INTERVAL].value)[0]
                    if not math.isnan(avg):
                        avg_metrics.append(avg)
                    ci = ExperimentUtil.mean_confidence_interval(
                        data=seed_values,
                        confidence=self.experiment_config.hparams[agents_constants.COMMON.CONFIDENCE_INTERVAL].value)[1]
                    if not math.isnan(ci):
                        std_metrics.append(ci)
                    else:
                        std_metrics.append(-1)
                else:
                    avg_metrics.append(-1)
                    std_metrics.append(-1)
                exp_result.avg_metrics[metric] = avg_metrics
                exp_result.std_metrics[metric] = std_metrics

        ts = time.time()
        self.exp_execution.timestamp = ts
        self.exp_execution.result = exp_result
        if self.save_to_metastore:
            MetastoreFacade.update_experiment_execution(experiment_execution=self.exp_execution,
                                                        id=self.exp_execution.id)
        return self.exp_execution

    def hparam_names(self) -> List[str]:
        """
        :return: a list with the hyperparameter names
        """
        return [agents_constants.REINFORCE.N, agents_constants.COMMON.EVAL_BATCH_SIZE,
                agents_constants.COMMON.CONFIDENCE_INTERVAL,
                agents_constants.COMMON.RUNNING_AVERAGE,
                agents_constants.COMMON.LEARNING_RATE_DECAY_RATE, agents_constants.COMMON.LEARNING_RATE_EXP_DECAY,
                constants.NEURAL_NETWORKS.NUM_HIDDEN_LAYERS, constants.NEURAL_NETWORKS.NUM_NEURONS_PER_HIDDEN_LAYER,
                constants.NEURAL_NETWORKS.ACTIVATION_FUNCTION, agents_constants.COMMON.OPTIMIZER]

    def reinforce(self, exp_result: ExperimentResult, seed: int,
                  training_job: TrainingJobConfig, random_seeds: List[int]) -> ExperimentResult:
        """
        Runs the random search algorithm

        :param exp_result: the experiment result object to store the result
        :param seed: the seed
        :param training_job: the training job config
        :param random_seeds: list of seeds
        :return: the updated experiment result and the trained policy
        """
        if self.env is None:
            raise ValueError("Need to specify an environment to run Reinforce")
        # Hyperparameters
        N = self.experiment_config.hparams[agents_constants.REINFORCE.N].value

        # Setup policy network
        policy_network = FNNwithSoftmax(
            input_dim=self.env.observation_space.shape[0],
            output_dim=self.env.action_space.n,
            hidden_dim=self.experiment_config.hparams[constants.NEURAL_NETWORKS.NUM_NEURONS_PER_HIDDEN_LAYER].value,
            num_hidden_layers=self.experiment_config.hparams[constants.NEURAL_NETWORKS.NUM_HIDDEN_LAYERS].value,
            hidden_activation=self.experiment_config.hparams[constants.NEURAL_NETWORKS.ACTIVATION_FUNCTION].value
        )

        # Setup device
        policy_network.to(torch.device(self.experiment_config.hparams[constants.NEURAL_NETWORKS.DEVICE].value))

        optimizer: Union[torch.optim.Adam, torch.optim.SGD, None] = None
        # Setup optimizer
        if self.experiment_config.hparams[agents_constants.COMMON.OPTIMIZER].value == agents_constants.COMMON.ADAM:
            optimizer = torch.optim.Adam(
                policy_network.parameters(),
                lr=self.experiment_config.hparams[agents_constants.COMMON.LEARNING_RATE].value)
        elif self.experiment_config.hparams[agents_constants.COMMON.OPTIMIZER].value == agents_constants.COMMON.SGD:
            optimizer = torch.optim.SGD(
                policy_network.parameters(),
                lr=self.experiment_config.hparams[agents_constants.COMMON.LEARNING_RATE].value)
        else:
            raise ValueError(f"Optimizer: {self.experiment_config.hparams[agents_constants.COMMON.OPTIMIZER].value}"
                             f" not recognized")

        for i in range(N):
            rewards_batch = []
            log_probs_batch = []
            metrics: Dict[str, Any] = {}
            ts = time.time()
            save_path = f"{self.experiment_config.output_dir}/reinforce_policy_seed_{seed}_{ts}.zip"
            policy = FNNWithSoftmaxPolicy(
                policy_network=policy_network, simulation_name=self.simulation_env_config.name,
                save_path=save_path,
                states=self.simulation_env_config.state_space_config.states,
                actions=self.simulation_env_config.joint_action_space_config.action_spaces[
                    self.experiment_config.player_idx].actions, player_type=self.experiment_config.player_type,
                experiment_config=self.experiment_config,
                avg_R=-1, input_dim=policy_network.input_dim, output_dim=policy_network.output_dim)
            policy.save_policy_network()

            # Run a batch of rollouts
            for j in range(self.experiment_config.hparams[agents_constants.REINFORCE.GRADIENT_BATCH_SIZE].value):
                cumulative_reward = 0.0
                rewards = []
                log_probs = []
                done = False
                o, _ = self.env.reset()
                while not done:
                    # get action
                    action, log_prob = policy.get_action_and_log_prob(state=o)

                    # Take a step in the environment
                    o_prime, reward, done, _, info = self.env.step(action)

                    # Update metrics
                    cumulative_reward += reward
                    rewards.append(cumulative_reward)
                    log_probs.append(log_prob)

                    # Move to the next state
                    o = o_prime

                # Accumulate batch
                rewards_batch.append(rewards)
                log_probs_batch.append(log_probs)

                metrics = ReinforceAgent.update_metrics(metrics=metrics, info=info)

            avg_metrics = ReinforceAgent.compute_avg_metrics(metrics=metrics)

            # Perform Batch Policy Gradient updates
            loss_tensor = self.training_step(saved_rewards=rewards_batch, saved_log_probs=log_probs_batch,
                                             policy_network=policy_network,
                                             optimizer=optimizer,
                                             gamma=self.experiment_config.hparams[agents_constants.COMMON.GAMMA].value)
            loss = loss_tensor.item()

            # Log metrics
            J = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
            policy.avg_R = J
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN].append(J)
            exp_result.all_metrics[seed][agents_constants.COMMON.POLICY_LOSSES].append(loss)
            running_avg_J = ExperimentUtil.running_average(
                exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN],
                self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value)
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN].append(running_avg_J)

            # Log intrusion lengths
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_LENGTH].append(
                round(avg_metrics[env_constants.ENV_METRICS.INTRUSION_LENGTH], 3))
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_LENGTH].append(
                ExperimentUtil.running_average(
                    exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_LENGTH],
                    self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))

            # Log stopping times
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_START].append(
                round(avg_metrics[env_constants.ENV_METRICS.INTRUSION_START], 3))
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_START].append(
                ExperimentUtil.running_average(
                    exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_START],
                    self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.TIME_HORIZON].append(
                round(avg_metrics[env_constants.ENV_METRICS.TIME_HORIZON], 3))
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON].append(
                ExperimentUtil.running_average(
                    exp_result.all_metrics[seed][env_constants.ENV_METRICS.TIME_HORIZON],
                    self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))

            # Log baseline returns
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN].append(
                round(avg_metrics[env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN], 3))
            exp_result.all_metrics[seed][
                env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN].append(
                round(avg_metrics[env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN], 3))

            if i % self.experiment_config.log_every == 0 and i > 0:
                # Update training job
                total_iterations = len(random_seeds) * N
                iterations_done = (random_seeds.index(seed)) * N + i
                progress = round(iterations_done / total_iterations, 2)
                training_job.progress_percentage = progress
                training_job.experiment_result = exp_result
                if len(training_job.simulation_traces) > training_job.num_cached_traces:
                    training_job.simulation_traces = training_job.simulation_traces[1:]
                if self.save_to_metastore:
                    MetastoreFacade.update_training_job(training_job=training_job, id=training_job.id)

                # Update execution
                ts = time.time()
                self.exp_execution.timestamp = ts
                self.exp_execution.result = exp_result
                if self.save_to_metastore:
                    MetastoreFacade.update_experiment_execution(experiment_execution=self.exp_execution,
                                                                id=self.exp_execution.id)

                Logger.__call__().get_logger().info(
                    f"[REINFORCE] i: {i}, J:{J}, "
                    f"J_avg_{self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value}:"
                    f"{running_avg_J}, "
                    f"opt_J:{exp_result.all_metrics[seed][env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN][-1]}, "
                    f"int_len:{exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_LENGTH][-1]}, "
                    f"progress: {round(progress * 100, 2)}%")

        ts = time.time()
        save_path = f"{self.experiment_config.output_dir}/ppo_policy_seed_{seed}_{ts}.zip"
        policy = FNNWithSoftmaxPolicy(
            policy_network=policy_network, simulation_name=self.simulation_env_config.name,
            save_path=save_path,
            states=self.simulation_env_config.state_space_config.states,
            actions=self.simulation_env_config.joint_action_space_config.action_spaces[
                self.experiment_config.player_idx].actions, player_type=self.experiment_config.player_type,
            experiment_config=self.experiment_config,
            avg_R=exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN][-1],
            input_dim=policy_network.input_dim, output_dim=policy_network.output_dim)
        policy.save_policy_network()

        exp_result.policies[seed] = policy
        # Save policy
        if self.save_to_metastore:
            MetastoreFacade.save_fnn_w_softmax_policy(fnn_w_softmax_policy=policy)
        return exp_result

    @staticmethod
    def update_metrics(metrics: Dict[str, List[Union[float, int]]], info: Dict[str, Union[float, int]]) \
            -> Dict[str, List[Union[float, int]]]:
        """
        Update a dict with aggregated metrics using new information from the environment

        :param metrics: the dict with the aggregated metrics
        :param info: the new information
        :return: the updated dict
        """
        for k, v in info.items():
            if k in metrics:
                metrics[k].append(round(v, 3))
            else:
                metrics[k] = [v]
        return metrics

    @staticmethod
    def compute_avg_metrics(metrics: Dict[str, List[Union[float, int]]]) -> Dict[str, Union[float, int]]:
        """
        Computes the average metrics of a dict with aggregated metrics

        :param metrics: the dict with the aggregated metrics
        :return: the average metrics
        """
        avg_metrics = {}
        for k, v in metrics.items():
            avg = round(sum(v) / len(v), 2)
            avg_metrics[k] = avg
        return avg_metrics

    @staticmethod
    def round_vec(vec) -> List[float]:
        """
        Rounds a vector to 3 decimals

        :param vec: the vector to round
        :return: the rounded vector
        """
        return list(map(lambda x: round(x, 3), vec))

    def training_step(self, saved_rewards: List[List[float]], saved_log_probs: List[List[torch.Tensor]],
                      policy_network: FNNwithSoftmax, optimizer: torch.optim.Optimizer, gamma: float) -> torch.Tensor:
        """
        Performs a training step of the REINFORCE algorithm

        :param saved_rewards: list of rewards encountered in the latest episode trajectory
        :param saved_log_probs: list of log-action probabilities (log p(a|s)) encountered in the latest
                                episode trajectory
        :param policy_network: the policy network
        :param optimizer: the optimizer for updating the weights
        :param gamma: the discount factor
        :return: loss
        """
        policy_loss = []
        num_batches = len(saved_rewards)

        for batch in range(num_batches):
            R = 0.0
            returns: List[float] = []

            # Create discounted returns. When episode is finished we can go back and compute the observed cumulative
            # discounted reward by using the observed rewards
            for r in saved_rewards[batch][::-1]:
                R = r + gamma * R
                returns.insert(0, R)
            num_rewards = len(returns)

            # convert list to torch tensor
            returns_tensor = torch.tensor(returns)

            # normalize
            std = float(returns_tensor.std())
            if num_rewards < 2:
                std = 0.0
            returns_tensor = (returns_tensor - returns_tensor.mean()) / (std + self.machine_eps)

            # Compute PG "loss" which in reality is the expected reward, which we want to maximize with gradient ascent
            for log_prob, R in zip(saved_log_probs[batch], returns_tensor):
                # negative log prob since we are doing gradient descent (not ascent)
                policy_loss.append(-log_prob * R)

        # Compute gradient and update models
        # reset gradients
        optimizer.zero_grad()
        # expected loss over the batch
        policy_loss_total = torch.stack(policy_loss).sum()
        policy_loss_val = policy_loss_total / num_batches
        # perform backprop
        policy_loss_val.backward()
        # gradient descent step
        optimizer.step()
        return policy_loss_val
