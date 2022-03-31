from typing import List
from csle_common.dao.emulation_action.defender.emulation_defender_action_type import EmulationDefenderActionType
from csle_common.dao.emulation_action.defender.emulation_defender_action_id import EmulationDefenderActionId
from csle_common.dao.emulation_action.defender.emulation_defender_action_outcome import EmulationDefenderActionOutcome


class EmulationDefenderAction:
    """
    Class representing an action of the defender in the environment
    """

    def __init__(self, id : EmulationDefenderActionId, name :str, cmds : List[str],
                 type: EmulationDefenderActionType, descr: str, cost: float,
                 ips : List[str], index: int, subnet : bool = False,
                 action_outcome: EmulationDefenderActionOutcome = EmulationDefenderActionOutcome.GAME_END,
                 alt_cmds : List[str] = None):
        """
        Class constructor

        :param id: id of the action
        :param name: name of the action
        :param cmds: command-line commands to apply the action on the emulation
        :param type: type of the action
        :param descr: description of the action (documentation)
        :param cost: cost of the action
        :param ips: ip of the machine to apply the action to
        :param index: index of the machine to apply the action to
        :param subnet: if True, apply action to entire subnet
        :param action_outcome: type of the outcome of the action
        :param alt_cmds: alternative command if the first command does not work
        """
        self.id = id
        self.name = name
        self.cmds = cmds
        self.type = type
        self.descr = descr
        self.cost = cost
        self.ips = ips
        self.subnet = subnet
        self.action_outcome = action_outcome
        self.alt_cmds = alt_cmds
        self.index = index

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "id:{},name:{},ips:{},subnet:{},index:{}".format(self.id, self.name, self.ips, self.subnet, self.index)

    @staticmethod
    def from_dict(d: dict) -> "EmulationDefenderAction":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the instance
        """
        obj = EmulationDefenderAction(
            id=d["id"], name=d["name"], cmds=d["cmds"], type=d["type"], descr=d["descr"], cost=d["cost"], ips=d["ips"],
            index=d["index"], subnet=d["subnet"], action_outcome=d["action_outcome"], alt_cmds=d["alt_cmds"]
        )
        return obj

    def to_dict(self) -> dict:
        """
        :return: a dicr representation of the object
        """
        d = {}
        d["id"] = self.id
        d["name"] = self.name
        d["cmds"] = self.cmds
        d["type"] = self.type
        d["descr"] = self.descr
        d["cost"] = self.cost
        d["ips"] = self.ips
        d["index"] = self.index
        d["subnet"] = self.subnet
        d["action_outcome"] = self.action_outcome
        d["alt_cmds"] = self.alt_cmds
        return d

    def ips_match(self, ips: List[str]) -> bool:
        """
        Checks if a list of ips overlap with the ips of this host

        :param ips: the list of ips to check
        :return:  True if they match, False otherwise
        """
        for ip in self.ips:
            if ip in ips:
                return True
        return False
