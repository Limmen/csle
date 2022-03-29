from abc import ABC, abstractmethod
from csle_common.dao.emulation_config.node_container_config import NodeContainerConfig


class CSLENodeRandomizer(ABC):

    @staticmethod
    @abstractmethod
    def randomize(CSLENodeRandomizerConfig)-> NodeContainerConfig:
        pass

