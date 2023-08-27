from csle_common.dao.emulation_observation.common.emulation_port_observation_state import EmulationPortObservationState
from csle_common.dao.emulation_config.transport_protocol import TransportProtocol


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
