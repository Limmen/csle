import gymnasium as gym
from csle_common.metastore.metastore_facade import MetastoreFacade
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil

if __name__ == '__main__':
    simulation_name = "csle-stopping-game-002"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    simulation_env_config.simulation_env_input_config.R = list(StoppingGameUtil.reward_tensor(
        R_INT=-1, R_COST=-10, R_SLA=0, R_ST=10, L=3))
    env = gym.make("csle-stopping-game-v1", config=simulation_env_config.simulation_env_input_config)
    env.manual_play()
