from typing import List
from abc import ABC, abstractmethod
from csle_common.dao.domain_randomization.randomization_space import RandomizationSpace
from csle_common.dao.domain_randomization.randomization_space_config import RandomizationSpaceConfig
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig


class CSLEDomainRandomizer(ABC):


    @staticmethod
    @abstractmethod
    def generate_randomization_space(config: RandomizationSpaceConfig) -> RandomizationSpace:
        pass


    @staticmethod
    @abstractmethod
    def randomize(subnet_prefix: str, network_ids: List, r_space: RandomizationSpace,
                  emulation_env_config: EmulationEnvConfig) -> EmulationEnvConfig:
        pass