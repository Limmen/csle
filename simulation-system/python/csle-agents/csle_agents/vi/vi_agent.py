import math
from typing import Union, List, Optional, Tuple
import time
import os
import numpy as np
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.experiment_result import ExperimentResult
from csle_common.dao.training.agent_type import AgentType
from csle_common.util.experiment_util import ExperimentUtil
from csle_common.logging.log import Logger
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.jobs.training_job_config import TrainingJobConfig
from csle_agents.base.base_agent import BaseAgent
import csle_agents.constants.constants as agents_constants
from csle_common.dao.training.experiment_execution import ExperimentExecution


class VIAgent(BaseAgent):
    """
    Value Iteration Agent
    """

    def __init__(self, simulation_env_config: SimulationEnvConfig,
                 experiment_config: ExperimentConfig,
                 training_job: Optional[TrainingJobConfig] = None, save_to_metastore : bool = True):
        """
        Initializes the value iteration agent

        :param simulation_env_config: configuration of the simulation environment
        :param experiment_config: the experiment configuration
        :param training_job: an existing training job to use (optional)
        :param save_to_metastore: boolean flag whether to save the execution to the metastore
        """
        super().__init__(simulation_env_config=simulation_env_config, emulation_env_config=None,
                         experiment_config=experiment_config)
        assert experiment_config.agent_type == AgentType.VALUE_ITERATION
        self.training_job = training_job
        self.save_to_metastore = save_to_metastore

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

        descr = f"Computation of V* with the Value Iteartion algorithm using " \
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
            exp_result = self.value_iteration(exp_result=exp_result, seed=seed, training_job=self.training_job,
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
                    ci = ExperimentUtil.mean_confidence_interval(data=seed_values,
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
        return [agents_constants.COMMON.EVAL_BATCH_SIZE, agents_constants.COMMON.CONFIDENCE_INTERVAL,
                agents_constants.COMMON.RUNNING_AVERAGE, agents_constants.COMMON.GAMMA,
                agents_constants.VI.THETA, agents_constants.VI.TRANSITION_TENSOR,
                agents_constants.VI.REWARD_TENSOR, agents_constants.VI.NUM_STATES, agents_constants.VI.NUM_ACTIONS]

    def value_iteration(self, exp_result: ExperimentResult, seed: int, training_job: TrainingJobConfig,
                        random_seeds: List[int]) -> ExperimentResult:
        theta = self.experiment_config.hparams[agents_constants.VI.THETA].value
        discount_factor = self.experiment_config.hparams[agents_constants.COMMON.GAMMA].value
        num_states = self.experiment_config.hparams[agents_constants.VI.NUM_STATES].value
        num_actions = self.experiment_config.hparams[agents_constants.VI.NUM_ACTIONS].value
        T = self.experiment_config.hparams[agents_constants.VI.TRANSITION_TENSOR].value
        R = self.experiment_config.hparams[agents_constants.VI.REWARD_TENSOR].value
        Logger.__call__().get_logger().info(f"Starting the value iteration algorithm, theta:{theta}, "
                                            f"num_states:{num_states}, discount_factor: {discount_factor}, "
                                            f"num_actions: {num_actions}")
        V, policy, deltas = self.vi(T=np.array(T), num_states=num_states, num_actions=num_actions,
                            R=np.array(R), theta=theta, discount_factor=discount_factor)
        exp_result.all_metrics[seed][agents_constants.VI.DELTA] = deltas
        exp_result.policies[seed] = policy
        exp_result.policies[seed] = V
        return exp_result

    def one_step_lookahead(self, state, V, num_actions, num_states, T, discount_factor, R) \
            -> np.ndarray:
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


    def vi(self, T: np.ndarray, num_states: int, num_actions: int, R: np.ndarray,
           theta=0.0001, discount_factor=1.0) -> Tuple[np.ndarray, np.ndarray, List]:
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
        :return: (greedy policy, value function, deltas)
        """
        deltas = []
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

            if iteration % self.experiment_config.log_every == 0 and iteration > 0:
                Logger.__call__().get_logger().info(f"[VI] i:{iteration}, delta: {delta}, theta: {theta}")
            iteration+=1

            deltas.append(delta)

            # Check if we can stop
            if delta < theta:
                break

        # Create a deterministic policy using the optimal value function
        policy = np.zeros([num_states, num_actions * 2])
        for s in range(num_states):
            # One step lookahead to find the best action for this state
            A = self.one_step_lookahead(s, V, num_actions, num_states, T, discount_factor, R)
            best_action = np.argmax(A)
            # Always take the best action
            policy[s, best_action] = 1.0

        return V, policy, deltas
