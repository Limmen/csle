"""
MIT License

Copyright (c) 2019 CleanRL developers https://github.com/vwxyzjn/cleanrl
"""

from typing import Union, List, Optional, Callable, Tuple, Any
import random
import time
import gymnasium as gym
from gymnasium.wrappers.common import RecordEpisodeStatistics
from gymnasium.spaces.discrete import Discrete
import os
import numpy as np
import torch
import torch.optim as optim
import torch.nn.utils.clip_grad as clip_grad
from torch.distributions.categorical import Categorical
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
from csle_common.util.general_util import GeneralUtil
from csle_common.dao.simulation_config.base_env import BaseEnv
from csle_common.dao.training.ppo_policy import PPOPolicy
from csle_agents.agents.base.base_agent import BaseAgent
from csle_common.models.ppo_network import PPONetwork
import csle_agents.constants.constants as agents_constants


class PPGCleanAgent(BaseAgent):
    """
    A Phasic Policy Gradient agent using the implementation from CleanRL
    """

    def __init__(self, simulation_env_config: SimulationEnvConfig,
                 emulation_env_config: Union[None, EmulationEnvConfig], experiment_config: ExperimentConfig,
                 training_job: Optional[TrainingJobConfig] = None, save_to_metastore: bool = True) -> None:
        """
        Initializes the agent, and sets the hyperparameters as attributes of the class representing the agent.

        :param simulation_env_config: the simulation environment configuration
        :param emulation_env_config: the emulation environment configuration
        :param experiment_config: the experiment configuration
        :param training_job: the training job
        :param save_to_metastore: boolean flag indicating whether the results should be saved to the metastore or not
        """
        super(PPGCleanAgent, self).__init__(simulation_env_config=simulation_env_config,
                                            emulation_env_config=emulation_env_config,
                                            experiment_config=experiment_config)
        assert experiment_config.agent_type == AgentType.PPG_CLEAN
        self.training_job = training_job
        self.save_to_metastore = save_to_metastore
        config = self.simulation_env_config.simulation_env_input_config
        self.orig_env: BaseEnv = gym.make(self.simulation_env_config.gym_env_name, config=config)

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
        descr = f"Training of policies with Clean-PPG using " \
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

        # Training runs, one per seed
        for seed in self.experiment_config.random_seeds:

            # Train
            exp_result, env, model = self.run_ppg(exp_result=exp_result, seed=seed)

            # Save policy
            ts = time.time()
            save_path = f"{self.experiment_config.output_dir}/ppo_policy_seed_{seed}_{ts}.zip"
            model.save(save_path)
            policy = PPOPolicy(
                model=model, simulation_name=self.simulation_env_config.name, save_path=save_path,
                states=self.simulation_env_config.state_space_config.states,
                actions=self.simulation_env_config.joint_action_space_config.action_spaces[
                    self.experiment_config.player_idx].actions, player_type=self.experiment_config.player_type,
                experiment_config=self.experiment_config,
                avg_R=exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN][-1])
            exp_result.policies[seed] = policy

            # Save policy metadata
            if self.save_to_metastore:
                MetastoreFacade.save_ppo_policy(ppo_policy=policy)
                os.chmod(save_path, 0o777)

            # Save trace
            traces = env.get_traces()
            if len(traces) > 0 and self.save_to_metastore:
                MetastoreFacade.save_simulation_trace(traces[-1])
            env.reset_traces()

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
        return self.exp_execution

    def run_ppg(self, exp_result: ExperimentResult, seed: int) -> Tuple[ExperimentResult, BaseEnv, PPONetwork]:
        """
        Runs PPG with a given seed

        :param exp_result: the object to save the experiment results
        :param seed: the random seed
        :return: the updated experiment results, the environment, and the trained model
        """
        Logger.__call__().get_logger().info(f"[CleanPPG] Start training; seed: {seed}")
        clip_coef = self.experiment_config.hparams[agents_constants.PPG_CLEAN.CLIP_COEF].value
        adv_norm_fullbatch = self.experiment_config.hparams[agents_constants.PPG_CLEAN.ADV_NORM_FULLBATCH].value
        clip_vloss = self.experiment_config.hparams[agents_constants.PPG_CLEAN.CLIP_VLOSS].value
        ent_coef = self.experiment_config.hparams[agents_constants.PPG_CLEAN.ENT_COEF].value
        max_grad_norm = self.experiment_config.hparams[agents_constants.PPG_CLEAN.MAX_GRAD_NORM].value
        target_kl = self.experiment_config.hparams[agents_constants.PPG_CLEAN.TARGET_KL].value
        vf_coef = self.experiment_config.hparams[agents_constants.PPG_CLEAN.VF_COEF].value
        learning_rate = self.experiment_config.hparams[agents_constants.PPG_CLEAN.LEARNING_RATE].value
        num_steps = self.experiment_config.hparams[agents_constants.PPG_CLEAN.NUM_STEPS].value
        aux_batch_rollouts = self.experiment_config.hparams[agents_constants.PPG_CLEAN.AUX_BATCH_ROLLOUTS].value
        n_iteration = self.experiment_config.hparams[agents_constants.PPG_CLEAN.N_ITERATION].value
        anneal_lr = self.experiment_config.hparams[agents_constants.PPG_CLEAN.ANNEAL_LR].value
        gamma = self.experiment_config.hparams[agents_constants.COMMON.GAMMA].value
        gae_lambda = self.experiment_config.hparams[agents_constants.PPG_CLEAN.GAE_LAMBDA].value
        e_policy = self.experiment_config.hparams[agents_constants.PPG_CLEAN.E_POLICY].value
        beta_clone = self.experiment_config.hparams[agents_constants.PPG_CLEAN.BETA_CLONE].value
        n_aux_grad_accum = self.experiment_config.hparams[agents_constants.PPG_CLEAN.NUM_AUX_GRAD_ACCUM].value
        num_aux_rollouts = self.experiment_config.hparams[agents_constants.PPG_CLEAN.NUM_AUX_ROLLOUTS].value
        e_auxiliary = self.experiment_config.hparams[agents_constants.PPG_CLEAN.E_AUXILIARY].value
        num_minibatches = self.experiment_config.hparams[agents_constants.PPG_CLEAN.NUM_MINIBATCHES].value
        total_timesteps = self.experiment_config.hparams[agents_constants.PPG_CLEAN.TOTAL_STEPS].value

        envs = gym.vector.SyncVectorEnv([self.make_env() for _ in range(1)])

        # Setup training metrics
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

        # Create neural network
        device = torch.device(agents_constants.PPO_CLEAN.CUDA if torch.cuda.is_available() and cuda else
                              self.experiment_config.hparams[constants.NEURAL_NETWORKS.DEVICE].value)
        num_hidden_layers = self.experiment_config.hparams[constants.NEURAL_NETWORKS.NUM_HIDDEN_LAYERS].value
        hidden_layer_dim = self.experiment_config.hparams[constants.NEURAL_NETWORKS.NUM_NEURONS_PER_HIDDEN_LAYER].value
        input_dim = np.array(envs.single_observation_space.shape).prod()
        env: BaseEnv = self.orig_env
        action_space: Discrete = env.action_space
        action_dim = int(action_space.n)
        agent = PPONetwork(input_dim=input_dim, output_dim_critic=1, output_dim_action=action_dim,
                           num_hidden_layers=num_hidden_layers, hidden_layer_dim=hidden_layer_dim).to(device)
        optimizer = optim.Adam(agent.parameters(), lr=learning_rate, eps=1e-8)

        # seeding
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.backends.cudnn.deterministic = True

        # Storage setup
        obs = torch.zeros((num_steps, 1) + envs.single_observation_space.shape).to(device) # type: ignore
        actions = torch.zeros((num_steps, 1) + envs.single_action_space.shape).to(device) # type: ignore
        logprobs = torch.zeros((num_steps, 1)).to(device) # type: ignore
        rewards = torch.zeros((num_steps, 1)).to(device) # type: ignore
        horizons = []
        info_returns = []
        dones = torch.zeros((num_steps, 1)).to(device) # type: ignore
        values = torch.zeros((num_steps, 1)).to(device) # type: ignore
        aux_obs = torch.zeros((num_steps, aux_batch_rollouts) + envs.single_observation_space.shape, # type: ignore
                              dtype=torch.uint8)  # type: ignore
        aux_returns = torch.zeros((num_steps, aux_batch_rollouts))

        # Training loop
        global_step = 0
        start_time = time.time()
        next_obs = torch.Tensor(envs.reset()[0]).to(device)
        next_done = torch.zeros(1).to(device)
        batch_size = max(1, int(num_steps))
        num_iterations = max(1, total_timesteps // batch_size)
        minibatch_size = max(2, batch_size // num_minibatches)
        num_phases = max(num_iterations // batch_size, 1)
        aux_batch_rollouts = max(1, n_iteration)

        for phase in range(1, num_phases + 1):

            # POLICY PHASE
            for update in range(1, n_iteration + 1):
                # Annealing the rate if instructed to do so.
                if anneal_lr:
                    frac = 1.0 - (update - 1.0) / num_iterations
                    lrnow = frac * learning_rate
                    optimizer.param_groups[0]["lr"] = lrnow

                for step in range(0, num_steps):
                    global_step += 1 * 1
                    obs[step] = next_obs
                    dones[step] = next_done

                    # action logic
                    with torch.no_grad():
                        action, logprob, _, value = agent.get_action_and_value(next_obs)
                        values[step] = value.flatten()
                    actions[step] = action
                    logprobs[step] = logprob

                    # execute the game and log data.
                    next_obs, reward, done, info, info_d = envs.step(action.cpu().numpy()) # type: ignore
                    if done[0] and "final_info" in info_d:
                        horizons.append(info_d["final_info"][0][agents_constants.ENV_METRICS.TIME_HORIZON])
                        info_returns.append(info_d["final_info"][0][agents_constants.ENV_METRICS.RETURN])
                    rewards[step] = torch.tensor(reward).to(device).view(-1)
                    next_obs, next_done = torch.Tensor(next_obs).to(device), torch.Tensor(done).to(device)

                # bootstrap value if not done
                with torch.no_grad():
                    next_value = agent.get_value(next_obs).reshape(1, -1)
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
                b_obs = obs.reshape((-1,) + envs.single_observation_space.shape) # type: ignore
                b_logprobs = logprobs.reshape(-1)
                b_actions = actions.reshape((-1,) + envs.single_action_space.shape) # type: ignore
                b_advantages = advantages.reshape(-1)
                b_returns = returns.reshape(-1)
                b_values = values.reshape(-1)

                # PPG code does full batch advantage normalization
                if adv_norm_fullbatch:
                    b_advantages = (b_advantages - b_advantages.mean()) / (b_advantages.std() + 1e-8)

                # Optimizing the policy and value network
                b_inds = np.arange(batch_size)
                clipfracs = []
                for epoch in range(e_policy):
                    np.random.shuffle(b_inds)
                    for start in range(0, batch_size, minibatch_size):
                        end = start + minibatch_size
                        mb_inds = b_inds[start:end]

                        _, newlogprob, entropy, newvalue = agent.get_action_and_value( # type: ignore
                            b_obs[mb_inds], b_actions.long()[mb_inds]) # type: ignore
                        logratio = newlogprob - b_logprobs[mb_inds] # type: ignore
                        ratio = logratio.exp()

                        with torch.no_grad():
                            approx_kl = ((ratio - 1) - logratio).mean()
                            clipfracs += [((ratio - 1.0).abs() > clip_coef).float().mean().item()]

                        mb_advantages = b_advantages[mb_inds] # type: ignore

                        # Policy loss
                        pg_loss1 = -mb_advantages * ratio
                        pg_loss2 = -mb_advantages * torch.clamp(ratio, 1 - clip_coef, 1 + clip_coef)
                        pg_loss = torch.max(pg_loss1, pg_loss2).mean()

                        # Value loss
                        newvalue = newvalue.view(-1)
                        if clip_vloss:
                            v_loss_unclipped = (newvalue - b_returns[mb_inds]) ** 2 # type: ignore
                            v_clipped = b_values[mb_inds] + torch.clamp( # type: ignore
                                newvalue - b_values[mb_inds], -clip_coef, clip_coef) # type: ignore
                            v_loss_clipped = (v_clipped - b_returns[mb_inds]) ** 2 # type: ignore
                            v_loss_max = torch.max(v_loss_unclipped, v_loss_clipped) # type: ignore
                            v_loss = 0.5 * v_loss_max.mean() # type: ignore
                        else:
                            v_loss = 0.5 * ((newvalue - b_returns[mb_inds]) ** 2).mean() # type: ignore

                        entropy_loss = entropy.mean()
                        loss = pg_loss - ent_coef * entropy_loss + v_loss * vf_coef

                        optimizer.zero_grad()
                        loss.backward()
                        clip_grad.clip_grad_norm_(agent.parameters(), max_grad_norm)
                        optimizer.step()

                    if target_kl is not None and approx_kl > target_kl:
                        break

                # PPG Storage - Rollouts are saved without flattening for sampling full rollouts later:
                aux_obs = obs.cpu().clone().to(torch.uint8)
                aux_returns = returns.cpu().clone()

            # AUXILIARY PHASE
            aux_inds = np.arange(aux_batch_rollouts)

            # Build the old policy on the aux buffer before distilling to the network
            aux_pi = torch.zeros((num_steps, aux_batch_rollouts, envs.single_action_space.n)) # type: ignore
            for i, start in enumerate(range(0, aux_batch_rollouts, num_aux_rollouts)):
                end = start + num_aux_rollouts
                m_aux_obs = aux_obs[start:end].to(torch.float32).to(device)
                if len(m_aux_obs) > 0:
                    with torch.no_grad():
                        pi_logits = agent.get_pi(m_aux_obs).logits.cpu().clone()
                    aux_pi[start:end] = pi_logits
                del m_aux_obs

            for auxiliary_update in range(1, e_auxiliary + 1):
                np.random.shuffle(aux_inds)
                for i, start in enumerate(range(0, aux_batch_rollouts, num_aux_rollouts)):
                    end = start + num_aux_rollouts
                    try:
                        m_aux_obs = aux_obs[start:end].to(torch.float32).to(device)
                        if len(m_aux_obs) == 0:
                            continue
                        m_aux_returns = aux_returns[start:end].to(torch.float32).to(device)
                        new_pi, new_values, new_aux_values = agent.get_pi_value_and_aux_value(m_aux_obs)

                        new_values = new_values.view(-1)
                        new_aux_values = new_aux_values.view(-1)
                        old_pi_logits = aux_pi[start:end].to(device)
                        old_pi = Categorical(logits=old_pi_logits)
                        kl_loss = torch.distributions.kl_divergence(old_pi, new_pi).mean()

                        real_value_loss = 0.5 * ((new_values - m_aux_returns) ** 2).mean()
                        aux_value_loss = 0.5 * ((new_aux_values - m_aux_returns) ** 2).mean()
                        joint_loss = aux_value_loss + beta_clone * kl_loss

                        loss = (joint_loss + real_value_loss) / n_aux_grad_accum
                        loss.backward()

                        if (i + 1) % n_aux_grad_accum == 0:
                            clip_grad.clip_grad_norm_(agent.parameters(), max_grad_norm)
                            optimizer.step()
                            optimizer.zero_grad()  # This cannot be outside, else gradients won't accumulate

                    except RuntimeError as e:
                        raise Exception(
                            "if running out of CUDA memory, try a higher --n-aux-grad-accum, which trades more time "
                            "for less gpu memory") from e

                    del m_aux_obs, m_aux_returns

            # Logging
            time_elapsed_minutes = round((time.time() - start_time) / 60, 3)
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNTIME].append(time_elapsed_minutes)
            avg_R = round(float(np.mean(info_returns)), 3)
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN].append(round(avg_R, 3))
            avg_T = round(float(np.mean(horizons)), 3)
            exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_TIME_HORIZON].append(round(avg_T, 3))
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNTIME].append(time_elapsed_minutes)
            running_avg_J = ExperimentUtil.running_average(
                exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_RETURN],
                self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value)
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_RETURN].append(
                round(running_avg_J, 3))
            running_avg_T = ExperimentUtil.running_average(
                exp_result.all_metrics[seed][agents_constants.COMMON.AVERAGE_TIME_HORIZON],
                self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value)
            exp_result.all_metrics[seed][agents_constants.COMMON.RUNNING_AVERAGE_TIME_HORIZON].append(
                round(running_avg_T, 3))
            Logger.__call__().get_logger().info(
                f"[CleanPPG] Iteration: {phase}/{num_phases}, "
                f"avg R: {avg_R}, "
                f"R_avg_{self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value}:"
                f"{running_avg_J}, Avg T:{round(avg_T, 3)}, "
                f"Running_avg_{self.experiment_config.hparams[agents_constants.COMMON.RUNNING_AVERAGE].value}_T: "
                f"{round(running_avg_T, 3)}, "
                f"runtime: {time_elapsed_minutes} min")

        envs.close()
        base_env: BaseEnv = envs.envs[0].env.env.env  # type: ignore
        return exp_result, base_env, agent

    def make_env(self) -> Callable[[], RecordEpisodeStatistics[Any, Any]]:
        """
        Helper function for creating the environment to use for training

        :return: a function that creates the environment
        """

        def thunk() -> RecordEpisodeStatistics[Any, Any]:
            """
            Function for creating a new environment

            :return: the created environment
            """
            config = self.simulation_env_config.simulation_env_input_config
            orig_env: BaseEnv = gym.make(self.simulation_env_config.gym_env_name, config=config)
            env = RecordEpisodeStatistics(orig_env)
            return env

        return thunk

    def hparam_names(self) -> List[str]:
        """
        :return: a list with the hyperparameter names
        """
        return [constants.NEURAL_NETWORKS.NUM_NEURONS_PER_HIDDEN_LAYER,
                constants.NEURAL_NETWORKS.NUM_HIDDEN_LAYERS,
                agents_constants.COMMON.NUM_PARALLEL_ENVS, agents_constants.COMMON.BATCH_SIZE,
                agents_constants.COMMON.EVAL_EVERY, constants.NEURAL_NETWORKS.DEVICE,
                agents_constants.COMMON.SAVE_EVERY, agents_constants.COMMON.NUM_TRAINING_TIMESTEPS,
                agents_constants.PPG_CLEAN.TOTAL_STEPS, agents_constants.PPG_CLEAN.LEARNING_RATE,
                agents_constants.PPG_CLEAN.NUM_STEPS, agents_constants.PPG_CLEAN.ANNEAL_LR,
                agents_constants.PPG_CLEAN.GAMMA, agents_constants.PPG_CLEAN.GAE_LAMBDA,
                agents_constants.PPG_CLEAN.NUM_MINIBATCHES, agents_constants.PPG_CLEAN.ADV_NORM_FULLBATCH,
                agents_constants.PPG_CLEAN.CLIP_COEF, agents_constants.PPG_CLEAN.ENT_COEF,
                agents_constants.PPG_CLEAN.VF_COEF, agents_constants.PPG_CLEAN.MAX_GRAD_NORM,
                agents_constants.PPG_CLEAN.TARGET_KL, agents_constants.PPG_CLEAN.N_ITERATION,
                agents_constants.PPG_CLEAN.E_POLICY, agents_constants.PPG_CLEAN.E_AUXILIARY,
                agents_constants.PPG_CLEAN.BETA_CLONE, agents_constants.PPG_CLEAN.NUM_AUX_ROLLOUTS,
                agents_constants.PPG_CLEAN.NUM_AUX_GRAD_ACCUM, agents_constants.PPG_CLEAN.BATCH_SIZE,
                agents_constants.PPG_CLEAN.MINIBATCH_SIZE, agents_constants.PPG_CLEAN.NUM_ITERATIONS,
                agents_constants.PPG_CLEAN.NUM_PHASES, agents_constants.PPG_CLEAN.AUX_BATCH_ROLLOUTS,
                agents_constants.PPG_CLEAN.V_VALUE]
