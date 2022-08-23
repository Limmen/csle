import json
import io
from csle_common.metastore.metastore_facade import MetastoreFacade

if __name__ == '__main__':
    training_result = MetastoreFacade.get_experiment_execution(id=62)
    json_str = training_result.to_json_str()
    with io.open("/home/kim/result_23_aug_noms.json", 'w', encoding='utf-8') as f:
        f.write(json_str)