import math
from typing import List, Optional, Tuple
import time
import os
import numpy as np
import pulp
import itertools
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.experiment_result import ExperimentResult
from csle_common.dao.training.agent_type import AgentType
from csle_common.util.experiment_util import ExperimentUtil
from csle_common.logging.log import Logger
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.jobs.training_job_config import TrainingJobConfig
from csle_common.dao.training.experiment_execution import ExperimentExecution
from csle_common.dao.training.alpha_vectors_policy import AlphaVectorsPolicy
from csle_agents.agents.base.base_agent import BaseAgent
import csle_agents.constants.constants as agents_constants
import csle_agents.common.pruning as pruning


class HSVIOSPOSGAgent(BaseAgent):
    """
    HSVI for OS-POSGs agent
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
        assert experiment_config.agent_type == AgentType.HSVI_OS_POSG
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
        exp_result.plot_metrics.append(agents_constants.HSVI_OS_POSG.WIDTHS)
        exp_result.plot_metrics.append(agents_constants.HSVI_OS_POSG.EXCESSES)

        descr = f"Computation of Nash equilibrium with the OS-POSG algorithm using " \
                f"simulation:{self.simulation_env_config.name}"

        for seed in self.experiment_config.random_seeds:
            exp_result.all_metrics[seed] = {}
            exp_result.all_metrics[seed][agents_constants.HSVI_OS_POSG.WIDTHS] = []
            exp_result.all_metrics[seed][agents_constants.HSVI_OS_POSG.EXCESSES] = []

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
            exp_result = self.hsvi_os_posg(exp_result=exp_result, seed=seed)

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
                agents_constants.HSVI_OS_POSG.TRANSITION_TENSOR,
                agents_constants.HSVI_OS_POSG.REWARD_TENSOR,
                agents_constants.HSVI_OS_POSG.STATE_SPACE, agents_constants.HSVI_OS_POSG.ACTION_SPACE_PLAYER_1,
                agents_constants.HSVI_OS_POSG.ACTION_SPACE_PLAYER_2, agents_constants.HSVI_OS_POSG.EPSILON,
                agents_constants.HSVI_OS_POSG.PRUNE_FREQUENCY, agents_constants.HSVI_OS_POSG.OBSERVATION_SPACE,
                agents_constants.HSVI_OS_POSG.OBSERVATION_FUNCTION]

    def hsvi_os_posg(self, exp_result: ExperimentResult, seed: int) -> ExperimentResult:
        """
        Runs the Shapley iteration algorithm

        :param exp_result: the experiment result object
        :param seed: the random seed
        :return: the updated experiment result
        """
        discount_factor = self.experiment_config.hparams[agents_constants.COMMON.GAMMA].value
        T = self.experiment_config.hparams[agents_constants.HSVI_OS_POSG.TRANSITION_TENSOR].value
        R = self.experiment_config.hparams[agents_constants.HSVI_OS_POSG.REWARD_TENSOR].value
        A1 = self.experiment_config.hparams[agents_constants.HSVI_OS_POSG.ACTION_SPACE_PLAYER_1].value
        A2 = self.experiment_config.hparams[agents_constants.HSVI_OS_POSG.ACTION_SPACE_PLAYER_2].value
        S = self.experiment_config.hparams[agents_constants.HSVI_OS_POSG.STATE_SPACE].value
        O = self.experiment_config.hparams[agents_constants.HSVI_OS_POSG.OBSERVATION_SPACE].value
        Z = self.experiment_config.hparams[agents_constants.HSVI_OS_POSG.OBSERVATION_FUNCTION].value
        b0 = self.experiment_config.hparams[agents_constants.HSVI_OS_POSG.INITIAL_BELIEF].value
        epsilon = self.experiment_config.hparams[agents_constants.HSVI_OS_POSG.EPSILON].value
        prune_frequency = self.experiment_config.hparams[agents_constants.HSVI_OS_POSG.PRUNE_FREQUENCY].value
        Logger.__call__().get_logger().info("Starting the HSVI algorithm of OS-POSGs")
        alpha_vectors, widths, excesses = self.hsvi(
            O=np.array(O), Z=np.array(Z), R=np.array(R), T=np.array(T), A1=np.array(A1), A2=np.array(A2),
            S=np.array(S), gamma=discount_factor, b0=np.array(b0),
            epsilon=epsilon, prune_frequency=prune_frequency, D=None)
        exp_result.all_metrics[seed][agents_constants.HSVI_OS_POSG.WIDTHS] = widths
        exp_result.all_metrics[seed][agents_constants.HSVI_OS_POSG.EXCESSES] = excesses
        alpha_vec_policy = AlphaVectorsPolicy(
            player_type=self.experiment_config.player_type,
            actions=self.simulation_env_config.joint_action_space_config.action_spaces[
                self.experiment_config.player_idx].actions,
            states=self.simulation_env_config.state_space_config.states,
            alpha_vectors=alpha_vectors, agent_type=self.experiment_config.agent_type, avg_R=-1,
            simulation_name=self.simulation_env_config.name, transition_tensor=T, reward_tensor=R)
        exp_result.policies[seed] = alpha_vec_policy
        return exp_result

    def hsvi(self, O: np.ndarray, Z: np.ndarray, R: np.ndarray, T: np.ndarray, A1: np.ndarray,
             A2: np.ndarray, S: np.ndarray, gamma: float, b0: np.ndarray,
             epsilon: float, prune_frequency: int = 10,
             D: float = None):
        """
        Heuristic Search Value Iteration for zero-sum OS-POSGs (Horak, Bosansky, Pechoucek, 2017)

        The value function represents the utility player 1 can achieve in each possible initial belief of the game.

        :param O: set of observations of the OS-POSG
        :param Z: observation tensor of the OS-POSG
        :param R: reward tensor of the OS-POSG
        :param T: transition tensor of the OS-POSG
        :param A1: action set of P1 in the OS-POSG
        :param A2: action set of P2 in the OS-POSG
        :param S: state set of the OS-POSG
        :param gamma: discount factor
        :param b0: initial belief point
        :param epsilon: accuracy parameter
        :param prune_frequency: how often to prune the upper and lower bounds
        :param D: neighborhood parameter
        :return: None
        """
        lower_bound = self.initialize_lower_bound(S=S, A1=A1, A2=A2, gamma=gamma, b0=b0, R=R, T=T)
        upper_bound = self.initialize_upper_bound(T=T, R=R, A1=A1, A2=A2, S=S, gamma=gamma)

        delta = self.compute_delta(S=S, A1=A1, A2=A2, gamma=gamma, R=R)

        if D is None:
            D = self.sample_D(gamma=gamma, epsilon=epsilon, delta=delta)

        excess_val, w = self.excess(lower_bound=lower_bound, upper_bound=upper_bound, b=b0, S=S, epsilon=epsilon,
                                    gamma=gamma, t=0, delta=delta, D=D)

        iteration = 0
        cumulative_r = 0
        widths = []
        excesses = []

        while excess_val > 0:

            lower_bound, upper_bound = self.explore(
                b=b0, epsilon=epsilon, t=0, lower_bound=lower_bound, upper_bound=upper_bound,
                gamma=gamma, S=S, O=O, R=R, T=T, A1=A1, A2=A2, Z=Z, delta=delta, D=D)

            excess_val, w = self.excess(lower_bound=lower_bound, upper_bound=upper_bound, b=b0, S=S, epsilon=epsilon,
                                        gamma=gamma, t=0, delta=delta, D=D)
            widths.append(w)
            excesses.append(excess_val)

            if iteration > 1 and iteration % prune_frequency == 0:
                lower_bound = pruning.prune_lower_bound(lower_bound=lower_bound, S=S)
                upper_bound = self.prune_upper_bound(upper_bound=upper_bound, delta=delta, S=S)

            initial_belief_V_star_upper = self.upper_bound_value(upper_bound=upper_bound, b=b0, delta=delta, S=S)
            initial_belief_V_star_lower = self.lower_bound_value(lower_bound=lower_bound, b=b0, S=S)
            iteration += 1

            Logger.__call__().get_logger().info(
                f"[HSVI-OS-POSG] iteration: {iteration}, excess: {excess_val}, w: {w}, "
                f"epsilon: {epsilon}, R: {cumulative_r}, "
                f"UB size:{len(upper_bound)}, LB size:{len(lower_bound)}, "
                f"Upper V*[b0]: {initial_belief_V_star_upper},"
                f"Lower V*[b0]:{initial_belief_V_star_lower}")

        return lower_bound, widths, excesses

    def compute_delta(self, S: np.ndarray, A1: np.ndarray, A2: np.ndarray, gamma: float, R: np.ndarray) -> float:
        """
        The optimal value function V* of a OS-POSG is delta-Lipschitz continuous.
        To prove convergence of HSVI, we require that V_UB and V_LB are delta-Lipschitz continuous as well.
        This function computes the delta value according to (Horák, Bosansky, Kovařík, Kiekintveld, 2020)
        Specifically, delta = (U-L)/2 where L and U are teh lower respectively upper bounds on the game values.

        :param S: the set of states of the OS-POSG
        :param A1: the set of actions of player 1
        :param A2: the set of actions of player 2
        :param gamma: the discount factor
        :param R: the reward tensor
        :return: the delta value
        """
        temp = []
        for s in S:
            for a1 in A1:
                for a2 in A2:
                    temp.append(R[a1][a2][s] / (1 - gamma))
        L = min(temp)
        U = max(temp)
        delta = (U - L) / 2
        return delta

    def sample_D(self, gamma: float, epsilon: float, delta: float) -> float:
        """
        Samples the neighborhood parameter in the legal range.

        To ensure that the sequence rho is monotonically increasing and unbounded, we need to select the parameter D
        from the interval (0, (1-gamma)*epsilon/2delta)

        :param gamma: the discount factor
        :param epsilon: the epsilon accuracy parameter
        :param delta: the Lipschitz-continuity parameter
        :return: the neighborhood parameter D
        """
        min_val = 1.e-10
        max_val = ((1 - gamma) * epsilon) / (2 * delta)
        return (max_val - min_val) / 2

    def obtain_equilibrium_strategy_profiles_in_stage_game(
            self, lower_bound: List, upper_bound: List, b: np.ndarray, delta: float, S: np.ndarray, A1: np.ndarray,
            A2: np.ndarray, gamma: float, R: np.ndarray, O: np.ndarray, Z: np.ndarray, T: np.ndarray) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Computes equilibrium strategy profiles in the stage game constructed from the lower and upper
        bound value functions

        :param lower_bound: the lower bound  of V
        :param upper_bound:  the upper bound of V
        :param b: the belief point
        :param delta: the Lipschitz-continuity parameter
        :param S: the set of states
        :param A1: the set of acitons of player 1
        :param A2: the set of actions of player 2
        :param R: the reward tensor
        :param O: the set of observations
        :param Z: the observation tensor
        :param T: the transition tensor
        :param gamma: the discount factor
        :return: Equilibrium strategy profiles in the upper and lower bound stage games
        """

        upper_bound_stage_game = np.zeros((len(A1), len(S) * len(A2)))
        lower_bound_stage_game = np.zeros((len(A1), len(S) * len(A2)))

        p2_policies = []
        policy_combinations = np.array(list(itertools.product(S, A2)))
        for p in policy_combinations:
            policy = np.zeros((len(S), len(A2)))
            policy[0][p[0]] = 1
            policy[1][p[1]] = 1
            p2_policies.append(policy)
        p2_policies = np.array(p2_policies)

        for a1 in A1:
            for i, pi_2 in enumerate(p2_policies):
                immediate_reward = 0
                expected_future_reward_upper_bound = 0
                expected_future_reward_lower_bound = 0
                payoff_upper_bound = 0
                payoff_lower_bound = 0
                for s in S:
                    a2 = int(np.argmax(pi_2[s]))
                    immediate_reward += b[s] * R[a1][a2][s]
                    for o in O:
                        new_belief = self.next_belief(o=o, a1=a1, b=b, S=S, Z=Z, T=T, pi_2=pi_2, A2=A2)
                        upper_bound_new_belief_value = self.upper_bound_value(upper_bound=upper_bound, b=new_belief,
                                                                              delta=delta, S=S)
                        lower_bound_new_belief_value = self.lower_bound_value(lower_bound=lower_bound, b=b, S=S)
                        prob = self.p_o_given_b_a1_a2(o=o, b=b, a1=a1, a2=a2, S=S, Z=Z, T=T)
                        expected_future_reward_upper_bound += prob * upper_bound_new_belief_value
                        expected_future_reward_lower_bound += prob * lower_bound_new_belief_value

                expected_future_reward_upper_bound = gamma * expected_future_reward_upper_bound
                expected_future_reward_lower_bound = gamma * expected_future_reward_lower_bound
                payoff_upper_bound += immediate_reward + expected_future_reward_upper_bound
                payoff_lower_bound += immediate_reward + expected_future_reward_lower_bound
                upper_bound_stage_game[a1][i] = payoff_upper_bound
                lower_bound_stage_game[a1][i] = payoff_upper_bound

        upper_bound_equlibrium_strategies = self.compute_equilibrium_strategies_in_matrix_game(
            A=upper_bound_stage_game, A1=A1, A2=np.array(list(range(len(S) * len(A2)))))
        lower_bound_equlibrium_strategies = self.compute_equilibrium_strategies_in_matrix_game(
            A=upper_bound_stage_game, A1=A1, A2=np.array(list(range(len(S) * len(A2)))))

        pi_1_upper_bound, temp = upper_bound_equlibrium_strategies
        pi_2_upper_bound = self.combine_weights_and_pure_strategies_into_mixed_strategy(weights=temp,
                                                                                        strategies=p2_policies)
        pi_1_lower_bound, temp = lower_bound_equlibrium_strategies
        pi_2_lower_bound = self.combine_weights_and_pure_strategies_into_mixed_strategy(weights=temp,
                                                                                        strategies=p2_policies)

        return pi_1_upper_bound, pi_2_upper_bound, pi_1_lower_bound, pi_2_lower_bound

    def combine_weights_and_pure_strategies_into_mixed_strategy(self, weights: np.ndarray, strategies: np.ndarray):
        """
        Uses a set of mixture weights and strategies to compute a mixed strategy

        :param weights: the mixture weights
        :param strategies: the set of strategies
        :return:  the mixed strategy
        """
        mixed_strategy = np.zeros(strategies[0].shape)
        for i in range(len(weights)):
            mixed_strategy = mixed_strategy + strategies[i] * weights[i]
        return mixed_strategy

    def compute_equilibrium_strategies_in_matrix_game(self, A: np.ndarray, A1: np.ndarray, A2: np.ndarray) \
            -> Tuple[np.ndarray, np.ndarray]:
        """
        Computes equilibrium strategies in a matrix game

        :param A: the matrix game
        :param A1: the action set of player 1 (the maximizer)
        :param A2: the action set of player 2 (the minimizer)
        :return: the equilibrium strategy profile
        """
        v1, maximin_strategy = self.compute_matrix_game_value(A=A, A1=A1, A2=A2, maximizer=True)
        v2, minimax_strategy = self.compute_matrix_game_value(A=A, A1=A1, A2=A2, maximizer=False)
        return maximin_strategy, minimax_strategy

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

    def explore(self, b: np.ndarray, epsilon: float, t: int, lower_bound: List, upper_bound: List,
                gamma: float, S: np.ndarray, O: np.ndarray, Z: np.ndarray, R: np.ndarray,
                T: np.ndarray, A1: np.ndarray, A2: np.ndarray, delta: float, D: float) \
            -> Tuple[List, List]:
        """
        Explores the OS-POSG tree

        :param b: current belief
        :param epsilon: accuracy parameter
        :param t: the current depth of the exploration
        :param lower_bound: the lower bound on the value function
        :param upper_bound: the upper bound on the value function
        :param gamma: discount factor
        :param S: set of states in the OS-POSG
        :param O: set of observations in the OS-POSG
        :param Z: observation tensor in the OS-POSG
        :param R: reward tensor in the OS-POSG
        :param T: transition tensor in the OS-POSG
        :param A1: set of actions of P1 in the OS-POSG
        :param A2: set of actions of P2 in the OS-POSG
        :param delta: the delta parameter in Lipschitz-continuity
        :return: new lower and upper bounds
        """
        pi_1_upper_bound, pi_2_upper_bound, pi_1_lower_bound, pi_2_lower_bound = \
            self.obtain_equilibrium_strategy_profiles_in_stage_game(
                lower_bound=lower_bound, upper_bound=upper_bound, b=b, delta=delta, S=S, A1=A1, A2=A2, gamma=gamma,
                R=R, O=O, Z=Z, T=T)

        a_star, o_star, weighted_excess, excess_val, w, new_belief = self.choose_a_o_for_exploration(
            A1=A1, O=O, t=t + 1, b=b, pi_1_upper_bound=pi_1_upper_bound,
            pi_2_lower_bound=pi_2_lower_bound, lower_bound=lower_bound,
            upper_bound=upper_bound, gamma=gamma, epsilon=epsilon, delta=delta, D=D, S=S, Z=Z, A2=A2, T=T)

        if weighted_excess > 0:
            lower_bound, upper_bound = self.explore(
                b=new_belief, epsilon=epsilon, t=t + 1, lower_bound=lower_bound,
                upper_bound=upper_bound, gamma=gamma, S=S, O=O, Z=Z, R=R, T=T, A1=A1, A2=A2, delta=delta, D=D)

            lower_bound, upper_bound = \
                self.local_updates(
                    lower_bound=lower_bound, upper_bound=upper_bound, b=b, A1=A1, A2=A2, S=S, Z=Z, O=O, R=R,
                    T=T, gamma=gamma, delta=delta)

        return lower_bound, upper_bound

    def choose_a_o_for_exploration(self, A1: np.ndarray, O: np.ndarray, t: int, b: np.ndarray,
                                   pi_1_upper_bound: np.ndarray, pi_2_lower_bound: np.ndarray,
                                   lower_bound: List, upper_bound: List, gamma: float, epsilon: float, delta: float,
                                   D: float, S: np.ndarray, Z: np.ndarray, A2: np.ndarray, T: np.ndarray) \
            -> Tuple[int, int, float, float, float, np.ndarray]:
        """
        Selects the action a* and observation * for exploration according to the heuristic:

        (a1*,o*) = argmax_(a1,o)[P[a1,o]*excess(b_1(a_1,o))]

        (Horák, Bosansky, Kovařík, Kiekintveld, 2020)

        :param A1: the action set of player 1
        :param O: the set of observations in the OS-POSG
        :param t: the time-step t
        :param b: the belief point
        :param pi_1_upper_bound: equilibrium strategy of player 1 in the stage game constructed from the upper bound V*
        :param pi_2_lower_bound: equilibrium strategy of player 2 in the stage game constructed from the lower bound V*
        :param lower_bound: the lower bound
        :param upper_bound: the upper bound
        :param gamma: the discount factor
        :param epsilon: the epsilon accuracy parameter
        :param delta: the Lipschitz-continuity parameter
        :param D: the neighboorhood parameter
        :param S: the set of states
        :param Z: the observation tensor
        :param A2: the set of actions of player 2
        :param T: the transition tensor
        :return: a*,o*,weighted_excess(a*,o*), excess(a*,o*), width(a*,o*), b_prime(a*,o*)
        """
        weighted_excess_values = []
        widths = []
        excess_values = []
        a_o_list = []
        new_beliefs = []
        for a1 in A1:
            for o in O:
                weighted_excess_val, excess_val, w, new_belief = self.weighted_excess_gap(
                    lower_bound=lower_bound, upper_bound=upper_bound, a1=a1, o=o,
                    b=b, t=t, gamma=gamma, pi_1_upper_bound=pi_1_upper_bound, pi_2_lower_bound=pi_2_lower_bound,
                    epsilon=epsilon, delta=delta, D=D, S=S, Z=Z, A1=A1, A2=A2, T=T)
                weighted_excess_values.append(weighted_excess_val)
                widths.append(w)
                excess_values.append(excess_val)
                a_o_list.append([a1, o])
                new_beliefs.append(new_belief)

        max_index = int(np.argmax(weighted_excess_values))
        max_a_o = a_o_list[max_index]
        a_star = max_a_o[0]
        o_star = max_a_o[1]

        return (a_star, o_star, weighted_excess_values[max_index], excess_values[max_index],
                widths[max_index], new_beliefs[max_index])

    def weighted_excess_gap(self, lower_bound: List, upper_bound: List, a1: int, o: int, b: np.ndarray, t: int,
                            gamma: float, pi_1_upper_bound, pi_2_lower_bound,
                            epsilon: float, delta: float, D: float, S: np.ndarray, Z: np.ndarray, A1: np.ndarray,
                            A2: np.ndarray, T: np.ndarray) \
            -> Tuple[float, float, float, np.ndarray]:
        """
        Computes the weighted excess gap

        :param lower_bound: the lower bound
        :param upper_bound: the upper bound
        :param a1: the action of player 1
        :param o: the observation
        :param b: the belief point
        :param t: the time-step
        :param gamma: the discount factor
        :param pi_1_upper_bound a maximin strategy of player 1 in the stage game based on upper bound V*
        :param pi_2_lower_bound: a minimax strategy of player 1 in the stage game based on lower bound V*
        :param epsilon: the epsilon accuracy parameter
        :param delta: the  Lipschitz-continuity parameter
        :param D: the neighborhood parameter
        :param S: the set of states
        :param Z: the observation tensor
        :param A1: the set of actions of player 1
        :param A2: the set of actions of player 2
        :param T: the transition tensor
        :return: (weighted excess, excess, width, b_prime)
        """
        new_belief = self.next_belief(o=o, a1=a1, b=b, S=S, Z=Z, T=T, pi_2=pi_2_lower_bound, A2=A2)
        excess_val, w = self.excess(lower_bound=lower_bound, upper_bound=upper_bound, b=new_belief, S=S,
                                    epsilon=epsilon, gamma=gamma, t=t, delta=delta, D=D)
        weight = self.p_o_given_b_pi_1_pi_2(o=o, b=b, pi_1=pi_1_upper_bound, pi_2=pi_2_lower_bound, S=S, Z=Z, A1=A1,
                                            A2=A2, T=T)
        return weight * excess_val, excess_val, w, new_belief

    def initialize_lower_bound(self, S: np.ndarray, A1: np.ndarray, A2: np.ndarray, gamma: float, b0: np.ndarray,
                               R: np.ndarray, T: np.ndarray) -> List:
        """
        Initializes the lower bound by computing the state-values of the POMDP induced by player 1 playing a uniform
        strategy

        :param S: the set of states
        :param A1: the set of actions of player 1
        :param A2: the set of actions of player 2
        :param gamma: the discount factor
        :param b0: the initial belief point
        :param R: the reward tensor
        :param T: the transition tensor
        :return: the lower bound (singleton set with an alpha vector)
        """
        uniform_strategy = np.zeros(len(A1))
        uniform_strategy.fill(1 / len(A1))
        alpha_vector, _ = self.value_of_p1_strategy_static(S=S, A1=A1, A2=A2, gamma=gamma,
                                                           P1_strategy=uniform_strategy, b0=b0, R=R, T=T)
        lower_bound = []
        lower_bound.append(alpha_vector)
        return lower_bound

    def value_of_p1_strategy_static(self, S: np.ndarray, A1: np.ndarray, A2: np.ndarray, gamma: float,
                                    P1_strategy: np.ndarray, b0: np.ndarray, R: np.ndarray, T: np.ndarray) \
            -> Tuple[np.ndarray, float]:
        """
        Computes the value of PI's strategy P1_strategy, assuming that P1's strategy is static and independent of
        observations/actions/beliefs in the game. For example a uniform strategy.

        The value function is computed by solving the Bellman equation of the induced MDP for P2.

        :param S: the set of states of the OS-POSG
        :param A1: the set of actions of P1 in the OS-POSG
        :param A2: the set of actions of P2 in the OS-POSG
        :param gamma: the discount factor
        :param P1_strategy: the static strategy of P1 to evaluate
        :param b0: the initial belief
        :param R: the reward tensor
        :param T: the transition tensor
        :return: the value vector and the value given the initial belief b0.
        """
        R_mdp = self.mdp_reward_matrix_p2(P1_strategy=P1_strategy, A1=A1, R=R)
        T_mdp = self.mdp_transition_tensor_p2(P1_strategy=P1_strategy, A1=A1, T=T)
        V, _ = self.vi(T=T_mdp, num_states=len(S), num_actions=len(A2), R=R_mdp, theta=0.0001, discount_factor=gamma)
        V = np.array(V)
        b0 = np.array(b0)
        return V, b0.dot(V)

    def mdp_reward_matrix_p2(self, R: np.ndarray, P1_strategy: np.ndarray, A1: List) -> np.ndarray:
        """
        Creates the reward matrix of player 2 induced by a fixed policy of player 1 (a MDP)

        :return: return a |A2|x|S| matrix
        """
        R_mdp = np.zeros(R[0].shape)
        for a1 in A1:
            R_i = R[a1]
            R_i = R_i * -P1_strategy[a1]
            R_mdp = R_mdp + R_i
        return R_mdp

    def mdp_transition_tensor_p2(self, T: np.ndarray, P1_strategy: np.ndarray, A1: List) -> np.ndarray:
        """
        Creates the transition tensor induced by a fixed policy of player 1 (MDP)

        :return: a |A2||S|^2 tensor
        """
        T_mdp = np.zeros(T[0].shape)
        for a1 in A1:
            T_i = T[a1]
            T_i = T_i * P1_strategy[a1]
            T_mdp = T_mdp + T_i

        return T_mdp

    def valcomp(self, pi_1: np.ndarray, alpha_bar: np.ndarray, s: int, A1: np.ndarray, A2: np.ndarray,
                O: np.ndarray, S: np.ndarray, Z: np.ndarray,
                T: np.ndarray, R: np.ndarray, gamma: float, substituted_alpha: bool = False) -> float:
        """
        Computes the value of a compositional strategy of player 1 in a given state s.
        The compositional strategy consists of the one-stage strategy pi_1 (a probability distribution over A1)
        and the expected value when taking action a according to pi_1 and then observing the next observation o and then
        following a behavioral strategy C^(a,o) in (Sigma_1)^(O x A). It is assumed that the value of following strategy
        C^(a,o) is represented by alpha^(a,o) in alpha_bar. Further, to compute the value, since the game is zero-sum,
        we assume that P2 plays a best response against the compositional strategy.

        :param pi_1: the one-stage strategy of P1 to evaluate
        :param alpha_bar: the set of alpha vectors representing the value of the behavioral strategies in
                          subsequent subgames
        :param s: the state to evaluate the value of
        :param A1: the action set of player 1 in the OS-POSG
        :param A2: the action set of player 2 in the OS-POSG
        :param O: the set of observations in the OS-POSG
        :param S: the set of states in the OS-POSG
        :param Z: the observation tensor in the OS-POSG
        :param T: the transition tensor in the OS-POSG
        :param R: the reward tensor in the OS-POSG
        :param substituted_alpha: if True, treat the alpha vectors as alpha^(a,o)(s) = pi_1[a]alpha^(a,o)(s)
        :return: the value of the compositional strategy of P1
        """
        values = []
        for a2 in A2:
            for a1 in A1:
                immediate_reward = R[a1][a2][s]
                expected_future_reward = 0
                for o in O:
                    for s_prime in S:
                        expected_future_reward += (Z[a1][a2][s_prime][o] * T[a1][a2][s][s_prime] *
                                                   alpha_bar[a1][o][s_prime])
                expected_future_reward = gamma * expected_future_reward
                immediate_reward = pi_1[a1] * immediate_reward
                if not substituted_alpha:
                    expected_future_reward = expected_future_reward * pi_1[a1]
                total_value = immediate_reward + expected_future_reward
                values.append(total_value)
        val = min(values)
        return val

    def initialize_upper_bound(self, T: np.ndarray, R: np.ndarray, A1: np.ndarray, A2: np.ndarray,
                               S: np.ndarray, gamma: float) -> List:
        """
        Initializes the upper bound by computing the values of the fully observed version of the OS-POSG using
        Shapley iteration.

        :param T: the transition tensor of the OS-POSG
        :param R: the reward tensor of the OS-POSG
        :param A1: the action set of player 1 in the the OS-POSG
        :param A2: the action set of player 2 in the the OS-POSG
        :param S: the set of states of the OS-POSG
        :param gamma: the discount factor
        :return: the initial upper bound
        """
        V, maximin_strategies, minimax_strategies, auxillary_games = self.si(
            S=S, A1=A1, A2=A2, T=T, R=R, gamma=gamma, max_iterations=1000, delta_threshold=0.001, log=False)
        point_set = []
        for s in S:
            b = self.generate_corner_belief(s=s, S=S)
            point_set.append([b, V[s]])
        return point_set

    def delta_lipschitz_envelope_of_upper_bound_value(self, upper_bound: List, b: np.ndarray, delta: float,
                                                      S: np.ndarray) -> float:
        """
        This function computes the delta-Lipschitz envelop of the upper bound value at a given belief point b.


        :param upper_bound: the upper bound
        :param b: the belief point
        :param delta: the delta parameter for Lipschitz-continuity
        :param S: the set of states
        :return: the belief value
        """
        problem = pulp.LpProblem("Delta-Lipschitz-Envelope", pulp.LpMinimize)

        # ----    Decision variables   ------

        # Convex hull coefficients
        lamb = []
        for i in range(len(upper_bound)):
            lamb_i = pulp.LpVariable("lambda_" + str(i), lowBound=0, upBound=1, cat=pulp.LpContinuous)
            lamb.append(lamb_i)

        # b_prime weights
        b_prime = []
        for i in range(len(b)):
            b_prime_i = pulp.LpVariable("b_prime_" + str(i), lowBound=0, upBound=1, cat=pulp.LpContinuous)
            b_prime.append(b_prime_i)

        # Delta variables
        state_deltas = []
        for i in range(len(b)):
            state_deltas_i = pulp.LpVariable("state_Delta_" + str(i), lowBound=0, upBound=1, cat=pulp.LpContinuous)
            state_deltas.append(state_deltas_i)

        # --- The objective ---

        # The objective function
        objective = 0
        for i, point in enumerate(upper_bound):
            objective += lamb[i] * point[1]
        for s in range(len(b)):
            objective += delta * state_deltas[s]
        problem += objective, "Lipschitz-Delta envelop"

        # --- The constraints ---

        # Belief probability constraint
        for j in range(len(S)):
            belief_sum = 0
            for i, point in enumerate(upper_bound):
                belief_sum += lamb[i] * point[0][j]
            problem += belief_sum == b_prime[j], "BeliefVectorConstraint_" + str(j)

        # Delta s constraints
        for s in range(len(b)):
            problem += state_deltas[s] >= (b_prime[s] - b[s]), "Delta_s_constraint_1_" + str(s)
            problem += state_deltas[s] >= (b[s] - b_prime[s]), "Delta_s_constraint_2_" + str(s)

        # Convex Hull constraint
        lambda_weights_sum = 0
        for i in range(len(lamb)):
            lambda_weights_sum += lamb[i]
        problem += lambda_weights_sum == 1, "ConvexHullWeightsSumConstraint"

        # Solve
        problem.solve(pulp.PULP_CBC_CMD(msg=0))

        # Extract solution
        projected_lamb_coefficients = []
        belief_value = 0
        for i in range(len(upper_bound)):
            projected_lamb_coefficients.append(lamb[i].varValue)
            belief_value += projected_lamb_coefficients[i] * upper_bound[i][1]

        state_deltas_coefficients = []
        state_deltas_sum = 0
        for s in range(len(b)):
            state_deltas_coefficients.append(state_deltas[s].varValue)
            state_deltas_sum += state_deltas_coefficients[s]
        state_deltas_sum = delta * state_deltas_sum

        belief_value += state_deltas_sum

        return belief_value

    def maxcomp_shapley_bellman_operator(self, Gamma: np.ndarray, A1: np.ndarray, S: np.ndarray, O: np.ndarray,
                                         A2: np.ndarray, gamma: float, b: np.ndarray, R, T, Z) \
            -> Tuple[np.ndarray, np.ndarray]:
        """
        A dear child with many names: Maxcomp/Shapley/Bellman operator that computes [HV](b) where V is represented by
        the pointwise maximum over the convex hull of a set of alpha vectors Gamma.
        By representing the set of vectors as the convex hull, the solution to the operator can be found by an LP.
        I.e the whole purpose of using the convex hull of Gamma is to be able to compute the operator through LP.

        The operator is represented as the solution to a linear program given in
        (Karel Horák PhD thesis, 2019).

        That is, the operator performs a backup to update the lower bound in HSVI or to perform iterations in exact
        value iteration for OS-POSGs.

        :param Gamma: the set of alpha vectors representing the value function
        :param A1: the action space of player 1
        :param S: the set of states in the OS-POSG
        :param O: the set of observations in the OS-POSG
        :param A2: the action space of player 2 in the OS-POSG
        :param gamma: the discount factor
        :param b: the belief point
        :param R: the reward tensor of the OS-POSG
        :param T: the transition tensor of the OS-POSG
        :param Z: the observation tensor of the OS-POSG
        :return: the "optimal" stage strategy of Player 1 and the set of alpha-vectors representing the  values of the
                 behavioral strategy following a1,o for any combination of a1,o.
        """
        problem = pulp.LpProblem("ShapleyOperator", pulp.LpMaximize)

        # ----    Decision variables   ------

        # Strategy weights of the stage strategy pi_1 of player 1
        pi_1 = []
        for a1 in A1:
            pi_1_1 = pulp.LpVariable("pi_1_" + str(a1), lowBound=0, upBound=1, cat=pulp.LpContinuous)
            pi_1.append(pi_1_1)

        # State-value function
        V = []
        for s in S:
            V_1 = pulp.LpVariable("V_" + str(s), lowBound=None, upBound=None, cat=pulp.LpContinuous)
            V.append(V_1)

        # Convex hull coefficients of Conv(Gamma_k)
        lamb = []
        for a1 in A1:
            a_o_lambs = []
            for o in O:
                o_lambs = []
                for i in range(len(Gamma)):
                    lamb_i = pulp.LpVariable("lambda_" + str(i) + "_" + str(o) + "_" + str(a1), lowBound=0,
                                             upBound=1, cat=pulp.LpContinuous)
                    o_lambs.append(lamb_i)
                a_o_lambs.append(o_lambs)
            lamb.append(a_o_lambs)

        # Alpha bar: set of alpha^(a,o) vectors representing the value of the behavioral strategy C^(a,o) in the subgame
        # after taking action a and observing o in belief point b
        alpha_bar = []
        for a1 in A1:
            a_o_alphas = []
            for o in O:
                o_alphas = []
                for s in S:
                    alpha_bar_i = pulp.LpVariable("alpha_bar_" + str(s) + "_" + str(o) + "_" + str(a1),
                                                  lowBound=None, upBound=None, cat=pulp.LpContinuous)
                    o_alphas.append(alpha_bar_i)
                a_o_alphas.append(o_alphas)
            alpha_bar.append(a_o_alphas)

        # The objective function
        objective = 0
        for s in S:
            objective = b[s] * V[s]
        problem += objective, "Expected state-value"

        # --- The constraints ---

        # State-Value function constraints
        for s in S:
            for a2 in A2:
                immediate_reward = 0
                for a1 in A1:
                    immediate_reward += pi_1[a1] * R[a1][a2][s]

                expected_future_reward = 0
                for a1 in A1:
                    for o in O:
                        for s_prime in S:
                            expected_future_reward += (T[a1][a2][s][s_prime] * Z[a1][a2][s_prime][o] *
                                                       alpha_bar[a1][o][s_prime])

                expected_future_reward = gamma * expected_future_reward
                sum = immediate_reward + expected_future_reward
                problem += sum >= V[s], "SecurityValueConstraint_" + str(s) + "_a2" + str(a2)

        # Alpha-bar constraints
        for a1 in A1:
            for o in O:
                for s_prime in S:
                    weighted_alpha_sum = 0
                    for i in range(len(Gamma)):
                        weighted_alpha_sum += lamb[a1][o][i] * Gamma[i][s_prime]
                    problem += weighted_alpha_sum == (alpha_bar[a1][o][s_prime], "AlphaBarConstraint_" +
                                                      str(s_prime) + "_" + str(a1) + "_" + str(o))

        # Lambda constraints
        for a1 in A1:
            for o in O:
                lambda_sum = 0
                for i in range(len(Gamma)):
                    lambda_sum += lamb[a1][o][i]

                problem += lambda_sum == pi_1[a1], "Lambconstraint_" + str(a1) + "_" + str(o)

        # Strategy constraints
        strategy_weights_sum = 0
        for i in range(len(pi_1)):
            strategy_weights_sum += pi_1[i]
        problem += strategy_weights_sum == 1, "probabilities sum"

        problem.solve(pulp.PULP_CBC_CMD(msg=0))

        value = []
        for s in S:
            value.append(V[s].varValue)

        pi_1_val = []
        for a1 in A1:
            pi_1_val.append(pi_1[a1].varValue)

        lamba_1_val = []
        for a1 in A1:
            lamba_1_val_a1 = []
            for o in O:
                lamba_1_val_o = []
                for k in range(len(Gamma)):
                    lamba_1_val_o.append(lamb[a1][o][k].varValue)
                lamba_1_val_a1.append(lamba_1_val_o)
            lamba_1_val.append(lamba_1_val_a1)

        alpha_bar_val = []
        for a1 in A1:
            alpha_1_val_a1 = []
            for o in O:
                alpha_1_val_o = []
                for s in S:
                    alpha_1_val_o.append(alpha_bar[a1][o][s].varValue)
                alpha_1_val_a1.append(alpha_1_val_o)
            alpha_bar_val.append(alpha_1_val_a1)

        return np.array(pi_1_val), np.array(alpha_bar_val)

    def generate_corner_belief(self, s: int, S: np.ndarray):
        """
        Generate the corner of the simplex that corresponds to being in some state with probability 1

        :param s: the state
        :param S: the set of States
        :return: the corner belief corresponding to state s
        """
        b = np.zeros(len(S))
        b[s] = 1
        return b

    def local_updates(self, lower_bound: List, upper_bound: List, b: np.ndarray, A1: np.ndarray,
                      A2: np.ndarray, S: np.ndarray,
                      O: np.ndarray, R: np.ndarray, T: np.ndarray, gamma: float, Z: np.ndarray, delta: float) \
            -> Tuple[List, List]:
        """
        Perform local updates to the upper and  lower bounds for the given belief in the heuristic-search-exploration

        :param lower_bound: the lower bound on V
        :param upper_bound: the upper bound on V
        :param b: the current belief point
        :param A1: the set of actions of player 1 in the OS-POSG
        :param A2: the set of actions of player 2 in the OS-POSG
        :param S: the set of states in the OS-POSG
        :param O: the set of observations in the OS-POSG
        :param R: the reward tensor in the OS-POSG
        :param T: the transition tensor in the OS-POSG
        :param gamma: the discount factor
        :param Z: the set of observations in the OS-POSG
        :param delta: the Lipschitz-Delta parameter
        :return: The updated lower and upper bounds
        """
        new_upper_bound = self.local_upper_bound_update(upper_bound=upper_bound, b=b, A1=A1, A2=A2,
                                                        S=S, O=O, R=R, T=T, gamma=gamma, Z=Z, delta=delta)
        new_lower_bound = self.local_lower_bound_update(lower_bound=lower_bound, b=b, Z=Z, A1=A1, A2=A2, O=O, S=S,
                                                        T=T, R=R, gamma=gamma)
        return new_lower_bound, new_upper_bound

    def local_upper_bound_update(self, upper_bound: List, b: np.ndarray, A1: np.ndarray, A2: np.ndarray,
                                 S: np.ndarray, O: np.ndarray, R: np.ndarray, T: np.ndarray,
                                 gamma: float, Z: np.ndarray, delta: float) -> np.ndarray:
        """
        Performs a local update to the upper bound during the heuristic-search exploration

        :param upper_bound: the upper bound to update
        :param b: the current belief point
        :param A1: the set of actions of player 1 in the OS-POSG
        :param S: the set of states in the OS-POSG
        :param O: the set of observations in the OS-POSG
        :param R: the reward tensor in the OS-POSG
        :param T: the transition tensor in the OS-POSG
        :param gamma: the discount factor in the OS-POSG
        :param Z: the set of observations in the OS-POSG
        :param delta: the Lipschitz-Delta parameter
        :return: the updated upper bound
        """
        new_val = self.upper_bound_backup(upper_bound=upper_bound, b=b, A1=A1, A2=A2, S=S,
                                          Z=Z, O=O, R=R, T=T, gamma=gamma, delta=delta)
        upper_bound.append([b, new_val])
        return upper_bound

    def local_lower_bound_update(self, lower_bound: List, b: np.ndarray, A1: np.ndarray,
                                 A2: np.ndarray, O: np.ndarray, Z: np.ndarray, S: np.ndarray,
                                 T: np.ndarray, R: np.ndarray, gamma: float) -> np.ndarray:
        """
        Performs a local update to the lower bound given a belief point in the heuristic search.

        The lower bound update preserves the lower bound property and the Delta-Lipschitz continuity property.

        :param lower_bound: the current lower bound
        :param b: the current belief point
        :param A1: the set of actions of player 1 in the OS-POSG
        :param A2: the set of actions of player 2 in the OS-POSG
        :param O: the set of observations in the OS-POSG
        :param Z: the observation tensor in the OS-POSG
        :param S: the set of states in the OS-POSG
        :param T: the transition tensor in the OS-POSG
        :param R: the reward tensor in the OS-POSG
        :param gamma: the discount factor in the OS-POSG
        :return: the updated lower bound
        """
        alpha_vec = self.lower_bound_backup(lower_bound=lower_bound, b=b, A1=A1, Z=Z, O=O, S=S, T=T, R=R,
                                            gamma=gamma, A2=A2)
        if not pruning.check_duplicate(lower_bound, alpha_vec):
            lower_bound.append(alpha_vec)
        return lower_bound

    def lower_bound_backup(self, lower_bound: List, b: np.ndarray, A1: np.ndarray, O: np.ndarray,
                           Z: np.ndarray, S: np.ndarray, T: np.ndarray, R: np.ndarray,
                           gamma: float, A2: np.ndarray) -> np.ndarray:
        """
        Generates a new alpha-vector for the lower bound

        :param lower_bound: the current lower bound
        :param b: the current belief point
        :param A1: the set of actions of player 1 in the OS-POSG
        :param A2: the set of actions of player 2 in the OS-POSG
        :param O: the set of observations in the OS-POSG
        :param Z: the observation tensor in the OS-POSG
        :param S: the set of states in the OS-POSG
        :param T: the transition tensor in the OS-POSG
        :param R: the reward tensor in the OS-POSG
        :param gamma: the discount factor
        :return: the new alpha vector
        """

        # Shapley operator to obtain optimal value composition
        pi_1_LB, alpha_bar_LB = self.maxcomp_shapley_bellman_operator(Gamma=lower_bound, A1=A1, S=S, O=O, A2=A2,
                                                                      gamma=gamma, b=b, R=R, T=T, Z=Z)
        alpha_vec = []
        for s in S:
            s_val = self.valcomp(pi_1=pi_1_LB, alpha_bar=alpha_bar_LB, s=s, A1=A1, A2=A2, O=O, S=S, Z=Z, T=T, R=R,
                                 gamma=gamma, substituted_alpha=True)
            alpha_vec.append(s_val)

        return alpha_vec

    def upper_bound_backup(self, upper_bound: List, b: np.ndarray, A1: np.ndarray, A2: np.ndarray, S: np.ndarray,
                           O: np.ndarray, Z: np.ndarray, R: np.ndarray, T: np.ndarray, gamma: float, delta: float) \
            -> Tuple[np.ndarray, float]:
        """
        Adds a point to the upper bound

        :param upper_bound: the current upper bound
        :param b: the current belief point
        :param A1: the set of actions of player 1 in the OS-POSG
        :param A2: the set of actions of player 1 in the OS-POSG
        :param S: the set of states in the OS-POSG
        :param O: the set of observations in the OS-POSG
        :param Z: the observation tensor in the OS-POSG
        :param R: the reward tensor in the OS-POSG
        :param T: the transition tensor in the OS-POSG
        :param gamma: the discount factor in the OS-POSG
        :param lp_nf: a boolean flag whether to use LP to compute the upper bound belief
        :param delta: the Lipschitz-delta parameter
        :return: the new point
        """
        problem = pulp.LpProblem("Local Upper Bound Backup", pulp.LpMinimize)

        # ----    Decision variables   -----

        # Policy weights of player 2
        pi_2 = []
        for s in S:
            pi_2_s = []
            for a2 in A2:
                pi_2_i = pulp.LpVariable("pi_2_" + str(s) + "_" + str(a2), lowBound=0, upBound=1, cat=pulp.LpContinuous)
                pi_2_s.append(pi_2_i)
            pi_2.append(pi_2_s)

        # V
        V = pulp.LpVariable("V", lowBound=None, upBound=None, cat=pulp.LpContinuous)

        # tau hat
        tau_hat = []
        for a1 in A1:
            a_o_tau_hats = []
            for o in O:
                o_tau_hats = []
                for s_prime in S:
                    tau_hat_i = pulp.LpVariable("tau_hat_" + str(a1) + "_" + str(o) + "_" + str(s_prime),
                                                lowBound=0, upBound=1, cat=pulp.LpContinuous)
                    o_tau_hats.append(tau_hat_i)
                a_o_tau_hats.append(o_tau_hats)
            tau_hat.append(a_o_tau_hats)

        # b_prime weights
        b_prime = []
        for a1 in A1:
            o_a1_b_primes = []
            for o in O:
                o_b_primes = []
                for s_prime in S:
                    b_prime_i = pulp.LpVariable("b_prime_" + str(s_prime) + "_" + str(o) + "_" + str(a1),
                                                lowBound=0, upBound=1, cat=pulp.LpContinuous)
                    o_b_primes.append(b_prime_i)
                o_a1_b_primes.append(o_b_primes)
            b_prime.append(o_a1_b_primes)

        # V-hat
        V_hat = []
        for a1 in A1:
            a_o_V_hats = []
            for o in O:
                V_hat_a_o_i = pulp.LpVariable("V_hat_" + str(a1) + "_" + str(o),
                                              lowBound=0, upBound=1, cat=pulp.LpContinuous)
                a_o_V_hats.append(V_hat_a_o_i)
            V_hat.append(a_o_V_hats)

        # Convex hull coefficients of the upper_bound_point_set
        lamb = []
        for a1 in A1:
            a_o_lambs = []
            for o in O:
                o_lambs = []
                for i in range(len(upper_bound)):
                    lamb_i = pulp.LpVariable("lambda_" + str(i) + "_" + str(o) + "_" + str(a1), lowBound=0,
                                             upBound=1, cat=pulp.LpContinuous)
                    o_lambs.append(lamb_i)
                a_o_lambs.append(o_lambs)
            lamb.append(a_o_lambs)

        # Delta variables
        state_action_observation_deltas = []
        for a1 in A1:
            a_o_state_deltas = []
            for o in O:
                o_state_deltas = []
                for s_prime in S:
                    state_deltas_i = pulp.LpVariable("state_Delta_" + str(a1) + "_" + str(o) + "_" + str(s_prime),
                                                     lowBound=0, upBound=1, cat=pulp.LpContinuous)
                    o_state_deltas.append(state_deltas_i)
                a_o_state_deltas.append(o_state_deltas)
            state_action_observation_deltas.append(a_o_state_deltas)

        # --- The objective ---

        # The objective function
        problem += V, "Upper bound local update objective"

        # --- The constraints ---

        # Value constraints
        for a1 in A1:
            sum = 0
            weighted_immediate_rew_sum = 0
            for a2 in A2:
                for s in S:
                    weighted_immediate_rew_sum += b[s] * pi_2[s][a2] * R[a1][a2][s]
            future_val_sum = 0
            for o in O:
                future_val_sum += V_hat[a1][o]
            future_val_sum = gamma * future_val_sum
            sum += future_val_sum
            problem += V >= sum, "V_constraint_" + str(a1)

        # Tau-hat constraints
        for a1 in A1:
            for o in O:
                for s_prime in S:
                    sum = 0
                    for s in S:
                        for a2 in A2:
                            sum += T[a1][a2][s][s_prime] * pi_2[s][a2]
                    problem += sum == tau_hat[a1][o][s_prime], ("belief_constraint_" + str(a1) + "_" + str(o)
                                                                + "_" + str(s_prime))

        # Pi_2 constraints
        for s in S:
            sum = 0
            for a2 in A2:
                sum += pi_2[s][a2]

            problem += sum == b[s], "pi_2_constraint_" + str(s)

        # V hat constraints
        for a1 in A1:
            for o in O:
                sum = 0
                for i, point in enumerate(upper_bound):
                    sum += lamb[a1][o][i] * point[1]
                deltas_sum = 0
                for s_prime in S:
                    deltas_sum += state_action_observation_deltas[a1][o][s_prime]
                deltas_sum = delta * deltas_sum
                sum += deltas_sum
                problem += sum == V_hat[a1][o], "V_hat_constraint_" + str(a1) + "_" + str(o)

        # Belief_prime constraints
        for a1 in A1:
            for o in O:
                for s_prime in S:
                    sum = 0
                    for i, point in enumerate(upper_bound):
                        sum += lamb[a1][o][i] * point[0][s_prime]
                    problem += sum == b_prime[a1][o][s_prime], ("b_prime constraint_" + str(a1) + "_" + str(o)
                                                                + "_" + str(s_prime))

        # Deltas constraints
        for a1 in A1:
            for o in O:
                for s_prime in S:
                    problem += state_action_observation_deltas[a1][o][s_prime] >= (
                        (b_prime[a1][o][s_prime] - tau_hat[a1][o][s_prime]), ("Delta_contraints_1_" + str(a1) + "_"
                                                                              + str(o) + "_" + str(s_prime)))
                    problem += state_action_observation_deltas[a1][o][s_prime] >= (
                        (tau_hat[a1][o][s_prime] - b_prime[a1][o][s_prime]), ("Delta_contraints_2_" + str(a1)
                                                                              + "_" + str(o) + "_" + str(s_prime)))

        # Lambda constraints
        for a1 in A1:
            for o in O:
                lambdas_sum = 0
                for i, point in enumerate(upper_bound):
                    lambdas_sum += lamb[a1][o][i]

                tau_hat_sum = 0
                for s_prime in S:
                    tau_hat_sum += tau_hat[a1][o][s_prime]

                problem += lambdas_sum == tau_hat_sum, "lambda_constraint_" + str(a1) + "_" + str(o)

        # Solve
        problem.solve(pulp.PULP_CBC_CMD(msg=0))

        # Obtain solution
        belief_value_var = V.varValue
        return belief_value_var

    def upper_bound_value(self, upper_bound: List, b: np.ndarray, delta: float, S: np.ndarray) -> float:
        """
        Computes the upper bound value of a given belief point

        :param upper_bound: the upper bound
        :param b: the belief point
        :param delta: the delta-parameter for Lipschitz-continuity
        :param lp_nf: boolean flag that decides whether to use LP to compute the upper bound value or not
        :param S: the set of states
        :return: the upper bound value
        """
        return self.delta_lipschitz_envelope_of_upper_bound_value(upper_bound=upper_bound, b=b, delta=delta, S=S)

    def lower_bound_value(self, lower_bound: List, b: np.ndarray, S: np.ndarray) -> float:
        """
        Computes the lower bound value of a given belief point

        :param lower_bound: the lower bound
        :param b: the belief point
        :param S: the set of states
        :return: the lower bound value
        """
        alpha_vals = []
        for alpha_vec in lower_bound:
            sum = 0
            for s in S:
                sum += b[s] * alpha_vec[s]
            alpha_vals.append(sum)
        return max(alpha_vals)

    def next_belief(self, o: int, a1: int, b: np.ndarray, S: np.ndarray, Z: np.ndarray, T: np.ndarray, pi_2: np.ndarray,
                    A2: np.ndarray) -> np.ndarray:
        """
        Computes the next belief using a Bayesian filter

        :param o: the latest observation
        :param a1: the latest action of player 1
        :param b: the current belief
        :param S: the set of states
        :param Z: the observation tensor
        :param T: the transition tensor
        :param pi_2: the policy of player 2
        :param A2: the set of actions of player 2
        :return: the new belief
        """
        b_prime = np.zeros(len(S))
        for s_prime in S:
            b_prime[s_prime] = self.bayes_filter(s_prime=s_prime, o=o, a1=a1, b=b, S=S, Z=Z, T=T, pi_2=pi_2, A2=A2)

        assert round(sum(b_prime), 5) == 1
        return b_prime

    def bayes_filter(self, s_prime: int, o: int, a1: int, b: np.ndarray, S: np.ndarray, Z: np.ndarray,
                     T: np.ndarray, pi_2: np.ndarray, A2: np.ndarray) -> float:
        """
        A Bayesian filter to compute the belief of player 1
        of being in s_prime when observing o after taking action a in belief b given that the opponent follows
        strategy pi_2

        :param s_prime: the state to compute the belief of
        :param o: the observation
        :param a1: the action of player 1
        :param b: the current belief point
        :param S: the set of states
        :param Z: the observation tensor
        :param T: the transition tensor
        :param pi_2: the policy of player 2
        :param A2: the action set of player 2
        :return: b_prime(s_prime)
        """
        norm = 0
        for s in S:
            for a2 in A2:
                for s_prime_1 in S:
                    prob_1 = Z[a1][a2][s_prime_1][o]
                    norm += b[s] * prob_1 * T[a1][a2][s][s_prime_1] * pi_2[s][a2]
        temp = 0

        for s in S:
            for a2 in A2:
                temp += Z[a1][a2][s_prime][o] * T[a1][a2][s][s_prime] * b[s] * pi_2[s][a2]

        if norm != 0:
            b_prime_s_prime = temp / norm
        else:
            b_prime_s_prime = temp

        assert b_prime_s_prime <= 1
        return b_prime_s_prime

    def p_o_given_b_a1_a2(self, o: int, b: np.ndarray, a1: int, a2: int, S: np.ndarray, Z: np.ndarray, T: np.ndarray) \
            -> float:
        """
        Computes P[o|a,b]

        :param o: the observation
        :param b: the belief point
        :param a1: the action of player 1
        :param a2: the action of player 2
        :param S: the set of states
        :param Z: the observation tensor
        :param T: the transition tensor
        :return: the probability of observing o when taking action a in belief point b
        """
        prob = 0
        for s in S:
            for s_prime in S:
                prob += b[s] * T[a1][a2][s][s_prime] * Z[a1][a2][s_prime][o]
        assert prob <= 1
        return prob

    def p_o_given_b_pi_1_pi_2(self, o: int, b: np.ndarray, pi_1: np.ndarray, pi_2: np.ndarray, S: np.ndarray,
                              Z: np.ndarray, A1: np.ndarray, A2: np.ndarray, T: np.ndarray) -> float:
        """
        Computes P[o|a,b]

        :param o: the observation
        :param b: the belief point
        :param pi_1: the policy of player 1
        :param pi_2: the policy of player 2
        :param S: the set of states
        :param Z: the observation tensor
        :param T: the transition tensor
        :return: the probability of observing o when taking action a in belief point b
        """
        prob = 0
        for a1 in A1:
            for a2 in A2:
                for s in S:
                    for s_prime in S:
                        prob += b[s] * pi_1[a1] * pi_2[s][a2] * T[a1][a2][s][s_prime] * Z[a1][a2][s_prime][o]
        assert prob < 1
        return prob

    def excess(self, lower_bound: List, upper_bound: List, b: np.ndarray, S: np.ndarray,
               epsilon: float, gamma: float, t: int, delta: float, D: float) -> Tuple[float, float]:
        """
        Computes the excess gap and width (Horak, Bosansky, Pechoucek, 2017)

        :param lower_bound: the lower bound
        :param upper_bound: the upper bound
        :param D: the neighborhood parameter
        :param delta: the Lipschitz-continuity parameter
        :param b: the current belief point
        :param S: the set of states
        :param epsilon: the epsilon accuracy parameter
        :param gamma: the discount factor
        :param t: the current exploration depth
        :return: the excess gap and gap width
        """
        w = self.width(lower_bound=lower_bound, upper_bound=upper_bound, b=b, S=S, delta=delta)
        return (w - self.rho(t=t, epsilon=epsilon, gamma=gamma, delta=delta, D=D)), w

    def rho(self, t: int, epsilon: float, gamma: float, delta: float, D: float) -> float:
        """
        During the exploration, the HSVI algorithms tries to keep the gap between V_UB and V_LB to be at most
        rho(t), which is monotonically increasing and unbounded

        rho(0) = epsilon
        rho(t+1) = (rho(t) -2*delta*D)/gamma

        :param t: the time-step of the exploration
        :param epsilon: the epsilon parameter
        :param gamma: the discount factor
        :param delta: the Lipshitz-continuity parameter
        :param D: the neighborhood parameter
        :return: rho(t)
        """
        if t == 0:
            return epsilon
        else:
            return (self.rho(t=t - 1, epsilon=epsilon, gamma=gamma, delta=delta, D=D) - 2 * delta * D) / gamma

    def width(self, lower_bound: List, upper_bound: List, b: np.ndarray, S: np.ndarray, delta: float) -> float:
        """
        Computes the bounds width (Trey Smith and Reid Simmons, 2004)

        :param lower_bound: the current lower bound
        :param upper_bound: the current upper bound
        :param b: the current belief point
        :param S: the set of states
        :param delta: the delta parameter for Lipschitz-continuity
        :return: the width of the bounds
        """
        ub = self.upper_bound_value(upper_bound=upper_bound, b=b, delta=delta, S=S)
        lb = self.lower_bound_value(lower_bound=lower_bound, b=b, S=S)
        return ub - lb

    def prune_upper_bound(self, upper_bound: List, delta: float, S: np.ndarray) -> List:
        """
        Prunes the points in the upper bound

        :param upper_bound: the current upper bound
        :param delta: the delta parameter for lipschitz-continuity
        :param S: the set of states
        :return: the pruned upper bound
        """
        pruned_upper_bound_point_set = []

        for point in upper_bound:
            true_val = self.upper_bound_value(upper_bound=upper_bound, b=point[0], delta=delta, S=S)
            if not (point[1] > true_val):
                pruned_upper_bound_point_set.append(point)

        return pruned_upper_bound_point_set

    def auxillary_game(self, V: np.ndarray, gamma: float, S: np.ndarray, s: int, A1: np.ndarray, A2: np.ndarray,
                       R: np.ndarray, T: np.ndarray) -> np.ndarray:
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
                expected_future_reward = 0
                for s_prime in S:
                    expected_future_reward += T[a1][a2][s][s_prime] * V[s_prime]
                expected_future_reward = expected_future_reward * gamma
                A[a1][a2] = immediate_reward + expected_future_reward
        return A

    def si(self, S: np.ndarray, A1: np.ndarray, A2: np.ndarray, R: np.ndarray, T: np.ndarray, gamma: float = 1,
           max_iterations: int = 500, delta_threshold: float = 0.1, log: bool = False) \
            -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
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
        :param log: a boolean flag whether to use verbose logging or not
        :return: the value function, the set of maximin strategies for all stage games,
        the set of minimax strategies for all stage games, and the stage games themselves
        """
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

        return V, np.array(maximin_strategies), np.array(minimax_strategies), np.array(auxillary_games)

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

    def vi(self, T: np.ndarray, num_states: int, num_actions: int, R: np.ndarray, theta: float = 0.0001,
           discount_factor: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
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
        :return: (greedy policy, value function)
        """
        V = np.zeros(num_states)

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

        return V, policy
