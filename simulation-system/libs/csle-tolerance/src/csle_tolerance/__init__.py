from . __version__ import __version__
from gymnasium.envs.registration import register

register(
    id='csle-tolerance-intrusion-recovery-pomdp-v1',
    entry_point='csle_tolerance.envs.intrusion_recovery_pomdp_env:IntrusionRecoveryPomdpEnv',
    kwargs={'config': None}
)

register(
    id='csle-tolerance-intrusion-response-cmdp-v1',
    entry_point='csle_tolerance.envs.intrusion_response_cmdp_env:IntrusionResponseCmdpEnv',
    kwargs={'config': None}
)