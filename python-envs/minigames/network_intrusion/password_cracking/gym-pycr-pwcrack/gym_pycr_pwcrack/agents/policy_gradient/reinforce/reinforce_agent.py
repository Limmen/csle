from typing import List, Union
import torch
from torch.distributions import Categorical
from torch.utils.tensorboard import SummaryWriter
import numpy as np
import time
import tqdm
from gym_pycr_pwcrack.agents.models.fnn_w_softmax import FNNwithSoftmax
from gym_pycr_pwcrack.envs.pycr_pwcrack_env import PyCRPwCrackEnv
from gym_pycr_pwcrack.agents.config.pg_agent_config import PolicyGradientAgentConfig
from gym_pycr_pwcrack.agents.policy_gradient.pg_agent import PolicyGradientAgent
from gym_pycr_pwcrack.dao.experiment.experiment_result import ExperimentResult
from gym_pycr_pwcrack.envs.rendering.video.pycr_pwcrack_monitor import PycrPwCrackMonitor

class ReinforceAgent(PolicyGradientAgent):

    def __init__(self, env:PyCRPwCrackEnv, config: PolicyGradientAgentConfig):
        super(ReinforceAgent, self).__init__(env, config)
        self.policy_network = None
        self.loss_fn = None
        self.optimizer = None
        self.lr_decay = None
        self.tensorboard_writer = SummaryWriter(self.config.tensorboard_dir)
        if torch.cuda.is_available() and self.config.gpu:
            self.device = torch.device("cuda:" + str(self.config.gpu_id))
            self.config.logger.info("Running on the GPU")
        else:
            self.device = torch.device("cpu")
            self.config.logger.info("Running on the CPU")
        self.initialize_models()
        self.tensorboard_writer.add_hparams(self.config.hparams_dict(), {})
        self.machine_eps = np.finfo(np.float32).eps.item()

    def train(self) -> ExperimentResult:
        pass

    def eval(self) -> ExperimentResult:
        pass

    def initialize_models(self) -> None:
        """
        Initialize models
        :return: None
        """

        # Initialize models
        self.policy_network = FNNwithSoftmax(self.config.input_dim, self.config.output_dim,
                                             self.config.pi_hidden_dim,
                                             num_hidden_layers=self.config.pi_hidden_layers,
                                             hidden_activation=self.config.hidden_activation)
        self.policy_network.to(self.device)

        # Define Optimizer. The call to model.parameters() in the optimizer constructor will contain the learnable
        # parameters of the layers in the model
        if self.config.optimizer == "Adam":
            self.optimizer = torch.optim.Adam(self.policy_network.parameters(), lr=self.config.alpha)
        elif self.config.optimizer == "SGD":
            self.optimizer = torch.optim.SGD(self.policy_network.parameters(), lr=self.alpha)
        else:
            raise ValueError("Optimizer not recognized")

        # LR decay
        if self.config.lr_exp_decay:
            self.lr_decay = torch.optim.lr_scheduler.ExponentialLR(optimizer=self.optimizer,
                                                                   gamma=self.config.lr_decay_rate)


    def training_step(self, saved_rewards : List[List[float]], saved_log_probs : List[List[torch.Tensor]]) -> torch.Tensor:
        """
        Performs a training step of the Deep-Q-learning algorithm (implemented in PyTorch)

        :param saved_rewards list of rewards encountered in the latest episode trajectory
        :param saved_log_probs list of log-action probabilities (log p(a|s)) encountered in the latest episode trajectory
        :return: loss
        """

        policy_loss = []
        num_batches = len(saved_rewards)

        for batch in range(num_batches):
            R = 0
            returns = []

            # Create discounted returns. When an episode is finished we can go back and compute the observed cumulative
            # discounted reward by using the observed rewards
            for r in saved_rewards[batch][::-1]:
                R = r + self.config.gamma * R
                returns.insert(0, R)
            num_rewards = len(returns)

            # convert list to torch tensor
            returns = torch.tensor(returns)

            # normalize
            std = returns.std()
            if num_rewards < 2:
                std = 0
            returns = (returns - returns.mean()) / (std + self.machine_eps)

            # Compute PG "loss" which in reality is the expected reward, which we want to maximize with gradient ascent
            for log_prob, R in zip(saved_log_probs[batch], returns):
                # negative log prob since we are doing gradient descent (not ascent)
                policy_loss.append(-log_prob * R)

        # reset gradients
        self.optimizer.zero_grad()
        # expected loss over the batch
        policy_loss_total = torch.stack(policy_loss).sum()
        policy_loss = policy_loss_total/num_batches
        # perform backprop
        policy_loss.backward()
        # maybe clip gradient
        if self.config.clip_gradient:
            torch.nn.utils.clip_grad_norm_(self.policy_network.parameters(), 1)
        # gradient descent step
        self.optimizer.step()

        return policy_loss


    def train(self) -> ExperimentResult:
        """
        Runs the REINFORCE algorithm

        :return: Experiment result
        """
        self.config.logger.info("Starting Training")
        self.config.logger.info(self.config.to_str())
        if len(self.train_result.avg_episode_steps) > 0:
            self.config.logger.warning("starting training with non-empty result object")
        done = False
        obs = self.env.reset()
        state = self.update_state(obs=obs, state=[])

        # Tracking metrics
        episode_rewards = []
        episode_steps = []
        episode_avg_loss = []

        # Logging
        self.outer_train.set_description_str("[Train] epsilon:{:.2f},avg_R:{:.2f},"
                                             "avg_t:{:.2f}".format(self.config.epsilon, 0.0, 0.0))

        saved_log_probs_batch = []
        saved_rewards_batch = []

        # Training
        for iter in range(self.config.num_episodes):

            # Batch
            for episode in range(self.config.batch_size):
                episode_reward = 0
                episode_step = 0
                episode_loss = 0.0
                saved_log_probs = []
                saved_rewards = []
                while not done:
                    if self.config.render:
                        self.env.render(mode="human")

                    # Default initialization
                    action = 0

                    # Get predicted action
                    action, log_prob= self.get_action(state)
                    saved_log_probs.append(log_prob)

                    # Take a step in the environment
                    obs_prime, reward, done, _ = self.env.step(action)

                    # Update metrics
                    episode_reward += reward
                    saved_rewards.append(reward)
                    episode_step += 1

                    # Move to the next state
                    obs = obs_prime

                    state = self.update_state(obs=obs, state=state)

                # Render final frame
                if self.config.render:
                    self.env.render(mode="human")

                # Accumulate batch
                saved_log_probs_batch.append(saved_log_probs)
                saved_rewards_batch.append(saved_rewards)

                # Record episode metrics
                episode_rewards.append(episode_reward)
                episode_steps.append(episode_step)

                # Reset environment for the next episode and update game stats
                done = False
                obs = self.env.reset()
                state = self.update_state(obs=obs, state=[])

            # Perform Batch Policy Gradient updates
            loss = self.training_step(saved_rewards_batch, saved_log_probs_batch)
            episode_loss += loss.item()


            if self.config.batch_size > 0:
                episode_avg_loss.append(episode_loss / self.config.batch_size)
            else:
                episode_avg_loss.append(episode_loss)

            # Reset batch
            saved_log_probs_batch = []
            saved_rewards_batch = []

            # Decay LR after every iteration
            lr = self.config.alpha
            if self.config.lr_exp_decay:
                self.lr_decay.step()
                lr = self.lr_decay.get_lr()[0]

            # Log average metrics every <self.config.train_log_frequency> iterations
            if iter % self.config.train_log_frequency == 0:
                self.log_metrics(iteration=iter, result=self.train_result, episode_rewards=episode_rewards,
                                 episode_steps=episode_steps, episode_avg_loss=episode_avg_loss,
                                 eval=False, lr=lr)

                # Log values and gradients of the parameters (histogram summary) to tensorboard
                for tag, value in self.policy_network.named_parameters():
                    tag = tag.replace('.', '/')
                    self.tensorboard_writer.add_histogram(tag, value.data.cpu().numpy(), iter)
                    self.tensorboard_writer.add_histogram(tag + '/grad', value.grad.data.cpu().numpy(),
                                                          iter)

                episode_rewards = []
                episode_steps = []

            # Run evaluation every <self.config.eval_frequency> iterations
            if iter % self.config.eval_frequency == 0:
                self.eval(iter)

            # Save models every <self.config.checkpoint_frequency> iterations
            if iter % self.config.checkpoint_freq == 0:
                self.save_model()
                if self.config.save_dir is not None:
                    time_str = str(time.time())
                    self.train_result.to_csv(self.config.save_dir + "/" + time_str + "_train_results_checkpoint.csv")
                    self.eval_result.to_csv(self.config.save_dir + "/" + time_str + "_eval_results_checkpoint.csv")

            self.outer_train.update(1)

            # Anneal epsilon linearly
            self.anneal_epsilon()

        self.config.logger.info("Training Complete")

        # Final evaluation (for saving Gifs etc)
        self.eval(self.config.num_episodes-1, log=False)

        # Save networks
        self.save_model()

        # Save other game data
        if self.config.save_dir is not None:
            time_str = str(time.time())
            self.train_result.to_csv(self.config.save_dir + "/" + time_str + "_train_results_checkpoint.csv")
            self.eval_result.to_csv(self.config.save_dir + "/" + time_str + "_eval_results_checkpoint.csv")

        return self.train_result


    def get_action(self, state: np.ndarray) -> Union[int, torch.Tensor]:
        """
        Samples an action from the policy network

        :param state: the state to sample an action for
        :return: The sampled action id
        """
        state = torch.from_numpy(state.flatten()).float()

        # Move to GPU if using GPU
        state = state.to(self.device)

        # Calculate legal actions
        actions = list(range(self.env.num_actions))
        legal_actions = list(filter(lambda action: self.env.is_action_legal(action), actions))
        non_legal_actions = list(filter(lambda action: not self.env.is_action_legal(action), actions))

        # Forward pass using the current policy network to predict P(a|s)
        action_probs = self.policy_network(state)

        # Set probability of non-legal actions to 0
        action_probs_1 = action_probs.clone()
        if len(legal_actions) > 0 and len(non_legal_actions) < len(action_probs_1):
            action_probs_1[non_legal_actions] = 0

        # Use torch.distributions package to create a parameterizable probability distribution of the learned policy
        # PG uses a trick to turn the gradient into a stochastic gradient which we can sample from in order to
        # approximate the true gradient (which we can’t compute directly). It can be seen as an alternative to the
        # reparameterization trick
        policy_dist = Categorical(action_probs_1)

        # Sample an action from the probability distribution
        try:
            action = policy_dist.sample()
        except Exception as e:
            print("Nan values in distribution, consider using a lower learning rate or gradient clipping")
            print("legal actions: {}".format(legal_actions))
            print("non_legal actions: {}".format(non_legal_actions))
            print("action_probs: {}".format(action_probs))
            print("action_probs_1: {}".format(action_probs_1))
            print("state: {}".format(state))
            print("policy_dist: {}".format(policy_dist))
            action = 0

        # log_prob returns the log of the probability density/mass function evaluated at value.
        # save the log_prob as it will use later on for computing the policy gradient
        # policy gradient theorem says that the stochastic gradient of the expected return of the current policy is
        # the log gradient of the policy times the expected return, therefore we save the log of the policy distribution
        # now and use it later to compute the gradient once the episode has finished.
        log_prob = policy_dist.log_prob(action)

        return action.item(), log_prob

    def eval(self, train_episode, log=True) -> ExperimentResult:
        """
        Performs evaluation

        :param train_episode: the train episode to keep track of logging
        :param log: whether to log the result
        :return: None
        """
        self.config.logger.info("Starting Evaluation")
        time_str = str(time.time())

        if self.config.eval_episodes < 1:
            return

        done = False

        # Video config
        if self.config.video:
            if self.config.video_dir is None:
                raise AssertionError("Video is set to True but no video_dir is provided, please specify "
                                     "the video_dir argument")
            self.env = PycrPwCrackMonitor(self.env, self.config.video_dir + "/" + time_str, force=True,
                                          video_frequency=self.config.video_frequency)
            self.env.metadata["video.frames_per_second"] = self.config.video_fps

        # Tracking metrics
        episode_rewards = []
        episode_steps = []

        # Logging
        self.outer_eval = tqdm.tqdm(total=self.config.eval_episodes, desc='Eval Episode', position=1)
        self.outer_eval.set_description_str(
            "[Eval] avg_R:{:.2f},avg_t:{:.2f}".format(0.0, 0))

        # Eval
        obs = self.env.reset()
        state = self.update_state(obs=obs, state=[])

        for episode in range(self.config.eval_episodes):
            episode_reward = 0
            episode_step = 0
            while not done:
                if self.config.eval_render:
                    self.env.render()
                    time.sleep(self.config.eval_sleep)

                # Default initialization
                action = 0

                # Get action
                action, _ = self.get_action(state)

                # Take a step in the environment
                obs_prime, reward, done, _ = self.env.step(action)

                # Update state information and metrics
                episode_reward += reward
                episode_step += 1
                state = self.update_state(obs=obs, state=state)

            # Render final frame when game completed
            if self.config.eval_render:
                self.env.render()
                time.sleep(self.config.eval_sleep)
            self.config.logger.info("Eval episode: {}, Game ended after {} steps".format(episode, episode_step))

            # Record episode metrics
            episode_rewards.append(episode_reward)
            episode_steps.append(episode_step)

            # Log average metrics every <self.config.eval_log_frequency> episodes
            if episode % self.config.eval_log_frequency == 0 and log:
                self.log_metrics(iteration=train_episode, result=self.eval_result, episode_rewards=episode_rewards,
                                 episode_steps=episode_steps, eval = True)

            # Save gifs
            if self.config.gifs and self.config.video:
                self.env.generate_gif(self.config.gif_dir + "/episode_" + str(train_episode) + "_"
                                      + time_str + ".gif", self.config.video_fps)

            # Reset for new eval episode
            done = False
            obs = self.env.reset()
            state = self.update_state(obs=obs, state=state)
            self.outer_eval.update(1)

        # Log average eval statistics
        if log:
            self.log_metrics(iteration=train_episode, result=self.eval_result, episode_rewards=episode_rewards,
                             episode_steps=episode_steps, eval=True)

        self.env.close()
        self.config.logger.info("Evaluation Complete")
        return self.eval_result

    def save_model(self) -> None:
        """
        Saves the PyTorch Model Weights

        :return: None
        """
        time_str = str(time.time())
        if self.config.save_dir is not None:
            path = self.config.save_dir + "/" + time_str + "_policy_network.pt"
            self.config.logger.info("Saving policy-network to: {}".format(path))
            torch.save(self.policy_network.state_dict(), path)
        else:
            self.config.logger.warning("Save path not defined, not saving policy-networks to disk")