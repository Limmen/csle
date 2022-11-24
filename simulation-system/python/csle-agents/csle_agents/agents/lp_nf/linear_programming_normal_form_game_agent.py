import math
from typing import Union, List, Dict, Optional, Tuple
import time
import gym
import os
import numpy as np
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
from csle_common.dao.training.vector_policy import VectorPolicy
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.jobs.training_job_config import TrainingJobConfig
from csle_agents.agents.base.base_agent import BaseAgent
import csle_agents.constants.constants as agents_constants


class LinearProgrammingNormalFormGameAgent(BaseAgent):
    """
    Linear programming agent for normal-form games
    """

    def __init__(self, simulation_env_config: SimulationEnvConfig,
                 experiment_config: ExperimentConfig, env: Optional[gym.Env] = None,
                 emulation_env_config: Union[None, EmulationEnvConfig] = None,
                 training_job: Optional[TrainingJobConfig] = None, save_to_metastore: bool = True):
        """
        Initializes the Linar programming agent for normal-form games

        :param simulation_env_config: the simulation env config
        :param emulation_env_config: the emulation env config
        :param experiment_config: the experiment config
        :param env: (optional) the gym environment to use for simulation
        :param training_job: (optional) a training job configuration
        :param save_to_metastore: boolean flag that can be set to avoid saving results and progress to the metastore
        """
        super().__init__(simulation_env_config=simulation_env_config, emulation_env_config=emulation_env_config,
                         experiment_config=experiment_config)
        assert experiment_config.agent_type == AgentType.LINEAR_PROGRAMMING_NORMAL_FORM
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

        descr = f"Training of policies with the linear programming for normal-form games algorithm using " \
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
                emulation_env_name=None, simulation_traces=[],
                num_cached_traces=agents_constants.COMMON.NUM_CACHED_SIMULATION_TRACES,
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
            exp_result = self.linear_programming_normal_form(
                exp_result=exp_result, seed=seed, training_job=self.training_job,
                random_seeds=self.experiment_config.random_seeds)

            # Save latest trace
            if self.save_to_metastore:
                if len(self.env.get_traces()) > 0:
                    MetastoreFacade.save_simulation_trace(self.env.get_traces()[-1])
            self.env.reset_traces()

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

        traces = self.env.get_traces()
        if len(traces) > 0 and self.save_to_metastore:
            MetastoreFacade.save_simulation_trace(traces[-1])
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
        return [agents_constants.LP_FOR_NF_GAMES.PAYOFF_MATRIX, agents_constants.LP_FOR_NF_GAMES.ACTION_SPACE_PLAYER_1,
                agents_constants.LP_FOR_NF_GAMES.ACTION_SPACE_PLAYER_2,
                agents_constants.COMMON.EVAL_BATCH_SIZE,
                agents_constants.COMMON.CONFIDENCE_INTERVAL,
                agents_constants.COMMON.RUNNING_AVERAGE]

    def linear_programming_normal_form(self, exp_result: ExperimentResult, seed: int,
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
        payoff_matrix = np.array(self.experiment_config.hparams[agents_constants.LP_FOR_NF_GAMES.PAYOFF_MATRIX].value)
        A1 = np.array(self.experiment_config.hparams[agents_constants.LP_FOR_NF_GAMES.ACTION_SPACE_PLAYER_1].value)
        A2 = np.array(self.experiment_config.hparams[agents_constants.LP_FOR_NF_GAMES.ACTION_SPACE_PLAYER_2].value)

        maximin_strategy, minimax_strategy, val = self.compute_equilibrium_strategies_in_matrix_game(
            A=payoff_matrix, A1=A1, A2=A2)
        # Log average return
        J = val
        exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN].append(J)
        running_avg_J = ExperimentUtil.running_average(
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN],
            self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value)
        exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN].append(running_avg_J)

        progress = 1
        training_job.progress_percentage = progress
        training_job.experiment_result = exp_result
        if len(self.env.get_traces()) > 0:
            training_job.simulation_traces.append(self.env.get_traces()[-1])
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

        p1_policy = VectorPolicy(policy_vector=maximin_strategy, simulation_name=self.simulation_env_config.name,
                                 player_type=self.experiment_config.player_type,
                                 actions=list(range(len(maximin_strategy))),
                                 avg_R=J, agent_type=AgentType.LINEAR_PROGRAMMING_NORMAL_FORM)
        p2_policy = VectorPolicy(policy_vector=minimax_strategy, simulation_name=self.simulation_env_config.name,
                                 player_type=self.experiment_config.player_type,
                                 actions=list(range(len(minimax_strategy))),
                                 avg_R=J,
                                 agent_type=AgentType.LINEAR_PROGRAMMING_NORMAL_FORM)
        exp_result.policies[seed] = p1_policy
        exp_result.policies[seed + 1] = p2_policy
        # Save policy
        if self.save_to_metastore:
            MetastoreFacade.save_vector_policy(vector_policy=p1_policy)
            MetastoreFacade.save_vector_policy(vector_policy=p2_policy)
        return exp_result

    def compute_equilibrium_strategies_in_matrix_game(self, A: np.ndarray, A1: np.ndarray, A2: np.ndarray) \
            -> Tuple[np.ndarray, np.ndarray, float]:
        """
        Computes equilibrium strategies in a matrix game

        :param A: the matrix game
        :param A1: the action set of player 1 (the maximizer)
        :param A2: the action set of player 2 (the minimizer)
        :return: the equilibrium strategy profile and the value
        """
        v1, maximin_strategy = self.compute_matrix_game_value(A=A, A1=A1, A2=A2, maximizer=True)
        v2, minimax_strategy = self.compute_matrix_game_value(A=A, A1=A1, A2=A2, maximizer=False)
        return maximin_strategy, minimax_strategy, v1

    def compute_matrix_game_value(self, A: np.ndarray, A1: np.ndarray, A2: np.ndarray, maximizer: bool = True) \
            -> Tuple[any, np.ndarray]:
        """
        Uses LP to compute the value of a a matrix game, also computes the maximin or minimax strategy

        :param A: the matrix game
        :param A1: the action set of player 1
        :param A2: the action set of player 2
        :param maximizer: boolean flag whether to compute the maximin strategy or minimax strategy
        :return: (val(A), maximin or minimax strategy)
        """
        if maximizer:
            problem = pulp.LpProblem("AuxillaryGame", pulp.LpMaximize)
            Ai = A1
        else:
            problem = pulp.LpProblem("AuxillaryGame", pulp.LpMinimize)
            Ai = A2

        # Decision variables, strategy-weights
        s = []
        for ai in Ai:
            si = pulp.LpVariable("s_" + str(ai), lowBound=0, upBound=1, cat=pulp.LpContinuous)
            s.append(si)

        # Auxillary decision variable, value of the game v
        v = pulp.LpVariable("v", lowBound=None, upBound=None, cat=pulp.LpContinuous)

        # The objective function
        problem += v, "Value of the game"

        # The constraints
        if maximizer:
            for j in range(A.shape[1]):
                sum = 0
                for i in range(A.shape[0]):
                    sum += s[i] * A[i][j]
                problem += sum >= v, "SecurityValueConstraint_" + str(j)
        else:
            for i in range(A.shape[0]):
                sum = 0
                for j in range(A.shape[1]):
                    sum += s[j] * A[i][j]
                problem += sum <= v, "SecurityValueConstraint_" + str(i)

        strategy_weights_sum = 0
        for si in s:
            strategy_weights_sum += si
        problem += strategy_weights_sum == 1, "probabilities sum"

        # Solve
        problem.solve(pulp.PULP_CBC_CMD(msg=0))

        # Extract solution
        optimal_strategy = np.array(list(map(lambda x: x.varValue, s)))
        value = v.varValue

        return value, optimal_strategy

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
