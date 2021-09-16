from pycr_common.agents.config.agent_config import AgentConfig
from gym_pycr_ctf.envs_model.config.generator.env_config_generator import EnvConfigGenerator
from pycr_common.dao.network.emulation_config import EmulationConfig
from pycr_common.agents.policy_gradient.ppo_baseline.impl.ppo.ppo import PPO
from gym_pycr_ctf.util.experiments_util import util
import gym
import numpy as np
import random
import torch
import matplotlib.pyplot as plt


def load_model(env, agent_config: AgentConfig, load_path: str, device: str):
    model = PPO.load(env=env, load_path=load_path, device=device,
                          agent_config=agent_config)
    return model


def create_env():
    containers_configs = EnvConfigGenerator.get_all_envs_containers_config(
        "/home/kim/pycr/emulation-envs/minigames/network_intrusion/ctf/001/random_many/")
    flags_configs = EnvConfigGenerator.get_all_envs_flags_config(
        "/home/kim/pycr/emulation-envs/minigames/network_intrusion/ctf/001/random_many/")
    eval_containers_configs = EnvConfigGenerator.get_all_envs_containers_config(
        "/home/kim/pycr/emulation-envs/minigames/network_intrusion/ctf/001/random_many_2/")
    eval_flags_configs = EnvConfigGenerator.get_all_envs_flags_config(
        "/home/kim/pycr/emulation-envs/minigames/network_intrusion/ctf/001/random_many_2/")
    max_num_nodes_train = max(list(map(lambda x: len(x.containers), containers_configs)))
    max_num_nodes_eval = max(list(map(lambda x: len(x.containers), eval_containers_configs)))
    max_num_nodes = max(max_num_nodes_train, max_num_nodes_eval)
    num_nodes = max_num_nodes - 1
    n_envs = 1
    agent_config = AgentConfig(gamma=0.99, alpha=0.00005, epsilon=1, render=False, eval_sleep=0.0,
                               min_epsilon=0.01, eval_episodes=1, train_log_frequency=1,
                               epsilon_decay=0.9999, video=False, eval_log_frequency=1,
                               video_fps=5, video_dir=util.default_output_dir() + "/results/videos",
                               num_iterations=50,
                               eval_render=False, gifs=True,
                               gif_dir=util.default_output_dir() + "/results/gifs",
                               eval_frequency=100, video_frequency=10,
                               save_dir=util.default_output_dir() + "/results/data",
                               checkpoint_freq=500,
                               input_dim=num_nodes * 12,
                               # input_dim=7,
                               # input_dim=11 * 8,
                               # output_dim=9,
                               output_dim=9 + (3 * num_nodes),
                               pi_hidden_dim=64, pi_hidden_layers=1,
                               vf_hidden_dim=64, vf_hidden_layers=1,
                               shared_hidden_layers=2, shared_hidden_dim=64,
                               # batch_size=util.round_batch_size(int(2000/n_envs)),
                               batch_size=500,
                               gpu=False, tensorboard=True,
                               tensorboard_dir=util.default_output_dir() + "/results/tensorboard",
                               optimizer="Adam", lr_exp_decay=False, lr_decay_rate=0.999,
                               state_length=1, gpu_id=0, sde_sample_freq=4, use_sde=False,
                               lr_progress_decay=False, lr_progress_power_decay=4, ent_coef=0.0005,
                               vf_coef=0.5, features_dim=512, gae_lambda=0.95, max_gradient_norm=0.5,
                               eps_clip=0.2, optimization_iterations=10,
                               render_steps=100, illegal_action_logit=-100,
                               filter_illegal_actions=False, train_progress_deterministic_eval=True,
                               n_deterministic_eval_iter=1, eval_deterministic=False,
                               num_nodes=max_num_nodes
                               )

    idx = 1
    print("ip:{}".format(containers_configs[idx].agent_ip))
    # emulation_config = emulationConfig(server_ip="172.31.212.92", agent_ip=containers_configs[idx].agent_ip,
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")
    emulation_config = EmulationConfig(agent_ip=containers_configs[idx].agent_ip, agent_username="agent", agent_pw="agent",
                                     server_connection=False, port_forward_next_port=9800)
    env_name = "pycr-ctf-random-many-emulation-v1"
    env = gym.make(env_name, env_config=None, emulation_config=emulation_config,
                   containers_configs=containers_configs, flags_configs=flags_configs, idx=idx,
                   num_nodes=max_num_nodes)
    return env, agent_config

def value_pred_essential_state_loggedin_shell(num_sh, num_logged_in, agent_config: AgentConfig, model):
    z = []
    for i in range(len(num_logged_in)):
        z1 = []
        for j in range(len(num_logged_in[i])):
            state = np.zeros(agent_config.input_dim)
            sh_list = np.zeros(agent_config.num_nodes-1)
            l_list = np.zeros(agent_config.num_nodes-1)
            nodes_list = list(range(agent_config.num_nodes-1))
            #print("{}, {}, {}, {}".format(len(num_logged_in), len(num_logged_in[i]), i, j))
            if num_logged_in[i][j] > 0:
                #l_nodes = random.randrange(num_logged_in[i][j])
                l_nodes = random.sample(nodes_list, int(round(num_sh[i][j])))
                l_list[l_nodes] = 1

            if num_sh[i][j] > 0:
                # sh_nodes = random.randrange(num_sh[i][j])
                sh_nodes = random.sample(nodes_list, int(round(num_sh[i][j])))
                sh_list[sh_nodes] = 1

            state = state.reshape(agent_config.num_nodes-1, 12)

            for k in range(agent_config.num_nodes-1):
                if sh_list[k] == 1:
                    state[k][0] = 1 # m found
                    state[k][1] = 1 # shell access
                    state[k][2] = 0 # logged in
                    state[k][3] = 2 # num open ports
                    state[k][4] = 0 # flag pts
                    state[k][5] = 0 # fs searched
                    state[k][6] = 1 # untried credentials
                    state[k][7] = 1 # ssh brute tried
                    state[k][8] = 1 # telnet brute tried
                    state[k][9] = 1  # ftp brute tried
                    state[k][10] = 0 # backdoor installed
                    state[k][11] = 0 # tools installed

                if l_list[k] == 1:
                    state[k][0] = 1 # m found
                    state[k][1] = 1 # shell access
                    state[k][2] = 1 # logged in
                    state[k][3] = 2 # num open ports
                    state[k][4] = 0 # flag pts
                    state[k][5] = 0 # fs searched
                    state[k][6] = 1 # untried credentials
                    state[k][7] = 1 # ssh brute tried
                    state[k][8] = 1 # telnet brute tried
                    state[k][9] = 1  # ftp brute tried
                    state[k][10] = 1 # backdoor installed
                    state[k][11] = 0 # tools installed

            state = state.flatten()

            actions, values, log_prob = model.policy.forward(torch.tensor(np.array([state])), deterministic=False,
                                                             mask_actions=None, env=None, infos=None)
            state_val = values.item()
            #action_mean, action_std, _ = model(torch.tensor(state, dtype=torch.float32), actor_only=False)
            # direction_mean = action_mean[1].item()
            #direction_mean = action_mean[0].item()
            # q_values = model(torch.tensor(state, dtype=torch.float32))
            # max_q = torch.argmax(q_values).item()
            z1.append(state_val)
        z.append(z1)
    z = np.array(z)
    return z


def value_pred_essential_state_loggedin(num_logged_in, agent_config: AgentConfig, model):
    z = []
    for i in range(len(num_logged_in)):
        z1 = []
        for j in range(len(num_logged_in[i])):
            state = np.zeros(agent_config.input_dim)
            l_list = np.zeros(agent_config.num_nodes-1)
            nodes_list = list(range(agent_config.num_nodes-1))
            #print("{}, {}, {}, {}".format(len(num_logged_in), len(num_logged_in[i]), i, j))
            if num_logged_in[i][j] > 0:
                #l_nodes = random.randrange(num_logged_in[i][j])
                l_nodes = random.sample(nodes_list, int(round(num_logged_in[i][j])))
                l_list[l_nodes] = 1

            state = state.reshape(agent_config.num_nodes-1, 12)

            for k in range(agent_config.num_nodes-1):
                if l_list[k] == 1:
                    state[k][0] = 1 # m found
                    state[k][1] = 1 # shell access
                    state[k][2] = 1 # logged in
                    state[k][3] = 2 # num open ports
                    state[k][4] = 0 # flag pts
                    state[k][5] = 0 # fs searched
                    state[k][6] = 1 # untried credentials
                    state[k][7] = 1 # ssh brute tried
                    state[k][8] = 1 # telnet brute tried
                    state[k][9] = 1  # ftp brute tried
                    state[k][10] = 1 # backdoor installed
                    state[k][11] = 0 # tools installed

            state = state.flatten()

            actions, values, log_prob = model.policy.forward(torch.tensor(np.array([state])), deterministic=False,
                                                             mask_actions=None, env=None, infos=None)
            state_val = values.item()
            #action_mean, action_std, _ = model(torch.tensor(state, dtype=torch.float32), actor_only=False)
            # direction_mean = action_mean[1].item()
            #direction_mean = action_mean[0].item()
            # q_values = model(torch.tensor(state, dtype=torch.float32))
            # max_q = torch.argmax(q_values).item()
            z1.append(state_val)
        z.append(z1)
    z = np.array(z)
    return z

def value_fun_plot_sh_logged(agent_config: AgentConfig, model):
    #num_sh = np.arange(0, 4, 1)
    num_sh = np.arange(0, agent_config.num_nodes-1, 1)
    #num_sh = np.arange(0, 4, 0.1)
    #num_logged_in = np.arange(0, 4, 1)
    num_logged_in = np.arange(0, agent_config.num_nodes-1, 1)
    #num_logged_in = np.arange(0, 4, 0.1)
    #theta = np.arange(-np.pi, np.pi, 0.1)
    sh, logged_in = np.meshgrid(num_sh, num_logged_in)  # grid of point
    state_val = value_pred_essential_state_loggedin_shell(sh, logged_in, agent_config, model)  # evaluation of the function on the grid

    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    plt.rcParams.update({'font.size': 12})
    fig, ax = plt.subplots(nrows=1, ncols=1, subplot_kw={'projection': '3d'})
    # ax.plot_wireframe(X, Y, Z, rstride=40, cstride=40)
    ax.plot_surface(sh, logged_in, state_val, rstride=12, cstride=12, cmap='viridis_r')
    ax.set_title(r"$V_{\phi}(s)$")
    ax.set_xlabel(r"$v$", fontsize=20)
    ax.set_ylabel(r"$c$", fontsize=20)
    fig.tight_layout()
    fig.savefig("ppo_state_val_sh_logged" + ".png", format="png", dpi=600)
    fig.savefig("ppo_state_val_sh_logged" + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    plt.show()


def plot_value_logged_in(agent_config: AgentConfig, model):
    #num_sh = np.arange(0, 4, 1)
    num_sh = [0]
    #num_sh = np.arange(0, 4, 0.1)
    #num_logged_in = np.arange(0, 4, 1)
    num_logged_in = np.arange(0, agent_config.num_nodes-2, 1)
    #num_logged_in = np.arange(0, 4, 0.1)
    #theta = np.arange(-np.pi, np.pi, 0.1)
    sh, logged_in = np.meshgrid(num_sh, num_logged_in)  # grid of point
    state_val = value_pred_essential_state_loggedin(logged_in, agent_config, model)  # evaluation of the function on the grid

    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 4))
    plt.rcParams.update({'font.size': 12})

    ax.plot(num_logged_in,
            state_val, label=r"$c$", marker="o", ls='-', color="r",
            markevery=1)

    #ax.plot(np.array(list(range(len(state_val)))),
     #       r_2, label=label_2, marker="o", ls='-', color="#661D98",
            #markevery=markevery)
    #
    # ax.plot(np.array(list(range(len(r_3)))),
    #         r_3, label=r"$\lambda={},\alpha=0.001$".format(lamb), marker="o", ls='-', color="#599ad3",
    #         markevery=markevery)
    #
    # ax.plot(np.array(list(range(len(r_4)))),
    #         r_4, label=r"$\lambda={},\alpha =0.0001$".format(lamb), marker="o", ls='-', color="#f9a65a",
    #         markevery=markevery)

    ax.set_title(r"State values versus number of compromised nodes")
    ax.set_xlabel(r"$c$", fontsize=20)
    ax.set_ylabel(r"$V(s)$", fontsize=20)
    # ax.set_xlim(0, len(state_values))
    # ax[0].set_ylim(0, 0.75)

    # set the grid on
    ax.grid('on')

    # tweak the axis labels
    xlab = ax.xaxis.get_label()
    ylab = ax.yaxis.get_label()

    xlab.set_size(10)
    ylab.set_size(10)

    # change the color of the top and right spines to opaque gray
    ax.spines['right'].set_color((.8, .8, .8))
    ax.spines['top'].set_color((.8, .8, .8))

    # ax.legend(loc="lower right")
    ax.xaxis.label.set_size(13.5)
    ax.yaxis.label.set_size(13.5)

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.18),
              ncol=2, fancybox=True, shadow=True)

    # ax[0].set_ylim(0, 1)
    # ax[1].set_ylim(0, 1)
    # ax[2].set_ylim(0, 1)

    fig.tight_layout()
    plt.show()
    plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig("logged_in_val_fun" + ".png", format="png", dpi=600)
    fig.savefig("logged_in_val_fun" + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    #plt.close(fig)

if __name__ == '__main__':
    env, agent_config = create_env()
    load_path = "/home/kim/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/random_many/training/v1/emulation/ppo_baseline/results/data/0/1609769574.4061646_policy_network.zip"
    device="cpu"
    model = load_model(env=env, load_path=load_path, device=device, agent_config=agent_config)
    print("model loaded")
    #test_input = np.zeros(agent_config.input_dim)
    #actions, values, log_prob = model.policy.forward(torch.tensor(np.array([test_input])), deterministic = False, mask_actions = None, env=None, infos=None)
    #print("values:{}".format(values))
    #value_fun_plot_sh_logged(agent_config, model)
    plot_value_logged_in(agent_config, model)