import io
import json
import numpy as np

if __name__ == '__main__':
    # paths = [
    #     "/Users/kim/Dropbox/pomcp/pomcp_05s_seed_148518.json",
    #     "/Users/kim/Dropbox/pomcp/pomcp_05s_seed_333410.json",
    #     "/Users/kim/Dropbox/pomcp/pomcp_05s_seed_711123.json",
    #     "/Users/kim/Dropbox/pomcp/pomcp_05s_seed_8887120.json"
    # ]
    # paths = [
    #     "/Users/kim/Dropbox/pomcp/pomcp_025s_seed_1118162.json",
    #     "/Users/kim/Dropbox/pomcp/pomcp_025s_seed_338193.json"
    # ]
    # paths = [
    #     "/Users/kim/Dropbox/pomcp/pomcp_1s_seed_222515.json",
    #     "/Users/kim/Dropbox/pomcp/pomcp_1s_seed_891823.json"
    # ]
    # paths = [
    #     "/Users/kim/Dropbox/pomcp/pomcp_01s_seed_222515.json",
    #     "/Users/kim/Dropbox/pomcp/pomcp_01s_seed_33459871.json",
    #     "/Users/kim/Dropbox/pomcp/pomcp_01s_seed_6651220.json"
    # ]
    # paths = [
    #     "/Users/kim/Dropbox/pomcp/pomcp_5s_seed_107293.json",
    #     "/Users/kim/Dropbox/pomcp/pomcp_5s_seed_891823.json"
    # ]
    # paths = [
    #     "/Users/kim/Dropbox/pomcp/pomcp_15s_seed_678192.json"
    # ]
    # paths = [
    #     "/Users/kim/Dropbox/pomcp/pomcp_30s_v2_seed_111120.json",
    #     "/Users/kim/Dropbox/pomcp/pomcp_30s_v2_seed_2231300.json",
    #     "/Users/kim/Dropbox/pomcp/pomcp_30s_v2_seed_3341951.json",
    #     "/Users/kim/Dropbox/pomcp/pomcp_30s_v2_seed_454545.json",
    #     "/Users/kim/Dropbox/pomcp/pomcp_30s_v2_seed_55561.json",
    #     "/Users/kim/Dropbox/pomcp/pomcp_30s_v2_seed_661700.json",
    #     "/Users/kim/Dropbox/pomcp/pomcp_30s_v2_seed_789871.json"
    # ]
    # paths = [
    #     "/Users/kim/Dropbox/pomcp/pomcp_10s_seed_55612.json"
    # ]
    paths = [
        "/Users/kim/Dropbox/pomcp/pomcp_005s_T_100_seed_3303919.json",
        "/Users/kim/Dropbox/pomcp/pomcp_005s_T_100_seed_33459871.json"
    ]
    data_dicts = []
    for path in paths:
        with io.open(path, 'r') as f:
            json_str = f.read()
            data_dicts.append(json.loads(json_str))

    returns_list = []
    for data_dict in data_dicts:
        returns_list.append(data_dict["returns"])

    means = []
    for r_list in returns_list:
        means.append(np.mean(r_list))

    mean_mean = np.mean(means)
    mean_std = np.std(means)
    # mean_std = np.std(returns_list[0])
    print(mean_mean)
    print(mean_mean + mean_std)
    print(mean_mean - mean_std)