import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.reinforce.reinforce_agent import ReinforceAgent
import csle_agents.constants.constants as agents_constants
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil

if __name__ == '__main__':
    emulation_name = "csle-level9-070"
    emulation_env_config = MetastoreFacade.get_emulation_by_name(emulation_name)
    if emulation_env_config is None:
        raise ValueError(f"Could not find an emulation environment with the name: {emulation_name}")
    simulation_name = "csle-stopping-pomdp-defender-002"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}reinforce_test", title="REINFORCE test",
        random_seeds=[399, 98912, 999, 555],
        agent_type=AgentType.REINFORCE,
        log_every=1,
        hparams={
            agents_constants.REINFORCE.N: HParam(value=50, name=agents_constants.REINFORCE.N,
                                                 descr="the number of training iterations"),
            agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(value=100, name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                                                            descr="number of iterations to evaluate theta"),
            agents_constants.RANDOM_SEARCH.THETA1: HParam(value=[-3, -3, -3],
                                                          name=agents_constants.RANDOM_SEARCH.THETA1,
                                                          descr="initial thresholds"),
            agents_constants.COMMON.SAVE_EVERY: HParam(value=1000, name=agents_constants.COMMON.SAVE_EVERY,
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
            constants.NEURAL_NETWORKS.DEVICE: HParam(value="cpu",
                                                     name=constants.NEURAL_NETWORKS.DEVICE,
                                                     descr="the device to train on (cpu or cuda:x)"),
            agents_constants.COMMON.OPTIMIZER: HParam(value=agents_constants.COMMON.ADAM,
                                                      name=agents_constants.COMMON.OPTIMIZER,
                                                      descr="the optimizer to use for training"),
            agents_constants.COMMON.LEARNING_RATE_EXP_DECAY: HParam(
                value=False, name=agents_constants.COMMON.LEARNING_RATE_EXP_DECAY,
                descr="whether or not to use learning rate decay"),
            agents_constants.COMMON.LEARNING_RATE_DECAY_RATE: HParam(
                value=0.999, name=agents_constants.COMMON.LEARNING_RATE_DECAY_RATE,
                descr="the rate of learning rate decay"),
            constants.NEURAL_NETWORKS.ACTIVATION_FUNCTION: HParam(
                value="ReLU", name=constants.NEURAL_NETWORKS.ACTIVATION_FUNCTION,
                descr="the activation function"),
            agents_constants.REINFORCE.GRADIENT_BATCH_SIZE: HParam(
                value=1, name=agents_constants.REINFORCE.GRADIENT_BATCH_SIZE,
                descr="the gradient batch size"),
            agents_constants.COMMON.GAMMA: HParam(
                value=0.99, name=agents_constants.COMMON.GAMMA,
                descr="the discount factor")
        },
        player_type=PlayerType.DEFENDER, player_idx=0
    )
    agent = ReinforceAgent(emulation_env_config=emulation_env_config, simulation_env_config=simulation_env_config,
                           experiment_config=experiment_config)
    simulation_env_config.simulation_env_input_config.stopping_game_config.R = list(StoppingGameUtil.reward_tensor(
        R_INT=-1, R_COST=-2, R_SLA=0, R_ST=2, L=3))
    experiment_execution = agent.train()
    MetastoreFacade.save_experiment_execution(experiment_execution)
    for policy in experiment_execution.result.policies.values():
        MetastoreFacade.save_fnn_w_softmax_policy(fnn_w_softmax_policy=policy)
