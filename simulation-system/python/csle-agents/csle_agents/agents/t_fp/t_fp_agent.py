from typing import Union, List, Dict, Tuple, Optional
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
from csle_common.dao.training.multi_threshold_stopping_policy import MultiThresholdStoppingPolicy
from csle_common.dao.training.mixed_multi_threshold_stopping_policy import MixedMultiThresholdStoppingPolicy
from csle_common.dao.training.policy import Policy
from csle_agents.agents.base.base_agent import BaseAgent
from csle_agents.agents.t_spsa.t_spsa_agent import TSPSAAgent
import csle_agents.constants.constants as agents_constants
import gym_csle_stopping_game.constants.constants as env_constants


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
        self.root_output_dir = str(self.experiment_config.output_dir)
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

        # Define which metrics to plot in the UI
        exp_result.plot_metrics.append(agents_constants.COMMON.EXPLOITABILITY)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_EXPLOITABILITY)
        exp_result.plot_metrics.append(agents_constants.COMMON.AVERAGE_ATTACKER_RETURN)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_ATTACKER_RETURN)
        exp_result.plot_metrics.append(agents_constants.T_FP.RUNNING_AVERAGE_BEST_RESPONSE_ATTACKER_RETURN)
        exp_result.plot_metrics.append(agents_constants.COMMON.AVERAGE_DEFENDER_RETURN)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_DEFENDER_RETURN)
        exp_result.plot_metrics.append(agents_constants.T_FP.RUNNING_AVERAGE_BEST_RESPONSE_DEFENDER_RETURN)
        exp_result.plot_metrics.append(env_constants.ENV_METRICS.INTRUSION_LENGTH)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_LENGTH)
        exp_result.plot_metrics.append(env_constants.ENV_METRICS.INTRUSION_START)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_START)
        exp_result.plot_metrics.append(env_constants.ENV_METRICS.TIME_HORIZON)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON)
        exp_result.plot_metrics.append(env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN)
        exp_result.plot_metrics.append(env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN)
        for l in range(1, self.experiment_config.hparams[agents_constants.T_SPSA.L].value + 1):
            exp_result.plot_metrics.append(env_constants.ENV_METRICS.STOP + f"_{l}")
            exp_result.plot_metrics.append(env_constants.ENV_METRICS.STOP + f"_running_average_{l}")

        descr = f"Approximating a Nash equilibrium with the T-FP algorithm using " \
                f"simulations: {self.defender_simulation_env_config.name} " \
                f"and {self.attacker_simulation_env_config.name}"
        for seed in self.experiment_config.random_seeds:
            exp_result.all_metrics[seed] = {}
            exp_result.all_metrics[seed][agents_constants.T_SPSA.THETAS] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_DEFENDER_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_DEFENDER_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_ATTACKER_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_ATTACKER_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.T_FP.AVERAGE_BEST_RESPONSE_DEFENDER_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.T_FP.RUNNING_AVERAGE_BEST_RESPONSE_DEFENDER_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.T_FP.AVERAGE_BEST_RESPONSE_ATTACKER_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.T_FP.RUNNING_AVERAGE_BEST_RESPONSE_ATTACKER_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.EXPLOITABILITY] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_EXPLOITABILITY] = []
            exp_result.all_metrics[seed][agents_constants.T_FP.DEFENDER_THRESHOLDS] = []
            exp_result.all_metrics[seed][agents_constants.T_FP.ATTACKER_THRESHOLDS] = []
            for l in range(1, self.experiment_config.hparams[agents_constants.T_SPSA.L].value + 1):
                exp_result.all_metrics[seed][agents_constants.T_SPSA.STOP_DISTRIBUTION_DEFENDER + f"_l={l}"] = []
            for s in self.simulation_env_config.state_space_config.states:
                for l in range(1, self.experiment_config.hparams[agents_constants.T_SPSA.L].value + 1):
                    exp_result.all_metrics[seed][agents_constants.T_SPSA.STOP_DISTRIBUTION_ATTACKER
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
            for l in range(1, self.experiment_config.hparams[agents_constants.T_SPSA.L].value + 1):
                exp_result.all_metrics[seed][env_constants.ENV_METRICS.STOP + f"_{l}"] = []
                exp_result.all_metrics[seed][env_constants.ENV_METRICS.STOP + f"_running_average_{l}"] = []

        if self.training_job is None:
            self.training_job = TrainingJobConfig(
                simulation_env_name=self.simulation_env_config.name, experiment_config=self.experiment_config,
                experiment_result=exp_result, progress_percentage=0, pid=pid,
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
        exp_execution = ExperimentExecution(result=exp_result, config=self.experiment_config, timestamp=ts,
                                            emulation_name=emulation_name, simulation_name=simulation_name,
                                            descr=descr, log_file_path=self.training_job.log_file_path)
        traces = env.get_traces()
        if len(traces) > 0:
            MetastoreFacade.save_simulation_trace(traces[-1])
        MetastoreFacade.remove_training_job(self.training_job)
        return exp_execution

    def t_fp(self, exp_result: ExperimentResult, seed: int, env: gym.Env,
             training_job: TrainingJobConfig, random_seeds: List[int]):

        # Initialize policies
        defender_policy = MixedMultiThresholdStoppingPolicy(
            Theta=np.zeros((self.experiment_config.hparams[agents_constants.T_SPSA.L].value,)).tolist(),
            simulation_name=self.defender_simulation_env_config.name,
            states=self.defender_simulation_env_config.state_space_config.states,
            player_type=PlayerType.DEFENDER,
            L=self.defender_experiment_config.hparams[agents_constants.T_SPSA.L].value,
            actions=self.defender_simulation_env_config.joint_action_space_config.action_spaces[
                self.defender_experiment_config.player_idx].actions,
            experiment_config=self.defender_experiment_config, avg_R=-1,
            agent_type=AgentType.T_FP)
        attacker_policy = MixedMultiThresholdStoppingPolicy(
            Theta=np.zeros((2, self.experiment_config.hparams[agents_constants.T_SPSA.L].value)).tolist(),
            simulation_name=self.attacker_simulation_env_config.name,
            states=self.attacker_simulation_env_config.state_space_config.states,
            player_type=PlayerType.ATTACKER,
            L=self.attacker_experiment_config.hparams[agents_constants.T_SPSA.L].value,
            actions=self.attacker_simulation_env_config.joint_action_space_config.action_spaces[
                self.attacker_experiment_config.player_idx].actions,
            experiment_config=self.attacker_experiment_config, avg_R=-1,
            agent_type=AgentType.T_FP, opponent_strategy=defender_policy)

        # Update average policies with initial thresholds
        # initial_attacker_thresholds = [
        #     [[0]*self.attacker_experiment_config.hparams[agents_constants.T_SPSA.L].value,
        #      [0]*self.attacker_experiment_config.hparams[agents_constants.T_SPSA.L].value
        #      ]*10
        # ]
        initial_attacker_thresholds = []
        initial_defender_thresholds = []
        initial_attacker_thresholds.append(
            [[0] * self.attacker_experiment_config.hparams[agents_constants.T_SPSA.L].value,
             [1] * self.attacker_experiment_config.hparams[agents_constants.T_SPSA.L].value
             ]
        )
        initial_defender_thresholds.append(
            [0] * self.attacker_experiment_config.hparams[agents_constants.T_SPSA.L].value)
        # for i in range(1):
        #     initial_attacker_thresholds.append(
        #         [[round(random.uniform(0,1),2)]*self.attacker_experiment_config.hparams[agents_constants.T_SPSA.L].value,
        #          [round(random.uniform(0,1),2)]*self.attacker_experiment_config.hparams[agents_constants.T_SPSA.L].value
        #          ]
        #     )
        #     initial_defender_thresholds.append(
        #         [round(random.uniform(0,1),2)]*self.attacker_experiment_config.hparams[agents_constants.T_SPSA.L].value)

        attacker_policy.update_Theta(new_thresholds=initial_attacker_thresholds)
        defender_policy.update_Theta(new_thresholds=initial_defender_thresholds)
        attacker_policy.opponent_strategy = defender_policy

        for i in range(self.experiment_config.hparams[agents_constants.T_FP.N_2].value):

            # Compute best responses
            br_seed = np.random.randint(0, 100)
            attacker_thresholds, attacker_val = self.attacker_best_response(
                seed=br_seed, defender_strategy=defender_policy, attacker_strategy=attacker_policy)
            defender_thresholds, defender_val = self.defender_best_response(
                seed=br_seed, attacker_strategy=attacker_policy)

            attacker_metrics = self.evaluate_attacker_policy(
                attacker_thresholds=attacker_thresholds, defender_strategy=defender_policy,
                attacker_strategy=attacker_policy)
            defender_metrics = self.evaluate_defender_policy(
                defender_thresholds=defender_thresholds, attacker_strategy=attacker_policy)
            strategy_profile_metrics = self.evaluate_strategy_profile(
                defender_strategy=defender_policy, attacker_strategy=attacker_policy)

            attacker_val = round(attacker_metrics[env_constants.ENV_METRICS.RETURN], 3)
            defender_val = round(defender_metrics[env_constants.ENV_METRICS.RETURN], 3)
            val = round(strategy_profile_metrics[env_constants.ENV_METRICS.RETURN], 3)

            attacker_policy.update_Theta(new_thresholds=[attacker_thresholds])
            defender_policy.update_Theta(new_thresholds=[defender_thresholds])
            val_attacker_exp = attacker_val
            val_defender_exp = defender_val

            # # Update empirical strategies
            # if attacker_val > -defender_val:
            #     attacker_policy.update_Theta(new_thresholds=[attacker_thresholds])
            #     val_attacker_exp= attacker_val
            # else:
            #     val_attacker_exp = -defender_val
            # if defender_val > -attacker_val:
            #     defender_policy.update_Theta(new_thresholds=[defender_thresholds])
            #     val_defender_exp=defender_val
            # else:
            #     val_defender_exp = -attacker_val

            attacker_policy.opponent_strategy = defender_policy

            # Log rewards
            exp_result.all_metrics[seed][agents_constants.T_FP.AVERAGE_BEST_RESPONSE_ATTACKER_RETURN].append(
                val_attacker_exp)
            exp_result.all_metrics[seed][agents_constants.T_FP.AVERAGE_BEST_RESPONSE_DEFENDER_RETURN].append(
                val_defender_exp)
            exp_result.all_metrics[seed][agents_constants.T_FP.RUNNING_AVERAGE_BEST_RESPONSE_ATTACKER_RETURN].append(
                ExperimentUtil.running_average(
                    exp_result.all_metrics[seed][agents_constants.T_FP.AVERAGE_BEST_RESPONSE_ATTACKER_RETURN],
                    self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))
            exp_result.all_metrics[seed][agents_constants.T_FP.RUNNING_AVERAGE_BEST_RESPONSE_DEFENDER_RETURN].append(
                ExperimentUtil.running_average(
                    exp_result.all_metrics[seed][agents_constants.T_FP.AVERAGE_BEST_RESPONSE_DEFENDER_RETURN],
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

            # Log thresholds
            exp_result.all_metrics[seed][agents_constants.T_FP.ATTACKER_THRESHOLDS].append(attacker_policy.Theta)
            exp_result.all_metrics[seed][agents_constants.T_FP.DEFENDER_THRESHOLDS].append(defender_policy.Theta)

            # Log stop distributions
            for k, v in attacker_policy.stop_distributions().items():
                exp_result.all_metrics[seed][k].append(v)
            for k, v in defender_policy.stop_distributions().items():
                exp_result.all_metrics[seed][k].append(v)

            # Log intrusion lengths
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_LENGTH].append(
                round(strategy_profile_metrics[env_constants.ENV_METRICS.INTRUSION_LENGTH], 3))
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_LENGTH].append(
                ExperimentUtil.running_average(
                    exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_LENGTH],
                    self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))

            # Log stopping times
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_START].append(
                round(strategy_profile_metrics[env_constants.ENV_METRICS.INTRUSION_START], 3))
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_INTRUSION_START].append(
                ExperimentUtil.running_average(
                    exp_result.all_metrics[seed][env_constants.ENV_METRICS.INTRUSION_START],
                    self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.TIME_HORIZON].append(
                round(strategy_profile_metrics[env_constants.ENV_METRICS.TIME_HORIZON], 3))
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON].append(
                ExperimentUtil.running_average(
                    exp_result.all_metrics[seed][env_constants.ENV_METRICS.TIME_HORIZON],
                    self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))
            for l in range(1, self.experiment_config.hparams[agents_constants.T_SPSA.L].value + 1):
                exp_result.plot_metrics.append(env_constants.ENV_METRICS.STOP + f"_{l}")
                exp_result.all_metrics[seed][env_constants.ENV_METRICS.STOP + f"_{l}"].append(
                    round(strategy_profile_metrics[env_constants.ENV_METRICS.STOP + f"_{l}"], 3))
                exp_result.all_metrics[seed][env_constants.ENV_METRICS.STOP + f"_running_average_{l}"].append(
                    ExperimentUtil.running_average(
                        exp_result.all_metrics[seed][env_constants.ENV_METRICS.STOP + f"_{l}"],
                        self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value))

            # Log baseline returns
            exp_result.all_metrics[seed][env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN].append(
                round(strategy_profile_metrics[env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN], 3))
            exp_result.all_metrics[seed][
                env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN].append(
                round(
                    strategy_profile_metrics[
                        env_constants.ENV_METRICS.AVERAGE_DEFENDER_BASELINE_STOP_ON_FIRST_ALERT_RETURN], 3))

            # Compute and log exploitability
            exp = TFPAgent.exploitability(attacker_val=val_attacker_exp, defender_val=val_defender_exp)
            exp_result.all_metrics[seed][agents_constants.COMMON.EXPLOITABILITY].append(exp)
            running_avg_exp = ExperimentUtil.running_average(
                exp_result.all_metrics[seed][agents_constants.COMMON.EXPLOITABILITY],
                self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value)
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_EXPLOITABILITY].append(running_avg_exp)

            # Logging the progress
            if i % self.experiment_config.log_every == 0:
                Logger.__call__().get_logger().info(
                    f"[T-FP] i: {i}, Exp: {exp}, "
                    f"Exp_avg_{self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value}: "
                    f"{running_avg_exp}, game_val: {val} "
                    f"opt_val:{exp_result.all_metrics[seed][env_constants.ENV_METRICS.AVERAGE_UPPER_BOUND_RETURN][-1]},"
                    f" Defender val:{defender_val}, Attacker val:{attacker_val}, "
                    f"defender BR thresholds:{defender_thresholds},"
                    f" attacker BR thresholds: {attacker_thresholds},"
                    f" defender stop dists: {defender_policy.stop_distributions()}, "
                    f"attacker stop dists: {attacker_policy.stop_distributions()}")

                # Update training job
                total_iterations = len(random_seeds) * self.experiment_config.hparams[agents_constants.T_FP.N_2].value
                iterations_done = ((random_seeds.index(seed)) *
                                   self.experiment_config.hparams[agents_constants.T_FP.N_2].value + i)
                progress = round(iterations_done / total_iterations, 2)
                training_job.progress_percentage = progress
                MetastoreFacade.update_training_job(training_job=training_job, id=training_job.id)

    def evaluate_defender_policy(self, defender_thresholds: List[float],
                                 attacker_strategy: MixedMultiThresholdStoppingPolicy) -> Dict[str, Union[float, int]]:
        """
        Monte-Carlo evaluation of the game value of a given defender policy against the average attacker strategy

        :param defender_thresholds: the defender strategy to evaluate
        :param attacker_strategy: the average attacker strategy
        :return: the average reward
        """
        defender_policy = MultiThresholdStoppingPolicy(
            theta=defender_thresholds, simulation_name=self.simulation_env_config.name,
            states=self.simulation_env_config.state_space_config.states,
            player_type=PlayerType.DEFENDER, L=self.defender_experiment_config.hparams[agents_constants.T_SPSA.L].value,
            actions=self.defender_simulation_env_config.joint_action_space_config.action_spaces[
                self.defender_experiment_config.player_idx].actions, experiment_config=self.defender_experiment_config,
            avg_R=-1, agent_type=AgentType.NONE)
        self.defender_simulation_env_config.simulation_env_input_config.attacker_strategy = attacker_strategy
        env = gym.make(self.defender_simulation_env_config.gym_env_name,
                       config=self.defender_simulation_env_config.simulation_env_input_config)
        return self._eval_env(
            env=env, policy=defender_policy,
            num_iterations=self.experiment_config.hparams[
                agents_constants.T_FP.BEST_RESPONSE_EVALUATION_ITERATIONS].value)

    def evaluate_strategy_profile(self, defender_strategy: MixedMultiThresholdStoppingPolicy,
                                  attacker_strategy: MixedMultiThresholdStoppingPolicy) -> Dict[str, Union[float, int]]:
        """
        Monte-Carlo evaluation of the game value following a given strategy profile

        :param defender_strategy: the average defender strategy
        :param attacker_strategy: the average attacker strategy
        :return: the average reward
        """
        self.attacker_simulation_env_config.simulation_env_input_config.defender_strategy = defender_strategy
        env = gym.make(self.attacker_simulation_env_config.gym_env_name,
                       config=self.attacker_simulation_env_config.simulation_env_input_config)
        env.set_model(attacker_strategy)
        attacker_strategy.opponent_strategy = env.static_defender_strategy
        return self._eval_env(
            env=env, policy=attacker_strategy,
            num_iterations=self.experiment_config.hparams[
                agents_constants.T_FP.EQUILIBRIUM_STRATEGIES_EVALUATION_ITERATIONS].value)

    def evaluate_attacker_policy(self, attacker_thresholds: List[List[float]],
                                 defender_strategy: MixedMultiThresholdStoppingPolicy,
                                 attacker_strategy: MixedMultiThresholdStoppingPolicy) -> Dict[str, Union[float, int]]:
        """
        Monte-Carlo evaluation of the game value of a given attacker policy against the average defender strategy

        :param defender_thresholds: the defender strategy to evaluate
        :param defender_strategy: the average defender strategy
        :param attacker_strategy: the average attacker strategy
        :return: the average reward
        """
        theta = [item for sublist in attacker_thresholds for item in sublist]
        attacker_policy = MultiThresholdStoppingPolicy(
            theta=theta, simulation_name=self.simulation_env_config.name,
            states=self.simulation_env_config.state_space_config.states,
            player_type=PlayerType.ATTACKER, L=self.attacker_experiment_config.hparams[agents_constants.T_SPSA.L].value,
            actions=self.attacker_simulation_env_config.joint_action_space_config.action_spaces[
                self.attacker_experiment_config.player_idx].actions, experiment_config=self.attacker_experiment_config,
            avg_R=-1, agent_type=AgentType.NONE)
        self.attacker_simulation_env_config.simulation_env_input_config.defender_strategy = defender_strategy
        env = gym.make(self.attacker_simulation_env_config.gym_env_name,
                       config=self.attacker_simulation_env_config.simulation_env_input_config)
        env.set_model(attacker_strategy)
        attacker_policy.opponent_strategy = env.static_defender_strategy
        return self._eval_env(
            env=env, policy=attacker_policy,
            num_iterations=self.experiment_config.hparams[
                agents_constants.T_FP.BEST_RESPONSE_EVALUATION_ITERATIONS].value)

    def defender_best_response(self, seed: int, attacker_strategy: MixedMultiThresholdStoppingPolicy) \
            -> Tuple[List, float]:
        """
        Learns a best response for the defender against a given attacker strategy

        :param seed: the random seed
        :param attacker_strategy: the attacker strategy
        :return: the learned thresholds and the value
        """
        self.defender_experiment_config.random_seeds = [seed]
        self.defender_experiment_config.output_dir = str(self.root_output_dir)
        self.defender_simulation_env_config.simulation_env_input_config.attacker_strategy = attacker_strategy
        env = gym.make(self.defender_simulation_env_config.gym_env_name,
                       config=self.defender_simulation_env_config.simulation_env_input_config)
        agent = TSPSAAgent(emulation_env_config=self.emulation_env_config,
                           simulation_env_config=self.defender_simulation_env_config,
                           experiment_config=self.defender_experiment_config, env=env, save_to_metastore=False)
        Logger.__call__().get_logger().info(f"[T-FP] Starting training of the defender's best response "
                                            f"against attacker strategy: {attacker_strategy}")
        experiment_execution = agent.train()
        policy: MultiThresholdStoppingPolicy = experiment_execution.result.policies[seed]
        thresholds = policy.thresholds()
        val = experiment_execution.result.avg_metrics[agents_constants.COMMON.RUNNING_AVERAGE_RETURN][-1]
        return thresholds, val

    def _eval_env(self, env: gym.Env, policy: Policy, num_iterations: int) -> Dict[str, Union[float, int]]:
        """

        :param env: the environment to use for evaluation
        :param policy: the policy to evaluate
        :param num_iterations: number of iterations to evaluate
        :return: the average reward
        """
        metrics = {}
        for j in range(num_iterations):
            done = False
            o = env.reset()
            J = 0
            t = 1
            while not done and t <= self.experiment_config.hparams[agents_constants.COMMON.MAX_ENV_STEPS].value:
                a = policy.action(o=o)
                o, r, done, info = env.step(a)
                J += r
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

    def attacker_best_response(self, seed: int, defender_strategy: MixedMultiThresholdStoppingPolicy,
                               attacker_strategy: MixedMultiThresholdStoppingPolicy) \
            -> Tuple[List, float]:
        """
        Learns a threshold best response strategy for the attacker against a given defender strategy

        :param seed: the random seed
        :param defender_strategy: the defender strategy
        :param attacker_strategy: the attacker strategy
        :return: the learned threshold strategy and its estimated value
        """
        self.attacker_experiment_config.random_seeds = [seed]
        self.attacker_experiment_config.output_dir = str(self.root_output_dir)
        self.attacker_simulation_env_config.simulation_env_input_config.defender_strategy = defender_strategy
        env = gym.make(self.attacker_simulation_env_config.gym_env_name,
                       config=self.attacker_simulation_env_config.simulation_env_input_config)
        env.set_model(attacker_strategy)
        agent = TSPSAAgent(emulation_env_config=self.emulation_env_config,
                           simulation_env_config=self.attacker_simulation_env_config,
                           experiment_config=self.attacker_experiment_config,
                           env=env, save_to_metastore=False)
        Logger.__call__().get_logger().info(f"[T-FP] Starting training of the attacker's best response "
                                            f"against defender strategy: {defender_strategy}")
        experiment_execution = agent.train()
        policy: MultiThresholdStoppingPolicy = experiment_execution.result.policies[seed]
        thresholds = policy.thresholds()
        val = experiment_execution.result.avg_metrics[agents_constants.COMMON.RUNNING_AVERAGE_RETURN][-1]
        attacker_thresholds = [
            thresholds[0:self.attacker_experiment_config.hparams[agents_constants.T_SPSA.L].value],
            thresholds[self.attacker_experiment_config.hparams[agents_constants.T_SPSA.L].value:]
        ]
        return attacker_thresholds, val

    def hparam_names(self) -> List[str]:
        """
        :return: a list with the hyperparameter names
        """
        return [agents_constants.T_SPSA.a, agents_constants.T_SPSA.c, agents_constants.T_SPSA.LAMBDA,
                agents_constants.T_SPSA.A, agents_constants.T_SPSA.EPSILON, agents_constants.T_SPSA.N,
                agents_constants.T_SPSA.L, agents_constants.T_FP.THETA1_ATTACKER, agents_constants.T_FP.THETA1_DEFENDER,
                agents_constants.COMMON.EVAL_BATCH_SIZE,
                agents_constants.T_FP.N_2, agents_constants.T_SPSA.GRADIENT_BATCH_SIZE,
                agents_constants.COMMON.CONFIDENCE_INTERVAL, agents_constants.COMMON.RUNNING_AVERAGE,
                agents_constants.T_FP.BEST_RESPONSE_EVALUATION_ITERATIONS,
                agents_constants.T_FP.EQUILIBRIUM_STRATEGIES_EVALUATION_ITERATIONS]

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

    def get_defender_experiment_config(self) -> ExperimentConfig:
        """
        :return: the experiment configuration for learning a best response of the defender
        """
        hparams = {
            agents_constants.T_SPSA.N: self.experiment_config.hparams[agents_constants.T_SPSA.N],
            agents_constants.T_SPSA.c: self.experiment_config.hparams[agents_constants.T_SPSA.c],
            agents_constants.T_SPSA.a: self.experiment_config.hparams[agents_constants.T_SPSA.a],
            agents_constants.T_SPSA.A: self.experiment_config.hparams[agents_constants.T_SPSA.A],
            agents_constants.T_SPSA.LAMBDA: self.experiment_config.hparams[agents_constants.T_SPSA.LAMBDA],
            agents_constants.T_SPSA.EPSILON: self.experiment_config.hparams[agents_constants.T_SPSA.EPSILON],
            agents_constants.T_SPSA.L: self.experiment_config.hparams[agents_constants.T_SPSA.L],
            agents_constants.COMMON.EVAL_BATCH_SIZE: self.experiment_config.hparams[
                agents_constants.COMMON.EVAL_BATCH_SIZE],
            agents_constants.COMMON.CONFIDENCE_INTERVAL: self.experiment_config.hparams[
                agents_constants.COMMON.CONFIDENCE_INTERVAL],
            agents_constants.COMMON.MAX_ENV_STEPS: self.experiment_config.hparams[
                agents_constants.COMMON.MAX_ENV_STEPS],
            agents_constants.T_SPSA.GRADIENT_BATCH_SIZE: self.experiment_config.hparams[
                agents_constants.T_SPSA.GRADIENT_BATCH_SIZE],
            agents_constants.COMMON.RUNNING_AVERAGE: self.experiment_config.hparams[
                agents_constants.COMMON.RUNNING_AVERAGE],
            agents_constants.COMMON.GAMMA: self.experiment_config.hparams[agents_constants.COMMON.GAMMA]
        }
        if agents_constants.T_FP.THETA1_DEFENDER in self.experiment_config.hparams:
            hparams[agents_constants.T_SPSA.THETA1] = \
                self.experiment_config.hparams[agents_constants.T_FP.THETA1_DEFENDER]
        return ExperimentConfig(
            output_dir=str(self.root_output_dir),
            title="Learning a best response of the defender as part of T-FP",
            random_seeds=[], agent_type=AgentType.T_SPSA,
            log_every=self.experiment_config.br_log_every,
            hparams=hparams,
            player_type=PlayerType.DEFENDER, player_idx=0
        )

    def get_attacker_experiment_config(self) -> ExperimentConfig:
        """
        :return: the experiment configuration for learning a best response of the attacker
        """
        hparams = {
            agents_constants.T_SPSA.N: self.experiment_config.hparams[agents_constants.T_SPSA.N],
            agents_constants.T_SPSA.c: self.experiment_config.hparams[agents_constants.T_SPSA.c],
            agents_constants.T_SPSA.a: self.experiment_config.hparams[agents_constants.T_SPSA.a],
            agents_constants.T_SPSA.A: self.experiment_config.hparams[agents_constants.T_SPSA.A],
            agents_constants.T_SPSA.LAMBDA: self.experiment_config.hparams[agents_constants.T_SPSA.LAMBDA],
            agents_constants.T_SPSA.EPSILON: self.experiment_config.hparams[agents_constants.T_SPSA.EPSILON],
            agents_constants.T_SPSA.L: self.experiment_config.hparams[agents_constants.T_SPSA.L],
            agents_constants.COMMON.EVAL_BATCH_SIZE: self.experiment_config.hparams[
                agents_constants.COMMON.EVAL_BATCH_SIZE],
            agents_constants.COMMON.CONFIDENCE_INTERVAL: self.experiment_config.hparams[
                agents_constants.COMMON.CONFIDENCE_INTERVAL],
            agents_constants.COMMON.MAX_ENV_STEPS: self.experiment_config.hparams[
                agents_constants.COMMON.MAX_ENV_STEPS],
            agents_constants.T_SPSA.GRADIENT_BATCH_SIZE: self.experiment_config.hparams[
                agents_constants.T_SPSA.GRADIENT_BATCH_SIZE],
            agents_constants.COMMON.RUNNING_AVERAGE: self.experiment_config.hparams[
                agents_constants.COMMON.RUNNING_AVERAGE],
            agents_constants.COMMON.GAMMA: self.experiment_config.hparams[
                agents_constants.COMMON.GAMMA]
        }
        if agents_constants.T_FP.THETA1_ATTACKER in self.experiment_config.hparams:
            hparams[agents_constants.T_SPSA.THETA1] = \
                self.experiment_config.hparams[agents_constants.T_FP.THETA1_ATTACKER]
        return ExperimentConfig(
            output_dir=str(self.root_output_dir),
            title="Learning a best response of the attacker as part of T-FP",
            random_seeds=[], agent_type=AgentType.T_SPSA,
            log_every=self.experiment_config.br_log_every,
            hparams=hparams,
            player_type=PlayerType.ATTACKER, player_idx=1
        )

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
            y[N - 1:] = np.convolve(x, np.ones((N, )) / N, mode='valid')
        else:
            N = len(x)
            y = np.copy(x)
            y[N - 1:] = np.convolve(x, np.ones((N, )) / N, mode='valid')
        return y.tolist()
