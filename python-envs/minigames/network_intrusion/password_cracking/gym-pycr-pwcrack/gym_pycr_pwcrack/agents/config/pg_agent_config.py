"""
Configuration for Policy gradient agents
"""
import csv

class PolicyGradientAgentConfig:
    """
    DTO with configuration for PolicyGradientAgent
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
                 multi_input_channel : bool = False, fw_input_dim : int = 64, traffic_input_dim : int = 64,
                 ar_policy : bool = False, learning_attacker : bool = False, attacker_output_dim : int = 4,
                 attacker_input_dim: int = 40
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
        :param rule_hidden_layers: number of hidden layers of rule-head
        :param rule_hidden_dim: dimension of hidden layers of rule head
        :param protocol_hidden_layers: number of hidden layers of protocol-head
        :param protocol_hidden_dim: dimension of hidden layers of protocol head
        :param source_hidden_layers: number of hidden layers of source-head
        :param source_hidden_dim: dimension of hidden layers of source head
        :param port_hidden_layers: number of hidden layers of port-head
        :param port_hidden_dim: dimension of hidden layers of port head
        :param multi_headed_type: the type of the multi-headed architecture
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
        self.fw_input_dim = fw_input_dim
        self.traffic_input_dim = traffic_input_dim
        self.ar_policy = ar_policy
        self.learning_attacker = learning_attacker
        self.attacker_output_dim = attacker_output_dim
        self.attacker_input_dim = attacker_input_dim


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
               "ent_coef:{35},vf_coef:{36},use_sde:{37},sde_sample_freq:{38}".format(
            self.gamma, self.alpha, self.epsilon, self.render, self.eval_sleep, self.epsilon_decay,
            self.min_epsilon, self.eval_episodes, self.train_log_frequency, self.eval_log_frequency, self.video,
            self.video_fps, self.video_dir, self.num_episodes, self.eval_render, self.gifs, self.gif_dir,
            self.eval_frequency, self.video_frequency, self.checkpoint_freq,
            self.random_seed, self.eval_epsilon, self.clip_gradient, self.max_gradient_norm, self.output_dim,
            self.critic_loss_fn, self.state_length, self.gpu_id, self.eps_clip, self.input_dim, self.lr_progress_decay,
            self.lr_progress_power_decay, self.optimization_iterations, self.gae_lambda, self.features_dim,
            self.ent_coef, self.vf_coef, self.use_sde, self.sde_sample_freq)

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
        return hparams
