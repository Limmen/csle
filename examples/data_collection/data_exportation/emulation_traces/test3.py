import json
import io
from csle_common.logging.log import Logger
import csle_common.constants.constants as constants
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.util.export_util import ExportUtil
from csle_common.dao.emulation_config.emulation_trace import EmulationTrace

if __name__ == '__main__':
    input_file = "/var/csle/datasets/traces_dataset_2_aug_22_json/1.json"
    with io.open(input_file, 'r', encoding='utf-8') as f:
        print("reading json")
        json_str = f.read()
        print("json read")
        d = json.loads(json_str)
        print("json loaded")
        traces_dicts = d["traces"][0:3]
        traces_dtos = []
        # for i, tr_dict in enumerate(traces_dicts):
        #     print(f"Parsing trace {i}/{len(traces_dicts)-1}")
        #     trace = EmulationTrace.from_dict(tr_dict)
        #     traces_dtos.append(trace)
        traces_dict = {
            constants.METADATA_STORE.TRACES_PROPERTY : traces_dicts
        }
        traces_str = json.dumps(traces_dict, indent=4, sort_keys=True)
        with io.open(f"/home/kim/test.json", 'w', encoding='utf-8') as f:
            f.write(traces_str)