from abc import ABC, abstractmethod
from pycr_common.dao.agent.base_tensorboard_data_dto import BaseTensorboardDataDTO


class BaseAttackerTrainAgentLogDTOAvg(ABC):
    """
    Abstract base class representing a DTO with average training metrics of the attacker
    """

    @staticmethod
    @abstractmethod
    def to_tensorboard_dto(avg_log_dto: "BaseAttackerTrainAgentLogDTOAvg", eps: float, tensorboard_writer) \
            -> BaseTensorboardDataDTO:
        """
        Converts the DTO to a TensorboardDTO

        :param avg_log_dto: the dto to convert
        :param eps: the machine epsilon value
        :param tensorboard_writer: a tensorboard writer
        :return: a tensorboard DTO
        """
        pass