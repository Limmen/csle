"""
Constants for csle-agents
"""


class COMMON:
    """
    Common string constants among all agents
    """
    NUM_CACHED_SIMULATION_TRACES = 3
    AVERAGE_REWARD = "average_reward"
    AVERAGE_DISCOUNTED_REWARD = "average_discounted_reward"
    RUNNING_AVERAGE_REWARD = "running_average_reward"
    RUNNING_AVERAGE_DISCOUNTED_REWARD = "running_average_discounted_reward"
    DEFENDER_AVERAGE_REWARD = "defender_average_reward"
    DEFENDER_AVERAGE_DISCOUNTED_REWARD = "defender_average_discounted_reward"
    ATTACKER_AVERAGE_REWARD = "attacker_average_reward"
    ATTACKER_AVERAGE_DISCOUNTED_REWARD = "attacker_average_discounted_reward"
    EVAL_EVERY = "eval_every"
    SAVE_EVERY = "save_every"
    EVAL_BATCH_SIZE = "eval_batch_size"
    NUM_TRAINING_TIMESTEPS = "num_training_timesteps"
    NUM_NEURONS_PER_HIDDEN_LAYER = "num_neurons_per_hidden_layer"
    NUM_HIDDEN_LAYERS = "num_hidden_layers"
    BATCH_SIZE = "batch_size"
    LEARNING_RATE = "learning_rate"
    DEVICE = "device"
    GAMMA = "gamma"
    EXPLOITABILITY = "exploitability"
    RUNNING_AVERAGE_EXPLOITABILITY = "running_average_exploitability"
    CONFIDENCE_INTERVAL = "confidence_interval"
    MAX_ENV_STEPS = "max_env_steps"
    RUNNING_AVG = "running_avg"
    L = "L"
    STOPPING_ENVS = [
        "csle-stopping-game-v1",
        "csle-stopping-game-mdp-attacker-v1",
        "csle-stopping-game-pomdp-defender-v1"
    ]


class PPO:
    """
    String constants related to PPO
    """
    STEPS_BETWEEN_UPDATES = "steps_between_updates"
    GAE_LAMBDA = "gae_lambda"
    CLIP_RANGE = "clip_range"
    CLIP_RANGE_VF = "clip_range_vf"
    ENT_COEF = "ent_coef"
    VF_COEF = "vf_coef"
    MAX_GRAD_NORM = "max_grad_norm"
    TARGET_KL = "target_kl"
    MLP_POLICY = "MlpPolicy"


class T_SPSA:
    """
    String constants related to T-SPSA
    """
    a = "a"
    c = "c"
    LAMBDA = "lambda"
    A = "A"
    EPSILON = "epsilon"
    N = "N"
    L = "L"
    THETA1 = "theta1"
    THETAS = "thetas"
    THRESHOLDS = "thresholds"
    R = "R"
    GRADIENT_BATCH_SIZE = "gradient_batch_size"


class T_FP:
    """
    String constants related to T-FP
    """
    N_2 = "N_2"
    DEFENDER_THRESHOLDS = "defender_thresholds"
    ATTACKER_THRESHOLDS = "attacker_thresholds"
    THETA1_ATTACKER = "theta1_attacker"
    THETA1_DEFENDER = "theta1_defender"
