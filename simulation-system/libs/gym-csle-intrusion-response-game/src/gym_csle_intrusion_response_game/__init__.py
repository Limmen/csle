"""
Register OpenAI Envs
"""
from . __version__ import __version__
from gymnasium.envs.registration import register

register(
    id='csle-intrusion-response-game-local-pomdp-defender-v1',
    entry_point='gym_csle_intrusion_response_game.envs.intrusion_response_game_local_pomdp_defender:'
                'IntrusionResponseGameLocalPOMDPDefenderEnv', kwargs={'config': None}
)

register(
    id='csle-intrusion-response-game-local-pomdp-attacker-v1',
    entry_point='gym_csle_intrusion_response_game.envs.intrusion_response_game_local_pomdp_attacker:'
                'IntrusionResponseGameLocalPOMDPAttackerEnv', kwargs={'config': None}
)

register(
    id='csle-intrusion-response-game-workflow-pomdp-defender-v1',
    entry_point='gym_csle_intrusion_response_game.envs.intrusion_response_game_workflow_pomdp_defender:'
                'IntrusionResponseGameWorkflowPOMDPDefenderEnv', kwargs={'config': None}
)

register(
    id='csle-intrusion-response-game-workflow-pomdp-attacker-v1',
    entry_point='gym_csle_intrusion_response_game.envs.intrusion_response_game_workflow_pomdp_attacker:'
                'IntrusionResponseGameWorkflowPOMDPAttackerEnv', kwargs={'config': None}
)

register(
    id='csle-intrusion-response-game-local-stopping-pomdp-defender-v1',
    entry_point='gym_csle_intrusion_response_game.envs.intrusion_response_game_local_stopping_pomdp_defender:'
                'IntrusionResponseGameLocalStoppingPOMDPDefenderEnv', kwargs={'config': None}
)