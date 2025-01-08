from typing import List, Union
from abc import ABC, abstractmethod
import os
import time
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.experiment_execution import ExperimentExecution
from csle_common.logging.log import Logger
from csle_tolerance.util.general_util import GeneralUtil


class BaseAgent(ABC):
    """
    Abstract class representing an RL agent
    """

    def __init__(self, simulation_env_config: SimulationEnvConfig,
                 emulation_env_config: Union[EmulationEnvConfig, None], experiment_config: ExperimentConfig,
                 create_log_dir: bool = True) -> None:
        """
        Initializes the agent

        :param simulation_env_config: the configuration of the simulation environment
        :param emulation_env_config: the configuration of the emulation environment
        :param experiment_config: the experiment configuration
        :param create_log_dir: Boolean flag whether to create a log directory or not
        """
        GeneralUtil.register_envs()
        self.simulation_env_config = simulation_env_config
        self.emulation_env_config = emulation_env_config
        self.experiment_config = experiment_config
        ts = time.time()
        if create_log_dir:
            if self.experiment_config.output_dir[-1] == "/":
                self.experiment_config.output_dir = self.experiment_config.output_dir[0:-1]
            self.experiment_config.output_dir = self.experiment_config.output_dir + f"_{ts}/"
            try:
                if not os.path.exists(self.experiment_config.output_dir):
                    os.makedirs(self.experiment_config.output_dir)
            except Exception as e:
                Logger.__call__().get_logger().info(f"There was an error creating log dirs: {str(e)}, {repr(e)}")

    @abstractmethod
    def train(self) -> ExperimentExecution:
        """
        Abstract method to be implemented by subclasses. Should contain the training logic

        :return: the training result
        """
        pass

    @abstractmethod
    def hparam_names(self) -> List[str]:
        """
        Abstract method to be implemented by subclasses. Gets the list of hyperparameters.

        :return: the list of hyperparameters
        """
        pass
