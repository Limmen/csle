"""
Generic runner for running experiments with pycr environments
"""
from typing import Tuple
import gym
import time
from gym_pycr_pwcrack.dao.experiment.client_config import ClientConfig
from gym_pycr_pwcrack.dao.agent.agent_type import AgentType
from gym_pycr_pwcrack.dao.experiment.experiment_result import ExperimentResult
from gym_pycr_pwcrack.agents.policy_gradient.reinforce.reinforce_agent import ReinforceAgent
from gym_pycr_pwcrack.envs.pycr_pwcrack_env import PyCRPwCrackEnv
from gym_pycr_pwcrack.agents.train_agent import TrainAgent
from gym_pycr_pwcrack.agents.policy_gradient.ppo_baseline.ppo_baseline_agent import PPOBaselineAgent
from gym_pycr_pwcrack.agents.bots.ppo_attacker_bot_agent import PPOAttackerBotAgent
from gym_pycr_pwcrack.util.experiments_util.simulator import Simulator
from gym_pycr_pwcrack.dao.experiment.runner_mode import RunnerMode
from gym_pycr_pwcrack.agents.dqn.dqn_baseline_agent import DQNBaselineAgent
from gym_pycr_pwcrack.agents.policy_gradient.a2c_baseline.a2c_baseline_agent import A2CBaselineAgent
from gym_pycr_pwcrack.agents.td3.td3_baseline_agent import TD3BaselineAgent
from gym_pycr_pwcrack.agents.ddpg.ddpg_baseline_agent import DDPGBaselineAgent
from gym_pycr_pwcrack.agents.manual.manual_attacker_agent import ManualAttackerAgent

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
        if config.mode == RunnerMode.TRAIN_ATTACKER.value:
            return Runner.train(config)
        elif config.mode == RunnerMode.SIMULATE.value:
            return Runner.simulate(config)
        elif config.mode == RunnerMode.MANUAL_ATTACKER.value:
            return Runner.manual_play(config)
        else:
            raise AssertionError("Runner mode not recognized: {}".format(config.mode))
        return Runner.train(config)

    @staticmethod
    def train(config: ClientConfig) -> Tuple[ExperimentResult, ExperimentResult]:
        """
        Trains an agent agent in the environment

        :param config: Training configuration
        :return: trainresult, evalresult
        """
        env: PyCRPwCrackEnv = None
        eval_env: PyCRPwCrackEnv = None
        env = gym.make(config.env_name, env_config = config.env_config, cluster_config = config.cluster_config,
                       checkpoint_dir = config.env_checkpoint_dir)
        if config.eval_env is not None:
            eval_env = gym.make(config.eval_env_name, env_config = config.env_config,
                                cluster_config = config.eval_cluster_config,
                                checkpoint_dir = config.env_checkpoint_dir)
        agent: TrainAgent = None
        if config.agent_type == AgentType.REINFORCE.value:
            agent = ReinforceAgent(env, config.agent_config)
        elif config.agent_type == AgentType.PPO_BASELINE.value:
            agent = PPOBaselineAgent(env, config.agent_config, eval_env=eval_env)
        elif config.agent_type == AgentType.DQN_BASELINE.value:
            agent = DQNBaselineAgent(env, config.agent_config)
        elif config.agent_type == AgentType.A2C_BASELINE.value:
            agent = A2CBaselineAgent(env, config.agent_config)
        elif config.agent_type == AgentType.TD3_BASELINE.value:
            agent = TD3BaselineAgent(env, config.agent_config)
        elif config.agent_type == AgentType.DDPG_BASELINE.value:
            agent = DDPGBaselineAgent(env, config.agent_config)
        else:
            raise AssertionError("Train agent type not recognized: {}".format(config.agent_type))
        agent.train()
        train_result = agent.train_result
        eval_result = agent.eval_result
        env.cleanup()
        env.close()
        if eval_env is not None:
            eval_env.cleanup()
            eval_env.close()
        time.sleep(2)
        return train_result, eval_result

    @staticmethod
    def simulate(config: ClientConfig) -> ExperimentResult:
        """
        Runs a simulation with two pre-defined policies against each other

        :param config: the simulation config
        :return: experiment result
        """
        env: PyCRPwCrackEnv = None
        env = gym.make(config.env_name, env_config=config.env_config, cluster_config=config.cluster_config,
                       checkpoint_dir=config.env_checkpoint_dir)
        attacker: PPOAttackerBotAgent = None
        if config.agent_type == AgentType.PPO_BASELINE.value:
            if config.agent_config is None or config.agent_config.load_path is None:
                raise ValueError("To run a simulation with a PPO agent, the path to the saved "
                                 "model must be specified")
            attacker = PPOAttackerBotAgent(pg_config=config.agent_config, env_config=env.env_config,
                                           model_path=config.agent_config.load_path, env=env)
        else:
            raise AssertionError("Agent type not recognized: {}".format(config.attacker_type))
        simulator = Simulator(env, config.simulation_config, attacker=attacker)
        return simulator.simulate()

    @staticmethod
    def manual_play(config: ClientConfig) -> ExperimentResult:
        """
        Starts the environment in manual mode where the user can specify actions using the keyboard

        :param config: the manual play config
        :return: experiment result
        """
        env: PyCRPwCrackEnv = None
        env = gym.make(config.env_name, env_config=config.env_config, cluster_config=config.cluster_config,
                       checkpoint_dir=config.env_checkpoint_dir)
        ManualAttackerAgent(env_config=env.env_config, env=env)
        return env