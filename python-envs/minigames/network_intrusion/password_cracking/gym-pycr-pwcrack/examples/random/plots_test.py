import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def bar_plot_stacked():

    pos_weight_upd = np.array([20, 10, 5])
    pos_grad_comp = np.array([10, 0, 0])
    pos_action_pred = np.array([10, 0, 0])
    pos_env_response = np.array([10, 30, 5])
    pos_other = np.array([5, 0, 7.5])
    labels = ["Simulation", "Emulation", "Emulation w. Cache"]

    with sns.axes_style("white"):
        plt.rc('text', usetex=True)
        plt.rc('text.latex', preamble=r'\usepackage{amsfonts}')
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(3.5, 3.5))
        plt.rcParams.update({'font.size': 12})

        sns.set_style("ticks")
        sns.set_context("talk")

        # plot details
        bar_width = 0.35
        epsilon = .015
        line_width = 1
        opacity = 0.7
        pos_bar_positions = np.arange(len(pos_weight_upd))
        neg_bar_positions = pos_bar_positions + bar_width

        # make bar plots
        weight_update_bar = ax.bar(pos_bar_positions, pos_weight_upd, bar_width,
                                  edgecolor='firebrick',
                                  color="white",
                                  label='Weight update',
                                  linewidth=line_width,
                                  hatch='O',
                                  alpha = 0.7)
        grad_comp_bar = ax.bar(pos_bar_positions, pos_grad_comp, bar_width - epsilon,
                                  bottom=pos_weight_upd,
                                  alpha=opacity,
                                  color='white',
                                  edgecolor='dimgrey',
                                  linewidth=line_width,
                                  hatch='//',
                                  label='Grad comp')
        action_pred_bar = ax.bar(pos_bar_positions, pos_action_pred, bar_width - epsilon,
                                   bottom=pos_grad_comp + pos_weight_upd,
                                   alpha=opacity,
                                   color='white',
                                   edgecolor='darkslateblue',
                                   linewidth=line_width,
                                   hatch='*',
                                   label='Action pred')
        env_response_bar = ax.bar(pos_bar_positions, pos_env_response, bar_width,
                                  bottom=pos_grad_comp + pos_weight_upd+pos_action_pred,
                                  label='Env response',
                                  edgecolor='#377EB8',
                                  color="white",
                                  hatch='x',
                                  )
        other_bar = ax.bar(pos_bar_positions, pos_other, bar_width - epsilon,
                                  bottom=pos_grad_comp + pos_weight_upd+pos_action_pred + pos_env_response,
                                  color="white",
                                  hatch='/',
                                  edgecolor='black',
                                  ecolor="#0000DD",
                                  linewidth=line_width,
                                  label='Other')
        ax.set_xticks(neg_bar_positions)
        ax.set_xticklabels(labels, rotation=45)
        #ax.set_xticklabels(neg_bar_positions, genes, rotation=45)
        ax.set_ylabel('Percentage of Samples')
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.4),
                  ncol=2, fancybox=True, shadow=True, fontsize=8)
        fig.tight_layout()
        sns.despine()
        plt.show()

if __name__ == '__main__':
    bar_plot_stacked()