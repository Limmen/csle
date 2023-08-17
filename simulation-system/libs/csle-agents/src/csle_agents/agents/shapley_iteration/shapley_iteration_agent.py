from typing import List, Optional, Tuple, Any
import math
import time
import os
import numpy as np
import numpy.typing as npt
import pulp
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
from csle_common.util.general_util import GeneralUtil
from csle_agents.agents.base.base_agent import BaseAgent
import csle_agents.constants.constants as agents_constants


class ShapleyIterationAgent(BaseAgent):
    """
    Shapley Iteration Agent
    """

    def __init__(self, simulation_env_config: SimulationEnvConfig, experiment_config: ExperimentConfig,
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
        assert experiment_config.agent_type == AgentType.SHAPLEY_ITERATION
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
        exp_result.plot_metrics.append(agents_constants.SHAPLEY_ITERATION.DELTA)

        descr = f"Computation of Nash equilibrium with the Shapley Iteration algorithm using " \
                f"simulation:{self.simulation_env_config.name}"

        for seed in self.experiment_config.random_seeds:
            exp_result.all_metrics[seed] = {}
            exp_result.all_metrics[seed][agents_constants.SHAPLEY_ITERATION.DELTA] = []

        # Initialize training job
        if self.training_job is None:
            self.training_job = TrainingJobConfig(
                simulation_env_name=self.simulation_env_config.name, experiment_config=self.experiment_config,
                progress_percentage=0, pid=pid, experiment_result=exp_result,
                emulation_env_name=None, simulation_traces=[],
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
            exp_result = self.shapley_iteration(exp_result=exp_result, seed=seed)

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
                agents_constants.SHAPLEY_ITERATION.TRANSITION_TENSOR,
                agents_constants.SHAPLEY_ITERATION.REWARD_TENSOR,
                agents_constants.SHAPLEY_ITERATION.STATE_SPACE,
                agents_constants.SHAPLEY_ITERATION.ACTION_SPACE_PLAYER_1,
                agents_constants.SHAPLEY_ITERATION.ACTION_SPACE_PLAYER_2, agents_constants.SHAPLEY_ITERATION.DELTA,
                agents_constants.SHAPLEY_ITERATION.N]

    def shapley_iteration(self, exp_result: ExperimentResult, seed: int) -> ExperimentResult:
        """
        Runs the Shapley iteration algorithm

        :param exp_result: the experiment result object
        :param seed: the random seed
        :return: the updated experiment result
        """
        discount_factor = self.experiment_config.hparams[agents_constants.COMMON.GAMMA].value
        T = self.experiment_config.hparams[agents_constants.SHAPLEY_ITERATION.TRANSITION_TENSOR].value
        R = self.experiment_config.hparams[agents_constants.SHAPLEY_ITERATION.REWARD_TENSOR].value
        A1 = self.experiment_config.hparams[agents_constants.SHAPLEY_ITERATION.ACTION_SPACE_PLAYER_1].value
        A2 = self.experiment_config.hparams[agents_constants.SHAPLEY_ITERATION.ACTION_SPACE_PLAYER_2].value
        S = self.experiment_config.hparams[agents_constants.SHAPLEY_ITERATION.STATE_SPACE].value
        N = self.experiment_config.hparams[agents_constants.SHAPLEY_ITERATION.N].value
        delta = self.experiment_config.hparams[agents_constants.SHAPLEY_ITERATION.DELTA].value
        Logger.__call__().get_logger().info("Starting the shapley iteration algorithm")
        V, maximin_strategies, minimax_strategies, auxillary_games, deltas = self.si(
            S=np.array(S), A1=np.array(A1), A2=np.array(A2), R=np.array(R), T=np.array(T), gamma=discount_factor,
            max_iterations=N, delta_threshold=delta)
        exp_result.all_metrics[seed][agents_constants.VI.DELTA] = deltas
        tabular_policy_p1 = TabularPolicy(
            player_type=self.experiment_config.player_type,
            actions=self.simulation_env_config.joint_action_space_config.action_spaces[
                self.experiment_config.player_idx].actions, agent_type=self.experiment_config.agent_type,
            value_function=list(V), lookup_table=list(maximin_strategies),
            simulation_name=self.simulation_env_config.name, avg_R=V[0])
        tabular_policy_p2 = TabularPolicy(
            player_type=self.experiment_config.player_type,
            actions=self.simulation_env_config.joint_action_space_config.action_spaces[
                self.experiment_config.player_idx].actions, agent_type=self.experiment_config.agent_type,
            value_function=list(V), lookup_table=list(minimax_strategies),
            simulation_name=self.simulation_env_config.name, avg_R=V[0])
        exp_result.policies[seed] = tabular_policy_p1
        exp_result.policies[seed + 1] = tabular_policy_p2
        return exp_result

    def auxillary_game(self, V: npt.NDArray[Any], gamma: float, S: npt.NDArray[Any], s: int,
                       A1: npt.NDArray[Any], A2: npt.NDArray[Any], R: npt.NDArray[Any],
                       T: npt.NDArray[Any]) -> npt.NDArray[Any]:
        """
        Creates an auxillary matrix game based on the value function V

        :param V: the value function
        :param gamma: the discount factor
        :param S: the set of states
        :param s: the state s
        :param A1: the set of actions of player 1
        :param A2: the set of actions of player 2
        :param R: the reward tensor
        :param T: the transition tensor
        :return: the matrix auxillary game
        """
        A = np.zeros((len(A1), len(A2)))
        for a1 in A1:
            for a2 in A2:
                immediate_reward = R[a1][a2][s]
                expected_future_reward = 0.0
                for s_prime in S:
                    expected_future_reward += T[a1][a2][s][s_prime] * V[s_prime]
                expected_future_reward = expected_future_reward * gamma
                A[a1][a2] = immediate_reward + expected_future_reward
        return A

    def compute_matrix_game_value(self, A: npt.NDArray[Any], A1: npt.NDArray[Any], A2: npt.NDArray[Any],
                                  maximizer: bool = True):
        """

        :param A: the matrix game
        :param A1: the set of actions of player 1
        :param A2: the set of acitons of player 2
        :param maximizer: a boolean flag indicating whether the maximin or minimax strategy should be computed
        :return: (val(A), maximin/minimax)
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

        # Obtain solution
        optimal_strategy = list(map(lambda x: x.varValue, s))
        value = v.varValue
        return value, optimal_strategy

    def si(self, S: npt.NDArray[Any], A1: npt.NDArray[Any], A2: npt.NDArray[Any], R: npt.NDArray[Any],
           T: npt.NDArray[Any], gamma: float = 1, max_iterations: int = 500, delta_threshold: float = 0.1) \
            -> Tuple[npt.NDArray[Any], npt.NDArray[Any], npt.NDArray[Any], npt.NDArray[Any], List[float]]:
        """
        Shapley Iteration (L. Shapley 1953)

        :param S: the set of states of the SG
        :param A1: the set of actions of player 1 in the SG
        :param A2: the set of actions of player 2 in the SG
        :param R: the reward tensor in the SG
        :param T: the transition tensor in the SG
        :param gamma: the discount factor
        :param max_iterations: the maximum number of iterations
        :param delta_threshold: the stopping threshold
        :return: the value function, the set of maximin strategies for all stage games,
        the set of minimax strategies for all stage games, and the stage games themselves
        """
        deltas = []
        num_states = len(S)
        V = np.zeros(num_states)
        for i in range(max_iterations):
            delta = 0.0
            auxillary_games = []
            for s in S:
                A = self.auxillary_game(V=V, gamma=gamma, S=S, s=s, A1=A1, A2=A2, R=R, T=T)
                auxillary_games.append(A)

            for s in S:
                value, _ = self.compute_matrix_game_value(A=auxillary_games[s], A1=A1, A2=A2, maximizer=True)
                delta += abs(V[s] - value)
                V[s] = value

            deltas.append(delta)

            if i % self.experiment_config.log_every == 0 and i > 0:
                Logger.__call__().get_logger().info(f"[Shapley iteration] i:{i}, delta: {delta}, V: {V}")

            if delta <= delta_threshold:
                break

        maximin_strategies = []
        minimax_strategies = []
        auxillary_games = []
        for s in S:
            A = self.auxillary_game(V=V, gamma=gamma, S=S, s=s, A1=A1, A2=A2, R=R, T=T)
            v1, maximin_strategy = self.compute_matrix_game_value(A=A, A1=A1, A2=A2, maximizer=True)
            v2, minimax_strategy = self.compute_matrix_game_value(A=A, A1=A1, A2=A2, maximizer=False)
            maximin_strategies.append(maximin_strategy)
            minimax_strategies.append(minimax_strategy)
            auxillary_games.append(A)

        return V, np.array(maximin_strategies), np.array(minimax_strategies), np.array(auxillary_games), deltas
