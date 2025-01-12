import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.ppg_clean.ppg_clean_agent import PPGCleanAgent
import csle_agents.constants.constants as agents_constants
from csle_common.dao.training.tabular_policy import TabularPolicy

if __name__ == '__main__':
    emulation_name = "csle-level9-070"
    emulation_env_config = MetastoreFacade.get_emulation_by_name(emulation_name)
    if emulation_env_config is None:
        raise ValueError(f"Could not find an emulation environment with the name: {emulation_name}")
    simulation_name = "csle-stopping-pomdp-defender-001"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}ppg_test",
        title="PPG test", random_seeds=[399], agent_type=AgentType.PPG_CLEAN,
        log_every=1,
        hparams={
            constants.NEURAL_NETWORKS.NUM_NEURONS_PER_HIDDEN_LAYER: HParam(
                value=64, name=constants.NEURAL_NETWORKS.NUM_NEURONS_PER_HIDDEN_LAYER,
                descr="neurons per hidden layer of the policy network"),
            constants.NEURAL_NETWORKS.NUM_HIDDEN_LAYERS: HParam(
                value=1, name=constants.NEURAL_NETWORKS.NUM_HIDDEN_LAYERS,
                descr="number of layers of the policy network"),
            constants.NEURAL_NETWORKS.DEVICE: HParam(value="cpu",
                                                     name=constants.NEURAL_NETWORKS.DEVICE,
                                                     descr="the device to train on (cpu or cuda:x)"),
            agents_constants.COMMON.NUM_PARALLEL_ENVS: HParam(
                value=1, name=agents_constants.COMMON.NUM_PARALLEL_ENVS,
                descr="the nunmber of parallel environments for training"),
            agents_constants.COMMON.GAMMA: HParam(
                value=0.999, name=agents_constants.COMMON.GAMMA, descr="the discount factor"),
            agents_constants.COMMON.NUM_TRAINING_TIMESTEPS: HParam(
                value=int(5), name=agents_constants.COMMON.NUM_TRAINING_TIMESTEPS,
                descr="number of timesteps to train"),
            agents_constants.COMMON.EVAL_EVERY: HParam(value=10, name=agents_constants.COMMON.EVAL_EVERY,
                                                       descr="training iterations between evaluations"),
            agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(value=1, name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                                                            descr="the batch size for evaluation"),
            agents_constants.COMMON.SAVE_EVERY: HParam(value=10000, name=agents_constants.COMMON.SAVE_EVERY,
                                                       descr="how frequently to save the model"),
            agents_constants.COMMON.CONFIDENCE_INTERVAL: HParam(
                value=0.95, name=agents_constants.COMMON.CONFIDENCE_INTERVAL,
                descr="confidence interval"),
            agents_constants.COMMON.MAX_ENV_STEPS: HParam(
                value=10, name=agents_constants.COMMON.MAX_ENV_STEPS,
                descr="maximum number of steps in the environment (for envs with infinite horizon generally)"),
            agents_constants.COMMON.RUNNING_AVERAGE: HParam(
                value=100, name=agents_constants.COMMON.RUNNING_AVERAGE,
                descr="the number of samples to include when computing the running avg"),
            agents_constants.COMMON.L: HParam(value=3, name=agents_constants.COMMON.L,
                                              descr="the number of stop actions"),
            agents_constants.COMMON.EVALUATE_WITH_DISCOUNT: HParam(
                value=False, name=agents_constants.COMMON.EVALUATE_WITH_DISCOUNT,
                descr="boolean flag indicating whether the evaluation should be with discount or not"),
            agents_constants.PPG_CLEAN.LEARNING_RATE: HParam(
                value=5e-4, name=agents_constants.PPG_CLEAN.LEARNING_RATE, descr="the learning rate"),
            agents_constants.PPG_CLEAN.NUM_STEPS: HParam(
                value=2, name=agents_constants.PPG_CLEAN.NUM_STEPS,
                descr="the number of steps to run in each environment per rollout policy"),
            agents_constants.PPG_CLEAN.ANNEAL_LR: HParam(
                value=False, name=agents_constants.PPG_CLEAN.ANNEAL_LR, descr="toogles lr annealing"),
            agents_constants.PPG_CLEAN.GAE_LAMBDA: HParam(
                value=0.95, name=agents_constants.PPG_CLEAN.GAE_LAMBDA,
                descr="the lambda for the general advantage estimation"),
            agents_constants.PPG_CLEAN.NUM_MINIBATCHES: HParam(
                value=8, name=agents_constants.PPG_CLEAN.NUM_MINIBATCHES,
                descr="The number of mini-batches"),
            agents_constants.PPG_CLEAN.ADV_NORM_FULLBATCH: HParam(
                value=True, name=agents_constants.PPG_CLEAN.ADV_NORM_FULLBATCH,
                descr="Toggle full batch advantage normalization as used in PPG code"),
            agents_constants.PPG_CLEAN.CLIP_COEF: HParam(
                value=0.2, name=agents_constants.PPG_CLEAN.CLIP_COEF,
                descr="The surrogate clipping coefficient"),
            agents_constants.PPG_CLEAN.CLIP_VLOSS: HParam(
                value=True, name=agents_constants.PPG_CLEAN.CLIP_VLOSS,
                descr="Toggles whether or not to use a clipped loss for the value function, as per the paper."),
            agents_constants.PPG_CLEAN.ENT_COEF: HParam(
                value=0.01, name=agents_constants.PPG_CLEAN.ENT_COEF,
                descr="Coefficient of the entropy"),
            agents_constants.PPG_CLEAN.VF_COEF: HParam(
                value=0.5, name=agents_constants.PPG_CLEAN.VF_COEF,
                descr="Coefficient of the value function"),
            agents_constants.PPG_CLEAN.TARGET_KL: HParam(
                value=None, name=agents_constants.PPG_CLEAN.TARGET_KL,
                descr="The target KL divergence threshold"),
            agents_constants.PPG_CLEAN.MAX_GRAD_NORM: HParam(
                value=0.5, name=agents_constants.PPG_CLEAN.MAX_GRAD_NORM,
                descr="The maximum norm for the gradient clipping"),
            agents_constants.PPG_CLEAN.N_ITERATION: HParam(
                value=32, name=agents_constants.PPG_CLEAN.N_ITERATION,
                descr="N_pi: the number of policy update in the policy phase"),
            agents_constants.PPG_CLEAN.E_POLICY: HParam(
                value=1, name=agents_constants.PPG_CLEAN.E_POLICY,
                descr="E_pi: the number of policy update in the policy phase"),
            agents_constants.PPG_CLEAN.E_AUXILIARY: HParam(
                value=6, name=agents_constants.PPG_CLEAN.E_AUXILIARY,
                descr="E_aux:the K epochs to update the policy"),
            agents_constants.PPG_CLEAN.BETA_CLONE: HParam(
                value=1.0, name=agents_constants.PPG_CLEAN.BETA_CLONE,
                descr="the behavior cloning coefficient"),
            agents_constants.PPG_CLEAN.NUM_AUX_ROLLOUTS: HParam(
                value=4, name=agents_constants.PPG_CLEAN.NUM_AUX_ROLLOUTS,
                descr="the number of mini batch in the auxiliary phase"),
            agents_constants.PPG_CLEAN.NUM_AUX_GRAD_ACCUM: HParam(
                value=1, name=agents_constants.PPG_CLEAN.NUM_AUX_GRAD_ACCUM,
                descr="the number of gradient accumulation in mini batch"),
            agents_constants.PPG_CLEAN.V_VALUE: HParam(
                value=1, name=agents_constants.PPG_CLEAN.V_VALUE,
                descr="E_V: the number of policy update in the policy phase"),
            agents_constants.PPG_CLEAN.BATCH_SIZE: HParam(
                value=1, name=agents_constants.PPG_CLEAN.BATCH_SIZE,
                descr="the batch size (computed in runtime)"),
            agents_constants.PPG_CLEAN.MINIBATCH_SIZE: HParam(
                value=1, name=agents_constants.PPG_CLEAN.MINIBATCH_SIZE,
                descr="the mini-batch size (computed in runtime)"),
            agents_constants.PPG_CLEAN.NUM_ITERATIONS: HParam(
                value=1, name=agents_constants.PPG_CLEAN.NUM_ITERATIONS,
                descr="the number of iterations (computed in runtime)"),
            agents_constants.PPG_CLEAN.NUM_PHASES: HParam(
                value=1, name=agents_constants.PPG_CLEAN.NUM_PHASES,
                descr="the number of phases (computed in runtime)"),
            agents_constants.PPG_CLEAN.AUX_BATCH_ROLLOUTS: HParam(
                value=1, name=agents_constants.PPG_CLEAN.AUX_BATCH_ROLLOUTS,
                descr="the number of rollouts in the auxiliary phase (computed in runtime)"),
            agents_constants.PPG_CLEAN.TOTAL_STEPS: HParam(
                value=10, name=agents_constants.PPG_CLEAN.TOTAL_STEPS,
                descr="the total number of steps")
        },
        player_type=PlayerType.DEFENDER, player_idx=0
    )
    simulation_env_config.simulation_env_input_config.attacker_strategy = TabularPolicy(
        player_type=PlayerType.ATTACKER,
        actions=simulation_env_config.joint_action_space_config.action_spaces[1].actions,
        simulation_name=simulation_env_config.name, value_function=None, q_table=None,
        lookup_table=[
            [0.8, 0.2],
            [1, 0],
            [1, 0]
        ],
        agent_type=AgentType.RANDOM, avg_R=-1)
    # simulation_env_config.simulation_env_input_config
    agent = PPGCleanAgent(emulation_env_config=emulation_env_config, simulation_env_config=simulation_env_config,
                          experiment_config=experiment_config, save_to_metastore=False)
    experiment_execution = agent.train()
    # MetastoreFacade.save_experiment_execution(experiment_execution)
    # for policy in experiment_execution.result.policies.values():
    #     MetastoreFacade.save_ppo_policy(ppo_policy=policy)
