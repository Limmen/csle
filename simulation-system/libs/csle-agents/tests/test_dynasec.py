import logging
import pytest
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_agents.agents.dynasec.dynasec_agent import DynaSecAgent


class TestDynaSecSuite(object):
    """
    Test suite for the DynaSecAgent
    """

    pytest.logger = logging.getLogger("dynasec_tests")

    def test_create_agent(self, mocker, experiment_config: ExperimentConfig) -> None:
        """
        Tests creation of the FPAgent

        :return: None
        """
        emulation_executions = [mocker.MagicMock()]
        attacker_sequence = mocker.MagicMock()
        defender_sequence = mocker.MagicMock()
        system_id_config = mocker.MagicMock()
        simulation_env_config = mocker.MagicMock()
        pytest.logger.info("Creating the DynaSec Agent")
        DynaSecAgent(emulation_executions=emulation_executions, simulation_env_config=simulation_env_config,
                     experiment_config=experiment_config, attacker_sequence=attacker_sequence,
                     defender_sequence=defender_sequence, system_identification_config=system_id_config)
        pytest.logger.info("Agent created successfully")
