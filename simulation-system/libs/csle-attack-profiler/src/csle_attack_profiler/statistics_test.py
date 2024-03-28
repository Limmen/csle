from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
 
if __name__ == '__main__':
    statistics = EmulationStatistics.from_json_file("./../../statistics.json")
    for condition, metric_distributions in statistics.conditionals_probs.items():
        condition_parts = condition.split('_')
        if len(condition_parts) < 3: # Condition c P(o|c) per metric
            continue
        attacker_action = condition_parts[0]
        defender_action = condition_parts[1]
        for metric in metric_distributions.keys():
            X = list(map(lambda x: float(x), list(metric_distributions[metric].keys())))
            Y = list(map(lambda x: float(x), list(metric_distributions[metric].values())))
            print(f"P({metric} | {attacker_action})")
            print(f"X: {X}")
            print(f"Y: {Y}")
 
    for metric, distribution in statistics.conditionals_probs["no_intrusion"].items():
        X = list(map(lambda x: float(x), list(distribution.keys())))
        Y = list(map(lambda x: float(x), list(distribution.values())))
        print(f"P({metric} | no intrusion)")
        print(f"X: {X}")
        print(f"Y: {Y}")