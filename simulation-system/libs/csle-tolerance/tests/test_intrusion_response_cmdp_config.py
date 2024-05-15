from csle_tolerance.dao.intrusion_response_cmdp_config import (
    IntrusionResponseCmdpConfig,
)
import pytest_mock


class TestIntrusionResponseCmdpConfigSuite:
    """
    Test suite for intrusion_response_cmdp_config.py
    """

    def test__init__(self) -> None:
        """
        Tests the function of initializing the DTO
        """
        p_a = 0.1
        p_c = 0.2
        p_u = 0.3
        s_max = 10
        transition_tensor = [[[0.1, 0.2], [0.3, 0.4]], [[0.5, 0.6], [0.7, 0.8]]]
        cost_tensor = [0.5, 0.6]
        negate_costs = True
        seed = 123
        states = [0, 1]
        actions = [0, 1]
        initial_state = 0
        constraint_cost_tensor = [0.7, 0.8]
        f = 5
        epsilon_a = 0.9
        simulation_env_name = "SimulationEnv"
        gym_env_name = "GymEnv"
        discount_factor = 0.95
        dto = IntrusionResponseCmdpConfig(
            p_a,
            p_c,
            p_u,
            s_max,
            transition_tensor,
            cost_tensor,
            negate_costs,
            seed,
            states,
            actions,
            initial_state,
            constraint_cost_tensor,
            f,
            epsilon_a,
            simulation_env_name,
            gym_env_name,
            discount_factor,
        )
        assert dto.p_a == p_a
        assert dto.p_c == p_c
        assert dto.p_u == p_u
        assert dto.s_max == s_max
        assert dto.transition_tensor == transition_tensor
        assert dto.cost_tensor == cost_tensor
        assert dto.negate_costs == negate_costs
        assert dto.seed == seed
        assert dto.states == states
        assert dto.actions == actions
        assert dto.initial_state == initial_state
        assert dto.constraint_cost_tensor == constraint_cost_tensor
        assert dto.f == f
        assert dto.epsilon_a == epsilon_a
        assert dto.simulation_env_name == simulation_env_name
        assert dto.gym_env_name == gym_env_name
        assert dto.discount_factor == discount_factor

    def test__str__(self) -> None:
        """
        Tests the function of returning a string representation of the DTO
        """
        p_a = 0.1
        p_c = 0.2
        p_u = 0.3
        s_max = 10
        transition_tensor = [[[0.1, 0.2], [0.3, 0.4]], [[0.5, 0.6], [0.7, 0.8]]]
        cost_tensor = [0.5, 0.6]
        negate_costs = True
        seed = 123
        states = [0, 1]
        actions = [0, 1]
        initial_state = 0
        constraint_cost_tensor = [0.7, 0.8]
        f = 5
        epsilon_a = 0.9
        simulation_env_name = "SimulationEnv"
        gym_env_name = "GymEnv"
        discount_factor = 0.95
        dto = IntrusionResponseCmdpConfig(
            p_a,
            p_c,
            p_u,
            s_max,
            transition_tensor,
            cost_tensor,
            negate_costs,
            seed,
            states,
            actions,
            initial_state,
            constraint_cost_tensor,
            f,
            epsilon_a,
            simulation_env_name,
            gym_env_name,
            discount_factor,
        )
        expected = (
            f"p_a: {p_a}, p_c: {p_c}, p_u: {p_u}, s_max: {s_max}, "
            f"transition_tensor: {transition_tensor}, cost_tensor: {cost_tensor}, seed: {seed}, "
            f"negate_costs: {negate_costs}, states: {states}, actions: {actions}, "
            f"initial state: {initial_state}, constraint_cost_tensor: {constraint_cost_tensor}, "
            f"f: {f}, epsilon_a: {epsilon_a}, simulation_env_name: {simulation_env_name}, "
            f"gym_env_name: {gym_env_name}, discount_factor: {discount_factor}"
        )
        assert dto.__str__() == expected

    def test_from_dict(self) -> None:
        """
        Tests the function of converting a dict representation to an instance
        """
        dto_dict = {
            "p_a": 0.1,
            "p_c": 0.2,
            "p_u": 0.3,
            "s_max": 10,
            "transition_tensor": [[[0.1, 0.2], [0.3, 0.4]], [[0.5, 0.6], [0.7, 0.8]]],
            "cost_tensor": [0.5, 0.6],
            "negate_costs": True,
            "seed": 123,
            "states": [0, 1],
            "actions": [0, 1],
            "initial_state": 0,
            "constraint_cost_tensor": [0.7, 0.8],
            "f": 5,
            "epsilon_a": 0.9,
            "simulation_env_name": "SimulationEnv",
            "gym_env_name": "GymEnv",
            "discount_factor": 0.95,
        }
        dto = IntrusionResponseCmdpConfig.from_dict(dto_dict)
        assert dto.p_a == dto_dict["p_a"]
        assert dto.p_c == dto_dict["p_c"]
        assert dto.p_u == dto_dict["p_u"]
        assert dto.s_max == dto_dict["s_max"]
        assert dto.transition_tensor == dto_dict["transition_tensor"]
        assert dto.cost_tensor == dto_dict["cost_tensor"]
        assert dto.negate_costs == dto_dict["negate_costs"]
        assert dto.seed == dto_dict["seed"]
        assert dto.states == dto_dict["states"]
        assert dto.actions == dto_dict["actions"]
        assert dto.initial_state == dto_dict["initial_state"]
        assert dto.constraint_cost_tensor == dto_dict["constraint_cost_tensor"]
        assert dto.f == dto_dict["f"]
        assert dto.epsilon_a == dto_dict["epsilon_a"]
        assert dto.simulation_env_name == dto_dict["simulation_env_name"]
        assert dto.gym_env_name == dto_dict["gym_env_name"]
        assert dto.discount_factor == dto_dict["discount_factor"]

    def test_to_dict(self) -> None:
        """
        Tests the function of getting a dict representation of the object
        """
        p_a = 0.1
        p_c = 0.2
        p_u = 0.3
        s_max = 10
        transition_tensor = [[[0.1, 0.2], [0.3, 0.4]], [[0.5, 0.6], [0.7, 0.8]]]
        cost_tensor = [0.5, 0.6]
        negate_costs = True
        seed = 123
        states = [0, 1]
        actions = [0, 1]
        initial_state = 0
        constraint_cost_tensor = [0.7, 0.8]
        f = 5
        epsilon_a = 0.9
        simulation_env_name = "SimulationEnv"
        gym_env_name = "GymEnv"
        discount_factor = 0.95
        dto = IntrusionResponseCmdpConfig(
            p_a,
            p_c,
            p_u,
            s_max,
            transition_tensor,
            cost_tensor,
            negate_costs,
            seed,
            states,
            actions,
            initial_state,
            constraint_cost_tensor,
            f,
            epsilon_a,
            simulation_env_name,
            gym_env_name,
            discount_factor,
        )
        expected = {
            "p_a": 0.1,
            "p_c": 0.2,
            "p_u": 0.3,
            "s_max": 10,
            "transition_tensor": [[[0.1, 0.2], [0.3, 0.4]], [[0.5, 0.6], [0.7, 0.8]]],
            "cost_tensor": [0.5, 0.6],
            "negate_costs": True,
            "seed": 123,
            "states": [0, 1],
            "actions": [0, 1],
            "initial_state": 0,
            "constraint_cost_tensor": [0.7, 0.8],
            "f": 5,
            "epsilon_a": 0.9,
            "simulation_env_name": "SimulationEnv",
            "gym_env_name": "GymEnv",
            "discount_factor": 0.95,
        }
        assert dto.to_dict() == expected

    def test_from_json_file(self, mocker: pytest_mock.MockFixture) -> None:
        """
        tests the function of reading a json file and converting it to a DTO
        """
        p_a = 0.1
        p_c = 0.2
        p_u = 0.3
        s_max = 10
        transition_tensor = [[[0.1, 0.2], [0.3, 0.4]], [[0.5, 0.6], [0.7, 0.8]]]
        cost_tensor = [0.5, 0.6]
        negate_costs = True
        seed = 123
        states = [0, 1]
        actions = [0, 1]
        initial_state = 0
        constraint_cost_tensor = [0.7, 0.8]
        f = 5
        epsilon_a = 0.9
        simulation_env_name = "SimulationEnv"
        gym_env_name = "GymEnv"
        discount_factor = 0.95
        config = IntrusionResponseCmdpConfig(
            p_a,
            p_c,
            p_u,
            s_max,
            transition_tensor,
            cost_tensor,
            negate_costs,
            seed,
            states,
            actions,
            initial_state,
            constraint_cost_tensor,
            f,
            epsilon_a,
            simulation_env_name,
            gym_env_name,
            discount_factor,
        )
        mocker.patch(
            "io.open", side_effect=mocker.mock_open(read_data=config.to_json_str())
        )
        dto = IntrusionResponseCmdpConfig.from_json_file("path")
        assert dto.p_a == p_a
        assert dto.p_c == p_c
        assert dto.p_u == p_u
        assert dto.s_max == s_max
        assert dto.transition_tensor == transition_tensor
        assert dto.cost_tensor == cost_tensor
        assert dto.negate_costs == negate_costs
        assert dto.seed == seed
        assert dto.states == states
        assert dto.actions == actions
        assert dto.initial_state == initial_state
        assert dto.constraint_cost_tensor == constraint_cost_tensor
        assert dto.f == f
        assert dto.epsilon_a == epsilon_a
        assert dto.simulation_env_name == simulation_env_name
        assert dto.gym_env_name == gym_env_name
        assert dto.discount_factor == discount_factor
