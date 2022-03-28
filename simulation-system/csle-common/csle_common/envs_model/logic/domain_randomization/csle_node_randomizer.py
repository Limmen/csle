from abc import ABC, abstractmethod
from csle_common.dao.network.node import Node


class CSLENodeRandomizer(ABC):

    @staticmethod
    @abstractmethod
    def randomize(CSLENodeRandomizerConfig)-> Node:
        pass

