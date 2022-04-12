from typing import Union, List, Dict
import time
import gym
import os
import numpy as np
import csle_common.constants.constants as constants
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.experiment_execution import ExperimentExecution
from csle_common.dao.training.experiment_result import ExperimentResult
from csle_common.dao.training.agent_type import AgentType
from csle_agents.base.base_agent import BaseAgent
from csle_common.util.experiment_util import ExperimentUtil
from csle_common.logging.log import Logger
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.jobs.training_job_config import TrainingJobConfig
from csle_common.dao.training.ppo_policy import PPOPolicy
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import BaseCallback


class PPOAgent(BaseAgent):
    """
    A PPO agent using the implementation from OpenAI baselines
    """
    def __init__(self, simulation_env_config: SimulationEnvConfig,
                 emulation_env_config: Union[None, EmulationEnvConfig], experiment_config: ExperimentConfig):
        super(PPOAgent, self).__init__(simulation_env_config=simulation_env_config, emulation_env_config=emulation_env_config,
                                       experiment_config=experiment_config)
        assert experiment_config.agent_type == AgentType.PPO

    def train(self) -> ExperimentExecution:
        pid = os.getpid()
        training_job = TrainingJobConfig(simulation_env_name=self.simulation_env_config.name,
                                         experiment_config=self.experiment_config, average_r=-1,
                                         progress_percentage=0, pid=pid)
        training_job_id = MetastoreFacade.save_training_job(training_job=training_job)
        training_job.id = training_job_id
        config = self.simulation_env_config.simulation_env_input_config
        env = gym.make(self.simulation_env_config.gym_env_name, config=config)
        env = Monitor(env)
        exp_result = ExperimentResult()
        exp_result.plot_metrics.append("average_reward")
        for seed in self.experiment_config.random_seeds:
            exp_result.all_metrics[seed] = {}
            exp_result.all_metrics[seed]["average_reward"] = []
            ExperimentUtil.set_seed(seed)
            cb = PPOTrainingCallback(eval_every=self.experiment_config.hparams["eval_every"].value,
                                     eval_batch_size=self.experiment_config.hparams["eval_batch_size"].value,
                                     random_seeds=self.experiment_config.random_seeds, training_job=training_job,
                                     max_steps=self.experiment_config.hparams["num_training_timesteps"].value,
                                     seed=seed, exp_result=exp_result, simulation_name=self.simulation_env_config.name)
            policy_kwargs = dict(
                net_arch=[self.experiment_config.hparams[
                              "num_neurons_per_hidden_layer"].value]*self.experiment_config.hparams[
                    "num_hidden_layers"].value)
            model = PPO(
                "MlpPolicy", env, verbose=0, policy_kwargs=policy_kwargs,
                n_steps=self.experiment_config.hparams["steps_between_updates"].value,
                batch_size=self.experiment_config.hparams["batch_size"].value,
                learning_rate=self.experiment_config.hparams["learning_rate"].value,
                seed=seed, device=self.experiment_config.hparams["device"].value,
                gamma=self.experiment_config.hparams["gamma"].value,
                gae_lambda=self.experiment_config.hparams["gae_lambda"].value,
                clip_range=self.experiment_config.hparams["clip_range"].value,
                clip_range_vf=self.experiment_config.hparams["clip_range_vf"].value,
                ent_coef=self.experiment_config.hparams["ent_coef"].value,
                vf_coef=self.experiment_config.hparams["vf_coef"].value,
                max_grad_norm=self.experiment_config.hparams["max_grad_norm"].value,
                target_kl=self.experiment_config.hparams["target_kl"].value,
            )
            model.learn(total_timesteps=self.experiment_config.hparams["num_training_timesteps"].value, callback=cb)
            exp_result=cb.exp_result
            ts = time.time()
            save_path = f"{constants.LOGGING.DEFAULT_LOG_DIR}/ppo_policy_seed_{seed}_{ts}.zip"
            model.save(save_path)
            exp_result.policies[seed] = PPOPolicy(model=model, simulation_name=self.simulation_env_config.name,
                                                  save_path=save_path)
            os.chmod(save_path, 0o777)

        # Calculate average and std metrics
        exp_result.avg_metrics = {}
        exp_result.std_metrics = {}
        for metric in exp_result.all_metrics[self.experiment_config.random_seeds[0]].keys():
            running_avg = 100
            confidence=0.95
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
                std_metrics.append(ExperimentUtil.mean_confidence_interval(data=seed_values, confidence=confidence)[0])
            exp_result.avg_metrics[metric] = avg_metrics
            exp_result.std_metrics[metric] = std_metrics

        ts = time.time()
        emulation_name = None
        if self.emulation_env_config is not None:
            emulation_name = self.emulation_env_config.name
        simulation_name = self.simulation_env_config.name
        descr = f"Training of policies with PPO using " \
                f"simulation:{self.simulation_env_config.name}"
        exp_execution = ExperimentExecution(result=exp_result, config=self.experiment_config, timestamp=ts,
                                            emulation_name=emulation_name, simulation_name=simulation_name,
                                            descr=descr)
        traces = env.get_traces()
        if len(traces) > 0:
            MetastoreFacade.save_simulation_trace(traces[-1])
        MetastoreFacade.remove_training_job(training_job)
        return exp_execution

    def hparam_names(self) -> List[str]:
        """
        :return: a list with the hyperparameter names
        """
        return ["num_neurons_per_hidden_layer", "num_hidden_layers", "steps_between_updates",
                "learning_rate", "batch_size", "gamma", "gae_lambda", "clip_range", "clip_range_vf", "ent_coef",
                "vf_coef", "max_grad_norm", "target_kl", "num_training_timesteps", "eval_every",
                "eval_batch_size", "device"]


class PPOTrainingCallback(BaseCallback):
    """
    Callback for monitoring PPO training
    """
    def __init__(self, exp_result: ExperimentResult, seed: int, random_seeds: List[int],
                 training_job: TrainingJobConfig, max_steps: int, simulation_name: str,
                 verbose=0,
                 eval_every: int = 100, eval_batch_size: int = 10):
        super(PPOTrainingCallback, self).__init__(verbose)
        self.simulation_name = simulation_name
        self.iter = 0
        self.eval_every = eval_every
        self.eval_batch_size = eval_batch_size
        self.exp_result = exp_result
        self.seed = seed
        self.random_seeds = random_seeds
        self.training_job = training_job
        self.max_steps = max_steps

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
        Logger.__call__().get_logger().info(f"Training iteration: {self.iter}, seed:{self.seed}, "
                                            f"progress: {100*round(self.num_timesteps/self.max_steps,2)}%")
        if self.iter % self.eval_every == 0:
            ts = time.time()
            policy = PPOPolicy(model=self.model, simulation_name=self.simulation_name,
                               save_path=f"{constants.LOGGING.DEFAULT_LOG_DIR}/ppo_model{self.iter}_{ts}.zip")
            self.model.save(policy.save_path)
            os.chmod(policy.save_path, 0o777)
            o = self.training_env.reset()
            max_horizon = 200
            avg_rewards = []
            for i in range(self.eval_batch_size):
                done = False
                t = 0
                cumulative_reward = 0
                while not done and t <= max_horizon:
                    a = policy.action(o=o)
                    o, r, done, info = self.training_env.step(a)
                    cumulative_reward +=r
                    t+= 1
                    # print(f"t:{t}, a1:{a}, r:{r}, info:{info}, done:{done}")
                avg_rewards.append(cumulative_reward)
            avg_R = np.mean(avg_rewards)
            Logger.__call__().get_logger().info(f"[EVAL] Training iteration: {self.iter}, Average R:{avg_R}")
            self.exp_result.all_metrics[self.seed]["average_reward"].append(round(avg_R, 3))
            self.training_env.reset()

            # Update training job
            total_steps_done = len(self.random_seeds)*self.max_steps
            steps_done = (self.random_seeds.index(self.seed))*self.max_steps + self.num_timesteps
            progress = round(steps_done/total_steps_done,2)
            self.training_job.progress_percentage = progress
            self.training_job.average_r = round(avg_R,3)
            MetastoreFacade.update_training_job(training_job=self.training_job, id=self.training_job.id)
        self.iter += 1