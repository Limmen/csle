"""
Constants for csle-agents
"""


class COMMON:
    """
    Common string constants among all agents
    """
    NUM_CACHED_SIMULATION_TRACES = 3
    AVERAGE_RETURN = "average_return"
    RUNNING_AVERAGE_RETURN = "running_average_return"
    AVERAGE_DEFENDER_RETURN = "average_defender_return"
    RUNNING_AVERAGE_DEFENDER_RETURN = "running_average_defender_return"
    AVERAGE_ATTACKER_RETURN = "average_attacker_return"
    RUNNING_AVERAGE_ATTACKER_RETURN = "running_average_attacker_return"
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
    RUNNING_AVERAGE = "running_average"
    L = "L"
    STOPPING_ENVS = [
        "csle-stopping-game-v1",
        "csle-stopping-game-mdp-attacker-v1",
        "csle-stopping-game-pomdp-defender-v1"
    ]
    RUNNING_AVERAGE_INTRUSION_LENGTH = "running_average_intrusion_length"
    RUNNING_AVERAGE_INTRUSION_START = "running_average_intrusion_start"
    RUNNING_AVERAGE_TIME_HORIZON = "running_average_time_horizon"
    NUM_PARALLEL_ENVS = "num_parallel_envs"


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
    GRADIENT_BATCH_SIZE = "gradient_batch_size"
    STOP_DISTRIBUTION_ATTACKER = "stop_distribution_attacker"
    STOP_DISTRIBUTION_DEFENDER = "stop_distribution_defender"


class T_FP:
    """
    String constants related to T-FP
    """
    N_2 = "N_2"
    DEFENDER_THRESHOLDS = "defender_thresholds"
    ATTACKER_THRESHOLDS = "attacker_thresholds"
    THETA1_ATTACKER = "theta1_attacker"
    THETA1_DEFENDER = "theta1_defender"
    BEST_RESPONSE_EVALUATION_ITERATIONS = "best_response_evaluation_iterations"
    EQUILIBRIUM_STRATEGIES_EVALUATION_ITERATIONS = "equilibrium_strategies_evaluation_iterations"
    AVERAGE_BEST_RESPONSE_DEFENDER_RETURN = "average_best_response_defender_return"
    RUNNING_AVERAGE_BEST_RESPONSE_DEFENDER_RETURN = "running_average_best_response_defender_return"
    AVERAGE_BEST_RESPONSE_ATTACKER_RETURN = "average_best_response_attacker_return"
    RUNNING_AVERAGE_BEST_RESPONSE_ATTACKER_RETURN = "running_average_best_response_attacker_return"


class VI:
    """
    String constants related to VI
    """
    THETA = "theta"
    TRANSITION_TENSOR = "transition_tensor"
    REWARD_TENSOR = "reward_tensor"
    NUM_STATES = "num_states"
    NUM_ACTIONS = "num_actions"
    DELTA = "delta"


class HSVI:
    """
    String constants related to HSVI
    """
    WIDTH = "width"
    WIDTHS = "widths"
    TRANSITION_TENSOR = "transition_tensor"
    REWARD_TENSOR = "reward_tensor"
    OBSERVATION_TENSOR = "observation_tensor"
    OBSERVATION_SPACE = "observation_space"
    STATE_SPACE = "state_space"
    ACTION_SPACE = "action_space"
    EPSILON = "epsilon"
    UB_SIZE = "upper_bound_size"
    UB_SIZES = "upper_bound_sizes"
    LB_SIZE = "lower_bound_size"
    LB_SIZES = "lower_bound_sizes"
    INITIAL_BELIEF = "initial_belief"
    USE_LP = "use_lp"
    PRUNE_FREQUENCY = "prune_frequency"
    SIMULATION_FREQUENCY = "simulation_frequency"
    SIMULATE_HORIZON = "SIMULATE_HORIZON"
    NUMBER_OF_SIMULATIONS = "NUMBER_OF_SIMULATIONS"
    INITIAL_BELIEF_VALUES = "initial_belief_values"


class SONDIK_VI:
    """
    String constants related to Sondik's VI
    """
    TRANSITION_TENSOR = "transition_tensor"
    REWARD_TENSOR = "reward_tensor"
    OBSERVATION_TENSOR = "observation_tensor"
    OBSERVATION_SPACE = "observation_space"
    STATE_SPACE = "state_space"
    ACTION_SPACE = "action_space"
    INITIAL_BELIEF = "initial_belief"
    USE_PRUNING = "use_pruning"
    PLANNING_HORIZON = "planning_horizon"
    INITIAL_BELIEF_VALUES = "initial_belief_values"
    NUM_ALPHA_VECTORS = "num_alpha_vectors"


class DQN:
    """
    String constants related to DQN
    """
    MLP_POLICY = "MlpPolicy"
    LEARNING_STARTS = "learning_starts"
    EXPLORATION_FRACTION = "exploration_fracion"
    EXPLORATION_INITIAL_EPS = "exploration_initial_eps"
    EXPLORATION_FINAL_EPS = "exploration_final_eps"
    MAX_GRAD_NORM = "max_grad_norm"
    TRAIN_FREQ = "train_freq"
    GRADIENT_STEPS = "gradient_steps"
    N_EPISODES_ROLLOUT = "n_episodes_rollout"
    TARGET_UPDATE_INTERVAL = "target_update_interval"
    BUFFER_SIZE = "buffer_size"
    DQN_BATCH_SIZE = "dqn_batch_size"


class RANDOM_SEARCH:
    """
    String constants related to random search
    """
    L = "L"
    N = "N"
    THETA1 = "theta1"
    THETAS = "thetas"
    THRESHOLDS = "thresholds"
    STOP_DISTRIBUTION_ATTACKER = "stop_distribution_attacker"
    STOP_DISTRIBUTION_DEFENDER = "stop_distribution_defender"
    DELTA = "delta"