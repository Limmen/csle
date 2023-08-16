from typing import Dict, Any
from csle_common.dao.emulation_config.emulation_trace import EmulationTrace
from csle_common.dao.simulation_config.simulation_trace import SimulationTrace
from csle_base.json_serializable import JSONSerializable


class EmulationSimulationTrace(JSONSerializable):
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
        self.id = -1

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
        obj.id = d["id"]
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the DTO
        """
        d: Dict[str, Any] = {}
        d["emulation_trace"] = self.emulation_trace.to_dict()
        d["simulation_trace"] = self.simulation_trace.to_dict()
        d["id"] = self.id
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"emulation_trace:{self.emulation_trace}, simulation_trace:{self.simulation_trace}, id:{self.id}"

    @staticmethod
    def from_json_file(json_file_path: str) -> "EmulationSimulationTrace":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return EmulationSimulationTrace.from_dict(json.loads(json_str))
