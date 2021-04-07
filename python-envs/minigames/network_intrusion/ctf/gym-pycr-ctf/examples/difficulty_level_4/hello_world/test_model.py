from gym_pycr_ctf.envs.derived_envs.level1.simulation.pycr_ctf_level1_sim_env import PyCRCTFLevel1Sim1Env
from gym_pycr_ctf.envs.derived_envs.level1.emulation.pycr_ctf_level1_emulation_env import PyCRCTFLevel1Emulation1Env
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.agents.manual.manual_defender_agent import ManualDefenderAgent
from gym_pycr_ctf.agents.bots.random_attacker_bot_agent import RandomAttackerBotAgent
from gym_pycr_ctf.agents.bots.custom_attacker_bot_agent import CustomAttackerBotAgent
from gym_pycr_ctf.agents.policy_gradient.ppo_baseline.impl.ppo.ppo import PPO
import torch
import numpy as np
import gym


def initialize_model(env, load_path, device, agent_config) -> None:
    """
    Initialize models

    :return: None
    """
    # Initialize models
    model = PPO.load(env=env, load_path=load_path, device=device,
                     agent_config=agent_config)
    return model


def model_test():
    emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip="172.18.4.191",
                                       agent_username="agent", agent_pw="agent", server_connection=True,
                                       server_private_key_file="/home/kim/.ssh/id_rsa",
                                       server_username="kim", port_forward_next_port=3000)
    env = gym.make("pycr-ctf-level-4-emulation-v5", env_config=None, emulation_config=emulation_config)
    load_path = "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_4/training/v5/generated_simulation/defender/ppo_baseline/results/data/1617774810.573099_policy_network.zip"
    load_path = "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_4/training/v5/generated_simulation/defender/ppo_baseline/results/data/1617775844.7080226_policy_network.zip"
    load_path = "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_4/training/v5/generated_simulation/defender/ppo_baseline/results/data/1617776883.0189135_policy_network.zip"
    model = initialize_model(env, load_path, "cpu:0", None)
    print("model loaded")

    obs_tensor = torch.as_tensor(np.array([[0., 0., 0., 0., 0., 0., 0., 0., 1.]]))
    actions, values = predict(model, obs_tensor, env)
    print("t:{}, a:{}".format(1, actions))

    obs_tensor = torch.as_tensor(np.array([[6., 12., 0., 6., 9., 18., 0., 9., 2.]]))
    actions, values = predict(model, obs_tensor, env)
    print("t:{}, a:{}".format(2, actions))

    obs_tensor = torch.as_tensor(np.array([[125., 270., 20., 105., 134., 288., 20., 114., 3.]]))
    actions, values = predict(model, obs_tensor, env)
    print("t:{}, a:{}".format(3, actions))

    obs_tensor = torch.as_tensor(np.array([[0., 0., 0., 0., 134., 288., 20., 114., 4.]]))
    actions, values = predict(model, obs_tensor, env)
    print("t:{}, a:{}".format(4, actions))

    obs_tensor = torch.as_tensor(np.array([[3., 6., 0., 3., 137., 294., 20., 117., 5.]]))
    actions, values = predict(model, obs_tensor, env)
    print("t:{}, a:{}".format(5, actions))

    obs_tensor = torch.as_tensor(np.array([[3., 6., 0., 3., 140., 300., 20., 120., 6.]]))
    actions, values = predict(model, obs_tensor, env)
    print("t:{}, a:{}".format(6, actions))

    obs_tensor = torch.as_tensor(np.array([[14., 32., 4., 10., 154., 332., 24., 130., 7.]]))
    actions, values = predict(model, obs_tensor, env)
    print("t:{}, a:{}".format(7, actions))

    obs_tensor = torch.as_tensor(np.array([[0., 0., 0., 0., 154., 332., 24., 130., 8.]]))
    actions, values = predict(model, obs_tensor, env)
    print("t:{}, a:{}".format(8, actions))

    obs_tensor = torch.as_tensor(np.array([[5., 10., 0., 5., 159., 342., 24., 135., 9.]]))
    actions, values = predict(model, obs_tensor, env)
    print("t:{}, a:{}".format(9, actions))

    obs_tensor = torch.as_tensor(np.array([[15., 34., 4., 11., 174., 376., 28., 146., 10.]]))
    actions, values = predict(model, obs_tensor, env)
    print("t:{}, a:{}".format(10, actions))

    obs_tensor = torch.as_tensor(np.array([[0., 0., 0., 0., 174., 376., 28., 146., 11.]]))
    actions, values = predict(model, obs_tensor, env)
    print("t:{}, a:{}".format(11, actions))

    obs_tensor = torch.as_tensor(np.array([[11., 26., 4., 7., 207., 446., 32., 175., 13.]]))
    actions, values = predict(model, obs_tensor, env)
    print("t:{}, a:{}".format(12, actions))

    obs_tensor = torch.as_tensor(np.array([[121., 262., 20., 101., 335., 722., 52., 283., 15.]]))
    actions, values = predict(model, obs_tensor, env)
    print("t:{}, a:{}".format(13, actions))

    obs_tensor = torch.as_tensor(np.array([[9., 18., 0., 9., 344., 740., 52., 292., 16.]]))
    actions, values = predict(model, obs_tensor, env)
    print("t:{}, a:{}".format(14, actions))

    obs_tensor = torch.as_tensor(np.array([[7., 14., 0., 7., 351., 754., 52., 299., 17.]]))
    actions, values = predict(model, obs_tensor, env)
    print("t:{}, a:{}".format(15, actions))

    obs_tensor = torch.as_tensor(np.array([[3., 6., 0., 3., 354., 760., 52., 302., 18.]]))
    actions, values = predict(model, obs_tensor, env)
    print("t:{}, a:{}".format(16, actions))


def eval_taus():
    tau_1 = [
        [0., 0., 0., 0., 0., 0., 0., 0., 0.],
        [2., 4., 0., 2., 2., 4., 0., 2., 1.],
        [2., 4., 0., 2., 2., 4., 0., 2., 1.],
        [4., 8., 0., 4., 6., 12., 0., 6., 2.],
        [123., 266., 20., 103., 129., 278., 20., 109., 3.],
        [0., 0., 0., 0., 129., 278., 20., 109., 4.],
        [4., 8., 0., 4., 133., 286., 20., 113., 5.],
        [3., 6., 0., 3., 136., 292., 20., 116., 6.],
        [13., 30., 4., 9., 149., 322., 24., 125., 7.],
        [1., 2., 0., 1., 150., 324., 24., 126., 8.],
        [4., 8., 0., 4., 154., 332., 24., 130., 9.],
        [13., 30., 4., 9., 167., 362., 28., 139., 10.],
        [0., 0., 0., 0., 167., 362., 28., 139., 11.],
        [4., 8., 0., 4., 171., 370., 28., 143., 12.],
        [14., 32., 4., 10., 185., 402., 32., 153., 13.],
        [2., 4., 0., 2., 187., 406., 32., 155., 14.],
        [121., 262., 20., 101., 308., 668., 52., 256., 15.],
        [1., 2., 0., 1., 309., 670., 52., 257., 16.],
        [3., 6., 0., 3., 312., 676., 52., 260., 17.],
        [6., 12., 0., 6., 318., 688., 52., 266., 18.]
    ]

    tau_2 = [
        [0., 0., 0., 0., 0., 0., 0., 0., 0.],
        [0., 0., 0., 0., 0., 0., 0., 0., 1.],
        [5., 10., 0., 5., 5., 10., 0., 5., 2.],
        [123., 266., 20., 103., 128., 276., 20., 108., 3.],
        [2., 4., 0., 2., 130., 280., 20., 110., 4.],
        [3., 6., 0., 3., 133., 286., 20., 113., 5.],
        [4., 8., 0., 4., 137., 294., 20., 117., 6.],
        [14., 32., 4., 10., 151., 326., 24., 127., 7.],
        [1., 2., 0., 1., 152., 328., 24., 128., 8.],
        [4., 8., 0., 4., 156., 336., 24., 132., 9.],
        [13., 30., 4., 9., 169., 366., 28., 141., 10.],
        [1., 2., 0., 1., 170., 368., 28., 142., 11.],
        [3., 6., 0., 3., 173., 374., 28., 145., 12.],
        [15., 34., 4., 11., 188., 408., 32., 156., 13.],
        [7., 14., 0., 7., 195., 422., 32., 163., 14.],
        [122., 264., 20., 102., 317., 686., 52., 265., 15.],
        [1., 2., 0., 1., 318., 688., 52., 266., 16.],
        [3., 6., 0., 3., 321., 694., 52., 269., 17.],
        [3., 6., 0., 3., 324., 700., 52., 272., 18.]
    ]

    tau_3 = [
        [0., 0., 0., 0., 0., 0., 0., 0., 0.],
        [1., 2., 0., 1., 1., 2., 0., 1., 1.],
        [4., 8., 0., 4., 5., 10., 0., 5., 2.],
        [124., 268., 20., 104., 129., 278., 20., 109., 3.],
        [1., 2., 0., 1., 130., 280., 20., 110., 4.],
        [3., 6., 0., 3., 133., 286., 20., 113., 5.],
        [2., 4., 0., 2., 135., 290., 20., 115., 6.],
        [12., 28., 4., 8., 147., 318., 24., 123., 7.],
        [1., 2., 0., 1., 148., 320., 24., 124., 8.],
        [2., 4., 0., 2., 150., 324., 24., 126., 9.],
        [13., 30., 4., 9., 163., 354., 28., 135., 10.],
        [1., 2., 0., 1., 164., 356., 28., 136., 11.],
        [4., 8., 0., 4., 168., 364., 28., 140., 12.],
        [13., 30., 4., 9., 181., 394., 32., 149., 13.],
        [2., 4., 0., 2., 183., 398., 32., 151., 14.],
        [120., 260., 20., 100., 303., 658., 52., 251., 15.],
        [0., 0., 0., 0., 303., 658., 52., 251., 16.],
        [4., 8., 0., 4., 307., 666., 52., 255., 17.],
        [3., 6., 0., 3., 310., 672., 52., 258., 18.]
    ]

    return tau_1, tau_2, tau_3


def model_eval():
    tau_1, tau_2, tau_3 = eval_taus()

    emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip="172.18.4.191",
                                       agent_username="agent", agent_pw="agent", server_connection=True,
                                       server_private_key_file="/home/kim/.ssh/id_rsa",
                                       server_username="kim", port_forward_next_port=3000)
    env = gym.make("pycr-ctf-level-4-emulation-v5", env_config=None, emulation_config=emulation_config)
    load_path = "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_4/training/v5/generated_simulation/defender/results_backup3/data/1617776883.0189135_policy_network.zip"
    model = initialize_model(env, load_path, "cpu:0", None)

    obs_tensor = torch.as_tensor(np.array(tau_1))
    actions, values = predict(model, obs_tensor, env)
    reward = compute_reward(actions)
    snort_warning_baseline_r = compute_snort_warning_baseline(tau_1, env.env_config)
    snort_severe_baseline_r = compute_snort_severe_baseline(tau_1, env.env_config)
    snort_critical_baseline_r = compute_snort_critical_baseline(tau_1, env.env_config)
    var_log_baseline = snort_warning_baseline_r
    steps = compute_steps(actions)
    print(actions)
    print("reward:{}, snort_warning:{}, snort_severe:{}, snort_critical:{}, var_log_baseline:{}, steps:{}".format(
        reward, snort_warning_baseline_r, snort_severe_baseline_r, snort_critical_baseline_r, var_log_baseline, steps))

    obs_tensor = torch.as_tensor(np.array(tau_2))
    actions, values = predict(model, obs_tensor, env)
    reward = compute_reward(actions)
    snort_warning_baseline_r = compute_snort_warning_baseline(tau_2, env.env_config)
    snort_severe_baseline_r = compute_snort_severe_baseline(tau_2, env.env_config)
    snort_critical_baseline_r = compute_snort_critical_baseline(tau_2, env.env_config)
    var_log_baseline = snort_warning_baseline_r
    steps = compute_steps(actions)
    print(actions)
    print("reward:{}, snort_warning:{}, snort_severe:{}, snort_critical:{}, var_log_baseline:{}, steps:{}".format(
        reward, snort_warning_baseline_r, snort_severe_baseline_r, snort_critical_baseline_r, var_log_baseline, steps))

    obs_tensor = torch.as_tensor(np.array(tau_3))
    actions, values = predict(model, obs_tensor, env)
    reward = compute_reward(actions)
    snort_warning_baseline_r = compute_snort_warning_baseline(tau_3, env.env_config)
    snort_severe_baseline_r = compute_snort_severe_baseline(tau_3, env.env_config)
    snort_critical_baseline_r = compute_snort_critical_baseline(tau_3, env.env_config)
    var_log_baseline = snort_warning_baseline_r
    steps = compute_steps(actions)
    print(actions)
    print("reward:{}, snort_warning:{}, snort_severe:{}, snort_critical:{}, var_log_baseline:{}, steps:{}".format(
        reward, snort_warning_baseline_r, snort_severe_baseline_r, snort_critical_baseline_r, var_log_baseline, steps))


def compute_reward(actions):
    stopping_idx = -1
    for i in range(len(actions)):
        if actions[i] == 0:
            stopping_idx = i
            break
    r = 0
    if stopping_idx < 6:
        return -1
    if stopping_idx == -1:
        return -1
    if stopping_idx >= 6:
        return 10.0 / max(1, stopping_idx - 5)


def compute_steps(actions):
    stopping_idx = -1
    for i in range(len(actions)):
        if actions[i] == 0:
            stopping_idx = i
            break
    if stopping_idx == -1:
        return len(actions)
    else:
        return stopping_idx

def compute_snort_warning_baseline(tau, env_config):
    stopping_thresh = env_config.snort_warning_baseline_threshold
    stopping_idx = -1
    for i in range(len(tau)):
        if tau[i][3] > stopping_thresh:
            stopping_idx = i
            break

    if stopping_idx < 6:
        return -1
    if stopping_idx == -1:
        return -1
    if stopping_idx >= 6:
        return 10.0 / max(1, stopping_idx - 5)

def compute_snort_severe_baseline(tau, env_config):
    stopping_thresh = env_config.snort_severe_baseline_threshold
    stopping_idx = -1
    for i in range(len(tau)):
        if tau[i][2] > stopping_thresh:
            stopping_idx = i
            break

    if stopping_idx < 6:
        return -1
    if stopping_idx == -1:
        return -1
    if stopping_idx >= 6:
        return 10.0 / max(1, stopping_idx - 5)

def compute_snort_critical_baseline(tau, env_config):
    stopping_thresh = env_config.snort_critical_baseline_threshold
    stopping_idx = -1
    for i in range(len(tau)):
        if tau[i][2] > stopping_thresh:
            stopping_idx = i
            break

    if stopping_idx < 6:
        return -1
    if stopping_idx == -1:
        return -1
    if stopping_idx >= 6:
        return 10.0 / max(1, stopping_idx - 5)

def predict(model, obs_tensor, env):
    actions, values = model.predict(observation=obs_tensor, deterministic=True,
                                    state=obs_tensor, attacker=False,
                                    infos={},
                                    env_config=env.env_config,
                                    env_configs=None, env=env,
                                    env_idx=0,
                                    env_state=env.env_state
                                    )
    return actions, values


if __name__ == '__main__':
    model_eval()
    # model_test()
