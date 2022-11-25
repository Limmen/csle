from typing import List, Union
from abc import ABC, abstractmethod
import os
import time
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.experiment_execution import ExperimentExecution
from csle_common.logging.log import Logger


class BaseAgent(ABC):
    """
    Abstract class representing an RL agent
    """

    def __init__(self, simulation_env_config: SimulationEnvConfig,
                 emulation_env_config: Union[None, EmulationEnvConfig], experiment_config: ExperimentConfig) -> None:
        """
        Initializes the agent

        :param simulation_env_config: the configuration of the simulation environment
        :param emulation_env_config: the configuration of the emulation environment
        :param experiment_config: the experiment configuration
        """
        self.simulation_env_config = simulation_env_config
        self.emulation_env_config = emulation_env_config
        self.experiment_config = experiment_config
        ts = time.time()
        if self.experiment_config.output_dir[-1] == "/":
            self.experiment_config.output_dir = self.experiment_config.output_dir[0:-1]
        self.experiment_config.output_dir = self.experiment_config.output_dir + f"_{ts}/"
        try:
            if not os.path.exists(self.experiment_config.output_dir):
                os.makedirs(self.experiment_config.output_dir)
        except Exception:
            Logger.__call__().get_logger().info("There was an error creating log dirs.")

    @abstractmethod
    def train(self) -> ExperimentExecution:
        pass

    @abstractmethod
    def hparam_names(self) -> List[str]:
        pass
