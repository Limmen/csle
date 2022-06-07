from typing import List
import numpy as np
import csle_common.constants.constants as constants
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_agents.agents.dynasec.dynasec_agent import DynaSecAgent
import csle_agents.constants.constants as agents_constants
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil
from csle_common.dao.emulation_action.attacker.emulation_attacker_action import EmulationAttackerAction
from csle_common.dao.emulation_action.defender.emulation_defender_action import EmulationDefenderAction
from csle_common.dao.emulation_action.attacker.emulation_attacker_stopping_actions \
    import EmulationAttackerStoppingActions
from csle_common.dao.emulation_action.defender.emulation_defender_stopping_actions \
    import EmulationDefenderStoppingActions
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
from csle_common.dao.training.tabular_policy import TabularPolicy
from csle_common.dao.system_identification.system_identification_config import SystemIdentificationConfig
from csle_common.dao.system_identification.system_model_type import SystemModelType
import csle_system_identification.constants.constants as system_identification_constants


def expert_attacker_sequence(wait_steps: int, emulation_env_config: EmulationEnvConfig) \
        -> List[EmulationAttackerAction]:
    """
    Returns a list of attacker actions representing the expert attacker

    :param wait_steps: the number of steps that the attacker waits before starting the intrusion
    :param emulation_env_config: the emulation configuration
    :return: the list of attacker actions
    """
    wait_seq = [EmulationAttackerStoppingActions.CONTINUE(index=-1)] * wait_steps
    intrusion_seq = emulation_env_config.static_attacker_sequences[constants.STATIC_ATTACKERS.EXPERT]
    seq = wait_seq + intrusion_seq
    return seq


def passive_defender_sequence(length: int, emulation_env_config: EmulationEnvConfig) -> List[EmulationDefenderAction]:
    """
    Returns a sequence of actions representing a passive defender

    :param length: the length of the sequence
    :param emulation_env_config: the configuration of the emulation to run the sequence
    :return: a sequence of defender actions in the emulation
    """
    seq = [EmulationDefenderStoppingActions.CONTINUE(index=-1)] * length
    return seq


if __name__ == '__main__':
    emulation_executions = [
        MetastoreFacade.get_emulation_execution(ip_first_octet=15, emulation_name="csle-level11-001"),
        MetastoreFacade.get_emulation_execution(ip_first_octet=16, emulation_name="csle-level11-001")
    ]
    # MetastoreFacade.get_emulation_execution(ip_first_octet=16, emulation_name="csle-level11-001")
    simulation_env_config = MetastoreFacade.get_simulation_by_name("csle-stopping-pomdp-defender-002")
    experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}dynasec_test", title="DynaSec test",
        random_seeds=[399],
        agent_type=AgentType.DYNA_SEC,
        log_every=1,
        hparams={
            agents_constants.COMMON.GAMMA: HParam(
                value=0.99, name=agents_constants.COMMON.GAMMA,
                descr="the discount factor gamma"),
            agents_constants.T_SPSA.THETA1: HParam(value=[-3]*(3), name=agents_constants.T_SPSA.THETA1,
                                                   descr="initial thresholds"),
            agents_constants.T_SPSA.N: HParam(value=50, name=agents_constants.T_SPSA.N,
                                              descr="the number of training iterations"),
            agents_constants.T_SPSA.c: HParam(
                value=10, name=agents_constants.T_SPSA.c,
                descr="scalar coefficient for determining perturbation sizes in T-SPSA"),
            agents_constants.T_SPSA.a: HParam(
                value=1, name=agents_constants.T_SPSA.a,
                descr="scalar coefficient for determining gradient step sizes in T-SPSA"),
            agents_constants.T_SPSA.A: HParam(
                value=100, name=agents_constants.T_SPSA.A,
                descr="scalar coefficient for determining gradient step sizes in T-SPSA"),
            agents_constants.T_SPSA.LAMBDA: HParam(
                value=0.602, name=agents_constants.T_SPSA.LAMBDA,
                descr="scalar coefficient for determining perturbation sizes in T-SPSA"),
            agents_constants.T_SPSA.EPSILON: HParam(
                value=0.101, name=agents_constants.T_SPSA.EPSILON,
                descr="scalar coefficient for determining gradient step sizes in T-SPSA"),
            agents_constants.T_SPSA.L: HParam(value=3, name="L", descr="the number of stop actions"),
            agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(value=25, name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                                                            descr="number of iterations to evaluate theta"),
            agents_constants.COMMON.SAVE_EVERY: HParam(value=1000, name=agents_constants.COMMON.SAVE_EVERY,
                                                       descr="how frequently to save the model"),
            agents_constants.COMMON.CONFIDENCE_INTERVAL: HParam(
                value=0.95, name=agents_constants.COMMON.CONFIDENCE_INTERVAL,
                descr="confidence interval"),
            agents_constants.COMMON.MAX_ENV_STEPS: HParam(
                value=100, name=agents_constants.COMMON.MAX_ENV_STEPS,
                descr="maximum number of steps in the environment (for envs with infinite horizon generally)"),
            agents_constants.T_SPSA.GRADIENT_BATCH_SIZE: HParam(
                value=1, name=agents_constants.T_SPSA.GRADIENT_BATCH_SIZE,
                descr="the batch size of the gradient estimator"),
            agents_constants.COMMON.RUNNING_AVERAGE: HParam(
                value=100, name=agents_constants.COMMON.RUNNING_AVERAGE,
                descr="the number of samples to include when computing the running avg"),
            agents_constants.DYNASEC.INTRUSION_START_P: HParam(
                value=0.2, name=agents_constants.DYNASEC.INTRUSION_START_P,
                descr="the p parameter for the geometric distribution of the intrusion start time"),
            agents_constants.DYNASEC.EMULATION_TRACES_TO_SAVE_W_DATA_COLLECTION_JOB: HParam(
                value=1, name=agents_constants.DYNASEC.EMULATION_TRACES_TO_SAVE_W_DATA_COLLECTION_JOB,
                descr="number of traces to cache with each data collection job"),
            agents_constants.DYNASEC.SLEEP_TIME: HParam(
                value=30, name=agents_constants.DYNASEC.SLEEP_TIME,
                descr="sleep time for data collection processes"),
            agents_constants.DYNASEC.TRAINING_EPOCHS: HParam(
                value=10000, name=agents_constants.DYNASEC.TRAINING_EPOCHS,
                descr="the number of training epochs of dynasec"),
            agents_constants.DYNASEC.EPISODES_BETWEEN_MODEL_UPDATES: HParam(
                value=2, name=agents_constants.DYNASEC.EPISODES_BETWEEN_MODEL_UPDATES,
                descr="the number of episodes between model updates in dynasec")
        },
        player_type=PlayerType.DEFENDER, player_idx=0
    )
    system_identifcation_config = SystemIdentificationConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}em_level9_test",
        title="Expectation-Maximization level 9 test",
        model_type=SystemModelType.GAUSSIAN_MIXTURE,
        log_every=1,
        hparams={
            system_identification_constants.SYSTEM_IDENTIFICATION.CONDITIONAL_DISTRIBUTIONS: HParam(
                value=["no_intrusion", "intrusion"],
                name=system_identification_constants.SYSTEM_IDENTIFICATION.CONDITIONAL_DISTRIBUTIONS,
                descr="the conditional distributions to estimate"),
            system_identification_constants.EXPECTATION_MAXIMIZATION.NUM_MIXTURES_PER_CONDITIONAL: HParam(
                value=[2,3],
                name=system_identification_constants.EXPECTATION_MAXIMIZATION.NUM_MIXTURES_PER_CONDITIONAL,
                descr="the number of mixtures per conditional distributions to estimate with EM"),
            system_identification_constants.SYSTEM_IDENTIFICATION.METRICS: HParam(
                value=["alerts_weighted_by_priority"],
                name=system_identification_constants.SYSTEM_IDENTIFICATION.METRICS,
                descr="the metrics to estimate")
        }
    )
    simulation_env_config.simulation_env_input_config.attacker_strategy = TabularPolicy(
        player_type=PlayerType.ATTACKER,
        actions=simulation_env_config.joint_action_space_config.action_spaces[1].actions,
        simulation_name=simulation_env_config.name, value_function=None, q_table=None,
        lookup_table=[
            [0.8, 0.2],
            [1, 0],
            [1,0]
        ],
        agent_type=AgentType.RANDOM, avg_R=-1)
    attacker_sequence = expert_attacker_sequence(wait_steps=0,
                                                 emulation_env_config=emulation_executions[0].emulation_env_config)
    defender_sequence = passive_defender_sequence(length=len(attacker_sequence),
                                                  emulation_env_config=emulation_executions[0].emulation_env_config)
    simulation_env_config.simulation_env_input_config.stopping_game_config.R = list(StoppingGameUtil.reward_tensor(
        R_INT=-10, R_COST=-10, R_SLA=0, R_ST=20, L=3))
    simulation_env_config.simulation_env_input_config.stopping_game_config.O = np.array(list(range(0, 15000)))
    agent = DynaSecAgent(emulation_executions=emulation_executions, simulation_env_config=simulation_env_config,
                       experiment_config=experiment_config, attacker_sequence=attacker_sequence,
                         defender_sequence=defender_sequence, system_identification_config=system_identifcation_config)
    experiment_execution = agent.train()
    # MetastoreFacade.save_experiment_execution(experiment_execution)
    # for policy in experiment_execution.result.policies.values():
    #     MetastoreFacade.save_multi_threshold_stopping_policy(multi_threshold_stopping_policy=policy)
