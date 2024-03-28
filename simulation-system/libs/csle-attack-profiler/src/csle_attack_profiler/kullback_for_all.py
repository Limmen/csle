#import silence_tensorflow.auto
import tensorflow as tf
import tensorflow_probability as tfp
from csle_common.dao.system_identification.emulation_statistics import EmulationStatistics
import tensorflow.keras as keras
import matplotlib.pyplot as plt
import numpy as np


def kullback_leibler_divergence(p, q):

    kl = tfp.distributions.kl_divergence(p, q)
    return kl

def kullback_leibler_divergence_for_all(p, q):

    pass


if __name__ == '__main__':
#    weather_A = tfp.distributions.Bernoulli(probs=0.3)
#    weather_B = tfp.distributions.Bernoulli(probs=0.5)
#    kl = kullback_leibler_divergence(weather_A, weather_B)
#    print(kl)
    
    statistics = EmulationStatistics.from_json_file("./../../statistics.json")

    test = len(statistics.conditionals_probs["no_intrusion"]["alerts_weighted_by_priority"])
    it = 0
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
            #print(f"X: {X}")
            #print(f"Y: {Y}")

            #print(len(X))
            #print(len(Y))
            # condition = no intrusion for the metric
            no_intrusion = statistics.conditionals_probs["no_intrusion"][metric]
            X_no_intrusion = list(map(lambda x: float(x), list(no_intrusion.keys())))
            Y_no_intrusion = list(map(lambda x: float(x), list(no_intrusion.values())))
            #print(len(X_no_intrusion))
            #print(len(Y_no_intrusion))
            it += 1

            if len(X) > 1:
                f1_0 = []
                f1_1 = []
                f1_values = list(set(X + X_no_intrusion))
                for val in f1_values:
                    if val in X:
                        f1_0.append(Y[X.index(val)])
                    else:
                        f1_0.append(0.0000001)
                    if val in X_no_intrusion:
                        f1_1.append(Y_no_intrusion[X_no_intrusion.index(val)])
                    else:
                        f1_1.append(0.0000001)
                f1_0_norm = tf.convert_to_tensor(f1_0) / tf.reduce_sum(f1_0)
                f1_1_norm = tf.convert_to_tensor(f1_1) / tf.reduce_sum(f1_1)
                f1_0_np = np.array(f1_0)
                f1_1_np = np.array(f1_1)
                kl_own = np.sum(f1_0_np * np.log(f1_0_np / f1_1_np))
                kl_list = f1_0_np * np.log(f1_0_np / f1_1_np)
                print(kl_own)

                p = tfp.distributions.Categorical(probs=f1_0)
                q = tfp.distributions.Categorical(probs=f1_1)
                kl = kullback_leibler_divergence(p, q)
                print(kl)
                plt.scatter(f1_values, f1_0, label=f'P({metric} | {attacker_action})', color='red', marker='o', s=10)
                plt.scatter(f1_values, f1_1, label=f'P({metric} | no intrusion)', color='blue', marker='s', s=10) 
                plt.xlabel('Value')
                plt.ylabel('Probability')
                plt.title(f'Probability distribution for metric {metric} given {attacker_action} and no intrusion')
                plt.legend()
                plt.grid(True)
                plt.xlim(1000,4000)
                plt.suptitle(f'Kullback-Leibler divergence: {kl_own}', fontweight='bold')
                plt.show()


            if it == 10:
                break
        break

