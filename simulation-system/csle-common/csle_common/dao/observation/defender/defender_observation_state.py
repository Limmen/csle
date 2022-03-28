from typing import List
from csle_common.dao.observation.defender.defender_machine_observation_state import DefenderMachineObservationState
from csle_common.dao.action.defender.defender_action import DefenderAction


class DefenderObservationState:
    """
    Represents the defender's agent's current belief state of the environment
    """

    def __init__(self):
        """
        Initializes the DTO

        :param num_machines: the numer of machines
        :param ids: whether there is an IDS or not
        """
        self.machines : List[DefenderMachineObservationState] = []
        self.defense_actions_tried = set()
        self.step = 1

    def sort_machines(self) -> None:
        """
        Sorts the machines in the observation

        :return: None
        """
        self.machines = sorted(self.machines, key=lambda x: int(x.internal_ip.rsplit(".", 1)[-1]), reverse=False)

    def cleanup(self) -> None:
        """
        Cleans up the machines in the observation

        :return: None
        """
        for m in self.machines:
            m.cleanup()

    def get_action_ip(self, a : DefenderAction) -> List[str]:
        """
        Gets the ip of the node that a defender action is targeted for

        :param a: the action
        :return: the ip of the target node
        """
        if a.index == -1:
            self.sort_machines()
            ips = list(map(lambda x: x.internal_ip, self.machines))
            return ips
        if a.index < len(self.machines):
            return self.machines[a.index].ips
        return a.ips

    def copy(self) -> "DefenderObservationState":
        """
        :return: a copy of the object
        """
        c = DefenderObservationState()
        c.defense_actions_tried = self.defense_actions_tried.copy()

        for m in self.machines:
            c.machines.append(m.copy())
        return c

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "\n".join([str(i) + ":" + str(self.machines[i]) for i in range(len(self.machines))])
