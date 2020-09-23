from gym_pycr_pwcrack.dao.action.action import Action
from gym_pycr_pwcrack.dao.action.action_type import ActionType
from gym_pycr_pwcrack.dao.action.action_id import ActionId
from gym_pycr_pwcrack.dao.action.action import ActionOutcome

class ShellActions:

    @staticmethod
    def BASH_FIND_FLAG() -> Action:
        id = ActionId.BASH_FIND_FLAG
        cmd = "find / -name 'flag*.txt'  2>&1 | grep -v 'Permission denied'"
        return Action(id=id, name="Find flag", cmd=cmd,
                      type=ActionType.POST_EXPLOIT,
                      descr="Searches the file system for a flag",
                      cost=0.0, noise=0.0,
                      ip=None, subnet=False, action_outcome=ActionOutcome.FLAG)