from enum import IntEnum


class AgentType(IntEnum):
    """
    Enum representing the different agent types in CSLE
    """
    T_SPSA=0
    PPO=1
    T_FP=2
    DQN=3
    REINFORCE=4
    NFSP=5
    RANDOM=6
    NONE=7
    VALUE_ITERATION=8
    HSVI=9
    SONDIK_VALUE_ITERATION=10
    RANDOM_SEARCH=11
    DIFFERENTIAL_EVOLUTION=12
    CROSS_ENTROPY=13
    KIEFER_WOLFOWITZ=14
    Q_LEARNING=15
    SARSA=16
