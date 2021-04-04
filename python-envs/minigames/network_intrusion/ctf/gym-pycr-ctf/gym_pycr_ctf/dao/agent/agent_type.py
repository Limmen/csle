from enum import Enum

class AgentType(Enum):
    REINFORCE = 0
    PPO_BASELINE = 1
    DQN_BASELINE = 2
    A2C_BASELINE = 3
    TD3_BASELINE = 4
    DDPG_BASELINE = 5
    RANDOM_ATTACKER = 6
    RANDOM_DEFENDER = 7
    CUSTOM_ATTACKER = 8