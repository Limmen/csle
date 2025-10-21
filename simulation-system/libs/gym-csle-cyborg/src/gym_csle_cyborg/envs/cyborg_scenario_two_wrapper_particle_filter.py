from typing import Tuple, Any, Dict, Union, List
import numpy as np
import gymnasium as gym
from collections import Counter
from csle_common.dao.simulation_config.base_env import BaseEnv
from gym_csle_cyborg.dao.csle_cyborg_wrapper_config import CSLECyborgWrapperConfig
import gym_csle_cyborg.constants.constants as constants
from gym_csle_cyborg.envs.cyborg_scenario_two_wrapper import CyborgScenarioTwoWrapper
from gym_csle_cyborg.dao.cyborg_wrapper_state import CyborgWrapperState
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace
import random
import numpy.typing as npt


class CyborgScenarioTwoWrapperParticleFilter(BaseEnv):
    """
    A Wrapper Gym Environment for Cyborg scenario 2 with a particle filter
    """

    def __init__(self, config: CSLECyborgWrapperConfig) -> None:
        """
        Initializes the environment

        :param config: the environment config
        """
        self.config = config
        self.env = CyborgScenarioTwoWrapper(config=self.config)
        self.train_env = CyborgScenarioTwoWrapper(config=self.config)
        self.particles: List[CyborgWrapperState] = []
        self.particles = self.env.initial_particles
        self.control_sequence: List[int] = []
        self.action_space = self.env.action_space
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(379,), dtype=np.int32)

    def step(self, action: int) -> Tuple[npt.NDArray[Any], float, bool, bool, Dict[str, Any]]:
        """
        Takes a step in the environment

        :param action: the defender action
        :return: (obs, reward, terminated, truncated, info)
        """
        self.control_sequence.append(action)
        _, r, done, _, info = self.env.step(action=action)
        self.particles = self.particle_filter(
            particles=self.particles, max_num_particles=50, train_env=self.train_env,
            obs=info[constants.COMMON.OBSERVATION], control_sequence=self.control_sequence)
        monte_carlo_particle = self.monte_carlo_most_frequent_particle(particles=self.particles, N=50)
        obs = monte_carlo_particle.to_vector()
        return np.array(obs), r, done, done, info

    def reset(self, seed: Union[None, int] = None, soft: bool = False, options: Union[Dict[str, Any], None] = None) \
            -> Tuple[npt.NDArray[Any], Dict[str, Any]]:
        """
        Resets the environment

        :param seed: the random seed
        :param soft: whether to do a soft reset or not
        :param options: reset options
        :return: the reset observation and info dict
        """
        self.control_sequence = []
        self.particles = self.env.initial_particles
        _, info = self.env.reset()
        self.train_env.reset()
        obs = self.particles[0].to_vector()
        return np.array(obs), info

    def particle_filter(self, particles: List[CyborgWrapperState], max_num_particles: int,
                        train_env: CyborgScenarioTwoWrapper, obs: int,
                        control_sequence: List[int]) -> List[CyborgWrapperState]:
        """
        Implements a particle filter

        :param particles: the list of particles
        :param max_num_particles: the maximum number of particles
        :param train_env: the environment used for sampling
        :param obs: the latest observation
        :param control_sequence: the control sequence up to the current observation
        :return: the list of updated particles
        """
        u = control_sequence[-1]
        new_particles: List[CyborgWrapperState] = []
        failed_samples = 0
        while len(new_particles) < max_num_particles:
            x = random.choice(particles)
            train_env.set_state(state=x)
            _, _, _, _, info = train_env.step(u)
            x_prime = info[constants.COMMON.STATE]
            o = info[constants.COMMON.OBSERVATION]
            if int(o) == int(obs):
                failed_samples = 0
                new_particles.append(x_prime)
            failed_samples += 1
            if failed_samples > 500:
                # Particle deprivation
                if len(new_particles) == 0:
                    while True:
                        t = 0
                        train_env.reset()
                        while t < len(control_sequence):
                            _, _, _, _, info = train_env.step(control_sequence[t])
                            o = info[constants.COMMON.OBSERVATION]
                            if int(o) == int(obs):
                                return [info[constants.COMMON.STATE]]
                            t += 1
                else:
                    return new_particles
        return new_particles

    def monte_carlo_most_frequent_particle(self, particles: List[CyborgWrapperState], N: int) -> CyborgWrapperState:
        """
        Samples N particles and returns the most frequently sampled particle

        :param particles: the list of particles
        :param N: the number of samples
        :return: the most frequently sampled particle
        """
        samples = [random.choice(particles) for _ in range(N)]
        counter = Counter(samples)
        most_frequent_particle = counter.most_common(1)[0][0]
        return most_frequent_particle

    def get_traces(self) -> List[SimulationTrace]:
        """
        :return: the list of simulation traces
        """
        return self.env.traces

    def reset_traces(self) -> None:
        """
        Resets the list of traces

        :return: None
        """
        self.env.reset_traces()

    def set_model(self, model) -> None:
        """
        Sets the model. Useful when using RL frameworks where the stage policy is not easy to extract

        :param model: the model
        :return: None
        """
        self.model = model

    def manual_play(self) -> None:
        """
        An interactive loop to test the environment manually

        :return: None
        """
        return None

    def set_state(self, state: CyborgWrapperState) -> None:
        """
        Sets the state of the environment

        :param state: the new state
        :return: None
        """
        self.env.set_state(state=state)
