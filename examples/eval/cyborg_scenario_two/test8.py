import io
import json
import numpy as np

if __name__ == '__main__':
    paths = [
        "/home/kim/Dropbox/pomcp/pomcp_30s_T_30_seed_304908.json",
        "/home/kim/Dropbox/pomcp/pomcp_30s_T_30_seed_4556123.json",
        "/home/kim/Dropbox/pomcp/pomcp_30s_T_30_seed_6671820.json"
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