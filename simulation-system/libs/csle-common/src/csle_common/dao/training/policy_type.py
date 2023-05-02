from enum import IntEnum


class PolicyType(IntEnum):
    """
    Enum representing the different policy types in CSLE
    """
    TABULAR = 0
    ALPHA_VECTORS = 1
    DQN = 2
    FNN_W_SOFTMAX = 3
    MIXED_MULTI_THRESHOLD = 4
    PPO = 5
    RANDOM = 6
    VECTOR = 7
    MULTI_THRESHOLD = 8
    LINEAR_THRESHOLD = 9
    MIXED_PPO_POLICY = 10
    LINEAR_TABULAR = 11
    MIXED_LINEAR_TABULAR = 12
