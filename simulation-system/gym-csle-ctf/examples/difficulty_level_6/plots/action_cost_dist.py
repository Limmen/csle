import numpy as np
import matplotlib.pyplot as plt
from gym_csle_ctf.util.plots import plotting_action_costs

if __name__ == '__main__':
    # plot_action_types_pie(CSLECTFSimpleBase.all_actions_conf(
    #     num_nodes=CSLECTFSimpleBase.num_nodes(),
    #     subnet_mask=CSLECTFSimpleBase.subnet_mask(),
    #     hacker_ip=CSLECTFSimpleBase.hacker_ip()
    # ))

    cm = plt.cm.get_cmap('RdYlBu_r')
    colors = plt.cm.GnBu(np.linspace(0.3, 1, 4))[-4:]
    colors = plt.cm.viridis(np.linspace(0.3, 1, 4))[-4:]
    print(colors[0])
    print(len(colors))

    # d_1 = read_action_costs(zip_file="/home/kim/storage/workspace/csle/emulation-system/minigames/network_intrusion/ctf/001/level_1/agent_cache.zip", num_bins=100)
    # d_2 = read_action_costs(zip_file="/home/kim/storage/workspace/csle/emulation-system/minigames/network_intrusion/ctf/001/level_2/agent_cache.zip", num_bins=100)
    #plot_freq_dist(d1=d_1,d2=d_2, num_bins=100)
    #path = "/home/kim/csle/emulation-system/minigames/network_intrusion/ctf/001/level_6/merged.zip"
    path = "/Users/kimham/workspace/csle/simulation-system/minigames/network_intrusion/ctf/gym-csle-ctf/examples/difficulty_level_6/plots/merged.zip"
    d_1, d_factors, bin_edges, costs_factors = plotting_action_costs.read_action_costs(
        zip_file=path,
        num_bins=100, factors=[2, 3, 4])
    print("loaded the data")
    # plot_freq_dist(d1=d_1, d2=d_factors, num_bins=100, labels=[r"$|\mathcal{N}|=25$", r"$|\mathcal{N}|=50$", r"$|\mathcal{N}|=75$", r"$|\mathcal{N}|=100$"],
    # title=r"Action execution times (costs)", xlabel=r"Time Cost (s)", colors=colors,
    # filename="action_cost_dist_plot", bin_edges=bin_edges, data=costs_factors)

    # plot_freq_dist_w_boxes(d1=d_1, d2=d_factors, num_bins=100,
    #                labels=[r"$|\mathcal{N}|=25$", r"$|\mathcal{N}|=50$", r"$|\mathcal{N}|=75$", r"$|\mathcal{N}|=100$"],
    #                title=r"Action execution times (costs)", xlabel=r"Time Cost (s)", colors=colors,
    #                filename="action_cost_dist_plot_25", bin_edges=bin_edges, data=costs_factors)

    # plot_freq_dist_w_boxes_all(d1=d_1, d2=d_factors, num_bins=100,
    #                        labels=[r"$|\mathcal{N}|=25$", r"$|\mathcal{N}|=50$", r"$|\mathcal{N}|=75$",
    #                                r"$|\mathcal{N}|=100$"],
    #                        title=r"Action execution times (costs)", xlabel=r"Time Cost (s)", colors=colors,
    #                        filename="action_cost_dist_plot_all_boxes", bin_edges=bin_edges, data=costs_factors,
    #                        ncols=4, figsize=(11, 2.5))

    plotting_action_costs.plot_freq_dist_w_boxes_all_2_rows(d1=d_1, d2=d_factors, num_bins=100,
                                                            labels=[r"$|\mathcal{N}|=25$", r"$|\mathcal{N}|=50$", r"$|\mathcal{N}|=75$",
                                       r"$|\mathcal{N}|=100$"],
                                                            title=r"Action execution times (costs)", xlabel=r"Time Cost (s)", colors=colors,
                                                            filename="action_cost_dist_plot_all_boxes_2_rows", bin_edges=bin_edges,
                                                            data=costs_factors,
                                                            ncols=2, figsize=(8, 5))

    #
    # colors = ["r"]

    # total_alerts, total_priority = read_action_alerts(
    #     zip_file="/home/kim/csle/emulation-system/minigames/network_intrusion/ctf/001/level_6/merged.zip",
    #     num_bins=250)

    #print(max(digitized_total))
    # plot_freq_dist(d1=None, d2=None,
    #                labels=[r"test"],title=r"Intrusion detection alerts per action", num_bins=30,
    #                colors=colors, xlabel=r"Number of triggered alerts",
    #                filename="action_alerts_dist_plot", data=total_alerts, bin_edges = None)

    #colors=["#599ad3"]
    # plot_freq_dist(d1=None, d2=None,
    #                labels=[r"test"], title=r"Intrusion detection alerts total priority $\sum_a p(a)$ per action", num_bins=30,
    #                colors=colors, xlabel=r"Total priority of triggered alerts",
    #                filename="action_alerts_priority_dist_plot", data=total_priority, bin_edges=None)

    # colors = ["#599ad3"]
    # cm = plt.cm.get_cmap('OrRd_r')
    # #colors = plt.cm.OrRd_r(np.linspace(0.3, 1, 4))[-4:]
    # colors = plt.cm.OrRd_r(np.linspace(0.3, 1, 10))
    #
    # plot_freq_dist_w_boxes_all_alerts(d1=None, d2=None, num_bins=30,
    #                            labels=[r"$|\mathcal{N}|=25$", r"$|\mathcal{N}|=50$", r"$|\mathcal{N}|=75$",
    #                                    r"$|\mathcal{N}|=100$"],
    #                            title=r"Intrusion detection alerts per action", xlabel=r"Number of triggered alerts",
    #                            colors=colors,
    #                            filename="action_alerts_dist_plot_all_boxes", bin_edges=None, data=total_alerts,
    #                                   data2=total_priority, title2="Alerts priority $\sum_a p(a)$ per action",
    #                                   xlabel2="Total priority of triggered alerts")
    # plot_profiling(d1=None, d2=None, num_bins=30,
    #                                   labels=[r"$|\mathcal{N}|=25$", r"$|\mathcal{N}|=50$", r"$|\mathcal{N}|=75$",
    #                                           r"$|\mathcal{N}|=100$"],
    #                                   title=r"Intrusion detection alerts per action",
    #                                   xlabel=r"Number of triggered alerts",
    #                                   colors=colors,
    #                                   filename="training_iter_profiling", bin_edges=None, data=total_alerts,
    #                                   data2=total_priority, title2="Alerts priority $\sum_a p(a)$ per action",
    #                                   xlabel2="Total priority of triggered alerts")

