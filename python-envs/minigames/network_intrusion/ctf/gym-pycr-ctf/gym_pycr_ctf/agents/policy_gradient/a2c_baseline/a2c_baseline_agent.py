"""
An agent for the pycr-ctf env that uses the A2C Policy Gradient algorithm from OpenAI stable baselines
"""
import time
import torch
import math

from gym_pycr_ctf.rendering.video.pycr_ctf_monitor import PyCrCTFMonitor
from gym_pycr_ctf.envs.pycr_ctf_env import PyCRCTFEnv
from gym_pycr_ctf.dao.experiment.experiment_result import ExperimentResult
from gym_pycr_ctf.agents.train_agent import TrainAgent
from gym_pycr_ctf.agents.config.agent_config import AgentConfig
from gym_pycr_ctf.agents.policy_gradient.a2c_baseline.impl.a2c import A2C


class A2CBaselineAgent(TrainAgent):
    """
    An agent for the pycr-ctf env that uses the A2C Policy Gradient algorithm from OpenAI stable baselines
    """

    def __init__(self, env: PyCRCTFEnv, config: AgentConfig, eval_env: PyCRCTFEnv):
        """
        Initialize environment and hyperparameters

        :param config: the configuration
        """
        super(A2CBaselineAgent, self).__init__(env, config, eval_env)

    def train(self) -> ExperimentResult:
        """
        Starts the training loop and returns the result when complete

        :return: the training result
        """

        # Custom MLP policy
        net_arch = []
        pi_arch = []
        vf_arch = []
        for l in range(self.config.shared_layers):
            net_arch.append(self.config.shared_hidden_dim)
        for l in range(self.config.pi_hidden_layers):
            pi_arch.append(self.config.pi_hidden_dim)
        for l in range(self.config.vf_hidden_layers):
            vf_arch.append(self.config.vf_hidden_dim)


        net_dict = {"pi":pi_arch, "vf":vf_arch}
        net_arch.append(net_dict)

        policy_kwargs = dict(activation_fn=self.get_hidden_activation(), net_arch=net_arch)
        device = "cpu" if not self.config.gpu else "cuda:" + str(self.config.gpu_id)
        policy = "MlpPolicy"

        if self.config.lr_progress_decay:
            temp = self.config.alpha
            lr_decay_func = lambda x: temp*math.pow(x, self.config.lr_progress_power_decay)
            self.config.alpha = lr_decay_func

        model = A2C(policy, self.env,
                    learning_rate=self.config.alpha,
                    n_steps=self.config.batch_size,
                    gamma=self.config.gamma,
                    gae_lambda=self.config.gae_lambda,
                    max_grad_norm=self.config.max_gradient_norm,
                    verbose=1,
                    seed=self.config.random_seed,
                    policy_kwargs=policy_kwargs,
                    device=device,
                    agent_config=self.config,
                    vf_coef=self.config.vf_coef,
                    ent_coef=self.config.ent_coef,
                    use_sde=self.config.use_sde,
                    sde_sample_freq=self.config.sde_sample_freq,
                    env_2=self.eval_env
                    )

        if self.config.load_path is not None:
            A2C.load(self.config.load_path, policy, agent_config=self.config)


        # Eval config
        if self.config.video or self.config.gifs:
            time_str = str(time.time())
            if self.config.video_dir is None:
                raise AssertionError("Video is set to True but no video_dir is provided, please specify "
                                     "the video_dir argument")
            train_eval_env = PyCrCTFMonitor(self.env, self.config.video_dir + "/" + time_str, force=True,
                                      video_frequency=self.config.video_frequency, openai_baseline=True)
            train_eval_env.metadata["video.frames_per_second"] = self.config.video_fps

        eval_env = None

        if self.eval_env is not None:
            eval_env = PyCrCTFMonitor(self.eval_env, self.config.video_dir + "/" + time_str, force=True,
                                          video_frequency=self.config.video_frequency, openai_baseline=True)
            eval_env.metadata["video.frames_per_second"] = self.config.video_fps

        model.learn(total_timesteps=self.config.num_episodes,
                    log_interval=self.config.train_log_frequency,
                    eval_freq=self.config.eval_frequency,
                    n_eval_episodes=self.config.eval_episodes,
                    eval_env=train_eval_env,
                    eval_env_2=eval_env
                    )

        self.config.logger.info("Training Complete")

        # Save networks
        model.save_model()

        # Save other game data
        if self.config.save_dir is not None:
            time_str = str(time.time())
            model.train_result.to_csv(self.config.save_dir + "/" + time_str + "_train_results_checkpoint.csv")
            model.eval_result.to_csv(self.config.save_dir + "/" + time_str + "_eval_results_checkpoint.csv")

        self.train_result = model.train_result
        self.eval_result = model.eval_result
        return model.train_result

    def get_hidden_activation(self):
        """
        Interprets the hidden activation

        :return: the hidden activation function
        """
        return torch.nn.Tanh
        if self.config.hidden_activation == "ReLU":
            return torch.nn.ReLU
        elif self.config.hidden_activation == "LeakyReLU":
            return torch.nn.LeakyReLU
        elif self.config.hidden_activation == "LogSigmoid":
            return torch.nn.LogSigmoid
        elif self.config.hidden_activation == "PReLU":
            return torch.nn.PReLU
        elif self.config.hidden_activation == "Sigmoid":
            return torch.nn.Sigmoid
        elif self.config.hidden_activation == "Softplus":
            return torch.nn.Softplus
        elif self.config.hidden_activation == "Tanh":
            return torch.nn.Tanh
        else:
            raise ValueError("Activation type: {} not recognized".format(self.config.hidden_activation))


    def get_action(self, s, eval=False, attacker=True) -> int:
        raise NotImplemented("not implemented")

    def eval(self, log=True) -> ExperimentResult:
        raise NotImplemented("not implemented")