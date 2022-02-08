"""
Some utility functions for csle CTF minigame
"""
import numpy as np
from csle_common.dao.network.network_config import NetworkConfig


def is_network_conf_incomplete(network_conf: NetworkConfig):
    """
    Checks if the network configuration is complete or not
    :param env_config:
    :return:
    """
    if network_conf is None:
        return True
    if network_conf.nodes is None:
        return True
    if len(network_conf.nodes) == 0:
        return True
    if network_conf.adj_matrix is None:
        return True
    if len(network_conf.adj_matrix) == 0:
        return True
    return False


def running_average(x, N):
    ''' Function used to compute the running average
        of the last N elements of a vector x
    '''
    if len(x) >= N:
        y = np.copy(x)
        y[N-1:] = np.convolve(x, np.ones((N, )) / N, mode='valid')
    else:
        y = [x[-1]]
    return y[-1]
