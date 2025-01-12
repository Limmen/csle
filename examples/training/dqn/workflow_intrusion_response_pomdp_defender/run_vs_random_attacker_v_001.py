import numpy as np
from csle_agents.agents.dqn.dqn_agent import DQNAgent
import csle_agents.constants.constants as agents_constants
import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
import gym_csle_intrusion_response_game.constants.constants as env_constants
from gym_csle_intrusion_response_game.util.intrusion_response_game_util import IntrusionResponseGameUtil
from gym_csle_intrusion_response_game.dao.workflow_intrusion_response_game_config \
    import WorkflowIntrusionResponseGameConfig
from csle_common.dao.training.tabular_policy import TabularPolicy

if __name__ == '__main__':
    emulation_name = "csle-level9-070"
    emulation_env_config = MetastoreFacade.get_emulation_by_name(emulation_name)
    if emulation_env_config is None:
        raise ValueError(f"Could not find an emulation environment with the name: {emulation_name}")
    simulation_name = "csle-intrusion-response-game-workflow-pomdp-defender-001"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    num_nodes = 2
    experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}dqn_test",
        title="DQN test", random_seeds=[399, 98912, 999], agent_type=AgentType.DQN,
        log_every=100,
        hparams={
            constants.NEURAL_NETWORKS.NUM_NEURONS_PER_HIDDEN_LAYER: HParam(
                value=64, name=constants.NEURAL_NETWORKS.NUM_NEURONS_PER_HIDDEN_LAYER,
                descr="neurons per hidden layer of the policy network"),
            constants.NEURAL_NETWORKS.NUM_HIDDEN_LAYERS: HParam(
                value=4, name=constants.NEURAL_NETWORKS.NUM_HIDDEN_LAYERS,
                descr="number of layers of the policy network"),
            agents_constants.COMMON.BATCH_SIZE: HParam(value=64, name=agents_constants.COMMON.BATCH_SIZE,
                                                       descr="batch size for updates"),
            agents_constants.COMMON.LEARNING_RATE: HParam(value=0.0001,
                                                          name=agents_constants.COMMON.LEARNING_RATE,
                                                          descr="learning rate for updating the policy"),
            constants.NEURAL_NETWORKS.DEVICE: HParam(value="cuda:1",
                                                     name=constants.NEURAL_NETWORKS.DEVICE,
                                                     descr="the device to train on (cpu or cuda:x)"),
            agents_constants.COMMON.GAMMA: HParam(
                value=1, name=agents_constants.COMMON.GAMMA, descr="the discount factor"),
            agents_constants.DQN.MAX_GRAD_NORM: HParam(
                value=0.5, name=agents_constants.DQN.MAX_GRAD_NORM, descr="the maximum allows gradient norm"),
            agents_constants.COMMON.NUM_TRAINING_TIMESTEPS: HParam(
                value=int(500000), name=agents_constants.COMMON.NUM_TRAINING_TIMESTEPS,
                descr="number of timesteps to train"),
            agents_constants.COMMON.NUM_PARALLEL_ENVS: HParam(
                value=100, name=agents_constants.COMMON.NUM_PARALLEL_ENVS,
                descr="the nunmber of parallel environments for training"),
            agents_constants.COMMON.EVAL_EVERY: HParam(value=1000, name=agents_constants.COMMON.EVAL_EVERY,
                                                       descr="training iterations between evaluations"),
            agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(value=20, name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                                                            descr="the batch size for evaluation"),
            agents_constants.COMMON.SAVE_EVERY: HParam(value=100000, name=agents_constants.COMMON.SAVE_EVERY,
                                                       descr="how frequently to save the model"),
            agents_constants.COMMON.CONFIDENCE_INTERVAL: HParam(
                value=0.95, name=agents_constants.COMMON.CONFIDENCE_INTERVAL,
                descr="confidence interval"),
            agents_constants.COMMON.MAX_ENV_STEPS: HParam(
                value=500, name=agents_constants.COMMON.MAX_ENV_STEPS,
                descr="maximum number of steps in the environment (for envs with infinite horizon generally)"),
            agents_constants.COMMON.RUNNING_AVERAGE: HParam(
                value=100, name=agents_constants.COMMON.RUNNING_AVERAGE,
                descr="the number of samples to include when computing the running avg"),
            agents_constants.COMMON.L: HParam(value=3, name=agents_constants.COMMON.L,
                                              descr="the number of stop actions"),
            agents_constants.DQN.LEARNING_STARTS: HParam(
                value=50000, name=agents_constants.DQN.LEARNING_STARTS,
                descr="time-step learning starts after warmup"),
            agents_constants.DQN.EXPLORATION_FRACTION: HParam(
                value=0.1, name=agents_constants.DQN.EXPLORATION_FRACTION,
                descr="epsilon for exploration"),
            agents_constants.DQN.EXPLORATION_INITIAL_EPS: HParam(
                value=1.0, name=agents_constants.DQN.EXPLORATION_INITIAL_EPS,
                descr="initial epsilon for exploration"),
            agents_constants.DQN.EXPLORATION_FINAL_EPS: HParam(
                value=0.05, name=agents_constants.DQN.EXPLORATION_FINAL_EPS,
                descr="final epsilon for exploration"),
            agents_constants.DQN.TRAIN_FREQ: HParam(
                value=4, name=agents_constants.DQN.TRAIN_FREQ,
                descr="how frequently to update policy"),
            agents_constants.DQN.GRADIENT_STEPS: HParam(
                value=1, name=agents_constants.DQN.GRADIENT_STEPS,
                descr="number of gradient steps for each update"),
            agents_constants.DQN.N_EPISODES_ROLLOUT: HParam(
                value=1, name=agents_constants.DQN.N_EPISODES_ROLLOUT,
                descr="number of episodes rollout"),
            agents_constants.DQN.TARGET_UPDATE_INTERVAL: HParam(
                value=10000, name=agents_constants.DQN.TARGET_UPDATE_INTERVAL,
                descr="how frequently to update the target network"),
            agents_constants.DQN.BUFFER_SIZE: HParam(
                value=1000000, name=agents_constants.DQN.BUFFER_SIZE,
                descr="size of the replay buffer"),
            agents_constants.DQN.DQN_BATCH_SIZE: HParam(
                value=10000, name=agents_constants.DQN.DQN_BATCH_SIZE,
                descr="the DQN batch size"),
            agents_constants.COMMON.NUM_NODES: HParam(value=num_nodes, name=agents_constants.COMMON.NUM_NODES,
                                                      descr="the number of nodes in the network")
        },
        player_type=PlayerType.DEFENDER, player_idx=0
    )

    number_of_zones = 5
    experiment_config.name = f"workflow_dqn_nodes={num_nodes}"
    X_max = 100
    eta = 0.5
    reachable = True
    beta = 3
    gamma = 0.99
    initial_zone = 3
    initial_state = [initial_zone, 0]
    zones = IntrusionResponseGameUtil.zones(num_zones=number_of_zones)
    Z_D_P = np.array([0, 0.8, 0.15, 0.12, 0.08])
    C_D = np.array([0, 5, 1, 2, 2, 2])
    A2 = IntrusionResponseGameUtil.local_attacker_actions()
    A_P = np.array([1, 1, 0.7, 0.5])
    Z_U = np.array([0, 1, 3, 3.5, 4])
    env_name = "csle-intrusion-response-game-pomdp-defender-v1"
    attacker_stage_strategy = np.zeros((len(IntrusionResponseGameUtil.local_attacker_state_space()), len(A2)))
    for i, s_a in enumerate(IntrusionResponseGameUtil.local_attacker_state_space()):
        if s_a == env_constants.ATTACK_STATES.HEALTHY:
            attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.WAIT] = 0.8
            attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.RECON] = 0.2
        elif s_a == env_constants.ATTACK_STATES.RECON:
            attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.WAIT] = 0.7
            attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.BRUTE_FORCE] = 0.15
            attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.EXPLOIT] = 0.15
        else:
            attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.WAIT] = 1
            attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.BRUTE_FORCE] = 0.
            attacker_stage_strategy[i][env_constants.ATTACKER_ACTIONS.EXPLOIT] = 0
    attacker_strategy = TabularPolicy(
        player_type=PlayerType.ATTACKER, actions=A2,
        simulation_name="csle-intrusion-response-game-pomdp-defender-001",
        value_function=None, q_table=None,
        lookup_table=list(attacker_stage_strategy.tolist()),
        agent_type=AgentType.RANDOM, avg_R=-1)
    gw_reachable = np.array([0, 1, 2])
    adjacency_matrix = [
        [1, 0, 0, 1, 1, 0, 0],
        [0, 1, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 1],
        [0, 0, 0, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 1, 1]
    ]
    adjacency_matrix = np.array(adjacency_matrix)
    nodes = np.array(list(range(num_nodes)))
    initial_zones = []
    attacker_strategies = []
    for node in nodes:
        initial_zones.append(np.random.choice(zones))
        attacker_strategies.append(attacker_strategy)
    initial_zones = np.array(initial_zones)
    simulation_env_config.simulation_env_input_config.game_config = WorkflowIntrusionResponseGameConfig(
        env_name="csle-intrusion-response-game-workflow-pomdp-defender-v1",
        nodes=nodes, initial_zones=initial_zones, X_max=X_max, beta=beta, gamma=gamma,
        zones=zones, Z_D_P=Z_D_P, C_D=C_D, A_P=A_P, Z_U=Z_U, adjacency_matrix=adjacency_matrix, eta=eta,
        gw_reachable=gw_reachable
    )
    simulation_env_config.simulation_env_input_config.attacker_strategies = attacker_strategies

    # simulation_env_config.simulation_env_input_config
    agent = DQNAgent(emulation_env_config=emulation_env_config, simulation_env_config=simulation_env_config,
                     experiment_config=experiment_config)
    experiment_execution = agent.train()
    MetastoreFacade.save_experiment_execution(experiment_execution)
    for policy in experiment_execution.result.policies.values():
        MetastoreFacade.save_dqn_policy(dqn_policy=policy)
