"""
Register OpenAI Envs
"""
from .__version__ import __version__
from gymnasium.envs.registration import register

register(
    id='csle-cyborg-scenario-two-v1',
    entry_point='gym_csle_cyborg.envs.cyborg_scenario_two_defender:CyborgScenarioTwoDefender',
    kwargs={'config': None}
)

register(
    id='csle-cyborg-scenario-two-wrapper-v1',
    entry_point='gym_csle_cyborg.envs.cyborg_scenario_two_wrapper:CyborgScenarioTwoWrapper',
    kwargs={'config': None}
)

register(
    id='csle-cyborg-scenario-two-wrapper-particle-filter-v1',
    entry_point='gym_csle_cyborg.envs.cyborg_scenario_two_wrapper_particle_filter:CyborgScenarioTwoWrapperParticleFilter',
    kwargs={'config': None}
)
