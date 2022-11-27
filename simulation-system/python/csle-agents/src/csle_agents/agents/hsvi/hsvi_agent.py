import math
from typing import List, Optional, Tuple
import time
import os
import numpy as np
import gym
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
from csle_common.dao.training.alpha_vectors_policy import AlphaVectorsPolicy
from csle_agents.agents.base.base_agent import BaseAgent
import csle_agents.constants.constants as agents_constants
import csle_agents.common.pruning as pruning


class HSVIAgent(BaseAgent):
    """
    Heuristic-Search Value Iteration for POMDPs (Trey Smith and Reid Simmons, 2004) Agent
    """

    def __init__(self, simulation_env_config: SimulationEnvConfig,
                 experiment_config: ExperimentConfig,
                 training_job: Optional[TrainingJobConfig] = None, save_to_metastore: bool = True):
        """
        Initializes the HSVI agent

        :param simulation_env_config: configuration of the simulation environment
        :param experiment_config: the experiment configuration
        :param training_job: an existing training job to use (optional)
        :param save_to_metastore: boolean flag whether to save the execution to the metastore
        """
        super().__init__(simulation_env_config=simulation_env_config, emulation_env_config=None,
                         experiment_config=experiment_config)
        assert experiment_config.agent_type == AgentType.HSVI
        self.training_job = training_job
        self.save_to_metastore = save_to_metastore
        self.env = gym.make(self.simulation_env_config.gym_env_name,
                            config=self.simulation_env_config.simulation_env_input_config)

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
        exp_result.plot_metrics.append(agents_constants.HSVI.WIDTHS)
        exp_result.plot_metrics.append(agents_constants.HSVI.LB_SIZES)
        exp_result.plot_metrics.append(agents_constants.HSVI.UB_SIZES)
        exp_result.plot_metrics.append(agents_constants.HSVI.INITIAL_BELIEF_VALUES)

        descr = f"Computation of V* with the HSVI algorithm using " \
                f"simulation:{self.simulation_env_config.name}"

        for seed in self.experiment_config.random_seeds:
            exp_result.all_metrics[seed] = {}
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.HSVI.WIDTH] = []
            exp_result.all_metrics[seed][agents_constants.HSVI.UB_SIZE] = []
            exp_result.all_metrics[seed][agents_constants.HSVI.LB_SIZE] = []

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
            exp_result = self.hsvi_algorithm(exp_result=exp_result, seed=seed)

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
                agents_constants.HSVI.TRANSITION_TENSOR,
                agents_constants.HSVI.REWARD_TENSOR, agents_constants.HSVI.OBSERVATION_TENSOR,
                agents_constants.HSVI.OBSERVATION_SPACE, agents_constants.HSVI.STATE_SPACE,
                agents_constants.HSVI.ACTION_SPACE, agents_constants.HSVI.EPSILON,
                agents_constants.HSVI.INITIAL_BELIEF, agents_constants.HSVI.USE_LP,
                agents_constants.HSVI.PRUNE_FREQUENCY, agents_constants.HSVI.SIMULATION_FREQUENCY,
                agents_constants.HSVI.SIMULATE_HORIZON, agents_constants.HSVI.NUMBER_OF_SIMULATIONS]

    def hsvi_algorithm(self, exp_result: ExperimentResult, seed: int) -> ExperimentResult:
        """
        Runs

        :param exp_result: the experiment result object
        :param seed: the random seed
        :return: the updated experiment result
        """
        discount_factor = self.experiment_config.hparams[agents_constants.COMMON.GAMMA].value
        T = self.experiment_config.hparams[agents_constants.HSVI.TRANSITION_TENSOR].value
        R = self.experiment_config.hparams[agents_constants.HSVI.REWARD_TENSOR].value
        Z = self.experiment_config.hparams[agents_constants.HSVI.OBSERVATION_TENSOR].value
        O = self.experiment_config.hparams[agents_constants.HSVI.OBSERVATION_SPACE].value
        S = self.experiment_config.hparams[agents_constants.HSVI.STATE_SPACE].value
        A = self.experiment_config.hparams[agents_constants.HSVI.ACTION_SPACE].value
        epsilon = self.experiment_config.hparams[agents_constants.HSVI.EPSILON].value
        b0 = self.experiment_config.hparams[agents_constants.HSVI.INITIAL_BELIEF].value
        lp = self.experiment_config.hparams[agents_constants.HSVI.USE_LP].value
        prune_frequency = self.experiment_config.hparams[agents_constants.HSVI.PRUNE_FREQUENCY].value
        simulation_frequency = self.experiment_config.hparams[agents_constants.HSVI.SIMULATION_FREQUENCY].value
        simulate_horizon = self.experiment_config.hparams[agents_constants.HSVI.SIMULATE_HORIZON].value
        number_of_simulations = self.experiment_config.hparams[agents_constants.HSVI.NUMBER_OF_SIMULATIONS].value
        Logger.__call__().get_logger().info(f"Starting the HSVI algorithm, epsilon:{epsilon}, "
                                            f"discount_factor: {discount_factor}, lp_nf: {lp}, "
                                            f"prune_frequency: {prune_frequency}, "
                                            f"simulation_frequency: {simulation_frequency}, "
                                            f"number_of_simulations: {number_of_simulations}, "
                                            f"simulate_horizon: {simulate_horizon}, b0: {b0}")
        alpha_vectors, avg_returns, running_avg_returns, widths, ub_sizes, lb_sizes, initial_belief_values = self.hsvi(
            T=np.array(T), R=np.array(R), O=np.array(O), S=np.array(S), Z=np.array(Z), A=np.array(A),
            gamma=discount_factor, b0=b0, epsilon=epsilon, lp=lp, prune_frequency=prune_frequency,
            simulation_frequency=simulation_frequency, simulate_horizon=simulate_horizon,
            number_of_simulations=number_of_simulations)
        exp_result.all_metrics[seed][agents_constants.HSVI.WIDTHS] = widths
        exp_result.all_metrics[seed][agents_constants.HSVI.LB_SIZES] = lb_sizes
        exp_result.all_metrics[seed][agents_constants.HSVI.UB_SIZES] = ub_sizes
        exp_result.all_metrics[seed][agents_constants.HSVI.INITIAL_BELIEF_VALUES] = initial_belief_values
        exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN] = avg_returns
        exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN] = running_avg_returns
        alpha_vec_policy = AlphaVectorsPolicy(
            player_type=self.experiment_config.player_type,
            actions=self.simulation_env_config.joint_action_space_config.action_spaces[
                self.experiment_config.player_idx].actions,
            states=self.simulation_env_config.state_space_config.states,
            alpha_vectors=alpha_vectors, agent_type=self.experiment_config.agent_type, avg_R=avg_returns[-1],
            simulation_name=self.simulation_env_config.name, transition_tensor=T, reward_tensor=R)
        exp_result.policies[seed] = alpha_vec_policy
        return exp_result

    def hsvi(self, O: np.ndarray, Z: np.ndarray, R: np.ndarray, T: np.ndarray, A: np.ndarray, S: np.ndarray,
             gamma: float, b0: np.ndarray, epsilon: float, lp: bool = False, prune_frequency: int = 10,
             simulation_frequency: int = 10, simulate_horizon: int = 10, number_of_simulations: int = 10) \
            -> Tuple[List[List[float]], List[float], List[float], List[float], List[float], List[float], List[float]]:
        """
        Heuristic Search Value Iteration for POMDPs (Trey Smith and Reid Simmons, 2004)

        :param O: set of observations of the POMDP
        :param Z: observation tensor of the POMDP
        :param R: reward tensor of the POMDP
        :param T: transition tensor of the POMDP
        :param A: action set of the POMDP
        :param S: state set of the POMDP
        :param gamma: discount factor
        :param b0: initial belief point
        :param epsilon: accuracy parameter
        :param lp: whether to use LP to compute upper bound values or SawTooth approximation
        :param prune_frequency: how often to prune the upper and lower bounds
        :param simulation_frequency: how frequently to simulate the POMDP to compure rewards of current policy
        :param simulate_horizon: length of simulations to compute rewards
        :param number_of_simulations: number of simulations to estimate reward
        :return: None
        """
        # Initialize upper and lower bound
        lower_bound = self.initialize_lower_bound(R=R, S=S, A=A, gamma=gamma)
        upper_bound = self.initialize_upper_bound(T=T, A=A, S=S, gamma=gamma, R=R)

        # Initialize state
        w = self.width(lower_bound=lower_bound, upper_bound=upper_bound, b=b0, S=S, lp=lp)
        iteration = 0
        cumulative_r = 0
        average_rewards = []
        widths = []
        ub_sizes = []
        lb_sizes = []
        average_running_rewards = []
        initial_belief_value = []

        # HSVI iterations
        while w > epsilon:

            lower_bound, upper_bound = self.explore(
                b=b0, epsilon=epsilon, t=0, lower_bound=lower_bound, upper_bound=upper_bound,
                gamma=gamma, S=S, O=O, R=R, T=T, A=A, Z=Z, lp=lp)
            w = self.width(lower_bound=lower_bound, upper_bound=upper_bound, b=b0, S=S, lp=lp)

            if iteration % simulation_frequency == 0:
                r = 0
                for i in range(number_of_simulations):
                    r += self.simulate(horizon=simulate_horizon, b0=b0, lower_bound=lower_bound, Z=Z,
                                       R=R, gamma=gamma, T=T, A=A, O=O, S=S)
                cumulative_r = r / number_of_simulations

            if iteration > 1 and iteration % prune_frequency == 0:
                size_before_lower_bound = len(lower_bound)
                size_before_upper_bound = len(upper_bound[0])
                lower_bound = pruning.prune_lower_bound(lower_bound=lower_bound, S=S)
                upper_bound = self.prune_upper_bound(upper_bound=upper_bound, S=S, lp=lp)
                Logger.__call__().get_logger().debug(
                    f"[HSVI] Pruning, LB before:{size_before_lower_bound}, after:{len(lower_bound)}, "
                    f"UB before: {size_before_upper_bound},after:{len(upper_bound[0])}")

            initial_belief_V_star_upper = self.upper_bound_value(upper_bound=upper_bound, b=b0, S=S, lp=lp)
            initial_belief_V_star_lower = self.lower_bound_value(lower_bound=lower_bound, b=b0, S=S)
            iteration += 1

            if iteration % self.experiment_config.log_every == 0 and iteration > 0:
                Logger.__call__().get_logger().info(f"[HSVI] iteration: {iteration}, width: {w}, epsilon: {epsilon}, "
                                                    f"R: {cumulative_r}, "
                                                    f"UB size:{len(upper_bound[0])}, LB size:{len(lower_bound)},"
                                                    f"Upper V*[b0]: {initial_belief_V_star_upper},"
                                                    f"Lower V*[b0]:{initial_belief_V_star_lower}")

            average_rewards.append(cumulative_r)
            running_avg_J = ExperimentUtil.running_average(
                average_rewards, self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value)
            average_running_rewards.append(running_avg_J)
            widths.append(w)
            ub_sizes.append(len(upper_bound[0]))
            lb_sizes.append(len(lower_bound))
            initial_belief_value.append(initial_belief_V_star_lower)

        return (list(lower_bound), average_rewards, average_running_rewards, widths, ub_sizes, lb_sizes,
                initial_belief_value)

    def explore(self, b: np.ndarray, epsilon: float, t: int, lower_bound: List, upper_bound: Tuple[List, List],
                gamma: float, S: np.ndarray, O: np.ndarray, Z: np.ndarray, R: np.ndarray, T: np.ndarray, A: np.ndarray,
                lp: bool) -> Tuple[List, Tuple[List, List]]:
        """
        Explores the POMDP tree

        :param b: current belief
        :param epsilon: accuracy parameter
        :param t: the current depth of the exploration
        :param lower_bound: the lower bound on the value function
        :param upper_bound: the upper bound on the value function
        :param gamma: discount factor
        :param S: set of states
        :param O: set of observations
        :param Z: observation tensor
        :param R: reward tensor
        :param T: transition tensor
        :param A: set of actions
        :param lp: whether to use LP to compute upper bound values
        :return: new lower and upper bounds
        """
        w = self.width(lower_bound=lower_bound, upper_bound=upper_bound, b=b, S=S, lp=lp)
        print(f"explore, w:{w}, ep:{epsilon * math.pow(gamma, -t)}")
        if (gamma > 0 and w <= epsilon * math.pow(gamma, -t)) or (w <= epsilon):
            return lower_bound, upper_bound

        # Determine a*
        a_Q_vals = []
        for a in A:
            upper_Q = self.q(b=b, a=a, lower_bound=lower_bound, upper_bound=upper_bound, S=S, O=O, Z=Z,
                             R=R, gamma=gamma, T=T, upper=True, lp=lp)
            a_Q_vals.append(upper_Q)
        a_star = int(np.argmax(np.array(a_Q_vals)))

        # Determine o*
        o_vals = []
        for o in O:
            if self.observation_possible(o=o, b=b, Z=Z, T=T, S=S, a=a_star):
                new_belief = self.next_belief(o=o, a=a_star, b=b, S=S, Z=Z, T=T)
                o_val = (self.p_o_given_b_a(o=o, b=b, a=a_star, S=S, Z=Z, T=T) *
                         self.excess(lower_bound=lower_bound, upper_bound=upper_bound, b=new_belief, S=S,
                                     epsilon=epsilon, gamma=gamma, t=(t + 1), lp=lp))
                o_vals.append(o_val)
            else:
                o_vals.append(-np.inf)
        o_star = int(np.argmax(np.array(o_vals)))

        b_prime = self.next_belief(o=o_star, a=a_star, b=b, S=S, Z=Z, T=T)
        lower_bound, upper_bound = self.explore(b=b_prime, epsilon=epsilon, t=t + 1, lower_bound=lower_bound,
                                                upper_bound=upper_bound, gamma=gamma, S=S, O=O, R=R, T=T, A=A,
                                                Z=Z, lp=lp)

        lower_bound, upper_bound = \
            self.local_updates(lower_bound=lower_bound, upper_bound=upper_bound, b=b, A=A, S=S, Z=Z, O=O, R=R,
                               T=T, gamma=gamma, lp=lp)

        return lower_bound, upper_bound

    def initialize_lower_bound(self, R: np.ndarray, S: np.ndarray, A: np.ndarray, gamma: float) -> List:
        """
        Initializes the lower bound

        :param R: reward tensor
        :param S: set of states
        :param A: set of actions
        :param gamma: discount factor
        :return: the initialized lower bound
        """
        vals_1 = []
        for a in A:
            vals_2 = []
            for s in S:
                vals_2.append(R[a][s] / (1 - gamma))
            vals_1.append(min(vals_2))
        R_underbar = max(vals_1)
        alpha_vector = np.zeros(len(S))
        alpha_vector.fill(R_underbar)
        lower_bound = []
        lower_bound.append(alpha_vector)
        return lower_bound

    def initialize_upper_bound(self, T: np.ndarray, A: np.ndarray, S: np.ndarray, gamma: float, R: np.ndarray) \
            -> Tuple[List, List]:
        """
        Initializes the upper bound

        :param T: the transition tensor
        :param A: the set of actions
        :param S: the set of states
        :param R: the reward tensor
        :param gamma: the discount factor
        :return: the initialized upper bound
        """
        V, pi = self.vi(T=T, num_states=len(S), num_actions=len(A), R=R, theta=0.0001, discount_factor=gamma)
        point_set = []
        for s in S:
            b = self.generate_corner_belief(s=s, S=S)
            point_set.append([b, V[s]])
        return (point_set, point_set.copy())

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

    def local_updates(self, lower_bound: List, upper_bound: Tuple[List, List], b: np.ndarray, A: np.ndarray,
                      S: np.ndarray, O: np.ndarray, R: np.ndarray, T: np.ndarray, gamma: float, Z: np.ndarray,
                      lp: bool) -> Tuple[List, Tuple[List, List]]:
        """
        Perform local updates to the upper and  lower bounds for the given belief in the heuristic-search-exploration

        :param lower_bound: the lower bound on V
        :param upper_bound: the upper bound on V
        :param b: the current belief point
        :param A: the set of actions
        :param S: the set of states
        :param O: the set of observations
        :param R: the reward tensor
        :param T: the transition tensor
        :param gamma: the discount factor
        :param Z: the set of observations
        :param lp: a boolean flag whether to use LP to compute upper bound beliefs
        :return: The updated lower and upper bounds
        """
        new_upper_bound = self.local_upper_bound_update(upper_bound=upper_bound, b=b, A=A, S=S, O=O, R=R, T=T,
                                                        gamma=gamma, Z=Z, lp=lp)
        new_lower_bound = self.local_lower_bound_update(lower_bound=lower_bound, b=b, Z=Z, A=A, O=O, S=S, T=T,
                                                        R=R, gamma=gamma)
        return new_lower_bound, new_upper_bound

    def local_upper_bound_update(self, upper_bound: Tuple[List, List], b: np.ndarray, A: np.ndarray,
                                 S: np.ndarray, O: np.ndarray, R: np.ndarray, T: np.ndarray,
                                 gamma: float, Z: np.ndarray, lp: bool) -> Tuple[List, List]:
        """
        Performs a local update to the upper bound during the heuristic-search exploration

        :param upper_bound: the upper bound to update
        :param b: the current belief point
        :param A: the set of actions
        :param S: the set of states
        :param O: the set of observations
        :param R: the reward tensor
        :param T: the transition tensor
        :param gamma: the discount factor
        :param Z: the set of observations
        :param lp: whether or not to use LP to compute upper bound beliefs
        :return: the updated upper bound
        """
        b, new_val = self.upper_bound_backup(upper_bound=upper_bound, b=b, A=A, S=S, Z=Z, O=O, R=R, T=T,
                                             gamma=gamma, lp=lp)
        upper_bound_point_set, corner_points = upper_bound
        upper_bound_point_set.append([b, new_val])
        new_corner_points = self.update_corner_points(corner_points=corner_points, new_point=(b, new_val))
        upper_bound = (upper_bound_point_set, new_corner_points)
        return upper_bound

    def update_corner_points(self, corner_points: List, new_point: Tuple[np.ndarray, float]) -> List:
        """
        (Maybe) update the corner points of the upper bound

        :param corner_points: the current set of corner points
        :param new_point: the new point to add to the upper bound
        :return: the new set of corner points
        """
        new_corner_points = []
        for cp in corner_points:
            corner_match = True
            for i in range(len(cp[0])):
                if cp[0][i] != new_point[0][i]:
                    corner_match = False
            if corner_match:
                new_corner_points.append((cp[0], new_point[1]))
            else:
                new_corner_points.append(cp)
        return new_corner_points

    def local_lower_bound_update(self, lower_bound: List, b: np.ndarray, A: np.ndarray, O: np.ndarray,
                                 Z: np.ndarray, S: np.ndarray,
                                 T: np.ndarray, R: np.ndarray, gamma: float) -> List:
        """
        Performs a local update to the lower bound given a belief point in the heuristic search

        :param lower_bound: the current lower bound
        :param b: the current belief point
        :param A: the set of actions
        :param O: the set of observations
        :param Z: the observation tensor
        :param S: the set of states
        :param T: the transition tensor
        :param R: the reward tensor
        :param gamma: the discount factor
        :return: the updated lower bound
        """
        beta = self.lower_bound_backup(lower_bound=lower_bound, b=b, A=A, Z=Z, O=O, S=S, T=T, R=R, gamma=gamma)
        if not pruning.check_duplicate(lower_bound, beta):
            lower_bound.append(beta)
        return lower_bound

    def lower_bound_backup(self, lower_bound: List, b: np.ndarray, A: np.ndarray, O: np.ndarray, Z: np.ndarray,
                           S: np.ndarray, T: np.ndarray, R: np.ndarray, gamma: float) -> np.ndarray:
        """
        Generates a new alpha-vector for the lower bound

        :param lower_bound: the current lower bound
        :param b: the current belief point
        :param A: the set of actions
        :param O: the set of observations
        :param Z: the observation tensor
        :param S: the set of states
        :param T: the transition tensor
        :param R: the reward tensor
        :param gamma: the discount factor
        :return: the new alpha vector
        """
        max_beta_a_o_alpha_vecs = []
        for a in A:
            max_beta_a_vecs = []
            for o in O:
                if self.observation_possible(o=o, b=b, Z=Z, T=T, S=S, a=a):
                    new_belief = np.array(self.next_belief(o=o, a=a, b=b, S=S, Z=Z, T=T))
                    max_alpha_vec = lower_bound[0]
                    max_alpha_val = float("-inf")
                    for alpha_vec in lower_bound:
                        alpha_val = new_belief.dot(alpha_vec)
                        if alpha_val > max_alpha_val:
                            max_alpha_val = alpha_val
                            max_alpha_vec = alpha_vec
                    max_beta_a_vecs.append(max_alpha_vec)
            max_beta_a_o_alpha_vecs.append(max_beta_a_vecs)
        beta_a_vecs = []
        for a in A:
            beta_a_vec = []
            for s in S:
                o_idx = 0
                beta_a_s_val = 0
                beta_a_s_val += R[a][s]
                expected_future_vals = 0
                for o in O:
                    if self.observation_possible(o=o, b=b, Z=Z, T=T, S=S, a=a):
                        for s_prime in S:
                            expected_future_vals += (max_beta_a_o_alpha_vecs[a][o_idx][s_prime] * Z[a][s_prime][o] *
                                                     T[a][s][s_prime])
                        o_idx += 1
                beta_a_s_val += gamma * expected_future_vals
                beta_a_vec.append(beta_a_s_val)
            beta_a_vecs.append(beta_a_vec)

        beta = beta_a_vecs[0]
        max_val = float("-inf")
        for beta_a_vec in beta_a_vecs:
            val = np.array(beta_a_vec).dot(np.array(b))
            if val > max_val:
                max_val = val
                beta = beta_a_vec

        return beta

    def upper_bound_backup(self, upper_bound: Tuple[List, List], b: np.ndarray, A: np.ndarray, S: np.ndarray,
                           O: np.ndarray, Z: np.ndarray, R: np.ndarray, T: np.ndarray,
                           gamma: float, lp: bool) -> Tuple[np.ndarray, float]:
        """
        Adds a point to the upper bound

        :param upper_bound: the current upper bound
        :param b: the current belief point
        :param A: the set of actions
        :param S: the set of states
        :param O: the set of observations
        :param Z: the observation tensor
        :param R: the reward tensor
        :param T: the transition tensor
        :param gamma: the discount factor
        :param lp: a boolean flag whether to use LP to compute the upper bound belief
        :return: the new point
        """
        q_vals = []
        for a in A:
            v = 0
            for s in S:
                immediate_r = b[s] * R[a][s]
                expected_future_rew = 0
                for o in O:
                    if self.observation_possible(o=o, b=b, Z=Z, T=T, S=S, a=a):
                        new_belief = self.next_belief(o=o, a=a, b=b, S=S, Z=Z, T=T)
                        for s_prime in S:
                            expected_future_rew += \
                                b[s] * T[a][s][s_prime] * Z[a][s_prime][o] * self.upper_bound_value(
                                    upper_bound=upper_bound, b=new_belief, S=S, lp=lp)
                v += immediate_r + gamma * expected_future_rew
            q_vals.append(v)
        new_val = max(q_vals)
        return b, new_val

    def lp_convex_hull_projection_lp(self, upper_bound: Tuple[List, List], b: np.ndarray, S: np.ndarray) -> float:
        """
        Reference: (Hauskreht 2000)

        Computes the upper bound belief by performing a projection onto the convex hull of the upper bound,
        it is computed by solving an LP

        :param upper_bound: the upper bound
        :param b: the belief point to compute the value for
        :param S: the set of states
        :return: the upper bound value of the belief point
        """
        upper_bound_point_set, corner_points = upper_bound

        problem = pulp.LpProblem("ConvexHullProjection", pulp.LpMinimize)

        # Convex hull coefficients
        lamb = []
        for i in range(len(upper_bound_point_set)):
            lamb_i = pulp.LpVariable("lambda_" + str(i), lowBound=0, upBound=1, cat=pulp.LpContinuous)
            lamb.append(lamb_i)

        # The objective function
        objective = 0
        for i, point in enumerate(upper_bound_point_set):
            objective += lamb[i] * point[1]
        problem += objective, "Convex hull projection"

        # --- The constraints ---

        # Belief probability constraint
        for j in range(len(S)):
            belief_sum = 0
            for i, point in enumerate(upper_bound_point_set):
                belief_sum += lamb[i] * point[0][j]
            problem += belief_sum == b[j], "BeliefVectorConstraint_" + str(j)

        # Convex Hull constraint
        lambda_weights_sum = 0
        for i in range(len(lamb)):
            lambda_weights_sum += lamb[i]
        problem += lambda_weights_sum == 1, "ConvexHullWeightsSumConstraint"

        # Solve
        problem.solve(pulp.PULP_CBC_CMD(msg=0))

        # Obtain solution
        projected_lamb_coefficients = []
        belief_value = 0
        for i in range(len(upper_bound_point_set)):
            projected_lamb_coefficients.append(lamb[i].varValue)
            belief_value += projected_lamb_coefficients[i] * upper_bound_point_set[i][1]

        return belief_value

    def approximate_projection_sawtooth(self, upper_bound: Tuple[List, List], b: np.ndarray, S: np.ndarray) -> float:
        """
        Reference: (Hauskreht 2000)

        Performs an approximate projection of the belief onto the convex hull of the upepr bound
        to compute the upper bound value of the belief

        :param upper_bound: the upper bound
        :param b: the belief point
        :param S: the set of states
        :return: the value of the belief point
        """
        upper_bound_point_set, corner_points = upper_bound
        alpha_corner = np.array(corner_points)[:, 1]

        # min_val = corner_points_belief_value
        interior_belief_values = []
        for point in upper_bound_point_set:
            interior_belief_values.append(self.interior_point_belief_val(interior_point=point, b=b,
                                                                         alpha_corner=alpha_corner, S=S))
        return min(interior_belief_values)

    def interior_point_belief_val(self, interior_point: Tuple[np.ndarray, float], b: np.ndarray,
                                  alpha_corner: np.ndarray, S: np.ndarray) -> float:
        """
        Computes the value induced on the belief point b projected onto the convex hull by a given interior belief point

        :param interior_point: the interior point
        :param b: the belief point
        :param alpha_corner: the alpha vector corresponding to the corners of the belief simplex
        :param S: the set of states
        :return: the value of the belief point induced by the interior point
        """
        min_ratios = []
        for s in S:
            if interior_point[0][s] > 0:
                min_ratio = b[s] / interior_point[0][s]
                min_ratios.append(min_ratio)
            else:
                min_ratios.append(float("inf"))
        min_ratio = min(min_ratios)

        if min_ratio > 1:
            min_ratio = 1

        interior_alpha_corner_dot = alpha_corner.dot(interior_point[0])

        return interior_alpha_corner_dot + min_ratio * (interior_point[1] - interior_alpha_corner_dot)

    def upper_bound_value(self, upper_bound: Tuple[List, List], b: np.ndarray, S: np.ndarray, lp: bool = False) \
            -> float:
        """
        Computes the upper bound value of a given belief point

        :param upper_bound: the upper bound
        :param b: the belief point
        :param S: the set of states
        :param lp: boolean flag that decides whether to use LP to compute the upper bound value or not
        :return: the upper bound value
        """

        if lp:
            return self.lp_convex_hull_projection_lp(upper_bound=upper_bound, b=b, S=S)
        else:
            return self.approximate_projection_sawtooth(upper_bound=upper_bound, b=b, S=S)

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

    def next_belief(self, o: int, a: int, b: List, S: List, Z: List, T: List) -> List:
        """
        Computes the next belief using a Bayesian filter

        :param o: the latest observation
        :param a: the latest action
        :param b: the current belief
        :param S: the set of states
        :param Z: the observation tensor
        :param T: the transition tensor
        :return: the new belief
        """
        b_prime = np.zeros(len(S))
        for s_prime in S:
            b_prime[s_prime] = self.bayes_filter(s_prime=s_prime, o=o, a=a, b=b, S=S, Z=Z, T=T)
        assert round(sum(b_prime), 5) == 1
        return b_prime

    def bayes_filter(self, s_prime: int, o: int, a: int, b: List, S: List, Z: List, T: List) -> float:
        """
        A Bayesian filter to compute the belief of being in s_prime when observing o after taking action a in belief b

        :param s_prime: the state to compute the belief of
        :param o: the observation
        :param a: the action
        :param b: the current belief point
        :param S: the set of states
        :param Z: the observation tensor
        :param T: the transition tensor
        :return: b_prime(s_prime)
        """
        norm = 0
        for s in S:
            for s_prime_1 in S:
                prob_1 = Z[a][s_prime_1][o]
                norm += b[s] * prob_1 * T[a][s][s_prime_1]
        if norm == 0:
            return 0
        temp = 0
        for s in S:
            temp += b[s] * T[a][s][s_prime] * Z[a][s_prime][o]
        b_prime = (temp) / norm
        assert b_prime <= 1
        return b_prime

    def p_o_given_b_a(self, o: int, b: np.ndarray, a: int, S: np.ndarray, Z: np.ndarray, T: np.ndarray) -> float:
        """
        Computes P[o|a,b]

        :param o: the observation
        :param b: the belief point
        :param a: the action
        :param S: the set of states
        :param Z: the observation tensor
        :param T: the transition tensor
        :return: the probability of observing o when taking action a in belief point b
        """
        prob = 0
        for s in S:
            for s_prime in S:
                prob += b[s] * T[a][s][s_prime] * Z[a][s_prime][o]
        prob = round(prob, 3)
        assert round(prob, 3) <= 1
        return prob

    def excess(self, lower_bound: List, upper_bound: Tuple[List, List], b: np.ndarray,
               S: np.ndarray, epsilon: float, gamma: float, t: int, lp: bool) -> float:
        """
        Computes the excess uncertainty  (Trey Smith and Reid Simmons, 2004)

        :param lower_bound: the lower bound
        :param upper_bound: the upper bound
        :param b: the current belief point
        :param S: the set of states
        :param epsilon: the epsilon accuracy parameter
        :param gamma: the discount factor
        :param t: the current exploration depth
        :param lp: whether to use LP or not to compute upper bound belief values
        :return: the excess uncertainty
        """
        w = self.width(lower_bound=lower_bound, upper_bound=upper_bound, b=b, S=S, lp=lp)
        if gamma == 0:
            return w
        else:
            return w - epsilon * math.pow(gamma, -(t))

    def width(self, lower_bound: List, upper_bound: Tuple[List, List], b: np.ndarray, S: np.ndarray, lp: bool) -> float:
        """
        Computes the bounds width (Trey Smith and Reid Simmons, 2004)

        :param lower_bound: the current lower bound
        :param upper_bound: the current upper bound
        :param b: the current belief point
        :param S: the set of states
        :param lp: boolean flag that decides whether to use LP to compute upper bound belief values
        :return: the width of the bounds
        """
        ub = self.upper_bound_value(upper_bound=upper_bound, b=b, S=S, lp=lp)
        lb = self.lower_bound_value(lower_bound=lower_bound, b=b, S=S)
        return ub - lb

    def q_hat_interval(self, b: np.ndarray, a: int, S: np.ndarray, O: np.ndarray, Z: np.ndarray, R: np.ndarray,
                       T: np.ndarray, gamma: float, lower_bound: List, upper_bound: Tuple[List, List], lp: bool) \
            -> List:
        """
        Computes the interval (Trey Smith and Reid Simmons, 2004)

        :param b: the current belief point
        :param a: the action
        :param S: the set of states
        :param O: the set of observations
        :param Z: the observation tensor
        :param R: the reward tensor
        :param T: the transition tensor
        :param gamma: the discount factor
        :param lower_bound: the lower bound
        :param upper_bound: the upper bound
        :param lp: boolean flag that decides whether to use LP to compute upper bound belief values
        :return: the interval
        """
        upper_Q = self.q(b=b, a=a, lower_bound=lower_bound, upper_bound=upper_bound, S=S, O=O, Z=Z,
                         R=R, gamma=gamma, T=T, upper=True, lp=lp)
        lower_Q = self.q(b=b, a=a, lower_bound=lower_bound, upper_bound=upper_bound, S=S, O=O, Z=Z,
                         R=R, gamma=gamma, T=T, upper=False, lp=lp)
        return [lower_Q, upper_Q]

    def q(self, b: np.ndarray, a: int, lower_bound: List, upper_bound: Tuple[List, List], S: np.ndarray, O: np.ndarray,
          Z: np.ndarray, R: np.ndarray, gamma: float, T: np.ndarray, upper: bool = True, lp: bool = False) -> float:
        """
        Applies the Bellman equation to compute Q values

        :param b: the belief point
        :param a: the action
        :param lower_bound: the lower bound
        :param upper_bound: the upper bound
        :param S: the set of states
        :param O: the set of observations
        :param Z: the observation tensor
        :param R: the reward tensor
        :param gamma: the discount factor
        :param T: the transition tensor
        :param upper: boolean flag that decides whether to use the upper bound or lower bound on V to
                      compute the Q-value
        :param lp: boolean flag that decides whether to use LP to compute upper bound belief values
        :return: the Q-value
        """
        Q_val = 0
        for s in S:
            immediate_r = R[a][s] * b[s]
            expected_future_rew = 0
            for o in O:
                if self.observation_possible(o=o, b=b, Z=Z, T=T, S=S, a=a):
                    new_belief = self.next_belief(o=o, a=a, b=b, S=S, Z=Z, T=T)
                    for s_prime in S:
                        if upper:
                            future_val = self.upper_bound_value(upper_bound=upper_bound, b=new_belief, S=S, lp=lp)
                        else:
                            future_val = self.lower_bound_value(lower_bound=lower_bound, b=new_belief, S=S)
                        expected_future_rew += \
                            b[s] * T[a][s][s_prime] * Z[a][s_prime][o] * future_val
            Q_val += immediate_r + expected_future_rew * gamma
        return Q_val

    def prune_upper_bound(self, upper_bound: Tuple[List, List], S: np.ndarray, lp: bool) -> Tuple[List, List]:
        """
        Prunes the points in the upper bound

        :param upper_bound: the current upper bound
        :param S: the set of states
        :param lp: boolean flag that decides whether to use LP to compute upper bound belief values
        :return: the pruned upper bound
        """

        upper_bound_point_set, corner_points = upper_bound
        pruned_upper_bound_point_set = []

        for point in upper_bound_point_set:
            true_val = self.upper_bound_value(upper_bound=upper_bound, S=S, b=point[0], lp=lp)
            if not (point[1] > true_val):
                pruned_upper_bound_point_set.append(point)

        return pruned_upper_bound_point_set, corner_points

    def simulate(self, horizon: int, b0: List, lower_bound: List, Z: np.ndarray, R: np.ndarray, gamma: float,
                 T: np.ndarray, A: np.ndarray,
                 O: np.ndarray, S: np.ndarray) -> float:
        """
        Simulates the POMDP to estimate the reward of the greedy policy with respect to the value function represented
        by the lower bound

        :param horizon: the horizon for the simulation
        :param b0: the initial belief
        :param lower_bound: the lower bound which represents the value function
        :param Z: the observation tensor
        :param R: the reward tensor
        :param gamma: the discount factor
        :param T: the transition operator
        :param A: the action set
        :param O: the observation set
        :param S: the set of states
        :return: the cumulative discounted reward
        """
        t = 0
        b = b0
        cumulative_r = 0
        while t < horizon:
            q_values = list(map(lambda a: self.q(
                b=b, a=a, lower_bound=lower_bound, upper_bound=([], []), S=S, O=O, Z=Z, R=R, gamma=gamma, T=T,
                upper=False, lp=False), A))
            a = int(np.argmax(np.array(q_values)))
            r = 0
            for s in S:
                r += R[a][s] * b[s]
            cumulative_r += math.pow(gamma, t) * r
            observation_probabilities = []
            for o in O:
                p = 0
                for s in S:
                    for s_prime in S:
                        p += b[s] * T[a][s][s_prime] * Z[a][s_prime][o]
                observation_probabilities.append(p)
            o = np.random.choice(np.arange(0, len(O)), p=observation_probabilities)
            b = self.next_belief(o=o, a=a, b=b, S=S, Z=Z, T=T)
            t += 1

        return cumulative_r

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
           theta=0.0001, discount_factor=1.0) -> Tuple[np.ndarray, np.ndarray]:
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

    def observation_possible(self, o, b, Z, T, S, a) -> bool:
        """
        Checks if a given observation can be observed when taking a given action in a given state

        :param o: the observation to check
        :param b: the belief to check
        :param Z: the observation tensor
        :param T: the transition tensor
        :param S: the state space
        :param a: the aciton tocheck
        :return: true if possible otherwise fasle
        """
        prob = 0
        for s in S:
            for s_prime in S:
                prob += b[s] * T[a][s][s_prime] * Z[a][s_prime][o]
        return prob > 0
