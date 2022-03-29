import gym
import numpy as np
from csle_common.util.experiment_util import ExperimentUtil
from gym_csle_stopping_game.envs.stopping_game_pomdp_defender_env import StoppingGameDefenderPomdpConfig
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig
from gym_csle_stopping_game.dao.stopping_game_defender_pomdp_config import StoppingGameDefenderPomdpConfig
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil


def static_attacker_strategy(obs: np.ndarray, config: StoppingGameConfig) -> np.ndarray:
    pi2 = np.zeros((3,2))
    pi2[0][0] = np.random.rand()
    pi2[0][1] = 1-pi2[0][0]
    pi2[1][0] = np.random.rand()
    pi2[1][1] = 1-pi2[1][0]
    pi2[2] = pi2[1]
    return pi2


def test_env():
    ExperimentUtil.set_seed(999)
    L=3
    p = 0.01
    num_observations = 100
    R_INT = -5
    R_COST = -5
    R_SLA = 1
    R_ST = 5

    stopping_game_config = StoppingGameConfig(
        A1 = StoppingGameUtil.attacker_actions(), A2= StoppingGameUtil.defender_actions(), L=L, R_INT=R_INT,
        R_COST=R_COST,
        R_SLA=R_SLA, R_ST =R_ST, b1 = StoppingGameUtil.b1(), save_dir=ExperimentUtil.default_output_dir() + "/results",
        T=StoppingGameUtil.transition_tensor(L=L, p=p), O=StoppingGameUtil.observation_space(num_observations),
        Z=StoppingGameUtil.observation_tensor(num_observations),
        R=StoppingGameUtil.reward_tensor(R_SLA=R_SLA, R_INT=R_INT, R_COST=R_COST, L=L, R_ST=R_ST),
        S = StoppingGameUtil.state_space())
    config = StoppingGameDefenderPomdpConfig(
        stopping_game_config=stopping_game_config, stopping_game_name="csle-stopping-game-v1",
        attacker_strategy=static_attacker_strategy)

    env = gym.make("csle-stopping-game-pomdp-defender-v1", config=config)
    num_episodes = 150
    ep = 1
    while ep < num_episodes:
        done = False
        o = env.reset()
        while not done:
            a1 = np.random.choice(np.arange(0, len(config.stopping_game_config.A1)),
                                  p=[1/len(config.stopping_game_config.A1)]*len(config.stopping_game_config.A1))
            o, r, done, info = env.step(a1)
            print(f"o_D:{list(o)}, r_D:{r}, done:{done}, info:{info}")
        ep+=1

if __name__ == '__main__':
    test_env()