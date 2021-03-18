import os
import glob
from gym_pycr_ctf.agents.config.agent_config import AgentConfig
from gym_pycr_ctf.dao.experiment.client_config import ClientConfig
from gym_pycr_ctf.dao.agent.agent_type import AgentType
from gym_pycr_ctf.util.experiments_util import util
from gym_pycr_ctf.dao.network.cluster_config import ClusterConfig
from gym_pycr_ctf.dao.experiment.simulation_config import SimulationConfig
from gym_pycr_ctf.dao.experiment.runner_mode import RunnerMode

def default_config() -> ClientConfig:
    """
    :return: Default configuration for the experiment
    """
    simulation_config = SimulationConfig(render=True, sleep=0, video=True, log_frequency=1000,
                                         video_fps=5, video_dir=util.default_output_dir() + "/results/videos",
                                         num_episodes=1000,
                                         gifs=True, gif_dir=util.default_output_dir() + "/results/gifs",
                                         video_frequency=1, domain_randomization=True, dr_max_num_nodes=4,
                                         dr_min_num_nodes=4, dr_min_num_users=1, dr_max_num_users=5,
                                         dr_min_num_flags=1, dr_max_num_flags=3, dr_use_base=True)
    env_name = "pycr-ctf-level-1-sim-v1"
    cluster_config = ClusterConfig(agent_ip="172.18.1.191", agent_username="agent", agent_pw="agent",
                                   server_connection=False)
    # cluster_config = ClusterConfig(server_ip="172.31.212.91", agent_ip="172.18.1.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
    #                                server_username="kim")
    client_config = ClientConfig(env_name=env_name, agent_config=None,
                                 agent_type=AgentType.PPO_BASELINE.value,
                                 output_dir=util.default_output_dir(),
                                 title="Manual Attacker v1 Simulation",
                                 run_many=False, random_seeds=[0, 999, 299, 399, 499],
                                 random_seed=399, cluster_config=cluster_config,
                                 mode=RunnerMode.MANUAL_ATTACKER.value, simulation_config=simulation_config)
    return client_config


def write_default_config(path:str = None) -> None:
    """
    Writes the default configuration to a json file

    :param path: the path to write the configuration to
    :return: None
    """
    if path is None:
        path = util.default_config_path()
    config = default_config()
    util.write_config_file(config, path)


# Program entrypoint
if __name__ == '__main__':

    # Setup
    args = util.parse_args(util.default_config_path())
    experiment_title = "PPO level_1 v1 cluster"
    if args.configpath is not None and not args.noconfig:
        if not os.path.exists(args.configpath):
            write_default_config()
        config = util.read_config(args.configpath)
    else:
        config = default_config()

    util.run_experiment(config, config.random_seed)
