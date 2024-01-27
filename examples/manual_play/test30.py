import numpy as np

if __name__ == '__main__':
    ids = list(range(1, 81))
    scan_counts_list = []
    scan_success_list = []
    hostscan_success_list = []
    hostscan_counts_list = []
    exploit_success_list = []
    exploit_counts_list = []
    exploit_root_list = []
    exploit_user_list = []
    exploit_type_counts_list = []
    privilege_escalation_success_list = []
    privilege_escalation_counts_list = []
    impact_success_list = []
    impact_counts_list = []
    for id in ids:
        print(f"Loading id {id}")
        with open(f'/home/kim/scan_counts_{id}.npy', 'rb') as f:
            scan_counts = np.load(f)
            scan_counts_list.append(scan_counts)
        with open(f'/home/kim/scan_success_{id}.npy', 'rb') as f:
            scan_success = np.load(f)
            scan_success_list.append(scan_success)
        with open(f'/home/kim/hostscan_success_{id}.npy', 'rb') as f:
            hostscan_success = np.load(f)
            hostscan_success_list.append(hostscan_success)
        with open(f'/home/kim/hostscan_counts_{id}.npy', 'rb') as f:
            hostscan_counts = np.load(f)
            hostscan_counts_list.append(hostscan_counts)
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
        with open(f'/home/kim/privilege_escalation_success_{id}.npy', 'rb') as f:
            privilege_escalation_success = np.load(f)
            privilege_escalation_success_list.append(privilege_escalation_success)
        with open(f'/home/kim/privilege_escalation_counts_{id}.npy', 'rb') as f:
            privilege_escalation_counts = np.load(f)
            privilege_escalation_counts_list.append(privilege_escalation_counts)
        with open(f'/home/kim/impact_success_{id}.npy', 'rb') as f:
            impact_success = np.load(f)
            impact_success_list.append(impact_success)
        with open(f'/home/kim/impact_counts_{id}.npy', 'rb') as f:
            impact_counts = np.load(f)
            impact_counts_list.append(impact_counts)

    scan_counts = scan_counts_list[0]
    scan_success = scan_success_list[0]
    for i in range(1, len(scan_counts_list)):
        for j in range(scan_counts.shape[0]):
            for k in range(scan_counts.shape[1]):
                scan_counts[j][k] += scan_counts_list[i][j][k]
                scan_success[j][k] += scan_success_list[i][j][k]

    hostscan_counts = hostscan_counts_list[0]
    hostscan_success = hostscan_success_list[0]
    for i in range(1, len(hostscan_counts_list)):
        for j in range(hostscan_counts.shape[0]):
            for k in range(hostscan_counts.shape[1]):
                hostscan_counts[j][k] += hostscan_counts_list[i][j][k]
                hostscan_success[j][k] += hostscan_success_list[i][j][k]

    exploit_counts = exploit_counts_list[0]
    exploit_success = exploit_success_list[0]
    for i in range(1, len(exploit_counts_list)):
        for j in range(exploit_counts.shape[0]):
            for k in range(exploit_counts.shape[1]):
                for l in range(exploit_counts.shape[2]):
                    exploit_counts[j][k][l] += exploit_counts_list[i][j][k][l]
                    exploit_success[j][k][l] += exploit_success_list[i][j][k][l]

    exploit_root = exploit_root_list[0]
    exploit_user = exploit_user_list[0]
    exploit_type_counts = exploit_type_counts_list[0]
    for i in range(1, len(exploit_root_list)):
        for j in range(exploit_root.shape[0]):
            for k in range(exploit_root.shape[1]):
                for l in range(exploit_root.shape[2]):
                    exploit_root[j][k][l] += exploit_root_list[i][j][k][l]
                    exploit_user[j][k][l] += exploit_user_list[i][j][k][l]
                    exploit_type_counts[j][k][l] += exploit_type_counts_list[i][j][k][l]

    privilege_escalation_counts = privilege_escalation_counts_list[0]
    privilege_escalation_success = privilege_escalation_success_list[0]
    for i in range(1, len(privilege_escalation_counts_list)):
        for j in range(privilege_escalation_counts.shape[0]):
            for k in range(privilege_escalation_counts.shape[1]):
                privilege_escalation_counts[j][k] += privilege_escalation_counts_list[i][j][k]
                privilege_escalation_success[j][k] += privilege_escalation_success_list[i][j][k]

    impact_counts = impact_counts_list[0]
    impact_success = impact_success_list[0]
    for i in range(1, len(impact_counts_list)):
        for j in range(impact_counts.shape[0]):
            for k in range(impact_counts.shape[1]):
                impact_counts[j][k] += impact_counts_list[i][j][k]
                impact_success[j][k] += impact_success_list[i][j][k]

    scan_success_probabilities = np.zeros(scan_counts.shape)
    for j in range(scan_counts.shape[0]):
        for k in range(scan_counts.shape[1]):
            if scan_counts[j][k] > 0:
                scan_success_probabilities[j][k] = scan_success[j][k] / scan_counts[j][k]

    hostscan_success_probabilities = np.zeros(hostscan_success.shape)
    for j in range(hostscan_success.shape[0]):
        for k in range(hostscan_success.shape[1]):
            if hostscan_counts[j][k] > 0:
                hostscan_success_probabilities[j][k] = hostscan_success[j][k] / hostscan_counts[j][k]

    exploit_success_probabilities = np.zeros(exploit_counts.shape)
    for i in range(exploit_counts.shape[0]):
        for j in range(exploit_counts.shape[1]):
            for k in range(exploit_counts.shape[2]):
                if exploit_counts[i][j][k] > 0:
                    exploit_success_probabilities[i][j][k] = exploit_success[i][j][k] / exploit_counts[i][j][k]

    exploit_root_probabilities = np.zeros(exploit_root.shape)
    exploit_user_probabilities = np.zeros(exploit_user.shape)
    for j in range(exploit_root.shape[0]):
        for k in range(exploit_root.shape[1]):
            for l in range(exploit_root.shape[2]):
                if exploit_type_counts[j][k][l] > 0:
                    exploit_root_probabilities[j][k][l] = exploit_root[j][k][l] / exploit_type_counts[j][k][l]
                    exploit_user_probabilities[j][k][l] = exploit_user[j][k][l] / exploit_type_counts[j][k][l]

    privilege_escalation_success_probabilities = np.zeros(privilege_escalation_counts.shape)
    for j in range(privilege_escalation_counts.shape[0]):
        for k in range(privilege_escalation_counts.shape[1]):
            if privilege_escalation_counts[j][k] > 0:
                privilege_escalation_success_probabilities[j][k] = \
                    privilege_escalation_success[j][k] / privilege_escalation_counts[j][k]

    impact_success_probabilities = np.zeros(impact_counts.shape)
    for j in range(impact_counts.shape[0]):
        for k in range(impact_counts.shape[1]):
            if impact_counts[j][k] > 0:
                impact_success_probabilities[j][k] = impact_success[j][k] / impact_counts[j][k]

    with open(f'/home/kim/scan_model.npy', 'wb') as f:
        np.save(f, np.array(scan_success_probabilities))
    with open(f'/home/kim/hostscan_model.npy', 'wb') as f:
        np.save(f, np.array(hostscan_success_probabilities))
    with open(f'/home/kim/exploit_model.npy', 'wb') as f:
        np.save(f, np.array(exploit_success_probabilities))
    with open(f'/home/kim/exploit_root_model.npy', 'wb') as f:
        np.save(f, np.array(exploit_root_probabilities))
    with open(f'/home/kim/exploit_user_model.npy', 'wb') as f:
        np.save(f, np.array(exploit_user_probabilities))
    with open(f'/home/kim/privilege_escalation_model.npy', 'wb') as f:
        np.save(f, np.array(privilege_escalation_success_probabilities))
    with open(f'/home/kim/impact_model.npy', 'wb') as f:
        np.save(f, np.array(impact_success_probabilities))
