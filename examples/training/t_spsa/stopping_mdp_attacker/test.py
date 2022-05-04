import json
import io
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.training.multi_threshold_stopping_policy import MultiThresholdStoppingPolicy

if __name__ == '__main__':
    theta = 0.2
    sigmoid_theta = MultiThresholdStoppingPolicy.sigmoid(theta)
    inverse = MultiThresholdStoppingPolicy.inverse_sigmoid(sigmoid_theta)
    print(sigmoid_theta)
    print(inverse)
    # stat = MetastoreFacade.get_emulation_statistic(id=36)
    # json_str = json.dumps(stat.to_dict(), indent=4, sort_keys=True)
    # with io.open("/home/kim/stat_backup_4_may.json", 'w', encoding='utf-8') as f:
    #     f.write(json_str)