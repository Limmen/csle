import math
from typing import List, Optional, Tuple
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
from csle_agents.agents.base.base_agent import BaseAgent
import csle_agents.constants.constants as agents_constants
from csle_common.dao.training.experiment_execution import ExperimentExecution
from csle_common.dao.training.tabular_policy import TabularPolicy


class PIAgent(BaseAgent):
    """
    Policy Iteration Agent
    """

    def __init__(self, simulation_env_config: SimulationEnvConfig,
                 experiment_config: ExperimentConfig,
                 training_job: Optional[TrainingJobConfig] = None, save_to_metastore: bool = True):
        """
        Initializes the value iteration agent

        :param simulation_env_config: configuration of the simulation environment
        :param experiment_config: the experiment configuration
        :param training_job: an existing training job to use (optional)
        :param save_to_metastore: boolean flag whether to save the execution to the metastore
        """
        super().__init__(simulation_env_config=simulation_env_config, emulation_env_config=None,
                         experiment_config=experiment_config)
        assert experiment_config.agent_type == AgentType.POLICY_ITERATION
        self.training_job = training_job
        self.save_to_metastore = save_to_metastore
        self.env = gym.make(self.simulation_env_config.gym_env_name,
                            config=self.simulation_env_config.simulation_env_input_config)

    def train(self) -> ExperimentExecution:
        """
        Runs the policy iteration algorithm to compute V*

        :return: the results
        """
        pid = os.getpid()

        # Initialize metrics
        exp_result = ExperimentResult()
        exp_result.plot_metrics.append(agents_constants.COMMON.AVERAGE_RETURN)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_RETURN)

        descr = f"Computation of V* with the Policy Iteration algorithm using " \
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
            exp_result = self.policy_iteration(exp_result=exp_result, seed=seed)

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
                agents_constants.VI.THETA, agents_constants.VI.TRANSITION_TENSOR,
                agents_constants.VI.REWARD_TENSOR, agents_constants.VI.NUM_STATES, agents_constants.VI.NUM_ACTIONS]

    def policy_iteration(self, exp_result: ExperimentResult, seed: int) -> ExperimentResult:
        """
        Runs the policy iteration algorithm

        :param exp_result: the experiment result object
        :param seed: the random seed
        :return: the updated experiment result
        """
        N = self.experiment_config.hparams[agents_constants.PI.N].value
        discount_factor = self.experiment_config.hparams[agents_constants.COMMON.GAMMA].value
        num_states = self.experiment_config.hparams[agents_constants.PI.NUM_STATES].value
        num_actions = self.experiment_config.hparams[agents_constants.PI.NUM_ACTIONS].value
        T = self.experiment_config.hparams[agents_constants.PI.TRANSITION_TENSOR].value
        R = self.experiment_config.hparams[agents_constants.PI.REWARD_TENSOR].value
        initial_pi = np.array(self.experiment_config.hparams[agents_constants.PI.INITIAL_POLICY].value)
        Logger.__call__().get_logger().info(f"Starting the policy iteration algorithm, N:{N}, "
                                            f"num_states:{num_states}, discount_factor: {discount_factor}, "
                                            f"num_actions: {num_actions}")
        policy, v, avg_returns, running_avg_returns = self.pi(
            P=np.array(T), num_states=num_states, num_actions=num_actions,
            R=np.array(R), gamma=discount_factor, N=N, policy=initial_pi)
        exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN] = avg_returns
        exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN] = running_avg_returns
        tabular_policy = TabularPolicy(player_type=self.experiment_config.player_type,
                                       actions=self.simulation_env_config.joint_action_space_config.action_spaces[
                                           self.experiment_config.player_idx].actions,
                                       agent_type=self.experiment_config.agent_type, value_function=list(v),
                                       lookup_table=list(policy), simulation_name=self.simulation_env_config.name,
                                       avg_R=avg_returns[-1])
        exp_result.policies[seed] = tabular_policy
        return exp_result

    def transition_probability_under_policy(self, P: np.ndarray, policy: np.ndarray, num_states: int) -> np.ndarray:
        """
        Utility function for computing the state transition probabilities under the current policy.
        Assumes a deterministic policy (probability 1 of selecting an action in a state)

        Args:
            :P: the state transition probabilities for all actions in the MDP
                (tensor num_actions x num_states x num_states)
            :policy: the policy (matrix num_states x num_actions)
            :num_states: the number of states

        Returns:
               :P_pi: the transition probabilities in the MDP under the given policy
                      (dimensions num_states x num_states)
        """
        P_pi = np.zeros((num_states, num_states))
        for i in range(0, num_states):
            action = np.where(policy[i] == 1)[0]
            P_pi[i] = P[action, i]
            assert sum(P_pi[i]) == 1  # stochastic
        return P_pi

    def expected_reward_under_policy(self, P: np.ndarray, R: np.ndarray, policy: np.ndarray, num_states: int,
                                     num_actions: int) -> np.ndarray:
        """
        Utility function for computing the expected immediate reward for each state
        in the MDP given a policy.

        Args:
            :P: the state transition probabilities for all actions in the MDP
                (tensor num_actions x num_states x num_states)
            :policy: the policy (matrix num_states x num_actions)
            :R: the reward function in the MDP (tensor num_actions x num_states x num_states)
            :num_states: the number of states
            :num_actions: the number of actions

        Returns:
               :r: a vector of dimension <num_states> with the expected immediate reward for each state.
        """
        r = np.zeros((num_states))
        for k in range(0, num_states):
            r[k] = sum(
                [policy[k][x] * sum([np.dot(P[x][y], [R[x][y]] * num_states)
                                     for y in range(0, num_states)])for x in range(0, num_actions)])
        return r

    def policy_evaluation(self, P: np.ndarray, policy: np.ndarray, R: np.ndarray, gamma: float,
                          num_states: int, num_actions: int) -> np.ndarray:
        """
        Implements the policy evaluation step in the policy iteration dynamic programming algorithm.
        Uses the linear algebra interpretation of policy evaluation, solving it as a linear system.

        Args:
            :P: the state transition probabilities for all actions in the MDP
                (tensor num_actions x num_states x num_states)
            :policy: the policy (matrix num_states x num_actions)
            :gamma: the discount factor
            :num_states: the number of states
            :num_actions: the number of actions

        Returns:
               :v: the state values, a vector of dimension NUM_STATES
        """
        P_pi = self.transition_probability_under_policy(P, policy, num_states=num_states)
        r_pi = self.expected_reward_under_policy(P, R, policy, num_states=num_states, num_actions=num_actions)
        I = np.identity(num_states)
        v = np.dot(np.linalg.inv(I - (np.dot(gamma, P_pi))), r_pi)
        return v

    def policy_improvement(self, P: np.ndarray, R: np.ndarray, gamma: float, v: np.ndarray,
                           pi: np.ndarray, num_states: int, num_actions: int) -> np.ndarray:
        """
        Implements the policy improvement step in the policy iteration dynamic programming algorithm.

        Args:
            :P: the state transition probabilities for all actions in the MDP
                (tensor num_actions x num_states x num_states)
            :R: the reward function in the MDP (tensor num_actions x num_states x num_states)
            :gamma: the discount factor
            :v: the state values (dimension NUM_STATES)
            :pi: the old policy (matrix num_states x num_actions)
            :num_states: the number of states
            :num_actions: the number of actions

        Returns:
               :pi_prime: a new updated policy (dimensions num_states x num_actions)
        """
        pi_prime = np.zeros((num_states, num_actions))
        for s in range(0, num_states):
            action_values = np.zeros(num_actions)
            for a in range(0, num_actions):
                for s_prime in range(0, num_states):
                    action_values[a] += P[a][s][s_prime] * (R[a][s] + gamma * v[s_prime])
            if max(action_values) == 0.0:
                pi_prime[s, np.argmax(pi[s])] = 1
            else:
                best_action = np.argmax(action_values)
                pi_prime[s][best_action] = 1
        return pi_prime

    def pi(self, P: np.ndarray, policy: np.ndarray, N: int, gamma: float, R: np.ndarray, num_states: int,
           num_actions: int) -> Tuple[np.ndarray, np.ndarray, List[float], List[float]]:
        """
        The policy iteration algorithm, interleaves policy evaluation and policy improvement for N iterations.
        Guaranteed to converge to the optimal policy and value function.

        Args:
            :P: the state transition probabilities for all actions in the MDP
            (tensor num_actions x num_states x num_states)
            :policy: the policy (matrix num_states x num_actions)
            :N: the number of iterations (scalar)
            :gamma: the discount factor
            :R: the reward function in the MDP (tensor num_actions x num_states x num_states)

        Returns:
               a tuple of (v, policy) where v is the state values after N iterations and policy is the policy
               after N iterations.
        """
        average_returns = []
        running_average_returns = []
        for i in range(0, N):
            v = self.policy_evaluation(P, policy, R, gamma, num_states=num_states, num_actions=num_actions)
            policy = self.policy_improvement(P, R, gamma, v, policy, num_states=num_states, num_actions=num_actions)

            if i % self.experiment_config.hparams[agents_constants.COMMON.EVAL_EVERY].value == 0:
                avg_return = self.evaluate_policy(policy=policy, eval_batch_size=self.experiment_config.hparams[
                    agents_constants.COMMON.EVAL_BATCH_SIZE].value)
                average_returns.append(avg_return)
                running_avg_J = ExperimentUtil.running_average(
                    average_returns, self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value)
                running_average_returns.append(running_avg_J)

            if i % self.experiment_config.log_every == 0 and i > 0:
                Logger.__call__().get_logger().info(f"[PI] i:{i}, avg_return: {avg_return}")

        return policy, v, average_returns, running_average_returns

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
            s = self.env.reset()
            R = 0
            while not done:
                s, r, done, info = self.env.step(policy)
                R += r
            returns.append(R)
        avg_return = np.mean(returns)
        return float(avg_return)
