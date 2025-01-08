import pytest
import numpy as np
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil
from csle_common.dao.training.multi_threshold_stopping_policy import MultiThresholdStoppingPolicy
from csle_common.dao.training.random_policy import RandomPolicy
from csle_common.dao.simulation_config.state import State
from csle_common.dao.simulation_config.state_type import StateType
from csle_common.dao.simulation_config.action import Action
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam


@pytest.fixture
def example_stopping_game_util() -> StoppingGameUtil:
    """
    Fixture that returns an example StoppingGameUtil object

    :return: an example StoppingGameUtil object
    """
    return StoppingGameUtil()


@pytest.fixture
def example_stopping_game_config(example_stopping_game_util: StoppingGameUtil) -> StoppingGameConfig:
    """
    Fixture that returns an example StoppingGameConfig object

    :return: an example StoppingGameConfig object
    """
    return StoppingGameConfig(env_name="test_env", T=example_stopping_game_util.transition_tensor(L=1),
                              O=example_stopping_game_util.observation_space(5),
                              Z=example_stopping_game_util.observation_tensor(5),
                              R=example_stopping_game_util.reward_tensor(R_SLA=1, R_INT=3, R_COST=4, L=1, R_ST=4),
                              S=example_stopping_game_util.state_space(),
                              A1=example_stopping_game_util.defender_actions(),
                              A2=example_stopping_game_util.attacker_actions(),
                              L=1, R_INT=1, R_COST=3, R_SLA=1, R_ST=1,
                              b1=example_stopping_game_util.b1(),
                              save_dir="test_dir", checkpoint_traces_freq=1)


@pytest.fixture
def example_state() -> State:
    """
    Fixture that returns an example State object

    :return: an example State object
    """
    return State(id=1, name="test", descr="test1", state_type=StateType.TERMINAL)


@pytest.fixture
def example_action() -> Action:
    """
    Fixture that returns an example Action object

    :return: an example Action object
    """
    return Action(id=1, descr="test")


@pytest.fixture
def example_experiment_config(example_hparam: HParam) -> ExperimentConfig:
    """
    Fixture that returns an example ExperimentConfig object

    :param example_hparam: an example HParam
    :return: an example ExperimentConfig object
    """
    hparams = dict()
    hparams["test"] = example_hparam
    return ExperimentConfig(output_dir="test/test", title="test1", random_seeds=[1],
                            agent_type=AgentType.PPO, hparams=hparams, log_every=10,
                            player_type=PlayerType.DEFENDER, player_idx=2)


@pytest.fixture
def example_hparam() -> HParam:
    """
    Fixture that returns an example HParam object

    :return: an example HParam object
    """
    return HParam(value=1, name="test", descr="test")


@pytest.fixture
def example_defender_strategy(
        example_state: State, example_action: Action, example_experiment_config: ExperimentConfig) \
        -> MultiThresholdStoppingPolicy:
    """
    Fixture that returns an example MultiThresholdStoppingPolicy object

    :param example_state: an example State
    :param example_action: an example Action
    :param example_experiment_config: an example ExperimentConfig
    :return: an example MultiThresholdStoppingPolicy object
    """
    theta = [0.2, 0.8]
    return MultiThresholdStoppingPolicy(
        theta=theta, simulation_name="test", L=2, player_type=PlayerType.DEFENDER, states=[example_state],
        actions=[example_action], experiment_config=example_experiment_config, avg_R=0.9, agent_type=AgentType.T_SPSA,
        opponent_strategy=None)


@pytest.fixture
def example_attacker_strategy(
        example_state: State, example_action: Action, example_experiment_config: ExperimentConfig) \
        -> RandomPolicy:
    """
    Fixture that returns an example MultiThresholdStoppingPolicy object

    :param example_state: an example State
    :param example_action: an example Action
    :param example_experiment_config: an example ExperimentConfig
    :return: an example MultiThresholdStoppingPolicy object
    """
    attacker_stage_strategy = np.zeros((3, 2))
    attacker_stage_strategy[0][0] = 0.9
    attacker_stage_strategy[0][1] = 0.1
    attacker_stage_strategy[1][0] = 1
    attacker_stage_strategy[1][1] = 0
    attacker_stage_strategy[2] = attacker_stage_strategy[1]
    attacker_strategy = RandomPolicy(actions=[example_action],
                                     player_type=PlayerType.ATTACKER,
                                     stage_policy_tensor=list(attacker_stage_strategy))
    return attacker_strategy
