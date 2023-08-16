from typing import Optional, List, Dict, Any
import gymnasium as gym
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_action.defender.emulation_defender_action_id import EmulationDefenderActionId
from csle_common.dao.emulation_action.defender.emulation_defender_stopping_actions \
    import EmulationDefenderStoppingActions
from csle_base.json_serializable import JSONSerializable


class EmulationDefenderActionConfig(JSONSerializable):
    """
    Configuration of the action space for the defender
    """

    def __init__(self, num_indices: int, actions: Optional[List[EmulationDefenderAction]] = None,
                 stopping_action_ids: Optional[List[EmulationDefenderActionId]] = None,
                 multiple_stop_actions: Optional[List[EmulationDefenderAction]] = None,
                 multiple_stop_actions_ids: Optional[List[EmulationDefenderActionId]] = None):
        """
        Class constructor

        :param num_indices: max num machine indexes allowed
        :param actions: list of actions in the action space
        :param stopping_action_ids: list of ids of the actions that are stopping actions
        :param multiple_stop_actions: if it is a multiple stopping environment, this defines the list of stop actions
        :param multiple_stop_actions_ids: if it is a multiple stopping environment, this defines the ids of
                                          the stop actions
        """
        self.actions = actions
        if self.actions is None:
            raise ValueError("Thera are no actions")
        self.num_actions = len(self.actions)
        self.num_indices = num_indices
        self.action_space = gym.spaces.Discrete(self.num_actions)
        self.action_lookup_d = {}
        self.action_lookup_d_val = {}
        if actions is not None:
            for action in actions:
                self.action_lookup_d[(action.id, action.index)] = action
                self.action_lookup_d_val[(action.id, action.index)] = action
        else:
            raise ValueError("actions is None and thus not iterable")

        self.stopping_action_ids = stopping_action_ids
        self.action_ids = self.stopping_action_ids
        self.multiple_stop_actions = multiple_stop_actions
        self.multiple_stop_actions_ids = multiple_stop_actions_ids
        if self.action_ids is not None:
            self.num_node_specific_actions = len(self.action_ids)
        else:
            raise ValueError("There are no number of node-specific actions")

    def print_actions(self) -> None:
        """
        Utility function for printing the list of actions

        :return: None
        """
        print("Defender Actions:")
        if self.actions is None:
            raise ValueError("self.actions is not iterable")
        else:
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
        if self.actions is None:
            raise ValueError("self.actions is None and thus has no length")
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

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"num_indices: {self.num_indices}, actions: {self.actions}, " \
               f"stopping_action_ids: {self.stopping_action_ids}, " \
               f"multiple_stop_actions: {self.multiple_stop_actions}, " \
               f"multiple_stop_actions_ids: {self.multiple_stop_actions_ids}"

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the object to a dict representation
        
        :return: a dict representation of the object
        """
        d: Dict[str, Any] = {}
        d["num_indices"] = self.num_indices
        d["actions"] = self.actions
        d["stopping_action_ids"] = self.stopping_action_ids
        d["multiple_stop_actions"] = self.multiple_stop_actions
        d["multiple_stop_actions_ids"] = self.multiple_stop_actions_ids
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EmulationDefenderActionConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = EmulationDefenderActionConfig(
            num_indices=d["num_indices"], actions=d["actions"],
            stopping_action_ids=d["stopping_action_ids"],
            multiple_stop_actions=d["multiple_stop_actions"],
            multiple_stop_actions_ids=d["multiple_stop_actions_ids"]
        )
        return obj

    @staticmethod
    def from_json_file(json_file_path: str) -> "EmulationDefenderActionConfig":
        """
        Reads a json file and converts it to a DTO

        :param json_file_path: the json file path
        :return: the converted DTO
        """
        import io
        import json
        with io.open(json_file_path, 'r') as f:
            json_str = f.read()
        return EmulationDefenderActionConfig.from_dict(json.loads(json_str))
