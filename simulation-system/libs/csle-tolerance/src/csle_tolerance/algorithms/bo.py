import numpy as np
import time
from csle_tolerance.dao.bo.bo_config import BOConfig
from csle_tolerance.dao.bo.bo_results import BOResults
from csle_tolerance.logging.logger import Logger
from csle_tolerance.dao.bo.optimization.objective_type import ObjectiveType


class BO:
    """
    Class containing functions related to the Bayesian Optimization algorithm.
    The implementation is based on (Garnett, 2023).
    """

    @staticmethod
    def bo(bo_config: BOConfig) -> BOResults:
        """
        The Bayesian optimization algorithm, implementation based on pseudocode in (Garnett, 2023).

        :param bo_config:the configuration of the execution of the algorithms
        :return: the results of the execution
        """

        # Setup logging
        logger = Logger.get_logger(log_file=bo_config.log_file, log_level=bo_config.log_level)

        # Initialize execution state
        logger.info(f"Starting BO execution, log file: {bo_config.log_file}, log level: {bo_config.log_level}")
        results = BOResults(remaining_budget=bo_config.evaluation_budget)

        # If the initial data is empty, pick the first point randomly so that we can initialize surrogate models
        if len(bo_config.X_init) == 0:
            x = []
            for i in range(len(bo_config.input_space.parameters)):
                level = np.random.uniform(bo_config.input_space.parameters[i].min,
                                          bo_config.input_space.parameters[i].max)
                x.append(level)
            bo_config.X_init = np.array([x])
            bo_config.Y_init = np.array(bo_config.objective_function(bo_config.X_init))

            # Compute cost of the initial point
            cost = bo_config.cost_function(bo_config.X_init[0])
            results.cumulative_cost += cost
            results.C = np.array([[results.cumulative_cost]])
        else:
            results.C = np.array([[0]])
            results.cumulative_cost = 0

        # Initialize the dataset
        results.X = bo_config.X_init.copy()
        results.Y = bo_config.Y_init.copy()

        # Initialize the best point and initial cost
        min_index = np.argmin(results.Y)
        results.Y_best = np.array([results.Y[min_index]])
        results.X_best = np.array([results.X[min_index]])

        # Fit the GP surrogate model based on the initial data
        results.surrogate_model = bo_config.gp_config.create_gp(X=bo_config.X_init, Y=bo_config.Y_init,
                                                              input_dim=len(bo_config.input_space.parameters))

        # Define the acquisition function
        results.acquisition = bo_config.get_acquisition_function(surrogate_model=results.surrogate_model)

        # Define the acquisition function optimizer
        results.acquisition_optimizer = bo_config.get_acquisition_optimizer()

        while results.remaining_budget > 0:

            # Update GP model
            results.surrogate_model.optimize()

            # Optimize acquisition function to get next evaluation point
            x, _ = results.acquisition_optimizer.optimize(results.acquisition)

            # x[0][0] = round(x[0][0], 2)

            # Evaluate the objective function at the new point
            y = bo_config.objective_function(x)

            # Append the new data point to the dataset
            results.X = np.append(results.X, x, axis=0)
            results.Y = np.append(results.Y, y, axis=0)

            logger.info(f"Iteration: {results.iteration}, remaining budget: {results.remaining_budget}, "
                        f"current best point: ({results.X_best[-1]}, {results.Y_best[-1]}), current point: ({x}, {y})")
            # logger.info(f"Iteration: {results.iteration}, remaining budget: {results.remaining_budget}, "
            #             f"current best value: {results.Y_best[-1]}")

            # Update the GP surrogate model with the new data
            results.surrogate_model.set_data(results.X, results.Y)

            # Compute cost
            cost = bo_config.cost_function(x)
            results.cumulative_cost += cost
            results.C = np.append(results.C, np.array([[results.cumulative_cost]]), axis=0)

            # Get current optimum
            min_index_y = np.argmin(results.Y)
            results.Y_best = np.append(results.Y_best, [results.Y[min_index_y]], axis=0)
            results.X_best = np.append(results.X_best, [results.X[min_index_y]], axis=0)

            # Move to next iteration
            results.iteration += 1
            results.remaining_budget -= cost

        results.total_time = time.time() - results.start_time
        logger.info(f"BO execution complete, total time: {round(results.total_time,2)}s")
        return results
