from abc import ABC

from csle_common.dao.action.attacker.base_attacker_action_config import BaseAttackerActionConfig
from csle_common.dao.action.defender.base_defender_action_config import BaseDefenderActionConfig


class BaseCSLEEnvConfig(ABC):
    """
    Abstract class representing the configuration of a csle environment
    """

    def __init__(self, attacker_action_conf: BaseAttackerActionConfig,
                 defender_action_conf: BaseDefenderActionConfig, manual_play: bool = False,
                 attacker_exploration_filter_illegal: bool = False):
        """
        Initializes the configuration

        :param attacker_action_conf: the configuration of the attacker's action space
        :param defender_action_conf: the configuration of the defender's action space
        :param manual_play: boolean flag whether the environment is supposed to be used for manual interation or not
        :param attacker_exploration_filter_illegal: boolean flag whether illegal actions should be masked during exploration
        """
        self.attacker_action_conf = attacker_action_conf
        self.defender_action_conf = defender_action_conf
        self.manual_play = manual_play
        self.attacker_exploration_filter_illegal = attacker_exploration_filter_illegal

