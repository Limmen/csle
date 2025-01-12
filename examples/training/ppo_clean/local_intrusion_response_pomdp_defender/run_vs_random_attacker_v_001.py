import numpy as np
import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.ppo_clean.ppo_clean_agent import PPOCleanAgent
import csle_agents.constants.constants as agents_constants
import gym_csle_intrusion_response_game.constants.constants as env_constants
from gym_csle_intrusion_response_game.util.intrusion_response_game_util import IntrusionResponseGameUtil
from gym_csle_intrusion_response_game.dao.local_intrusion_response_game_config import LocalIntrusionResponseGameConfig
from csle_common.dao.training.tabular_policy import TabularPolicy

if __name__ == '__main__':
    emulation_name = "csle-level9-070"
    emulation_env_config = MetastoreFacade.get_emulation_by_name(emulation_name)
    if emulation_env_config is None:
        raise ValueError(f"Could not find an emulation environment with the name: {emulation_name}")
    simulation_name = "csle-intrusion-response-game-local-pomdp-defender-001"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}ppo_test",
        title="PPO_clean test", random_seeds=[399, 98912, 999], agent_type=AgentType.PPO_CLEAN,
        log_every=1,
        hparams={
            constants.NEURAL_NETWORKS.NUM_NEURONS_PER_HIDDEN_LAYER: HParam(
                value=64, name=constants.NEURAL_NETWORKS.NUM_NEURONS_PER_HIDDEN_LAYER,
                descr="neurons per hidden layer of the policy network"),
            constants.NEURAL_NETWORKS.NUM_HIDDEN_LAYERS: HParam(
                value=4, name=constants.NEURAL_NETWORKS.NUM_HIDDEN_LAYERS,
                descr="number of layers of the policy network"),
            agents_constants.COMMON.BATCH_SIZE: HParam(value=32, name=agents_constants.COMMON.BATCH_SIZE,
                                                       descr="batch size for updates"),
            agents_constants.COMMON.LEARNING_RATE: HParam(value=2.4e-5,
                                                          name=agents_constants.COMMON.LEARNING_RATE,
                                                          descr="learning rate for updating the policy"),
            agents_constants.PPO_CLEAN.NUM_STEPS: HParam(value=32,
                                                         name=agents_constants.PPO_CLEAN.NUM_STEPS,
                                                         descr="number of steps in each iteration"),
            agents_constants.PPO_CLEAN.ANNEAL_LR: HParam(value=True,
                                                         name=agents_constants.PPO_CLEAN.ANNEAL_LR,
                                                         descr="anneal learning rate for updating the policy"),
            constants.NEURAL_NETWORKS.DEVICE: HParam(value="cpu",
                                                     name=constants.NEURAL_NETWORKS.DEVICE,
                                                     descr="the device to train on (cpu or cuda:x)"),
            agents_constants.COMMON.NUM_PARALLEL_ENVS: HParam(
                value=1, name=agents_constants.COMMON.NUM_PARALLEL_ENVS,
                descr="the nunmber of parallel environments for training"),
            agents_constants.PPO_CLEAN.CLIP_VLOSS: HParam(
                value=True, name=agents_constants.PPO_CLEAN.CLIP_VLOSS, descr="the clip-vloss"),
            agents_constants.COMMON.GAMMA: HParam(
                value=1, name=agents_constants.COMMON.GAMMA, descr="the discount factor"),
            agents_constants.PPO_CLEAN.GAE_LAMBDA: HParam(
                value=0.95, name=agents_constants.PPO_CLEAN.GAE_LAMBDA, descr="the GAE weighting term"),
            agents_constants.PPO_CLEAN.CLIP_RANGE: HParam(
                value=0.2, name=agents_constants.PPO_CLEAN.CLIP_RANGE, descr="the clip range for PPO"),
            agents_constants.PPO_CLEAN.CLIP_RANGE_VF: HParam(
                value=0.5, name=agents_constants.PPO_CLEAN.CLIP_RANGE_VF,
                descr="the clip range for PPO-update of the value network"),
            agents_constants.PPO_CLEAN.ENT_COEF: HParam(
                value=0.01, name=agents_constants.PPO_CLEAN.ENT_COEF,
                descr="the entropy coefficient for exploration"),
            agents_constants.PPO_CLEAN.VF_COEF: HParam(value=0.5, name=agents_constants.PPO.VF_COEF,
                                                       descr="the coefficient of the value network for the loss"),
            agents_constants.PPO_CLEAN.NUM_MINIBATCHES: HParam(value=4, name=agents_constants.PPO_CLEAN.NUM_MINIBATCHES,
                                                               descr="the number of minibatches"),
            agents_constants.PPO_CLEAN.MAX_GRAD_NORM: HParam(
                value=0.5, name=agents_constants.PPO_CLEAN.MAX_GRAD_NORM, descr="the maximum allows gradient norm"),
            agents_constants.PPO_CLEAN.NORM_ADV: HParam(
                value=0.5, name=agents_constants.PPO_CLEAN.NORM_ADV, descr="norm_av param value"),
            agents_constants.PPO_CLEAN.UPDATE_EPOCHS: HParam(
                value=4, name=agents_constants.PPO_CLEAN.UPDATE_EPOCHS, descr="value of update_epochs"),
            agents_constants.PPO_CLEAN.TARGET_KL: HParam(value=-1,
                                                         name=agents_constants.PPO_CLEAN.TARGET_KL,
                                                         descr="the target kl"),
            agents_constants.PPO_CLEAN.CUDA: HParam(value=False, name=agents_constants.PPO_CLEAN.TARGET_KL,
                                                    descr="boolean flag indicating whether GPU should be used"),
            agents_constants.COMMON.NUM_TRAINING_TIMESTEPS: HParam(
                value=int(1000), name=agents_constants.COMMON.NUM_TRAINING_TIMESTEPS,
                descr="number of timesteps to train"),
            agents_constants.COMMON.EVAL_EVERY: HParam(value=1, name=agents_constants.COMMON.EVAL_EVERY,
                                                       descr="training iterations between evaluations"),
            agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(value=100, name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                                                            descr="the batch size for evaluation"),
            agents_constants.COMMON.SAVE_EVERY: HParam(value=10000, name=agents_constants.COMMON.SAVE_EVERY,
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
                                              descr="the number of stop actions")
        },
        player_type=PlayerType.DEFENDER, player_idx=0
    )
    experiment_config.name = f"workflow_ppo_nodes={1}"
    number_of_zones = 6
    X_max = 100
    eta = 0.5
    reachable = True
    beta = 3
    gamma = 0.99
    initial_zone = 3
    initial_state = [initial_zone, 0]
    zones = IntrusionResponseGameUtil.zones(num_zones=number_of_zones)
    Z_D_P = np.array([0, 0.8, 0.5, 0.1, 0.05, 0.025])
    S = IntrusionResponseGameUtil.local_state_space(number_of_zones=number_of_zones)
    states_to_idx = {}
    for i, s in enumerate(S):
        states_to_idx[(s[env_constants.STATES.D_STATE_INDEX], s[env_constants.STATES.A_STATE_INDEX])] = i
    S_A = IntrusionResponseGameUtil.local_attacker_state_space()
    S_D = IntrusionResponseGameUtil.local_defender_state_space(number_of_zones=number_of_zones)
    A1 = IntrusionResponseGameUtil.local_defender_actions(number_of_zones=number_of_zones)
    C_D = np.array([0, 35, 30, 25, 20, 20, 20, 15])
    A2 = IntrusionResponseGameUtil.local_attacker_actions()
    A_P = np.array([1, 1, 0.75, 0.85])
    O = IntrusionResponseGameUtil.local_observation_space(X_max=X_max)
    T = np.array([IntrusionResponseGameUtil.local_transition_tensor(S=S, A1=A1, A2=A2, Z_D=Z_D_P, A_P=A_P)])
    Z = IntrusionResponseGameUtil.local_observation_tensor_betabinom(S=S, A1=A1, A2=A2, O=O)
    Z_U = np.array([0, 0, 2.5, 5, 10, 15])
    R = np.array(
        [IntrusionResponseGameUtil.local_reward_tensor(eta=eta, C_D=C_D, A1=A1, A2=A2, reachable=reachable, beta=beta,
                                                       S=S, Z_U=Z_U, initial_zone=initial_zone)])
    d_b1 = IntrusionResponseGameUtil.local_initial_defender_belief(S_A=S_A)
    a_b1 = IntrusionResponseGameUtil.local_initial_attacker_belief(S_D=S_D, initial_zone=initial_zone)
    initial_state_idx = states_to_idx[(initial_state[env_constants.STATES.D_STATE_INDEX],
                                       initial_state[env_constants.STATES.A_STATE_INDEX])]
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
    simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config = \
        LocalIntrusionResponseGameConfig(
            env_name=env_name, T=T, O=O, Z=Z, R=R, S=S, S_A=S_A, S_D=S_D, s_1_idx=initial_state_idx, zones=zones,
            A1=A1, A2=A2, d_b1=d_b1, a_b1=a_b1, gamma=gamma, beta=beta, C_D=C_D, A_P=A_P, Z_D_P=Z_D_P, Z_U=Z_U,
            eta=eta
        )
    simulation_env_config.simulation_env_input_config.attacker_strategy = attacker_strategy

    agent = PPOCleanAgent(emulation_env_config=emulation_env_config, simulation_env_config=simulation_env_config,
                          experiment_config=experiment_config)
    experiment_execution = agent.train()
    for policy in experiment_execution.result.policies.values():
        id = MetastoreFacade.save_ppo_policy(ppo_policy=policy)
        policy.id = id
    MetastoreFacade.update_experiment_execution(experiment_execution, id=experiment_execution.id)
