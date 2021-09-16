"""
An agent for the pycr-ctf env that uses the TD3 algorithm from OpenAI stable baselines
"""
import time
import math

from gym_pycr_ctf.rendering.video.pycr_ctf_monitor import PyCrCTFMonitor
from gym_pycr_ctf.envs.pycr_ctf_env import PyCRCTFEnv
from gym_pycr_ctf.dao.experiment.experiment_result import ExperimentResult
from pycr_common.agents.train_agent import TrainAgent
from pycr_common.agents.config.agent_config import AgentConfig
from pycr_common.agents.td3.impl.td3 import TD3
from pycr_common.agents.util.agent_util import AgentUtil


class TD3BaselineAgent(TrainAgent):
    """
    An agent for the pycr-ctf env that uses the TD3 algorithm from OpenAI stable baselines
    """

    def __init__(self, env: PyCRCTFEnv, attacker_config: AgentConfig, eval_env: PyCRCTFEnv):
        """
        Initialize environment and hyperparameters

        :param attacker_config: the attacker configuration
        """
        super(TD3BaselineAgent, self).__init__(env, attacker_config, eval_env)

    def train(self) -> ExperimentResult:
        """
        Starts the training loop and returns the result when complete

        :return: the training result
        """

        # Custom MLP policy
        net_arch = []
        for l in range(self.attacker_config.shared_layers):
            net_arch.append(self.attacker_config.shared_hidden_dim)

        policy_kwargs = dict(activation_fn=AgentUtil.get_hidden_activation(config=self.attacker_config),
                             net_arch=net_arch)
        device = "cpu" if not self.attacker_config.gpu else "cuda:" + str(self.attacker_config.gpu_id)
        policy = "MlpPolicy"

        if self.attacker_config.lr_progress_decay:
            temp = self.attacker_config.alpha
            lr_decay_func = lambda x: temp*math.pow(x, self.attacker_config.lr_progress_power_decay)
            self.attacker_config.alpha = lr_decay_func

        model = TD3(
            policy, self.env, learning_rate=self.attacker_config.alpha,
            buffer_size=self.attacker_config.buffer_size,
            learning_starts=self.attacker_config.learning_starts,
            batch_size=self.attacker_config.batch_size,
            tau=self.attacker_config.tau,gamma=self.attacker_config.gamma,
            train_freq=self.attacker_config.train_freq,
            gradient_steps=self.attacker_config.gradient_steps,
            agent_attacker_config=self.attacker_config, device=device,
            policy_kwargs=policy_kwargs,
            policy_delay=self.attacker_config.policy_delay,
            target_policy_noise=self.attacker_config.target_policy_noise,
            target_noise_clip=self.attacker_config.target_noise_clip,
            n_episodes_rollout=-1,
            env_2=self.eval_env
        )

        if self.attacker_config.load_path is not None:
            TD3.load(self.attacker_config.load_path, policy, agent_config=self.attacker_config)


        # Eval config
        if self.attacker_config.video or self.attacker_config.gifs:
            time_str = str(time.time())
            if self.attacker_config.video_dir is None:
                raise AssertionError("Video is set to True but no video_dir is provided, please specify "
                                     "the video_dir argument")
            train_eval_env = PyCrCTFMonitor(self.env, self.attacker_config.video_dir + "/" + time_str, force=True,
                                      video_frequency=self.attacker_config.video_frequency, openai_baseline=True)
            train_eval_env.metadata["video.frames_per_second"] = self.attacker_config.video_fps

        eval_env = None

        if self.eval_env is not None:
            eval_env = PyCrCTFMonitor(self.eval_env, self.attacker_config.video_dir + "/" + time_str, force=True,
                                          video_frequency=self.attacker_config.video_frequency, openai_baseline=True)
            eval_env.metadata["video.frames_per_second"] = self.attacker_config.video_fps

        model.learn(total_timesteps=self.attacker_config.num_iterations,
                    log_interval=self.attacker_config.train_log_frequency,
                    eval_freq=self.attacker_config.eval_frequency,
                    n_eval_episodes=self.attacker_config.eval_episodes,
                    eval_env=train_eval_env,
                    eval_env_2=eval_env)

        self.attacker_config.logger.info("Training Complete")

        # Save networks
        model.save_model()

        # Save other game data
        if self.attacker_config.save_dir is not None:
            time_str = str(time.time())
            model.train_result.to_csv(self.attacker_config.save_dir + "/" + time_str + "_train_results_checkpoint.csv")
            model.eval_result.to_csv(self.attacker_config.save_dir + "/" + time_str + "_eval_results_checkpoint.csv")

        self.train_result = model.train_result
        self.eval_result = model.eval_result
        return model.train_result

    def get_action(self, s, eval=False, attacker=True) -> int:
        raise NotImplemented("not implemented")

    def eval(self, log=True) -> ExperimentResult:
        raise NotImplemented("not implemented")