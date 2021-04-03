"""
Abstract Train Agent
"""
import numpy as np
import logging
import random
import torch
from abc import ABC, abstractmethod
from gym_pycr_ctf.agents.config.agent_config import AgentConfig
from gym_pycr_ctf.dao.experiment.experiment_result import ExperimentResult
from gym_pycr_ctf.dao.agent.train_mode import TrainMode
from gym_pycr_ctf.dao.agent.agent_type import AgentType

class TrainAgent(ABC):
    """
    Abstract Train Agent
    """
    def __init__(self, env, attacker_config: AgentConfig,
                 defender_config: AgentConfig,
                 eval_env, train_mode : TrainMode = TrainMode.TRAIN_ATTACKER):
        """
        Initialize environment and hyperparameters

        :param env: the training env
        :param attacker_config: the configuration
        :param eval_env: the eval env
        """
        self.env = env
        self.eval_env = eval_env
        self.attacker_config = attacker_config
        self.defender_config = defender_config
        self.train_result = ExperimentResult()
        self.eval_result = ExperimentResult()
        self.train_mode=train_mode
        #self.outer_train = tqdm.tqdm(total=self.config.num_iterations, desc='Train Episode', position=0)
        if self.attacker_config is None:
            self.attacker_config = self.defender_config
        if self.attacker_config.logger is None:
            self.attacker_config.logger = logging.getLogger('Train Agent - Attacker')
        random.seed(self.attacker_config.random_seed)
        np.random.seed(self.attacker_config.random_seed)
        torch.manual_seed(self.attacker_config.random_seed)

        if self.defender_config is None:
            self.defender_config = self.attacker_config
        if self.defender_config.logger is None:
            self.defender_config.logger = logging.getLogger('Train Agent - Defender')
        random.seed(self.defender_config.random_seed)
        np.random.seed(self.defender_config.random_seed)
        torch.manual_seed(self.defender_config.random_seed)

        if self.defender_config.attacker_opponent_baseline_type is not None and self.train_mode != TrainMode.SELF_PLAY:
            self.attacker_opponent_type = AgentType(self.defender_config.attacker_opponent_baseline_type)
        if self.attacker_config.defender_opponent_baseline_type is not None and self.train_mode != TrainMode.SELF_PLAY:
            self.defender_opponent_type = AgentType(self.attacker_config.defender_opponent_baseline_type)

    def log_action_dist_attacker(self, dist):
        log_str = " Initial State Action Dist for Attacker: ["
        dist_str = ",".join(list(map(lambda x: str(x), dist.data.cpu().numpy().tolist())))
        log_str = log_str + dist_str + "]"
        self.attacker_config.logger.info(log_str)

    def log_action_dist_defender(self, dist):
        log_str = " Initial State Action Dist for Defender: ["
        dist_str = ",".join(list(map(lambda x: str(x), dist.data.cpu().numpy().tolist())))
        log_str = log_str + dist_str + "]"
        self.defender_config.logger.info(log_str)

    def log_metrics_attacker(self, iteration: int, result: ExperimentResult, episode_rewards: list,
                             episode_steps: list, episode_avg_loss: list = None,
                             eval: bool = False, lr: float = None, total_num_episodes : int = 0) -> None:
        """
        Logs average metrics for the last <self.config.log_frequency> episodes

        :param iteration: the training iteration (equivalent to episode if batching is not used)
        :param result: the result object to add the results to
        :param episode_rewards: list of attacker episode rewards for the last <self.config.log_frequency> episodes
        :param episode_steps: list of episode steps for the last <self.config.log_frequency> episodes
        :param episode_avg_loss: list of episode attacker loss for the last <self.config.log_frequency> episodes
        :param eval: boolean flag whether the metrics are logged in an evaluation context.
        :param lr: the learning rate of the attacker
        :param total_num_episodes: number of training episodes
        :return: None
        """
        avg_episode_rewards = np.mean(episode_rewards)
        if lr is None:
            lr = 0.0
        if not eval and episode_avg_loss is not None:
            avg_episode_loss = np.mean(episode_avg_loss)
        else:
            avg_episode_loss = 0.0

        avg_episode_steps = np.mean(episode_steps)
        if eval:
            log_str = "[Eval] iter:{},avg_a_R:{:.2f},avg_t:{:.2f},lr:{:.2E}".format(
                iteration, avg_episode_rewards, avg_episode_steps, lr)
            self.outer_eval.set_description_str(log_str)
        else:
            log_str = "[Train] iter: {:.2f} epsilon:{:.2f},avg_R:{:.2f},avg_t:{:.2f}," \
                      "loss:{:.6f},lr:{:.2E},episode:{}".format(
                iteration, self.attacker_config.epsilon, avg_episode_rewards, avg_episode_steps, avg_episode_loss, lr,
                total_num_episodes)
            self.outer_train.set_description_str(log_str)
        self.attacker_config.logger.info(log_str)
        if self.attacker_config.tensorboard:
            self.log_tensorboard_attacker(iteration, avg_episode_rewards, avg_episode_steps,
                                          avg_episode_loss, self.attacker_config.epsilon, lr, eval=eval)

        result.avg_episode_steps.append(avg_episode_steps)
        result.avg_episode_rewards.append(avg_episode_rewards)
        result.epsilon_values.append(self.attacker_config.epsilon)
        result.avg_episode_loss.append(avg_episode_loss)
        result.lr_list.append(lr)

    def log_tensorboard_attacker(self, episode: int, avg_episode_rewards: float,
                                 avg_episode_steps: float, episode_avg_loss: float,
                                 epsilon: float, lr: float, eval=False) -> None:
        """
        Log metrics to tensorboard

        :param episode: the episode
        :param avg_episode_rewards: the average attacker episode reward
        :param avg_episode_steps: the average number of episode steps
        :param episode_avg_loss: the average episode loss
        :param epsilon: the exploration rate
        :param lr: the learning rate of the attacker
        :param eval: boolean flag whether eval or not
        :return: None
        """
        train_or_eval = "eval" if eval else "train"
        self.tensorboard_writer.add_scalar('avg_episode_rewards/' + train_or_eval,
                                           avg_episode_rewards, episode)
        self.tensorboard_writer.add_scalar('episode_steps/' + train_or_eval, avg_episode_steps, episode)
        self.tensorboard_writer.add_scalar('episode_avg_loss/' + train_or_eval, episode_avg_loss, episode)
        self.tensorboard_writer.add_scalar('epsilon', epsilon, episode)
        if not eval:
            self.tensorboard_writer.add_scalar('lr', lr, episode)

    def anneal_epsilon(self) -> None:
        """
        Anneals the exploration rate slightly until it reaches the minimum value

        :return: None
        """
        if self.attacker_config.epsilon > self.attacker_config.min_epsilon:
            self.attacker_config.epsilon = self.attacker_config.epsilon * self.attacker_config.epsilon_decay

    def update_state(self, obs: np.ndarray = None, state: np.ndarray = None) -> np.ndarray:
        """
        Update approximative Markov state

        :param obs: attacker obs
        :param defender_obs: defender observation
        :param state: current state
        :param attacker: boolean flag whether it is attacker or not
        :return: new state
        """
        state = obs
        return state

    @abstractmethod
    def train(self) -> ExperimentResult:
        pass

    @abstractmethod
    def eval(self, log=True) -> ExperimentResult:
        pass