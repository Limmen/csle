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
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math

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
    emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip="172.18.9.191",
                                       agent_username="agent", agent_pw="agent", server_connection=True,
                                       server_private_key_file="/home/kim/.ssh/id_rsa",
                                       server_username="kim", port_forward_next_port=3000)
    emulation_config.skip_exploration = True
    env = gym.make("pycr-ctf-level-9-generated-sim-v5", env_config=None, emulation_config=emulation_config)
    load_path = "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_9/training/v5/generated_simulation/defender/results_backup/data/1619281840.2562084_0_50_policy_network.zip"
    model = initialize_model(env, load_path, "cpu:0", None)
    print("model loaded")


def action_pred_core_state_severe_warning(severe_alerts, warning_alerts, model):
    z = []
    for i in range(len(severe_alerts)):
        z1 = []
        for j in range(len(severe_alerts[i])):
            # state = np.array([warning_alerts[i][j]+severe_alerts[i][j],warning_alerts[i][j],severe_alerts[i][j],
            #                   2*severe_alerts[i][j] + warning_alerts[i][j],
            #                  warning_alerts[i][j]+severe_alerts[i][j],2*severe_alerts[i][j] + warning_alerts[i][j],severe_alerts[i][j],warning_alerts[i][j],0])
            state = np.array([0, 0, severe_alerts[i][j], warning_alerts[i][j],
                              0, 0, 0, 0, 0])
            #severe_alerts[i][j]+warning_alerts[i][j]
            #l_list = np.zeros(agent_config.num_nodes-1)
            #nodes_list = list(range(agent_config.num_nodes-1))
            #print("{}, {}, {}, {}".format(len(num_logged_in), len(num_logged_in[i]), i, j))
            # if severe_alerts[i][j] > 0:
            #     #l_nodes = random.randrange(num_logged_in[i][j])
            #     l_nodes = random.sample(nodes_list, int(round(severe_alerts[i][j])))
            #     l_list[l_nodes] = 1

            #state = state.reshape(agent_config.num_nodes-1, 12)

            #state = state.flatten()

            actions, values, log_prob = model.defender_policy.forward(torch.tensor(np.array([state])), deterministic=False,
                                                             mask_actions=None, env=None, infos=None)
            #obs_tensor = torch.tensor(np.array([state]))
            # actions, values = model.predict(observation=obs_tensor, deterministic=False,
            #                                 state=obs_tensor, attacker=False,
            #                                 infos={},
            #                                 env_config=env.env_config,
            #                                 env_configs=None, env=env,
            #                                 env_idx=0,
            #                                 env_state=env.env_state
            #                                 )
            #value_val = values.item()
            if actions.item() == 0:
                val = math.exp(log_prob.item())
            else:
                val = 1 - math.exp(log_prob.item())
            #val = actions.item()
            #action_mean, action_std, _ = model(torch.tensor(state, dtype=torch.float32), actor_only=False)
            # direction_mean = action_mean[1].item()
            #direction_mean = action_mean[0].item()
            # q_values = model(torch.tensor(state, dtype=torch.float32))
            # max_q = torch.argmax(q_values).item()
            z1.append(val)
        z.append(z1)
    z = np.array(z)
    return z

def plot():
    emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip="172.18.9.191",
                                       agent_username="agent", agent_pw="agent", server_connection=True,
                                       server_private_key_file="/home/kim/.ssh/id_rsa",
                                       server_username="kim", port_forward_next_port=3000)
    emulation_config.skip_exploration = True
    #env = gym.make("pycr-ctf-level-9-generated-sim-v5", env_config=None, emulation_config=emulation_config)
    env = None
    load_path = "/home/kim/storage/workspace/pycr/python-envs/minigames/network_intrusion/ctf/gym-pycr-ctf/examples/difficulty_level_9/training/v5/generated_simulation/defender/results_backup/data/1619281840.2562084_0_50_policy_network.zip"
    model = initialize_model(env, load_path, "cpu:0", None)
    # plot_value_logged_in(model, env)
    plot_stopping_num_alerts(model)
    plot_3d(model)

def plot_3d(model):
    num_severe_alerts_recent = np.arange(0, 200, 1)
    num_severe_alerts_total = np.arange(0, 200, 1)
    sev, warn = np.meshgrid(num_severe_alerts_recent, num_severe_alerts_total)
    action_val = action_pred_core_state_severe_warning(sev, warn, model)

    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts,amsmath}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['axes.titlepad'] = 8
    plt.rcParams['xtick.major.pad'] = 0.0
    plt.rcParams['ytick.major.pad'] = 0.0
    plt.rcParams['axes.labelpad'] = 0.0
    plt.rcParams['axes.linewidth'] = 0.05
    plt.rcParams.update({'font.size': 6.5})
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams.update({'font.size': 10})
    plt.rcParams.update({'figure.autolayout': True})

    #
    #fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(8, 5))
    fig, ax = plt.subplots(nrows=1, ncols=1, subplot_kw={'projection': '3d'}, figsize=(4.5,3))

    ax.plot_surface(num_severe_alerts_recent, num_severe_alerts_total, action_val, rstride=12, cstride=12,
                    cmap='cividis')

    ax.set_title(r"$\pi_{\theta}(\text{stop} | w_a, s_a)$", fontsize=12.5)
    ax.set_xlabel(r"warn alerts $w_a$")
    ax.set_ylabel(r"sev alerts $s_a$")
    ax.xaxis.labelpad = 0
    ax.yaxis.labelpad = 0
    ax.set_xticks(np.arange(0, 200 + 1, 50))
    ax.set_yticks(np.arange(0, 200+1, 50))
    xlab = ax.xaxis.get_label()
    ylab = ax.yaxis.get_label()
    xlab.set_size(11.5)
    ylab.set_size(11.5)
    ax.tick_params(axis='both', which='major', labelsize=10, length=2.2, width=0.6)
    ax.tick_params(axis='both', which='minor', labelsize=10, length=2.2, width=0.6)
    #plt.subplots_adjust(wspace=150, hspace=150, top=200, bottom=0.0)
    fig.tight_layout()
    #plt.subplots_adjust(wspace=150, hspace=150, top=200, bottom=0.0)
    fig.subplots_adjust(bottom=0.9)
    #plt.autoscale()
    #plt.subplots_adjust(bottom=0.55)
    plt.show()
    fig.savefig("alerts_stopping" + ".png", format="png", dpi=600)
    fig.savefig("alerts_stopping" + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)

def plot_stopping_num_alerts(model):
    num_alerts = np.arange(0, 400, 1)
    num_severe_alerts_recent = np.arange(0, 200, 1)
    num_severe_alerts_total = np.arange(0, 200, 1)
    x = []
    y = []
    for i in range(len(num_alerts)):
        state = np.array([0, 0, num_alerts[i], 0, 0, 0, 0, 0, 0])
        actions, values, log_prob = model.defender_policy.forward(torch.tensor(np.array([state])), deterministic=False,
                                                                  mask_actions=None, env=None, infos=None)
        if actions.item() == 0:
            val = math.exp(log_prob.item())
        else:
            val = 1 - math.exp(log_prob.item())
        x.append(i)
        y.append(val)

    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts,amsmath}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['axes.titlepad'] = 0.02
    # plt.rcParams['xtick.major.pad'] = 0.5
    plt.rcParams['ytick.major.pad'] = 0.05
    plt.rcParams['axes.labelpad'] = 0.8
    plt.rcParams['axes.linewidth'] = 0.1
    plt.rcParams.update({'font.size': 10})


    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(3.5,3.2))


    # ylims = (0, 920)

    # Plot Avg Eval rewards Gensim
    colors = plt.cm.viridis(np.linspace(0.3, 1, 2))[-2:]
    ax.plot(x,
            y, label=r"$\pi_{\theta}$ simulation",
            ls='-', color=colors[0])
    ax.fill_between(x,y, np.zeros(len(y)),
        alpha=0.35, color=colors[0])

    # if plot_opt:
    ax.plot(x,
            [0.5] * len(x), label=r"0.5",
            color="black",
            linestyle="dashed")


    ax.set_title(r"$\pi_{\theta}(\text{stop}|a)$", fontsize=12.5)
    ax.set_xlabel(r"\# Alerts $a$", fontsize=11.5)
    #ax.set_ylabel(r"$\mathbb{P}[\text{stop}|w]$", fontsize=12)
    ax.set_xlim(0, len(x))
    ax.set_ylim(0, 1.1)
    # ax.set_ylim(ylim_rew)

    # set the grid on
    ax.grid('on')

    # tweak the axis labels
    xlab = ax.xaxis.get_label()
    ylab = ax.yaxis.get_label()

    xlab.set_size(11.5)
    ylab.set_size(11.5)

    # change the color of the top and right spines to opaque gray
    ax.spines['right'].set_color((.8, .8, .8))
    ax.spines['top'].set_color((.8, .8, .8))

    # ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.18),
    #           ncol=2, fancybox=True, shadow=True)
    # ax.legend(loc="lower right")
    # ax.xaxis.label.set_size(13.5)
    # ax.yaxis.label.set_size(13.5)

    ttl = ax.title
    ttl.set_position([.5, 1.05])

    fig.tight_layout()
    # plt.show()
    # plt.subplots_adjust(wspace=0, hspace=0)
    fig.savefig("threshold_alerts" + ".png", format="png", dpi=600)
    fig.savefig("threshold_alerts" + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    # plt.close(fig)



def plot_value_logged_in(model, env):
    #num_sh = np.arange(0, 4, 1)
    num_severe_alerts_recent = np.arange(0, 200, 1)
    num_severe_alerts_total = np.arange(0, 200, 1)
    #num_sh = np.arange(0, 4, 0.1)
    #num_logged_in = np.arange(0, 4, 1)
    #num_logged_in = np.arange(0, agent_config.num_nodes-2, 1)
    #num_logged_in = np.arange(0, 4, 0.1)
    #theta = np.arange(-np.pi, np.pi, 0.1)
    #sh, logged_in = np.meshgrid(num_sh, num_logged_in)  # grid of point
    sev, warn = np.meshgrid(num_severe_alerts_recent, num_severe_alerts_total)
    action_val = action_pred_core_state_severe_warning(sev, warn, model)  # evaluation of the function on the grid

    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts,amsmath}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['axes.titlepad'] = 15
    # plt.rcParams['xtick.major.pad'] = 0.5
    #plt.rcParams['ytick.major.pad'] = 0.05
    plt.rcParams['axes.labelpad'] = 10
    plt.rcParams['axes.linewidth'] = 0.1
    plt.rcParams.update({'font.size': 6.5})
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
    plt.rcParams['font.family'] = ['serif']
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams.update({'font.size': 10})

    #figsize=(8,5)
    fig, ax = plt.subplots(nrows=1, ncols=1, subplot_kw={'projection': '3d'})

    ax.plot_surface(num_severe_alerts_recent, num_severe_alerts_total, action_val, rstride=12, cstride=12, cmap='cividis')

    ax.set_title(r"$\pi_{\theta}(stop | w_a, s_a)$", fontsize=16)
    ax.set_xlabel(r"warning alerts $w_a$")
    ax.set_ylabel(r"severe alerts $s_a$")
    xlab = ax.xaxis.get_label()
    ylab = ax.yaxis.get_label()
    xlab.set_size(14)
    ylab.set_size(14)
    ax.tick_params(axis='both', which='major', labelsize=10, length=2.2, width=0.6)
    ax.tick_params(axis='both', which='minor', labelsize=10, length=2.2, width=0.6)
    fig.tight_layout()
    plt.show()
    plt.subplots_adjust(wspace=0, hspace=0, top=80)
    fig.savefig("alerts_stopping" + ".png", format="png", dpi=600)
    fig.savefig("alerts_stopping" + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    #plt.close(fig)


if __name__ == '__main__':
    plot()
    #model_eval()
    # model_test()
