from typing import Union, List, Dict, Optional
import random
import time
import gym
import os
import numpy as np
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.experiment_execution import ExperimentExecution
from csle_common.dao.training.experiment_result import ExperimentResult
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.player_type import PlayerType
from csle_common.util.experiment_util import ExperimentUtil
from csle_common.logging.log import Logger
from csle_common.dao.training.t_spsa_policy import TSPSAPolicy
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.jobs.training_job_config import TrainingJobConfig
from csle_agents.base.base_agent import BaseAgent
import csle_agents.constants.constants as agents_constants


class TSPSAAgent(BaseAgent):
    """
    RL Agent implementing the T-SPSA algorithm from
    (Hammar, Stadler 2021 - Intrusion Prevention through Optimal Stopping))
    """

    def __init__(self, simulation_env_config: SimulationEnvConfig,
                 emulation_env_config: Union[None, EmulationEnvConfig],
                 experiment_config: ExperimentConfig, env: Optional[gym.Env] = None,
                 training_job: Optional[TrainingJobConfig] = None):
        """
        Initializes the TSPSA agent

        :param simulation_env_config: the simulation env config
        :param emulation_env_config: the emulation env config
        :param experiment_config: the experiment config
        :param env: (optional) the gym environment to use for simulation
        :param training_job: (optional) a training job configuration
        """
        super().__init__(simulation_env_config=simulation_env_config, emulation_env_config=emulation_env_config,
                         experiment_config=experiment_config)
        assert experiment_config.agent_type == AgentType.T_SPSA
        self.env = env
        self.training_job = training_job

    def train(self) -> ExperimentExecution:
        """
        Performs the policy training for the given random seeds using T-SPSA

        :return: the training metrics and the trained policies
        """
        pid = os.getpid()

        # Initialize metrics
        exp_result = ExperimentResult()
        exp_result.plot_metrics.append(agents_constants.COMMON.AVERAGE_REWARD)
        descr = f"Training of policies with the T-SPSA algorithm using " \
                f"simulation:{self.simulation_env_config.name}"
        for seed in self.experiment_config.random_seeds:
            exp_result.all_metrics[seed] = {}
            exp_result.all_metrics[seed][agents_constants.T_SPSA.THETAS] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_REWARD] = []
            exp_result.all_metrics[seed][agents_constants.T_SPSA.THRESHOLDS] = []

        # Initialize training job
        if self.training_job is None:
            self.training_job = TrainingJobConfig(
                simulation_env_name=self.simulation_env_config.name, experiment_config=self.experiment_config,
                progress_percentage=0, pid=pid, experiment_result=exp_result,
                emulation_env_name=self.emulation_env_config.name, simulation_traces=[],
                num_cached_traces=agents_constants.COMMON.NUM_CACHED_SIMULATION_TRACES,
                log_file_path=Logger.__call__().get_log_file_path(), descr=descr)
            training_job_id = MetastoreFacade.save_training_job(training_job=self.training_job)
            self.training_job.id = training_job_id
        else:
            self.training_job.pid = pid
            self.training_job.progress_percentage = 0
            self.training_job.experiment_result = exp_result
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
        exp_execution_id = MetastoreFacade.save_experiment_execution(self.exp_execution)
        self.exp_execution.id = exp_execution_id

        config = self.simulation_env_config.simulation_env_input_config
        if self.env is None:
            self.env = gym.make(self.simulation_env_config.gym_env_name, config=config)
        for seed in self.experiment_config.random_seeds:
            ExperimentUtil.set_seed(seed)
            exp_result = self.spsa(exp_result=exp_result, seed=seed, training_job=self.training_job,
                                   random_seeds=self.experiment_config.random_seeds)
            self.training_job = MetastoreFacade.get_training_job_config(id=training_job_id)

            # Save latest trace
            MetastoreFacade.save_simulation_trace(self.env.get_traces()[-1])
            self.env.reset_traces()

        # Calculate average and std metrics
        exp_result.avg_metrics = {}
        exp_result.std_metrics = {}
        for metric in exp_result.all_metrics[self.experiment_config.random_seeds[0]].keys():
            running_avg = 100
            confidence = 0.95
            value_vectors = []
            for seed in self.experiment_config.random_seeds:
                value_vectors.append(exp_result.all_metrics[seed][metric])

            avg_metrics = []
            std_metrics = []
            for i in range(len(value_vectors[0])):
                seed_values = []
                for seed_idx in range(len(self.experiment_config.random_seeds)):
                    seed_values.append(value_vectors[seed_idx][i])
                avg_metrics.append(ExperimentUtil.mean_confidence_interval(data=seed_values, confidence=confidence)[0])
                std_metrics.append(ExperimentUtil.mean_confidence_interval(data=seed_values, confidence=confidence)[1])
            exp_result.avg_metrics[metric] = avg_metrics
            exp_result.std_metrics[metric] = std_metrics

        traces = self.env.get_traces()
        if len(traces) > 0:
            MetastoreFacade.save_simulation_trace(traces[-1])
        ts = time.time()
        self.exp_execution.timestamp = ts
        self.exp_execution.result = exp_result
        MetastoreFacade.update_experiment_execution(experiment_execution=self.exp_execution,
                                                    id=self.exp_execution.id)
        return self.exp_execution

    def hparam_names(self) -> List[str]:
        """
        :return: a list with the hyperparameter names
        """
        return [agents_constants.T_SPSA.a, agents_constants.T_SPSA.c, agents_constants.T_SPSA.LAMBDA,
                agents_constants.T_SPSA.A, agents_constants.T_SPSA.EPSILON, agents_constants.T_SPSA.N,
                agents_constants.T_SPSA.L, agents_constants.T_SPSA.THETA1, agents_constants.COMMON.EVAL_BATCH_SIZE]

    def spsa(self, exp_result: ExperimentResult, seed: int,
             training_job: TrainingJobConfig, random_seeds: List[int]) -> ExperimentResult:
        """
        Runs the SPSA algorithm

        :param exp_result: the experiment result object to store the result
        :param seed: the seed
        :param training_job: the training job config
        :param random_seeds: list of seeds
        :return: the updated experiment result and the trained policy
        """
        L = self.experiment_config.hparams[agents_constants.T_SPSA.L].value
        if agents_constants.T_SPSA.THETA1 in self.experiment_config.hparams:
            theta = self.experiment_config.hparams[agents_constants.T_SPSA.THETA1].value
        else:
            theta = TSPSAAgent.initial_theta(L=L)

        # Initial eval
        policy = TSPSAPolicy(theta=theta, simulation_name=self.simulation_env_config.name,
                             states=self.simulation_env_config.state_space_config.states,
                             player_type=self.experiment_config.player_type, L=L,
                             actions=self.simulation_env_config.joint_action_space_config.action_spaces[
                                 self.experiment_config.player_idx].actions,
                             experiment_config=self.experiment_config, avg_R=-1)
        avg_metrics = self.eval_theta(policy=policy)
        J = round(avg_metrics[agents_constants.T_SPSA.R], 3)
        policy.avg_R=J
        exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_REWARD].append(J)
        exp_result.all_metrics[seed][agents_constants.T_SPSA.THETAS].append(TSPSAAgent.round_vec(theta))

        # Iterations
        N = self.experiment_config.hparams[agents_constants.T_SPSA.N].value
        a = self.experiment_config.hparams[agents_constants.T_SPSA.a].value
        c = self.experiment_config.hparams[agents_constants.T_SPSA.c].value
        A = self.experiment_config.hparams[agents_constants.T_SPSA.A].value
        lamb = self.experiment_config.hparams[agents_constants.T_SPSA.LAMBDA].value
        epsilon = self.experiment_config.hparams[agents_constants.T_SPSA.EPSILON].value
        Logger.__call__().get_logger().info(f"[T-SPSA] i: {0}, J:{J}, "
                                            f"thresholds:{policy.thresholds()}")
        for i in range(N):
            # Step sizes and perturbation size
            ak = self.standard_ak(a=a, A=A, epsilon=epsilon, k=i)
            ck = self.standard_ck(c=c, lamb=lamb, k=i)
            deltak = self.standard_deltak(dimension=len(theta), k=i)

            # Get estimated gradient
            gk = self.estimate_gk(theta=theta, deltak=deltak, ck=ck, L=L)

            # Adjust theta using SA
            theta = [t + ak * gkk for t, gkk in zip(theta, gk)]

            # Constrain (Theorem 1.A, Hammar Stadler 2021)
            for l in range(L - 1):
                theta[l] = max(theta[l], theta[l + 1])

            # Evaluate new theta
            policy = TSPSAPolicy(theta=theta, simulation_name=self.simulation_env_config.name,
                                 states=self.simulation_env_config.state_space_config.states,
                                 player_type=self.experiment_config.player_type, L=L,
                                 actions=self.simulation_env_config.joint_action_space_config.action_spaces[
                                     self.experiment_config.player_idx].actions,
                                 experiment_config=self.experiment_config, avg_R=-1)
            avg_metrics = self.eval_theta(policy=policy)
            J = round(avg_metrics[agents_constants.T_SPSA.R], 3)
            policy.avg_R = J

            # Record metrics
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_REWARD].append(J)
            exp_result.all_metrics[seed][agents_constants.T_SPSA.THETAS].append(TSPSAAgent.round_vec(theta))
            exp_result.all_metrics[seed][agents_constants.T_SPSA.THRESHOLDS].append(
                TSPSAAgent.round_vec(policy.thresholds()))

            if i % self.experiment_config.log_every == 0 and i > 0:
                Logger.__call__().get_logger().info(f"[T-SPSA] i: {i}, J:{J}, "
                                                    f"sigmoid(theta):{policy.thresholds()}")
                # Update training job
                total_iterations = len(random_seeds) * N
                iterations_done = (random_seeds.index(seed)) * N + i
                progress = round(iterations_done / total_iterations, 2)
                training_job.progress_percentage = progress
                training_job.experiment_result = exp_result
                training_job.simulation_traces.append(self.env.get_traces()[-1])
                if len(training_job.simulation_traces) > training_job.num_cached_traces:
                    training_job.simulation_traces = training_job.simulation_traces[1:]
                MetastoreFacade.update_training_job(training_job=training_job, id=training_job.id)

                # Update execution
                ts = time.time()
                self.exp_execution.timestamp = ts
                self.exp_execution.result = exp_result
                MetastoreFacade.update_experiment_execution(experiment_execution=self.exp_execution,
                                                            id=self.exp_execution.id)

        policy = TSPSAPolicy(theta=theta, simulation_name=self.simulation_env_config.name,
                             states=self.simulation_env_config.state_space_config.states,
                             player_type=self.experiment_config.player_type, L=L,
                             actions=self.simulation_env_config.joint_action_space_config.action_spaces[
                                 self.experiment_config.player_idx].actions,
                             experiment_config=self.experiment_config, avg_R=J)
        exp_result.policies[seed] = policy
        # Save policy
        MetastoreFacade.save_tspsa_policy(t_spsa_policy=policy)
        return exp_result

    def eval_theta(self, policy: TSPSAPolicy) -> Dict[str, Union[float, int]]:
        """
        Evaluates a given threshold policy by running monte-carlo simulations

        :param policy: the policy to evaluate
        :return: the average metrics of the evaluation
        """
        eval_batch_size = self.experiment_config.hparams[agents_constants.COMMON.EVAL_BATCH_SIZE].value
        metrics = {}
        for j in range(eval_batch_size):
            done = False
            o = self.env.reset()
            l = int(o[0])
            b1 = o[1]
            t = 1
            r = 0
            a = 0
            info = {}
            while not done:
                Logger.__call__().get_logger().debug(f"t:{t}, a: {a}, b1:{b1}, r:{r}, l:{l}, info:{info}")
                if self.experiment_config.player_type == PlayerType.ATTACKER:
                    a = policy.stage_policy(o=o)
                else:
                    a = policy.action(o=o)
                o, r, done, info = self.env.step(a)
                l = int(o[0])
                b1 = o[1]
                t += 1
            metrics = TSPSAAgent.update_metrics(metrics=metrics, info=info)
        avg_metrics = TSPSAAgent.compute_avg_metrics(metrics=metrics)
        return avg_metrics

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
    def standard_ak(a: int, A: int, epsilon: float, k: int) -> float:
        """
        Gets the step size for gradient ascent at iteration k

        :param a: a scalar hyperparameter
        :param A: a scalar hyperparameter
        :param epsilon: the epsilon scalar hyperparameter
        :param k: the iteration index
        :return: the step size a_k
        """
        return a / (k + 1 + A) ** epsilon

    @staticmethod
    def standard_ck(c: float, lamb: float, k: int) -> float:
        """
        Gets the step size of perturbations at iteration k

        :param c: a scalar hyperparameter
        :param lamb: (lambda) a scalar hyperparameter
        :param k: the iteration
        :return: the pertrubation step size
        """
        '''Create a generator for values of c_k in the standard form.'''
        return c / (k + 1) ** lamb

    @staticmethod
    def standard_deltak(dimension: int, k: int) -> List[float]:
        """
        Gets the perturbation direction at iteration k

        :param k: the iteration
        :param dimension: the dimension of the perturbation vector
        :return: delta_k the perturbation vector at iteration k
        """
        return [random.choice((-1, 1)) for _ in range(dimension)]

    @staticmethod
    def initial_theta(L: int) -> np.ndarray:
        """
        Initializes theta randomly

        :param L: the dimension of theta
        :return: the initialized theta vector
        """
        theta_1 = []
        for k in range(L):
            theta_1.append(np.random.uniform(-3, 3))
        theta_1 = np.array(theta_1)
        return theta_1

    def estimate_gk(self, theta: List[float], deltak: List[float], ck: float, L: int):
        """
        Estimate the gradient at iteration k of the T-SPSA algorithm

        :param theta: the current parameter vector
        :param deltak: the perturbation direction vector
        :param ck: the perturbation step size
        :param env: the env for evaluation
        :param L: the total number of stops for the defender
        :return: the estimated gradient
        """
        # Get the two perturbed values of theta
        # list comprehensions like this are quite nice
        ta = [t + ck * dk for t, dk in zip(theta, deltak)]
        tb = [t - ck * dk for t, dk in zip(theta, deltak)]

        # Calculate g_k(theta_k)
        avg_metrics = self.eval_theta(TSPSAPolicy(
            theta=ta, simulation_name=self.simulation_env_config.name,
            player_type=self.experiment_config.player_type,
            states=self.simulation_env_config.state_space_config.states, L=L,
            actions=self.simulation_env_config.joint_action_space_config.action_spaces[
                self.experiment_config.player_idx].actions, experiment_config=self.experiment_config, avg_R=-1))
        J_a = round(avg_metrics[agents_constants.T_SPSA.R], 3)
        avg_metrics = self.eval_theta(TSPSAPolicy(
            theta=tb, simulation_name=self.simulation_env_config.name,
            player_type=self.experiment_config.player_type,states=self.simulation_env_config.state_space_config.states,
            L=L, actions=self.simulation_env_config.joint_action_space_config.action_spaces[
                self.experiment_config.player_idx].actions, experiment_config=self.experiment_config, avg_R=-1))
        J_b = round(avg_metrics[agents_constants.T_SPSA.R], 3)
        gk = [(J_a - J_b) / (2 * ck * dk) for dk in deltak]

        return gk

    @staticmethod
    def round_vec(vec) -> List[float]:
        """
        Rounds a vector to 3 decimals

        :param vec: the vector to round
        :return: the rounded vector
        """
        return list(map(lambda x: round(x, 3), vec))
