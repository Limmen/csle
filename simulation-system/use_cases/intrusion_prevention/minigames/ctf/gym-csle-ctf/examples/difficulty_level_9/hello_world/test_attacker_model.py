from csle_common.agents.policy_gradient.ppo_baseline.impl.ppo.ppo import PPO
import torch
import numpy as np
import matplotlib.pyplot as plt
import math
from csle_common.dao.network.trajectory import Trajectory

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
    # emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}9.191",
    #                                    agent_username="agent", agent_pw="agent", server_connection=True,
    #                                    server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                    server_username="kim", port_forward_next_port=3000)
    # emulation_config.skip_exploration = True
    # env = gym.make("csle-ctf-level-9-generated-sim-v5", env_config=None, emulation_config=emulation_config)
    env = None
    #load_path = "/Users/kimham/workspace/csle/simulation-system/minigames/network_intrusion/ctf/gym-csle-ctf/examples/difficulty_level_9/results/data/888/1618647459.4010603_888_600_policy_network.zip"
    load_path = "/home/kim/storage/workspace/csle/simulation-system/minigames/network_intrusion/ctf/gym-csle-ctf/examples/difficulty_level_9/hello_world/results/data/888/1618550590.298014_888_225_policy_network.zip"
    load_path = "/home/kim/storage/workspace/csle/simulation-system/minigames/network_intrusion/ctf/gym-csle-ctf/examples/difficulty_level_9/hello_world/results/data/888/1618556447.9984174_888_250_policy_network.zip"
    load_path = "/home/kim/storage/workspace/csle/simulation-system/minigames/network_intrusion/ctf/gym-csle-ctf/examples/difficulty_level_9/hello_world/results/data/888/1618544521.276592_888_200_policy_network.zip"
    load_path = "/home/kim/storage/workspace/csle/simulation-system/minigames/network_intrusion/ctf/gym-csle-ctf/examples/difficulty_level_9/hello_world/results/data/235/1618650142.70875_235_250_policy_network.zip"
    load_path = "/home/kim/storage/workspace/csle/simulation-system/minigames/network_intrusion/ctf/gym-csle-ctf/examples/difficulty_level_9/hello_world/results/data/210/1618555562.3001144_210_250_policy_network.zip"
    load_path = "/home/kim/storage/workspace/csle/simulation-system/minigames/network_intrusion/ctf/gym-csle-ctf/examples/difficulty_level_9/hello_world/results/data/210/1618550587.747856_210_225_policy_network.zip"
    load_path = "/home/kim/storage/workspace/csle/simulation-system/minigames/network_intrusion/ctf/gym-csle-ctf/examples/difficulty_level_9/hello_world/results/data/210/1618545468.4964974_210_200_policy_network.zip"
    load_path = "/home/kim/storage/workspace/csle/simulation-system/minigames/network_intrusion/ctf/gym-csle-ctf/examples/difficulty_level_9/hello_world/results/data/52112/1618629744.766635_52112_250_policy_network.zip"
    load_path = "/home/kim/storage/workspace/csle/simulation-system/minigames/network_intrusion/ctf/gym-csle-ctf/examples/difficulty_level_9/hello_world/results/data/52112/1618642987.5118797_52112_275_policy_network.zip"
    #load_path = "/home/kim/storage/workspace/csle/simulation-system/minigames/network_intrusion/ctf/gym-csle-ctf/examples/difficulty_level_9/hello_world/results/data/52112/1618616492.3097079_52112_225_policy_network.zip"
    model = initialize_model(env, load_path, "cpu:0", None)
    print("model loaded")
    plot_value_fun(model)
    #plot_initial_state_dist(model)

def plot_value_fun(model):
    print("test")
    states = load_states()

    x = []
    y = []
    for i in range(len(states)):
        latent_pi, latent_vf = model.attacker_policy._get_latent(torch.tensor(np.array([states[i]])))
        values = model.attacker_policy.value_net(latent_vf)
        print(values)
        x.append(i)
        y.append(values.item())
    print(y)

    cm = plt.cm.get_cmap('RdYlBu_r')
    num_colors = 5
    fontsize = 6.5
    file_name = "value_fun_attacker"
    labelsize = 6
    colors = plt.cm.GnBu(np.linspace(0.3, 1, num_colors))[-num_colors:]
    colors = plt.cm.viridis(np.linspace(0.3, 1, num_colors))[-num_colors:]
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts,amsmath}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['axes.titlepad'] = 0.02
    # plt.rcParams['xtick.major.pad'] = 0.5
    plt.rcParams['ytick.major.pad'] = 0.05
    plt.rcParams['axes.labelpad'] = 0.8
    plt.rcParams['axes.linewidth'] = 0.1
    plt.rcParams.update({'font.size': fontsize})

    colors = plt.cm.viridis(np.linspace(0.3, 1, 4))[-4:]
    # plt.rcParams['font.serif'] = ['Times New Roman']
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(3.75,1.3))

    ax.plot(x, y, label=r"$V^{\pi_{\theta^A}}$",
                  marker="s", ls='-', color=colors[2],
                  markevery=5, markersize=2, lw=0.5)
    #ax[0][2].grid('on')
    ax.set_xlabel(r"Time-step $t$", fontsize=labelsize)
    xlab = ax.xaxis.get_label()
    ylab = ax.yaxis.get_label()
    xlab.set_size(labelsize)
    ylab.set_size(fontsize)
    ax.tick_params(axis='both', which='major', labelsize=labelsize -1.5, length=2.2, width=0.6)
    ax.tick_params(axis='both', which='minor', labelsize=labelsize -1.5, length=2.2, width=0.6)
    #ax.set_ylim(-150, 110)
    ax.set_xlim(0, len(states))
    ax.set_title(r"$V^{\pi_{\theta^A}}(s_t)$", fontsize=fontsize)
    # fig.patch.set_visible(False)
    # ax.axis('off')
    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    fig.tight_layout()
    #fig.subplots_adjust(wspace=0.18, hspace=0.22)
    # hspace=hspace, top=top
    #plt.show()
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)

    # ax[0][2].fill_between(
    #     np.array(
    #         list(range(len(attacker_avg_train_rewards_means_v1[::sample_step])))) * sample_step * iterations_per_step,
    #     attacker_avg_train_rewards_means_v1[::sample_step] - attacker_avg_train_rewards_stds_v1[::sample_step],
    #     attacker_avg_train_rewards_means_v1[::sample_step] + attacker_avg_train_rewards_stds_v1[::sample_step],
    #     alpha=0.35, color="r")




def plot_initial_state_dist(model):
    #state = initial_state()
    #state = state_2()
    #state = state_13()
    #state= state_1()
    #state = state_38()
    states = load_states()
    state1 =states[1]

    latent_pi, latent_vf = model.attacker_policy._get_latent(torch.tensor(np.array([state1])))
    dist1 = model.attacker_policy._get_action_dist_from_latent(latent_pi, non_legal_actions=[])
    action1 = dist1.distribution.sample()
    print(action1)
    x1 = []
    y1 = []
    for i in range(372):
        x1.append(i)
        y1.append(math.exp(dist1.distribution.log_prob(torch.tensor(i))))
    print("y1 top 10: {}".format([i[0] for i in sorted(enumerate(y1), key=lambda x:x[1])][-10:]))

    state2 = states[2]
    latent_pi, latent_vf = model.attacker_policy._get_latent(torch.tensor(np.array([state2])))
    dist2 = model.attacker_policy._get_action_dist_from_latent(latent_pi, non_legal_actions=[action1])
    action2 = dist2.distribution.sample()
    print(action2)
    x2 = []
    y2 = []
    for i in range(372):
        x2.append(i)
        y2.append(math.exp(dist2.distribution.log_prob(torch.tensor(i))))
    print("y2 top 10: {}".format([i[0] for i in sorted(enumerate(y2), key=lambda x: x[1])][-10:]))

    state3 = states[3]
    latent_pi, latent_vf = model.attacker_policy._get_latent(torch.tensor(np.array([state3])))
    dist3 = model.attacker_policy._get_action_dist_from_latent(latent_pi, non_legal_actions=[action1, action2])
    action3 = dist3.distribution.sample()
    print(action3)
    x3 = []
    y3 = []
    for i in range(372):
        x3.append(i)
        y3.append(math.exp(dist3.distribution.log_prob(torch.tensor(i))))
    print("y3 top 10: {}".format([i[0] for i in sorted(enumerate(y3), key=lambda x: x[1])][-10:]))

    state4 = states[4]
    latent_pi, latent_vf = model.attacker_policy._get_latent(torch.tensor(np.array([state4])))
    dist4 = model.attacker_policy._get_action_dist_from_latent(latent_pi, non_legal_actions=[action1, action2, action3])
    action4 = dist4.distribution.sample()
    print(action4)
    x4 = []
    y4 = []
    for i in range(372):
        x4.append(i)
        y4.append(math.exp(dist4.distribution.log_prob(torch.tensor(i))))
    print("y4 top 10: {}".format([i[0] for i in sorted(enumerate(y4), key=lambda x: x[1])][-10:]))


    state5 = states[5]
    latent_pi, latent_vf = model.attacker_policy._get_latent(torch.tensor(np.array([state5])))
    dist5 = model.attacker_policy._get_action_dist_from_latent(latent_pi, non_legal_actions=[action1, action2, action3, action4])
    action5 = dist5.distribution.sample()
    print(action5)
    x5 = []
    y5 = []
    for i in range(372):
        x5.append(i)
        y5.append(math.exp(dist5.distribution.log_prob(torch.tensor(i))))
    print("y5 top 10: {}".format([i[0] for i in sorted(enumerate(y5), key=lambda x: x[1])][-10:]))

    state6 = states[6]
    latent_pi, latent_vf = model.attacker_policy._get_latent(torch.tensor(np.array([state6])))
    dist6 = model.attacker_policy._get_action_dist_from_latent(latent_pi,
                                                               non_legal_actions=[action1, action2, action3, action4,
                                                                                  action5])
    action6 = dist6.distribution.sample()
    print(action6)
    x6 = []
    y6 = []
    for i in range(372):
        x6.append(i)
        y6.append(math.exp(dist6.distribution.log_prob(torch.tensor(i))))
    print("y6 top 10: {}".format([i[0] for i in sorted(enumerate(y6), key=lambda x: x[1])][-10:]))

    state7 = states[7]
    latent_pi, latent_vf = model.attacker_policy._get_latent(torch.tensor(np.array([state7])))
    dist7 = model.attacker_policy._get_action_dist_from_latent(latent_pi,
                                                               non_legal_actions=[action1, action2, action3, action4,
                                                                                  action5, action6])
    action7 = dist7.distribution.sample()
    print(action7)
    x7 = []
    y7 = []
    for i in range(372):
        x7.append(i)
        y7.append(math.exp(dist7.distribution.log_prob(torch.tensor(i))))
    print("y7 top 10: {}".format([i[0] for i in sorted(enumerate(y7), key=lambda x: x[1])][-10:]))

    state8 = states[8]
    latent_pi, latent_vf = model.attacker_policy._get_latent(torch.tensor(np.array([state8])))
    dist8 = model.attacker_policy._get_action_dist_from_latent(latent_pi,
                                                               non_legal_actions=[action1, action2, action3, action4,
                                                                                  action5, action6, action7])
    action8 = dist8.distribution.sample()
    print(action8)
    x8 = []
    y8 = []
    for i in range(372):
        x8.append(i)
        y8.append(math.exp(dist8.distribution.log_prob(torch.tensor(i))))
    print("y8 top 10: {}".format([i[0] for i in sorted(enumerate(y8), key=lambda x: x[1])][-10:]))

    state9 = states[9]
    latent_pi, latent_vf = model.attacker_policy._get_latent(torch.tensor(np.array([state9])))
    dist9 = model.attacker_policy._get_action_dist_from_latent(latent_pi,
                                                               non_legal_actions=[action1, action2, action3, action4,
                                                                                  action5, action6, action7, action8])
    action9 = dist9.distribution.sample()
    print(action9)
    x9 = []
    y9 = []
    for i in range(372):
        x9.append(i)
        y9.append(math.exp(dist9.distribution.log_prob(torch.tensor(i))))
    print("y9 top 10: {}".format([i[0] for i in sorted(enumerate(y9), key=lambda x: x[1])][-10:]))


    # actions, values, log_prob, dist = model.attacker_policy.forward(torch.tensor(np.array([state])),
    #                                                                 deterministic=False,
    #                                                                 mask_actions=None, env=None, infos=None,
    #                                                                 return_distribution=True)

    print("max actions")
    #print(actions)
    cm = plt.cm.get_cmap('RdYlBu_r')
    num_colors = 5
    fontsize = 6.5
    file_name = "test_attacker_model"
    labelsize = 6
    colors = plt.cm.GnBu(np.linspace(0.3, 1, num_colors))[-num_colors:]
    colors = plt.cm.viridis(np.linspace(0.3, 1, num_colors))[-num_colors:]

    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['axes.titlepad'] = 0.02
    plt.rcParams['xtick.major.pad'] = 0.0
    plt.rcParams['ytick.major.pad'] = 0.05
    plt.rcParams['axes.labelpad'] = 0.0
    plt.rcParams['axes.linewidth'] = 0.1
    plt.rcParams.update({'font.size': fontsize})
    fig, ax = plt.subplots(nrows=3, ncols=3, figsize=(3.75, 3.4))
    colors = plt.cm.viridis(np.linspace(0.3, 1, 4))[-4:]

    ax[0][0].bar(x1, y1, alpha=1,
             label="test", color=colors[0], edgecolor=colors[0], ls="-")
    #ax[0][0].grid('on')
    #ax[0][0].set_ylabel(r"\pi_{\theta^A}(a|s_1)", fontsize=labelsize)
    #ax[0][0].set_xlabel(r"action $a$", fontsize=labelsize)
    ax[0][0].tick_params(axis='both', which='major', labelsize=labelsize-1.5, length=1.2, width=0.2)
    ax[0][0].tick_params(axis='both', which='minor', labelsize=labelsize-1.5, length=1.2, width=0.2)
    #ax[0][0].set_yticks([])
    #ax[0][0].set_ylim(0, 1)
    ax[0][0].set_xlim(0, 372)
    ax[0][0].set_title(r"$\pi_{\theta^A}(a|s_1)$", fontsize=fontsize)

    ax[0][1].bar(x2, y2, alpha=1,
                 label="test", color=colors[0], edgecolor=colors[0], ls="-")
    # ax[0][0].grid('on')
    # ax[0][0].set_ylabel(r"\pi_{\theta^A}(a|s_1)", fontsize=labelsize)
    #ax[0][1].set_xlabel(r"action $a$", fontsize=labelsize)
    ax[0][1].tick_params(axis='both', which='major', labelsize=labelsize-1.5, length=1.2, width=0.2)
    ax[0][1].tick_params(axis='both', which='minor', labelsize=labelsize-1.5, length=1.2, width=0.2)
    #ax[0][1].set_yticks([])
    #ax[0][1].set_ylim(0, 1)
    ax[0][1].set_xlim(0, 372)
    ax[0][1].set_title(r"$\pi_{\theta^A}(a|s_2)$", fontsize=fontsize)

    ax[0][2].bar(x3, y3, alpha=1,
                 label="test", color=colors[0], edgecolor=colors[0], ls="-")
    #ax[0][2].set_xlabel(r"action $a$", fontsize=labelsize)
    ax[0][2].tick_params(axis='both', which='major', labelsize=labelsize-1.5, length=1.2, width=0.2)
    ax[0][2].tick_params(axis='both', which='minor', labelsize=labelsize-1.5, length=1.2, width=0.2)
    #ax[0][2].set_yticks([])
    #ax[0][2].set_ylim(0, 1)
    ax[0][2].set_xlim(0, 372)
    ax[0][2].set_title(r"$\pi_{\theta^A}(a|s_3)$", fontsize=fontsize)

    ax[1][0].bar(x4, y4, alpha=1,
                 label="test", color=colors[0], edgecolor=colors[0], ls="-")
    #ax[1][0].set_xlabel(r"action $a$", fontsize=labelsize)
    ax[1][0].tick_params(axis='both', which='major', labelsize=labelsize - 1.5, length=1.2, width=0.2)
    ax[1][0].tick_params(axis='both', which='minor', labelsize=labelsize - 1.5, length=1.2, width=0.2)
    #ax[1][0].set_yticks([])
    #ax[1][0].set_ylim(0, 1)
    ax[1][0].set_xlim(0, 372)
    ax[1][0].set_title(r"$\pi_{\theta^A}(a|s_4)$", fontsize=fontsize)

    ax[1][1].bar(x5, y5, alpha=1,
                 label="test", color=colors[0], edgecolor=colors[0], ls="-")
    #ax[1][1].set_xlabel(r"action $a$", fontsize=labelsize)
    ax[1][1].tick_params(axis='both', which='major', labelsize=labelsize - 1.5, length=1.2, width=0.2)
    ax[1][1].tick_params(axis='both', which='minor', labelsize=labelsize - 1.5, length=1.2, width=0.2)
    #ax[1][1].set_yticks([])
    #ax[1][1].set_ylim(0, 1)
    ax[1][1].set_xlim(0, 372)
    ax[1][1].set_title(r"$\pi_{\theta^A}(a|s_5)$", fontsize=fontsize)

    ax[1][2].bar(x6, y6, alpha=1,
                 label="test", color=colors[0], edgecolor=colors[0], ls="-")
    #ax[1][2].set_xlabel(r"action $a$", fontsize=labelsize)
    ax[1][2].tick_params(axis='both', which='major', labelsize=labelsize - 1.5, length=1.2, width=0.2)
    ax[1][2].tick_params(axis='both', which='minor', labelsize=labelsize - 1.5, length=1.2, width=0.2)
    #ax[1][2].set_yticks([])
    #ax[1][2].set_ylim(0, 1)
    ax[1][2].set_xlim(0, 372)
    ax[1][2].set_title(r"$\pi_{\theta^A}(a|s_6)$", fontsize=fontsize)

    ax[2][0].bar(x7, y7, alpha=1,
                 label="test", color=colors[0], edgecolor=colors[0], ls="-")
    ax[2][0].set_xlabel(r"action $a$", fontsize=labelsize)
    ax[2][0].tick_params(axis='both', which='major', labelsize=labelsize - 1.5, length=1.2, width=0.2)
    ax[2][0].tick_params(axis='both', which='minor', labelsize=labelsize - 1.5, length=1.2, width=0.2)
    #ax[2][0].set_yticks([])
    #ax[2][0].set_ylim(0, 1)
    ax[2][0].set_xlim(0, 372)
    ax[2][0].set_title(r"$\pi_{\theta^A}(a|s_7)$", fontsize=fontsize)

    ax[2][1].bar(x8, y8, alpha=1,
                 label="test", color=colors[0], edgecolor=colors[0], ls="-")
    ax[2][1].set_xlabel(r"action $a$", fontsize=labelsize)
    ax[2][1].tick_params(axis='both', which='major', labelsize=labelsize - 1.5, length=1.2, width=0.2)
    ax[2][1].tick_params(axis='both', which='minor', labelsize=labelsize - 1.5, length=1.2, width=0.2)
    #ax[2][1].set_yticks([])
    #ax[2][1].set_ylim(0, 1)
    ax[2][1].set_xlim(0, 372)
    ax[2][1].set_title(r"$\pi_{\theta^A}(a|s_8)$", fontsize=fontsize)

    ax[2][2].bar(x9, y9, alpha=1,
                 label="test", color=colors[0], edgecolor=colors[0], ls="-")
    ax[2][2].set_xlabel(r"action $a$", fontsize=labelsize)
    ax[2][2].tick_params(axis='both', which='major', labelsize=labelsize - 1.5, length=1.2, width=0.2)
    ax[2][2].tick_params(axis='both', which='minor', labelsize=labelsize - 1.5, length=1.2, width=0.2)
    #ax[2][2].set_yticks([])
    #ax[2][2].set_ylim(0, 1)
    ax[2][2].set_xlim(0, 372)
    ax[2][2].set_title(r"$\pi_{\theta^A}(a|s_9)$", fontsize=fontsize)

    fig.tight_layout()
    fig.subplots_adjust(wspace=0.18, hspace=0.22)
    #hspace=hspace, top=top
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)

def initial_state():
    state = np.zeros((1 + (20)*33))
    return state

def state_2():
    state = np.array([[2.0, 1.0, 0.0, 0.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 4.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]])
    return state

def state_1():
    state = np.array([1.0, 1.0, 0.0, 0.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 4.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    return state

def state_13():
    state = np.array([13.0, 1.0, 1.0, 1.0, 3.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 2.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 4.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    return state

def state_38():
    state = np.array([38.0, 1.0, 1.0, 1.0, 3.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 4.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 2.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 7.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    return state

def load_states():
    save_dynamics_model_dir = "/home/kim/storage/workspace/csle/simulation-system/minigames/network_intrusion/ctf/gym-csle-ctf/examples/difficulty_level_9/hello_world/"
    #"/Users/kimham/workspace/csle/simulation-system/minigames/network_intrusion/ctf/gym-csle-ctf/examples/difficulty_level_9/hello_world/"
    trajectories = Trajectory.load_trajectories(save_dynamics_model_dir, trajectories_file="taus3.json")
    trajectory = trajectories[10]
    observations = trajectory.attacker_observations
    print("actions:{}".format(trajectory.attacker_actions))
    observations = np.array(observations)
    return observations


if __name__ == '__main__':
    #plot()
    model_test()
