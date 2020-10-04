"""
Client configuration for running experiments (parsed from JSON)
"""
from gym_pycr_pwcrack.agents.config.pg_agent_config import PolicyGradientAgentConfig
from gym_pycr_pwcrack.dao.experiment.runner_mode import RunnerMode
from gym_pycr_pwcrack.dao.experiment.simulation_config import SimulationConfig

class ClientConfig:
    """
    DTO with client config for running experiments
    """

    def __init__(self, env_name:str,
                 pg_agent_config: PolicyGradientAgentConfig = None,
                 output_dir:str = None, title = None,
                 env_config = None, run_many :bool = False,
                 random_seeds : list = None, random_seed = 0, agent_type : int = 0,
                 cluster_config = None, env_checkpoint_dir : str = None,
                 mode: RunnerMode = RunnerMode.TRAIN_ATTACKER,
                 simulation_config: SimulationConfig = None):
        """
        Class constructor, initializes the DTO

        :param env_name: name of the environment for the experiment
        :param output_dir: directory to save outputs (results)
        :param title: title in the GUI
        :param env_config: network configuration
        :param initial_state_path: path to initial state
        :param run_many: if this is true, it will try to run many experiments in a row, using different random seeds
        :param random_seeds: list of random seeds when running several experiments in a row
        :param random_seed: specific random seed
        :param pg_agent_config: policy gradient agent config
        :param agent_type: agent_type
        :param cluster_config: cluster_config
        :param env_checkpoint_dir: checkpoint dir for env data
        :param mode: the mode for the experiment
        :param simulation_config: the simulation config
        """
        self.env_name = env_name
        self.logger = None
        self.output_dir = output_dir
        self.title = title
        self.env_config = env_config
        self.run_many = run_many
        self.random_seeds = random_seeds
        self.random_seed = random_seed
        self.pg_agent_config = pg_agent_config
        self.agent_type = agent_type
        self.cluster_config = cluster_config
        self.env_checkpoint_dir = env_checkpoint_dir
        self.mode = mode
        self.simulation_config = simulation_config