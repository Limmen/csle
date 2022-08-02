import json
import io
from csle_common.logging.log import Logger
import csle_common.constants.constants as constants
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.util.export_util import ExportUtil

if __name__ == '__main__':
    output_dir = "/home/kim/traces_2_aug_22"
    zip_file_output="/home/kim/traces_2_aug_22.zip"
    traces = []
    ids = list(range(1901, 2001))
    num_attributes_per_time_step = -1
    schema = None
    for i, id_obj in enumerate(ids):
        print(f"Reading trace {i}/{len(ids)} from the metastore")
        tr = MetastoreFacade.get_emulation_trace(id=id_obj[0])
        traces.append(tr.to_dict())
        if num_attributes_per_time_step == -1:
            num_attributes_per_time_step = tr.num_attributes_per_time_step()
        if schema is None:
            schema = json.dumps(tr.get_schema().to_dict(), indent=4, sort_keys=True)
    traces_dict = {
        constants.METADATA_STORE.EMULATIONS_PROPERTY : traces
    }
    traces_str = json.dumps(traces_dict, indent=4, sort_keys=True)
    with io.open(f"/home/kim/20.json", 'w', encoding='utf-8') as f:
        f.write(traces_str)

    file_format = "json"
    num_traces = 2000
    num_traces_per_file = 100
    with io.open(f"/home/kim/{constants.DATASETS.METADATA_FILE_NAME}", 'w',
                 encoding='utf-8') as f:
        metadata_str = f"{constants.DATASETS.FILE_FORMAT_PROPERTY}{constants.COMMANDS.COLON_DELIM}{file_format}\n" \
                       f"{constants.DATASETS.NUM_TRACES_PROPERTY}{constants.COMMANDS.COLON_DELIM}{num_traces}\n" \
                       f"{constants.DATASETS.NUM_ATTRIBUTES_PER_TIME_STEP_PROPERTY}{constants.COMMANDS.COLON_DELIM}" \
                       f"{num_attributes_per_time_step}\n" \
                       f"{constants.DATASETS.SCHEMA_PROPERTY}{constants.COMMANDS.COLON_DELIM}{schema}\n" \
                       f"{constants.DATASETS.NUM_TRACES_PER_FILE_PROPERTY}{constants.COMMANDS.COLON_DELIM}" \
                       f"{num_traces_per_file}"
        f.write(metadata_str)
    # ExportUtil.zipdir(dir_path=output_dir, zip_file_path=zip_file_output)