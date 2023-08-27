from csle_common.dao.emulation_observation.common.emulation_port_observation_state import EmulationPortObservationState
from csle_common.dao.emulation_config.transport_protocol import TransportProtocol
from csle_common.dao.emulation_observation.attacker.\
    emulation_attacker_machine_observation_state import EmulationAttackerMachineObservationState


class TestEmulationObservationDaoSuite:
    """
    Test suite for emulation observation data access objects (DAOs)
    """

    def test_emulation_port_observation_state(self) -> None:
        """
        Tests creation and dict conversion of the EmulationPortObservationState DAO

        :return: None
        """

        emulation_port_observation_state = EmulationPortObservationState(
            port=3333, open=False, service="myservice", protocol=TransportProtocol.TCP, http_enum="testenum",
            http_grep="testgrep", vulscan="vulscantest", version="myversion", fingerprint="myfp")

        assert isinstance(emulation_port_observation_state.to_dict(), dict)
        assert isinstance(EmulationPortObservationState.from_dict(emulation_port_observation_state.to_dict()),
                          EmulationPortObservationState)
        assert (EmulationPortObservationState.from_dict(emulation_port_observation_state.to_dict()).to_dict() ==
                emulation_port_observation_state.to_dict())
        assert (EmulationPortObservationState.from_dict(emulation_port_observation_state.to_dict()) ==
                emulation_port_observation_state)

    def test_emulation_attacker_machine_observation_state(self) -> None:
        """
                Tests creation and dict conversion of the EmulationAttackerMachineObservationState DAO

                :return: None
                """

        emulation_attack_machine_observation_state = (EmulationAttackerMachineObservationState
                                                      (ips=["172.31.212.1", "172.31.212.2"]))

        assert isinstance(emulation_attack_machine_observation_state.to_dict(), dict)

        assert isinstance(EmulationAttackerMachineObservationState.from_dict
                          (emulation_attack_machine_observation_state.to_dict()),
                          EmulationAttackerMachineObservationState)
        assert (EmulationAttackerMachineObservationState.from_dict
                (emulation_attack_machine_observation_state.to_dict()).to_dict() ==
                emulation_attack_machine_observation_state.to_dict())
        assert (EmulationAttackerMachineObservationState.from_dict
                (emulation_attack_machine_observation_state.to_dict()) ==
                emulation_attack_machine_observation_state)
