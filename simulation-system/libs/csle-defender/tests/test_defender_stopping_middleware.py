from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_defender.emulation.defender_stopping_middleware import DefenderStoppingMiddleware


class TestDefenderStoppingMiddlewareSuite:
    """
    Test suite for defender_update_state_middleware.py
    """

    def test_update_state(self, get_ex_em_env: EmulationEnvConfig) -> None:
        """
        Tests the update_state function

        :return: None
        """
        s = EmulationEnvState(emulation_env_config=get_ex_em_env)
        s_prime = DefenderStoppingMiddleware.stop_monitor(s=s)
        if s_prime.defender_obs_state is not None:
            assert s_prime.defender_obs_state.stopped
