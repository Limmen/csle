from csle_tolerance.dao.intrusion_recovery_game_config import (
    IntrusionRecoveryGameConfig,
)
from csle_tolerance.util.intrusion_recovery_pomdp_util import IntrusionRecoveryPomdpUtil
import pytest_mock


class TestIntrusionRecoveryGameConfigSuite:
    """
    Test suite for intrusion_recovery_game_config.py
    """

    def test__init__(self) -> None:
        """
        Tests the function of initializing the DTO
        """
        dto = IntrusionRecoveryGameConfig(
            eta=0.5,
            p_a=0.8,
            p_c_1=0.1,
            BTR=10,
            negate_costs=True,
            seed=123,
            discount_factor=0.9,
            states=[0, 1, 2],
            actions=[0, 1],
            observations=[0, 1],
            cost_tensor=[[1, 2], [3, 4]],
            observation_tensor=[[1, 2], [3, 4]],
            transition_tensor=[[[[0.1, 0.2], [0.3, 0.4]], [[0.5, 0.6], [0.7, 0.8]]]],
            b1=[0.1, 0.9],
            T=100,
            simulation_env_name="sim_env",
            gym_env_name="gym_env",
            max_horizon=1000,
        )
        assert dto.eta == 0.5
        assert dto.p_a == 0.8
        assert dto.p_c_1 == 0.1
        assert dto.BTR == 10
        assert dto.negate_costs is True
        assert dto.seed == 123
        assert dto.discount_factor == 0.9
        assert dto.states == [0, 1, 2]
        assert dto.actions == [0, 1]
        assert dto.observations == [0, 1]
        assert dto.cost_tensor == [[1, 2], [3, 4]]
        assert dto.observation_tensor == [[1, 2], [3, 4]]
        assert dto.transition_tensor == [
            [[[0.1, 0.2], [0.3, 0.4]], [[0.5, 0.6], [0.7, 0.8]]]
        ]
        assert dto.b1 == [0.1, 0.9]
        assert dto.T == 100
        assert dto.simulation_env_name == "sim_env"
        assert dto.gym_env_name == "gym_env"
        assert dto.max_horizon == 1000

    def test__str__(self) -> None:
        """
        Tests the function of returning a string representation of the DTO
        """
        dto = IntrusionRecoveryGameConfig(
            eta=0.5,
            p_a=0.8,
            p_c_1=0.1,
            BTR=10,
            negate_costs=True,
            seed=123,
            discount_factor=0.9,
            states=[0, 1, 2],
            actions=[0, 1],
            observations=[0, 1],
            cost_tensor=[[1, 2], [3, 4]],
            observation_tensor=[[1, 2], [3, 4]],
            transition_tensor=[[[[0.1, 0.2], [0.3, 0.4]], [[0.5, 0.6], [0.7, 0.8]]]],
            b1=[0.1, 0.9],
            T=100,
            simulation_env_name="sim_env",
            gym_env_name="gym_env",
            max_horizon=1000,
        )
        expected = (
            "eta: 0.5, p_a: 0.8, p_c_1: 0.1, BTR: 10, negate_costs: True, seed: 123, "
            "discount_factor: 0.9, states: [0, 1, 2], actions: [0, 1], observations: [[1, 2], [3, 4]], "
            "cost_tensor: [[1, 2], [3, 4]], observation_tensor: [[1, 2], [3, 4]], "
            "transition_tensor: [[[[0.1, 0.2], [0.3, 0.4]], [[0.5, 0.6], [0.7, 0.8]]]], b1:[0.1, 0.9], "
            "T: 100, simulation_env_name: sim_env, gym_env_name: gym_env, max_horizon: 1000"
        )
        assert dto.__str__() == expected

    def test_from_dict(self) -> None:
        """
        Tests the function of converting a dict representation to an instance
        """
        dto_dict = {
            "eta": 0.5,
            "p_a": 0.8,
            "p_c_1": 0.1,
            "BTR": 10,
            "negate_costs": True,
            "seed": 123,
            "discount_factor": 0.9,
            "states": [0, 1, 2],
            "actions": [0, 1],
            "observations": [0, 1],
            "cost_tensor": [[1, 2], [3, 4]],
            "observation_tensor": [[1, 2], [3, 4]],
            "transition_tensor": [[[[0.1, 0.2], [0.3, 0.4]], [[0.5, 0.6], [0.7, 0.8]]]],
            "b1": [0.1, 0.9],
            "T": 100,
            "simulation_env_name": "sim_env",
            "gym_env_name": "gym_env",
        }
        dto = IntrusionRecoveryGameConfig.from_dict(dto_dict)
        assert dto.eta == 0.5
        assert dto.p_a == 0.8
        assert dto.p_c_1 == 0.1
        assert dto.BTR == 10
        assert dto.negate_costs is True
        assert dto.seed == 123
        assert dto.discount_factor == 0.9
        assert dto.states == [0, 1, 2]
        assert dto.actions == [0, 1]
        assert dto.observations == [0, 1]
        assert dto.cost_tensor == [[1, 2], [3, 4]]
        assert dto.observation_tensor == [[1, 2], [3, 4]]
        assert dto.transition_tensor == [
            [[[0.1, 0.2], [0.3, 0.4]], [[0.5, 0.6], [0.7, 0.8]]]
        ]
        assert dto.b1 == [0.1, 0.9]
        assert dto.T == 100
        assert dto.simulation_env_name == "sim_env"
        assert dto.gym_env_name == "gym_env"

    def test_to_dict(self) -> None:
        """
        Tests the function of getting a dict representation of the object
        """
        dto = IntrusionRecoveryGameConfig(
            eta=0.5,
            p_a=0.8,
            p_c_1=0.1,
            BTR=10,
            negate_costs=True,
            seed=123,
            discount_factor=0.9,
            states=[0, 1, 2],
            actions=[0, 1],
            observations=[0, 1],
            cost_tensor=[[1, 2], [3, 4]],
            observation_tensor=[[1, 2], [3, 4]],
            transition_tensor=[[[[0.1, 0.2], [0.3, 0.4]], [[0.5, 0.6], [0.7, 0.8]]]],
            b1=[0.1, 0.9],
            T=100,
            simulation_env_name="sim_env",
            gym_env_name="gym_env",
        )
        expected = {
            "eta": 0.5,
            "p_a": 0.8,
            "p_c_1": 0.1,
            "BTR": 10,
            "negate_costs": True,
            "seed": 123,
            "discount_factor": 0.9,
            "states": [0, 1, 2],
            "actions": [0, 1],
            "observations": [0, 1],
            "cost_tensor": [[1, 2], [3, 4]],
            "observation_tensor": [[1, 2], [3, 4]],
            "transition_tensor": [[[[0.1, 0.2], [0.3, 0.4]], [[0.5, 0.6], [0.7, 0.8]]]],
            "b1": [0.1, 0.9],
            "T": 100,
            "simulation_env_name": "sim_env",
            "gym_env_name": "gym_env",
        }
        assert dto.to_dict() == expected

    def test_from_json_file(self, mocker: pytest_mock.MockFixture) -> None:
        """
        tests the function of reading a json file and converting it to a DTO
        """
        eta = 2
        p_a = 0.05
        p_c_1 = 0.01
        BTR = 100
        negate_costs = False
        discount_factor = 1 - p_c_1
        num_observations = 100
        simulation_name = "csle-tolerance-intrusion-recovery-pomdp-defender-001"
        cost_tensor = IntrusionRecoveryPomdpUtil.cost_tensor(
            eta=eta,
            states=IntrusionRecoveryPomdpUtil.state_space(),
            actions=IntrusionRecoveryPomdpUtil.action_space(),
            negate=negate_costs,
        )
        observation_tensor = IntrusionRecoveryPomdpUtil.observation_tensor(
            states=IntrusionRecoveryPomdpUtil.state_space(),
            observations=IntrusionRecoveryPomdpUtil.observation_space(
                num_observations=num_observations
            ),
        )
        transition_tensor = IntrusionRecoveryPomdpUtil.transition_tensor_game(
            states=IntrusionRecoveryPomdpUtil.state_space(),
            defender_actions=IntrusionRecoveryPomdpUtil.action_space(),
            attacker_actions=IntrusionRecoveryPomdpUtil.action_space(),
            p_a=p_a,
            p_c_1=p_c_1,
        )
        config = IntrusionRecoveryGameConfig(
            eta=eta,
            p_a=p_a,
            p_c_1=p_c_1,
            BTR=100,
            negate_costs=negate_costs,
            seed=999,
            discount_factor=discount_factor,
            states=IntrusionRecoveryPomdpUtil.state_space(),
            actions=IntrusionRecoveryPomdpUtil.action_space(),
            observations=IntrusionRecoveryPomdpUtil.observation_space(
                num_observations=num_observations
            ),
            cost_tensor=cost_tensor,
            observation_tensor=observation_tensor,
            transition_tensor=transition_tensor,
            b1=IntrusionRecoveryPomdpUtil.initial_belief(p_a=p_a),
            T=int(BTR),
            simulation_env_name=simulation_name,
            gym_env_name="csle-tolerance-intrusion-recovery-pomdp-v1",
        )
        mocker.patch(
            "io.open", side_effect=mocker.mock_open(read_data=config.to_json_str())
        )
        dto = IntrusionRecoveryGameConfig.from_json_file("path")
        assert dto.eta == 2
        assert dto.p_a == 0.05
        assert dto.p_c_1 == 0.01
        assert dto.BTR == 100
        assert dto.negate_costs is False
        assert dto.seed == 999
        assert dto.discount_factor == 1 - p_c_1