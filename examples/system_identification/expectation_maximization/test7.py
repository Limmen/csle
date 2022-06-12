from csle_common.metastore.metastore_facade import MetastoreFacade
import json
import io

if __name__ == '__main__':
    exp_result = MetastoreFacade.get_experiment_execution(id=2062)
    exp_result_dict = exp_result.to_dict()
    exp_result_json_str = json.dumps(exp_result_dict, indent=4, sort_keys=True)
    with io.open("/home/kim/cnsm_22_12_june.json", 'w', encoding='utf-8') as f:
        f.write(exp_result_json_str)
