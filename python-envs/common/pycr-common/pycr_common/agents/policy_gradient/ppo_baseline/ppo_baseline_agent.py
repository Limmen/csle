"""
An agent for the pycr-ctf env that uses the PPO Policy Gradient algorithm from OpenAI stable baselines
"""
import time
import math

from pycr_common.rendering.video.pycr_ctf_monitor import PyCrCTFMonitor
from pycr_common.dao.experiment.base_experiment_result import BaseExperimentResult
from pycr_common.agents.train_agent import TrainAgent
from pycr_common.agents.config.agent_config import AgentConfig
from pycr_common.agents.policy_gradient.ppo_baseline.impl.ppo.ppo import PPO
import pycr_common.agents.policy_gradient.ppo_baseline.impl.ppo.policies # to register policies
from pycr_common.agents.openai_baselines.common.vec_env.dummy_vec_env import DummyVecEnv
from pycr_common.agents.openai_baselines.common.vec_env.subproc_vec_env import SubprocVecEnv
from pycr_common.dao.agent.train_mode import TrainMode
from pycr_common.agents.util.agent_util import AgentUtil
from pycr_common.dao.agent.base_train_agent_log_dto import BaseTrainAgentLogDTO
from pycr_common.dao.agent.base_rollout_data_dto import BaseRolloutDataDTO
from pycr_common.envs_model.util.base_eval_util import BaseEvalUtil


class PPOBaselineAgent(TrainAgent):
    """
    An agent for the pycr-ctf env that uses the PPO Policy Gradient algorithm from OpenAI stable baselines
    """

    def __init__(self, env, attacker_agent_config: AgentConfig,
                 defender_agent_config: AgentConfig,
                 train_agent_dto: BaseTrainAgentLogDTO, rollout_data_dto: BaseRolloutDataDTO,
                 eval_util: BaseEvalUtil, experiment_result: BaseExperimentResult,
                 eval_env, train_mode: TrainMode = TrainMode.TRAIN_ATTACKER):
        """
        Initialize environment and hyperparameters

        :param the training env
        :param attacker_config: the attacker configuration
        :param defender_config: the defender configuration
        :param train_agent_dto: the DTO for logging training data
        :param rollout_data_dto: the DTO for rollout data
        :param eval_util: the util class for running custom evaluations
        :param experiment_result: the DTO for saving experiment results
        :param eval_env: the evaluation env
        """
        super(PPOBaselineAgent, self).__init__(env, attacker_agent_config,
                                               defender_agent_config,
                                               train_agent_dto, rollout_data_dto,
                                               eval_util,
                                               eval_env, train_mode)

    def train(self) -> BaseExperimentResult:
        """
        Starts the training loop and returns the result when complete

        :return: the training result
        """

        # Setup Attacker
        if self.attacker_config is not None:
            # Custom MLP policy for attacker
            attacker_net_arch = []
            attacker_pi_arch = []
            attacker_vf_arch = []
            for l in range(self.attacker_config.shared_layers):
                attacker_net_arch.append(self.attacker_config.shared_hidden_dim)
            for l in range(self.attacker_config.pi_hidden_layers):
                attacker_pi_arch.append(self.attacker_config.pi_hidden_dim)
            for l in range(self.attacker_config.vf_hidden_layers):
                attacker_vf_arch.append(self.attacker_config.vf_hidden_dim)

            net_dict_attacker = {"pi": attacker_pi_arch, "vf": attacker_vf_arch}
            attacker_net_arch.append(net_dict_attacker)

            policy_kwargs_attacker = dict(activation_fn=AgentUtil.get_hidden_activation(config=self.attacker_config),
                                          net_arch=attacker_net_arch)
            device_attacker = "cpu" if not self.attacker_config.gpu else "cuda:" + str(self.attacker_config.gpu_id)
            policy_attacker = "MlpPolicy"

            if self.attacker_config.lr_progress_decay:
                temp = self.attacker_config.alpha
                lr_decay_func = lambda x: temp * math.pow(x, self.attacker_config.lr_progress_power_decay)
                self.attacker_config.alpha = lr_decay_func

        # Setup Defender
        if self.defender_config is not None:
            # Custom MLP policy for attacker
            defender_net_arch = []
            defender_pi_arch = []
            defender_vf_arch = []
            for l in range(self.defender_config.shared_layers):
                defender_net_arch.append(self.defender_config.shared_hidden_dim)
            for l in range(self.defender_config.pi_hidden_layers):
                defender_pi_arch.append(self.defender_config.pi_hidden_dim)
            for l in range(self.defender_config.vf_hidden_layers):
                defender_vf_arch.append(self.defender_config.vf_hidden_dim)

            net_dict_defender = {"pi": defender_pi_arch, "vf": defender_vf_arch}
            defender_net_arch.append(net_dict_defender)

            policy_kwargs_defender = dict(activation_fn=AgentUtil.get_hidden_activation(config=self.defender_config),
                                          net_arch=defender_net_arch)
            device_defender = "cpu" if not self.defender_config.gpu else "cuda:" + str(self.defender_config.gpu_id)
            policy_defender = "MlpPolicy"

        # Create model
        model = PPO(policy_attacker, policy_defender,
                    self.env,
                    batch_size=self.attacker_config.mini_batch_size,
                    attacker_learning_rate=self.attacker_config.alpha,
                    defender_learning_rate=self.defender_config.alpha,
                    n_steps=self.attacker_config.batch_size,
                    n_epochs=self.attacker_config.optimization_iterations,
                    attacker_gamma=self.attacker_config.gamma,
                    defender_gamma=self.defender_config.gamma,
                    attacker_gae_lambda=self.attacker_config.gae_lambda,
                    defender_gae_lambda=self.defender_config.gae_lambda,
                    attacker_clip_range=self.attacker_config.eps_clip,
                    defender_clip_range=self.defender_config.eps_clip,
                    attacker_max_grad_norm=self.attacker_config.max_gradient_norm,
                    defender_max_grad_norm=self.defender_config.max_gradient_norm,
                    verbose=1,
                    seed=self.attacker_config.random_seed,
                    attacker_policy_kwargs=policy_kwargs_attacker,
                    defender_policy_kwargs=policy_kwargs_defender,
                    device=device_attacker,
                    attacker_agent_config=self.attacker_config,
                    defender_agent_config=self.defender_config,
                    attacker_vf_coef=self.attacker_config.vf_coef,
                    defender_vf_coef=self.defender_config.vf_coef,
                    attacker_ent_coef=self.attacker_config.ent_coef,
                    defender_ent_coef=self.defender_config.ent_coef,
                    env_2=self.eval_env,
                    train_mode = self.train_mode,
                    train_agent_log_dto=self.train_agent_dto,
                    rollout_data_dto=self.rollout_data_dto,
                    eval_util=self.eval_util
                    )

        if self.attacker_config.load_path is not None:
            PPO.load(self.attacker_config.load_path, policy_attacker, agent_config=self.attacker_config)

        elif self.defender_config.load_path is not None:
            PPO.load(self.defender_config.load_path, policy_defender, agent_config=self.defender_config)

        # Eval config
        time_str = str(time.time())

        if self.train_mode == TrainMode.TRAIN_ATTACKER or self.train_mode == TrainMode.SELF_PLAY:
            video_dir = self.attacker_config.video_dir
            video_frequency = self.attacker_config.video_frequency
            video_fps = self.attacker_config.video_fps
            total_timesteps = self.attacker_config.num_episodes
            train_log_frequency = self.attacker_config.train_log_frequency
            eval_frequency = self.attacker_config.eval_frequency
            eval_episodes = self.attacker_config.eval_episodes
            save_dir = self.attacker_config.save_dir
        else:
            video_dir = self.defender_config.video_dir
            video_frequency = self.defender_config.video_frequency
            video_fps = self.defender_config.video_fps
            total_timesteps = self.defender_config.num_episodes
            train_log_frequency = self.defender_config.train_log_frequency
            eval_frequency = self.defender_config.eval_frequency
            eval_episodes = self.defender_config.eval_episodes
            save_dir = self.defender_config.save_dir

        if video_dir is None:
            raise AssertionError("Video is set to True but no video_dir is provided, please specify "
                                 "the video_dir argument")
        if isinstance(self.env, DummyVecEnv):
            train_eval_env_i = self.env
            train_eval_env = train_eval_env_i
        elif isinstance(self.env, SubprocVecEnv):
            train_eval_env_i = self.env
            train_eval_env = train_eval_env_i
        else:
            train_eval_env_i = self.env
            if train_eval_env_i is not None:
                train_eval_env = PyCrCTFMonitor(train_eval_env_i, video_dir + "/" + time_str, force=True,
                                          video_frequency=video_frequency, openai_baseline=True)
                train_eval_env.metadata["video.frames_per_second"] = video_fps
            else:
                train_eval_env = None

        eval_env = None
        if isinstance(self.eval_env, DummyVecEnv) or isinstance(self.eval_env, SubprocVecEnv):
            eval_env = self.eval_env
        else:
            if self.eval_env is not None:
                eval_env = PyCrCTFMonitor(self.eval_env, video_dir + "/" + time_str, force=True,
                                                    video_frequency=video_frequency, openai_baseline=True)
                eval_env.metadata["video.frames_per_second"] = video_fps

        model.learn(total_timesteps=total_timesteps,
                    log_interval=train_log_frequency,
                    eval_freq=eval_frequency,
                    n_eval_episodes=eval_episodes,
                    eval_env=train_eval_env,
                    eval_env_2=eval_env
                    )

        if self.attacker_config is not None:
            self.attacker_config.logger.info("Training Complete")
        if self.defender_config is not None:
            self.defender_config.logger.info("Training Complete")

        # Save networks
        try:
            model.save_model()
        except Exception as e:
            print("There was en error saving the model:{}".format(str(e)))

        # Save other game data
        if save_dir is not None:
            time_str = str(time.time())
            model.train_result.to_csv(save_dir + "/" + time_str + "_train_results_checkpoint.csv")
            model.eval_result.to_csv(save_dir + "/" + time_str + "_eval_results_checkpoint.csv")

        self.train_result = model.train_result
        self.eval_result = model.eval_result
        return model.train_result


    def get_action(self, s, eval=False, attacker=True) -> int:
        raise NotImplemented("not implemented")

    def eval(self, log=True) -> BaseExperimentResult:
        raise NotImplemented("not implemented")