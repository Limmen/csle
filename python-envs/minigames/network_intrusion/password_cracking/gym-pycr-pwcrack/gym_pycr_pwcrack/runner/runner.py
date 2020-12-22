"""
Generic runner for running experiments with pycr environments
"""
from typing import Tuple
import gym
import time
from copy import deepcopy
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
from gym_pycr_pwcrack.agents.openai_baselines.common.env_util import make_vec_env
from gym_pycr_pwcrack.agents.openai_baselines.common.vec_env.dummy_vec_env import DummyVecEnv
from gym_pycr_pwcrack.agents.openai_baselines.common.vec_env.subproc_vec_env import SubprocVecEnv

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
        if config.multi_env:
            cluster_conf_temps = deepcopy(config.cluster_configs)
            for cf in cluster_conf_temps:
                cf.warmup = False
                cf.skip_exploration = True
        else:
            cluster_conf_temp = deepcopy(config.cluster_config)
            cluster_conf_temp.warmup = False
            cluster_conf_temp.skip_exploration = True
        if config.eval_multi_env:
            eval_cluster_conf_temps = deepcopy(config.eval_env_cluster_configs)
            for cf in eval_cluster_conf_temps:
                cf.warmup = False
                cf.skip_exploration = True

        if config.multi_env:
            env, base_envs = Runner.multi_env_creation(config=config, cluster_conf_temps=cluster_conf_temps)
        elif config.randomized_env:
            env, base_env = Runner.randomized_env_creation(config=config, cluster_conf_temp=cluster_conf_temp)
        else:
            env, base_env = Runner.randomized_env_creation(config=config, cluster_conf_temp=cluster_conf_temp)
        if config.eval_env is not None:
            if config.eval_randomized_env:
                eval_env = gym.make(config.eval_env_name, env_config=config.env_config, cluster_config=config.eval_cluster_config,
                                    checkpoint_dir=config.env_checkpoint_dir,
                                    containers_config=config.eval_env_containers_config,
                                    flags_config=config.eval_env_flags_config, num_nodes = config.eval_env_num_nodes)
            elif config.eval_multi_env:
                eval_env, eval_base_envs = Runner.eval_multi_env_creation(config=config, cluster_conf_temps=eval_cluster_conf_temps)
            else:
                eval_env = gym.make(config.eval_env_name, env_config = config.env_config,
                                    cluster_config = config.eval_cluster_config,
                                    checkpoint_dir = config.env_checkpoint_dir)
            if config.eval_multi_env:
                config.agent_config.eval_env_configs = list(map(lambda x: x.env_config, eval_base_envs))
            else:
                config.agent_config.eval_env_config = eval_env.env_config
        agent: TrainAgent = None
        if config.multi_env:
            config.agent_config.env_configs = list(map(lambda x: x.env_config, base_envs))
        else:
            config.agent_config.env_config = base_env.env_config

        if config.agent_type == AgentType.REINFORCE.value:
            agent = ReinforceAgent(env, config.agent_config)
        elif config.agent_type == AgentType.PPO_BASELINE.value:
            agent = PPOBaselineAgent(env, config.agent_config, eval_env=eval_env)
        elif config.agent_type == AgentType.DQN_BASELINE.value:
            agent = DQNBaselineAgent(env, config.agent_config, eval_env=eval_env)
        elif config.agent_type == AgentType.A2C_BASELINE.value:
            agent = A2CBaselineAgent(env, config.agent_config, eval_env=eval_env)
        elif config.agent_type == AgentType.TD3_BASELINE.value:
            agent = TD3BaselineAgent(env, config.agent_config, eval_env=eval_env)
        elif config.agent_type == AgentType.DDPG_BASELINE.value:
            agent = DDPGBaselineAgent(env, config.agent_config, eval_env=eval_env)
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

    @staticmethod
    def multi_env_creation(config: ClientConfig, cluster_conf_temps):
        base_envs = [gym.make(config.env_name, env_config=config.env_config, cluster_config=cluster_conf_temps[i],
                              checkpoint_dir=config.env_checkpoint_dir, containers_configs=config.containers_configs,
                              flags_configs=config.flags_configs, idx=i,
                              num_nodes=config.agent_config.num_nodes) for i in range(len(config.containers_configs))]
        env_kwargs = [{"env_config": config.env_config, "cluster_config": config.cluster_configs[i],
                      "checkpoint_dir": config.env_checkpoint_dir, "containers_config": config.containers_configs,
                      "flags_config": config.flags_configs, "idx": i,
                       "num_nodes": config.agent_config.num_nodes} for i in range(len(config.containers_configs))]
        vec_env_kwargs = {"env_config": config.env_config}
        vec_env_cls = DummyVecEnv
        if config.sub_proc_env:
            vec_env_cls = SubprocVecEnv
        if config.dummy_vec_env or config.sub_proc_env:
            env = make_vec_env(config.env_name, n_envs=config.n_envs, seed=config.random_seed,
                               env_kwargs=env_kwargs, vec_env_kwargs=vec_env_kwargs, vec_env_cls=vec_env_cls,
                               multi_env=True)
        else:
            raise ValueError("Have to use a vectorized env class to instantiate a multi-env config")
        return env, base_envs

    @staticmethod
    def randomized_env_creation(config: ClientConfig, cluster_conf_temp):
        base_env = gym.make(config.env_name, env_config=config.env_config, cluster_config=cluster_conf_temp,
                            checkpoint_dir=config.env_checkpoint_dir, containers_config=config.containers_config,
                            flags_config=config.flags_config, num_nodes = config.agent_config.num_nodes)
        env_kwargs = {"env_config": config.env_config, "cluster_config": config.cluster_config,
                      "checkpoint_dir": config.env_checkpoint_dir, "containers_config": config.containers_config,
                      "flags_config": config.flags_config, "num_nodes": config.agent_config.num_nodes}
        vec_env_kwargs = {"env_config": config.env_config}
        vec_env_cls = DummyVecEnv
        if config.sub_proc_env:
            vec_env_cls = SubprocVecEnv
        if config.dummy_vec_env or config.sub_proc_env:
            env = make_vec_env(config.env_name, n_envs=config.n_envs, seed=config.random_seed,
                               env_kwargs=env_kwargs, vec_env_kwargs=vec_env_kwargs, vec_env_cls=vec_env_cls)
        else:
            env = gym.make(config.env_name, env_config=config.env_config, cluster_config=config.cluster_config,
                           checkpoint_dir=config.env_checkpoint_dir, containers_config=config.containers_config,
                           flags_config=config.flags_config, num_nodes=config.agent_config.num_nodes)
        return env, base_env


    @staticmethod
    def regular_env_creation(config: ClientConfig, cluster_conf_temp):
        base_env = gym.make(config.env_name, env_config=config.env_config, cluster_config=cluster_conf_temp,
                            checkpoint_dir=config.env_checkpoint_dir)
        env_kwargs = {"env_config": config.env_config, "cluster_config": config.cluster_config,
                      "checkpoint_dir": config.env_checkpoint_dir}
        vec_env_kwargs = {"env_config": config.env_config}
        vec_env_cls = DummyVecEnv
        if config.sub_proc_env:
            vec_env_cls = SubprocVecEnv
        if config.dummy_vec_env or config.sub_proc_env:
            env = make_vec_env(config.env_name, n_envs=config.n_envs, seed=config.random_seed,
                               env_kwargs=env_kwargs, vec_env_kwargs=vec_env_kwargs, vec_env_cls=vec_env_cls)
        else:
            env = gym.make(config.env_name, env_config=config.env_config, cluster_config=config.cluster_config,
                           checkpoint_dir=config.env_checkpoint_dir)
        return env, base_env

    @staticmethod
    def eval_multi_env_creation(config: ClientConfig, cluster_conf_temps):
        base_envs = [gym.make(config.eval_env_name, env_config=config.env_config, cluster_config=cluster_conf_temps[i],
                              checkpoint_dir=config.env_checkpoint_dir, containers_configs=config.eval_env_containers_configs,
                              flags_configs=config.eval_env_flags_configs, idx=i) for i in range(len(config.eval_env_containers_configs))]

        env_kwargs = [{"env_config": config.env_config, "cluster_config": config.eval_env_cluster_configs[i],
                       "checkpoint_dir": config.env_checkpoint_dir, "containers_config": config.eval_env_containers_configs,
                       "flags_config": config.eval_env_flags_configs, "idx": i, "num_nodes": config.eval_env_num_nodes
                       } for i in range(len(config.eval_env_containers_configs))]
        vec_env_kwargs = {"env_config": config.env_config}
        vec_env_cls = DummyVecEnv
        if config.sub_proc_env:
            vec_env_cls = SubprocVecEnv
        if config.eval_dummy_vec_env or config.eval_sub_proc_env:
            env = make_vec_env(config.eval_env_name, n_envs=config.eval_n_envs, seed=config.random_seed,
                               env_kwargs=env_kwargs, vec_env_kwargs=vec_env_kwargs, vec_env_cls=vec_env_cls,
                               multi_env=True)
        else:
            raise ValueError("Have to use a vectorized env class to instantiate a multi-env config")
        return env, base_envs