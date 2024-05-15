from typing import List, Dict, Any, Callable
import random
import numpy as np
from collections import Counter
from csle_common.logging.log import Logger
from csle_common.dao.simulation_config.base_env import BaseEnv
from csle_agents.agents.pomcp.node import Node
import csle_agents.constants.constants as constants


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
    def rand_choice(candidates: List[Any]) -> Any:
        """
        Selects an element from a given list uniformly at random

        :param candidates: the list to sample from
        :return: the sample
        """
        return random.choice(candidates)

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
    def ucb(history_visit_count, action_visit_count):
        """
        Implements the upper-confidence-bound acquisiton function

        :param history_visit_count: counter of the number of times the history has been visited
        :param action_visit_count: counter of the number of times the action has been taken in the history
        :return: the ucb acquisition value
        """
        # If we have never seen this history before, its exploration utility is initialized to zero
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

        :param action: the action node
        :param c: the exploration parameter
        :param rollout_policy: the rollout policy
        :param prior_weight: the weight to put on the prior
        :return: the acquisition value of the action
        """
        if action.parent.visit_count == 0:
            return 0
        if action.visit_count == 0:
            return np.inf
        return float(action.value + c * POMCPUtil.ucb(action.parent.visit_count, action.visit_count))

    @staticmethod
    def alpha_go_acquisition_function(action: "Node", c: float, c2: float, prior: float, prior_weight: float) -> float:
        """
        The UCB acquisition function

        :param action: the action node
        :param c: the exploration parameter
        :param c2: the c2 parameter
        :param prior: the prior weight
        :param prior_weight: the weight to put on the prior
        :return: the acquisition value of the action
        """
        # prior = rollout_policy.probability(o=o, a=action.action)
        # visit_term = math.sqrt(action.parent.visit_count) / (action.visit_count + 1)
        # base_term = math.log((action.parent.visit_count + c2 + 1) / c2 + c)
        # prior_term = prior_weight * prior * visit_term * base_term
        exploration_term = POMCPUtil.ucb(action.parent.visit_count, action.visit_count)
        return float(action.value + (c + prior_weight * prior) * exploration_term)
        # return float(action.value + prior_term + exploration_term)

    @staticmethod
    def trajectory_simulation_particles(o: int, env: BaseEnv, action_sequence: List[int], num_particles: int,
                                        verbose: bool = False) -> List[int]:
        """
        Performs trajectory simulations to find possible states matching to the given observation

        :param o: the observation to match against
        :param env: the black-box simulator to sue for generating trajectories
        :param action_sequence: the action sequence for the trajectory
        :param num_particles: the number of particles to collect
        :param verbose: boolean flag indicating whether logging should be verbose or not
        :return: the list of particles matching the given observation
        """
        particles: List[int] = []
        if verbose:
            Logger.__call__().get_logger().info(f"Filling {num_particles} particles"
                                                f" through trajectory simulations, "
                                                f"action sequence: {action_sequence}, observation: {o}")
        while len(particles) < num_particles:
            done = False
            _, info = env.reset()
            t = 0
            while not done and t < len(action_sequence):
                _, r, done, _, info = env.step(action=action_sequence[t])
                sampled_o = info[constants.COMMON.OBSERVATION]
                s = info[constants.COMMON.STATE]
                if t == len(action_sequence) - 1 and sampled_o == o:
                    particles.append(s)
                t += 1
        return particles

    @staticmethod
    def get_default_value(particles: List[int], action: int, default_value: float, env: BaseEnv,
                          value_function: Callable[[Any], float]) -> float:
        """
        Gets the default value of a node

        :param particles: the particles of the parent node
        :param action: the action of the node
        :param default_value: the default value
        :param env: the black-box simulator
        :param value_function: the value function
        :return: the value
        """
        node_value = default_value
        if value_function is not None:
            sample_values = []
            for i in range(20):
                state = int(POMCPUtil.rand_choice(particles))
                env.set_state(state=state)
                o, r, _, _, info = env.step(action)
                sample_values.append(value_function(o))
            node_value = float(np.mean(sample_values))
        return node_value
