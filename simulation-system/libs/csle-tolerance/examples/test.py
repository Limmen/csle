import logging
import datetime
import numpy as np
import random
from emukit.test_functions import forrester_function
from csle_tolerance.dao.bo.bo_config import BOConfig
from csle_tolerance.dao.bo.gp.gp_config import GPConfig
from csle_tolerance.dao.bo.kernel.rbf_kernel_config import RBFKernelConfig
from csle_tolerance.dao.bo.acquisition.acquisition_function_type import AcquisitionFunctionType
from csle_tolerance.dao.bo.acquisition.acquisition_optimizer_type import AcquisitionOptimizerType
from csle_tolerance.algorithms.bo import BO
from csle_tolerance.dao.bo.optimization.objective_type import ObjectiveType
from csle_tolerance.plotting.plot_bo_forrester_results import plot_bo_results_and_gp

# Runs BO

if __name__ == '__main__':

    # --- Define input configuration ---

    # Random seed
    seed = 3151
    random.seed(seed)
    np.random.seed(seed)

    # Objective and cost functions, and evaluation budget
    objective_function, input_space = forrester_function()
    cost_function = lambda x: 1
    evaluation_budget = 100
    lengthscale_rbf_kernel = 1.
    variance_rbf_kernel = 1.
    obs_likelihood_variance = 1.

    # Initial data samples
    input_space_dim = 1
    size_init = 2
    X_init = np.linspace(input_space.parameters[0].min, input_space.parameters[0].max, num=size_init).reshape(
        size_init, input_space_dim)
    Y_init = np.array(list(map(lambda x: objective_function(x), X_init))).reshape(len(X_init), input_space_dim)

    # GP and kernels configuration
    kernel_config = RBFKernelConfig(lengthscale_rbf_kernel=lengthscale_rbf_kernel,
                                    variance_rbf_kernel=variance_rbf_kernel)
    gp_config = GPConfig(kernel_config=kernel_config, obs_likelihood_variance=obs_likelihood_variance)

    # Acquisition function config
    acquisition_function_type = AcquisitionFunctionType.EXPECTED_IMPROVEMENT
    acquisition_optimizer_type = AcquisitionOptimizerType.GRADIENT

    # Complete BO config
    date_str = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    log_file_name = f"{date_str}_bo.log"
    bo_config = BOConfig(
        objective_function=objective_function, cost_function=cost_function, X_init=X_init, Y_init=Y_init,
        input_space=input_space, evaluation_budget=evaluation_budget, gp_config=gp_config,
        acquisition_function_type=acquisition_function_type, acquisition_optimizer_type=acquisition_optimizer_type,
        log_level=logging.INFO, log_file=log_file_name, objective_type=ObjectiveType.MIN)

    # --- Run BO ---
    results = BO.bo(bo_config=bo_config)

    # # --- Plotting ---

    # Generate some data from the objective function to compare
    num_samples_from_objective = 200
    results.X_objective = np.linspace(input_space.parameters[0].min, input_space.parameters[0].max,
                                      num_samples_from_objective).reshape(
        num_samples_from_objective, input_space_dim)
    results.Y_objective = objective_function(results.X_objective)
    results.y_opt = np.min(results.Y_objective)

    # Save the results
    results.to_json_file(f"{date_str}_bo_results.json")

    # Plot the results and compare with the true objective function
    plot_bo_results_and_gp(bo_results=results, file_name=f"{date_str}_bo_results")
