from abc import ABC, abstractmethod
from pycr_common.dao.agent.base_tensorboard_data_dto import BaseTensorboardDataDTO


class BaseAttackerTrainAgentLogDTOAvg(ABC):


    @abstractmethod
    @staticmethod
    def to_tensorboard_dto(avg_log_dto: "BaseAttackerTrainAgentLogDTOAvg", eps: float,
                           tensorboard_writer) -> BaseTensorboardDataDTO:
        pass