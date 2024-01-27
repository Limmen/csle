import numpy as np

if __name__ == '__main__':
    ids = list(range(1, 65))
    exploit_success_list = []
    exploit_counts_list = []
    exploit_root_list = []
    exploit_user_list = []
    exploit_type_counts_list = []
    for id in ids:
        print(f"Loading id {id}")
        with open(f'/home/kim/exploit_success_{id}.npy', 'rb') as f:
            exploit_success = np.load(f)
            exploit_success_list.append(exploit_success)
        with open(f'/home/kim/exploit_counts_{id}.npy', 'rb') as f:
            exploit_counts = np.load(f)
            exploit_counts_list.append(exploit_counts)
        with open(f'/home/kim/exploit_root_{id}.npy', 'rb') as f:
            exploit_root = np.load(f)
            exploit_root_list.append(exploit_root)
        with open(f'/home/kim/exploit_user_{id}.npy', 'rb') as f:
            exploit_user = np.load(f)
            exploit_user_list.append(exploit_user)
        with open(f'/home/kim/exploit_type_counts_{id}.npy', 'rb') as f:
            exploit_type_counts = np.load(f)
            exploit_type_counts_list.append(exploit_type_counts)

    exploit_counts = exploit_counts_list[0]
    exploit_success = exploit_success_list[0]
    for i in range(1, len(exploit_counts_list)):
        for j in range(exploit_counts.shape[0]):
            for k in range(exploit_counts.shape[1]):
                exploit_counts[j][k] += exploit_counts_list[i][j][k]
                exploit_success[j][k] += exploit_success_list[i][j][k]

    exploit_root = exploit_root_list[0]
    exploit_user = exploit_user_list[0]
    exploit_type_counts = exploit_type_counts_list[0]
    for i in range(1, len(exploit_root_list)):
        for j in range(exploit_root.shape[0]):
            for k in range(exploit_root.shape[1]):
                exploit_root[j][k] += exploit_root_list[i][j][k]
                exploit_user[j][k] += exploit_user_list[i][j][k]
                exploit_type_counts[j][k] += exploit_type_counts_list[i][j][k]

    exploit_success_probabilities = np.zeros(exploit_counts.shape)
    for i in range(exploit_counts.shape[0]):
        for j in range(exploit_counts.shape[1]):
            if exploit_counts[i][j] > 0:
                exploit_success_probabilities[i][j] = exploit_success[i][j] / exploit_counts[i][j]

    exploit_root_probabilities = np.zeros(exploit_root.shape)
    exploit_user_probabilities = np.zeros(exploit_user.shape)
    for j in range(exploit_root.shape[0]):
        for k in range(exploit_root.shape[1]):
            if exploit_type_counts[j][k] > 0:
                exploit_root_probabilities[j][k] = exploit_root[j][k] / exploit_type_counts[j][k]
                exploit_user_probabilities[j][k] = exploit_user[j][k] / exploit_type_counts[j][k]

    for host in range(exploit_success_probabilities.shape[0]):
        for decoy in range(exploit_success_probabilities.shape[1]):
            print(exploit_success_probabilities[host][decoy])

    with open(f'/home/kim/exploit_model.npy', 'wb') as f:
        np.save(f, np.array(exploit_success_probabilities))
    with open(f'/home/kim/exploit_root_model.npy', 'wb') as f:
        np.save(f, np.array(exploit_root_probabilities))
    with open(f'/home/kim/exploit_user_model.npy', 'wb') as f:
        np.save(f, np.array(exploit_user_probabilities))
