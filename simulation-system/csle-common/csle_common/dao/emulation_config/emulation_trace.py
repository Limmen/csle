from typing import List
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

    def __init__(self):
        self.attacker_observation_states : List[EmulationAttackerObservationState] = []
        self.defender_observation_states : List[EmulationDefenderObservationState] = []
        self.attacker_actions : List[EmulationAttackerAction] = []
        self.defender_actions : List[EmulationDefenderAction] = []

    def __str__(self):
        """
        :return: a string representation of the object
        """
        print(f"attacker_observation_states:{self.attacker_observation_states}\n"
              f"defender_observation_states:{self.defender_observation_states}\n"
              f"attacker_actions:{self.attacker_actions}\n"
              f"defender_actions:{self.defender_actions}\n")

    def to_dict(self) -> dict:
        d = {}
        d["attacker_observation_states"] = self.attacker_observation_states
        d["defender_observation_states"] = self.defender_observation_states
        d["attacker_actions"] = self.attacker_actions
        d["defender_actions"] = self.defender_actions
        return d