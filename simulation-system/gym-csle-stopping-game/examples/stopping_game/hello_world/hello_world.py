import random

import gym
import numpy as np
from csle_common.util.experiment_util import ExperimentUtil
from gym_csle_stopping_game.envs.stopping_game_env import StoppingGameEnv
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil

def test_env():
    ExperimentUtil.set_seed(999)
    L=3
    p = 0.01
    num_observations = 100
    R_INT = -5
    R_COST = -5
    R_SLA = 1
    R_ST = 5

    for env in gym.envs.registry.all():
        print(env.id)

    config = StoppingGameConfig(
        A1 = StoppingGameUtil.attacker_actions(), A2= StoppingGameUtil.defender_actions(), L=L, R_INT=R_INT,
        R_COST=R_COST,
        R_SLA=R_SLA, R_ST =R_ST, b1 = StoppingGameUtil.b1(), save_dir=ExperimentUtil.default_output_dir() + "/results",
        T=StoppingGameUtil.transition_tensor(L=L, p=p), O=StoppingGameUtil.observation_space(num_observations),
        Z=StoppingGameUtil.observation_tensor(num_observations),
        R=StoppingGameUtil.reward_tensor(R_SLA=R_SLA, R_INT=R_INT, R_COST=R_COST, L=L, R_ST=R_ST),
        S = StoppingGameUtil.state_space())

    env = gym.make("csle-stopping-game-v1", config=config)
    num_episodes = 50
    ep = 1
    while ep < num_episodes:
        done = False
        o = env.reset()
        while not done:
            a1 = np.random.choice(np.arange(0, len(config.A1)),
                                  p=[1/len(config.A1)]*len(config.A1))
            pi2 = np.zeros((3,2))
            pi2[0][0] = np.random.rand()
            pi2[0][1] = 1-pi2[0][0]
            pi2[1][0] = np.random.rand()
            pi2[1][1] = 1-pi2[1][0]
            pi2[2] = pi2[1]
            action_profile = (a1, pi2)
            o, r, done, info = env.step(action_profile)
            print(f"o_D:{list(o[0])}, o_A:{list(o[1])}, r_D:{r[0]}, r_A:{r[1]}, done:{done}, info:{info}")
        ep+=1

if __name__ == '__main__':
    test_env()