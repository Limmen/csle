from typing import List, Tuple
from abc import ABC, abstractmethod
from csle_common.dao.domain_randomization.csle_randomization_space import CSLERandomizationSpace
from csle_common.dao.domain_randomization.csle_randomization_space_config import CSLERandomizationSpaceConfig
from csle_common.dao.network.base_env_config import BaseCSLEEnvConfig
from csle_common.dao.network.network_config import NetworkConfig


class CSLEDomainRandomizer(ABC):


    @staticmethod
    @abstractmethod
    def generate_randomization_space(config: CSLERandomizationSpaceConfig) -> CSLERandomizationSpace:
        pass


    @staticmethod
    @abstractmethod
    def randomize(subnet_prefix: str, network_ids: List, r_space: CSLERandomizationSpace, env_config: BaseCSLEEnvConfig) \
            -> Tuple[NetworkConfig, BaseCSLEEnvConfig]:
        pass