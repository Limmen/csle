"""
MIT License

Copyright (c) 2019 CleanRL developers https://github.com/vwxyzjn/cleanrl
"""

import random
from typing import Union, List, Optional
import time
from torch.distributions.categorical import Categorical
import gymnasium as gym
import os
import numpy as np
import math
import torch
import torch.nn as nn
import torch.optim as optim
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env.vec_monitor import VecMonitor
from stable_baselines3.common.vec_env.dummy_vec_env import DummyVecEnv
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import BaseCallback
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
from csle_common.dao.training.ppo_policy import PPOPolicy
from csle_common.dao.simulation_config.state import State
from csle_common.dao.simulation_config.action import Action
from csle_common.dao.training.player_type import PlayerType
from csle_common.util.general_util import GeneralUtil
from csle_common.dao.simulation_config.base_env import BaseEnv
from csle_agents.agents.base.base_agent import BaseAgent
import csle_agents.constants.constants as agents_constants


def layer_init(layer, std=np.sqrt(2), bias_const=0.0):
    torch.nn.init.orthogonal_(layer.weight, std)
    torch.nn.init.constant_(layer.bias, bias_const)
    return layer

class Agent(nn.Module):
    def __init__(self, envs):
        super().__init__()
        self.critic = nn.Sequential(
            layer_init(nn.Linear(np.array(envs.single_observation_space.shape).prod(), 64)),
            nn.Tanh(),
            layer_init(nn.Linear(64, 64)),
            nn.Tanh(),
            layer_init(nn.Linear(64, 1), std=1.0),
        )
        self.actor = nn.Sequential(
            layer_init(nn.Linear(np.array(envs.single_observation_space.shape).prod(), 64)),
            nn.Tanh(),
            layer_init(nn.Linear(64, 64)),
            nn.Tanh(),
            layer_init(nn.Linear(64, envs.single_action_space.n), std=0.01),
        )


    def get_value(self, x):
        return self.critic(x)

    def get_action_and_value(self, x, action=None):
        logits = self.actor(x)
        probs = Categorical(logits=logits)
        if action is None:
            action = probs.sample()
        return action, probs.log_prob(action), probs.entropy(), self.critic(x)

class PPOCleanAgent(BaseAgent):
    """
    A PPO agent using the implementation from CleanRL
    """

    def __init__(self, simulation_env_config: SimulationEnvConfig,
                 emulation_env_config: Union[None, EmulationEnvConfig], experiment_config: ExperimentConfig,
                 training_job: Optional[TrainingJobConfig] = None, save_to_metastore: bool = True):
        """
        Intializes the agent

        :param simulation_env_config: the simulation environment configuration
        :param emulation_env_config: the emulation environment configuration
        :param experiment_config: the experiment configuration
        :param training_job: the training job
        :param save_to_metastore: boolean flag indicating whether the results should be saved to the metastore or not
        """
        super(PPOCleanAgent, self).__init__(simulation_env_config=simulation_env_config,
                                            emulation_env_config=emulation_env_config,
                                            experiment_config=experiment_config)
        assert experiment_config.agent_type == AgentType.PPO
        self.training_job = training_job
        self.save_to_metastore = save_to_metastore

    def make_env(self, env_id, seed, idx, run_name, capture_video=False):
        def thunk():
            # print(env_id)
            if capture_video and idx == 0:
                env = gym.make(env_id)
                env = gym.wrappers.RecordVideo(env, f"videos/{run_name}")
            else:
                env = gym.make(env_id)
            # print(env)
            env = gym.wrappers.RecordEpisodeStatistics(env)
            # env.seed(seed)
            # env.action_space.seed(seed)
            # env.observation_space.seed(seed)
            return env

        return thunk

    

    def train(self) -> ExperimentExecution:
        """
        Runs the training process

        :return: the results
        """
        pid = os.getpid()

        # Setup experiment metrics
        exp_result = ExperimentResult()
        exp_result.plot_metrics.append(agents_constants.COMMON.AVERAGE_RETURN)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_RETURN)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON)
        exp_result.plot_metrics.append(agents_constants.COMMON.AVERAGE_TIME_HORIZON)
        exp_result.plot_metrics.append(agents_constants.COMMON.AVERAGE_UPPER_BOUND_RETURN)
        exp_result.plot_metrics.append(agents_constants.COMMON.AVERAGE_RANDOM_RETURN)
        exp_result.plot_metrics.append(agents_constants.COMMON.AVERAGE_HEURISTIC_RETURN)
        exp_result.plot_metrics.append(agents_constants.COMMON.RUNTIME)
        descr = f"Training of policies with PPO using " \
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
            training_job_id = -1
            if self.save_to_metastore:
                training_job_id = MetastoreFacade.save_training_job(training_job=self.training_job)
            self.training_job.id = training_job_id
        else:
            self.training_job.pid = pid
            self.training_job.progress_percentage = 0
            self.training_job.experiment_result = exp_result
            if self.save_to_metastore:
                MetastoreFacade.update_training_job(training_job=self.training_job, id=self.training_job.id)

        # Setup experiment execution
        ts = time.time()
        emulation_name = ""
        if self.emulation_env_config is not None:
            emulation_name = self.emulation_env_config.name
        simulation_name = self.simulation_env_config.name
        self.exp_execution = ExperimentExecution(
            result=exp_result, config=self.experiment_config, timestamp=ts,
            emulation_name=emulation_name, simulation_name=simulation_name, descr=descr,
            log_file_path=self.training_job.log_file_path)
        exp_execution_id = -1
        if self.save_to_metastore:
            exp_execution_id = MetastoreFacade.save_experiment_execution(self.exp_execution)
        self.exp_execution.id = exp_execution_id


        # size- and parameter setup of run
        num_steps = self.experiment_config.hparams[agents_constants.COMMON.NUM_TRAINING_TIMESTEPS].value
        
        num_envs = self.experiment_config.hparams[agents_constants.COMMON.NUM_PARALLEL_ENVS].value

        batch_size = int(num_envs * num_steps)
        total_timesteps = batch_size * 10
        num_minibatches = 4
        minibatch_size = int(batch_size // num_minibatches)
        num_iterations = total_timesteps // batch_size
        update_epochs = 4
        clip_coef = 0.2
        clip_vloss = True
        norm_adv = True
        vf_coef = 0.5
        ent_coef = 0.01
        max_grad_norm = 0.5
        target_kl = None
        # Training runs, one per seed
        for seed in self.experiment_config.random_seeds:

            self.simulation_env_config.name = "JohnDoe"
            envs = gym.vector.SyncVectorEnv([self.make_env(env_id=self.simulation_env_config.gym_env_name, seed=seed + i, idx=i, run_name=self.simulation_env_config.name) for i in range(num_envs)])

            self.start: float = time.time()
            exp_result.all_metrics[seed] = {}
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_TIME_HORIZON] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_UPPER_BOUND_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RANDOM_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_HEURISTIC_RETURN] = []
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNTIME] = []
            ExperimentUtil.set_seed(seed)
            cuda = False
            device = torch.device("cuda" if torch.cuda.is_available() and cuda else "cpu")
            model = Agent(envs=envs).to(device)
            # seeding
            random.seed(seed)
            np.random.seed(seed)
            torch.manual_seed(seed)
            torch_deterministic = True
            torch.backends.cudnn.deterministic = torch_deterministic

            # here, I exclude the writer-init


            # Setup gym environment
            # perhaps the right params are in the config
            config = self.simulation_env_config.simulation_env_input_config
            orig_env: BaseEnv = gym.make(self.simulation_env_config.gym_env_name)
            learning_rate = self.experiment_config.hparams[agents_constants.COMMON.LEARNING_RATE].value
            gamma = self.experiment_config.hparams[agents_constants.COMMON.GAMMA].value
            gae_lambda = self.experiment_config.hparams[agents_constants.COMMON.GAMMA].value
            obs = torch.zeros((num_steps, num_envs) + envs.single_observation_space.shape).to(device)
            actions = torch.zeros((num_steps, num_envs) + envs.single_action_space.shape).to(device)
            logprobs = torch.zeros((num_steps, num_envs)).to(device)
            rewards = torch.zeros((num_steps, num_envs)).to(device)
            dones = torch.zeros((num_steps, num_envs)).to(device)
            values = torch.zeros((num_steps, num_envs)).to(device)

            # TRY NOT TO MODIFY: start the game
            global_step = 0
            start_time = time.time()
            next_obs, _ = envs.reset(seed=seed)
            next_obs = torch.Tensor(next_obs).to(device)
            next_done = torch.zeros(num_envs).to(device)


            # model.cpu()

            optimizer = optim.Adam(model.parameters(), lr=learning_rate, eps=1e-5)

            for iteration in range(1, num_iterations + 1):
                # Annealing the rate if instructed to do so.
                anneal_lr = True
                if anneal_lr:
                    frac = 1.0 - (iteration - 1.0) / num_iterations
                    lrnow = frac * learning_rate
                    optimizer.param_groups[0]["lr"] = lrnow
                for step in range(0, num_steps):
                    global_step += num_envs
                    obs[step] = next_obs
                    dones[step] = next_done
                    # ALGO LOGIC: action logic
                    with torch.no_grad():
                        action, logprob, _, value = model.get_action_and_value(next_obs)
                        values[step] = value.flatten()
                    actions[step] = action
                    logprobs[step] = logprob  

                    # TRY NOT TO MODIFY: execute the game and log data.
                    next_obs, reward, terminations, truncations, infos = envs.step(action.cpu().numpy())
                    next_done = np.logical_or(terminations, truncations)
                    rewards[step] = torch.tensor(reward).to(device).view(-1)
                    next_obs, next_done = torch.Tensor(next_obs).to(device), torch.Tensor(next_done).to(device)

                    if "final_info" in infos:
                        for info in infos["final_info"]:
                            if info and "episode" in info:
                                pass
                                print(f"global_step={global_step}, episodic_return={info['episode']['r']}")

                # bootstrap value if not done
                with torch.no_grad():
                    next_value = model.get_value(next_obs).reshape(1, -1)
                    advantages = torch.zeros_like(rewards).to(device)
                    lastgaelam = 0
                    for t in reversed(range(num_steps)):
                        if t == num_steps - 1:
                            nextnonterminal = 1.0 - next_done
                            nextvalues = next_value
                        else:
                            nextnonterminal = 1.0 - dones[t + 1]
                            nextvalues = values[t + 1]
                        delta = rewards[t] + gamma * nextvalues * nextnonterminal - values[t]
                        advantages[t] = lastgaelam = delta + gamma * gae_lambda * nextnonterminal * lastgaelam
                    returns = advantages + values

                # flatten the batch
                b_obs = obs.reshape((-1,) + envs.single_observation_space.shape)
                b_logprobs = logprobs.reshape(-1)
                b_actions = actions.reshape((-1,) + envs.single_action_space.shape)
                b_advantages = advantages.reshape(-1)
                b_returns = returns.reshape(-1)
                b_values = values.reshape(-1)

                # Optimizing the policy and value network
                b_inds = np.arange(batch_size)
                clipfracs = []
                for epoch in range(update_epochs):
                    print(epoch)
                    np.random.shuffle(b_inds)
                    for start in range(0, batch_size, minibatch_size):
                        end = start + minibatch_size
                        mb_inds = b_inds[start:end]

                        _, newlogprob, entropy, newvalue = model.get_action_and_value(b_obs[mb_inds], b_actions.long()[mb_inds])
                        logratio = newlogprob - b_logprobs[mb_inds]
                        ratio = logratio.exp()

                        with torch.no_grad():
                            # calculate approx_kl http://joschu.net/blog/kl-approx.html
                            old_approx_kl = (-logratio).mean()
                            approx_kl = ((ratio - 1) - logratio).mean()
                            clipfracs += [((ratio - 1.0).abs() > clip_coef).float().mean().item()]

                        mb_advantages = b_advantages[mb_inds]
                        if norm_adv:
                            mb_advantages = (mb_advantages - mb_advantages.mean()) / (mb_advantages.std() + 1e-8)

                        # Policy loss
                        pg_loss1 = -mb_advantages * ratio
                        pg_loss2 = -mb_advantages * torch.clamp(ratio, 1 - clip_coef, 1 + clip_coef)
                        pg_loss = torch.max(pg_loss1, pg_loss2).mean()

                        # Value loss
                        newvalue = newvalue.view(-1)
                        if clip_vloss:
                            v_loss_unclipped = (newvalue - b_returns[mb_inds]) ** 2
                            v_clipped = b_values[mb_inds] + torch.clamp(
                                newvalue - b_values[mb_inds],
                                -clip_coef,
                                clip_coef,
                            )
                            v_loss_clipped = (v_clipped - b_returns[mb_inds]) ** 2
                            v_loss_max = torch.max(v_loss_unclipped, v_loss_clipped)
                            v_loss = 0.5 * v_loss_max.mean()
                        else:
                            v_loss = 0.5 * ((newvalue - b_returns[mb_inds]) ** 2).mean()

                        entropy_loss = entropy.mean()
                        loss = pg_loss - ent_coef * entropy_loss + v_loss * vf_coef

                        optimizer.zero_grad()
                        loss.backward()
                        nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm)
                        optimizer.step()

                    if target_kl is not None and approx_kl > target_kl:
                        break

                y_pred, y_true = b_values.cpu().numpy(), b_returns.cpu().numpy()
                var_y = np.var(y_true)
                explained_var = np.nan if var_y == 0 else 1 - np.var(y_true - y_pred) / var_y

                # TRY NOT TO MODIFY: record rewards for plotting purposes

                print("SPS:", int(global_step / (time.time() - start_time)))
            envs.close()

    def hparam_names(self) -> List[str]:
        """
        :return: a list with the hyperparameter names
        """
        return [constants.NEURAL_NETWORKS.NUM_NEURONS_PER_HIDDEN_LAYER,
                constants.NEURAL_NETWORKS.NUM_HIDDEN_LAYERS,
                agents_constants.PPO.STEPS_BETWEEN_UPDATES,
                agents_constants.COMMON.LEARNING_RATE, agents_constants.COMMON.BATCH_SIZE,
                agents_constants.COMMON.GAMMA, agents_constants.PPO.GAE_LAMBDA, agents_constants.PPO.CLIP_RANGE,
                agents_constants.PPO.CLIP_RANGE_VF, agents_constants.PPO.ENT_COEF,
                agents_constants.PPO.VF_COEF, agents_constants.PPO.MAX_GRAD_NORM, agents_constants.PPO.TARGET_KL,
                agents_constants.COMMON.NUM_TRAINING_TIMESTEPS, agents_constants.COMMON.EVAL_EVERY,
                agents_constants.COMMON.EVAL_BATCH_SIZE, constants.NEURAL_NETWORKS.DEVICE,
                agents_constants.COMMON.SAVE_EVERY]