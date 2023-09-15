import matplotlib.pyplot as plt
import numpy as np
from csle_tolerance.util.pomdp_solve_parser import PomdpSolveParser

if __name__ == '__main__':
    file_name="intrusion_recovery_value_function"
    fontsize=18
    markevery=5
    markersize=5
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts,amsmath}')
    plt.rcParams['axes.linewidth'] = 0.8
    plt.rcParams.update({'font.size': fontsize})
    plt.rcParams['font.family'] = ['serif']
    fig, ax = plt.subplots(nrows=1, ncols=5, figsize=(18, 3.3))
    lw=1.5


    alpha_vectors_01 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01.alpha")
    alpha_vectors_005 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_005.alpha")
    alpha_vectors_0025 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_0025.alpha")
    alpha_vectors_001 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_001.alpha")
    alpha_vectors_0005 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_0005.alpha")
    belief_space = np.linspace(0.0, 1, int(1/0.05))
    values_01 = []
    for j, b in enumerate(belief_space):
        b_vec = [1-b, b]
        dot_vals = []
        for i in range(len(alpha_vectors_01)):
            dot_vals.append(-np.dot(b_vec, alpha_vectors_01[i][1][0:2]))
        min_index = np.argmin(dot_vals)
        values_01.append(dot_vals[min_index])
        vec_dots = []
        for b in belief_space:
            b_vec = [1-b, b]
            vec_dots.append(-np.dot(b_vec, alpha_vectors_01[min_index][1][0:2]))
        ax[0].plot(belief_space, vec_dots, ls='dashed', color="r", lw=lw, alpha=0.2)
    ax[0].plot(belief_space, values_01, ls='-', color="black", lw=lw)
    ax[0].spines['top'].set_visible(False)
    ax[0].spines['right'].set_visible(False)
    ax[0].set_ylabel(r"$V^{*}_{i,1}(b_{i,1})$")
    ax[0].set_xlabel(r"$b_{i,1}$")
    ax[0].set_title("$p_{\mathrm{A}}=0.1$", fontsize=fontsize)

    values_005 = []
    for j, b in enumerate(belief_space):
        b_vec = [1-b, b]
        dot_vals = []
        for i in range(len(alpha_vectors_005)):
            dot_vals.append(-np.dot(b_vec, alpha_vectors_005[i][1][0:2]))
        min_index = np.argmin(dot_vals)
        values_005.append(dot_vals[min_index])
        vec_dots = []
        for b in belief_space:
            b_vec = [1-b, b]
            vec_dots.append(-np.dot(b_vec, alpha_vectors_005[min_index][1][0:2]))
        ax[1].plot(belief_space, vec_dots, ls='dashed', color="r", lw=lw, alpha=0.2)

    ax[1].plot(belief_space, values_005, ls='-', color="black", lw=lw)
    ax[1].spines['top'].set_visible(False)
    ax[1].spines['right'].set_visible(False)
    ax[1].set_ylabel(r"$V^{*}_{i,1}(b_{i,1})$")
    ax[1].set_xlabel(r"$b_{i,1}$")
    ax[1].set_title("$p_{\mathrm{A}}=0.05$", fontsize=fontsize)

    values_0025 = []
    for j, b in enumerate(belief_space):
        b_vec = [1-b, b]
        dot_vals = []
        for i in range(len(alpha_vectors_0025)):
            dot_vals.append(-np.dot(b_vec, alpha_vectors_0025[i][1][0:2]))
        min_index = np.argmin(dot_vals)
        values_0025.append(dot_vals[min_index])
        vec_dots = []
        for b in belief_space:
            b_vec = [1-b, b]
            vec_dots.append(-np.dot(b_vec, alpha_vectors_0025[min_index][1][0:2]))
        ax[2].plot(belief_space, vec_dots, ls='dashed', color="r", lw=lw, alpha=0.2)

    ax[2].plot(belief_space, values_0025, ls='-', color="black", lw=lw)
    ax[2].spines['top'].set_visible(False)
    ax[2].spines['right'].set_visible(False)
    ax[2].set_ylabel(r"$V^{*}_{i,1}(b_{i,1})$")
    ax[2].set_xlabel(r"$b_{i,1}$")
    ax[2].set_title("$p_{\mathrm{A}}=0.025$", fontsize=fontsize)

    values_001 = []
    for j, b in enumerate(belief_space):
        b_vec = [1-b, b]
        dot_vals = []
        for i in range(len(alpha_vectors_001)):
            dot_vals.append(-np.dot(b_vec, alpha_vectors_001[i][1][0:2]))
        min_index = np.argmin(dot_vals)
        values_001.append(dot_vals[min_index])
        vec_dots = []
        for b in belief_space:
            b_vec = [1-b, b]
            vec_dots.append(-np.dot(b_vec, alpha_vectors_001[min_index][1][0:2]))
        ax[3].plot(belief_space, vec_dots, ls='dashed', color="r", lw=lw, alpha=0.2)

    ax[3].plot(belief_space, values_001, ls='-', color="black", lw=lw)
    ax[3].spines['top'].set_visible(False)
    ax[3].spines['right'].set_visible(False)
    ax[3].set_ylabel(r"$V^{*}_{i,1}(b_{i,1})$")
    ax[3].set_xlabel(r"$b_{i,1}$")
    ax[3].set_title("$p_{\mathrm{A}}=0.01$", fontsize=fontsize)

    values_0005 = []
    for j, b in enumerate(belief_space):
        b_vec = [1-b, b]
        dot_vals = []
        for i in range(len(alpha_vectors_0005)):
            dot_vals.append(-np.dot(b_vec, alpha_vectors_0005[i][1][0:2]))
        min_index = np.argmin(dot_vals)
        values_0005.append(dot_vals[min_index])
        vec_dots = []
        for b in belief_space:
            b_vec = [1-b, b]
            vec_dots.append(-np.dot(b_vec, alpha_vectors_0005[min_index][1][0:2]))
        ax[4].plot(belief_space, vec_dots, ls='dashed', color="r", lw=lw, alpha=0.2)

    ax[4].plot(belief_space, values_0005, ls='-', color="black", lw=lw)
    ax[4].spines['top'].set_visible(False)
    ax[4].spines['right'].set_visible(False)
    ax[4].set_ylabel(r"$V^{*}_{i,1}(b_{i,1})$")
    ax[4].set_xlabel(r"$b_{i,1}$")
    ax[4].set_title("$p_{\mathrm{A}}=0.005$", fontsize=fontsize)

    # for i in range(len(alpha_vectors_01)):
    #     alpha_vec = alpha_vectors_01[i][1][0:2]
    #     # action = alpha_vectors_action_0[i][0]
    #     # color = "r"
    #     dots = []
    #     for b in belief_space:
    #         vec = [1-b, b]
    #         dots.append(-np.dot(vec, alpha_vec))
    #     ax.plot(belief_space, dots, ls='dashed', color="r", lw=lw, alpha=0.2)

    # colors = ["r", "#f9a65a", "#599ad3", "#009E73", "b", "purple"]
    # ax.plot(belief_space, values_005, ls='-', color="r", lw=lw, label="$p_{\mathrm{A}}=0.005$")
    # ax.plot(belief_space, values_0025, ls='-', color="#f9a65a", lw=lw, label="$p_{\mathrm{A}}=0.0025$")
    # ax.plot(belief_space, values_001, ls='-', color="#599ad3", lw=lw, label="$p_{\mathrm{A}}=0.001$")
    # ax.plot(belief_space, values_0005, ls='-', color="#009E73", lw=lw, label="$p_{\mathrm{A}}=0.0005$")
    # handles, labels = ax.get_legend_handles_labels()
    # fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.6, 0.17),
    #            ncol=4, fancybox=True, shadow=False, handletextpad=0.4, labelspacing=0.5, columnspacing=0.65,
    #            prop={'size': fontsize})
    fig.tight_layout()
    # fig.subplots_adjust(wspace=0.1, hspace=0.25, bottom=0.25)
    fig.savefig(file_name + ".png", format="png", dpi=600)
    fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)
    fig.savefig(file_name + ".eps", format='eps', dpi=600, bbox_inches='tight', transparent=True)
    plt.show()