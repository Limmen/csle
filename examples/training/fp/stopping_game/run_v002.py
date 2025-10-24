import numpy as np
import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.fp.fictitious_play_agent import FictitiousPlayAgent
import csle_agents.constants.constants as agents_constants


def game_matrix() -> np.ndarray:
    """
    Gets the game matrix

    :return: the game matrix for a 2-player matrix game
    """
    return np.array([
        [3, 3, 1, 4],
        [2, 5, 6, 3],
        [1, 0, 7, 0],
    ])


if __name__ == '__main__':
    emulation_name = "csle-level9-090"
    emulation_env_config = MetastoreFacade.get_emulation_by_name(emulation_name)
    if emulation_env_config is None:
        raise ValueError(f"Could not find an emulation environment with the name: {emulation_name}")
    A = game_matrix()
    p1_prior = [1, 1, 1]
    p2_prior = [1, 1, 1, 1]
    simulation_name = "csle-stopping-game-002"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}fp_test",
        title="Fictitious Play to approximate a Nash equilibrium",
        random_seeds=[399, 98912], agent_type=AgentType.FICTITIOUS_PLAY,
        log_every=1, br_log_every=5000,
        hparams={
            agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(value=1,
                                                            name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                                                            descr="number of iterations to evaluate theta"),
            agents_constants.COMMON.SAVE_EVERY: HParam(
                value=10000, name=agents_constants.COMMON.SAVE_EVERY, descr="how frequently to save the model"),
            agents_constants.COMMON.CONFIDENCE_INTERVAL: HParam(
                value=0.95, name=agents_constants.COMMON.CONFIDENCE_INTERVAL,
                descr="confidence interval"),
            agents_constants.COMMON.MAX_ENV_STEPS: HParam(
                value=500, name=agents_constants.COMMON.MAX_ENV_STEPS,
                descr="maximum number of steps in the environment (for envs with infinite horizon generally)"),
            agents_constants.COMMON.RUNNING_AVERAGE: HParam(
                value=40, name=agents_constants.COMMON.RUNNING_AVERAGE,
                descr="the number of samples to include when computing the running avg"),
            agents_constants.COMMON.GAMMA: HParam(
                value=0.99, name=agents_constants.COMMON.GAMMA,
                descr="the discount factor gamma"),
            agents_constants.FICTITIOUS_PLAY.PAYOFF_MATRIX: HParam(
                value=list(A.tolist()), name=agents_constants.FICTITIOUS_PLAY.PAYOFF_MATRIX,
                descr="the payoff matrix"),
            agents_constants.FICTITIOUS_PLAY.PLAYER_1_PRIOR: HParam(
                value=p1_prior, name=agents_constants.FICTITIOUS_PLAY.PLAYER_1_PRIOR,
                descr="the prior for player 1"),
            agents_constants.FICTITIOUS_PLAY.PLAYER_2_PRIOR: HParam(
                value=p2_prior, name=agents_constants.FICTITIOUS_PLAY.PLAYER_2_PRIOR,
                descr="the prior for player 2"),
            agents_constants.FICTITIOUS_PLAY.N: HParam(
                value=100, name=agents_constants.FICTITIOUS_PLAY.N,
                descr="the number of iterations")
        },
        player_type=PlayerType.SELF_PLAY, player_idx=1
    )
    agent = FictitiousPlayAgent(simulation_env_config=simulation_env_config,
                                experiment_config=experiment_config, save_to_metastore=True,
                                emulation_env_config=emulation_env_config)
    experiment_execution = agent.train()
    MetastoreFacade.save_experiment_execution(experiment_execution)
    for policy in experiment_execution.result.policies.values():
        MetastoreFacade.save_vector_policy(vector_policy=policy)
