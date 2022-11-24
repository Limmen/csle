from typing import List, Optional, Tuple, Union
import math
import time
import os
import numpy as np
import gym
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.experiment_result import ExperimentResult
from csle_common.dao.training.agent_type import AgentType
from csle_common.util.experiment_util import ExperimentUtil
from csle_common.logging.log import Logger
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.jobs.training_job_config import TrainingJobConfig
from csle_common.dao.training.experiment_execution import ExperimentExecution
from csle_common.dao.training.tabular_policy import TabularPolicy
from csle_agents.agents.base.base_agent import BaseAgent
import csle_agents.constants.constants as agents_constants


class SARSAAgent(BaseAgent):
    """
    SARSA Agent
    """

    def __init__(self, simulation_env_config: SimulationEnvConfig, experiment_config: ExperimentConfig,
                 training_job: Optional[TrainingJobConfig] = None, save_to_metastore: bool = True):
        """
        Initializes the SARSA agent

        :param simulation_env_config: configuration of the simulation environment
        :param experiment_config: the experiment configuration
        :param training_job: an existing training job to use (optional)
        :param save_to_metastore: boolean flag whether to save the execution to the metastore
        """
        super().__init__(simulation_env_config=simulation_env_config, emulation_env_config=None,
                         experiment_config=experiment_config)
        assert experiment_config.agent_type == AgentType.SARSA
        self.training_job = training_job
        self.save_to_metastore = save_to_metastore
        self.env = gym.make(self.simulation_env_config.gym_env_name,
                            config=self.simulation_env_config.simulation_env_input_config)

    def train(self) -> ExperimentExecution:
        """
        Runs the SARSA algorithm to compute Q*

        :return: the results
        """
        pid = os.getpid()

        # Initialize metrics
        exp_result = ExperimentResult()
        exp_result.plot_metrics.append(agents_constants.COMMON.AVERAGE_RETURN)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_RETURN)
        exp_result.plot_metrics.append(agents_constants.Q_LEARNING.INITIAL_STATE_VALUES)

        descr = f"Computation of V* with the SARSA algorithm using " \
                f"simulation:{self.simulation_env_config.name}"

        for seed in self.experiment_config.random_seeds:
            exp_result.all_metrics[seed] = {}
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN] = []

        # Initialize training job
        if self.training_job is None:
            self.training_job = TrainingJobConfig(
                simulation_env_name=self.simulation_env_config.name, experiment_config=self.experiment_config,
                progress_percentage=0, pid=pid, experiment_result=exp_result,
                emulation_env_name=None, simulation_traces=[],
                num_cached_traces=0,
                log_file_path=Logger.__call__().get_log_file_path(), descr=descr)
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
        emulation_name = None
        if self.emulation_env_config is not None:
            emulation_name = self.emulation_env_config.name
        simulation_name = self.simulation_env_config.name
        self.exp_execution = ExperimentExecution(result=exp_result, config=self.experiment_config, timestamp=ts,
                                                 emulation_name=emulation_name, simulation_name=simulation_name,
                                                 descr=descr, log_file_path=self.training_job.log_file_path)
        if self.save_to_metastore:
            exp_execution_id = MetastoreFacade.save_experiment_execution(self.exp_execution)
            self.exp_execution.id = exp_execution_id

        for seed in self.experiment_config.random_seeds:
            ExperimentUtil.set_seed(seed)
            exp_result = self.q_learning(exp_result=exp_result, seed=seed)

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
        self.training_job.experiment_result = exp_result
        if self.save_to_metastore:
            MetastoreFacade.update_experiment_execution(experiment_execution=self.exp_execution,
                                                        id=self.exp_execution.id)
            MetastoreFacade.update_training_job(training_job=self.training_job, id=self.training_job.id)
        return self.exp_execution

    def hparam_names(self) -> List[str]:
        """
        :return: a list with the hyperparameter names
        """
        return [agents_constants.COMMON.EVAL_BATCH_SIZE, agents_constants.COMMON.CONFIDENCE_INTERVAL,
                agents_constants.COMMON.RUNNING_AVERAGE, agents_constants.COMMON.GAMMA,
                agents_constants.Q_LEARNING.EPSILON, agents_constants.Q_LEARNING.N,
                agents_constants.Q_LEARNING.S, agents_constants.Q_LEARNING.A]

    def q_learning(self, exp_result: ExperimentResult, seed: int) -> ExperimentResult:
        """
        Runs the SARSA algorithm

        :param exp_result: the experiment result object
        :param seed: the random seed
        :return: the updated experiment result
        """
        discount_factor = self.experiment_config.hparams[agents_constants.COMMON.GAMMA].value
        S = self.experiment_config.hparams[agents_constants.Q_LEARNING.S].value
        A = self.experiment_config.hparams[agents_constants.Q_LEARNING.A].value
        epsilon = self.experiment_config.hparams[agents_constants.Q_LEARNING.EPSILON].value
        N = self.experiment_config.hparams[agents_constants.Q_LEARNING.N].value
        Logger.__call__().get_logger().info(f"Starting the SARSA algorithm, N:{N}, "
                                            f"num_states:{len(S)}, discount_factor: {discount_factor}, "
                                            f"num_actions: {len(A)}, epsilon: {epsilon}")
        avg_returns, running_avg_returns, initial_state_values, q_table, policy = self.train_sarsa(
            A=A, S=S, gamma=discount_factor, N=N, epsilon=epsilon)
        exp_result.all_metrics[seed][agents_constants.Q_LEARNING.INITIAL_STATE_VALUES] = initial_state_values
        exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN] = avg_returns
        exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN] = running_avg_returns
        tabular_policy = TabularPolicy(player_type=self.experiment_config.player_type,
                                       actions=self.simulation_env_config.joint_action_space_config.action_spaces[
                                           self.experiment_config.player_idx].actions,
                                       agent_type=self.experiment_config.agent_type, q_table=q_table,
                                       lookup_table=list(policy), simulation_name=self.simulation_env_config.name,
                                       avg_R=avg_returns[-1])
        exp_result.policies[seed] = tabular_policy
        return exp_result

    def train_sarsa(self, A: List, S: List, gamma: float = 0.8, N: int = 10000, epsilon: float = 0.2) \
            -> Tuple[List[float], list, List[np.ndarray], Union[np.ndarray, np.ndarray], Union[np.ndarray, np.ndarray]]:
        """
        Runs the Q learning algorithm

        :param A: the action space
        :param S: the state space
        :param gamma: the discount factor
        :param N: the number of iterations
        :param epsilon: the exploration parameter
        :return: the average returns, the running average returns, the initial state values, the q table, policy
        """
        init_state_values = []
        average_returns = []
        running_average_returns = []

        Logger.__call__().get_logger().info("Starting Q Learning, gamma:{}, n_iter:{}, eps:{}".format(gamma, N,
                                                                                                      epsilon))
        q_table = self.initialize_q_table(n_states=len(S), n_actions=len(A))
        count_table = self.initialize_count_table(n_states=256, n_actions=5)
        steps = []
        prog = 0
        state_val = 0
        avg_return = 0

        o = self.env.reset()
        if self.simulation_env_config.gym_env_name in agents_constants.COMMON.STOPPING_ENVS:
            s = int(o[2])
        else:
            s = o
        for i in range(N):
            a = self.eps_greedy(q_table=q_table, A=A, s=s, epsilon=epsilon)
            o, r, done, _ = self.env.step(a)
            if self.simulation_env_config.gym_env_name in agents_constants.COMMON.STOPPING_ENVS:
                s_prime = int(o[2])
            else:
                s_prime = o
            a1 = self.eps_greedy(q_table=q_table, A=A, s=s_prime, epsilon=epsilon)
            q_table, count_table = self.sarsa_update(q_table=q_table, count_table=count_table,
                                                     s=s, a=a, r=r, s_prime=s_prime, gamma=gamma, a1=a1)

            if i % self.experiment_config.hparams[agents_constants.COMMON.EVAL_EVERY].value == 0:
                steps.append(i)
                state_val = np.sum(
                    np.dot(
                        np.array(list(map(lambda x: sum(q_table[x]), S))),
                        np.array(
                            self.simulation_env_config.initial_state_distribution_config.initial_state_distribution)))
                prog = float(i / N)
                init_state_values.append(state_val)

                policy = self.create_policy_from_q_table(num_states=len(S), num_actions=len(A), q_table=q_table)
                avg_return = self.evaluate_policy(policy=policy, eval_batch_size=self.experiment_config.hparams[
                    agents_constants.COMMON.EVAL_BATCH_SIZE].value)
                average_returns.append(avg_return)
                running_avg_J = ExperimentUtil.running_average(
                    average_returns, self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value)
                running_average_returns.append(running_avg_J)

            if i % self.experiment_config.log_every == 0 or i == 0:
                Logger.__call__().get_logger().info(
                    f"[SARSA] i:{i}, progress:{prog}, V(s0):{state_val}, J:{avg_return}, "
                    f"running_avg_J:{running_average_returns}")

            s = s_prime
            if done:
                o = self.env.reset()
                if self.simulation_env_config.gym_env_name in agents_constants.COMMON.STOPPING_ENVS:
                    s = int(o[2])
                else:
                    s = o

        policy = self.create_policy_from_q_table(num_states=len(S), num_actions=len(A), q_table=q_table)
        return average_returns, running_average_returns, init_state_values, q_table, policy

    def initialize_q_table(self, n_states: int = 256, n_actions: int = 5) -> np.ndarray:
        """
        Initializes the Q table

        :param n_states: the number of states in the MDP
        :param n_actions: the number of actions in the MDP
        :return: the initialized Q table
        """
        q_table = np.zeros((n_states, n_actions))
        return q_table

    def initialize_count_table(self, n_states: int = 256, n_actions: int = 5) -> np.ndarray:
        """
        Initializes the count table

        :param n_states: the number of states in the MDP
        :param n_actions: the number of actions in the MDP
        :return: the initialized count table
        """
        count_table = np.zeros((n_states, n_actions))
        return count_table

    def eps_greedy(self, q_table: np.ndarray, A: List, s: int, epsilon: float = 0.2) -> int:
        """
        Selects an action according to the epsilon-greedy strategy

        :param q_table: the q table
        :param A: the action space
        :param s: the state
        :param epsilon: the exploration epsilon
        :return: the sampled action
        """
        if np.random.rand() <= epsilon:
            a = np.random.choice(A)
        else:
            a = np.argmax(q_table[s])
        return a

    def step_size(self, n: int) -> float:
        """
        Calculates the SA step size

        :param n: the iteration
        :return: the step size
        """
        return float(1) / math.pow(n, 2 / 3)

    def sarsa_update(self, q_table: np.ndarray, count_table: np.ndarray, s: int, a: int, r: float, s_prime: int,
                     gamma: float, a1: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        SARSA update

        :param q_table: the Q-table
        :param count_table: the count table (used for determining SA step sizes)
        :param s: the sampled state
        :param a: the exploration action
        :param r: the reward
        :param s_prime: the next sampled state
        :param gamma: the discount factor
        :param a1: the next eaction
        :return: the updated q table and updated count table
        """
        count_table[s][a] = count_table[s_prime][a] + 1
        alpha = self.step_size(count_table[s][a])
        q_table[s][a] = q_table[s][a] + alpha * ((r + gamma * q_table[s_prime][a1]) - q_table[s][a])
        return q_table, count_table

    def create_policy_from_q_table(self, num_states: int, num_actions: int, q_table: np.ndarray) -> np.ndarray:
        """
        Creates a tabular policy from a q table

        :param num_states: the number of states
        :param num_actions: the number of actions
        :param q_table: the q_table
        :return: the tabular policy
        """
        # Create a deterministic policy using the optimal value function
        policy = np.zeros([num_states, num_actions])
        for s in range(num_states):
            # Find best action
            best_action = np.argmax(q_table[s])
            # Always take the best action
            policy[s][best_action] = 1.0
        return policy

    def evaluate_policy(self, policy: np.ndarray, eval_batch_size: int) -> float:
        """
        Evalutes a tabular policy

        :param policy: the tabular policy to evaluate
        :param eval_batch_size: the batch size
        :return: None
        """
        returns = []
        for i in range(eval_batch_size):
            done = False
            self.env.reset()
            R = 0
            while not done:
                s, r, done, info = self.env.step(policy)
                R += r
            returns.append(R)
        avg_return = np.mean(returns)
        return float(avg_return)
