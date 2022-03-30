from typing import List
from csle_common.dao.emulation_action.defender.emulation_defender_action_type import EmulationDefenderActionType
from csle_common.dao.emulation_action.defender.emulation_defender_action_id import EmulationDefenderActionId
from csle_common.dao.emulation_action.defender.emulation_defender_action_outcome import EmulationDefenderActionOutcome


class EmulationDefenderAction:
    """
    Class representing an action of the defender in the environment
    """

    def __init__(self, id : EmulationDefenderActionId, name :str, cmd : List[str],
                 type: EmulationDefenderActionType, descr: str, cost: float,
                 ips : List[str], index: int, subnet : bool = False,
                 action_outcome: EmulationDefenderActionOutcome = EmulationDefenderActionOutcome.GAME_END,
                 alt_cmd = List[str]):
        """
        Class constructor

        :param id: id of the action
        :param name: name of the action
        :param cmd: command-line commands to apply the action on the emulation
        :param type: type of the action
        :param descr: description of the action (documentation)
        :param cost: cost of the action
        :param ips: ip of the machine to apply the action to
        :param index: index of the machine to apply the action to
        :param subnet: if True, apply action to entire subnet
        :param action_outcome: type of the outcome of the action
        :param alt_cmd: alternative command if the first command does not work
        """
        self.id = id
        self.name = name
        self.cmd = cmd
        self.type = type
        self.descr = descr
        self.cost = cost
        self.ips = ips
        self.subnet = subnet
        self.action_outcome = action_outcome
        self.alt_cmd = alt_cmd
        self.index = index

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "id:{},name:{},ips:{},subnet:{},index:{}".format(self.id, self.name, self.ips, self.subnet, self.index)
