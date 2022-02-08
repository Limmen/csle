from abc import ABC, abstractmethod

from csle_common.dao.agent.base_train_agent_log_dto import BaseTrainAgentLogDTO


class BaseEvalUtil(ABC):

    @staticmethod
    @abstractmethod
    def eval_defender(env, model, train_log_dto: BaseTrainAgentLogDTO, deterministic: bool = False) -> \
            BaseTrainAgentLogDTO:
        pass