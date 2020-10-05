from enum import Enum

class AgentType(Enum):
    REINFORCE = 0
    PPO_BASELINE = 1
    DQN_BASELINE = 2