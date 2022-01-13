from abc import ABC, abstractmethod
from csle_common.dao.network.node import Node
from csle_common.dao.domain_randomization.csle_node_randomizer_config import CSLENodeRandomizerConfig


class CSLENodeRandomizer(ABC):


    @staticmethod
    @abstractmethod
    def randomize(CSLENodeRandomizerConfig)-> Node:
        pass

