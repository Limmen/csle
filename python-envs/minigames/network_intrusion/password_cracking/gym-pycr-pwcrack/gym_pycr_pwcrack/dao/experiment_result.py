"""
Experiment results
"""
from typing import List
import csv

class ExperimentResult:
    """
    DTO with experiment result from an experiment in the pycr-pwcrack-envs
    """

    def __init__(self, avg_episode_rewards: List[float] = None,
                 avg_episode_rewards_a: List[float] = None,
                 avg_episode_steps: List[int] = None, epsilon_values: List[float] = None,
                 cumulative_reward: List[int] = None, avg_episode_loss: List[float] = None,
                 lr_list : List[float] = None):
        """
        Constructor, initializes the DTO

        :param avg_episode_rewards: list of episode rewards for attacker
        :param avg_episode_steps: list of episode steps
        :param epsilon_values: list of epsilon values
        :param cumulative_reward: list of attacker cumulative rewards
        :param avg_episode_loss: average loss for attacker
        :param lr_list: learning rates
        """
        self.avg_episode_rewards = avg_episode_rewards
        self.avg_episode_rewards_a = avg_episode_rewards_a
        self.avg_episode_steps = avg_episode_steps
        self.epsilon_values = epsilon_values
        self.cumulative_reward = cumulative_reward
        self.avg_episode_loss = avg_episode_loss
        self.lr_list = lr_list
        if avg_episode_steps is None:
            self.avg_episode_steps = []
        if avg_episode_rewards is None:
            self.avg_episode_rewards = []
        if avg_episode_rewards_a is None:
            self.avg_episode_rewards_a = []
        if epsilon_values is None:
            self.epsilon_values = []
        if cumulative_reward is None:
            self.cumulative_reward = []
        if avg_episode_loss is None:
            self.avg_episode_loss = []
        if lr_list is None:
            self.lr_list = []

    def to_csv(self, file_path : str) -> None:
        """
        Save result to csv

        :param file_path: path to save the csv file
        :return: None
        """
        metrics = [self.avg_episode_rewards, self.avg_episode_rewards_a, self.avg_episode_steps, self.epsilon_values,
                   self.cumulative_reward, self.avg_episode_loss, self.lr_list]
        metric_labels = ["avg_episode_rewards", "avg_episode_rewards_a", "avg_episode_steps",
                         "epsilon_values", "cumulative_reward", "avg_episode_loss",
                         "lr_list"]
        filtered_metric_labels = []
        filtered_metrics = []
        for i in range(len(metrics)):
            if len(metrics[i]) > 0:
                filtered_metrics.append(metrics[i])
                filtered_metric_labels.append(metric_labels[i])
        rows = zip(*filtered_metrics)
        with open(file_path, "w") as f:
            writer = csv.writer(f)
            writer.writerow(filtered_metric_labels)
            for row in rows:
                writer.writerow(row)