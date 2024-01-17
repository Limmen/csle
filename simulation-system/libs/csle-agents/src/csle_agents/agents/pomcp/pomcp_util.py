from typing import List, Dict, Union
import numpy as np
from csle_agents.agents.pomcp.node import Node
from collections import Counter


class POMCPUtil:
    """
    Class with utility functions related to POMCP
    """

    @staticmethod
    def sample_from_distribution(probability_vector: List[float]) -> int:
        """
        Utility function to sample from a probability vector

        :param probability_vector: the probability vector to sample from
        :return: the sampled element
        """
        probability_vector_np = np.array(probability_vector)
        sample = np.random.choice(list(range(len(probability_vector_np))),
                                  p=probability_vector_np / probability_vector_np.sum())
        return int(sample)

    @staticmethod
    def rand_choice(candidates: List[int]) -> int:
        """
        Selects an element from a given list uniformly at random

        :param candidates: the list to sample from
        :return: the sample
        """
        return int(np.random.choice(candidates))

    @staticmethod
    def convert_samples_to_distribution(samples) -> Dict[int, float]:
        """
        Converts a list of samples to a probability distribution

        :param samples: the list of samples
        :return: a dict with the sample values and their probabilities
        """
        cnt = Counter(samples)
        _sum = sum(cnt.values())
        return {k: v / _sum for k, v in cnt.items()}

    @staticmethod
    def generate_particles(states: List[int], num_particles: int, probability_vector: Union[None, List[float]]):
        """
        Generates a list of particles (sample states) for a given list of states
        with a frequency determined by a given probability vector

        :param states: the
        :param n:
        :param probability_vector: (optional) probability vector to determine the frequency of each sample
        :return:
        """
        # by default use uniform distribution for particles generation
        if probability_vector is None:
            probability_vector = [1 / len(states)] * len(states)
        return [states[int(POMCPUtil.sample_from_distribution(probability_vector))] for _ in range(num_particles)]

    @staticmethod
    def ucb(history_visit_count, action_visit_count):
        """
        Implements the upper-confidence-bound acquisiton function

        :param history_visit_count: counter of the number of times the history has been visited
        :param action_visit_count: counter of the number of times the action has been taken in the history
        :return: the ucb acquisition value
        """
        # If we have never seen this history before, its utility is initialized to zero
        if history_visit_count == 0:
            return 0.0
        # If we have never taken this action before, its utility is infinity to encourage exploration
        if action_visit_count == 0:
            return np.inf
        # If we have taken this action before, return the UCB exploration bonus
        return np.sqrt(np.log(history_visit_count) / action_visit_count)

    @staticmethod
    def ucb_acquisition_function(action: "Node", c: float) -> float:
        """
        The UCB acquisition function

        :param action: the action
        :param c: the exploration parameter
        :return: the acquisition value of the action
        """
        return float(action.value + c * POMCPUtil.ucb(action.parent.visit_count, action.visit_count))
