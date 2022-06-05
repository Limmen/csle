from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.dao.emulation_config.emulation_trace import EmulationTrace
import json
import io

if __name__ == '__main__':
    with io.open("/home/kim/new_traces_xw_5_june.json", 'r', encoding='utf-8') as f:
        json_str = f.read()
        dict = json.loads(json_str)
        traces_dicts = dict["emulations"]
        traces_dtos = []
        for i, tr_dict in enumerate(traces_dicts):
            print(f"Parsing trace {i}/{len(traces_dicts)-1}")
            trace = EmulationTrace.from_dict(tr_dict)
            MetastoreFacade.save_emulation_trace(trace)

