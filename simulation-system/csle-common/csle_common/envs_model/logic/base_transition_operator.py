from typing import Tuple
from abc import ABC, abstractmethod
from csle_common.dao.network.base_env_state import BaseEnvState
from csle_common.dao.network.base_env_config import BaseCSLEEnvConfig
from csle_common.dao.action.attacker.base_attacker_action import BaseAttackerAction
from csle_common.dao.action.defender.base_defender_action import BaseDefenderAction


class BaseTransitionOperator(ABC):

    @staticmethod
    @abstractmethod
    def attacker_transition(s: BaseEnvState, attacker_action: BaseAttackerAction, env_config: BaseCSLEEnvConfig) -> \
            Tuple[BaseEnvState, float, bool]:
        pass

    @staticmethod
    @staticmethod
    def defender_transition(s: BaseEnvState, defender_action: BaseDefenderAction, env_config: BaseCSLEEnvConfig,
                            attacker_action: BaseAttackerAction = None) \
            -> Tuple[BaseEnvState, float, bool]:
        pass