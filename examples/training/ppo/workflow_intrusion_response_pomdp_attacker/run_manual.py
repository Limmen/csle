import gym
from csle_common.metastore.metastore_facade import MetastoreFacade

if __name__ == '__main__':
    simulation_env_config = MetastoreFacade.get_simulation_by_name(
        "csle-intrusion-response-game-workflow-pomdp-attacker-001")
    env = gym.make("csle-intrusion-response-game-workflow-pomdp-attacker-v1",
                   config=simulation_env_config.simulation_env_input_config)
    env.manual_play()
