from typing import Union, List, Optional, Any, Dict, Tuple
import math
import time
import random
import gymnasium as gym
import os
import numpy as np
import numpy.typing as npt
import gym_csle_stopping_game.constants.constants as env_constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.experiment_execution import ExperimentExecution
from csle_common.dao.training.experiment_result import ExperimentResult
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.player_type import PlayerType
from csle_common.util.experiment_util import ExperimentUtil
from csle_common.logging.log import Logger
from csle_common.dao.training.multi_threshold_stopping_policy import MultiThresholdStoppingPolicy
from csle_common.dao.training.linear_threshold_stopping_policy import LinearThresholdStoppingPolicy
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.jobs.training_job_config import TrainingJobConfig
from csle_common.util.general_util import GeneralUtil
from csle_common.dao.simulation_config.base_env import BaseEnv
from csle_common.dao.training.policy_type import PolicyType
from csle_agents.agents.base.base_agent import BaseAgent
from csle_agents.common.objective_type import ObjectiveType
import csle_agents.constants.constants as agents_constants


class ParticleSwarmAgent(BaseAgent):
    """
    Particle Swarm Search Agent
    """

    def __init__(self, simulation_env_config: SimulationEnvConfig,
                 emulation_env_config: Union[None, EmulationEnvConfig],
                 experiment_config: ExperimentConfig,
                 env: Optional[BaseEnv] = None, training_job: Optional[TrainingJobConfig] = None,
                 save_to_metastore: bool = True):
        """
        Initializes the Particle Swarm Agent

        :param simulation_env_config: the simulation env config
        :param emulation_env_config: the emulation env config
        :param experiment_config: the experiment config
        :param env: (optional) the gym environment to use for simulation
        :param training_job: (optional) a training job configuration
        :param save_to_metastore: boolean flag that can be set to avoid saving results and progress to the metastore
        """
        super().__init__(simulation_env_config=simulation_env_config, emulation_env_config=emulation_env_config,
                         experiment_config=experiment_config)
        assert experiment_config.agent_type == AgentType.PARTICLE_SWARM
        self.env = env
        self.training_job = training_job
        self.save_to_metastore = save_to_metastore

    def train(self) -> ExperimentExecution:
        """
        Performs the policy training for the given random seeds using particle swarm

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
        for l in range(1, self.experiment_config.hparams[agents_constants.PARTICLE_SWARM.L].value + 1):
            exp_result.plot_metrics.append(env_constants.ENV_METRICS.STOP + f"_{l}")
            exp_result.plot_metrics.append(env_constants.ENV_METRICS.STOP + f"_running_average_{l}")

        descr = f"Training of policies with the random search algorithm using " \
                f"simulation:{self.simulation_env_config.name}"
        for seed in self.experiment_config.random_seeds:
            exp_result.all_metrics[seed] = {}
            exp_result.all_metrics[seed][agents_constants.PARTICLE_SWARM.THETAS] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.PARTICLE_SWARM.THRESHOLDS] = []
            if self.experiment_config.player_type == PlayerType.DEFENDER:
                for l in range(1, self.experiment_config.hparams[agents_constants.PARTICLE_SWARM.L].value + 1):
                    exp_result.all_metrics[seed][
                        agents_constants.PARTICLE_SWARM.STOP_DISTRIBUTION_DEFENDER + f"_l={l}"] = []
            else:
                for s in self.simulation_env_config.state_space_config.states:
                    for l in range(1, self.experiment_config.hparams[agents_constants.PARTICLE_SWARM.L].value + 1):
                        exp_result.all_metrics[seed][agents_constants.PARTICLE_SWARM.STOP_DISTRIBUTION_ATTACKER
                                                     + f"_l={l}_s={s.id}"] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_START] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_LENGTH] = []
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_START] = []
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_LENGTH] = []
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.TIME_HORIZON] = []
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN] = []
            exp_result.all_metrics[seed][
                env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN] = []
            for l in range(1, self.experiment_config.hparams[agents_constants.PARTICLE_SWARM.L].value + 1):
                exp_result.all_metrics[seed][env_constants.ENV_METRICS.STOP + f"_{l}"] = []
                exp_result.all_metrics[seed][env_constants.ENV_METRICS.STOP + f"_running_average_{l}"] = []

        # Initialize training job
        if self.training_job is None:
            emulation_name = ""
            if self.emulation_env_config is not None:
                emulation_name = self.emulation_env_config.name
            self.training_job = TrainingJobConfig(
                simulation_env_name=self.simulation_env_config.name, experiment_config=self.experiment_config,
                progress_percentage=0, pid=pid, experiment_result=exp_result,
                emulation_env_name=emulation_name, simulation_traces=[],
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
        emulation_name = ""
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
            exp_result = self.particle_swarm(exp_result=exp_result, seed=seed,
                                             random_seeds=self.experiment_config.random_seeds,
                                             training_job=self.training_job)

        # Calculate average and std metrics
        exp_result.avg_metrics = {}
        exp_result.std_metrics = {}
        for metric in exp_result.all_metrics[self.experiment_config.random_seeds[0]].keys():
            value_vectors = []
            for seed in self.experiment_config.random_seeds:
                value_vectors.append(exp_result.all_metrics[seed][metric])

            max_num_measurements = max(list(map(lambda x: len(x), value_vectors)))
            value_vectors = list(filter(lambda x: len(x) == max_num_measurements, value_vectors))

            avg_metrics = []
            std_metrics = []
            for i in range(len(value_vectors[0])):
                if type(value_vectors[0][0]) is int or type(value_vectors[0][0]) is float \
                        or type(value_vectors[0][0]) is np.int64 or type(value_vectors[0][0]) is np.float64:
                    seed_values = []
                    for seed_idx in range(len(value_vectors)):
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
        return [agents_constants.PARTICLE_SWARM.N, agents_constants.PARTICLE_SWARM.DELTA,
                agents_constants.PARTICLE_SWARM.L, agents_constants.PARTICLE_SWARM.THETA1,
                agents_constants.COMMON.EVAL_BATCH_SIZE,
                agents_constants.COMMON.CONFIDENCE_INTERVAL,
                agents_constants.COMMON.RUNNING_AVERAGE]

    def particle_swarm(self, exp_result: ExperimentResult, seed: int, random_seeds: List[int],
                       training_job: TrainingJobConfig):
        """
        Runs the particle swarm algorithm

        :param exp_result: the experiment result object to store the result
        :param seed: the seed
        :param training_job: the training job config
        :param random_seeds: list of seeds
        :return: the updated experiment result and the trained policy
        """
        S = self.experiment_config.hparams[agents_constants.PARTICLE_SWARM.S].value
        b_lo = self.experiment_config.hparams[agents_constants.PARTICLE_SWARM.B_LOW].value
        b_up = self.experiment_config.hparams[agents_constants.PARTICLE_SWARM.B_UP].value
        Phi_p = self.experiment_config.hparams[agents_constants.PARTICLE_SWARM.COGNITIVE_COEFFICIENT].value
        Phi_g = self.experiment_config.hparams[agents_constants.PARTICLE_SWARM.SOCIAL_COEFFICIENT].value
        w = self.experiment_config.hparams[agents_constants.PARTICLE_SWARM.INERTIA_WEIGHT].value
        L = self.experiment_config.hparams[agents_constants.PARTICLE_SWARM.L].value
        objective_type_param = self.experiment_config.hparams[agents_constants.PARTICLE_SWARM.OBJECTIVE_TYPE].value
        if agents_constants.PARTICLE_SWARM.THETA1 in self.experiment_config.hparams:
            thetas = self.experiment_config.hparams[agents_constants.PARTICLE_SWARM.THETA1].value
            print("thetas = ", thetas)
        else:
            if self.experiment_config.player_type == PlayerType.DEFENDER:
                P, thetas = ParticleSwarmAgent.initial_theta(L=L, S=S, b_lo=b_lo, b_up=b_up)
            else:
                P, thetas = ParticleSwarmAgent.initial_theta(L=2 * L, S=S, b_lo=b_lo, b_up=b_up)
        theta = list(thetas[:, random.randint(0, S - 1)])
        policy = self.get_policy(theta=theta, L=L)
        avg_metrics = self.eval_theta(
            policy=policy, max_steps=self.experiment_config.hparams[agents_constants.COMMON.MAX_ENV_STEPS].value)
        J = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
        policy.avg_R = J
        exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN].append(J)
        exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN].append(J)
        exp_result.all_metrics[seed][agents_constants.PARTICLE_SWARM.THETAS].append(
            ParticleSwarmAgent.round_vec(theta))

        g = [random.uniform(b_lo, b_up) for i in range(L)]

        # Hyperparameters
        N = self.experiment_config.hparams[agents_constants.PARTICLE_SWARM.N].value

        for i in range(S):
            policy = self.get_policy(theta=list(P[:, i]), L=L)
            avg_metrics = self.eval_theta(
                policy=policy, max_steps=self.experiment_config.hparams[agents_constants.COMMON.MAX_ENV_STEPS].value)
            J_p = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
            if objective_type_param == ObjectiveType.MAX:
                J_p = -J_p

            policy = self.get_policy(theta=list(g), L=L)
            avg_metrics = self.eval_theta(
                policy=policy, max_steps=self.experiment_config.hparams[agents_constants.COMMON.MAX_ENV_STEPS].value)
            J_g = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
            if objective_type_param == ObjectiveType.MAX:
                J_g = -J_g
            policy.avg_R = J_g
            if J_p < J_g:
                g = list(P[:, i])
        V = ParticleSwarmAgent.initial_velocity(L, S, b_lo, b_up)
        iter_variable = 0
        while iter_variable <= N:
            for j in range(S):
                for l in range(L):
                    r_p = random.random()
                    r_g = random.random()
                    V[l, j] = w * V[l, j] + Phi_p * r_p * (P[l, j] - thetas[l, j]) + Phi_g * r_g * (g[l] - thetas[l, j])
                thetas[:, j] += V[:, j]
                policy = self.get_policy(theta=list(thetas[:, j]), L=L)
                avg_metrics = self.eval_theta(
                    policy=policy, max_steps=self.experiment_config.hparams[
                        agents_constants.COMMON.MAX_ENV_STEPS].value)
                J_t = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
                if objective_type_param == ObjectiveType.MAX:
                    J_t = -J_t
                policy = self.get_policy(theta=list(P[:, j]), L=L)
                avg_metrics = self.eval_theta(
                    policy=policy, max_steps=self.experiment_config.hparams[
                        agents_constants.COMMON.MAX_ENV_STEPS].value)
                J_p = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
                if objective_type_param == ObjectiveType.MAX:
                    J_p = -J_p
                if J_t < J_p:
                    P[:, j] = thetas[:, j]
                    policy = self.get_policy(theta=list(P[:, j]), L=L)
                    avg_metrics = self.eval_theta(policy=policy,
                                                  max_steps=self.experiment_config.hparams[
                                                      agents_constants.COMMON.MAX_ENV_STEPS].value)
                    J_p = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
                    if objective_type_param == ObjectiveType.MAX:
                        J_p = -J_p
                    policy = self.get_policy(theta=list(g), L=L)
                    avg_metrics = self.eval_theta(policy=policy,
                                                  max_steps=self.experiment_config.hparams[
                                                      agents_constants.COMMON.MAX_ENV_STEPS].value)
                    J_g = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
                    if objective_type_param == ObjectiveType.MAX:
                        J_g = -J_g
                    J = J_g
                    if J_p < J_g:
                        g = list(P[:, j])
                        policy = self.get_policy(theta=list(g), L=L)
                        avg_metrics = self.eval_theta(policy=policy,
                                                      max_steps=self.experiment_config.hparams[
                                                          agents_constants.COMMON.MAX_ENV_STEPS].value)
                        J_g = round(avg_metrics[env_constants.ENV_METRICS.RETURN], 3)
                        J = J_g
            theta = g
            iter_variable += 1
            if objective_type_param == ObjectiveType.MAX:
                J = -J
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN].append(J)
            running_avg_J = ExperimentUtil.running_average(
                exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN],
                self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value)
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN].append(J)
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN].append(running_avg_J)

            # Log thresholds
            exp_result.all_metrics[seed][agents_constants.PARTICLE_SWARM.THETAS].append(
                ParticleSwarmAgent.round_vec(theta))
            exp_result.all_metrics[seed][agents_constants.PARTICLE_SWARM.THRESHOLDS].append(
                ParticleSwarmAgent.round_vec(policy.thresholds()))

            # Log stop distribution
            for k, v in policy.stop_distributions().items():
                exp_result.all_metrics[seed][k].append(v)

            # Log intrusion lengths
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_LENGTH].append(
                round(avg_metrics[env_constants.ENV_METRICS.INTRUSION_LENGTH], 3))
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_LENGTH].append(
                ExperimentUtil.running_average(
                    exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_LENGTH],
                    self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))

            # Log stopping times
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_START].append(
                round(avg_metrics[env_constants.ENV_METRICS.INTRUSION_START], 3))
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_START].append(
                ExperimentUtil.running_average(
                    exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_START],
                    self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.TIME_HORIZON].append(
                round(avg_metrics[env_constants.ENV_METRICS.TIME_HORIZON], 3))
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON].append(
                ExperimentUtil.running_average(
                    exp_result.all_metrics[seed][env_constants.ENV_METRICS.TIME_HORIZON],
                    self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))
            for l in range(1, self.experiment_config.hparams[agents_constants.PARTICLE_SWARM.L].value + 1):
                exp_result.plot_metrics.append(env_constants.ENV_METRICS.STOP + f"_{l}")
                exp_result.all_metrics[seed][env_constants.ENV_METRICS.STOP + f"_{l}"].append(
                    round(avg_metrics[env_constants.ENV_METRICS.STOP + f"_{l}"], 3))
                exp_result.all_metrics[seed][env_constants.ENV_METRICS.STOP + f"_running_average_{l}"].append(
                    ExperimentUtil.running_average(
                        exp_result.all_metrics[seed][env_constants.ENV_METRICS.STOP + f"_{l}"],
                        self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))

            # Log baseline returns
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN].append(
                round(avg_metrics[env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN], 3))
            exp_result.all_metrics[seed][
                env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN].append(
                round(avg_metrics[env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN], 3))

            if iter_variable % self.experiment_config.log_every == 0 and iter_variable > 0:
                # Update training job
                total_iterations = len(random_seeds) * N
                iterations_done = (random_seeds.index(seed)) * N + iter_variable
                progress = round(iterations_done / total_iterations, 2)
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
                    f"[PARTICLE-SWARM] i: {iter_variable}, J:{J}, "
                    f"J_avg_{self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value}:"
                    f"{running_avg_J}, "
                    f"opt_J:{exp_result.all_metrics[seed][env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN][-1]}, "
                    f"int_len:{exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_LENGTH][-1]}, "
                    f"sigmoid(theta):{policy.thresholds()}, progress: {round(progress * 100, 2)}%, "
                    f"stop distributions:{policy.stop_distributions()}")
        policy = self.get_policy(theta=list(theta), L=L)
        exp_result.policies[seed] = policy
        # Save policy
        if self.save_to_metastore:
            MetastoreFacade.save_multi_threshold_stopping_policy(multi_threshold_stopping_policy=policy)
        return exp_result

    def eval_theta(self, policy: Union[MultiThresholdStoppingPolicy, LinearThresholdStoppingPolicy],
                   max_steps: int = 200) -> Dict[str, Union[float, int]]:
        """
        Evaluates a given threshold policy by running monte-carlo simulations

        :param policy: the policy to evaluate
        :return: the average metrics of the evaluation
        """
        if self.env is None:
            raise ValueError("Need to specify an environment to run policy evaluation")
        eval_batch_size = self.experiment_config.hparams[agents_constants.COMMON.EVAL_BATCH_SIZE].value
        metrics: Dict[str, Any] = {}
        for j in range(eval_batch_size):
            done = False
            o, _ = self.env.reset()
            l = int(o[0])
            b1 = o[1]
            t = 1
            r = 0
            a = 0
            info: Dict[str, Any] = {}
            while not done and t <= max_steps:
                Logger.__call__().get_logger().debug(f"t:{t}, a: {a}, b1:{b1}, r:{r}, l:{l}, info:{info}")
                if self.experiment_config.player_type == PlayerType.ATTACKER:
                    policy.opponent_strategy = self.env.unwrapped.static_defender_strategy
                    a = policy.action(o=o)
                else:
                    a = policy.action(o=o)
                o, r, done, _, info = self.env.step(a)
                l = int(o[0])
                b1 = o[1]
                t += 1
            metrics = ParticleSwarmAgent.update_metrics(metrics=metrics, info=info)
        avg_metrics = ParticleSwarmAgent.compute_avg_metrics(metrics=metrics)
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
    def initial_theta(L: int, S: int, b_lo: Union[int, float],
                      b_up: Union[int, float]) -> Tuple[npt.NDArray[Any], npt.NDArray[Any]]:
        """
        Initializes particle positions (thetas) randomly

        :param L: the dimension of theta
        :param S: the number of particles in the swarm
        :param b_lo: lower boundary of randomization
        :param b_up: upper boundary of randomization
        :return: the initialized theta vector
        """
        X = [[random.uniform(b_lo, b_up) for i in range(S)] for i in range(L)]
        thetas = np.array(X)
        P = np.zeros(np.shape(thetas))
        for k in range(thetas.shape[0]):
            for l in range(thetas.shape[1]):
                P[k, l] = thetas[k, l]

        return P, thetas

    @staticmethod
    def initial_velocity(L: int, S: int, b_lo: Union[int, float], b_up: Union[int, float]) -> npt.NDArray[Any]:
        """
        Initializes the voleicities amongst each particle in the swarm
        :param L: the dimension
        :param S: the number of particles in the swarm
        :param b_lo: lower boundary od randomization
        :param b_up: upper boundary of randomization
        """
        V = [[random.uniform(-abs(b_up - b_lo), abs(b_up - b_lo)) for i in range(S)] for k in range(L)]
        V_np = np.array(V)
        return V_np

    def get_policy(self, theta: List[float], L: int) \
            -> Union[MultiThresholdStoppingPolicy, LinearThresholdStoppingPolicy]:
        """
        Gets the policy of a given parameter vector

        :param theta: the parameter vector
        :param L: the number of parameters
        :return: the policy
        """
        if self.experiment_config.hparams[agents_constants.PARTICLE_SWARM.POLICY_TYPE].value \
                == PolicyType.MULTI_THRESHOLD.value:
            policy = MultiThresholdStoppingPolicy(
                theta=list(theta), simulation_name=self.simulation_env_config.name,
                states=self.simulation_env_config.state_space_config.states,
                player_type=self.experiment_config.player_type, L=L,
                actions=self.simulation_env_config.joint_action_space_config.action_spaces[
                    self.experiment_config.player_idx].actions, experiment_config=self.experiment_config, avg_R=-1,
                agent_type=AgentType.PARTICLE_SWARM)
        else:
            policy = LinearThresholdStoppingPolicy(
                theta=list(theta), simulation_name=self.simulation_env_config.name,
                states=self.simulation_env_config.state_space_config.states,
                player_type=self.experiment_config.player_type, L=L,
                actions=self.simulation_env_config.joint_action_space_config.action_spaces[
                    self.experiment_config.player_idx].actions, experiment_config=self.experiment_config, avg_R=-1,
                agent_type=AgentType.PARTICLE_SWARM)
        return policy

    @staticmethod
    def round_vec(vec) -> List[float]:
        """
        Rounds a vector to 3 decimals

        :param vec: the vector to round
        :return: the rounded vector
        """
        return list(map(lambda x: round(x, 3), vec))

    def random_position(self, L: int, S, b_lo: float, b_up: float) -> npt.NDArray[Any]:
        """
        Utility function to get a random position

        :param L: the number of parameters
        :param S: number of points
        :param b_lo: lower bound
        :param b_up: upper bound
        :return: an array with the random coordinates
        """
        X = [[random.uniform(b_lo, b_up) for _ in range(S)] for i in range(L)]
        return np.array(X)
