from typing import List, Tuple
from abc import ABC, abstractmethod
from csle_common.dao.domain_randomization.randomization_space import RandomizationSpace
from csle_common.dao.domain_randomization.randomization_space_config import RandomizationSpaceConfig
from csle_common.dao.network.emulation_env_agent_config import EmulationEnvAgentConfig
from csle_common.dao.network.network_config import NetworkConfig


class CSLEDomainRandomizer(ABC):


    @staticmethod
    @abstractmethod
    def generate_randomization_space(config: RandomizationSpaceConfig) -> RandomizationSpace:
        pass


    @staticmethod
    @abstractmethod
    def randomize(subnet_prefix: str, network_ids: List, r_space: RandomizationSpace, env_config: EmulationEnvAgentConfig) \
            -> Tuple[NetworkConfig, EmulationEnvAgentConfig]:
        pass