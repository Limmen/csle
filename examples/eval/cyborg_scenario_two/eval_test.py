from typing import List, Dict, Tuple
import random
import numpy as np
from collections import Counter
from gym_csle_cyborg.envs.cyborg_scenario_two_wrapper import CyborgScenarioTwoWrapper
from gym_csle_cyborg.dao.red_agent_type import RedAgentType
from gym_csle_cyborg.dao.csle_cyborg_wrapper_config import CSLECyborgWrapperConfig
from gym_csle_cyborg.util.cyborg_env_util import CyborgEnvUtil
from gym_csle_cyborg.dao.cyborg_wrapper_state import CyborgWrapperState
from cage2_aggregate_mdp import Cage2AggregateMDP
import csle_agents.constants.constants as agents_constants
from gym_csle_cyborg.envs.cyborg_scenario_two_wrapper_particle_filter import CyborgScenarioTwoWrapperParticleFilter


def one_hot_encode_integer(value, max_value):
    """

    :param value:
    :param max_value:
    :return:
    """
    if not (0 <= value <= max_value):
        raise ValueError(f"Value must be between 0 and {max_value} (inclusive).")
    one_hot_vector = np.zeros(max_value + 1, dtype=int)
    one_hot_vector[value] = 1
    return one_hot_vector


def one_hot_encode_state(vector):
    """

    :param vector:
    :return:
    """
    vector = np.array(vector)
    if not np.all(np.isin(vector, [0, 1, 2])):
        raise ValueError("Input vector can only contain values 0, 1, or 2.")

    one_hot = np.eye(3)[vector]  # Create identity matrix and index it with the vector
    return one_hot.flatten()


if __name__ == '__main__':
    config = CSLECyborgWrapperConfig(maximum_steps=100, gym_env_name="",
                                     save_trace=False, reward_shaping=False, scenario=2,
                                     red_agent_type=RedAgentType.B_LINE_AGENT)
    # env = CyborgScenarioTwoWrapper(config=config)
    env = CyborgScenarioTwoWrapperParticleFilter(config=config)
    env.step(0)
    env.step(0)
    print(len(env.particles[0].to_vector()))
    # print(one_hot_encode_state(env.scan_state))
    # # print(env.s)
    # print(one_hot_encode_state(np.array(env.s).flatten()))
    # print(one_hot_encode_integer(value=env.red_agent_state, max_value=14))
    # print(one_hot_encode_integer(value=env.red_agent_target, max_value=12))
    # observation = (list(one_hot_encode_state(env.scan_state)) + list(one_hot_encode_state(np.array(env.s).flatten()))
    #                + list(one_hot_encode_integer(value=env.red_agent_target, max_value=12)) +
    #                list(one_hot_encode_integer(value=env.red_agent_target, max_value=12)))
    # print(len(observation))
