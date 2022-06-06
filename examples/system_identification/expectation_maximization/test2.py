from csle_common.metastore.metastore_facade import MetastoreFacade
import json
import io

if __name__ == '__main__':
    emulation_traces_ids = MetastoreFacade.list_emulation_traces_ids()
    traces = []
    for i, id_obj in enumerate(emulation_traces_ids):
        print(f"{i}/{len(emulation_traces_ids)}")
        tr = MetastoreFacade.get_emulation_trace(id=id_obj[0])
        traces.append(tr.to_dict())
    traces_dict = {
        "emulations" : traces
    }
    traces_str = json.dumps(traces_dict, indent=4, sort_keys=True)
    with io.open("/home/kim/new_traces_xw_6_june.json", 'w', encoding='utf-8') as f:
        f.write(traces_str)
