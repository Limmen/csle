# This file is here just to define MlpPolicy/CnnPolicy
# that work for PPO
from pycr_common.agents.openai_baselines.common.policies import \
    ActorCriticCnnPolicy, ActorCriticPolicy, register_policy

MlpPolicy = ActorCriticPolicy
CnnPolicy = ActorCriticCnnPolicy

register_policy("MlpPolicy", ActorCriticPolicy)
register_policy("CnnPolicy", ActorCriticCnnPolicy)