from abc import ABC, abstractmethod
from pycr_common.dao.network.base_env_config import BaseEnvConfig
from pycr_common.dao.agent.base_rollout_data_dto import BaseRolloutDataDTO
from pycr_common.dao.agent.train_mode import TrainMode
from pycr_common.agents.config.agent_config import AgentConfig
from pycr_common.dao.envs.base_pycr_env import BasePyCREnv

class BaseTrainAgentLogDTO(ABC):

    def __init__(self, iteration: int):
        self.iteration = iteration


    @abstractmethod
    def eval_update(self, attacker_episode_reward, defender_episode_reward, _info: dict, episode_length: int,
                    env_conf: BaseEnvConfig, i: int) -> None:
        pass

    @abstractmethod
    def eval_2_update(self, attacker_episode_reward, defender_episode_reward, _info: dict, episode_length: int,
                    env_conf: BaseEnvConfig, i: int) -> None:
        pass


    @abstractmethod
    def copy(self)-> "BaseTrainAgentLogDTO":
        pass


    @abstractmethod
    def initialize(self) -> None:
        pass


    @abstractmethod
    def update(self, rollout_data_dto: BaseRolloutDataDTO, start):
        pass


    @abstractmethod
    def copy_saved_env_2(self, saved_log_dto: "BaseTrainAgentLogDTO") -> None:
        pass

    @abstractmethod
    def get_avg_attacker_dto(self, attacker_agent_config: AgentConfig, env: BasePyCREnv,
                             env_2: BasePyCREnv, eval: bool):
        pass

    @abstractmethod
    def get_avg_defender_dto(self, defender_agent_config: AgentConfig, env: BasePyCREnv,
                             env_2: BasePyCREnv, eval: bool,
                             train_mode: TrainMode):
        pass