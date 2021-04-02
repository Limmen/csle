from typing import List
import gym
from gym_pycr_ctf.dao.action.defender.defender_action import DefenderAction
from gym_pycr_ctf.dao.action.defender.defender_action_id import DefenderActionId
from gym_pycr_ctf.dao.action.defender.defender_update_state_actions import DefenderUpdateStateActions

class DefenderActionConfig:
    """
    Configuration of the action space for the defender
    """
    def __init__(self, num_indices : int, actions: List[DefenderAction] = None,
                 stopping_action_ids : List[int] = None):
        """
        Class constructor

        :param num_indices: max num machine indexes allowed
        :param actions: list of actions in the action space
        :param stopping_action_ids: list of ids of the actions that are stopping actions
        """
        self.actions = actions
        self.num_actions = len(self.actions)
        self.num_indices = num_indices
        self.action_space = gym.spaces.Discrete(self.num_actions)
        self.action_lookup_d = {}
        self.action_lookup_d_val = {}
        for action in actions:
            self.action_lookup_d[(action.id, action.index)] = action
            self.action_lookup_d_val[(action.id.value, action.index)] = action

        self.stopping_action_ids = stopping_action_ids
        self.action_ids = self.stopping_action_ids
        self.num_node_specific_actions = len(self.action_ids)
        self.state_update_action = DefenderUpdateStateActions.UPDATE_STATE(index=-1)
        self.state_init_action = DefenderUpdateStateActions.INITIALIZE_STATE(index=-1)
        self.state_reset_action = DefenderUpdateStateActions.RESET_STATE(index=-1)

    def print_actions(self) -> None:
        """
        Utility function for printing the list of actions

        :return: None
        """
        print("Defender Actions:")
        for i, action in enumerate(self.actions):
            tag = "-"
            if not action.subnet:
                if action.index is not None:
                    tag = str(action.index)
            else:
                tag = "*"
            print(str(i) + ":" + action.name + "[" + tag + "] c:" + str(action.cost))


    def get_continue_action_idx(self):
        for i in range(len(self.actions)):
            if self.actions[i].id == DefenderActionId.CONTINUE:
                return i
        raise ValueError("No Continue Action in the action space")
