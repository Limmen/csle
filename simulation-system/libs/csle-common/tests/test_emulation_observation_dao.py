from csle_common.dao.emulation_observation.common.emulation_port_observation_state import EmulationPortObservationState
from csle_common.dao.emulation_observation.attacker. \
    emulation_attacker_machine_observation_state import EmulationAttackerMachineObservationState
from csle_common.dao.emulation_observation.attacker. \
    emulation_attacker_observation_state import EmulationAttackerObservationState
from csle_common.dao.emulation_observation.common.emulation_connection_observation_state \
    import EmulationConnectionObservationState
from csle_common.dao.emulation_observation.common.emulation_vulnerability_observation_state \
    import EmulationVulnerabilityObservationState
from csle_common.dao.emulation_observation.defender.emulation_defender_machine_observation_state import \
    EmulationDefenderMachineObservationState
from csle_common.dao.emulation_observation.defender.emulation_defender_observation_state import \
    EmulationDefenderObservationState


class TestEmulationObservationDaoSuite:
    """
    Test suite for emulation observation data access objects (DAOs)
    """

    def test_emulation_port_observation_state(
            self, example_emulation_port_observation_state: EmulationPortObservationState) -> None:
        """
        Tests creation and dict conversion of the EmulationPortObservationState DAO

        :param example_emulation_port_observation_state: an example EmulationPortObservationState
        :return: None
        """
        assert isinstance(example_emulation_port_observation_state.to_dict(), dict)
        assert isinstance(EmulationPortObservationState.from_dict(example_emulation_port_observation_state.to_dict()),
                          EmulationPortObservationState)
        assert (EmulationPortObservationState.from_dict(example_emulation_port_observation_state.to_dict()).to_dict() ==
                example_emulation_port_observation_state.to_dict())
        assert (EmulationPortObservationState.from_dict(example_emulation_port_observation_state.to_dict()) ==
                example_emulation_port_observation_state)

    def test_emulation_attacker_machine_observation_state(
            self, example_emulation_attacker_machine_observation_state: EmulationAttackerObservationState) -> None:
        """
        Tests creation and dict conversion of the EmulationAttackerMachineObservationState DAO

        :param example_emulation_attacker_machine: an example EmulationAttackerMachineObservationState
        :return: None
        """
        assert isinstance(example_emulation_attacker_machine_observation_state.to_dict(), dict)
        assert isinstance(EmulationAttackerMachineObservationState.from_dict
                          (example_emulation_attacker_machine_observation_state.to_dict()),
                          EmulationAttackerMachineObservationState)
        assert (EmulationAttackerMachineObservationState.from_dict
                (example_emulation_attacker_machine_observation_state.to_dict()).to_dict() ==
                example_emulation_attacker_machine_observation_state.to_dict())
        assert (EmulationAttackerMachineObservationState.from_dict
                (example_emulation_attacker_machine_observation_state.to_dict()) ==
                example_emulation_attacker_machine_observation_state)

    def test_emulation_attacker_observation_state(
            self, example_emulation_attacker_observation_state: EmulationAttackerObservationState) -> None:
        """
        Tests creation and dict conversion of the EmulationAttackerObservationState DAO

        :param example_emulation_attacker_observation_state: an example EmulationAttackerObservationState
        :return: None
        """
        assert isinstance(example_emulation_attacker_observation_state.to_dict(), dict)
        assert isinstance(EmulationAttackerObservationState.from_dict
                          (example_emulation_attacker_observation_state.to_dict()), EmulationAttackerObservationState)
        assert (EmulationAttackerObservationState.from_dict
                (example_emulation_attacker_observation_state.to_dict()).to_dict() ==
                example_emulation_attacker_observation_state.to_dict())
        assert (EmulationAttackerObservationState.from_dict
                (example_emulation_attacker_observation_state.to_dict()) ==
                example_emulation_attacker_observation_state)

    def test_emulation_connection_observation_state(
            self, example_emulation_connection_observation_state: EmulationConnectionObservationState) -> None:
        """
        Tests creation and dict conversion of the EmulationConnectionObservationState DAO

        :param example_emulation_connection_observation_state: an example EmulationConnectionObservationState
        :return: None
        """
        assert isinstance(example_emulation_connection_observation_state.to_dict(), dict)
        assert isinstance(EmulationConnectionObservationState.from_dict
                          (example_emulation_connection_observation_state.to_dict()),
                          EmulationConnectionObservationState)
        assert (EmulationConnectionObservationState.from_dict
                (example_emulation_connection_observation_state.to_dict()).to_dict() ==
                example_emulation_connection_observation_state.to_dict())
        assert (EmulationConnectionObservationState.from_dict
                (example_emulation_connection_observation_state.to_dict()) ==
                example_emulation_connection_observation_state)

    def test_emulation_vulnerability_observation_state(
            self, example_emulation_vulnerability_observation_state: EmulationVulnerabilityObservationState) -> None:
        """
        Tests creation and dict conversion of the EmulationVulnerabilityObservationState DAO

        :param example_emulation_vulnerability_observation_state: an example EmulationVulnerabilityObservationState
        :return: None
        """
        assert isinstance(example_emulation_vulnerability_observation_state.to_dict(), dict)
        assert isinstance(EmulationVulnerabilityObservationState.from_dict
                          (example_emulation_vulnerability_observation_state.to_dict()),
                          EmulationVulnerabilityObservationState)
        assert (EmulationVulnerabilityObservationState.from_dict
                (example_emulation_vulnerability_observation_state.to_dict()).to_dict() ==
                example_emulation_vulnerability_observation_state.to_dict())
        assert (EmulationVulnerabilityObservationState.from_dict
                (example_emulation_vulnerability_observation_state.to_dict()) ==
                example_emulation_vulnerability_observation_state)

    def test_emulation_defender_machine_observation_state(
            self,
            example_emulation_defender_machine_observation_state: EmulationDefenderMachineObservationState) -> None:
        """
        Tests creation and dict conversion of the EmulationDefenderMachineObservationState DAO

        :param example_emulation_defender_machine_observation_state: an example EmulationDefenderMachineObservationState
        :return: None
        """
        assert isinstance(example_emulation_defender_machine_observation_state.to_dict(), dict)
        assert isinstance(EmulationDefenderMachineObservationState.from_dict
                          (example_emulation_defender_machine_observation_state.to_dict()),
                          EmulationDefenderMachineObservationState)
        assert (EmulationDefenderMachineObservationState.from_dict
                (example_emulation_defender_machine_observation_state.to_dict()).to_dict() ==
                example_emulation_defender_machine_observation_state.to_dict())
        assert (EmulationDefenderMachineObservationState.from_dict
                (example_emulation_defender_machine_observation_state.to_dict()) ==
                example_emulation_defender_machine_observation_state)

    def test_emulation_defender_observation_state(
            self, example_emulation_defender_observation_state: EmulationDefenderObservationState) -> None:
        """
        Tests creation and dict conversion of the EmulationDefenderObservationState DAO

        :param example_emulation_defender_observation_state: an example EmulationDefenderObservationState
        :return: None
        """
        assert isinstance(example_emulation_defender_observation_state.to_dict(), dict)
        assert isinstance(EmulationDefenderObservationState.from_dict(
            example_emulation_defender_observation_state.to_dict()),
            EmulationDefenderObservationState)
        assert (EmulationDefenderObservationState.from_dict
                (example_emulation_defender_observation_state.to_dict()).to_dict() ==
                example_emulation_defender_observation_state.to_dict())
        assert (EmulationDefenderObservationState.from_dict(example_emulation_defender_observation_state.to_dict()) ==
                example_emulation_defender_observation_state)
