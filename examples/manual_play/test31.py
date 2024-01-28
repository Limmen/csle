import numpy as np

if __name__ == '__main__':
    # ids = list(range(1, 66))
    ids = list(range(1, 41))
    activity_counts_list = []
    compromised_counts_list = []
    for id in ids:
        print(f"Loading id {id}")
        with open(f'/home/kim/activity_counts_{id}.npy', 'rb') as f:
            activity_counts = np.load(f)
            activity_counts_list.append(activity_counts)
        with open(f'/home/kim/compromised_counts_{id}.npy', 'rb') as f:
            compromised_counts = np.load(f)
            compromised_counts_list.append(compromised_counts)

    activity_counts = activity_counts_list[0]
    for i in range(1, len(activity_counts_list)):
        for j in range(activity_counts.shape[0]):
            for k in range(activity_counts.shape[1]):
                for l in range(activity_counts.shape[2]):
                    activity_counts[j][k][l] += activity_counts_list[i][j][k][l]

    compromised_counts = compromised_counts_list[0]
    for i in range(1, len(compromised_counts_list)):
        for j in range(compromised_counts.shape[0]):
            for k in range(compromised_counts.shape[1]):
                for l in range(compromised_counts.shape[2]):
                    for m in range(compromised_counts.shape[3]):
                        compromised_counts[j][k][l][m] += compromised_counts_list[i][j][k][l][m]

    activity_probabilities = np.zeros(activity_counts.shape)
    for j in range(activity_counts.shape[0]):
        for k in range(activity_counts.shape[1]):
            norm_constant = sum(activity_counts[j][k])
            for l in range(activity_counts.shape[2]):
                if norm_constant > 0:
                    activity_probabilities[j][k][l] += activity_counts[j][k][l]/norm_constant

    compromise_probabilities = np.zeros(compromised_counts.shape)
    for j in range(compromised_counts.shape[0]):
        for k in range(compromised_counts.shape[1]):
            for l in range(compromised_counts.shape[2]):
                norm_constant = sum(compromised_counts[j][k][l])
                for m in range(compromised_counts.shape[3]):
                    if norm_constant > 0:
                        compromise_probabilities[j][k][l][m] += compromised_counts[j][k][l][m]/norm_constant


    print(compromise_probabilities[7][0][0])


    # for host in range(activity_probabilities.shape[0]):
    #     for attacker_action in range(activity_probabilities.shape[1]):
    #         print(activity_probabilities[host][attacker_action])

    with open(f'/home/kim/activity_model.npy', 'wb') as f:
        np.save(f, np.array(activity_probabilities))
    with open(f'/home/kim/compromise_model.npy', 'wb') as f:
        np.save(f, np.array(compromise_probabilities))
