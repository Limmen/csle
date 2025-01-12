import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.ppo.ppo_agent import PPOAgent
import csle_agents.constants.constants as agents_constants
from gym_csle_cyborg.dao.csle_cyborg_config import CSLECyborgConfig
from gym_csle_cyborg.dao.red_agent_type import RedAgentType

if __name__ == '__main__':
    emulation_name = "csle-level9-070"
    emulation_env_config = MetastoreFacade.get_emulation_by_name(emulation_name)
    if emulation_env_config is None:
        raise ValueError(f"Could not find an emulation environment with the name: {emulation_name}")
    simulation_name = "csle-cyborg-001"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}ppo_test",
        title="Apple PPO Cyborg BLine", random_seeds=[399, 98912, 999], agent_type=AgentType.PPO,
        log_every=1,
        hparams={
            constants.NEURAL_NETWORKS.NUM_NEURONS_PER_HIDDEN_LAYER: HParam(
                value=256, name=constants.NEURAL_NETWORKS.NUM_NEURONS_PER_HIDDEN_LAYER,
                descr="neurons per hidden layer of the policy network"),
            constants.NEURAL_NETWORKS.NUM_HIDDEN_LAYERS: HParam(
                value=2, name=constants.NEURAL_NETWORKS.NUM_HIDDEN_LAYERS,
                descr="number of layers of the policy network"),
            agents_constants.PPO.STEPS_BETWEEN_UPDATES: HParam(
                value=2048, name=agents_constants.PPO.STEPS_BETWEEN_UPDATES,
                descr="number of steps in the environment for doing rollouts between policy updates"),
            agents_constants.COMMON.BATCH_SIZE: HParam(value=16, name=agents_constants.COMMON.BATCH_SIZE,
                                                       descr="batch size for updates"),
            agents_constants.COMMON.LEARNING_RATE: HParam(value=0.00005148,
                                                          name=agents_constants.COMMON.LEARNING_RATE,
                                                          descr="learning rate for updating the policy"),
            constants.NEURAL_NETWORKS.DEVICE: HParam(value="cpu",
                                                     name=constants.NEURAL_NETWORKS.DEVICE,
                                                     descr="the device to train on (cpu or cuda:x)"),
            agents_constants.COMMON.NUM_PARALLEL_ENVS: HParam(
                value=1, name=agents_constants.COMMON.NUM_PARALLEL_ENVS,
                descr="the nunmber of parallel environments for training"),
            agents_constants.COMMON.GAMMA: HParam(
                value=0.99, name=agents_constants.COMMON.GAMMA, descr="the discount factor"),
            agents_constants.PPO.GAE_LAMBDA: HParam(
                value=0.99, name=agents_constants.PPO.GAE_LAMBDA, descr="the GAE weighting term"),
            agents_constants.PPO.CLIP_RANGE: HParam(
                value=0.2, name=agents_constants.PPO.CLIP_RANGE, descr="the clip range for PPO"),
            agents_constants.PPO.CLIP_RANGE_VF: HParam(
                value=None, name=agents_constants.PPO.CLIP_RANGE_VF,
                descr="the clip range for PPO-update of the value network"),
            agents_constants.PPO.ENT_COEF: HParam(
                value=0.0002, name=agents_constants.PPO.ENT_COEF,
                descr="the entropy coefficient for exploration"),
            agents_constants.PPO.VF_COEF: HParam(value=0.102, name=agents_constants.PPO.VF_COEF,
                                                 descr="the coefficient of the value network for the loss"),
            agents_constants.PPO.MAX_GRAD_NORM: HParam(
                value=0.5, name=agents_constants.PPO.MAX_GRAD_NORM, descr="the maximum allows gradient norm"),
            agents_constants.PPO.TARGET_KL: HParam(value=None,
                                                   name=agents_constants.PPO.TARGET_KL,
                                                   descr="the target kl"),
            agents_constants.PPO.NUM_GRADIENT_STEPS: HParam(value=10,
                                                            name=agents_constants.PPO.NUM_GRADIENT_STEPS,
                                                            descr="number of gradient steps"),
            agents_constants.COMMON.NUM_TRAINING_TIMESTEPS: HParam(
                value=int(2048) * 1500, name=agents_constants.COMMON.NUM_TRAINING_TIMESTEPS,
                descr="number of timesteps to train"),
            agents_constants.COMMON.EVAL_EVERY: HParam(value=10, name=agents_constants.COMMON.EVAL_EVERY,
                                                       descr="training iterations between evaluations"),
            agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(value=10, name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                                                            descr="the batch size for evaluation"),
            agents_constants.COMMON.SAVE_EVERY: HParam(value=10000, name=agents_constants.COMMON.SAVE_EVERY,
                                                       descr="how frequently to save the model"),
            agents_constants.COMMON.CONFIDENCE_INTERVAL: HParam(
                value=0.95, name=agents_constants.COMMON.CONFIDENCE_INTERVAL,
                descr="confidence interval"),
            agents_constants.COMMON.MAX_ENV_STEPS: HParam(
                value=100, name=agents_constants.COMMON.MAX_ENV_STEPS,
                descr="maximum number of steps in the environment (for envs with infinite horizon generally)"),
            agents_constants.COMMON.RUNNING_AVERAGE: HParam(
                value=50, name=agents_constants.COMMON.RUNNING_AVERAGE,
                descr="the number of samples to include when computing the running avg"),
            agents_constants.COMMON.L: HParam(value=3, name=agents_constants.COMMON.L,
                                              descr="the number of stop actions"),
            agents_constants.COMMON.EVALUATE_WITH_DISCOUNT: HParam(
                value=False, name=agents_constants.COMMON.EVALUATE_WITH_DISCOUNT,
                descr="boolean flag indicating whether the evaluation should be with discount or not")
        },
        player_type=PlayerType.DEFENDER, player_idx=0
    )
    simulation_env_config.simulation_env_input_config = CSLECyborgConfig(
        gym_env_name="csle-cyborg-scenario-two-v1", scenario=2, baseline_red_agents=[RedAgentType.B_LINE_AGENT],
        maximum_steps=100, red_agent_distribution=[1.0], reduced_action_space=False, scanned_state=False,
        decoy_state=False, decoy_optimization=False)
    agent = PPOAgent(emulation_env_config=emulation_env_config, simulation_env_config=simulation_env_config,
                     experiment_config=experiment_config, save_to_metastore=True)
    experiment_execution = agent.train()
    MetastoreFacade.save_experiment_execution(experiment_execution)
    for policy in experiment_execution.result.policies.values():
        MetastoreFacade.save_ppo_policy(ppo_policy=policy)
