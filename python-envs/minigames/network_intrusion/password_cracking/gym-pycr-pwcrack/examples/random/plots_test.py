import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob


def read_data():
    base_path = "/home/kim/pycr/python-envs/minigames/network_intrusion/password_cracking/gym-pycr-pwcrack/examples/difficulty_level_6/training/v1/cluster/ppo_baseline/results/data/"
    ppo_v1_df_399 = pd.read_csv(glob.glob(base_path + "399/*_train.csv")[0])
    emulation_w_cache_env_response_times = np.mean(np.array(list(filter(lambda x: x  >0.0, ppo_v1_df_399["env_response_times"].values))))
    emulation_w_cache_action_pred_times = np.mean(np.array(list(filter(lambda x: x > 0.0, ppo_v1_df_399["action_pred_times"].values))))
    emulation_w_cache_grad_comp_times = np.mean(np.array(list(filter(lambda x: x > 0.0, ppo_v1_df_399["grad_comp_times"].values))))
    emulation_w_cache_weight_update_times = np.mean(np.array(list(filter(lambda x: x > 0.0, ppo_v1_df_399["weight_update_times"].values))))

    total_emulation_w_cache = emulation_w_cache_env_response_times + emulation_w_cache_action_pred_times + \
                              emulation_w_cache_grad_comp_times + emulation_w_cache_weight_update_times
    #emulation_w_cache_rollout_times_percentage  = (emulation_w_cache_rollout_times/total_emulation_w_cache)*100
    emulation_w_cache_env_response_times_percentage = (emulation_w_cache_env_response_times/total_emulation_w_cache)*100
    emulation_w_cache_action_pred_times_percentage = (emulation_w_cache_action_pred_times/total_emulation_w_cache)*100
    emulation_w_cache_grad_comp_times_percentage = (emulation_w_cache_grad_comp_times/total_emulation_w_cache)*100
    emulation_w_cache_weight_update_times_percentage = (emulation_w_cache_weight_update_times/total_emulation_w_cache)*100


    return emulation_w_cache_env_response_times_percentage, \
           emulation_w_cache_action_pred_times_percentage, emulation_w_cache_grad_comp_times_percentage, \
           emulation_w_cache_weight_update_times_percentage


def bar_plot_stacked(emulation_w_cache_env_response_times, emulation_w_cache_action_pred_times, \
           emulation_w_cache_grad_comp_times, emulation_w_cache_weight_update_times):
    print([emulation_w_cache_env_response_times, emulation_w_cache_action_pred_times, \
           emulation_w_cache_grad_comp_times, emulation_w_cache_weight_update_times])

    pos_weight_upd = np.array([5.5, 0.005, emulation_w_cache_weight_update_times])
    pos_grad_comp = np.array([8.5, 0.005, emulation_w_cache_grad_comp_times])
    pos_action_pred = np.array([71, 0.01, emulation_w_cache_action_pred_times])
    pos_env_response = np.array([15, 99.98, emulation_w_cache_env_response_times])
    pos_other = np.array([5, 0, 0])

    with sns.axes_style("white"):

        plt.rc('text', usetex=True)
        # plt.rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
        plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
        plt.rcParams['font.family'] = ['serif']
        plt.rcParams['font.serif'] = ['Times New Roman']
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(3.5, 2.5))
        plt.rcParams.update({'font.size': 10})
        plt.rcParams["axes.grid"] = True
        labels = [r"Simulation", r"Emulation", r"Emulation w. Cache"]

        #sns.set_style("ticks")
        #sns.set_context("talk")

        # plot details
        bar_width = 0.35
        epsilon = .015
        line_width = 1
        opacity = 1
        pos_bar_positions = np.arange(len(pos_weight_upd))
        neg_bar_positions = pos_bar_positions + bar_width - 0.45

        cm = plt.cm.get_cmap('RdYlBu_r')
        #colors = plt.cm.GnBu(np.linspace(0.3, 1, 4))[-4:]
        colors = plt.cm.viridis(np.linspace(0.3, 1, 10))[-10:]

        # make bar plots
        weight_update_bar = ax.bar(pos_bar_positions, pos_weight_upd, bar_width-epsilon,
                                  edgecolor=colors[0],
                                  #edgecolor='',
                                  color="white",
                                  label=r'Weight update',
                                  linewidth=line_width,
                                  hatch='OO',
                                  alpha = opacity)
        grad_comp_bar = ax.bar(pos_bar_positions, pos_grad_comp, bar_width - epsilon,
                                  bottom=pos_weight_upd,
                                  alpha=opacity,
                                  color='white',
                                  edgecolor=colors[1],
                                  #edgecolor='black',
                                  linewidth=line_width,
                                  hatch='////',
                                  label=r'Grad comp')
        action_pred_bar = ax.bar(pos_bar_positions, pos_action_pred, bar_width - epsilon,
                                   bottom=pos_grad_comp + pos_weight_upd,
                                   alpha=opacity,
                                   color='white',
                                   edgecolor="black",
                                   linewidth=line_width,
                                   hatch='---',
                                   label=r'Action pred')
        env_response_bar = ax.bar(pos_bar_positions, pos_env_response, bar_width-epsilon,
                                  bottom=pos_grad_comp + pos_weight_upd+pos_action_pred,
                                  label=r'Env response',
                                  edgecolor=colors[6],
                                  #edgecolor='black',
                                  color="white",
                                  hatch='xxx',
                                  linewidth=line_width,
                                  alpha=opacity,
                                  )
        # other_bar = ax.bar(pos_bar_positions, pos_other, bar_width - epsilon,
        #                           bottom=pos_grad_comp + pos_weight_upd+pos_action_pred + pos_env_response,
        #                           color="white",
        #                           hatch='/',
        #                           edgecolor='black',
        #                           ecolor="#0000DD",
        #                           linewidth=line_width,
        #                           label='Other')
        # set the grid on
        ax.grid('on')
        ax.set_xticks(neg_bar_positions)
        ax.set_xticklabels(labels, rotation=45)
        ax.patch.set_edgecolor('black')
        ax.set_ylim((0,100))

        ax.patch.set_linewidth('1')
        #ax.set_xticklabels(neg_bar_positions, genes, rotation=45)
        ax.set_ylabel(r'Percentage $(\%)$')
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.25),
                  ncol=2, fancybox=True, shadow=True, fontsize=8)
        file_name = "perf_analysis"
        plt.savefig(file_name + ".png", format="png", dpi=600)
        plt.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
        fig.tight_layout()
        sns.despine()
        plt.show()

if __name__ == '__main__':
    emulation_w_cache_env_response_times, emulation_w_cache_action_pred_times, \
    emulation_w_cache_grad_comp_times, emulation_w_cache_weight_update_times = read_data()
    bar_plot_stacked(emulation_w_cache_env_response_times,
                     emulation_w_cache_action_pred_times, emulation_w_cache_grad_comp_times,
                     emulation_w_cache_weight_update_times)