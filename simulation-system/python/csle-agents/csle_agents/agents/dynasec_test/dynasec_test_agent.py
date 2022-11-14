import random
from typing import List, Optional, Dict, Tuple
import time
import gym
import os
import sys
import math
from scipy.stats import norm
import numpy as np
from scipy.stats import binom
import threading
import gym_csle_stopping_game.constants.constants as env_constants
from csle_system_identification.emulator import Emulator
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_config.emulation_execution import EmulationExecution
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.experiment_execution import ExperimentExecution
from csle_common.dao.training.experiment_result import ExperimentResult
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.util.experiment_util import ExperimentUtil
from csle_common.dao.jobs.data_collection_job_config import DataCollectionJobConfig
from csle_common.dao.emulation_config.emulation_trace import EmulationTrace
from csle_common.logging.log import Logger
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.jobs.training_job_config import TrainingJobConfig
from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
from csle_agents.agents.base.base_agent import BaseAgent
from csle_common.dao.emulation_action.attacker.emulation_attacker_stopping_actions \
    import EmulationAttackerStoppingActions
from csle_common.dao.emulation_action.defender.emulation_defender_stopping_actions \
    import EmulationDefenderStoppingActions
import csle_agents.constants.constants as agents_constants
from csle_system_identification.expectation_maximization.expectation_maximization_algorithm \
    import ExpectationMaximizationAlgorithm
from csle_common.dao.system_identification.gaussian_mixture_system_model import GaussianMixtureSystemModel
from csle_agents.agents.t_spsa.t_spsa_agent import TSPSAAgent
from csle_agents.agents.ppo.ppo_agent import PPOAgent
import csle_system_identification.constants.constants as system_identification_constants
from csle_common.dao.system_identification.system_identification_config import SystemIdentificationConfig
from csle_common.dao.training.policy import Policy
from csle_common.util.read_emulation_statistics_util import ReadEmulationStatisticsUtil
from csle_common.dao.emulation_config.static_emulation_attacker_type import StaticEmulationAttackerType
from csle_common.dao.emulation_config.emulation_statistics_windowed import EmulationStatisticsWindowed
from scipy.stats import poisson
from scipy.stats import expon


class ClientThread(threading.Thread):
    """
    Thread representing a client
    """

    def __init__(self, service_time: float) -> None:
        """
        Initializes the client

        :param service_time: the service time of the client
        """
        threading.Thread.__init__(self)
        self.service_time = service_time

    def run(self) -> None:
        """
        The main function of the client

        :return: None
        """
        time.sleep(self.service_time)

def observation_tensor(n, intrusion_mean, no_intrusion_mean):
    """
    :return: a |A1|x|A2|x|S|x|O| tensor
    """
    intrusion_dist = []
    no_intrusion_dist = []
    intrusion_rv = norm(loc=intrusion_mean, scale=2000)
    no_intrusion_rv = norm(loc=no_intrusion_mean, scale=800)
    for i in range(n):
        intrusion_dist.append(intrusion_rv.pdf(i))
        no_intrusion_dist.append(no_intrusion_rv.pdf(i))
    intrusion_dist = list(np.array(intrusion_dist)*(1/sum(intrusion_dist)))
    no_intrusion_dist = list(np.array(no_intrusion_dist)*(1/sum(no_intrusion_dist)))
    terminal_dist = np.zeros(n)
    terminal_dist[-1] = 1
    Z = np.array(
        [
            [
                [
                    no_intrusion_dist,
                    intrusion_dist,
                    terminal_dist
                ],
                [
                    no_intrusion_dist,
                    intrusion_dist,
                    terminal_dist
                ],
            ],
            [
                [
                    no_intrusion_dist,
                    intrusion_dist,
                    terminal_dist
                ],
                [
                    no_intrusion_dist,
                    intrusion_dist,
                    terminal_dist
                ],
            ]
        ]
    )
    return Z


class ArrivalThread(threading.Thread):
    """
    Thread that generates client arrivals (starts client threads according to a Poisson process)
    """

    def __init__(self, time_step_len_seconds: float, lamb: int = 10, mu: float = 0.1,
                 exp_result: ExperimentResult = None, seed = 399):
        """
        Initializes the arrival thread

        :param time_step_len_seconds: the number of seconds that one time-unit of the Poisson process corresponds to
        :param lamb: the lambda parameter of the Poisson process for arrivals
        :param mu: the mu parameter of the service times of the clients
        """
        threading.Thread.__init__(self)
        self.time_step_len_seconds = time_step_len_seconds
        self.client_threads = []
        self.t = 0
        self.lamb = lamb
        self.mu = mu
        self.stopped = False
        self.exp_result = exp_result
        self.seed = seed
        self.intrusion_alerts = 2000
        self.no_intrusion_alerts = 0
        self.baseline_intrusion_alerts = None
        self.baseline_no_intrusion_alerts = None
        self.Z = observation_tensor(n=6000, intrusion_mean=self.intrusion_alerts,
                                              no_intrusion_mean=self.intrusion_alerts)
        self.baseline_Z = observation_tensor(n=6000, intrusion_mean=self.intrusion_alerts,
                                    no_intrusion_mean=self.intrusion_alerts)

    def sinus_modulated_poisson_rate(self, t):
        return 60 + 160*math.sin(2*math.pi*t*(1/100))

    def run(self) -> None:
        """
        Runs the arrival generator, generates new clients dynamically according to a Poisson process

        :return: None
        """
        while not self.stopped:
            new_client_threads = []
            for ct in self.client_threads:
                if ct.is_alive():
                    new_client_threads.append(ct)
            self.client_threads = new_client_threads
            self.t += 1
            rate = self.sinus_modulated_poisson_rate(self.t)
            new_clients = poisson.rvs(rate, size=1)[0]
            for nc in range(new_clients):
                service_time = expon.rvs(scale=1/self.mu, loc=0, size=1)[0]
                thread = ClientThread(service_time=service_time)
                thread.start()
                self.client_threads.append(thread)
            no_intrusion_alerts = 40
            for i in range(len(self.client_threads)):
                no_intrusion_alerts += random.randint(25, 55)
            self.no_intrusion_alerts = self.no_intrusion_alerts
            self.intrusion_alerts = self.intrusion_alerts + self.no_intrusion_alerts + random.randint(50, 750)
            if self.baseline_intrusion_alerts is None:
                self.baseline_intrusion_alerts = self.intrusion_alerts
                self.baseline_no_intrusion_alerts = self.no_intrusion_alerts
            self.exp_result.all_metrics[self.seed][agents_constants.DYNASEC.NUM_CLIENTS].append(len(self.client_threads))
            self.exp_result.all_metrics[self.seed][agents_constants.DYNASEC.CLIENTS_ARRIVAL_RATE].append(rate)
            self.exp_result.all_metrics[self.seed][agents_constants.DYNASEC.INTRUSION_ALERTS_MEAN].append(self.intrusion_alerts)
            self.exp_result.all_metrics[self.seed][agents_constants.DYNASEC.NO_INTRUSION_ALERTS_MEAN].append(self.no_intrusion_alerts)
            self.exp_result.all_metrics[self.seed][agents_constants.DYNASEC.INTRUSION_ALERTS_MEAN_BASELINE].append(self.baseline_intrusion_alerts)
            self.exp_result.all_metrics[self.seed][agents_constants.DYNASEC.NO_INTRUSION_ALERTS_MEAN_BASELINE].append(self.baseline_no_intrusion_alerts)
            self.Z = observation_tensor(n=6000, intrusion_mean=self.intrusion_alerts,
                                        no_intrusion_mean=self.intrusion_alerts)
            self.baseline_Z = observation_tensor(n=6000, intrusion_mean=self.baseline_intrusion_alerts,
                                                 no_intrusion_mean=self.baseline_intrusion_alerts)
            time.sleep(self.time_step_len_seconds)
            print(f"clients:{len(self.client_threads)}, rate: {rate}, intrusion_alerts_mean: {self.intrusion_alerts}, "
                  f"no_intrusion_alerts_mean: {self.no_intrusion_alerts}, "
                  f"baseline_intrusion_alerts_mean: {self.baseline_intrusion_alerts},"
                  f"baseline_no_intrusion_alerts_mean: {self.baseline_no_intrusion_alerts}")



class TrainingThread(threading.Thread):

    def __init__(self, sleep_time: float, exp_result: ExperimentResult, arrival_thread: ArrivalThread,
                 experiment_config: ExperimentConfig, emulation_env_config: EmulationEnvConfig,
                 simulation_env_config: SimulationEnvConfig, env, seed):
        threading.Thread.__init__(self)
        self.sleep_time = sleep_time
        self.exp_result = exp_result
        self.arrival_thread = arrival_thread
        self.stopped = False
        self.experiment_config = experiment_config
        self.emulation_env_config = emulation_env_config
        self.simulation_env_config = simulation_env_config
        self.baseline_policy = None
        self.policy = None
        self.seed = seed
        self.env = env

    def run(self) -> None:
        """
        Runs the arrival generator, generates new clients dynamically according to a Poisson process

        :return: None
        """
        time.sleep(self.sleep_time)
        self.simulation_env_config.simulation_env_input_config.stopping_game_config.Z = self.arrival_thread.baseline_Z
        self.agent = PPOAgent(emulation_env_config=self.emulation_env_config,
                                simulation_env_config=self.simulation_env_config,
                                experiment_config=self.experiment_config)
        print("starting training")
        self.experiment_execution = self.agent.train()
        MetastoreFacade.save_experiment_execution(self.experiment_execution)
        self.baseline_policy = self.experiment_execution.result.policies.values()[0]
        self.policy = self.baseline_policy.copy()
        avg_return_baseline = self.eval_policy(policy=self.baseline_policy, Z=self.arrival_thread.baseline_Z,
                                               sample_Z=self.arrival_thread.baseline_Z, env=self.env, batch=100)
        self.exp_result.all_metrics[self.seed][agents_constants.COMMON.BASELINE_PREFIX +
                                     agents_constants.COMMON.AVERAGE_RETURN].append(avg_return_baseline)
        self.exp_result.all_metrics[self.seed][agents_constants.COMMON.BASELINE_PREFIX +
                                               agents_constants.COMMON.RUNNING_AVERAGE_RETURN].append(avg_return_baseline)
        self.exp_result.all_metrics[self.seed][agents_constants.COMMON.AVERAGE_RETURN].append(avg_return_baseline)
        self.exp_result.all_metrics[self.seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN].append(avg_return_baseline)
        i =1

        while not self.stopped:
            time.sleep(self.sleep_time)
            self.simulation_env_config.simulation_env_input_config.stopping_game_config.Z = self.arrival_thread.Z
            self.agent = PPOAgent(emulation_env_config=self.emulation_env_config,
                                  simulation_env_config=self.simulation_env_config,
                                  experiment_config=self.experiment_config)
            self.experiment_execution = self.agent.train()
            MetastoreFacade.save_experiment_execution(self.experiment_execution)
            self.policy = self.experiment_execution.result.policies.values()[0]
            avg_return_baseline = self.eval_policy(policy=self.baseline_policy, Z=self.arrival_thread.baseline_Z,
                                                   sample_Z=self.arrival_thread.baseline_Z, env=self.env, batch=100)
            avg_return = self.eval_policy(policy=self.policy, Z=self.arrival_thread.Z,
                                                   sample_Z=self.arrival_thread.Z, env=self.env, batch=100)
            self.exp_result.all_metrics[self.seed][agents_constants.COMMON.BASELINE_PREFIX +
                                                   agents_constants.COMMON.AVERAGE_RETURN].append(avg_return_baseline)
            self.exp_result.all_metrics[self.seed][agents_constants.COMMON.BASELINE_PREFIX +
                                                   agents_constants.COMMON.RUNNING_AVERAGE_RETURN].append(
                ExperimentUtil.running_average(avg_return_baseline,
                                               self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))
            self.exp_result.all_metrics[self.seed][agents_constants.COMMON.AVERAGE_RETURN].append(avg_return)
            self.exp_result.all_metrics[self.seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN].append(
                ExperimentUtil.running_average(avg_return,
                    self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))
            i+=1

            Logger.__call__().get_logger().info(
                f"[DynaSec] i: {i}, "                                                
                f"J_eval:{self.exp_result.all_metrics[self.seed][agents_constants.COMMON.EVAL_PREFIX + agents_constants.COMMON.AVERAGE_RETURN][-1]}, "
                f"J_eval_avg_{self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value}:"
                f"{self.exp_result.all_metrics[self.seed][agents_constants.COMMON.EVAL_PREFIX + agents_constants.COMMON.RUNNING_AVERAGE_RETURN][-1]}, "
                f"J_baseline:{self.exp_result.all_metrics[self.seed][agents_constants.COMMON.BASELINE_PREFIX + agents_constants.COMMON.AVERAGE_RETURN][-1]}, "
                f"J_baseline_avg_{self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value}:"
                f"{self.exp_result.all_metrics[self.seed][agents_constants.COMMON.BASELINE_PREFIX + agents_constants.COMMON.RUNNING_AVERAGE_RETURN][-1]}, "
                f"")


    def eval_policy(self, policy, Z, sample_Z, batch, env):
        returns = []
        env.stopping_game_config.Z = Z
        for i in range(batch):
            done = False
            R = 0
            o=env.reset()
            while not done:
                a = policy.action(o=o)
                o, r, done, info = env.step_test(a1=a, sample_Z=sample_Z)
                R+=r
            returns.append(R)
        return float(np.mean(returns))


class DynaSecTestAgent(BaseAgent):
    """
    DynaSec
    """

    def __init__(self, simulation_env_config: SimulationEnvConfig,
                 emulation_env_config: EmulationEnvConfig,
                 experiment_config: ExperimentConfig, env: Optional[gym.Env] = None,
                 training_job: Optional[TrainingJobConfig] = None, save_to_metastore : bool = True):
        """
        Initializes the DynaSec agent

        :param simulation_env_config: the simulation env config
        :param emulation_env_config: the emulation env config
        :param system_identification_config: the system identification config
        :param attacker_sequence: attacker sequence to emulate intrusions
        :param defender_sequence: defender sequence to emulate defense
        :param experiment_config: the experiment config
        :param env: (optional) the gym environment to use for simulation
        :param training_job: (optional) a training job configuration
        :param save_to_metastore: boolean flag that can be set to avoid saving results and progress to the metastore
        """
        super().__init__(simulation_env_config=simulation_env_config,
                         emulation_env_config=emulation_env_config,
                         experiment_config=experiment_config)
        assert experiment_config.agent_type == AgentType.DYNA_SEC_TEST
        self.env = env
        self.training_job = training_job
        self.save_to_metastore = save_to_metastore

    def get_ppo_experiment_config(self) -> ExperimentConfig:
        """
        :return: the experiment configuration for SPSA training
        """
        hparams= {
            agents_constants.COMMON.NUM_NEURONS_PER_HIDDEN_LAYER: self.experiment_config.hparams[agents_constants.COMMON.NUM_NEURONS_PER_HIDDEN_LAYER],
            agents_constants.COMMON.NUM_HIDDEN_LAYERS: self.experiment_config.hparams[agents_constants.COMMON.NUM_HIDDEN_LAYERS],
            agents_constants.PPO.STEPS_BETWEEN_UPDATES: self.experiment_config.hparams[agents_constants.PPO.STEPS_BETWEEN_UPDATES],
            agents_constants.COMMON.LEARNING_RATE: self.experiment_config.hparams[agents_constants.COMMON.LEARNING_RATE],
            agents_constants.COMMON.BATCH_SIZE: self.experiment_config.hparams[agents_constants.COMMON.BATCH_SIZE],
            agents_constants.COMMON.GAMMA: self.experiment_config.hparams[agents_constants.COMMON.GAMMA],
            agents_constants.PPO.GAE_LAMBDA: self.experiment_config.hparams[agents_constants.PPO.GAE_LAMBDA],
            agents_constants.PPO.CLIP_RANGE: self.experiment_config.hparams[
                agents_constants.PPO.CLIP_RANGE],
            agents_constants.PPO.CLIP_RANGE_VF: self.experiment_config.hparams[
                agents_constants.PPO.CLIP_RANGE_VF],
            agents_constants.PPO.ENT_COEF: self.experiment_config.hparams[
                agents_constants.PPO.ENT_COEF],
            agents_constants.PPO.VF_COEF: self.experiment_config.hparams[
                agents_constants.PPO.VF_COEF],
            agents_constants.COMMON.NUM_PARALLEL_ENVS: self.experiment_config.hparams[
                agents_constants.COMMON.NUM_PARALLEL_ENVS],
            agents_constants.PPO.MAX_GRAD_NORM: self.experiment_config.hparams[
                agents_constants.PPO.MAX_GRAD_NORM],
            agents_constants.COMMON.NUM_TRAINING_TIMESTEPS: self.experiment_config.hparams[
                agents_constants.COMMON.NUM_TRAINING_TIMESTEPS],
            agents_constants.PPO.TARGET_KL: self.experiment_config.hparams[
                agents_constants.PPO.TARGET_KL],
            agents_constants.COMMON.EVAL_EVERY: self.experiment_config.hparams[
                agents_constants.COMMON.EVAL_EVERY],
            agents_constants.COMMON.EVAL_BATCH_SIZE: self.experiment_config.hparams[
                agents_constants.COMMON.EVAL_BATCH_SIZE],
            agents_constants.COMMON.DEVICE: self.experiment_config.hparams[
                agents_constants.COMMON.DEVICE],
            agents_constants.COMMON.SAVE_EVERY: self.experiment_config.hparams[
                agents_constants.COMMON.SAVE_EVERY],
            agents_constants.COMMON.RUNNING_AVERAGE: self.experiment_config.hparams[
                agents_constants.COMMON.RUNNING_AVERAGE],
            agents_constants.COMMON.L: self.experiment_config.hparams[agents_constants.COMMON.L],
            agents_constants.COMMON.MAX_ENV_STEPS: self.experiment_config.hparams[agents_constants.COMMON.MAX_ENV_STEPS],
            agents_constants.COMMON.CONFIDENCE_INTERVAL: self.experiment_config.hparams[agents_constants.COMMON.CONFIDENCE_INTERVAL]
        }
        return ExperimentConfig(
            output_dir=str(self.experiment_config.output_dir),
            title="Learning a policy through PPO",
            random_seeds=self.experiment_config.random_seeds, agent_type=AgentType.PPO,
            log_every=self.experiment_config.log_every,
            hparams=hparams,
            player_type=self.experiment_config.player_type, player_idx=self.experiment_config.player_idx
        )

    def train(self) -> ExperimentExecution:
        """
        Performs the policy training for the given random seeds using T-SPSA

        :return: the training metrics and the trained policies
        """
        pid = os.getpid()

        # Initialize metrics
        exp_result = ExperimentResult()
        exp_result.plot_metrics.append(agents_constants.DYNASEC.NUM_CLIENTS)
        exp_result.plot_metrics.append(agents_constants.DYNASEC.INTRUSION_ALERTS_MEAN)
        exp_result.plot_metrics.append(agents_constants.DYNASEC.NO_INTRUSION_ALERTS_MEAN)
        exp_result.plot_metrics.append(agents_constants.DYNASEC.INTRUSION_ALERTS_MEAN_BASELINE)
        exp_result.plot_metrics.append(agents_constants.DYNASEC.NO_INTRUSION_ALERTS_MEAN_BASELINE)
        exp_result.plot_metrics.append(agents_constants.DYNASEC.CLIENTS_ARRIVAL_RATE)
        exp_result.plot_metrics.append(agents_constants.COMMON.AVERAGE_RETURN)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_RETURN)

        exp_result.plot_metrics.append(agents_constants.COMMON.BASELINE_PREFIX +
                                       agents_constants.COMMON.AVERAGE_RETURN)
        exp_result.plot_metrics.append(agents_constants.COMMON.BASELINE_PREFIX +
                                       agents_constants.COMMON.RUNNING_AVERAGE_RETURN)

        descr = f"Training of policies with the DynaSecTest algorithm using " \
                f"simulation:{self.simulation_env_config.name}"

        for seed in self.experiment_config.random_seeds:
            exp_result.all_metrics[seed] = {}
            exp_result.all_metrics[seed][agents_constants.DYNASEC.NUM_CLIENTS] = []
            exp_result.all_metrics[seed][agents_constants.DYNASEC.INTRUSION_ALERTS_MEAN] = []
            exp_result.all_metrics[seed][agents_constants.DYNASEC.NO_INTRUSION_ALERTS_MEAN] = []
            exp_result.all_metrics[seed][agents_constants.DYNASEC.INTRUSION_ALERTS_MEAN_BASELINE] = []
            exp_result.all_metrics[seed][agents_constants.DYNASEC.NO_INTRUSION_ALERTS_MEAN_BASELINE] = []
            exp_result.all_metrics[seed][agents_constants.DYNASEC.CLIENTS_ARRIVAL_RATE] = []
            exp_result.all_metrics[seed][agents_constants.DYNASEC.STATIC_ATTACKER_TYPE] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                         agents_constants.COMMON.AVERAGE_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.BASELINE_PREFIX +
                                         agents_constants.COMMON.RUNNING_AVERAGE_RETURN] = []

        # Initialize training job
        if self.training_job is None:
            self.training_job = TrainingJobConfig(
                simulation_env_name=self.simulation_env_config.name, experiment_config=self.experiment_config,
                progress_percentage=0, pid=pid, experiment_result=exp_result,
                emulation_env_name=self.emulation_env_config.name, simulation_traces=[],
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
        self.exp_execution = ExperimentExecution(result=exp_result, config=self.experiment_config, timestamp=ts,
                                            emulation_name=emulation_name, simulation_name=simulation_name,
                                            descr=descr, log_file_path=self.training_job.log_file_path)
        if self.save_to_metastore:
            exp_execution_id = MetastoreFacade.save_experiment_execution(self.exp_execution)
            self.exp_execution.id = exp_execution_id

        config = self.simulation_env_config.simulation_env_input_config
        if self.env is None:
            self.env = gym.make(self.simulation_env_config.gym_env_name, config=config)
        seed = self.experiment_config.random_seeds[0]
        ExperimentUtil.set_seed(seed)

        # Hyperparameters
        ppo_experiment_config = self.get_ppo_experiment_config()
        training_epochs = self.experiment_config.hparams[agents_constants.DYNASEC.TRAINING_EPOCHS].value
        sleep_time = self.experiment_config.hparams[agents_constants.DYNASEC.SLEEP_TIME].value
        max_steps = self.experiment_config.hparams[agents_constants.COMMON.MAX_ENV_STEPS].value

        # Start client arrival processes
        a_t = ArrivalThread(time_step_len_seconds=30, lamb=20, mu=1/(4*30), exp_result=exp_result, seed=seed)
        a_t.start()

        # Start training thread
        p_t = TrainingThread(sleep_time=sleep_time, exp_result=exp_result, arrival_thread=a_t,
                             experiment_config=ppo_experiment_config,
                             emulation_env_config=self.emulation_env_config,
                             simulation_env_config=self.simulation_env_config, env=self.env, seed=seed)
        p_t.start()

        while True:
            time.sleep(sleep_time)

            # Update training job
            total_iterations = training_epochs
            iterations_done = 1
            progress = round(iterations_done / total_iterations, 2)
            self.training_job.progress_percentage = progress
            self.training_job.experiment_result = a_t.exp_result
            if len(self.env.get_traces()) > 0:
                self.training_job.simulation_traces.append(self.env.get_traces()[-1])
            if len(self.training_job.simulation_traces) > self.training_job.num_cached_traces:
                self.training_job.simulation_traces = self.training_job.simulation_traces[1:]
            if self.save_to_metastore:
                MetastoreFacade.update_training_job(training_job=self.training_job, id=self.training_job.id)

            # Update execution
            ts = time.time()
            self.exp_execution.timestamp = ts
            self.exp_execution.result = a_t.exp_result
            if self.save_to_metastore:
                MetastoreFacade.update_experiment_execution(experiment_execution=self.exp_execution,
                                                                id=self.exp_execution.id)

        return self.exp_execution

    @staticmethod
    def mean(prob_vector):
        m = 0
        for i in range(len(prob_vector)):
            m += prob_vector[i]*i
        return m

    def hparam_names(self) -> List[str]:
        """
        :return: a list with the hyperparameter names
        """
        return [agents_constants.COMMON.NUM_NEURONS_PER_HIDDEN_LAYER, agents_constants.COMMON.NUM_HIDDEN_LAYERS,
                agents_constants.PPO.STEPS_BETWEEN_UPDATES,
                agents_constants.COMMON.LEARNING_RATE, agents_constants.COMMON.BATCH_SIZE,
                agents_constants.COMMON.GAMMA, agents_constants.PPO.GAE_LAMBDA, agents_constants.PPO.CLIP_RANGE,
                agents_constants.PPO.CLIP_RANGE_VF, agents_constants.PPO.ENT_COEF,
                agents_constants.PPO.VF_COEF, agents_constants.PPO.MAX_GRAD_NORM, agents_constants.PPO.TARGET_KL,
                agents_constants.COMMON.NUM_TRAINING_TIMESTEPS, agents_constants.COMMON.EVAL_EVERY,
                agents_constants.COMMON.EVAL_BATCH_SIZE, agents_constants.COMMON.DEVICE,
                agents_constants.COMMON.SAVE_EVERY, agents_constants.COMMON.CONFIDENCE_INTERVAL,
                agents_constants.COMMON.RUNNING_AVERAGE,
                system_identification_constants.SYSTEM_IDENTIFICATION.CONDITIONAL_DISTRIBUTIONS,
                system_identification_constants.EXPECTATION_MAXIMIZATION.NUM_MIXTURES_PER_CONDITIONAL,
                agents_constants.DYNASEC.TRAINING_EPOCHS, agents_constants.DYNASEC.SLEEP_TIME,
                agents_constants.DYNASEC.INTRUSION_START_P,
                agents_constants.DYNASEC.EMULATION_TRACES_TO_SAVE_W_DATA_COLLECTION_JOB,
                agents_constants.DYNASEC.EMULATION_MONITOR_SLEEP_TIME,
                agents_constants.DYNASEC.REPLAY_WINDOW_SIZE
                ]
