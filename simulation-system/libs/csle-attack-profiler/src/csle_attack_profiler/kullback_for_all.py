from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
import matplotlib.pyplot as plt
import numpy as np
import seaborn as seaborn



def kullback_leibler_divergence_for_counts(p, q):
    probs_p = p / np.sum(p)
    probs_q = q / np.sum(q)
    kl_div = np.sum(probs_p * np.log(probs_p / probs_q))
    return kl_div



if __name__ == '__main__':
    
    statistics = EmulationStatistics.from_json_file("./../../statistics.json")

    #test2 = len(statistics.conditionals_counts["no_intrusion"]["alerts_weighted_by_priority"])
    KLD_valuesPQ = []
    KLD_valuesQP = []
    metric_and_action = []
    metric_and_action_dict = {}
    data_points = []
    distributions = []
    metrics_temp = []


    for condition, metric_distributions in statistics.conditionals_probs.items():
        condition_parts = condition.split('_')
        if len(condition_parts) < 3: # Condition c P(o|c) per metric
            continue
        attacker_action = condition_parts[0]
        # If the attacker action is continue, we skip it
        if attacker_action == 'A:Continue':
            continue
        defender_action = condition_parts[1]
        if attacker_action not in metric_and_action_dict:
            metric_and_action_dict[attacker_action] = []
        for metric in metric_distributions.keys():
            X = list(map(lambda x: float(x), list(metric_distributions[metric].keys())))
            Y = list(map(lambda x: float(x), list(metric_distributions[metric].values())))
            # Out p(x)
            no_intrusion = statistics.conditionals_probs["no_intrusion"][metric]
            #no_intrusion = statistics.conditionals_counts["no_intrusion"][metric]
            X_no_intrusion = list(map(lambda x: float(x), list(no_intrusion.keys())))
            Y_no_intrusion = list(map(lambda x: float(x), list(no_intrusion.values())))
            if len(X) > 10:
                metric_and_action.append((metric, attacker_action))
                # q(x)
                q_dist = []
                # p(x)
                p_dist = []

                # KLD Backoff smoothing
                P = X
                Q = X_no_intrusion
                CP = len(P)
                CQ = len(Q)
                SU = list(set(X + X_no_intrusion))
                CU = len(SU)
                epsilon = 0.0000001
                SU_disjoint_P = len(list(set(SU) - set(P))) 
                SU_disjoint_Q = len(list(set(SU) - set(Q)))

                pc = (sum(Y) + epsilon*(SU_disjoint_P) - 1) / CP
                qc = (sum(Y_no_intrusion) + epsilon*(SU_disjoint_Q) - 1) / CQ
                p_prime = []
                q_prime = []


                for val in SU:
                    if val in P:
                        p_prime.append((Y[X.index(val)] - pc))
                    else:
                        p_prime.append(epsilon)
                    if val in X_no_intrusion:
                        q_prime.append((Y_no_intrusion[X_no_intrusion.index(val)] - qc))
                    else:
                        q_prime.append(epsilon) 

                p_prime_np = np.array(p_prime) / np.sum(p_prime)
                q_prime_np = np.array(q_prime) / np.sum(q_prime)

                KLD_PQ = np.around(np.sum(p_prime_np * np.log(p_prime_np / q_prime_np)), 4)
                KLD_QP = np.around(np.sum(q_prime_np * np.log(q_prime_np / p_prime_np)), 4)

                KLD_valuesPQ.append(KLD_PQ)
                KLD_valuesQP.append(KLD_QP)
                data_points.append(len(X))
                distributions.append((SU, q_prime, p_prime))




    metric_kl_valuesPQ = {}
    metric_kl_valuesQP = {}
    for i in range(len(KLD_valuesPQ)):
        metric = metric_and_action[i][0]
        action = metric_and_action[i][1]
        if action == 'A:Continue':
            continue
        if metric not in metric_kl_valuesPQ:
            metric_kl_valuesPQ[metric] = []
            metric_kl_valuesQP[metric] = []
            metric_kl_valuesPQ[metric].append(KLD_valuesPQ[i])
            metric_kl_valuesQP[metric].append(KLD_valuesQP[i])
        else: 
            metric_kl_valuesPQ[metric].append(KLD_valuesPQ[i])
            metric_kl_valuesQP[metric].append(KLD_valuesQP[i])

    # Extract the values from the dictionary
    kl_valuesPQ = [metric_kl_valuesPQ[metric] for metric in metric_kl_valuesPQ.keys()]
    kl_valuesQP = [metric_kl_valuesQP[metric] for metric in metric_kl_valuesQP.keys()]

    

    median = np.median(np.array(KLD_valuesPQ))
    percentile_75 = np.percentile(np.array(KLD_valuesPQ), 75)
    percentile_90 = np.percentile(np.array(KLD_valuesPQ), 90)
    median_QP = np.median(np.array(KLD_valuesQP))
    percentile_75_QP = np.percentile(np.array(KLD_valuesQP), 75)
    percentile_90_QP = np.percentile(np.array(KLD_valuesQP), 90)
    """
    print(f'KLD(P||Q) median: {median}')
    print(f'KLD(Q||P) median: {median_QP}')
    print(f'KLD(P||Q) P90: {percentile_90}')
    print(f'KLD(P||Q) P75: {percentile_75}')
    print(f'KLD(Q||P) P90: {percentile_90_QP}')
    print(f'KLD(Q||P) P75: {percentile_75_QP}')
    """

    # Plot the distributions when the KLD is above the 90 percentile
    dists_to_plot = []
    metric_and_action_to_plot = []
    KLD_values_to_plot = []
    #for i in range(len(KLD_valuesPQ)):
    for i in range(len(metric_kl_valuesPQ)):
        metric = metric_and_action[i][0]
        action = metric_and_action[i][1]
        percentile_90_metric = np.percentile(np.array(metric_kl_valuesPQ[metric]), 90)
        percentile_90_metric_QP = np.percentile(np.array(metric_kl_valuesQP[metric]), 90)
        percentile_75_metric = np.percentile(np.array(metric_kl_valuesPQ[metric]), 75)
        percentile_75_metric_QP = np.percentile(np.array(metric_kl_valuesQP[metric]), 75)
        median = np.median(np.array(metric_kl_valuesPQ[metric]))
        median_QP = np.median(np.array(metric_kl_valuesQP[metric]))
        """ 
        print(f'KLD(P||Q) median for {metric} : {median}')
        print(f'KLD(P||Q) P90 for {metric} : {percentile_90_metric}')
        print(f'KLD(P||Q) P75 for {metric} : {percentile_75_metric}')
        print(f'KLD(Q||P) median for {metric} : {median_QP}')
        print(f'KLD(Q||P) P90 for {metric} : {percentile_90_metric_QP}')
        print(f'KLD(Q||P) P75 for {metric} : {percentile_75_metric_QP}')
        """

        if (KLD_valuesPQ[i] < percentile_90_metric and KLD_valuesQP[i] < percentile_90_metric_QP) and (KLD_valuesPQ[i] > percentile_75_metric and KLD_valuesQP[i] > percentile_75_metric_QP):# and (KLD_valuesPQ[i] > median and KLD_valuesQP[i] > median_QP): 
            KLD_values_to_plot.append((KLD_valuesPQ[i], KLD_valuesQP[i]))
            dists_to_plot.append(distributions[i])
            metric_and_action_to_plot.append(metric_and_action[i])
    
    """
    plt.figure(figsize=(12, 6))
    seaborn.boxplot(data=kl_valuesPQ, orient='v', palette='Set2', showmeans=True)
    plt.xticks(rotation=45, ha='right', ticks=range(len(metric_kl_valuesPQ)), labels=list(metric_kl_valuesPQ.keys()))
    plt.ylabel('Kullback-Leibler divergence')
    #plt.title('Boxplot of Kullback-Leibler divergence for all metrics KLD(P||Q)')
    plt.tight_layout()
    plt.show()
        
    plt.figure(figsize=(12, 6))
    seaborn.boxplot(data=kl_valuesQP, orient='v', palette='Set2', showmeans=True)
    plt.xticks(rotation=45, ha='right', ticks=range(len(metric_kl_valuesQP)), labels=list(metric_kl_valuesQP.keys()))
    plt.ylabel('Kullback-Leibler divergence')
    #plt.title('Boxplot of Kullback-Leibler divergence for all metrics KLD(Q||P)')
    plt.tight_layout()
    plt.show()
    
    it = 0
    for dist, (metric, attacker_action), (KD_PQ, KD_QP) in zip(dists_to_plot, metric_and_action_to_plot, KLD_values_to_plot):
        # Unpack distribution values
        dist_values, q_dist, p_dist = dist
        percentile_90_metric = np.percentile(np.array(metric_kl_valuesPQ[metric]), 90)
        percentile_90_metric_QP = np.percentile(np.array(metric_kl_valuesQP[metric]), 90)
        
        # Plot the distributions
        plt.figure(figsize=(12, 6))
        seaborn.scatterplot(x=dist_values, y=q_dist, label=f'P({metric} | {attacker_action})', color='red', marker='o', s=8)
        seaborn.scatterplot(x=dist_values, y=p_dist, label=f'Q({metric} | no intrusion)', color='blue', marker='o', s=8)
        plt.xlabel('Value')
        plt.ylabel('Probability')
        plt.title(f'Kullback-Leibler divergence: KLD(P||Q)={KD_PQ},  KLD(Q||P)={KD_QP}')
        plt.legend()
        plt.grid(True)


        q1, q3 = np.percentile(np.concatenate([q_dist, p_dist]), [25, 75])
        iqr = q3 - q1 
        lower_limit = q1 - 1.1 * iqr 
        upper_limit = q3 + 1.9 * iqr
        plt.ylim([0, upper_limit])

        q1, q3 = np.percentile(dist_values, [25, 75])
        iqr = q3 - q1
        lower_limit = q1 - 1.5 * iqr
        upper_limit = q3 + 1.5 * iqr
        data = np.array(dist_values)
        filtered_data = data[(data > lower_limit) & (data < upper_limit)]
        x_min = np.min(filtered_data)
        x_max = np.max(filtered_data)
        #Boundaries of the x-axis
        plt.xlim(x_min, x_max)
        #plt.xlim(min_x - padding_amount, p99 + padding_amount)
        #plt.savefig(f'./plots/P90{attacker_action}{it}.png', dpi = 500)
        it += 1
        #plt.close()
        plt.show()
    """
