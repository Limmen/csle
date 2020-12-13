"""
Client configuration for running experiments (parsed from JSON)
"""
from typing import List
from gym_pycr_pwcrack.agents.config.agent_config import AgentConfig
from gym_pycr_pwcrack.dao.experiment.runner_mode import RunnerMode
from gym_pycr_pwcrack.dao.experiment.simulation_config import SimulationConfig
from gym_pycr_pwcrack.dao.container_config.containers_config import ContainersConfig
from gym_pycr_pwcrack.dao.container_config.flags_config import FlagsConfig
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig

class ClientConfig:
    """
    DTO with client config for running experiments
    """

    def __init__(self, env_name:str,
                 agent_config: AgentConfig = None,
                 output_dir:str = None, title = None,
                 env_config = None, run_many :bool = False,
                 random_seeds : list = None, random_seed = 0, agent_type : int = 0,
                 cluster_config = None, env_checkpoint_dir : str = None,
                 mode: RunnerMode = RunnerMode.TRAIN_ATTACKER,
                 simulation_config: SimulationConfig = None,
                 eval_env: bool = None,
                 eval_env_name: str = None,
                 eval_cluster_config = None,
                 containers_config : ContainersConfig = None,
                 flags_config: FlagsConfig = None,
                 randomized_env :bool = False,
                 eval_randomized_env: bool = False,
                 n_envs : int = 1,
                 dummy_vec_env : bool = False,
                 sub_proc_env: bool = False,
                 containers_configs: List[ContainersConfig] = None,
                 flags_configs: List[FlagsConfig] = None,
                 cluster_configs: List[ClusterConfig] = None,
                 multi_env: bool = False
                 ):
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
        :param agent_config: policy gradient agent config
        :param agent_type: agent_type
        :param cluster_config: cluster_config
        :param eval_cluster_config: eval_cluster_config
        :param env_checkpoint_dir: checkpoint dir for env data
        :param mode: the mode for the experiment
        :param simulation_config: the simulation config
        :param eval_env: separate eval env
        :param eval_env_name: separate eval env name
        :param eval_cluster_config: cluster config for eval env
        :param containers_config: containers config for the env
        :param flags_config: flags config for the env
        :param randomized_env: boolean flag whether the env is randomized or not
        :param eval_randomized_env: boolean flag whether the eval env is randomized or not
        :param n_envs: number of envs to use
        :param dummy_vec_env: whether to use dummy vec env (sequential stepping)
        :param sub_proc_env: whether to use subproc env (parallel env)
        :param containers_configs: list of containers config when using multi-env
        :param flags_configs: list of flags config when using multi-env
        :param multi_env: boolean flag whether using a multi-env or not
        :param cluster_configs: list of cluster configs when using a multi-env
        """
        self.env_name = env_name
        self.logger = None
        self.output_dir = output_dir
        self.title = title
        self.env_config = env_config
        self.run_many = run_many
        self.random_seeds = random_seeds
        self.random_seed = random_seed
        self.agent_config = agent_config
        self.agent_type = agent_type
        self.cluster_config = cluster_config
        self.env_checkpoint_dir = env_checkpoint_dir
        self.mode = mode
        self.simulation_config = simulation_config
        self.eval_env = eval_env
        self.eval_env_name = eval_env_name
        self.eval_cluster_config = eval_cluster_config
        self.containers_config = containers_config
        self.flags_config = flags_config
        self.randomized_env = randomized_env
        self.eval_randomized_env = eval_randomized_env
        self.n_envs = n_envs
        self.dummy_vec_env = dummy_vec_env
        self.sub_proc_env = sub_proc_env
        self.containers_configs = containers_configs
        self.flags_configs = flags_configs
        self.multi_env = multi_env
        self.cluster_configs = cluster_configs