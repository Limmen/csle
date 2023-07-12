import logging
import pytest
import pytest_mock
from csle_common.dao.training.agent_type import AgentType
from csle_agents.agents.dynasec.dynasec_agent import DynaSecAgent


class TestDynaSecSuite:
    """
    Test suite for the DynaSecAgent
    """

    pytest.logger = logging.getLogger("dynasec_tests")

    def test_create_agent(self, mocker: pytest_mock.MockFixture) -> None:
        """
        Tests creation of the FPAgent

        :return: None
        """
        emulation_executions = [mocker.MagicMock()]
        attacker_sequence = mocker.MagicMock()
        defender_sequence = mocker.MagicMock()
        system_id_config = mocker.MagicMock()
        experiment_config = mocker.MagicMock()
        experiment_config.configure_mock(**{"agent_type": AgentType.DYNA_SEC})
        simulation_env_config = mocker.MagicMock()
        pytest.logger.info("Creating the DynaSec Agent")
        DynaSecAgent(emulation_executions=emulation_executions, simulation_env_config=simulation_env_config,
                     experiment_config=experiment_config, attacker_sequence=attacker_sequence,
                     defender_sequence=defender_sequence, system_identification_config=system_id_config)
        pytest.logger.info("Agent created successfully")
