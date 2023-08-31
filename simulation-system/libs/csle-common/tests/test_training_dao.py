from csle_common.dao.training.alpha_vectors_policy import AlphaVectorsPolicy
from csle_common.dao.simulation_config.action import Action
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.simulation_config.state import State
from csle_common.dao.simulation_config.state_type import StateType
from csle_common.dao.training.agent_type import AgentType


class TestTrainingDaoSuite:
    """
    Test suite for training data access objects (DAOs)
    """

    def test_alpha_vectors_policy(self) -> None:
        """
        Tests creation and dict conversion of the AlphaVectorsPolicy DAO

        :return: None
        """

        action = Action(id=1, descr="test")
        states = State(id=1, name="test", descr="test1", state_type=StateType.TERMINAL)
        alpha_vectors_policy = AlphaVectorsPolicy(
            player_type=PlayerType.DEFENDER, actions=[action], alpha_vectors=[1, 2], transition_tensor=[1, 3],
            reward_tensor=[5, 6], states=[states], agent_type=AgentType.PPO, simulation_name="test", avg_R=0.3)

        assert isinstance(alpha_vectors_policy.to_dict(), dict)
        assert isinstance(AlphaVectorsPolicy.from_dict(alpha_vectors_policy.to_dict()),
                          AlphaVectorsPolicy)
        assert (AlphaVectorsPolicy.from_dict(alpha_vectors_policy.to_dict()).to_dict() ==
                alpha_vectors_policy.to_dict())
        assert (AlphaVectorsPolicy.from_dict(alpha_vectors_policy.to_dict()) ==
                alpha_vectors_policy)
