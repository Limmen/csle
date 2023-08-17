from typing import List, Optional, Tuple, Any
import math
import time
import os
import numpy as np
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
from csle_common.dao.training.alpha_vectors_policy import AlphaVectorsPolicy
from csle_common.util.general_util import GeneralUtil
from csle_common.dao.simulation_config.base_env import BaseEnv
from csle_agents.agents.base.base_agent import BaseAgent
import csle_agents.constants.constants as agents_constants
from scipy.optimize import linprog
from itertools import product


class SondikVIAgent(BaseAgent):
    """
    Sondik's value iteration for POMDPs (Sondik 1971)
    """

    def __init__(self, simulation_env_config: SimulationEnvConfig,
                 experiment_config: ExperimentConfig,
                 training_job: Optional[TrainingJobConfig] = None, save_to_metastore: bool = True,
                 env: Optional[BaseEnv] = None):
        """
        Initializes the Sondik-VI agent

        :param simulation_env_config: configuration of the simulation environment
        :param experiment_config: the experiment configuration
        :param training_job: an existing training job to use (optional)
        :param save_to_metastore: boolean flag whether to save the execution to the metastore
        :param env: the gym environment for training
        """
        super().__init__(simulation_env_config=simulation_env_config, emulation_env_config=None,
                         experiment_config=experiment_config)
        assert experiment_config.agent_type == AgentType.SONDIK_VALUE_ITERATION
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
        exp_result.plot_metrics.append(agents_constants.SONDIK_VI.INITIAL_BELIEF_VALUES)
        exp_result.plot_metrics.append(agents_constants.SONDIK_VI.NUM_ALPHA_VECTORS)

        descr = f"Computation of V* with the Sondik value algorithm using " \
                f"simulation:{self.simulation_env_config.name}"

        for seed in self.experiment_config.random_seeds:
            exp_result.all_metrics[seed] = {}
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.SONDIK_VI.NUM_ALPHA_VECTORS] = []
            exp_result.all_metrics[seed][agents_constants.SONDIK_VI.INITIAL_BELIEF_VALUES] = []

        if self.env is None:
            self.env = gym.make(self.simulation_env_config.gym_env_name,
                                config=self.simulation_env_config.simulation_env_input_config)

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
            exp_result = self.sondik_vi_algorithm(exp_result=exp_result, seed=seed)

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
                agents_constants.SONDIK_VI.TRANSITION_TENSOR,
                agents_constants.SONDIK_VI.REWARD_TENSOR, agents_constants.SONDIK_VI.OBSERVATION_TENSOR,
                agents_constants.SONDIK_VI.OBSERVATION_SPACE, agents_constants.SONDIK_VI.STATE_SPACE,
                agents_constants.SONDIK_VI.USE_PRUNING, agents_constants.SONDIK_VI.PLANNING_HORIZON,
                agents_constants.SONDIK_VI.INITIAL_BELIEF]

    def sondik_vi_algorithm(self, exp_result: ExperimentResult, seed: int) -> ExperimentResult:
        """
        Runs

        :param exp_result: the experiment result object
        :param seed: the random seed
        :return: the updated experiment result
        """
        discount_factor = self.experiment_config.hparams[agents_constants.COMMON.GAMMA].value
        eval_batch_size = self.experiment_config.hparams[agents_constants.COMMON.EVAL_BATCH_SIZE].value
        T = self.experiment_config.hparams[agents_constants.SONDIK_VI.TRANSITION_TENSOR].value
        R = self.experiment_config.hparams[agents_constants.SONDIK_VI.REWARD_TENSOR].value
        Z = self.experiment_config.hparams[agents_constants.SONDIK_VI.OBSERVATION_TENSOR].value
        O = self.experiment_config.hparams[agents_constants.SONDIK_VI.OBSERVATION_SPACE].value
        S = self.experiment_config.hparams[agents_constants.SONDIK_VI.STATE_SPACE].value
        A = self.experiment_config.hparams[agents_constants.SONDIK_VI.ACTION_SPACE].value
        b0 = self.experiment_config.hparams[agents_constants.SONDIK_VI.INITIAL_BELIEF].value
        use_pruning = \
            self.experiment_config.hparams[agents_constants.SONDIK_VI.USE_PRUNING].value
        planning_horizon = self.experiment_config.hparams[agents_constants.SONDIK_VI.PLANNING_HORIZON].value
        Logger.__call__().get_logger().info(f"Starting Sondik's value iteration,"
                                            f"discount_factor: {discount_factor}, pruning: {use_pruning}, b0: {b0}")
        alpha_vectors, num_alpha_vectors, initial_belief_values, avg_returns, running_avg_returns = \
            self.sondik_vi(P=np.array(T), R=np.array(R), n_obs=len(O), n_states=len(S), Z=np.array(Z), n_actions=len(A),
                           b0=b0, T=planning_horizon, gamma=discount_factor, eval_batch_size=eval_batch_size)
        exp_result.all_metrics[seed][agents_constants.SONDIK_VI.INITIAL_BELIEF_VALUES] = initial_belief_values
        exp_result.all_metrics[seed][agents_constants.SONDIK_VI.NUM_ALPHA_VECTORS] = num_alpha_vectors
        exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN] = avg_returns
        exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN] = running_avg_returns
        alpha_vec_policy = AlphaVectorsPolicy(
            player_type=self.experiment_config.player_type,
            actions=self.simulation_env_config.joint_action_space_config.action_spaces[
                self.experiment_config.player_idx].actions,
            states=self.simulation_env_config.state_space_config.states,
            alpha_vectors=alpha_vectors, agent_type=self.experiment_config.agent_type, avg_R=-1,
            simulation_name=self.simulation_env_config.name, transition_tensor=T, reward_tensor=R)
        exp_result.policies[seed] = alpha_vec_policy
        return exp_result

    def compute_all_conditional_plans_conditioned_on_a_t(self, n_alpha_vectors_t_plus_one, n_obs):
        """
        Compute the number of conditional plans conditioned on an action a. It produces all possible combinations of
        (observation -> conditional_plan)

        :param n_alpha_vectors_t_plus_one: Number of alpha-vectors (number of conditional plans) for t+1
        :param n_obs: Number of observations
        :return: list of lists, where each list contains n_obs elements, and each element is in [0, n_alpha_vectors-1].

        The number of conditional plans will be be n_alpha_vectors^n_obs elements.
        The plan is of the form: (o^(1)_i, o^(2)_j, ..., o^(n_alpha_vectors_t_plus_one)_k)
        where o^(1)_i means that if observation o_i is observed, conditional plan 1 should be followed,
        o^(2)_j means that if observation o_j is observed, conditional plan 2 should be followed,
        o^(n_alpha_vectors_t_plus_one)_k means that if observation o_k is observed, conditional plan
        n_alpha_vectors_t_plus_one should be followed.
        """
        x = list(range(n_alpha_vectors_t_plus_one))
        return [p for p in product(x, repeat=n_obs)]

    def sondik_vi(self, P, Z, R, T, gamma, n_states, n_actions, n_obs, b0, eval_batch_size: int,
                  use_pruning: bool = True) \
            -> Tuple[List[Any], List[int], List[float], List[float], List[float]]:
        """

        :param P: The transition probability matrix
        :param Z: The observation probability matrix
        :param R: The immediate rewards matrix
        :param T: The planning horizon
        :param gamma: The discount factor
        :param n_states: The number of states
        :param n_actions: The number of actions
        :param n_obs: The number of observations
        :param eval_batch_size: number of simulations to evaluate the policy induced by the alpha vectors
                               at each iteration
        :param b0: The initial belief
        :return:
        """
        alepth_t_plus_1 = set()
        zero_alpha_vec = (-1, tuple(np.zeros(n_states)))  # an alpha vector is associated with an action and
        # a set of values
        alepth_t_plus_1.add(zero_alpha_vec)
        first = True
        num_alpha_vectors: List[int] = []
        num_alpha_vectors.append(len(alepth_t_plus_1))
        initial_values: List[float] = []
        average_returns: List[float] = []
        average_running_returns: List[float] = []

        # Backward induction
        for t in range(T):
            Logger.__call__().get_logger().info(
                '[Value Iteration] planning horizon {}, |aleph|:{} ...'.format(t, len(alepth_t_plus_1)))

            # New set of alpha vectors which will be constructed from the previous (backwards) set aleph_t+1.
            aleph_t = set()

            # Weight the alpha vectors in aleph_t by the transition probabilities alpha(s)*Z(s'|s,o)*P(s'|s,a)
            # forall a,o,s,s'
            # alpha'(s) = alpha(s)*Z(s'|s,o)*P(s'|s,a) forall a,o,s,s'
            alpha_new = np.zeros(shape=(len(alepth_t_plus_1), n_actions, n_obs, n_states))
            n_alpha_vectors = 0
            for old_alpha_vec in alepth_t_plus_1:
                for a in range(n_actions):
                    for o in range(n_obs):
                        for s in range(n_states):
                            for s_prime in range(n_states):
                                # Half of Sondik's one-pass DP backup, alpha'_(a,o)(s)=alpha(s')*Z(s'|s,o)*P(s'|s,a)
                                # forall a,o,s,s'
                                # note that alpha(s) is a representation of $V(s)$
                                alpha_new[n_alpha_vectors][a][o][s] += \
                                    np.array(old_alpha_vec[1][s_prime]) * Z[a][s_prime][o] * P[a][s][s_prime]
                n_alpha_vectors += 1

            # Compute the new alpha vectors by adding the discounted immediate rewards and the expected
            # alpha vectors at time t+1
            # There are in total |Gamma^(k+1)|=|A|*|Gamma^k|^(|Z|) number of conditional plans, which means that there
            # is |Gamma^(k+1)|=|A|*|Gamma^k|^(|Z|) number of alpha vectors
            for a in range(n_actions):

                # |Gamma^k|^(|Z|) number of conditional plans conditioned on 'a'
                conditional_plans_conditioned_on_a = self.compute_all_conditional_plans_conditioned_on_a_t(
                    n_alpha_vectors, n_obs)

                # Each conditional plan is of the form (o^(1)_i, o^(2)_j, ..., o^(n_alpha_vectors_t_plus_one)_k)
                # where o^(p)_i means that if observation o_i is observed, conditional plan p should be followed
                for conditional_plan_conditioned_on_a in conditional_plans_conditioned_on_a:
                    for o in range(n_obs):
                        conditional_plan_to_follow_when_observing_o = conditional_plan_conditioned_on_a[o]
                        temp = np.zeros(n_states)
                        for s in range(n_states):
                            # Second half of Sondik's one-pass DP backup,
                            # alpha_(a,o,beta)'(s) = gamma*(R(a,s) alpha_beta(s)*Z(s'|s,o)*P(s'|s,a) forall a,o,s,s')
                            temp[s] = gamma * (R[a][s] +
                                               alpha_new[conditional_plan_to_follow_when_observing_o][a][o][s])
                        aleph_t.add((a, tuple(temp)))

            alepth_t_plus_1.update(aleph_t)
            num_alpha_vectors.append(len(alepth_t_plus_1))

            if first:
                # remove the dummy alpha vector
                alepth_t_plus_1.remove(zero_alpha_vec)
                first = False

            if use_pruning:
                alepth_t_plus_1 = self.prune(n_states, alepth_t_plus_1)  # remove dominated alpha vectors

            # The optimal value function is implicitly represented by aleph^0. Note that aleph^0 is a much larger set of
            # elements than the set of states. To compute the optimal value function V^*(b0) given an initial belief b0,
            # compute
            # V^*(b) = max_alpha b0*alpha for all alpha in aleph^0
            max_v = -np.inf
            for alpha in aleph_t:
                v = np.dot(np.array(alpha[1]), b0)

                if v > max_v:
                    max_v = v
            initial_values.append(max_v)
            avg_R = -1.0
            if len(average_returns) > 0:
                avg_R = average_returns[-1]
            alpha_vec_policy = AlphaVectorsPolicy(
                player_type=self.experiment_config.player_type,
                actions=self.simulation_env_config.joint_action_space_config.action_spaces[
                    self.experiment_config.player_idx].actions,
                states=self.simulation_env_config.state_space_config.states,
                alpha_vectors=list(map(lambda x: x[1], list(aleph_t))), agent_type=self.experiment_config.agent_type,
                avg_R=avg_R,
                simulation_name=self.simulation_env_config.name, transition_tensor=P, reward_tensor=R)
            avg_r = self.evaluate_policy(alpha_vec_policy, eval_batch_size=eval_batch_size)
            average_returns.append(avg_r)
            running_avg_J = ExperimentUtil.running_average(
                average_returns, self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value)
            average_running_returns.append(running_avg_J)
        vectors: List[Any] = list(map(lambda x: x[1], list(aleph_t)))
        return (vectors, num_alpha_vectors, initial_values, average_returns,
                average_running_returns)

    def prune(self, n_states, aleph):
        """
        Remove dominated alpha-vectors using Lark's filtering algorithm
        :param n_states
        :return:
        """
        # parameters for linear program
        delta = 0.0000000001
        # equality constraints on the belief states
        A_eq = np.array([np.append(np.ones(n_states), [0.])])
        b_eq = np.array([1.])

        # dirty set
        F = aleph.copy()

        # clean set
        Q = set()

        for i in range(n_states):
            max_i = -np.inf
            best = None
            for av in F:
                # av[1] = np.array(av[1])
                if av[1][i] > max_i:
                    max_i = av[1][i]
                    best = av
            if best is not None and len(F) > 0:
                Q.update({best})
                F.remove(best)
        while F:
            av_i = F.pop()  # get a reference to av_i
            F.add(av_i)  # don't want to remove it yet from F
            dominated = False
            for av_j in Q:
                c = np.append(np.zeros(n_states), [1.])
                A_ub = np.array([np.append(-(np.array(av_i[1]) - np.array(av_j[1])), [-1.])])
                b_ub = np.array([-delta])

                res = linprog(c, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub, bounds=(0, None))
                if res.x[n_states] > 0.0:
                    # this one is dominated
                    dominated = True
                    F.remove(av_i)
                    break

            if not dominated:
                max_k = -np.inf
                best = None
                for av_k in F:
                    b = res.x[0:2]
                    v = np.dot(av_k.v, b)
                    if v > max_k:
                        max_k = v
                        best = av_k
                F.remove(best)
                if not self.check_duplicate(Q, best):
                    Q.update({best})
        return Q

    def check_duplicate(self, a, av):
        """
        Check whether alpha vector av is already in set a

        :param a:
        :param av:
        :return:
        """
        for av_i in a:
            if np.allclose(av_i[1], av.v):
                return True
            if av_i[1][0] == av[1][0] and av_i[1][1] > av[1][1]:
                return True
            if av_i[1][1] == av[1][1] and av_i[1][0] > av[1][0]:
                return True

    def evaluate_policy(self, policy: AlphaVectorsPolicy, eval_batch_size: int) -> float:
        """
        Evalutes a tabular policy

        :param policy: the tabular policy to evaluate
        :param eval_batch_size: the batch size
        :return: None
        """
        if self.env is None:
            raise ValueError("An environment must be specified to run policy evaluation")
        returns = []
        for i in range(eval_batch_size):
            done = False
            o, _ = self.env.reset()
            R = 0
            while not done:
                b1 = o[1]
                b = [1 - b1, b1, 0]
                a = policy.action(b)
                o, r, done, _, info = self.env.step(a)
                R += r
            returns.append(R)
        avg_return = np.mean(returns)
        return float(avg_return)
