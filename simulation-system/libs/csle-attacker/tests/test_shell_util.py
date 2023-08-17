import pytest_mock
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_id import EmulationAttackerActionId
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_type import EmulationAttackerActionType
from csle_common.dao.emulation_action.attacker.emulation_attacker_action_outcome import EmulationAttackerActionOutcome
from csle_attacker.emulation.util.shell_util import ShellUtil


class TestShellUtilSuite:
    """
    Test suite for shell_util.py
    """

    def test_execute_service_login_helper(self, mocker: pytest_mock.MockFixture,
                                          get_ex_em_env: EmulationEnvConfig) -> None:
        """
        Tests the execute_service_login_helper function

        :return: None
        """
        a = EmulationAttackerAction(
            id=EmulationAttackerActionId.CONTINUE, name="test", cmds=[], descr="", ips=["test"], index=0,
            action_outcome=EmulationAttackerActionOutcome.CONTINUE, vulnerability="", alt_cmds=[], backdoor=False,
            execution_time=0.0, ts=0.0, type=EmulationAttackerActionType.CONTINUE)
        s = EmulationEnvState(emulation_env_config=get_ex_em_env)
        mocker.patch('csle_common.util.connection_util.ConnectionUtil.login_service_helper',
                     return_value=(s, "conn"))
        s_prime = ShellUtil.execute_service_login_helper(s=s, a=a)
        for m in s_prime.attacker_obs_state.machines:
            if m.ips == a.ips:
                assert not m.untried_credentials
