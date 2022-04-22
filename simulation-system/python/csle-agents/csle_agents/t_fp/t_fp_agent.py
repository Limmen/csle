from typing import Union, List, Dict, Tuple, Callable, Optional
import time
import gym
import os
import math
import numpy as np
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.experiment_execution import ExperimentExecution
from csle_common.dao.training.experiment_result import ExperimentResult
from csle_common.dao.training.agent_type import AgentType
from csle_common.util.experiment_util import ExperimentUtil
from csle_common.dao.training.player_type import PlayerType
from csle_common.logging.log import Logger
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.jobs.training_job_config import TrainingJobConfig
from csle_common.dao.training.t_spsa_policy import TSPSAPolicy
from csle_agents.base.base_agent import BaseAgent
from csle_agents.t_spsa.t_spsa_agent import TSPSAAgent
import csle_agents.constants.constants as agents_constants


class TFPAgent(BaseAgent):
    """
    RL Agent implementing the T-FP algorithm from TODO
    """

    def __init__(self, defender_simulation_env_config: SimulationEnvConfig,
                 attacker_simulation_env_config: SimulationEnvConfig,
                 emulation_env_config: Union[None, EmulationEnvConfig], experiment_config: ExperimentConfig,
                 training_job: Optional[TrainingJobConfig] = None):
        """
        Initializes the T-FP agent

        :param attacker_simulation_env_config: the simulation env config of the attacker
        :param defender_simulation_env_config: the simulation env config of the defender
        :param emulation_env_config: the emulation env config
        :param experiment_config: the experiment config
        :param training_job: (optional) reuse an existing training job configuration
        """
        super().__init__(simulation_env_config=defender_simulation_env_config,
                         emulation_env_config=emulation_env_config,
                         experiment_config=experiment_config)
        assert experiment_config.agent_type == AgentType.T_FP
        self.defender_experiment_config = self.get_defender_experiment_config()
        self.attacker_experiment_config = self.get_attacker_experiment_config()
        self.attacker_simulation_env_config = attacker_simulation_env_config
        self.defender_simulation_env_config = defender_simulation_env_config
        self.training_job = training_job

    def train(self) -> ExperimentExecution:
        """
        Performs the policy training for the given random seeds using T-FP

        :return: the training metrics and the trained policies
        """
        pid = os.getpid()

        # Initialize result metrics
        exp_result = ExperimentResult()
        exp_result.plot_metrics.append(agents_constants.COMMON.AVERAGE_REWARD)
        for seed in self.experiment_config.random_seeds:
            exp_result.all_metrics[seed] = {}
            exp_result.all_metrics[seed][agents_constants.T_SPSA.THETAS] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.DEFENDER_AVERAGE_REWARD] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.ATTACKER_AVERAGE_REWARD] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.EXPLOITABILITY] = []
            exp_result.all_metrics[seed][agents_constants.T_FP.DEFENDER_THRESHOLDS] = []
            exp_result.all_metrics[seed][agents_constants.T_FP.ATTACKER_THRESHOLDS] = []

        if self.training_job is None:
            self.training_job = TrainingJobConfig(
                simulation_env_name=self.simulation_env_config.name, experiment_config=self.experiment_config,
                experiment_result=exp_result, progress_percentage=0, pid=pid,
                emulation_env_name=self.emulation_env_config.name, simulation_traces=[])
            training_job_id = MetastoreFacade.save_training_job(training_job=self.training_job)
            self.training_job.id = training_job_id
        else:
            self.training_job.pid = pid
            self.training_job.progress_percentage = 0
            self.training_job.experiment_result = exp_result
            MetastoreFacade.update_training_job(training_job=self.training_job, id=self.training_job.id)
        config = self.simulation_env_config.simulation_env_input_config
        env = gym.make(self.simulation_env_config.gym_env_name, config=config)
        for seed in self.experiment_config.random_seeds:
            ExperimentUtil.set_seed(seed)
            exp_result = self.t_fp(exp_result=exp_result, seed=seed, env=env, training_job=self.training_job,
                                   random_seeds=self.experiment_config.random_seeds)
            self.training_job = MetastoreFacade.get_training_job_config(id=self.training_job.id)

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

        ts = time.time()
        emulation_name = None
        if self.emulation_env_config is not None:
            emulation_name = self.emulation_env_config.name
        simulation_name = self.simulation_env_config.name
        descr = f"Training of policies with the T-SPSA algorithm using " \
                f"simulation:{self.simulation_env_config.name}"
        exp_execution = ExperimentExecution(result=exp_result, config=self.experiment_config, timestamp=ts,
                                            emulation_name=emulation_name, simulation_name=simulation_name,
                                            descr=descr)
        traces = env.get_traces()
        if len(traces) > 0:
            MetastoreFacade.save_simulation_trace(traces[-1])
        MetastoreFacade.remove_training_job(self.training_job)
        return exp_execution

    def t_fp(self, exp_result: ExperimentResult, seed: int, env: gym.Env,
             training_job: TrainingJobConfig, random_seeds: List[int]):

        # Initialize variables
        pi_2 = np.zeros((2, self.experiment_config.hparams[agents_constants.T_SPSA.L])).tolist()
        pi_1 = np.zeros((self.experiment_config.hparams[agents_constants.T_SPSA.L],)).tolist()
        initial_attacker_thresholds = [
            list(map(lambda x: round(TSPSAPolicy.sigmoid(x),3),
                     self.attacker_experiment_config.hparams[agents_constants.T_SPSA.THETA1].value))]
        initial_defender_thresholds = [
            list(map(lambda x: round(TSPSAPolicy.sigmoid(x),3),
                     self.defender_experiment_config.hparams[agents_constants.T_SPSA.THETA1].value))]
        pi_2 = TFPAgent.empirical_strategy_attacker(
            attacker_thresholds=initial_attacker_thresholds,
            pi_2=pi_2, L=self.attacker_experiment_config.hparams[agents_constants.T_SPSA.L].value)
        pi_1 = TFPAgent.empirical_strategy_defender(
            defender_thresholds=initial_defender_thresholds,
            pi_1=pi_1, L=self.attacker_experiment_config.hparams[agents_constants.T_SPSA.L].value)

        for i in range(self.experiment_config.hparams[agents_constants.T_FP.N_2].value):

            # Compute best responses
            attacker_thresholds, attacker_val = self.attacker_best_response(seed=seed, defender_strategy=None)
            defender_thresholds, defender_val = self.defender_best_response(seed=seed, attacker_strategy=None)

            # Update empirical strategies
            if attacker_val > -defender_val:
                pi_2 = self.empirical_strategy_attacker(
                    attacker_thresholds=[attacker_thresholds], pi_2=pi_2,
                    L=self.experiment_config.hparams[agents_constants.T_SPSA.L])
                val_attacker_exp= attacker_val
            else:
                val_attacker_exp = -defender_val
            if defender_val > -attacker_val:
                pi_1 = self.empirical_strategy_defender(
                    defender_thresholds=[defender_thresholds], pi_1=pi_1,
                    L=self.experiment_config.hparams[agents_constants.T_SPSA.L])
                val_defender_exp=defender_val
            else:
                val_defender_exp = -attacker_val

            # Compute exploitability
            exp = TFPAgent.exploitability(attacker_val=val_attacker_exp, defender_val=val_defender_exp)
            exp_result.all_metrics[seed][agents_constants.COMMON.EXPLOITABILITY].append(exp)

            # Logging the progress
            if i % self.experiment_config.log_every == 0 and i > 0:
                avg_exp = TFPAgent.running_average(
                    exp_result.all_metrics[seed][agents_constants.COMMON.EXPLOITABILITY], 50)
                Logger.__call__().get_logger().info(
                    f"[T-FP] i: {i}, Exploitability: {exp}, average exploitability: {avg_exp}"
                    f"Defender val:{defender_val}, Attacker val:{attacker_val}, "
                    f"defender thresholds:{defender_thresholds},"
                    f" attacker_thresholds: {attacker_thresholds}")

                # Update training job
                total_iterations = len(random_seeds) * self.experiment_config.hparams[agents_constants.T_FP.N_2].value
                iterations_done = (random_seeds.index(seed)) \
                                  * self.experiment_config.hparams[agents_constants.T_FP.N_2].value + i
                progress = round(iterations_done / total_iterations, 2)
                training_job.progress_percentage = progress
                MetastoreFacade.update_training_job(training_job=training_job, id=training_job.id)

    def defender_best_response(self, seed: int, attacker_strategy: Callable) -> Tuple[List, float]:
        self.defender_experiment_config.random_seeds = [seed]
        gym.make(self.simulation_env_config.gym_env_name,
                 config=self.defender_simulation_env_config.simulation_env_input_config,
                 attacker_strategy=attacker_strategy)
        agent = TSPSAAgent(emulation_env_config=self.emulation_env_config,
                           simulation_env_config=self.defender_simulation_env_config,
                           experiment_config=self.defender_experiment_config)
        experiment_execution = agent.train()
        policy :TSPSAPolicy = experiment_execution.result.policies[seed]
        thresholds = policy.thresholds()
        val = experiment_execution.result.avg_metrics[agents_constants.COMMON.AVERAGE_REWARD]
        return thresholds, val


    def attacker_best_response(self, seed: int, defender_strategy: Callable) -> Tuple[List, float]:
        self.attacker_experiment_config.random_seeds = [seed]
        gym.make(self.simulation_env_config.gym_env_name,
                 config=self.defender_simulation_env_config.simulation_env_input_config,
                 defender_strategy=defender_strategy)
        agent = TSPSAAgent(emulation_env_config=self.emulation_env_config,
                           simulation_env_config=self.attacker_simulation_env_config,
                           experiment_config=self.attacker_experiment_config)
        experiment_execution = agent.train()
        policy :TSPSAPolicy = experiment_execution.result.policies[seed]
        thresholds = policy.thresholds()
        val = experiment_execution.result.avg_metrics[agents_constants.COMMON.AVERAGE_REWARD]
        return thresholds, val

    def hparam_names(self) -> List[str]:
        """
        :return: a list with the hyperparameter names
        """
        return [agents_constants.T_SPSA.a, agents_constants.T_SPSA.c, agents_constants.T_SPSA.LAMBDA,
                agents_constants.T_SPSA.A, agents_constants.T_SPSA.EPSILON, agents_constants.T_SPSA.N,
                agents_constants.T_SPSA.L, agents_constants.T_SPSA.THETA1, agents_constants.COMMON.EVAL_BATCH_SIZE,
                agents_constants.T_FP.N_2]

    @staticmethod
    def exploitability(attacker_val: float, defender_val: float) -> float:
        """
        Computes the exploitability metric given the value of the attacker when following a best response
        against the current defender strategy and the value of the defender when following a best response against
        the current attacker strategy.

        :param attacker_val: the value of the attacker when following a best response against
                             the current defender strategy
        :param defender_val: the value of the defender when following a best response against the
                             current attacker strategy
        :return: the exploitability
        """
        return round(math.fabs(attacker_val + defender_val), 2)

    @staticmethod
    def empirical_strategy_attacker(pi_2: List[List[List[List[float]]]], attacker_thresholds: List[List[float]], L: int) \
            -> List[List[List[List[float]]]]:
        """
        Updates the attacker's empirical strategy

        :param pi_2: the current empirical strategy of the attacker
        :param L: the number of stop actions of the defender
        :param attacker_thresholds: the thresholds to add to the strategy
        :return: returns a SxLxA array with the updated empirical strategy of the attacker
        """
        for a_thresholds in attacker_thresholds:
            for s in range(2):
                for l in range(L):
                    if pi_2[s][l] == 0:
                        pi_2[s][l] = [[a_thresholds[s][l]], [1]]
                    else:
                        if a_thresholds[s][l] in pi_2[s][l][0]:
                            i = pi_2[s][l][0].index(a_thresholds[s][l])
                            pi_2[s][l][1][i] = pi_2[s][l][1][i] + 1
                        else:
                            pi_2[s][l][0].append(a_thresholds[s][l])
                            pi_2[s][l][1].append(1)
        return pi_2

    @staticmethod
    def empirical_strategy_defender(pi_1: List[List[List[float]]], defender_thresholds: List[List[float]],
                                    L: int) -> List[List[List[float]]]:
        """
        Updates teh defender's empirical strategy
        :param pi_1: the current empirical strategy of the defender
        :param defender_thresholds: the thresholds of the defender
        :param L: the number of stop actions of the defender
        :return: the updated empirical strategy of the defender (a LxA array
        """
        for defender_theta in defender_thresholds:
            for l in range(L):
                if pi_1[l] == 0:
                    pi_1[l] = [[defender_theta[l]], [1]]
                else:
                    if defender_theta[l] in pi_1[l][0]:
                        i = pi_1[l][0].index(defender_theta[l])
                        pi_1[l][1][i] = pi_1[l][1][i] + 1
                    else:
                        pi_1[l][0].append(defender_theta[l])
                        pi_1[l][1].append(1)
        return pi_1

    def get_defender_experiment_config(self) -> ExperimentConfig:
        """
        :return: the experiment configuration for learning a best response of the defender
        """
        return ExperimentConfig(
            output_dir=self.experiment_config.output_dir,
            title="Learning a best response of the defender as part of T-FP",
            random_seeds=[399, 98912,999,555], agent_type=AgentType.T_SPSA,
            log_every=10,
            hparams={
                agents_constants.T_SPSA.N: self.experiment_config.hparams[agents_constants.T_SPSA.N],
                agents_constants.T_SPSA.c: self.experiment_config.hparams[agents_constants.T_SPSA.c],
                agents_constants.T_SPSA.a: self.experiment_config.hparams[agents_constants.T_SPSA.a],
                agents_constants.T_SPSA.A: self.experiment_config.hparams[agents_constants.T_SPSA.A],
                agents_constants.T_SPSA.LAMBDA: self.experiment_config.hparams[agents_constants.T_SPSA.LAMBDA],
                agents_constants.T_SPSA.EPSILON: self.experiment_config.hparams[agents_constants.T_SPSA.EPSILON],
                agents_constants.T_SPSA.L: self.experiment_config.hparams[agents_constants.T_SPSA.L],
                agents_constants.COMMON.EVAL_BATCH_SIZE: self.experiment_config.hparams[
                    agents_constants.COMMON.EVAL_BATCH_SIZE],
                agents_constants.T_SPSA.THETA1: self.experiment_config.hparams[agents_constants.T_SPSA.THETA1]
            },
            player_type=PlayerType.DEFENDER, player_idx=0
        )

    def get_attacker_experiment_config(self) -> ExperimentConfig:
        """
        :return: the experiment configuration for learning a best response of the attacker
        """
        return ExperimentConfig(
            output_dir=self.experiment_config.output_dir,
            title="Learning a best response of the attacker as part of T-FP",
            random_seeds=[399, 98912,999,555], agent_type=AgentType.T_SPSA,
            log_every=10,
            hparams={
                agents_constants.T_SPSA.N: self.experiment_config.hparams[agents_constants.T_SPSA.N],
                agents_constants.T_SPSA.c: self.experiment_config.hparams[agents_constants.T_SPSA.c],
                agents_constants.T_SPSA.a: self.experiment_config.hparams[agents_constants.T_SPSA.a],
                agents_constants.T_SPSA.A: self.experiment_config.hparams[agents_constants.T_SPSA.A],
                agents_constants.T_SPSA.LAMBDA: self.experiment_config.hparams[agents_constants.T_SPSA.LAMBDA],
                agents_constants.T_SPSA.EPSILON: self.experiment_config.hparams[agents_constants.T_SPSA.EPSILON],
                agents_constants.T_SPSA.L: self.experiment_config.hparams[agents_constants.T_SPSA.L],
                agents_constants.COMMON.EVAL_BATCH_SIZE: self.experiment_config.hparams[
                    agents_constants.COMMON.EVAL_BATCH_SIZE],
                agents_constants.T_SPSA.THETA1: self.experiment_config.hparams[agents_constants.T_SPSA.THETA1]
            },
            player_type=PlayerType.ATTACKER, player_idx=1
        )

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

    @staticmethod
    def running_average(x: List[float], N: int) -> List[float]:
        """
        Calculates the running average of the last N elements of vector x

        :param x: the vector
        :param N: the number of elements to use for average calculation
        :return: the running average vector
        """
        if len(x) >= N:
            y = np.copy(x)
            y[N-1:] = np.convolve(x, np.ones((N, )) / N, mode='valid')
        else:
            N = len(x)
            y = np.copy(x)
            y[N-1:] = np.convolve(x, np.ones((N, )) / N, mode='valid')
        return y.tolist()


    @staticmethod
    def threshold_attacker_strategy(pi_2, o: List, pi_1_S):
        s = o[2]
        b1 = o[1]
        l = int(o[0])

        thresholds = pi_2[s][l][0]
        counts = pi_2[s][l][1]

        mixture_weights = np.array(counts) / sum(pi_2[s][l][1])
        random_threshold = np.random.choice(thresholds, p=mixture_weights)
        if s == 1:
            a = 0
            if pi_1_S >= random_threshold:
                a = 1
        else:
            a = 1
            if pi_1_S >= random_threshold:
                a = 0
        return a
