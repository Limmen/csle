import numpy as np

from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.emulation_config.emulation_trace import EmulationTrace
from csle_common.dao.system_identification.gaussian_mixture_system_model import GaussianMixtureSystemModel
import json
import io

if __name__ == '__main__':
    model = MetastoreFacade.get_gaussian_mixture_system_model_config(id=10)
    intrusion_dist = np.zeros(15000)
    no_intrusion_dist = np.zeros(15000)
    zero_dist = list(range(-10000, 1))
    for metric_conds in model.conditional_metric_distributions:
        for metric_cond in metric_conds:
            if metric_cond.conditional_name == "intrusion" \
                    and metric_cond.metric_name == "alerts_weighted_by_priority":
                intrusion_dist[0] = sum(metric_cond.generate_distributions_for_samples(samples=zero_dist))
            if metric_cond.conditional_name == "no_intrusion" \
                    and metric_cond.metric_name == "alerts_weighted_by_priority":
                no_intrusion_dist[0] = sum(metric_cond.generate_distributions_for_samples(samples=zero_dist))
    sample_space = list(range(1, 15000))
    for metric_conds in model.conditional_metric_distributions:
        for metric_cond in metric_conds:
            if metric_cond.conditional_name == "intrusion" \
                    and metric_cond.metric_name == "alerts_weighted_by_priority":
                intrusion_dist[1:] = metric_cond.generate_distributions_for_samples(samples=sample_space)
            if metric_cond.conditional_name == "no_intrusion" \
                    and metric_cond.metric_name == "alerts_weighted_by_priority":
                no_intrusion_dist[1:] = metric_cond.generate_distributions_for_samples(samples=sample_space)
    intrusion_dist = list(np.array(intrusion_dist)*(1/sum(intrusion_dist)))
    no_intrusion_dist = list(np.array(no_intrusion_dist)*(1/sum(no_intrusion_dist)))
    print(sum(intrusion_dist))
    print(sum(no_intrusion_dist))

