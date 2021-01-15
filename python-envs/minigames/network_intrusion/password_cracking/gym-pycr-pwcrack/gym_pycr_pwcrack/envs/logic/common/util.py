import numpy as np
from gym_pycr_pwcrack.dao.network.env_config import EnvConfig

def is_network_conf_incomplete(env_config: EnvConfig):
    if env_config.network_conf is None:
        return True
    if env_config.network_conf.nodes == None:
        return True
    if len(env_config.network_conf.nodes) == 0:
        return True
    if env_config.network_conf.adj_matrix == None:
        return True
    if len(env_config.network_conf.adj_matrix) == 0:
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
