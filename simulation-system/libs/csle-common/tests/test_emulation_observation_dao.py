from csle_common.dao.emulation_observation.common.emulation_port_observation_state import EmulationPortObservationState
from csle_common.dao.emulation_config.transport_protocol import TransportProtocol
from csle_common.dao.emulation_observation.attacker.\
    emulation_attacker_machine_observation_state import EmulationAttackerMachineObservationState
from csle_common.dao.emulation_observation.attacker.\
    emulation_attacker_observation_state import EmulationAttackerObservationState
from csle_common.dao.emulation_observation.common.emulation_connection_observation_state \
    import EmulationConnectionObservationState
from csle_common.dao.emulation_config.credential import Credential


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

    def test_emulation_attacker_observation_state(self) -> None:
        """
                Tests creation and dict conversion of the EmulationAttackerObservationState DAO

                :return: None
                """

        emulation_attack_observation_state = (EmulationAttackerObservationState
                                              (catched_flags=1, agent_reachable=set(["test1", "test2"])))

        assert isinstance(emulation_attack_observation_state.to_dict(), dict)

        assert isinstance(EmulationAttackerObservationState.from_dict
                          (emulation_attack_observation_state.to_dict()),
                          EmulationAttackerObservationState)
        assert (EmulationAttackerObservationState.from_dict
                (emulation_attack_observation_state.to_dict()).to_dict() ==
                emulation_attack_observation_state.to_dict())
        assert (EmulationAttackerObservationState.from_dict
                (emulation_attack_observation_state.to_dict()) ==
                emulation_attack_observation_state)

    def test_emulation_connection_observation_state(self) -> None:
        """
                Tests creation and dict conversion of the EmulationConnectionObservationState DAO

                :return: None
                """
        emulation_connection_observation_state = (EmulationConnectionObservationState
                                                  (conn=None, credential=Credential(username="shahab", pw="123"),
                                                   root=False, service="test1", port=123))

        assert isinstance(emulation_connection_observation_state.to_dict(), dict)

        assert isinstance(EmulationConnectionObservationState.from_dict
                          (emulation_connection_observation_state.to_dict()),
                          EmulationConnectionObservationState)
        assert (EmulationConnectionObservationState.from_dict
                (emulation_connection_observation_state.to_dict()).to_dict() ==
                emulation_connection_observation_state.to_dict())
        assert (EmulationConnectionObservationState.from_dict
                (emulation_connection_observation_state.to_dict()) ==
                emulation_connection_observation_state)
