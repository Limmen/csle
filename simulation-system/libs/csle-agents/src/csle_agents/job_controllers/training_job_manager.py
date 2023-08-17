import subprocess
import csle_common.constants.constants as constants
from csle_common.dao.jobs.training_job_config import TrainingJobConfig
from csle_common.dao.training.agent_type import AgentType
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_agents.agents.t_spsa.t_spsa_agent import TSPSAAgent
from csle_agents.agents.ppo.ppo_agent import PPOAgent


class TrainingJobManager:
    """
    Class that manages training jobs in CSLE
    """

    @staticmethod
    def run_training_job(job_config: TrainingJobConfig) -> None:
        """
        Runs a given training job

        :param job_config: the configuration of the job
        :return: None
        """
        emulation_env_config = None
        simulation_env_config = None
        if job_config.emulation_env_name is not None:
            emulation_env_config = MetastoreFacade.get_emulation_by_name(name=job_config.emulation_env_name)
        if job_config.simulation_env_name is not None:
            simulation_env_config = MetastoreFacade.get_simulation_by_name(name=job_config.simulation_env_name)
        if job_config.experiment_config.agent_type == AgentType.T_SPSA:
            tspsa_agent = TSPSAAgent(emulation_env_config=emulation_env_config,
                                     simulation_env_config=simulation_env_config,
                                     experiment_config=job_config.experiment_config, training_job=job_config)
            tspsa_agent.train()
        elif job_config.experiment_config.agent_type == AgentType.PPO:
            ppo_agent = PPOAgent(emulation_env_config=emulation_env_config, simulation_env_config=simulation_env_config,
                                 experiment_config=job_config.experiment_config, training_job=job_config)
            experiment_execution = ppo_agent.train()
            for policy in experiment_execution.result.policies.values():
                MetastoreFacade.save_ppo_policy(ppo_policy=policy)
        else:
            raise ValueError(f"Agent type: {job_config.experiment_config.agent_type} not recognized")

    @staticmethod
    def start_training_job_in_background(training_job: TrainingJobConfig) -> None:
        """
        Starts a training job with a given configuration in the background

        :param training_job: the job configuration
        :return: None
        """
        cmd = constants.COMMANDS.START_TRAINING_JOB.format(training_job.id)
        p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
        p.communicate()
