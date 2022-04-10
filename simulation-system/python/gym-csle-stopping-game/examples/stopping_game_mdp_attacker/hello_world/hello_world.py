from typing import Tuple, List
import gym
import numpy as np
from csle_common.util.experiment_util import ExperimentUtil
from gym_csle_stopping_game.envs.stopping_game_mdp_attacker_env import StoppingGameMdpAttackerEnv
from gym_csle_stopping_game.dao.stopping_game_config import StoppingGameConfig
from gym_csle_stopping_game.dao.stopping_game_attacker_mdp_config import StoppingGameAttackerMdpConfig
from gym_csle_stopping_game.util.stopping_game_util import StoppingGameUtil
import gym_csle_stopping_game.constants.constants as constants


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
    config = StoppingGameAttackerMdpConfig(
        stopping_game_config=stopping_game_config, stopping_game_name="csle-stopping-game-v1",
        defender_strategy_name=constants.STATIC_DEFENDER_STRATEGIES.RANDOM)

    env = gym.make("csle-stopping-game-mdp-attacker-v1", config=config)
    num_episodes = 50
    ep = 1
    while ep < num_episodes:
        done = False
        o = env.reset()
        while not done:
            pi2 = np.zeros((3,2))
            pi2[0][0] = np.random.rand()
            pi2[0][1] = 1-pi2[0][0]
            pi2[1][0] = np.random.rand()
            pi2[1][1] = 1-pi2[1][0]
            pi2[2] = pi2[1]
            o, r, done, info = env.step(pi2)
            print(f"o_A:{list(o)}, r_A:{r}, done:{done}, info:{info}")
        ep+=1

if __name__ == '__main__':
    test_env()