from abc import ABC

from pycr_common.dao.action.attacker.base_attacker_action_config import BaseAttackerActionConfig
from pycr_common.dao.action.defender.base_defender_action_config import BaseDefenderActionConfig


class BaseEnvConfig(ABC):

    def __init__(self, attacker_action_conf: BaseAttackerActionConfig,
                 defender_action_conf: BaseDefenderActionConfig, manual_play: bool = False,
                 attacker_exploration_filter_illegal: bool = False):
        self.attacker_action_conf = attacker_action_conf
        self.defender_action_conf = defender_action_conf
        self.manual_play = manual_play
        self.attacker_exploration_filter_illegal = attacker_exploration_filter_illegal

