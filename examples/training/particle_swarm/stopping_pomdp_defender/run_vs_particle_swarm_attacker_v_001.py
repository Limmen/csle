import csle_agents.constants.constants as agents_constants
import csle_common.constants.constants as constants
from csle_agents.agents.particle_swarm.particle_swarm_agent import ParticleSwarmAgent
from csle_agents.common.objective_type import ObjectiveType
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.player_type import PlayerType
from csle_common.dao.training.policy_type import PolicyType
from csle_common.metastore.metastore_facade import MetastoreFacade

if __name__ == "__main__":
    emulation_name = "csle-level1-070"
    emulation_env_config = MetastoreFacade.get_emulation_by_name(emulation_name)
    if emulation_env_config is None:
        raise ValueError(
            f"Could not find an emulation environment with the name: {emulation_name}"
        )
    simulation_name = "csle-stopping-pomdp-defender-002"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    experiment_config = ExperimentConfig(
        output_dir=f"{constants.LOGGING.DEFAULT_LOG_DIR}particle_swarm_test",
        title="Particle Swarm test",
        random_seeds=[399, 98912],
        agent_type=AgentType.PARTICLE_SWARM,
        log_every=1,
        hparams={
            agents_constants.PARTICLE_SWARM.N: HParam(
                value=5,
                name=constants.T_SPSA.N,
                descr="the number of training iterations",
            ),
            agents_constants.PARTICLE_SWARM.S: HParam(
                value=10,
                name=agents_constants.PARTICLE_SWARM.S,
                descr="The number of particles in the swarm",
            ),
            agents_constants.PARTICLE_SWARM.L: HParam(
                value=2,
                name=agents_constants.PARTICLE_SWARM.L,
                descr="the number of stop actions",
            ),
            agents_constants.PARTICLE_SWARM.B_LOW: HParam(
                value=-3,
                name=agents_constants.PARTICLE_SWARM.B_LOW,
                descr="lower boundary of random initialition",
            ),
            agents_constants.PARTICLE_SWARM.B_UP: HParam(
                value=3,
                name=agents_constants.PARTICLE_SWARM.B_UP,
                descr="upperboundary of random initialization",
            ),
            agents_constants.PARTICLE_SWARM.INERTIA_WEIGHT: HParam(
                value=0.5,
                name=agents_constants.PARTICLE_SWARM.INERTIA_WEIGHT,
                descr="intertia weight w",
            ),
            agents_constants.PARTICLE_SWARM.COGNITIVE_COEFFICIENT: HParam(
                value=1,
                name=agents_constants.PARTICLE_SWARM.COGNITIVE_COEFFICIENT,
                descr="cognitive coefficient Phi_p",
            ),
            agents_constants.PARTICLE_SWARM.SOCIAL_COEFFICIENT: HParam(
                value=1,
                name=agents_constants.PARTICLE_SWARM.SOCIAL_COEFFICIENT,
                descr="social coefficient Phi_g",
            ),
            agents_constants.COMMON.EVAL_BATCH_SIZE: HParam(
                value=100,
                name=agents_constants.COMMON.EVAL_BATCH_SIZE,
                descr="number of iterations to evaluate theta",
            ),
            agents_constants.COMMON.SAVE_EVERY: HParam(
                value=1000,
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
            agents_constants.COMMON.GAMMA: HParam(
                value=0.99,
                name=agents_constants.COMMON.GAMMA,
                descr="the discount factor",
            ),
            agents_constants.PARTICLE_SWARM.POLICY_TYPE: HParam(
                value=PolicyType.MULTI_THRESHOLD,
                name=agents_constants.PARTICLE_SWARM.POLICY_TYPE,
                descr="policy type for the execution",
            ),
            agents_constants.PARTICLE_SWARM.OBJECTIVE_TYPE: HParam(
                value=ObjectiveType.MAX,
                name=agents_constants.PARTICLE_SWARM.OBJECTIVE_TYPE,
                descr="Objective type",
            ),
        },
        player_type=PlayerType.DEFENDER,
        player_idx=0,
    )
    agent = ParticleSwarmAgent(
        simulation_env_config=simulation_env_config,
        emulation_env_config=emulation_env_config,
        experiment_config=experiment_config,
    )
    experiment_execution = agent.train()
    MetastoreFacade.save_experiment_execution(experiment_execution)
    for policy in experiment_execution.result.policies.values():
        if (
            experiment_config.hparams[agents_constants.PARTICLE_SWARM.POLICY_TYPE].value
            == PolicyType.MULTI_THRESHOLD
        ):
            MetastoreFacade.save_multi_threshold_stopping_policy(
                multi_threshold_stopping_policy=policy
            )
        elif (
            experiment_config.hparams[agents_constants.PARTICLE_SWARM.POLICY_TYPE].value
            == PolicyType.LINEAR_THRESHOLD
        ):
            MetastoreFacade.save_linear_threshold_stopping_policy(
                linear_threshold_stopping_policy=policy
            )
        else:
            raise ValueError(
                "Policy type: "
                f"{experiment_config.hparams[agents_constants.PARTICLE_SWARM.POLICY_TYPE].value} "
                f"not recognized for particle swarm"
            )
