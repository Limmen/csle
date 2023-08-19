from typing import List, Optional
import time
import gymnasium as gym
import os
import numpy as np
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.vec_env.vec_monitor import VecMonitor
from stable_baselines3.common.vec_env.dummy_vec_env import DummyVecEnv
from stable_baselines3.common.env_util import make_vec_env
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.experiment_execution import ExperimentExecution
from csle_common.dao.training.experiment_result import ExperimentResult
from csle_common.dao.training.agent_type import AgentType
from csle_common.util.experiment_util import ExperimentUtil
from csle_common.logging.log import Logger
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.jobs.training_job_config import TrainingJobConfig
from csle_common.dao.training.dqn_policy import DQNPolicy
from csle_common.dao.simulation_config.state import State
from csle_common.dao.simulation_config.action import Action
from csle_common.dao.training.player_type import PlayerType
from csle_common.util.general_util import GeneralUtil
from csle_common.dao.simulation_config.base_env import BaseEnv
from csle_agents.agents.base.base_agent import BaseAgent
import csle_agents.constants.constants as agents_constants


class DQNAgent(BaseAgent):
    """
    A DQN agent using the implementation from OpenAI baselines
    """
    def __init__(self, simulation_env_config: SimulationEnvConfig,
                 emulation_env_config: Optional[EmulationEnvConfig], experiment_config: ExperimentConfig,
                 training_job: Optional[TrainingJobConfig] = None, save_to_metastore: bool = True) -> None:
        """
        Initializes the agent

        :param simulation_env_config: the simulation environment configuration
        :param emulation_env_config: the emulation environment configuration
        :param experiment_config: the experiment configuration
        :param training_job: the training job configuration
        :param save_to_metastore: boolean flag indicating whether job information should be saved to the metastore
        """
        super(DQNAgent, self).__init__(simulation_env_config=simulation_env_config,
                                       emulation_env_config=emulation_env_config,
                                       experiment_config=experiment_config)
        assert experiment_config.agent_type == AgentType.DQN
        self.training_job = training_job
        self.save_to_metastore = save_to_metastore

    def train(self) -> ExperimentExecution:
        """
        Implements the training logic of the DQN algorithm

        :return: the experiment result
        """
        pid = os.getpid()

        # Setup experiment metrics
        exp_result = ExperimentResult()
        exp_result.plot_metrics.append(agents_constants.COMMON.AVERAGE_RETURN)
        descr = f"Training of policies with DQN using " \
                f"simulation:{self.simulation_env_config.name}"

        # Setup training job
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
            training_job_id = MetastoreFacade.save_training_job(training_job=self.training_job)
            self.training_job.id = training_job_id
        else:
            self.training_job.pid = pid
            self.training_job.progress_percentage = 0
            self.training_job.experiment_result = exp_result
            MetastoreFacade.update_training_job(training_job=self.training_job, id=self.training_job.id)

        # Setup experiment execution
        ts = time.time()
        simulation_name = self.simulation_env_config.name
        emulation_name = ""
        if self.emulation_env_config is not None:
            emulation_name = self.emulation_env_config.name
        self.exp_execution = ExperimentExecution(
            result=exp_result, config=self.experiment_config, timestamp=ts,
            emulation_name=emulation_name, simulation_name=simulation_name,
            descr=descr, log_file_path=self.training_job.log_file_path)
        exp_execution_id = MetastoreFacade.save_experiment_execution(self.exp_execution)
        self.exp_execution.id = exp_execution_id

        # Setup gym environment
        config = self.simulation_env_config.simulation_env_input_config
        orig_env: BaseEnv = gym.make(self.simulation_env_config.gym_env_name, config=config)
        env = make_vec_env(env_id=self.simulation_env_config.gym_env_name,
                           n_envs=self.experiment_config.hparams[agents_constants.COMMON.NUM_PARALLEL_ENVS].value,
                           env_kwargs={"config": config}, vec_env_cls=DummyVecEnv)
        env = VecMonitor(env)

        # Training runs, one per seed
        for seed in self.experiment_config.random_seeds:
            exp_result.all_metrics[seed] = {}
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN] = []
            ExperimentUtil.set_seed(seed)

            # Callback for logging training metrics
            cb = DQNTrainingCallback(
                eval_every=self.experiment_config.hparams[agents_constants.COMMON.EVAL_EVERY].value,
                eval_batch_size=self.experiment_config.hparams[agents_constants.COMMON.EVAL_BATCH_SIZE].value,
                random_seeds=self.experiment_config.random_seeds, training_job=self.training_job,
                max_steps=self.experiment_config.hparams[agents_constants.COMMON.NUM_TRAINING_TIMESTEPS].value,
                seed=seed, exp_result=exp_result, simulation_name=self.simulation_env_config.name,
                player_type=self.experiment_config.player_type,
                states=self.simulation_env_config.state_space_config.states,
                actions=(
                    self.simulation_env_config.joint_action_space_config.action_spaces[
                        self.experiment_config.player_idx].actions),
                save_every=self.experiment_config.hparams[agents_constants.COMMON.SAVE_EVERY].value,
                save_dir=self.experiment_config.output_dir, exp_execution=self.exp_execution,
                env=orig_env, experiment_config=self.experiment_config,
                L=self.experiment_config.hparams[agents_constants.COMMON.L].value,
                gym_env_name=self.simulation_env_config.gym_env_name
            )

            # Create DQN Agent
            policy_kwargs = dict(
                net_arch=[self.experiment_config.hparams[constants.NEURAL_NETWORKS.NUM_NEURONS_PER_HIDDEN_LAYER].value
                          ] * self.experiment_config.hparams[constants.NEURAL_NETWORKS.NUM_HIDDEN_LAYERS].value)
            model = DQN(
                agents_constants.DQN.MLP_POLICY, env, verbose=0, policy_kwargs=policy_kwargs,
                batch_size=self.experiment_config.hparams[agents_constants.DQN.DQN_BATCH_SIZE].value,
                learning_rate=self.experiment_config.hparams[agents_constants.COMMON.LEARNING_RATE].value,
                seed=seed, device=self.experiment_config.hparams[constants.NEURAL_NETWORKS.DEVICE].value,
                gamma=self.experiment_config.hparams[agents_constants.COMMON.GAMMA].value,
                exploration_fraction=self.experiment_config.hparams[agents_constants.DQN.EXPLORATION_FRACTION].value,
                exploration_final_eps=(
                    self.experiment_config.hparams[agents_constants.DQN.EXPLORATION_FINAL_EPS].value),
                exploration_initial_eps=(
                    self.experiment_config.hparams[agents_constants.DQN.EXPLORATION_INITIAL_EPS].value),
                learning_starts=self.experiment_config.hparams[agents_constants.DQN.LEARNING_STARTS].value,
                max_grad_norm=self.experiment_config.hparams[agents_constants.DQN.MAX_GRAD_NORM].value,
                gradient_steps=self.experiment_config.hparams[agents_constants.DQN.GRADIENT_STEPS].value,
                target_update_interval=(
                    self.experiment_config.hparams[agents_constants.DQN.TARGET_UPDATE_INTERVAL].value),
                buffer_size=self.experiment_config.hparams[agents_constants.DQN.BUFFER_SIZE].value
            )
            if self.experiment_config.player_type == PlayerType.ATTACKER:
                orig_env.set_model(model)

            # Train
            model.learn(total_timesteps=self.experiment_config.hparams[
                agents_constants.COMMON.NUM_TRAINING_TIMESTEPS].value, callback=cb)

            # Save policy
            exp_result = cb.exp_result
            ts = time.time()
            save_path = f"{self.experiment_config.output_dir}/dqn_policy_seed_{seed}_{ts}.zip"
            model.save(save_path)
            policy = DQNPolicy(
                model=model, simulation_name=self.simulation_env_config.name, save_path=save_path,
                states=self.simulation_env_config.state_space_config.states,
                actions=self.simulation_env_config.joint_action_space_config.action_spaces[
                    self.experiment_config.player_idx].actions, player_type=self.experiment_config.player_type,
                experiment_config=self.experiment_config,
                avg_R=exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN][-1])
            exp_result.policies[seed] = policy

            # Save policy metadata
            MetastoreFacade.save_dqn_policy(dqn_policy=policy)
            os.chmod(save_path, 0o777)

            # Save latest trace
            MetastoreFacade.save_simulation_trace(orig_env.get_traces()[-1])
            orig_env.reset_traces()

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
                seed_values = []
                for seed_idx in range(len(self.experiment_config.random_seeds)):
                    seed_values.append(value_vectors[seed_idx][i])
                avg_metrics.append(ExperimentUtil.mean_confidence_interval(
                    data=seed_values,
                    confidence=self.experiment_config.hparams[agents_constants.COMMON.CONFIDENCE_INTERVAL].value)[0])
                std_metrics.append(ExperimentUtil.mean_confidence_interval(
                    data=seed_values,
                    confidence=self.experiment_config.hparams[agents_constants.COMMON.CONFIDENCE_INTERVAL].value)[1])
            exp_result.avg_metrics[metric] = avg_metrics
            exp_result.std_metrics[metric] = std_metrics

        traces = orig_env.get_traces()
        if len(traces) > 0:
            MetastoreFacade.save_simulation_trace(traces[-1])
        return self.exp_execution

    def hparam_names(self) -> List[str]:
        """
        Gets the hyperparameters

        :return: a list with the hyperparameter names
        """
        return [constants.NEURAL_NETWORKS.NUM_NEURONS_PER_HIDDEN_LAYER,
                constants.NEURAL_NETWORKS.NUM_HIDDEN_LAYERS,
                agents_constants.COMMON.LEARNING_RATE, agents_constants.COMMON.BATCH_SIZE,
                agents_constants.COMMON.GAMMA,
                agents_constants.COMMON.NUM_TRAINING_TIMESTEPS, agents_constants.COMMON.EVAL_EVERY,
                agents_constants.COMMON.EVAL_BATCH_SIZE,
                constants.NEURAL_NETWORKS.DEVICE,
                agents_constants.COMMON.SAVE_EVERY, agents_constants.DQN.EXPLORATION_INITIAL_EPS,
                agents_constants.DQN.EXPLORATION_FINAL_EPS, agents_constants.DQN.EXPLORATION_FRACTION,
                agents_constants.DQN.MLP_POLICY, agents_constants.DQN.MAX_GRAD_NORM,
                agents_constants.DQN.GRADIENT_STEPS, agents_constants.DQN.N_EPISODES_ROLLOUT,
                agents_constants.DQN.TARGET_UPDATE_INTERVAL, agents_constants.DQN.LEARNING_STARTS,
                agents_constants.DQN.BUFFER_SIZE, agents_constants.DQN.DQN_BATCH_SIZE]


class DQNTrainingCallback(BaseCallback):
    """
    Callback for monitoring DQN training
    """
    def __init__(self, exp_result: ExperimentResult, seed: int, random_seeds: List[int],
                 training_job: TrainingJobConfig, exp_execution: ExperimentExecution,
                 max_steps: int, simulation_name: str,
                 states: List[State], actions: List[Action], player_type: PlayerType,
                 env: BaseEnv, experiment_config: ExperimentConfig, verbose=0,
                 eval_every: int = 100, eval_batch_size: int = 10, save_every: int = 10, save_dir: str = "",
                 L: int = 3, gym_env_name: str = ""):
        """
        Initializes the callback

        :param exp_result: the experiment result to populate
        :param seed: the random seed
        :param random_seeds: the list of all random seeds
        :param training_job: the training job
        :param exp_execution: the experiment execution
        :param max_steps: the maximum number of steps for evaluation
        :param simulation_name: the name of the simulation
        :param states: the list of states in the environment
        :param actions: the list of actions in the environment
        :param player_type: the type of the player
        :param verbose: whether logging should be verbose or not
        :param eval_every: how frequently to run the evaluation
        :param eval_batch_size: the batch size for evaluation
        :param save_every: how frequently to checkpoint the current model
        :param save_dir: the path to checkpoint models
        :param env: the training environment
        :param experiment_config: the experiment configuration
        :param L: num stops if a stopping environment
        :param gym_env_name: name of gym env
        """
        super(DQNTrainingCallback, self).__init__(verbose)
        self.states = states
        self.simulation_name = simulation_name
        self.iter = 0
        self.eval_every = eval_every
        self.eval_batch_size = eval_batch_size
        self.exp_result = exp_result
        self.seed = seed
        self.random_seeds = random_seeds
        self.training_job = training_job
        self.exp_execution = exp_execution
        self.max_steps = max_steps
        self.player_type = player_type
        self.actions = actions
        self.save_every = save_every
        self.save_dir = save_dir
        self.env: BaseEnv = env
        self.experiment_config = experiment_config
        self.L = L
        self.gym_env_name = gym_env_name

    def _on_training_start(self) -> None:
        """
        This method is called before the first rollout starts.
        """
        pass

    def _on_rollout_start(self) -> None:
        """
        A rollout is the collection of environment interaction
        using the current policy.
        This event is triggered before collecting new samples.
        """
        pass

    def _on_step(self) -> bool:
        """
        This method will be called by the model after each call to `env.step()`.

        For child callback (of an `EventCallback`), this will be called
        when the event is triggered.

        :return: (bool) If the callback returns False, training is aborted early.
        """
        if self.player_type == PlayerType.ATTACKER:
            self.env.set_model(self.model)
        return True

    def _on_training_end(self) -> None:
        """
        This event is triggered before exiting the `learn()` method.
        """
        pass

    def _on_rollout_end(self) -> None:
        """
        This event is triggered before updating the policy.
        """
        if self.iter % self.experiment_config.log_every == 0:
            Logger.__call__().get_logger().info(f"Training iteration: {self.iter}, seed:{self.seed}, "
                                                f"progress: {round(100*round(self.num_timesteps/self.max_steps,2),2)}%")
        ts = time.time()
        save_path = self.save_dir + f"/dqn_model{self.iter}_{ts}.zip"

        # Save model
        if self.iter % self.save_every == 0 and self.iter > 0:
            Logger.__call__().get_logger().info(f"Saving model to path: {save_path}")
            self.model.save(save_path)
            os.chmod(save_path, 0o777)

        # Eval model
        if self.iter % self.eval_every == 0:
            if self.player_type == PlayerType.ATTACKER:
                self.env.set_model(self.model)
            policy = DQNPolicy(
                model=self.model, simulation_name=self.simulation_name, save_path=save_path,
                states=self.states, player_type=self.player_type, actions=self.actions,
                experiment_config=self.experiment_config, avg_R=-1)
            o, _ = self.env.reset()
            max_horizon = self.experiment_config.hparams[agents_constants.COMMON.MAX_ENV_STEPS].value
            avg_rewards = []
            for i in range(self.eval_batch_size):
                o, _ = self.env.reset()
                done = False
                t = 0
                cumulative_reward = 0
                while not done and t <= max_horizon:
                    a = policy.action(o=o)
                    o, r, done, _, info = self.env.step(a)
                    cumulative_reward += r
                    t += 1
                    Logger.__call__().get_logger().debug(f"t:{t}, a1:{a}, r:{r}, info:{info}, done:{done}")
                avg_rewards.append(cumulative_reward)

            avg_R = np.mean(avg_rewards)
            policy.avg_R = avg_R
            Logger.__call__().get_logger().info(f"[EVAL] Training iteration: {self.iter}, Average R:{avg_R}")

            self.exp_result.all_metrics[self.seed][agents_constants.COMMON.AVERAGE_RETURN].append(round(avg_R, 3))
            self.env.reset()

            # Update training job
            total_steps_done = len(self.random_seeds) * self.max_steps
            steps_done = (self.random_seeds.index(self.seed)) * self.max_steps + self.num_timesteps
            progress = round(steps_done / total_steps_done, 2)
            self.training_job.progress_percentage = progress
            self.training_job.experiment_result = self.exp_result
            self.training_job.simulation_traces.append(self.env.get_traces()[-1])
            if len(self.training_job.simulation_traces) > self.training_job.num_cached_traces:
                self.training_job.simulation_traces = self.training_job.simulation_traces[1:]
            MetastoreFacade.update_training_job(training_job=self.training_job, id=self.training_job.id)

            # Update execution
            ts = time.time()
            self.exp_execution.timestamp = ts
            self.exp_execution.result = self.exp_result
            MetastoreFacade.update_experiment_execution(experiment_execution=self.exp_execution,
                                                        id=self.exp_execution.id)

        self.iter += 1
