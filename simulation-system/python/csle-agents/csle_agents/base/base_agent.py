from typing import List, Union
from abc import ABC, abstractmethod
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.experiment_execution import ExperimentExecution



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

    @abstractmethod
    def train(self) -> ExperimentExecution:
        pass


    @abstractmethod
    def hparam_names(self) -> List[str]:
        pass