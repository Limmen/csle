"""
Configuration for training agents
"""
import csv

class AgentConfig:
    """
    DTO with configuration for training agents
    """

    def __init__(self, gamma :float = 0.8, alpha:float = 0.1,
                 epsilon :float =0.9, render :bool =False,
                 eval_sleep :float = 0.35,
                 epsilon_decay :float = 0.999, min_epsilon :float = 0.1, eval_episodes :int = 1,
                 train_log_frequency :int =100,
                 eval_log_frequency :int =1, video :bool = False, video_fps :int = 5, video_dir :bool = None,
                 num_episodes :int = 5000,
                 eval_render :bool = False, gifs :bool = False, gif_dir: str = None, eval_frequency :int =1000,
                 video_frequency :int = 101,
                 save_dir :str = None, load_path : str = None,
                 checkpoint_freq : int = 100000, random_seed: int = 0, eval_epsilon : float = 0.0,
                 input_dim: int = 30, output_dim: int = 30,
                 pi_hidden_dim: int = 64, batch_size: int = 64, pi_hidden_layers=2,
                 vf_hidden_layers=2, vf_hidden_dim: int = 64,
                 gpu: bool = False, tensorboard: bool = False, tensorboard_dir: str = "",
                 optimizer: str = "Adam", lr_exp_decay: bool = False,
                 lr_decay_rate: float = 0.96, hidden_activation: str = "ReLU", clip_gradient = False,
                 max_gradient_norm = 40, critic_loss_fn : str = "MSE", state_length = 1,
                 gpu_id: int = 0, eps_clip : float = 0.2, lr_progress_decay : bool = False,
                 lr_progress_power_decay : int = 1, optimization_iterations : int = 28,
                 gae_lambda: float = 0.95, features_dim: int = 44,
                 ent_coef: float = 0.0, vf_coef: float = 0.5, use_sde: bool = False, sde_sample_freq: int = 4,
                 shared_hidden_dim : int = 64, shared_hidden_layers = 4,
                 mini_batch_size : int = 64, render_steps: int = 20, num_iterations : int = 50,
                 multi_input_channel : bool = False,
                 ar_policy : bool = False, illegal_action_logit = -100, buffer_size : int = 1000000,
                 tau : float = 1.0, learning_starts : int = 50000, train_freq : int = 4, gradient_steps: int = 1,
                 target_update_interval: int = 10000, exploration_fraction: float = 0.1,
                 exploration_initial_eps: float = 1.0, exploration_final_eps: float = 0.05,
                 policy_delay : int = 2, target_policy_noise : float = 0.2, target_noise_clip : float = 0.5,
                 input_dim_2 : int = 30, output_dim_2 : int = 30, pi_hidden_dim_2 : int = 64,
                 pi_hidden_layers_2 : int = 2, vf_hidden_layers_2 : int = 2, vf_hidden_dim_2 : int = 64,
                 filter_illegal_actions : bool = False, train_progress_deterministic_eval: bool = False,
                 eval_deterministic: bool = False,
                 n_deterministic_eval_iter : int = 10, env_config = None, env_configs = None,
                 eval_env_config = None, eval_env_configs = None, num_nodes: int = 10,
                 performance_analysis : bool = False, ar_policy2: bool = False
                 ):
        """
        Initialize environment and hyperparameters

        :param gamma: the discount factor
        :param alpha: the learning rate
        :param epsilon: the exploration rate
        :param render: whether to render the environment *during training*
        :param eval_sleep: amount of sleep between time-steps during evaluation and rendering
        :param epsilon_decay: rate of decay of epsilon
        :param min_epsilon: minimum epsilon rate
        :param eval_episodes: number of evaluation episodes
        :param train_log_frequency: number of episodes between logs during train
        :param eval_log_frequency: number of episodes between logs during eval
        :param video: boolean flag whether to record video of the evaluation.
        :param video_dir: path where to save videos (will overwrite)
        :param gif_dir: path where to save gifs (will overwrite)
        :param num_episodes: number of training epochs
        :param eval_render: whether to render the game during evaluation or not
                            (perhaps set to False if video is recorded instead)
        :param gifs: boolean flag whether to save gifs during evaluation or not
        :param eval_frequency: the frequency (episodes) when running evaluation
        :param video_frequency: the frequency (eval episodes) to record video and gif
        :param save_dir: dir to save model
        :param load_path: path to load a saved model
        :param checkpoint_freq: frequency of checkpointing the model (episodes)
        :param random_seed: the random seed for reproducibility
        :param eval_epsilon: evaluation epsilon for implementing a "soft policy" rather than a "greedy policy"
        :param input_dim: input dimension of the policy network
        :param output_dim: output dimensions of the policy network
        :param pi_hidden_dim: hidden dimension of the policy network
        :param pi_hidden_layers: number of hidden layers in the policy network
        :param vf_hidden_dim: hidden dimension of the value network
        :param vf_hidden_layers: number of hidden layers in the value network
        :param batch_size: the batch size during training
        :param gpu: boolean flag whether using GPU or not
        :param tensorboard: boolean flag whether using tensorboard logging or not
        :param tensorboard_dir: tensorboard logdir
        :param optimizer: optimizer
        :param lr_exp_decay: whether to use exponential decay of learning rate or not
        :param lr_decay_rate: decay rate of lr
        :param hidden_activation: the activation function for hidden units
        :param clip_gradient: boolean flag whether to clip gradient or not
        :param max_gradient_norm: max norm of gradient before clipping it
        :param critic_loss_fn: loss function for the critic
        :param state_length: length of observations to use for approximative Markov state
        :param gpu_id: id of the GPU to use
        :param optimization_iterations: number of optimization iterations, this correspond to "K" in PPO
        :param eps_clip: clip parameter for PPO
        :param lr_progress_decay: boolean flag whether learning rate is decayed with respect to progress
        :param lr_progress_power_decay: the power that the progress is raised before lr decay
        :param optimization_iterations: number of optimization iterations, this correspond to "K" in PPO
        :param gae_lambda: gae_lambda parameter of PPO
        :param features_dim: number of features in final layer of CNN before softmax
        :param ent_coef: entropy coefficient for PPO
        :param vf_coef: value coefficient for PPO
        :param use_sde: boolean flag whether to use state-dependent exploration
        :param sde_sample_freq: frequency of sampling in state-dependent exploration
        :param multiple_heads: boolean flag whether to use multi-headed NN for the combinatorial action space
        :param shared_hidden_layers_dim: dimension of the shared hidden layers
        :param shared_hidden_layers: number of shared hidden layers
        :param mini_batch_size: the minibatch size to use for training
        :param render_steps: maximum number of steps when rendering an episode
        :param num_iterations: number of training iterations
        :param multi_input_channel: boolean flag whether to use a multi-input channel or not if supported
        :param ar_policy: boolean flag whether to use auto-regressive policy or not if supported
        :param illegal_action_logit: value to mask illegal action logits with
        :param buffer_size: size of the replay buffer for off-policy algorithms
        :param tau: tau
        :param learning_starts: specify how much warmup to use to populate replay buffer
        :param train_freq: train frequency for off policy algos
        :param gradient_steps: gradient steps for off policy algos
        :param target_update_interval: update interval with target network for DQN
        :param exploration_fraction: exploration fraction for off policy algos
        :param exploration_initial_eps: exploration initial eps for off policy algos
        :param exploration_final_eps: exploration final eps for off policy algos
        :param policy_delay: policy delay for TD3 and similar algos
        :param target_policy_noise: policy noise for TD3 and similar algos
        :param target_noise_clip: target noise for TD3 and similar algos
        :param filter_illegal_actions: boolean flag whether to filter illegal actions
        :param train_progress_deterministic_eval: boolean flag whether to use deterministic policy for eval during train
        :param n_deterministic_eval_iter: number of iterations for determinisitic eval
        """
        self.gamma = gamma
        self.alpha = alpha
        self.epsilon = epsilon
        self.render = render
        self.eval_sleep = eval_sleep
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.eval_episodes = eval_episodes
        self.train_log_frequency = train_log_frequency
        self.eval_log_frequency = eval_log_frequency
        self.video = video
        self.video_fps = video_fps
        self.video_dir = video_dir
        self.num_episodes = num_episodes
        self.eval_render = eval_render
        self.gifs = gifs
        self.gif_dir = gif_dir
        self.eval_frequency = eval_frequency
        self.logger = None
        self.video_frequency = video_frequency
        self.save_dir = save_dir
        self.load_path = load_path
        self.checkpoint_freq = checkpoint_freq
        self.random_seed = random_seed
        self.eval_epsilon = eval_epsilon
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.pi_hidden_dim = pi_hidden_dim
        self.batch_size = batch_size
        self.pi_hidden_layers = pi_hidden_layers
        self.gpu = gpu
        self.tensorboard = tensorboard
        self.tensorboard_dir = tensorboard_dir
        self.optimizer = optimizer
        self.lr_exp_decay = lr_exp_decay
        self.lr_decay_rate = lr_decay_rate
        self.hidden_activation = hidden_activation
        self.clip_gradient = clip_gradient
        self.max_gradient_norm = max_gradient_norm
        self.critic_loss_fn = critic_loss_fn
        self.state_length = state_length
        self.gpu_id = gpu_id
        self.eps_clip = eps_clip
        self.lr_progress_decay = lr_progress_decay
        self.lr_progress_power_decay = lr_progress_power_decay
        self.optimization_iterations = optimization_iterations
        self.gae_lambda = gae_lambda
        self.features_dim = features_dim
        self.ent_coef = ent_coef
        self.vf_coef = vf_coef
        self.use_sde = use_sde
        self.sde_sample_freq = sde_sample_freq
        self.vf_hidden_dim = vf_hidden_dim
        self.vf_hidden_layers = vf_hidden_layers
        self.shared_layers = shared_hidden_layers
        self.shared_hidden_dim = shared_hidden_dim
        self.mini_batch_size = mini_batch_size
        self.render_steps = render_steps
        self.num_iterations = num_iterations
        self.multi_input_channel = multi_input_channel
        self.ar_policy = ar_policy
        self.illegal_action_logit = illegal_action_logit
        self.buffer_size = buffer_size
        self.tau = tau
        self.learning_starts = learning_starts
        self.train_freq = train_freq
        self.gradient_steps = gradient_steps
        self.target_update_interval = target_update_interval
        self.exploration_fraction = exploration_fraction
        self.exploration_initial_eps = exploration_initial_eps
        self.exploration_final_eps = exploration_final_eps
        self.policy_delay = policy_delay
        self.target_policy_noise = target_policy_noise
        self.target_noise_clip = target_noise_clip
        self.input_dim_2 = input_dim_2
        self.output_dim_2 = output_dim_2
        self.pi_hidden_dim_2 = pi_hidden_dim_2
        self.pi_hidden_layers_2 = pi_hidden_layers_2
        self.vf_hidden_layers_2 = vf_hidden_layers_2
        self.vf_hidden_dim_2 = vf_hidden_dim_2
        self.filter_illegal_actions = filter_illegal_actions
        self.train_progress_deterministic_eval = train_progress_deterministic_eval
        self.n_deterministic_eval_iter = n_deterministic_eval_iter
        self.env_config = env_config
        self.env_configs = env_configs
        self.eval_env_config = eval_env_config
        self.eval_env_configs = eval_env_configs
        self.eval_deterministic = eval_deterministic
        self.num_nodes = num_nodes
        self.performance_analysis = performance_analysis
        self.ar_policy2 = ar_policy2


    def to_str(self) -> str:
        """
        :return: a string with information about all of the parameters
        """
        return "Hyperparameters: gamma:{0},alpha:{1},epsilon:{2},render:{3},eval_sleep:{4}," \
               "epsilon_decay:{5},min_epsilon:{6},eval_episodes:{7},train_log_frequency:{8}," \
               "eval_log_frequency:{9},video:{10},video_fps:{11}," \
               "video_dir:{12},num_episodes:{13},eval_render:{14},gifs:{15}," \
               "gifdir:{16},eval_frequency:{17},video_frequency:{18}" \
               "checkpoint_freq:{19},random_seed:{20},eval_epsilon:{21},clip_gradient:{22},max_gradient_norm:{23}," \
               "output_dim:{24},critic_loss_fn:{25},state_length:{26}" \
               "gpu_id:{27},eps_clip:{28},input_dim:{29},lr_progress_decay:{30},lr_progress_power_decay:{31}," \
               "optimization_iterations:{32},gae_lambda:{33},features_dim:{34}," \
               "ent_coef:{35},vf_coef:{36},use_sde:{37},sde_sample_freq:{38},illegal_action_logit:{39}," \
               "save_dir:{40}, load_path:{41}, pi_hidden_dim:{42}, pi_hidden_layers:{43}," \
               "vf_hidden_layers:{44},vf_hidden_dim:{45},gpu:{46},tensorboard:{47},tensorboard_dir:{48}," \
               "optimizer:{50},lr_exp_decay:{51},hidden_activation:{52},render_steps:{53}," \
               "num_iterations:{54},mini_batch_size:{55},shared_hidden_dim:{56},shared_hidden_layers:{57}," \
               "ar_policy:{58},buffer_size:{59},tau:{60},learning_starts:{61},train_freq:{62}," \
               "gradient_steps:{63},target_update_interval:{64},exploration_fraction:{65}," \
               "exploration_initial_eps:{66},exploration_final_eps:{67},policy_delay:{68}," \
               "target_policy_noise:{69},target_noise_clip:{70},input_dim_2:{71}," \
               "output_dim_2:{72},pi_hidden_dim_2:{73},pi_hidden_layers_2:{74}," \
               "vf_hidden_layers_2:{75},vf_hidden_dim_2:{76},filter_illegal_actions:{77}," \
               "train_progress_deterministic_eval:{78},n_deterministic_eval_iter:{79}".format(
            self.gamma, self.alpha, self.epsilon, self.render, self.eval_sleep, self.epsilon_decay,
            self.min_epsilon, self.eval_episodes, self.train_log_frequency, self.eval_log_frequency, self.video,
            self.video_fps, self.video_dir, self.num_episodes, self.eval_render, self.gifs, self.gif_dir,
            self.eval_frequency, self.video_frequency, self.checkpoint_freq,
            self.random_seed, self.eval_epsilon, self.clip_gradient, self.max_gradient_norm, self.output_dim,
            self.critic_loss_fn, self.state_length, self.gpu_id, self.eps_clip, self.input_dim, self.lr_progress_decay,
            self.lr_progress_power_decay, self.optimization_iterations, self.gae_lambda, self.features_dim,
            self.ent_coef, self.vf_coef, self.use_sde, self.sde_sample_freq, self.illegal_action_logit,
            self.save_dir, self.load_path, self.pi_hidden_dim, self.pi_hidden_layers, self.vf_hidden_layers,
            self.vf_hidden_dim, self.gpu, self.tensorboard, self.tensorboard_dir,self.optimizer,
            self.lr_exp_decay, self.hidden_activation, self.render_steps, self.num_iterations, self.mini_batch_size,
            self.shared_hidden_dim, self.shared_layers, self.ar_policy,self.buffer_size,self.tau,
            self.learning_starts, self.train_freq, self.gradient_steps, self.target_update_interval,
            self.target_update_interval, self.exploration_fraction,self.exploration_initial_eps,
            self.exploration_final_eps, self.policy_delay, self.target_policy_noise, self.target_noise_clip,
            self.input_dim_2, self.output_dim_2, self.pi_hidden_dim_2, self.pi_hidden_layers_2, self.vf_hidden_layers_2,
            self.vf_hidden_dim_2, self.filter_illegal_actions, self.train_progress_deterministic_eval,
            self.n_deterministic_eval_iter)

    def to_csv(self, file_path: str) -> None:
        """
        Write parameters to csv file

        :param file_path: path to the file
        :return: None
        """
        with open(file_path, "w") as f:
            writer = csv.writer(f)
            writer.writerow(["parameter", "value"])
            writer.writerow(["gamma", str(self.gamma)])
            writer.writerow(["alpha", str(self.alpha)])
            writer.writerow(["epsilon", str(self.epsilon)])
            writer.writerow(["render", str(self.render)])
            writer.writerow(["eval_sleep", str(self.eval_sleep)])
            writer.writerow(["epsilon_decay", str(self.epsilon_decay)])
            writer.writerow(["min_epsilon", str(self.min_epsilon)])
            writer.writerow(["eval_episodes", str(self.eval_episodes)])
            writer.writerow(["train_log_frequency", str(self.train_log_frequency)])
            writer.writerow(["eval_log_frequency", str(self.eval_log_frequency)])
            writer.writerow(["video", str(self.video)])
            writer.writerow(["video_fps", str(self.video_fps)])
            writer.writerow(["video_dir", str(self.video_dir)])
            writer.writerow(["num_episodes", str(self.num_episodes)])
            writer.writerow(["eval_render", str(self.eval_render)])
            writer.writerow(["gifs", str(self.gifs)])
            writer.writerow(["gifdir", str(self.gif_dir)])
            writer.writerow(["eval_frequency", str(self.eval_frequency)])
            writer.writerow(["video_frequency", str(self.video_frequency)])
            writer.writerow(["checkpoint_freq", str(self.checkpoint_freq)])
            writer.writerow(["random_seed", str(self.random_seed)])
            writer.writerow(["eval_epsilon", str(self.eval_epsilon)])
            writer.writerow(["input", str(self.input_dim)])
            writer.writerow(["output_dim", str(self.output_dim)])
            writer.writerow(["hidden_dim", str(self.pi_hidden_dim)])
            writer.writerow(["batch_size", str(self.batch_size)])
            writer.writerow(["gpu", str(self.gpu)])
            writer.writerow(["tensorboard", str(self.tensorboard)])
            writer.writerow(["tensorboard_dir", str(self.tensorboard_dir)])
            writer.writerow(["optimizer", str(self.optimizer)])
            writer.writerow(["num_hidden_layers", str(self.pi_hidden_layers)])
            writer.writerow(["lr_exp_decay", str(self.lr_exp_decay)])
            writer.writerow(["lr_decay_rate", str(self.lr_decay_rate)])
            writer.writerow(["hidden_activation", str(self.hidden_activation)])
            writer.writerow(["clip_gradient", str(self.clip_gradient)])
            writer.writerow(["max_gradient_norm", str(self.max_gradient_norm)])
            writer.writerow(["output_dim", str(self.output_dim)])
            writer.writerow(["critic_loss_fn", str(self.critic_loss_fn)])
            writer.writerow(["state_length", str(self.state_length)])
            writer.writerow(["gpu_id", str(self.gpu_id)])
            writer.writerow(["eps_clip", str(self.eps_clip)])
            writer.writerow(["lr_progress_decay", str(self.lr_progress_decay)])
            writer.writerow(["lr_progress_power_decay", str(self.lr_progress_power_decay)])
            writer.writerow(["optimization_iterations", str(self.optimization_iterations)])
            writer.writerow(["gae_lambda", str(self.gae_lambda)])
            writer.writerow(["features_dim", str(self.features_dim)])
            writer.writerow(["ent_coef", str(self.ent_coef)])
            writer.writerow(["vf_coef", str(self.vf_coef)])
            writer.writerow(["use_sde", str(self.use_sde)])
            writer.writerow(["sde_sample_freq", str(self.sde_sample_freq)])
            writer.writerow(["illegal_action_logit", str(self.illegal_action_logit)])
            writer.writerow(["buffer_size", str(self.buffer_size)])
            writer.writerow(["tau", str(self.tau)])
            writer.writerow(["learning_starts", str(self.learning_starts)])
            writer.writerow(["train_freq", str(self.train_freq)])
            writer.writerow(["gradient_steps", str(self.gradient_steps)])
            writer.writerow(["target_update_interval", str(self.target_update_interval)])
            writer.writerow(["exploration_fraction", str(self.exploration_fraction)])
            writer.writerow(["exploration_initial_eps", str(self.exploration_initial_eps)])
            writer.writerow(["exploration_final_eps", str(self.exploration_final_eps)])
            writer.writerow(["policy_delay", str(self.policy_delay)])
            writer.writerow(["target_policy_noise", str(self.target_policy_noise)])
            writer.writerow(["target_noise_clip", str(self.target_noise_clip)])
            writer.writerow(["input_dim_2", str(self.input_dim_2)])
            writer.writerow(["output_dim_2", str(self.output_dim_2)])
            writer.writerow(["pi_hidden_dim_2", str(self.pi_hidden_dim_2)])
            writer.writerow(["pi_hidden_layers_2", str(self.pi_hidden_layers_2)])
            writer.writerow(["vf_hidden_layers_2", str(self.vf_hidden_layers_2)])
            writer.writerow(["vf_hidden_dim_2", str(self.vf_hidden_dim_2)])
            writer.writerow(["filter_illegal_actions", str(self.filter_illegal_actions)])
            writer.writerow(["train_progress_deterministic_eval", str(self.train_progress_deterministic_eval)])
            writer.writerow(["n_deterministic_eval_iter", str(self.n_deterministic_eval_iter)])


    def hparams_dict(self):
        hparams = {}
        hparams["gamma"] = self.gamma
        hparams["alpha"] = self.alpha
        hparams["epsilon"] = self.epsilon
        hparams["epsilon_decay"] = self.epsilon_decay
        hparams["min_epsilon"] = self.min_epsilon
        hparams["eval_episodes"] = self.eval_episodes
        hparams["train_log_frequency"] = self.train_log_frequency
        hparams["eval_log_frequency"] = self.eval_log_frequency
        hparams["num_episodes"] = self.num_episodes
        hparams["eval_frequency"] = self.eval_frequency
        hparams["checkpoint_freq"] = self.checkpoint_freq
        hparams["random_seed"] = self.random_seed
        hparams["eval_epsilon"] = self.eval_epsilon
        hparams["input_dim"] = self.input_dim
        hparams["output_dim"] = self.output_dim
        hparams["hidden_dim"] = self.pi_hidden_dim
        hparams["batch_size"] = self.batch_size
        hparams["num_hidden_layers"] = self.pi_hidden_layers
        hparams["gpu"] = self.gpu
        hparams["optimizer"] = self.optimizer
        hparams["lr_exp_decay"] = self.lr_exp_decay
        hparams["lr_decay_rate"] = self.lr_decay_rate
        hparams["hidden_activation"] = self.hidden_activation
        hparams["clip_gradient"] = self.clip_gradient
        hparams["max_gradient_norm"] = self.max_gradient_norm
        hparams["output_dim"] = self.output_dim
        hparams["critic_loss_fn"] = self.critic_loss_fn
        hparams["state_length"] = self.state_length
        hparams["gpu_id"] = self.gpu_id
        hparams["eps_clip"] = self.eps_clip
        hparams["lr_progress_decay"] = self.lr_progress_decay
        hparams["lr_progress_power_decay"] = self.lr_progress_power_decay
        hparams["optimization_iterations"] = self.optimization_iterations
        hparams["gae_lambda"] = self.gae_lambda
        hparams["features_dim"] = self.features_dim
        hparams["ent_coef"] = self.ent_coef
        hparams["vf_coef"] = self.vf_coef
        hparams["use_sde"] = self.use_sde
        hparams["sde_sample_freq"] = self.sde_sample_freq
        hparams["illegal_action_logit"] = self.illegal_action_logit
        hparams["buffer_size"] = self.buffer_size
        hparams["tau"] = self.tau
        hparams["learning_starts"] = self.learning_starts
        hparams["train_freq"] = self.train_freq
        hparams["gradient_steps"] = self.gradient_steps
        hparams["target_update_interval"] = self.target_update_interval
        hparams["exploration_fraction"] = self.exploration_fraction
        hparams["exploration_initial_eps"] = self.exploration_initial_eps
        hparams["exploration_final_eps"] = self.exploration_final_eps
        hparams["policy_delay"] = self.policy_delay
        hparams["target_policy_noise"] = self.target_policy_noise
        hparams["target_noise_clip"] = self.target_noise_clip
        hparams["input_dim_2"] = self.input_dim_2
        hparams["output_dim_2"] = self.output_dim_2
        hparams["pi_hidden_dim_2"] = self.pi_hidden_dim_2
        hparams["pi_hidden_layers_2"] = self.pi_hidden_layers_2
        hparams["vf_hidden_layers_2"] = self.vf_hidden_layers_2
        hparams["vf_hidden_dim_2"] = self.vf_hidden_dim_2
        hparams["filter_illegal_actions"] = self.filter_illegal_actions
        hparams["train_progress_deterministic_eval"] = self.train_progress_deterministic_eval
        hparams["n_deterministic_eval_iter"] = self.n_deterministic_eval_iter
        return hparams
