from typing import List
import json
import os
import numpy as np
import csle_common.constants.constants as constants
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_observation.attacker.emulation_attacker_observation_state \
    import EmulationAttackerObservationState
from csle_common.dao.emulation_observation.defender.emulation_defender_observation_state \
    import EmulationDefenderObservationState


class EmulationTrace:
    """
    DTO class representing a trace in the emulation system
    """

    def __init__(self, initial_attacker_observation_state: EmulationAttackerObservationState,
                 initial_defender_observation_state: EmulationDefenderObservationState, emulation_name : str):
        """
        Initializes the DTO

        :param initial_attacker_observation_state: the initial state of the attacker
        :param initial_defender_observation_state: the intial state of the defender
        :param emulation_name: the name of the emulation
        """
        self.initial_attacker_observation_state = initial_attacker_observation_state
        self.initial_defender_observation_state = initial_defender_observation_state
        self.attacker_observation_states : List[EmulationAttackerObservationState] = []
        self.defender_observation_states : List[EmulationDefenderObservationState] = []
        self.attacker_actions : List[EmulationAttackerAction] = []
        self.defender_actions : List[EmulationDefenderAction] = []
        self.emulation_name = emulation_name

    def __str__(self):
        """
        :return: a string representation of the object
        """
        print(f"initial_attacker_observation_state:{self.initial_attacker_observation_state}"
              f"initial_defender_observation_state:{self.initial_defender_observation_state}"
              f"attacker_observation_states:{self.attacker_observation_states}\n"
              f"defender_observation_states:{self.defender_observation_states}\n"
              f"attacker_actions:{self.attacker_actions}\n"
              f"defender_actions:{self.defender_actions}\n"
              f"emulation_name: {self.emulation_name}")

    @staticmethod
    def from_dict(d: dict) -> "EmulationTrace":
        """
        Converts a dict representation into an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = EmulationTrace(
            initial_attacker_observation_state=EmulationAttackerObservationState.from_dict(
                d["initial_attacker_observation_state"]),
            initial_defender_observation_state=EmulationDefenderObservationState.from_dict(
                d["initial_defender_observation_state"]),
            emulation_name=d["emulation_name"]
        )
        obj.attacker_observation_states = list(map(lambda x: EmulationAttackerObservationState.from_dict(x),
                                                   d["attacker_observation_states"]))
        obj.defender_observation_states = list(map(lambda x: EmulationDefenderObservationState.from_dict(x),
                                                   d["defender_observation_states"]))
        obj.attacker_actions = list(map(lambda x: EmulationAttackerAction.from_dict(x),
                                                   d["attacker_actions"]))
        obj.defender_actions = list(map(lambda x: EmulationDefenderAction.from_dict(x),
                                        d["defender_actions"]))
        return obj

    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["initial_attacker_observation_state"] = self.initial_attacker_observation_state.to_dict()
        d["initial_defender_observation_state"] = self.initial_defender_observation_state.to_dict()
        d["attacker_observation_states"] = list(map(lambda x: x.to_dict(), self.attacker_observation_states))
        d["defender_observation_states"] = list(map(lambda x: x.to_dict(), self.defender_observation_states))
        d["attacker_actions"] = list(map(lambda x: x.to_dict(), self.attacker_actions))
        d["defender_actions"] = list(map(lambda x: x.to_dict(), self.defender_actions))
        d["emulation_name"] = self.emulation_name
        return d

    @staticmethod
    def save_traces_to_disk(traces_save_dir, traces : List["EmulationTrace"],
                            traces_file : str = None) -> None:
        """
        Utility function for saving a list of traces to a json file

        :param traces_save_dir: the directory where to save the traces
        :param traces: the traces to save
        :param traces_file: the filename of the traces file
        :return: None
        """
        traces = list(map(lambda x: x.to_dict(), traces))
        if traces_file is None:
            traces_file =  constants.SYSTEM_IDENTIFICATION.TRACES_FILE
        if not os.path.exists(traces_save_dir):
            os.makedirs(traces_save_dir)
        with open(traces_save_dir + "/" + traces_file, 'w') as fp:
            json.dump({"traces": traces}, fp, cls=NpEncoder)

    @staticmethod
    def load_traces_from_disk(traces_save_dir, traces_file : str = None) -> List["EmulationTrace"]:
        """
        Utility function for loading and parsing a list of traces from a json file

        :param traces_save_dir: the directory where to load the traces from
        :param traces_file: (optional) a custom name of the traces file
        :return: a list of the loaded traces
        """
        if traces_file is None:
            traces_file =  constants.SYSTEM_IDENTIFICATION.TRACES_FILE
        path = traces_save_dir + constants.COMMANDS.SLASH_DELIM + traces_file
        if os.path.exists(path):
            with open(path, 'r') as fp:
                d = json.load(fp)
                traces  = d["traces"]
                traces = list(map(lambda x: EmulationTrace.from_dict(x), traces))
                return traces
        else:
            print("Warning: Could not read traces file, path does not exist:{}".format(path))
            return []


class NpEncoder(json.JSONEncoder):
    """
    Encoder for Numpy arrays to JSON
    """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)