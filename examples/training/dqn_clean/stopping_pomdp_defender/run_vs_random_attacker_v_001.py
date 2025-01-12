import csle_agents.constants.constants as agents_constants
import csle_common.constants.constants as constants
from csle_agents.agents.dqn_clean.dqn_clean_agent import DQNCleanAgent
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.training.tabular_policy import TabularPolicy
from csle_common.metastore.metastore_facade import MetastoreFacade

if __name__ == "__main__":
    emulation_name = "csle-level1-070"
    emulation_env_config = MetastoreFacade.get_emulation_by_name(emulation_name)
    if emulation_env_config is None:
        raise ValueError(
            f"Could not find an emulation environment with the name: {emulation_name}"
        )
    simulation_name = "csle-intrusion-response-game-local-pomdp-defender-001"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}dqn_clean_test",
        title="DQN_clean test",
        random_seeds=[399, 98912, 999],
        agent_type=AgentType.DQN_CLEAN,
        log_every=1000,
        hparams={
            constants.NEURAL_NETWORKS.NUM_NEURONS_PER_HIDDEN_LAYER: HParam(
                value=7,
                name=constants.NEURAL_NETWORKS.NUM_NEURONS_PER_HIDDEN_LAYER,
                descr="neurons per hidden layer of the policy network",
            ),
            constants.NEURAL_NETWORKS.NUM_HIDDEN_LAYERS: HParam(
                value=4,
                name=constants.NEURAL_NETWORKS.NUM_HIDDEN_LAYERS,
                descr="number of layers of the policy network",
            ),
            agents_constants.DQN_CLEAN.EXP_FRAC: HParam(
                value=0.5,
                name=agents_constants.DQN_CLEAN.EXP_FRAC,
                descr="the fraction of `total-timesteps it takes from start-e to go end-e",
            ),
            agents_constants.DQN_CLEAN.TAU: HParam(
                value=1.0,
                name=agents_constants.DQN_CLEAN.TAU,
                descr="target network update rate",
            ),
            agents_constants.COMMON.BATCH_SIZE: HParam(
                value=64,
                name=agents_constants.COMMON.BATCH_SIZE,
                descr="batch size for updates",
            ),
            agents_constants.DQN_CLEAN.LEARNING_STARTS: HParam(
                value=10000,
                name=agents_constants.DQN_CLEAN.LEARNING_STARTS,
                descr="timestep to start learning",
            ),
            agents_constants.DQN_CLEAN.TRAIN_FREQ: HParam(
                value=10,
                name=agents_constants.DQN_CLEAN.TRAIN_FREQ,
                descr="the frequency of training",
            ),
            agents_constants.DQN_CLEAN.T_N_FREQ: HParam(
                value=500,
                name=agents_constants.DQN_CLEAN.T_N_FREQ,
                descr="the batch size of sample from the reply memory",
            ),
            agents_constants.DQN_CLEAN.BUFFER_SIZE: HParam(
                value=1000,
                name=agents_constants.DQN_CLEAN.BUFFER_SIZE,
                descr="the replay memory buffer size",
            ),
            agents_constants.DQN_CLEAN.SAVE_MODEL: HParam(
                value=False,
                name=agents_constants.DQN_CLEAN.SAVE_MODEL,
                descr="decision param for model saving",
            ),
            agents_constants.COMMON.LEARNING_RATE: HParam(
                value=2.4e-5,
                name=agents_constants.COMMON.LEARNING_RATE,
                descr="learning rate for updating the policy",
            ),
            agents_constants.DQN_CLEAN.NUM_STEPS: HParam(
                value=164,
                name=agents_constants.DQN_CLEAN.NUM_STEPS,
                descr="number of steps in each time step",
            ),
            constants.NEURAL_NETWORKS.DEVICE: HParam(
                value="cpu",
                name=constants.NEURAL_NETWORKS.DEVICE,
                descr="the device to train on (cpu or cuda:x)",
            ),
            agents_constants.COMMON.NUM_PARALLEL_ENVS: HParam(
                value=1,
                name=agents_constants.COMMON.NUM_PARALLEL_ENVS,
                descr="the nunmber of parallel environments for training",
            ),
            agents_constants.COMMON.GAMMA: HParam(
                value=0.99,
                name=agents_constants.COMMON.GAMMA,
                descr="the discount factor",
            ),
            agents_constants.COMMON.NUM_TRAINING_TIMESTEPS: HParam(
                value=int(100000),
                name=agents_constants.COMMON.NUM_TRAINING_TIMESTEPS,
                descr="number of timesteps to train",
            ),
            agents_constants.COMMON.EVAL_EVERY: HParam(
                value=1,
                name=agents_constants.COMMON.EVAL_EVERY,
                descr="training iterations between evaluations",
            ),
            agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(
                value=100,
                name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                descr="the batch size for evaluation",
            ),
            agents_constants.COMMON.SAVE_EVERY: HParam(
                value=10000,
                name=agents_constants.COMMON.SAVE_EVERY,
                descr="how frequently to save the model",
            ),
            agents_constants.COMMON.CONFIDENCE_INTERVAL: HParam(
                value=0.95,
                name=agents_constants.COMMON.CONFIDENCE_INTERVAL,
                descr="confidence interval",
            ),
            agents_constants.COMMON.MAX_ENV_STEPS: HParam(
                value=500,
                name=agents_constants.COMMON.MAX_ENV_STEPS,
                descr="maximum number of steps in the environment (for envs with infinite horizon generally)",
            ),
            agents_constants.COMMON.RUNNING_AVERAGE: HParam(
                value=100,
                name=agents_constants.COMMON.RUNNING_AVERAGE,
                descr="the number of samples to include when computing the running avg",
            ),
            agents_constants.COMMON.L: HParam(
                value=3,
                name=agents_constants.COMMON.L,
                descr="the number of stop actions",
            ),
        },
        player_type=PlayerType.DEFENDER,
        player_idx=0,
    )
    simulation_env_config.simulation_env_input_config.attacker_strategy = TabularPolicy(
        player_type=PlayerType.ATTACKER,
        actions=simulation_env_config.joint_action_space_config.action_spaces[
            1
        ].actions,
        simulation_name=simulation_env_config.name,
        value_function=None,
        q_table=None,
        lookup_table=[[0.8, 0.2], [1, 0], [1, 0]],
        agent_type=AgentType.RANDOM,
        avg_R=-1,
    )
    agent = DQNCleanAgent(
        simulation_env_config=simulation_env_config,
        emulation_env_config=emulation_env_config,
        experiment_config=experiment_config,
        save_to_metastore=False,
    )
    experiment_execution = agent.train()
