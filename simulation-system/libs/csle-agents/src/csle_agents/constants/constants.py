"""
Constants for csle-agents
"""


class COMMON:
    """
    Common string constants among all agents
    """
    WEIGHTED_INTRUSION_PREDICTION_DISTANCE = "weighted_intrusion_prediction_distance"
    RUNNING_AVERAGE_WEIGHTED_INTRUSION_PREDICTION_DISTANCE = "running_average_weighted_intrusion_prediction_distance"
    START_POINT_CORRECT = "start_point_correct"
    RUNNING_AVERAGE_START_POINT_CORRECT = "running_average_start_point_correct"
    NUM_CACHED_SIMULATION_TRACES = 3
    AVERAGE_RETURN = "average_return"
    RUNNING_AVERAGE_RETURN = "running_average_return"
    AVERAGE_DEFENDER_RETURN = "average_defender_return"
    RUNNING_AVERAGE_DEFENDER_RETURN = "running_average_defender_return"
    AVERAGE_ATTACKER_RETURN = "average_attacker_return"
    RUNNING_AVERAGE_ATTACKER_RETURN = "running_average_attacker_return"
    EVAL_PREFIX = "eval_"
    BASELINE_PREFIX = "baseline_"
    EVAL_EVERY = "eval_every"
    SAVE_EVERY = "save_every"
    EVAL_BATCH_SIZE = "eval_batch_size"
    BATCH_SIZE = "batch_size"
    LEARNING_RATE = "learning_rate"
    GAMMA = "gamma"
    NUM_TRAINING_TIMESTEPS = "num_training_timesteps"
    EXPLOITABILITY = "exploitability"
    POLICY_LOSSES = "policy_losses"
    RUNNING_AVERAGE_EXPLOITABILITY = "running_average_exploitability"
    CONFIDENCE_INTERVAL = "confidence_interval"
    MAX_ENV_STEPS = "max_env_steps"
    RUNNING_AVERAGE = "running_average"
    L = "L"
    NUM_NODES = "num_nodes"
    STOPPING_ENVS = [
        "csle-stopping-game-v1",
        "csle-stopping-game-mdp-attacker-v1",
        "csle-stopping-game-pomdp-defender-v1"
    ]
    RUNNING_AVERAGE_INTRUSION_LENGTH = "running_average_intrusion_length"
    RUNNING_AVERAGE_INTRUSION_START = "running_average_intrusion_start"
    AVERAGE_TIME_HORIZON = "average_time_horizon"
    AVERAGE_UPPER_BOUND_RETURN = "average_upper_bound_return"
    AVERAGE_RANDOM_RETURN = "average_random_return"
    AVERAGE_HEURISTIC_RETURN = "average_heuristic_return"
    RUNNING_AVERAGE_TIME_HORIZON = "running_average_time_horizon"
    NUM_PARALLEL_ENVS = "num_parallel_envs"
    OPTIMIZER = "optimizer"
    ADAM = "Adam"
    SGD = "SGD"
    LEARNING_RATE_EXP_DECAY = "learning_rate_exp_decay"
    LEARNING_RATE_DECAY_RATE = "learning_rate_decay_rate"
    RUNTIME = "runtime"
    EVALUATE_WITH_DISCOUNT = "evaluate_with_discount"
    STATE = "s"
    OBSERVATION = "o"
    REWARD = "r"


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
    NUM_GRADIENT_STEPS = "num_gradient_steps"


class PPO_CLEAN:
    """
    String constants related to PPO clean
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
    MINIBATCH_SIZE = "minibatch_size"
    NUM_STEPS = "num_steps"
    NUM_MINIBATCHES = "num_minibatches"
    NUM_ENVS = "num_envs"
    ANNEAL_LR = "anneal_lr"
    UPDATE_EPOCHS = "update_epochs"
    CLIP_VLOSS = "clip_vloss"
    REWARD_SCALER = "reward_scaler"
    NORM_ADV = "norm_adv"
    CUDA = "cuda"


class PPG_CLEAN:
    """
    String constants related to PPG clean
    """
    TOTAL_STEPS = "total_steps"
    LEARNING_RATE = "learning_rate"
    NUM_STEPS = "num_steps"
    ANNEAL_LR = "anneal_lr"
    GAMMA = "gamma"
    GAE_LAMBDA = "gae_lambda"
    NUM_MINIBATCHES = "num_minibatches"
    ADV_NORM_FULLBATCH = "adv_norm_fullbatch"
    CLIP_COEF = "clip_coef"
    ENT_COEF = "ent_coef"
    CLIP_VLOSS = "clip_vloss"
    VF_COEF = "vf_coef"
    MAX_GRAD_NORM = "max_grad_norm"
    TARGET_KL = "target_kl"
    N_ITERATION = "n_iteration"
    E_POLICY = "e_policy"
    E_AUXILIARY = "e_auxiliary"
    BETA_CLONE = "beta_clone"
    NUM_AUX_ROLLOUTS = "num_aux_rollouts"
    NUM_AUX_GRAD_ACCUM = "num_aux_grad_accum"
    BATCH_SIZE = "batch_size"
    MINIBATCH_SIZE = "minibatch_size"
    NUM_ITERATIONS = "num_iterations"
    NUM_PHASES = "num_phases"
    AUX_BATCH_ROLLOUTS = "aux_batch_rollouts"
    V_VALUE = "v_value"


class DQN_CLEAN:
    """
    String constants related to the DQN-Clean agent
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
    MINIBATCH_SIZE = "minibatch_size"
    NUM_STEPS = "num_steps"
    NUM_MINIBATCHES = "num_minibatches"
    NUM_ENVS = "num_envs"
    ANNEAL_LR = "anneal_lr"
    UPDATE_EPOCHS = "update_epochs"
    CLIP_VLOSS = "clip_vloss"
    REWARD_SCALER = "reward_scaler"
    NORM_ADV = "norm_adv"
    TAU = "tau"
    EXP_FRAC = "exploration_fraction"
    LEARNING_STARTS = "learning_starts"
    TRAIN_FREQ = "train_frequency"
    T_N_FREQ = "target_network_frequency"
    BUFFER_SIZE = "buffer_size"
    SAVE_MODEL = "save_model"
    CUDA = "cuda"


class C51_CLEAN:
    """
    String constants related to the C51-clean agent
    """
    STEPS_BETWEEN_UPDATES = "steps_between_updates"
    MINIBATCH_SIZE = "minibatch_size"
    NUM_STEPS = "num_steps"
    NUM_ENVS = "num_envs"
    ANNEAL_LR = "anneal_lr"
    CLIP_VLOSS = "clip_vloss"
    REWARD_SCALER = "reward_scaler"
    NORM_ADV = "norm_adv"
    TAU = "tau"
    EXP_FRAC = "exploration_fraction"
    LEARNING_STARTS = "learning_starts"
    TRAIN_FREQ = "train_frequency"
    T_N_FREQ = "target_network_frequency"
    BUFFER_SIZE = "buffer_size"
    START_EXPLORATION_RATE = "start_exploration_rate"
    END_EXPLORATION_RATE = "end_exploration_rate"
    SAVE_MODEL = "save_model"
    CUDA = "cuda"
    N_ATOMS = "n_atoms"
    V_MIN = "v_min"
    V_MAX = "v_max"


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
    POLICY_TYPE = "policy_type"
    OBJECTIVE_TYPE = "objective_type"


class SIMULATED_ANNEALING:
    """
    String constants related to simulated annealing
    """
    L = "L"
    N = "N"
    THETA1 = "theta1"
    THRESHOLDS = "thresholds"
    STOP_DISTRIBUTION_ATTACKER = "stop_distribution_attacker"
    STOP_DISTRIBUTION_DEFENDER = "stop_distribution_defender"
    THETAS = "thetas"
    DELTA = "delta"
    POLICY_TYPE = "policy_type"
    COOLING_FACTOR = "cooling_factor"
    INITIAL_TEMPERATURE = "initial_temperature"
    OBJECTIVE_TYPE = "objective_type"


class NELDER_MEAD:
    """
    String constants related to Nelder-Mead
    """
    L = "L"
    IMPROVE_THRESHOLD = "improve_threshold"
    IMPROVE_BREAK = "improve_break"
    N = "N"
    STEP = "step"
    THETA1 = "theta1"
    UCB = "ucb"
    THRESHOLDS = "thresholds"
    STOP_DISTRIBUTION_ATTACKER = "stop_distribution_attacker"
    STOP_DISTRIBUTION_DEFENDER = "stop_distribution_defender"
    UTILITY_FUNCTION = "utility_function"
    THETAS = "thetas"
    DELTA = "delta"
    POLICY_TYPE = "policy_type"
    COOLING_FACTOR = "cooling_factor"
    INITIAL_TEMPERATURE = "initial_temperature"
    OBJECTIVE_TYPE = "objective_type"


class BAYESIAN_OPTIMIZATION:
    """
    String constants related to Bayesian Optimization
    """
    L = "L"
    PARAMETER_BOUNDS = "parameter_bounds"
    N = "N"
    THETA1 = "theta1"
    THETAS = "thetas"
    THRESHOLDS = "thresholds"
    STOP_DISTRIBUTION_ATTACKER = "stop_distribution_attacker"
    STOP_DISTRIBUTION_DEFENDER = "stop_distribution_defender"
    UTILITY_FUNCTION = "utility_function"
    UCB_KAPPA = "ucb_kappa"
    UCB_XI = "ucb_xi"
    UCB = "ucb"
    TARGET = "target"
    PARAMS = "params"
    POLICY_TYPE = "policy_type"
    OBJECTIVE_TYPE = "objective_type"


class CMA_ES_OPTIMIZATION:
    """
    String constants related to CMA-ES Optimization
    """
    L = "L"
    PARAMETER_BOUNDS = "parameter_bounds"
    N = "N"
    THETA1 = "theta1"
    THETAS = "thetas"
    THRESHOLDS = "thresholds"
    STOP_DISTRIBUTION_ATTACKER = "stop_distribution_attacker"
    STOP_DISTRIBUTION_DEFENDER = "stop_distribution_defender"
    UTILITY_FUNCTION = "utility_function"
    UCB_KAPPA = "ucb_kappa"
    UCB_XI = "ucb_xi"
    UCB = "ucb"
    TARGET = "target"
    PARAMS = "params"
    POLICY_TYPE = "policy_type"
    OBJECTIVE_TYPE = "objective_type"


class PARTICLE_SWARM:
    """
    String constants related to simulated annealing
    """
    S = "S"
    B_LOW = "b_lo"
    B_UP = "b_up"
    INERTIA_WEIGHT = "w"
    COGNITIVE_COEFFICIENT = "Phi_p"
    SOCIAL_COEFFICIENT = "Phi_g"
    L = "L"
    N = "N"
    THETA1 = "theta1"
    THRESHOLDS = "thresholds"
    STOP_DISTRIBUTION_ATTACKER = "stop_distribution_attacker"
    STOP_DISTRIBUTION_DEFENDER = "stop_distribution_defender"
    THETAS = "thetas"
    DELTA = "delta"
    POLICY_TYPE = "policy_type"
    OBJECTIVE_TYPE = "objective_type"


class MCS:
    """
    String constants related to Multilevel Coordinate Search
    """
    STEP = "step"
    STEP1 = "step1"
    THETAS = "thetas"
    U = "u"
    V = "v"
    L = "L"
    STOPPING_ACTIONS = "stopping_actions"
    STOP_DISTRIBUTION_DEFENDER = "stop_distribution_defender"
    GAMMA = "gamma"
    EPSILON = "epsilon"
    LOCAL = "local"
    IINIT = "iinit"
    M = "m"
    PRT = "prt"
    SMAX = "smax"
    NF = "nf"
    STOP = "stop"
    POLICY_TYPE = "policy_type"
    OBJECTIVE_TYPE = "objective_type"
    THRESHOLDS = "thresholds"


class BAYESIAN_OPTIMIZATION_EMUKIT:
    """
    String constants related to Bayesian Optimization Emukit
    """
    POLICY_TYPE = "policy_type"
    EVALUATION_BUDGET = "evaluation_budget"
    LENGTHSCALE_RBF_KERNEL = "lengthscale_rbf_kernel"
    VARIANCE_RBF_KERNEL = "variance_rbf_kernel"
    OBS_LIKELIHOOD_VARIANCE = "obs_likelihood_variance"
    BETA = "beta"
    INPUT_SPACE_DIM = "input_space_dim"
    KERNEL_TYPE = "kernel_type"
    ACQUISITION_FUNCTION_TYPE = "acquisition_function_type"
    ACQUISITION_OPTIMIZER_TYPE = "acquisition_optimizer_type"
    X_init = "X_init"
    Y_init = "Y_init"
    PARAMS = "params"
    OBJECTIVE_TYPE = "objective_type"


class DIFFERENTIAL_EVOLUTION:
    """
    String constants related to differential evolution
    """
    L = "L"
    N = "N"
    POLICY_TYPE = "policy_type"
    OBJECTIVE_TYPE = "objective_type"
    THETA1 = "theta1"
    THETAS = "thetas"
    THRESHOLDS = "thresholds"
    STOP_DISTRIBUTION_ATTACKER = "stop_distribution_attacker"
    STOP_DISTRIBUTION_DEFENDER = "stop_distribution_defender"
    POPULATION_SIZE = "population_size"
    MUTATE = "mutate"
    RECOMBINATION = "recombination"
    BOUNDS = "bounds"


class CROSS_ENTROPY:
    """
    String constants related to the cross-entropy
    """
    L = "L"
    N = "N"
    K = "K"
    LAMB = "lamb"
    THETA1 = "theta1"
    THETAS = "thetas"
    THRESHOLDS = "thresholds"
    STOP_DISTRIBUTION_ATTACKER = "stop_distribution_attacker"
    STOP_DISTRIBUTION_DEFENDER = "stop_distribution_defender"
    POLICY_TYPE = "policy_type"
    OBJECTIVE_TYPE = "objective_type"


class KIEFER_WOLFOWITZ:
    """
    String constants related to Kiefer-Wolfowitz
    """
    N = "N"
    L = "L"
    THETA1 = "theta1"
    THETAS = "thetas"
    THRESHOLDS = "thresholds"
    GRADIENT_BATCH_SIZE = "gradient_batch_size"
    STOP_DISTRIBUTION_ATTACKER = "stop_distribution_attacker"
    STOP_DISTRIBUTION_DEFENDER = "stop_distribution_defender"
    INITIAL_ALPHA = "initial_alpha"
    DELTA = "delta"
    POLICY_TYPE = "policy_type"


class Q_LEARNING:
    """
    String constants related to Q-learning
    """
    N = "N"
    EPSILON = "epsilon"
    S = "S"
    A = "A"
    INITIAL_STATE_VALUES = "initial_state_values"
    EPSILON_DECAY_RATE = "epsilon_decay_rate"


class SARSA:
    """
    String constants related to Sarsa
    """
    N = "N"
    EPSILON = "epsilon"
    S = "S"
    A = "A"
    INITIAL_STATE_VALUES = "initial_state_values"


class PI:
    """
    String constants related to PI
    """
    TRANSITION_TENSOR = "transition_tensor"
    REWARD_TENSOR = "reward_tensor"
    NUM_STATES = "num_states"
    NUM_ACTIONS = "num_actions"
    N = "N"
    INITIAL_POLICY = "initial_policy"


class REINFORCE:
    """
    String constants related to REINFORCE
    """
    N = "N"
    GRADIENT_BATCH_SIZE = "gradient_batch_size"
    CLIP_GRADIENT = "clip_gradient"


class SHAPLEY_ITERATION:
    """
    String constants related to Shapley Iteration
    """
    N = "N"
    DELTA = "delta"
    TRANSITION_TENSOR = "transition_tensor"
    REWARD_TENSOR = "reward_tensor"
    STATE_SPACE = "state_space"
    ACTION_SPACE_PLAYER_1 = "action_space_player_1"
    ACTION_SPACE_PLAYER_2 = "action_space_player_2"


class HSVI_OS_POSG:
    """
    String constants related to the HSVI algorithm for OS-POSGs
    """
    N = "N"
    TRANSITION_TENSOR = "transition_tensor"
    REWARD_TENSOR = "reward_tensor"
    STATE_SPACE = "state_space"
    ACTION_SPACE_PLAYER_1 = "action_space_player_1"
    ACTION_SPACE_PLAYER_2 = "action_space_player_2"
    OBSERVATION_SPACE = "observation_space"
    OBSERVATION_FUNCTION = "observation_function"
    INITIAL_BELIEF = "initial_belief"
    PRUNE_FREQUENCY = "prune_frequency"
    EPSILON = "epsilon"
    WIDTHS = "widths"
    EXCESSES = "excesses"


class FICTITIOUS_PLAY:
    """
    String constants related to fictitious play
    """
    PAYOFF_MATRIX = "payoff_matrix"
    N = "N"
    PLAYER_1_PRIOR = "player_1_prior"
    PLAYER_2_PRIOR = "player_2_prior"


class LP_FOR_NF_GAMES:
    """
    String constants related to linear programming for normal-form games
    """
    PAYOFF_MATRIX = "payoff_matrix"
    N = "N"
    ACTION_SPACE_PLAYER_1 = "action_space_player_1"
    ACTION_SPACE_PLAYER_2 = "action_space_player_2"


class LP_FOR_CMDPs:
    """
    String constants related to linear programming for CMDPs
    """
    ACTIONS = "actions"
    STATES = "states"
    COST_TENSOR = "cost_tensor"
    TRANSITION_TENSOR = "transition_tensor"
    CONSTRAINT_COST_TENSORS = "constraint_cost_tensors"
    CONSTRAINT_COST_THRESHOLDS = "constraint_cost_thresholds"


class DYNASEC:
    """
    String constants related to the DynaSec algorithm
    """
    SLEEP_TIME = "sleep_time"
    EMULATION_TRACES_TO_SAVE_W_DATA_COLLECTION_JOB = "emulation_traces_to_save_with_data_collection_job"
    INTRUSION_START_P = "intrusion_start_p"
    TRAINING_EPOCHS = "training_epochs"
    WARMUP_EPISODES = "warmup_episodes"
    NUM_CLIENTS = "num_clients"
    CLIENTS_ARRIVAL_RATE = "clients_arrival_rate"
    EMULATION_MONITOR_SLEEP_TIME = "emulation_monitor_sleep_time"
    STATIC_ATTACKER_TYPE = "static_attacker_type"
    REPLAY_WINDOW_SIZE = "replay_window_size"
    INTRUSION_ALERTS_MEAN = "intrusion_alerts_mean"
    NO_INTRUSION_ALERTS_MEAN = "no_intrusion_alerts_mean"
    INTRUSION_ALERTS_MEAN_BASELINE = "intrusion_alerts_mean_baseline"
    NO_INTRUSION_ALERTS_MEAN_BASELINE = "no_intrusion_alerts_mean_baseline"


class ENV_METRICS:
    """
    String constants representing environment metrics
    """
    RETURN = "R"
    TIME_HORIZON = "T"
    STATE = "s"
    DEFENDER_ACTION = "a1"
    ATTACKER_ACTION = "a2"
    OBSERVATION = "o"
    TIME_STEP = "t"
    AVERAGE_UPPER_BOUND_RETURN = "average_upper_bound_return"
    AVERAGE_RANDOM_RETURN = "average_random_return"
    AVERAGE_HEURISTIC_RETURN = "average_heuristic_return"


class LOCAL_DFSP:
    """
    String constants related to the local DFSP algorithm
    """
    BEST_RESPONSE_EVALUATION_ITERATIONS = "best_response_evaluation_iterations"
    EQUILIBRIUM_STRATEGIES_EVALUATION_ITERATIONS = "equilibrium_strategies_evaluation_iterations"
    AVERAGE_BEST_RESPONSE_DEFENDER_RETURN = "average_best_response_defender_return"
    RUNNING_AVERAGE_BEST_RESPONSE_DEFENDER_RETURN = "running_average_best_response_defender_return"
    AVERAGE_BEST_RESPONSE_ATTACKER_RETURN = "average_best_response_attacker_return"
    RUNNING_AVERAGE_BEST_RESPONSE_ATTACKER_RETURN = "running_average_best_response_attacker_return"
    N_2 = "N_2"


class POMCP:
    """
    String constants related to POMCP
    """
    ROLLOUT_POLICY = "rollout_policy"
    VALUE_FUNCTION = "value_function"
    OBJECTIVE_TYPE = "objective_type"
    S = "S"
    N = "N"
    A = "A"
    O = "O"
    GAMMA = "gamma"
    INITIAL_PARTICLES = "initial_particles"
    REINVIGORATION = "reinvigoration"
    PLANNING_TIME = "planning_time"
    MAX_PARTICLES = "max_particles"
    MAX_NEGATIVE_SAMPLES = "max_negative_samples"
    C = "c"
    C2 = "c2"
    PRIOR_WEIGHT = "prior_weight"
    PRIOR_CONFIDENCE = "prior_confidence"
    MAX_PLANNING_DEPTH = "max_planning_depth"
    USE_ROLLOUT_POLICY = "use_rollout_policy"
    MAX_ROLLOUT_DEPTH = "max_rollout_depth"
    LOG_STEP_FREQUENCY = "log_step_frequency"
    DEFAULT_NODE_VALUE = "default_node_value"
    VERBOSE = "verbose"
    PARALLEL_ROLLOUT = "parallel_rollout"
    NUM_PARALLEL_PROCESSES = "num_parallel_processes"
    NUM_EVALS_PER_PROCESS = "num_evals_per_process"
    ACQUISITION_FUNCTION_TYPE = "acquisition_function_type"
    REINVIGORATED_PARTICLES_RATIO = "reinvigorated_particles_ratio"
    EVAL_ENV_NAME = "eval_env_name"
    EVAL_ENV_CONFIG = "eval_env_config"
    PRUNE_ACTION_SPACE = "prune_action_space"
    PRUNE_SIZE = "prune_size"
