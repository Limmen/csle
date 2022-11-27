from typing import List, Dict, Any
import json
import os
import csle_common.constants.constants as constants
from csle_common.dao.encoding.np_encoder import NpEncoder


class SimulationTrace:
    """
    Class that represents a trace in the simulation system
    """

    def __init__(self, simulation_env: str):
        """
        Initializes the DTO
        """
        self.simulation_env = simulation_env
        self.attacker_rewards = []
        self.defender_rewards = []
        self.attacker_observations = []
        self.defender_observations = []
        self.infos = []
        self.dones = []
        self.attacker_actions = []
        self.defender_actions = []
        self.states = []
        self.beliefs = []
        self.infrastructure_metrics = []
        self.id = -1

    def __str__(self) -> str:
        """
        :return: a string representation of the trace
        """
        return f"simulation_env: {self.simulation_env}, attacker_rewards:{self.attacker_rewards}, " \
               f"defender_rewards:{self.defender_rewards}, attacker_observations:{self.attacker_observations}, " \
               f"defender_observations:{self.defender_observations}, " \
               f"infos:{self.infos}, dones:{self.dones}, attacker_actions:{self.attacker_actions}, " \
               f"defender_actions:{self.defender_actions}, states: {self.states}, beliefs: {self.beliefs}, " \
               f"infrastructure_metrics: {self.infrastructure_metrics}, id: {self.id}"

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the trace
        """
        return {
            "simulation_env": self.simulation_env,
            "attacker_rewards": self.attacker_rewards,
            "defender_rewards": self.defender_rewards,
            "attacker_observations": self.attacker_observations,
            "defender_observations": self.defender_observations,
            "infos": self.infos,
            "dones": self.dones,
            "attacker_actions": self.attacker_actions,
            "defender_actions": self.defender_actions,
            "states": self.states,
            "beliefs": self.beliefs,
            "infrastructure_metrics": self.infrastructure_metrics,
            "id": self.id
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "SimulationTrace":
        """
        Converts a dict representation of the trace to a DTO representation

        :param d: the dict to convert
        :return: the trace DTO
        """
        trace = SimulationTrace(simulation_env=d["simulation_env"])
        if "attacker_rewards" in d:
            trace.attacker_rewards = d["attacker_rewards"]
        if "defender_rewards" in d:
            trace.defender_rewards = d["defender_rewards"]
        if "attacker_observations" in d:
            trace.attacker_observations = d["attacker_observations"]
        if "defender_observations" in d:
            trace.defender_observations = d["defender_observations"]
        if "infos" in d:
            trace.infos = d["infos"]
        if "dones" in d:
            trace.dones = d["dones"]
        if "attacker_actions" in d:
            trace.attacker_actions = d["attacker_actions"]
        if "defender_actions" in d:
            trace.defender_actions = d["defender_actions"]
        if "beliefs" in d:
            trace.beliefs = d["beliefs"]
        if "states" in d:
            trace.states = d["states"]
        if "infrastructure_metrics" in d:
            trace.infrastructure_metrics = d["infrastructure_metrics"]
        if "id" in d:
            trace.id = d["id"]
        return trace

    @staticmethod
    def save_traces(traces_save_dir, traces: List["SimulationTrace"], traces_file: str = None) -> None:
        """
        Utility function for saving a list of traces to a json file

        :param traces_save_dir: the directory where to save the traces
        :param traces: the traces to save
        :param traces_file: the filename of the traces file
        :return: None
        """
        if traces_file is None:
            traces_file = constants.SYSTEM_IDENTIFICATION.SIMULATION_TRACES_FILE
        traces = list(map(lambda x: x.to_dict(), traces))
        if not os.path.exists(traces_save_dir):
            os.makedirs(traces_save_dir)
        with open(traces_save_dir + constants.COMMANDS.SLASH_DELIM + traces_file, 'w') as fp:
            json.dump({"traces": traces}, fp, cls=NpEncoder)

    @staticmethod
    def load_traces(traces_save_dir: str, traces_file: str = None) -> List["SimulationTrace"]:
        """
        Utility function for loading and parsing a list of traces from a json file

        :param traces_save_dir: the directory where to load the traces from
        :param traces_file: (optional) a custom name of the traces file
        :return: a list of the loaded traces
        """
        if traces_file is None:
            traces_file = constants.SYSTEM_IDENTIFICATION.SIMULATION_TRACES_FILE
        path = traces_save_dir + constants.COMMANDS.SLASH_DELIM + traces_file
        if os.path.exists(path):
            with open(path, 'r') as fp:
                d = json.load(fp)
                traces = d["traces"]
                traces = list(map(lambda x: SimulationTrace.from_dict(x), traces))
                return traces
        else:
            print("Warning: Could not read traces file, path does not exist:{}".format(path))
            return []
