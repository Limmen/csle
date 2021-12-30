from typing import List, Tuple
from abc import ABC, abstractmethod
from pycr_common.dao.domain_randomization.pycr_randomization_space import PyCRRandomizationSpace
from pycr_common.dao.domain_randomization.pycr_randomization_space_config import PyCRRandomizationSpaceConfig
from pycr_common.dao.network.base_env_config import BasePyCREnvConfig
from pycr_common.dao.network.network_config import NetworkConfig


class PyCRDomainRandomizer(ABC):


    @staticmethod
    @abstractmethod
    def generate_randomization_space(config: PyCRRandomizationSpaceConfig) -> PyCRRandomizationSpace:
        pass


    @staticmethod
    @abstractmethod
    def randomize(subnet_prefix: str, network_ids: List, r_space: PyCRRandomizationSpace, env_config: BasePyCREnvConfig) \
            -> Tuple[NetworkConfig, BasePyCREnvConfig]:
        pass