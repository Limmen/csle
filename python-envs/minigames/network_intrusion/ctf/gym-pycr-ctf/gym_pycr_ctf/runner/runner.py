"""
Generic runner for running experiments with pycr environments
"""
from typing import Tuple
import gym
import time
from copy import deepcopy
from gym_pycr_ctf.dao.experiment.client_config import ClientConfig
from gym_pycr_ctf.dao.agent.agent_type import AgentType
from gym_pycr_ctf.dao.experiment.experiment_result import ExperimentResult
from gym_pycr_ctf.agents.policy_gradient.reinforce.reinforce_agent import ReinforceAgent
#from gym_pycr_ctf.envs.pycr_ctf_env import PyCRCTFEnv
from gym_pycr_ctf.agents.train_agent import TrainAgent
from gym_pycr_ctf.agents.policy_gradient.ppo_baseline.ppo_baseline_agent import PPOBaselineAgent
from gym_pycr_ctf.agents.bots.ppo_attacker_bot_agent import PPOAttackerBotAgent
from gym_pycr_ctf.util.experiments_util.simulator import Simulator
from gym_pycr_ctf.dao.experiment.runner_mode import RunnerMode
from gym_pycr_ctf.agents.dqn.dqn_baseline_agent import DQNBaselineAgent
from gym_pycr_ctf.agents.policy_gradient.a2c_baseline.a2c_baseline_agent import A2CBaselineAgent
from gym_pycr_ctf.agents.td3.td3_baseline_agent import TD3BaselineAgent
from gym_pycr_ctf.agents.ddpg.ddpg_baseline_agent import DDPGBaselineAgent
from gym_pycr_ctf.agents.manual.manual_attacker_agent import ManualAttackerAgent
from gym_pycr_ctf.agents.openai_baselines.common.env_util import make_vec_env
from gym_pycr_ctf.agents.openai_baselines.common.vec_env.dummy_vec_env import DummyVecEnv
from gym_pycr_ctf.agents.openai_baselines.common.vec_env.subproc_vec_env import SubprocVecEnv
from gym_pycr_ctf.envs_model.logic.common.domain_randomizer import DomainRandomizer
from gym_pycr_ctf.dao.agent.train_mode import TrainMode

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
        if config.mode == RunnerMode.TRAIN_ATTACKER.value or config.mode == RunnerMode.TRAIN_DEFENDER.value:
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
        env = None
        eval_env = None
        if config.multi_env:
            emulation_config_temps = None
            if config.emulation_configs is not None:
                emulation_config_temps = deepcopy(config.emulation_configs)
                for cf in emulation_config_temps:
                    cf.warmup = False
                    cf.skip_exploration = True
        else:
            emulation_config_temp = None
            if config.emulation_config is not None:
                emulation_config_temp = deepcopy(config.emulation_config)
                emulation_config_temp.warmup = False
                emulation_config_temp.skip_exploration = True
        if config.eval_multi_env:
            eval_emulation_config_temps = None
            if config.eval_env_emulation_configs is not None:
                eval_emulation_config_temps = deepcopy(config.eval_env_emulation_configs)
                for cf in eval_emulation_config_temps:
                    cf.warmup = False
                    cf.skip_exploration = True

        if config.multi_env:
            env, base_envs = Runner.multi_env_creation(config=config, emulation_config_temps=emulation_config_temps)
        elif config.randomized_env:
            env, base_env = Runner.randomized_env_creation(config=config, emulation_config_temp=emulation_config_temp)
        elif config.train_multi_sim:
            env, base_envs = Runner.multisim_env_creation(config=config)
        else:
            env, base_env = Runner.regular_env_creation(config=config, emulation_config_temp=emulation_config_temp)
        if config.eval_env is not None and config.eval_env:
            if config.eval_randomized_env:
                eval_env = gym.make(config.eval_env_name, env_config=config.env_config, emulation_config=config.eval_emulation_config,
                                    checkpoint_dir=config.env_checkpoint_dir,
                                    containers_config=config.eval_env_containers_config,
                                    flags_config=config.eval_env_flags_config, num_nodes = config.eval_env_num_nodes)
            elif config.eval_multi_env:
                eval_env, eval_base_envs = Runner.eval_multi_env_creation(config=config, emulation_config_temps=eval_emulation_config_temps)
            elif config.eval_multi_sim:
                eval_env, eval_base_envs = Runner.eval_multisim_env_creation(config=config)
            else:
                eval_env = gym.make(config.eval_env_name, env_config = config.env_config,
                                    emulation_config = config.eval_emulation_config,
                                    checkpoint_dir = config.env_checkpoint_dir)
            if config.eval_multi_env:
                if config.attacker_agent_config is not None:
                    config.attacker_agent_config.eval_env_configs = list(map(lambda x: x.env_config, eval_base_envs))
                if config.defender_agent_config is not None:
                    config.defender_agent_config.eval_env_configs = list(map(lambda x: x.env_config, eval_base_envs))
            elif config.train_multi_sim:
                if config.attacker_agent_config is not None:
                    config.attacker_agent_config.eval_env_configs = list(map(lambda x: x.env_config, eval_base_envs))
                if config.defender_agent_config is not None:
                    config.defender_agent_config.eval_env_configs = list(map(lambda x: x.env_config, eval_base_envs))
            else:
                if config.attacker_agent_config is not None:
                    config.attacker_agent_config.eval_env_config = eval_env.env_config
                if config.defender_agent_config is not None:
                    config.defender_agent_config.eval_env_config = eval_env.env_config

        if config.train_mode == TrainMode.TRAIN_ATTACKER or config.train_mode == TrainMode.SELF_PLAY:
            cfg = config.attacker_agent_config
        else:
            cfg = config.defender_agent_config
        if cfg.domain_randomization and config.sub_proc_env:
            if isinstance(env, DummyVecEnv):
                pass
            elif isinstance(env, SubprocVecEnv):
                randomization_space = DomainRandomizer.generate_randomization_space(
                    env.network_confs, max_num_nodes = cfg.dr_max_num_nodes,
                min_num_nodes = cfg.dr_min_num_nodes, max_num_flags=cfg.dr_max_num_flags,
                min_num_flags=cfg.dr_min_num_flags, min_num_users=cfg.dr_min_num_users,
                max_num_users=cfg.dr_max_num_users, use_base_randomization=cfg.dr_use_base)
                print("Randomization space created, base:{}".format(cfg.dr_use_base))
                env.set_randomization_space(randomization_space)
                print("Randomization space sent to all envs")
                if eval_env is not None:
                    eval_env.set_randomization_space(randomization_space)
                    eval_env.set_domain_randomization(False)
            else:
                # No aggregation to do since there is just a single env
                pass

        agent: TrainAgent = None
        if config.multi_env:
            if config.attacker_agent_config is not None:
                config.attacker_agent_config.env_configs = list(map(lambda x: x.env_config, base_envs))
            if config.defender_agent_config is not None:
                config.defender_agent_config.env_configs = list(map(lambda x: x.env_config, base_envs))
        elif config.train_multi_sim:
            if config.attacker_agent_config is not None:
                config.attacker_agent_config.env_configs = list(map(lambda x: x.env_config, base_envs))
            if config.defender_agent_config is not None:
                config.defender_agent_config.env_configs = list(map(lambda x: x.env_config, base_envs))
        else:
            if config.attacker_agent_config is not None:
                config.attacker_agent_config.env_config = base_env.env_config
            if config.defender_agent_config is not None:
                config.defender_agent_config.env_config = base_env.env_config

        if config.agent_type == AgentType.REINFORCE.value:
            agent = ReinforceAgent(env,
                                   attacker_agent_config=config.attacker_agent_config,
                                   defender_agent_config=config.defender_agent_config,
                                   train_mode=TrainMode(config.train_mode))
        elif config.agent_type == AgentType.PPO_BASELINE.value:
            agent = PPOBaselineAgent(env,
                                     attacker_agent_config=config.attacker_agent_config,
                                     defender_agent_config=config.defender_agent_config,
                                     eval_env=eval_env,
                                     train_mode=TrainMode(config.train_mode))
        elif config.agent_type == AgentType.DQN_BASELINE.value:
            agent = DQNBaselineAgent(env,
                                     attacker_agent_config=config.attacker_agent_config,
                                     defender_agent_config=config.defender_agent_config,
                                     eval_env=eval_env, train_mode=TrainMode(config.train_mode))
        elif config.agent_type == AgentType.A2C_BASELINE.value:
            agent = A2CBaselineAgent(env,
                                     attacker_agent_config=config.attacker_agent_config,
                                     defender_agent_config=config.defender_agent_config,
                                     eval_env=eval_env, train_mode=TrainMode(config.train_mode))
        elif config.agent_type == AgentType.TD3_BASELINE.value:
            agent = TD3BaselineAgent(env,
                                     attacker_agent_config=config.attacker_agent_config,
                                     defender_agent_config=config.defender_agent_config,
                                     eval_env=eval_env, train_mode=TrainMode(config.train_mode))
        elif config.agent_type == AgentType.DDPG_BASELINE.value:
            agent = DDPGBaselineAgent(env,
                                      attacker_agent_config=config.attacker_agent_config,
                                      defender_agent_config=config.defender_agent_config,
                                      eval_env=eval_env, train_mode=TrainMode(config.train_mode))
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
        env = None
        env = gym.make(config.env_name, env_config=config.env_config, emulation_config=config.emulation_config,
                       checkpoint_dir=config.env_checkpoint_dir)

        if config.simulation_config.domain_randomization:
            randomization_space = DomainRandomizer.generate_randomization_space(
                [], max_num_nodes=config.simulation_config.dr_max_num_nodes,
                min_num_nodes=config.simulation_config.dr_min_num_nodes,
                max_num_flags=config.simulation_config.dr_max_num_flags,
                min_num_flags=config.simulation_config.dr_min_num_flags,
                min_num_users=config.simulation_config.dr_min_num_users,
                max_num_users=config.simulation_config.dr_max_num_users,
                use_base_randomization=config.simulation_config.dr_use_base)
            env.randomization_space = randomization_space
            env.env_config.domain_randomization = True

        attacker: PPOAttackerBotAgent = None
        if config.agent_type == AgentType.PPO_BASELINE.value:
            if config.attacker_agent_config is None or config.attacker_agent_config.load_path is None:
                raise ValueError("To run a simulation with a PPO agent, the path to the saved "
                                 "model must be specified")
            attacker = PPOAttackerBotAgent(pg_config=config.attacker_agent_config, env_config=env.env_config,
                                           model_path=config.attacker_agent_config.load_path, env=env)
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
        env = None
        env = gym.make(config.env_name, env_config=config.env_config, emulation_config=config.emulation_config,
                       checkpoint_dir=config.env_checkpoint_dir)
        if config.simulation_config.domain_randomization:
            randomization_space = DomainRandomizer.generate_randomization_space(
                [], max_num_nodes=config.simulation_config.dr_max_num_nodes,
                min_num_nodes=config.simulation_config.dr_min_num_nodes,
                max_num_flags=config.simulation_config.dr_max_num_flags,
                min_num_flags=config.simulation_config.dr_min_num_flags,
                min_num_users=config.simulation_config.dr_min_num_users,
                max_num_users=config.simulation_config.dr_max_num_users,
                use_base_randomization=config.simulation_config.dr_use_base)
            env.randomization_space = randomization_space
            env.env_config.domain_randomization = True
            env.randomize()
        ManualAttackerAgent(env_config=env.env_config, env=env)
        return env

    @staticmethod
    def multi_env_creation(config: ClientConfig, emulation_config_temps):
        base_envs = [gym.make(config.env_name, env_config=config.env_config, emulation_config=emulation_config_temps[i],
                              checkpoint_dir=config.env_checkpoint_dir, containers_configs=config.containers_configs,
                              flags_configs=config.flags_configs, idx=i,
                              num_nodes=config.attacker_agent_config.num_nodes) for i in range(len(config.containers_configs))]
        env_kwargs = [{"env_config": config.env_config, "emulation_config": config.emulation_configs[i],
                      "checkpoint_dir": config.env_checkpoint_dir, "containers_config": config.containers_configs,
                      "flags_config": config.flags_configs, "idx": i,
                       "num_nodes": config.attacker_agent_config.num_nodes} for i in range(len(config.containers_configs))]
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
    def randomized_env_creation(config: ClientConfig, emulation_config_temp):
        base_env = gym.make(config.env_name, env_config=config.env_config, emulation_config=emulation_config_temp,
                            checkpoint_dir=config.env_checkpoint_dir, containers_config=config.containers_config,
                            flags_config=config.flags_config, num_nodes = config.attacker_agent_config.num_nodes)
        env_kwargs = {"env_config": config.env_config, "emulation_config": config.emulation_config,
                      "checkpoint_dir": config.env_checkpoint_dir, "containers_config": config.containers_config,
                      "flags_config": config.flags_config, "num_nodes": config.attacker_agent_config.num_nodes}
        vec_env_kwargs = {"env_config": config.env_config}
        vec_env_cls = DummyVecEnv
        if config.sub_proc_env:
            vec_env_cls = SubprocVecEnv
        if config.dummy_vec_env or config.sub_proc_env:
            env = make_vec_env(config.env_name, n_envs=config.n_envs, seed=config.random_seed,
                               env_kwargs=env_kwargs, vec_env_kwargs=vec_env_kwargs, vec_env_cls=vec_env_cls)
        else:
            env = gym.make(config.env_name, env_config=config.env_config, emulation_config=config.emulation_config,
                           checkpoint_dir=config.env_checkpoint_dir, containers_config=config.containers_config,
                           flags_config=config.flags_config, num_nodes=config.attacker_agent_config.num_nodes)
        return env, base_env


    @staticmethod
    def regular_env_creation(config: ClientConfig, emulation_config_temp):
        base_env = gym.make(config.env_name, env_config=config.env_config, emulation_config=emulation_config_temp,
                            checkpoint_dir=config.env_checkpoint_dir)
        env_kwargs = {"env_config": config.env_config, "emulation_config": config.emulation_config,
                      "checkpoint_dir": config.env_checkpoint_dir}
        vec_env_kwargs = {"env_config": config.env_config}
        vec_env_cls = DummyVecEnv
        if config.sub_proc_env:
            vec_env_cls = SubprocVecEnv
        if config.dummy_vec_env or config.sub_proc_env:
            env = make_vec_env(config.env_name, n_envs=config.n_envs, seed=config.random_seed,
                               env_kwargs=env_kwargs, vec_env_kwargs=vec_env_kwargs, vec_env_cls=vec_env_cls)
        else:
            env = gym.make(config.env_name, env_config=config.env_config, emulation_config=config.emulation_config,
                           checkpoint_dir=config.env_checkpoint_dir)
            if config.train_mode == TrainMode.TRAIN_ATTACKER or config.train_mode == TrainMode.SELF_PLAY:
                cfg = config.attacker_agent_config
            else:
                cfg = config.defender_agent_config
            if cfg.domain_randomization:
                randomization_space = DomainRandomizer.generate_randomization_space(
                    [], max_num_nodes=config.attacker_agent_config.dr_max_num_nodes,
                    min_num_nodes=cfg.dr_min_num_nodes,
                    max_num_flags=cfg.dr_max_num_flags,
                    min_num_flags=cfg.dr_min_num_flags,
                    min_num_users=cfg.dr_min_num_users,
                    max_num_users=cfg.dr_max_num_users,
                    use_base_randomization=cfg.dr_use_base)
                env.randomization_space = randomization_space
                env.env_config.domain_randomization = True
                base_env.randomization_space = randomization_space
                base_env.env_config.domain_randomization = True
        return env, base_env

    @staticmethod
    def eval_multi_env_creation(config: ClientConfig, emulation_config_temps):
        base_envs = [gym.make(config.eval_env_name, env_config=config.env_config, emulation_config=emulation_config_temps[i],
                              checkpoint_dir=config.env_checkpoint_dir, containers_configs=config.eval_env_containers_configs,
                              flags_configs=config.eval_env_flags_configs, idx=i) for i in range(len(config.eval_env_containers_configs))]

        env_kwargs = [{"env_config": config.env_config, "emulation_config": config.eval_env_emulation_configs[i],
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

    @staticmethod
    def multisim_env_creation(config: ClientConfig):
        base_envs = [gym.make(config.eval_env_name, env_config=config.env_config, emulation_config=None,
                              idx=i, checkpoint_dir=config.env_checkpoint_dir,
                              dr_max_num_nodes=config.attacker_agent_config.dr_max_num_nodes,
                              dr_min_num_nodes=config.attacker_agent_config.dr_min_num_nodes,
                              dr_max_num_users=config.attacker_agent_config.dr_max_num_users,
                              dr_min_num_users=config.attacker_agent_config.dr_min_num_users,
                              dr_max_num_flags=config.attacker_agent_config.dr_max_num_flags,
                              dr_min_num_flags=config.attacker_agent_config.dr_min_num_flags
                              ) for i in range(config.num_sims)]
        env_kwargs = [{"env_config": config.env_config, "emulation_config": None,
                       "checkpoint_dir": config.env_checkpoint_dir, "idx": i,
                       "dr_max_num_nodes": config.attacker_agent_config.dr_max_num_nodes,
                       "dr_min_num_nodes": config.attacker_agent_config.dr_min_num_nodes,
                       "dr_max_num_flags": config.attacker_agent_config.dr_max_num_flags,
                       "dr_min_num_flags": config.attacker_agent_config.dr_min_num_flags,
                       "dr_max_num_users": config.attacker_agent_config.dr_max_num_users,
                       "dr_min_num_users": config.attacker_agent_config.dr_min_num_users
                       } for i in range(config.num_sims)]
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
    def eval_multisim_env_creation(config: ClientConfig):
        base_envs = [gym.make(config.eval_env_name, env_config=config.env_config, emulation_config=None,
                              idx=i, checkpoint_dir=config.env_checkpoint_dir,
                              dr_max_num_nodes = config.attacker_agent_config.dr_max_num_nodes,
                              dr_min_num_nodes = config.attacker_agent_config.dr_min_num_nodes,
                              dr_max_num_users = config.attacker_agent_config.dr_max_num_users,
                              dr_min_num_users = config.attacker_agent_config.dr_min_num_users,
                              dr_max_num_flags = config.attacker_agent_config.dr_max_num_flags,
                              dr_min_num_flags = config.attacker_agent_config.dr_min_num_flags
                              ) for i in range(config.num_sims_eval)]
        env_kwargs = [{"env_config": config.env_config, "emulation_config": None,
                       "checkpoint_dir": config.env_checkpoint_dir, "idx": i,
                       "dr_max_num_nodes": config.attacker_agent_config.dr_max_num_nodes,
                       "dr_min_num_nodes": config.attacker_agent_config.dr_min_num_nodes,
                       "dr_max_num_flags": config.attacker_agent_config.dr_max_num_flags,
                       "dr_min_num_flags": config.attacker_agent_config.dr_min_num_flags,
                       "dr_max_num_users": config.attacker_agent_config.dr_max_num_users,
                       "dr_min_num_users": config.attacker_agent_config.dr_min_num_users
                       } for i in range(config.num_sims_eval)]
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