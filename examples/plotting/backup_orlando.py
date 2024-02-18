from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.util.plotting_util import PlottingUtil
from csle_common.dao.training.experiment_execution import ExperimentExecution

if __name__ == '__main__':
    apple_b_line_256_id = 6
    apple_meander_256_id = 7
    cardiff_b_line_64_id = 222
    cardiff_meander_64_id = 2
    # experiment_apple_bline_256 = MetastoreFacade.get_experiment_execution(id=apple_b_line_256_id)
    # experiment_apple_meander_256 = MetastoreFacade.get_experiment_execution(id=apple_meander_256_id)
    # experiment_cardiff_b_line_64 = MetastoreFacade.get_experiment_execution(id=cardiff_b_line_64_id)
    # experiment_cardiff_meander_64 = MetastoreFacade.get_experiment_execution(id=cardiff_meander_64_id)
    experiment_cardiff_b_line_64 = ExperimentExecution.from_json_file("/home/kim/orlando_results/16_jan/cardiff_b_line_64_2.json")
    # experiment_cardiff_meander_64 = ExperimentExecution.from_json_file("/home/kim/orlando_results/17_feb/cardiff_meander_64.json")

    # experiment_apple_bline_256.to_json_file("/home/kim/orlando_results/15_jan/apple_b_line_256.json")
    # experiment_apple_meander_256.to_json_file("/home/kim/orlando_results/15_jan/apple_meander_256.json")
    # experiment_cardiff_b_line_64.to_json_file("/home/kim/orlando_results/16_jan/cardiff_b_line_64.json")
    # experiment_cardiff_b_line_64.to_json_file("/home/kim/orlando_results/16_jan/cardiff_b_line_64_2.json")
    # experiment_cardiff_meander_64.to_json_file("/home/kim/orlando_results/17_feb/cardiff_meander_64.json")

    metric = "average_return"
    returns = []
    confidence = 0.95
    running_avg = 50
    seeds = list(experiment_cardiff_b_line_64.result.all_metrics.keys())
    running_times = experiment_cardiff_b_line_64.result.all_metrics[seeds[0]]["runtime"]
    for seed in seeds:
        r = PlottingUtil.running_average(experiment_cardiff_b_line_64.result.all_metrics[seed][metric], running_avg)
        # print(len(experiment_cardiff_b_line_64.result.all_metrics[seed]["runtime"]))
        # print(experiment_cardiff_b_line_64.result.all_metrics[seed]["runtime"][43])
        returns.append(r)
    avg_returns_means = []
    avg_returns_stds = []
    b_line_opt = -12.98
    for i in range(len(returns[0])):
        values = []
        for j in range(len(seeds)):
            if len(avg_returns_means) > 0:
                values.append(b_line_opt-returns[j][i] + avg_returns_means[-1])
            else:
                values.append(b_line_opt-returns[j][i])
        mean_and_ci = PlottingUtil.mean_confidence_interval(data=values, confidence=confidence)
        avg_returns_means.append(mean_and_ci[0])
        avg_returns_stds.append(mean_and_ci[1])
    for i in range(len(avg_returns_means)):
        # print(f"{(i + 1)*10} {avg_returns_means[i]} {avg_returns_means[i] + avg_returns_stds[i]} "
        #       f"{avg_returns_means[i] - avg_returns_stds[i]}")
        # print(f"{running_times[i]} {avg_returns_means[i]} {avg_returns_means[i] + avg_returns_stds[i]} "
        #       f"{avg_returns_means[i] - avg_returns_stds[i]}")
        print(f"{running_times[i]} 273.5 273.5 273.5")


    # returns = np.array(returns)
    # returns = returns.reshape((returns.shape[1], len(seeds)))
    # avg_returns_means = np.array(list(map(lambda x: PlottingUtil.mean_confidence_interval(
    #     data=x, confidence=confidence)[0], returns)))
    # print(avg_returns_means.shape)
    # avg_returns_stds = np.array(list(map(lambda x: PlottingUtil.mean_confidence_interval(
    #     data=x, confidence=confidence)[1], returns)))
    #432
