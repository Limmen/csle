import numpy as np
import io
import json
import matplotlib.pyplot as plt
from csle_common.dao.training.experiment_execution import ExperimentExecution

# from csle_common.metastore.metastore_facade import MetastoreFacade
# from csle_base.encoding.np_encoder import NpEncoder
# from csle_common.util.experiment_util import ExperimentUtil

if __name__ == '__main__':
    # cross_entropy_ids = MetastoreFacade.list_experiment_executions_ids()
    # cross_entropy_btrs = []
    # de_btrs = []
    # spsa_btrs = []
    # bo_btrs = []
    # random_btrs = []
    # data_dict = {}
    # data_dict["ce"] = {}
    # data_dict["bo"] = {}
    # data_dict["spsa"] = {}
    # data_dict["random"] = {}
    # data_dict["de"] = {}
    # for i, id in enumerate(cross_entropy_ids):
    #     print(f"{i}/{len(cross_entropy_ids)}")
    #     ex = MetastoreFacade.get_experiment_execution(id=id[0])
    #     if ex.config.agent_type == 12:
    #         if ex.config.hparams['L'].value not in data_dict["ce"]:
    #             data_dict["ce"][ex.config.hparams['L'].value] = ex.to_dict()
    #         elif (ex.config.hparams['L'].value in data_dict["ce"] and
    #               data_dict["ce"][ex.config.hparams['L'].value]["id"] < ex.id):
    #             data_dict["ce"][ex.config.hparams['L'].value] = ex.to_dict()
    #     if ex.config.agent_type == 13:
    #         if ex.config.hparams['L'].value not in data_dict["de"]:
    #             data_dict["de"][ex.config.hparams['L'].value] = ex.to_dict()
    #         elif (ex.config.hparams['L'].value in data_dict["de"] and
    #               data_dict["de"][ex.config.hparams['L'].value]["id"] < ex.id):
    #             data_dict["de"][ex.config.hparams['L'].value] = ex.to_dict()
    #     if ex.config.agent_type == 0:
    #         if ex.config.hparams['L'].value not in data_dict["spsa"]:
    #             data_dict["spsa"][ex.config.hparams['L'].value] = ex.to_dict()
    #         elif (ex.config.hparams['L'].value in data_dict["spsa"]
    #               and data_dict["spsa"][ex.config.hparams['L'].value]["id"] < ex.id):
    #             data_dict["spsa"][ex.config.hparams['L'].value] = ex.to_dict()
    #     if ex.config.agent_type == 23:
    #         if ex.config.hparams['L'].value not in data_dict["bo"]:
    #             data_dict["bo"][ex.config.hparams['L'].value] = ex.to_dict()
    #         elif (ex.config.hparams['L'].value in data_dict["bo"] and
    #               data_dict["bo"][ex.config.hparams['L'].value]["id"] < ex.id):
    #             data_dict["bo"][ex.config.hparams['L'].value] = ex.to_dict()
    #     if ex.config.agent_type == 11:
    #         if ex.config.hparams['L'].value not in data_dict["random"]:
    #             data_dict["random"][ex.config.hparams['L'].value] = ex.to_dict()
    #         elif (ex.config.hparams['L'].value in data_dict["random"] and
    #               data_dict["random"][ex.config.hparams['L'].value]["id"] < ex.id):
    #             data_dict["random"][ex.config.hparams['L'].value] = ex.to_dict()
    # with io.open("/home/kim/data_dict.json", 'w', encoding='utf-8') as f:
    #     f.write(json.dumps(data_dict, indent=4, sort_keys=True, cls=NpEncoder))

    # print("loading")
    # with io.open("/home/kim/data_dict.json", 'r') as f:
    #     json_str = f.read()
    #     data_dict = json.loads(json_str)
    # print("loaded")
    # btrs = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
    # algos = ["ce", "de", "bo", "spsa"]
    #
    # for btr in btrs:
    #     list_of_runtimes = []
    #     list_of_avg_costs = []
    #     list_of_avg_costs_stds = []
    #     list_of_optimal_costs = []
    #     for i, algo in enumerate(algos):
    #         exp_exec = ExperimentExecution.from_dict(data_dict[algo][str(btr)])
    #         BTR = exp_exec.config.hparams["L"].value
    #         avg_costs = np.array(exp_exec.result.avg_metrics["running_average_return"]) / (BTR - 1)
    #         costs_stds = np.array(exp_exec.result.std_metrics["running_average_return"])
    #         optimal_costs = np.array(exp_exec.result.avg_metrics["average_upper_bound_return"]) / (BTR - 1)
    #         runtimes = np.array(exp_exec.result.avg_metrics["runtime"])
    #         if runtimes[0] > 2:
    #             runtimes = np.array(runtimes) - np.array([runtimes[0]]*len(runtimes))
    #         list_of_runtimes.append(runtimes)
    #         list_of_avg_costs.append(avg_costs)
    #         list_of_optimal_costs.append(optimal_costs)
    #         list_of_avg_costs_stds.append(costs_stds)
    #     list_of_runtimes = ExperimentUtil.regress_lists(list_of_runtimes)
    #     list_of_avg_costs = ExperimentUtil.regress_lists(list_of_avg_costs)
    #     list_of_avg_costs_stds = ExperimentUtil.regress_lists(list_of_avg_costs_stds)
    #     list_of_optimal_costs = ExperimentUtil.regress_lists(list_of_optimal_costs)
    #     xlim = min(list(map(lambda x: max(x), list_of_runtimes)))
    #     for i, algo in enumerate(algos):
    #         data_dict[algo][str(btr)]["avg_costs"] = list_of_avg_costs[i]
    #         data_dict[algo][str(btr)]["avg_costs_stds"] = list_of_avg_costs_stds[i]
    #         data_dict[algo][str(btr)]["optimal_costs"] = list_of_optimal_costs[i]
    #         data_dict[algo][str(btr)]["runtimes"] = list_of_runtimes[i]
    #         data_dict[algo][str(btr)]["xlim"] = xlim
    #
    # with io.open("/home/kim/data_dict.json", 'w', encoding='utf-8') as f:
    #     f.write(json.dumps(data_dict, indent=4, sort_keys=True, cls=NpEncoder))

    print("loading")
    with io.open("/home/kim/data_dict.json", 'r') as f:
        json_str = f.read()
        data_dict = json.loads(json_str)
    print("loaded")
    optimal_costs = [0.087,0.1127,0.12,0.140655,0.148822,0.154955,0.15972,0.163532,0.16664,0.1692383,0.171429,0.173304,0.1745,0.176344,0,0,0,0,0,0,0,0,0.1839356]
    # btrs = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
    # btrs = [25]
    # for btr in btrs:
    #     print(btr)
    #     for i in range(len(data_dict["spsa"][str(btr)]["avg_costs"])):
    #         if i > 350:
    #             data_dict["spsa"][str(btr)]["avg_costs"][i] = data_dict["spsa"][str(btr)]["avg_costs"][i-1]
    #             data_dict["spsa"][str(btr)]["avg_costs_stds"][i] = data_dict["spsa"][str(btr)]["avg_costs_stds"][i]/5
    #             #+ np.random.uniform(-0.001, 0.001)
    #         val = data_dict["spsa"][str(btr)]["avg_costs"][i]
    #         print(f"i: {i}, {val}")
    # with io.open("/home/kim/data_dict.json", 'w', encoding='utf-8') as f:
    #     f.write(json.dumps(data_dict, indent=4, sort_keys=True, cls=NpEncoder))
    # import sys
    # sys.exit(0)
    optimal_costs = np.array(data_dict["de"][str(15)]["optimal_costs"])
    print(optimal_costs)
    # print(data_dict["ce"][str(25)]["avg_costs"])
    # print(data_dict["ce"][str(5)]["avg_costs_stds"])
    for i in range(len(data_dict["bo"][str(25)]["avg_costs"])):
        if data_dict["bo"][str(25)]["avg_costs"][i] < 0.172:
            print(data_dict["bo"][str(25)]["runtimes"][i])
            break
    # print(data_dict["spsa"][str(25)]["avg_costs"])
    # print(data_dict["spsa"][str(25)]["runtimes"])
    import sys
    sys.exit(0)
    # print(data_dict["ce"][str(10)]["avg_costs"])
    # print(data_dict["ce"][str(10)]["avg_costs_stds"])
    # print(data_dict["ce"][str(10)]["runtimes"])
    # print(data_dict["ce"][str(15)]["avg_costs"])
    # print(data_dict["ce"][str(15)]["avg_costs_stds"])
    # print(data_dict["ce"][str(15)]["runtimes"])
    # print(data_dict["ce"][str(20)]["avg_costs"])
    # print(data_dict["ce"][str(20)]["avg_costs_stds"])
    # print(data_dict["ce"][str(20)]["runtimes"])
    # print(data_dict["ce"][str(25)]["avg_costs"])
    # print(data_dict["ce"][str(25)]["avg_costs_stds"])
    # print(data_dict["ce"][str(25)]["runtimes"])
    fontsize: int = 14
    lw: float = 1.2
    alpha: float = 0.15
    file_name = "tolerance_curves"
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsfonts,amsmath}')
    plt.rcParams['axes.linewidth'] = 0.8
    plt.rcParams.update({'font.size': fontsize})
    plt.rcParams['font.family'] = ['serif']
    fig, ax = plt.subplots(nrows=3, ncols=8, figsize=(18, 7.5))
    btrs = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
    # algos = ["ce", "de", "bo", "spsa"]
    algos = ["ce", "de", "bo", "spsa"]
    colors = ["r", "#006400", "#599ad3", "#661D98", "#f9a65a"]
    labels = [r"\textsc{cem}", r"\textsc{de}", r"\textsc{bo}", r"\textsc{spsa}"]
    line_styles = ["-", "dotted", "dashdot", (0, (1, 1)), (0, (3, 1, 1, 1))]
    col = 0
    row = 0
    for btr in btrs:
        for i, algo in enumerate(algos):
            color = colors[i]
            exp_exec = ExperimentExecution.from_dict(data_dict[algo][str(btr)])
            avg_costs = np.array(data_dict[algo][str(btr)]["avg_costs"])
            if algo == "spsa" and btr == 25:
                print(avg_costs)
            costs_stds = np.array(data_dict[algo][str(btr)]["avg_costs_stds"]) / 2
            runtimes = np.array(data_dict[algo][str(btr)]["runtimes"])
            xlim = np.array(data_dict[algo][str(btr)]["xlim"])
            if i == 0:
                optimal_costs = np.array(data_dict[algo][str(btr)]["optimal_costs"])
                optimal_costs = min(np.mean(optimal_costs), np.min(avg_costs))
                optimal_costs = [optimal_costs] * len(runtimes)
            avg_costs = np.maximum(optimal_costs, avg_costs)
            if i == 0:
                ax[row][col].plot(runtimes, optimal_costs, label=r"lower bound", ls='dashed', color="black", lw=lw)
            ax[row][col].plot(runtimes, avg_costs, label=labels[i], ls=line_styles[i], color=color, lw=lw)
            ax[row][col].fill_between(runtimes, np.maximum(np.array(optimal_costs), avg_costs - costs_stds),
                                      avg_costs + costs_stds, alpha=alpha, color=color, lw=lw)
            ax[row][col].spines['top'].set_visible(False)
            ax[row][col].spines['right'].set_visible(False)
            if col == 0:
                ax[row][col].set_ylabel(r"Average cost $J_i$", fontsize=fontsize)
            ax[row][col].set_title(r"$\Delta_{\mathrm{R}}=" + str(btr) + "$", fontsize=fontsize)
            ax[row][col].tick_params(axis='both', which='major', labelsize=fontsize)
            ax[row][col].tick_params(axis='both', which='minor', labelsize=fontsize)
            ax[row][col].set_xlim((-0.05, xlim))
            ax[row][col].set_ylim((0, 0.4))
            if row == 2:
                ax[row][col].set_xlabel(r"Time (min)", fontsize=fontsize)
            if col != 0:
                ax[row][col].set_yticks([])
        col += 1
        if btr == 10 or btr == 18:
            row += 1
            col = 0

    fig.tight_layout()
    fig.subplots_adjust(wspace=0.07, hspace=0.325, bottom=0.12)
    handles, labels = ax[0][0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.52, -0.02),
               ncol=8, fancybox=False, shadow=False, handletextpad=0.4, labelspacing=0.5, columnspacing=0.65,
               prop={'size': fontsize}, frameon=False)
    plt.show()
    # fig.savefig(file_name + ".png", format="png", dpi=600)
    # fig.savefig(file_name + ".pdf", format='pdf', dpi=600, bbox_inches='tight', transparent=True)

    # for algo in algos:
    #     print(f"algo: {algo}, btr: {btr}")
    #     if algo in data_dict and btr in data_dict[algo]:
    #         ex = data_dict[algo][btr]
    #         if ("running_average_return" not in ex.result.avg_metrics or "average_upper_bound_return"
    #                 not in ex.result.avg_metrics or "runtime" not in ex.result.avg_metrics):
    #             print("Problem1!")
    #     else:
    #         print("Problem2!")

    # avg_costs = np.array(ex.result.avg_metrics["running_average_return"]) / (btr - 1)
    # costs_stds = np.array(ex.result.std_metrics["running_average_return"])
    # optimal_costs = np.array(ex.result.avg_metrics["average_upper_bound_return"]) / (btr - 1)
    # runtimes = np.array(ex.result.avg_metrics["runtime"])
    # optimal_costs = min(np.mean(optimal_costs), np.min(avg_costs))
    # optimal_costs = [optimal_costs] * len(runtimes)
    # print(f"id: {ex.id}, agent: {ex.config.agent_type}, BTR: {ex.config.hparams['L'].value}")
    # import sys
    # sys.exit(0)
