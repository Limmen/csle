from abc import ABC, abstractmethod
from csle_common.dao.network.base_env_config import BaseCSLEEnvConfig
from csle_common.dao.agent.base_rollout_data_dto import BaseRolloutDataDTO
from csle_common.dao.agent.train_mode import TrainMode
from csle_common.agents.config.agent_config import AgentConfig
from csle_common.dao.envs.base_csle_env import BaseCSLEEnv
from csle_common.dao.agent.base_attacker_train_agent_log_dto_avg import BaseAttackerTrainAgentLogDTOAvg
from csle_common.dao.agent.base_defender_train_agent_log_dto_avg import BaseDefenderTrainAgentLogDTOAvg


class BaseTrainAgentLogDTO(ABC):
    """
    Abstract base class that represents a DTO with training metrics
    """

    def __init__(self, iteration: int):
        """
        Class constructor

        :param iteration: the iteration
        """
        self.iteration = iteration


    @abstractmethod
    def eval_update(self, attacker_episode_reward, defender_episode_reward, _info: dict, episode_length: int,
                    env_conf: BaseCSLEEnvConfig, i: int) -> None:
        """
        A method for updating the DTO with more data during evaluation

        :param attacker_episode_reward: a list of rewards of the attacker
        :param defender_episode_reward: a list of rewards of the defender
        :param _info: a dict with the info
        :param episode_length: the length of the episode
        :param env_conf: the configuration of the environment
        :param i: the index
        :return: None
        """
        pass

    @abstractmethod
    def eval_2_update(self, attacker_episode_reward, defender_episode_reward, _info: dict, episode_length: int,
                      env_conf: BaseCSLEEnvConfig, i: int) -> None:
        """
        A method for updating the DTO during evaluation in the dedicate evaluation environment

        :param attacker_episode_reward: a list of rewards of the attacker
        :param defender_episode_reward: a list of rewards of the defender
        :param _info: the dict with info metrics
        :param episode_length: the length of the episode
        :param env_conf: the configuration of the environment
        :param i: the index
        :return: None
        """
        pass


    @abstractmethod
    def copy(self)-> "BaseTrainAgentLogDTO":
        """
        :return: a copy of the DTO
        """
        pass


    @abstractmethod
    def initialize(self) -> None:
        """
        Initialized the DTO

        :return: None
        """
        pass


    @abstractmethod
    def update(self, rollout_data_dto: BaseRolloutDataDTO, start, attacker_agent_config: AgentConfig) -> None:
        """
        A method for updating the DTO with new data during training

        :param rollout_data_dto: the DTO to update
        :param start: the start time of the training step (timestamp)
        :param attacker_agent_config: training configuration
        :return: None
        """
        pass


    @abstractmethod
    def copy_saved_env_2(self, saved_log_dto: "BaseTrainAgentLogDTO") -> None:
        """
        Copies the eval_2 variables from a different DTO

        :param saved_log_dto: the DTO to copy from
        :return: None
        """
        pass

    @abstractmethod
    def get_avg_attacker_dto(self, attacker_agent_config: AgentConfig, env: BaseCSLEEnv,
                             env_2: BaseCSLEEnv, eval: bool) -> BaseAttackerTrainAgentLogDTOAvg:
        """
        Averages the attacker metrics of the DTO and returns a new DTO containing the averages

        :param attacker_agent_config: the training configuration
        :param env: the training environment
        :param env_2: the evaluation environment
        :param eval: whether this is an evaluation round or not (Boolean)
        :return: the DTO with the average metrics
        """
        pass

    @abstractmethod
    def get_avg_defender_dto(self, defender_agent_config: AgentConfig, env: BaseCSLEEnv,
                             env_2: BaseCSLEEnv, eval: bool,
                             train_mode: TrainMode) -> BaseDefenderTrainAgentLogDTOAvg:
        """
        Averages the defender metrics of the DTO and returns a new DTO containing the averages

        :param defender_agent_config: the training configuration
        :param env: the training environment
        :param env_2: the evaluation environment
        :param eval: whether this is an evaluation round or not (Boolean)
        :return: the DTO with the average metrics
        """
        pass