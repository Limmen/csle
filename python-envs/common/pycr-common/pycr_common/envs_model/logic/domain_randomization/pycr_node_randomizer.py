from abc import ABC, abstractmethod
from pycr_common.dao.network.node import Node
from pycr_common.dao.domain_randomization.pycr_node_randomizer_config import PyCRNodeRandomizerConfig


class PyCRNodeRandomizer(ABC):


    @staticmethod
    @abstractmethod
    def randomize(PyCRNodeRandomizerConfig)-> Node:
        pass

