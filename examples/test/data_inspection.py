import numpy as np
from csle_common.metastore.metastore_facade import MetastoreFacade
import csle_common.constants.constants as constants

if __name__ == '__main__':
    emulation_statistic = MetastoreFacade.get_emulation_statistic(id=13)
    no_intrusion = emulation_statistic.conditionals_counts[constants.SYSTEM_IDENTIFICATION.NO_INTRUSION_CONDITIONAL]["alerts_weighted_by_priority"]
    intrusion = emulation_statistic.conditionals_counts[constants.SYSTEM_IDENTIFICATION.INTRUSION_CONDITIONAL]["alerts_weighted_by_priority"]
    intrusion_counts = [0,0,0]
    no_intrusion_counts = [0,0,0]
    for k,v in intrusion.items():
        if k < 4000:
            intrusion_counts[0] = intrusion_counts[0] + 1
        elif k >= 4000 and k <10000:
            intrusion_counts[1] = intrusion_counts[1] + 1
        else:
            intrusion_counts[2] = intrusion_counts[2] + 1


    for k,v in no_intrusion.items():
        if k < 4000:
            no_intrusion_counts[0] = no_intrusion_counts[0] + 1
        elif k >= 4000 and k <10000:
            no_intrusion_counts[1] = no_intrusion_counts[1] + 1
        else:
            no_intrusion_counts[2] = no_intrusion_counts[2] + 1

    print(intrusion_counts)
    print(no_intrusion_counts)

    intrusion_probs = np.array(intrusion_counts)*(1/sum(intrusion_counts))
    no_intrusion_probs = np.array(no_intrusion_counts)*(1/sum(no_intrusion_counts))

    print(intrusion_probs)
    print(no_intrusion_probs)