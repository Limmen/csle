from typing import List
from csle_common.dao.action.defender.base_defender_action import BaseDefenderAction
from gym_csle_ctf.dao.action.defender.defender_action_type import DefenderActionType
from gym_csle_ctf.dao.action.defender.defender_action_id import DefenderActionId
from gym_csle_ctf.dao.action.defender.defender_action_outcome import DefenderActionOutcome


class DefenderAction(BaseDefenderAction):
    """
    Class representing an action of the defender in the environment
    """

    def __init__(self, id : DefenderActionId, name :str, cmd : List[str],
                 type: DefenderActionType, descr: str, cost: float,
                 ip :str, index: int, subnet : bool = False,
                 action_outcome: DefenderActionOutcome = DefenderActionOutcome.GAME_END,
                 alt_cmd = List[str]):
        """
        Class constructor

        :param id: id of the action
        :param name: name of the action
        :param cmd: command-line commands to apply the action on the emulation
        :param type: type of the action
        :param descr: description of the action (documentation)
        :param cost: cost of the action
        :param ip: ip of the machine to apply the action to
        :param index: index of the machine to apply the action to
        :param subnet: if True, apply action to entire subnet
        :param action_outcome: type of the outcome of the action
        :param alt_cmd: alternative command if the first command does not work
        """
        super().__init__()
        self.id = id
        self.name = name
        self.cmd = cmd
        self.type = type
        self.descr = descr
        self.cost = cost
        self.ip = ip
        self.subnet = subnet
        self.action_outcome = action_outcome
        self.alt_cmd = alt_cmd
        self.index = index

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "id:{},name:{},ip:{},subnet:{},index:{}".format(self.id, self.name, self.ip, self.subnet,self.index)
