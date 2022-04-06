from typing import Dict, Any
from csle_common.dao.emulation_config.emulation_trace import EmulationTrace
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace


class EmulationSimulationTrace:
    """
    DTO class representing a combined emulation and simulation trace
    """

    def __init__(self, emulation_trace: EmulationTrace, simulation_trace: SimulationTrace):
        """
        Intializes the DTO

        :param emulation_trace: the emulation trace
        :param simulation_trace: the simulation trace
        """
        self.emulation_trace = emulation_trace
        self.simulation_trace = simulation_trace

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EmulationSimulationTrace":
        """
        Converts a dict representation into an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = EmulationSimulationTrace(
            emulation_trace=EmulationTrace.from_dict(d["emulation_trace"]),
            simulation_trace=SimulationTrace.from_dict(d["simulation_trace"]),
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the DTO
        """
        d = {}
        d["emulation_trace"] = self.emulation_trace.to_dict()
        d["simulation_trace"] = self.simulation_trace.to_dict()
        return d

    def __str__(self):
        """
        :return: a string representation of the object
        """
        return f"emulation_trace:{self.emulation_trace}, simulation_trace:{self.simulation_trace}"