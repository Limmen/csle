import numpy as np
import gymnasium as gym
from csle_common.metastore.metastore_facade import MetastoreFacade
import gym_csle_intrusion_response_game.constants.constants as env_constants
from gym_csle_intrusion_response_game.util.intrusion_response_game_util import IntrusionResponseGameUtil
from gym_csle_intrusion_response_game.dao.local_intrusion_response_game_config import LocalIntrusionResponseGameConfig
from csle_common.dao.training.tabular_policy import TabularPolicy
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.player_type import PlayerType

if __name__ == '__main__':
    simulation_name = "csle-intrusion-response-game-local-pomdp-attacker-001"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    number_of_zones = 5
    X_max = 10
    eta = 0.5
    reachable = True
    beta = 1
    gamma = 0.99
    initial_zone = 3
    initial_state = [initial_zone, 0]
    zones = IntrusionResponseGameUtil.zones(num_zones=number_of_zones)
    Z_D_P = np.array([0, 0.8, 0.07, 0.06, 0.05])
    S = IntrusionResponseGameUtil.local_state_space(number_of_zones=number_of_zones)
    states_to_idx = {}
    for i, s in enumerate(S):
        states_to_idx[(s[env_constants.STATES.D_STATE_INDEX], s[env_constants.STATES.A_STATE_INDEX])] = i
    S_A = IntrusionResponseGameUtil.local_attacker_state_space()
    S_D = IntrusionResponseGameUtil.local_defender_state_space(number_of_zones=number_of_zones)
    A1 = IntrusionResponseGameUtil.local_defender_actions(number_of_zones=number_of_zones)
    C_D = np.array([0, 5, 1, 2, 2, 2])
    A2 = IntrusionResponseGameUtil.local_attacker_actions()
    A_P = np.array([1, 1, 0.9, 0.8])
    O = IntrusionResponseGameUtil.local_observation_space(X_max=X_max)
    T = np.array([IntrusionResponseGameUtil.local_transition_tensor(S=S, A1=A1, A2=A2, Z_D=Z_D_P, A_P=A_P)])
    Z = IntrusionResponseGameUtil.local_observation_tensor_betabinom(S=S, A1=A1, A2=A2, O=O)
    Z_U = np.array([0, 1, 2, 2.5, 3])
    R = np.array(
        [IntrusionResponseGameUtil.local_reward_tensor(eta=eta, C_D=C_D, A1=A1, A2=A2, reachable=reachable, beta=beta,
                                                       S=S, Z_U=Z_U, initial_zone=initial_zone)])
    d_b1 = IntrusionResponseGameUtil.local_initial_defender_belief(S_A=S_A)
    a_b1 = IntrusionResponseGameUtil.local_initial_attacker_belief(S_D=S_D, initial_zone=initial_zone)
    initial_state_idx = states_to_idx[(initial_state[env_constants.STATES.D_STATE_INDEX],
                                       initial_state[env_constants.STATES.A_STATE_INDEX])]
    env_name = "csle-intrusion-response-game-pomdp-defender-v1"
    defender_stage_strategy = np.zeros((len(IntrusionResponseGameUtil.local_defender_state_space(
        number_of_zones=number_of_zones)), len(A1)))
    for i, s_d in enumerate(IntrusionResponseGameUtil.local_defender_state_space(number_of_zones=number_of_zones)):
        # if i == env_constants.ZONES.SHUTDOWN_ZONE:
        #     defender_stage_strategy[i][initial_zone] = 1
        # else:
        defender_stage_strategy[i][env_constants.DEFENDER_ACTIONS.WAIT] = 0.99
        for z in zones:
            defender_stage_strategy[i][z] = 0.01 / len(zones)
    defender_strategy = TabularPolicy(
        player_type=PlayerType.DEFENDER,
        actions=A1,
        simulation_name="csle-intrusion-response-game-pomdp-attacker-001",
        value_function=None, q_table=None,
        lookup_table=list(defender_stage_strategy.tolist()),
        agent_type=AgentType.RANDOM, avg_R=-1)
    simulation_env_config.simulation_env_input_config.local_intrusion_response_game_config = \
        LocalIntrusionResponseGameConfig(
            env_name=env_name, T=T, O=O, Z=Z, R=R, S=S, S_A=S_A, S_D=S_D, s_1_idx=initial_state_idx, zones=zones,
            A1=A1, A2=A2, d_b1=d_b1, a_b1=a_b1, gamma=gamma, beta=beta, C_D=C_D, A_P=A_P, Z_D_P=Z_D_P, Z_U=Z_U,
            eta=eta
        )
    simulation_env_config.simulation_env_input_config.defender_strategy = defender_strategy

    env = gym.make("csle-intrusion-response-game-local-pomdp-attacker-v1",
                   config=simulation_env_config.simulation_env_input_config)
    env.manual_play()
