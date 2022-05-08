import numpy as np
import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.t_fp.t_fp_agent import TFPAgent
import csle_agents.constants.constants as agents_constants
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil

if __name__ == '__main__':
    emulation_env_config = MetastoreFacade.get_emulation("csle-level9-001")
    defender_simulation_env_config = MetastoreFacade.get_simulation("csle-stopping-pomdp-defender-003")
    attacker_simulation_env_config = MetastoreFacade.get_simulation("csle-stopping-mdp-attacker-003")
    experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}tfp_test",
        title="T-FP training attacker and defender through self-play to approximate a Nash equilibrium",
        random_seeds=[399, 98912], agent_type=AgentType.T_FP,
        log_every=1, br_log_every=5000,
        hparams={
            agents_constants.T_SPSA.N: HParam(
                value=100, name=agents_constants.T_SPSA.N,
                descr="the number of training iterations to learn best response with T-SPSA"),
            agents_constants.T_SPSA.c: HParam(
                value=10, name=agents_constants.T_SPSA.c,
                descr="scalar coefficient for determining perturbation sizes in T-SPSA for best-response learning"),
            agents_constants.T_SPSA.a: HParam(
                value=1, name=agents_constants.T_SPSA.a,
                descr="scalar coefficient for determining gradient step sizes in T-SPSA for best-response learning"),
            agents_constants.T_SPSA.A: HParam(
                value=100, name=agents_constants.T_SPSA.A,
                descr="scalar coefficient for determining gradient step sizes in T-SPSA for best-response learning"),
            agents_constants.T_SPSA.LAMBDA: HParam(
                value=0.602, name=agents_constants.T_SPSA.LAMBDA,
                descr="scalar coefficient for determining perturbation sizes in T-SPSA for best-response learning"),
            agents_constants.T_SPSA.EPSILON: HParam(
                value=0.101, name=agents_constants.T_SPSA.EPSILON,
                descr="scalar coefficient for determining gradient step sizes in T-SPSA for best-response learning"),
            agents_constants.T_FP.N_2: HParam(
                value=10000, name=agents_constants.T_FP.N_2,
                descr="the number of self-play training iterations of T-FP"),
            agents_constants.T_SPSA.L: HParam(value=7, name=agents_constants.T_SPSA.L,
                                              descr="the number of stop actions"),
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
            agents_constants.T_SPSA.GRADIENT_BATCH_SIZE: HParam(
                value=1, name=agents_constants.T_SPSA.GRADIENT_BATCH_SIZE,
                descr="the batch size of the gradient estimator"),
            agents_constants.COMMON.RUNNING_AVG: HParam(
                value=40, name=agents_constants.COMMON.RUNNING_AVG,
                descr="the number of samples to include when computing the running avg"),
        },
        player_type=PlayerType.ATTACKER, player_idx=1
    )
    agent = TFPAgent(emulation_env_config=emulation_env_config,
                     defender_simulation_env_config=defender_simulation_env_config,
                     attacker_simulation_env_config=attacker_simulation_env_config,
                     experiment_config=experiment_config)
    attacker_simulation_env_config.simulation_env_input_config.stopping_game_config.R = list(StoppingGameUtil.reward_tensor(
        R_INT=-1, R_COST=-2, R_SLA=0, R_ST=20, L=7))
    defender_simulation_env_config.simulation_env_input_config.stopping_game_config.R = list(StoppingGameUtil.reward_tensor(
        R_INT=-1, R_COST=-2, R_SLA=0, R_ST=20, L=7))
    defender_simulation_env_config.simulation_env_input_config.stopping_game_config.b1 = np.array([0.5,0.5,0])
    attacker_simulation_env_config.simulation_env_input_config.stopping_game_config.b1 = np.array([0.5,0.5,0])
    experiment_execution = agent.train()
    MetastoreFacade.save_experiment_execution(experiment_execution)
    for policy in experiment_execution.result.policies.values():
        MetastoreFacade.save_multi_threshold_stopping_policy(multi_threshold_stopping_policy=policy)
