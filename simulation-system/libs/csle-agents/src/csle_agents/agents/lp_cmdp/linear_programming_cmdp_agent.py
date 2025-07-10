from typing import Union, List, Dict, Optional, Tuple, Any
import math
import time
import gymnasium as gym
import os
import numpy as np
import numpy.typing as npt
import pulp
import gym_csle_stopping_game.constants.constants as env_constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.experiment_execution import ExperimentExecution
from csle_common.dao.training.experiment_result import ExperimentResult
from csle_common.dao.training.agent_type import AgentType
from csle_common.util.experiment_util import ExperimentUtil
from csle_common.logging.log import Logger
from csle_common.dao.training.tabular_policy import TabularPolicy
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.jobs.training_job_config import TrainingJobConfig
from csle_common.util.general_util import GeneralUtil
from csle_common.dao.simulation_config.base_env import BaseEnv
from csle_agents.agents.base.base_agent import BaseAgent
import csle_agents.constants.constants as agents_constants


class LinearProgrammingCMDPAgent(BaseAgent):
    """
    Linear programming agent for CMDPs
    """

    def __init__(self, simulation_env_config: SimulationEnvConfig,
                 experiment_config: ExperimentConfig, env: Optional[BaseEnv] = None,
                 emulation_env_config: Union[None, EmulationEnvConfig] = None,
                 training_job: Optional[TrainingJobConfig] = None, save_to_metastore: bool = True):
        """
        Initializes the Linear programming agent for normal-form games

        :param simulation_env_config: the simulation env config
        :param emulation_env_config: the emulation env config
        :param experiment_config: the experiment config
        :param env: (optional) the gym environment to use for simulation
        :param training_job: (optional) a training job configuration
        :param save_to_metastore: boolean flag that can be set to avoid saving results and progress to the metastore
        """
        super().__init__(simulation_env_config=simulation_env_config, emulation_env_config=emulation_env_config,
                         experiment_config=experiment_config)
        assert experiment_config.agent_type == AgentType.LINEAR_PROGRAMMING_CMDP
        self.env = env
        self.training_job = training_job
        self.save_to_metastore = save_to_metastore

    def train(self) -> ExperimentExecution:
        """
        Performs the policy training for the given random seeds using linear programming

        :return: the training metrics and the trained policies
        """
        pid = os.getpid()

        # Initialize metrics
        exp_result = ExperimentResult()
        exp_result.plot_metrics.append(agents_constants.COMMON.AVERAGE_RETURN)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_RETURN)
        exp_result.plot_metrics.append(env_constants.ENV_METRICS.INTRUSION_LENGTH)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_LENGTH)
        exp_result.plot_metrics.append(env_constants.ENV_METRICS.INTRUSION_START)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_START)
        exp_result.plot_metrics.append(env_constants.ENV_METRICS.TIME_HORIZON)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON)
        exp_result.plot_metrics.append(env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN)
        exp_result.plot_metrics.append(env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN)

        descr = f"Training of policies with the linear programming for CMDPs algorithm using " \
                f"simulation:{self.simulation_env_config.name}"
        for seed in self.experiment_config.random_seeds:
            exp_result.all_metrics[seed] = {}
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN] = []
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
            self.training_job = TrainingJobConfig(
                simulation_env_name=self.simulation_env_config.name, experiment_config=self.experiment_config,
                progress_percentage=0, pid=pid, experiment_result=exp_result,
                emulation_env_name="", simulation_traces=[],
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
        emulation_name = None
        if self.emulation_env_config is not None:
            emulation_name = self.emulation_env_config.name
        simulation_name = self.simulation_env_config.name
        self.exp_execution = ExperimentExecution(
            result=exp_result, config=self.experiment_config, timestamp=ts, emulation_name=emulation_name,
            simulation_name=simulation_name, descr=descr, log_file_path=self.training_job.log_file_path)
        if self.save_to_metastore:
            exp_execution_id = MetastoreFacade.save_experiment_execution(self.exp_execution)
            self.exp_execution.id = exp_execution_id

        config = self.simulation_env_config.simulation_env_input_config
        if self.env is None:
            self.env = gym.make(self.simulation_env_config.gym_env_name, config=config)
        for seed in self.experiment_config.random_seeds:
            ExperimentUtil.set_seed(seed)
            exp_result = self.linear_programming_cmdp(
                exp_result=exp_result, seed=seed, training_job=self.training_job,
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
        return [agents_constants.LP_FOR_CMDPs.ACTIONS,
                agents_constants.LP_FOR_CMDPs.STATES,
                agents_constants.LP_FOR_CMDPs.COST_TENSOR,
                agents_constants.LP_FOR_CMDPs.TRANSITION_TENSOR,
                agents_constants.LP_FOR_CMDPs.CONSTRAINT_COST_TENSORS,
                agents_constants.LP_FOR_CMDPs.CONSTRAINT_COST_THRESHOLDS,
                agents_constants.COMMON.EVAL_BATCH_SIZE,
                agents_constants.COMMON.CONFIDENCE_INTERVAL,
                agents_constants.COMMON.RUNNING_AVERAGE]

    def linear_programming_cmdp(self, exp_result: ExperimentResult, seed: int,
                                training_job: TrainingJobConfig, random_seeds: List[int]) -> ExperimentResult:
        """
        Runs the linear programming algorithm for normal-form games

        :param exp_result: the experiment result object to store the result
        :param seed: the seed
        :param training_job: the training job config
        :param random_seeds: list of seeds
        :return: the updated experiment result and the trained policy
        """
        # Hyperparameters
        actions = np.array(self.experiment_config.hparams[agents_constants.LP_FOR_CMDPs.ACTIONS].value)
        states = np.array(self.experiment_config.hparams[agents_constants.LP_FOR_CMDPs.STATES].value)
        cost_tensor = np.array(self.experiment_config.hparams[agents_constants.LP_FOR_CMDPs.COST_TENSOR].value)
        transition_tensor = np.array(
            self.experiment_config.hparams[agents_constants.LP_FOR_CMDPs.TRANSITION_TENSOR].value)
        constraint_cost_tensors = np.array(
            self.experiment_config.hparams[agents_constants.LP_FOR_CMDPs.CONSTRAINT_COST_TENSORS].value)
        constraint_cost_thresholds = np.array(
            self.experiment_config.hparams[agents_constants.LP_FOR_CMDPs.CONSTRAINT_COST_THRESHOLDS].value)

        solution_status, optimal_occupancy_measures, optimal_strategy, expected_constraint_costs, objective_value = (
            self.lp(
                actions=actions, states=states, cost_tensor=cost_tensor, transition_tensor=transition_tensor,
                constraint_cost_tensors=constraint_cost_tensors, constraint_cost_thresholds=constraint_cost_thresholds
            ))
        # Log average return
        J = objective_value
        exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN].append(J)
        running_avg_J = ExperimentUtil.running_average(
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN],
            self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value)
        exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN].append(running_avg_J)

        progress = 1
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
            f"[Linear programming for normal-form games] J:{J}, "
            f"J_avg_{self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value}:"
            f"{running_avg_J}")

        policy = TabularPolicy(
            lookup_table=optimal_strategy, simulation_name=self.simulation_env_config.name,
            player_type=self.experiment_config.player_type,
            actions=self.simulation_env_config.joint_action_space_config.action_spaces[0].actions,
            avg_R=J, agent_type=AgentType.LINEAR_PROGRAMMING_CMDP
        )
        exp_result.policies[seed] = policy
        # Save policy
        if self.save_to_metastore:
            MetastoreFacade.save_tabular_policy(tabular_policy=policy)
        return exp_result

    @staticmethod
    def lp(actions: npt.NDArray[Any], states: npt.NDArray[Any], cost_tensor: npt.NDArray[Any],
           transition_tensor: npt.NDArray[Any],
           constraint_cost_tensors: npt.NDArray[Any],
           constraint_cost_thresholds: npt.NDArray[Any]) \
            -> Tuple[str, npt.NDArray[Any], npt.NDArray[Any], npt.NDArray[Any], float]:
        """
        Linear program for solving a CMDP (see Altman '99 for details)

        :param actions: the action space
        :param states: the state space
        :param cost_tensor: the cost tensor
        :param transition_tensor: the transition tensor
        :param constraint_cost_tensors: the constraint cost tensors
        :param constraint_cost_thresholds: the constraint cost thresholds
        :return: the solution status, the optimal occupancy measure, the optimal strategy, the expeted constraint cost,
                 the objective value
        """
        problem = pulp.LpProblem("AvgCostMdp", pulp.LpMinimize)

        # Decision variables, state-action occupancy measures
        occupancy_measures = []
        for s in states:
            occupancy_measures_s = []
            for a in actions:
                s_a_occupancy = pulp.LpVariable(f"occupancy_{s}_{a}", lowBound=0, upBound=1, cat=pulp.LpContinuous)
                occupancy_measures_s.append(s_a_occupancy)
            occupancy_measures.append(occupancy_measures_s)

        # The non-zero constraints
        for s in states:
            for a in actions:
                problem += occupancy_measures[s][a] >= 0, f"NonZeroConstraint_{s}_{a}"

        # The probability constraints
        occupancy_measures_sum = 0
        for s in states:
            for a in actions:
                occupancy_measures_sum += occupancy_measures[s][a]
        problem += occupancy_measures_sum == 1, "StochasticConstraint"

        # The transition constraints
        for s_prime in states:
            rho_s_prime_a_sum = 0
            for a in actions:
                rho_s_prime_a_sum += occupancy_measures[s_prime][a]

            transition_sum = 0
            for s in states:
                for a in actions:
                    transition_sum += occupancy_measures[s][a] * transition_tensor[a][s][s_prime]

            problem += rho_s_prime_a_sum == transition_sum, f"TransitionConstraint_{s_prime}"

        # The cost constraints
        for i in range(len(constraint_cost_tensors)):
            expected_constraint_cost = 0.0
            for s in states:
                for a in actions:
                    if (isinstance(constraint_cost_tensors[i][a], list) or
                            isinstance(constraint_cost_tensors[i][a], np.ndarray)):
                        expected_constraint_cost += occupancy_measures[s][a] * constraint_cost_tensors[i][a][s]
                    else:
                        expected_constraint_cost += occupancy_measures[s][a] * constraint_cost_tensors[i][s]
            threshold = constraint_cost_thresholds[i]
            problem += expected_constraint_cost >= threshold, f"ExpectedCostConstraint_{i}"

        # Objective function
        avg_cost = 0
        for s in states:
            for a in actions:
                if isinstance(cost_tensor[a], list):
                    avg_cost += cost_tensor[a][s] * occupancy_measures[s][a]
                else:
                    avg_cost += cost_tensor[s] * occupancy_measures[s][a]
        problem += avg_cost, "Average cost"

        # Solve
        problem.solve(pulp.PULP_CBC_CMD(msg=0))

        # Extract solution
        optimal_occupancy_measures = []
        for i in range(len(occupancy_measures)):
            optimal_occupanct_measures_s = []
            for j in range(len(occupancy_measures[i])):
                optimal_occupanct_measures_s.append(occupancy_measures[i][j].varValue)
            optimal_occupancy_measures.append(optimal_occupanct_measures_s)
        optimal_occupancy_measures = optimal_occupancy_measures
        optimal_strategy = []
        for s in states:
            optimal_strategy_s = []
            for a in actions:
                normalizing_sum = 0
                for s_prime in states:
                    normalizing_sum += optimal_occupancy_measures[s_prime][a]
                if normalizing_sum != 0:
                    action_prob = optimal_occupancy_measures[s][a] / normalizing_sum
                else:
                    action_prob = 0
                optimal_strategy_s.append(action_prob)
            optimal_strategy.append(optimal_strategy_s)
        expected_constraint_costs = []
        for i in range(len(constraint_cost_tensors)):
            expected_constraint_cost = 0.0
            for s in states:
                for a in actions:
                    if (isinstance(constraint_cost_tensors[i][a], list) or
                            isinstance(constraint_cost_tensors[i][a], np.ndarray)):
                        expected_constraint_cost += optimal_occupancy_measures[s][a] * constraint_cost_tensors[i][a][s]
                    else:
                        expected_constraint_cost += optimal_occupancy_measures[s][a] * constraint_cost_tensors[i][s]
            expected_constraint_costs.append(expected_constraint_cost)
        return (pulp.LpStatus[problem.status],
                np.array(optimal_occupancy_measures), np.array(optimal_strategy), np.array(expected_constraint_costs),
                problem.objective.value())

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
