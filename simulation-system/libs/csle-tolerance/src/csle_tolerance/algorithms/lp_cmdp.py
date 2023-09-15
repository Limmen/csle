from typing import List, Union, Tuple
import pulp
import numpy as np


class LpCmdp:
    """
    Class implementing the LP for solving a CMDP
    """

    @staticmethod
    def lp(actions: List[int], states: List[int], cost_tensor: Union[List[float], List[List[float]]],
           transition_tensor: List[List[List[float]]],
           constraint_cost_tensors: List[Union[List[float], List[List[float]]]],
           constraint_cost_thresholds: List[float]) \
            -> Tuple[str, List[List[float]], List[List[float]], List[float], float]:
        """
        Linear program for solving a CMDP (see Altman '99 for details)

        :param actions: the action space
        :param states: the state space
        :param cost_tensor: the cost tensor
        :param transition_tensor: the transition tensor
        :param constraint_cost_tensors: the constraint cost tensors
        :param constraint_cost_thresholds: the constraint cost thresholds
        :return: the solution status, the optimal occupancy measure, the optimal strategy, the expeted constraint cost,
                 the objective value
        """
        problem = pulp.LpProblem("AvgCostMdp", pulp.LpMinimize)

        # Decision variables, state-action occupancy measures
        occupancy_measures = []
        for s in states:
            occupancy_measures_s = []
            for a in actions:
                s_a_occupancy = pulp.LpVariable(f"occupancy_{s}_{a}", lowBound=0, upBound=1, cat=pulp.LpContinuous)
                occupancy_measures_s.append(s_a_occupancy)
            occupancy_measures.append(occupancy_measures_s)

        # The non-zero constraints
        for s in states:
            for a in actions:
                problem += occupancy_measures[s][a] >= 0, f"NonZeroConstraint_{s}_{a}"

        # The probability constraints
        occupancy_measures_sum = 0
        for s in states:
            for a in actions:
                occupancy_measures_sum += occupancy_measures[s][a]
        problem += occupancy_measures_sum == 1, f"StochasticConstraint"

        # The transition constraints
        for s_prime in states:
            rho_s_prime_a_sum = 0
            for a in actions:
                rho_s_prime_a_sum += occupancy_measures[s_prime][a]

            transition_sum = 0
            for s in states:
                for a in actions:
                    transition_sum += occupancy_measures[s][a] * transition_tensor[a][s][s_prime]

            problem += rho_s_prime_a_sum == transition_sum, f"TransitionConstraint_{s_prime}"

        # The cost constraints
        for i in range(len(constraint_cost_tensors)):
            expected_constraint_cost = 0.0
            for s in states:
                for a in actions:
                    if (isinstance(constraint_cost_tensors[i][a], list) or
                            isinstance(constraint_cost_tensors[i][a], np.ndarray)):
                        expected_constraint_cost += occupancy_measures[s][a] * constraint_cost_tensors[i][a][s]
                    else:
                        expected_constraint_cost += occupancy_measures[s][a] * constraint_cost_tensors[i][s]
            threshold = constraint_cost_thresholds[i]
            problem += expected_constraint_cost >= threshold, f"ExpectedCostConstraint_{i}"

        # Objective function
        avg_cost = 0
        for s in states:
            for a in actions:
                if isinstance(cost_tensor[a], list):
                    avg_cost += cost_tensor[a][s] * occupancy_measures[s][a]
                else:
                    avg_cost += cost_tensor[s] * occupancy_measures[s][a]
        problem += avg_cost, "Average cost"

        # Solve
        problem.solve(pulp.PULP_CBC_CMD(msg=0))

        # Extract solution
        optimal_occupancy_measures = []
        for i in range(len(occupancy_measures)):
            optimal_occupanct_measures_s = []
            for j in range(len(occupancy_measures[i])):
                optimal_occupanct_measures_s.append(occupancy_measures[i][j].varValue)
            optimal_occupancy_measures.append(optimal_occupanct_measures_s)
        optimal_occupancy_measures = optimal_occupancy_measures
        optimal_strategy = []
        for s in states:
            optimal_strategy_s = []
            for a in actions:
                normalizing_sum = 0
                for s_prime in states:
                    normalizing_sum += optimal_occupancy_measures[s_prime][a]
                if normalizing_sum != 0:
                    action_prob = optimal_occupancy_measures[s][a] / normalizing_sum
                else:
                    action_prob = 0
                optimal_strategy_s.append(action_prob)
            optimal_strategy.append(optimal_strategy_s)
        expected_constraint_costs = []
        for i in range(len(constraint_cost_tensors)):
            expected_constraint_cost = 0.0
            for s in states:
                for a in actions:
                    if (isinstance(constraint_cost_tensors[i][a], list) or
                            isinstance(constraint_cost_tensors[i][a], np.ndarray)):
                        expected_constraint_cost += optimal_occupancy_measures[s][a] * constraint_cost_tensors[i][a][s]
                    else:
                        expected_constraint_cost += optimal_occupancy_measures[s][a] * constraint_cost_tensors[i][s]
            expected_constraint_costs.append(expected_constraint_cost)
        return (pulp.LpStatus[problem.status],
                optimal_occupancy_measures, optimal_strategy, expected_constraint_costs, problem.objective.value())
