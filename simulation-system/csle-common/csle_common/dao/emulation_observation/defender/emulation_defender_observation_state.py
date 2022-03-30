from typing import List
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.emulation_observation.defender.emulation_defender_machine_observation_state \
    import EmulationDefenderMachineObservationState
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction


class EmulationDefenderObservationState:
    """
    Represents the defender's agent's current belief state of the emulation
    """

    def __init__(self):
        """
        Initializes the DTO

        :param num_machines: the numer of machines
        :param ids: whether there is an IDS or not
        """
        self.machines : List[EmulationDefenderMachineObservationState] = []
        self.actions_tried = set()


    @staticmethod
    def from_dict(d: dict)-> "EmulationDefenderObservationState":
        """
        Converts a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = EmulationDefenderObservationState()
        obj.machines = list(map(lambda x: EmulationDefenderMachineObservationState.from_dict(x), d["machines"]))
        obj.actions_tried = set(d["actions_tried"])

    def to_dict(self) -> dict:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["machines"] = list(map(lambda x: x.to_dict(), self.machines))
        d["actions_tried"] = list(self.actions_tried)
        return d

    def sort_machines(self) -> None:
        """
        Sorts the machines in the observation

        :return: None
        """
        self.machines = sorted(self.machines, key=lambda x: int(x.ips[0].rsplit(".", 1)[-1]), reverse=False)

    def cleanup(self) -> None:
        """
        Cleans up the machines in the observation

        :return: None
        """
        for m in self.machines:
            m.cleanup()

    def get_action_ips(self, a : EmulationDefenderAction, emulation_env_config: EmulationEnvConfig) -> List[str]:
        """
        Gets the ips of the node that a defender action is targeted for

        :param a: the action
        :param emulation_env_config: the emulation env config
        :return: the ip of the target node
        """
        if a.index == -1:
            return emulation_env_config.topology_config.subnetwork_masks
        if a.index < len(self.machines):
            return self.machines[a.index].ips
        return a.ips

    def copy(self) -> "EmulationDefenderObservationState":
        """
        :return: a copy of the object
        """
        c = EmulationDefenderObservationState()
        c.actions_tried = self.actions_tried.copy()

        for m in self.machines:
            c.machines.append(m.copy())
        return c

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "\n".join([str(i) + ":" + str(self.machines[i]) for i in range(len(self.machines))])
