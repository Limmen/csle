from typing import List, Union
from abc import ABC, abstractmethod
import os
import time
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
from csle_common.dao.system_identification.system_identification_config import SystemIdentificationConfig
from csle_common.dao.system_identification.system_model import SystemModel
from csle_common.logging.log import Logger


class BaseSystemIdentificationAlgorithm(ABC):
    """
    Abstract class representing a system identification algorithm
    """

    def __init__(self, emulation_env_config: Union[None, EmulationEnvConfig], emulation_statistics: EmulationStatistics,
                 system_identification_config: SystemIdentificationConfig) -> None:
        """
        Initializes the algorithm

        :param emulation_env_config: the configuration of the emulation environment
        :param emulation_statistics: the statistics to use for training
        :param system_identification_config: the configuration of the algorithm
        """
        self.emulation_env_config = emulation_env_config
        self.system_identification_config = system_identification_config
        self.emulation_statistics = emulation_statistics
        ts = time.time()
        if self.system_identification_config.output_dir[-1] == "/":
            self.system_identification_config.output_dir = self.system_identification_config.output_dir[0:-1]
        self.system_identification_config.output_dir = self.system_identification_config.output_dir + f"_{ts}/"
        try:
            if not os.path.exists(self.system_identification_config.output_dir):
                os.makedirs(self.system_identification_config.output_dir)
        except Exception as e:
            Logger.__call__().get_logger().info(f"There was an error creating log dirs: {str(e)}, {repr(e)}")

    @abstractmethod
    def fit(self) -> SystemModel:
        """
        Abstract method to be implemented by subclasses. Fits the system model

        :return: the fitted system model
        """
        pass

    @abstractmethod
    def hparam_names(self) -> List[str]:
        """
        Abstract method to be implemented by subclasses. Gives the hyperparameters of the algorithm

        :return: the hyperparameters of the algorithm
        """
        pass
