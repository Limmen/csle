import gymnasium as gym
from csle_common.metastore.metastore_facade import MetastoreFacade

if __name__ == '__main__':
    simulation_name = "csle-intrusion-response-game-workflow-pomdp-defender-001"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    env = gym.make("csle-intrusion-response-game-workflow-pomdp-defender-v1",
                   config=simulation_env_config.simulation_env_input_config)
    env.manual_play()
