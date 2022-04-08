from enum import IntEnum


class AgentType(IntEnum):
    """
    Enum representing the different agent types in CSLE
    """
    T_SPSA=0
    PPO=1
    FP_SPSA=2
    DQN=3
    REINFORCE=4
    NFSP=5