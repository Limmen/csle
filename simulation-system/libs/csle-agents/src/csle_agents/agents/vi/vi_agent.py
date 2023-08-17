from typing import List, Optional, Tuple, Any
import math
import time
import os
import numpy as np
import numpy.typing as npt
import gymnasium as gym
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
from csle_common.dao.simulation_config.base_env import BaseEnv
from csle_common.util.general_util import GeneralUtil
from csle_agents.agents.base.base_agent import BaseAgent
import csle_agents.constants.constants as agents_constants


class VIAgent(BaseAgent):
    """
    Value Iteration Agent
    """

    def __init__(self, simulation_env_config: SimulationEnvConfig,
                 experiment_config: ExperimentConfig,
                 training_job: Optional[TrainingJobConfig] = None, save_to_metastore: bool = True,
                 env: Optional[BaseEnv] = None):
        """
        Initializes the value iteration agent

        :param simulation_env_config: configuration of the simulation environment
        :param experiment_config: the experiment configuration
        :param training_job: an existing training job to use (optional)
        :param save_to_metastore: boolean flag whether to save the execution to the metastore
        :param env: the gym environment for training
        """
        super().__init__(simulation_env_config=simulation_env_config, emulation_env_config=None,
                         experiment_config=experiment_config)
        assert experiment_config.agent_type == AgentType.VALUE_ITERATION
        self.training_job = training_job
        self.save_to_metastore = save_to_metastore
        self.env = env

    def train(self) -> ExperimentExecution:
        """
        Runs the value iteration algorithm to compute V*

        :return: the results
        """
        pid = os.getpid()

        # Initialize metrics
        exp_result = ExperimentResult()
        exp_result.plot_metrics.append(agents_constants.COMMON.AVERAGE_RETURN)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_RETURN)
        exp_result.plot_metrics.append(agents_constants.VI.DELTA)

        descr = f"Computation of V* with the Value Iteration algorithm using " \
                f"simulation:{self.simulation_env_config.name}"

        for seed in self.experiment_config.random_seeds:
            exp_result.all_metrics[seed] = {}
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN] = []

        if self.env is None:
            self.env = gym.make(self.simulation_env_config.gym_env_name,
                                config=self.simulation_env_config.simulation_env_input_config)

        # Initialize training job
        if self.training_job is None:
            self.training_job = TrainingJobConfig(
                simulation_env_name=self.simulation_env_config.name, experiment_config=self.experiment_config,
                progress_percentage=0, pid=pid, experiment_result=exp_result,
                emulation_env_name="", simulation_traces=[],
                num_cached_traces=0,
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
            exp_result = self.value_iteration(exp_result=exp_result, seed=seed)

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

    def value_iteration(self, exp_result: ExperimentResult, seed: int) -> ExperimentResult:
        """
        Runs the value iteration algorithm

        :param exp_result: the experiment result object
        :param seed: the random seed
        :return: the updated experiment result
        """
        theta = self.experiment_config.hparams[agents_constants.VI.THETA].value
        discount_factor = self.experiment_config.hparams[agents_constants.COMMON.GAMMA].value
        num_states = self.experiment_config.hparams[agents_constants.VI.NUM_STATES].value
        num_actions = self.experiment_config.hparams[agents_constants.VI.NUM_ACTIONS].value
        T = self.experiment_config.hparams[agents_constants.VI.TRANSITION_TENSOR].value
        R = self.experiment_config.hparams[agents_constants.VI.REWARD_TENSOR].value
        Logger.__call__().get_logger().info(f"Starting the value iteration algorithm, theta:{theta}, "
                                            f"num_states:{num_states}, discount_factor: {discount_factor}, "
                                            f"num_actions: {num_actions}")
        V, policy, deltas, avg_returns, running_avg_returns = self.vi(
            T=np.array(T), num_states=num_states, num_actions=num_actions,
            R=np.array(R), theta=theta, discount_factor=discount_factor)
        exp_result.all_metrics[seed][agents_constants.VI.DELTA] = deltas
        exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN] = avg_returns
        exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN] = running_avg_returns
        lookup_table = list(policy)
        for i in range(len(lookup_table)):
            lookup_table[i] = list(lookup_table[i])
        tabular_policy = TabularPolicy(player_type=self.experiment_config.player_type,
                                       actions=self.simulation_env_config.joint_action_space_config.action_spaces[
                                           self.experiment_config.player_idx].actions,
                                       agent_type=self.experiment_config.agent_type, value_function=list(V),
                                       lookup_table=lookup_table, simulation_name=self.simulation_env_config.name,
                                       avg_R=avg_returns[-1])
        exp_result.policies[seed] = tabular_policy
        return exp_result

    def one_step_lookahead(self, state, V, num_actions, num_states, T, discount_factor, R) -> npt.NDArray[Any]:
        """
        Performs a one-step lookahead for value iteration
        :param state: the current state
        :param V: the current value function
        :param num_actions: the number of actions
        :param num_states: the number of states
        :param T: the transition kernel
        :param discount_factor: the discount factor
        :param R: the table with rewards
        :param next_state_lookahead: the next state lookahead table
        :return: an array with lookahead values
        """
        A = np.zeros(num_actions)
        for a in range(num_actions):
            reward = R[a][state]
            for next_state in range(num_states):
                prob = T[a][state][next_state]
                A[a] += prob * (reward + discount_factor * V[next_state])
        return A

    def vi(self, T: npt.NDArray[Any], num_states: int, num_actions: int, R: npt.NDArray[Any],
           theta=0.0001, discount_factor=1.0) \
            -> Tuple[npt.NDArray[Any], npt.NDArray[Any], List[Any], List[Any], List[Any]]:
        """
        An implementation of the Value Iteration algorithm
        :param T: the transition kernel T
        :param num_states: the number of states
        :param num_actions: the number of actions
        :param state_to_id: the state-to-id lookup table
        :param HP: the table with hack probabilities
        :param R: the table with rewards
        :param next_state_lookahead: the next-state-lookahead table
        :param theta: convergence threshold
        :param discount_factor: the discount factor
        :return: (greedy policy, value function, deltas, average_returns)
        """
        deltas = []
        average_returns = []
        running_average_returns = []
        V = np.zeros(num_states)
        iteration = 0
        while True:
            # Stopping condition
            delta = 0
            # Update each state...
            for s in range(num_states):
                # Do a one-step lookahead to find the best action
                A = self.one_step_lookahead(s, V, num_actions, num_states, T, discount_factor, R)
                best_action_value = np.max(A)
                # Calculate delta across all states seen so far
                delta = max(delta, np.abs(best_action_value - V[s]))
                # Update the value function. Ref: Sutton book eq. 4.10.
                V[s] = best_action_value

            deltas.append(delta)

            avg_return = -1.0
            if iteration % self.experiment_config.hparams[agents_constants.COMMON.EVAL_EVERY].value == 0:
                policy = self.create_policy_from_value_function(num_states=num_states, num_actions=num_actions, V=V,
                                                                T=T, discount_factor=discount_factor, R=R)
                avg_return = self.evaluate_policy(policy=policy, eval_batch_size=self.experiment_config.hparams[
                    agents_constants.COMMON.EVAL_BATCH_SIZE].value)
                average_returns.append(avg_return)
                running_avg_J = ExperimentUtil.running_average(
                    average_returns,
                    self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value)
                running_average_returns.append(running_avg_J)

            if iteration % self.experiment_config.log_every == 0 and iteration > 0:
                Logger.__call__().get_logger().info(f"[VI] i:{iteration}, delta: {delta}, "
                                                    f"theta: {theta}, avg_return: {avg_return}")
            iteration += 1

            # Check if we can stop
            if delta < theta:
                break

        policy = self.create_policy_from_value_function(num_states=num_states, num_actions=num_actions, V=V, T=T,
                                                        discount_factor=discount_factor, R=R)
        return V, policy, deltas, average_returns, running_average_returns

    def evaluate_policy(self, policy: npt.NDArray[Any], eval_batch_size: int) -> float:
        """
        Evalutes a tabular policy

        :param policy: the tabular policy to evaluate
        :param eval_batch_size: the batch size
        :return: None
        """
        if self.env is None:
            raise ValueError("Need to specify an environment to run policy evaluation")
        returns = []
        for i in range(eval_batch_size):
            done = False
            s, _ = self.env.reset()
            R = 0
            while not done:
                if self.simulation_env_config.gym_env_name == "csle-intrusion-response-game-local-pomdp-defender-v1":
                    a = np.random.choice(np.arange(0, len(policy[int(s[0])])), p=policy[int(s[0])])
                    s, r, done, _, info = self.env.step(a)
                    done = True
                else:
                    s, r, done, _, info = self.env.step(policy)
                R += r
            returns.append(R)
        avg_return = np.mean(returns)
        return float(avg_return)

    def create_policy_from_value_function(self, num_states: int, num_actions: int, V: npt.NDArray[Any],
                                          T: npt.NDArray[Any], discount_factor: float, R: npt.NDArray[Any]) \
            -> npt.NDArray[Any]:
        """
        Creates a tabular policy from a value function

        :param num_states: the number of states
        :param num_actions: the number of actions
        :param V: the value function
        :param T: the transition operator
        :param discount_factor: the discount factor
        :param R: the reward function
        :return: the tabular policy
        """
        # Create a deterministic policy using the optimal value function
        policy = np.zeros([num_states, num_actions])
        for s in range(num_states):
            # One step lookahead to find the best action for this state
            A = self.one_step_lookahead(s, V, num_actions, num_states, T, discount_factor, R)
            best_action = np.argmax(A)
            # Always take the best action
            policy[s, best_action] = 1.0
        return policy
