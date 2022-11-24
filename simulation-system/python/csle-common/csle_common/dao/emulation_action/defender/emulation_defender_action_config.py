from typing import List
import gym
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_action.defender.emulation_defender_action_id import EmulationDefenderActionId
from csle_common.dao.emulation_action.defender.emulation_defender_stopping_actions \
    import EmulationDefenderStoppingActions


class EmulationDefenderActionConfig:
    """
    Configuration of the action space for the defender
    """
    def __init__(self, num_indices: int, actions: List[EmulationDefenderAction] = None,
                 stopping_action_ids: List[EmulationDefenderActionId] = None,
                 multiple_stop_actions: List[EmulationDefenderAction] = None,
                 multiple_stop_actions_ids: List[EmulationDefenderActionId] = None):
        """
        Class constructor

        :param num_indices: max num machine indexes allowed
        :param actions: list of actions in the action space
        :param stopping_action_ids: list of ids of the actions that are stopping actions
        :param multiple_stop_actions: if it is a multiple stopping environment, this defines the list of stop actions
        :param multiple_stop_actions_ids: if it is a multiple stopping environment, this defines the ids of
                                          the stop actions
        """
        self.num_actions = len(actions)
        self.actions = actions
        self.num_actions = len(self.actions)
        self.num_indices = num_indices
        self.action_space = gym.spaces.Discrete(self.num_actions)
        self.action_lookup_d = {}
        self.action_lookup_d_val = {}
        for action in actions:
            self.action_lookup_d[(action.id, action.index)] = action
            self.action_lookup_d_val[(action.id, action.index)] = action

        self.stopping_action_ids = stopping_action_ids
        self.action_ids = self.stopping_action_ids
        self.multiple_stop_actions = multiple_stop_actions
        self.multiple_stop_actions_ids = multiple_stop_actions_ids
        self.num_node_specific_actions = len(self.action_ids)

    def print_actions(self) -> None:
        """
        Utility function for printing the list of actions

        :return: None
        """
        print("Defender Actions:")
        for i, action in enumerate(self.actions):
            tag = "-"
            if not action.index == -1 and action.index is not None:
                tag = str(action.index)
            else:
                tag = "*"
            print(str(i) + ":" + action.name + "[" + tag + "]")

    def get_continue_action_idx(self) -> int:
        """
        :return: the index of the continue action
        """
        for i in range(len(self.actions)):
            if self.actions[i].id == EmulationDefenderActionId.CONTINUE:
                return i
        raise ValueError("No Continue Action in the action space")

    @staticmethod
    def all_actions_config(num_nodes: int, subnet_masks: List[str]) -> "EmulationDefenderActionConfig":
        """
        Creates an action configuration for the defender with all actions

        :param num_nodes: the number of nodes in the environment
        :param subnet_masks: the the subnet masks in the environment
        :return: the action configuration
        """
        defender_actions = []

        # Host actions
        for idx in range(num_nodes):
            pass

        # Subnet actions
        defender_actions.append(EmulationDefenderStoppingActions.STOP(index=num_nodes + 1))
        defender_actions.append(EmulationDefenderStoppingActions.CONTINUE(index=num_nodes + 1))

        defender_actions = sorted(defender_actions, key=lambda x: (x.id, x.index))
        stopping_action_ids = [
            EmulationDefenderActionId.STOP, EmulationDefenderActionId.CONTINUE
        ]
        defender_action_config = EmulationDefenderActionConfig(
            num_indices=num_nodes + 1, actions=defender_actions, stopping_action_ids=stopping_action_ids)
        return defender_action_config
