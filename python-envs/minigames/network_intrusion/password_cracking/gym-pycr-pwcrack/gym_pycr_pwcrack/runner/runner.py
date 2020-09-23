"""
Generic runner for running experiments with pycr environments
"""
from typing import Union
import gym
from gym_pycr_pwcrack.dao.experiment.client_config import ClientConfig
from gym_pycr_pwcrack.dao.agent.agent_type import AgentType
from gym_pycr_pwcrack.dao.experiment.experiment_result import ExperimentResult
from gym_pycr_pwcrack.agents.policy_gradient.reinforce_agent import ReinforceAgent
from gym_pycr_pwcrack.envs.pycr_pwcrack_env import PyCRPwCrackEnv
from gym_pycr_pwcrack.agents.train_agent import TrainAgent

class Runner:
    """
    Class with utility methods for running structured experiments with cgc environments
    """

    @staticmethod
    def run(config: ClientConfig):
        """
        Run entrypoint

        :param config: configuration for the run
        :return: the result
        """
        return Runner.train(config)

    @staticmethod
    def train(config: ClientConfig) -> Union[ExperimentResult, ExperimentResult]:
        """
        Trains an agent agent in the environment

        :param config: Training configuration
        :return: trainresult, evalresult
        """
        env: PyCRPwCrackEnv = None
        env = gym.make(config.env_name, env_config = config.env_config)
        agent: TrainAgent = None
        if config.agent_type == AgentType.REINFORCE.value:
            agent = ReinforceAgent(env, config.pg_agent_config)
        else:
            raise AssertionError("Train agent type not recognized: {}".format(config.agent_type))
        agent.train()
        train_result = agent.train_result
        eval_result = agent.eval_result
        return train_result, eval_result