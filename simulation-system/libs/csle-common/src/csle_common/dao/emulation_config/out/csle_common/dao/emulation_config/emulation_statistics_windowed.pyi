from _typeshed import Incomplete
from csle_base.json_serializable import JSONSerializable
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction as EmulationAttackerAction
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction as EmulationDefenderAction
from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState as EmulationEnvState
from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics as EmulationStatistics
from csle_common.metastore.metastore_facade import MetastoreFacade as MetastoreFacade
from typing import Any, Dict

class EmulationStatisticsWindowed(JSONSerializable):
    window_size: Incomplete
    initial_states: Incomplete
    state_transitions: Incomplete
    emulation_name: Incomplete
    descr: Incomplete
    emulation_statistics: Incomplete
    statistics_id: Incomplete
    def __init__(self, window_size: int, emulation_name: str, descr: str) -> None: ...
    def add_initial_state(self, s: EmulationEnvState) -> None: ...
    def add_state_transition(self, s: EmulationEnvState, s_prime: EmulationEnvState, a1: EmulationDefenderAction, a2: EmulationAttackerAction) -> None: ...
    def update_emulation_statistics(self) -> None: ...
    @staticmethod
    def from_dict(d: Dict[str, Any]) -> EmulationStatisticsWindowed: ...
    def to_dict(self) -> Dict[str, Any]: ...
    @staticmethod
    def from_json_file(json_file_path: str) -> EmulationStatisticsWindowed: ...
