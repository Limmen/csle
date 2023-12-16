import gymnasium as gym
import numpy as np
import json
import io
from csle_common.metastore.metastore_facade import MetastoreFacade
from gym_csle_apt_game.util.apt_game_util import AptGameUtil
from gym_csle_apt_game.dao.apt_game_config import AptGameConfig

if __name__ == '__main__':
    filename = "/home/kim/nyu_data_dict_3"
    with io.open(filename, 'r') as f:
        json_str = f.read()
    data_dict = json.loads(json_str)

    simulation_name = "csle-apt-game-001"
    simulation_env_config = MetastoreFacade.get_simulation_by_name(simulation_name)
    if simulation_env_config is None:
        raise ValueError(f"Could not find a simulation with name: {simulation_name}")
    N = 10
    p_a = 0.1
    num_observations = 1000
    Z = []
    no_intrusion_min_val = max([0, int(data_dict["no_intrusion_alerts_means"][10] -
                                       data_dict["no_intrusion_alerts_stds"][10])])
    no_intrusion_max_val = data_dict["no_intrusion_alerts_means"][10] + data_dict["no_intrusion_alerts_stds"][10]
    no_intrusion_range = (no_intrusion_min_val, no_intrusion_max_val)
    intrusion_min_val = max([0, int(data_dict["intrusion_alerts_means"][10] * (1 + N * 0.2) -
                                    data_dict["intrusion_alerts_stds"][10])])
    intrusion_max_val = data_dict["intrusion_alerts_means"][10] * (1 + N * 0.2) + data_dict["intrusion_alerts_stds"][10]
    max_intrusion_range = (intrusion_min_val, intrusion_max_val)
    O = list(range(int(no_intrusion_range[0]), int(max_intrusion_range[1])))
    no_intrusion_dist = []
    for i in O:
        if i in list(range(int(no_intrusion_range[0]), int(no_intrusion_range[1]))):
            no_intrusion_dist.append(round(1 / (no_intrusion_range[1] - no_intrusion_range[0]), 10))
        else:
            no_intrusion_dist.append(0)
    Z.append(list(np.array(no_intrusion_dist) / sum(no_intrusion_dist)))
    for s in range(1, N + 1):
        intrusion_dist = []
        min_val = max([0, int(data_dict["intrusion_alerts_means"][10] * (1 + s * 0.2) -
                              data_dict["intrusion_alerts_stds"][10])])
        max_val = data_dict["intrusion_alerts_means"][10] * (1 + s * 0.2) + data_dict["intrusion_alerts_stds"][10]
        intrusion_range = (min_val, max_val)
        for i in O:
            if i in range(int(intrusion_range[0]), int(intrusion_range[1])):
                intrusion_dist.append(round(1 / (intrusion_range[1] - intrusion_range[0]), 10))
            else:
                intrusion_dist.append(0)
        Z.append(list(np.array(intrusion_dist) / sum(intrusion_dist)))

    C = AptGameUtil.cost_tensor(N=N)
    T = AptGameUtil.transition_tensor(N=N, p_a=p_a)
    # Z = AptGameUtil.observation_tensor(N=N, num_observations=num_observations)
    # O = AptGameUtil.observation_space(num_observations=num_observations)
    S = AptGameUtil.state_space(N=N)
    A1 = AptGameUtil.defender_actions()
    A2 = AptGameUtil.attacker_actions()
    b1 = AptGameUtil.b1(N=N)
    gamma = 0.99
    input_config = AptGameConfig(
        T=T, O=O, Z=Z, C=C, S=S, A1=A1, A2=A2, N=N, p_a=p_a, save_dir=".", checkpoint_traces_freq=10000, gamma=gamma,
        b1=b1, env_name="csle-apt-game-v1")

    AptGameUtil.generate_os_posg_game_file(game_config=input_config)

    env = gym.make("csle-apt-game-v1", config=input_config)
    p_intrusion = 0.5
    pi2 = []
    for s in S:
        pi2.append([1 - p_intrusion, p_intrusion])
    pi2 = np.array(pi2)
    o, info = env.reset()
    (defender_obs, attacker_obs) = o
    for t in range(200):
        b = attacker_obs[0]
        s = attacker_obs[1]
        a1 = 0
        a2 = (pi2, AptGameUtil.sample_attacker_action(pi2=pi2, s=s))
        action_profile = (a1, a2)
        o, costs, done, _, info = env.step(action_profile)
        (defender_obs, attacker_obs) = o
        c = costs[0]
        b_str = ",".join(list(map(lambda x: f"{x:.2f}", b)))
        print(f"t:{t}, s:{s}, c: {c:.2f}, b: {b_str}")
