import numpy as np
from csle_common.metastore.metastore_facade import MetastoreFacade

if __name__ == '__main__':
    cross_entropy_ids = MetastoreFacade.list_experiment_executions_ids()
    cross_entropy_btrs = []
    de_btrs = []
    spsa_btrs = []
    bo_btrs = []
    random_btrs = []
    data_dict = {}
    data_dict["ce"] = {}
    data_dict["bo"] = {}
    data_dict["spsa"] = {}
    data_dict["random"] = {}
    data_dict["de"] = {}
    for i, id in enumerate(cross_entropy_ids):
        print(f"{i}/{len(cross_entropy_ids)}")
        ex = MetastoreFacade.get_experiment_execution(id=id[0])
        if ex.config.agent_type == 12:
            if ex.config.hparams['L'].value not in data_dict["ce"]:
                data_dict["ce"][ex.config.hparams['L'].value] = ex
            elif (ex.config.hparams['L'].value in data_dict["ce"] and
                  data_dict["ce"][ex.config.hparams['L'].value].id < ex.id):
                data_dict["ce"][ex.config.hparams['L'].value] = ex
        if ex.config.agent_type == 13:
            if ex.config.hparams['L'].value not in data_dict["de"]:
                data_dict["de"][ex.config.hparams['L'].value] = ex
            elif (ex.config.hparams['L'].value in data_dict["de"] and
                  data_dict["de"][ex.config.hparams['L'].value].id < ex.id):
                data_dict["de"][ex.config.hparams['L'].value] = ex
        if ex.config.agent_type == 0:
            if ex.config.hparams['L'].value not in data_dict["spsa"]:
                data_dict["spsa"][ex.config.hparams['L'].value] = ex
            elif (ex.config.hparams['L'].value in data_dict["spsa"]
                  and data_dict["spsa"][ex.config.hparams['L'].value].id < ex.id):
                data_dict["spsa"][ex.config.hparams['L'].value] = ex
        if ex.config.agent_type == 23:
            if ex.config.hparams['L'].value not in data_dict["bo"]:
                data_dict["bo"][ex.config.hparams['L'].value] = ex
            elif (ex.config.hparams['L'].value in data_dict["bo"] and
                  data_dict["bo"][ex.config.hparams['L'].value].id < ex.id):
                data_dict["bo"][ex.config.hparams['L'].value] = ex
        if ex.config.agent_type == 11:
            if ex.config.hparams['L'].value not in data_dict["random"]:
                data_dict["random"][ex.config.hparams['L'].value] = ex
            elif (ex.config.hparams['L'].value in data_dict["random"] and
                  data_dict["random"][ex.config.hparams['L'].value].id < ex.id):
                data_dict["random"][ex.config.hparams['L'].value] = ex
    btrs = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
    algos = ["ce", "de", "bo", "spsa"]
    for btr in btrs:
        for algo in algos:
            print(f"algo: {algo}, btr: {btr}")
            if algo in data_dict and btr in data_dict[algo]:
                ex = data_dict[algo][btr]
                if ("running_average_return" not in ex.result.avg_metrics or "average_upper_bound_return"
                        not in ex.result.avg_metrics or "runtime" not in ex.result.avg_metrics):
                    print("Problem1!")
            else:
                print("Problem2!")

                # avg_costs = np.array(ex.result.avg_metrics["running_average_return"]) / (btr - 1)
                # costs_stds = np.array(ex.result.std_metrics["running_average_return"])
                # optimal_costs = np.array(ex.result.avg_metrics["average_upper_bound_return"]) / (btr - 1)
                # runtimes = np.array(ex.result.avg_metrics["runtime"])
                # optimal_costs = min(np.mean(optimal_costs), np.min(avg_costs))
                # optimal_costs = [optimal_costs] * len(runtimes)
    # print(f"id: {ex.id}, agent: {ex.config.agent_type}, BTR: {ex.config.hparams['L'].value}")
    # import sys
    # sys.exit(0)
