from typing import Union, List, Dict, Tuple, Optional, Any
import time
import gymnasium as gym
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
from csle_common.dao.training.mixed_ppo_policy import MixedPPOPolicy
from csle_common.dao.training.mixed_linear_tabular import MixedLinearTabularPolicy
from csle_common.dao.training.ppo_policy import PPOPolicy
from csle_common.dao.training.linear_threshold_stopping_policy import LinearThresholdStoppingPolicy
from csle_common.dao.training.tabular_policy import TabularPolicy
from csle_common.dao.training.linear_tabular_policy import LinearTabularPolicy
from csle_agents.agents.ppo.ppo_agent import PPOAgent
from csle_agents.agents.differential_evolution.differential_evolution_agent import DifferentialEvolutionAgent
from csle_common.dao.training.policy import Policy
from csle_common.dao.simulation_config.base_env import BaseEnv
import csle_common.constants.constants as constants
from csle_common.util.general_util import GeneralUtil
from csle_agents.agents.base.base_agent import BaseAgent
import csle_agents.constants.constants as agents_constants
import gym_csle_stopping_game.constants.constants as env_constants
from gym_csle_intrusion_response_game.util.intrusion_response_game_util import IntrusionResponseGameUtil
from csle_agents.agents.vi.vi_agent import VIAgent


def reduce_T(T, strategy):
    """
    Reduces the transition tensor based on a given strategy

    :param T: the tensor to reduce
    :param strategy: the strategy to use for the reduction
    :return: the reduced transition tensor
    """
    attacker_state = 2
    reduced_T = np.zeros((T.shape[0], T.shape[2], T.shape[3]))
    for i in range(T.shape[0]):
        for j in range(T.shape[2]):
            for k in range(T.shape[3]):
                prob = 0
                for a2 in range(T.shape[1]):
                    prob += strategy[attacker_state][a2] * T[i][a2][j][k]
                reduced_T[i][j][k] = prob
    return reduced_T


def reduce_R(R, strategy):
    """
    Reduces the reward tensor based on a given strategy

    :param R: the reward tensor to reduce
    :param strategy: the strategy to use for the reduction
    :return: the reduced reward tensor
    """
    attacker_state = 2
    reduced_R = np.zeros((R.shape[0], R.shape[2]))
    for i in range(R.shape[0]):
        for j in range(R.shape[2]):
            r = 0
            for a2 in range(R.shape[1]):
                r += strategy[attacker_state][a2] * R[i][a2][j]
            reduced_R[i][j] = r
    return reduced_R


class DFSPLocalAgent(BaseAgent):
    """
    RL Agent implementing the local DFSP algorithm
    """

    def __init__(self, defender_simulation_env_config: SimulationEnvConfig,
                 attacker_simulation_env_config: SimulationEnvConfig,
                 emulation_env_config: Union[None, EmulationEnvConfig], ppo_experiment_config: ExperimentConfig,
                 de_experiment_config: ExperimentConfig, vi_experiment_config: ExperimentConfig,
                 training_job: Optional[TrainingJobConfig] = None):
        """
        Initializes the local DFSP agent

        :param attacker_simulation_env_config: the simulation env config of the attacker
        :param defender_simulation_env_config: the simulation env config of the defender
        :param emulation_env_config: the emulation env config
        :param attacker_experiment_config: the experiment config
        :param training_job: (optional) reuse an existing training job configuration
        """
        super().__init__(simulation_env_config=defender_simulation_env_config,
                         emulation_env_config=emulation_env_config,
                         experiment_config=ppo_experiment_config)
        self.root_output_dir = str(self.experiment_config.output_dir)
        self.ppo_experiment_config = ppo_experiment_config
        self.de_experiment_config = de_experiment_config
        self.vi_experiment_config = vi_experiment_config
        self.attacker_simulation_env_config = attacker_simulation_env_config
        self.defender_simulation_env_config = defender_simulation_env_config
        self.training_job = training_job

    def train(self) -> ExperimentExecution:
        """
        Performs the policy training for the given random seeds using the local DFSP algorithm

        :return: the training metrics and the trained policies
        """
        pid = os.getpid()

        # Initialize result metrics
        exp_result = ExperimentResult()

        # Define which metrics to plot in the UI
        exp_result.plot_metrics.append(agents_constants.COMMON.EXPLOITABILITY)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_EXPLOITABILITY)
        exp_result.plot_metrics.append(agents_constants.COMMON.AVERAGE_ATTACKER_RETURN)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_ATTACKER_RETURN)
        exp_result.plot_metrics.append(agents_constants.LOCAL_DFSP.RUNNING_AVERAGE_BEST_RESPONSE_ATTACKER_RETURN)
        exp_result.plot_metrics.append(agents_constants.COMMON.AVERAGE_DEFENDER_RETURN)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_DEFENDER_RETURN)
        exp_result.plot_metrics.append(agents_constants.LOCAL_DFSP.RUNNING_AVERAGE_BEST_RESPONSE_DEFENDER_RETURN)
        exp_result.plot_metrics.append(env_constants.ENV_METRICS.INTRUSION_LENGTH)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_LENGTH)
        exp_result.plot_metrics.append(env_constants.ENV_METRICS.INTRUSION_START)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_START)
        exp_result.plot_metrics.append(env_constants.ENV_METRICS.TIME_HORIZON)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON)
        exp_result.plot_metrics.append(env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN)
        descr = f"Approximating a Nash equilibrium with the local DFSP algorithm using " \
                f"simulations: {self.defender_simulation_env_config.name} " \
                f"and {self.attacker_simulation_env_config.name}"
        for seed in self.experiment_config.random_seeds:
            exp_result.all_metrics[seed] = {}
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_DEFENDER_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_DEFENDER_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_ATTACKER_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_ATTACKER_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.LOCAL_DFSP.AVERAGE_BEST_RESPONSE_DEFENDER_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.LOCAL_DFSP.RUNNING_AVERAGE_BEST_RESPONSE_DEFENDER_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.LOCAL_DFSP.AVERAGE_BEST_RESPONSE_ATTACKER_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.LOCAL_DFSP.RUNNING_AVERAGE_BEST_RESPONSE_ATTACKER_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.EXPLOITABILITY] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_EXPLOITABILITY] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_START] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_LENGTH] = []
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_START] = []
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_LENGTH] = []
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.TIME_HORIZON] = []
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN] = []

        if self.training_job is None:
            emulation_name = ""
            if self.emulation_env_config is not None:
                emulation_name = self.emulation_env_config.name
            self.training_job = TrainingJobConfig(
                simulation_env_name=self.simulation_env_config.name, experiment_config=self.experiment_config,
                experiment_result=exp_result, progress_percentage=0, pid=pid,
                emulation_env_name=emulation_name, simulation_traces=[],
                num_cached_traces=agents_constants.COMMON.NUM_CACHED_SIMULATION_TRACES,
                log_file_path=Logger.__call__().get_log_file_path(), descr=descr,
                physical_host_ip=GeneralUtil.get_host_ip())
            training_job_id = MetastoreFacade.save_training_job(training_job=self.training_job)
            self.training_job.id = training_job_id
        else:
            self.training_job.pid = pid
            self.training_job.progress_percentage = 0
            self.training_job.experiment_result = exp_result
            MetastoreFacade.update_training_job(training_job=self.training_job, id=self.training_job.id)
        config = self.simulation_env_config.simulation_env_input_config
        env: BaseEnv = gym.make(self.simulation_env_config.gym_env_name, config=config)
        for seed in self.experiment_config.random_seeds:
            ExperimentUtil.set_seed(seed)
            exp_result = self.local_dfsp(exp_result=exp_result, seed=seed, env=env, training_job=self.training_job,
                                         random_seeds=self.experiment_config.random_seeds)
            self.training_job = MetastoreFacade.get_training_job_config(id=self.training_job.id)

        # Calculate average and std metrics
        exp_result.avg_metrics = {}
        exp_result.std_metrics = {}
        for metric in exp_result.all_metrics[self.experiment_config.random_seeds[0]].keys():
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
        emulation_name = ""
        if self.emulation_env_config is not None:
            emulation_name = self.emulation_env_config.name
        simulation_name = self.simulation_env_config.name
        exp_execution = ExperimentExecution(result=exp_result, config=self.experiment_config, timestamp=ts,
                                            emulation_name=emulation_name, simulation_name=simulation_name,
                                            descr=descr, log_file_path=self.training_job.log_file_path)
        traces = env.get_traces()
        if len(traces) > 0:
            MetastoreFacade.save_simulation_trace(traces[-1])
        MetastoreFacade.remove_training_job(self.training_job)
        return exp_execution

    def local_dfsp(self, exp_result: ExperimentResult, seed: int, env: BaseEnv,
                   training_job: TrainingJobConfig, random_seeds: List[int]) -> ExperimentResult:
        """
        Implements the logic of the local DFSP algorithm

        :param exp_result: the experiment result
        :param seed: the random seed of the experiment
        :param env: the environment for the experiment
        :param training_job: the training job for the experiment
        :param random_seeds: the random seeds for the experiment
        :return: None
        """
        # Initialize policies
        defender_strategy = MixedLinearTabularPolicy(
            simulation_name=self.defender_simulation_env_config.name,
            states=self.defender_simulation_env_config.state_space_config.states,
            player_type=PlayerType.DEFENDER,
            actions=self.defender_simulation_env_config.joint_action_space_config.action_spaces[
                self.de_experiment_config.player_idx].actions,
            experiment_config=self.de_experiment_config, avg_R=-1)
        defender_strategy.states = \
            self.defender_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.S_D
        defender_strategy.actions = \
            self.defender_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.A1
        attacker_strategy = MixedPPOPolicy(
            simulation_name=self.attacker_simulation_env_config.name,
            states=self.attacker_simulation_env_config.state_space_config.states,
            player_type=PlayerType.ATTACKER,
            actions=self.attacker_simulation_env_config.joint_action_space_config.action_spaces[
                self.ppo_experiment_config.player_idx].actions,
            experiment_config=self.ppo_experiment_config, avg_R=-1)
        attacker_strategy.states = \
            self.attacker_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.S_A
        attacker_strategy.actions = \
            self.attacker_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.A2

        for i in range(self.experiment_config.hparams[agents_constants.LOCAL_DFSP.N_2].value):

            # Compute best responses
            br_seed = np.random.randint(0, 100)
            attacker_br, attacker_val = self.attacker_best_response(
                seed=br_seed, defender_strategy=defender_strategy, attacker_strategy=attacker_strategy)
            defender_br, defender_val = self.defender_best_response(
                seed=br_seed, attacker_strategy=attacker_strategy, defender_strategy=defender_strategy)

            # Update strategies
            defender_br.states = \
                self.defender_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.S_D
            defender_br.actions = \
                self.defender_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.A1
            attacker_br.states = \
                self.attacker_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.S_A
            attacker_br.actions = \
                self.attacker_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.A2

            # Update empirical strategies
            attacker_strategy.ppo_policies.append(attacker_br)
            defender_strategy.linear_tabular_policies.append(defender_br)

            # Evaluate best response strategies against empirical strategies
            attacker_metrics = self.evaluate_attacker_policy(
                defender_strategy=self.attacker_simulation_env_config.simulation_env_input_config.defender_strategy,
                attacker_strategy=attacker_br)
            defender_metrics = self.evaluate_attacker_policy(
                attacker_strategy=self.defender_simulation_env_config.simulation_env_input_config.attacker_strategy,
                defender_strategy=defender_br)

            # Evaluate empirical against empirical
            strategy_profile_metrics = self.evaluate_strategy_profile(
                defender_strategy=defender_strategy, attacker_strategy=attacker_strategy)

            # Update envs for the next BR iteration
            self.attacker_simulation_env_config.simulation_env_input_config.defender_strategy = defender_strategy
            self.attacker_simulation_env_config.simulation_env_input_config.attacker_strategy = attacker_strategy
            self.defender_simulation_env_config.simulation_env_input_config.defender_strategy = defender_strategy
            self.defender_simulation_env_config.simulation_env_input_config.attacker_strategy = attacker_strategy

            # Compute exploitability
            attacker_val = round(attacker_metrics[env_constants.ENV_METRICS.RETURN], 3)
            defender_val = -round(defender_metrics[env_constants.ENV_METRICS.RETURN], 3)
            attacker_val = max(attacker_val, -defender_val)
            defender_val = max(defender_val, -attacker_val)
            val = -round(strategy_profile_metrics[env_constants.ENV_METRICS.RETURN], 3)
            val_attacker_exp = attacker_val
            val_defender_exp = defender_val

            # Don't log the first iteration which is just initializing the policies
            if i == 0:
                continue

            # Log rewards
            exp_result.all_metrics[seed][agents_constants.LOCAL_DFSP.AVERAGE_BEST_RESPONSE_ATTACKER_RETURN].append(
                val_attacker_exp)
            exp_result.all_metrics[seed][agents_constants.LOCAL_DFSP.AVERAGE_BEST_RESPONSE_DEFENDER_RETURN].append(
                val_defender_exp)
            exp_result.all_metrics[seed][
                agents_constants.LOCAL_DFSP.RUNNING_AVERAGE_BEST_RESPONSE_ATTACKER_RETURN].append(
                ExperimentUtil.running_average(
                    exp_result.all_metrics[seed][agents_constants.LOCAL_DFSP.AVERAGE_BEST_RESPONSE_ATTACKER_RETURN],
                    self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))
            exp_result.all_metrics[seed][
                agents_constants.LOCAL_DFSP.RUNNING_AVERAGE_BEST_RESPONSE_DEFENDER_RETURN].append(
                ExperimentUtil.running_average(
                    exp_result.all_metrics[seed][agents_constants.LOCAL_DFSP.AVERAGE_BEST_RESPONSE_DEFENDER_RETURN],
                    self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))

            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_ATTACKER_RETURN].append(val)
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_DEFENDER_RETURN].append(-val)
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_ATTACKER_RETURN].append(
                ExperimentUtil.running_average(
                    exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_ATTACKER_RETURN],
                    self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_DEFENDER_RETURN].append(
                ExperimentUtil.running_average(
                    exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_DEFENDER_RETURN],
                    self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))

            exp_result.all_metrics[seed][env_constants.ENV_METRICS.TIME_HORIZON].append(
                round(strategy_profile_metrics[env_constants.ENV_METRICS.TIME_HORIZON], 3))
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON].append(
                ExperimentUtil.running_average(
                    exp_result.all_metrics[seed][env_constants.ENV_METRICS.TIME_HORIZON],
                    self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))

            # Log baseline returns
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN].append(
                round(strategy_profile_metrics[env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN], 3))

            # Compute and log exploitability
            exp = DFSPLocalAgent.exploitability(attacker_val=val_attacker_exp, defender_val=val_defender_exp)
            exp_result.all_metrics[seed][agents_constants.COMMON.EXPLOITABILITY].append(exp)
            running_avg_exp = ExperimentUtil.running_average(
                exp_result.all_metrics[seed][agents_constants.COMMON.EXPLOITABILITY],
                self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value)
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_EXPLOITABILITY].append(running_avg_exp)

            # Logging the progress
            if i % self.experiment_config.log_every == 0:
                Logger.__call__().get_logger().info(
                    f"[Local DFSP] i: {i}, Exp: {exp}, "
                    f"Exp_avg_{self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value}: "
                    f"{running_avg_exp}, game_val: {val} "
                    f"opt_val:{exp_result.all_metrics[seed][env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN][-1]},"
                    f" Defender val:{defender_val}, Attacker val:{attacker_val}")

                # Update training job
                total_iterations = len(random_seeds) * self.experiment_config.hparams[
                    agents_constants.LOCAL_DFSP.N_2].value
                iterations_done = ((random_seeds.index(seed)) *
                                   self.experiment_config.hparams[agents_constants.LOCAL_DFSP.N_2].value + i)
                progress = round(iterations_done / total_iterations, 2)
                training_job.progress_percentage = progress
                MetastoreFacade.update_training_job(training_job=training_job, id=training_job.id)
        return exp_result

    def evaluate_defender_policy(self, defender_strategy: LinearTabularPolicy,
                                 attacker_strategy: MixedPPOPolicy) -> Dict[str, Union[float, int]]:
        """
        Monte-Carlo evaluation of the game value of a given defender policy against the average attacker strategy

        :param defender_thresholds: the defender strategy to evaluate
        :param attacker_strategy: the average attacker strategy
        :return: the average reward
        """
        attacker_strategy.states = \
            self.attacker_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.S_A
        attacker_strategy.actions = \
            self.attacker_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.A2
        defender_strategy.states = \
            self.attacker_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.S_D
        defender_strategy.actions = \
            self.attacker_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.A1
        self.defender_simulation_env_config.simulation_env_input_config.attacker_strategy = attacker_strategy
        self.defender_simulation_env_config.simulation_env_input_config.defender_strategy = defender_strategy
        env = gym.make(self.defender_simulation_env_config.gym_env_name,
                       config=self.defender_simulation_env_config.simulation_env_input_config)
        return self._eval_env(
            env=env, policy=defender_strategy,
            num_iterations=self.experiment_config.hparams[
                agents_constants.LOCAL_DFSP.BEST_RESPONSE_EVALUATION_ITERATIONS].value)

    def evaluate_strategy_profile(self, defender_strategy: MixedPPOPolicy,
                                  attacker_strategy: MixedPPOPolicy) -> Dict[str, Union[float, int]]:
        """
        Monte-Carlo evaluation of the game value following a given strategy profile

        :param defender_strategy: the average defender strategy
        :param attacker_strategy: the average attacker strategy
        :return: the average reward
        """
        defender_strategy.states = \
            self.defender_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.S_D
        defender_strategy.actions = \
            self.defender_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.A1
        attacker_strategy.states = \
            self.attacker_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.S_A
        attacker_strategy.actions = \
            self.attacker_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.A2
        self.attacker_simulation_env_config.simulation_env_input_config.defender_strategy = defender_strategy
        self.attacker_simulation_env_config.simulation_env_input_config.attacker_strategy = attacker_strategy
        env = gym.make(self.attacker_simulation_env_config.gym_env_name,
                       config=self.attacker_simulation_env_config.simulation_env_input_config)
        return self._eval_env(
            env=env, policy=attacker_strategy,
            num_iterations=self.experiment_config.hparams[
                agents_constants.LOCAL_DFSP.EQUILIBRIUM_STRATEGIES_EVALUATION_ITERATIONS].value)

    def evaluate_attacker_policy(self, defender_strategy: MixedPPOPolicy,
                                 attacker_strategy: PPOPolicy) -> Dict[str, Union[float, int]]:
        """
        Monte-Carlo evaluation of the game value of a given attacker strategy against the average defender strategy

        :param defender_strategy: the average defender strategy
        :param attacker_strategy: the attacker strategy to evaluate
        :return: the average reward
        """
        defender_strategy.states = \
            self.defender_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.S_D
        defender_strategy.actions = \
            self.defender_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.A1
        attacker_strategy.states = \
            self.attacker_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.S_A
        attacker_strategy.actions = \
            self.attacker_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.A2
        self.attacker_simulation_env_config.simulation_env_input_config.defender_strategy = defender_strategy
        self.attacker_simulation_env_config.simulation_env_input_config.attacker_strategy = attacker_strategy
        env = gym.make(self.attacker_simulation_env_config.gym_env_name,
                       config=self.attacker_simulation_env_config.simulation_env_input_config)
        return self._eval_env(
            env=env, policy=attacker_strategy,
            num_iterations=self.experiment_config.hparams[
                agents_constants.LOCAL_DFSP.BEST_RESPONSE_EVALUATION_ITERATIONS].value)

    def defender_best_response(self, seed: int, defender_strategy: MixedPPOPolicy,
                               attacker_strategy: MixedPPOPolicy) -> Tuple[PPOPolicy, float]:
        """
        Learns a best response for the defender against a given attacker strategy

        :param seed: the random seed
        :param defender_strategy: the defender strategy
        :param attacker_strategy: the attacker strategy
        :return: the learned best response strategy and the average return
        """
        self.de_experiment_config.random_seeds = [seed]
        self.vi_experiment_config.random_seeds = [seed]
        self.de_experiment_config.output_dir = str(self.root_output_dir)
        self.vi_experiment_config.output_dir = str(self.root_output_dir)
        self.de_experiment_config.agent_type = AgentType.DIFFERENTIAL_EVOLUTION
        self.defender_simulation_env_config.gym_env_name = \
            "csle-intrusion-response-game-local-stopping-pomdp-defender-v1"
        agent = DifferentialEvolutionAgent(
            emulation_env_config=self.emulation_env_config,
            simulation_env_config=self.defender_simulation_env_config,
            experiment_config=self.de_experiment_config, save_to_metastore=False)
        Logger.__call__().get_logger().info(f"[Local DFSP] Starting training of the defender's best response "
                                            f"against defender strategy: {defender_strategy}")
        experiment_execution = agent.train()
        stopping_policy: LinearThresholdStoppingPolicy = experiment_execution.result.policies[seed]
        S_D = self.defender_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.S_D
        self.defender_simulation_env_config.gym_env_name = "csle-intrusion-response-game-local-pomdp-defender-v1"
        T = IntrusionResponseGameUtil.local_stopping_mdp_transition_tensor(
            S=self.defender_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.S,
            A1=self.defender_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.A1,
            A2=self.defender_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.A2,
            S_D=S_D,
            T=self.defender_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.T[0]
        )
        o = [self.defender_simulation_env_config.simulation_env_input_config.stopping_zone] + \
            list(self.defender_simulation_env_config.simulation_env_input_config.
                 local_intrusion_response_game_config.a_b1)
        strategy = self.defender_simulation_env_config.simulation_env_input_config.attacker_strategy
        T = reduce_T(T=T, strategy=strategy.stage_policy(o=o))
        R = IntrusionResponseGameUtil.local_stopping_mdp_reward_tensor(
            S=self.defender_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.S,
            A1=self.defender_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.A1,
            A2=self.defender_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.A2,
            R=self.defender_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.R[0],
            S_D=self.defender_simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config.S_D
        )
        o = [self.defender_simulation_env_config.simulation_env_input_config.stopping_zone] + \
            list(self.defender_simulation_env_config.simulation_env_input_config
                 .local_intrusion_response_game_config.a_b1)
        strategy = self.defender_simulation_env_config.simulation_env_input_config.attacker_strategy
        R = reduce_R(R=R, strategy=strategy.stage_policy(o=o))
        self.vi_experiment_config.hparams[agents_constants.VI.REWARD_TENSOR].value == list(R.tolist())
        self.vi_experiment_config.hparams[agents_constants.VI.TRANSITION_TENSOR].value == list(T.tolist())
        vi_agent = VIAgent(simulation_env_config=self.defender_simulation_env_config,
                           experiment_config=self.vi_experiment_config, save_to_metastore=False)
        experiment_execution = vi_agent.train()
        action_policy: TabularPolicy = experiment_execution.result.policies[seed]
        policy = LinearTabularPolicy(
            stopping_policy=stopping_policy, action_policy=action_policy,
            simulation_name=self.defender_simulation_env_config.name,
            states=self.simulation_env_config.state_space_config.states,
            actions=self.simulation_env_config.joint_action_space_config.action_spaces,
            experiment_config=None, avg_R=-1, agent_type=AgentType.DFSP_LOCAL,
            player_type=PlayerType.DEFENDER
        )
        defender_metrics = self.evaluate_defender_policy(
            defender_strategy=policy,
            attacker_strategy=self.defender_simulation_env_config.simulation_env_input_config.attacker_strategy
        )
        val = round(defender_metrics[env_constants.ENV_METRICS.RETURN], 3)
        return policy, val

    def _eval_env(self, env: BaseEnv, policy: Policy, num_iterations: int) -> Dict[str, Union[float, int]]:
        """

        :param env: the environment to use for evaluation
        :param policy: the policy to evaluate
        :param num_iterations: number of iterations to evaluate
        :return: the average reward
        """
        metrics: Dict[str, Any] = {}
        for j in range(num_iterations):
            done = False
            o, _ = env.reset()
            J = 0
            t = 1
            while not done and t <= self.experiment_config.hparams[agents_constants.COMMON.MAX_ENV_STEPS].value:
                if isinstance(policy, TabularPolicy):
                    o = int(o[0])
                a = policy.action(o=o)
                o, r, done, _, info = env.step(a)
                J += r
                t += 1
            metrics = self.update_metrics(metrics=metrics, info=info)
        avg_metrics = self.compute_avg_metrics(metrics=metrics)
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
            try:
                if k in metrics:
                    metrics[k].append(round(v, 3))
                else:
                    metrics[k] = [v]
            except Exception:
                pass
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
            try:
                avg = round(sum(v) / len(v), 2)
                avg_metrics[k] = avg
            except Exception:
                pass
        return avg_metrics

    def attacker_best_response(self, seed: int, defender_strategy: MixedPPOPolicy, attacker_strategy: MixedPPOPolicy) \
            -> Tuple[PPOPolicy, float]:
        """
        Learns a best response strategy for the attacker against a given defender strategy

        :param seed: the random seed
        :param defender_strategy: the defender strategy
        :param attacker_strategy: the attacker strategy
        :return: the learned best response strategy and the average return
        """
        self.ppo_experiment_config.random_seeds = [seed]
        self.ppo_experiment_config.output_dir = str(self.root_output_dir)
        self.ppo_experiment_config.agent_type = AgentType.PPO
        agent = PPOAgent(emulation_env_config=self.emulation_env_config,
                         simulation_env_config=self.attacker_simulation_env_config,
                         experiment_config=self.ppo_experiment_config, save_to_metastore=False)
        Logger.__call__().get_logger().info(f"[Local DFSP] Starting training of the attacker's best response "
                                            f"against defender strategy: {defender_strategy}")
        experiment_execution = agent.train()
        policy: PPOPolicy = experiment_execution.result.policies[seed]
        val = experiment_execution.result.avg_metrics[agents_constants.COMMON.RUNNING_AVERAGE_RETURN][-1]
        return policy, val

    def hparam_names(self) -> List[str]:
        """
        :return: a list with the hyperparameter names
        """
        return [
            constants.NEURAL_NETWORKS.NUM_NEURONS_PER_HIDDEN_LAYER,
            constants.NEURAL_NETWORKS.NUM_HIDDEN_LAYERS,
            agents_constants.PPO.STEPS_BETWEEN_UPDATES,
            agents_constants.COMMON.LEARNING_RATE, agents_constants.COMMON.BATCH_SIZE,
            agents_constants.COMMON.GAMMA, agents_constants.PPO.GAE_LAMBDA, agents_constants.PPO.CLIP_RANGE,
            agents_constants.PPO.CLIP_RANGE_VF, agents_constants.PPO.ENT_COEF,
            agents_constants.PPO.VF_COEF, agents_constants.PPO.MAX_GRAD_NORM, agents_constants.PPO.TARGET_KL,
            agents_constants.COMMON.NUM_TRAINING_TIMESTEPS, agents_constants.COMMON.EVAL_EVERY,
            agents_constants.COMMON.EVAL_BATCH_SIZE, constants.NEURAL_NETWORKS.DEVICE,
            agents_constants.COMMON.EVAL_BATCH_SIZE,
            agents_constants.LOCAL_DFSP.N_2,
            agents_constants.COMMON.CONFIDENCE_INTERVAL, agents_constants.COMMON.RUNNING_AVERAGE,
            agents_constants.LOCAL_DFSP.BEST_RESPONSE_EVALUATION_ITERATIONS,
            agents_constants.LOCAL_DFSP.EQUILIBRIUM_STRATEGIES_EVALUATION_ITERATIONS]

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
            y[N - 1:] = np.convolve(x, np.ones((N,)) / N, mode='valid')
        else:
            N = len(x)
            y = np.copy(x)
            y[N - 1:] = np.convolve(x, np.ones((N,)) / N, mode='valid')
        return list(y.tolist())
