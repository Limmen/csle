from typing import List
import logging
import datetime
import numpy as np
import random
from emukit.core import ParameterSpace, ContinuousParameter
from csle_tolerance.envs.intrusion_recovery_pomdp_env import IntrusionRecoveryPomdpEnv
from csle_tolerance.dao.intrusion_recovery_pomdp_config import IntrusionRecoveryPomdpConfig
from csle_tolerance.util.intrusion_recovery_pomdp_util import IntrusionRecoveryPomdpUtil
from csle_tolerance.dao.bo.bo_config import BOConfig
from csle_tolerance.dao.bo.gp.gp_config import GPConfig
from csle_tolerance.dao.bo.kernel.rbf_kernel_config import RBFKernelConfig
from csle_tolerance.dao.bo.acquisition.acquisition_function_type import AcquisitionFunctionType
from csle_tolerance.dao.bo.acquisition.acquisition_optimizer_type import AcquisitionOptimizerType
from csle_tolerance.algorithms.bo import BO
from csle_tolerance.dao.bo.optimization.objective_type import ObjectiveType
from csle_tolerance.plotting.plot_intrusion_recovery_single_threshold_results import plot_bo_results_and_gp


def evaluate_threshold(alphas: List[float], env: IntrusionRecoveryPomdpEnv, n_samples = 100) -> float:
    """
    Black box objective function of the intrusion recover POMDP

    :param alphas: the threshold
    :param env: the POMDP environment
    :param n_samples: the number of samples to estimate the mean
    :return: the estimated expected cost
    """
    if not isinstance(alphas[0], float):
        alphas = alphas[0]
    costs = []
    for i in range(n_samples):
        cumulative_cost = 0
        s, _ = env.reset()
        done = False
        t = 0
        while not done:
            alpha = alphas[t]
            b = s[2]
            a = 0
            if b >= alpha:
                a = 1
            s, c, _, done, info = env.step(a=a)
            cumulative_cost += c
            t+= 1
        costs.append(cumulative_cost)
    return float(np.mean(costs))



if __name__ == '__main__':
    # --- Define POMDP configuration ---
    num_observations = 10
    eta = 1
    p_a = 0.3
    p_c_1 = 0.00001
    p_c_2 = 0.001
    p_u = 0.02
    BTR = 20
    negate_costs = False
    seed = 999
    discount_factor = 1
    config = IntrusionRecoveryPomdpConfig(
        eta=eta, p_a=p_a, p_c_1=p_c_1, p_c_2=p_c_2, p_u=p_u, BTR=BTR, negate_costs=negate_costs, seed=seed,
        discount_factor=discount_factor, states=IntrusionRecoveryPomdpUtil.state_space(),
        actions=IntrusionRecoveryPomdpUtil.action_space(),
        observations=IntrusionRecoveryPomdpUtil.observation_space(num_observations=num_observations),
        cost_tensor=IntrusionRecoveryPomdpUtil.cost_tensor(eta=eta, states=IntrusionRecoveryPomdpUtil.state_space(),
                                                           actions=IntrusionRecoveryPomdpUtil.action_space()),
        observation_tensor=IntrusionRecoveryPomdpUtil.observation_tensor(
            states=IntrusionRecoveryPomdpUtil.state_space(),
            observations=IntrusionRecoveryPomdpUtil.observation_space(num_observations=num_observations)),
        transition_tensor=IntrusionRecoveryPomdpUtil.transition_tensor(
            states=IntrusionRecoveryPomdpUtil.state_space(), actions=IntrusionRecoveryPomdpUtil.action_space(),
            p_c_2=p_c_2, p_c_1=p_c_1, p_u=p_u, p_a=p_a),
        b1=IntrusionRecoveryPomdpUtil.initial_belief(p_a=p_a), T=BTR
    )
    env = IntrusionRecoveryPomdpEnv(config = config)


    # --- Define BO input configuration ---

    # Random seed
    num_thresholds =  BTR
    random.seed(config.seed)
    np.random.seed(config.seed)

    # input space
    parameters = []
    for i in range(num_thresholds):
        parameters.append(ContinuousParameter(name=f"Belief threshold {i}", min_value=0, max_value=1))
    input_space = ParameterSpace(parameters=parameters)

    # Objective function
    objective_function = lambda x: np.array([[evaluate_threshold(alphas=x, env=env, n_samples=100)]])

    # Cost function and evaluation budget
    cost_function = lambda x: 1
    evaluation_budget = 400
    lengthscale_rbf_kernel = 1.
    variance_rbf_kernel = 1.
    obs_likelihood_variance = 1.
    beta = 10000

    # Initial data samples
    input_space_dim = num_thresholds
    size_init = 5

    X_init = []
    for i in range(num_thresholds):
        X_init.append(np.linspace(input_space.parameters[0].min, input_space.parameters[0].max, num=size_init))
    X_init = np.array(X_init)
    X_init = X_init.reshape((size_init, num_thresholds))
    Y_init = np.array(list(map(lambda x: objective_function(x), X_init))).reshape((len(X_init), 1))

    # GP and kernels configuration
    kernel_config = RBFKernelConfig(lengthscale_rbf_kernel=lengthscale_rbf_kernel,
                                    variance_rbf_kernel=variance_rbf_kernel)
    gp_config = GPConfig(kernel_config=kernel_config, obs_likelihood_variance=obs_likelihood_variance)

    # Acquisition function config
    acquisition_function_type = AcquisitionFunctionType.NEGATIVE_LOWER_CONFIDENCE_BOUND
    acquisition_optimizer_type = AcquisitionOptimizerType.GRADIENT

    # Complete BO config
    date_str = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    log_file_name = f"{date_str}_bo.log"
    bo_config = BOConfig(
        objective_function=objective_function, cost_function=cost_function, X_init=X_init, Y_init=Y_init,
        input_space=input_space, evaluation_budget=evaluation_budget, gp_config=gp_config,
        acquisition_function_type=acquisition_function_type, acquisition_optimizer_type=acquisition_optimizer_type,
        log_level=logging.INFO, log_file=log_file_name, objective_type=ObjectiveType.MIN, beta=beta)

    # --- Run BO ---
    results = BO.bo(bo_config=bo_config)

    # # --- Plotting ---

    # Generate some data from the objective function to compare
    num_samples_from_objective = 100
    alphas = []
    for i in range(num_thresholds):
        alphas.append(np.linspace(input_space.parameters[0].min, input_space.parameters[0].max, num=num_samples_from_objective))
    alphas = np.array(alphas).reshape(num_samples_from_objective, input_space_dim)
    costs = list(map(lambda x: objective_function(x), alphas))
    results.Y_objective = np.array(costs).reshape(num_samples_from_objective, 1)
    results.X_objective = alphas
    results.y_opt = np.min(results.Y_objective)

    # Save the results
    results.to_json_file(f"{date_str}_bo_results.json")

    # Plot the results and compare with the true objective function
    plot_bo_results_and_gp(bo_results=results, file_name=f"{date_str}_bo_results", markevery=10)